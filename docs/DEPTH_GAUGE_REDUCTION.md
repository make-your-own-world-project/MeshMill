# Depth Adaptive QEM

## Origin and research boundary

Depth Adaptive QEM began with the project author's physical depth-gauge analogy. A
mechanical contour gauge does not reproduce every grain of dust on a surface. Its probes have a
diameter, a rounded end, and finite spacing. Wide spacing follows a broad flat trajectory. Closer
probes are needed only where curvature or unresolved form requires them. Applying that model to a
scanned mesh produced the first experimental path that improved sampled surface error while staying
close to Fast QEM speed.

Published work supplied the QEM baseline, implementation references, and several GPU strategies to
test. Those sources did not supply the adaptive physical-probe model. GPU clustering, direct GPU
QEM mutation, tiled simplification, visibility filtering, and scalar-density preservation were
implemented and measured, then rejected because they missed the target, damaged topology, reduced
quality, or took longer than the existing CPU reducer. The production algorithm combines MeshMill's
depth-gauge analysis with the established Fast QEM backend.

- **Established component:** Fast QEM performs the final global edge-collapse reduction.
- **MeshMill contribution:** physical probe dimensions, adaptive probe spacing,
  surface-coherence tests, bounded removal of supported excursions, and the resulting QEM input.
- **Comparison or rejected direction:** GPU clustering, independent parallel collapses,
  topology-safe GPU QEM, RXMesh QSlim, regional quotas, visibility cleanup, and attribute-aware QEM.

MeshMill uses the graphics hardware already available through the operating system and driver to
draw, rotate, and inspect meshes. Depth Adaptive QEM asks the GPU to perform a separate computation:
CUDA surface measurement before reduction. MeshMill bundles the minimal NVIDIA computation
libraries used by this path, avoiding a separate component or system-wide CUDA installation.

Depth Adaptive QEM appears as **Depth Adaptive QEM (GPU / Higher Quality)** in the algorithm list.
When compatible NVIDIA hardware or its driver is unavailable, the entry is muted and selecting it
explains the hardware requirement. Fast QEM remains the default, and every other built-in algorithm
continues to work. The first use prepares and caches kernels for the detected GPU and backend; that
setup does not repeat for every mesh. Broader fixtures and independent reproduction remain part of
continued validation.

## Processing path

1. Start from the indexed mesh already resident in application memory. Benchmark timing excludes
   the one-time STL connectivity conversion shared by every reducer.
2. Derive a physical probe diameter and rounded-tip radius from the source mesh.
3. Derive the finest useful probe pitch from surface area and the requested output count.
4. On the GPU, test the widest pitch first. Accept broad flat trajectories and refine only curved,
   incoherent, or unresolved regions.
5. Project small supported excursions toward the fitted trajectory. Leave unresolved geometry
   unchanged and cap every displacement.
6. Return the adjusted vertex positions once, retaining the source triangle connectivity.
7. Run one global, boundary-preserving Fast QEM pass to produce an assembled indexed mesh.

The GPU stage analyzes all faces with regular vector operations. Fast QEM remains responsible for
the dependency-heavy topology mutation.

## Physical probe model

Let the indexed mesh contain vertices $V$, edges $E$, faces $F$, surface area $A_M$, and a
requested output count $N$. The probe diameter is the median valid source-edge length:


$$
d=\operatorname{median}\left\{\lVert\mathbf v_i-\mathbf v_j\rVert:(i,j)\in E\right\}.
$$

`d` is probe diameter; `E` is the mesh-edge set; `v_i` and `v_j` are edge
endpoints; and their Euclidean distance is the edge length. The median resists extreme samples.


The probe end is a hemisphere with radius


$$
r=\frac d2.
$$

`r` is hemispherical tip radius and `d` is probe diameter.


The representative edge length for $N$ ideal equilateral output triangles is


