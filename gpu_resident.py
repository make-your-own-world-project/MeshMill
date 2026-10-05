"""Inspection and planning for geometry already resident in the viewport GPU.

This module does not initialize CUDA or enumerate adapters. Native compute backends must bind to
the device associated with the active OpenGL context so Windows system-default selection remains
authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResidentBufferInfo:
    handle: int
    size_bytes: int
    stride_bytes: int
    components: int
    tuples: int


@dataclass(frozen=True)
class ComputeDecision:
    backend: str
    reason: str


def inspect_resident_vertices(actor) -> ResidentBufferInfo | None:
    """Return VTK's current OpenGL vertex-buffer metadata after a completed render."""
    if actor is None:
        return None
    mapper = actor.GetMapper()
    get_vbos = getattr(mapper, "GetVBOs", None)
    if get_vbos is None:
        return None
    group = get_vbos()
    if group is None:
        return None
    vertex_buffer = group.GetVBO("vertexMC")
    if vertex_buffer is None or not vertex_buffer.IsReady():
        return None
    handle = int(vertex_buffer.GetHandle())
    if handle <= 0:
        return None
    return ResidentBufferInfo(
        handle=handle,
        size_bytes=int(vertex_buffer.GetSize()),
        stride_bytes=int(vertex_buffer.GetStride()),
        components=int(vertex_buffer.GetNumberOfComponents()),
        tuples=int(vertex_buffer.GetNumberOfTuples()),
    )


def choose_compute_backend(
    triangle_count: int,
    resident: ResidentBufferInfo | None,
    *,
    interop_available: bool,
    minimum_gpu_triangles: int = 262_144,
) -> ComputeDecision:
    """Choose conservatively; availability alone never enables a GPU path."""
    if triangle_count < minimum_gpu_triangles:
        return ComputeDecision("cpu", "work unit is below the measured GPU crossover")
    if resident is None:
        return ComputeDecision("cpu", "geometry is not resident in a reusable viewport buffer")
    if not interop_available:
        return ComputeDecision("cpu", "validated graphics-compute interoperability is unavailable")
    return ComputeDecision(
        "gpu-resident", "large work unit is resident on the active graphics device"
    )
