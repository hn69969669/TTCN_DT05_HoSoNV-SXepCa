# Lộ trình thực tập DT05 · Hồ sơ nhân viên và xếp ca

**Nhóm N01 — Nguyễn Hữu Hiệp và Lê Thành Chung · 12/11–18/12/2026**

Để triển khai từng buổi, mở [hồ sơ kế hoạch, yêu cầu và thiết kế DT05](HO_SO_DT05/README.md). Bộ này có đặc tả để đem tới cuộc hẹn M2, mô hình SQL Server và dữ liệu thực hành cho hai máy.

**Bắt đầu bằng việc mở [Hướng dẫn buổi đầu và bộ câu hỏi M2](./BAT_DAU_DT05.md).** Ngày 12–13/11, hai bạn cần có một repo cả hai chạy được, biết ai duyệt bài và đưa cho người phụ trách nghiệp vụ một tình huống xếp ca cụ thể để họ góp ý. Bản này dùng để theo dõi từ buổi đầu đến ngày báo cáo.

## 1. Sản phẩm nhóm sẽ trình diễn

Người quản lý chi nhánh mở ca bếp cần hai người. Khi chọn NV02, màn hình chỉ ra giấy tờ bắt buộc đã hết hạn trước ngày làm việc và giữ nguyên ca. Quản lý thay bằng NV01 đủ điều kiện, nhìn thấy ca còn thiếu một người, bổ sung NV05 rồi công bố lịch. NV01 đăng nhập, thấy lịch của mình và đề nghị đổi với NV04. Quản lý kiểm tra cả hai, duyệt yêu cầu và hai nhân viên mở lại lịch để thấy kết quả.

