const fs = require('fs');
const path = require('path');

const filesToClean = [
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/zh/bedroom/index.html',
        regex: /<!-- TH Collection Special Card -->[\s\S]*?请点击查看更多产品<\/a>\s*<\/div>\s*<\/div>\s*/g
    },
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/bedroom/index.html',
        regex: /<!-- TH Collection Special Card -->[\s\S]*?Click to view more products<\/a>\s*<\/div>\s*<\/div>\s*/g
    },
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/zh/living-room/index.html',
        regex: /<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?请点击查看更多产品<\/a>\s*<\/div>\s*<\/div>\s*/g
    },
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/living-room/index.html',
        regex: /<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?Click to view more products<\/a>\s*<\/div>\s*<\/div>\s*/g
    },
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/zh/office/index.html',
        regex: /<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?请点击查看更多产品<\/a>\s*<\/div>\s*<\/div>\s*/g
    },
    {
        file: '/Users/kivinwang/Documents/GitHub/yifa-furniture/office/index.html',
        regex: /<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?Click to view more products<\/a>\s*<\/div>\s*<\/div>\s*/g
    }
];

filesToClean.forEach(({ file, regex }) => {
    if (fs.existsSync(file)) {
        let content = fs.readFileSync(file, 'utf8');
        if (regex.test(content)) {
            content = content.replace(regex, '');
            fs.writeFileSync(file, content, 'utf8');
            console.log(`Successfully removed special TH card from: ${file}`);
        } else {
            console.log(`Pattern not matched in: ${file}`);
        }
    }
});

// Fix bedroom links in zh/index.html and index.html
const zhHome = '/Users/kivinwang/Documents/GitHub/yifa-furniture/zh/index.html';
if (fs.existsSync(zhHome)) {
    let content = fs.readFileSync(zhHome, 'utf8');
    content = content.replace('href="https://th-nycfurniture.com/#products" target="_blank" rel="noopener noreferrer">查看卧室系列</a>', 'href=./bedroom/>查看卧室系列</a>');
    fs.writeFileSync(zhHome, content, 'utf8');
    console.log('Fixed zh/index.html bedroom link');
}

const enHome = '/Users/kivinwang/Documents/GitHub/yifa-furniture/index.html';
if (fs.existsSync(enHome)) {
    let content = fs.readFileSync(enHome, 'utf8');
    content = content.replace('href="https://th-nycfurniture.com/#products" target="_blank" rel="noopener noreferrer">View Bedroom</a>', 'href=./bedroom/>View Bedroom</a>');
    fs.writeFileSync(enHome, content, 'utf8');
    console.log('Fixed index.html bedroom link');
}
