# Reduction algorithm comparison

This report compares every production reducer in MeshMill and the completed GPU and surface-field
prototypes. It records quality and runtime separately because reaching a target quickly is not useful
when the result changes topology or the model envelope beyond an acceptable amount.

For the focused production comparison with matched resident timings and close wireframe and
physical-density renders, see
[`CURRENT_BEST_COMPARISON.md`](CURRENT_BEST_COMPARISON.md).

## Reproduction setup

- Fixture: `samples/original-scan.stl`
- Input size: 196.8 MB
- Input geometry: 4,126,315 triangles, 2,070,061 vertices
- Input dimensions: 831.659 x 371.834 x 479.154 mm
- Requested production target: 250,000 triangles
- Host: Windows 11 Pro, Intel Core i9-7900X, 10 cores and 20 logical processors
- Memory: 63.7 GiB
- GPU used by GPU prototypes: NVIDIA GeForce RTX 3060, 12 GiB
- Production timing: packaged `MeshMillCLI.exe`, complete process wall time

The fixture intentionally contains open boundaries, layered surfaces, overlap, uneven density, and
redundant geometry. Those properties make it a difficult but representative comparison case.

## Metric definitions

- **RMS**: root mean square distance from sampled original vertices to their nearest output vertex.
- **P95**: 95th percentile of those sampled distances.
- **Area error**: $|A_{out}/A_{in}-1|\times100\%$.
- **Max drift**: largest component of the axis-aligned dimension drift.
- **Boundary edges**: mesh edges referenced by exactly one triangle. This is not a semantic hole
  count.
- **Non-manifold edges**: mesh edges referenced by more than two triangles.

The sampled nearest-vertex distance is reproducible and useful for relative testing. It is not a
symmetric surface Hausdorff distance and can understate some errors. Visual review uses matched,
close wireframe and density views. Shaded and vertices modes remain useful secondary checks, but
they do not replace direct inspection of triangle placement and local density allocation.

## Current application algorithms

| Algorithm | Wall time | Triangles | Vertices | Max drift | RMS | P95 | Area error | Boundary | Non-manifold |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fast QEM | 16.623 s | 249,999 | 127,010 | 0.6987 mm | 1.1721 mm | 2.3504 mm | 0.3993% | 4,329 | 54 |
| Density balanced | 18.473 s | 249,999 | 131,947 | 0.0030 mm | 1.2041 mm | 2.4341 mm | 0.0405% | 14,215 | 52 |
| Shape preserving | 63.529 s | 250,000 | 130,299 | 0.0009 mm | 1.1933 mm | 2.3323 mm | 0.0491% | 10,892 | 26 |
| Preserve topology | 41.153 s | 249,999 | 131,903 | 0.0000 mm | 3.1672 mm | 6.8266 mm | 0.0709% | 14,215 | 5 |

### Interpretation

- **Fast QEM** was fastest and had the best sampled RMS in this run. It changed the model bounds
  most and removed many source boundary edges.
- **Density balanced** preserved the source boundary-edge count and nearly preserved the envelope
  and surface area. Its RMS and P95 were slightly worse than Fast QEM. The result supports its role
  as a conservative open-scan preset, not a universally higher-quality reducer.
- **Shape preserving** had the best P95 and the lowest nonzero drift, with a major runtime cost. It
  produced fewer non-manifold edges than either Fast QEM mode.
- **Preserve topology** exactly preserved the dimensions and retained the source boundary-edge
  count. Its nearest-vertex distances were substantially worse, illustrating the geometric cost of
  restricting legal topology operations on this layered, open input.

No single row wins every metric. The selection depends on whether runtime, envelope, open
boundaries, topology, or local surface proximity matters most.

## Completed experimental reducers

These results use the same full fixture and approximately the same target when the prototype could
reach it.

