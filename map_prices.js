const fs = require('fs');

// 1. Load the price list
const csvContent = fs.readFileSync('素材库/价钱/Furniture_Price_List_Adjusted.csv', 'utf8');
const lines = csvContent.split('\n').map(l => l.trim()).filter(Boolean);
const headers = lines[0].split(',').map(h => h.trim());

// BOM character strip
if (headers[0].charCodeAt(0) === 0xFEFF) {
    headers[0] = headers[0].substring(1);
}

const priceData = [];
for (let i = 1; i < lines.length; i++) {
    // Regex for parsing CSV correctly if quotes are used, but split by comma might be enough here
    // Simple split:
    const parts = lines[i].split(',');
    if (parts.length >= 6) {
        priceData.push({
            code: parts[2].trim(),
            desc: parts[3].trim(),
            price: parts[5].trim()
        });
    }
}

// 2. Load the rich mapping of products currently on website
const richMapping = JSON.parse(fs.readFileSync('product_codes_rich.json', 'utf8'));

// Get all unique product codes from our mapping
const uniqueProductsOnSite = new Set();
for (const val of Object.values(richMapping)) {
    if (val.code) {
        uniqueProductsOnSite.add(val.code);
    }
}

// 3. Match them up
const matchedPrices = {}; // code -> price
let successCount = 0;
const failedCodes = [];

for (const code of uniqueProductsOnSite) {
    // Exact match
    const exactMatches = priceData.filter(p => p.code.toLowerCase() === code.toLowerCase() || p.code.toLowerCase().includes(code.toLowerCase()));
    
    if (exactMatches.length > 0) {
        // If there are multiple, maybe pick the highest or lowest? Let's just pick the first one's price for now.
        matchedPrices[code] = exactMatches[0].price;
        successCount++;
    } else {
        // Fuzzy match by trying to match parts of the code?
        // E.g. "F3210" vs "F3210#1"
        const fuzzyMatches = priceData.filter(p => p.desc.toLowerCase().includes(code.toLowerCase()) || code.toLowerCase().includes(p.code.toLowerCase()));
        if (fuzzyMatches.length > 0) {
             matchedPrices[code] = fuzzyMatches[0].price;
             successCount++;
        } else {
             failedCodes.push(code);
        }
    }
}

console.log(`Matching complete. Success: ${successCount}, Failed: ${failedCodes.length}`);
if (failedCodes.length > 0) {
    console.log(`Failed to match:`);
    failedCodes.forEach(c => console.log(`- ${c}`));
}

fs.writeFileSync('product_prices.json', JSON.stringify(matchedPrices, null, 2));

