# サードパーティ製ソフトウェア

MeshMillは以下のソフトウェアに依存します。これらのコンポーネントは独自のライセンスを保持し、
著作権表示。

|コンポーネント |バージョン |ライセンス |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Python ソフトウェア ファウンデーション ライセンス |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3 条項とバンドルされた寛容ライセンス |
| [高速簡略化](https://github.com/pyvista/fast-simplification) | 0.2.0 |マサチューセッツ工科大学 |
| [VTK](https://vtk.org/) | 9.7.1 | BSD-3 条項 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | LGPL-3.0 のみ、GPL-2.0 のみ、または GPL-3.0 のみ |
| [しぼけん6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | LGPL-3.0 のみ、GPL-2.0 のみ、または GPL-3.0 のみ |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 以降 (ブートローダー例外あり) |

Windows バンドルは、一貫性のある GPL-3.0 オプションに基づいて PySide6 と Shiboken6 を配布します。
MeshMill の GPL-3.0 以降のライセンスを使用します。 NumPy ホイールには、許可された追加のライセンスが含まれています
コンポーネント。これらの通知はインストールされたパッケージのメタデータに含まれているため、保持する必要があります。
変更されたバイナリバンドルを再配布するとき。
