# MeshMill

![Cửa sổ hiển thị dạng khối đặc (shaded viewport) của MeshMill](../../images/meshmill-shaded.png)

MeshMill là ứng dụng máy tính chuyên dụng giúp xử lý các mô hình lưới (mesh) có kích thước lớn,
mật độ cao hoặc cấu trúc phức tạp. Ứng dụng hỗ trợ kiểm tra nhanh, phân tích mật độ, chọn vùng, cắt, xóa,
và giảm số lượng lưới có kiểm soát mà không yêu cầu tài khoản hay tải dữ liệu hình học lên máy chủ.

Kết xuất OpenGL tăng tốc bằng GPU giúp thao tác trong khung nhìn, chọn bằng phần cứng, hiển thị mật độ và kiểm tra tương tác luôn phản hồi nhanh. Việc giảm lưới hiện chạy trong các tiến trình CPU gốc riêng biệt, nhờ đó các phép tính hình học kéo dài không chặn giao diện.

MeshMill hoạt động với dữ liệu lưới từ máy quét 3D, tệp xuất từ ​​CAD và phần mềm mô hình hóa, quy trình tái tạo,
dữ liệu hình học được tạo tự động và các nguồn khác. Ứng dụng chuẩn bị dữ liệu cho các công cụ chỉnh sửa, (STL)
công cụ sản xuất và các quy trình xử lý lưới khác. Các tính năng mô hình hóa tổng quát, điêu khắc, hoạt ảnh,
tạo vật liệu và dựng cảnh không nằm trong phạm vi chức năng của ứng dụng.

## Tải xuống

