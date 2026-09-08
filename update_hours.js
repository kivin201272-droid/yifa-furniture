const fs = require('fs');
const path = require('path');

function getAllFiles(dirPath, arrayOfFiles = []) {
    const files = fs.readdirSync(dirPath);
    files.forEach(file => {
        const fullPath = path.join(dirPath, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (!file.startsWith('.') && file !== 'node_modules') {
                arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
            }
        } else if (file.endsWith('.html')) {
            arrayOfFiles.push(fullPath);
        }
    });
    return arrayOfFiles;
}

const htmlFiles = getAllFiles('/Users/kivinwang/Documents/GitHub/yifa-furniture');

htmlFiles.forEach(filePath => {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    // 1. Chinese Footers
    content = content.replace(/<li>周一至周五:\s*9:00\s*AM\s*–\s*5:30\s*PM<\/li>\s*<li>周六\s*&\s*周日:\s*休息<\/li>/g,
        '<li>周一至周六: 11:00 AM – 4:30 PM</li><li>周日: 休息</li>');
    content = content.replace(/<li>周一至周五:\s*9:00\s*AM\s*–\s*5:30\s*PM<\/li>\s*<li>周六\s*&amp;\s*周日:\s*休息<\/li>/g,
        '<li>周一至周六: 11:00 AM – 4:30 PM</li><li>周日: 休息</li>');

    // 2. English Footers
    content = content.replace(/<li>Mon&ndash;Fri:\s*9:00\s*AM\s*&ndash;\s*5:30\s*PM<\/li>\s*<li>Saturday\s*&amp;\s*Sunday:\s*Closed<\/li>/g,
        '<li>Mon&ndash;Sat: 11:00 AM &ndash; 4:30 PM</li><li>Sunday: Closed</li>');
    content = content.replace(/<li>Mon–Fri:\s*9:00\s*AM\s*–\s*5:30\s*PM<\/li>\s*<li>Sat\s*&\s*Sun:\s*Closed<\/li>/g,
        '<li>Mon–Sat: 11:00 AM – 4:30 PM</li><li>Sunday: Closed</li>');
    content = content.replace(/<li>Mon–Fri:\s*9:00\s*AM\s*–\s*5:30\s*PM<\/li>\s*<li>Saturday\s*&\s*Sunday:\s*Closed<\/li>/g,
        '<li>Mon–Sat: 11:00 AM – 4:30 PM</li><li>Sunday: Closed</li>');

    // 3. Contact page hours
    content = content.replace(/<ul class=hours-list>[\s\S]*?<\/ul>/, (match) => {
        if (filePath.includes('/zh/')) {
            return `<ul class=hours-list><li><span>周一</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周二</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周三</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周四</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周五</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周六</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>周日</span><span class=closed>休息</span></li></ul>`;
        } else {
            return `<ul class=hours-list><li><span>Monday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Tuesday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Wednesday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Thursday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Friday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Saturday</span><span>11:00 AM &ndash; 4:30 PM</span></li><li><span>Sunday</span><span class=closed>Closed</span></li></ul>`;
        }
    });

    // 4. Dining page text
    content = content.replace(/开放时间：周一至周五，9:00\s*AM\s*-\s*5:30\s*PM。/g, '开放时间：周一至周六，11:00 AM - 4:30 PM，周日休息。');
    content = content.replace(/Open Monday to Friday, 9:00 AM to 5:30 PM\./g, 'Open Monday to Saturday, 11:00 AM to 4:30 PM (Sunday Closed).');

    // 5. FAQ page text & JSON-LD
    content = content.replace(/周一至周五 9:00 AM 至 5:30 PM/g, '周一至周六 11:00 AM 至 4:30 PM（周日休息）');
    content = content.replace(/Monday to Friday, 9:00 AM to 5:30 PM/g, 'Monday to Saturday, 11:00 AM to 4:30 PM (Sunday Closed)');
    content = content.replace(/Monday to Friday 9:00 AM to 5:30 PM/g, 'Monday to Saturday 11:00 AM to 4:30 PM (Sunday Closed)');

    // 6. Schema.org JSON-LD
    content = content.replace(/"dayOfWeek":\["周一","周二","周三","周四","周五"\],"opens":"09:00","closes":"17:30"/g,
        '"dayOfWeek":["周一","周二","周三","周四","周五","周六"],"opens":"11:00","closes":"16:30"');
    content = content.replace(/"dayOfWeek":\["Monday","Tuesday","Wednesday","Thursday","Friday"\],"opens":"09:00","closes":"17:30"/g,
        '"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"11:00","closes":"16:30"');

    if (content !== original) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated hours in: ${filePath}`);
    }
});
