# Hướng dẫn làm việc trong repo DT05

Áp dụng cho toàn bộ repo. Nhóm N01 (Nguyễn Hữu Hiệp và Lê Thành Chung) xây ứng dụng **Hồ sơ nhân viên và xếp ca** cho chi nhánh nhà hàng. Giao tiếp với nhóm bằng tiếng Việt. Giữ tên model, hàm và mã lỗi theo thiết kế để hai người có thể tích hợp phần việc của nhau.

## Khi bắt đầu một yêu cầu

1. Xác định người dùng cần **hướng dẫn**, **đánh giá hiện trạng**, **viết code** hay **tạo tài liệu**. Khi họ muốn tự thực hành, giao các bước và dấu hiệu hoàn thành. Khi họ giao việc triển khai, thực hiện đến khi kiểm tra được kết quả.
2. Chạy `git status --short --branch`. Đọc các thay đổi đang có trong phần sắp sửa. Dùng `rg` để tìm điểm vào, model, dịch vụ và kiểm thử liên quan. Giữ phần việc đang làm của thành viên khác.
3. Chọn đúng tài liệu trong bảng dưới. Kiểm tra lại bằng code, migration, câu trả lời nghiệp vụ hoặc kết quả chạy cùng phiên bản. Một URL trong tài liệu thiết kế chỉ thể hiện ý định cho đến khi tìm thấy route và view tương ứng.
4. Nếu yêu cầu là **“tiếp tục”**, tìm đầu việc đầu tiên chưa đạt trong [hướng dẫn Hiệp và Chung](HO_SO_DT05/06_BUOC_TIEP_THEO.md). Nêu người thực hiện, điều kiện đầu vào và một thao tác phải chạy được cuối buổi. Nếu mã nguồn đã vượt tài liệu, tiếp tục từ phần thiếu thực tế.

| Cần quyết định | Nguồn trong repo |
|---|---|
| Cài mới, chạy ứng dụng, cấu hình máy | [README](README.md), [hướng dẫn import](scripts/HUONG_DAN_IMPORT.md) |
| Ai làm, mốc nào cần giao gì | [Kế hoạch](HO_SO_DT05/01_KE_HOACH.md), [lịch từng buổi](LO_TRINH_DT05.md) |
| Chức năng, quyền và quyết định đã được duyệt | [YC01–YC11, CL01–CL05](HO_SO_DT05/02_YEU_CAU.md), [phiếu Q1–Q6](HO_SO_DT05/05_XAC_NHAN_M2.md) |
| Quan hệ bảng, trạng thái và hợp đồng giữa giao diện với nghiệp vụ | [Thiết kế hệ thống](HO_SO_DT05/03_THIET_KE.md), [models hiện hành](lichca/models.py), [migration](lichca/migrations/) |
| Dùng dữ liệu nào, mong đợi điều gì | [Bộ mẫu JSON](HO_SO_DT05/du_lieu_mau.json), [kịch bản T01–T15](HO_SO_DT05/04_NGHIEM_THU.md) |

## Điểm tiếp tục của nhóm

Ở phiên bản khởi tạo, repo đã có app `lichca`, trang chủ, Django Admin, 13 bảng nghiệp vụ, script import và lệnh `seed_demo`. Kiểm tra [route](lichca/urls.py), [view](lichca/views.py) và [cấu hình Admin](lichca/admin.py) để biết màn hình nào đã có. Việc máy Chung đã chạy thành công và việc M2 được duyệt cần minh chứng từ chính người thực hiện.

| Thứ tự khi nhóm yêu cầu phát triển tiếp | Công việc và dấu hiệu hoàn thành |
|---|---|
| 1. Hai máy dùng cùng dữ liệu | Chung clone/pull, cấu hình SQL Server của máy mình và chạy migration. Hiệp cùng Chung kiểm lệnh seed hiện có. Trên DB thử mới, lần đầu có 5 nhân viên, 2 chi nhánh, 4 ca; lần hai tạo thêm 0 bản ghi. |
| 2. Đọc hồ sơ và chi tiết ca | Chung làm trang danh sách/chi tiết theo quyền và đăng ký bảng nghiệp vụ ở Admin theo chế độ đọc. Quản lý CN01 xem được giấy của NV02 hết hạn 22/11/2026 và CA01 còn 0/2 người. Thử thêm tài khoản quản lý CN02 để kiểm tra giới hạn xem hồ sơ. |
| 3. Phân công đầu tiên | Hiệp làm hàm đánh giá điều kiện và dịch vụ ghi, Chung nối form POST. Chọn NV02 vào CA01 phải nêu lý do và giữ 0/2. Chọn NV01 hợp lệ phải lưu thành 1/2 kể cả sau khi tải lại. |
| 4. Hoàn thiện M3 | Ghép các quy tắc đã chốt về hồ sơ, trùng giờ, thời gian nghỉ, tổng giờ và Chủ nhật. Kiểm lại toàn ca khi công bố. Đăng nhập bằng tài khoản nhân viên đã gắn với hồ sơ để xem lịch cá nhân. |
| 5. Hoàn thiện M4–M6 | Gửi và duyệt đổi ca, kiểm hai người trong một giao dịch, chạy kịch bản lỗi và đồng thời. Sau đó lập báo cáo kiểm thử, tái lập cài đặt trên máy thứ hai và tổng duyệt 15 phút. |

## Kỹ năng và công cụ theo loại việc

Chọn kỹ năng theo đầu ra người dùng yêu cầu. Đọc hướng dẫn của skill đang có trong phiên khi sử dụng. Các việc lập trình thông thường dùng trực tiếp công cụ của repo.

