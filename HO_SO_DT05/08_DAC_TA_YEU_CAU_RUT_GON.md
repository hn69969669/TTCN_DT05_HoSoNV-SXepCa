# Đặc tả yêu cầu rút gọn

## Hồ sơ nhân viên và xếp ca cho chi nhánh nhà hàng

**Đề tài DT05 | Nhóm N01 | Phiên bản 0.1 | Ngày 12/11/2026**

**Thực hiện:** Nguyễn Hữu Hiệp và Lê Thành Chung. **Trạng thái:** Trình duyệt M2; các quyết định Q1–Q6 chờ xác nhận nghiệp vụ.

## 1 Mục tiêu và phạm vi

Ứng dụng web hỗ trợ quản lý chi nhánh lưu hồ sơ nhân viên, xác định nhu cầu nhân sự và phân công ca có kiểm tra điều kiện. Nhân viên xem lịch cá nhân đã công bố, gửi đề nghị hoán đổi và theo dõi kết quả. Mục tiêu là ngăn phân công không hợp lệ, thể hiện rõ số người còn thiếu và giữ lịch nhất quán khi công bố hoặc đổi ca.

**Trong phạm vi:** đăng nhập và phân quyền theo chi nhánh; hồ sơ, giấy tờ và đào tạo vệ sinh; nhu cầu theo vị trí; ca nháp và phân công thủ công; kiểm tra hồ sơ, trùng giờ, tổng giờ, nghỉ giữa hai ca và Chủ nhật; công bố, lịch cá nhân; gửi, duyệt hoặc từ chối hoán đổi hai ca cùng chi nhánh; lưu dấu vết quyết định.

**Ngoài phạm vi kỳ này:** tối ưu xếp ca tự động, chấm công, tính lương, ứng dụng di động riêng, lưu bản scan hồ sơ và triển khai Internet. Ca gãy, cơ chế bù bình quân, nghỉ bù, ngoại lệ ngành, đổi xuyên chi nhánh và điều chỉnh khẩn cấp sau công bố cần được chốt riêng trước khi bổ sung.

**Mốc thực hiện:** M3 gồm YC01–YC09, kết thúc ở công bố và xem lịch; M4 bổ sung YC10–YC11 cùng các trường hợp đặc biệt; M5 kiểm thử và tái lập trên hai máy; M6 báo cáo và trình diễn.

### Tác nhân và giới hạn quyền

| Tác nhân | Quyền nghiệp vụ | Giới hạn bắt buộc |
|---|---|---|
| Quản lý chi nhánh | Sửa hồ sơ thuộc chi nhánh chủ quản; lập ca, phân công, công bố và duyệt đổi tại chi nhánh được giao. | Với nhân viên được chia sẻ, chỉ xem tên, vị trí đủ điều kiện và lý do cần cho phân công; không sửa hồ sơ chi tiết của chi nhánh khác. |
| Nhân viên | Xem lịch đã công bố của chính mình, gửi đơn bằng phân công mình sở hữu và xem kết quả đơn có liên quan. | Không tự sửa lịch, duyệt đơn, xem lịch riêng hoặc hồ sơ chi tiết của người khác. |
| Quản trị kỹ thuật | Tạo tài khoản, gán vai trò, phạm vi quản lý và cấu hình danh mục. | Tài khoản cài đặt tách khỏi tài khoản thử phân quyền. Thay đổi nghiệp vụ phải tuân theo cùng dịch vụ và giao dịch kiểm tra. |

### Thuật ngữ và quy trình chính

**Ca** là một khoảng thời gian tại một chi nhánh, cho một vị trí và một số lượng người cần. **Phân công** là một chỗ trong ca gắn với một nhân viên. **Minh chứng** là thông tin giấy tờ hoặc đào tạo đã được xác minh. **Lịch dự kiến** là lịch sau khi giả lập toàn bộ thay đổi để kiểm tra trước khi ghi.

