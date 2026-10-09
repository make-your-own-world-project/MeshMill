# Changelog

All notable release changes are documented here.

## 0.2.0 - Unreleased

- Ships with the English interface and English documentation. Updated translations were deferred
  because translation, structural validation, and human review exceeded the resources and processing
  capacity available for this release. Incomplete catalogs are excluded from the packaged application.

- Middle-drag orbit now uses the visible mesh beneath the pointer as its rotation center.
- Plain left-drag now pans the viewport while selection and measurement modifiers retain their existing actions.
- Mouse panning now tracks screen-space movement at the geometry depth beneath the pointer, keeping movement responsive at close zoom levels.
- Added Depth Adaptive QEM (GPU / Higher Quality) as an automatically detected reduction option.
- Kept Fast QEM as the default with no GPU initialization requirement.
- Bundled the minimal NVIDIA CUDA computation runtime used by Depth Adaptive QEM in the Windows
  installer and portable package. No separate download or system-wide CUDA installation is needed.
- Added GPU-adaptive physical-probe analysis followed by boundary-preserving Fast QEM.
- Added automatic Fast QEM fallback when the CUDA analysis backend is unavailable.
- Added a GPU preference that selects a specific CUDA adapter by PCI address for Depth Adaptive QEM.
- Added the self-contained CUDA runtime compiler required by the Windows package.
- Promoted the adaptive-probe research implementation, tests, benchmarks, and documentation into
  the production application.
- Added a compact color-coded quality row for sampled RMS and P95 error, surface-area change, and
  non-manifold topology. Reduction and dimension drift remain in the main statistics list.
- Added printable solid synthesis based on Depth Adaptive QEM to the roadmap.
- Added Depth and Density Adaptive QEM to the roadmap as a benchmark-gated hybrid experiment.

- Added parallel, memory-aware analysis and bounded overview loading for large binary STL files.
- Added automatic worker and memory budgets with plain-language performance settings.
- Added CPU, RAM, GPU, VRAM, geometry activity, and cumulative I/O metrics.
- Added manual and optional startup update checks. Startup checks are off by default and do not install a service or scheduled task.
- Added verified installer upgrades that reopen the active STL after installation.
- Improved maximized-window layout, viewport controls, ruler contrast, and alternate zoom shortcuts.
- Added algorithm documentation, matched-view comparisons, and reproducible research benchmarks.
- Refreshed the application screenshots and project links for the Make Your Own World organization.
- Documented tested GPU reduction prototypes and retained native CPU reduction where it produced the best measured result.

## 0.1.0

- Connected the application GitHub button to the MeshMill repository.
- Added GitHub and Buy Me a Coffee links to the About dialog.
- Added local STL loading, inspection, selection, cropping, deletion, optimization, and export.
- Added Fast QEM, density-balanced, shape-preserving, and topology-preserving optimization.
- Added shaded, density, wireframe, and vertex display modes.
- Added cancelable background operations, cached comparisons, undo, and redo.
- Added standard-view calibration with paired opposite views and configurable shortcuts.
- Added large-mesh memory preflight and bounded overview loading.
- Added Windows performance metrics, portable packaging, installer packaging, and CLI operation.
- Added localization catalogs and contributor tooling for future translations.
