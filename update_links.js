const fs = require('fs');
const path = require('path');

function replaceInFile(filePath, search, replace) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf-8');
    if (content.includes(search)) {
        content = content.split(search).join(replace);
        fs.writeFileSync(filePath, content);
        console.log(`Updated ${filePath}`);
    }
}

// 1. Update index.html
replaceInFile('index.html', '<a class=cc-link href=./products/>View Mattress</a>', '<a class=cc-link href=./mattress/>View Mattress</a>');
replaceInFile('zh/index.html', '<a class=cc-link href=./products/>查看床垫系列</a>', '<a class=cc-link href=./mattress/>查看床垫系列</a>');
// Also fallback if the zh version differs
replaceInFile('zh/index.html', 'href=./products/>了解更多床垫', 'href=./mattress/>了解更多床垫');

// 2. Update products/index.html
replaceInFile('products/index.html', '<a class="btn btn-outline" href=../contact/>Request Pricing</a>', '<a class="btn btn-outline" href=../mattress/>Explore Mattress</a>');
// In zh/products/index.html
replaceInFile('zh/products/index.html', '<a class="btn btn-outline" href=../contact/>索取报价</a>', '<a class="btn btn-outline" href=../mattress/>浏览床垫系列</a>');

// 3. Update footer in all files
function updateFooterInDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (file !== 'node_modules' && file !== '.git' && file !== 'venv') {
                updateFooterInDir(fullPath);
            }
        } else if (fullPath.endsWith('.html')) {
            // English footer
            replaceInFile(fullPath, 
                '<li><a href=../dining/>Dining</a></li></ul>', 
                '<li><a href=../dining/>Dining</a></li><li><a href=../mattress/>Mattress</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=./dining/>Dining</a></li></ul>', 
                '<li><a href=./dining/>Dining</a></li><li><a href=./mattress/>Mattress</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=../../dining/>Dining</a></li></ul>', 
                '<li><a href=../../dining/>Dining</a></li><li><a href=../../mattress/>Mattress</a></li></ul>'
            );
            
            // Chinese footer
            replaceInFile(fullPath, 
                '<li><a href=../dining/>餐厅系列</a></li></ul>', 
                '<li><a href=../dining/>餐厅系列</a></li><li><a href=../mattress/>床垫系列</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=./dining/>餐厅系列</a></li></ul>', 
                '<li><a href=./dining/>餐厅系列</a></li><li><a href=./mattress/>床垫系列</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=../../dining/>餐厅系列</a></li></ul>', 
                '<li><a href=../../dining/>餐厅系列</a></li><li><a href=../../mattress/>床垫系列</a></li></ul>'
            );
        }
    }
}

updateFooterInDir(__dirname);
