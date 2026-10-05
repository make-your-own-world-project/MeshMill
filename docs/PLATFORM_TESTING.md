# Linux and macOS preview testing

Linux and macOS packages are preview builds until they have been exercised on real hardware by
multiple users. They run locally and contain the application runtime. Python, Node.js, and a cloud
account are not required.

## Current packages

- [Linux x86-64 preview](https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz): portable `tar.gz`, built on Ubuntu 22.04.
- [macOS Intel preview](https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip): `.app` bundle in a ZIP archive.
- [macOS Apple silicon preview](https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip): native arm64 `.app` bundle in a ZIP archive.

The macOS previews are ad-hoc signed, not Apple-notarized. Gatekeeper may require the user to open
the application from Finder's context menu or explicitly allow it in system settings. Do not
disable system-wide security controls to run MeshMill.

## What to test

1. Download the package for the operating system and processor architecture.
2. Verify it against the matching SHA-256 checksum file.
3. Launch MeshMill and open `samples/sample-scan.stl` from the repository.
4. Exercise Shaded, Density, Wireframe, and Vertices modes.
5. Test orbit, pan, cursor-centered zoom, standard views, selection, crop, measurement, and undo.
6. Run each optimization algorithm, compare the result, apply it, and save the current mesh.
7. Run the packaged command-line entry point against a small STL.
8. Close and reopen the application to verify saved settings.

## Report useful details

Use the **Platform preview test** issue form. Include:

- MeshMill preview version and downloaded filename
- operating system version and desktop environment
- CPU architecture
- GPU model and driver or macOS version
- display server on Linux (`Wayland` or `X11`)
- whether launch, rendering, navigation, optimization, and export worked
- the smallest shareable STL or steps that reproduce a failure

Linux and macOS GPU utilization metrics are not implemented yet. This does not mean the OpenGL
viewport is using software rendering. Include the renderer shown by the operating system or driver
tools when reporting performance.

## Command-line paths

Linux, after extracting the complete archive:

```bash
./MeshMill/MeshMill --cli input.stl --preset balanced --output output.stl
```

macOS, after copying `MeshMill.app` to Applications:

```bash
/Applications/MeshMill.app/Contents/MacOS/MeshMill --cli input.stl --preset balanced --output output.stl
```
