# Phần mềm của bên thứ ba

MeshMill phụ thuộc vào phần mềm sau. Các thành phần này giữ lại giấy phép riêng của họ và
thông báo bản quyền.

| Thành phần | Phiên bản | Giấy phép |
| --- | ---: | --- |
| [Python](https://www.python.org/) | 3.12 | Giấy phép nền tảng phần mềm Python |
| [NumPy](https://numpy.org/) | 2.5.3 | BSD-3-Điều khoản và các giấy phép cho phép đi kèm |
| [đơn giản hóa nhanh](https://github.com/pyvista/fast-simplification) | 0.2.0 | MIT |
| [VTK](https://vtk.org/) | 9.7.1 | Điều khoản BSD-3 |
| [PySide6](https://doc.qt.io/qtforpython-6/) | 6.11.2 | Chỉ LGPL-3.0, chỉ GPL-2.0 hoặc chỉ GPL-3.0 |
| [Shiboken6](https://doc.qt.io/qtforpython-6/shiboken6/) | 6.11.2 | Chỉ LGPL-3.0, chỉ GPL-2.0 hoặc chỉ GPL-3.0 |
| [PyInstaller](https://pyinstaller.org/) | 6.22.3 | GPL-2.0 trở lên với ngoại lệ bộ nạp khởi động |

Gói Windows phân phối PySide6 và Shiboken6 theo tùy chọn GPL-3.0 của họ, nhất quán
với giấy phép GPL-3.0 trở lên của MeshMill. Bánh xe NumPy chứa bổ sung được cấp phép cho phép
thành phần; thông báo của họ được bao gồm trong siêu dữ liệu gói đã cài đặt và phải được giữ lại
khi phân phối lại gói nhị phân đã sửa đổi.
