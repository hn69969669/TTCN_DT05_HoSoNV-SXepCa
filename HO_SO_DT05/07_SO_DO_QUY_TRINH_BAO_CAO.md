# Sơ đồ quy trình nghiệp vụ — Hồ sơ nhân viên và xếp ca

Nhóm N01: Nguyễn Hữu Hiệp và Lê Thành Chung. Phiên bản ngày 12/11/2026.

**Phạm vi:** mô tả quy trình ứng dụng đề xuất cho chi nhánh nhà hàng theo YC01–YC11. Quản lý chủ động chọn nhân viên; hệ thống kiểm tra điều kiện trước khi lưu và công bố. Các quyết định Q1–Q6 đang chờ xác nhận theo [phiếu M2](05_XAC_NHAN_M2.md). Đây là sơ đồ thiết kế để trình bày báo cáo, chưa phải bằng chứng chức năng đã triển khai hoặc nghiệm thu. Khi đối chiếu phiên bản tạo tài liệu, `lichca/urls.py` chỉ khai báo trang chủ, còn các trạng thái nghiệp vụ đã có trong models.

## 1. Quy trình tổng quan

![Quy trình tổng quan](so_do_quy_trinh/01_tong_quan.png)

*Hình 1. Quy trình tổng quan quản lý hồ sơ, xếp ca và xử lý đề nghị đổi ca.*

**Đoạn thuyết minh có thể dùng trong báo cáo:** Quy trình bắt đầu khi quản lý cập nhật hồ sơ nhân viên, minh chứng và yêu cầu theo vị trí. Quản lý tạo ca làm việc cho chi nhánh và lựa chọn nhân viên. Hệ thống kiểm tra điều kiện trước mỗi lần lưu phân công; khi phát hiện vi phạm hoặc thiếu dữ liệu, hệ thống trả lý do để quản lý bổ sung hồ sơ hoặc chọn người khác. Khi ca đủ người, quản lý yêu cầu công bố và hệ thống đánh giá lại toàn bộ ca. Nhân viên xem lịch đã công bố của mình và có thể gửi đề nghị hoán đổi ca. Quản lý xem xét đề nghị, hệ thống kiểm tra trước khi cập nhật, sau đó nhân viên theo dõi kết quả xử lý và lịch cá nhân.

Quản lý có thể lưu ca nháp chưa đủ người và tiếp tục vào phiên sau. “Kết thúc lượt xử lý” trong các hình là kết thúc một lượt thao tác, không phải chấm dứt vòng đời quản lý lịch.

## 2. Quy trình phân công và công bố ca

![Phân công và công bố ca](so_do_quy_trinh/02_phan_cong_cong_bo.png)

*Hình 2. Kiểm tra điều kiện khi phân công và kiểm tra lại trước khi công bố ca.*

**Thuyết minh:** Hệ thống kiểm tra quyền quản lý chi nhánh, trạng thái nháp và sức chứa trước khi đánh giá nhân viên. Điều kiện gồm trạng thái hoạt động, quyền làm tại chi nhánh, hồ sơ và đào tạo theo vị trí, trùng giờ, thời gian nghỉ, tổng giờ làm và quỹ nghỉ Chủ nhật khi bị tác động. Kết quả `OK` cho phép lưu phân công; `BLOCKED` hoặc `NEED_DATA` giữ nguyên phân công và trả lý do. Sau khi đủ số người, quản lý thực hiện một yêu cầu công bố riêng. Hệ thống đọc lại dữ liệu và kiểm tra toàn ca; chỉ khi mọi điều kiện đạt mới chuyển từ `DRAFT` sang `PUBLISHED`, đồng thời lưu người và thời điểm công bố.

**Ví dụ minh họa:** CA01 cần 2 người, ban đầu có 0/2. Chọn NV02 bị chặn vì giấy điều kiện bếp hết hạn ngày 22/11/2026, trước ngày ca 23/11/2026. Chọn NV01 hợp lệ thì lưu thành 1/2. Ca vẫn nháp cho tới khi đủ 2/2 và kiểm tra công bố thành công. Đây là kết quả mong đợi theo bộ mẫu, chưa phải kết quả chạy thực tế.

Nếu không đạt, quản lý sửa dữ liệu hoặc lựa chọn nhân viên rồi thực hiện lại. Lưu phân công và công bố là hai thao tác riêng; sau khi lưu, quản lý cũng có thể dừng và tiếp tục sau.

## 3. Quy trình gửi và duyệt đổi ca

![Gửi và duyệt đổi ca](so_do_quy_trinh/03_gui_duyet_doi_ca.png)

*Hình 3. Tiếp nhận đề nghị và xử lý hoán đổi hai ca trong cùng chi nhánh.*

**Thuyết minh:** Nhân viên chọn một phân công tương lai đã công bố của mình và nhập mã phân công do đối tác cung cấp. Hệ thống kiểm tra quyền sở hữu, hai ca khác nhau, hai người khác nhau, cùng chi nhánh và không có đơn chờ trùng cặp trước khi tạo đơn `PENDING`. Đơn chờ chưa làm thay đổi lịch. Khi quản lý duyệt, hệ thống đọc lại chủ sở hữu, trạng thái đơn, thời điểm ca và dựng lịch sau đổi cho cả hai người. Nếu hợp lệ, hai phân công và quyết định `APPROVED` được ghi trong cùng giao dịch. Nếu kiểm tra không đạt, đơn vẫn chờ và lịch giữ nguyên. Quản lý có thể từ chối bằng cách ghi lý do, chuyển đơn thành `REJECTED`. Hai nhân viên xem được kết quả có liên quan đến mình.

