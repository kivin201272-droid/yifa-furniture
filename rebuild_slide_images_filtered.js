const fs = require('fs');
const path = require('path');

// Read the mapping configuration (if any)
const MAPPING_FILE = path.join(__dirname, 'product_mapping.json');
let productMapping = {};
if (fs.existsSync(MAPPING_FILE)) {
    productMapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf-8'));
}

// Default fallbacks if a set is not explicitly mapped in product_mapping.json
const DEFAULT_CATEGORY = {
    'pdf1': 'living-room',
    'pdf2': 'living-room',
    'pdf3': 'living-room',
    'pdf5': 'living-room',
    'pdf6': 'mattress',
    'pdf7': 'dining',
    'pdf8': 'dining',
    'pdf10': 'dining'
};

const PAGES = [
    { file: 'bedroom/index.html', cat: 'bedroom', level: 1 },
    { file: 'zh/bedroom/index.html', cat: 'bedroom', level: 2 },
    { file: 'living-room/index.html', cat: 'living-room', level: 1 },
    { file: 'zh/living-room/index.html', cat: 'living-room', level: 2 },
    { file: 'dining/index.html', cat: 'dining', level: 1 },
    { file: 'zh/dining/index.html', cat: 'dining', level: 2 },
    { file: 'mattress/index.html', cat: 'mattress', level: 1 },
    { file: 'zh/mattress/index.html', cat: 'mattress', level: 2 },
    { file: 'office/index.html', cat: 'office', level: 1 },
    { file: 'zh/office/index.html', cat: 'office', level: 2 }
];

const allSets = [];

// 1. Gather all sets from all PDFs
const pdfs = ['pdf1', 'pdf2', 'pdf3', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf10'];
for (const pdf of pdfs) {
    const pdfDir = path.join(__dirname, 'assets', 'images', pdf);
    if (!fs.existsSync(pdfDir)) continue;
    
    let files = fs.readdirSync(pdfDir)
        .filter(f => f.toLowerCase().endsWith('.jpg') || f.toLowerCase().endsWith('.png'));
    
    files = files.filter(f => {
        const stat = fs.statSync(path.join(pdfDir, f));
        return stat.size >= 30000;
    });

    files.sort((a, b) => {
        const numA = parseInt(a.replace(/\D/g, '')) || 0;
        const numB = parseInt(b.replace(/\D/g, '')) || 0;
        return numA - numB;
    });
        
    const chunkSize = 3;
    for (let i = 0; i < files.length; i += chunkSize) {
        const chunk = files.slice(i, i + chunkSize);
        const setIndex = i / chunkSize; // e.g., 0 for Set 1
        const setId = `${pdf}-set-${setIndex}`;
        
        // Determine category for this specific set
        let category = productMapping[setId];
        if (!category) {
            category = DEFAULT_CATEGORY[pdf] || 'living-room';
        }
        
        allSets.push({
            pdf,
            setIndex,
            setId,
            chunk,
            category
        });
    }
}

// 2. Inject into pages
for (const page of PAGES) {
    const filePath = path.join(__dirname, page.file);
    if (!fs.existsSync(filePath)) continue;

    let html = fs.readFileSync(filePath, 'utf-8');

    const pdfIndex = html.indexOf('    <!-- PDF');
    const dynIndex = html.indexOf('    <!-- DYNAMIC COLLECTION');
    const injectStart = pdfIndex !== -1 ? pdfIndex : (dynIndex !== -1 ? dynIndex : -1);
    
    if (injectStart !== -1) {
        const mainEndIndex = html.indexOf('</main>', injectStart);
        if (mainEndIndex !== -1) {
            html = html.substring(0, injectStart) + html.substring(mainEndIndex);
        }
    }

    let injectionHtml = '';
    const setsForThisPage = allSets.filter(s => s.category === page.cat);
    
    if (setsForThisPage.length > 0) {
        injectionHtml += `    <!-- DYNAMIC COLLECTION -->\n`;
        injectionHtml += `    <div class="sofa-grid">\n`;
        
        const prefix = page.level === 1 ? '../' : '../../';
        
        setsForThisPage.forEach(setObj => {
            const { pdf, setIndex, setId, chunk } = setObj;
            const mainImg = chunk[0];
            const title = `${pdf.toUpperCase()} Set ${setIndex + 1}`;
            const subtitle = page.file.startsWith('zh/') ? '高品质家具' : 'Premium Quality';
            const tag = page.file.startsWith('zh/') ? '精选' : 'Featured';
            
            injectionHtml += `        <div class="sofa-card reveal">\n`;
            injectionHtml += `            <div class="sofa-img-container">\n`;
            injectionHtml += `                <img src="${prefix}assets/images/${pdf}/${mainImg}" alt="${title}" class="main-sofa-img" id="${setId}-main" loading="lazy">\n`;
            injectionHtml += `            </div>\n`;
            injectionHtml += `            <div class="sofa-thumbnails">\n`;
            
            chunk.forEach((img, imgIndex) => {
                const activeClass = imgIndex === 0 ? ' active' : '';
                injectionHtml += `                <img src="${prefix}assets/images/${pdf}/${img}" alt="Detail" class="sofa-thumb${activeClass}" onclick="changeImage(this, '${setId}-main')">\n`;
            });
            
            injectionHtml += `            </div>\n`;
            injectionHtml += `            <div class="sofa-info">\n`;
            injectionHtml += `                <h3>${title}</h3>\n`;
            injectionHtml += `                <p>${subtitle}</p>\n`;
            injectionHtml += `                <div class="sofa-details">\n`;
            injectionHtml += `                    <span class="detail-tag">${tag}</span>\n`;
            injectionHtml += `                </div>\n`;
            injectionHtml += `            </div>\n`;
            injectionHtml += `        </div>\n`;
        });
        
        injectionHtml += `    </div>\n\n`;
    }

    html = html.replace('</main>', injectionHtml + '</main>');
    fs.writeFileSync(filePath, html);
    console.log(`Rebuilt dynamic slider for ${page.file} (${setsForThisPage.length} items)`);
}
