# GPU geometry reduction prototype

These experiments evaluated published GPU approaches and implementation strategies. The rejected
approaches below did not produce Depth Adaptive QEM. That algorithm originated with the
project author's physical depth-gauge analogy and combines adaptive physical probes with the
existing Fast QEM assembly backend. Its derivation and the reason GPU acceleration does not
automatically accelerate topology mutation are documented in
[`DEPTH_GAUGE_REDUCTION.md`](../docs/DEPTH_GAUGE_REDUCTION.md).

This experiment is isolated from the MeshMill application. It does not alter the application,
runtime dependencies, user settings, or released algorithms.

## Test setup

- Input: `samples/original-scan.stl`
- Source: 4,126,315 triangles and 2,070,061 connected vertices
- Target: 250,000 triangles
- GPU: Windows-active NVIDIA GeForce RTX 3060, compute capability 8.6
- CPU comparison: MeshMill's Fast QEM backend, `agg=7`, with boundary preservation
- GPU prototype: voxel clustering with GPU target search, cluster averaging, degenerate-face
  removal, and duplicate-face removal

The prototype records transfer and compute time separately. Production use could share an
OpenGL/CUDA-compatible geometry buffer with the viewer, so the comparison does not treat the
prototype's avoidable upload as GPU compute cost.

## Results

| Measurement | GPU voxel prototype | CPU Fast QEM |
| --- | ---: | ---: |
| Output triangles | 243,813 | 249,999 |
| Output vertices | 124,937 | 131,947 |
| Upload | 0.317 s | n/a |
| GPU target search | 0.342 s | n/a |
| Reduction kernel | 0.153 s | n/a |
| Download | 0.005 s | n/a |
| Total prototype reduction | 0.817 s | 9.598 s |
| Resident processing (search + reduction) | 0.495 s | 9.598 s |
| Peak GPU memory pool | 995 MiB | n/a |
| Maximum dimension drift | 0.846 mm | 0.005 mm |
| Surface-area ratio | 0.9808 | 1.0005 |
| Boundary edges | 9,614 | 14,215 |
| Non-manifold edges | 3,297 | 52 |

The GPU prototype is about 11.7 times faster including transfer and about 19.4 times faster when
the geometry is treated as GPU-resident. Its reduction kernel alone is about 62.6 times faster
than the CPU comparison, but target search remains part of a complete automatic operation.

## Decision

GPU geometry processing is technically worthwhile on this scan. Voxel clustering is not suitable
as MeshMill's production reducer because it merges unrelated nearby surfaces, introduces
non-manifold geometry, and changes the model envelope more than Fast QEM.

## Topology-safe GPU QEM follow-up

A second prototype calculated quadrics and edge costs on the GPU, validated the manifold link
condition, pinned irregular boundaries, and scheduled vertex-disjoint collapses with disjoint
one-ring neighborhoods. It used QEM-tested endpoint or midpoint placement rather than spatial
clustering.

On the 250,000-triangle sample, it reached 50,000 triangles with no increase in non-manifold edges,
zero drift on two dimensions, 0.032 mm drift on the third dimension, and a 0.9995 surface-area
ratio. This established that a GPU path can preserve topology on clean-enough local regions.

On the complete scan, the same safety rules stopped at 722,687 triangles because no further legal
collapses remained:

| Measurement | Topology-safe GPU QEM | CPU Fast QEM |
| --- | ---: | ---: |
| Requested triangles | 250,000 | 250,000 |
| Output triangles | 722,687 | 249,999 |
| Reduction time | 67.489 s | 9.701 s |
| Maximum dimension drift | 0.395 mm | 0.005 mm |
| Sample nearest-vertex RMS | 1.537 mm | 1.193 mm |
| Surface-area ratio | 1.0114 | 1.0005 |
| Boundary edges | 14,215 | 14,215 |
| Non-manifold edges | 0 | 52 |

This version protects topology but is too conservative and too slow on the composite scan. It also
does not meet the requested triangle count or the CPU baseline's geometric accuracy. It is not a
result selected for application integration.

