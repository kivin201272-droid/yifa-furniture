const fs = require('fs');
const path = require('path');

const enFiles = [
    'index.html',
    'products/index.html',
    'bedroom/index.html',
    'living-room/index.html',
    'dining/index.html',
    'office/index.html',
    'mattress/index.html',
    'magical-mattress/index.html',
    'about/index.html',
    'faq/index.html',
    'contact/index.html'
];

enFiles.forEach(relPath => {
    const filePath = path.join(__dirname, relPath);
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');

    const isRoot = relPath === 'index.html';
    const p = isRoot ? './' : '../';

    // 1. Language switch button text: 中文
    html = html.replace(/>ZH<\/a>/g, '>中文</a>');

    // 2. Footer Brand Column
    const oldBrandPattern = /<div class="footer-col footer-brand">[\s\S]*?<\/div><div class=footer-col><h3>/i;
    const newBrandCol = `<div class="footer-col footer-brand"><span class=lg-main>YIFA</span><p style="font-size:0.75rem;letter-spacing:0.1em;color:#bcae93;margin-top:-6px;margin-bottom:8px;">YI FA FURNITURE / YOUR FURNITURE</p><p>Yifa Furniture Inc. — Modern furniture importer and distributor, serving Brooklyn, NY since 2002.</p><p class=footer-contact>6410 8th Ave, Brooklyn, NY<br><a href="tel:+19177715493">917-771-5493</a> </p></div><div class=footer-col><h3>`;
    html = html.replace(oldBrandPattern, newBrandCol);

    // 3. Footer Product Categories
    const oldProductColPattern = /<h3>(Collections|Product Categories)<\/h3><ul>[\s\S]*?<\/ul><\/div><div class=footer-col><h3>Company<\/h3>/i;
    const newProductCol = `<h3>Collections</h3><ul><li><a href=${p}products/>All Collections</a></li><li><a href=${p}mattress/>Classic Mattress</a></li><li><a href=${p}magical-mattress/>Magical Mattress</a></li><li><a href=${p}living-room/>Living Room</a></li><li><a href=${p}dining/>Dining Room</a></li><li><a href=${p}bedroom/>Bedroom</a></li><li><a href=${p}office/>Office</a></li></ul></div><div class=footer-col><h3>Company</h3>`;
    html = html.replace(oldProductColPattern, newProductCol);

    // 4. Showroom hours
    const oldShowroomPattern = /<h3>Visit Showroom<\/h3><ul>[\s\S]*?<\/ul><\/div>/i;
    const newShowroomCol = `<h3>Visit Showroom</h3><ul><li>Mon–Fri: 9:00 AM – 5:30 PM</li><li>Sat & Sun: Closed</li><li><a href="https://www.google.com/maps/search/?api=1&amp;query=6410+8th+Ave+Brooklyn+NY+11220" target=_blank rel=noopener>Get Directions</a></li></ul></div>`;
    html = html.replace(oldShowroomPattern, newShowroomCol);

    // 5. Footer copyright
    html = html.replace(/&copy; <span id=yr>\d+<\/span> [^<]*<\/span>/, `&copy; <span id=yr>2026</span> Yifa Furniture Inc.</span>`);
    html = html.replace(/© <span id=yr>\d+<\/span> [^<]*<\/span>/, `© <span id=yr>2026</span> Yifa Furniture Inc.</span>`);

    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Successfully updated EN ${relPath}`);
});
