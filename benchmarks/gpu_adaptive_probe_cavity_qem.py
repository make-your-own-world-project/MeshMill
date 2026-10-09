"""Benchmark the existing adaptive-probe analysis with GPU cavity QEM mutation."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from gpu_adaptive_probe_qem import adaptive_probe_projection
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    gpu_qem_reduce,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()

    total_started = time.perf_counter()
    points, faces, connectivity_seconds = connected_arrays(load_binary_stl(args.input))
    projected, probe_report = adaptive_probe_projection(points, faces, args.target)
    out_points, out_faces, mutation = gpu_qem_reduce(
        projected,
        faces,
        args.target,
        max_passes=512,
        scheduling="cavity",
        quarantine_irregular_vertices=False,
        validate_face_orientation=False,
        preserve_boundary_vertices=True,
        placement_mode="optimal",
        area_weighted_quadrics=False,
        prefilter_face_orientation=False,
        candidate_fraction=0.30,
    )
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
        "gpu_adaptive_probes": probe_report,
        "gpu_cavity_mutation": mutation,
        "resident_compute_seconds": probe_report["seconds"] + mutation["total_seconds"],
        "wall_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
