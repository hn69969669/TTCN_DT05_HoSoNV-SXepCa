# Quy ước đối chiếu sơ đồ DT05

Bộ nguồn chính là 13 file PlantUML trong [diagram_bao_cao](README.md), kèm SVG, PNG và trang xem. Các ghi chú dưới đây giữ tên trường, trạng thái và phạm vi thống nhất với code và thiết kế.

## Các điểm cần giữ đúng khi phát triển

1. **Tên model và trường:** hiện không có EmployeePosition, Branch.is_active, Employee.full_name/hired_on/status, Evidence.status/verified_at/document_file hay EvidenceType.validity_months. Nếu muốn thêm phải xác nhận yêu cầu và tạo migration riêng; không chỉ sửa hình để coi như đã có.
2. **Xác minh hồ sơ:** Evidence.verified_by là FK không cho phép NULL. Không đổi quan hệ thành tùy chọn, và không mô tả Xác minh là «extend» tùy chọn của việc ghi minh chứng đủ điều kiện. Quy trình tiếp nhận hồ sơ chưa xác minh là một yêu cầu mới.
3. **Ca qua nửa đêm:** không tính tất cả vào ngày bắt đầu. Theo Q2/T13, ca 22:00–06:00 nghỉ 23:45–00:15 có 105 phút ở ngày đầu và 345 phút ở ngày sau. Chỉ một con số break_minutes không đủ xác định phải trừ nghỉ ở ngày nào. Giấy hết hạn vào ngày làm cuối vẫn có hiệu lực hết ngày đó.
4. **Gửi đơn:** chặn PENDING trùng cùng cặp phân công, kể cả thứ tự đảo. Chặn mọi đơn có một phân công chung là một chính sách chặt hơn chưa được yêu cầu; T15 còn dùng đơn khác có chung phân công để kiểm phát hiện chủ gốc đã đổi.
5. **Duyệt đơn:** ca hết tính tương lai hoặc chủ gốc thay đổi làm thao tác duyệt thất bại, không tự ghi INVALIDATED. Kiểm dữ liệu mới nhất, giữ PENDING và lịch cũ; quản lý có thể từ chối.
6. **Quyền đối tác và liên chi nhánh:** một người gửi, quản lý quyết định; hai ca cùng chi nhánh. Nút xác nhận của đối tác hoặc đổi xuyên chi nhánh đang chờ Q5, chưa chuyển thành điều kiện bắt buộc trong Use Case, sequence hay model.
7. **Cảnh báo:** Q4 có cảnh báo khi hồ sơ thay đổi làm ca sắp tới cần rà soát. Điều này khác một chức năng nhắc “sắp hết hạn” cần ngưỡng, phạm vi người xem và cách hiển thị được xác định thêm.
8. **ScheduleGate:** tách khỏi ERD nghiệp vụ là lựa chọn trình bày. Bảng vẫn có trong model và migration; mọi đường ghi ảnh hưởng điều kiện lịch tuân cùng quy ước khóa. Không được suy ra đã bỏ khóa khỏi hệ thống.
9. **Giới hạn sơ đồ:** số thuộc tính được vẽ ít không có nghĩa schema thiếu thuộc tính. Bổ sung các trường quan trọng vào ERD là cải thiện cách trình bày; thay đổi schema phải được quyết định độc lập.

## Căn cứ đối chiếu

- [YC01–YC11 và phạm vi loại trừ](../02_YEU_CAU.md): YC05–YC11, Q1–Q6.
- [Thiết kế](../03_THIET_KE.md): từ điển dữ liệu, hợp đồng request_swap/decide_swap, kiểm lịch dự kiến và trạng thái.
- [Model hiện hành](../../lichca/models.py) và [migration](../../lichca/migrations/): trường, NULL, UNIQUE và tập trạng thái.
- [T01–T15](../04_NGHIEM_THU.md): T13 về qua ngày; T14 về giao dịch; T15 về đơn lỗi thời.
- [Phiếu M2](../05_XAC_NHAN_M2.md): xác nhận nghiệp vụ vẫn chờ; chưa có cơ sở đổi các đề xuất thành yêu cầu đã duyệt.


Các sơ đồ thiết kế không thay thế bằng chứng chạy phần mềm hoặc nghiệm thu nghiệp vụ.
