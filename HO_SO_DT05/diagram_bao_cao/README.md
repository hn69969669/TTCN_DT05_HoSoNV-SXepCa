# Bộ sơ đồ báo cáo DT05 · Hồ sơ nhân viên và xếp ca

**Nhóm N01 · Nguyễn Hữu Hiệp và Lê Thành Chung.** Mở [bản xem và in](index.html) để duyệt hình cùng chú thích. Trong Word, chèn SVG để giữ nét khi đổi kích thước, hoặc dùng PNG nền trắng. Dùng tên hình bên dưới làm caption và đánh lại số theo chương của báo cáo.

| Hình | Chú thích đề xuất | Ảnh và nguồn sửa |
|---|---|---|
| 1 | Use Case tổng quan hệ thống DT05 | [SVG](01_use_case_tong_quan.svg) · [PNG](01_use_case_tong_quan.png) · [PlantUML](01_use_case_tong_quan.puml) |
| 2 | Use Case quản lý hồ sơ, phân công và công bố ca | [SVG](02_use_case_phan_cong.svg) · [PNG](02_use_case_phan_cong.png) · [PlantUML](02_use_case_phan_cong.puml) |
| 3 | Use Case gửi và xử lý đề nghị đổi ca | [SVG](03_use_case_doi_ca.svg) · [PNG](03_use_case_doi_ca.png) · [PlantUML](03_use_case_doi_ca.puml) |
| 4 | Kiến trúc ứng dụng Django và SQL Server | [SVG](04_kien_truc.svg) · [PNG](04_kien_truc.png) · [PlantUML](04_kien_truc.puml) |
| 5 | ERD hồ sơ, quyền chi nhánh và minh chứng | [SVG](05_erd_ho_so.svg) · [PNG](05_erd_ho_so.png) · [PlantUML](05_erd_ho_so.puml) |
| 6 | ERD lịch làm việc, phân công và đơn đổi ca | [SVG](06_erd_lich.svg) · [PNG](06_erd_lich.png) · [PlantUML](06_erd_lich.puml) |
| 7 | Sơ đồ tuần tự phân công nhân viên | [SVG](07_trinh_tu_phan_cong.svg) · [PNG](07_trinh_tu_phan_cong.png) · [PlantUML](07_trinh_tu_phan_cong.puml) |
| 8 | Sơ đồ tuần tự duyệt đổi ca | [SVG](08_trinh_tu_duyet_doi.svg) · [PNG](08_trinh_tu_duyet_doi.png) · [PlantUML](08_trinh_tu_duyet_doi.puml) |

**Thứ tự đưa vào báo cáo.** Trong chương phân tích, dùng Hình 1 để giới thiệu phạm vi, Hình 2–3 để mô tả mục tiêu từng vai trò, rồi chọn [lưu đồ nghiệp vụ đã có](../07_SO_DO_QUY_TRINH_BAO_CAO.md) khi cần trình bày thứ tự thao tác. Trong chương thiết kế, dùng Hình 4 cho kiến trúc, Hình 5–6 cho dữ liệu, Hình 7–8 để giải thích giao dịch. Hai hình ERD có thể đặt trên trang A4 ngang.

**Mức độ xác minh.** Hình 5–6 đối chiếu 13 model nghiệp vụ trong [models.py](../../lichca/models.py) và bảng User của Django; ERD chỉ hiện các thuộc tính chính. Các hình khác mô tả thiết kế M2 theo [đặc tả](../02_YEU_CAU.md) và [thiết kế](../03_THIET_KE.md). [Route hiện tại](../../lichca/urls.py) của app chỉ có trang chủ. Các ví dụ là kết quả mong đợi, Q1–Q6 vẫn [chờ xác nhận](../05_XAC_NHAN_M2.md).

## Cách đọc từng hình

**Hình 1. Use Case tổng quan hệ thống DT05.** Hai vai trò nghiệp vụ là quản lý chi nhánh và nhân viên. Quản trị viên kỹ thuật tạo tài khoản, phân vai và cấu hình danh mục. Đăng nhập tạo phiên dùng cho các chức năng theo quyền.

**Hình 2. Use Case quản lý hồ sơ, phân công và công bố ca.** Quản lý chọn người cho ca nháp. Phân công và công bố cùng bao gồm kiểm tra điều kiện: khi phân công xét ứng viên; khi công bố xét lại mọi người trong ca và kiểm đủ số chỗ.

