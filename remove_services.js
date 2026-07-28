const fs = require('fs');
const path = require('path');

function removeServicesSection(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Remove Services section
    html = html.replace(/<section[^>]*>[\s\S]*?(?:我们的服务|Our Services)[\s\S]*?<\/section>/g, '');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        console.log(`Updated ${filePath}`);
    }
}

removeServicesSection(path.join(__dirname, 'about/index.html'));
removeServicesSection(path.join(__dirname, 'zh/about/index.html'));
