"""Bounded-memory indexing primitives for binary STL meshes.

The module deliberately has no Qt, VTK, or GPU dependency. It provides the stable storage and
work-unit boundary that rendering and optional GPU compute backends can share.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import struct
import threading
from typing import Callable

import numpy as np


INDEX_VERSION = 1
STL_RECORD_BYTES = 50
STL_HEADER_BYTES = 84
TRIANGLE_RECORD_DTYPE = np.dtype(
    [("normal", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")]
)


class IndexCancelled(Exception):
    """Raised when index creation is cancelled without publishing a partial index."""


@dataclass(frozen=True)
class TileRecord:
    level: int
    morton: int
    triangle_count: int
    relative_path: str


@dataclass(frozen=True)
class IndexManifest:
    index_version: int
    source_size: int
    source_mtime_ns: int
    source_fingerprint: str
    triangle_count: int
    bounds: tuple[float, float, float, float, float, float]
    max_depth: int
    target_triangles_per_tile: int
    tiles: tuple[TileRecord, ...]


def binary_stl_count(path: Path) -> int:
    size = path.stat().st_size
    if size < STL_HEADER_BYTES:
        raise ValueError("The file is too small to be a binary STL.")
    with path.open("rb") as stream:
        header = stream.read(STL_HEADER_BYTES)
    count = struct.unpack_from("<I", header, 80)[0]
    if STL_HEADER_BYTES + STL_RECORD_BYTES * count != size:
        raise ValueError("Out-of-core indexing currently requires a valid binary STL.")
    return count


def source_fingerprint(path: Path, sample_bytes: int = 1 << 20) -> str:
    """Hash stable source metadata and bounded samples without reading the complete file."""
    stat = path.stat()
    digest = sha256()
    digest.update(struct.pack("<QQ", stat.st_size, stat.st_mtime_ns))
    with path.open("rb") as stream:
        digest.update(stream.read(sample_bytes))
        if stat.st_size > sample_bytes:
            stream.seek(max(0, stat.st_size - sample_bytes))
            digest.update(stream.read(sample_bytes))
    return digest.hexdigest()


def default_index_directory(source: Path) -> Path:
    """Return a private, stable cache path without exposing the source filename."""
    cache_root = (
        Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache")) / "MeshMill" / "indexes"
    )
    normalized_source = os.path.normcase(os.fspath(source.resolve())).encode("utf-8")
    source_key = sha256(normalized_source).hexdigest()[:24]
    return cache_root / f"{source_key}.meshmill-index"


def _cancelled(cancel_event: threading.Event | None) -> None:
    if cancel_event is not None and cancel_event.is_set():
        raise IndexCancelled


def _progress(callback: Callable[[str, int, int], None] | None, stage: str, done: int, total: int):
    if callback is not None:
        callback(stage, done, total)


def _part1by2(value: np.ndarray) -> np.ndarray:
    value = value.astype(np.uint64, copy=False) & np.uint64(0x1FFFFF)
    value = (value | (value << np.uint64(32))) & np.uint64(0x1F00000000FFFF)
    value = (value | (value << np.uint64(16))) & np.uint64(0x1F0000FF0000FF)
    value = (value | (value << np.uint64(8))) & np.uint64(0x100F00F00F00F00F)
    value = (value | (value << np.uint64(4))) & np.uint64(0x10C30C30C30C30C3)
    return (value | (value << np.uint64(2))) & np.uint64(0x1249249249249249)


def morton3(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    return _part1by2(x) | (_part1by2(y) << np.uint64(1)) | (_part1by2(z) << np.uint64(2))


def _bounds(records: np.memmap, block_triangles: int, cancel_event, progress_callback):
    low = np.full(3, np.inf, dtype=np.float64)
    high = np.full(3, -np.inf, dtype=np.float64)
    total = len(records)
    for start in range(0, total, block_triangles):
        _cancelled(cancel_event)
        vertices = records[start : start + block_triangles]["vertices"]
        low = np.minimum(low, vertices.min(axis=(0, 1)))
        high = np.maximum(high, vertices.max(axis=(0, 1)))
        _progress(progress_callback, "bounds", min(total, start + len(vertices)), total)
    if not np.all(np.isfinite(low)) or np.any(high < low):
        raise ValueError("The STL contains invalid coordinate bounds.")
    return low, high


def _tile_counts(
    records: np.memmap,
    low: np.ndarray,
    extent: np.ndarray,
    grid: int,
    block_triangles: int,
    cancel_event,
    progress_callback,
) -> dict[int, int]:
    counts: dict[int, int] = {}
    total = len(records)
    for start in range(0, total, block_triangles):
        _cancelled(cancel_event)
        chunk = records[start : start + block_triangles]
        centroids = chunk["vertices"].mean(axis=1, dtype=np.float64)
        cells = np.floor((centroids - low) / extent * grid).astype(np.int64)
        np.clip(cells, 0, grid - 1, out=cells)
        codes, chunk_counts = np.unique(
            morton3(cells[:, 0], cells[:, 1], cells[:, 2]), return_counts=True
        )
        for code, count in zip(codes, chunk_counts, strict=True):
            key = int(code)
            counts[key] = counts.get(key, 0) + int(count)
        _progress(progress_callback, "planning", min(total, start + len(chunk)), total)
    return counts


def _plan_adaptive_tiles(
    records: np.memmap,
    low: np.ndarray,
    extent: np.ndarray,
    target: int,
    block_triangles: int,
    cancel_event,
    progress_callback,
) -> tuple[int, dict[tuple[int, int], int]]:
    """Subdivide only overflowing octree leaves and return their measured counts."""
    if len(records) <= target:
        return 0, {(0, 0): len(records)}
    leaves: dict[tuple[int, int], int] = {}
    split_parents = {0}
    for level in range(1, 22):
        grid = 1 << level
        counts = _tile_counts(
            records, low, extent, grid, block_triangles, cancel_event, progress_callback
        )
        next_split: set[int] = set()
        for code, count in counts.items():
            parent = code >> 3
            if parent not in split_parents:
                continue
            if count > target:
                next_split.add(code)
            else:
                leaves[(level, code)] = count
        if not next_split:
            return level, leaves
        split_parents = next_split
    raise ValueError("The mesh cannot be partitioned within the configured tile target.")


def _leaf_assignments(
    centroids: np.ndarray,
    low: np.ndarray,
    extent: np.ndarray,
    max_depth: int,
    leaves: dict[tuple[int, int], int],
) -> tuple[np.ndarray, np.ndarray]:
    assigned_levels = np.full(len(centroids), -1, dtype=np.int16)
    assigned_codes = np.zeros(len(centroids), dtype=np.uint64)
    for level in range(max_depth + 1):
        level_codes = np.fromiter(
            (code for leaf_level, code in leaves if leaf_level == level), dtype=np.uint64
        )
        if not len(level_codes):
            continue
        grid = 1 << level
        cells = np.floor((centroids - low) / extent * grid).astype(np.int64)
        np.clip(cells, 0, grid - 1, out=cells)
        codes = morton3(cells[:, 0], cells[:, 1], cells[:, 2])
        selected = (assigned_levels < 0) & np.isin(codes, level_codes)
        assigned_levels[selected] = level
        assigned_codes[selected] = codes[selected]
    if np.any(assigned_levels < 0):
        raise RuntimeError("Adaptive tile planning left triangles without a leaf owner.")
    return assigned_levels, assigned_codes


def build_index(
    source: Path,
    index_directory: Path,
    *,
    target_triangles_per_tile: int = 262_144,
    block_triangles: int = 262_144,
    cancel_event: threading.Event | None = None,
    progress_callback: Callable[[str, int, int], None] | None = None,
) -> IndexManifest:
    """Create a deterministic spatial index without holding the full mesh in RAM.

    Triangle records are assigned by centroid. Boundary overlap belongs to later operation-specific
    work-unit construction, which prevents the persistent index from duplicating source geometry.
    """
    source = source.resolve()
    triangle_count = binary_stl_count(source)
    target_triangles_per_tile = max(65_536, int(target_triangles_per_tile))
    block_triangles = max(16_384, int(block_triangles))
    records = np.memmap(
        source, dtype=TRIANGLE_RECORD_DTYPE, mode="r", offset=STL_HEADER_BYTES,
        shape=(triangle_count,),
    )
    low, high = _bounds(records, block_triangles, cancel_event, progress_callback)
    extent = np.maximum(high - low, np.finfo(np.float64).eps)
    max_depth, planned_counts = _plan_adaptive_tiles(
        records,
        low,
        extent,
        target_triangles_per_tile,
        block_triangles,
        cancel_event,
        progress_callback,
    )

    staging = index_directory.with_name(index_directory.name + ".building")
    staging.mkdir(parents=True, exist_ok=True)
    for stale in staging.glob("tile-*.bin"):
        stale.unlink()

    counts: dict[tuple[int, int], int] = {}
    handles: dict[tuple[int, int], object] = {}
    try:
        for start in range(0, triangle_count, block_triangles):
            _cancelled(cancel_event)
            chunk = records[start : start + block_triangles]
            centroids = chunk["vertices"].mean(axis=1, dtype=np.float64)
            levels, codes = _leaf_assignments(
                centroids, low, extent, max_depth, planned_counts
            )
            keys = (levels.astype(np.uint64) << np.uint64(56)) | codes
            order = np.argsort(keys, kind="stable")
            sorted_keys = keys[order]
            boundaries = np.flatnonzero(np.diff(sorted_keys)) + 1
            for group in np.split(order, boundaries):
                level = int(levels[group[0]])
                code = int(codes[group[0]])
                key = (level, code)
                handle = handles.get(key)
                if handle is None:
                    handle = (staging / f"tile-L{level:02d}-{code:016x}.bin").open("ab")
                    handles[key] = handle
                payload = np.ascontiguousarray(chunk[group]).view(np.uint8)
                handle.write(payload.tobytes())
                counts[key] = counts.get(key, 0) + len(group)
            _progress(
                progress_callback,
                "partition",
                min(triangle_count, start + len(chunk)),
                triangle_count,
            )
    except Exception:
        for handle in handles.values():
            handle.close()
        shutil.rmtree(staging, ignore_errors=True)
        raise
    finally:
        del records
    for handle in handles.values():
        handle.flush()
        os.fsync(handle.fileno())
        handle.close()
    if counts != planned_counts:
        raise RuntimeError("Spatial index counts changed between planning and partitioning.")

    stat = source.stat()
    tiles = tuple(
        TileRecord(level, code, count, f"tile-L{level:02d}-{code:016x}.bin")
        for (level, code), count in sorted(counts.items())
    )
    manifest = IndexManifest(
        INDEX_VERSION,
        stat.st_size,
        stat.st_mtime_ns,
        source_fingerprint(source),
        triangle_count,
        (
            float(low[0]), float(high[0]),
            float(low[1]), float(high[1]),
            float(low[2]), float(high[2]),
        ),
        max_depth,
        target_triangles_per_tile,
        tiles,
    )
    manifest_payload = asdict(manifest)
    manifest_payload["tiles"] = [asdict(tile) for tile in tiles]
    temporary_manifest = staging / "manifest.json.tmp"
    temporary_manifest.write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary_manifest, staging / "manifest.json")
    backup = index_directory.with_name(index_directory.name + ".previous")
    had_previous = index_directory.exists()
    if had_previous:
        if backup.exists():
            shutil.rmtree(backup)
        os.replace(index_directory, backup)
    try:
        os.replace(staging, index_directory)
    except Exception:
        if had_previous and backup.exists() and not index_directory.exists():
            os.replace(backup, index_directory)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)
    _progress(progress_callback, "complete", triangle_count, triangle_count)
    return manifest


def load_manifest(index_directory: Path) -> IndexManifest:
    payload = json.loads((index_directory / "manifest.json").read_text(encoding="utf-8"))
    tiles = tuple(TileRecord(**tile) for tile in payload.pop("tiles"))
    payload["bounds"] = tuple(payload["bounds"])
    return IndexManifest(tiles=tiles, **payload)


def index_matches(source: Path, manifest: IndexManifest) -> bool:
    stat = source.stat()
    return (
        manifest.index_version == INDEX_VERSION
        and manifest.source_size == stat.st_size
        and manifest.source_mtime_ns == stat.st_mtime_ns
        and manifest.source_fingerprint == source_fingerprint(source)
    )