$$
p_o=\sqrt{\frac{4A_M}{\sqrt 3N}},
\qquad p_{min}=\max(d,p_o).
$$

`p_o` is ideal output edge length; `A_M` is source surface area; `N` is the
requested triangle count; and `p_min` is the finer-scale limit, never below source spacing.


The tested hierarchy is


$$
P=\{8p_{min},4p_{min},2p_{min},p_{min}\}.
$$

`P` is the coarse-to-fine probe hierarchy and `p_min` is its finest pitch.


Each face begins at the widest pitch and advances to a denser level only when the local surface
cannot be represented safely.

## Local surface trajectory

For spatial probe cell $c$, face $f$ has area $A_f$, unit normal $\mathbf n_f$, and center
$\mathbf c_f$. The area-weighted local normal and center are


$$
\mathbf n_c=\frac{\sum_{f\in c}A_f\mathbf n_f}
{\left\lVert\sum_{f\in c}A_f\mathbf n_f\right\rVert},
\qquad
\mathbf o_c=\frac{\sum_{f\in c}A_f\mathbf c_f}{\sum_{f\in c}A_f}.
$$

`c` is a probe cell; `f` is an assigned face; `A_f`, `n_f`, and `c_f` are its
area, normal, and center; `n_c` and `o_c` are the area-weighted cell normal and center.


Normal coherence and a face center's plane residual are


$$
h_c=\frac{\left\lVert\sum_{f\in c}A_f\mathbf n_f\right\rVert}{\sum_{f\in c}A_f},
\qquad
e_f=\left|\mathbf n_c\cdot(\mathbf c_f-\mathbf o_c)\right|.
$$

`h_c` is 0-to-1 normal coherence; `e_f` is perpendicular face-center distance
from the fitted plane; values near `h_c = 1` indicate one consistent local surface direction.


An area-weighted mean and standard deviation are calculated for cell residuals. Values above
$\mu_c+2.5\sigma_c$ are excluded when testing the fitted trajectory, preventing isolated spikes
from defining the surface they are being tested against. The clipped RMS residual is


$$
R_c=\sqrt{\frac{\sum_{f\in c}A_fI_f e_f^2}{\sum_{f\in c}A_fI_f}},
$$

`R_c` is area-weighted RMS residual; `I_f` is 1 for a statistical inlier and 0
otherwise; and `e_f^2` emphasizes larger supported departures.


where $I_f$ is one for an inlier and zero otherwise. The hemispherical tip determines the maximum
local normal change supportable at pitch $p$:


$$
\theta_p=\tan^{-1}\left(\frac r{p/2}\right),
\qquad h_c\ge\cos\theta_p.
$$

`theta_p` is allowed normal variation at pitch `p`; `r` is tip radius; and the
coherence condition becomes stricter as spacing widens.


A cell is valid at that pitch when the coherence test passes and $R_c\le r$. Coarse spacing is
therefore strict on long flat surfaces. Curved or conflicting regions fall through to smaller
pitches instead of being flattened.

## Supported-excursion removal

A surface excursion is treated as removable scan noise only when it belongs to an accepted
trajectory and falls inside the physical tip interval


$$
\frac r2<e_f\le\frac{3r}{2}.
$$

`e_f` is plane residual and `r` is tip radius. Only excursions in this physical
band are eligible for correction; larger deviations remain unresolved.


For an incident vertex $\mathbf v$, orthogonal projection onto the fitted plane is


$$
\mathbf v'=\mathbf v-\mathbf n_c
\left(\mathbf n_c\cdot(\mathbf v-\mathbf o_c)\right).
$$

`v` is an original vertex; `v'` is its projection; and `n_c` and `o_c` define
the fitted plane. The projection removes only normal-direction offset.


Incident-face displacement proposals are area-weighted at each vertex. Total displacement is capped
at $d_{max}=r/4$, so repeated projection cannot erase a feature without limit. Faces unresolved at
the finest pitch remain untouched.

