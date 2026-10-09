"""Adaptive physical-probe surface analysis followed by Fast QEM assembly."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import fast_simplification
import numpy as np
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)


def _bincount(keys, weights, count):
    return cp.bincount(keys, weights=weights, minlength=count).astype(cp.float32)


def physical_probe_dimensions(points, faces, target):
    """Derive the probe body and sampling pitch from source and requested output geometry."""
    sample_faces = faces[:: max(1, len(faces) // 500_000)]
    triangles = points[sample_faces]
    edges = np.concatenate(
        (
            np.linalg.norm(triangles[:, 1] - triangles[:, 0], axis=1),
            np.linalg.norm(triangles[:, 2] - triangles[:, 1], axis=1),
            np.linalg.norm(triangles[:, 0] - triangles[:, 2], axis=1),
        )
    )
    probe_diameter = float(np.median(edges[edges > 1e-12]))
    area = 0.5 * np.linalg.norm(
        np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]), axis=1
    ).sum() * (len(faces) / len(sample_faces))
    output_pitch = float(np.sqrt(4.0 * area / (np.sqrt(3.0) * target)))
    return {
        "diameter": probe_diameter,
        "tip_radius": probe_diameter * 0.5,
        "minimum_pitch": max(output_pitch, probe_diameter),
    }


def adaptive_probe_projection(points, faces, target):
    """Use the coarsest locally valid probe spacing, refining only around unresolved form."""
    started = time.perf_counter()
    physical = physical_probe_dimensions(points, faces, target)
    tip_radius = physical["tip_radius"]
    displacement_cap = tip_radius * 0.25
    pitches = [physical["minimum_pitch"] * factor for factor in (8.0, 4.0, 2.0, 1.0)]

    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    triangles = gp[gf]
    cross = cp.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    twice_area = cp.linalg.norm(cross, axis=1)
    face_normals = cross / cp.maximum(twice_area[:, None], cp.float32(1e-12))
    centers = cp.mean(triangles, axis=1)
    weights = twice_area * cp.float32(0.5)
    low = cp.min(gp, axis=0)
    high = cp.max(gp, axis=0)
    vertex_delta = cp.zeros_like(gp)
    vertex_weight = cp.zeros(len(points), dtype=cp.float32)
    unresolved = cp.ones(len(faces), dtype=cp.bool_)
    level_stats = []

    for pitch in pitches:
        dims = cp.maximum(cp.ceil((high - low) / pitch).astype(cp.int64) + 1, 1)
        cell = cp.floor((centers - low) / pitch).astype(cp.int64)
        raw_keys = cell[:, 0] + dims[0] * (cell[:, 1] + dims[1] * cell[:, 2])
        _occupied_keys, keys = cp.unique(raw_keys, return_inverse=True)
        cell_count = int(cp.max(keys).get()) + 1
        area_sum = _bincount(keys, weights, cell_count)
        weighted_normal = cp.stack(
            [_bincount(keys, weights * face_normals[:, axis], cell_count) for axis in range(3)],
            axis=1,
        )
        normal_length = cp.linalg.norm(weighted_normal, axis=1)
        mean_normal = weighted_normal / cp.maximum(normal_length[:, None], cp.float32(1e-12))
        coherence = normal_length / cp.maximum(area_sum, cp.float32(1e-12))
        mean_center = cp.stack(
            [_bincount(keys, weights * centers[:, axis], cell_count) for axis in range(3)], axis=1
        ) / cp.maximum(area_sum[:, None], cp.float32(1e-12))
        local_normal = mean_normal[keys]
        local_center = mean_center[keys]
        residual = cp.abs(cp.sum(local_normal * (centers - local_center), axis=1))

        residual_mean = _bincount(keys, weights * residual, cell_count) / cp.maximum(
            area_sum, cp.float32(1e-12)
        )
        residual_sq = _bincount(keys, weights * residual * residual, cell_count) / cp.maximum(
            area_sum, cp.float32(1e-12)
        )
        residual_sigma = cp.sqrt(cp.maximum(residual_sq - residual_mean * residual_mean, 0.0))
        inlier = residual <= cp.maximum(
            residual_mean[keys] + cp.float32(2.5) * residual_sigma[keys],
            cp.float32(tip_radius),
        )
        inlier_weight = weights * inlier
        inlier_area = _bincount(keys, inlier_weight, cell_count)
        clipped_rms = cp.sqrt(
            _bincount(keys, inlier_weight * residual * residual, cell_count)
            / cp.maximum(inlier_area, cp.float32(1e-12))
        )
        # A wide probe interval is valid only when its normals agree and the fitted surface stays
        # inside the spherical tip's physical radius. Other faces proceed to the next denser level.
        maximum_angle = np.arctan2(tip_radius, pitch * 0.5)
        coherence_limit = float(np.cos(maximum_angle))
        valid_cell = (coherence >= cp.float32(coherence_limit)) & (
            clipped_rms <= cp.float32(tip_radius)
        )
        assigned = unresolved & valid_cell[keys]
        # The spherical end ignores supported excursions smaller than its diameter. Only those
        # excursions are projected; ordinary faces define the trajectory and remain unchanged.
        dust = assigned & (residual > cp.float32(tip_radius * 0.5)) & (
            residual <= cp.float32(tip_radius * 1.5)
        )
        flat_vertices = gf[dust].ravel()
        if int(cp.count_nonzero(dust).get()):
            selected_triangles = triangles[dust]
            selected_normal = local_normal[dust]
            selected_center = local_center[dust]
            selected_weight = weights[dust]
            signed = cp.sum(
                (selected_triangles - selected_center[:, None, :])
                * selected_normal[:, None, :],
                axis=2,
            )
            repeated_weight = cp.repeat(selected_weight, 3)
            for axis in range(3):
                delta = -signed * selected_normal[:, None, axis]
                vertex_delta[:, axis] += _bincount(
                    flat_vertices, repeated_weight * delta.ravel(), len(points)
                )
            vertex_weight += _bincount(flat_vertices, repeated_weight, len(points))
        assigned_keys = cp.unique(keys[assigned])
        level_stats.append(
            {
                "pitch": float(pitch),
                "maximum_normal_angle_degrees": float(np.degrees(maximum_angle)),
                "coherence_limit": coherence_limit,
                "assigned_faces": int(cp.count_nonzero(assigned).get()),
                "probe_count": len(assigned_keys),
                "projected_outlier_faces": int(cp.count_nonzero(dust).get()),
            }
        )
        unresolved &= ~assigned

    delta = vertex_delta / cp.maximum(vertex_weight[:, None], cp.float32(1e-12))
    length = cp.linalg.norm(delta, axis=1)
    delta *= cp.minimum(1.0, cp.float32(displacement_cap) / cp.maximum(length, 1e-12))[:, None]
    projected = gp + delta
    cp.cuda.Stream.null.synchronize()
    report = {
        "seconds": time.perf_counter() - started,
        "probe_geometry": {
            **physical,
            "maximum_pitch": pitches[0],
            "displacement_cap": displacement_cap,
        },
        "levels": level_stats,
        "unresolved_faces": int(cp.count_nonzero(unresolved).get()),
        "moved_vertex_share": float(cp.mean(length > 1e-6).get()),
        "mean_displacement": float(cp.mean(cp.minimum(length, displacement_cap)).get()),
        "max_displacement": float(cp.max(cp.minimum(length, displacement_cap)).get()),
    }
    return cp.asnumpy(projected).astype(np.float32, copy=False), report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--aggressiveness", type=float, default=5.0)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    total_started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    projected, probe_report = adaptive_probe_projection(points, faces, args.target)
    reduction_started = time.perf_counter()
    out_points, out_faces = fast_simplification.simplify(
        projected,
        faces,
        target_count=args.target,
        agg=args.aggressiveness,
        verbose=False,
        preserve_border=True,
    )
    reduction_seconds = time.perf_counter() - reduction_started
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
        "cpu_qem_seconds": reduction_seconds,
        "aggressiveness": args.aggressiveness,
        "resident_compute_seconds": probe_report["seconds"] + reduction_seconds,
        "total_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