Nếu chủ sở hữu đã thay đổi, đơn cũ phải được từ chối và nhân viên lập đơn mới khi cần. Đơn đã quyết định trả lại kết quả đã lưu khi thao tác lặp, không hoán đổi lần hai. Lỗi trong lúc ghi phải hoàn tác toàn bộ giao dịch. Sau lỗi, hệ thống cần báo xử lý chưa thành công; không hiển thị kết quả duyệt thành công.

Sơ đồ dùng phương án một người gửi, quản lý quyết định. Yêu cầu đối tác xác nhận riêng trong ứng dụng vẫn là câu hỏi Q5 chưa được chốt.

## 4. Quy ước và điều kiện áp dụng

| Nội dung | Cách đọc / yêu cầu |
|---|---|
| Hình bầu dục | Bắt đầu hoặc kết thúc một lượt xử lý. |
| Hình chữ nhật | Thao tác của người dùng hoặc xử lý của hệ thống. |
| Hình thoi | Điều kiện hoặc lựa chọn; đọc nhãn trên mũi tên để theo nhánh. |
| Màu sắc | Xanh nhạt: xử lý; vàng: quyết định; xanh lá: thành công; đỏ nhạt: lỗi, giữ nguyên dữ liệu hoặc từ chối. Nhãn chữ vẫn đủ để đọc khi in đen trắng. |
| Đăng nhập và quyền | Người dùng phải đăng nhập đúng vai trò. Mọi GET/POST đều kiểm phạm vi phía máy chủ. Sai quyền thì từ chối và giữ nguyên dữ liệu; điều kiện này áp dụng cho mọi hình. |
| Giới hạn dữ liệu | Quản lý chính sửa hồ sơ; quản lý nơi nhận chỉ xem thông tin cần cho phân ca. Trùng lịch xét mọi chi nhánh nhưng không tiết lộ chi tiết ngoài phạm vi. Lịch cá nhân lấy từ tài khoản đăng nhập. |
| Giao dịch ghi | Các đường ghi ảnh hưởng lịch dùng cùng dịch vụ và khóa `ScheduleGate(id=1)` bên trong `transaction.atomic()`, rồi đọc lại điều kiện trước khi ghi. Sơ đồ giản lược bước kỹ thuật này để dễ đọc. |
| Lỗi khi ghi | Rollback toàn bộ giao dịch và báo lỗi; không báo thành công trước khi commit. Điều này áp dụng cả lưu phân công, công bố và duyệt đổi. |
| Thời gian | Hiển thị theo `Europe/Berlin`, lưu UTC; xét ca qua nửa đêm, khoảng nghỉ và chuyển giờ mùa. |
| Ngưỡng demo chờ xác nhận | Q2 đề xuất tối đa 480 phút làm thực mỗi ca/ngày và nghỉ ít nhất 660 phút giữa hai ca riêng. Q3 đề xuất ít nhất 15 Chủ nhật nghỉ/năm; thiếu lịch nền thì chặn để bổ sung. Các số này là giả định của bản mô phỏng, chưa được ghi nhận là quyết định nghiệp vụ đã duyệt. |

## 5. Chèn vào báo cáo và chỉnh sửa

1. Trong Word, chọn **Insert → Pictures → This Device**, chọn PNG trong thư mục [so_do_quy_trinh](so_do_quy_trinh/). Giữ nguyên tỷ lệ và căn giữa; nên đặt mỗi sơ đồ trên một trang riêng, ưu tiên trang ngang nếu chữ bị nhỏ.
2. Chèn chú thích tương ứng Hình 1–3, rồi đặt đoạn thuyết minh bên dưới hoặc ở trang kế tiếp. Nếu báo cáo đã đánh số hình theo chương, thay số cho phù hợp.
3. Dùng SVG cùng tên khi cần phóng to hoặc bản in sắc nét. PNG có nền trắng, phù hợp với Word và Google Docs.
4. Dùng `.mmd` để chỉnh nội dung trong trình hỗ trợ Mermaid; `.dot` dùng cho Graphviz. Sửa `tao_so_do.cjs` rồi chạy lại sẽ tạo đồng bộ các định dạng. Nếu chỉ sửa `.mmd` hoặc `.dot`, cần tự xuất lại ảnh; lần chạy script sau sẽ ghi đè chúng.

Script tạo hình cần Node.js, `@viz-js/viz` và `sharp`. Chạy từ gốc repo:

```powershell
node .\HO_SO_DT05\so_do_quy_trinh\tao_so_do.cjs 'DUONG_DAN_NODE_MODULES'
```

Thay tham số bằng thư mục `node_modules` thực tế có hai gói trên. Repo không cần thay dependency của ứng dụng Django để sử dụng các ảnh đã xuất.

## 6. Đối chiếu yêu cầu và nguồn

| Sơ đồ | Yêu cầu liên quan | Kịch bản tham chiếu |
|---|---|---|
| Hình 1 | YC01–YC11 | T01–T15 theo từng chức năng |
| Hình 2 | YC03–YC09; YC01 về quyền | T01–T08, T11–T14 |
| Hình 3 | YC10–YC11; CL02–CL03 | T09–T10, T14–T15 |

Nguồn nội bộ: [đặc tả YC01–YC11](02_YEU_CAU.md), [thiết kế và trạng thái](03_THIET_KE.md), [kịch bản nghiệm thu](04_NGHIEM_THU.md), [các câu hỏi chờ xác nhận Q1–Q6](05_XAC_NHAN_M2.md), [điểm tiếp tục triển khai](06_BUOC_TIEP_THEO.md). Sơ đồ chưa bổ sung xếp ca tối ưu tự động, chấm công hoặc tính lương vì nằm ngoài phạm vi đề xuất.
