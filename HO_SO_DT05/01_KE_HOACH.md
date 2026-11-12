# Kế hoạch phát triển và bàn giao

**Hiệp phụ trách dữ liệu và kiểm tra điều kiện. Chung phụ trách luồng sử dụng và quyền truy cập.** Đến giữa kỳ, hai phần phải gặp nhau ở thao tác “xếp người vào ca”. Quản lý chọn người, máy chủ giải thích kết quả và chỉ lưu được một phân công hợp lệ. Đến cuối kỳ, hai người trình diễn tiếp từ công bố cho đến khi đổi ca xong.

### Quỹ thời gian

Từ chiều 12/11 đến 18/12 có 18 buổi đã đăng ký, mỗi buổi 4 giờ cho mỗi người. Nhóm có tối đa 144 giờ-người nếu đủ cả 18 buổi. Dự toán 120 giờ-người cho công việc trong bảng, 24 giờ còn lại dành cho phản hồi, sửa lỗi và buổi đã sử dụng một phần. Cuối mỗi thứ Sáu, người đang giữ đầu việc ghi số giờ còn cần và lỗi đang cản mốc kế tiếp. Lịch cụ thể theo từng buổi có trong [lộ trình chung](../LO_TRINH_DT05.md).

| Việc | Thời điểm chuẩn bị / hạn chính thức 2026 | Người chính, phối hợp | Phụ thuộc | Kết quả để đóng việc | Giờ-người ước tính |
|---|---|---|---|---|---:|
| P1. Môi trường và bổ sung M1 | Rà 12/11 / M1 đã đến hạn 11/11 | Hiệp tạo repo, Chung cài máy hai | Có đầu mối giao bài đầu vào cho từng người | Cả hai chạy migration trên SQL Server của mình, có minh chứng cá nhân. Xin xác nhận cách bổ sung bài M1. | 8 |
| P2. Khảo sát và M2 | Gửi 13/11 / 18/11 | Chung ghi biên bản, Hiệp chạy ví dụ | Gặp hoặc nhận phản hồi từ nghiệp vụ | Hai người duyệt nhận sơ đồ, bộ mẫu, đặc tả, biên bản thật và phạm vi. Lưu phiên bản cùng ý kiến. | 12 |
| P3. Tạo dữ liệu nền | 19–20/11 | Hiệp tạo models, Chung nhập và xem hồ sơ | P1, danh mục và trường dữ liệu ở P2 | Migrate trên hai máy, nạp mẫu hai lần cho cùng kết quả. Quản lý A chỉ xem được hồ sơ thuộc phạm vi. | 12 |
| P4. Phân ca có kiểm tra | 20–26/11 | Hiệp viết quy tắc, Chung nối màn hình | P3 và chính sách demo | CA01 chặn NV02, nhận NV01, số chỗ còn thiếu cập nhật sau khi tải lại. Có ví dụ biên cho ba nhóm quy tắc giờ, nghỉ, Chủ nhật. | 20 |
| P5. Công bố và giữa kỳ | Tổng duyệt 26/11 / M3 ngày 27/11 | Chung viết lịch cá nhân, Hiệp kiểm lại điều kiện công bố | P4 | Chạy lần lượt T01, T02, T08. Mỗi người trình bày một thao tác do mình làm và cách biết kết quả đúng. | 10 |
| P6. Đổi ca trọn luồng | 27/11–03/12 | Chung viết đơn và trang duyệt, Hiệp viết giao dịch đổi | P4, P5, xác nhận cách đổi | Duyệt đổi cập nhật cả hai lịch. Bấm lần hai và trường hợp hồ sơ vừa hết hạn đều bảo toàn dữ liệu. | 16 |
| P7. Hoàn thiện M4 | Gửi 04/12 / 09/12 | Hiệp và Chung thử chéo | P3–P6 | Mỗi yêu cầu đã duyệt có màn hình hoặc quy tắc tương ứng và ca kiểm thử. Ghi các điểm còn vướng cho người hướng dẫn. | 12 |
| P8. Kiểm thử và bàn giao | Gửi 11/12 / M5 ngày 15/12 | Chung ghi báo cáo, Hiệp tái lập trên máy hai | P7 | Kiểm thử viên chạy được từ database trống, có hướng dẫn theo hai vai trò và danh sách lỗi cùng trạng thái. | 16 |
| P9. Báo cáo cuối | Tổng duyệt 17/12 / M6 ngày 18/12 | Hai người trình bày | P8 và mẫu trường | Demo 15 phút, báo cáo theo mẫu, bộ dữ liệu có thể khôi phục và phiên bản đã trình. | 14 |

### Buổi triển khai đầu tiên sau khi chốt phạm vi

1. **Hiệp** tạo các bảng chi nhánh, vị trí, nhân viên, điều kiện và hồ sơ trước. Tạo CA01 cùng 5 nhân viên từ dữ liệu mẫu. Đưa migration, lệnh nạp mẫu và kết quả mong đợi vào cùng thay đổi.
2. **Chung** dựng trang ca với dữ liệu mẫu theo hợp đồng trong thiết kế. Thử với người quản lý CN01 và một tài khoản nhân viên. Hai người thống nhất ngay câu chữ khi NV02 hết hạn giấy.
3. **Hai người** nối nút thêm người vào cùng hàm phân công. Chung chọn NV02 rồi NV01. Hiệp kiểm tra trực tiếp số bản ghi sau từng lần và đối chiếu trạng thái hiển thị sau khi tải lại. Ghi kết quả và phiên bản Git vào nhật ký.
4. **Buổi kế tiếp** triển khai từng quy tắc giờ/nghỉ và dữ liệu Chủ nhật trước khi mở chức năng công bố. Khi đổi một quyết định M2, cập nhật đồng thời hàng yêu cầu, hàm kiểm tra và ví dụ nghiệm thu chịu ảnh hưởng.

### Khi cần điều chỉnh

| Dấu hiệu | Người xử lý và phương án |
|---|---|
| Đến 13/11 chưa có người trả lời nghiệp vụ | Hiệp gửi bộ nháp và phiếu còn mở, xin lịch trả lời trước 18/11. Chung tiếp tục mẫu màn hình và sơ đồ. |
| Máy thứ hai chưa có SQL Server hoặc driver | Chung dùng dữ liệu JSON để làm form. Hiệp đối chiếu mục 2a của hướng dẫn buổi đầu, sau đó cùng chạy migration và một giao dịch thật trên máy Chung. |
| Đến 26/11 luồng phân công vẫn chưa chạy | Hai người cùng sửa đúng kịch bản CA01. Dùng màn hình quản trị cho danh mục và bảng HTML cho lịch. Ghi phần cần dời và trình người hướng dẫn nếu ảnh hưởng tiêu chí đã duyệt. |
| Hai người chỉnh cùng một phân công, kết quả khác dự kiến | Giữ thao tác trong một giao dịch, chạy lại T14 trên SQL Server bằng hai phiên độc lập trước khi bàn giao. |
