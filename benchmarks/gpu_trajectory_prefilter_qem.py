"""GPU contour-gauge surface projection followed by indexed Fast QEM assembly."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import fast_simplification
import numpy as np
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def _bincount(keys, weights, count):
    return cp.bincount(keys, weights=weights, minlength=count).astype(cp.float32)


def project_to_trajectories(points, faces, resolutions, tolerance, displacement_cap):
    """Project vertices toward coherent multiscale tangent surfaces without changing connectivity."""
    started = time.perf_counter()
    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    triangles = gp[gf]
    cross = cp.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    twice_area = cp.linalg.norm(cross, axis=1)
    face_normals = cross / cp.maximum(twice_area[:, None], cp.float32(1e-12))
    centers = cp.mean(triangles, axis=1)
    weights = twice_area * cp.float32(0.5)
    low = cp.min(gp, axis=0)
    extent = cp.maximum(cp.max(gp, axis=0) - low, cp.float32(1e-12))
    vertex_delta = cp.zeros_like(gp)
    vertex_weight = cp.zeros(len(points), dtype=cp.float32)
    stats = []

    for resolution in resolutions:
        cells = cp.floor((centers - low) / extent * resolution).astype(cp.int32)
        cells = cp.clip(cells, 0, resolution - 1)
        keys = cells[:, 0] + resolution * (cells[:, 1] + resolution * cells[:, 2])
        cell_count = resolution ** 3
        area_sum = _bincount(keys, weights, cell_count)
        weighted_normal = cp.stack(
            [_bincount(keys, weights * face_normals[:, axis], cell_count) for axis in range(3)],
            axis=1,
        )
        normal_length = cp.linalg.norm(weighted_normal, axis=1)
        mean_normal = weighted_normal / cp.maximum(normal_length[:, None], cp.float32(1e-12))
        coherence = normal_length / cp.maximum(area_sum, cp.float32(1e-12))
        mean_center = cp.stack(
            [_bincount(keys, weights * centers[:, axis], cell_count) for axis in range(3)], axis=1
        ) / cp.maximum(area_sum[:, None], cp.float32(1e-12))
        local_normal = mean_normal[keys]
        local_center = mean_center[keys]
        residual = cp.abs(cp.sum(local_normal * (centers - local_center), axis=1))
        # Broad coherent surfaces qualify. High-curvature, conflicting, and isolated cells remain
        # untouched. The final per-vertex displacement cap prevents a coarse cell from flattening
        # legitimate form.
        supported = (
            (coherence[keys] >= cp.float32(0.970))
            & (residual > cp.float32(tolerance))
            & (residual <= cp.float32(tolerance * 3.0))
        )
        face_weight = weights * supported
        flat_vertices = gf.ravel()
        repeated_weight = cp.repeat(face_weight, 3)
        for axis in range(3):
            coordinate = triangles[:, :, axis]
            signed = cp.sum(
                (triangles - local_center[:, None, :]) * local_normal[:, None, :], axis=2
            )
            projected = coordinate - signed * local_normal[:, None, axis]
            delta = projected - coordinate
            vertex_delta[:, axis] += _bincount(
                flat_vertices, repeated_weight * delta.ravel(), len(points)
            )
        vertex_weight += _bincount(flat_vertices, repeated_weight, len(points))
        stats.append(
            {
                "resolution": resolution,
                "coherent_face_share": float(cp.mean(supported).get()),
                "mean_supported_residual": float(
                    cp.sum(residual * face_weight).get() / max(float(cp.sum(face_weight).get()), 1e-12)
                ),
            }
        )

    delta = vertex_delta / cp.maximum(vertex_weight[:, None], cp.float32(1e-12))
    length = cp.linalg.norm(delta, axis=1)
    scale = cp.minimum(cp.float32(1.0), cp.float32(displacement_cap) / cp.maximum(length, 1e-12))
    delta *= scale[:, None]
    projected = gp + delta
    cp.cuda.Stream.null.synchronize()
    report = {
        "seconds": time.perf_counter() - started,
        "scales": stats,
        "moved_vertex_share": float(cp.mean(length > 1e-6).get()),
        "mean_displacement": float(cp.mean(cp.minimum(length, displacement_cap)).get()),
        "max_displacement": float(cp.max(cp.minimum(length, displacement_cap)).get()),
    }
    return cp.asnumpy(projected).astype(np.float32, copy=False), report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--resolutions", default="24,48,72")
    parser.add_argument("--tolerance", type=float, default=0.10)
    parser.add_argument("--displacement-cap", type=float, default=0.10)
    parser.add_argument("--aggressiveness", type=float, default=5.0)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()

    total_started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    projected, analysis = project_to_trajectories(
        points,
        faces,
        [int(value) for value in args.resolutions.split(",")],
        args.tolerance,
        args.displacement_cap,
    )
    reduction_started = time.perf_counter()
    out_points, out_faces = fast_simplification.simplify(
        projected,
        faces,
        target_count=args.target,
        agg=args.aggressiveness,
        verbose=False,
        preserve_border=True,
    )
    reduction_seconds = time.perf_counter() - reduction_started
    save_binary_stl(args.output_mesh, out_points, out_faces)
    quality = quality_metrics(points, faces, out_points, out_faces, args.sample_count)
    quality.update(topology_metrics(out_faces))
    report = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "target_triangles": args.target,
        "output_triangles": len(out_faces),
        "output_vertices": len(out_points),
        "connectivity_seconds": connectivity_seconds,
        "gpu_surface_projection": analysis,
        "cpu_qem_seconds": reduction_seconds,
        "aggressiveness": args.aggressiveness,
        "total_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
