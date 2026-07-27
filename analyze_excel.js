const xlsx = require('xlsx');
const path = require('path');

const filePath = path.join(__dirname, '素材库/价钱/d8860b3f-7487-4c5e-8455-ccef1fa92fdc.xlsx');
const workbook = xlsx.readFile(filePath);
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const data = xlsx.utils.sheet_to_json(sheet, { header: 1 });

const categories = {};

for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row || row.length < 4) continue;
    
    const source = row[0]; // e.g. PJ Warehouse
    const page = String(row[1]).trim();
    const desc = (row[3] || '').toLowerCase();
    
    if (!categories[source]) categories[source] = {};
    if (!categories[source][page]) categories[source][page] = new Set();
    
    if (desc.includes('bed') || desc.includes('night stand') || desc.includes('dresser') || desc.includes('chest')) {
        categories[source][page].add('Bedroom');
    } else if (desc.includes('sofa') || desc.includes('chair') || desc.includes('recliner') || desc.includes('tv stand') || desc.includes('coffee table') || desc.includes('end table') || desc.includes('loveseat')) {
        categories[source][page].add('Living Room');
    } else if (desc.includes('dining') || desc.includes('table')) {
        categories[source][page].add('Dining Room');
    } else {
        categories[source][page].add('Other: ' + desc);
    }
}

for (const source in categories) {
    console.log(`Source: ${source}`);
    for (const page in categories[source]) {
        console.log(`  Page ${page}: ${Array.from(categories[source][page]).join(', ')}`);
    }
}