## Public-algorithm prototypes

Two further variants were reproduced in Python/CuPy from published algorithm descriptions and
permissively licensed source references. No external geometry runtime is linked or packaged.

- **Quadric cluster** follows the streaming vertex-clustering formulation described by DeCoro and
  Lindstrom. Each cell accumulates face quadrics and solves for a clamped least-error
  representative instead of averaging its vertices.
- **Parallel QEM** follows the independent-collapse direction used by RXMesh and other GPU QEM
  systems, with vertex-disjoint batches and link-condition validation. It relaxes the conservative
  prototype's disjoint-one-ring scheduler to expose more parallel work.

Full-scan results at a 250,000-triangle target:

| Algorithm | Time | Output triangles | Max drift | Sample RMS | Area ratio | Boundary | Non-manifold |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GPU voxel | 0.771 s | 243,813 | 0.8465 mm | 0.8105 mm | 0.98079 | 9,614 | 3,297 |
| GPU quadric cluster | 2.173 s | 243,813 | 0.0656 mm | 1.0991 mm | 1.44145 | 9,614 | 3,297 |
| GPU conservative QEM | 66.936 s | 722,687 | 0.3953 mm | 1.5368 mm | 1.01143 | 14,215 | 0 |
| GPU parallel QEM | 25.282 s | 706,682 | 0.6213 mm | 1.5313 mm | 1.01092 | 14,533 | 170 |
| CPU Fast QEM | 10.097 s | 249,999 | 0.0053 mm | 1.1927 mm | 1.00046 | 14,215 | 52 |

Quadric representatives materially improve the clustering envelope, but clustering still merges
unrelated nearby surfaces and can fold triangles over one another. The 1.44145 area ratio rejects
that output despite its speed and target count. Relaxing collapse scheduling improves GPU QEM
runtime but introduces topology damage and still stalls far above the requested count.

These results reject unrestricted clustering and the tested Python/CuPy mutation paths for product
integration. A later implementation would need a native, fully resident topology engine that avoids
per-collapse host coordination and matches the CPU baseline before it is considered.

1. Keep vertices, faces, quadrics, and candidate costs resident on the GPU.
2. Use the GPU for face planes, quadric accumulation, edge extraction, error scoring, flip tests,
   and conflict labeling.
3. Transfer only a compact ordered candidate batch to a CPU topology coordinator.
4. Commit legal collapses with an authoritative mutable adjacency structure, returning only local
   dirty ranges to the GPU.
5. Measure whether the reduced CPU work exceeds the synchronization cost before considering app
   integration.

If a custom implementation remains necessary, it should keep topology-changing decisions explicit:

1. Reuse or share the viewer's resident vertex and index buffers through supported graphics/compute
   interoperability rather than assuming that an OpenGL buffer is automatically a CUDA array.
2. Calculate quadric errors, density statistics, and independent edge-collapse candidates in
   parallel on the GPU.
3. Partition candidates into conflict-free batches.
4. Preserve boundary, non-manifold, material, and tile-border vertices unless a validated collapse
   explicitly permits them.
5. Apply topology changes in deterministic batches and rebuild affected adjacency locally.
6. Validate dimension drift, surface area, flipped faces, boundary changes, non-manifold edges, and
   tile seams after each pass.
7. Retain CPU Fast QEM as the quality baseline and fallback until the GPU path matches it.

Raw local result files:

- `meshmill-gpu-sample-results.json`
- `meshmill-gpu-original-results.json`
- `meshmill-gpu-sample-results-v9.json`
- `meshmill-gpu-original-results-v9.json`
- `meshmill-gpu-public-algorithms.json`

## Native RXMesh and exterior-cleanup checks

RXMesh QSlim was compiled from its public source with CUDA 12.4 and run against the same scan. The
conversion needed to prepare its input took 23.21 seconds and was excluded from reducer timing. The
native reduction did not produce output within 150 seconds, so it was stopped. This does not support
replacing MeshMill's roughly 10-second Fast QEM path with RXMesh for this input.

