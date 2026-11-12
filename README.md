# DT05 · Hồ sơ nhân viên và xếp ca

Nhóm N01 — Nguyễn Hữu Hiệp và Lê Thành Chung.

Dự án dùng Django 5.2, Python 3.13 và SQL Server qua mssql-django/pyodbc.
Khung ban đầu có trang chủ, Django Admin và ứng dụng lichca để phát triển nghiệp vụ.

## Chạy trên máy Hiệp

Mở PowerShell trong thư mục dự án. Cấu hình local đã lưu ở .env. Bấm đúp [start_server.cmd](start_server.cmd), hoặc chạy:

```powershell
.\start_server.cmd
```

Script chuẩn bị `.venv`/thư viện nếu thiếu, kiểm kết nối SQL Server, tạo database nếu thiếu, chạy migration, nạp các hàng mẫu còn thiếu và xác minh dữ liệu đầy đủ trước khi mở web. Khi SQL lỗi hoặc hàng mẫu có nội dung xung đột, script dừng và báo lý do. Không ghi đè hàng mẫu đã bị sửa.

Lệnh Django quen thuộc cũng tự kiểm SQL/migrate/seed trước khi khởi động (cần có môi trường Python sẵn):

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Việc chuẩn bị dữ liệu chỉ chạy một lần khi bật server, không chạy lại theo mỗi lần autoreload code. Để đổi instance/database/cổng từ script:

```powershell
.\start_server.cmd -Server 'localhost\HIEP' -Database 'DT05_Demo' -Address '127.0.0.1:8001'
```

Thông số SQL truyền vào được lưu trong `.env`. Thêm `-InstallDependencies` nếu vừa cập nhật requirements; `-NoReload` nếu muốn tắt autoreload. Dừng server bằng Ctrl+C. Script này dùng cho phát triển/demo local; kiểm dữ liệu trước khi nhận request, không chạy migration song song với request.

Mở http://127.0.0.1:8000/ hoặc http://127.0.0.1:8000/admin/.
Database demo local là DT05_Demo, instance localhost\HIEP, Windows Authentication và ODBC Driver 17. Bộ mẫu đầy đủ đã được nạp bằng script import; database DT05_Dev cũ được giữ riêng. Máy khác dùng thông số SQL Server trong `.env` của máy đó.

Để tạo tài khoản quản trị, chạy lệnh sau và tự nhập thông tin:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Cài trên máy Chung hoặc máy mới

Có thể dùng [script tự tạo database và nhập dữ liệu mẫu](scripts/HUONG_DAN_IMPORT.md).
Sau khi cài Python/SQL Server/ODBC, chạy tại thư mục dự án:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -Server '.\SQLEXPRESS'
```

Thay tên server theo máy nhận. Script mặc định tạo database, migrate, nạp **bộ mẫu đầy đủ** rồi tự kiểm schema/dữ liệu: 5 chi nhánh, 5 vị trí, 10 nhân viên, 15 ca, 11 phân công, 5 đơn đổi ca. Mỗi bảng nghiệp vụ có ít nhất 5 dòng; riêng ScheduleGate bắt buộc 1 dòng id=1. Tài khoản mẫu tự tạo không có mật khẩu đăng nhập; tự đặt mật khẩu local bằng `manage.py changepassword TEN_TAI_KHOAN`. Dùng `-SkipSeed` nếu chỉ tạo bảng, `-BasicDemo` nếu cần bộ nhỏ cũ. Chạy lại không tạo trùng; khác dữ liệu mẫu cùng khóa sẽ báo lỗi và rollback lần nạp. Các bước thủ công tương đương nằm bên dưới.

Cũng có thể mở [auto_import.sql](scripts/auto_import.sql) trong SSMS, sửa biến `@Database` đầu file rồi F5 toàn bộ để tạo schema và mẫu mà không cần Python. Chi tiết số dòng, tài khoản, kiểm tra `DATA READY` và phạm vi YC/T nằm trong [hướng dẫn import](scripts/HUONG_DAN_IMPORT.md).

1. Cài Python 3.13, SQL Server và ODBC Driver 17 hoặc 18.
2. Clone repo rồi mở PowerShell tại thư mục có manage.py.
3. Chạy:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

4. Điền chuỗi ngẫu nhiên vừa tạo vào DJANGO_SECRET_KEY trong .env.
   Điền DT05_SQL_HOST theo Server name đăng nhập được bằng SSMS và DT05_SQL_DRIVER theo driver đã cài.
   Hai trường user/password để trống dùng Windows Authentication.
   Với SQL Authentication, điền tài khoản database vào .env trên máy mình.
   Tệp .env được Git bỏ qua.
5. Trong SSMS, tạo database dự án:

```sql
IF DB_ID(N'DT05_Dev') IS NULL
    CREATE DATABASE DT05_Dev;
```

6. Chạy lần lượt:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py seed_demo --manager TEN_DANG_NHAP_LOCAL
.\.venv\Scripts\python.exe manage.py runserver
```

DT05_SQL_TRUST_CERTIFICATE=yes dành cho SQL Server local khi phát triển.
Khi triển khai máy chủ dùng chung, cấu hình xác thực và chứng chỉ theo môi trường đó.

## Nền tảng để phát triển

Bắt đầu từ [việc tiếp theo của Hiệp và Chung](HO_SO_DT05/06_BUOC_TIEP_THEO.md).

- [Bộ kế hoạch, yêu cầu và thiết kế](HO_SO_DT05/README.md)
- [Lộ trình 18 buổi](LO_TRINH_DT05.md)
- [Hướng dẫn làm việc và chuẩn bị M2](BAT_DAU_DT05.md)

Mỗi máy có database riêng. Chia sẻ models, migration và dữ liệu giả lập qua Git.
Thiết kế nghiệp vụ nằm trong HO_SO_DT05. Lệnh `seed_demo` đọc bộ JSON và nạp dữ liệu thử ngay khi import.
Models và migration đã có cho 12 bảng nghiệp vụ cùng bảng khóa kỹ thuật `ScheduleGate` trong lichca.
Hiện app chỉ có route trang chủ; Admin chưa đăng ký các bảng nghiệp vụ. Các màn hình và dịch vụ trong thiết kế vẫn cần triển khai.
Nhóm triển khai tiếp form, phân quyền chi nhánh và dịch vụ kiểm tra/lưu lịch theo thiết kế.
Các điều kiện liên bảng như tổng giờ làm, trùng ca và số người trong ca cần được kiểm tra trong dịch vụ ghi.

## Kiểm tra khi thay đổi code

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations lichca
.\.venv\Scripts\python.exe manage.py test lichca --noinput
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
```

Lệnh test dùng database SQL Server thử riêng do Django tạo (mặc định `test_<tên database đang cấu hình>`); tài khoản SQL cần quyền tạo/xóa database thử. Không dùng database này để lưu dữ liệu cần giữ.

Sau khi sửa models, tạo migration và chạy migrate trước khi thử luồng nghiệp vụ.
