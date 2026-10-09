"""Generate the matched meshes used by the visual algorithm comparison."""

# ruff: noqa: I001

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from meshmill import arrays_polydata, load_stl, save_stl, simplify_arrays


ALGORITHMS = (
    ("Fast QEM", "meshmill-current-fast.stl"),
    ("Density balanced", "meshmill-current-density.stl"),
    ("Shape preserving", "meshmill-current-shape.stl"),
    ("Preserve topology", "meshmill-current-topology.stl"),
    ("Depth Adaptive QEM (GPU / Higher Quality)", "meshmill-depth-adaptive-qem.stl"),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    _poly, points, faces = load_stl(args.input)
    for algorithm, filename in ALGORITHMS:
        destination = args.output / filename
        print(f"{algorithm}: {destination}", flush=True)
        reduced_points, reduced_faces = simplify_arrays(
            points, faces, args.target, algorithm, aggressiveness=8.0
        )
        save_stl(arrays_polydata(reduced_points, reduced_faces), destination)


if __name__ == "__main__":
    main()
