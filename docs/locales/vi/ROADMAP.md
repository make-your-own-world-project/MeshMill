# Lộ trình MeshMill

## Hỗ trợ nền tảng

Windows là nền tảng đóng gói ban đầu. Kiến trúc ứng dụng và các định dạng lưới
đa nền tảng và các bản phát hành trong tương lai sẽ thêm các gói Linux và macOS gốc. Nền tảng làm việc
bao gồm đóng gói, tích hợp ứng dụng, số liệu phần cứng, hành vi hệ thống tập tin và tự động
phát hành thử nghiệm trong khi vẫn duy trì cùng một dự án và quy trình công việc STL trên mọi hệ thống được hỗ trợ.

- Xác thực gói xem trước Linux x86-64 trên các bản phân phối, môi trường máy tính để bàn, màn hình
  máy chủ và trình điều khiển GPU trước khi nâng cấp nó lên mức ổn định.
- Xác thực các gói xem trước macOS Apple silicon và x86-64 trên phần cứng thực, sau đó thêm Nhà phát triển
  Ký CMND và công chứng trước khi thăng hạng lên ổn định.
- Thêm các nhà cung cấp số liệu CPU, bộ nhớ và GPU gốc nền tảng đằng sau một giao diện dùng chung.
- Giữ các cài đặt đã lưu, ánh xạ bàn phím, hành vi dòng lệnh và dữ liệu dự án ở dạng di động.

Lộ trình này ghi lại công việc theo kế hoạch. Nó không mô tả các tính năng trong phiên bản hiện tại.

## Phạm vi

MeshMill quản lý hình học, mật độ lưới, mật độ điểm, tối ưu hóa, dọn dẹp, xác thực và STL
trao đổi để các tệp lưới lớn hoặc nặng vẫn hữu ích trong quy trình chỉnh sửa tiếp theo.

Tạo mô hình đa năng, điêu khắc, hội họa, hoạt hình, kết xuất, bố cục cảnh, vật liệu,
gian lận và các hệ thống tạo nội dung khác nằm ngoài lộ trình này. Áp dụng tổng hợp phân tán
đối với các hoạt động quản lý lưới của MeshMill và không mở rộng sản phẩm thành một trình soạn thảo chung.

## Hình học tham khảo

Lưới tổng hợp đi kèm là công cụ phát triển chung cho các thuật toán và lộ trình hiện tại
làm việc. Các lớp dư thừa có chủ ý và mật độ không đồng đều của nó hỗ trợ việc so sánh lặp lại của
giảm chất lượng, phân tích mật độ, xử lý chồng chéo, vận hành khu vực, xử lý ngoài lõi,
và tổng hợp trong tương lai. Việc triển khai lộ trình sẽ báo cáo kết quả đối với lịch thi đấu này và các
lưới hồi quy được xây dựng có mục đích, thay vì chỉ tối ưu hóa hành vi cho một mô hình.

## Không gian làm việc Multi-STL và tổng hợp thống kê

Một không gian làm việc phải chấp nhận nhiều đầu vào STL dưới dạng các đối tượng nguồn riêng biệt, hiển thị độc lập.
MeshMill sẽ căn chỉnh các nguồn đó, đo lường sự phù hợp hình học của chúng và tổng hợp một nguồn có thể sử dụng được
lưới mà không giữ lại các bề mặt bên trong trùng lặp hoặc hình học chồng chéo lặp đi lặp lại.

Hành vi có kế hoạch:

- thêm, xóa, ẩn, cô lập, sắp xếp lại và kiểm tra nhiều nguồn STL trong một không gian làm việc;
- giữ lại danh tính nguồn, đơn vị, biến đổi, giới hạn, độ phân giải và lịch sử hoạt động;
- cung cấp đăng ký tự động với các biện pháp kiểm soát căn chỉnh thủ công và chất lượng phù hợp có thể đo lường được;
- phân chia nguồn thành các vùng không gian trước khi so sánh sao cho đầu vào lớn vẫn bị giới hạn;
- phân tích tỷ lệ chiếm chỗ, khoảng cách bề mặt gần nhất, thỏa thuận bình thường, mật độ cục bộ, phương sai và
  số lượng quan sát trên các vùng chồng chéo;
