# Logiciel tiers

MeshMill dépend du logiciel suivant. Ces composants conservent leurs propres licences et
mentions de droits d'auteur.

| Composant | Version | Licence |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Licence de base logicielle Python |
| [NumPy](https://numpy.org/) | 2.5.3 | Clause BSD-3 et licences permissives groupées |
| [simplification rapide](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Clause BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | LGPL-3.0 uniquement, GPL-2.0 uniquement ou GPL-3.0 uniquement |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | LGPL-3.0 uniquement, GPL-2.0 uniquement ou GPL-3.0 uniquement |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 ou version ultérieure avec une exception du chargeur de démarrage |

Le bundle Windows distribue PySide6 et Shiboken6 sous leur option GPL-3.0, cohérent
avec la licence GPL-3.0 ou version ultérieure de MeshMill. Les roues NumPy contiennent des licences permissives supplémentaires
composants; leurs avis sont inclus dans les métadonnées du package installé et doivent être conservés
lors de la redistribution d'un bundle binaire modifié.
