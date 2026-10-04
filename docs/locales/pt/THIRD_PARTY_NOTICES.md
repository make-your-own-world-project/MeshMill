# Software de terceiros

MeshMill depende do seguinte software. Esses componentes mantêm suas próprias licenças e
avisos de direitos autorais.

| Componente | Versão | Licença |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Licença Python Software Foundation |
| [NumPy](https://numpy.org/) | 2.5.3 | Cláusula BSD-3 e licenças permissivas agrupadas |
| [simplificação rápida](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Cláusula BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Somente LGPL-3.0, somente GPL-2.0 ou somente GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Somente LGPL-3.0, somente GPL-2.0 ou somente GPL-3.0 |
| [PyInstalador](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 ou posterior com uma exceção de bootloader |

O pacote Windows distribui PySide6 e Shiboken6 sob sua opção GPL-3.0, consistente
com licença GPL-3.0 ou posterior do MeshMill. As rodas NumPy contêm licenças adicionais permissivamente
componentes; seus avisos estão incluídos nos metadados do pacote instalado e devem ser retidos
ao redistribuir um pacote binário modificado.
