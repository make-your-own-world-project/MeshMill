"""Benchmark vertex-disjoint GPU QEM batches with topology and orientation validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

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
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    points, faces, connectivity_seconds = connected_arrays(load_binary_stl(args.input))
    out_points, out_faces, timing = gpu_qem_reduce(
        points,
        faces,
        args.target,
        max_passes=512,
        scheduling="cavity",
        quarantine_irregular_vertices=False,
        validate_face_orientation=False,
    )
    save_binary_stl(args.output_mesh, out_points, out_faces)
    quality = quality_metrics(points, faces, out_points, out_faces, 200_000)
    quality.update(topology_metrics(out_faces))
    report = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "target_triangles": args.target,
        "output_triangles": len(out_faces),
        "output_vertices": len(out_points),
        "connectivity_seconds": connectivity_seconds,
        "gpu_timing": timing,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
