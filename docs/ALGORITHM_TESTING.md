# Algorithm testing and contribution

MeshMill algorithms should make difficult geometry manageable while keeping their effects visible,
measurable, and reversible before a result is applied.

## Reference fixtures

Use both bundled versions of the composite sample geometry:

- `samples/sample-scan.stl` is the smaller normal-Git fixture for routine development, automated
  checks, and learning the controls.
- `samples/original-scan.stl` is the full Git LFS fixture for large-file behavior, redundant layers,
  uneven density, overlap, and performance work.

The redundant and dense regions are intentional test characteristics. A test may target them, but
should not assume every overlapping surface is disposable. Add compact synthetic meshes when a
change needs a known boundary, curvature, topology, density, or overlap invariant.

## Comparison checklist

For an algorithm or parameter change, record:

- MeshMill version or commit;
- input fixture and checksum;
- algorithm, quality preset, target, and advanced settings;
- original and resulting triangle and vertex counts;
- reduction percentage, dimensions, and dimension drift;
- elapsed time and peak memory when performance is relevant;
- screenshots from the same saved views and display modes;
- visible boundary, hole, self-intersection, overlap, or distortion changes;
- whether the result came from a whole-mesh or selection-only operation.

Compare against the current behavior at the same target, not only against another preset with a
different output count. Inspect shaded, density, wireframe, and vertices displays where applicable.

## Acceptance guidance

An optimization change should avoid unexpected dimension changes, obvious surface inversion,
cracks between processed regions, loss of meaningful boundaries, and large quality regressions at a
similar output count. Density-oriented changes should demonstrate that removed concentration did
not carry useful curvature or topology.

Performance results should identify the processor, memory capacity, graphics hardware, operating
system, input size, and whether the data was already cached. Structural validation and screenshots
support review but do not replace inspection by contributors familiar with the source geometry.

## Regression tests

Prefer deterministic tests with explicit tolerances. Keep new fixtures small enough for normal Git,
document their origin and license, and use synthetic geometry when real source data is unnecessary.
Tests should cover cancellation and state restoration when an operation can modify geometry.
