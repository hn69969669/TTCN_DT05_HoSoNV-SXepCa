# Buổi đầu của Hiệp và Chung · Đồng bộ dự án và chuẩn bị M2

**Cập nhật sau khởi tạo repo.** Khung Django và SQL Server trên máy Hiệp đã được thiết lập trong thư mục dự án. Khi lấy code hiện tại, làm theo [README của repo](README.md) để chạy hoặc cài trên máy Chung. Repo đã có models, migration và lệnh nạp mẫu; dùng các bước dưới để đồng bộ và kiểm tra trên hai máy.

**Mục tiêu cuối chiều 13/11/2026:** cả hai mở được cùng ứng dụng từ một repo, biết phần còn thiếu của M1, và gửi được bản M2 cho người hướng dẫn cùng người phụ trách nghiệp vụ. M2 đến hạn **thứ Tư 18/11**, trước buổi làm chung kế tiếp. Dùng [lộ trình đến ngày bảo vệ](./LO_TRINH_DT05.md) cho các buổi sau.

## 1. Chiều thứ Năm 12/11 tại văn phòng

| Thời gian tính từ đầu buổi | Hiệp làm gì | Chung làm gì | Dấu hiệu xong |
|---|---|---|---|
| 0–30 phút | Hỏi quản lý tên hai đầu mối, bài đầu vào, cách nộp bù M1 và xin 20–30 phút trao đổi DT05. | Mở trang Đề tài dòng DT05, trang Mốc, đăng ký và lịch N01. Ghi các mục đã có, còn thiếu. | Có người tiếp nhận hoặc tin nhắn chờ phản hồi, kèm thời điểm cần trả lời. |
| 30–100 phút | Kiểm repo và lệnh nạp mẫu theo mục 2. Ghi phiên bản Python và mã commit đang dùng. | Kiểm tra tài khoản Git, Python và quyền vào repo. Chuẩn bị câu hỏi mục 3. | Hiệp chạy được trang đầu, Chung mở được repo bằng tài khoản của mình. |
| 100–190 phút | Cùng trao đổi nghiệp vụ khi có lịch. Xin một ví dụ xếp đúng và một ví dụ phải chặn. | Ghi câu trả lời thực tế. Nếu chưa gặp được, làm sơ đồ và đánh dấu từng giả định cần hỏi. | Có biên bản thật hoặc danh sách câu hỏi đã gửi và lịch chờ. |
| 190–240 phút | Kiểm hướng dẫn cài trên máy Chung. Gom minh chứng M1 cho cả hai. | Lấy repo về máy, mở trang đầu, thêm sơ đồ nháp và tạo commit đầu tiên của mình. | Có commit của từng người, hai máy chạy được. Mỗi người ghi một dòng nhật ký có sản phẩm hoặc vướng mắc thực tế. |

Nếu buổi 12/11 đã kết thúc khi nhóm nhận kế hoạch, giữ nguyên lịch đã làm trong nhật ký. Dùng 30 phút đầu của buổi kế tiếp để liên hệ quản lý, rồi chia đôi việc: Hiệp kiểm dữ liệu mẫu trong lúc Chung chuẩn bị M2. Ưu tiên gặp nghiệp vụ và gửi hồ sơ 13/11. Nếu M1 hoặc một đầu ra M2 chưa kịp, ghi rõ phần thiếu, người làm và xin thời điểm bổ sung.

**Tin nhắn để Hiệp gửi cho quản lý chương trình**

> Em chào anh/chị, nhóm N01 gồm Nguyễn Hữu Hiệp và Lê Thành Chung đã được giao DT05 “Hồ sơ nhân viên và xếp ca”. Hai bạn đã đăng ký lịch. Nhóm đang khởi tạo môi trường và cần hoàn thiện M1 đã đến hạn 11/11. Anh/chị cho nhóm xin tên người hướng dẫn, người phụ trách nghiệp vụ, bài đầu vào theo vai trò và cách nộp bổ sung M1 được không ạ? Nhóm cũng muốn hẹn 20–30 phút để xác nhận quy tắc xếp ca và phạm vi tối thiểu, dự kiến gửi bản M2 chiều 13/11 để kịp hạn 18/11. Em cảm ơn anh/chị.

