# Tự tạo SQL Server database và mock data đầy đủ

## Tự kiểm SQL mỗi lần chạy web

Từ thư mục dự án, chạy `start_server.cmd` hoặc bấm đúp file đó. Script `scripts/start_server.ps1` tự chuẩn bị môi trường Python nếu thiếu rồi gọi `manage.py runserver`. Chính lệnh `runserver` cũng có bước chuẩn bị SQL: tạo database nếu thiếu → migrate → seed đầy đủ → kiểm schema/mẫu → mở web khi tất cả đạt. Vì vậy chạy trực tiếp `.\.venv\Scripts\python.exe manage.py runserver` cũng được kiểm như nhau.

Mặc định lấy SQL từ `.env`, web ở `127.0.0.1:8000`. Có thể chạy `start_server.cmd -Server '.\SQLEXPRESS' -Database 'DT05_Demo' -Address '127.0.0.1:8001'`; tham số SQL được lưu vào `.env`. `-InstallDependencies` cài lại requirements khi cần, `-NoReload` tắt autoreload. Bước SQL chạy trước khi web nhận request và không lặp theo mỗi lần Django tải lại code.

Nếu mất kết nối, thiếu quyền, migration lỗi hoặc dữ liệu cùng khóa đã bị sửa khác bộ mẫu, server không mở; sửa lỗi được báo rồi chạy lại. Dữ liệu mẫu còn thiếu sẽ được bổ sung, dữ liệu đúng không tạo trùng. Đây là kiểm bộ mẫu demo; các hàng mẫu đã sửa để thử nghiệp vụ sẽ báo xung đột thay vì bị tự ghi đè.

## Cách 1 — Chạy một file SQL trong SSMS

Mở [auto_import.sql](auto_import.sql) trong SSMS, kết nối đúng instance của máy. Sửa biến đầu file nếu muốn tên database khác:

```sql
DECLARE @Database sysname=N'DT05_Demo';
```

Chạy **toàn bộ file bằng F5**, không cần bật SQLCMD Mode. File không cần Python để chạy trong SSMS. Tài khoản SQL/Windows cần quyền tạo database nếu chưa có và quyền tạo bảng/ghi dữ liệu trong database được chọn.

File tự tạo database nếu thiếu, tạo schema cuối của migration (gồm bảng Django và 13 bảng `lichca_`), FK/CHECK/UNIQUE/index, lịch sử migration, content types/quyền Django và bộ mẫu mở rộng. Với database đã có, script kiểm phiên bản migration và cấu trúc trước khi nạp. Database thiếu migration cần chạy cách 2 trước; database có cấu trúc khác hoặc dữ liệu mẫu khác cùng khóa sẽ bị chặn, không xóa để làm lại.

Script kiểm các khóa mẫu và số dòng, thêm hàng mẫu còn thiếu, giữ nguyên hàng đúng và dữ liệu khác ngoài bộ mẫu. Khi lỗi, rollback toàn bộ phần tạo schema/nạp mẫu của lần chạy. Database mới rỗng vẫn có thể còn lại sau lỗi. Schema và mẫu ghi trong một transaction; phần nạp dùng khóa `ScheduleGate(id=1)` cùng thiết kế ứng dụng. Kết quả thành công có `DATA READY` và bảng đếm `OK`.

Sau khi chạy SQL trực tiếp, điền `.env` theo đúng server/database của máy nếu muốn mở ứng dụng Django. File SQL không thay `.env` và không tạo SQL Server login.

## Cách 2 — Tự cài môi trường, migrate, seed và kiểm dữ liệu

Máy cần SQL Server, Python 3.13, Microsoft ODBC Driver 17/18. Mở PowerShell tại thư mục có `manage.py`. Thay Server name theo SSMS:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -Server '.\SQLEXPRESS' -Database 'DT05_Demo'
```

Nếu máy đã có `.env` đúng, chỉ cần:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1
```