Quản lý chuẩn bị hồ sơ và nhu cầu → tạo ca nháp → chọn nhân viên → hệ thống kiểm tra → lưu phân công hợp lệ → kiểm lại toàn ca và công bố → nhân viên xem lịch → gửi đơn hoán đổi → quản lý kiểm tra, quyết định → hai bên xem kết quả.

<!-- PAGE_BREAK -->

## 2 Yêu cầu chức năng

Mỗi yêu cầu phải được kiểm tra phía máy chủ. Kết quả thành công phải còn đúng sau khi tải lại trang; thao tác bị chặn phải giữ nguyên dữ liệu nghiệp vụ. Mã T dẫn đến kịch bản nghiệm thu tại mục 6.

| Mã | Yêu cầu và kết quả chấp nhận | Mốc | Kiểm thử |
|---|---|---|---|
| YC01 | Đăng nhập xác định đúng vai trò và phạm vi chi nhánh. Kiểm quyền cho cả đọc và ghi; từ chối truy cập trực tiếp hoặc sửa tham số để vượt quyền. | M3 | T08, T11 |
| YC02 | Tạo, sửa hồ sơ gồm mã duy nhất, tên hiển thị, trạng thái, ngày bắt đầu, chi nhánh chính và các nơi được nhận ca. Chặn phân mới cho nhân viên ngừng hoạt động. | M3 | T11 |
| YC03 | Lưu loại giấy, ngày cấp, ngày hiệu lực, ngày hết hạn và người xác minh. Giấy bắt buộc phải phủ toàn ca; khi hết hạn phải chỉ rõ loại giấy, hạn và phần cần bổ sung. | M3 | T02, T13 |
| YC04 | Lưu riêng chứng nhận vệ sinh ban đầu và hướng dẫn lại, ngày thực hiện, hiệu lực nếu có. Chặn khi thiếu loại đào tạo bắt buộc và nêu rõ loại còn thiếu. | M3 | T03 |
| YC05 | Tạo ca theo chi nhánh, vị trí, giờ bắt đầu/kết thúc, một khoảng nghỉ tùy chọn và số người cần. Lịch tuần hiển thị số đã xếp/cần và trạng thái; dữ liệu không hợp lệ trả lỗi đúng trường. | M3 | T01, T12 |
| YC06 | Thêm hoặc bỏ người ở ca nháp. Khi thêm, kiểm điều kiện, quyền nhận ca, trùng người, trùng giờ và sức chứa. Số phân công cập nhật chính xác sau khi lưu và tải lại. | M3 | T01, T04, T14 |
| YC07 | Kiểm tổng phút làm và khoảng nghỉ với ca trước lẫn ca sau ở mọi chi nhánh. Khi vi phạm, nêu số thực tế và ngưỡng; tính đúng nghỉ nội ca và ca qua ngày. | M3 | T05, T06, T13 |
| YC08 | Khi thay đổi ảnh hưởng Chủ nhật, kiểm số Chủ nhật nghỉ dự kiến cho từng năm bị tác động. Phân biệt dưới ngưỡng với thiếu lịch nền; cả hai trường hợp đều chặn ghi. | M3 | T07 |
| YC09 | Chỉ công bố ca đủ người và mọi phân công còn hợp lệ tại thời điểm công bố. Ghi người, thời điểm công bố; khi lỗi ca vẫn nháp. Lịch cá nhân lọc theo tuần và tài khoản đăng nhập. | M3 | T01, T08, T12 |
| YC10 | Nhân viên chọn ca tương lai đã công bố của mình và nhập mã phân công đối tác tại ca khác cùng chi nhánh. Lưu hai phân công, chủ sở hữu gốc, người và thời điểm gửi. Chặn đơn chờ trùng cặp kể cả đảo thứ tự. | M4 | T09, T15 |
| YC11 | Quản lý duyệt bằng dữ liệu mới nhất, kiểm lịch dự kiến của cả hai người và đổi cả hai trong một giao dịch. Từ chối phải ghi lý do. Lưu người, thời điểm quyết định; hai bên thấy kết quả, xử lý lặp không đổi lần hai. | M4 | T09, T10, T14, T15 |