Tải xuống một trong các tệp sau từ mục [Phát hành GitHub](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: trình cài đặt cho từng người dùng, bao gồm mục trong menu Start và tùy chọn
  tạo lối tắt trên màn hình nền.
- `MeshMill-<version>-windows-x64-portable.zip`: ứng dụng dạng portable (chạy trực tiếp không cần cài đặt). Giải nén toàn bộ tệp lưu trữ,
  sau đó chạy `MeshMill.exe`.

Cả hai gói đều đã bao gồm môi trường thực thi (runtime) cần thiết cho ứng dụng. Người dùng cuối không cần cài đặt Python, Node.js hoặc
các thành phần phụ thuộc. Bản phát hành đầu tiên hỗ trợ Windows 10 và Windows 11 trên phần cứng x64. Các gói Linux và
macOS đang được lên kế hoạch; định dạng sản phẩm và tệp tin không bị giới hạn riêng cho Windows.

Các bản dựng cộng đồng chưa được ký số có thể hiển thị cảnh báo SmartScreen của Windows. Các mã kiểm tra (checksum) của bản phát hành được liệt kê
trong `SHA256SUMS.txt` bên cạnh mỗi bản phát hành.

## Hướng dẫn nhanh

1. Mở một STL.
2. Kiểm tra nó ở chế độ hiển thị Shaded (Có bóng), Density (Mật độ), Wireframe (Khung dây) hoặc Vertices (Đỉnh).
3. Chọn mức chất lượng, thuật toán và số lượng tam giác mục tiêu.
4. Chọn **Optimize** (Tối ưu hóa) để tính toán kết quả.
5. So sánh lưới (mesh) gốc và lưới đã tối ưu hóa, sau đó chọn **Apply** (Áp dụng) để xác nhận thao tác.
6. Chọn **Save current state** (Lưu trạng thái hiện tại) hoặc nhấn `Ctrl+S`.

MeshMill không bao giờ tự động bắt đầu tối ưu hóa chỉ vì tệp tin hoặc cài đặt bị thay đổi.

## Các tính năng

- Nhập dữ liệu STL định dạng nhị phân và ASCII, xuất dữ liệu STL định dạng nhị phân
- Giảm thiểu dữ liệu Fast QEM nhưng vẫn cân bằng mật độ, bảo toàn hình dạng và cấu trúc topo
- Các chế độ hiển thị: tô bóng (shaded), mật độ, khung dây (wireframe) và đỉnh (vertex)
- Các mục tiêu tự động dựa trên hình học thay vì giới hạn số lượng tam giác cố định
- Chọn đa giác với tính năng chọn cộng dồn nhiều vùng
- Cắt, xóa hoặc tối ưu hóa chỉ vùng được chọn
- So sánh lưới (mesh) gốc, lưới trước đó và lưới hiện tại (có sử dụng bộ nhớ đệm)
- Hoàn tác (undo) và làm lại (redo) các thay đổi hình học đã áp dụng
- Thông số về độ lệch kích thước, tỷ lệ giảm thiểu và kích thước đầu ra ước tính
- Các đơn vị hiển thị: milimét, centimet, mét, inch và foot
- Các chỉ số về CPU, bộ nhớ, GPU và hoạt động hình học
- Tải chế độ xem tổng quan có giới hạn khi tệp STL nhị phân vượt quá hạn mức bộ nhớ đã cấu hình
- Các ứng dụng có giao diện đồ họa (GUI) và dòng lệnh
- Xử lý cục bộ, không phụ thuộc vào tài khoản, dữ liệu từ xa (telemetry), tải lên hay đám mây

![Hiển thị mật độ MeshMill](../../images/meshmill-density.png)

## Các điều khiển hiển thị

| Đầu vào | Thao tác |
| --- | --- |
| Kéo bằng nút giữa | Xoay góc nhìn (Orbit) |
| Shift + kéo bằng nút giữa | Di chuyển khung nhìn (Pan) |
| Con lăn chuột | Phóng to/thu nhỏ về phía con trỏ |
| Ctrl + con lăn chuột | Cuộn theo chiều kim đồng hồ hoặc ngược chiều kim đồng hồ |
| Các phím mũi tên | Xoay quanh tâm khung nhìn |
| Ctrl + các phím mũi tên | Di chuyển khung nhìn (Pan) |
| Ctrl + Shift + Lên/Xuống | Phóng to/thu nhỏ (Zoom) |
| Ctrl + Shift + Trái/Phải | Cuộn |
| `F1` / `F2` / `F3` / `F4` | Bóng mờ / Mật độ / Khung dây / Đỉnh |
| Giữ chuột phải | Kính lúp |
| Shift + nhấp chuột trái | Thêm hoặc xóa điểm thước |
| Ctrl + kéo trái | Vẽ đa giác lựa chọn |
| `Ctrl+C` | Thêm đa giác vào vùng chọn đã lưu |
| `Ctrl+X` | Cắt theo vùng chọn |
| `Ctrl+Space` | Tối ưu hóa lựa chọn |
| `Delete` | Xóa lựa chọn |
| `Escape` | Xóa vùng chọn hoặc thước đang hoạt động |
| `Ctrl+Z` / `Ctrl+Y` | Hoàn tác / làm lại |
| `Ctrl+S` | Lưu trạng thái lưới hiện tại |

Các phím xem tiêu chuẩn tuân theo khối điều hướng sáu phím:

| Chìa khóa | Xem | Ctrl + phím |
| --- | --- | --- |
| `Insert` | Trái | Đặt hướng hiện tại là Left |
| `Home` | Mặt trận | Đặt hướng hiện tại là Mặt trước |
| `Page Up` | Đúng | Đặt hướng hiện tại là Phải |
| `Delete` | Lên trên khi không có lựa chọn nào | Đặt hướng hiện tại là Top |
| `End` | Quay lại | Đặt hướng hiện tại là Quay lại |
| `Page Down` | Dưới cùng | Đặt hướng hiện tại là Dưới cùng |

Việc lưu một chế độ xem cũng cập nhật chế độ xem đối diện của nó. Trái và Phải, Trước và Sau, Trên và Dưới
vẫn ghép đôi. Trong hộp thoại xác nhận, **Save** là hành động mặc định, do đó Enter sẽ lưu
định hướng. Mặt trước xuất hiện ở trên cùng của cả chế độ xem Trên và Dưới.

Các phím tắt có thể được thay đổi hoặc đặt lại trong Cài đặt.

## Quy trình lựa chọn

Giữ Ctrl và kéo sang trái để vẽ đa giác. Kéo các góc để định hình lại nó, nhấp chuột trái vào một cạnh để thêm
điểm hoặc nhấp chuột phải vào một cạnh để loại bỏ một cạnh. Thêm nhiều vùng hơn với `Ctrl+C`. Di chuyển camera ẩn
đa giác trong không gian màn hình trong khi vẫn giữ lại hình học đã chọn.

Việc tối ưu hóa với lựa chọn đang hoạt động chỉ ảnh hưởng đến lựa chọn đó. Kết quả vẫn tạm thời
cho đến khi **Áp dụng** được chọn. **Hủy** loại bỏ kết quả tạm thời và giữ lại lựa chọn để
cấu hình khác có thể được thử. Các thao tác cắt và xóa trở thành các chỉnh sửa lưới không thể hoàn tác thông thường.

## Mắt lưới lớn

Trước khi phân bổ STL nhị phân, MeshMill so sánh bộ nhớ làm việc ước tính của nó với cấu hình
ngân sách bộ nhớ. Một tệp vượt quá ngân sách sẽ mở ra dưới dạng tổng quan có giới hạn, chỉ đọc. Các báo cáo tổng quan
đếm tam giác nguồn đầy đủ nhưng vô hiệu hóa chỉnh sửa và xuất vì đây là mẫu chứ không phải đầy đủ
đối tượng. Quá trình xử lý ngoài lõi phụ thuộc vào thu phóng, được lập chỉ mục được lên kế hoạch trong
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Dòng lệnh

`MeshMillCLI.exe` được bao gồm trong cả hai gói phát hành:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Chạy `.\MeshMillCLI.exe --help` cho tất cả các tùy chọn. MeshMill từ chối ghi đè tệp đầu vào của nó.

## hình học mẫu

Hai phiên bản của mẫu phát triển có sẵn. Mẫu là một lưới tổng hợp với
các lớp hình học dư thừa có chủ ý và mật độ đa dạng. Nó cung cấp cho những người không có máy quét một
vật cố thực tế để so sánh các thuật toán, kiểm tra mật độ, thực hiện các hoạt động trong khu vực,
và phát triển các tính năng lộ trình. MeshMill không yêu cầu đầu vào được quét.

| Tập tin | Hình tam giác | Kích thước | Giao hàng | Tốt nhất cho |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Git bình thường | Đánh giá nhanh, CI và tìm hiểu các điều khiển |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MIB | Git LFS | Kiểm tra hình học nguồn dày đặc và hiệu suất lưới lớn |

Mẫu nhỏ hơn được tải xuống với mọi bản sao bình thường. Bản gốc nguyên vẹn là tùy chọn và
được quản lý thông qua Git LFS để nó không làm tăng lịch sử kho lưu trữ thông thường. Máy tính để bàn GitHub bao gồm
Git LFS. Người dùng dòng lệnh có thể cài đặt Git LFS và chạy:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Các bản phát hành được gắn thẻ cũng xuất bản STL gốc dưới dạng bản tải xuống trực tiếp cho những người không sử dụng Git.
Xem [`samples/README.md`](../../../samples/README.md) để biết nguồn gốc, kích thước và tổng kiểm tra.

Những người đóng góp thuật toán cũng nên đọc
[hướng dẫn kiểm tra thuật toán](docs/ALGORITHM_TESTING.md) trước khi so sánh hoặc thay đổi mức giảm
hành vi.

## Đơn vị STL

STL không mã hóa một đơn vị. Thay đổi Đơn vị mô hình thay đổi nhãn và số đo mà không chia tỷ lệ
tọa độ đã lưu. Chọn đơn vị mô tả hình học nguồn.

## Quyền riêng tư

MeshMill đọc và ghi các tệp cục bộ. Nó không chứa tài khoản, đo từ xa, tải lên, quảng cáo hoặc
tính năng xử lý đám mây. Việc triển khai số liệu GPU hiện tại sử dụng hiệu suất Windows cục bộ
quầy. Các nhà cung cấp số liệu gốc tương đương được lên kế hoạch cho Linux và macOS.

Để khắc phục sự cố chẩn đoán, nhà phát triển có thể khởi động GUI bằng
`--diagnostic-log <local-file.jsonl>`. Nhật ký ghi lại định tuyến đầu vào và trạng thái camera cục bộ và được
bị vô hiệu hóa trong quá trình sử dụng bình thường.

## Phát triển và phát hành

- [Đóng góp](CONTRIBUTING.md)
- [Quy trình phát hành](RELEASING.md)
- [Lộ trình](ROADMAP.md)
- [Khắc phục sự cố](docs/TROUBLESHOOTING.md)
- [Thông báo của bên thứ ba](THIRD_PARTY_NOTICES.md)

## Hỗ trợ MeshMill

MeshMill được phát triển và duy trì độc lập. Đọc
[tại sao việc hỗ trợ công việc này lại quan trọng](SUPPORT.md), hoặc hỗ trợ tiếp tục phát triển thông qua
[Mua cho tôi một ly cà phê](https://buymeacoffee.com/tednv).

MeshMill được cấp phép theo Giấy phép Công cộng GNU, phiên bản 3 trở lên. Xem
[`LICENSE`](../../../LICENSE).
