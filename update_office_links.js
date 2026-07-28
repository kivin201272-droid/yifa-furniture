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

// Update footer in all files
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
                '<li><a href=../mattress/>Mattress</a></li></ul>', 
                '<li><a href=../mattress/>Mattress</a></li><li><a href=../office/>Office</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=./mattress/>Mattress</a></li></ul>', 
                '<li><a href=./mattress/>Mattress</a></li><li><a href=./office/>Office</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=../../mattress/>Mattress</a></li></ul>', 
                '<li><a href=../../mattress/>Mattress</a></li><li><a href=../../office/>Office</a></li></ul>'
            );
            
            // Chinese footer
            replaceInFile(fullPath, 
                '<li><a href=../mattress/>床垫系列</a></li></ul>', 
                '<li><a href=../mattress/>床垫系列</a></li><li><a href=../office/>办公系列</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=./mattress/>床垫系列</a></li></ul>', 
                '<li><a href=./mattress/>床垫系列</a></li><li><a href=./office/>办公系列</a></li></ul>'
            );
            replaceInFile(fullPath, 
                '<li><a href=../../mattress/>床垫系列</a></li></ul>', 
                '<li><a href=../../mattress/>床垫系列</a></li><li><a href=../../office/>办公系列</a></li></ul>'
            );
        }
    }
}

updateFooterInDir(__dirname);
