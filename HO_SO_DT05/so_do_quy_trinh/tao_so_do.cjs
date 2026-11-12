// Tạo lại SVG, PNG, DOT và Mermaid từ cùng một mô tả quy trình.
// node tao_so_do.cjs <thư mục node_modules có @viz-js/viz và sharp>
const fs = require('fs');
const path = require('path');
const modules = process.argv[2];
if (!modules) throw new Error('Cần truyền đường dẫn node_modules có @viz-js/viz và sharp.');
const { instance } = require(path.join(modules, '@viz-js/viz'));
const sharp = require(path.join(modules, 'sharp'));
const charts = [
  {
    file: '01_tong_quan', title: 'QUY TRÌNH TỔNG QUAN',
    subtitle: 'Hồ sơ nhân viên và xếp ca · Nhóm N01 · Quy trình đề xuất',
    nodes: [
      ['a','Bắt đầu','end'],
      ['b','Quản lý: cập nhật hồ sơ nhân viên\nvà yêu cầu minh chứng theo vị trí'],
      ['c','Quản lý: tạo ca nháp\nChi nhánh · vị trí · giờ · số người cần'],
      ['d','Quản lý: chọn nhân viên\nHệ thống kiểm tra trước khi lưu'],
      ['e','Hợp lệ và còn chỗ?','decision'],
      ['f','Hiển thị lý do; giữ nguyên phân công\nQuản lý bổ sung dữ liệu hoặc chọn lại','error'],
      ['g','Lưu phân công\nCập nhật số đã xếp / số cần'],
      ['h','Đủ số người?','decision'],
      ['i','Quản lý: yêu cầu công bố\nHệ thống kiểm tra lại toàn ca'],
      ['j','Toàn ca đạt?','decision'],
      ['k','Công bố lịch\nNhân viên xem lịch cá nhân','success'],
      ['l','Có nhu cầu đổi ca?','decision'],
      ['m','Nhân viên: gửi đơn đổi hai ca\nQuản lý: duyệt hoặc từ chối\nTheo quy trình chi tiết ở Hình 3'],
      ['n','Nhân viên xem lịch và kết quả xử lý'],
      ['o','Kết thúc lượt xử lý','end'],
    ],
    edges: [['a','b'],['b','c'],['c','d'],['d','e'],['e','f','Không'],['f','d','Sửa / chọn lại'],['e','g','Có'],['g','h'],['h','d','Chưa đủ'],['h','i','Đủ'],['i','j'],['j','f','Chưa đạt'],['j','k','Đạt'],['k','l'],['l','m','Có'],['l','o','Không'],['m','n'],['n','o']],
  },
  {
    file: '02_phan_cong_cong_bo', title: 'PHÂN CÔNG VÀ CÔNG BỐ CA',
    subtitle: 'Quản lý chi nhánh và hệ thống · YC03–YC09 · Quy trình đề xuất',
    nodes: [
      ['a','Quản lý chọn nhân viên và ca nháp','end'],
      ['b','Hệ thống kiểm tra quyền và dữ liệu\nĐọc lại dữ liệu trong giao dịch'],
      ['c','Đúng quyền, ca nháp\nvà còn chỗ?','decision'],
      ['d','Đánh giá nhân viên trên lịch dự kiến\n• Hoạt động, được làm tại chi nhánh\n• Đủ hồ sơ / đào tạo, hiệu lực suốt ca\n• Không trùng lịch ở mọi chi nhánh\n• Đạt giờ làm, nghỉ và quỹ Chủ nhật'],
      ['e','Kết quả đánh giá?','decision'],
      ['f','BLOCKED / NEED_DATA\nNêu lý do hoặc dữ liệu cần bổ sung\nGiữ nguyên phân công','error'],
      ['g','OK: lưu phân công và kết thúc giao dịch\nĐọc lại số đã xếp / số cần','success'],
      ['h','Quản lý yêu cầu công bố ca'],
      ['i','Trong giao dịch mới: đọc lại quyền,\ntrạng thái, số người và điều kiện\ncủa toàn bộ phân công'],
      ['j','Đúng số người\nvà mọi phân công đạt?','decision'],
      ['k','Giữ ca DRAFT (nháp)\nThông báo nội dung cần khắc phục','error'],
      ['l','Lưu PUBLISHED, người và giờ công bố\nNhân viên xem được ca của mình','success'],
      ['m','Kết thúc lượt xử lý','end'],
    ],
    edges: [['a','b'],['b','c'],['c','d','Có'],['c','f','Không'],['d','e'],['e','f','Bị chặn / thiếu dữ liệu'],['e','g','OK'],['f','m'],['g','h','Khi đã chuẩn bị đủ người'],['h','i'],['i','j'],['j','k','Không'],['j','l','Có'],['k','m'],['l','m']],
  },
  {
    file: '03_gui_duyet_doi_ca', title: 'GỬI VÀ DUYỆT ĐỔI CA',
    subtitle: 'Nhân viên · quản lý chi nhánh · hệ thống · YC10–YC11 · Đề xuất',
    nodes: [
      ['a','Nhân viên chọn phân công của mình\nvà nhập mã phân công đối tác','end'],
      ['b','Kiểm quyền sở hữu, hai người / hai ca\nkhác nhau, cùng chi nhánh, ca tương lai\nđã công bố và không trùng cặp đơn chờ'],
      ['c','Yêu cầu hợp lệ?','decision'],
      ['d','Thông báo lỗi\nKhông tạo đơn, giữ nguyên lịch','error'],
      ['e','Lưu đơn PENDING và hai chủ sở hữu gốc\nLịch hiện tại chưa thay đổi'],
      ['f','Quản lý mở đơn, chọn quyết định\nHệ thống kiểm quyền và đọc lại đơn'],
      ['g','Đơn còn PENDING?','decision'],
      ['h','Trả kết quả đã lưu\nKhông thực hiện lần hai'],
      ['i','Quyết định?','decision'],
      ['j','Nhập lý do; lưu REJECTED\nngười và thời điểm; giữ nguyên lịch','error'],
      ['k','Trong cùng giao dịch: kiểm chủ sở hữu,\nca chưa bắt đầu và dựng lịch dự kiến\nsau hoán đổi cho cả hai người'],
      ['l','Cả hai đạt điều kiện\ntrên dữ liệu mới nhất?','decision'],
      ['m','Giữ đơn PENDING và lịch cũ\nTrả lý do; quản lý có thể từ chối','error'],
      ['n','Đổi hai phân công và lưu APPROVED\nngười, thời điểm trong một giao dịch\nLỗi khi ghi: rollback toàn bộ','success'],
      ['o','Hai nhân viên xem kết quả\nvà lịch cá nhân sau xử lý'],
      ['p','Kết thúc lượt xử lý','end'],
    ],
    edges: [['a','b'],['b','c'],['c','d','Không'],['d','p'],['c','e','Có'],['e','f'],['f','g'],['g','h','Đã xử lý'],['h','o'],['g','i','Còn chờ'],['i','j','Từ chối'],['i','k','Duyệt'],['k','l'],['l','m','Không'],['m','p'],['l','n','Có'],['j','o'],['n','o','Ghi thành công'],['o','p']],
  },
];
const quote = x => JSON.stringify(x);
const styles = {
  end: 'shape=oval, fillcolor="#e2e8f0", color="#64748b"',
  decision: 'shape=diamond, fillcolor="#fff4d6", color="#bd831b", margin="0.14,0.08"',
  error: 'shape=box, fillcolor="#fff0ee", color="#c56557"',
  success: 'shape=box, fillcolor="#e5f5ee", color="#3f9072"',
};
(async () => {
  const viz = await instance();
  for (const chart of charts) {
    const dot = `digraph G {
      graph [rankdir=TB, bgcolor="white", pad=0.3, nodesep=0.42, ranksep=0.46,
        labelloc=t, label=${quote(chart.title+'\n'+chart.subtitle)}, fontname="Arial", fontsize=20];
      node [shape=box, style="rounded,filled", fillcolor="#eef4fc", color="#6885aa",
        fontname="Arial", fontsize=13, fontcolor="#172c44", margin="0.20,0.12", penwidth=1.2];
      edge [color="#60758c", arrowsize=0.65, fontname="Arial", fontsize=11, fontcolor="#334155"];
      ${chart.nodes.map(([id,label,type]) => `${id} [label=${quote(label)}${type?', '+styles[type]:''}];`).join('\n')}
      ${chart.edges.map(([a,b,label]) => `${a} -> ${b}${label?' [label='+quote(label)+']':''};`).join('\n')}
    }`;
    const base = path.join(__dirname, chart.file);
    fs.writeFileSync(base+'.dot',dot+'\n');
    const svg = viz.renderString(dot, {format:'svg', engine:'dot'});
    fs.writeFileSync(base+'.svg',svg);
    await sharp(Buffer.from(svg), {density:210}).flatten({background:'#ffffff'}).png().toFile(base+'.png');
    await sharp(base+'.png').resize({width:850}).toFile(base+'_xem_truoc.png');
    const mmd = ['flowchart TD', ...chart.nodes.map(([id,label,type]) => {
      const text = quote(label.replaceAll('\n','<br/>'));
      return `  ${id}${type==='decision'?'{'+text+'}':type==='end'?'(['+text+'])':'['+text+']'}`;
    }), ...chart.edges.map(([a,b,label])=>`  ${a} -->${label?'|'+label+'|':''} ${b}`)].join('\n');
    fs.writeFileSync(base+'.mmd',mmd+'\n');
    const meta = await sharp(base+'.png').metadata();
    console.log(`${chart.file}: ${meta.width} x ${meta.height} px`);
  }
})();
