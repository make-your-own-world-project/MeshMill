"""GPU prototype for density-independent, multiscale surface analysis.

This experiment treats spatial cells as an acceleration structure, not as surfaces. It fits
area-weighted local tangent planes, rejects residual outliers, and joins compatible neighboring
fits into surface trajectories that may span any later processing-tile boundary.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import numpy as np
from gpu_geometry_prototype import connected_arrays, load_binary_stl


def _bincount(keys, weights, count):
    return cp.bincount(keys, weights=weights, minlength=count).astype(cp.float32)


def analyze_scale(points_gpu, faces_gpu, resolution: int, tolerance: float):
    started = time.perf_counter()
    triangles = points_gpu[faces_gpu]
    edge_a = triangles[:, 1] - triangles[:, 0]
    edge_b = triangles[:, 2] - triangles[:, 0]
    cross = cp.cross(edge_a, edge_b)
    twice_area = cp.linalg.norm(cross, axis=1)
    valid = twice_area > cp.float32(1e-12)
    normals = cross / cp.maximum(twice_area[:, None], cp.float32(1e-12))
    centers = cp.mean(triangles, axis=1)
    weights = twice_area * cp.float32(0.5)

    low = cp.min(points_gpu, axis=0)
    extent = cp.maximum(cp.max(points_gpu, axis=0) - low, cp.float32(1e-12))
    cells = cp.floor((centers - low) / extent * resolution).astype(cp.int32)
    cells = cp.clip(cells, 0, resolution - 1)
    keys = cells[:, 0] + resolution * (cells[:, 1] + resolution * cells[:, 2])
    cell_count = resolution ** 3

    area_sum = _bincount(keys, weights, cell_count)
    face_count = cp.bincount(keys, minlength=cell_count).astype(cp.int32)
    weighted_normal = cp.stack(
        [_bincount(keys, weights * normals[:, axis], cell_count) for axis in range(3)], axis=1
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
    residual_sum = _bincount(keys, weights * residual, cell_count)
    residual_sq_sum = _bincount(keys, weights * residual * residual, cell_count)
    residual_mean = residual_sum / cp.maximum(area_sum, cp.float32(1e-12))
    residual_var = cp.maximum(
        residual_sq_sum / cp.maximum(area_sum, cp.float32(1e-12)) - residual_mean * residual_mean,
        cp.float32(0.0),
    )
    residual_sigma = cp.sqrt(residual_var)

    # A second fit excludes sparse dust and scan spikes from the surface-error estimate.
    clip_limit = residual_mean[keys] + cp.float32(2.5) * residual_sigma[keys]
    inlier = valid & (residual <= cp.maximum(clip_limit, cp.float32(tolerance)))
    inlier_weight = weights * inlier
    inlier_area = _bincount(keys, inlier_weight, cell_count)
    clipped_sq = _bincount(keys, inlier_weight * residual * residual, cell_count)
    clipped_rms = cp.sqrt(clipped_sq / cp.maximum(inlier_area, cp.float32(1e-12)))
    outlier_area = _bincount(keys, weights * (~inlier), cell_count)
    outlier_share = outlier_area / cp.maximum(area_sum, cp.float32(1e-12))

    occupied = face_count > 0
    planar = occupied & (coherence >= cp.float32(0.995)) & (clipped_rms <= tolerance)
    face_planar = planar[keys]
    face_outlier = ~inlier
    # A looser support field says that an outlier sits on a stable high-level surface. Sharp
    # transitions and genuinely curved regions have low normal coherence and are excluded.
    supported = occupied & (coherence >= cp.float32(0.970)) & (clipped_rms <= tolerance)
    face_supported = supported[keys]
    cp.cuda.Stream.null.synchronize()

    occupied_ids = cp.asnumpy(cp.flatnonzero(occupied))
    planar_ids = cp.asnumpy(cp.flatnonzero(planar))
    normals_cpu = cp.asnumpy(mean_normal[planar_ids])
    centers_cpu = cp.asnumpy(mean_center[planar_ids])
    counts_cpu = cp.asnumpy(face_count[planar_ids])
    id_to_index = {int(cell_id): index for index, cell_id in enumerate(planar_ids)}
    parent = np.arange(len(planar_ids), dtype=np.int32)

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = int(parent[index])
        return index

    def union(left, right):
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    max_angle_cos = float(np.cos(np.deg2rad(5.0)))
    links = 0
    for index, cell_id in enumerate(planar_ids):
        x = int(cell_id % resolution)
        y = int((cell_id // resolution) % resolution)
        z = int(cell_id // (resolution * resolution))
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            nx, ny, nz = x + dx, y + dy, z + dz
            if nx >= resolution or ny >= resolution or nz >= resolution:
                continue
            neighbor_id = nx + resolution * (ny + resolution * nz)
            other = id_to_index.get(neighbor_id)
            if other is None:
                continue
            dot = abs(float(np.dot(normals_cpu[index], normals_cpu[other])))
            delta = centers_cpu[other] - centers_cpu[index]
            plane_gap = max(
                abs(float(np.dot(normals_cpu[index], delta))),
                abs(float(np.dot(normals_cpu[other], delta))),
            )
            if dot >= max_angle_cos and plane_gap <= tolerance * 2.0:
                union(index, other)
                links += 1

    component_faces: dict[int, int] = {}
    for index, count in enumerate(counts_cpu):
        root = find(index)
        component_faces[root] = component_faces.get(root, 0) + int(count)
    largest = sorted(component_faces.values(), reverse=True)[:10]

    result = {
        "resolution": resolution,
        "cell_size": cp.asnumpy(extent / resolution).tolist(),
        "occupied_cells": len(occupied_ids),
        "planar_cells": len(planar_ids),
        "surface_trajectory_links": int(links),
        "surface_trajectories": len(component_faces),
        "largest_trajectory_face_counts": largest,
        "planar_face_count": int(cp.count_nonzero(face_planar).get()),
        "planar_face_share": float(cp.mean(face_planar).get()),
        "dust_or_spike_face_count": int(cp.count_nonzero(face_outlier).get()),
        "dust_or_spike_face_share": float(cp.mean(face_outlier).get()),
        "area_weighted_mean_normal_coherence": float(
            (cp.sum(coherence * area_sum) / cp.maximum(cp.sum(area_sum), 1e-12)).get()
        ),
        "area_weighted_outlier_share": float(
            (cp.sum(outlier_share * area_sum) / cp.maximum(cp.sum(area_sum), 1e-12)).get()
        ),
        "seconds": time.perf_counter() - started,
    }
    del triangles, edge_a, edge_b, cross, normals, centers
    cp.get_default_memory_pool().free_all_blocks()
    return result, face_planar, face_outlier, face_supported


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--resolutions", default="12,24,48")
    parser.add_argument("--tolerance", type=float, default=0.10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connect_seconds = connected_arrays(triangles)
    load_seconds = time.perf_counter() - started
    points_gpu = cp.asarray(points)
    faces_gpu = cp.asarray(faces)
    report = {
        "input": str(args.input),
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "tolerance": args.tolerance,
        "load_and_connect_seconds": load_seconds,
        "connect_seconds": connect_seconds,
        "scales": [],
    }
    planar_votes = cp.zeros(len(faces), dtype=cp.uint8)
    outlier_votes = cp.zeros(len(faces), dtype=cp.uint8)
    support_votes = cp.zeros(len(faces), dtype=cp.uint8)
    resolutions = [int(value) for value in args.resolutions.split(",")]
    for resolution in resolutions:
        scale, planar, outlier, supported = analyze_scale(
            points_gpu, faces_gpu, resolution, args.tolerance
        )
        planar_votes += planar
        outlier_votes += outlier
        support_votes += supported
        report["scales"].append(scale)
        print(json.dumps(scale, indent=2), flush=True)
    required_votes = max(2, (len(resolutions) + 1) // 2)
    stable_surface = planar_votes >= required_votes
    # A deletion candidate must be anomalous at multiple scales while the surrounding area is
    # repeatedly explained by a coherent tangent surface. Density alone never qualifies it.
    removable_noise = (outlier_votes >= required_votes) & (support_votes >= required_votes)
    cleanup_noise = (outlier_votes >= 1) & (support_votes >= 1)
    consensus = {
        "required_scale_votes": required_votes,
        "stable_surface_triangles": int(cp.count_nonzero(stable_surface).get()),
        "stable_surface_share": float(cp.mean(stable_surface).get()),
        "removable_noise_candidate_triangles": int(cp.count_nonzero(removable_noise).get()),
        "removable_noise_candidate_share": float(cp.mean(removable_noise).get()),
        "cleanup_candidate_triangles": int(cp.count_nonzero(cleanup_noise).get()),
        "cleanup_candidate_share": float(cp.mean(cleanup_noise).get()),
        "feature_or_uncertain_triangles": int(cp.count_nonzero(~stable_surface).get()),
    }
    report["multiscale_consensus"] = consensus
    print(json.dumps({"multiscale_consensus": consensus}, indent=2), flush=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
