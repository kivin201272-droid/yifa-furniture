const fs = require('fs');

const richMapping = JSON.parse(fs.readFileSync('product_codes_rich.json', 'utf8'));

let counter = 100; // Start at M6100 to be safe and sequential

for (const [key, val] of Object.entries(richMapping)) {
    if (key.startsWith('pdf6/')) {
        // If it's a mattress and doesn't start with M6 (e.g. ELEVATE)
        if (!val.code.startsWith('M6')) {
            const oldCode = val.code;
            val.code = `M6${counter++}`;
            val.name = oldCode; // e.g. "ELEVATE"
        }
    }
}

fs.writeFileSync('product_codes_rich.json', JSON.stringify(richMapping, null, 2));
console.log('Fixed ALL mattress codes.');
