# Perangkat lunak pihak ketiga

MeshMill bergantung pada perangkat lunak berikut. Komponen-komponen ini memiliki lisensinya sendiri dan
pemberitahuan hak cipta.

| Komponen | Versi | Lisensi |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Lisensi Yayasan Perangkat Lunak Python |
| [NumPy](https://numpy.org/) | 2.5.3 | Klausul BSD-3 dan paket lisensi permisif |
| [penyederhanaan cepat](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Klausul BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Khusus LGPL-3.0, Khusus GPL-2.0, atau Khusus GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Khusus LGPL-3.0, Khusus GPL-2.0, atau Khusus GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0-atau-lebih baru dengan pengecualian bootloader |

Bundel Windows mendistribusikan PySide6 dan Shiboken6 di bawah opsi GPL-3.0, konsisten
dengan lisensi GPL-3.0 atau lebih baru MeshMill. Roda NumPy berisi tambahan yang dilisensikan secara permisif
komponen; pemberitahuan mereka disertakan dalam metadata paket yang diinstal dan harus disimpan
saat mendistribusikan ulang bundel biner yang dimodifikasi.
