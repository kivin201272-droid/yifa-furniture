const fs = require('fs');

const richMapping = JSON.parse(fs.readFileSync('product_codes_rich.json', 'utf8'));

// We need to change specific placeholder codes to M60xx style
let counter = 10; // Start at M6010 to avoid conflicts with M6001-M6003 if they exist

for (const [key, val] of Object.entries(richMapping)) {
    if (key.startsWith('pdf6/')) {
        if (val.code === 'Sleepy Edge Mattress' || val.code === 'Mattress Base' || val.code === 'Mattress Details') {
            const newCode = `M60${counter++}`;
            val.name = val.code; // Move the descriptive text to the name/subtitle
            val.code = newCode; 
        }
    }
}

fs.writeFileSync('product_codes_rich.json', JSON.stringify(richMapping, null, 2));
console.log('Fixed mattress placeholder codes.');
