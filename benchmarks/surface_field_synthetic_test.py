"""Controlled test for the surface-field noise classifier."""

from __future__ import annotations

import json
import time

import cupy as cp
import numpy as np
from surface_field_prototype import analyze_scale


def grid_mesh(size: int = 360):
    axis = np.linspace(-90.0, 90.0, size, dtype=np.float32)
    x, y = np.meshgrid(axis, axis, indexing="xy")
    rng = np.random.default_rng(20261005)
    z = rng.normal(0.0, 0.008, x.shape).astype(np.float32)
    dust_vertices = np.zeros(x.shape, dtype=bool)
    for center_x, center_y, height in rng.uniform(
        [-80.0, -80.0, 0.15], [80.0, 80.0, 0.45], size=(90, 3)
    ):
        radius_sq = (x - center_x) ** 2 + (y - center_y) ** 2
        bump = height * np.exp(-radius_sq / (2.0 * 0.38 ** 2))
        z += bump.astype(np.float32)
        dust_vertices |= bump > 0.035

    # A broad, intentional raised feature. Its coherent sides and transitions should not be
    # treated like isolated dust even though it departs from the base plane.
    feature = (x > 15.0) & (x < 60.0) & (y > -25.0) & (y < 25.0)
    blend_x = np.minimum((x - 15.0) / 4.0, (60.0 - x) / 4.0)
    blend_y = np.minimum((y + 25.0) / 4.0, (25.0 - y) / 4.0)
    blend = np.clip(np.minimum(blend_x, blend_y), 0.0, 1.0)
    z += (3.0 * blend).astype(np.float32)

    points = np.column_stack((x.ravel(), y.ravel(), z.ravel())).astype(np.float32)
    rows = np.arange(size - 1)[:, None]
    cols = np.arange(size - 1)[None, :]
    upper_left = (rows * size + cols).ravel()
    lower_left = upper_left + size
    faces = np.concatenate(
        (
            np.column_stack((upper_left, lower_left, upper_left + 1)),
            np.column_stack((upper_left + 1, lower_left, lower_left + 1)),
        )
    ).astype(np.int32)
    dust_faces = dust_vertices.ravel()[faces].any(axis=1)
    feature_faces = feature.ravel()[faces].any(axis=1)
    return points, faces, dust_faces, feature_faces


def main() -> int:
    points, faces, dust_truth, feature_truth = grid_mesh()
    gp, gf = cp.asarray(points), cp.asarray(faces)
    planar_votes = cp.zeros(len(faces), dtype=cp.uint8)
    outlier_votes = cp.zeros(len(faces), dtype=cp.uint8)
    support_votes = cp.zeros(len(faces), dtype=cp.uint8)
    started = time.perf_counter()
    for resolution in (18, 36, 72):
        _, planar, outlier, support = analyze_scale(gp, gf, resolution, tolerance=0.035)
        planar_votes += planar
        outlier_votes += outlier
        support_votes += support
    elapsed = time.perf_counter() - started
    trials = []
    for outlier_required, support_required in ((1, 1), (2, 1), (2, 2), (3, 1)):
        candidate = cp.asnumpy(
            (outlier_votes >= outlier_required) & (support_votes >= support_required)
        )
        true_positive = int(np.count_nonzero(candidate & dust_truth & ~feature_truth))
        false_positive = int(np.count_nonzero(candidate & ~dust_truth))
        missed = int(np.count_nonzero(~candidate & dust_truth & ~feature_truth))
        feature_hits = int(np.count_nonzero(candidate & feature_truth))
        trials.append(
            {
                "outlier_votes": outlier_required,
                "support_votes": support_required,
                "candidate_triangles": int(np.count_nonzero(candidate)),
                "dust_precision": true_positive / max(1, true_positive + false_positive),
                "dust_recall": true_positive / max(1, true_positive + missed),
                "intentional_feature_false_positive_share": feature_hits
                / max(1, np.count_nonzero(feature_truth)),
            }
        )
    result = {
        "triangles": len(faces),
        "known_dust_triangles": int(np.count_nonzero(dust_truth & ~feature_truth)),
        "intentional_feature_triangles": int(np.count_nonzero(feature_truth)),
        "trials": trials,
        "seconds": elapsed,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