- phân loại các bề mặt phù hợp, bề mặt xung đột, quét tiếng ồn, khoảng trống và hình học độc đáo;
- hợp nhất các bề mặt thống kê thành một bề mặt đại diện với các bề mặt được ghi lại
  sự tự tin thay vì xếp chồng các hình tam giác trùng lặp;
- loại bỏ hình học kèm theo, trùng khớp và chia sẻ mà không đóng góp chi tiết hình dạng bên ngoài;
- giữ lại hình dạng nguồn không chồng chéo và hiển thị các vùng mơ hồ để xem xét trực quan;
- cho phép tính trọng số theo từng nguồn và từng vùng khi một lần quét sạch hơn hoặc chi tiết hơn;
- xác nhận tính kín nước, ranh giới, quy chuẩn, kích thước và cấu trúc liên kết sau khi tổng hợp;
- ghi lại các thông số tổng hợp và xuất xứ nguồn để lưới kết hợp có thể tái tạo được;
- xem trước số lượng tam giác dự kiến, giới hạn, loại bỏ chồng chéo và phân bổ độ tin cậy trước
  thực hiện kết quả tổng hợp.

Quy trình công việc này nên sử dụng cùng một chỉ mục không gian bên ngoài lõi và mô hình đơn vị công việc được lên kế hoạch cho quy mô lớn.
mắt lưới. So sánh thống kê và hợp nhất chồng chéo cũng nên được phân phối giữa các địa phương
hoặc các nút MeshMill từ xa.

## Tổng hợp phân tán

Cụm MeshMill phải phối hợp nhiều nút hoạt động song song trên nhiều
các máy trạm. Một nút có thể kiểm tra, lựa chọn, giảm bớt, xác nhận, sửa chữa hoặc kết hợp một vùng hoặc
đơn vị công tác. Đóng góp vẫn được phiên bản độc lập cho đến khi chúng được xem xét và kết hợp
thành một phiên bản đối tượng được chia sẻ.

Hệ thống cần hỗ trợ:

- đóng góp đồng thời từ nhiều nhà khai thác và các nút tự động;
- đầu vào, tham số, sự phụ thuộc và đầu ra của đơn vị công việc xác định;
- lập lịch nhận biết khả năng dựa trên CPU, GPU, bộ nhớ, thuật toán và tải hiện tại;
- phân vùng nhận biết phụ thuộc của các mắt lưới, vùng, các bước xác thực và các giai đoạn tổng hợp;
- hàng đợi bền bỉ với tính năng tạm dừng, tiếp tục, hủy, thử lại, phân công lại và phục hồi lỗi;
- các tạo phẩm có địa chỉ nội dung và kiểm tra tính toàn vẹn giữa các nút;
- tổng hợp có thể tái tạo từ một tập hợp các phiên bản đóng góp được chấp nhận đã được ghi lại;
- các máy trạm ngoại tuyến hoặc được kết nối không liên tục có thể đồng bộ hóa sau này;
- hoạt động ưu tiên cục bộ với quyền kiểm soát rõ ràng đối với các nút tham gia và dữ liệu dự án được chia sẻ.

## Hợp tác theo phiên bản

Mọi đóng góp phải ghi lại phiên bản đối tượng gốc, khu vực hoặc đơn vị công việc đã chọn, hoạt động,
tham số, nhận dạng nút, dấu thời gian, phụ thuộc, kết quả xác thực và tổng kiểm tra đầu ra.

Hành vi hợp tác dự kiến:

