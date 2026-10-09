"""End-to-end GPU QEM prototype with indexed-mesh assembly and CPU baseline."""

from __future__ import annotations

import argparse
import json
import struct
import time
from pathlib import Path

import fast_simplification
import numpy as np
from gpu_geometry_prototype import (
    connected_arrays,
    gpu_qem_reduce,
    load_binary_stl,
    quality_metrics,
)


def save_binary_stl(path, points, faces):
    triangles = points[faces].astype(np.float32, copy=False)
    normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    lengths = np.linalg.norm(normals, axis=1)
    normals /= np.maximum(lengths[:, None], 1e-20)
    record = np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attr", "<u2")])
    output = np.zeros(len(faces), dtype=record)
    output["normal"] = normals
    output["vertices"] = triangles
    with path.open("wb") as stream:
        stream.write(b"MeshMill GPU QEM prototype".ljust(80, b"\0"))
        stream.write(struct.pack("<I", len(faces)))
        output.tofile(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)

    gpu_points, gpu_faces, gpu_timing = gpu_qem_reduce(
        points, faces, args.target, max_passes=512, scheduling="priority"
    )
    save_binary_stl(args.output_mesh, gpu_points, gpu_faces)

    started = time.perf_counter()
    cpu_points, cpu_faces = fast_simplification.simplify(
        points, faces, target_count=args.target, agg=7.0, verbose=False, preserve_border=True
    )
    cpu_seconds = time.perf_counter() - started
    report = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "target_triangles": args.target,
        "connectivity_seconds": connectivity_seconds,
        "gpu": {
            "timing": gpu_timing,
            "quality": quality_metrics(points, faces, gpu_points, gpu_faces, args.sample_count),
            "output_mesh": str(args.output_mesh),
        },
        "cpu_fast_qem": {
            "timing": {"total_seconds": cpu_seconds},
            "quality": quality_metrics(points, faces, cpu_points, cpu_faces, args.sample_count),
        },
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
