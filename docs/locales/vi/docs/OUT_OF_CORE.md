# Kiến trúc lưới ngoài lõi

Tính năng bảo vệ tệp lớn hiện tại của MeshMill ước tính bộ nhớ làm việc trước khi phân bổ toàn bộ
lưới. Các tệp vượt quá ngân sách được định cấu hình có thể mở dưới dạng tổng quan điều hướng giới hạn. Một
tổng quan là hình học được lấy mẫu, được xác định rõ ràng như vậy và không thể chỉnh sửa hoặc xuất dưới dạng
mặc dù đó là nguồn hoàn chỉnh.

Chi tiết phụ thuộc vào thu phóng thực sự đòi hỏi chỉ số không gian liên tục. Thiết kế dưới đây xác định rằng
giai đoạn thực hiện tiếp theo.

## Định dạng chỉ mục

Mỗi lưới nguồn nhận được một thư mục `.meshmill-index` được phiên bản chứa:

- `manifest.json`, với kích thước nguồn, thời gian sửa đổi, băm nội dung được lấy mẫu, giới hạn,
  số lượng tam giác, phiên bản chỉ mục, độ chính xác tọa độ và mô tả cấp độ;
- các ô không gian được xử lý theo cấp độ octree và mã Morton;
- một lưới hiển thị thô cho mỗi ô gốc được sử dụng;
- bản ghi tam giác có độ phân giải đầy đủ trong các ô lá; Và
- quyền sở hữu ranh giới và siêu dữ liệu chồng chéo được sử dụng trong các hoạt động và tập hợp khu vực.

Tạo chỉ mục đọc nguồn một cách tuần tự trong các khối giới hạn. Nó ghi các lần chạy ô tạm thời và
xuất bản một cách nguyên tử tệp kê khai sau khi mọi tệp được yêu cầu vượt qua quá trình xác thực. Bị gián đoạn hoặc
chỉ mục cũ được phát hiện từ bảng kê khai của nó và có thể được tiếp tục hoặc xây dựng lại mà không cần mở toàn bộ
lưới trong bộ nhớ.

## Truyền trực tuyến khung nhìn

Chế độ xem chọn các ô dựa trên sự thất vọng của máy ảnh và lỗi không gian màn hình. Gạch cha mẹ thô là
được hiển thị đầu tiên. Các ô con hiển thị sẽ thay thế chúng khi máy ảnh di chuyển đến gần hơn, trong khi ở ngoài màn hình và
gạch có tác động thấp vẫn còn thô. RAM và VRAM có ngân sách độc lập và ít được sử dụng gần đây nhất
bộ nhớ đệm. Việc giải phóng chi tiết không bao giờ giải phóng sự biểu diễn toàn bộ đối tượng thô.

Bộ lập lịch ghi lại các trạng thái ngăn xếp này: đã xếp hàng, đang đọc, đang xử lý, đang tải lên, thường trú, không thành công,
và bị hủy bỏ. Khung nhìn có thể tô màu các hình khối theo trạng thái và tô màu từng hình khối theo tỷ lệ của nó.
tiến bộ. Việc hủy bỏ sẽ loại bỏ một phần kết quả và để lại biểu diễn hoàn chỉnh cuối cùng đang hoạt động.

## Chế biến và công suất

Đơn vị công việc cục bộ là một khối cộng với sự chồng chéo xác định được yêu cầu bởi hoạt động của nó. Đồng thời
được giới hạn bởi RAM hiện có sẵn, phần trăm bộ nhớ được định cấu hình, số lượng bộ xử lý logic và
đo kích thước đơn vị công việc. Tải lên và hiển thị GPU có ngân sách VRAM riêng. Báo cáo song song
công suất là ước tính cho đến khi đo được các ô đại diện.

Hoạt động giữ lại một chủ sở hữu cho mọi phần tử ranh giới. Hội xác nhận ranh giới được chia sẻ,
loại bỏ các bản sao, kiểm tra số lượng và giới hạn cũng như ghi lại các tham số chính xác được sử dụng. Công việc giống nhau
định dạng đơn vị và kết quả sau này có thể được lên lịch trên các nút tổng hợp phân tán.

## Quy tắc an toàn

- Mẫu toàn cục được gắn nhãn là tổng quan, không phải chi tiết khung nhìn có độ phân giải đầy đủ.
- Tổng quan không thể ghi đè hoặc xuất dưới dạng lưới nguồn hoàn chỉnh.
- Các yêu cầu tải đầy vượt quá ngân sách hiện tại đòi hỏi phải có sự lựa chọn rõ ràng.
- Việc tạo chỉ mục, xử lý khối và lắp ráp vẫn có thể bị hủy và duy trì dữ liệu trước đó
  trạng thái hoàn chỉnh.
- Giá trị công suất là ước tính và xác định xem chúng mô tả động cơ hiện tại hay dự định
  thực thi gạch song song.
