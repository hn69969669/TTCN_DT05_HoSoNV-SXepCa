# Bộ sơ đồ báo cáo DT05

**Nhóm N01 · Nguyễn Hữu Hiệp và Lê Thành Chung.** Đây là bộ 13 sơ đồ chính dùng cho báo cáo. Mở [bản xem và in](index.html) để xem hình cùng chú thích. Đọc [quy ước đối chiếu](QUY_UOC_SO_DO.md) trước khi sửa tên trường, trạng thái hoặc luồng nghiệp vụ.

| Hình | Chú thích đề xuất | Ảnh và nguồn sửa |
|---|---|---|
| 1 | Use Case tổng quan hệ thống DT05 | [SVG](01_use_case_tong_quan.svg) · [PNG](01_use_case_tong_quan.png) · [PlantUML](01_use_case_tong_quan.puml) |
| 2 | Use Case hồ sơ, phân công và công bố ca | [SVG](02_use_case_phan_cong.svg) · [PNG](02_use_case_phan_cong.png) · [PlantUML](02_use_case_phan_cong.puml) |
| 3 | Use Case gửi và xử lý đề nghị đổi ca | [SVG](03_use_case_doi_ca.svg) · [PNG](03_use_case_doi_ca.png) · [PlantUML](03_use_case_doi_ca.puml) |
| 4 | Kiến trúc ứng dụng Django và SQL Server | [SVG](04_kien_truc.svg) · [PNG](04_kien_truc.png) · [PlantUML](04_kien_truc.puml) |
| 5 | ERD hồ sơ, quyền chi nhánh và minh chứng | [SVG](05_erd_ho_so.svg) · [PNG](05_erd_ho_so.png) · [PlantUML](05_erd_ho_so.puml) |
| 6 | ERD lịch làm việc, phân công và đơn đổi ca | [SVG](06_erd_lich.svg) · [PNG](06_erd_lich.png) · [PlantUML](06_erd_lich.puml) |
| 7 | Sơ đồ tuần tự phân công nhân viên | [SVG](07_trinh_tu_phan_cong.svg) · [PNG](07_trinh_tu_phan_cong.png) · [PlantUML](07_trinh_tu_phan_cong.puml) |
| 8 | Sơ đồ tuần tự xử lý đề nghị đổi ca | [SVG](08_trinh_tu_duyet_doi.svg) · [PNG](08_trinh_tu_duyet_doi.png) · [PlantUML](08_trinh_tu_duyet_doi.puml) |
| 9 | Sơ đồ tuần tự gửi đề nghị đổi ca | [SVG](09_trinh_tu_de_nghi_doi_ca.svg) · [PNG](09_trinh_tu_de_nghi_doi_ca.png) · [PlantUML](09_trinh_tu_de_nghi_doi_ca.puml) |
| 10 | Sơ đồ hoạt động đánh giá điều kiện phân công | [SVG](10_hoat_dong_kiem_tra_quy_dinh.svg) · [PNG](10_hoat_dong_kiem_tra_quy_dinh.png) · [PlantUML](10_hoat_dong_kiem_tra_quy_dinh.puml) |
| 11 | Sơ đồ trạng thái ca làm việc | [SVG](11_trang_thai_ca.svg) · [PNG](11_trang_thai_ca.png) · [PlantUML](11_trang_thai_ca.puml) |
| 12 | Sơ đồ trạng thái đề nghị đổi ca | [SVG](12_trang_thai_don_doi_ca.svg) · [PNG](12_trang_thai_don_doi_ca.png) · [PlantUML](12_trang_thai_don_doi_ca.puml) |
| 13 | Sơ đồ hoạt động tổng thể theo vai trò | [SVG](13_hoat_dong_quy_trinh_tong_the.svg) · [PNG](13_hoat_dong_quy_trinh_tong_the.png) · [PlantUML](13_hoat_dong_quy_trinh_tong_the.puml) |

## Đưa hình vào báo cáo

