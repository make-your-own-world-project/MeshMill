# Phát hành MeshMill

Quy trình phát hành ổn định xây dựng các tạo phẩm Windows trên các trình chạy Windows được lưu trữ trên GitHub. riêng biệt
quy trình làm việc thủ công xây dựng các bản xem trước silicon x86-64 và macOS không có chữ ký của Intel/Apple trên bản gốc (Linux)
Người chạy được lưu trữ trên GitHub. Người dùng cuối không cài đặt Python, Node.js hoặc các phần phụ thuộc.

Trước khi xây dựng, hãy làm mới và xác thực danh mục nguồn bản địa hóa:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Trước khi phát hành ra công chúng lần đầu tiên

1. Hoàn thiện và xác nhận các bản dịch tài liệu và ứng dụng theo kế hoạch.
2. Xem lại GPL và các thông báo của bên thứ ba.
3. Kiểm tra cài đặt, khởi chạy, tải, tối ưu hóa, xuất và gỡ cài đặt STL một cách sạch sẽ
   Tài khoản Windows hoặc máy ảo.
4. Chạy CI với `samples/sample-scan.stl`. Kiểm tra mọi ảnh chụp màn hình tài liệu và cắt bỏ
   thanh tác vụ, chrome cửa sổ không thuộc MeshMill, thông báo, đường dẫn riêng tư, tài khoản
   chi tiết và nội dung máy tính để bàn không liên quan trước khi xuất bản.
5. Định cấu hình tác giả Git cục bộ của kho lưu trữ với địa chỉ không trả lời GitHub của tài khoản trước
   cam kết đầu tiên. Xác nhận nó với `git config --local --get user.email`.
6. Định cấu hình bí mật ký Authenticode tùy chọn:
   - `WINDOWS_CERTIFICATE_BASE64`: Chứng chỉ PFX được mã hóa Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: Mật khẩu PFX.

Nếu không có chứng chỉ ký, các tệp được tạo vẫn hoạt động nhưng Windows SmartScreen có thể hiển thị
một cảnh báo nhà xuất bản không được công nhận. Không mô tả các bản dựng chưa được ký là đã được ký hoặc đáng tin cậy.

## Quét gốc và Git LFS

`samples/original-scan.stl` được theo dõi thông qua Git LFS vì nó vượt quá 100 MiB bình thường của GitHub
giới hạn tập tin. Trước lần cam kết đầu tiên, hãy xác minh:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Bộ lọc phải là `lfs` và ID đối tượng con trỏ phải khớp với `samples/SHA256SUMS.txt`. Việc phát hành
quy trình làm việc kiểm tra nội dung LFS và xuất bản STL gốc dưới dạng nội dung phát hành riêng biệt. sử dụng CI
mẫu Git bình thường nhỏ hơn và không tải xuống đối tượng LFS.

## Kiểm tra bản phát hành mà không xuất bản

Mở **Hành động**, chọn **Phát hành**, chọn **Chạy quy trình công việc** và nhập phiên bản số, chẳng hạn như
`0.1.0`. Chạy thủ công tải lên các tạo phẩm quy trình làm việc để thử nghiệm nhưng không tạo GitHub công khai
Thả ra.

## Xuất bản một bản phát hành

Từ một nhánh `main` sạch sẽ, được đánh giá:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Thẻ bắt đầu quy trình phát hành. Nó:

1. cài đặt các phần phụ thuộc của bản dựng được ghim;
2. tạo siêu dữ liệu phiên bản Windows phù hợp;
3. xây dựng các tệp thực thi GUI và CLI độc lập;
4. ký các tệp thực thi khi ký bí mật được định cấu hình;
5. xây dựng trình cài đặt Inno Setup cho mỗi người dùng;
6. ký vào trình cài đặt khi được cấu hình;
7. tạo tệp tổng kiểm tra ZIP và SHA-256 di động;
8. tải lên các tạo phẩm quy trình công việc;
9. tạo Bản phát hành GitHub cho thẻ được đẩy.

Xác minh trình cài đặt và kho lưu trữ di động trên hệ thống Windows sạch trước khi thông báo phát hành.
Giữ nguồn tương ứng với mọi tệp nhị phân được phân phối có sẵn trong cùng một thẻ phát hành.
Xác nhận rằng nút GitHub trỏ đến URL kho lưu trữ công cộng cuối cùng trước khi gắn thẻ đầu tiên
thả ra.

## Xây dựng bản xem trước Linux và macOS

Mở **Tác vụ**, chọn **Bản xem trước nền tảng** và chọn **Chạy quy trình công việc**. Nhập bản xem trước
phiên bản chẳng hạn như `0.2.0-preview.1`.

Tắt **Xuất bản bản phát hành trước GitHub công khai** trong lần chạy đầu tiên. Quy trình xây dựng và kiểm tra quy trình làm việc:

- Linux x86-64 trên Ubuntu 22.04;
- macOS x86-64 trên bộ chạy Intel;
- macOS arm64 trên một con chạy silicon của Apple.

Tải xuống các tạo phẩm của quy trình làm việc và kiểm tra tổng kiểm tra cũng như nhật ký của chúng. Chạy lại quy trình làm việc với
chỉ được phép xuất bản sau khi mỗi công việc xây dựng trôi qua. Các bản xem trước macOS đã xuất bản được ký đặc biệt,
không được Apple công chứng. Mô tả chúng dưới dạng bản dựng xem trước và liên kết người thử nghiệm với
`docs/PLATFORM_TESTING.md` và biểu mẫu vấn đề **Kiểm tra bản xem trước nền tảng**.
