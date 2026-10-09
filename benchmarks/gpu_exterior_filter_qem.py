"""Prototype GPU exterior-surface filtering followed by adaptive probes and Fast QEM."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import fast_simplification
from depth_gauge_prefilter_qem import compact, visible_faces_gpu
from depth_gauge_prototype import make_views
from gpu_adaptive_probe_qem import adaptive_probe_projection
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--resolution", type=int, default=512)
    parser.add_argument("--depth-tolerance", type=float, default=0.05)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--preserve-border", action="store_true")
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()

    total_started = time.perf_counter()
    points, faces, connectivity_seconds = connected_arrays(load_binary_stl(args.input))
    visible, filter_seconds = visible_faces_gpu(
        points,
        faces,
        make_views(14),
        args.resolution,
        args.depth_tolerance,
    )
    compact_started = time.perf_counter()
    filtered_points, filtered_faces = compact(points, faces[visible])
    compact_seconds = time.perf_counter() - compact_started

    projected, probe_report = adaptive_probe_projection(
        filtered_points, filtered_faces, args.target
    )
    qem_started = time.perf_counter()
    output_points, output_faces = fast_simplification.simplify(
        projected,
        filtered_faces,
        target_count=args.target,
        agg=5.0,
        verbose=False,
        preserve_border=args.preserve_border,
    )
    qem_seconds = time.perf_counter() - qem_started
    save_binary_stl(args.output_mesh, output_points, output_faces)

    quality = quality_metrics(
        points, faces, output_points, output_faces, args.sample_count
    )
    quality.update(topology_metrics(output_faces))
    report = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "retained_triangles": len(filtered_faces),
        "retained_vertices": len(filtered_points),
        "removed_triangles": int(len(faces) - len(filtered_faces)),
        "removed_percent": float(100.0 * (1.0 - len(filtered_faces) / len(faces))),
        "target_triangles": args.target,
        "output_triangles": len(output_faces),
        "output_vertices": len(output_points),
        "resolution": args.resolution,
        "depth_tolerance": args.depth_tolerance,
        "preserve_border": args.preserve_border,
        "connectivity_seconds": connectivity_seconds,
        "gpu_filter_seconds": filter_seconds,
        "cpu_compact_seconds": compact_seconds,
        "gpu_adaptive_probes": probe_report,
        "cpu_qem_seconds": qem_seconds,
        "resident_compute_seconds": (
            filter_seconds
            + compact_seconds
            + probe_report["seconds"]
            + qem_seconds
        ),
        "wall_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