- dự án chứa các đối tượng, nhánh, điểm kiểm tra, đóng góp và phiên bản tổng hợp;
- những người đóng góp có thể làm việc từ cùng một phiên bản gốc mà không ghi đè lên nhau;
- đóng góp không chồng chéo có thể tự động hợp nhất sau khi xác thực;
- hình học chồng chéo hoặc sự phụ thuộc không tương thích tạo ra xung đột rõ ràng;
- xung đột cung cấp so sánh trực quan, lựa chọn cấp khu vực, rebase, chạy lại và giải quyết thủ công;
- các trạng thái xem xét bao gồm đang chờ xử lý, được chấp nhận, bị từ chối, bị thay thế, xung đột và được hợp nhất;
- bản kê khai tổng hợp cuối cùng xác định mọi đóng góp và phụ thuộc được kết hợp.

## Giao diện điều phối

Ứng dụng máy tính để bàn sẽ quản lý công việc phân tán mà không yêu cầu dòng lệnh riêng
hoặc quy trình làm việc quản trị máy chủ. Các chế độ xem theo kế hoạch bao gồm:

- **Dự án:** đối tượng, nhánh, phiên bản, người đóng góp và trạng thái tổng hợp.
- **Cụm:** các máy trạm và nút được kết nối, khả năng, tình trạng, tải và phân công hiện tại.
- **Hàng đợi:** đơn vị công việc đang chờ xử lý, đang hoạt động, bị tạm dừng, bị chặn, không thành công và đã hoàn thành.
- **Đóng góp:** tác giả, nút, phiên bản gốc, khu vực bị ảnh hưởng, thông số, kiểm tra và trạng thái đánh giá.
- **So sánh:** chế độ xem 3D được đồng bộ hóa, sự khác biệt về hình học, số liệu và kiểm tra ranh giới.
- **Xung đột:** các vùng chồng chéo, xung đột phụ thuộc, lựa chọn giải pháp và kết quả xác thực.
- **Tổng hợp:** biểu đồ phụ thuộc, tiến trình tổng hợp, các phiên bản đóng góp đã chọn và đầu ra cuối cùng.
- **Lịch sử:** biểu đồ nhánh, điểm kiểm tra, hợp nhất, phiên bản tổng hợp và bảng kê khai khả năng tái tạo.

Chế độ xem sẽ hiển thị quyền sở hữu, khu vực được chỉ định, công việc đã hoàn thành, các thay đổi đang chờ xử lý, xung đột,
và sự khác biệt về phiên bản mà không làm thay đổi lưới bên dưới.

## Điều phối và vận chuyển

Giai đoạn thiết kế đầu tiên cần xác định ranh giới giao thức trước khi chọn phương thức vận chuyển. giao thức
nên tách biệt siêu dữ liệu phối hợp khỏi các tạo phẩm lưới lớn, hỗ trợ quá trình truyền có thể tiếp tục và
vẫn có thể sử dụng được trên mạng cục bộ mà không cần tài khoản bên ngoài hoặc dịch vụ lưu trữ.

Khái niệm phối hợp cần thiết:

- bầu cử điều phối viên hoặc điều phối viên được lựa chọn rõ ràng;
- phát hiện nút và đăng ký nút thủ công;
- phiên xác thực và ủy quyền trong phạm vi dự án;
- hợp đồng thuê và nhịp tim để sở hữu công việc;
- trình bày công việc bình thường và chấp nhận kết quả;
- đàm phán phiên bản giữa các bản phát hành MeshMill khác nhau;
- các sự kiện có cấu trúc về tiến trình, nhật ký, xác thực, lỗi và thử lại;
- phục hồi sau khi điều phối viên, máy trạm, mạng hoặc nút bị gián đoạn.

## Giai đoạn giao hàng

### Giai đoạn 0: xử lý lưới lớn ngoài lõi

