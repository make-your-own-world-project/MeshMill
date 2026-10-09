"""Use adaptive physical probes as a continuous QEM triangle-budget field."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy as cp
import numpy as np
from gpu_adaptive_probe_qem import _bincount, physical_probe_dimensions
from gpu_complete_reducer import save_binary_stl
from gpu_geometry_prototype import (
    connected_arrays,
    load_binary_stl,
    quality_metrics,
    topology_metrics,
)
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkQuadricDecimation


def adaptive_budget_field(points, faces, target):
    """Return per-vertex required sampling density from adaptive physical probes."""
    started = time.perf_counter()
    physical = physical_probe_dimensions(points, faces, target)
    tip_radius = physical["tip_radius"]
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
    unresolved = cp.ones(len(faces), dtype=cp.bool_)
    face_levels = cp.full(len(faces), 4, dtype=cp.uint8)
    # Zero means not assigned. Unresolved faces receive a value above the finest probe level.
    face_budget = cp.zeros(len(faces), dtype=cp.float32)
    levels = []

    for pitch in pitches:
        dims = cp.maximum(cp.ceil((high - low) / pitch).astype(cp.int64) + 1, 1)
        cell = cp.floor((centers - low) / pitch).astype(cp.int64)
        raw_keys = cell[:, 0] + dims[0] * (cell[:, 1] + dims[1] * cell[:, 2])
        _occupied, keys = cp.unique(raw_keys, return_inverse=True)
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
        residual = cp.abs(cp.sum(mean_normal[keys] * (centers - mean_center[keys]), axis=1))
        residual_rms = cp.sqrt(
            _bincount(keys, weights * residual * residual, cell_count)
            / cp.maximum(area_sum, cp.float32(1e-12))
        )
        maximum_angle = np.arctan2(tip_radius, pitch * 0.5)
        coherence_limit = float(np.cos(maximum_angle))
        valid = (coherence >= cp.float32(coherence_limit)) & (
            residual_rms <= cp.float32(tip_radius)
        )
        assigned = unresolved & valid[keys]
        # Required samples per unit length are proportional to inverse pitch. Add a continuous
        # residual term so transitions do not become four hard density bands.
        base_density = physical["minimum_pitch"] / pitch
        detail = cp.clip(residual / cp.float32(tip_radius), 0.0, 1.0)
        face_budget[assigned] = cp.float32(base_density) + cp.float32(0.25) * detail[assigned]
        face_levels[assigned] = cp.uint8(len(levels))
        assigned_keys = cp.unique(keys[assigned])
        levels.append(
            {
                "pitch": float(pitch),
                "probe_count": len(assigned_keys),
                "assigned_faces": int(cp.count_nonzero(assigned).get()),
                "base_density": float(base_density),
            }
        )
        unresolved &= ~assigned

    face_budget[unresolved] = cp.float32(1.5)
    flat_vertices = gf.ravel()
    repeated_area = cp.repeat(weights, 3)
    vertex_area = _bincount(flat_vertices, repeated_area, len(points))
    vertex_budget = _bincount(
        flat_vertices, cp.repeat(weights * face_budget, 3), len(points)
    ) / cp.maximum(vertex_area, cp.float32(1e-12))
    # Normalize to [0,1]. The value is an attribute field, not a displacement.
    vertex_budget = cp.clip(vertex_budget / cp.float32(1.5), 0.0, 1.0)
    cp.cuda.Stream.null.synchronize()
    report = {
        "seconds": time.perf_counter() - started,
        "probe_geometry": physical,
        "levels": levels,
        "unresolved_faces": int(cp.count_nonzero(unresolved).get()),
        "budget_percentiles": cp.asnumpy(
            cp.percentile(vertex_budget, cp.asarray([0, 25, 50, 75, 95, 100]))
        ).tolist(),
    }
    return (
        cp.asnumpy(vertex_budget).astype(np.float32, copy=False),
        cp.asnumpy(face_levels).astype(np.uint8, copy=False),
        report,
    )


def make_polydata(points, faces, budget):
    poly = vtkPolyData()
    vtk_points = vtkPoints()
    vtk_points.SetData(numpy_to_vtk(np.ascontiguousarray(points), deep=True))
    poly.SetPoints(vtk_points)
    packed = np.empty((len(faces), 4), dtype=np.int64)
    packed[:, 0] = 3
    packed[:, 1:] = faces
    cells = vtkCellArray()
    cells.ImportLegacyFormat(numpy_to_vtkIdTypeArray(packed.ravel(), deep=True))
    poly.SetPolys(cells)
    scalars = numpy_to_vtk(np.ascontiguousarray(budget), deep=True)
    scalars.SetName("AdaptiveProbeBudget")
    poly.GetPointData().SetScalars(scalars)
    return poly


def arrays_from_polydata(poly):
    points = np.asarray(vtk_to_numpy(poly.GetPoints().GetData()), dtype=np.float32)
    offsets = np.asarray(vtk_to_numpy(poly.GetPolys().GetOffsetsArray()), dtype=np.int64)
    connectivity = np.asarray(vtk_to_numpy(poly.GetPolys().GetConnectivityArray()), dtype=np.int64)
    if not np.all(np.diff(offsets) == 3):
        raise RuntimeError("Reducer returned non-triangle cells")
    return points, connectivity.reshape(-1, 3).astype(np.int32, copy=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--attribute-weight", type=float, default=1.0)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()
    total_started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    budget, _face_levels, probe_report = adaptive_budget_field(points, faces, args.target)
    source = make_polydata(points, faces, budget)
    reducer = vtkQuadricDecimation()
    reducer.SetInputData(source)
    reducer.SetTargetReduction(1.0 - args.target / len(faces))
    reducer.VolumePreservationOn()
    reducer.AttributeErrorMetricOn()
    reducer.ScalarsAttributeOn()
    reducer.SetScalarsWeight(args.attribute_weight)
    reducer.NormalsAttributeOff()
    reducer.VectorsAttributeOff()
    reducer.TCoordsAttributeOff()
    reducer.TensorsAttributeOff()
    reduction_started = time.perf_counter()
    reducer.Update()
    reduction_seconds = time.perf_counter() - reduction_started
    out_points, out_faces = arrays_from_polydata(reducer.GetOutput())
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
        "gpu_probe_budget": probe_report,
        "attribute_weight": args.attribute_weight,
        "cpu_qem_seconds": reduction_seconds,
        "resident_compute_seconds": probe_report["seconds"] + reduction_seconds,
        "total_seconds": time.perf_counter() - total_started,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