**Hình 3. Use Case gửi và xử lý đề nghị đổi ca.** Nhân viên chỉ định ca đối tác bằng mã phân công. Quản lý có thể từ chối kèm lý do; để duyệt, phải kiểm điều kiện trên lịch sau đổi của cả hai người.

**Hình 4. Kiến trúc ứng dụng Django và SQL Server.** Trình duyệt gửi yêu cầu cho Django. Truy vấn đọc giới hạn dữ liệu theo quyền; thay đổi lịch đi qua dịch vụ ghi và kiểm tra nghiệp vụ trước khi lưu bằng ORM.

**Hình 5. ERD hồ sơ, quyền chi nhánh và minh chứng.** Chi nhánh chủ quản (Employee.home_branch) khác với các nơi nhân viên được nhận ca (EmployeeBranch). Một loại minh chứng có thể bắt buộc ở nhiều vị trí. Tài khoản của nhân viên là tùy chọn và duy nhất khi đã liên kết.

**Hình 6. ERD lịch làm việc, phân công và đơn đổi ca.** Assignment đại diện cho một chỗ trong ca. Đơn đổi tham chiếu hai chỗ, hai nhân viên gốc, người tạo và người quyết định. ScheduleGate có một hàng id=1 và không có khóa ngoại.

**Hình 7. Sơ đồ tuần tự phân công nhân viên.** Ví dụ dự kiến: chọn NV02 vào CA01 bị chặn vì giấy bếp hết hạn ngày 22/11/2026; ca vẫn 0/2. Với NV01 đủ điều kiện, số đã xếp thành 1/2 sau khi ghi thành công.

**Hình 8. Sơ đồ tuần tự duyệt đổi ca.** Duyệt lặp trả quyết định đã lưu. Đơn lỗi thời hoặc lịch không đạt vẫn chờ; lỗi khi ghi phải hoàn tác cả hai phân công và quyết định. Nhánh quản lý chủ động từ chối được trình bày ở Use Case đổi ca và lưu đồ nghiệp vụ.

Ở hai ERD, chân quạ chỉ phía nhiều; vòng tròn chỉ tùy chọn. PK là khóa chính, FK là khóa ngoại, UK là khóa duy nhất. Các cặp khóa duy nhất quan trọng gồm EmployeeBranch(employee, branch), PositionRequirement(position, evidence_type), Assignment(shift, employee), SundayBaseline(employee, sunday_date) và ManagerBranch(user, branch). Trên Hình 6, decided_by_id và published_by_id cho phép NULL trước khi có quyết định hoặc công bố.

## Tác nhân và quan hệ trong ba hình Use Case

| Actor | Use case | Quan hệ |
|---|---|---|
| Cả ba tác nhân | Đăng nhập hệ thống | Association |
| Quản lý chi nhánh | Quản lý hồ sơ nhân viên; xếp ca làm việc; xử lý đề nghị đổi ca | Association (tổng quan) |
| Quản lý chi nhánh | Cập nhật hồ sơ; cập nhật giấy tờ và đào tạo; xem lịch chi nhánh; tạo ca; phân công; bỏ phân công; công bố ca | Association (chi tiết) |
| Quản lý chi nhánh | Xem, duyệt hoặc từ chối đề nghị đổi ca | Association |
| Nhân viên | Xem lịch cá nhân; gửi đề nghị đổi ca; xem kết quả đổi ca | Association |
| Quản trị viên kỹ thuật | Tạo tài khoản; phân vai tài khoản; cấu hình danh mục | Association |
| — | Phân công nhân viên, Công bố ca làm việc và Duyệt đề nghị đổi ca → Kiểm tra điều kiện phân công | «include» |

Các hình là những góc nhìn của cùng một hệ thống: Hình 2–3 chi tiết hóa phạm vi Hình 1, không biểu diễn thứ tự thực hiện. Actor ngoài khung, liên kết actor không có mũi tên. Chỉ chức năng kiểm tra dùng chung được nối bằng phụ thuộc nét đứt. Không có quan hệ kế thừa hay mở rộng trong phạm vi này.

**Sửa và xuất lại.** Mỗi tệp .puml là một sơ đồ PlantUML độc lập, mã hóa UTF-8. Sau khi sửa, dùng PlantUML với tùy chọn `-charset UTF-8 -tsvg` để tạo SVG; với PNG độ phân giải cao dùng `-charset UTF-8 -tpng -Sdpi=216`. Trang xem dùng ảnh SVG cùng tên nên tự nhận bản mới.
