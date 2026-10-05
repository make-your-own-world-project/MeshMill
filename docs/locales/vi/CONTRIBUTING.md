# Đóng góp

Đóng góp được chào đón thông qua các vấn đề và yêu cầu kéo.

## Phạm vi dự án

MeshMill làm cho các tệp lưới quá khổ, dày đặc hoặc khó quản lý để chỉnh sửa và
quy trình công việc sản xuất. Những đóng góp sẽ cải thiện việc kiểm tra hình học, mật độ lưới và điểm
quản lý, tối ưu hóa, lựa chọn, cắt xén, dọn dẹp, xác thực, trao đổi STL, hiệu suất,
hoặc sự phối hợp của các hoạt động đó.

Dự án không bao gồm mô hình hóa, điêu khắc, hội họa, hoạt hình, kết xuất,
bố cục cảnh, vật liệu, sự sắp xếp hoặc các hệ thống tạo nội dung khác. Những đề xuất giới thiệu
những tính năng đó nằm ngoài phạm vi dự án.

Các tính năng mới sẽ giữ cho ứng dụng tập trung, duy trì quy trình làm việc trực tiếp từ nguồn
hình học thành các mắt lưới có thể quản lý được và tránh biến các điều khiển hỗ trợ thành một chỉnh sửa chung
môi trường.

## Bản địa hóa

Văn bản nguồn UI tiếng Anh được lưu trữ trong `locales/en-US.json`. Siêu dữ liệu miền địa phương được lưu trữ trong
`locales/manifest.json`. Danh mục giao diện người dùng được dịch sử dụng cùng khóa ổn định và tên tệp
`<locale>.json`. Tài liệu được dịch sử dụng tên tệp gốc phù hợp bên dưới
`docs/locales/<locale>/`.

Các bản dịch ban đầu được thực hiện bằng dịch vụ dịch máy bên ngoài và nhận
xác nhận cấu trúc tự động. Quá trình đó không thể đảm bảo tính tự nhiên, chính xác về mặt kỹ thuật hoặc
ngôn ngữ đúng ngữ cảnh. Người bản ngữ được khuyến khích xem xét và sửa giao diện người dùng đã dịch
văn bản và tài liệu. Việc sửa bản dịch phải giữ nguyên khóa danh mục, phần giữ chỗ,
lệnh, liên kết, số đo, tên sản phẩm và cấu trúc Markdown.

Sau khi thay đổi nhãn, chú giải công cụ, hộp thoại hoặc văn bản khác mà người dùng hiển thị, hãy chạy:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Xem lại các thay đổi nguồn và các khóa được tạo lại cùng nhau.

## Thay đổi hình học và thuật toán

Sử dụng hình học mẫu đi kèm khi thay đổi tối ưu hóa, phân tích mật độ, lựa chọn, cắt xén,
xử lý tệp lớn hoặc hành vi so sánh khung nhìn. Nó cố tình chứa các lớp dư thừa
và mật độ không đồng đều, do đó, một kết quả hữu ích sẽ cải thiện khả năng quản lý mà không che giấu sự biến dạng,
loại bỏ các ranh giới có ý nghĩa hoặc âm thầm loại bỏ hình học mà thuật toán khác bảo tồn.

Ghi lại đầu vào, thuật toán, cài đặt, số lượng tam giác, kích thước, độ lệch kích thước, thời gian đã trôi qua,
và ảnh chụp màn hình có liên quan để so sánh. Kiểm tra cả vật cố định Git bình thường nhỏ hơn và khi
thay đổi liên quan đến hình học lớn hoặc nhiều lớp, vật cố định Git LFS ban đầu. Không điều chỉnh một thuật toán
chỉ riêng với vật cố định này. Thêm các trường hợp tổng hợp nhỏ cho bất biến hoặc hồi quy cụ thể
đã thử nghiệm.

Xem [Thử nghiệm và đóng góp thuật toán](docs/ALGORITHM_TESTING.md) để biết danh sách kiểm tra so sánh.

## Thiết lập phát triển

1. Cài đặt Python 3.12 64-bit trên Windows.
2. Tạo và kích hoạt một môi trường ảo.
3. Cài đặt `requirements-dev.txt`.
4. Chạy `python meshmill.py` cho GUI hoặc `python meshmill.py --help` để sử dụng CLI.
5. Chạy `python -m py_compile meshmill.py` trước khi gửi thay đổi.

Giữ các lưới riêng tư, các tệp thực thi được tạo, ảnh chụp màn hình chứa thông tin cá nhân và các tệp cục bộ
xây dựng thư mục từ các cam kết. Hình học thử nghiệm có thể phân phối lại thuộc `samples/` với
nguồn, giấy phép, kích thước và phương pháp tạo được ghi lại. Các tập tin nguồn mới nên sử dụng
Mã định danh SPDX `GPL-3.0-or-later`.

Cắt mọi ảnh chụp màn hình tài liệu thành nội dung ứng dụng MeshMill. Không bao gồm
thanh tác vụ, chrome cửa sổ không liên quan, thông báo, chi tiết tài khoản, đường dẫn riêng tư hoặc nền
nội dung máy tính để bàn.
