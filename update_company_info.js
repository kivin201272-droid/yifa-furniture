const fs = require('fs');
const path = require('path');

const zhFiles = [
    'zh/index.html',
    'zh/products/index.html',
    'zh/bedroom/index.html',
    'zh/living-room/index.html',
    'zh/dining/index.html',
    'zh/office/index.html',
    'zh/mattress/index.html',
    'zh/magical-mattress/index.html',
    'zh/about/index.html',
    'zh/faq/index.html',
    'zh/contact/index.html'
];

zhFiles.forEach(relPath => {
    const filePath = path.join(__dirname, relPath);
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');

    const isRootZh = relPath === 'zh/index.html';
    const p = isRootZh ? './' : '../';

    // 1. Header Navigation: 家具系列 -> 产品分类
    html = html.replace(/<a href=([^>]*products\/[^>]*)>家具系列<\/a>/g, '<a href=$1>产品分类</a>');

    // 2. Header Logo alt text
    html = html.replace(/alt="Yifa 家具"/g, 'alt="易发家具"');
    html = html.replace(/alt="Yifa Furniture"/g, 'alt="易发家具"');

    // 3. Language button text (ensure EN)
    html = html.replace(/>English<\/a>/g, '>EN</a>');

    // 4. Footer Brand Column
    const oldBrandPattern = /<div class="footer-col footer-brand">[\s\S]*?<\/div><div class=footer-col><h3>/i;
    const newBrandCol = `<div class="footer-col footer-brand"><span class=lg-main>易发家具</span><p style="font-size:0.75rem;letter-spacing:0.1em;color:#bcae93;margin-top:-6px;margin-bottom:8px;">YI FA FURNITURE / YOUR FURNITURE</p><p>Yifa 家具 Inc. — 现代家具进口商与分销商，自2002年起扎根纽约布鲁克林。</p><p class=footer-contact>6410 8th Ave, 布鲁克林, NY<br><a href="tel:+19177715493">917-771-5493</a> </p></div><div class=footer-col><h3>`;
    html = html.replace(oldBrandPattern, newBrandCol);

    // 5. Footer Category Column Title: <h3>家具系列</h3> -> <h3>产品分类</h3>
    html = html.replace(/<h3>家具系列<\/h3>/g, '<h3>产品分类</h3>');

    // 6. Ensure products list in footer has all categories cleanly
    const oldProductColPattern = /<h3>产品分类<\/h3><ul>[\s\S]*?<\/ul><\/div><div class=footer-col><h3>公司信息<\/h3>/;
    const newProductCol = `<h3>产品分类</h3><ul><li><a href=${p}products/>全部系列</a></li><li><a href=${p}mattress/>经典床垫</a></li><li><a href=${p}magical-mattress/>神奇床垫</a></li><li><a href=${p}living-room/>客厅系列</a></li><li><a href=${p}dining/>餐厅系列</a></li><li><a href=${p}bedroom/>卧室系列</a></li><li><a href=${p}office/>办公系列</a></li></ul></div><div class=footer-col><h3>公司信息</h3>`;
    html = html.replace(oldProductColPattern, newProductCol);

    // 7. Footer 参观展厅 column
    const oldShowroomPattern = /<h3>参观展厅<\/h3><ul>[\s\S]*?<\/ul><\/div>/;
    const newShowroomCol = `<h3>参观展厅</h3><ul><li>周一至周五: 9:00 AM – 5:30 PM</li><li>周六 & 周日: 休息</li><li><a href="https://www.google.com/maps/search/?api=1&amp;query=6410+8th+Ave+布鲁克林+NY+11220" target=_blank rel=noopener>获取路线指引</a></li></ul></div>`;
    html = html.replace(oldShowroomPattern, newShowroomCol);

    // 8. Footer Bottom: © 2026 Yifa 家具 Inc., Privacy, Terms, Accessibility, 技术支持 Tooo.ai
    html = html.replace(/&copy; <span id=yr>\d+<\/span> [^<]*<\/span>/, `&copy; <span id=yr>2026</span> Yifa 家具 Inc.</span>`);
    html = html.replace(/© <span id=yr>\d+<\/span> [^<]*<\/span>/, `© <span id=yr>2026</span> Yifa 家具 Inc.</span>`);

    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Successfully updated ${relPath}`);
});