## 2. Đồng bộ repo và chạy ứng dụng trên Windows

1. **Hiệp** gửi địa chỉ repo và mã `git rev-parse HEAD` đang dùng cho Chung. **Chung** clone repo nếu chưa có; nếu đã có, chạy `git status --short --branch`, giữ các thay đổi đang làm rồi mới `git pull --ff-only` khi thư mục sạch. Hai người kiểm cùng mã commit trước khi thử dữ liệu.
2. **Mỗi người** cài Python 3.13, SQL Server và ODBC Driver 17 hoặc 18. Từ thư mục chứa `manage.py`, chạy script [import database](scripts/HUONG_DAN_IMPORT.md) với đúng tên instance trên máy mình:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\import_database.ps1 -Server '.\SQLEXPRESS'
   ```

   Script tạo `.venv`, cài requirements, lưu cấu hình riêng trong `.env`, tạo database, migrate và nạp mẫu. Nếu chưa có quản trị, script yêu cầu tạo tài khoản trong terminal. Không có mật khẩu mặc định. Khi nạp lại, chọn đúng tài khoản đã dùng lần đầu; xem hướng dẫn import nếu có nhiều quản trị hoặc cần bỏ qua mẫu.
3. **Cả hai** kiểm tra và chạy ứng dụng:

   ```powershell
   .\.venv\Scripts\python.exe -m pip check
   .\.venv\Scripts\python.exe manage.py check
   .\.venv\Scripts\python.exe manage.py showmigrations lichca
   .\.venv\Scripts\python.exe manage.py seed_demo --manager TEN_DANG_NHAP_LOCAL
   .\.venv\Scripts\python.exe manage.py runserver
   ```

   Thay `TEN_DANG_NHAP_LOCAL` bằng tài khoản của lần import. Lần seed này phải báo `Created 0 records`. Mở `http://127.0.0.1:8000/` và đăng nhập `http://127.0.0.1:8000/admin/`, rồi dừng bằng Ctrl+C. Admin hiện chưa đăng ký bảng nghiệp vụ; việc xem hồ sơ/ca được triển khai theo [bước tiếp theo](HO_SO_DT05/06_BUOC_TIEP_THEO.md).
4. **Chung** rà tài liệu M2 trong [bộ hồ sơ](HO_SO_DT05/README.md). Khi có chỉnh sửa thực tế, commit đúng các file của mình rồi bàn giao cho Hiệp thử. Lưu mã commit và bằng chứng chạy của từng máy vào nhật ký; chưa có kết quả máy Chung thì ghi đang chờ xác nhận.

## 2a. Kiểm cấu hình SQL Server của từng máy

- Trong SSMS, dùng tài khoản Windows đang phát triển để kết nối và ghi đúng **Server name**. Thay `.\SQLEXPRESS` trong lệnh import bằng tên đã kết nối được. SSMS là công cụ quản lý; máy vẫn cần SQL Server Database Engine đang chạy.
- Script import nhận driver 17/18 và lưu thông số trong `.env`. Nếu cài thủ công, dùng [README](README.md) và `.env.example`; `config/settings.py` đã đọc các biến này, không cần thay khối `DATABASES`. Giữ mật khẩu, khóa ứng dụng và database ngoài Git.
- Nếu cần kiểm driver sau khi tạo `.venv`, chạy:

  ```powershell
  .\.venv\Scripts\python.exe -c "import pyodbc; print(pyodbc.drivers())"
  ```

- Nếu lỗi kết nối, thử cùng instance và tài khoản trong SSMS; kiểm dịch vụ SQL Server, tên server trong `.env` và driver đã cài. Nếu thiếu quyền tạo database, nhờ quản trị tạo `DT05_Dev` và cấp quyền migration. Không đổi cấu hình máy khác để khớp máy Hiệp.
- Nếu cổng 8000 bận, chạy `.\.venv\Scripts\python.exe manage.py runserver 8001` rồi mở cổng 8001. Ghi lỗi và thao tác tái hiện khi cần hỗ trợ.

