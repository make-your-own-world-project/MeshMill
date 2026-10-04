"""Small deterministic checks for density display and density-balanced reduction."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from meshmill import density_balance_arrays, point_density_colors


def grid(nx: int, ny: int, x_offset: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    x, y = np.meshgrid(np.linspace(x_offset, x_offset + 1.0, nx), np.linspace(0.0, 1.0, ny))
    points = np.column_stack((x.ravel(), y.ravel(), np.zeros(x.size)))
    faces = []
    for row in range(ny - 1):
        for column in range(nx - 1):
            index = row * nx + column
            faces.extend(
                ([index, index + 1, index + nx + 1], [index, index + nx + 1, index + nx])
            )
    return points, np.asarray(faces, dtype=np.int32)


dense_points, dense_faces = grid(61, 61)
sparse_points, sparse_faces = grid(15, 15, 1.1)
sparse_faces += len(dense_points)
points = np.vstack((dense_points, sparse_points))
faces = np.vstack((dense_faces, sparse_faces))

colors = point_density_colors(points, faces)
assert colors.shape == (len(points), 3)
assert colors.dtype == np.uint8
assert colors[:len(dense_points), 0].mean() > colors[len(dense_points):, 0].mean()

reduced_points, reduced_faces = density_balance_arrays(points, faces, 1_500, 7.0)
assert 1_000 <= len(reduced_faces) <= 1_600
assert np.allclose(np.ptp(reduced_points, axis=0)[:2], np.ptp(points, axis=0)[:2], atol=0.03)

print("density checks passed")
