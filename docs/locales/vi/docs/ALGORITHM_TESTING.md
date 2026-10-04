# Kiểm tra và đóng góp thuật toán

Các thuật toán MeshMill sẽ giúp quản lý các hình học khó trong khi vẫn giữ được hiệu ứng của chúng,
đo lường được và có thể đảo ngược trước khi áp dụng kết quả.

## Đồ đạc tham khảo

Sử dụng cả hai phiên bản đi kèm của hình dạng mẫu tổng hợp:

- `samples/sample-scan.stl` là công cụ Git thông thường nhỏ hơn để phát triển thường xuyên, tự động
  kiểm tra và tìm hiểu các điều khiển.
- `samples/original-scan.stl` là bộ cố định Git LFS đầy đủ cho hành vi tệp lớn, các lớp dự phòng,
  mật độ không đồng đều, chồng chéo và hiệu suất làm việc.

Các vùng dư thừa và dày đặc là các đặc tính thử nghiệm có chủ ý. Một bài kiểm tra có thể nhắm vào họ, nhưng
không nên cho rằng mọi bề mặt chồng lên nhau đều là đồ dùng một lần. Thêm lưới tổng hợp nhỏ gọn khi
sự thay đổi cần một ranh giới, độ cong, cấu trúc liên kết, mật độ hoặc bất biến chồng chéo đã biết.

## Danh sách kiểm tra so sánh

Đối với thay đổi thuật toán hoặc tham số, hãy ghi lại:

- Phiên bản hoặc cam kết MeshMill;
- dữ liệu đầu vào và tổng kiểm tra;
- thuật toán, cài đặt trước chất lượng, mục tiêu và cài đặt nâng cao;
- số lượng tam giác và đỉnh ban đầu và kết quả;
- tỷ lệ giảm, kích thước và độ trôi kích thước;
- thời gian đã trôi qua và bộ nhớ cao nhất khi hiệu suất phù hợp;
- ảnh chụp màn hình từ cùng chế độ xem và chế độ hiển thị đã lưu;
- những thay đổi về ranh giới, lỗ hổng, tự giao nhau, chồng chéo hoặc biến dạng có thể nhìn thấy được;
- liệu kết quả đến từ thao tác toàn lưới hay chỉ chọn.

So sánh với hành vi hiện tại ở cùng một mục tiêu, không chỉ với một cài đặt trước khác có
số lượng đầu ra khác nhau. Kiểm tra màn hình bóng mờ, mật độ, khung dây và đỉnh nếu có.

## Hướng dẫn chấp nhận

Một thay đổi tối ưu hóa sẽ tránh những thay đổi kích thước không mong muốn, sự đảo ngược bề mặt rõ ràng,
vết nứt giữa các vùng được xử lý, mất ranh giới có ý nghĩa và hồi quy chất lượng lớn ở mức
số lượng đầu ra tương tự. Những thay đổi theo định hướng mật độ sẽ chứng minh rằng nồng độ bị loại bỏ đã
không mang độ cong hoặc cấu trúc liên kết hữu ích.

Kết quả hiệu năng cần xác định bộ vi xử lý, dung lượng bộ nhớ, phần cứng đồ họa, hệ điều hành
hệ thống, kích thước đầu vào và liệu dữ liệu đã được lưu vào bộ nhớ đệm hay chưa. Xác thực cấu trúc và ảnh chụp màn hình
hỗ trợ đánh giá nhưng không thay thế việc kiểm tra của những người đóng góp quen thuộc với hình học nguồn.

## Kiểm tra hồi quy

Thích các thử nghiệm xác định với dung sai rõ ràng. Giữ đồ đạc mới đủ nhỏ cho Git bình thường,
ghi lại nguồn gốc và giấy phép của chúng, đồng thời sử dụng hình học tổng hợp khi không cần thiết phải có dữ liệu nguồn thực.
Các thử nghiệm nên bao gồm việc hủy bỏ và khôi phục trạng thái khi một thao tác có thể sửa đổi hình học.
