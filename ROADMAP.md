# MeshMill roadmap

## Reliable application updates

- Add a Developer ID signed and notarized macOS package, then enable verified in-app replacement on macOS.
- Add a supported Linux AppImage and native upgrade/relaunch tests, then enable verified in-app replacement on Linux.
- Preserve complete unsaved editing state across an application upgrade, beyond reopening the source STL.

## Platform support

Windows is the initial packaged platform. The application architecture and mesh formats are
cross-platform, and future releases should add native Linux and macOS packages. Platform work
includes packaging, application integration, hardware metrics, filesystem behavior, and automated
release testing while preserving the same project and STL workflows on every supported system.

- Validate the Linux x86-64 preview package across distributions, desktop environments, display
  servers, and GPU drivers before promoting it to stable.
- Validate the macOS Apple silicon and x86-64 preview packages on real hardware, then add Developer
  ID signing and notarization before promoting them to stable.
- Add platform-native CPU, memory, and GPU metrics providers behind a shared interface.
- Keep saved settings, keyboard mappings, command-line behavior, and project data portable.

This roadmap records planned work. It does not describe features in the current release.

## Scope

MeshMill manages geometry, mesh density, point density, optimization, cleanup, validation, and STL
interchange so large or heavy mesh files remain useful in downstream editing workflows.

General-purpose modeling, sculpting, painting, animation, rendering, scene composition, materials,
rigging, and other content-creation systems are outside this roadmap. Distributed synthesis applies
to MeshMill's mesh-management operations and does not expand the product into a general editor.

## Control profiles

Navigation preferences vary by operator, pointing device, and established workflow. Add named
control profiles so users can change the complete interaction model without remapping each control
individually.

Planned behavior:

- ship clear starting profiles for the MeshMill default, conventional CAD navigation, trackpads,
  and left-handed input without naming or depending on another application;
- map left, middle, right, auxiliary mouse buttons, wheel movement, drag modifiers, keyboard
  commands, and viewport-axis controls independently;
- configure orbit pivots, pan and orbit sensitivity, zoom rate, roll direction, and per-axis input
  inversion within each profile;
- detect conflicting or unreachable bindings before a profile can be applied;
- preview and test a profile temporarily, with an automatic path back to the previous controls;
- create, duplicate, rename, reset, and delete user profiles while keeping the built-in profiles
  recoverable;
- choose a global default and allow an optional profile override for a workspace or input device;
- import and export a versioned, human-readable profile that contains no machine-specific or
  personal data;
- preserve profile compatibility across supported platforms and report unavailable device-specific
  bindings clearly.

## Reference geometry

The bundled composite mesh is the common development fixture for current algorithms and roadmap
work. Its intentionally redundant layers and uneven density support repeatable comparisons of
reduction quality, density analysis, overlap handling, regional operations, out-of-core processing,
and future synthesis. Roadmap implementations should report results against this fixture and small
purpose-built regression meshes, rather than optimizing behavior for one model alone.

## Multi-STL workspaces and statistical synthesis

A workspace should accept multiple STL inputs as separate, independently visible source objects.
MeshMill should align those sources, measure their geometric agreement, and synthesize one usable
mesh without retaining duplicate internal surfaces or repeated overlap geometry.

Planned behavior:

- add, remove, hide, isolate, reorder, and inspect multiple STL sources in one workspace;
- retain source identity, units, transforms, bounds, resolution, and operation history;
- provide automatic registration with manual alignment controls and measurable fit quality;
- partition sources into spatial regions before comparison so large inputs remain bounded;
- analyze occupancy, nearest-surface distance, normal agreement, local density, variance, and
  observation count across overlapping regions;
- classify matching surfaces, conflicting surfaces, scan noise, gaps, and unique geometry;
- consolidate statistically agreeing surfaces into a representative surface with recorded
  confidence instead of stacking duplicate triangles;
