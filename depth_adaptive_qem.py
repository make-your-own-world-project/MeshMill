"""GPU-guided adaptive physical probes followed by boundary-preserving Fast QEM."""

from __future__ import annotations

import importlib.util
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import fast_simplification
import numpy as np

_cuda_dll_directories = []
if os.name == "nt":
    frozen_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    bundled_root = frozen_root / "cuda_runtime"
    legacy_component_root = (
        Path(os.environ.get("LOCALAPPDATA", Path.home()))
        / "MeshMill"
        / "components"
        / "cuda"
    )
    for runtime_root in (bundled_root, legacy_component_root):
        if not runtime_root.is_dir():
            continue
        sys.path.insert(0, str(runtime_root))
        runtime_dll_directories = [runtime_root]
        runtime_dll_directories.extend(
            path for path in (runtime_root / "nvidia").glob("*/bin") if path.is_dir()
        )
        for directory in runtime_dll_directories:
            _cuda_dll_directories.append(os.add_dll_directory(str(directory)))
            os.environ["PATH"] = str(directory) + os.pathsep + os.environ.get("PATH", "")
    try:
        nvrtc_spec = importlib.util.find_spec("nvidia.cuda_nvrtc")
    except ModuleNotFoundError:
        nvrtc_spec = None
    nvrtc_directories: list[Path] = []
    if nvrtc_spec is not None and nvrtc_spec.submodule_search_locations:
        package_root = next(iter(nvrtc_spec.submodule_search_locations), None)
        if package_root:
            nvrtc_directories.append(Path(package_root) / "bin")
    if any(frozen_root.glob("nvrtc64_*.dll")):
        nvrtc_directories.append(frozen_root)
    for nvrtc_directory in nvrtc_directories:
        if nvrtc_directory.is_dir():
            _cuda_dll_directories.append(os.add_dll_directory(str(nvrtc_directory)))
            os.environ["PATH"] = str(nvrtc_directory) + os.pathsep + os.environ.get("PATH", "")
            break

_cupy_import_error: str | None = None
try:
    import cupy as cp
except (ImportError, OSError) as exc:
    cp = None
    _cupy_import_error = repr(exc)

if os.environ.get("MESHMILL_GPU_DIAGNOSTICS") and _cupy_import_error:
    print(f"MeshMill GPU backend import failed: {_cupy_import_error}", file=sys.stderr)


def cuda_devices() -> list[dict[str, Any]]:
    """Return CUDA devices with stable PCI identifiers for application preferences."""
    if cp is None:
        return []
    devices: list[dict[str, Any]] = []
    try:
        count = cp.cuda.runtime.getDeviceCount()
    except Exception:  # noqa: BLE001 - enumeration must not block application startup
        return []
    for device_id in range(count):
        try:
            properties = cp.cuda.runtime.getDeviceProperties(device_id)
            name = properties.get("name", f"CUDA GPU {device_id}")
            if isinstance(name, bytes):
                name = name.decode("utf-8", errors="replace")
            pci_bus_id = str(cp.cuda.runtime.deviceGetPCIBusId(device_id))
            devices.append(
                {
                    "id": device_id,
                    "name": str(name),
                    "pci_bus_id": pci_bus_id,
                    "total_memory": int(properties.get("totalGlobalMem", 0)),
                }
            )
        except Exception:  # noqa: BLE001,S112 - one inaccessible adapter should not hide the others
            continue
    return devices


def select_cuda_device(preference: str = "system") -> int | None:
    """Select a CUDA device by stable PCI ID, or retain CUDA's default device."""
    if cp is None:
        return None
    if not preference or preference == "system":
        device = cp.cuda.Device(0)
        device.use()
        return int(device.id)
    device = cp.cuda.Device.from_pci_bus_id(preference)
    device.use()
    return int(device.id)