- Chương phân tích: Hình 1–3 mô tả mục tiêu của các vai trò; Hình 13 thể hiện hoạt động giữa quản lý, hệ thống và nhân viên.
- Chương thiết kế: Hình 4 là kiến trúc; Hình 5–6 là ERD; Hình 7–9 là tuần tự; Hình 10 diễn giải việc đánh giá điều kiện; Hình 11–12 mô tả trạng thái.
- Chọn các hình phù hợp nội dung báo cáo, không cần đặt lại cùng một quy trình bằng nhiều kiểu sơ đồ cạnh nhau. [Ba lưu đồ trước đây](../07_SO_DO_QUY_TRINH_BAO_CAO.md) có thể dùng cho phần giới thiệu nghiệp vụ, còn Hình 13 dùng khi cần làn trách nhiệm.
- Trong Word, chèn SVG để giữ nét, hoặc PNG nền trắng đã xuất ở mật độ 216 DPI. Giữ tỷ lệ, căn giữa và đánh lại số hình theo chương. ERD và sơ đồ tuần tự thường phù hợp trang ngang; hình dọc dùng trang dọc. Chú thích đề xuất có ở bảng trên.

## Phạm vi và căn cứ

Hai ERD đối chiếu [models.py](../../lichca/models.py): 12 model nghiệp vụ chính được thể hiện trong Hình 5–6 cùng User của Django. Model thứ 13 là `ScheduleGate`, một bảng khóa kỹ thuật với một hàng `id=1` và không có FK, được giải thích tại Hình 4 thay vì đặt lẻ trong ERD nghiệp vụ. Tên trường, NULL, UK và trạng thái phải khớp code; các thuộc tính Django User không liên quan được lược bớt.

Các hình chức năng và tương tác theo [YC01–YC11](../02_YEU_CAU.md), [thiết kế](../03_THIET_KE.md) và [kịch bản T01–T15](../04_NGHIEM_THU.md). [Route hiện tại](../../lichca/urls.py) của app chỉ khai báo trang chủ; các hình này là thiết kế, không khẳng định dịch vụ đã chạy. Q1–Q6 và các ngưỡng demo vẫn [chờ xác nhận nghiệp vụ](../05_XAC_NHAN_M2.md).

## Cách đọc từng hình

**Hình 1. Use Case tổng quan hệ thống DT05.** Khai báo nhu cầu ca và xem lịch chi nhánh được thể hiện rõ. Ba vai trò đăng nhập để sử dụng các chức năng trong phạm vi của mình.

Đối chiếu: YC01–YC11.

**Hình 2. Use Case hồ sơ, phân công và công bố ca.** Quản lý ghi nhận minh chứng đã xác minh và sửa ca nháp. Phân công và công bố dùng chung việc kiểm tra điều kiện; khi sửa ca có người phải kiểm lại các phân công.

Đối chiếu: YC02–YC09.

**Hình 3. Use Case gửi và xử lý đề nghị đổi ca.** Một nhân viên gửi mã phân công; quản lý duyệt hoặc từ chối. Khi duyệt, hệ thống kiểm lịch sau đổi của cả hai người.

Đối chiếu: YC10–YC11.

**Hình 4. Kiến trúc ứng dụng Django và SQL Server.** Dữ liệu đi qua truy vấn theo quyền hoặc dịch vụ ghi. Khóa ScheduleGate(id=1) tuần tự hóa các thao tác ảnh hưởng lịch; Templates trả HTML cho trình duyệt.

Đối chiếu: CL01–CL03.

**Hình 5. ERD hồ sơ, quyền chi nhánh và minh chứng.** Tên trường và khóa bám models.py. Evidence.verified_by không cho phép NULL; Employee.user là liên kết tùy chọn và duy nhất khi khác NULL. EmployeeBranch chứa cả chi nhánh chính.

Đối chiếu: Models hiện hành.

**Hình 6. ERD lịch làm việc, phân công và đơn đổi ca.** Ca lưu giờ bắt đầu/kết thúc và hai đầu khoảng nghỉ. Đơn lưu chủ gốc và lịch sử quyết định. ScheduleGate là bảng kỹ thuật được thể hiện ở Hình 4.