## QEM assembly

The probe stage preserves the source face index array. Fast QEM then evaluates edge collapses using
the standard summed vertex quadric. For supporting plane $\mathbf p=(a,b,c,d)^T$,


$$
K_p=\mathbf p\mathbf p^T.
$$

`p = (a,b,c,d)^T` is a normalized supporting plane and `K_p` is its 4-by-4
squared-distance matrix.


For an edge joining vertices $i$ and $j$,


$$
Q_{ij}=Q_i+Q_j,
\qquad
\epsilon_{ij}(\bar{\mathbf v})=\bar{\mathbf v}^{T}Q_{ij}\bar{\mathbf v},
$$

`Q_i` and `Q_j` are endpoint quadrics; `Q_ij` is their sum; `v_bar` is a proposed
replacement vertex; and `epsilon_ij` is its estimated squared geometric error.


where $\bar{\mathbf v}=(x,y,z,1)^T$ is the replacement position. Collapses are accepted in
increasing-error order subject to validity rules and boundary preservation. This global ordering is
why Depth Adaptive QEM produces one indexed output rather than independently reduced pieces with seams.

## Why a GPU does not automatically make QEM faster

GPU speed comes from running many similar, independent operations over contiguous memory. The probe
stage matches that model: face normals, centers, keys, weighted sums, residuals, masks, and
projections can be evaluated in bulk while the mesh remains in VRAM.

Topology mutation behaves differently. Collapsing edge $(i,j)$ changes the active vertices and
faces, both one-ring neighborhoods, boundary and manifold classifications, neighboring quadrics and
edge costs, and the priority order of later collapses.

Two nearby collapses are not independent. If $C(e)$ is the set of geometry touched by collapse
$e$, a safe parallel batch requires


$$
C(e_a)\cap C(e_b)=\varnothing
$$

`C(e)` is every topology record touched by collapse `e`; the empty intersection
means two collapses can run together without conflicting writes.


for every pair, plus validity after earlier accepted mutations. Finding those sets, resolving
conflicts, updating variable-length adjacency, and rebuilding priorities cause scattered memory
access, branch divergence, synchronization, atomic contention, and repeated work. A GPU can perform
these operations, but the workload uses far less of its arithmetic throughput than regular surface
analysis.

Keeping geometry in VRAM removes PCIe transfer as an explanation. It does not remove the data
dependencies. A host call around a granular CPU topology engine also leaves CPU mutation as the
gate. A useful GPU reducer must keep adjacency, validity, cost updates, conflict scheduling, and
compaction resident across many collapse rounds. The tested implementations did not beat mature
CPU Fast QEM while preserving comparable quality.

The measured conclusion is narrower than “GPUs are bad at geometry.” GPUs are effective for regular
geometry analysis and display. This reduction stage is dominated by irregular, ordered graph
mutation, which is a poor match for throughput hardware unless the complete algorithm is redesigned
around safe parallel batches.

## Controlled result

The controlled comparison used the 4,126,315-triangle composite fixture, a target of 250,000
triangles, one resident indexed mesh, and identical quality measurements.

| Method | Resident time | RMS | P95 | Maximum drift | Area error | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Fast QEM | **9.827 s** | 1.1721 mm | 2.3504 mm | 0.6987 mm | 0.3993% | Production baseline |
| Density balanced | 11.439 s | 1.2041 mm | 2.4341 mm | 0.0030 mm | **0.0405%** | Production |
| Shape preserving | 56.404 s | 1.1933 mm | 2.3323 mm | **0.0009 mm** | 0.0491% | Production |
| Depth Adaptive QEM | 10.156 s | **1.0668 mm** | **2.0586 mm** | 0.0234 mm | 0.1241% | GPU / Higher Quality option |

Compared with Fast QEM, Depth Adaptive QEM improved sampled RMS by 9.0%, P95 by 12.4%, maximum drift by
96.7%, and surface-area error by 68.9%. It was 0.329 seconds, or 3.3%, slower. Three complete
resident runs took 10.481, 10.112, and 10.156 seconds.