Script tự tạo `.venv` nếu thiếu, cài requirements, nhận driver, tạo khóa ứng dụng local, tạo database, migrate, nạp đầy đủ và chạy `check_demo_data`. Thông số kết nối được lưu vào `.env` của máy chạy; file này không đưa lên Git. Mặc định Windows Authentication. Với SQL Authentication, cấu hình `DT05_SQL_USER`/`DT05_SQL_PASSWORD` trong `.env` theo [.env.example](../.env.example).

Lần đầu không cần tạo tài khoản trước: script tự tạo các tài khoản hư cấu không có mật khẩu đăng nhập. Nếu mở rộng bộ mẫu nhỏ đã nạp, script tự dùng lại người xác minh của `NV01-GIAY_BEP` để giữ dấu vết cũ. Có thể chỉ định người xác minh local bằng `-Manager TEN_DANG_NHAP_LOCAL`; tài khoản đó phải tồn tại và hoạt động. Chạy các lần sau với cùng người xác minh.

Nếu dependencies đã cài, bỏ qua bước cài bằng lệnh:

```powershell
.\.venv\Scripts\python.exe scripts\setup_database.py --database DT05_Demo
```

Chỉ tạo cấu trúc, không seed: thêm `-SkipSeed` vào PowerShell hoặc `--no-seed-demo` vào Python. Tùy chọn `-BasicDemo`/`--basic-demo` giữ luồng bộ mẫu nhỏ cũ (2 chi nhánh, 5 nhân viên, 4 ca); luồng này vẫn cần tài khoản local qua `-Manager` hoặc tạo tương tác. `-SeedDemo` được giữ để tương thích; bộ mẫu đầy đủ đã là mặc định.

## Số bản ghi ở database mới

| Bảng | Số dòng mẫu |
|---|---:|
| auth_user | 15 (5 quản lý, 10 nhân viên) |
| lichca_branch | 5 |
| lichca_position | 5 |
| lichca_managerbranch | 5 |
| lichca_employee | 10 |
| lichca_employeebranch | 15 |
| lichca_evidencetype | 5 |
| lichca_positionrequirement | 11 |
| lichca_evidence | 39 |
| lichca_sundaybaseline | 520 |
| lichca_shift | 15 |
| lichca_assignment | 11 |
| lichca_swaprequest | 5 |
| lichca_schedulegate | **1** |

12 bảng nghiệp vụ có ít nhất 5 dòng. `ScheduleGate` bắt buộc chỉ có **một dòng id=1**, theo CHECK và thiết kế khóa. Bảng kỹ thuật Django như session, log quản trị, group và các bảng nối quyền chỉ có dữ liệu khi chức năng tương ứng được sử dụng; không tạo giả phiên đăng nhập hoặc lịch sử quản trị để đủ 5 dòng. Metadata content type/quyền/migration được tạo đầy đủ. Nếu dùng tài khoản local có sẵn, tổng tài khoản thực tế có thể khác 15.

## Dữ liệu phục vụ yêu cầu đề tài

Nguồn là [bộ nhỏ gốc](../HO_SO_DT05/du_lieu_mau.json) và [phần mở rộng](../HO_SO_DT05/du_lieu_mau_mo_rong.json), đều hư cấu. Phần mở rộng không sửa ý nghĩa CA01–CA04 và NV01–NV05.

