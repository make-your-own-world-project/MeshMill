# Software de terceros

MeshMill depende del siguiente software. Estos componentes conservan sus propias licencias y
avisos de derechos de autor.

| Componente | Versión | Licencia |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Licencia básica de software Python |
| [NumPy](https://numpy.org/) | 2.5.3 | Cláusula BSD-3 y licencias permisivas empaquetadas |
| [simplificación rápida](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Cláusula BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Solo LGPL-3.0, solo GPL-2.0 o solo GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Solo LGPL-3.0, solo GPL-2.0 o solo GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 o posterior con una excepción del gestor de arranque |

El paquete Windows distribuye PySide6 y Shiboken6 bajo su opción GPL-3.0, consistente
con la licencia GPL-3.0 o posterior de MeshMill. Las ruedas NumPy contienen licencias permisivas adicionales
componentes; sus avisos están incluidos en los metadatos del paquete instalado y deben conservarse
al redistribuir un paquete binario modificado.
