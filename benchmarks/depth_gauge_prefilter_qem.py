"""Use GPU depth gauges to remove hidden redundant layers before topology-preserving Fast QEM."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import fast_simplification
import numpy as np
from depth_gauge_prototype import make_views
from gpu_geometry_prototype import connected_arrays, load_binary_stl, quality_metrics
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def visible_faces_gpu(points, faces, views, resolution, depth_tolerance):
    started = time.perf_counter()
    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    centers = cp.mean(gp[gf], axis=1)
    visible = cp.zeros(len(faces), dtype=cp.bool_)
    for direction, axis_u, axis_v in views:
        d = cp.asarray(direction, dtype=cp.float32)
        u_axis = cp.asarray(axis_u, dtype=cp.float32)
        v_axis = cp.asarray(axis_v, dtype=cp.float32)
        u = cp.sum(gp * u_axis[None, :], axis=1)
        v = cp.sum(gp * v_axis[None, :], axis=1)
        depth = cp.sum(gp * d[None, :], axis=1)
        low_u, high_u = cp.min(u), cp.max(u)
        low_v, high_v = cp.min(v), cp.max(v)
        span_u = cp.maximum(high_u - low_u, 1e-12)
        span_v = cp.maximum(high_v - low_v, 1e-12)
        ix = cp.clip(cp.floor((u - low_u) / span_u * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
        iy = cp.clip(cp.floor((v - low_v) / span_v * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
        gauge = cp.full(resolution * resolution, cp.inf, dtype=cp.float32)
        cp.minimum.at(gauge, ix + resolution * iy, depth)

        center_u = cp.sum(centers * u_axis[None, :], axis=1)
        center_v = cp.sum(centers * v_axis[None, :], axis=1)
        center_depth = cp.sum(centers * d[None, :], axis=1)
        center_x = cp.clip(cp.floor((center_u - low_u) / span_u * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
        center_y = cp.clip(cp.floor((center_v - low_v) / span_v * (resolution - 1)), 0, resolution - 1).astype(cp.int32)
        first_hit = gauge[center_x + resolution * center_y]
        visible |= center_depth <= first_hit + depth_tolerance
    cp.cuda.Stream.null.synchronize()
    return cp.asnumpy(visible), time.perf_counter() - started


def compact(points, faces):
    used, inverse = np.unique(faces.reshape(-1), return_inverse=True)
    return points[used], inverse.reshape(-1, 3).astype(np.int32, copy=False)


def keep_supported_components(vertex_count, faces, visible, minimum_visible_share):
    rows = np.concatenate((faces[:, 0], faces[:, 1], faces[:, 2]))
    cols = np.concatenate((faces[:, 1], faces[:, 2], faces[:, 0]))
    graph = coo_matrix(
        (np.ones(len(rows), dtype=np.uint8), (rows, cols)),
        shape=(vertex_count, vertex_count),
    ).tocsr()
    component_count, labels = connected_components(graph, directed=False)
    face_component = labels[faces[:, 0]]
    totals = np.bincount(face_component, minlength=component_count)
    visible_totals = np.bincount(
        face_component, weights=visible.astype(np.uint8), minlength=component_count
    )
    share = visible_totals / np.maximum(totals, 1)
    keep_component = share >= minimum_visible_share
    return keep_component[face_component], component_count, int(np.count_nonzero(keep_component))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--views", type=int, choices=(6, 14), default=14)
    parser.add_argument("--resolution", type=int, default=512)
    parser.add_argument("--depth-tolerance", type=float, default=1.0)
    parser.add_argument("--component-visible-share", type=float, default=0.05)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    triangles = load_binary_stl(args.input)
    points, faces, connect_seconds = connected_arrays(triangles)
    visible, gauge_seconds = visible_faces_gpu(
        points, faces, make_views(args.views), args.resolution, args.depth_tolerance
    )
    keep, component_count, kept_components = keep_supported_components(
        len(points), faces, visible, args.component_visible_share
    )
    filtered_points, filtered_faces = compact(points, faces[keep])
    qem_started = time.perf_counter()
    output_points, output_faces = fast_simplification.simplify(
        filtered_points,
        filtered_faces,
        target_count=args.target,
        agg=7.0,
        verbose=False,
        preserve_border=True,
    )
    qem_seconds = time.perf_counter() - qem_started
    report = {
        "views": args.views,
        "resolution": args.resolution,
        "depth_tolerance": args.depth_tolerance,
        "source_triangles": len(faces),
        "visible_triangles": int(np.count_nonzero(visible)),
        "connected_components": component_count,
        "kept_components": kept_components,
        "whole_component_triangles_removed": int(np.count_nonzero(~keep)),
        "gpu_gauge_seconds": gauge_seconds,
        "cpu_qem_seconds": qem_seconds,
        "total_reduction_seconds": gauge_seconds + qem_seconds,
        "connectivity_seconds": connect_seconds,
        "quality": quality_metrics(
            points, faces, output_points, output_faces, args.sample_count
        ),
    }
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
