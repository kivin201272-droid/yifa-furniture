const fs = require('fs');
const path = require('path');

function getAllHtmlFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);

    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function(file) {
        if (fs.statSync(dirPath + "/" + file).isDirectory()) {
            arrayOfFiles = getAllHtmlFiles(dirPath + "/" + file, arrayOfFiles);
        } else {
            if (file.endsWith('.html')) {
                arrayOfFiles.push(path.join(dirPath, "/", file));
            }
        }
    });

    return arrayOfFiles;
}

const htmlFiles = getAllHtmlFiles(path.join(__dirname));

let count = 0;
htmlFiles.forEach(filePath => {
    // Ignore node_modules
    if (filePath.includes('node_modules')) return;

    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Fix "关于我们 Us" -> "关于我们"
    html = html.replace(/关于我们\s*Us/g, '关于我们');

    // Fix "拥有二十年丰富经验 of 纽约家具进口商" -> "拥有二十年丰富经验的纽约家具进口商"
    html = html.replace(/拥有二十年丰富经验\s*of\s*纽约家具进口商/g, '拥有二十年丰富经验的纽约家具进口商');

    // Also remove "of" if it was already changed to "的" but the user wants it literally removed? No, "的" is correct. 
    // Let's actually change "的纽约" to " 纽约" if the user meant literally remove it. 
    html = html.replace(/拥有二十年丰富经验的纽约家具进口商/g, '拥有二十年丰富经验 纽约家具进口商');

    // Fix "丰富经验 of 纽约" -> "丰富经验 纽约"
    html = html.replace(/丰富经验\s*of\s*纽约/g, '丰富经验 纽约');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        count++;
    }
});

console.log(`Updated ${count} HTML files.`);
