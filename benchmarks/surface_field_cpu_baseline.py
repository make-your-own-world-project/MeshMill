"""CPU timing baseline for the GPU surface-field prototype's numeric core."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
from gpu_geometry_prototype import connected_arrays, load_binary_stl


def bins(keys, weights, count):
    return np.bincount(keys, weights=weights, minlength=count).astype(np.float32)


def analyze(points, faces, resolution, tolerance):
    started = time.perf_counter()
    triangles = points[faces]
    cross = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    twice_area = np.linalg.norm(cross, axis=1)
    valid = twice_area > 1e-12
    normals = cross / np.maximum(twice_area[:, None], 1e-12)
    centers = np.mean(triangles, axis=1)
    weights = twice_area * 0.5
    low = np.min(points, axis=0)
    extent = np.maximum(np.max(points, axis=0) - low, 1e-12)
    cells = np.floor((centers - low) / extent * resolution).astype(np.int32)
    cells = np.clip(cells, 0, resolution - 1)
    keys = cells[:, 0] + resolution * (cells[:, 1] + resolution * cells[:, 2])
    count = resolution ** 3
    area = bins(keys, weights, count)
    face_count = np.bincount(keys, minlength=count)
    weighted_normal = np.stack(
        [bins(keys, weights * normals[:, axis], count) for axis in range(3)], axis=1
    )
    length = np.linalg.norm(weighted_normal, axis=1)
    mean_normal = weighted_normal / np.maximum(length[:, None], 1e-12)
    coherence = length / np.maximum(area, 1e-12)
    mean_center = np.stack(
        [bins(keys, weights * centers[:, axis], count) for axis in range(3)], axis=1
    ) / np.maximum(area[:, None], 1e-12)
    residual = np.abs(np.sum(mean_normal[keys] * (centers - mean_center[keys]), axis=1))
    residual_mean = bins(keys, weights * residual, count) / np.maximum(area, 1e-12)
    residual_sq = bins(keys, weights * residual * residual, count) / np.maximum(area, 1e-12)
    sigma = np.sqrt(np.maximum(residual_sq - residual_mean * residual_mean, 0.0))
    inlier = valid & (residual <= np.maximum(residual_mean[keys] + 2.5 * sigma[keys], tolerance))
    inlier_weight = weights * inlier
    inlier_area = bins(keys, inlier_weight, count)
    clipped_rms = np.sqrt(
        bins(keys, inlier_weight * residual * residual, count) / np.maximum(inlier_area, 1e-12)
    )
    occupied = face_count > 0
    planar = occupied & (coherence >= 0.995) & (clipped_rms <= tolerance)
    return {
        "resolution": resolution,
        "seconds": time.perf_counter() - started,
        "planar_face_count": int(np.count_nonzero(planar[keys])),
        "outlier_face_count": int(np.count_nonzero(~inlier)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--resolutions", default="24,48,72")
    parser.add_argument("--tolerance", type=float, default=0.20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    triangles = load_binary_stl(args.input)
    points, faces, _ = connected_arrays(triangles)
    runs = [
        analyze(points, faces, int(value), args.tolerance)
        for value in args.resolutions.split(",")
    ]
    result = {"backend": "numpy_cpu", "runs": runs, "total_seconds": sum(x["seconds"] for x in runs)}
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
