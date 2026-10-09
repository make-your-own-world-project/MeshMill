"""Boundary-first tiled simplification experiment.

This is benchmark code, not an application backend. The GPU classifies connected geometry into
cubes and extracts triangles crossing cube boundaries. Those shared interface triangles remain
canonical while cube interiors are simplified concurrently with their newly exposed borders locked.
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import cupy as cp
import fast_simplification
import numpy as np
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def classify_gpu(points: np.ndarray, faces: np.ndarray, grid: int):
    started = time.perf_counter()
    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    low = cp.min(gp, axis=0)
    extent = cp.maximum(cp.max(gp, axis=0) - low, cp.float32(1e-12))
    cells = cp.floor((gp - low) / extent * grid).astype(cp.int32)
    cells = cp.minimum(cells, grid - 1)
    vertex_cube = cells[:, 0] + grid * (cells[:, 1] + grid * cells[:, 2])
    face_cubes = vertex_cube[gf]
    interior = (face_cubes[:, 0] == face_cubes[:, 1]) & (face_cubes[:, 0] == face_cubes[:, 2])
    owner = face_cubes[:, 0]
    cp.cuda.Stream.null.synchronize()
    elapsed = time.perf_counter() - started
    return cp.asnumpy(interior), cp.asnumpy(owner), elapsed


def simplify_tile(
    tile_id: int,
    points: np.ndarray,
    faces: np.ndarray,
    halo_faces: np.ndarray,
    target: int,
    drift_limit: float,
):
    started = time.perf_counter()
    used, inverse = np.unique(faces.reshape(-1), return_inverse=True)
    local_points = points[used]
    local_faces = inverse.reshape(-1, 3).astype(np.int32, copy=False)
    source_topology = topology_metrics(local_faces)
    if target >= len(local_faces):
        out_points, out_faces = local_points, local_faces
    else:
        out_points, out_faces = fast_simplification.simplify(
            local_points,
            local_faces,
            target_count=max(4, target),
            agg=7.0,
            verbose=False,
            preserve_border=True,
        )
    output_topology = topology_metrics(out_faces)
    halo_used, halo_inverse = np.unique(halo_faces.reshape(-1), return_inverse=True)
    halo_points = points[halo_used]
    halo_local_faces = halo_inverse.reshape(-1, 3).astype(np.int32, copy=False)
    source_contract_points, source_contract_faces = weld(
        [(local_points, local_faces), (halo_points, halo_local_faces)]
    )
    output_contract_points, output_contract_faces = weld(
        [(out_points, out_faces), (halo_points, halo_local_faces)]
    )
    source_contract_topology = topology_metrics(source_contract_faces)
    output_contract_topology = topology_metrics(output_contract_faces)
    source_bounds = np.ptp(source_contract_points, axis=0)
    output_bounds = np.ptp(output_contract_points, axis=0)
    drift = float(np.max(np.abs(output_bounds - source_bounds)))
    rejected = (
        output_topology["nonmanifold_edges"] > source_topology["nonmanifold_edges"]
        or output_contract_topology["nonmanifold_edges"]
        > source_contract_topology["nonmanifold_edges"]
        or drift > drift_limit
    )
    if rejected:
        out_points, out_faces = local_points, local_faces
        output_topology = source_topology
    return (
        tile_id,
        out_points.astype(np.float32, copy=False),
        out_faces.astype(np.int32, copy=False),
        time.perf_counter() - started,
        rejected,
        source_topology["boundary_edges"],
        target,
        len(local_faces),
        drift,
    )


def weld(parts: list[tuple[np.ndarray, np.ndarray]]):
    all_points = []
    all_faces = []
    offset = 0
    for points, faces in parts:
        all_points.append(points)
        all_faces.append(faces + offset)
        offset += len(points)
    joined_points = np.concatenate(all_points)
    joined_faces = np.concatenate(all_faces)
    unique_points, inverse = np.unique(joined_points, axis=0, return_inverse=True)
    joined_faces = inverse[joined_faces].astype(np.int32, copy=False)
    keep = (
        (joined_faces[:, 0] != joined_faces[:, 1])
        & (joined_faces[:, 1] != joined_faces[:, 2])
        & (joined_faces[:, 0] != joined_faces[:, 2])
    )
    return unique_points.astype(np.float32, copy=False), joined_faces[keep]


def run(points: np.ndarray, faces: np.ndarray, grid: int, target: int, workers: int, sample_count: int):
    interior_mask, owner, classify_seconds = classify_gpu(points, faces, grid)
    interface_faces = faces[~interior_mask]
    interior_total = int(np.count_nonzero(interior_mask))
    remaining_target = target - len(interface_faces)
    report = {
        "grid": grid,
        "cubes": grid ** 3,
        "gpu_classify_seconds": classify_seconds,
        "interface_triangles": len(interface_faces),
        "interface_share": float(len(interface_faces) / len(faces)),
        "interior_triangles": interior_total,
    }
    if remaining_target < 4:
        report["rejected"] = "The frozen interface alone exceeds the target."
        return report

    tile_inputs = []
    occupied = np.unique(owner[interior_mask])
    tile_records = []
    for tile_id in occupied:
        tile_faces = faces[interior_mask & (owner == tile_id)]
        local_used, local_inverse = np.unique(tile_faces.reshape(-1), return_inverse=True)
        local_faces = local_inverse.reshape(-1, 3).astype(np.int32, copy=False)
        boundary_edges = topology_metrics(local_faces)["boundary_edges"]
        # A triangle patch needs enough faces to span its locked perimeter. Twice the open-edge
        # count is a conservative empirical floor for irregular scan patches and disconnected
        # components; workers may still stop above it.
        minimum_target = min(len(tile_faces), max(4, boundary_edges * 2))
        proportional = max(4, round(remaining_target * len(tile_faces) / interior_total))
        touches = np.any(np.isin(interface_faces, local_used), axis=1)
        halo_faces = interface_faces[touches]
        tile_records.append(
            (int(tile_id), tile_faces, halo_faces, minimum_target, proportional, len(local_used))
        )

    minimum_sum = sum(record[3] for record in tile_records)
    extra_budget = max(0, remaining_target - minimum_sum)
    reducible = sum(max(0, len(record[1]) - record[3]) for record in tile_records)
    for tile_id, tile_faces, halo_faces, minimum_target, proportional, _ in tile_records:
        share = max(0, len(tile_faces) - minimum_target) / max(1, reducible)
        tile_target = min(len(tile_faces), minimum_target + round(extra_budget * share))
        tile_inputs.append((tile_id, tile_faces, halo_faces, tile_target))
    report["boundary_minimum_target_sum"] = int(minimum_sum + len(interface_faces))

    started = time.perf_counter()
    outputs = []
    worker_times = []
    rejected_tiles = 0
    with ThreadPoolExecutor(max_workers=min(workers, len(tile_inputs))) as pool:
        pending = {
            pool.submit(
                simplify_tile, tile_id, points, tile_faces, halo_faces, tile_target, 0.05
            ): tile_id
            for tile_id, tile_faces, halo_faces, tile_target in tile_inputs
        }
        for future in as_completed(pending):
            _, out_points, out_faces, seconds, rejected, _, _, _, _ = future.result()
            outputs.append((out_points, out_faces))
            worker_times.append(seconds)
            rejected_tiles += int(rejected)
    parallel_seconds = time.perf_counter() - started

    interface_used, interface_inverse = np.unique(interface_faces.reshape(-1), return_inverse=True)
    interface_points = points[interface_used]
    interface_local_faces = interface_inverse.reshape(-1, 3).astype(np.int32, copy=False)
    started = time.perf_counter()
    out_points, out_faces = weld([(interface_points, interface_local_faces), *outputs])
    assembly_seconds = time.perf_counter() - started
    report.update(
        {
            "occupied_cubes": len(tile_inputs),
            "parallel_simplify_seconds": parallel_seconds,
            "worker_seconds_sum": float(sum(worker_times)),
            "rejected_tiles": rejected_tiles,
            "assembly_seconds": assembly_seconds,
            "total_processing_seconds": classify_seconds + parallel_seconds + assembly_seconds,
            "quality": quality_metrics(points, faces, out_points, out_faces, sample_count),
        }
    )
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--grids", type=int, nargs="+", default=[2, 3, 4])
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    result = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "target_triangles": args.target,
        "connectivity_seconds": connectivity_seconds,
        "runs": [],
    }
    for grid in args.grids:
        current = run(points, faces, grid, args.target, args.workers, args.sample_count)
        result["runs"].append(current)
        print(json.dumps(current, indent=2), flush=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
