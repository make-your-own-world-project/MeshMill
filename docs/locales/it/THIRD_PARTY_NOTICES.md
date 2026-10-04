# Software di terze parti

MeshMill dipende dal seguente software. Questi componenti mantengono le proprie licenze e
avvisi sul diritto d'autore.

| Componente | Versione | Licenza |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python Licenza Software Foundation |
| [NumPy](https://numpy.org/) | 2.5.3 | Clausola BSD-3 e licenze permissive in bundle |
| [semplificazione rapida](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Clausola BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Solo LGPL-3.0, solo GPL-2.0 o solo GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Solo LGPL-3.0, solo GPL-2.0 o solo GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0-o successiva con eccezione del bootloader |

Il bundle Windows distribuisce PySide6 e Shiboken6 sotto la loro opzione GPL-3.0, coerente
con la licenza GPL-3.0 o successiva di MeshMill. Le ruote NumPy contengono ulteriori licenze permissive
componenti; i relativi avvisi sono inclusi nei metadati del pacchetto installato e devono essere conservati
quando si ridistribuisce un pacchetto binario modificato.
