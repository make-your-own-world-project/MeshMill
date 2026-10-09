"""GPU multi-direction depth-gauge surface reconstruction experiment.

Each view projects the mesh into a regular bank of parallel probes. The first supported hit is
retained, isolated protrusions are replaced by the neighborhood surface, and adjacent probe tips
are connected into surface sheets. This is benchmark code, not an application backend.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import numpy as np
from cupyx.scipy.ndimage import median_filter
from gpu_geometry_prototype import connected_arrays, load_binary_stl
from scipy.spatial import Delaunay, cKDTree

AXIS_VIEWS = (
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((0, 1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (1, 0, 0), (0, 1, 0)),
)


def make_views(count):
    views = list(AXIS_VIEWS)
    if count == 6:
        return views
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                direction = np.asarray((sx, sy, sz), dtype=np.float32)
                direction /= np.linalg.norm(direction)
                reference = np.asarray((0.0, 0.0, 1.0), dtype=np.float32)
                axis_u = np.cross(reference, direction)
                axis_u /= np.linalg.norm(axis_u)
                axis_v = np.cross(direction, axis_u)
                views.append((tuple(direction), tuple(axis_u), tuple(axis_v)))
    return views


def probe_view(points, direction, axis_u, axis_v, resolution, support, noise_depth):
    direction = cp.asarray(direction, dtype=cp.float32)
    axis_u = cp.asarray(axis_u, dtype=cp.float32)
    axis_v = cp.asarray(axis_v, dtype=cp.float32)
    # Elementwise dot products avoid making this prototype depend on a separate cuBLAS runtime.
    u = cp.sum(points * axis_u[None, :], axis=1)
    v = cp.sum(points * axis_v[None, :], axis=1)
    depth = cp.sum(points * direction[None, :], axis=1)
    low_u, high_u = cp.min(u), cp.max(u)
    low_v, high_v = cp.min(v), cp.max(v)
    span_u = cp.maximum(high_u - low_u, cp.float32(1e-12))
    span_v = cp.maximum(high_v - low_v, cp.float32(1e-12))
    ix = cp.clip(cp.floor((u - low_u) / span_u * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
    iy = cp.clip(cp.floor((v - low_v) / span_v * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
    keys = ix + resolution * iy
    gauge = cp.full(resolution * resolution, cp.inf, dtype=cp.float32)
    cp.minimum.at(gauge, keys, depth)
    gauge = gauge.reshape(resolution, resolution)
    valid = cp.isfinite(gauge)

    # Median support behaves like neighboring pins linked by a flexible surface. An isolated first
    # hit is dust; a supported run of hits is retained as geometry.
    finite_high = cp.max(depth) + cp.ptp(depth)
    median = median_filter(cp.where(valid, gauge, finite_high), size=support, mode="nearest")
    isolated = valid & (median - gauge > noise_depth)
    # Preserve the six outer support points so cleanup cannot shrink the object's dimensions.
    isolated.ravel()[keys[cp.argmin(depth)]] = False
    filtered = cp.where(isolated, median, gauge)
    valid &= cp.isfinite(filtered) & (filtered < finite_high)

    yy, xx = cp.meshgrid(cp.arange(resolution), cp.arange(resolution), indexing="ij")
    sample_u = low_u + xx.astype(cp.float32) / (resolution - 1) * span_u
    sample_v = low_v + yy.astype(cp.float32) / (resolution - 1) * span_v
    # Preserve the exact lateral coordinates of the winning first hit. The grid chooses which
    # probe owns the sample; it does not quantize the retained surface point to the cell center.
    winning = cp.flatnonzero(depth == gauge.ravel()[keys])
    sample_u.ravel()[keys[winning]] = u[winning]
    sample_v.ravel()[keys[winning]] = v[winning]
    reconstructed = (
        filtered[..., None] * direction
        + sample_u[..., None] * axis_u
        + sample_v[..., None] * axis_v
    )
    local_surface = median_filter(cp.where(valid, filtered, finite_high), size=3, mode="nearest")
    feature_score = cp.where(valid, cp.abs(filtered - local_surface), cp.float32(-1.0))
    return reconstructed, valid, isolated, feature_score, float(max(float(span_u.get()), float(span_v.get())) / (resolution - 1))


def connect_sheet(points, valid, jump_limit):
    points = cp.asnumpy(points)
    valid = cp.asnumpy(valid)
    height, width = valid.shape
    ids = np.full((height, width), -1, dtype=np.int32)
    ids[valid] = np.arange(np.count_nonzero(valid), dtype=np.int32)
    compact = points[valid].astype(np.float32, copy=False)
    a = ids[:-1, :-1]
    b = ids[:-1, 1:]
    c = ids[1:, :-1]
    d = ids[1:, 1:]
    first = np.column_stack((a.ravel(), c.ravel(), b.ravel()))
    second = np.column_stack((b.ravel(), c.ravel(), d.ravel()))
    faces = np.concatenate((first, second))
    faces = faces[np.all(faces >= 0, axis=1)]
    tri = compact[faces]
    edge_max = np.maximum.reduce(
        (
            np.linalg.norm(tri[:, 0] - tri[:, 1], axis=1),
            np.linalg.norm(tri[:, 1] - tri[:, 2], axis=1),
            np.linalg.norm(tri[:, 2] - tri[:, 0], axis=1),
        )
    )
    return compact, faces[edge_max <= jump_limit].astype(np.int32, copy=False)


def connect_adaptive_sheet(points, valid, feature_score, jump_limit, point_budget):
    points = cp.asnumpy(points)
    valid = cp.asnumpy(valid)
    score = cp.asnumpy(feature_score)
    coords = np.argwhere(valid)
    if len(coords) <= point_budget:
        return connect_sheet(cp.asarray(points), cp.asarray(valid), jump_limit)
    valid_flat = np.flatnonzero(valid)
    ranked = valid_flat[np.argpartition(score.ravel()[valid_flat], -point_budget)[-point_budget:]]
    # Reserve part of the budget for uniform coverage, then spend the rest on curvature.
    stride = max(2, int(np.sqrt(len(coords) / max(1, point_budget // 2))))
    uniform_mask = valid.copy()
    yy, xx = np.indices(valid.shape)
    uniform_mask &= (yy % stride == 0) & (xx % stride == 0)
    chosen = set(np.flatnonzero(uniform_mask).tolist())
    flat_points = points.reshape(-1, 3)
    for axis in range(3):
        chosen.add(int(valid_flat[np.argmin(flat_points[valid_flat, axis])]))
        chosen.add(int(valid_flat[np.argmax(flat_points[valid_flat, axis])]))
    for index in ranked[np.argsort(score.ravel()[ranked])[::-1]]:
        if len(chosen) >= point_budget:
            break
        chosen.add(int(index))
    selected = np.asarray(sorted(chosen), dtype=np.int64)
    selected_coords = np.column_stack(np.unravel_index(selected, valid.shape))
    compact = points.reshape(-1, 3)[selected].astype(np.float32, copy=False)
    faces = Delaunay(selected_coords[:, ::-1]).simplices.astype(np.int32, copy=False)
    tri = compact[faces]
    edge_max = np.maximum.reduce(
        (
            np.linalg.norm(tri[:, 0] - tri[:, 1], axis=1),
            np.linalg.norm(tri[:, 1] - tri[:, 2], axis=1),
            np.linalg.norm(tri[:, 2] - tri[:, 0], axis=1),
        )
    )
    return compact, faces[edge_max <= jump_limit]


def reconstruct(points, probe_samples, views, resolution, support, noise_depth, target):
    started = time.perf_counter()
    gp = cp.asarray(probe_samples)
    parts = []
    isolated_total = 0
    spacing = 0.0
    for direction, axis_u, axis_v in views:
        sheet, valid, isolated, feature_score, view_spacing = probe_view(
            gp, direction, axis_u, axis_v, resolution, support, noise_depth
        )
        cp.cuda.Stream.null.synchronize()
        spacing = max(spacing, view_spacing)
        isolated_total += int(cp.count_nonzero(isolated).get())
        jump_limit = max(noise_depth * 8.0, view_spacing * 5.0)
        if target:
            parts.append(
                connect_adaptive_sheet(
                    sheet,
                    valid,
                    feature_score,
                    jump_limit,
                    point_budget=max(100, target // (2 * len(views))),
                )
            )
        else:
            parts.append(connect_sheet(sheet, valid, jump_limit=jump_limit))
    offset = 0
    all_points, all_faces = [], []
    for part_points, part_faces in parts:
        all_points.append(part_points)
        all_faces.append(part_faces + offset)
        offset += len(part_points)
    return (
        np.concatenate(all_points),
        np.concatenate(all_faces),
        {
            "seconds": time.perf_counter() - started,
            "probe_spacing": spacing,
            "isolated_probe_hits_removed": isolated_total,
        },
    )


def quality(source, output, sample_count):
    rng = np.random.default_rng(20261005)
    sample = source[rng.choice(len(source), min(sample_count, len(source)), replace=False)]
    distances, _ = cKDTree(output).query(sample, workers=-1)
    source_size = np.ptp(source, axis=0)
    output_size = np.ptp(output, axis=0)
    return {
        "dimension_drift": np.abs(output_size - source_size).tolist(),
        "sample_nearest_vertex_rms": float(np.sqrt(np.mean(distances * distances))),
        "sample_nearest_vertex_p95": float(np.percentile(distances, 95)),
        "sample_nearest_vertex_max": float(np.max(distances)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--resolutions", default="256,384,512")
    parser.add_argument("--support", type=int, default=3)
    parser.add_argument("--views", type=int, choices=(6, 14), default=6)
    parser.add_argument("--noise-depth", type=float, default=0.35)
    parser.add_argument("--target", type=int)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    triangles = load_binary_stl(args.input)
    points, faces, connect_seconds = connected_arrays(triangles)
    face_centers = np.mean(points[faces], axis=1, dtype=np.float32)
    probe_samples = np.concatenate((points, face_centers))
    views = make_views(args.views)
    report = {
        "source_triangles": len(faces),
        "source_vertices": len(points),
        "connectivity_seconds": connect_seconds,
        "views": len(views),
        "support": args.support,
        "noise_depth": args.noise_depth,
        "runs": [],
    }
    for resolution in [int(value) for value in args.resolutions.split(",")]:
        out_points, out_faces, timing = reconstruct(
            points,
            probe_samples,
            views,
            resolution,
            args.support,
            args.noise_depth,
            args.target,
        )
        run = {
            "resolution": resolution,
            "output_vertices": len(out_points),
            "output_triangles": len(out_faces),
            "timing": timing,
            "quality": quality(points, out_points, args.sample_count),
        }
        report["runs"].append(run)
        print(json.dumps(run, indent=2), flush=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
