"""Benchmark production reducers, including Depth Adaptive QEM, on one resident mesh."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gpu_geometry_prototype import connected_arrays, load_binary_stl

from meshmill import simplify_arrays


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("meshmill-production-candidate-resident-times.json"),
    )
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "samples" / "original-scan.stl"
    points, faces, connectivity_seconds = connected_arrays(load_binary_stl(source))
    target = 250_000
    results = {"connectivity_seconds": connectivity_seconds, "runs": {}}
    for name in (
        "Depth Adaptive QEM",
        "Fast QEM",
        "Density balanced",
        "Shape preserving",
        "Preserve topology",
    ):
        started = time.perf_counter()
        output_points, output_faces = simplify_arrays(points, faces, target, name, 7.0)
        results["runs"][name] = {
            "seconds": time.perf_counter() - started,
            "triangles": len(output_faces),
            "vertices": len(output_points),
        }
    output = args.output
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
