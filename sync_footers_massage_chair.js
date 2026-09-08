const fs = require('fs');
const glob = require('glob');

const files = glob.sync('**/*.html', { ignore: ['node_modules/**', '.npm-cache/**'] });

files.forEach(file => {
    let html = fs.readFileSync(file, 'utf8');
    let changed = false;

    // Chinese footers
    if (html.includes('<li><a href=../office/>办公系列</a></li>') && !html.includes('massage-chair/')) {
        html = html.replace('<li><a href=../office/>办公系列</a></li>', '<li><a href=../massage-chair/>按摩椅系列</a></li>\n<li><a href=../office/>办公系列</a></li>');
        changed = true;
    } else if (html.includes('<li><a href=./office/>办公系列</a></li>') && !html.includes('massage-chair/')) {
        html = html.replace('<li><a href=./office/>办公系列</a></li>', '<li><a href=./massage-chair/>按摩椅系列</a></li>\n<li><a href=./office/>办公系列</a></li>');
        changed = true;
    }

    // English footers
    if (html.includes('<li><a href=../office/>Office</a></li>') && !html.includes('massage-chair/')) {
        html = html.replace('<li><a href=../office/>Office</a></li>', '<li><a href=../massage-chair/>Massage Chairs</a></li>\n<li><a href=../office/>Office</a></li>');
        changed = true;
    } else if (html.includes('<li><a href=./office/>Office</a></li>') && !html.includes('massage-chair/')) {
        html = html.replace('<li><a href=./office/>Office</a></li>', '<li><a href=./massage-chair/>Massage Chairs</a></li>\n<li><a href=./office/>Office</a></li>');
        changed = true;
    }

    if (changed) {
        fs.writeFileSync(file, html, 'utf8');
        console.log('Synced footer in:', file);
    }
});
