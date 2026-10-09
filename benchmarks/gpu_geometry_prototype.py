"""Isolated GPU geometry-reduction benchmark.

This prototype is intentionally separate from MeshMill's application path. It compares a
CUDA voxel-clustering reducer with the current Fast QEM backend using a binary STL input.
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import time
from pathlib import Path

import cupy as cp
import fast_simplification
import numpy as np
import psutil
from scipy.spatial import cKDTree

STL_HEADER_BYTES = 84
STL_RECORD_BYTES = 50
STL_DTYPE = np.dtype(
    [("normal", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")]
)


def load_binary_stl(path: Path) -> np.ndarray:
    size = path.stat().st_size
    with path.open("rb") as stream:
        header = stream.read(STL_HEADER_BYTES)
    count = struct.unpack_from("<I", header, 80)[0]
    if STL_HEADER_BYTES + count * STL_RECORD_BYTES != size:
        raise ValueError("Prototype requires a valid binary STL.")
    records = np.memmap(path, dtype=STL_DTYPE, mode="r", offset=STL_HEADER_BYTES, shape=(count,))
    return np.asarray(records["vertices"], dtype=np.float32)


def connected_arrays(triangles: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    started = time.perf_counter()
    points, inverse = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
    faces = inverse.reshape(-1, 3).astype(np.int32, copy=False)
    return points, faces, time.perf_counter() - started


def packed_voxel_keys(points: cp.ndarray, low: cp.ndarray, cell_size: float) -> cp.ndarray:
    cells = cp.floor((points - low) / cell_size).astype(cp.uint64)
    maximum = int(cp.max(cells).get())
    if maximum >= (1 << 21):
        raise ValueError("Voxel grid exceeds 21-bit packed-coordinate range.")
    return cells[:, 0] | (cells[:, 1] << 21) | (cells[:, 2] << 42)


def choose_cell_size(points: cp.ndarray, low: cp.ndarray, high: cp.ndarray, target_vertices: int):
    extent = float(cp.max(high - low).get())
    lower = max(extent / 2_000_000.0, np.finfo(np.float32).eps)
    upper = extent
    trials = []
    for _ in range(12):
        cell = (lower * upper) ** 0.5
        count = int(cp.unique(packed_voxel_keys(points, low, cell)).size)
        trials.append((cell, count))
        if count > target_vertices:
            lower = cell
        else:
            upper = cell
    return min(trials, key=lambda item: abs(item[1] - target_vertices)), trials


def gpu_voxel_reduce(triangles: np.ndarray, target_faces: int):
    timings = {}
    started = time.perf_counter()
    gpu_points = cp.asarray(triangles.reshape(-1, 3))
    low = cp.min(gpu_points, axis=0)
    high = cp.max(gpu_points, axis=0)
    cp.cuda.Stream.null.synchronize()
    timings["upload_seconds"] = time.perf_counter() - started

    target_vertices = max(4, target_faces // 2)
    started = time.perf_counter()
    (cell_size, estimated_vertices), trials = choose_cell_size(
        gpu_points, low, high, target_vertices
    )
    timings["cell_search_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    keys = packed_voxel_keys(gpu_points, low, cell_size)
    _, inverse = cp.unique(keys, return_inverse=True)
    vertex_count = int(cp.max(inverse).get()) + 1
    counts = cp.bincount(inverse, minlength=vertex_count).astype(cp.float32)
    clustered = cp.stack(
        [cp.bincount(inverse, weights=gpu_points[:, axis], minlength=vertex_count) for axis in range(3)],
        axis=1,
    ) / counts[:, None]
    mapped_faces = inverse.reshape(-1, 3)
    keep = (
        (mapped_faces[:, 0] != mapped_faces[:, 1])
        & (mapped_faces[:, 1] != mapped_faces[:, 2])
        & (mapped_faces[:, 0] != mapped_faces[:, 2])
    )
    mapped_faces = mapped_faces[keep]
    canonical = cp.sort(mapped_faces, axis=1).astype(cp.uint64, copy=False)
    if vertex_count >= (1 << 21):
        raise ValueError("Cluster count exceeds packed-face range.")
    face_keys = canonical[:, 0] | (canonical[:, 1] << 21) | (canonical[:, 2] << 42)
    _, unique_index = cp.unique(face_keys, return_index=True)
    mapped_faces = mapped_faces[cp.sort(unique_index)]
    cp.cuda.Stream.null.synchronize()
    timings["reduce_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    output_points = cp.asnumpy(clustered).astype(np.float32, copy=False)
    output_faces = cp.asnumpy(mapped_faces).astype(np.int32, copy=False)
    timings["download_seconds"] = time.perf_counter() - started
    timings["total_seconds"] = sum(timings.values())
    return output_points, output_faces, timings, cell_size, estimated_vertices, trials


def gpu_feature_voxel_reduce(points: np.ndarray, faces: np.ndarray, target_faces: int):
    """Cluster only spatially and directionally compatible vertices, preserving risky edges."""
    timings = {}
    started = time.perf_counter()
    gpu_points = cp.asarray(points)
    gpu_faces = cp.asarray(faces)
    low = cp.min(gpu_points, axis=0)
    high = cp.max(gpu_points, axis=0)

    # Vertices on boundary or non-manifold edges are excluded from clustering. This retains the
    # source envelope and prevents a voxel from welding many common scan defects together.
    edges = cp.concatenate(
        (gpu_faces[:, [0, 1]], gpu_faces[:, [1, 2]], gpu_faces[:, [2, 0]]), axis=0
    ).astype(cp.uint64, copy=False)
    edges.sort(axis=1)
    edge_keys = edges[:, 0] | (edges[:, 1] << 32)
    unique_edges, edge_counts = cp.unique(edge_keys, return_counts=True)
    risky_edges = unique_edges[edge_counts != 2]
    risky_vertices = cp.unique(
        cp.concatenate(((risky_edges & cp.uint64(0xFFFFFFFF)), (risky_edges >> 32)))
    ).astype(cp.int64)
    preserve = cp.zeros(len(gpu_points), dtype=cp.bool_)
    preserve[risky_vertices] = True

    tri = gpu_points[gpu_faces]
    face_normals = cp.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    lengths = cp.linalg.norm(face_normals, axis=1)
    face_normals /= cp.maximum(lengths[:, None], cp.float32(1e-20))
    flat_indices = gpu_faces.reshape(-1)
    repeated_normals = cp.repeat(face_normals, 3, axis=0)
    point_normals = cp.stack(
        [
            cp.bincount(flat_indices, weights=repeated_normals[:, axis], minlength=len(gpu_points))
            for axis in range(3)
        ],
        axis=1,
    )
    point_normals /= cp.maximum(cp.linalg.norm(point_normals, axis=1)[:, None], cp.float32(1e-20))
    # Six bits per axis keeps curved surfaces distinct without preventing useful clustering.
    normal_cells = cp.rint((point_normals + 1.0) * 31.5).astype(cp.uint64)
    normal_keys = normal_cells[:, 0] | (normal_cells[:, 1] << 6) | (normal_cells[:, 2] << 12)
    cp.cuda.Stream.null.synchronize()
    timings["upload_and_features_seconds"] = time.perf_counter() - started

    target_vertices = max(4, target_faces // 2)
    extent = float(cp.max(high - low).get())
    lower = max(extent / 2_000_000.0, np.finfo(np.float32).eps)
    upper = extent
    trials = []
    started = time.perf_counter()
    for _ in range(12):
        cell = (lower * upper) ** 0.5
        spatial = packed_voxel_keys(gpu_points, low, cell)
        combined = spatial ^ (normal_keys * cp.uint64(0x9E3779B185EBCA87))
        count = int(cp.unique(combined).size)
        # Conservatively account for preserved vertices that would otherwise share clusters.
        count += int(cp.count_nonzero(preserve).get())
        trials.append((cell, count))
        if count > target_vertices:
            lower = cell
        else:
            upper = cell
    cell_size, estimated_vertices = min(trials, key=lambda item: abs(item[1] - target_vertices))
    timings["cell_search_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    spatial = packed_voxel_keys(gpu_points, low, cell_size)
    combined = spatial ^ (normal_keys * cp.uint64(0x9E3779B185EBCA87))
    _, inverse = cp.unique(combined, return_inverse=True)
    base_clusters = int(cp.max(inverse).get()) + 1
    preserve_indices = cp.flatnonzero(preserve)
    inverse[preserve_indices] = base_clusters + cp.arange(len(preserve_indices), dtype=inverse.dtype)
    _, inverse = cp.unique(inverse, return_inverse=True)
    vertex_count = int(cp.max(inverse).get()) + 1
    counts = cp.bincount(inverse, minlength=vertex_count).astype(cp.float32)
    clustered = cp.stack(
        [cp.bincount(inverse, weights=gpu_points[:, axis], minlength=vertex_count) for axis in range(3)],
        axis=1,
    ) / counts[:, None]
    mapped_faces = inverse[gpu_faces]
    keep = (
        (mapped_faces[:, 0] != mapped_faces[:, 1])
        & (mapped_faces[:, 1] != mapped_faces[:, 2])
        & (mapped_faces[:, 0] != mapped_faces[:, 2])
    )
    mapped_faces = mapped_faces[keep]
    canonical = cp.sort(mapped_faces, axis=1).astype(cp.uint64, copy=False)
    if vertex_count >= (1 << 21):
        raise ValueError("Cluster count exceeds packed-face range.")
    face_keys = canonical[:, 0] | (canonical[:, 1] << 21) | (canonical[:, 2] << 42)
    _, unique_index = cp.unique(face_keys, return_index=True)
    mapped_faces = mapped_faces[cp.sort(unique_index)]
    cp.cuda.Stream.null.synchronize()
    timings["reduce_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    output_points = cp.asnumpy(clustered).astype(np.float32, copy=False)
    output_faces = cp.asnumpy(mapped_faces).astype(np.int32, copy=False)
    timings["download_seconds"] = time.perf_counter() - started
    timings["total_seconds"] = sum(timings.values())
    return (
        output_points,
        output_faces,
        timings,
        cell_size,
        estimated_vertices,
        trials,
        len(preserve_indices),
    )


def _gpu_unique_faces(faces: cp.ndarray) -> cp.ndarray:
    keep = (
        (faces[:, 0] != faces[:, 1])
        & (faces[:, 1] != faces[:, 2])
        & (faces[:, 0] != faces[:, 2])
    )
    faces = faces[keep]
    canonical = cp.sort(faces, axis=1).astype(cp.uint64, copy=False)
    if int(cp.max(faces).get()) >= (1 << 21):
        raise ValueError("Vertex count exceeds packed-face range.")
    keys = canonical[:, 0] | (canonical[:, 1] << 21) | (canonical[:, 2] << 42)
    _, indices = cp.unique(keys, return_index=True)
    return faces[cp.sort(indices)]


def _gpu_edges(faces: cp.ndarray):
    edges = cp.concatenate(
        (faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), axis=0
    ).astype(cp.uint64, copy=False)
    edges.sort(axis=1)
    keys = edges[:, 0] | (edges[:, 1] << 32)
    unique, counts = cp.unique(keys, return_counts=True)
    return cp.stack((unique & cp.uint64(0xFFFFFFFF), unique >> 32), axis=1).astype(cp.int64), counts


def _gpu_vertex_quadrics(
    points: cp.ndarray, faces: cp.ndarray, area_weighted: bool = False
) -> cp.ndarray:
    tri = points[faces]
    normals = cp.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    lengths = cp.linalg.norm(normals, axis=1)
    normals /= cp.maximum(lengths[:, None], cp.float32(1e-20))
    d = -cp.sum(normals * tri[:, 0], axis=1)
    a, b, c = normals[:, 0], normals[:, 1], normals[:, 2]
    quadrics = cp.stack(
        (a*a, a*b, a*c, a*d, b*b, b*c, b*d, c*c, c*d, d*d), axis=1
    )
    if area_weighted:
        scale = cp.mean(lengths)
        quadrics *= (lengths / cp.maximum(scale, cp.float32(1e-20)))[:, None]
    flat = faces.reshape(-1)
    repeated = cp.repeat(quadrics, 3, axis=0)
    return cp.stack(
        [cp.bincount(flat, weights=repeated[:, i], minlength=len(points)) for i in range(10)],
        axis=1,
    )


def _quadric_cost(q: cp.ndarray, p: cp.ndarray) -> cp.ndarray:
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    return (
        q[:, 0]*x*x + 2*q[:, 1]*x*y + 2*q[:, 2]*x*z + 2*q[:, 3]*x
        + q[:, 4]*y*y + 2*q[:, 5]*y*z + 2*q[:, 6]*y
        + q[:, 7]*z*z + 2*q[:, 8]*z + q[:, 9]
    )


def _quadric_optimal_position(q: cp.ndarray, p0: cp.ndarray, p1: cp.ndarray):
    """Solve the 3x3 QEM system in parallel and reject unstable remote solutions."""
    a, b, c, d = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    e, f, g = q[:, 4], q[:, 5], q[:, 6]
    h, i = q[:, 7], q[:, 8]
    det = a * (e * h - f * f) - b * (b * h - c * f) + c * (b * f - c * e)
    rhs0, rhs1, rhs2 = -d, -g, -i
    safe_det = cp.where(cp.abs(det) > cp.float32(1e-10), det, cp.float32(1.0))
    x = (
        rhs0 * (e * h - f * f)
        - b * (rhs1 * h - f * rhs2)
        + c * (rhs1 * f - e * rhs2)
    ) / safe_det
    y = (
        a * (rhs1 * h - f * rhs2)
        - rhs0 * (b * h - c * f)
        + c * (b * rhs2 - rhs1 * c)
    ) / safe_det
    z = (
        a * (e * rhs2 - rhs1 * f)
        - b * (b * rhs2 - rhs1 * c)
        + rhs0 * (b * f - e * c)
    ) / safe_det
    position = cp.stack((x, y, z), axis=1)
    edge = p1 - p0
    edge_length_sq = cp.sum(edge * edge, axis=1)
    segment_t = cp.clip(
        cp.sum((position - p0) * edge, axis=1)
        / cp.maximum(edge_length_sq, cp.float32(1e-20)),
        cp.float32(0.0),
        cp.float32(1.0),
    )
    position = p0 + segment_t[:, None] * edge
    valid = (
        (cp.abs(det) > cp.float32(1e-10))
        & cp.all(cp.isfinite(position), axis=1)
    )
    return position, valid


_VALIDATE_COLLAPSES = cp.RawKernel(
    r'''
    extern "C" __global__
    void validate(const long long* candidates, const long long* selected,
                  const long long* offsets, const long long* neighbors,
                  const unsigned char* selected_vertex, unsigned char* valid,
                  const long long selected_count) {
        long long i = (long long)blockDim.x * blockIdx.x + threadIdx.x;
        if (i >= selected_count) return;
        long long edge_index = selected[i];
        long long u = candidates[2 * edge_index];
        long long v = candidates[2 * edge_index + 1];
        long long a = offsets[u], a_end = offsets[u + 1];
        long long b = offsets[v], b_end = offsets[v + 1];
        int common = 0;
        while (a < a_end && b < b_end) {
            long long na = neighbors[a], nb = neighbors[b];
            if (na == nb) { common++; a++; b++; }
            else if (na < nb) a++;
            else b++;
        }
        valid[i] = common == 2 ? 1 : 0;
    }
    ''',
    "validate",
)

_GREEDY_ONE_RING = cp.RawKernel(
    r'''
    extern "C" __global__
    void select_batch(const long long* candidates, const long long* selected,
                      const long long* offsets, const long long* neighbors,
                      unsigned char* forbidden, unsigned char* accepted,
                      const long long selected_count) {
        if (blockIdx.x != 0 || threadIdx.x != 0) return;
        for (long long i = 0; i < selected_count; ++i) {
            long long edge_index = selected[i];
            long long u = candidates[2 * edge_index];
            long long v = candidates[2 * edge_index + 1];
            if (forbidden[u] || forbidden[v]) continue;
            accepted[i] = 1;
            forbidden[u] = 1;
            forbidden[v] = 1;
            for (long long j = offsets[u]; j < offsets[u + 1]; ++j) forbidden[neighbors[j]] = 1;
            for (long long j = offsets[v]; j < offsets[v + 1]; ++j) forbidden[neighbors[j]] = 1;
        }
    }
    ''',
    "select_batch",
)

_GREEDY_VERTEX_MATCHING = cp.RawKernel(
    r'''
    extern "C" __global__
    void select_vertex_matching(const long long* candidates, const long long* selected,
                                unsigned char* claimed, unsigned char* accepted,
                                const long long selected_count) {
        // Candidate order is global QEM priority. One thread provides deterministic greedy
        // ownership without the excessive one-ring exclusion used by the conservative prototype.
        if (blockIdx.x != 0 || threadIdx.x != 0) return;
        for (long long i = 0; i < selected_count; ++i) {
            long long edge_index = selected[i];
            long long u = candidates[2 * edge_index];
            long long v = candidates[2 * edge_index + 1];
            if (claimed[u] || claimed[v]) continue;
            claimed[u] = 1;
            claimed[v] = 1;
            accepted[i] = 1;
        }
    }
    ''',
    "select_vertex_matching",
)

_VALIDATE_FACE_ORIENTATION = cp.RawKernel(
    r'''
    __device__ void cross3(const float* a, const float* b, float* out) {
        out[0] = a[1]*b[2] - a[2]*b[1];
        out[1] = a[2]*b[0] - a[0]*b[2];
        out[2] = a[0]*b[1] - a[1]*b[0];
    }
    extern "C" __global__
    void validate_orientation(const float* points, const int* faces,
                  const long long* face_offsets, const long long* incident_faces,
                  const long long* winners, const long long* losers,
                  const float* positions, unsigned char* valid,
                  const long long selected_count) {
        long long i = (long long)blockDim.x * blockIdx.x + threadIdx.x;
        if (i >= selected_count) return;
        long long winner = winners[i], loser = losers[i];
        for (int side = 0; side < 2; ++side) {
            long long vertex = side == 0 ? winner : loser;
            for (long long cursor = face_offsets[vertex]; cursor < face_offsets[vertex + 1]; ++cursor) {
                long long fi = incident_faces[cursor];
                int ia = faces[3*fi], ib = faces[3*fi+1], ic = faces[3*fi+2];
                bool has_winner = ia == winner || ib == winner || ic == winner;
                bool has_loser = ia == loser || ib == loser || ic == loser;
                if (has_winner && has_loser) continue;
                const float *oa=&points[3*ia], *ob=&points[3*ib], *oc=&points[3*ic];
                float old_ab[3]={ob[0]-oa[0],ob[1]-oa[1],ob[2]-oa[2]};
                float old_ac[3]={oc[0]-oa[0],oc[1]-oa[1],oc[2]-oa[2]};
                float old_n[3]; cross3(old_ab,old_ac,old_n);
                float na[3]={oa[0],oa[1],oa[2]}, nb[3]={ob[0],ob[1],ob[2]}, nc[3]={oc[0],oc[1],oc[2]};
                if (ia == winner || ia == loser) { na[0]=positions[3*i];na[1]=positions[3*i+1];na[2]=positions[3*i+2]; }
                if (ib == winner || ib == loser) { nb[0]=positions[3*i];nb[1]=positions[3*i+1];nb[2]=positions[3*i+2]; }
                if (ic == winner || ic == loser) { nc[0]=positions[3*i];nc[1]=positions[3*i+1];nc[2]=positions[3*i+2]; }
                float new_ab[3]={nb[0]-na[0],nb[1]-na[1],nb[2]-na[2]};
                float new_ac[3]={nc[0]-na[0],nc[1]-na[1],nc[2]-na[2]};
                float new_n[3]; cross3(new_ab,new_ac,new_n);
                float old_sq=old_n[0]*old_n[0]+old_n[1]*old_n[1]+old_n[2]*old_n[2];
                float new_sq=new_n[0]*new_n[0]+new_n[1]*new_n[1]+new_n[2]*new_n[2];
                float dot=old_n[0]*new_n[0]+old_n[1]*new_n[1]+old_n[2]*new_n[2];
                if (new_sq < old_sq*1.0e-12f || dot < 0.2f*sqrtf(old_sq*new_sq)) { valid[i]=0; return; }
            }
        }
    }
    ''',
    "validate_orientation",
)


def gpu_qem_reduce(
    points: np.ndarray,
    faces: np.ndarray,
    target_faces: int,
    max_passes: int = 512,
    scheduling: str = "one-ring",
    quarantine_irregular_vertices: bool = True,
    validate_face_orientation: bool = True,
    preserve_boundary_vertices: bool = False,
    placement_mode: str = "optimal",
    area_weighted_quadrics: bool = False,
    prefilter_face_orientation: bool = False,
    candidate_fraction: float = 1.0,
):
    """Parallel endpoint-QEM prototype using conflict-free edge batches."""
    timings = {"passes": []}
    started = time.perf_counter()
    gpu_points = cp.asarray(points)
    gpu_faces = cp.asarray(faces)
    gpu_quadrics = _gpu_vertex_quadrics(
        gpu_points, gpu_faces, area_weighted=area_weighted_quadrics
    )
    boundary_vertex = None
    if preserve_boundary_vertices:
        initial_edges, initial_counts = _gpu_edges(gpu_faces)
        boundary_vertex = cp.zeros(len(gpu_points), dtype=cp.bool_)
        boundary_edges = initial_edges[initial_counts == 1]
        if len(boundary_edges):
            boundary_vertex[cp.unique(boundary_edges)] = True
    cp.cuda.Stream.null.synchronize()
    timings["upload_seconds"] = time.perf_counter() - started

    for pass_index in range(max_passes):
        if len(gpu_faces) <= target_faces:
            break
        pass_started = time.perf_counter()
        edges, edge_counts = _gpu_edges(gpu_faces)
        valid = edge_counts == 2
        if preserve_boundary_vertices:
            valid &= ~boundary_vertex[edges[:, 0]] & ~boundary_vertex[edges[:, 1]]
        if quarantine_irregular_vertices:
            # Conservative mode for clean manifold inputs. Dirty scans often contain open
            # layers, so quarantining every vertex adjacent to one irregular edge can spread
            # across an otherwise usable surface and strand nearly every legal collapse.
            irregular = cp.zeros(len(gpu_points), dtype=cp.bool_)
            risky = edges[edge_counts != 2]
            if len(risky):
                irregular[cp.unique(risky)] = True
            valid &= ~irregular[edges[:, 0]] & ~irregular[edges[:, 1]]
        candidates = edges[valid]
        candidate_count = len(candidates)
        if not len(candidates):
            break
        combined = gpu_quadrics[candidates[:, 0]] + gpu_quadrics[candidates[:, 1]]
        position0 = gpu_points[candidates[:, 0]]
        position1 = gpu_points[candidates[:, 1]]
        midpoint = (position0 + position1) * 0.5
        optimal, optimal_valid = _quadric_optimal_position(
            combined, position0, position1
        )
        cost0 = _quadric_cost(combined, position0)
        cost1 = _quadric_cost(combined, position1)
        cost_mid = _quadric_cost(combined, midpoint)
        cost_opt = cp.where(
            optimal_valid,
            _quadric_cost(combined, optimal),
            cp.float32(cp.inf),
        )
        costs = (
            cp.minimum(cost0, cost1)
            if placement_mode == "endpoint"
            else cp.minimum(cp.minimum(cp.minimum(cost0, cost1), cost_mid), cost_opt)
        )

        order = None if scheduling == "cavity" else cp.argsort(costs)
        if scheduling in ("priority", "vertex", "cavity"):
            # Feed a broad low-error candidate frontier into the topology and one-ring guards.
            # Mutual-cheapest selection strands valid edges late in reduction and stalls early.
            pool_size = (
                len(candidates)
                if scheduling in ("vertex", "cavity")
                else min(len(order), max(50_000, len(gpu_points) // 3))
            )
            selected = (
                cp.arange(pool_size, dtype=cp.int64)
                if scheduling == "cavity"
                else order[:pool_size]
            )
            if scheduling == "cavity" and candidate_fraction < 1.0:
                eligible_count = max(1, int(len(selected) * candidate_fraction))
                # Non-negative IEEE-754 float bits preserve numeric ordering. Their high byte
                # provides a cheap 256-bin GPU histogram, matching the threshold mechanism used
                # by GPU QSlim implementations without sorting or partitioning every edge.
                ordered_cost = cp.maximum(costs, cp.float32(0.0)).astype(cp.float32)
                cost_bins = (ordered_cost.view(cp.uint32) >> cp.uint32(24)).astype(cp.int32)
                histogram = cp.bincount(cost_bins, minlength=256)
                cutoff_bin = cp.searchsorted(
                    cp.cumsum(histogram, dtype=cp.int64), eligible_count
                ).astype(cp.int32)
                selected = selected[cost_bins <= cutoff_bin]
        else:
            # Each vertex proposes its cheapest incident edge. An edge collapses only when both
            # endpoints choose it, producing a deterministic vertex-disjoint batch.
            rank = cp.empty(len(order), dtype=cp.int64)
            rank[order] = cp.arange(len(order), dtype=cp.int64)
            best = cp.full(len(gpu_points), len(order), dtype=cp.int64)
            cp.minimum.at(best, candidates[:, 0], rank)
            cp.minimum.at(best, candidates[:, 1], rank)
            selected_mask = (best[candidates[:, 0]] == rank) & (best[candidates[:, 1]] == rank)
            selected = cp.flatnonzero(selected_mask)
        if not len(selected):
            break
        # Enforce the manifold link condition and prevent two collapses from touching the same
        # one-ring neighborhood. The latter makes every accepted batch locally independent.
        directed = cp.concatenate((edges, edges[:, ::-1]), axis=0)
        directed_keys = (
            directed[:, 0].astype(cp.uint64) << 32
        ) | directed[:, 1].astype(cp.uint64)
        directed = directed[cp.argsort(directed_keys)]
        neighbors = cp.ascontiguousarray(directed[:, 1])
        degree = cp.bincount(directed[:, 0], minlength=len(gpu_points))
        offsets = cp.empty(len(gpu_points) + 1, dtype=cp.int64)
        offsets[0] = 0
        offsets[1:] = cp.cumsum(degree, dtype=cp.int64)
        selected_vertex = cp.zeros(len(gpu_points), dtype=cp.uint8)
        selected_vertex[candidates[selected].reshape(-1)] = 1
        link_valid = cp.zeros(len(selected), dtype=cp.uint8)
        blocks = (len(selected) + 255) // 256
        _VALIDATE_COLLAPSES(
            (blocks,),
            (256,),
            (
                candidates,
                selected,
                offsets,
                neighbors,
                selected_vertex,
                link_valid,
                len(selected),
            ),
        )
        selected = selected[link_valid.astype(cp.bool_)]
        link_valid_count = len(selected)
        if not len(selected):
            break
        if prefilter_face_orientation:
            pre_chosen = candidates[selected]
            pre_cost0 = cost0[selected]
            pre_cost1 = cost1[selected]
            pre_mid = cost_mid[selected]
            pre_opt = cost_opt[selected]
            pre_choose_opt = (placement_mode != "endpoint") & (
                (pre_opt <= pre_cost0)
                & (pre_opt <= pre_cost1)
                & (pre_opt <= pre_mid)
            )
            pre_choose_mid = (placement_mode != "endpoint") & (
                ~pre_choose_opt & (pre_mid <= pre_cost0) & (pre_mid <= pre_cost1)
            )
            pre_choose_first = pre_cost0 <= pre_cost1
            pre_winners = cp.where(pre_choose_first, pre_chosen[:, 0], pre_chosen[:, 1])
            pre_losers = cp.where(pre_choose_first, pre_chosen[:, 1], pre_chosen[:, 0])
            pre_positions = cp.where(
                pre_choose_opt[:, None],
                optimal[selected],
                cp.where(
                    pre_choose_mid[:, None],
                    midpoint[selected],
                    gpu_points[pre_winners],
                ),
            )
            flat_vertices = gpu_faces.reshape(-1)
            incident_face_ids = cp.repeat(cp.arange(len(gpu_faces), dtype=cp.int64), 3)
            incidence_order = cp.argsort(flat_vertices)
            incident_faces = cp.ascontiguousarray(incident_face_ids[incidence_order])
            incident_degree = cp.bincount(flat_vertices, minlength=len(gpu_points))
            face_offsets = cp.empty(len(gpu_points) + 1, dtype=cp.int64)
            face_offsets[0] = 0
            face_offsets[1:] = cp.cumsum(incident_degree, dtype=cp.int64)
            safe = cp.ones(len(selected), dtype=cp.uint8)
            _VALIDATE_FACE_ORIENTATION(
                ((len(selected) + 255) // 256,),
                (256,),
                (
                    gpu_points,
                    gpu_faces,
                    face_offsets,
                    incident_faces,
                    pre_winners,
                    pre_losers,
                    pre_positions,
                    safe,
                    len(selected),
                ),
            )
            selected = selected[safe.astype(cp.bool_)]
            if not len(selected):
                break
        if scheduling != "cavity":
            selected = selected[cp.argsort(costs[selected])]
        if scheduling in ("one-ring", "priority"):
            forbidden = cp.zeros(len(gpu_points), dtype=cp.uint8)
            accepted = cp.zeros(len(selected), dtype=cp.uint8)
            _GREEDY_ONE_RING(
                (1,),
                (1,),
                (candidates, selected, offsets, neighbors, forbidden, accepted, len(selected)),
            )
            selected = selected[accepted.astype(cp.bool_)]
            if not len(selected):
                break
        elif scheduling == "cavity":
            # A collapse owns the complete one-ring cavity around both endpoints. Select an
            # edge only when its QEM rank wins throughout that union. This is the parallel
            # equivalent of RXMesh's independent cavity filtering and prevents neighboring
            # mutations from rewriting the same faces or adjacency entries.
            endpoints = candidates[selected]
            cost_bits = costs[selected].astype(cp.float32).view(cp.uint32).astype(cp.uint64)
            descriptor = (cost_bits << cp.uint64(32)) | selected.astype(cp.uint64)
            sentinel = cp.uint64(0xFFFFFFFFFFFFFFFF)
            best_incident = cp.full(len(gpu_points), sentinel, dtype=cp.uint64)
            cp.minimum.at(best_incident, endpoints[:, 0], descriptor)
            cp.minimum.at(best_incident, endpoints[:, 1], descriptor)
            cavity_best = best_incident.copy()
            cp.minimum.at(cavity_best, directed[:, 0], best_incident[directed[:, 1]])
            keep_cavity = (
                (descriptor <= cavity_best[endpoints[:, 0]])
                & (descriptor <= cavity_best[endpoints[:, 1]])
            )
            selected = selected[keep_cavity]
            cavity_selected_count = len(selected)
            if not len(selected):
                break
        elif scheduling == "vertex":
            # Build a large maximal matching with vectorized mutual-priority rounds. The old
            # prototype ran a greedy loop in one CUDA thread, serializing millions of edges.
            remaining = selected
            claimed = cp.zeros(len(gpu_points), dtype=cp.bool_)
            accepted_rounds = []
            for _ in range(12):
                if not len(remaining):
                    break
                endpoints = candidates[remaining]
                available = ~claimed[endpoints[:, 0]] & ~claimed[endpoints[:, 1]]
                remaining = remaining[available]
                endpoints = endpoints[available]
                if not len(remaining):
                    break
                local_rank = cp.arange(len(remaining), dtype=cp.int64)
                best = cp.full(len(gpu_points), len(remaining), dtype=cp.int64)
                cp.minimum.at(best, endpoints[:, 0], local_rank)
                cp.minimum.at(best, endpoints[:, 1], local_rank)
                mutual = (
                    (best[endpoints[:, 0]] == local_rank)
                    & (best[endpoints[:, 1]] == local_rank)
                )
                batch = remaining[mutual]
                if not len(batch):
                    break
                accepted_rounds.append(batch)
                claimed[candidates[batch].reshape(-1)] = True
                remaining = remaining[~mutual]
            selected = (
                cp.concatenate(accepted_rounds)
                if accepted_rounds
                else cp.empty(0, dtype=cp.int64)
            )
            if not len(selected):
                break
        # An interior edge normally removes two faces. Cap the batch near the requested count.
        remaining_collapses = max(1, (len(gpu_faces) - target_faces + 1) // 2)
        # Vertex-disjoint matching is already the batch-conflict guard. Artificially limiting
        # it to one percent of vertices turns topology maintenance into the dominant cost by
        # forcing dozens of complete edge/index rebuilds.
        wanted = (
            remaining_collapses
            if scheduling in ("vertex", "cavity")
            else min(remaining_collapses, max(256, len(gpu_points) // 100))
        )
        if len(selected) > wanted:
            if scheduling == "cavity":
                selected = selected[cp.argpartition(costs[selected], wanted - 1)[:wanted]]
            else:
                selected = selected[cp.argsort(costs[selected])[:wanted]]
        chosen = candidates[selected]
        selected_cost0 = cost0[selected]
        selected_cost1 = cost1[selected]
        selected_mid = cost_mid[selected]
        selected_opt = cost_opt[selected]
        choose_opt = (placement_mode != "endpoint") & (
            (selected_opt <= selected_cost0)
            & (selected_opt <= selected_cost1)
            & (selected_opt <= selected_mid)
        )
        choose_mid = (placement_mode != "endpoint") & (
            ~choose_opt
            & (selected_mid <= selected_cost0)
            & (selected_mid <= selected_cost1)
        )
        choose_first = selected_cost0 <= selected_cost1
        winners = cp.where(choose_first, chosen[:, 0], chosen[:, 1])
        losers = cp.where(choose_first, chosen[:, 1], chosen[:, 0])
        winner_positions = cp.where(
            choose_opt[:, None],
            optimal[selected],
            cp.where(
                choose_mid[:, None],
                (gpu_points[chosen[:, 0]] + gpu_points[chosen[:, 1]]) * 0.5,
                gpu_points[winners],
            ),
        )
        if validate_face_orientation:
            # This compatibility guard needs a global vertex-to-face index. Cavity mode uses
            # isolated link-valid local reconstruction instead, so avoid building this index.
            flat_vertices = gpu_faces.reshape(-1)
            incident_face_ids = cp.repeat(cp.arange(len(gpu_faces), dtype=cp.int64), 3)
            incidence_order = cp.argsort(flat_vertices)
            incident_faces = cp.ascontiguousarray(incident_face_ids[incidence_order])
            incident_degree = cp.bincount(flat_vertices, minlength=len(gpu_points))
            face_offsets = cp.empty(len(gpu_points) + 1, dtype=cp.int64)
            face_offsets[0] = 0
            face_offsets[1:] = cp.cumsum(incident_degree, dtype=cp.int64)
            orientation_valid = cp.ones(len(selected), dtype=cp.uint8)
            orientation_blocks = (len(selected) + 255) // 256
            _VALIDATE_FACE_ORIENTATION(
                (orientation_blocks,),
                (256,),
                (
                    gpu_points,
                    gpu_faces,
                    face_offsets,
                    incident_faces,
                    winners,
                    losers,
                    winner_positions,
                    orientation_valid,
                    len(selected),
                ),
            )
            keep = orientation_valid.astype(cp.bool_)
            chosen, winners, losers, winner_positions = (
                chosen[keep], winners[keep], losers[keep], winner_positions[keep]
            )
            selected = selected[keep]
        if not len(selected):
            break
        orientation_valid_count = len(selected)
        gpu_points[winners] = winner_positions
        gpu_quadrics[winners] += gpu_quadrics[losers]
        representative = cp.arange(len(gpu_points), dtype=cp.int64)
        representative[losers] = winners
        used, compact = cp.unique(representative, return_inverse=True)
        gpu_points = gpu_points[used]
        gpu_quadrics = gpu_quadrics[used]
        if boundary_vertex is not None:
            boundary_vertex = boundary_vertex[used]
        gpu_faces = _gpu_unique_faces(compact[gpu_faces])
        cp.cuda.Stream.null.synchronize()
        timings["passes"].append(
            {
                "pass": pass_index + 1,
                "seconds": time.perf_counter() - pass_started,
                "collapses": len(selected),
                "candidate_edges": candidate_count,
                "link_valid_edges": link_valid_count,
                "cavity_selected_edges": (
                    cavity_selected_count if scheduling == "cavity" else None
                ),
                "orientation_valid_edges": orientation_valid_count,
                "triangles": len(gpu_faces),
                "vertices": len(gpu_points),
            }
        )

    started = time.perf_counter()
    output_points = cp.asnumpy(gpu_points).astype(np.float32, copy=False)
    output_faces = cp.asnumpy(gpu_faces).astype(np.int32, copy=False)
    timings["download_seconds"] = time.perf_counter() - started
    timings["compute_seconds"] = sum(item["seconds"] for item in timings["passes"])
    timings["total_seconds"] = (
        timings["upload_seconds"] + timings["compute_seconds"] + timings["download_seconds"]
    )
    return output_points, output_faces, timings


def gpu_quadric_cluster_reduce(points: np.ndarray, faces: np.ndarray, target_faces: int):
    """Streaming vertex clustering with a QEM-minimizing representative per occupied cell.

    This follows the public DeCoro/Lindstrom formulation. Unlike centroid voxel clustering,
    every cluster accumulates incident face quadrics and solves for the least-error point. The
    solve is clamped to the occupied cell to prevent unstable singular systems from moving a
    representative across unrelated geometry.
    """
    timings = {}
    started = time.perf_counter()
    p = cp.asarray(points)
    f = cp.asarray(faces)
    low = cp.min(p, axis=0)
    high = cp.max(p, axis=0)
    quadrics = _gpu_vertex_quadrics(p, f)
    cp.cuda.Stream.null.synchronize()
    timings["upload_and_quadrics_seconds"] = time.perf_counter() - started

    target_vertices = max(4, target_faces // 2)
    started = time.perf_counter()
    (cell_size, estimated_vertices), trials = choose_cell_size(p, low, high, target_vertices)
    timings["cell_search_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    keys = packed_voxel_keys(p, low, cell_size)
    _, inverse = cp.unique(keys, return_inverse=True)
    count = int(cp.max(inverse).get()) + 1
    cluster_q = cp.stack(
        [cp.bincount(inverse, weights=quadrics[:, i], minlength=count) for i in range(10)], axis=1
    )
    weights = cp.bincount(inverse, minlength=count).astype(cp.float32)
    centroid = cp.stack(
        [cp.bincount(inverse, weights=p[:, i], minlength=count) for i in range(3)], axis=1
    ) / weights[:, None]

    # Solve the symmetric 3x3 QEM system A*x=-b in a batched GPU operation. Singular cells use
    # their centroid. Clamping retains the locality guarantee of streaming vertex clustering.
    A = cp.empty((count, 3, 3), dtype=cp.float32)
    A[:, 0, 0], A[:, 0, 1], A[:, 0, 2] = cluster_q[:, 0], cluster_q[:, 1], cluster_q[:, 2]
    A[:, 1, 0], A[:, 1, 1], A[:, 1, 2] = cluster_q[:, 1], cluster_q[:, 4], cluster_q[:, 5]
    A[:, 2, 0], A[:, 2, 1], A[:, 2, 2] = cluster_q[:, 2], cluster_q[:, 5], cluster_q[:, 7]
    b = -cluster_q[:, [3, 6, 8]]
    a, ab, ac = A[:, 0, 0], A[:, 0, 1], A[:, 0, 2]
    d, dc, ff = A[:, 1, 1], A[:, 1, 2], A[:, 2, 2]
    det = a * (d * ff - dc * dc) - ab * (ab * ff - ac * dc) + ac * (ab * dc - ac * d)
    stable = cp.abs(det) > cp.float32(1e-10)
    representatives = centroid.copy()
    if int(cp.count_nonzero(stable).get()):
        inv00 = d * ff - dc * dc
        inv01 = ac * dc - ab * ff
        inv02 = ab * dc - ac * d
        inv11 = a * ff - ac * ac
        inv12 = ab * ac - a * dc
        inv22 = a * d - ab * ab
        solved_all = cp.stack(
            (
                inv00 * b[:, 0] + inv01 * b[:, 1] + inv02 * b[:, 2],
                inv01 * b[:, 0] + inv11 * b[:, 1] + inv12 * b[:, 2],
                inv02 * b[:, 0] + inv12 * b[:, 1] + inv22 * b[:, 2],
            ),
            axis=1,
        ) / det[:, None]
        solved = solved_all[stable]
        cell_min = low + cp.floor((centroid[stable] - low) / cell_size) * cell_size
        representatives[stable] = cp.minimum(cp.maximum(solved, cell_min), cell_min + cell_size)

    mapped = inverse[f]
    mapped = _gpu_unique_faces(mapped)
    cp.cuda.Stream.null.synchronize()
    timings["reduce_seconds"] = time.perf_counter() - started
    started = time.perf_counter()
    out_points = cp.asnumpy(representatives).astype(np.float32, copy=False)
    out_faces = cp.asnumpy(mapped).astype(np.int32, copy=False)
    timings["download_seconds"] = time.perf_counter() - started
    timings["total_seconds"] = sum(v for v in timings.values() if isinstance(v, float))
    return out_points, out_faces, timings, cell_size, estimated_vertices, trials


def triangle_area(points: np.ndarray, faces: np.ndarray) -> float:
    chunk = 500_000
    total = 0.0
    for start in range(0, len(faces), chunk):
        tri = points[faces[start : start + chunk]].astype(np.float64)
        total += float(np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1).sum() * 0.5)
    return total


def topology_metrics(faces: np.ndarray) -> dict[str, int]:
    edges = np.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]))
    edges.sort(axis=1)
    _, counts = np.unique(edges, axis=0, return_counts=True)
    return {
        "boundary_edges": int(np.count_nonzero(counts == 1)),
        "nonmanifold_edges": int(np.count_nonzero(counts > 2)),
    }


def quality_metrics(
    source_points: np.ndarray,
    source_faces: np.ndarray,
    output_points: np.ndarray,
    output_faces: np.ndarray,
    sample_count: int,
) -> dict[str, object]:
    rng = np.random.default_rng(20261005)
    sample_count = min(sample_count, len(source_points))
    sample = source_points[rng.choice(len(source_points), sample_count, replace=False)]
    tree = cKDTree(output_points)
    distances, _ = tree.query(sample, workers=-1)
    source_bounds = np.vstack((source_points.min(axis=0), source_points.max(axis=0)))
    output_bounds = np.vstack((output_points.min(axis=0), output_points.max(axis=0)))
    source_area = triangle_area(source_points, source_faces)
    output_area = triangle_area(output_points, output_faces)
    result = {
        "triangles": len(output_faces),
        "vertices": len(output_points),
        "dimension_drift": np.abs(np.diff(output_bounds, axis=0)[0] - np.diff(source_bounds, axis=0)[0]).tolist(),
        "sample_nearest_vertex_rms": float(np.sqrt(np.mean(distances * distances))),
        "sample_nearest_vertex_p95": float(np.percentile(distances, 95)),
        "surface_area_ratio": float(output_area / source_area),
    }
    result.update(topology_metrics(output_faces))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--target", type=int, default=250_000)
    parser.add_argument("--sample-count", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    process = psutil.Process()
    device = cp.cuda.Device()
    props = cp.cuda.runtime.getDeviceProperties(device.id)
    report = {
        "input": os.fspath(args.input),
        "target_triangles": args.target,
        "cuda_device": {
            "visible_index": device.id,
            "name": props["name"].decode() if isinstance(props["name"], bytes) else props["name"],
            "compute_capability": f"{props['major']}.{props['minor']}",
            "total_vram_bytes": int(props["totalGlobalMem"]),
        },
    }

    started = time.perf_counter()
    triangles = load_binary_stl(args.input)
    report["load_seconds"] = time.perf_counter() - started
    report["source_triangles"] = len(triangles)

    source_points, source_faces, connect_seconds = connected_arrays(triangles)
    report["connectivity_seconds"] = connect_seconds
    report["source_vertices"] = len(source_points)

    gpu_points, gpu_faces, gpu_timing, cell, estimate, trials = gpu_voxel_reduce(
        triangles, args.target
    )
    report["gpu_voxel"] = {
        "timing": gpu_timing,
        "cell_size": cell,
        "search_estimated_vertices": estimate,
        "search_trials": trials,
        "quality": quality_metrics(
            source_points, source_faces, gpu_points, gpu_faces, args.sample_count
        ),
    }

    (
        feature_points,
        feature_faces,
        feature_timing,
        feature_cell,
        feature_estimate,
        feature_trials,
        preserved_vertices,
    ) = gpu_feature_voxel_reduce(source_points, source_faces, args.target)
    report["gpu_feature_voxel"] = {
        "timing": feature_timing,
        "cell_size": feature_cell,
        "search_estimated_vertices": feature_estimate,
        "search_trials": feature_trials,
        "preserved_irregular_vertices": preserved_vertices,
        "quality": quality_metrics(
            source_points, source_faces, feature_points, feature_faces, args.sample_count
        ),
    }

    cluster_points, cluster_faces, cluster_timing, cluster_cell, cluster_estimate, cluster_trials = (
        gpu_quadric_cluster_reduce(source_points, source_faces, args.target)
    )
    report["gpu_quadric_cluster"] = {
        "timing": cluster_timing,
        "cell_size": cluster_cell,
        "search_estimated_vertices": cluster_estimate,
        "search_trials": cluster_trials,
        "quality": quality_metrics(
            source_points, source_faces, cluster_points, cluster_faces, args.sample_count
        ),
    }

    qem_gpu_points, qem_gpu_faces, qem_gpu_timing = gpu_qem_reduce(
        source_points, source_faces, args.target
    )
    report["gpu_qem"] = {
        "timing": qem_gpu_timing,
        "quality": quality_metrics(
            source_points, source_faces, qem_gpu_points, qem_gpu_faces, args.sample_count
        ),
    }


    parallel_points, parallel_faces, parallel_timing = gpu_qem_reduce(
        source_points, source_faces, args.target, scheduling="vertex-disjoint"
    )
    report["gpu_parallel_qem"] = {
        "timing": parallel_timing,
        "quality": quality_metrics(
            source_points, source_faces, parallel_points, parallel_faces, args.sample_count
        ),
    }

    started = time.perf_counter()
    qem_points, qem_faces = fast_simplification.simplify(
        source_points,
        source_faces,
        target_count=args.target,
        agg=7.0,
        verbose=False,
        preserve_border=True,
    )
    qem_seconds = time.perf_counter() - started
    report["cpu_fast_qem"] = {
        "timing": {"reduce_seconds": qem_seconds},
        "quality": quality_metrics(
            source_points, source_faces, qem_points, qem_faces, args.sample_count
        ),
    }
    report["peak_rss_bytes"] = int(process.memory_info().rss)
    report["gpu_memory_pool_peak_bytes"] = int(cp.get_default_memory_pool().total_bytes())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
