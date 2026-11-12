// node xuat_diagram.cjs <plantuml.jar> <node_modules> [java.exe]
// Node modules cần có sharp; Java/Graphviz do PlantUML sử dụng.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const [jar, modules, java = 'java'] = process.argv.slice(2);
if (!jar || !modules) {
  console.error('Cách dùng: node xuat_diagram.cjs <plantuml.jar> <node_modules> [java.exe]');
  process.exit(1);
}
const sharp = require(path.join(path.resolve(modules), 'sharp'));
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'danh_muc.json'), 'utf8'));
const sources = manifest.map(d => path.join(__dirname, d.file + '.puml'));
execFileSync(java, [
  '-Djava.awt.headless=true', '-jar', path.resolve(jar),
  '-failfast2', '-charset', 'UTF-8', '-tsvg', ...sources
], { stdio: 'inherit' });
const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
(async () => {
  for (const d of manifest) {
    const base = path.join(__dirname, d.file);
    const svg = fs.readFileSync(base + '.svg', 'utf8');
    if (svg.includes('Syntax Error')) throw new Error('PlantUML lỗi: ' + d.file);
    await sharp(Buffer.from(svg), { density: 216 }).flatten({ background: 'white' }).png().toFile(base + '.png');
    const size = await sharp(base + '.png').metadata();
    if (d.page === 'auto') {
      d.page = size.width / size.height > 1.32 ? 'landscape' : 'portrait';
    }
    console.log(d.file + ': ' + size.width + ' x ' + size.height);
  }
  const html = `<!doctype html>
<html lang="vi">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DT05 · Bộ sơ đồ báo cáo</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#edf2f4;color:#193141;font:16px/1.55 Arial,sans-serif}
main{max-width:1280px;margin:auto;padding:24px}header,figure{margin:0 0 22px;padding:28px;background:white;border:1px solid #cedade}
h1,h2{line-height:1.25;margin:0 0 12px}small{font-weight:bold;color:#296259}a{color:#165d88}
nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:6px}
.visual{overflow:auto;display:flex;justify-content:center}img{display:block;max-width:100%;height:auto;max-height:1150px;margin:24px auto}
figcaption{border-top:1px solid #d3dfe0;padding-top:12px}.links{margin-top:8px}
@page{size:A4 landscape;margin:12mm}@page portraitDiagram{size:A4 portrait;margin:12mm}
@media print{
body,main{background:white;margin:0;padding:0}header,.links{display:none}
figure{border:0;padding:0;margin:0;break-inside:avoid;break-after:page}
figure:last-child{break-after:auto}figure.portrait{page:portraitDiagram}
.visual{overflow:visible}figure img{max-width:100%;max-height:142mm;margin:3mm auto}
figure.portrait img{max-height:222mm}h2{font-size:14pt}small,figcaption{font-size:9pt}
}
</style></head>
<body><main><header><small>DT05 / NHÓM N01</small><h1>Hồ sơ nhân viên và xếp ca</h1>
<p>Bộ 13 sơ đồ chính dùng cho báo cáo DT05. ERD theo model hiện hành; Use Case, hoạt động, trạng thái và tương tác theo thiết kế đề xuất.</p>
<p><a href="README.md">Hướng dẫn và chú thích</a> · <a href="QUY_UOC_SO_DO.md">Quy ước đối chiếu sơ đồ</a></p>
<nav>${manifest.map((d,i) => '<a href="#h'+(i+1)+'">'+(i+1)+'. '+escape(d.title)+'</a>').join('')}</nav>
<p>Nhấn vào hình để mở SVG ở kích thước đầy đủ. Dùng chức năng in của trình duyệt để in mỗi sơ đồ trên một trang.</p></header>
${manifest.map((d,i) => '<figure id="h'+(i+1)+'" class="'+d.page+'"><small>DT05 / '+(i===4||i===5?'MÔ HÌNH DỮ LIỆU HIỆN HÀNH':'THIẾT KẾ ĐỀ XUẤT')+'</small><h2>Hình '+(i+1)+'. '+escape(d.title)+'</h2><div class="visual"><a href="'+d.file+'.svg"><img src="'+d.file+'.svg" alt="'+escape(d.title)+'"></a></div><figcaption>'+escape(d.caption)+'</figcaption><p class="links"><a href="'+d.file+'.svg">SVG</a> · <a href="'+d.file+'.png">PNG</a> · <a href="'+d.file+'.puml">Nguồn PlantUML</a></p></figure>').join('\n')}
</main></body></html>`;
  fs.writeFileSync(path.join(__dirname, 'index.html'), html + '\n');
})().catch(error => { console.error(error); process.exitCode = 1; });