| Prototype | Compute time | Triangles | Max drift | RMS | P95 | Area ratio | Boundary | Non-manifold | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| GPU voxel clustering | 0.771 s | 243,813 | 0.8465 mm | 0.8105 mm | 1.2489 mm | 0.98079 | 9,614 | 3,297 | Rejected: merges nearby unrelated sheets |
| GPU quadric clustering | 2.173 s | 243,813 | 0.0656 mm | 1.0991 mm | 1.8288 mm | 1.44145 | 9,614 | 3,297 | Rejected: severe folded-area growth |
| GPU conservative QEM | 66.936 s | 722,687 | 0.3953 mm | 1.5368 mm | 3.2350 mm | 1.01143 | 14,215 | 0 | Rejected: slow and stalls above target |
| GPU parallel QEM | 25.282 s | 706,682 | 0.6213 mm | 1.5313 mm | 3.2820 mm | 1.01092 | 14,533 | 170 | Rejected: topology damage and stalls |
| Complete GPU QEM | 19.486 s | 249,999 | 0.0538 mm | 2.6929 mm | 5.9292 mm | 1.00655 | 14,215 | 0 | Rejected: slower and less accurate than CPU |
| Depth-gauge surface sheets | 2.581 s | 224,730 | 0.0000 mm | 1.2139 mm | 2.1807 mm | n/a | n/a | n/a | Incomplete: output is six overlapping open sheets |
| GPU trajectory normals + VTK QEM | 65.339 s resident compute | 250,000 | 0.0466 mm | 1.3385 mm | 2.6944 mm | 1.00065 | 14,223 | 43 | Rejected: slower and less accurate than Shape preserving |
| GPU trajectory projection + Fast QEM | 12.526 s resident compute | 249,999 | 0.0177 mm | 1.1208 mm | 2.1526 mm | 1.00068 | 14,215 | 46 | Candidate: assembled output and best sampled distance |
| Adaptive physical probes + Fast QEM | 12.673 s resident compute | 249,999 | 0.0205 mm | 1.2348 mm | 2.5292 mm | 1.00107 | 14,215 | 41 | Architecture retained; projection result needs refinement |
| Depth Adaptive QEM, aggressiveness 8 | **10.156 s median resident** | 249,999 | 0.0234 mm | **1.0668 mm** | **2.0586 mm** | 1.00124 | 14,215 | Production GPU / Higher Quality option |
| Adaptive probe scalar + VTK QEM | 61.096 s resident compute | 250,000 | 0.1236 mm | 1.2591 mm | 2.4558 mm | 1.00150 | 13,626 | 30 | Rejected: scalar magnitude is not a local quota |
| Probe partitions + weld + global QEM | 26.536 s resident compute | 250,000 | 0.0176 mm | 1.7353 mm | 3.4573 mm | 1.00182 | 14,242 | 35 | Rejected: pinned interfaces damage collapse ordering |

The complete GPU QEM compute time excludes 11.706 seconds spent constructing mutable connectivity.
Even under that favorable accounting, it did not beat the packaged Fast QEM wall time and its
sampled surface error was higher.

The depth-gauge prototype was fast and geometrically promising as a sampled surface envelope. It
did not reconstruct the source mesh's connectivity. Its six directional sheets overlap and remain
open, so the triangle count is not directly equivalent to a production decimator's result.

The trajectory-projection follow-up resolves that assembly failure by retaining the source indexed
mesh, moving only statistically supported surface outliers toward multiscale tangent planes, and
passing the resulting vertices and original faces to boundary-preserving Fast QEM. GPU analysis took
0.593 seconds and CPU QEM took 11.933 seconds. Initial connectivity construction took 11.085 seconds;
that cost is excluded from resident compute because an open MeshMill model already has indexed
connectivity. The complete standalone process, including loading, connectivity, metrics, and output,
took 25.810 seconds.

At a 0.05 mm projection cap, it produced the lowest RMS and P95 of the tested 250,000-triangle
outputs, retained all 14,215 source boundary edges, and limited area error to 0.0681%. Maximum
dimension drift was 0.0177 mm and 46 non-manifold edges remained after Fast QEM. This is a viable
a production option, with continued testing on broader fixtures.

The adaptive physical-probe follow-up derived probe diameter, hemispherical tip radius, and spacing
from source edge length, surface area, and the target triangle count. It assigned each face to the
widest locally valid pitch. On flat regions, 311 coarse probes represented 273,988 faces. Curved or
conflicting areas refined through 2,258, 14,350, and 51,519 probes, while 686,197 unresolved faces
were left unchanged. Its GPU analysis took 0.955 seconds. The resulting sampled distances were worse
than the fixed-scale candidate, so the adaptive hierarchy is retained while its projection rule
requires further work.

