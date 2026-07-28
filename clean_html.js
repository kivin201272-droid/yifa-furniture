const fs = require('fs');
const path = require('path');

function processFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Remove Services section (from <section to </section>)
    html = html.replace(/<section[^>]*>[\s\S]*?(?:我们的服务|Our Services)[\s\S]*?<\/section>/g, '');

    // Remove Categories section
    html = html.replace(/<section[^>]*>[\s\S]*?(?:包含品类|Categories)[\s\S]*?<\/section>/g, '');

    // Remove Mattress section (only the informational part)
    html = html.replace(/<section[^>]*>[\s\S]*?(?:床垫系列完善整套|Mattresses Complete the Suite)[\s\S]*?<\/section>/g, '');

    // Remove Quote CTA section
    html = html.replace(/<section[^>]*cta-band[^>]*>[\s\S]*?<\/section>/gi, '');

    // Fix 'of' in About Section
    html = html.replace(/拥有二十年丰富经验\s*of\s*纽约家具进口商/g, '拥有二十年丰富经验的纽约家具进口商');
    html = html.replace(/丰富经验\s*of\s*纽约/g, '丰富经验的纽约');
    
    // Fix office collection image
    html = html.replace(/src="[^"]*office-collection\.jpg"/g, 'src="assets/images/pdf7/img-000.jpg"');
    html = html.replace(/src="[^"]*office-collection\.webp"/g, 'src="assets/images/pdf7/img-000.jpg"');
    html = html.replace(/src="\.\.\/assets\/images\/office-collection\.jpg"/g, 'src="../assets/images/pdf7/img-000.jpg"');
    html = html.replace(/src="\.\.\/\.\.\/assets\/images\/office-collection\.jpg"/g, 'src="../../assets/images/pdf7/img-000.jpg"');

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
