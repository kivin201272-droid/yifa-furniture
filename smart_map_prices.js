const fs = require('fs');

const csvContent = fs.readFileSync('素材库/价钱/Furniture_Price_List_Adjusted.csv', 'utf8');
const lines = csvContent.split('\n').map(l => l.trim()).filter(Boolean);
const headers = lines[0].split(',').map(h => h.trim());
if (headers[0].charCodeAt(0) === 0xFEFF) headers[0] = headers[0].substring(1);

const priceData = [];
for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split(',');
    if (parts.length >= 6) {
        priceData.push({
            code: parts[2].trim(),
            desc: parts[3].trim(),
            price: parts[5].trim() // New price
        });
    }
}

const richMapping = JSON.parse(fs.readFileSync('product_codes_rich.json', 'utf8'));
const uniqueProductsOnSite = new Set();
for (const val of Object.values(richMapping)) {
    if (val.code) uniqueProductsOnSite.add(val.code);
}

const matchedPrices = {};
let successCount = 0;
const failedCodes = [];

for (const code of uniqueProductsOnSite) {
    let matchedPrice = null;
    
    // 1. Exact or simple inclusion match
    let matches = priceData.filter(p => p.code.toLowerCase() === code.toLowerCase() || p.code.toLowerCase().includes(code.toLowerCase()) || code.toLowerCase().includes(p.code.toLowerCase()));
    
    // 2. If no match, try extracting numbers and matching that
    if (matches.length === 0) {
        const numbersMatch = code.match(/\d{3,}/);
        if (numbersMatch) {
            const num = numbersMatch[0];
            matches = priceData.filter(p => p.code.includes(num));
        }
    }
    
    if (matches.length > 0) {
        // Find the maximum price if there are multiple parts (e.g. Sofa vs Loveseat vs Chair)
        // Usually we want the price of the Set or the Sofa.
        let selectedMatch = matches[0];
        
        // Prefer "Sectional" or "Sofa" over "Chair" or "Loveseat"
        const preferred = matches.filter(m => m.desc.toLowerCase().includes('sectional') || m.desc.toLowerCase().includes('sofa') || m.code.toLowerCase().includes('sect'));
        if (preferred.length > 0) {
            selectedMatch = preferred[0];
        } else {
            // Pick highest price
            selectedMatch = matches.reduce((max, cur) => parseFloat(cur.price) > parseFloat(max.price) ? cur : max, matches[0]);
        }
        
        const rawPrice = parseFloat(selectedMatch.price);
        const roundedPrice = Math.round(rawPrice / 10) * 10;
        matchedPrices[code] = roundedPrice;
        successCount++;
    } else {
        failedCodes.push(code);
    }
}

console.log(`Matching complete. Success: ${successCount}, Failed: ${failedCodes.length}`);
if (failedCodes.length > 0) {
    console.log(`Failed to match:`);
    failedCodes.forEach(c => console.log(`- ${c}`));
}

fs.writeFileSync('product_prices.json', JSON.stringify(matchedPrices, null, 2));
