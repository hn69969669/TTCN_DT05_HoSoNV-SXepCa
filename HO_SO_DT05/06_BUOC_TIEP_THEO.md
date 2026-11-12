# Việc tiếp theo sau phiên bản khởi tạo

**Kết quả cần đạt ở bước kế tiếp** là hai máy chạy được cùng phiên bản, có cùng bộ dữ liệu thử và quản lý mở được CA01 để xem hồ sơ của người dự kiến nhận ca. Sau đó nhóm nối thao tác chọn NV02 → nhận lý do giấy hết hạn → chọn NV01 → lưu được phân công đầu tiên.

Phiên bản hiện tại đã có Django, SQL Server, 12 models nghiệp vụ cùng model khóa kỹ thuật `ScheduleGate`, migration và lệnh seed_demo. Database trên máy Hiệp có một tài khoản quản trị. Hiệp kiểm tra lệnh nạp trên hai máy. Chung tiếp tục phần đăng ký bảng nghiệp vụ trong Admin, màn hình nhân sự và dịch vụ phân ca cùng Hiệp. Trạng thái này được ghi ngày 12/11/2026.

## 1. Đồng bộ hai máy trước khi chia code

**Chung** làm theo mục cài máy mới trong [README](../README.md). Nếu đã clone, chạy git status trước. Khi thư mục sạch, dùng git pull --ff-only. Nếu đang có thay đổi, lưu thay đổi vào nhánh riêng rồi mới đồng bộ main.

| Kiểm tra | Hiệp | Chung | Dấu hiệu hoàn thành |
|---|---|---|---|
| Phiên bản code | Gửi mã commit đang dùng | Lấy đúng commit đó | git rev-parse HEAD trả cùng mã |
| Môi trường | Đã có .env local và SQL Server HIEP | Điền .env theo SQL Server máy Chung, cài requirements | pip check đạt trên mỗi máy |
| Database | Đối chiếu migration | Tạo DT05_Dev và chạy migrate | Có 13 bảng lichca_ và một dòng lichca_schedulegate id=1 |
| Tài khoản | Kiểm tra đăng nhập Admin với tài khoản đã có | Tạo quản trị local bằng createsuperuser | Mỗi bạn tự đăng nhập được trên máy mình |
| Ứng dụng | Chạy runserver | Chạy runserver | Trang chủ và trang đăng nhập quản trị mở được |

Tại thư mục có manage.py, hai người chạy:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations lichca
.\.venv\Scripts\python.exe manage.py runserver
```

Dừng máy chủ bằng Ctrl+C sau khi thử. Ghi commit, kết quả và lỗi còn mở vào nhật ký. Máy Hiệp đã được kiểm tra kết nối và migration. Việc Chung chạy thành công cần được xác nhận trên chính máy của Chung.

## 2. Chốt phần đã rõ và gửi các câu còn mở của M2

**Cả hai** dùng [phiếu xác nhận M2](05_XAC_NHAN_M2.md) trong cuộc gặp. Hiệp chuẩn bị dữ liệu và hai kết quả dự kiến, Chung ghi phản hồi. Hoàn thiện tên người hướng dẫn, phụ trách nghiệp vụ, ngày trao đổi và phiên bản đã gửi.

Các phần có thể triển khai trước gồm danh mục, nhập hồ sơ, hiển thị dữ liệu và form ca theo cấu trúc hiện có. Đối với ngưỡng giờ, Chủ nhật, công bố và đổi ca, lưu quyết định Q1–Q6 cạnh mã yêu cầu chịu ảnh hưởng. Nếu chưa nhận phản hồi, ghi rõ quy tắc demo đang áp dụng khi trình diễn.

## 3. Hiệp kiểm tra lệnh nạp bộ mẫu

Lệnh đã có trong lichca/management/commands/seed_demo.py, đọc [du_lieu_mau.json](du_lieu_mau.json). Script [import trên máy mới](../scripts/HUONG_DAN_IMPORT.md) đã tự nạp mẫu. Để kiểm khả năng chạy lặp, dùng lại đúng tài khoản của lần import:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo --manager TEN_DANG_NHAP_LOCAL
```

Tham số manager trỏ đến tài khoản đang có trên máy. Lệnh phải tìm đúng tài khoản đó trước khi ghi dữ liệu. Ánh xạ các trường verified_by và published_by trong bộ mẫu vào tài khoản được chỉ định. Tạo quan hệ ManagerBranch cho CN01 của tài khoản này để thử vai trò quản lý.

