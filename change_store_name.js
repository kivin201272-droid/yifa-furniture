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

const htmlFiles = getAllHtmlFiles(path.join(__dirname, 'zh'));

let count = 0;
htmlFiles.forEach(filePath => {
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Replace text
    html = html.replace(/拥有二十年丰富经验纽约家具进口商/g, '拥有二十年丰富经验纽约家具店');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        count++;
    }
});

console.log(`Updated ${count} HTML files in zh directory.`);
