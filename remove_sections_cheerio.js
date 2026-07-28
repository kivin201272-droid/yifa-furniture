const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

function processFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    const $ = cheerio.load(html, { decodeEntities: false });
    let modified = false;

    // Homepage: Remove Services Section
    const servicesTitle = $('h2:contains("我们的服务"), h2:contains("Our Services")').closest('section');
    if (servicesTitle.length > 0) {
        servicesTitle.remove();
        modified = true;
    }

    // Category Pages: Remove "Categories" / "包含品类" section
    const categoriesTitle = $('h2:contains("包含品类"), h2:contains("Categories")').closest('section');
    if (categoriesTitle.length > 0) {
        categoriesTitle.remove();
        modified = true;
    }

    // Category Pages: Remove "Mattress" / "床垫系列完善整套" section
    const mattressTitle = $('h2:contains("床垫系列完善整套"), h2:contains("Mattresses Complete the Suite")').closest('section');
    if (mattressTitle.length > 0) {
        mattressTitle.remove();
        modified = true;
    }

    // Category Pages: Remove Quote CTA section
    const ctaTitle = $('h2:contains("索取卧室系列报价及库存"), h2:contains("索取客厅系列报价及库存"), h2:contains("索取办公系列报价及库存"), h2:contains("索取餐厅系列报价及库存"), h2:contains("Request Bedroom Quote"), h2:contains("Request Living Room Quote"), h2:contains("Request Office Quote"), h2:contains("Request Dining Quote")').closest('section');
    if (ctaTitle.length > 0) {
        ctaTitle.remove();
        modified = true;
    }

    // Since the CTA for quote is standard for all collections:
    const ctaGeneral = $('.cta-band').closest('section');
    if (ctaGeneral.length > 0) {
        ctaGeneral.remove();
        modified = true;
    }

    // Fix 'of' in About Section
    let newHtml = $.html();
    let textModified = newHtml.replace(/拥有二十年丰富经验\s*of\s*纽约家具进口商/g, '拥有二十年丰富经验的纽约家具进口商');
    textModified = textModified.replace(/丰富经验\s*of\s*纽约/g, '丰富经验的纽约');
    
    // Fix office collection image
    textModified = textModified.replace(/src="[^"]*office-collection\.(jpg|webp)"/g, 'src="assets/images/pdf7/img-000.jpg"');
    textModified = textModified.replace(/src="\.\.\/assets\/images\/office-collection\.(jpg|webp)"/g, 'src="../assets/images/pdf7/img-000.jpg"');
    textModified = textModified.replace(/src="\.\.\/\.\.\/assets\/images\/office-collection\.(jpg|webp)"/g, 'src="../../assets/images/pdf7/img-000.jpg"');

    if (textModified !== original || modified) {
        fs.writeFileSync(filePath, textModified);
        console.log(`Updated ${filePath}`);
    }
}

const filesToProcess = [
    'index.html',
    'zh/index.html',
    'products/index.html',
    'zh/products/index.html',
    'bedroom/index.html',
    'zh/bedroom/index.html',
    'living-room/index.html',
    'zh/living-room/index.html',
    'dining/index.html',
    'zh/dining/index.html',
    'office/index.html',
    'zh/office/index.html',
    'mattress/index.html',
    'zh/mattress/index.html'
];

filesToProcess.forEach(file => processFile(path.join(__dirname, file)));