GPU exterior filtering was also measured before QEM. Exact duplicate and degenerate removal found
no removable faces. Conservative component cleanup removed nothing and took 11.95 seconds including
QEM. A moderate filter removed 70,892 triangles but increased total time to 14.05 seconds and reduced
surface-area retention to 98.15%. An aggressive filter removed 51.79% of the source, but retained
only 42.56% of its surface area and created 168,357 boundary edges. These filters are rejected.

The release therefore keeps GPU acceleration for rendering, picking, density visualization, and
measured surface analysis. Production mesh mutation remains on the native CPU reducer because it is
faster than the tested topology-safe GPU paths and produces the best complete result.

## Surface-trajectory assembly result

The directional depth-sheet prototype did not produce one usable source-like mesh. A later
prototype avoided sheet fusion entirely. It retained the original indexed mesh, used GPU
multiscale plane analysis to identify supported surface outliers, projected affected vertices by at
most 0.05 mm, and passed the adjusted geometry to boundary-preserving Fast QEM.

Full-scan result at 250,000 requested triangles:

| Measurement | Trajectory projection + Fast QEM | Density balanced baseline |
| --- | ---: | ---: |
| Output triangles | 249,999 | 249,999 |
| GPU surface analysis | 0.593 s | n/a |
| CPU QEM | 11.933 s | implementation-dependent |
| Resident analysis plus reduction | 12.526 s | n/a |
| Maximum dimension drift | 0.0177 mm | 0.0030 mm |
| Sample nearest-vertex RMS | 1.1208 mm | 1.2041 mm |
| Sample nearest-vertex P95 | 2.1526 mm | 2.4341 mm |
| Surface-area ratio | 1.00068 | 1.00041 |
| Boundary edges | 14,215 | 14,215 |
| Non-manifold edges | 46 | 52 |

This resolves mesh assembly for the prototype: the result is one indexed STL with the source's open
boundary count, not overlapping directional sheets. It is a candidate for additional validation,
not a released algorithm.

### Adaptive probe hierarchy

A follow-up replaced generic resolution and tolerance inputs with derived physical probe dimensions.
For the full fixture, the median source edge produced a 0.4513 mm probe diameter and 0.2256 mm
hemispherical tip radius. Surface area and the requested output count produced a 2.0553 mm closest
pitch. The GPU tested pitches of 16.4428, 8.2214, 4.1107, and 2.0553 mm, assigning a face to the
widest level whose normal spread and plane residual fit the probe geometry.

| Pitch | Active probes | Assigned source faces | Projected outlier faces |
| ---: | ---: | ---: | ---: |
| 16.4428 mm | 311 | 273,988 | 2,504 |
| 8.2214 mm | 2,258 | 587,899 | 5,218 |
| 4.1107 mm | 14,350 | 1,172,231 | 18,233 |
| 2.0553 mm | 51,519 | 1,406,000 | 18,891 |

The adaptive analysis took 0.955 seconds and left 686,197 unresolved faces unchanged. It proves that
long flat surfaces can use far fewer probes while curved regions refine locally. The first adaptive
projection output had 1.2348 mm RMS and 2.5292 mm P95 sampled distance, worse than the fixed-scale
trajectory result. The hierarchy is useful; its outlier projection rule is not yet accepted.

### Probe-budget refinements

| Refinement | Resident compute | Output triangles | RMS | P95 | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Probe density as VTK scalar attribute | 61.096 s | 250,000 | 1.2591 mm | 2.4558 mm | Rejected |
| Probe partitions, weld, global QEM | 26.536 s | 250,000 | 1.7353 mm | 3.4573 mm | Rejected |

The attribute test preserved scalar variation rather than allocating triangles in proportion to the
scalar value. The partitioned test pinned artificial interfaces, stopped at 690,124 triangles before
reconciliation, and retained a poor collapse history after the final global pass. The next
implementation should apply probe importance inside one global Fast QEM edge-cost calculation.