| Yêu cầu / ca thử | Dữ liệu đã chuẩn bị |
|---|---|
| YC01, YC02, CL01 / T08, T11 | Quản lý `quanly01`–`quanly05` có phạm vi CN01–CN05; `demo_nv01`–`demo_nv10` gắn đúng hồ sơ; NV01 làm được CN01/CN02; NV10 ngừng hoạt động. |
| YC03, YC04 / T02, T03 | Giấy NV02 hết 22/11/2026; NV03 thiếu IFSG_NHAC; BEP vẫn yêu cầu đúng 3 loại ban đầu. Có thêm mẫu an toàn lao động/PCCC và 4 vị trí. Các danh mục bổ sung là giả định demo, chưa phải quy tắc đã duyệt. |
| YC05–YC07, YC09 / T01, T04–T06, T12, T13 | CA01 nháp trống 0/2, CA02 trùng giờ ở CN02, CA03 công bố có NV04. Có ca đêm CA_MAU_DEM 22:00–06:00, nghỉ 23:45–00:15 tại CN04, đang nháp và chưa phân người. Các ngưỡng giờ/nghỉ vẫn thử bằng bước chuẩn bị ở T05/T06. |
| YC08 / T07 | Đủ 52 Chủ nhật năm 2026 cho mỗi nhân viên. NV01 giữ đúng 37 ngày làm ngoài/15 ngày nghỉ để thử CA04 làm giảm quỹ xuống 14. |
| YC10, YC11, CL03 / T09, T10, T15 | 10 ca công bố bổ sung tại CN03 và 10 phân công; 5 đơn gồm 2 chờ, 1 đã duyệt, 2 từ chối. Đơn đã duyệt có hai chủ sở hữu hiện tại đã đảo và giữ người gốc; đơn từ chối có lý do/người/thời điểm. |
| CL02, CL04 / T14 | Nạp và kiểm dưới khóa chung, chạy lại không tạo trùng, lỗi rollback. T14 cho dịch vụ phân ca/duyệt đồng thời vẫn cần kiểm khi triển khai các dịch vụ đó. |

Ngày mẫu cố định trong tháng 11–12/2026. Dùng ngày mô phỏng 20/11/2026 cho các kịch bản T, hoặc đồng bộ lại toàn bộ ngày khi chuyển kỳ. `DATA READY` xác nhận schema/mẫu có đủ, **không xác nhận ứng dụng đã hoàn thành YC01–YC11**. Hiện các view/form/dịch vụ nghiệp vụ vẫn cần được xây theo thiết kế và nghiệm thu T01–T15.

## Tài khoản và kiểm tra lại

Tài khoản mẫu không phải superuser và không có mật khẩu mặc định. Để dùng thử vai trò sau khi có giao diện, tự đặt mật khẩu local:

```powershell
.\.venv\Scripts\python.exe manage.py changepassword quanly01
.\.venv\Scripts\python.exe manage.py changepassword demo_nv01
```

Tạo tài khoản quản trị kỹ thuật riêng bằng `manage.py createsuperuser` khi cần vào `/admin/`. Script không đổi mật khẩu/quyền của tài khoản local được truyền qua `-Manager`. Nhân viên của bộ nhỏ chưa có tài khoản sẽ được gắn với tài khoản mẫu khi mở rộng; hồ sơ đã gắn tài khoản khác sẽ báo xung đột.

Kiểm tra schema/mẫu mà không ghi dữ liệu:

```powershell
.\.venv\Scripts\python.exe manage.py check_demo_data
```

Lệnh kiểm migration, cột, khóa/chỉ mục, FK/CHECK còn hiệu lực, từng khóa và giá trị mẫu, liên kết tài khoản và số dòng. Vì kiểm ảnh chụp mẫu, sửa nghiệp vụ trên các hàng mẫu có thể làm lệnh báo khác biệt; không tự ghi đè để vượt kiểm tra.

Khi đổi models/migration/bộ JSON, sinh lại file SQL rồi chạy kiểm thử:

```powershell
.\.venv\Scripts\python.exe manage.py export_demo_sql
.\.venv\Scripts\python.exe scripts\verify_sql_import.py
.\.venv\Scripts\python.exe manage.py test lichca --noinput
```

`verify_sql_import.py` tự tạo database tên `test_DT05_SqlImport_<mã ngẫu nhiên>`, chạy chính file SQL, thử chạy lại/bù hàng thiếu/giữ hàng riêng/xung đột rollback/khóa bị vô hiệu và đối chiếu Django, rồi xóa đúng database thử đó. Django test runner cũng dùng database `test_...` riêng. Tài khoản chạy kiểm thử cần quyền tạo/xóa database thử. Không chạy các bài thử ghi vào database đang dùng để trình diễn.
