"""Complete GPU surface-analysis plus CPU topology-assembly prototype.

The GPU estimates multiscale surface-trajectory normals. VTK then performs the actual edge
collapses on the original indexed topology while treating those normals as attributes that should
survive simplification. This avoids reconstructing a mesh from disconnected depth sheets.
"""

from __future__ import annotations

import argparse
import json
import struct
import time
from pathlib import Path

import cupy as cp
import numpy as np
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


def _bincount(keys, weights, count):
    return cp.bincount(keys, weights=weights, minlength=count).astype(cp.float32)


def trajectory_normals(points, faces, resolutions, tolerance):
    """Return GPU-derived per-vertex normals and analysis statistics."""
    started = time.perf_counter()
    gp = cp.asarray(points)
    gf = cp.asarray(faces)
    triangles = gp[gf]
    cross = cp.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    twice_area = cp.linalg.norm(cross, axis=1)
    face_normals = cross / cp.maximum(twice_area[:, None], cp.float32(1e-12))
    centers = cp.mean(triangles, axis=1)
    weights = twice_area * cp.float32(0.5)
    low = cp.min(gp, axis=0)
    extent = cp.maximum(cp.max(gp, axis=0) - low, cp.float32(1e-12))

    trajectory_sum = cp.zeros_like(face_normals)
    stable_votes = cp.zeros(len(faces), dtype=cp.uint8)
    dust_votes = cp.zeros(len(faces), dtype=cp.uint8)
    scale_stats = []

    for resolution in resolutions:
        cells = cp.floor((centers - low) / extent * resolution).astype(cp.int32)
        cells = cp.clip(cells, 0, resolution - 1)
        keys = cells[:, 0] + resolution * (cells[:, 1] + resolution * cells[:, 2])
        cell_count = resolution ** 3
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
        # Plane normals have two equivalent signs. Align the trajectory normal to each source face.
        signs = cp.where(cp.sum(local_normal * face_normals, axis=1) < 0, -1.0, 1.0)
        local_normal = local_normal * signs[:, None]
        residual = cp.abs(cp.sum(local_normal * (centers - mean_center[keys]), axis=1))
        stable = (coherence[keys] >= cp.float32(0.970)) & (residual <= tolerance)
        dust = (coherence[keys] >= cp.float32(0.970)) & (residual > tolerance)
        # Coherent cells contribute their high-level trajectory. Features retain their raw normal.
        trajectory_sum += cp.where(stable[:, None] | dust[:, None], local_normal, face_normals)
        stable_votes += stable
        dust_votes += dust
        scale_stats.append(
            {
                "resolution": resolution,
                "stable_share": float(cp.mean(stable).get()),
                "supported_outlier_share": float(cp.mean(dust).get()),
            }
        )

    trajectory_face_normals = trajectory_sum / cp.maximum(
        cp.linalg.norm(trajectory_sum, axis=1)[:, None], cp.float32(1e-12)
    )
    # Accumulate face trajectories into an area-weighted vertex field.
    vertex_sum = cp.zeros((len(points), 3), dtype=cp.float32)
    flat_vertices = gf.ravel()
    for axis in range(3):
        vertex_sum[:, axis] = _bincount(
            flat_vertices,
            cp.repeat(weights * trajectory_face_normals[:, axis], 3),
            len(points),
        )
    vertex_normals = vertex_sum / cp.maximum(
        cp.linalg.norm(vertex_sum, axis=1)[:, None], cp.float32(1e-12)
    )
    cp.cuda.Stream.null.synchronize()
    report = {
        "seconds": time.perf_counter() - started,
        "scales": scale_stats,
        "stable_consensus_share": float(cp.mean(stable_votes >= max(2, len(resolutions) // 2)).get()),
        "supported_outlier_consensus_share": float(
            cp.mean(dust_votes >= max(2, len(resolutions) // 2)).get()
        ),
    }
    return cp.asnumpy(vertex_normals).astype(np.float32, copy=False), report


def make_polydata(points, faces, normals):
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
    vtk_normals = numpy_to_vtk(np.ascontiguousarray(normals), deep=True)
    vtk_normals.SetName("SurfaceTrajectoryNormal")
    poly.GetPointData().SetNormals(vtk_normals)
    return poly


def arrays_from_polydata(poly):
    points = np.asarray(vtk_to_numpy(poly.GetPoints().GetData()), dtype=np.float32)
    packed = np.asarray(vtk_to_numpy(poly.GetPolys().GetData()), dtype=np.int64).reshape(-1, 4)
    return points, packed[:, 1:].astype(np.int32, copy=False)


def save_binary_stl(path, points, faces):
    triangles = points[faces].astype(np.float32, copy=False)
    normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-20)
    record = np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attr", "<u2")])
    output = np.zeros(len(faces), dtype=record)
    output["normal"] = normals
    output["vertices"] = triangles
    with path.open("wb") as stream:
        stream.write(b"MeshMill surface-guided QEM prototype".ljust(80, b"\0"))
        stream.write(struct.pack("<I", len(faces)))
        output.tofile(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--resolutions", default="24,48,72")
    parser.add_argument("--tolerance", type=float, default=0.10)
    parser.add_argument("--normal-weight", type=float, default=2.0)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output-mesh", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    args = parser.parse_args()

    total_started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    points, faces, connectivity_seconds = connected_arrays(triangles)
    resolutions = [int(value) for value in args.resolutions.split(",")]
    normals, analysis = trajectory_normals(points, faces, resolutions, args.tolerance)
    source = make_polydata(points, faces, normals)
    decimator = vtkQuadricDecimation()
    decimator.SetInputData(source)
    decimator.SetTargetReduction(1.0 - args.target / len(faces))
    decimator.VolumePreservationOn()
    decimator.AttributeErrorMetricOn()
    decimator.NormalsAttributeOn()
    decimator.SetScalarsAttribute(False)
    decimator.SetVectorsAttribute(False)
    decimator.SetTCoordsAttribute(False)
    decimator.SetTensorsAttribute(False)
    # VTK uses the normal attribute weight in its augmented quadric objective.
    if hasattr(decimator, "SetNormalsWeight"):
        decimator.SetNormalsWeight(args.normal_weight)
    reduction_started = time.perf_counter()
    decimator.Update()
    reduction_seconds = time.perf_counter() - reduction_started
    out_points, out_faces = arrays_from_polydata(decimator.GetOutput())
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
        "gpu_surface_analysis": analysis,
        "cpu_topology_assembly_seconds": reduction_seconds,
        "total_seconds": time.perf_counter() - total_started,
        "normal_weight": args.normal_weight,
        "quality": quality,
        "output_mesh": str(args.output_mesh),
    }
    args.output_report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
