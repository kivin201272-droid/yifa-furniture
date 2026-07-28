const fs = require('fs');

const transcriptPath = '/Users/kivinwang/.gemini/antigravity-ide/brain/f60a2597-4e76-4627-ac1d-f1991e150f54/.system_generated/logs/transcript.jsonl';
const lines = fs.readFileSync(transcriptPath, 'utf8').split('\n').filter(Boolean);

let mappings = {};

for (const line of lines) {
    try {
        const obj = JSON.parse(line);
        if (obj.source === 'MODEL' && obj.content) {
            // Check for markdown tables
            const tableRegex = /\|\s*\*\*(pdf\d+\/img-\d+)\*\*\s*\|\s*[^|]+\|\s*\*\*([^*]+)\*\*/g;
            let match;
            while ((match = tableRegex.exec(obj.content)) !== null) {
                const img = match[1].toLowerCase().replace('pdf', 'pdf'); 
                const productCode = match[2].trim();
                mappings[img] = productCode;
            }
        }
    } catch (e) {}
}

console.log(JSON.stringify(mappings, null, 2));
fs.writeFileSync('extracted_product_codes.json', JSON.stringify(mappings, null, 2));
console.log(`Extracted ${Object.keys(mappings).length} mappings.`);
