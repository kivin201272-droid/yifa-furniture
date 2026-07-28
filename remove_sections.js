const fs = require('fs');
const path = require('path');

function removeSection(html, startComment, endComment) {
    const regex = new RegExp(`${startComment}[\\s\\S]*?${endComment}`, 'g');
    return html.replace(regex, '');
}

function processFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Remove Services Section (Homepage)
    html = removeSection(html, '<!-- Services Section -->', '</section>');

    // Remove Categories Sections (Category pages)
    html = removeSection(html, '<!-- Categories Section -->', '</section>');

    // Remove Quote CTA Section (Category pages)
    html = removeSection(html, '<!-- Quote CTA Section -->', '</section>');
    html = removeSection(html, '<!-- CTA Section -->', '</section>');

    // Fix 'of' in About Section (Homepage)
    html = html.replace('拥有二十年丰富经验 of 纽约家具进口商', '拥有二十年丰富经验的纽约家具进口商');
    
    // Also check for English 'of' if it was just 'of' instead of '的'
    html = html.replace('丰富经验 of 纽约', '丰富经验的纽约');

    // Fix office collection image (Products page or Homepage)
    html = html.replace(/src="[^"]*office-collection\.jpg"/g, 'src="assets/images/pdf7/img-000.jpg"');
    html = html.replace(/src="[^"]*office-collection\.webp"/g, 'src="assets/images/pdf7/img-000.jpg"');
    // Also if path is relative
    html = html.replace(/src="\.\.\/assets\/images\/office-collection\.jpg"/g, 'src="../assets/images/pdf7/img-000.jpg"');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
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
