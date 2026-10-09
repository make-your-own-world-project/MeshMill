# Why GPU depth analysis is fast and GPU QEM is difficult

Mesh processing contains workloads with different dependency structures. A GPU can measure a
surface quickly without being an efficient place to mutate that surface's indexed topology. The
distinction matters more than whether the geometry is already resident in VRAM.

## Depth and ray analysis

A depth query casts a ray from origin $\mathbf o_q$ in direction $\mathbf d_q$:

$$
\mathbf r_q(t)=\mathbf o_q+t\mathbf d_q,\qquad t\ge0.
$$

`q` identifies one ray or image sample, `o_q` is its origin, `d_q` is its direction, and `t` is
distance along the ray.

For image location $(u,v)$, the visible depth is the nearest valid intersection:

$$
z_q(u,v)=\min\{t\ge0:\mathbf r_q(t)\cap M\ne\varnothing\}.
$$

`M` is the source mesh and `z_q(u,v)` is one scalar depth result. The corresponding surface sample
is $\mathbf x_q=\mathbf o_q+z_q\mathbf d_q$.

This work maps well to GPU hardware:

- rays, pixels, triangles, and probe cells can be evaluated in parallel;
- the input acceleration structure is read repeatedly but is not changed by each query;
- neighboring rays usually follow similar branches and access nearby memory;
- each query produces a fixed-size result such as a depth, normal, mask, or residual;
- reductions such as nearest depth, weighted sums, histograms, and segmented statistics are regular;
- traversal setup is amortized across many rays.

The same pattern applies when MeshMill calculates triangle normals, centers, spatial keys,
area-weighted tangent planes, normal coherence, residuals, masks, and bounded projection proposals.
These are independent or segmented-array operations. On the retained full-scan benchmark, the
multiscale surface-field calculation took 0.581 seconds on the GPU and 5.819 seconds on the CPU,
about a 10-times speedup for that stage.

Depth analysis is inexpensive surface measurement, not automatic mesh reconstruction. A nearest-hit
depth map does not distinguish every valid internal layer, back-facing sheet, cavity, open boundary,
or disconnected component. Multi-view depth can improve coverage, but combining views still needs
rules for visibility, layer identity, correspondence, and topology. MeshMill uses depth-like evidence
conservatively: supported measurements can influence bounded surface correction, while unresolved
geometry remains unchanged.

## QEM topology mutation

Quadric error metrics assign a geometric cost to collapsing edge $(i,j)$ into replacement vertex
$\bar{\mathbf v}$:

$$
Q_{ij}=Q_i+Q_j,
\qquad
\epsilon_{ij}(\bar{\mathbf v})=\bar{\mathbf v}^{T}Q_{ij}\bar{\mathbf v}.
$$

Calculating many candidate costs is parallel. Committing candidates changes vertex-to-face and
edge-to-face adjacency, active geometry, boundary and manifold classification, local quadrics,
neighboring costs, triangle orientation, collapse validity, and the priority order for later work.

Two proposed collapses can run together only when their affected neighborhoods do not overlap:

$$
C(e_a)\cap C(e_b)=\varnothing.
$$

`C(e)` contains every topology record touched by collapse `e`. The conflict graph changes after each
accepted batch. Previously calculated costs and safe sets can become stale immediately.

This produces a poor GPU execution profile:

- adjacency lists have variable length and scattered memory access;
- legal-collapse tests take different branches for different neighborhoods;
- concurrent mutations require atomics, barriers, conflict coloring, or conservative batches;
- a global or approximate priority structure must be rebuilt as costs change;
- conservative batches preserve validity but expose too little parallel work and may stall;
- relaxed batches improve throughput by accepting stale or conflicting decisions, which can damage
  topology, surface shape, or collapse order.

Keeping vertices and faces in VRAM removes transfer overhead. It does not remove graph dependencies,
conflict discovery, synchronization, or mutable-adjacency updates. Raw arithmetic throughput is not
the limiting resource in this stage.

## What the prototypes measured

The retained benchmark used a 4,126,315-triangle scan and a target near 250,000 triangles.

| Path | Time | Output | Result |
| --- | ---: | ---: | --- |
| GPU surface-field analysis | 0.581 s | Analysis only | About 10x faster than the 5.819 s CPU analysis |
| CPU Fast QEM | 9.827 s resident | 249,999 | Reached target with the strongest simple baseline |
| Conservative GPU QEM | 66.936 s | 722,687 | Preserved safety but stalled above target |
| Parallel GPU QEM | 25.282 s | 706,682 | Stalled and introduced topology damage |
| Complete GPU QEM | 19.486 s | 249,999 | Reached target with substantially worse sampled error |
| Depth Adaptive QEM | 10.156 s resident | 249,999 | GPU measurement plus CPU Fast QEM, improved RMS and P95 |

The complete GPU QEM time excludes 11.706 seconds of mutable-connectivity construction. Even with
that favorable timing boundary, it was slower than CPU Fast QEM and produced higher surface error.
RXMesh QSlim was tested from public source. Input conversion took 23.21 seconds, and reduction did
not finish within 150 seconds on this fixture.

Depth Adaptive QEM uses the two processors for the work each handled well in testing:

1. The GPU performs dense, regular, read-mostly surface measurement and derives bounded correction
   proposals.
2. The original indexed mesh remains assembled as one global object.
3. Native Fast QEM performs ordered topology mutation with established boundary and validity checks.

This division increased resident time from 9.827 seconds for Fast QEM to 10.156 seconds while
improving sampled RMS from 1.1721 mm to 1.0668 mm and P95 from 2.3504 mm to 2.0586 mm on the retained
fixture. It is a measured architecture choice, not a claim that GPUs are poor at geometry in
general.

## Design implications

- Use GPU depth, ray, projection, normal, density, and probe analysis when the output can be expressed
  as independent or segmented fixed-size records.
- Keep complete surface evidence. Visibility filtering that deletes geometry can remove valid
  occluded layers from open or composite scans.
- Treat depth fusion that fills intervals as a separate solid-synthesis objective. It is useful for
  future printable-solid work but is destructive when the goal is faithful reduction.
- Benchmark topology mutation as a complete reducer. A fast candidate-cost kernel does not establish
  a fast or accurate end-to-end QEM implementation.
- Count connectivity construction, conflict processing, synchronization, target completion, surface
  error, boundary changes, and non-manifold changes when comparing CPU and GPU paths.
- Retain Fast QEM as the default. Offer Depth Adaptive QEM where the GPU analysis backend is
  available and its initialization cost is acceptable.

## Related project records

- [Algorithm reference](ALGORITHMS.md)
- [Depth-gauge reduction derivation](DEPTH_GAUGE_REDUCTION.md)
- [Full algorithm comparison](../benchmarks/ALGORITHM_COMPARISON.md)
- [GPU prototype results](../benchmarks/GPU_GEOMETRY_PROTOTYPE_RESULTS.md)
- [Current production comparison](../benchmarks/CURRENT_BEST_COMPARISON.md)