### Luồng phân công và công bố

Quản lý mở ca thuộc phạm vi của mình, chọn người được phép nhận ca rồi gửi yêu cầu. Hệ thống đọc lại dữ liệu, kiểm điều kiện và sức chứa. Khi đạt, lưu phân công và hiển thị số đã xếp/cần; khi chưa đạt, trả lý do và giữ nguyên số người. Công bố là thao tác riêng, phải kiểm lại toàn ca dù các phân công trước đó đã hợp lệ.

### Luồng hoán đổi

Hai nhân viên trao đổi mã phân công; một người gửi đơn. Đơn chờ chưa đổi lịch. Quản lý xem lịch trước/sau dự kiến, duyệt hoặc từ chối. Nếu ca đã bắt đầu, chủ sở hữu đã thay đổi hoặc một người không đạt quy tắc, thao tác duyệt thất bại, đơn vẫn chờ và lịch giữ nguyên. Quản lý có thể từ chối kèm lý do.

<!-- PAGE_BREAK -->

## 3 Quy tắc nghiệp vụ

Các quy tắc Q1–Q6 dưới đây là phương án mô phỏng trình M2. Ngưỡng 480 phút, 660 phút và 15 Chủ nhật chưa phải quyết định nghiệp vụ đã được phê duyệt. Phạm vi mô phỏng áp dụng cho nhân viên trưởng thành.

### Q1 Điều kiện hồ sơ

Nhân viên phải đang hoạt động, được nhận ca tại chi nhánh và có đủ loại minh chứng theo vị trí. Hồ sơ phải còn hiệu lực từ ngày đầu đến hết ngày địa phương cuối cùng thực sự làm. Ngày hết hạn được tính bao gồm ngày đó; ca kết thúc đúng 00:00 không sử dụng ngày tiếp theo. Loại yêu cầu có hạn không được để trống hạn; thiếu thông tin để xác minh phải yêu cầu bổ sung.

Vị trí BEP trong bộ mẫu yêu cầu GIAY_BEP, IFSG_DAU và IFSG_NHAC. Chứng nhận ban đầu, hướng dẫn lại và ngày bắt đầu làm được ghi riêng. Người có trách nhiệm xác minh hồ sơ được chốt tại Q1.

### Q2 Thời gian làm và nghỉ

Hiển thị theo Europe/Berlin, lưu thời điểm theo UTC và tính phút đã trôi qua. Khoảng ca là [bắt đầu, kết thúc); hai ca chỉ chạm đầu mút không trùng giờ nhưng vẫn phải kiểm nghỉ. Giờ địa phương bị lặp hoặc không tồn tại khi đổi giờ mùa phải được làm rõ bằng độ lệch UTC hoặc sửa dữ liệu.

Trần demo là **480 phút làm thực cho cả ca và tổng từng ngày địa phương**; giữa hai ca riêng phải nghỉ ít nhất **660 phút**. Kiểm cả ca liền trước và liền sau, gồm ca nháp lẫn đã công bố ở mọi chi nhánh. Khoảng nghỉ vẫn thuộc ca khi xét trùng giờ; khi cộng phút làm phải trừ nghỉ đúng ngày. Ví dụ 09:00–17:30 nghỉ 30 phút là 480 phút; kết thúc 17:31 là 481 phút và bị chặn.

### Q3 Chủ nhật

Chỉ yêu cầu lịch nền cho những năm có Chủ nhật bị tác động bởi thay đổi. Mỗi Chủ nhật của năm cần một hàng xác nhận có hoặc không có làm việc ngoài ca ứng dụng. Một ngày được tính là làm nếu lịch nền ghi có làm hoặc lịch dự kiến có phút làm thực; nhiều ca cùng ngày chỉ tính một lần.