Chỉ mục, phát trực tuyến, bộ đệm, đơn vị công việc và hợp đồng an toàn được ghi lại trong
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Ước tính số lượng tam giác và bộ nhớ làm việc trước khi phân bổ lưới hoàn chỉnh.
- Mở các tệp STL nhị phân quá khổ dưới dạng tổng quan về điều hướng được lấy mẫu đồng đều, có giới hạn.
- Phân vùng hình học có độ phân giải đầy đủ thành các khối không gian có ranh giới chồng chéo xác định.
- Đọc, phân tích và tối ưu hóa các khối độc lập đồng thời trong giới hạn bộ nhớ và CPU.
- Việc triển khai tính toán GPU điểm chuẩn cho các giai đoạn giảm thiểu như đánh giá lỗi, đánh giá ứng cử viên
  tính điểm, truy vấn không gian và xử lý đơn vị công việc độc lập. Chỉ giảm tải một giai đoạn khi nó
  cung cấp lợi ích về bộ nhớ hoặc tốc độ từ đầu đến cuối có thể đo lường được mà không làm giảm tính xác định, tính lưới
  chất lượng, đảm bảo cấu trúc liên kết hoặc khả năng tương thích với các hệ thống thiếu GPU phù hợp.
- Truyền phát các cấp độ khung nhìn từ thô đến mịn thay vì yêu cầu lưới hoàn chỉnh trong bộ nhớ.
- Vẽ trạng thái khối trực tiếp trong khung nhìn: xếp hàng, đọc, xử lý, hoàn thành và không thành công.
- Hiển thị tiến trình trên mỗi khối bằng cách lấp đầy từng khối và duy trì chế độ xem toàn bộ đối tượng ở cấp độ cao.
- Tập hợp các khối đã xử lý với xác thực ranh giới, loại bỏ trùng lặp và cài đặt có thể tái tạo.
- Mở rộng bộ lập lịch khối cục bộ thành các đơn vị công việc tổng hợp phân tán trong các giai đoạn sau.

### Giai đoạn 1: nền tảng địa phương được phiên bản

- Xác định các định dạng đối tượng, hoạt động, đóng góp, nhánh và bảng kê khai.
- Thêm không gian làm việc đa STL với khả năng hiển thị, biến đổi, siêu dữ liệu và xuất xứ theo từng nguồn.
- Thêm số liệu chất lượng đăng ký và phân loại chồng chéo không gian.
- Tổng hợp các bề mặt phù hợp về mặt thống kê trong khi loại bỏ các hình học trùng lặp và kèm theo.
- Thêm đánh giá trực quan về các xung đột, khoảng trống, độ tin cậy và hình học duy nhất cho một nguồn.
- Duy trì lịch sử cục bộ qua các phiên ứng dụng.
- Thêm so sánh lưới và khu vực trực quan.
- Làm cho các hoạt động mang tính xác định và có thể tái sản xuất độc lập.

### Giai đoạn 2: các nút cục bộ phối hợp

- Chạy các nút công nhân trên một máy trạm.
- Thêm hàng đợi, báo cáo năng lực, phân công công việc và hủy bỏ.
- Hiển thị trạng thái nút và đơn vị công việc trong giao diện người dùng MeshMill.
- Xác thực phân vùng và lắp ráp kết quả cục bộ.

### Giai đoạn 3: tổng hợp nhiều máy trạm

- Thêm khám phá và đăng ký mạng LAN được xác thực.
- Chuyển đầu vào và kết quả công việc được giải quyết theo nội dung với sự hỗ trợ sơ yếu lý lịch.
- Phối hợp công việc đồng thời trên nhiều máy trạm.
- Khôi phục các bài tập sau khi nút hoặc mạng bị lỗi.

### Giai đoạn 4: phiên bản hợp tác

- Thêm người đóng góp, chi nhánh, trạng thái đánh giá và quyền.
- Hợp nhất các đóng góp không chồng chéo.
- Phát hiện và giải quyết xung đột chồng chéo hoặc phụ thuộc.
- Tổng hợp những đóng góp đã chọn thành một phiên bản đối tượng có thể tái tạo.

### Giai đoạn 5: tăng cường sản xuất

- Thêm các bài kiểm tra khả năng tương thích giao thức và xử lý phiên bản hỗn hợp.
- Thêm các bài kiểm tra kiểm toán, tính toàn vẹn, tham nhũng, gián đoạn và phục hồi.
- Hiệu suất lập lịch, phân vùng, chuyển giao, hợp nhất và tổng hợp điểm chuẩn.
- Triển khai, sao lưu, di chuyển và khắc phục sự cố tài liệu.