def gpu_backend_available(preference: str = "system") -> bool:
    """Return whether a CUDA device can execute the adaptive-probe analysis."""
    if cp is None:
        return False
    try:
        if cp.cuda.runtime.getDeviceCount() < 1:
            return False
        select_cuda_device(preference)
        probe = cp.arange(1, dtype=cp.float32)
        cp.cuda.Stream.null.synchronize()
        return float(probe.get()[0]) == 0.0
    except Exception:  # noqa: BLE001 - CuPy exposes several backend/compiler exception types
        return False


def gpu_backend_supported(preference: str = "system") -> bool:
    """Return whether the packaged backend and a CUDA device are present without compiling kernels."""
    if os.environ.get("MESHMILL_DISABLE_CUDA") == "1":
        return False
    if cp is None:
        return False
    try:
        if cp.cuda.runtime.getDeviceCount() < 1:
            return False
        if preference != "system":
            select_cuda_device(preference)
        return not (os.name == "nt" and not _cuda_dll_directories)
    except Exception as exc:  # noqa: BLE001 - capability detection must not block application startup
        if os.environ.get("MESHMILL_GPU_DIAGNOSTICS"):
            print(f"MeshMill GPU capability check failed: {exc!r}", file=sys.stderr)
        return False


def _gpu_cache_marker(preference: str = "system") -> Path | None:
    """Return a versioned local marker for MeshMill's successfully compiled GPU kernels."""
    if cp is None:
        return None
    try:
        if cp.cuda.runtime.getDeviceCount() < 1:
            return None
        device_id = select_cuda_device(preference)
        device = cp.cuda.runtime.getDeviceProperties(device_id or 0)
        device_name = device.get("name", b"gpu")
        if isinstance(device_name, bytes):
            device_name = device_name.decode("utf-8", errors="replace")
        identity = re.sub(r"[^A-Za-z0-9._-]+", "-", str(device_name)).strip("-")
    except Exception:  # noqa: BLE001 - detection must not prevent the CPU fallback
        identity = "gpu"
    try:
        runtime = cp.cuda.runtime.runtimeGetVersion()
    except Exception:  # noqa: BLE001 - the marker can still identify the backend without a version
        runtime = "unknown"
    cupy_version = getattr(cp, "__version__", "unknown")
    base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "MeshMill" / "gpu-cache"
    return base / f"cupy-{cupy_version}-cuda-{runtime}-{identity}.ready"


def first_time_gpu_setup_needed(preference: str = "system") -> bool:
    """Return whether this GPU/backend combination lacks a completed MeshMill setup marker."""
    if not gpu_backend_supported(preference):
        return False
    marker = _gpu_cache_marker(preference)
    return marker is not None and not marker.exists()


def _mark_gpu_cache_ready(preference: str = "system") -> None:
    marker = _gpu_cache_marker(preference)
    if marker is None:
        return
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("Depth Adaptive QEM GPU kernels prepared.\n", encoding="utf-8")
    except OSError as exc:
        if os.environ.get("MESHMILL_GPU_DIAGNOSTICS"):
            print(f"MeshMill GPU cache marker failed: {exc!r}", file=sys.stderr)


def physical_probe_dimensions(
    points: np.ndarray, faces: np.ndarray, target: int
) -> dict[str, float]:
    """Derive probe diameter, tip radius, and minimum pitch from the mesh."""
    sample_faces = faces[:: max(1, len(faces) // 500_000)]
    triangles = points[sample_faces]
    edges = np.concatenate(
        (
            np.linalg.norm(triangles[:, 1] - triangles[:, 0], axis=1),
            np.linalg.norm(triangles[:, 2] - triangles[:, 1], axis=1),
            np.linalg.norm(triangles[:, 0] - triangles[:, 2], axis=1),
        )
    )
    valid_edges = edges[edges > 1e-12]
    probe_diameter = float(np.median(valid_edges)) if len(valid_edges) else 0.0
    twice_area = np.linalg.norm(
        np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]),
        axis=1,
    )
    area = float(0.5 * twice_area.sum() * (len(faces) / len(sample_faces)))
    output_pitch = float(np.sqrt(4.0 * area / (np.sqrt(3.0) * target)))
    return {
        "diameter": probe_diameter,
        "tip_radius": probe_diameter * 0.5,
        "minimum_pitch": max(output_pitch, probe_diameter, 1e-12),
    }


