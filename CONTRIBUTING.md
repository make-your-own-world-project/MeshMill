# Contributing

Contributions are welcome through issues and pull requests.

## Project scope

MeshMill makes oversized, dense, or difficult mesh files manageable for downstream editing and
production workflows. Contributions should improve geometry inspection, mesh and point density
management, optimization, selection, cropping, cleanup, validation, STL interchange, performance,
or the coordination of those operations.

The project does not include general-purpose modeling, sculpting, painting, animation, rendering,
scene composition, materials, rigging, or other content-creation systems. Proposals that introduce
those features are outside the project scope.

New features should keep the application focused, preserve direct workflows that turn source
geometry into manageable meshes, and avoid turning supporting controls into a general editing
environment.

## Localization

English UI source text is stored in `locales/en-US.json`. Locale metadata is stored in
`locales/manifest.json`. Translated UI catalogs use the same stable keys and the filename
`<locale>.json`. Translated documentation uses the matching root filename under
`docs/locales/<locale>/`.

Translations are initially produced with external machine-translation services and receive
automated structural validation. That process cannot guarantee natural, technically precise, or
contextually correct language. Native speakers are encouraged to review and correct translated UI
text and documentation. Translation corrections should preserve catalog keys, placeholders,
commands, links, measurements, product names, and Markdown structure.

After changing labels, tooltips, dialogs, or other user-visible text, run:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Review source changes and regenerated keys together.

## Geometry and algorithm changes

Use the bundled sample geometry when changing optimization, density analysis, selection, cropping,
large-file handling, or viewport comparison behavior. It intentionally contains redundant layers
and uneven density, so a useful result should improve manageability without hiding distortion,
discarding meaningful boundaries, or silently removing geometry that another algorithm preserves.

Record the input, algorithm, settings, triangle count, dimensions, dimension drift, elapsed time,
and relevant screenshots for comparisons. Test both the smaller normal-Git fixture and, when the
change concerns large or layered geometry, the original Git LFS fixture. Do not tune an algorithm
to this fixture alone. Add small synthetic cases for the specific invariant or regression being
tested.

See [Algorithm testing and contribution](docs/ALGORITHM_TESTING.md) for the comparison checklist.

## Development setup

1. Install 64-bit Python 3.12 on Windows.
2. Create and activate a virtual environment.
3. Install `requirements-dev.txt`.
4. Run `python meshmill.py` for the GUI or `python meshmill.py --help` for CLI usage.
5. Run `python -m py_compile meshmill.py` before submitting a change.

Keep private meshes, generated executables, screenshots containing private information, and local
build directories out of commits. Redistributable test geometry belongs under `samples/` with its
source, license, dimensions, and generation method documented. New source files should use the
SPDX identifier `GPL-3.0-or-later`.

Crop every documentation screenshot to the MeshMill application content. Do not include the
taskbar, unrelated window chrome, notifications, account details, private paths, or background
desktop content.