- remove enclosed, coincident, and shared geometry that contributes no exterior shape detail;
- retain non-overlapping source geometry and expose ambiguous regions for visual review;
- allow per-source and per-region weighting when one scan is cleaner or more detailed;
- validate watertightness, boundaries, normals, dimensions, and topology after synthesis;
- record source provenance and synthesis parameters so the combined mesh is reproducible;
- preview the expected triangle count, bounds, overlap removed, and confidence distribution before
  committing the synthesized result.

This workflow should use the same out-of-core spatial index and work-unit model planned for large
meshes. Statistical comparison and overlap consolidation should also be distributable across local
or remote MeshMill nodes.

## Depth Adaptive solid synthesis

Create a separate Depth Adaptive QEM workflow that reconstructs a closed, printable solid from an
open or incomplete surface. This mode should use the adaptive physical-probe surface estimate to
bridge scan gaps and fill holes, then assemble a watertight exterior suitable for additive
manufacturing. It remains separate from ordinary Depth Adaptive QEM, which preserves open
boundaries and does not intentionally change topology.

Planned validation and controls:

- preview every filled region and the estimated enclosed volume before applying the result;
- set the smallest hole to fill and the largest gap the surface model may bridge;
- preserve deliberate openings through protected regions or explicit boundary selection;
- remove enclosed duplicate and internal geometry that does not contribute to the exterior solid;
- verify watertightness, manifold edges, consistent normals, self-intersections, and positive volume;
- report dimensional drift and surface deviation against the source mesh;
- export a printable STL only after solid validation passes, with unresolved regions identified for
  review.

## Distributed synthesis

A MeshMill cluster should coordinate multiple nodes operating in parallel across multiple
workstations. A node may inspect, select, reduce, validate, repair, or combine an assigned region or
work unit. Contributions remain independently versioned until they are reviewed and incorporated
into a shared object version.

The system should support:

- concurrent contributions from multiple operators and automated nodes;
- deterministic work-unit inputs, parameters, dependencies, and outputs;
- capability-aware scheduling based on CPU, GPU, memory, algorithms, and current load;
- dependency-aware partitioning of meshes, regions, validation passes, and synthesis stages;
- durable queues with pause, resume, cancellation, retry, reassignment, and failure recovery;
- content-addressed artifacts and integrity checks between nodes;
- reproducible synthesis from a recorded set of accepted contribution versions;
- offline or intermittently connected workstations that can synchronize later;
- local-first operation with explicit control over participating nodes and shared project data.

## Versioned collaboration

Every contribution should record its parent object version, selected region or work unit, operation,
parameters, node identity, timestamps, dependencies, validation results, and output checksum.

Planned collaboration behavior:

- projects contain objects, branches, checkpoints, contributions, and synthesized versions;
- contributors can work from the same parent version without overwriting one another;
- non-overlapping contributions can merge automatically after validation;
- overlapping geometry or incompatible dependencies create an explicit conflict;
- conflicts provide visual comparison, region-level choice, rebase, rerun, and manual resolution;
- review states include pending, accepted, rejected, superseded, conflicted, and incorporated;
- the final synthesis manifest identifies every incorporated contribution and dependency.

## Coordination UI

The desktop application should manage distributed work without requiring a separate command-line
or server-administration workflow. Planned views include:

- **Projects:** objects, branches, versions, contributors, and synthesis status.
- **Cluster:** connected workstations and nodes, capabilities, health, load, and current assignment.
- **Queue:** pending, active, paused, blocked, failed, and completed work units.
- **Contributions:** author, node, parent version, affected region, parameters, checks, and review state.
- **Compare:** synchronized 3D views, geometry differences, metrics, and boundary inspection.
- **Conflicts:** overlapping regions, dependency conflicts, resolution choices, and validation results.
- **Synthesis:** dependency graph, aggregate progress, selected contribution versions, and final output.
- **History:** branch graph, checkpoints, merges, synthesized versions, and reproducibility manifests.

The viewport should show ownership, assigned regions, completed work, pending changes, conflicts,
and version differences without altering the underlying mesh.

## Coordination and transport

The first design phase should define protocol boundaries before selecting a transport. The protocol
should separate coordination metadata from large mesh artifacts, support resumable transfer, and
remain usable on a local network without an external account or hosted service.