Sau thay đổi, mỗi năm bị tác động phải còn ít nhất **15 Chủ nhật nghỉ**. Thiếu hàng nền trả NEED_DATA; đủ dữ liệu nhưng dưới ngưỡng thì chặn. Khi đổi ca phải xét cả ngày bị bỏ lẫn ngày được thêm, kể cả hai năm. Dữ liệu nền không được đếm trùng phần ca ứng dụng quản lý.

### Q4 Ca nháp và công bố

Một ca chỉ có một vị trí, nhu cầu là số nguyên dương, giờ kết thúc sau giờ bắt đầu. Nếu có nghỉ thì phải đủ hai đầu, nằm trong ca và ngắn hơn ca. Ca nháp có thể thiếu người; thêm vượt sức chứa hoặc trùng nhân viên bị chặn. Sửa giờ, vị trí, nhu cầu hoặc khoảng nghỉ của ca đã có người phải kiểm lại các phân công bị ảnh hưởng.

Chỉ công bố khi số người bằng nhu cầu và mọi người đạt điều kiện. Ca đã công bố cố định thời gian, vị trí và nhu cầu; thay nhân sự trong bản đầu qua luồng hoán đổi. Khi hồ sơ thay đổi làm ca sắp tới cần rà soát, hiển thị cảnh báo cho quản lý; quy trình xử lý khẩn cấp chờ Q4.

### Q5 Điều kiện hoán đổi

Hai phân công phải thuộc hai ca khác nhau, hai nhân viên khác nhau, cùng chi nhánh, đã công bố và chưa bắt đầu. Người gửi sở hữu phân công thứ nhất. Khi duyệt phải kiểm chủ sở hữu gốc và dựng lịch sau khi thay cả hai người trước khi đánh giá; không được tạo trùng phân công ở ca đích. Số người mỗi ca giữ nguyên.

### Q6 Phạm vi quản lý

Một nhân viên có một chi nhánh chủ quản và có thể được nhận ca ở nhiều chi nhánh. Quyền sửa hồ sơ dựa trên chi nhánh chủ quản; quyền phân công và duyệt dựa trên chi nhánh của ca. Kiểm xung đột toàn bộ lịch nhưng chỉ trả chi tiết thuộc phạm vi được xem, chẳng hạn “trùng lịch ở chi nhánh khác”.

<!-- PAGE_BREAK -->

## 4 Dữ liệu và trạng thái

### Dữ liệu tối thiểu

| Nhóm dữ liệu | Model | Nội dung và ràng buộc chính |
|---|---|---|
| Danh mục và quyền | Branch, Position, ManagerBranch | Mã chi nhánh/vị trí duy nhất; cặp quản lý–chi nhánh duy nhất. Dùng User và Group của Django cho tài khoản, vai trò. |
| Hồ sơ nhân viên | Employee, EmployeeBranch | Mã, tên, ngày bắt đầu, trạng thái, chi nhánh chính; tài khoản liên kết tối đa một hồ sơ; danh sách nơi được nhận ca gồm chi nhánh chính. |
| Điều kiện và minh chứng | EvidenceType, PositionRequirement, Evidence | Loại giấy/đào tạo bắt buộc theo vị trí; ngày cấp, thời gian hiệu lực, mã chứng từ và người xác minh. Cho phép lưu nhiều lần gia hạn. |
| Lịch nền Chủ nhật | SundayBaseline | Nhân viên, ngày Chủ nhật, có làm bên ngoài hay không; duy nhất theo nhân viên và ngày. Thiếu bản ghi nghĩa là chưa biết. |
| Ca và phân công | Shift, Assignment | Ca có mã, chi nhánh, vị trí, giờ, nghỉ, nhu cầu, trạng thái và thông tin công bố. Mỗi cặp ca–nhân viên duy nhất; mã chia sẻ khó đoán, duy nhất và giữ ổn định khi đổi chủ. |
| Đơn đổi ca | SwapRequest | Hai phân công và chủ sở hữu gốc, người/lúc gửi, trạng thái, người/lúc quyết định, lý do từ chối. Không xóa lịch sử khi đổi. |
| Điều phối giao dịch | ScheduleGate | Một hàng id=1 để thống nhất khóa ghi lịch trong bản demo. |

