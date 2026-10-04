# Khắc phục sự cố

## Windows chặn tải xuống

Các bản dựng cộng đồng chưa được ký có thể kích hoạt SmartScreen của Bộ bảo vệ Microsoft. So sánh đã tải xuống
hàm băm SHA-256 của tệp với `SHA256SUMS.txt` từ cùng một Bản phát hành GitHub. Bản phát hành đã ký xác định
nhà xuất bản của họ trong thuộc tính tệp Windows.

## Bản dựng di động không khởi động

Giải nén ZIP hoàn chỉnh trước khi chạy `MeshMill.exe`. Thư mục `_internal` phải được giữ nguyên tiếp theo
cho cả hai tệp thực thi. Không chạy tệp thực thi từ bên trong trình xem ZIP.

## Một STL lớn mở ra như một cái nhìn tổng quan

Nhóm làm việc ước tính vượt quá mức bộ nhớ trong Cài đặt. Chế độ tổng quan là có chủ ý
chỉ đọc. Chỉ tăng ngân sách khi máy có đủ bộ nhớ khả dụng hoặc giảm
lưới trước khi mở nó để chỉnh sửa.

## Chế độ xem chuẩn chưa được lưu

Nhấn phím tắt chế độ xem được sửa đổi Ctrl, sau đó chọn **Save** hoặc nhấn Enter để xác nhận
hộp thoại. Việc lưu một chế độ xem cũng cập nhật chế độ xem ngược lại. Dòng trạng thái báo cáo chế độ xem đã lưu.

## Phím tắt điều hướng không phản hồi

Đóng bất kỳ hộp thoại phương thức nào trước tiên. Xem lại hoặc đặt lại các phím tắt trong Cài đặt nếu chúng đã được tùy chỉnh. các
các phím tắt chế độ xem mặc định sử dụng Chèn, Trang chủ, Lên trang, Xóa, Kết thúc và Xuống trang.

## Tạo nhật ký chẩn đoán định hướng cục bộ

Ghi nhật ký chẩn đoán bị tắt theo mặc định. Để ghi lại trạng thái cục bộ của bàn phím và camera:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Nhật ký có thể chứa đường dẫn tệp đã mở. Xem lại và biên tập lại trước khi chia sẻ. Hình học lưới không
được ghi vào nhật ký.

## Báo cáo sự cố

Bao gồm phiên bản MeshMill, phiên bản Windows, mẫu GPU, số lượng tam giác lưới, hành động chính xác
trình tự và liệu trình cài đặt hoặc gói di động đã được sử dụng hay chưa. Sử dụng mẫu có thể phân phối lại
lưới khi có thể. Không đính kèm bản quét riêng tư hoặc nhật ký chẩn đoán mà không xem xét chúng trước.