| Thứ tự | Việc lệnh nạp phải làm |
|---|---|
| 1 | Đọc và kiểm cấu trúc JSON, mã trùng, khóa tham chiếu, ngày giờ và các trường bắt buộc. Báo lỗi kèm mã bản ghi khi dữ liệu sai. |
| 2 | Tạo Branch CN01/CN02 và Position BEP. Tên hiển thị có thể lấy “Chi nhánh mẫu 1”, “Chi nhánh mẫu 2”, “Bếp” trong lệnh. |
| 3 | Tạo 5 Employee cùng quan hệ EmployeeBranch. Trường user để trống ở giai đoạn này, sau đó nhóm gắn tài khoản nhân viên khi làm lịch cá nhân. |
| 4 | Tạo EvidenceType, PositionRequirement và 14 Evidence. Dùng reference ổn định trong bộ mẫu để tìm lại minh chứng đã nạp. |
| 5 | Tạo 52 SundayBaseline cho NV01. CA04 là Chủ nhật cần kiểm quỹ ngày nghỉ. |
| 6 | Tạo 4 Shift và một Assignment CA03–NV04. Đây là ảnh chụp dữ liệu mẫu có CA03 đã công bố, cần giữ đủ thông tin người và thời điểm công bố. |
| 7 | Thực hiện việc ghi trong transaction.atomic(). Nếu có lỗi, rollback toàn bộ lần nạp. In số tạo mới/đã có và mã bản ghi khác dữ liệu nguồn để người chạy biết cách xử lý. |

**Chạy lại an toàn.** Dùng code cho danh mục/nhân viên/ca, reference cho minh chứng, public_code cho phân công, cặp nhân viên-ngày cho lịch nền và cặp FK cho các bảng nối. Nếu bản ghi đã có cùng nội dung, giữ nguyên. Nếu có cùng khóa nhưng dữ liệu khác, báo khác biệt và dừng cả lần nạp để hai bạn quyết định. Giữ riêng những bản ghi do người dùng tạo ngoài bộ mẫu.

**Chung kiểm tra độc lập.** Chạy migrate rồi seed_demo trên máy mình. Đối chiếu được 2 chi nhánh, 1 vị trí, 5 nhân viên, 3 loại minh chứng, 3 yêu cầu theo vị trí, 14 minh chứng, 52 hàng Chủ nhật, 4 ca và 1 phân công. Chạy seed_demo lần hai, số bản ghi giữ nguyên. Cố tình đổi một tham chiếu trong bản JSON dùng riêng để thử, bảo đảm lỗi chỉ rõ bản ghi và database giữ nguyên.

## 4. Chung dựng màn hình đọc dữ liệu

Trong lúc Hiệp kiểm tra lệnh nạp hiện có, **Chung** làm ba việc theo thứ tự.

1. Đăng ký các bảng nghiệp vụ ở lichca/admin.py với chế độ chỉ xem để hai bạn đối chiếu dữ liệu nạp. Hiện các cột mã, tên, ngày hiệu lực và trạng thái, có ô tìm mã nhân viên và mã ca. Các thao tác sửa lịch sẽ đi qua dịch vụ được thiết kế ở bước 5.
2. Tạo trang /nhan-su/ và /nhan-su/{id}/ để quản lý xem nhân viên, nơi được làm và minh chứng. Dùng quan hệ ManagerBranch, home_branch và EmployeeBranch đúng phạm vi trong thiết kế. Kiểm quyền ở máy chủ khi người dùng thay ID trên đường dẫn.
3. Tạo trang /ca/{id}/ hiển thị CA01 gồm chi nhánh, vị trí, ngày/giờ, khoảng nghỉ, trạng thái và số người đã xếp/cần. Màn hình mở ra ở mức 0/2 trên dữ liệu gốc. Chuẩn bị form chọn nhân viên nhưng chỉ báo lưu thành công khi bước 5 đã thực sự ghi được xuống database.

**Tệp dự kiến chỉnh** gồm lichca/admin.py, urls.py, views.py và các template nhân sự/chi tiết ca. Đưa truy vấn chọn dữ liệu theo quyền vào một chỗ rõ ràng để trang danh sách và chi tiết dùng cùng cách lọc. Quyền superuser local chỉ dùng để kiểm tra kỹ thuật. Khi thử phạm vi CN01/CN02, dùng các tài khoản quản lý có quan hệ chi nhánh tương ứng.