Hồ sơ đã được tham chiếu phải được bảo vệ bằng khóa ngoại; nhân viên nghỉ việc chuyển sang ngừng hoạt động. Dữ liệu thử là hư cấu. Thông tin kết nối, khóa ứng dụng, mật khẩu và bản sao lưu nằm ngoài Git.

### Chuyển trạng thái

| Đối tượng | Sự kiện hợp lệ | Trạng thái sau và dữ liệu giữ lại |
|---|---|---|
| Shift DRAFT | Phân công, bỏ người hoặc sửa ca hợp lệ | Vẫn DRAFT; đọc lại số người từ cơ sở dữ liệu. |
| Shift DRAFT | Công bố đủ điều kiện | PUBLISHED; lưu người và thời điểm công bố. Công bố lặp trả trạng thái hiện có. |
| SwapRequest PENDING | Duyệt đạt điều kiện | APPROVED; đổi hai chủ sở hữu và ghi quyết định cùng giao dịch. |
| SwapRequest PENDING | Từ chối có lý do | REJECTED; lưu quyết định, giữ lịch. |
| SwapRequest PENDING | Duyệt thất bại | Vẫn PENDING; giữ nguyên cả hai lịch và trả nguyên nhân. |
| Đơn đã quyết định | Gửi lại thao tác xử lý | Trả kết quả đã lưu, không áp dụng lần hai. |

### Kết quả kiểm tra và thông báo

**OK:** đủ điều kiện. **BLOCKED:** có vi phạm xác định. **NEED_DATA:** thiếu dữ liệu để kết luận. Nếu vừa có vi phạm vừa thiếu dữ liệu, trả BLOCKED và các lý do được phép hiển thị. Cả BLOCKED lẫn NEED_DATA đều không ghi thay đổi phân công. Dữ liệu sai định dạng trả lỗi trường trước bước kiểm nghiệp vụ.

Mã lỗi giữ thống nhất: DOCUMENT_EXPIRED, EVIDENCE_MISSING, OVERLAP, REST_SHORT, HOURS_EXCEEDED, SUNDAY_DATA_MISSING, SUNDAY_QUOTA, CAPACITY_FULL, HEADCOUNT_MISMATCH. Thông báo cần có nguyên nhân, dữ liệu thực tế/ngưỡng khi phù hợp và việc người dùng có thể thực hiện tiếp.

<!-- PAGE_BREAK -->

## 5 Yêu cầu chất lượng và giao diện

### Yêu cầu chất lượng

| Mã | Yêu cầu bắt buộc | Cách xác minh |
|---|---|---|
| CL01 | Bảo vệ lịch cá nhân, hồ sơ và phạm vi chi nhánh. Kiểm tài khoản, vai trò, quyền đối tượng cho GET lẫn POST; thông báo liên chi nhánh chỉ tiết lộ phần cần thiết. | T08, T11 bằng tài khoản nhân viên và hai quản lý khác chi nhánh; thử sửa URL và dữ liệu gửi. |
| CL02 | Một quyết định chỉ có hiệu lực một lần. Thao tác đồng thời không vượt sức chứa, không đổi một nửa và không ghi đè chủ sở hữu mới. | T14 bằng hai phiên SQL Server độc lập; đọc lại dữ liệu sau commit và sau lỗi mô phỏng. |
| CL03 | Truy được người/lúc công bố, gửi đơn, duyệt hoặc từ chối; nhận biết hai phân công và chủ sở hữu trước khi đổi. | T09, T10: đối chiếu trạng thái, lịch và thông tin quyết định trước/sau xử lý. |
| CL04 | Cài đặt và khởi tạo lại được từ repo, migration, bộ mẫu trên hai máy. Seed lặp an toàn; dữ liệu khác gây xung đột phải báo rõ và rollback lần nạp. | Ở M5, đối chiếu số bản ghi và T01/T02 trên hai máy; nạp lần hai không tạo thêm. |
| CL05 | Hiển thị ngày giờ Đức, ngày kết thúc với ca qua đêm, số đã xếp/cần và lý do bị chặn rõ ràng bằng chữ/số. | T02, T07, T13: người thử chỉ ra được hồ sơ cần bổ sung và ca chưa công bố. |

