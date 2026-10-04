# Software van derden

MeshMill is afhankelijk van de volgende software. Deze componenten behouden hun eigen licenties en
auteursrechtvermeldingen.

| Onderdeel | Versie | Licentie |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python Software Foundation-licentie |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3-clausule en gebundelde permissieve licenties |
| [snelle vereenvoudiging](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | BSD-3-clausule |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Alleen LGPL-3.0, alleen GPL-2.0 of alleen GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Alleen LGPL-3.0, alleen GPL-2.0 of alleen GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 of hoger met een bootloader-uitzondering |

De Windows-bundel distribueert PySide6 en Shiboken6 onder hun GPL-3.0-optie, consistent
met de GPL-3.0-of-later-licentie van MeshMill. NumPy-wielen bevatten aanvullende licenties
componenten; hun mededelingen zijn opgenomen in de metagegevens van het geïnstalleerde pakket en moeten worden bewaard
bij het herverdelen van een gewijzigde binaire bundel.
