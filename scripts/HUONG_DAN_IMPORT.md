# Tự tạo database trên máy khác

Máy nhận cần có SQL Server đang hoạt động, Python 3.13 và Microsoft ODBC Driver 17 hoặc 18. Lấy toàn bộ repo về máy rồi mở PowerShell trong thư mục dự án.

## Tạo database và các bảng

Thay tên server bằng Server name đã kết nối thành công trong SSMS. Ví dụ với SQL Express:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -Server '.\SQLEXPRESS'
```

Máy có instance tên khác dùng đúng tên đó, ví dụ localhost\HIEP. Có thể đặt tên database riêng:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -Server 'localhost\HIEP' -Database 'DT05_Dev'
```

Script tạo môi trường .venv nếu cần, cài requirements, tự nhận driver 17/18, sinh khóa ứng dụng local, tạo .env, tạo database nếu chưa có và chạy Django migration. Tên server/database truyền vào được lưu trong .env của máy nhận. Tham số ExecutionPolicy chỉ áp dụng cho lần chạy này.

Mặc định dùng Windows Authentication. Tài khoản Windows cần quyền tạo database. Nếu database đã được quản trị viên tạo, tài khoản cần quyền thực hiện migration trên database đó. Với SQL Authentication, điền DT05_SQL_USER và DT05_SQL_PASSWORD vào .env trước khi chạy. Mẫu các biến nằm trong [.env.example](../.env.example).

Nếu thư viện đã cài sẵn, có thể chỉ chạy phần tạo database:

```powershell
.\.venv\Scripts\python.exe scripts\setup_database.py --server '.\SQLEXPRESS'
```

## Nhập dữ liệu giả lập

Sau khi tạo cấu trúc, tạo tài khoản quản trị local nếu chưa có:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Chọn tên đăng nhập riêng, sau đó dùng đúng tên đó thay cho TEN_DANG_NHAP_LOCAL:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo --manager TEN_DANG_NHAP_LOCAL
```

Hoặc chạy lại script với tùy chọn nạp mẫu:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -SeedDemo -Manager TEN_DANG_NHAP_LOCAL
```

Bộ mẫu gồm 2 chi nhánh, 5 nhân viên, 4 ca, 14 minh chứng, 52 ngày Chủ nhật và một phân công. Nhân viên mẫu chưa gắn tài khoản đăng nhập. Tài khoản được chỉ định làm người xác minh hồ sơ, người công bố CA03 và quản lý CN01 của dữ liệu mẫu. Các ngày cố định dùng cho kịch bản tháng 11/2026 trong tài liệu nghiệm thu.

Chạy nạp mẫu lần hai giữ nguyên bản ghi cùng nội dung. Nếu cùng mã nhưng dữ liệu đã khác, lệnh báo xung đột và rollback phần nạp. Dữ liệu tự tạo ngoài bộ mẫu được giữ. Migration theo dõi phiên bản cấu trúc trong django_migrations và áp dụng phần còn thiếu.

## Sau khi nhập

Mở SSMS → database vừa tạo → Tables và Refresh để xem các bảng lichca_. Chạy:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Mở http://127.0.0.1:8000/. Nếu gặp lỗi kết nối, kiểm tra tên instance trong SSMS và driver đã cài. Nếu báo thiếu quyền tạo database, nhờ quản trị viên tạo database rồi chạy lại script.
