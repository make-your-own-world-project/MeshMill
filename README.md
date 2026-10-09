<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

<!-- localization-navigation:start -->
> **0.2.0 localization status:** The current application and documentation release is English-only.
> Updated translations were deferred because translation, structural validation, and review exceeded
> the resources and processing capacity available for this release. The links below lead to older
> community translation work and may not describe current features.

<p align="center">
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/README.md">English</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ar/README.md">العربية</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/bn/README.md">বাংলা</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/de/README.md">Deutsch</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/el/README.md">Ελληνικά</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/es/README.md">Español</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/fa/README.md">فارسی</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/fr/README.md">Français</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ga/README.md">Gaeilge</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/hi/README.md">हिन्दी</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/hu/README.md">Magyar</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/id/README.md">Bahasa Indonesia</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/it/README.md">Italiano</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ja/README.md">日本語</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ko/README.md">한국어</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/nl/README.md">Nederlands</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/pl/README.md">Polski</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/pt/README.md">Português</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ro/README.md">Română</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ru/README.md">Русский</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/sr/README.md">Српски</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/th/README.md">ไทย</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/tr/README.md">Türkçe</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/uk/README.md">Українська</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/ur/README.md">اردو</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/vi/README.md">Tiếng Việt</a> ·
  <a href="https://github.com/make-your-own-world/MeshMill/blob/main/docs/locales/zh-CN/README.md">简体中文</a>
</p>
<!-- localization-navigation:end -->

MeshMill is a focused desktop application for making oversized, dense, or difficult mesh geometry
manageable. It provides fast inspection, density analysis, regional selection, cropping, deletion,
and controlled mesh reduction without requiring an account or uploading geometry.

GPU-accelerated OpenGL rendering keeps viewport navigation, hardware picking, density visualization,
and interactive inspection responsive. That graphics support is included in the normal MeshMill
package. **Depth Adaptive QEM (GPU / Higher Quality)** asks the GPU to perform a different kind of
work: CUDA surface measurement before boundary-preserving Fast QEM. The Windows packages include the
minimal NVIDIA CUDA computation runtime inside MeshMill, without installing a system-wide toolkit or
background service. The first Depth Adaptive QEM run prepares and caches GPU kernels for that machine;
later meshes reuse the cache. Geometry work runs outside the interface so long operations do not block
navigation or controls.

MeshMill works with meshes from 3D scanners, CAD and modeling exports, reconstruction pipelines,
generated geometry, and other STL sources. It prepares geometry for downstream editors,
manufacturing tools, and other mesh workflows. General-purpose modeling, sculpting, animation,
materials, and scene creation are outside its scope.

## Download

Choose your operating system. Every package is self-contained. Python, Node.js, and other
development dependencies are not required.

| System | Recommended download | Status |
| --- | --- | --- |
| **Windows x64** | **[Download the Windows installer](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0/MeshMill-0.2.0-windows-x64-setup.exe)** | Supported release |
| Windows x64, no installation | [Download the portable ZIP](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0/MeshMill-0.2.0-windows-x64-portable.zip) | Supported release |
| Linux x86-64 | [Download the Linux preview](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz) | Early testing preview |
| macOS Apple silicon | [Download the Apple silicon preview](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip) | Early testing preview |
| macOS Intel | [Download the Intel Mac preview](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip) | Early testing preview |

**Most Windows users should choose the Windows installer.** Use the portable ZIP only when you do
not want MeshMill installed or do not have permission to install applications. The normal package
includes GPU-accelerated viewing, every built-in CPU reduction algorithm, and the minimal CUDA
runtime used by Depth Adaptive QEM. That algorithm activates when MeshMill detects a compatible
NVIDIA GPU and driver. It requires no separate download or system-wide CUDA installation.
CUDA Runtime, NVRTC, and CuPy remain separately licensed components. See the
[third-party notices](THIRD_PARTY_NOTICES.md) and the
[CUDA interoperability exception](CUDA_EXCEPTION.md).

Linux and macOS packages are unsigned early previews. They pass automated native builds and
packaged smoke tests, but still need real-hardware testing. Read the
[Linux and macOS preview notes](docs/PLATFORM_TESTING.md) before installing them.