**Cách biết đã xong.** Mở NV02 và thấy GIAY_BEP hết hạn 22/11/2026, mở NV03 và nhận ra còn thiếu IFSG_NHAC, mở CA01 và thấy nhu cầu hai người. Một quản lý CN02 không thể mở hồ sơ chi tiết thuộc CN01 bằng cách đổi URL.

## 5. Hai bạn cùng hoàn thành phân công đầu tiên

**Hiệp** tạo lichca/services.py. Chung gọi các hàm đó từ form POST. Hợp đồng chi tiết có trong [thiết kế](03_THIET_KE.md). Trước tiên hoàn thành đúng ví dụ CA01, sau đó bổ sung từng quy tắc còn lại.

| Bước | Hiệp thực hiện | Chung thực hiện | Kết quả để kiểm tra |
|---|---|---|---|
| A | Viết evaluate_assignment trả OK/BLOCKED/NEED_DATA cùng mã và lý do. Thử điều kiện giấy tờ đầu tiên. | Hiện thông báo trả về cạnh ô chọn người. | Chọn NV02 vào CA01 thấy ngày hết hạn 22/11, số phân công vẫn là 0. |
| B | Viết assign_employee dùng giao dịch, khóa ScheduleGate và đọc lại dữ liệu trước khi ghi. Kiểm quyền, ca nháp, nhân viên hoạt động, nơi được làm, giấy tờ và sức chứa. | Nối form POST có CSRF, sau thành công quay lại chi tiết ca và đọc dữ liệu mới. | Chọn NV01, tải lại vẫn thấy đúng một phân công và 1/2. |
| C | Bổ sung trùng giờ, nghỉ trước/sau, tổng giờ và Chủ nhật theo Q1–Q3. | Hiện số giờ/ngưỡng hoặc mục dữ liệu cần bổ sung, giới hạn thông tin liên chi nhánh. | Các T04–T07 có kết quả như phạm vi đã duyệt. |
| D | Kiểm công bố toàn ca và lưu người/thời điểm. | Nối nút công bố và lịch của nhân viên đăng nhập. | CA01 chỉ xuất hiện trong lịch cá nhân sau khi đủ điều kiện công bố. |

Khi chạy bước A/B, nhóm trình bày rõ các quy tắc đang phát triển. Mở công bố sau khi các điều kiện của phạm vi M3 đã chạy đầy đủ phía máy chủ. Dùng [bộ nghiệm thu](04_NGHIEM_THU.md) để ghi kết quả thực tế thay vì suy ra từ thông báo giao diện.

## 6. Chia nhánh và bàn giao

Hiệp dùng nhánh `codex/kiem-tra-du-lieu-mau`, Chung dùng `codex/nhan-su-va-ca` từ cùng main. Mỗi thay đổi ghi file đã sửa, cách chạy thử và kết quả. Khi nhánh làm xong một phần có thể thử, đưa lên repo để bạn còn lại kiểm tra trước khi gộp vào main.

Ví dụ với nhánh của Hiệp:

```powershell
git switch main
git pull --ff-only
git switch -c codex/kiem-tra-du-lieu-mau
```

Trước khi bàn giao phần code:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
git status --short
```

Với phần models thay đổi, tạo migration rồi thử migrate trên SQL Server trước khi bàn giao. Phần phân ca cần được thử bằng dữ liệu thật trong database local và thử trường hợp thất bại. Các lệnh kiểm cấu hình phía trên chỉ là một phần của việc kiểm tra.

## 7. Kết quả nhóm gửi lại sau bước này

- Mã commit hai máy đang dùng và xác nhận Chung đã chạy ứng dụng.
- Kết quả nạp lần một/lần hai cùng số bản ghi.
- Kết quả ba thao tác xem NV02, xem CA01 và lưu NV01.
- Phiếu Q1–Q6 đã ghi ý kiến thật hoặc còn mục nào đang chờ, ai trả lời và ngày cần phản hồi.

Khi hoàn thành các mục trên, nhóm có dữ liệu và luồng phân công đầu tiên để phát triển tiếp kiểm tra đầy đủ, công bố lịch và đổi ca theo mốc M3/M4.
