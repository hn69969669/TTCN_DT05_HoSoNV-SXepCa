# DT05 · Hồ sơ nhân viên và xếp ca
**Hồ sơ chuẩn bị phát triển · N01 · bản 0.1 ngày 12/11/2026 · chờ xác nhận M2**

**Đích của bản đầu** là giúp quản lý trả lời hai câu hỏi trước khi công bố ca bếp: “Chi nhánh còn thiếu mấy người?” và “Người vừa chọn có thể làm ca này không?”. Nhân viên xem lịch đã công bố và theo dõi đề nghị đổi ca đến khi có kết quả.

| Dùng khi nào | Mở tài liệu nào | Kết quả cần lấy |
|---|---|---|
| Hai bạn họp chia việc | [Kế hoạch và danh sách công việc](01_KE_HOACH.md) | Biết việc nào có thể bắt đầu ngay, ai nhận, phần nào cần bàn giao cho bạn còn lại. |
| Gặp người phụ trách nghiệp vụ | [Đặc tả và quy trình](02_YEU_CAU.md) cùng [phiếu quyết định M2](05_XAC_NHAN_M2.md) | Đi qua một ca hợp lệ, một ca bị chặn và một lần đổi ca. Ghi quyết định thực tế vào phiếu. |
| Bắt đầu viết models, services và giao diện | [Thiết kế hệ thống](03_THIET_KE.md) | Hai người dùng cùng mô hình dữ liệu, cách gọi chức năng và cách hiểu trạng thái. |
| Chạy thử trước khi demo | [Kịch bản nghiệm thu](04_NGHIEM_THU.md) và [dữ liệu giả lập](du_lieu_mau.json) | Đối chiếu kết quả mong đợi với lịch thật trong ứng dụng khi đã phát triển. |
| Tiếp tục từ phiên bản khởi tạo | [Việc tiếp theo của Hiệp và Chung](06_BUOC_TIEP_THEO.md) | Đồng bộ hai máy, viết lệnh nạp mẫu, dựng màn hình và nối phân công đầu tiên. |
| Viết báo cáo quy trình nghiệp vụ | [Sơ đồ quy trình và thuyết minh](07_SO_DO_QUY_TRINH_BAO_CAO.md) | Ba sơ đồ tổng quan, phân công/công bố và đổi ca; có PNG, SVG và nguồn chỉnh sửa. |
| Viết chương phân tích và thiết kế | [Bộ sơ đồ báo cáo DT05](diagram_bao_cao/README.md) | Use Case UML, kiến trúc, ERD và sơ đồ tuần tự; có ảnh và nguồn PlantUML. |

**Căn cứ.** Nhóm chọn SQL Server. Dòng DT05 yêu cầu hồ sơ, giấy tờ, đào tạo vệ sinh, nhu cầu nhân sự theo chi nhánh, kiểm tra giờ làm, lịch cá nhân và đề nghị đổi ca. M1–M6 và người duyệt lấy theo trang Mốc. Các ngưỡng demo, cách duyệt đổi và phạm vi quản lý chi nhánh đang là phương án nhóm trình M2. [Bảng chương trình, dòng DT05](https://docs.google.com/spreadsheets/d/1NY6msgE6lJuXRuEuBP4bVPVmSU7FKnFBtdhE9q2dKEU/edit?gid=97601406#gid=97601406&range=A9:H9)

**Gói đem đi duyệt M2.** Sơ đồ nghiệp vụ và đặc tả có ở mục 2 của bộ hồ sơ, dữ liệu mẫu có trong tệp JSON, phạm vi đề xuất có ngay đầu đặc tả. Phiếu M2 cần được hoàn thiện tại cuộc trao đổi và được người hướng dẫn cùng người phụ trách nghiệp vụ xác nhận. Lịch 18 buổi và các lệnh cài hai máy nằm trong [lộ trình đã lập](../LO_TRINH_DT05.md) và [hướng dẫn buổi đầu](../BAT_DAU_DT05.md).