### Nhất quán khi ghi dữ liệu

Mọi đường ghi làm thay đổi điều kiện xếp lịch phải dùng chung dịch vụ nghiệp vụ và quy ước khóa, gồm cả sửa hồ sơ, quyền nhận ca và lịch nền. Thiết kế demo mở transaction.atomic(), khóa ScheduleGate(id=1) bằng UPDLOCK, HOLDLOCK rồi đọc lại quyền, hồ sơ, lịch, sức chứa, trạng thái và chủ sở hữu trước khi ghi.

Khi duyệt đổi, ghi cả hai phân công và quyết định trong một giao dịch. Lỗi ở bất kỳ bước nào phải rollback toàn bộ; lịch hiển thị sau thành công phải lấy từ truy vấn mới. Trang quản trị kỹ thuật chỉ đọc bảng nghiệp vụ hoặc gọi cùng dịch vụ ghi. Các hàm thống nhất trong thiết kế gồm evaluate_assignment, assign_employee, remove_assignment, publish_shift, request_swap và decide_swap.

### Màn hình và thông tin trao đổi

**Quản lý:** đăng nhập; danh sách/chi tiết hồ sơ và minh chứng; lịch tuần của chi nhánh; tạo/chi tiết ca với các thao tác phân công, bỏ người, công bố; danh sách/chi tiết đơn đổi và nút duyệt/từ chối. Trước khi quyết định đổi phải thấy lịch dự kiến của cả hai người.

**Nhân viên:** đăng nhập; lịch cá nhân theo tuần; mã phân công của mình ở ca tương lai; form nhập mã đối tác và gửi đơn; danh sách đơn liên quan với trạng thái, kết quả và lý do từ chối. Không cho chọn tùy ý người khác để xem lịch cá nhân.

Form phải kiểm dữ liệu trên máy chủ, dùng session auth và CSRF cho thao tác ghi. Gửi thành công chuyển về trang đọc kết quả để tải lại không vô tình gửi lại biểu mẫu. Thông báo vượt quyền không được làm lộ hồ sơ hoặc chi tiết lịch ngoài phạm vi.

### Môi trường và giới hạn vận hành

Windows/PowerShell, Python 3.13, Django 5.2, SQL Server qua mssql-django và ODBC 17/18; mỗi máy dùng cấu hình .env riêng. Bản đầu phục vụ quy mô demo ít người dùng, thao tác ghi có thể chờ khóa chung. Chỉ tiêu hiệu năng định lượng và tải triển khai thực tế cần thỏa thuận trước khi mở rộng phạm vi.

<!-- PAGE_BREAK -->

## 6 Nghiệm thu và quyết định còn mở

### Dữ liệu và tiêu chí nghiệm thu

Dùng mẫu hư cấu gồm **2 chi nhánh, 5 nhân viên, 4 ca, 14 minh chứng, 1 phân công**; CA01 nháp cần 2 người, CA03 đã công bố có NV04. NV01 được nhận ca tại hai chi nhánh; NV02 có GIAY_BEP hết hạn 22/11/2026; NV03 thiếu IFSG_NHAC. NV01 có 52 hàng Chủ nhật năm 2026, trong đó 15 ngày nghỉ. Mỗi bài thử khôi phục mẫu gốc và dùng ngày mô phỏng 20/11/2026 hoặc đồng bộ lại toàn bộ ngày mẫu.

