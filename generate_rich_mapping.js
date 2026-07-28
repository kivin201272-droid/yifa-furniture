const fs = require('fs');

// Load raw mappings
const raw = JSON.parse(fs.readFileSync('extracted_product_codes.json', 'utf8'));

// Fix up the known ones from our discussion
if (raw['pdf8/img-000'] === '未匹配') raw['pdf8/img-000'] = 'GN8322';
if (raw['pdf7/img-086'] === '未匹配') raw['pdf7/img-086'] = 'F4872';
if (raw['pdf3/img-000'] === '未匹配') raw['pdf3/img-000'] = 'F4972';
if (raw['pdf6/img-000'] === '未匹配') raw['pdf6/img-000'] = 'Sleepy Edge Mattress';
if (raw['pdf6/img-028'] === '未匹配') raw['pdf6/img-028'] = 'Mattress Base';
if (raw['pdf6/img-040'] === '未匹配') raw['pdf6/img-040'] = 'Mattress Details';

// Parse product_labels.csv to get Names
const csv = fs.readFileSync('素材库/产品标注/product_labels.csv', 'utf8').split('\n').filter(Boolean);
const productInfo = {};
for (let i = 1; i < csv.length; i++) {
    const parts = csv[i].split(',');
    if (parts.length >= 2) {
        productInfo[parts[0].trim()] = parts[1].trim();
    }
}

const richMapping = {};

for (const [img, code] of Object.entries(raw)) {
    let cleanCode = code;
    // Clean up codes like "F3210#1~#4", "GN4730 / GNT4632", "GS5122 / GS2898系列"
    if (cleanCode.includes('/')) {
        cleanCode = cleanCode.split('/')[0].trim();
    }
    if (cleanCode.includes('系列')) {
        cleanCode = cleanCode.replace('系列', '').trim();
    }
    if (cleanCode.includes('细节') || cleanCode.includes('尺寸图')) {
        cleanCode = cleanCode.replace('细节', '').replace('尺寸图', '').trim();
    }
    if (cleanCode.includes(' 等')) {
        cleanCode = cleanCode.replace(' 等', '').trim();
    }
    if (cleanCode.includes(' (推测)')) {
        cleanCode = cleanCode.replace(' (推测)', '').trim();
    }
    
    // For F3210#1~#4 -> F3210
    if (cleanCode.includes('~')) {
        cleanCode = cleanCode.split('~')[0].trim();
    }

    let name = '';
    
    if (cleanCode !== '未匹配' && !cleanCode.includes('封面') && !cleanCode.includes('线框图')) {
        // Try to look up
        if (productInfo[cleanCode]) {
            name = productInfo[cleanCode];
        } else {
            // Try without # suffix if any
            const base = cleanCode.split('#')[0];
            if (productInfo[base]) {
                name = productInfo[base];
            } else if (productInfo[cleanCode + 'A']) {
                name = productInfo[cleanCode + 'A'];
            }
        }
    }
    
    richMapping[img] = {
        code: cleanCode === '未匹配' ? '' : cleanCode,
        name: name
    };
}

fs.writeFileSync('product_codes_rich.json', JSON.stringify(richMapping, null, 2));
console.log("Created product_codes_rich.json with " + Object.keys(richMapping).length + " items.");
