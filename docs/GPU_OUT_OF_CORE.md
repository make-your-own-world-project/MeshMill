# GPU and out-of-core design record

This document records measurements and design constraints for the first out-of-core implementation.
It is a development record, not a claim that every listed GPU stage is available in the release.

## Release baseline

The `v0.1.2` release is the comparison baseline for these measurements.

## Reference input and environment

The benchmark used the development reference scan with 4,126,315 triangles and a 206,315,834-byte
binary STL file. Its measured bounds were approximately 831.659 by 371.834 by 479.154 model units.
Paths, user information, timestamps, and machine identifiers are intentionally omitted.

Windows exposed one CUDA device to the benchmark process: the active system-default RTX 3060 with
12 GB of VRAM. Three other installed adapters were not visible to CUDA in the process and were not
selected or used.

The representative kernel calculated triangle areas, centroids, and spatial-bin assignments. It
models independent analysis and work-unit planning, not a complete QEM edge-collapse implementation.

| Triangles | Single-thread CPU | GPU including transfer | GPU kernel only |
| ---: | ---: | ---: | ---: |
| 65,536 | about 0.75 ms | 1.5 to 2.2 ms | 0.18 to 0.71 ms |
| 262,144 | 3 to 8 ms | about 2.5 ms | about 0.05 ms |
| 1,048,576 | 12 to 23 ms | 9 to 10 ms | about 0.20 ms |
| 4,126,315 | 46 to 55 ms | 32 to 34 ms | about 0.73 ms |

Cold source reading took about 3.0 seconds. A Windows-cached read took about 0.30 seconds. The tested
math was therefore cheaper than storage access even after caching. GPU dispatch was counterproductive
at 65K triangles, began to help around 262K, and became compelling only when data was already resident
or the calculation performed substantially more work per triangle.

These figures are observations from one machine and input. They are not fixed product thresholds.

## Index implementation measurements

The first uniform 3 by 3 by 3 partition produced a 1,118,739-triangle hot tile despite a nominal
262K target. The scan is too spatially uneven for uniform-count assumptions.

The adaptive octree implementation measured the actual centroid distribution and subdivided only
overflowing leaves. On the same scan it produced:

- 50 occupied tiles across octree levels 1, 2, and 3;
- a median tile size of 65,075 triangles;
- a largest tile of 249,043 triangles;
- exactly 4,126,315 indexed triangles and 206,315,750 bytes of triangle records; and
- a validated index in approximately 14.6 seconds, followed by removal of the test index.

### Parallel analysis measurement

Bounds and adaptive tile counting are read-only, independent block operations. They were measured
before enabling multiprocessing. On the same 4,126,315-triangle scan, using 262,144-triangle
blocks, the analysis results were:

| Analysis workers | Analysis time | Speedup |
| ---: | ---: | ---: |
| 1 | 10.531 s | 1.00x |
| 8 | 1.838 s | 5.73x |

Both runs produced identical bounds, 50 tiles, and 4,126,315 assigned triangles. Complete index
creation, including the deliberately single-owner partition-writing phase, improved from 8.836
seconds to 5.406 seconds (1.63x) with a warm filesystem cache. MeshMill therefore parallelizes
only bounds and adaptive tile counting, selects up to eight workers from available CPU capacity,
and keeps partition publication under one owner. This preserves deterministic output and avoids
competing writes to tile files.

The persistent index duplicates the compact 50-byte binary STL triangle records so arbitrary tiles
can be read independently. Later storage work may compare compression and shared immutable stores,
but it should preserve deterministic addressing and bounded reads.

## Backend decisions

The release uses a measured hybrid pipeline:

1. CPU threads read, validate, schedule, publish, and assemble tiles.
2. The active GPU handles rendering, picking, density visualization, and validated independent
   analysis batches.
3. Reading tile N+1 overlaps compute for tile N and assembly for tile N-1.
4. Small tiles remain on CPU unless adjacent compatible tiles can be batched safely.
5. Topology mutation and cross-tile boundary decisions remain on CPU. Tested GPU voxel, quadric
   clustering, conservative QEM, parallel QEM, RXMesh QSlim, and exterior-filtering prototypes did
   not match the complete CPU result for speed and quality.

Prefer resident-buffer processing. VTK's OpenGL mapper exposes vertex-buffer objects, and CUDA can
map OpenGL buffers. A production implementation needs a native interoperability layer that:

- runs on the render-context thread;
- queries the compute device associated with the current OpenGL context;
- registers each buffer once and unregisters it before destruction or replacement;
- prevents OpenGL access while CUDA has the resource mapped;
- accounts for VTK's packed vertex layout, stride, shift, and scale;
- treats mapper buffer replacement as cache invalidation;
- owns separate index or adjacency data where VTK does not expose stable public buffers; and
- falls back without changing output when interoperability is unavailable.

OpenGL compute shaders remain a cross-vendor option for display analysis. Future reduction work
should proceed only after a native resident implementation beats the measured CPU baseline without
adding topology damage, platform baggage, or a host-coordination bottleneck.

## Multi-mesh expansion

Each source keeps an immutable adaptive index with source identity and fingerprint. A workspace
catalog overlays sources spatially without copying them into one monolithic mesh. When a merge or
synthesis operation needs more detail, it expands only affected leaves. Work units carry source
references, transforms, overlap margins, operation parameters, and expected input hashes.

This supports:

- adding and removing sources without rebuilding unaffected indexes;
- coarse overlap discovery before full-resolution reads;
- different resolution and confidence per source;
- local subdivision around conflicts, gaps, and dense regions;
- independently cancellable and cacheable merge work; and
- reproducible assembly with provenance for every accepted result.

## Validation requirements

Before enabling a GPU stage by default, compare it with the CPU reference across the composite
sample, small regression meshes, open boundaries, disconnected components, degenerate triangles,
extreme coordinate ranges, uneven density, and overlapping sources.

Record:

- wall time including reads, transfers, synchronization, and assembly;
- peak RAM and VRAM;
- triangle and vertex counts;
- bounds and dimension drift;
- boundary mismatch and duplicate counts;
- topology, normal, and watertightness results;
- deterministic hashes for repeated runs; and
- cancellation and device-loss recovery behavior.

GPU execution should be enabled only when end-to-end time or memory use improves materially and
the result satisfies the same quality and topology contract as the CPU path.