| Mã | Kết quả tối thiểu phải quan sát được |
|---|---|
| T01 | Thêm NV01 và NV05 vào CA01: 0/2 → 1/2 → 2/2; công bố xong hai người thấy ca. |
| T02 | NV02 bị chặn vì giấy hết 22/11, số người giữ 0; gia hạn phủ ca thì lưu thành 1/2. |
| T03 | NV03 bị chặn vì thiếu IFSG_NHAC; bổ sung hợp lệ thì phân công được. |
| T04 | NV01 trùng CA01/CA02 ở hai chi nhánh bị chặn; thông báo không lộ lịch ngoài quyền. |
| T05 | Nghỉ 10 giờ 59 phút bị chặn, đủ 11 giờ qua điều kiện nghỉ; thử cả thứ tự nhập đảo. |
| T06 | 480 phút làm đạt, 481 phút bị chặn; kiểm cho một ca và tổng nhiều ca trong ngày. |
| T07 | Quỹ Chủ nhật 15 xuống 14 bị chặn, 16 xuống 15 đạt; thiếu một hàng nền trả NEED_DATA. |
| T08 | Nhân viên không thấy ca nháp và không xem được lịch người khác bằng sửa tham số. |
| T09 | Duyệt đổi CA01/CA03 cập nhật cả hai lịch; duyệt lại không đổi ngược, có dấu vết quyết định. |
| T10 | Giấy mất hiệu lực trước khi duyệt: giữ hai lịch, đơn vẫn chờ; từ chối ghi REJECTED và lý do. |
| T11 | Chặn quản lý CN02 sửa hồ sơ/công bố ca CN01; chặn phân mới cho người ngừng hoạt động. |
| T12 | Chặn giờ/nghỉ/nhu cầu sai; 1/2 người không công bố; ca đủ chỗ không nhận thêm. |
| T13 | Ca 22:00–06:00 nghỉ 23:45–00:15 có 105/345 phút hai ngày; giấy phải phủ ngày 24. |
| T14 | Hai phiên tranh chỗ cuối không vượt nhu cầu; duyệt đồng thời chỉ đổi một lần; lỗi giữa hai lần ghi rollback toàn bộ. |
| T15 | Chặn gửi đơn bằng ca người khác hoặc ca nháp; đơn cũ không đổi chủ sở hữu đã thay đổi. |

Các dòng trên là **kết quả kỳ vọng**. Bản triển khai được nghiệm thu khi các yêu cầu trong phạm vi được duyệt vượt qua ca thử tương ứng, dữ liệu sau thao tác đúng và có bằng chứng. Báo cáo ghi mã T, phiên bản Git, máy/SQL Server, người/lúc chạy, thực tế, đạt/trượt và lỗi cần sửa.

### Nội dung cần xác nhận trước khi chốt M2

**Q1:** người xác minh và cách xác định hiệu lực hồ sơ. **Q2:** ngưỡng giờ/nghỉ, nghỉ nội ca, ca gãy và ngoại lệ. **Q3:** quỹ Chủ nhật, dữ liệu đủ kỳ, phạm vi nghỉ bù. **Q4:** điều chỉnh khẩn cấp và hồ sơ mất hiệu lực sau công bố. **Q5:** có cần đối tác xác nhận trong ứng dụng, có mở đổi xuyên chi nhánh. **Q6:** mức thông tin được chia sẻ cho quản lý chi nhánh nhận người.

Người hướng dẫn và người phụ trách nghiệp vụ ghi quyết định, ngày xác nhận, mã yêu cầu bị ảnh hưởng và người cập nhật tại 05_XAC_NHAN_M2.md. Khi thay đổi phạm vi, cập nhật đồng thời yêu cầu, thiết kế và ca nghiệm thu.

### Tài liệu liên quan

Trong HO_SO_DT05: 02_YEU_CAU.md (YC/CL và phạm vi), 03_THIET_KE.md (dữ liệu và xử lý), 04_NGHIEM_THU.md (bước thử đầy đủ), 05_XAC_NHAN_M2.md (quyết định), du_lieu_mau.json (đầu vào). Quy chiếu mã YC/CL/T của bản này giữ nguyên các tài liệu đó.
