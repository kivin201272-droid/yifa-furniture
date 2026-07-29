const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        if (isDirectory && f !== '.git' && f !== 'node_modules' && f !== 'assets') {
            walkDir(dirPath, callback);
        } else if (!isDirectory && f.endsWith('.html')) {
            callback(dirPath);
        }
    });
}

walkDir('.', function(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    // 1. Replace Normal Mattress with Classic Mattress
    content = content.replace(/普通床垫/g, '经典床垫');
    content = content.replace(/Normal Mattress/gi, 'Classic Mattress');
    content = content.replace(/normal mattress/gi, 'classic mattress');

    // 2. Replace cover image in products pages
    content = content.replace(/pdf6\/N6001\.png/g, 'classic-mattress.png');

    if (content !== original) {
        fs.writeFileSync(filePath, content);
        console.log('Updated ' + filePath);
    }
});