Đối chiếu: Models hiện hành.

**Hình 7. Sơ đồ tuần tự phân công nhân viên.** Đọc lại điều kiện sau khi khóa chung. Thêm Assignment khi hợp lệ; nếu lỗi ghi thì rollback. Chỉ trả thành công sau commit, rồi đọc lại số người trên trang chi tiết.

Đối chiếu: YC06–YC08 · T01–T07, T11–T14.

**Hình 8. Sơ đồ tuần tự xử lý đề nghị đổi ca.** Bổ sung nhánh từ chối có lý do, xử lý lặp và lỗi ghi. Chỉ nhánh duyệt đánh giá lịch mới. Đơn lỗi thời vẫn PENDING để quản lý có thể từ chối.

Đối chiếu: YC11 · T09–T10, T14–T15.

**Hình 9. Sơ đồ tuần tự gửi đề nghị đổi ca.** Dùng request_swap đúng hợp đồng. Kiểm sở hữu và hai ca cùng chi nhánh, đã công bố, chưa bắt đầu; chỉ chặn đơn chờ trùng cặp kể cả đảo thứ tự. Tạo đơn chưa đổi lịch.

Đối chiếu: YC10 · T09, T15.

**Hình 10. Sơ đồ hoạt động đánh giá điều kiện phân công.** Hàm evaluate_assignment chỉ đọc lịch dự kiến. Kiểm cả hồ sơ, giờ làm, nghỉ và Chủ nhật; ưu tiên BLOCKED khi có vi phạm chắc chắn, NEED_DATA khi chỉ thiếu căn cứ. Các ngưỡng là giả định demo Q1–Q3.

Đối chiếu: YC03–YC04, YC07–YC08 · T02–T07, T13.

**Hình 11. Sơ đồ trạng thái ca làm việc.** Chỉ có DRAFT và PUBLISHED. Công bố thất bại giữ nháp; đổi người qua hoán đổi không làm ca mất trạng thái công bố. Ca đã qua vẫn giữ trạng thái trong model.

Đối chiếu: YC05–YC06, YC09 · Q4.

**Hình 12. Sơ đồ trạng thái đề nghị đổi ca.** Chỉ có PENDING, APPROVED và REJECTED. Lỗi kiểm tra hoặc lỗi giao dịch giữ dữ liệu; xử lý lặp trả quyết định đã lưu. Không tự chuyển sang trạng thái vô hiệu.

Đối chiếu: YC10–YC11 · T09–T10, T14–T15.

**Hình 13. Sơ đồ hoạt động tổng thể theo vai trò.** Ba làn quản lý, hệ thống và nhân viên. Công bố không đạt giữ ca nháp để quản lý khắc phục và thực hiện lại; chỉ sau công bố nhân viên mới xem được ca. Phần xử lý đơn tham chiếu Hình 8–9.

Đối chiếu: YC01–YC11.

**ERD:** chân quạ chỉ phía nhiều; vòng tròn chỉ tùy chọn. PK là khóa chính, FK là khóa ngoại, UK là khóa duy nhất. Trường không ghi NULL không cho phép NULL; một số trường được gộp bằng dấu / để tiết kiệm chỗ. Employee.user có UNIQUE có điều kiện khi khác NULL. Evidence.verified_by bắt buộc; không có trạng thái xác minh riêng trong model.

**Tuần tự:** khung `alt` biểu diễn các nhánh loại trừ nhau; `opt` là phần thực hiện khi điều kiện đúng. Các nhãn COMMIT/ROLLBACK mô tả kết quả giao dịch do Django quản lý khi thoát `transaction.atomic()`, không hướng dẫn gọi commit thủ công bên trong atomic. Nhánh không ghi cũng phải kết thúc giao dịch để giải phóng khóa. Kết quả cho UI đặt sau khung giao dịch. Lỗi DB ở bất kỳ bước nào được xử lý như lỗi giao dịch và không báo thành công.