Windows SmartScreen or macOS Gatekeeper may warn about unsigned packages.
An optional [sample STL](https://github.com/make-your-own-world/MeshMill/releases/download/v0.2.0/MeshMill-sample-scan-original.stl)
is included with the supported Windows release. Older versions and download checksums are available
on [GitHub Releases](https://github.com/make-your-own-world/MeshMill/releases).

## Quick start

1. Open an STL.
2. Inspect it in Shaded, Density, Wireframe, or Vertices display mode.
3. Choose a quality level, algorithm, and target triangle count.
4. Select **Optimize** to calculate a result.
5. Compare the original and optimized meshes, then select **Apply** to commit the pass.
6. Select **Save current state** or press `Ctrl+S`.

MeshMill never starts optimization merely because a file or setting changed.

## Capabilities

- Binary and ASCII STL input, binary STL output
- Fast QEM plus optional Depth Adaptive QEM (GPU / Higher Quality), density-balanced,
  shape-preserving, and topology-preserving reduction
- A color-coded quality row comparing reduction, sampled error, dimensional drift, area change,
  and non-manifold topology after optimization
- GPU-adaptive physical probes that remove supported scan-scale variation before QEM reduction
- Per-application CUDA GPU selection for Depth Adaptive QEM on multi-GPU systems
- GPU-accelerated OpenGL viewport, hardware picking, and density visualization
- Native background geometry workers for mesh reduction
- Shaded, density, wireframe, and vertex display modes
- Automatic targets derived from geometry rather than a fixed triangle ceiling
- Polygon selection with additive multi-region selection
- Crop, delete, or optimize only the selected region
- Cached original, previous, and current mesh comparison
- Undo and redo for committed geometry changes
- Dimension drift, reduction percentage, and estimated output size
- Millimeter, centimeter, meter, inch, and foot display units
- CPU, memory, GPU, and geometry-activity metrics
- Bounded overview loading when a binary STL exceeds the configured memory budget
- GUI and command-line applications
- Local processing with no account, telemetry, upload, or cloud dependency

The Performance settings list CUDA adapters by model, PCI address, and memory capacity. Selecting an
adapter directs Depth Adaptive QEM analysis to that device for whole-mesh and selection-only work.
System default uses CUDA device 0. The OpenGL viewport continues to use the graphics adapter chosen
by the operating system.

## Inspect geometry before reducing it

The Shaded display provides a clean view of the surface and silhouette. It is useful for comparing
shape preservation before applying an optimization pass.

![MeshMill shaded viewport showing the bundled sample mesh](docs/images/meshmill-shaded.png)

The Vertices display exposes the actual point distribution. Dense scan regions, sparse areas, and
abrupt changes in sampling are visible without changing the geometry. The expanded metrics panel
tracks CPU, memory, GPU, and geometry-processing activity while working with the mesh.

![MeshMill Vertices display with expanded performance metrics](docs/images/meshmill-vertices.png)

The Wireframe display shows triangle structure directly. It helps identify unnecessary density,
irregular triangulation, and regions where simplification can remove substantial geometry.

![MeshMill Wireframe display showing variation in triangle density](docs/images/meshmill-wireframe.png)

## Analyze mesh density

The Density display maps relative local density across the model. Sparse regions remain cool while
increasingly dense regions move through brighter colors, making uneven sampling visible at a glance.

![MeshMill density display showing relative mesh density](docs/images/meshmill-density.png)

Density remains available while evaluating a provisional optimization. The toolbox reports the
algorithm, target, resulting triangle and vertex counts, reduction percentage, dimensions, and
estimated output size before the pass is applied.

![MeshMill Density display showing a provisional optimization](docs/images/meshmill-density-overview.png)

Hold the right mouse button to inspect a region through the circular magnifier. The magnified view
stays centered on the pointer and reveals local density without changing the main camera position.

![MeshMill Density display with the viewport magnifier](docs/images/meshmill-density-zoom.png)

## View controls

| Input | Action |
| --- | --- |
| Left-drag | Pan |
| Middle-drag | Orbit around the visible mesh beneath the pointer |
| Shift + middle-drag | Pan |
| Mouse wheel | Zoom toward the pointer |
| Ctrl + mouse wheel | Roll clockwise or counterclockwise |
| Arrow keys | Orbit around the view center |
| Ctrl + arrow keys | Pan |
| Ctrl + Shift + Up/Down | Zoom |
| Ctrl + Shift + Left/Right | Roll |
| `F1` / `F2` / `F3` / `F4` | Shaded / Density / Wireframe / Vertices |
| Right mouse hold | Magnifier |
| Shift + left-click | Add or remove ruler points |
| Ctrl + left-drag | Draw a selection polygon |
| `Ctrl+C` | Add the polygon to the saved selection |
| `Ctrl+X` | Crop to the selection |
| `Ctrl+Space` | Optimize the selection |
| `Delete` | Delete the selection |
| `Escape` | Clear the active selection or ruler |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo |
| `Ctrl+S` | Save the current mesh state |

Standard view keys follow the six-key navigation block:

| Key | View | Ctrl + key |
| --- | --- | --- |
| `Insert` | Left | Set current orientation as Left |
| `Home` | Front | Set current orientation as Front |
| `Page Up` | Right | Set current orientation as Right |
| `Delete` | Top when no selection exists | Set current orientation as Top |
| `End` | Back | Set current orientation as Back |
| `Page Down` | Bottom | Set current orientation as Bottom |

Saving a view also updates its opposite view. Left and Right, Front and Back, and Top and Bottom
remain paired. In the confirmation dialog, **Save** is the default action, so Enter saves the
orientation. Front appears at the top of both Top and Bottom views.

Shortcuts can be changed or reset in Settings.

## Selection workflow

Hold Ctrl and left-drag to draw a polygon. Drag corners to reshape it, left-click an edge to add a
point, or right-click an edge to remove one. Add more regions with `Ctrl+C`. Moving the camera hides
the screen-space polygon while retaining the selected geometry.

Optimization with an active selection affects that selection only. The result remains provisional
until **Apply** is selected. **Cancel** discards the provisional result and retains the selection so
another configuration can be tried. Crop and delete operations become normal undoable mesh edits.

The selection panel reports the cumulative selected vertices, triangles, mesh share, estimated
size, and dimensions. Its actions crop, add, optimize, delete, step back, or clear the retained
selection without hiding the surrounding geometry.

![MeshMill showing a retained regional selection and its geometry statistics](docs/images/meshmill-crop-selection.png)

## Large meshes

Before allocating a binary STL, MeshMill compares its estimated working memory with the configured
memory budget. A file above the budget opens as a bounded, read-only overview. The overview reports
the full source triangle count but disables editing and export because it is a sample, not the full
object. Indexed, zoom-dependent out-of-core processing is planned in
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Updates

Update checks are off by default. Click the version beside **General** to check manually, or enable
one check when MeshMill opens in Settings. Supported installer builds can download a newer release,
verify its GitHub SHA-256 digest, replace the installed version, and reopen the active STL. Portable
archives are not modified in place. Platform packaging status and the updater contract are documented
in [docs/UPDATES.md](docs/UPDATES.md).

## Command line

`MeshMillCLI.exe` is included in both release packages:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm depth-adaptive --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Run `.\MeshMillCLI.exe --help` for all options. MeshMill refuses to overwrite its input file.

## Sample geometry

Two versions of the development sample are available. The sample is a composite mesh with
intentional layers of redundant geometry and varied density. It gives people without a scanner a
realistic fixture for comparing algorithms, inspecting density, exercising regional operations,
and developing roadmap features. MeshMill does not require scanned input.

| File | Triangles | Size | Delivery | Best for |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](samples/sample-scan.stl) | 249,999 | 11.9 MiB | Normal Git | Quick evaluation, CI, and learning the controls |
| [`original-scan.stl`](samples/original-scan.stl) | 4,126,315 | 196.8 MiB | Git LFS | Testing dense source geometry and large-mesh performance |

The smaller sample is downloaded with every normal clone. The untouched original is optional and
managed through Git LFS so it does not inflate ordinary repository history. GitHub Desktop includes
Git LFS. Command-line users can install Git LFS and run:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Tagged releases also publish the original STL as a direct download for people who do not use Git.
See [`samples/README.md`](samples/README.md) for provenance, dimensions, and checksums.

Algorithm contributors should also read the
[algorithm testing guide](docs/ALGORITHM_TESTING.md) before comparing or changing reduction
behavior.

The [algorithm reference](docs/ALGORITHMS.md) documents the production formulas, implementation
sources, MeshMill-specific decisions, and density-display analysis. The
[GPU QEM and depth-analysis note](docs/GPU_QEM_AND_DEPTH_ANALYSIS.md) explains why ray, depth, and
surface-measurement workloads benefit from GPU parallelism while ordered QEM topology mutation did
not, including the measured prototype results. The
[full algorithm comparison](benchmarks/ALGORITHM_COMPARISON.md) records CPU, GPU, quality, topology,
and runtime results for released algorithms and completed prototypes.

The [Depth Adaptive QEM design](docs/DEPTH_GAUGE_REDUCTION.md) records the project-originated
physical-probe model, its complete mathematics, the GPU execution profile, and why the other GPU
approaches tested during development were rejected. The published paper,
[Depth Adaptive QEM: GPU-Guided Surface Measurement for Practical Mesh Reduction](https://github.com/make-your-own-world/rnd/blob/main/depth-adaptive-qem/depth-adaptive-qem-v1.1.pdf),
provides the consolidated derivation, measurements, comparisons, and research context. The
[production reducer comparison](benchmarks/CURRENT_BEST_COMPARISON.md) provides matched resident
timings, numerical quality metrics, and six identical camera views for all production reducers.

## STL units

STL does not encode a unit. Changing Model units changes labels and measurements without scaling
the saved coordinates. Select the unit that describes the source geometry.

## Privacy

MeshMill reads and writes local files. It contains no account, telemetry, upload, advertising, or
cloud-processing feature. The current GPU metrics implementation uses local Windows performance
counters. Equivalent native metrics providers are planned for Linux and macOS.

For diagnostic troubleshooting, developers can start the GUI with
`--diagnostic-log <local-file.jsonl>`. The log records input routing and camera state locally and is
disabled during normal use.

## Development and release

Localized UI text and documentation are initially produced with external machine-translation
services and checked automatically for structural damage. Machine translation can still be
unnatural or incorrect. Native speakers are encouraged to review and correct translations through
the contribution process.

- [Contributing](CONTRIBUTING.md)
- [Release process](RELEASING.md)
- [Roadmap](ROADMAP.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Support MeshMill

MeshMill is independently developed and maintained. Read
[why supporting this work matters](SUPPORT.md), or support continued development through
[Buy Me a Coffee](https://buymeacoffee.com/tednv).

MeshMill is licensed under the GNU General Public License, version 3 or later. See
[`LICENSE`](LICENSE).