| Công việc | Cách thực hiện |
|---|---|
| Backend, schema và dữ liệu mẫu | Dùng Django ORM, migration, management command và SQL Server. Đọc [lệnh seed](lichca/management/commands/seed_demo.py) trước khi đổi bộ mẫu. |
| Giao diện và phân quyền | Dùng Django views/forms/templates, session auth và CSRF. Thử qua trình duyệt hoặc Django test client với tài khoản đúng vai trò. Dùng skill điều khiển máy tính khi cần thao tác thật trên giao diện. |
| Kiểm thử, rà soát code | Lần từ thao tác của người dùng qua view, quyền, dịch vụ tới DB. Chọn ca T tương ứng, kiểm kết quả trả về và dữ liệu sau khi tải lại. Với lỗi, ghi thao tác tái hiện và chạy lại sau khi sửa. |
| Tài liệu M2/M5/M6 | Dùng Markdown và Mermaid cho tài liệu repo. Khi cần Word, PDF, bảng tính hoặc slide, dùng skill Documents, PDF, Spreadsheets hoặc Presentations tương ứng nếu có. Kiểm tra bản xuất đúng định dạng. |
| GitHub và bàn giao | Dùng Git hoặc kết nối GitHub có quyền trong phiên. Theo yêu cầu xuất bản, rà diff và danh sách file, commit đúng phạm vi, push bình thường, đối chiếu SHA local/remote. |

## Quy ước kỹ thuật và nghiệp vụ

- **Môi trường.** Windows/PowerShell, Python 3.13, Django 5.2, Microsoft SQL Server qua `mssql-django` và ODBC 17/18. Mỗi máy dùng `.env` riêng dựa trên [.env.example](.env.example). Lấy tên instance từ máy đang dùng. Giữ khóa ứng dụng, mật khẩu, file database và bản sao lưu ngoài Git.
- **Schema.** Thay đổi model trong `lichca/models.py`, tạo migration mới, đọc thao tác và thử trên SQL Server. Ràng buộc duy nhất, FK và CHECK trong DB phải tương thích với dữ liệu đã có. Kiểm tra lịch sử trước khi sửa lỗi migration trên máy thành viên.
- **Quyền.** Kiểm tra tài khoản, vai trò và phạm vi chi nhánh phía máy chủ cho GET lẫn POST. Lịch cá nhân lấy nhân viên từ tài khoản đăng nhập. Khi kiểm tra trùng lịch, xét cả chi nhánh khác nhưng chỉ trả chi tiết người xem được phép biết. Tách tài khoản superuser phục vụ cài đặt khỏi tài khoản dùng kiểm thử phân quyền.
- **Phân ca và đổi ca.** Các đường ghi có thể thay đổi kết quả xếp lịch phải dùng cùng dịch vụ nghiệp vụ và quy ước khóa. Mở `transaction.atomic()`, khóa hàng `ScheduleGate(id=1)` theo thiết kế, rồi đọc lại điều kiện và sức chứa. Khi đổi, dựng lịch dự kiến của cả hai người, kiểm chủ sở hữu và trạng thái đơn, ghi hai phân công cùng quyết định trong một giao dịch. Thử cả bấm duyệt lại và lỗi giữa hai lần ghi.
- **Thời gian.** Hiển thị giờ chi nhánh theo `Europe/Berlin`, lưu thời điểm theo UTC và tính khoảng ca dạng [bắt đầu, kết thúc). Chú ý ca qua nửa đêm, nghỉ nội ca và thời điểm đổi giờ. Đối chiếu Q1–Q6 trước khi thay ngưỡng. Các giả định demo chỉ trở thành quyết định nghiệp vụ khi có xác nhận thực tế.
- **Dữ liệu.** Dùng bộ mẫu hư cấu. Lệnh seed phải chạy lặp an toàn, báo khóa xung đột và rollback lần nạp khi dữ liệu khác. Kiểm thử ghi, xung đột và đồng thời trên database thử dành riêng. Khi chạy lệnh import, chú ý script lưu thông số kết nối vào `.env` của máy chạy.

## Lệnh kiểm tra và bàn giao

Chạy từ gốc repo trong PowerShell. Chọn lệnh tương ứng với thay đổi:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations lichca
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test lichca
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

- Khi sửa model: chạy `makemigrations lichca`, đọc migration, chạy `migrate` trên DB phát triển/thử rồi kiểm tra lại. Khi cài máy mới, dùng script import trong README. Khi thử dữ liệu mẫu, chạy `manage.py seed_demo --manager TEN_DANG_NHAP_LOCAL` với tài khoản quản trị đã tạo trên máy đó.
- Khi sửa hành vi: bổ sung kiểm thử cho rủi ro cụ thể mà bộ hiện có chưa bắt được. Kiểm cả trường hợp được phép, bị chặn và trạng thái DB sau thất bại. Nếu test runner báo 0 test, ghi đúng con số và mô tả ca nào thực sự đã chạy. Với sửa tài liệu, kiểm đường dẫn, tên lệnh và sự khớp với code.
- Khi bàn giao: ghi tính năng đã chạy, mã YC/T liên quan, kết quả thực tế, điểm chưa xác minh và việc tiếp theo của Hiệp/Chung. Chỉ ghi “đã duyệt”, “đã chạy trên máy Chung” hoặc “đã push” khi có bằng chứng tương ứng. Cập nhật tài liệu liên quan nếu kết quả làm thay đổi bước tiếp tục.
