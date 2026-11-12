# DT05 · Hồ sơ nhân viên và xếp ca

Nhóm N01 — Nguyễn Hữu Hiệp và Lê Thành Chung.

Dự án dùng Django 5.2, Python 3.13 và SQL Server qua mssql-django/pyodbc.
Khung ban đầu có trang chủ, Django Admin và ứng dụng lichca để phát triển nghiệp vụ.

## Chạy trên máy Hiệp

Mở PowerShell trong thư mục dự án. Cấu hình local đã lưu ở .env.

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Mở http://127.0.0.1:8000/ hoặc http://127.0.0.1:8000/admin/.
Database local là DT05_Dev, instance localhost\HIEP, Windows Authentication và ODBC Driver 17.

Để tạo tài khoản quản trị, chạy lệnh sau và tự nhập thông tin:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Cài trên máy Chung hoặc máy mới

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
.\.venv\Scripts\python.exe manage.py runserver
```

DT05_SQL_TRUST_CERTIFICATE=yes dành cho SQL Server local khi phát triển.
Khi triển khai máy chủ dùng chung, cấu hình xác thực và chứng chỉ theo môi trường đó.

## Nền tảng để phát triển

- [Bộ kế hoạch, yêu cầu và thiết kế](HO_SO_DT05/README.md)
- [Lộ trình 18 buổi](LO_TRINH_DT05.md)
- [Hướng dẫn làm việc và chuẩn bị M2](BAT_DAU_DT05.md)

Mỗi máy có database riêng. Chia sẻ models, migration và dữ liệu giả lập qua Git.
Thiết kế nghiệp vụ nằm trong HO_SO_DT05. Bộ dữ liệu JSON phục vụ bước phát triển tiếp theo.
Models và migration đã có cho 13 bảng nghiệp vụ trong lichca.
Nhóm triển khai tiếp form, phân quyền chi nhánh và dịch vụ kiểm tra/lưu lịch theo thiết kế.
Các điều kiện liên bảng như tổng giờ làm, trùng ca và số người trong ca cần được kiểm tra trong dịch vụ ghi.

## Kiểm tra khi thay đổi code

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
```

Sau khi sửa models, tạo migration và chạy migrate trước khi thử luồng nghiệp vụ.
