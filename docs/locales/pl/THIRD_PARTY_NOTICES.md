# Oprogramowanie innych firm

MeshMill zależy od następującego oprogramowania. Komponenty te zachowują własne licencje i
informacje o prawach autorskich.

| Składnik | Wersja | Licencja |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python Licencja Software Foundation |
| [NumPy](https://numpy.org/) | 2.5.3 | Klauzula BSD-3 i dołączone licencje zezwalające |
| [szybkie uproszczenie](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Klauzula BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Tylko LGPL-3.0, tylko GPL-2.0 lub tylko GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Tylko LGPL-3.0, tylko GPL-2.0 lub tylko GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 lub nowsza wersja z wyjątkiem bootloadera |

Pakiet Windows dystrybuuje PySide6 i Shiboken6 w ramach opcji GPL-3.0, spójnie
z licencją MeshMill GPL-3.0 lub nowszą. Koła NumPy zawierają dodatkowe, zezwalające na licencję
komponenty; ich uwagi są zawarte w metadanych zainstalowanego pakietu i należy je zachować
podczas redystrybucji zmodyfikowanego pakietu binarnego.
