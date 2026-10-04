# Out-of-core mesh architecture

MeshMill's current large-file safeguard estimates working memory before allocating a complete
mesh. Files that exceed the configured budget can open as bounded navigation overviews. An
overview is sampled geometry, is visibly identified as such, and cannot be edited or exported as
though it were the complete source.

True zoom-dependent detail requires a persistent spatial index. The design below defines that
next implementation phase.

## Index format

Each source mesh receives a versioned `.meshmill-index` directory containing:

- `manifest.json`, with the source size, modification time, sampled content hashes, bounds,
  triangle count, index version, coordinate precision, and level descriptions;
- spatial tiles addressed by octree level and Morton code;
- a coarse display mesh for every occupied parent tile;
- full-resolution triangle records in leaf tiles; and
- boundary ownership and overlap metadata used during regional operations and assembly.

Index creation reads the source sequentially in bounded blocks. It writes temporary tile runs and
atomically publishes the manifest after every required file passes validation. An interrupted or
stale index is detected from its manifest and can be resumed or rebuilt without opening the full
mesh in memory.

## Viewport streaming

The viewport selects tiles using the camera frustum and screen-space error. Coarse parent tiles are
shown first. Visible child tiles replace them as the camera moves closer, while off-screen and
low-impact tiles remain coarse. RAM and VRAM have independent budgets and least-recently-used
caches. Releasing detail never releases the coarse whole-object representation.

The scheduler records these tile states: queued, reading, processing, uploading, resident, failed,
and cancelled. The viewport can color cubes by state and fill each cube in proportion to its
progress. Cancellation removes partial results and leaves the last complete representation active.

## Processing and capacity

A local work unit is a tile plus the deterministic overlap required by its operation. Concurrency
is capped by currently available RAM, configured memory percentage, logical processor count, and
measured work-unit size. GPU upload and display have a separate VRAM budget. Reported parallel
capacity is an estimate until representative tiles have been measured.

Operations retain one owner for every boundary element. Assembly validates shared boundaries,
removes duplicates, checks counts and bounds, and records the exact parameters used. The same work
unit and result format can later be scheduled across distributed synthesis nodes.

## Safety rules

- A global sample is labeled as an overview, not full-resolution viewport detail.
- An overview cannot overwrite or export as the complete source mesh.
- Full-load requests that exceed the current budget require an explicit choice.
- Index generation, tile processing, and assembly remain cancellable and preserve the previous
  complete state.
- Capacity values are estimates and identify whether they describe the current engine or planned
  parallel tile execution.
