"""Benchmark sequential and multiprocessing out-of-core tile analysis.

This does not create or modify a MeshMill index. Each worker opens the binary STL read-only and
returns small aggregate results so the measurement includes realistic process and I/O overhead.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from out_of_core import (
    STL_HEADER_BYTES,
    TRIANGLE_RECORD_DTYPE,
    _bounds,
    _plan_adaptive_tiles,
    binary_stl_count,
    build_index,
    morton3,
)


def _ranges(total: int, block: int):
    return [(start, min(total, start + block)) for start in range(0, total, block)]


def _worker_bounds(source: str, total: int, start: int, stop: int):
    records = np.memmap(
        source, dtype=TRIANGLE_RECORD_DTYPE, mode="r", offset=STL_HEADER_BYTES,
        shape=(total,),
    )
    vertices = records[start:stop]["vertices"]
    return vertices.min(axis=(0, 1)), vertices.max(axis=(0, 1))


def _worker_counts(
    source: str,
    total: int,
    start: int,
    stop: int,
    low: np.ndarray,
    extent: np.ndarray,
    grid: int,
):
    records = np.memmap(
        source, dtype=TRIANGLE_RECORD_DTYPE, mode="r", offset=STL_HEADER_BYTES,
        shape=(total,),
    )
    centroids = records[start:stop]["vertices"].mean(axis=1, dtype=np.float64)
    cells = np.floor((centroids - low) / extent * grid).astype(np.int64)
    np.clip(cells, 0, grid - 1, out=cells)
    codes, counts = np.unique(
        morton3(cells[:, 0], cells[:, 1], cells[:, 2]), return_counts=True
    )
    return tuple(zip(codes.tolist(), counts.tolist()))


def _merge_counts(results):
    merged: dict[int, int] = {}
    for result in results:
        for code, count in result:
            merged[int(code)] = merged.get(int(code), 0) + int(count)
    return merged


def parallel_bounds(source: Path, workers: int, block: int):
    total = binary_stl_count(source)
    chunks = _ranges(total, block)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(
            pool.map(
                _worker_bounds,
                [str(source)] * len(chunks),
                [total] * len(chunks),
                [item[0] for item in chunks],
                [item[1] for item in chunks],
            )
        )
    return (
        np.minimum.reduce([item[0] for item in results]),
        np.maximum.reduce([item[1] for item in results]),
    )


def parallel_plan(
    source: Path,
    workers: int,
    block: int,
    target: int,
    low: np.ndarray,
    extent: np.ndarray,
):
    total = binary_stl_count(source)
    chunks = _ranges(total, block)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        leaves: dict[tuple[int, int], int] = {}
        split_parents = {0}
        for level in range(1, 22):
            results = list(
                pool.map(
                    _worker_counts,
                    [str(source)] * len(chunks),
                    [total] * len(chunks),
                    [item[0] for item in chunks],
                    [item[1] for item in chunks],
                    [low] * len(chunks),
                    [extent] * len(chunks),
                    [1 << level] * len(chunks),
                )
            )
            counts = _merge_counts(results)
            next_split: set[int] = set()
            for code, count in counts.items():
                if code >> 3 not in split_parents:
                    continue
                if count > target:
                    next_split.add(code)
                else:
                    leaves[(level, code)] = count
            if not next_split:
                return level, leaves
            split_parents = next_split
    raise RuntimeError("maximum octree depth exceeded")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--workers", default="1,2,4,8")
    parser.add_argument("--block", type=int, default=262_144)
    parser.add_argument("--target", type=int, default=262_144)
    parser.add_argument("--full-index", action="store_true")
    args = parser.parse_args()
    source = args.source.resolve()
    total = binary_stl_count(source)
    records = np.memmap(
        source, dtype=TRIANGLE_RECORD_DTYPE, mode="r", offset=STL_HEADER_BYTES,
        shape=(total,),
    )
    bounds_started = time.perf_counter()
    low, high = _bounds(records, args.block, None, None)
    bounds_seconds = time.perf_counter() - bounds_started
    planning_started = time.perf_counter()
    depth, leaves = _plan_adaptive_tiles(
        records,
        low,
        np.maximum(high - low, np.finfo(np.float64).eps),
        args.target,
        args.block,
        None,
        None,
    )
    planning_seconds = time.perf_counter() - planning_started
    sequential_seconds = bounds_seconds + planning_seconds
    expected = (depth, leaves)
    print(
        f"sequential: {sequential_seconds:.3f}s "
        f"(bounds={bounds_seconds:.3f}s, planning={planning_seconds:.3f}s), depth={depth}, "
        f"tiles={len(leaves)}, triangles={sum(leaves.values()):,}",
        flush=True,
    )
    del records

    for workers in (int(value) for value in args.workers.split(",") if value.strip()):
        parallel_bounds_started = time.perf_counter()
        worker_low, worker_high = parallel_bounds(source, workers, args.block)
        parallel_bounds_seconds = time.perf_counter() - parallel_bounds_started
        bounds_match = np.array_equal(worker_low, low) and np.array_equal(worker_high, high)
        started = time.perf_counter()
        result = parallel_plan(
            source,
            workers,
            args.block,
            args.target,
            low,
            np.maximum(high - low, np.finfo(np.float64).eps),
        )
        parallel_planning_seconds = time.perf_counter() - started
        seconds = parallel_bounds_seconds + parallel_planning_seconds
        if result != expected:
            result_depth, result_leaves = result
            missing = sorted(set(leaves) - set(result_leaves))[:5]
            extra = sorted(set(result_leaves) - set(leaves))[:5]
            changed = [
                key for key in set(leaves) & set(result_leaves)
                if leaves[key] != result_leaves[key]
            ][:5]
            raise RuntimeError(
                f"{workers}-worker result differs: depth={result_depth}/{depth}, "
                f"tiles={len(result_leaves)}/{len(leaves)}, missing={missing}, "
                f"extra={extra}, changed={[(key, leaves[key], result_leaves[key]) for key in changed]}"
            )
        print(
            f"workers={workers}: {seconds:.3f}s "
            f"(bounds={parallel_bounds_seconds:.3f}s, planning={parallel_planning_seconds:.3f}s, "
            f"bounds_match={bounds_match}), "
            f"speedup={sequential_seconds / seconds:.2f}x, "
            f"saved={sequential_seconds - seconds:+.3f}s",
            flush=True,
        )
    if args.full_index:
        root = Path(tempfile.mkdtemp(prefix="meshmill-index-benchmark-"))
        try:
            for workers in (1, 8):
                destination = root / f"workers-{workers}.meshmill-index"
                started = time.perf_counter()
                manifest = build_index(
                    source,
                    destination,
                    target_triangles_per_tile=args.target,
                    block_triangles=args.block,
                    analysis_workers=workers,
                )
                seconds = time.perf_counter() - started
                print(
                    f"full-index workers={workers}: {seconds:.3f}s, "
                    f"tiles={len(manifest.tiles)}, triangles={sum(t.triangle_count for t in manifest.tiles):,}",
                    flush=True,
                )
        finally:
            shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