## 3. Cuộc hẹn nghiệp vụ 20–30 phút

Chung mở biên bản và ghi **ngày, người tham gia, tình huống trao đổi, câu trả lời, quyết định, điểm còn mở, ai trả lời tiếp và hạn phản hồi**. Hiệp hỏi bằng tình huống cụ thể. Sau buổi gặp, gửi bản tóm tắt để người tham gia sửa hoặc xác nhận.

| Hỏi người phụ trách | Quyết định nhóm cần mang về |
|---|---|
| “Một ca bếp ở CN01 cần hai người. Người xếp dựa vào vị trí, giấy tờ và lịch sử đào tạo nào? Giấy hết hạn đúng ngày làm ca hoặc giữa ca qua đêm thì tính thế nào?” | Danh mục bắt buộc theo vị trí, thời điểm xét hiệu lực, dữ liệu cho phép quản lý sửa. |
| “Nếu ca trước kết thúc lúc 22:00, những giờ nào hôm sau được bắt đầu? Nhóm dùng chính sách bảo thủ 11 giờ nghỉ và tối đa 8 giờ làm thực tế/ngày cho demo được không?” | Ngưỡng, cách trừ nghỉ giữa giờ, cách cộng nhiều ca, cách xử lý qua ngày và các ngoại lệ được đưa vào phạm vi. |
| “Khi chỉ biết lịch một tuần thì màn hình phải báo gì về số Chủ nhật nghỉ? Nếu lập lịch Chủ nhật, có kiểm ngày nghỉ bù trong bản này không?” | Kỳ dữ liệu, cách xử lý thiếu lịch sử/tương lai, lịch năm giả lập, quy tắc chặn/cảnh báo và giới hạn bản demo. |
| “Lịch cần hai người nhưng mới có một. Quản lý được lưu nháp, được công bố hay phải bổ sung? Nhân viên thấy lịch từ thời điểm nào?” | Trạng thái nháp/đã công bố và cách thể hiện thiếu người. |
| “Đổi ca là hai người hoán đổi hai ca hay một người nhận thay? Ai đề nghị, ai cần đồng ý, ai duyệt? Nếu người thay mất điều kiện trước khi duyệt thì sao?” | Chọn một luồng cho bản đầu. Đề xuất hai người hoán đổi, quản lý duyệt, kiểm lại cả hai và giữ lịch cũ nếu thất bại. |
| “Đến 27/11, anh/chị muốn thấy thao tác nào để chấm giữa kỳ? M2 duyệt bằng email, tin nhắn hay buổi họp? Ai nhận bản cuối?” | Một ví dụ nghiệm thu, đầu mối, kênh gửi, ngày phản hồi và hình thức xác nhận. |

### Căn cứ để viết bảng quy tắc

Các con số dưới đây giúp hai bạn trao đổi với nghiệp vụ và ghi rõ giới hạn của bản mô phỏng. Trong đặc tả, ghi riêng căn cứ, **chính sách demo đã duyệt**, dữ liệu cần có và cách hiển thị khi thiếu dữ liệu.