**Trạng thái:** nhãn chuyển trạng thái dùng dạng sự kiện [điều kiện] / tác động. Trạng thái phản ánh giá trị được lưu; thời gian ca đã qua không tự làm xuất hiện trạng thái mới. Không vẽ kết thúc chỉ để biểu diễn một bản ghi được giữ lại sau xử lý.

**Hoạt động:** Hình 10 đánh giá trên lịch dự kiến đã tạo xong, không chỉ cộng một ca mới vào lịch cũ. Khi đổi ca, thay cả hai chủ trong lịch dự kiến trước khi kiểm người nào. Với ca 23/11 22:00–24/11 06:00, nghỉ 23:45–00:15, số phút làm là 105 ngày 23 và 345 ngày 24 theo T13. Hồ sơ cần phủ hết ngày thực sự làm cuối cùng; ngày hết hạn được tính bao gồm ngày đó.

## Tác nhân và quan hệ Use Case

| Actor | Use case | Quan hệ |
|---|---|---|
| Cả ba vai trò | Đăng nhập hệ thống | Association |
| Quản lý chi nhánh | Quản lý hồ sơ; khai báo nhu cầu ca; xem lịch chi nhánh; xếp ca; xử lý đề nghị đổi ca | Association ở tổng quan |
| Quản lý chi nhánh | Cập nhật hồ sơ; ghi nhận giấy tờ và đào tạo đã xác minh; tạo/sửa ca nháp; phân công; bỏ phân công; công bố ca | Association ở chi tiết |
| Quản lý chi nhánh | Xem, duyệt hoặc từ chối đề nghị đổi ca | Association |
| Nhân viên | Xem lịch cá nhân; gửi đề nghị đổi ca; xem kết quả đổi ca | Association |
| Quản trị viên kỹ thuật | Tạo tài khoản; phân vai; cấu hình danh mục | Association |
| — | Phân công, Công bố, Duyệt đổi ca → Kiểm tra điều kiện phân công | «include» |

Hình 1 là tổng quan, Hình 2–3 là các góc nhìn chi tiết của cùng một hệ thống. Actor ở ngoài system boundary; use case ở trong khung, tên là động từ + danh từ. Association không có mũi tên. `include` đi từ mục tiêu gốc tới chức năng bắt buộc dùng chung. Không thêm `extend` hoặc kế thừa khi không có quan hệ nghiệp vụ tương ứng. Phiên đăng nhập đúng vai trò là điều kiện đầu vào của các chức năng cần quyền.

“Sửa ca nháp” chỉ áp dụng DRAFT. Khi ca đã có người, dịch vụ phải kiểm lại các phân công bị ảnh hưởng; ghi chú điều kiện này trong sơ đồ thay vì biến một hành vi có điều kiện thành `include` bắt buộc cho mọi ca rỗng. “Ghi nhận minh chứng đã xác minh” không thể hiện việc xác minh như một mở rộng tùy chọn.

## Chỉnh sửa và xuất lại

Sửa các file `.puml` (UTF-8); sửa tiêu đề, chú thích hoặc hướng trang trong [danh_muc.json](danh_muc.json). Giá trị `page: auto` chọn hướng in theo tỷ lệ hình; có thể cố định `portrait` hoặc `landscape`. Có thể dùng PlantUML độc lập để xuất SVG hoặc PNG. Nếu dùng Node.js có `sharp`, script [xuat_diagram.cjs](xuat_diagram.cjs) sẽ xuất đồng bộ SVG, PNG và trang xem:

```powershell
node .\HO_SO_DT05\diagram_bao_cao\xuat_diagram.cjs 'DUONG_DAN_PLANTUML_JAR' 'DUONG_DAN_NODE_MODULES' 'DUONG_DAN_JAVA_EXE'
```

Tham số Java có thể bỏ khi lệnh `java` đã có trong PATH. Cần môi trường PlantUML chạy được các sơ đồ có layout Graphviz. Không đưa JAR hoặc thư viện runtime vào repo; người đọc dùng ngay các ảnh đã xuất mà không cần cài công cụ.
