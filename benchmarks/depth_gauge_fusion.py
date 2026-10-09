"""Watertight mesh assembly prototype for the multi-direction depth gauge."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import numpy as np
from cupyx.scipy.ndimage import maximum_filter, minimum_filter
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def axis_bounds(keys, coordinate, line_count):
    low = cp.full(line_count, cp.inf, dtype=cp.float32)
    high = cp.full(line_count, -cp.inf, dtype=cp.float32)
    cp.minimum.at(low, keys, coordinate)
    cp.maximum.at(high, keys, coordinate)
    return low, high


def fill_projection_gaps(low, high, shape):
    low = low.reshape(shape)
    high = high.reshape(shape)
    for _ in range(2):
        missing = ~cp.isfinite(low)
        low = cp.where(missing, minimum_filter(low, size=3, mode="nearest"), low)
        high = cp.where(missing, maximum_filter(high, size=3, mode="nearest"), high)
    return low, high


def visual_hull_gpu(points, longest_resolution):
    started = time.perf_counter()
    gp = cp.asarray(points)
    source_low = cp.min(gp, axis=0)
    source_high = cp.max(gp, axis=0)
    extent = source_high - source_low
    spacing = cp.max(extent) / cp.float32(longest_resolution - 3)
    dims = cp.ceil(extent / spacing).astype(cp.int32) + 3
    low = source_low - spacing
    index = cp.floor((gp - low) / spacing).astype(cp.int32)
    nx, ny, nz = (int(value) for value in cp.asnumpy(dims))
    ix, iy, iz = index[:, 0], index[:, 1], index[:, 2]

    min_x, max_x = axis_bounds(iy + ny * iz, ix, ny * nz)
    min_y, max_y = axis_bounds(ix + nx * iz, iy, nx * nz)
    min_z, max_z = axis_bounds(ix + nx * iy, iz, nx * ny)
    min_x, max_x = fill_projection_gaps(min_x, max_x, (nz, ny))
    min_x, max_x = min_x.T, max_x.T
    min_y, max_y = fill_projection_gaps(min_y, max_y, (nz, nx))
    min_y, max_y = min_y.T, max_y.T
    min_z, max_z = fill_projection_gaps(min_z, max_z, (ny, nx))
    min_z, max_z = min_z.T, max_z.T

    gx = cp.arange(nx, dtype=cp.float32)[:, None, None]
    gy = cp.arange(ny, dtype=cp.float32)[None, :, None]
    gz = cp.arange(nz, dtype=cp.float32)[None, None, :]
    inside_x = (gx >= min_x[None, :, :]) & (gx <= max_x[None, :, :])
    inside_y = (gy >= min_y[:, None, :]) & (gy <= max_y[:, None, :])
    inside_z = (gz >= min_z[:, :, None]) & (gz <= max_z[:, :, None])
    occupied = inside_x & inside_y & inside_z
    occupied[[0, -1], :, :] = False
    occupied[:, [0, -1], :] = False
    occupied[:, :, [0, -1]] = False
    cp.cuda.Stream.null.synchronize()
    return (
        cp.asnumpy(occupied),
        cp.asnumpy(low),
        float(spacing.get()),
        time.perf_counter() - started,
    )


def surface_nets(occupied, low, spacing):
    started = time.perf_counter()
    corners = (
        occupied[:-1, :-1, :-1],
        occupied[1:, :-1, :-1],
        occupied[:-1, 1:, :-1],
        occupied[1:, 1:, :-1],
        occupied[:-1, :-1, 1:],
        occupied[1:, :-1, 1:],
        occupied[:-1, 1:, 1:],
        occupied[1:, 1:, 1:],
    )
    active = np.logical_or.reduce(corners) & ~np.logical_and.reduce(corners)
    cells = np.argwhere(active)
    sums = np.zeros((len(cells), 3), dtype=np.float32)
    counts = np.zeros(len(cells), dtype=np.float32)
    corner_offsets = np.asarray(
        ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
         (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)), dtype=np.float32
    )
    edges = ((0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3),
             (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7))
    cell_corner_values = np.column_stack([corner[active] for corner in corners])
    for left, right in edges:
        crossing = cell_corner_values[:, left] != cell_corner_values[:, right]
        sums[crossing] += (corner_offsets[left] + corner_offsets[right]) * 0.5
        counts[crossing] += 1.0
    vertices = low + (cells + sums / counts[:, None]) * spacing
    vertex_ids = np.full(active.shape, -1, dtype=np.int32)
    vertex_ids[active] = np.arange(len(cells), dtype=np.int32)
    faces = []

    def add_quads(edge_crossing, a, b, c, d):
        mask = edge_crossing & (a >= 0) & (b >= 0) & (c >= 0) & (d >= 0)
        qa, qb, qc, qd = a[mask], b[mask], c[mask], d[mask]
        faces.append(np.column_stack((qa, qb, qc)))
        faces.append(np.column_stack((qa, qc, qd)))

    # Sign-changing grid edges connect the four surrounding cell vertices.
    add_quads(
        occupied[:-1, 1:-1, 1:-1] != occupied[1:, 1:-1, 1:-1],
        vertex_ids[:, :-1, :-1], vertex_ids[:, 1:, :-1],
        vertex_ids[:, 1:, 1:], vertex_ids[:, :-1, 1:],
    )
    add_quads(
        occupied[1:-1, :-1, 1:-1] != occupied[1:-1, 1:, 1:-1],
        vertex_ids[:-1, :, :-1], vertex_ids[:-1, :, 1:],
        vertex_ids[1:, :, 1:], vertex_ids[1:, :, :-1],
    )
    add_quads(
        occupied[1:-1, 1:-1, :-1] != occupied[1:-1, 1:-1, 1:],
        vertex_ids[:-1, :-1, :], vertex_ids[1:, :-1, :],
        vertex_ids[1:, 1:, :], vertex_ids[:-1, 1:, :],
    )
    return (
        vertices.astype(np.float32, copy=False),
        np.concatenate(faces).astype(np.int32, copy=False),
        time.perf_counter() - started,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--resolutions", default="192,256,320")
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    triangles = load_binary_stl(args.input)
    points, faces, connect_seconds = connected_arrays(triangles)
    face_centers = np.mean(points[faces], axis=1, dtype=np.float32)
    samples = np.concatenate((points, face_centers))
    report = {"connectivity_seconds": connect_seconds, "runs": []}
    for resolution in [int(value) for value in args.resolutions.split(",")]:
        occupied, low, spacing, gauge_seconds = visual_hull_gpu(samples, resolution)
        out_points, out_faces, assembly_seconds = surface_nets(occupied, low, spacing)
        run = {
            "resolution": resolution,
            "spacing": spacing,
            "gpu_depth_seconds": gauge_seconds,
            "assembly_seconds": assembly_seconds,
            "total_seconds": gauge_seconds + assembly_seconds,
            "quality": quality_metrics(points, faces, out_points, out_faces, args.sample_count),
        }
        run["quality"].update(topology_metrics(out_faces))
        report["runs"].append(run)
        print(json.dumps(run, indent=2), flush=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
