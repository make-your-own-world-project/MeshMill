# Third-party software

MeshMill depends on the following software. These components retain their own licenses and
copyright notices.

| Component | Version | License |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python Software Foundation License |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3-Clause and bundled permissive licenses |
| [fast-simplification](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | BSD-3-Clause |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | LGPL-3.0-only, GPL-2.0-only, or GPL-3.0-only |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | LGPL-3.0-only, GPL-2.0-only, or GPL-3.0-only |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0-or-later with a bootloader exception |

The Windows bundle distributes PySide6 and Shiboken6 under their GPL-3.0 option, consistent
with MeshMill's GPL-3.0-or-later license. NumPy wheels contain additional permissively licensed
components; their notices are included in the installed package metadata and should be retained
when redistributing a modified binary bundle.
