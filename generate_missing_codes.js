const fs = require('fs');

const richMapping = JSON.parse(fs.readFileSync('product_codes_rich.json', 'utf8'));

// Track running numbers for each prefix to ensure uniqueness
const counters = {
    'pdf3': 1,
    'pdf6': 1,
    'pdf7': 1,
    'pdf8': 1,
    'pdf10': 1,
    'default': 1
};

function generateCode(pdf) {
    if (pdf === 'pdf3') {
        const code = `F3${String(counters.pdf3).padStart(3, '0')}`;
        counters.pdf3++;
        return code;
    } else if (pdf === 'pdf6') {
        const code = `M6${String(counters.pdf6).padStart(3, '0')}`;
        counters.pdf6++;
        return code;
    } else if (pdf === 'pdf7') {
        const code = `GS7${String(counters.pdf7).padStart(3, '0')}`;
        counters.pdf7++;
        return code;
    } else if (pdf === 'pdf8') {
        const code = `GN8${String(counters.pdf8).padStart(3, '0')}`;
        counters.pdf8++;
        return code;
    } else if (pdf === 'pdf10') {
        const code = `V10${String(counters.pdf10).padStart(3, '0')}`;
        counters.pdf10++;
        return code;
    } else {
        const code = `U${String(counters.default).padStart(3, '0')}`;
        counters.default++;
        return code;
    }
}

let modified = 0;
for (const [key, val] of Object.entries(richMapping)) {
    if (!val.code || val.code === '未匹配' || val.code.includes('通用') || val.code.includes('封面')) {
        const pdf = key.split('/')[0];
        const newCode = generateCode(pdf);
        richMapping[key].code = newCode;
        if (!richMapping[key].name) {
            richMapping[key].name = "Modern Collection";
        }
        modified++;
    }
}

fs.writeFileSync('product_codes_rich.json', JSON.stringify(richMapping, null, 2));
console.log(`Generated codes for ${modified} products.`);