Required coordination concepts:

- coordinator election or an explicitly selected coordinator;
- node discovery and manual node enrollment;
- authenticated sessions and project-scoped authorization;
- leases and heartbeats for work ownership;
- idempotent work submission and result acceptance;
- version negotiation between different MeshMill releases;
- structured events for progress, logs, validation, failures, and retries;
- recovery after coordinator, workstation, network, or node interruption.

## Delivery phases

### Phase 0: out-of-core large-mesh processing

The index, streaming, cache, work-unit, and safety contract is documented in
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Estimate triangle count and working memory before allocating the complete mesh.
- Open oversized binary STL files as bounded, evenly sampled navigation overviews.
- Partition full-resolution geometry into spatial cubes with deterministic overlap boundaries.
- Read, analyze, and optimize independent cubes concurrently within CPU and memory limits.
- Continue GPU reduction research only from the measured baseline in
  [`benchmarks/GPU_GEOMETRY_PROTOTYPE_RESULTS.md`](benchmarks/GPU_GEOMETRY_PROTOTYPE_RESULTS.md).
  Depth Adaptive QEM is now a production GPU / Higher Quality option. Current voxel, clustering, topology-safe QEM,
  parallel QEM, RXMesh, and exterior-cleanup paths
  were rejected for speed, completeness, or quality. Integrate a future stage only when it improves
  end-to-end time or memory while matching the CPU result's geometry and topology contract.
- Prototype Depth and Density Adaptive QEM as a hybrid of the existing depth-probe analysis and
  robust local-density statistics. Use density to allocate probe and triangle budgets, then use
  depth agreement, curvature, and surface trajectory to distinguish useful detail from redundant
  scan concentration. Compare it with Fast QEM, Density balanced, and Depth Adaptive QEM at matched
  output counts before considering it for the application.
- Stream coarse-to-fine viewport levels instead of requiring the complete mesh in memory.
- Draw cube state directly in the viewport: queued, reading, processing, completed, and failed.
- Show per-cube progress by filling each cube and retain a high-level whole-object view.
- Assemble processed cubes with boundary validation, duplicate removal, and reproducible settings.
- Extend the local cube scheduler into distributed synthesis work units in later phases.
- Reuse resident viewport buffers through a native graphics-compute interoperability layer when the
  active system-default adapter supports it; retain validated CPU and staged-buffer fallbacks.
- Use adaptive octree leaves so dense, overlapping, or disputed regions can expand independently
  for multi-STL alignment, comparison, merge, and synthesis.

### Phase 1: versioned local foundation

- Define object, operation, contribution, branch, and manifest formats.
- Add multi-STL workspaces with per-source visibility, transforms, metadata, and provenance.
- Add registration quality metrics and spatial overlap classification.
- Synthesize statistically agreeing surfaces while removing duplicate and enclosed geometry.
- Add visual review for conflicts, gaps, confidence, and geometry unique to one source.
- Persist local history across application sessions.
- Add visual mesh and region comparisons.
- Make operations deterministic and independently reproducible.

### Phase 2: coordinated local nodes

- Run worker nodes on one workstation.
- Add queueing, capability reporting, work assignment, and cancellation.
- Display node and work-unit state in the MeshMill UI.
- Validate partitioning and result assembly locally.

### Phase 3: multi-workstation synthesis

- Add authenticated LAN discovery and enrollment.
- Transfer content-addressed work inputs and results with resume support.
- Coordinate concurrent work across multiple workstations.
- Recover assignments after node or network failure.

### Phase 4: collaborative versioning

- Add contributors, branches, review states, and permissions.
- Merge non-overlapping contributions.
- Detect and resolve overlapping or dependency conflicts.
- Synthesize selected contributions into a reproducible object version.

### Phase 5: production hardening

- Add protocol compatibility tests and mixed-version handling.
- Add audit, integrity, corruption, interruption, and recovery tests.
- Benchmark scheduling, partitioning, transfer, merge, and synthesis performance.
- Document deployment, backup, migration, and incident recovery.