Two allocation refinements were then tested. Encoding adaptive density as a VTK scalar did not make
the scalar magnitude act as a triangle quota and was slower than Shape preserving. Reducing the five
probe levels independently caused their pinned interfaces to stall at 690,124 triangles. Welding and
a global reconciliation pass reached 250,000, but the two-stage collapse history increased RMS to
1.7353 mm. These results rule out attribute preservation and hard regional partitioning. Adaptive
probe density needs to modify edge costs inside one global QEM pass.

## Boundary-safe tiled experiments

Protecting tile interfaces avoided new non-manifold edges, but it also prevented useful reduction:

| Grid | Time | Output triangles | RMS | P95 | Area ratio | Non-manifold |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 x 3 x 3 | 30.043 s | 2,787,643 | 0.7912 mm | 1.8684 mm | 1.00031 | 0 |
| 4 x 4 x 4 | 29.450 s | 2,297,205 | 0.9192 mm | 2.0667 mm | 1.00042 | 0 |
| 5 x 5 x 5 | 30.671 s | 2,039,801 | 0.9782 mm | 2.1490 mm | 1.00033 | 0 |

Tiles are useful for out-of-core storage, scheduling, visibility, and bounded working sets. Treating
tile boundaries as permanently fixed geometry creates seams or blocks reduction. A production
tiled reducer needs halos, shared boundary ownership, and a global reconciliation pass.

## GPU analysis benchmark

The surface-field prototype evaluated multiscale geometric evidence at three scales. It completed in
0.581 seconds on the GPU and 5.819 seconds on the CPU, about 10 times faster. This is a useful GPU
workload because face planes, normal variation, density, and scale-space evidence can be calculated
independently before topology changes.

That result does not imply a 10-times-faster complete reducer. Mesh assembly and topology mutation
remain the expensive serial or synchronization-heavy steps.

## Findings

1. A GPU-resident buffer removes repeated upload cost, but it does not remove adjacency building,
   conflict resolution, or legal-collapse checks.
2. Spatial clustering is fast because it avoids most topology reasoning. That is also why it merges
   separate sheets and creates non-manifold results.
3. Parallel edge collapse exposes useful GPU work, but independent local choices still conflict.
   Conservative scheduling preserves topology and stalls; relaxed scheduling progresses faster and
   damages topology.
4. Global surface analysis is a better proven GPU role than unconstrained mesh mutation on this
   fixture.
5. Reconstructing disconnected directional depth sheets is unnecessary. Bounded projection of the
   original indexed mesh supplies an assembled output while retaining open boundaries.
6. The trajectory-projection candidate improves sampled RMS and P95, but introduces a small
   preprocessing displacement and still inherits Fast QEM's non-manifold behavior. CPU Fast QEM
   remains the released baseline until broader regression and visual testing pass.

## Research provenance

The prototypes were implemented locally from published descriptions and public source for study;
they do not package those projects as dependencies.

- [Garland and Heckbert, Surface Simplification Using Quadric Error Metrics](https://publications.ri.cmu.edu/surface-simplification-using-quadric-error-metrics)
- [DeCoro and Lindstrom, Real-time Mesh Simplification Using the GPU](https://gfx.cs.princeton.edu/gfx/pubs/DeCoro_2007_RMS/real_time_simplification.pdf)
- [Topology-preserving parallel mesh simplification study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8341488/)
- [RXMesh public implementation](https://github.com/owensgroup/RXMesh)
- [Trellis public implementation](https://github.com/pwilkin/trellis.cpp)
- [Fast Quadric Mesh Simplification](https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification)
- [VTK](https://github.com/Kitware/VTK)

## Reproducibility files

The benchmark programs are in this directory. Detailed local JSON reports are generated outside the
repository because they include machine-specific paths and environment data. Relevant scripts
include:

- `gpu_geometry_prototype.py`
- `gpu_complete_reducer.py`
- `boundary_first_tiles.py`
- `surface_field_prototype.py`
- `surface_field_cpu_baseline.py`
- `surface_field_synthetic_test.py`
- `depth_gauge_prototype.py`
- `depth_gauge_fusion.py`
- `depth_gauge_prefilter_qem.py`
- `gpu_surface_guided_qem.py`
- `gpu_trajectory_prefilter_qem.py`
- `gpu_adaptive_probe_qem.py`
- `gpu_probe_budget_qem.py`
- `gpu_probe_partition_qem.py`
- `benchmark_parallel_tile_analysis.py`

Run comparisons against the same source checksum and target. Record package versions, hardware,
process timing boundaries, and whether connectivity construction is included.
