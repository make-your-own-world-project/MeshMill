"""Allocate triangle quotas from adaptive probes and weld independently reduced regions."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import fast_simplification
import numpy as np
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)
from gpu_probe_budget_qem import adaptive_budget_field


def compact(points, faces):
    used, inverse = np.unique(faces.ravel(), return_inverse=True)
    return points[used], inverse.reshape(-1, 3).astype(np.int32, copy=False)


def weld(points_parts, faces_parts):
    points = np.concatenate(points_parts)
    offsets = np.cumsum([0] + [len(part) for part in points_parts[:-1]], dtype=np.int64)
    faces = np.concatenate([part + offset for part, offset in zip(faces_parts, offsets)])
    # Pinned interfaces retain bit-identical source coordinates. Exact welding restores their shared
    # indexed vertices without introducing a distance-based merge across neighboring surface sheets.
    unique_points, inverse = np.unique(points, axis=0, return_inverse=True)
    faces = inverse[faces]
    valid = (faces[:, 0] != faces[:, 1]) & (faces[:, 1] != faces[:, 2]) & (
        faces[:, 2] != faces[:, 0]
    )
    faces = faces[valid]
    canonical = np.sort(faces, axis=1)
    _, first = np.unique(canonical, axis=0, return_index=True)
    return unique_points.astype(np.float32, copy=False), faces[np.sort(first)].astype(np.int32)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    total_started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    _vertex_budget, levels, probe_report = adaptive_budget_field(points, faces, args.target)

    density = np.asarray((0.125, 0.25, 0.5, 1.0, 1.5), dtype=np.float64)
    counts = np.bincount(levels, minlength=len(density))
    weighted = counts * density
    raw_targets = args.target * weighted / weighted.sum()
    targets = np.maximum(4, np.rint(raw_targets).astype(np.int64))
    # Correct rounding while favoring the most detailed regions.
    difference = int(args.target - targets.sum())
    for level in np.argsort(-density):
        if difference == 0:
            break
        adjustment = difference if difference > 0 else -min(targets[level] - 4, -difference)
        targets[level] += adjustment
        difference -= int(adjustment)

    reduce_started = time.perf_counter()
    point_parts = []
    face_parts = []
    region_stats = []
    for level in range(len(density)):
        selected = faces[levels == level]
        region_points, region_faces = compact(points, selected)
        requested = min(int(targets[level]), len(region_faces))
        if requested < len(region_faces):
            out_points, out_faces = fast_simplification.simplify(
                region_points,
                region_faces,
                target_count=requested,
                agg=5.0,
                verbose=False,
                preserve_border=True,
            )
        else:
            out_points, out_faces = region_points, region_faces
        point_parts.append(out_points)
        face_parts.append(out_faces)
        region_stats.append(
            {
                "level": level,
                "density_weight": float(density[level]),
                "input_triangles": len(region_faces),
                "requested_triangles": requested,
                "output_triangles": len(out_faces),
            }
        )
    reduction_seconds = time.perf_counter() - reduce_started
    weld_started = time.perf_counter()
    out_points, out_faces = weld(point_parts, face_parts)
    weld_seconds = time.perf_counter() - weld_started
    reconciled_input_triangles = len(out_faces)
    reconciliation_started = time.perf_counter()
    if len(out_faces) > args.target:
        out_points, out_faces = fast_simplification.simplify(
            out_points,
            out_faces,
            target_count=args.target,
            agg=5.0,
            verbose=False,
            preserve_border=True,
        )
    reconciliation_seconds = time.perf_counter() - reconciliation_started
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
        "gpu_probe_budget": probe_report,
        "regions": region_stats,
        "cpu_partitioned_qem_seconds": reduction_seconds,
        "weld_seconds": weld_seconds,
        "reconciliation_input_triangles": reconciled_input_triangles,
        "global_reconciliation_seconds": reconciliation_seconds,
        "resident_compute_seconds": (
            probe_report["seconds"] + reduction_seconds + weld_seconds + reconciliation_seconds
        ),
        "total_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