The derived fixture geometry was a 0.4513 mm probe diameter, 0.2256 mm tip radius, 2.0553 mm finest
pitch, and 16.4428 mm widest pitch. At the widest level, 311 probes represented 273,988 faces. Finer
levels used 2,258, 14,350, and 51,519 probes. The analysis left 686,197 faces unresolved instead of
flattening them.

## Why the other strategies were rejected

| Strategy | Measured outcome | Reason rejected |
| --- | --- | --- |
| GPU voxel clustering | About 11.7 times faster including transfer | Disconnected cells, non-manifold geometry, and excessive envelope change |
| Conservative GPU QEM | 66.936 s, 722,687 triangles | Much slower and missed the 250,000 target |
| Parallel GPU QEM | 25.282 s, 706,682 triangles | Missed the target and introduced topology damage |
| Complete GPU QEM | 19.486 s, excluding 11.706 s connectivity construction | Slower than Fast QEM with worse RMS and P95 |
| Native RXMesh QSlim | Conversion took 23.21 s; no result within 150 s | Did not support replacing the roughly 10-second baseline |
| Exterior visibility cleanup | 11.95 to 14.05 s with QEM | Conservative modes removed nothing; stronger filtering removed legitimate disconnected surfaces |
| Fixed-scale trajectory + Fast QEM | 12.526 s, 1.1208 mm RMS, 2.1526 mm P95 | Useful predecessor, but depended on free tuning knobs rather than physical geometry |
| Probe scalar + VTK QEM | 61.096 s, 1.2591 mm RMS, 2.4558 mm P95 | Preserved scalar values instead of enforcing a local triangle quota |
| Probe partitions, weld, global QEM | 26.536 s, 1.7353 mm RMS, 3.4573 mm P95 | Pinned interfaces blocked reduction and damaged global ordering |
| Independent tiled reduction | Interfaces stalled or cracked | Cubes are scheduling units, not independent surfaces |

These failures explain which shortcuts do not preserve the result. They are not the source of the
successful adaptive-probe model.

## Provenance and reproduction

Published and public references used for baselines and rejected implementations:

- [Garland and Heckbert, Surface Simplification Using Quadric Error Metrics](https://publications.ri.cmu.edu/surface-simplification-using-quadric-error-metrics)
- [DeCoro and Lindstrom, Real-time Mesh Simplification Using the GPU](https://gfx.cs.princeton.edu/gfx/pubs/DeCoro_2007_RMS/real_time_simplification.pdf)
- [Topology-preserving parallel mesh simplification study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8341488/)
- [RXMesh](https://github.com/owensgroup/RXMesh)
- [Trellis](https://github.com/pwilkin/trellis.cpp)
- [Fast Quadric Mesh Simplification](https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification)
- [VTK](https://github.com/Kitware/VTK)

Reproduction material:

- [`gpu_adaptive_probe_qem.py`](../benchmarks/gpu_adaptive_probe_qem.py)
- [`benchmark_production_and_candidate.py`](../benchmarks/benchmark_production_and_candidate.py)
- [`CURRENT_BEST_COMPARISON.md`](../benchmarks/CURRENT_BEST_COMPARISON.md)
- [`ALGORITHM_COMPARISON.md`](../benchmarks/ALGORITHM_COMPARISON.md)
- [`GPU_GEOMETRY_PROTOTYPE_RESULTS.md`](../benchmarks/GPU_GEOMETRY_PROTOTYPE_RESULTS.md)
- [`ALGORITHM_TESTING.md`](ALGORITHM_TESTING.md)

Raw reports remain local because they contain machine-specific paths and environment information.
The repository retains benchmark programs, formulas, summarized measurements, matched-angle images,
fixture checksums, and the acceptance procedure needed to repeat the work.
