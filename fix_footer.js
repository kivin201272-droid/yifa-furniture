const fs = require('fs');
const path = require('path');

function fixFooter(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Change footer header from "关于我们" to "公司信息" to avoid duplication with the "关于我们" link
    html = html.replace(/<h3>关于我们<\/h3><ul><li><a href=\.\/about\/>关于我们<\/a><\/li>/g, '<h3>公司信息</h3><ul><li><a href=./about/>关于我们</a></li>');
    html = html.replace(/<h3>关于我们<\/h3><ul><li><a href=\.\.\/about\/>关于我们<\/a><\/li>/g, '<h3>公司信息</h3><ul><li><a href=../about/>关于我们</a></li>');
    
    // Also remove the empty <li></li> that was left behind from a previous deletion
    html = html.replace(/<li><a href=\.\/about\/>关于我们<\/a><\/li><li><\/li>/g, '<li><a href=./about/>关于我们</a></li>');
    html = html.replace(/<li><a href=\.\.\/about\/>关于我们<\/a><\/li><li><\/li>/g, '<li><a href=../about/>关于我们</a></li>');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        console.log(`Updated ${filePath}`);
    }
}

const zhFiles = [
    'zh/index.html',
    'zh/products/index.html',
    'zh/bedroom/index.html',
    'zh/living-room/index.html',
    'zh/dining/index.html',
    'zh/office/index.html',
    'zh/mattress/index.html',
    'zh/about/index.html',
    'zh/faq/index.html',
    'zh/contact/index.html'
];

zhFiles.forEach(file => {
    fixFooter(path.join(__dirname, file));
});