def _bincount(keys: Any, weights: Any, count: int) -> Any:
    return cp.bincount(keys, weights=weights, minlength=count).astype(cp.float32)


def adaptive_probe_projection(
    points: np.ndarray, faces: np.ndarray, target: int, gpu_preference: str = "system"
) -> tuple[np.ndarray, dict[str, Any]]:
    """Project supported scan-scale excursions onto locally fitted surface trajectories."""
    if not gpu_backend_available(gpu_preference):
        return np.ascontiguousarray(points), {
            "backend": "Fast QEM fallback",
            "seconds": 0.0,
            "reason": "CUDA adaptive-probe backend unavailable",
        }

    started = time.perf_counter()
    device_id = select_cuda_device(gpu_preference)
    physical = physical_probe_dimensions(points, faces, target)
    tip_radius = physical["tip_radius"]
    displacement_cap = tip_radius * 0.25
    pitches = [physical["minimum_pitch"] * factor for factor in (8.0, 4.0, 2.0, 1.0)]

    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    triangles = gp[gf]
    cross = cp.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    twice_area = cp.linalg.norm(cross, axis=1)
    face_normals = cross / cp.maximum(twice_area[:, None], cp.float32(1e-12))
    centers = cp.mean(triangles, axis=1)
    weights = twice_area * cp.float32(0.5)
    low = cp.min(gp, axis=0)
    high = cp.max(gp, axis=0)
    vertex_delta = cp.zeros_like(gp)
    vertex_weight = cp.zeros(len(points), dtype=cp.float32)
    unresolved = cp.ones(len(faces), dtype=cp.bool_)
    level_stats: list[dict[str, Any]] = []

    for pitch in pitches:
        dims = cp.maximum(cp.ceil((high - low) / pitch).astype(cp.int64) + 1, 1)
        cell = cp.floor((centers - low) / pitch).astype(cp.int64)
        raw_keys = cell[:, 0] + dims[0] * (cell[:, 1] + dims[1] * cell[:, 2])
        _occupied_keys, keys = cp.unique(raw_keys, return_inverse=True)
        cell_count = int(cp.max(keys).get()) + 1
        area_sum = _bincount(keys, weights, cell_count)
        weighted_normal = cp.stack(
            [_bincount(keys, weights * face_normals[:, axis], cell_count) for axis in range(3)],
            axis=1,
        )
        normal_length = cp.linalg.norm(weighted_normal, axis=1)
        mean_normal = weighted_normal / cp.maximum(normal_length[:, None], cp.float32(1e-12))
        coherence = normal_length / cp.maximum(area_sum, cp.float32(1e-12))
        mean_center = cp.stack(
            [_bincount(keys, weights * centers[:, axis], cell_count) for axis in range(3)],
            axis=1,
        ) / cp.maximum(area_sum[:, None], cp.float32(1e-12))
        local_normal = mean_normal[keys]
        local_center = mean_center[keys]
        residual = cp.abs(cp.sum(local_normal * (centers - local_center), axis=1))
        residual_mean = _bincount(keys, weights * residual, cell_count) / cp.maximum(
            area_sum, cp.float32(1e-12)
        )
        residual_sq = _bincount(keys, weights * residual * residual, cell_count) / cp.maximum(
            area_sum, cp.float32(1e-12)
        )
        residual_sigma = cp.sqrt(cp.maximum(residual_sq - residual_mean * residual_mean, 0.0))
        inlier = residual <= cp.maximum(
            residual_mean[keys] + cp.float32(2.5) * residual_sigma[keys],
            cp.float32(tip_radius),
        )
        inlier_weight = weights * inlier
        inlier_area = _bincount(keys, inlier_weight, cell_count)
        clipped_rms = cp.sqrt(
            _bincount(keys, inlier_weight * residual * residual, cell_count)
            / cp.maximum(inlier_area, cp.float32(1e-12))
        )
        maximum_angle = np.arctan2(tip_radius, pitch * 0.5)
        coherence_limit = float(np.cos(maximum_angle))
        valid_cell = (coherence >= cp.float32(coherence_limit)) & (
            clipped_rms <= cp.float32(tip_radius)
        )
        assigned = unresolved & valid_cell[keys]
        dust = assigned & (residual > cp.float32(tip_radius * 0.5)) & (
            residual <= cp.float32(tip_radius * 1.5)
        )
        flat_vertices = gf[dust].ravel()
        if int(cp.count_nonzero(dust).get()):
            selected_triangles = triangles[dust]
            selected_normal = local_normal[dust]
            selected_center = local_center[dust]
            selected_weight = weights[dust]
            signed = cp.sum(
                (selected_triangles - selected_center[:, None, :])
                * selected_normal[:, None, :],
                axis=2,
            )
            repeated_weight = cp.repeat(selected_weight, 3)
            for axis in range(3):
                delta = -signed * selected_normal[:, None, axis]
                vertex_delta[:, axis] += _bincount(
                    flat_vertices, repeated_weight * delta.ravel(), len(points)
                )
            vertex_weight += _bincount(flat_vertices, repeated_weight, len(points))
        level_stats.append(
            {
                "pitch": float(pitch),
                "assigned_faces": int(cp.count_nonzero(assigned).get()),
                "probe_count": len(cp.unique(keys[assigned])),
                "projected_outlier_faces": int(cp.count_nonzero(dust).get()),
            }
        )
        unresolved &= ~assigned

    delta = vertex_delta / cp.maximum(vertex_weight[:, None], cp.float32(1e-12))
    length = cp.linalg.norm(delta, axis=1)
    delta *= cp.minimum(
        1.0, cp.float32(displacement_cap) / cp.maximum(length, cp.float32(1e-12))
    )[:, None]
    projected = gp + delta
    cp.cuda.Stream.null.synchronize()
    report = {
        "backend": "CUDA",
        "device_id": device_id,
        "device_preference": gpu_preference,
        "seconds": time.perf_counter() - started,
        "probe_geometry": {
            **physical,
            "maximum_pitch": pitches[0],
            "displacement_cap": displacement_cap,
        },
        "levels": level_stats,
        "unresolved_faces": int(cp.count_nonzero(unresolved).get()),
        "moved_vertex_share": float(cp.mean(length > 1e-6).get()),
    }
    _mark_gpu_cache_ready(gpu_preference)
    return cp.asnumpy(projected).astype(np.float32, copy=False), report


def simplify_depth_adaptive_qem(
    points: np.ndarray,
    faces: np.ndarray,
    target: int,
    aggressiveness: float = 8.0,
    gpu_preference: str = "system",
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Run Depth Adaptive QEM, or boundary-preserving Fast QEM without CUDA."""
    try:
        projected, report = adaptive_probe_projection(points, faces, target, gpu_preference)
    except Exception as error:  # noqa: BLE001 - unavailable GPU backends fall back safely
        if os.environ.get("MESHMILL_GPU_DIAGNOSTICS"):
            print(f"MeshMill GPU analysis failed: {error!r}", file=sys.stderr)
        projected = np.ascontiguousarray(points)
        report = {
            "backend": "Fast QEM fallback",
            "seconds": 0.0,
            "reason": f"GPU adaptive-probe analysis failed: {type(error).__name__}",
        }
        if cp is not None:
            cp.get_default_memory_pool().free_all_blocks()
    qem_started = time.perf_counter()
    output_points, output_faces = fast_simplification.simplify(
        projected,
        faces,
        target_count=target,
        agg=aggressiveness,
        verbose=False,
        preserve_border=True,
    )
    report["qem_seconds"] = time.perf_counter() - qem_started
    return output_points, output_faces, report