- **Giờ làm.** ArbZG §3 nêu mức thông thường 8 giờ mỗi ngày làm việc, có thể đến 10 giờ với điều kiện bình quân trong 6 tháng lịch hoặc 24 tuần. Phương án gọn là giới hạn demo 8 giờ làm thực tế và chưa xét cơ chế bình quân. §4 còn quy định nghỉ giữa giờ. Chốt liệu phần mềm nhận khoảng nghỉ hay chỉ nhận tổng số phút theo phạm vi được duyệt. [ArbZG §3](https://www.gesetze-im-internet.de/arbzg/__3.html) · [ArbZG §4](https://www.gesetze-im-internet.de/arbzg/__4.html)
- **Nghỉ giữa hai ngày làm việc.** §5 đặt nguyên tắc 11 giờ nghỉ liên tục và có ngoại lệ có bù cho ngành nhà hàng. Nhóm đề xuất chỉ nhận các lịch đủ 11 giờ cho demo. Khi nghiệp vụ cho phép chia một ngày làm thành nhiều đoạn, cần phân biệt nghỉ giữa ngày làm việc với nghỉ sau khi kết thúc ngày làm việc. Chốt định nghĩa “ca” trước khi viết điều kiện. [ArbZG §5 trong văn bản chính thức](https://www.gesetze-im-internet.de/arbzg/BJNR117100994.html)
- **Chủ nhật.** §11 quy định chung ít nhất 15 Chủ nhật được nghỉ mỗi năm và có quy định về ngày nghỉ bù. Dùng một lịch năm giả lập đã biết ngày làm/nghỉ để kiểm thử ngưỡng, cùng một bộ thiếu dữ liệu để thử thông báo. Nếu bộ lịch chưa đủ để kết luận, đề xuất chặn công bố đến khi người quản lý bổ sung. Ghi rõ trong M2 cách xử lý ngày nghỉ bù và ngoại lệ ngành. [ArbZG §11](https://www.gesetze-im-internet.de/arbzg/__11.html) · [ArbZG §10](https://www.gesetze-im-internet.de/arbzg/__10.html)
- **Đào tạo vệ sinh.** Với các công việc thuộc phạm vi §42, IfSG §43 phân biệt chứng nhận ở lần bắt đầu công việc đầu tiên và việc người sử dụng lao động hướng dẫn sau khi bắt đầu rồi định kỳ hai năm. Khi làm dữ liệu, tách căn cứ ban đầu, ngày bắt đầu và ngày hướng dẫn lại. Hỏi nghiệp vụ vị trí nào áp dụng và cần lưu minh chứng gì. [IfSG §43](https://www.gesetze-im-internet.de/ifsg/__43.html)

## 4. Thứ Sáu 13/11 · Làm hồ sơ M2 để gửi duyệt

Nhóm đã có [bản soạn sẵn của các đầu ra M2](HO_SO_DT05/README.md). Dùng các mục dưới đây để rà lại bản soạn, hoàn thiện biên bản từ cuộc trao đổi thực tế và ghi phản hồi của hai người duyệt.

**Sáng — Hiệp chuẩn bị dữ liệu, Chung viết quy trình và yêu cầu.** Dưới đây là năm mục để hai bạn tạo trong repo hoặc thư mục tài liệu nhóm. Tên tệp là gợi ý. Thay mọi giả định bằng quyết định đã được xác nhận khi có phản hồi.

| Đầu ra M2 | Cách làm bản đầu | Tự kiểm trước khi gửi |
|---|---|---|
| 1. Biên bản trao đổi | Dùng mục 3. Tách quyết định đã thống nhất khỏi câu hỏi còn mở. | Có tên người trao đổi, ngày thực tế, nội dung phản hồi và người xác nhận. Nếu chưa gặp, ghi đang chờ. |
| 2. Sơ đồ quy trình | Vẽ hai làn **Quản lý** và **Nhân viên**. Quản lý khai hồ sơ → nhập nhu cầu → chọn người → kiểm tra → lưu nháp → công bố. Nhân viên xem → đề nghị đổi → quản lý kiểm lại → duyệt/từ chối → nhân viên xem kết quả. | Có nhánh hồ sơ/ca vi phạm, lịch thiếu người và yêu cầu đổi bị từ chối. |
| 3. Bộ dữ liệu giả lập | Lập bảng theo mẫu bên dưới. Dùng mã cố định để nối nhân viên, chi nhánh, ca và hồ sơ. Ghi ngày giờ theo giờ địa phương chi nhánh giả lập tại Đức. | Truy lại được đầu vào của một ca đúng và lý do cụ thể của một ca sai. Chỉ sử dụng danh tính và giấy tờ giả lập. |
| 4. Đặc tả rút gọn | Mỗi dòng gồm mã, vai trò, thao tác, điều kiện, kết quả, cách thử. Ví dụ **YC03**: quản lý xếp NV02 vào ca bếp sau ngày hết hiệu lực → từ chối lưu, nêu loại giấy và ngày hết hạn → đối chiếu T02 trong lộ trình. | Bao quát hồ sơ, đào tạo, nhu cầu, phân ca, ba nhóm kiểm tra giờ/nghỉ/Chủ nhật, công bố, xem lịch và đổi ca. |
| 5. Phạm vi tối thiểu xin duyệt | Ghi rõ hai vai trò, luồng demo, quy tắc dùng, trường hợp thiếu dữ liệu, phần hoãn lại và các ví dụ nghiệm thu. Đính kèm ngày, phiên bản, tên hai người duyệt. | Người đọc xác định được chức năng nào sẽ chạy ở M3, chức năng nào trọn vẹn ở M4 và điểm nào vẫn chờ trả lời. |

**Bộ dữ liệu để hai người dựng cùng một ví dụ**

| Bảng nên có | Bản mẫu đủ để bắt đầu |
|---|---|
| Chi nhánh và nhu cầu | CN01, CN02. CA01 ở CN01, 23/11/2026 09:00–17:30, nghỉ 30 phút, cần 2 người bếp. CA02 ở CN02 cùng ngày, bắt đầu 12:00 để thử trùng giờ. |
| Nhân viên và hồ sơ | NV01 đủ toàn bộ điều kiện. NV02 có giấy bắt buộc cho vị trí hết hạn 22/11. NV03 thiếu lần hướng dẫn vệ sinh cần có. NV04 đủ điều kiện và có sẵn một ca ngày khác để thử đổi. Thêm NV05 đủ điều kiện, còn trống để lấp vị trí thứ hai ở CA01. |
| Hồ sơ và đào tạo | Mỗi bản ghi có mã nhân viên, loại hồ sơ, vị trí áp dụng, ngày cấp/ngày hướng dẫn, ngày hiệu lực và ngày đến hạn nếu áp dụng. Tách lần đầu và lần hướng dẫn tiếp theo. |
| Lịch và phân công | Thêm một ca kết thúc 22:00 hôm trước và hai giờ bắt đầu hôm sau để thử biên 11 giờ. Lưu giờ bắt đầu/kết thúc có ngày, thời gian nghỉ, người, chi nhánh và trạng thái công bố. Mỗi ca thử biên dùng bản dữ liệu sạch để cô lập lý do bị chặn. |
| Chủ nhật và đổi ca | Tạo bảng các ngày Chủ nhật của năm 2026 cho một nhân viên, đánh dấu rõ ngày làm/nghỉ, điều chỉnh để còn đúng 15 ngày nghỉ. Thêm một trường hợp chỉ biết một tuần. Tạo ví dụ A/B muốn đổi hai ca ở hai ngày khác nhau. |

**Chiều — ráp thử và gửi.** Chung đóng vai quản lý, Hiệp đọc dữ liệu như hệ thống: thử xếp NV02 vào CA01, thay bằng NV01, bổ sung NV05, công bố, rồi thử hai người đổi ca. Chỗ nào hai bạn dự đoán kết quả khác nhau thì bổ sung vào danh sách cần duyệt. Gửi cả năm mục hoặc ghi rõ mục đang chờ. Lưu phản hồi gắn với đúng phiên bản.

> Em gửi bản M2 của N01 cho DT05, gồm biên bản [link/trạng thái], sơ đồ [link], dữ liệu giả lập [link], đặc tả [link] và phạm vi tối thiểu [link]. Nhóm đề nghị xác nhận các điểm [liệt kê ngắn]. Anh/chị cho nhóm xin phản hồi trước hoặc trong ngày 18/11 để triển khai theo đúng phạm vi. Hiệp theo dõi quy tắc và dữ liệu, Chung theo dõi luồng sử dụng và biên bản.

**Cuối buổi, gửi lại cho người điều phối bốn dòng:** (1) link repo và phiên bản cả hai đã chạy, (2) M1 đã có gì và còn thiếu gì, (3) link năm mục M2 và câu trả lời thực tế của người duyệt, (4) một vướng mắc cần quyết định trước buổi 19/11. Với bốn dòng này, nhóm có thể điều chỉnh buổi kế tiếp theo kết quả thật.