Đây là kịch bản để thống nhất ở M2. **Đầu ra chính thức của DT05** là công cụ xếp ca có tự kiểm tra quy định và lịch ca cho nhân viên. Đề bài bao gồm hồ sơ, giấy tờ có thời hạn, đào tạo bắt buộc, nhu cầu từng chi nhánh, nghỉ giữa hai ca, số giờ/ngày, số Chủ nhật nghỉ và đề nghị đổi ca. Dữ liệu chương trình cho phép là dữ liệu giả lập hoặc đã ẩn danh. Nhóm bắt đầu từ số 0 nên dùng toàn bộ dữ liệu giả lập. [Bảng chương trình, trang Đề tài, dòng DT05](https://docs.google.com/spreadsheets/d/1NY6msgE6lJuXRuEuBP4bVPVmSU7FKnFBtdhE9q2dKEU/edit?gid=97601406#gid=97601406&range=A9:H9)

| Phần việc | Người làm chính | Kết quả để bạn còn lại thử |
|---|---|---|
| Quy tắc xếp ca và dữ liệu | **Hiệp** | Nhập nhân viên, ca dự kiến và lịch liên quan → trả về đủ điều kiện hoặc mã lỗi, lý do và dữ liệu còn thiếu. Cùng một phép kiểm tra dùng lúc phân ca, công bố và duyệt đổi. |
| Hồ sơ và màn hình sử dụng | **Chung** | Quản lý sửa hồ sơ, mở lịch chi nhánh, thấy vì sao bị chặn. Nhân viên đăng nhập bằng tài khoản khác, xem lịch cá nhân và tạo đề nghị đổi. |
| Tích hợp và bàn giao | **Cả hai** | Hiệp kiểm luồng qua giao diện Chung viết. Chung bắt đầu từ dữ liệu mẫu để kiểm tra kết quả quy tắc Hiệp viết. Mỗi người tự demo phần của mình và giải thích một lỗi đã xử lý. |

Đây là phân công đề xuất cho hai người khởi đầu. Theo lựa chọn của nhóm, dùng **một ứng dụng Django 5.2, giao diện HTML phía máy chủ và SQL Server**, kết nối bằng backend Microsoft `mssql-django`. Mỗi người phát triển với database `DT05_Dev` trên SQL Server của máy mình, đồng bộ cấu trúc bằng migration và tái tạo dữ liệu từ cùng bộ mẫu. Máy demo dùng một database có cả tài khoản quản lý và nhân viên để diễn trọn luồng. Tận dụng đăng nhập, phân quyền và màn hình quản trị có sẵn để nhập danh mục. Dành thời gian xây màn hình phân ca và lịch nhân viên. Xếp người bằng tay và kiểm tra tự động đáp ứng luồng đề xuất. Chỉ đưa tối ưu tự động bằng AI, kéo-thả, chấm công, tính lương hoặc triển khai công khai vào kế hoạch nếu người hướng dẫn thay đổi phạm vi. [Hướng dẫn chính thức của Django](https://docs.djangoproject.com/en/5.2/intro/tutorial01/) · [Backend SQL Server của Microsoft](https://github.com/microsoft/mssql-django)

**Điểm hai bạn cần thống nhất trước khi chia nhau viết code.** Một ca lưu chi nhánh, vị trí, ngày giờ bắt đầu/kết thúc, khoảng nghỉ và số người cần. Mỗi phân công nối một nhân viên với một ca. Hiệp trả về một trong ba kết quả **đủ điều kiện**, **vi phạm kèm lý do**, **thiếu dữ liệu kèm mục cần bổ sung**. Chung dùng chính kết quả đó ở màn hình phân ca và duyệt đổi. Chốt cùng nghiệp vụ khi nào lịch nháp được lưu và khi nào được công bố. Để thử tích hợp lần đầu, hai bạn chỉ cần cùng trả lời được câu “vì sao NV02 chưa thể vào CA01?” trên màn hình.

## 2. Sáu mốc chính thức và ngày nhóm cần có hàng

Cả hai đăng ký **chiều thứ Năm tại văn phòng, sáng và chiều thứ Sáu online**, mỗi buổi 4 giờ. Mỗi người có 12 giờ/tuần. Cột “nhóm chuẩn bị xong” bên dưới là lịch nội bộ đề xuất. Hạn và người duyệt lấy từ trang **Mốc**. [Bảng quản lý thực tập](https://docs.google.com/spreadsheets/d/1NY6msgE6lJuXRuEuBP4bVPVmSU7FKnFBtdhE9q2dKEU/edit)

| Mốc | Nhóm chuẩn bị xong | Hạn chính thức | Giao gì, cho ai |
|---|---|---|---|
| M1 · Khởi động | Rà soát và xin xử lý phần còn thiếu ngay 12/11 | **11/11**, đã qua | Đề tài và lịch đã có trong bảng. Mỗi người bổ sung môi trường, tài khoản Git và bài đầu vào theo vai trò do đơn vị giao. Người hướng dẫn xác nhận cách nộp bù và đánh giá. |
| M2 · Yêu cầu | **Chiều 13/11** gửi hồ sơ và xin lịch phản hồi | **18/11, thứ Tư** | Biên bản trao đổi thực tế, sơ đồ quy trình, bộ dữ liệu giả lập, đặc tả rút gọn, phạm vi tối thiểu. Người hướng dẫn **và** người phụ trách nghiệp vụ duyệt. |
| M3 · Giữa kỳ | **26/11** chạy thử trên hai máy | **27/11, thứ Sáu** | Demo chức năng chính có một ca thành công và một ca bị chặn. Mỗi sinh viên có phần trình diễn và minh chứng đóng góp riêng cho người hướng dẫn. |
| M4 · Hoàn thiện | **Chiều 04/12** gửi bản đủ luồng | **09/12, thứ Tư** | Đủ phạm vi M2 đã duyệt, có các trường hợp đặc biệt. Gửi người hướng dẫn bản chạy, dữ liệu và kết quả đối chiếu từng yêu cầu. |
| M5 · Kiểm thử và bàn giao | **Chiều 11/12** gửi gói bàn giao | **15/12, thứ Ba** | Báo cáo kiểm thử, hướng dẫn cài đặt và sử dụng. Kiểm thử viên và người hướng dẫn duyệt. |
| M6 · Báo cáo | **17/12** tổng duyệt, xác nhận giờ trình bày | **18/12, thứ Sáu** | Trình bày sản phẩm 15 phút xuyên suốt quy trình cho ban lãnh đạo và nộp báo cáo thực tập theo mẫu trường. |

M1 đang ghi “Chưa bắt đầu” ở trang **Tiến độ**. Trang nhật ký đã có một dòng làm quen ngày 05/11 của Hiệp. Hai bạn cho biết chưa có repo, công nghệ hay sản phẩm để kế thừa. Hãy dùng kết quả có thật để đối chiếu với người hướng dẫn. Chỉ người hướng dẫn cập nhật hoàn thành. Hai ô người hướng dẫn và phụ trách nghiệp vụ của N01 còn trống tại thời điểm đọc bảng.

## 3. Giao việc theo từng buổi

Mỗi dòng là **một buổi chung**. Cuối buổi dành 15 phút chạy lại kết quả của nhau và ghi nhật ký. Hẹn việc duyệt ngay trong buổi thứ Năm khi gặp người phụ trách. Với các hạn thứ Ba/thứ Tư, thống nhất cách nhận phản hồi ngay khi gửi hồ sơ thứ Sáu. Nếu cần sửa ngoài lịch, trao đổi trước và dùng trang **Nghỉ & đổi lịch** theo hướng dẫn của chương trình.

| Buổi | Hiệp | Chung | Trước khi kết thúc buổi |
|---|---|---|---|
| **12/11 · chiều VP** | Liên hệ quản lý để biết hai đầu mối, xin bài đầu vào và lịch duyệt. Tạo repo và ứng dụng khởi đầu. | Kiểm tra công cụ trên máy mình, lấy repo, chạy thử. Ghi biên bản khi trao đổi và vẽ luồng hiện tại. | Hai máy mở được ứng dụng. Có danh sách M1 đã có/còn thiếu, người theo dõi từng việc và lịch hoặc yêu cầu hẹn nghiệp vụ. |
| **13/11 · sáng OL** | Lập dữ liệu mẫu và bảng quy tắc. Ghi đầu vào, lý do bị chặn và ví dụ ở từng quy tắc. Làm phần bài đầu vào đã nhận. | Soạn sơ đồ quy trình, yêu cầu và phác thảo màn hình. Ghi quyết định thực tế vào biên bản. Làm phần bài đầu vào đã nhận. | Dùng giấy hoặc bảng dữ liệu đi qua một ca được xếp, một ca bị chặn, một yêu cầu đổi. Đánh dấu các câu chưa có người trả lời. |
| **13/11 · chiều OL** | Kiểm dữ liệu có đủ các trường hợp trong đặc tả. Gom minh chứng M1 và dẫn liên kết từng phần. | Rà 5 đầu ra M2, gửi hồ sơ cho hai đầu mối, đề nghị phản hồi trước 18/11. | Có bản gửi, ngày gửi, người nhận và danh sách đang chờ. Nếu chưa trao đổi được, gửi bản nháp và báo thiếu biên bản thật. |
| **19/11 · chiều VP** | Theo phạm vi M2 đã thống nhất, dựng bảng chi nhánh, nhân viên, điều kiện công việc, giấy tờ, đào tạo, ca và phân công. | Dùng đăng nhập có sẵn, tạo hai vai trò và màn hình nhập hồ sơ bằng trang quản trị. | Một máy tạo hồ sơ mẫu, máy kia nạp cùng bộ mẫu và nhìn thấy hồ sơ tương đương. Nếu M2 chờ duyệt, ưu tiên hồ sơ và dữ liệu đã rõ. |
| **20/11 · sáng OL** | Viết kiểm tra giấy tờ, đào tạo, trùng giờ và kiểm tra ca liền trước/liền sau trên mọi chi nhánh. | Tạo màn hình chọn chi nhánh, chọn ca, hiện vị trí cần người và chọn nhân viên. | Chung chọn người có giấy hết hạn và đọc được lý do trả về từ máy chủ. Hiệp kiểm tra dữ liệu ca vẫn như cũ. |
| **20/11 · chiều OL** | Bổ sung tổng giờ làm, kiểm tra Chủ nhật theo dữ liệu năm và các ví dụ biên M2. | Nối thao tác lưu phân công, số người đã xếp/còn thiếu và lịch tuần. | Một ca có từ 0 lên 1 người, thêm người hợp lệ thành 2. Hai bạn mở lại trang và thấy kết quả đã lưu. |
| **26/11 · chiều VP** | Kiểm các thông báo sai, chạy bộ quy tắc với dữ liệu sạch. Chuẩn bị minh chứng phần cá nhân. | Nối công bố lịch và trang lịch cá nhân. Dùng tài khoản nhân viên để diễn tập. | Chạy kịch bản M3 từ đầu đến lúc nhân viên thấy lịch. Ghi phiên bản dùng để trình và danh sách lỗi còn mở. |
| **27/11 · sáng OL** | Demo ca bị chặn, ca hợp lệ và giải thích cách kiểm tra. | Demo nhập hồ sơ, công bố và xem lịch bằng vai trò nhân viên. | Người hướng dẫn có thể đánh giá từng người. Nếu lịch đánh giá được xếp vào chiều, dùng sáng để tổng duyệt và đổi hai đầu việc trong ngày. |
| **27/11 · chiều OL** | Xử lý góp ý giữa kỳ. Dựng bước kiểm tra người thay và ca còn lại sau khi đổi. | Dựng đơn đề nghị đổi, hiển thị trạng thái chờ và danh sách cho quản lý. | Nhân viên gửi yêu cầu, quản lý thấy yêu cầu chờ, lịch đã công bố vẫn giữ nguyên. |
| **03/12 · chiều VP** | Hoàn thiện duyệt đổi, kiểm lại hai người và lịch mới tại lúc duyệt. Nếu thất bại, giữ toàn bộ phân công cũ. | Hoàn thiện thao tác duyệt/từ chối đúng quyền, lý do, lịch của hai nhân viên. | Thử một yêu cầu được duyệt, một yêu cầu người thay vừa mất điều kiện và một yêu cầu bị từ chối. |
| **04/12 · sáng OL** | Kiểm ca sát ngưỡng giờ, thiếu dữ liệu năm, ngày hết hạn, trùng giờ ở hai chi nhánh. | Kiểm số người còn thiếu, lịch nháp/đã công bố, đổi ca đã xử lý và quyền xem lịch cá nhân. | Mỗi yêu cầu M2 có ít nhất một ca kiểm thử và kết quả thực tế. Ưu tiên sửa lỗi có thể xếp sai người hoặc đổi sai lịch. |
| **04/12 · chiều OL** | Tạo bộ mẫu phục hồi được và ghi phiên bản M4. | Chạy lại toàn bộ kịch bản rồi gửi người hướng dẫn bản M4 cùng danh sách điểm cần xác nhận. | Người nhận có thể mở bản demo, đọc giới hạn đã duyệt và tự thử một trường hợp lỗi. |
| **10/12 · chiều VP** | Cài mới từ repo trên máy thứ hai theo bản nháp hướng dẫn của Chung. Ghi bước bị thiếu và sửa lỗi. | Soạn hướng dẫn cài và hướng dẫn theo hai vai trò. Mời kiểm thử viên thử phân ca và đổi ca. | Cài được từ dữ liệu trống, nạp lại bộ mẫu và trình diễn được mà người viết không phải thao tác hộ. |
| **11/12 · sáng OL** | Sửa lỗi chặn bàn giao, chạy lại ca lỗi và ca lân cận, ghi phiên bản đã sửa. | Ghi kết quả thực tế, ảnh minh chứng và danh sách hạn chế còn lại. | Báo cáo nêu môi trường, phiên bản, từng ca đã chạy, số đạt/trượt và lỗi chưa đóng. |
| **11/12 · chiều OL** | Đóng gói phiên bản bàn giao, kiểm tra đường dẫn, hướng dẫn nạp lại dữ liệu. | Gửi gói M5 cho kiểm thử viên và người hướng dẫn, thống nhất kênh phản hồi. Lấy mẫu báo cáo trường nếu còn thiếu. | Có mã nguồn, dữ liệu mẫu, hướng dẫn cài, hướng dẫn dùng, báo cáo kiểm thử và người nhận. |
| **17/12 · chiều VP** | Chuẩn bị máy demo, dữ liệu ban đầu, bản dự phòng. Viết phần thiết kế và quy tắc vào mẫu trường. | Hoàn thiện báo cáo, ảnh và slide. Bấm giờ, ghi chỗ bị vấp. | Hai người chạy trọn 15 phút. Đã xác nhận giờ bảo vệ và cách nộp báo cáo. |
| **18/12 · sáng OL** | Khôi phục dữ liệu, thử tài khoản và kiểm tra bản dự phòng. | Đối chiếu danh sách cần nộp, mở sẵn báo cáo và đường dẫn. | Sẵn sàng trình bày đầu buổi nếu ban lãnh đạo xếp lịch sáng. |
| **18/12 · chiều OL hoặc giờ được xếp** | Trình diễn quy tắc, cùng trả lời câu hỏi. | Dẫn luồng sản phẩm và nộp báo cáo theo mẫu. | Lưu bản đã nộp, phiên bản đã trình và phản hồi. Nếu bảo vệ buổi sáng, dùng chiều để hoàn tất bàn giao. |

## 4. Nhóm biết sản phẩm đạt bằng cách nào?

Dùng các trường hợp sau để hỏi nghiệp vụ ở M2. Khi đã duyệt, mỗi dòng thành một ca kiểm thử. Hiệp chuẩn bị dữ liệu đầu vào. Chung ghi kết quả mong đợi trước, sau đó chạy và ghi kết quả thực tế. Ký hiệu NV, CN là nhân viên và chi nhánh giả lập.

| Mã | Thao tác để thử | Kết quả mong đợi trong phạm vi đề xuất |
|---|---|---|
| T01 | CN01 cần 2 người. Chọn NV01 có đủ hồ sơ và lịch trống. | Lưu được, hiện 1/2 và còn thiếu 1. Thêm người thứ hai đủ điều kiện thì hiện 2/2. |
| T02 | Xếp NV02 vào vị trí bếp khi giấy tờ bắt buộc hết hạn trước ca. | Bị chặn, nêu đúng giấy tờ và ngày hết hạn. Đổi sang ngày còn hiệu lực thì cho xếp nếu các điều kiện khác đạt. |
| T03 | Xếp NV03 thiếu lần hướng dẫn vệ sinh bắt buộc cho bếp, sau đó bổ sung hồ sơ hợp lệ. | Lần đầu chặn vì đào tạo. Sau bổ sung, chạy lại toàn bộ điều kiện và cho xếp khi đạt. |
| T04 | Cùng người đang ở CN01, thử xếp vào CN02 với khoảng giờ giao nhau. | Bị chặn dù khác chi nhánh. Hai ca chạm đầu mút không bị báo trùng giờ, nhưng vẫn phải kiểm các quy tắc khác. |
| T05 | Theo chính sách demo nghỉ tối thiểu 11 giờ, ca trước kết thúc 22:00. Thử hôm sau bắt đầu 08:59 rồi 09:00. Làm lại với thứ tự nhập hai ca đảo ngược. | Trường hợp đầu bị chặn, trường hợp sau qua riêng điều kiện nghỉ. Khi chèn ca cũ, ca liền sau vẫn được kiểm. |
| T06 | Theo trần nội bộ demo 8 giờ làm, nhập ca 09:00–17:30 có nghỉ 30 phút, sau đó đổi giờ kết thúc thành 17:31. | Lần đầu đạt 8 giờ, lần sau vượt 1 phút và bị chặn. Thử hai khoảng làm trong cùng ngày để bắt lỗi chỉ tính riêng ca mới. |
| T07 | Bộ mẫu cả năm có 15 Chủ nhật nghỉ, thử phân công vào một trong 15 ngày đó. Thử lại với bộ mẫu chỉ có lịch một tuần. | Lần đầu báo còn 14 và chặn theo chính sách đã duyệt. Lần sau báo thiếu dữ liệu để kết luận và xử lý theo quyết định M2. |
| T08 | Dùng tài khoản nhân viên A xem lịch đã công bố rồi mở đường dẫn lịch cá nhân của B. | A thấy ca của A. Máy chủ từ chối truy cập lịch riêng của B. Lịch nháp chưa xuất hiện ở tài khoản nhân viên. |
| T09 | A gửi yêu cầu đổi ca với B. Quản lý duyệt khi cả hai vẫn đủ điều kiện. Mở lại lịch và thử bấm duyệt lần nữa. | Trước duyệt lịch giữ nguyên. Sau duyệt cập nhật một lần cho cả hai, số người ở ca vẫn đúng. |
| T10 | Sau khi gửi đề nghị, làm giấy tờ người thay hết hạn rồi mới duyệt. Thử thêm nhánh quản lý từ chối. | Trường hợp đầu chặn và giải thích. Nhánh từ chối ghi trạng thái/lý do. Cả hai trường hợp giữ nguyên lịch đã công bố. |

Trong báo cáo M5, thêm cột **phiên bản · kết quả thực tế · đạt/trượt · người chạy · minh chứng**. Bổ sung ca theo phạm vi nghiệp vụ thực sự duyệt, nhất là cách xử lý ca qua nửa đêm, lịch thiếu người và ngày nghỉ bù. Chỉ ghi “đạt” sau khi đã chạy.

## 5. Xử lý khi công việc bị kẹt

| Khi gặp tình huống | Việc thực hiện ngay | Ai quyết định tiếp |
|---|---|---|
| Chưa có tên người duyệt hoặc chưa nhận bài M1 | Hiệp hỏi quản lý chương trình bằng mẫu ở tài liệu buổi đầu. Chung tiếp tục sơ đồ, dữ liệu và đặc tả nháp. Ghi ngày giờ đã hỏi, phần còn chờ và hạn 18/11. | Quản lý chỉ định người. Người hướng dẫn xác nhận cách bù M1. |
| Chưa có phản hồi trước hạn M2 | Gửi 5 mục với trạng thái thực của từng mục, nêu rõ phần chưa có biên bản/duyệt và đề nghị lịch xử lý. Chỉ triển khai trước các phần dễ điều chỉnh như danh mục, đăng nhập và mẫu dữ liệu. | Người hướng dẫn và phụ trách nghiệp vụ xác nhận phạm vi. |
| Hai cách hiểu về một quy tắc | Đưa hai ca ví dụ khác nhau đúng một yếu tố, ghi kết quả A/B, xin chọn và lưu tên/ngày phản hồi. | Nghiệp vụ xác nhận ý nghĩa, người hướng dẫn xác nhận phạm vi triển khai. |
| Nguy cơ trễ M3/M4 | Giữ thứ tự hồ sơ → xếp hợp lệ/chặn ca sai → công bố → đổi ca. Dùng trang quản trị cho nhập liệu, lịch dạng bảng và bộ dữ liệu nhỏ. Báo sớm nếu phải đổi yêu cầu đã duyệt. | Hai bạn thu gọn giao diện. Người duyệt quyết định thay đổi phạm vi. |
| Lỗi chỉ xảy ra trên máy một bạn | Ghi phiên bản Git, phiên bản Python, bước gây lỗi và thông báo đầu tiên. Bạn kia chạy lại với dữ liệu mẫu. Khi sửa xong, người phát hiện thử lại trên chính máy ban đầu. | Người làm phần lỗi sửa, người còn lại xác nhận. |

**Nhật ký.** Trang đang có tên **Nhật ký buổi làm** và yêu cầu mỗi sinh viên ghi một dòng cuối mỗi buổi theo thứ tự thời gian. Ghi công việc, sản phẩm hoặc link, vướng mắc, người cần hỗ trợ, kế hoạch buổi sau và mức rủi ro. Trang Hướng dẫn còn nhắc “Nhật ký tuần”. Cuối thứ Sáu, gom hai hoặc ba dòng kết quả nhóm và hỏi người hướng dẫn nơi nhận nếu họ yêu cầu bản tuần. [Bảng quản lý thực tập](https://docs.google.com/spreadsheets/d/1NY6msgE6lJuXRuEuBP4bVPVmSU7FKnFBtdhE9q2dKEU/edit)

**Kịch bản bảo vệ 15 phút.** Chung dùng 2 phút giới thiệu nhu cầu chi nhánh và hồ sơ mẫu. Hiệp dùng 5 phút để phân một ca hợp lệ, thử một hồ sơ bị chặn và giải thích một quy tắc bằng dữ liệu. Chung dùng 5 phút công bố lịch, gửi và duyệt đổi, sau đó mở lại lịch hai người. Hiệp dùng 2 phút trình bày kết quả kiểm thử và giới hạn của dữ liệu. Dành 1 phút cuối cho kết luận hoặc câu hỏi.
