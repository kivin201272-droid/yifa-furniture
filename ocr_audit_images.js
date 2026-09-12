const fs = require('fs');
const path = require('path');
const Tesseract = require('tesseract.js');

async function main() {
    console.log("=== Starting OCR Inspection on Product Images ===");
    
    // Collect all images used across the 5 categories
    const htmlFiles = [
        'zh/bedroom/index.html',
        'zh/living-room/index.html',
        'zh/dining/index.html',
        'zh/office/index.html',
        'zh/mattress/index.html'
    ];
    
    const imageSet = new Set();
    for (const f of htmlFiles) {
        const content = fs.readFileSync(f, 'utf8');
        const regex = /<img[^>]+src=["']([^"']+)["']/g;
        let match;
        while ((match = regex.exec(content)) !== null) {
            let img = match[1].split('?')[0].replace(/\.\.\//g, '').replace(/^\//, '');
            // check if it is a pj / pdf image
            if (img.includes('assets/images/')) {
                imageSet.add(img);
            }
        }
    }
    
    const imageList = Array.from(imageSet).sort();
    console.log(`Found ${imageList.length} unique product images to inspect.`);
    
    // Focus especially on the newly created or replaced images: pdf3, pj_bedroom, pj_office, pj_living, pj_dining
    const targetImages = imageList.filter(img => 
        img.includes('pdf3/') || 
        img.includes('pj_bedroom/') || 
        img.includes('pj_office/') || 
        img.includes('pj_living/') || 
        img.includes('pj_dining/')
    );
    
    console.log(`Targeting ${targetImages.length} PDF-extracted / PJ-supplemented images for OCR audit.`);
    
    const worker = await Tesseract.createWorker('eng');
    
    const resultsWithText = [];
    
    for (let i = 0; i < targetImages.length; i++) {
        const imgPath = targetImages[i];
        if (!fs.existsSync(imgPath)) continue;
        
        try {
            const ret = await worker.recognize(imgPath);
            const text = ret.data.text.trim();
            
            // Check if text has price or page keywords
            if (text && (/\$|\bpage\b|\bprice\b|\b\d+\.\d{2}\b/i.test(text))) {
                console.log(`[ALERT] Text detected in ${imgPath}: "${text.replace(/\n/g, ' ')}"`);
                resultsWithText.push({ imgPath, text });
            }
        } catch (err) {
            console.error(`Error processing ${imgPath}:`, err.message);
        }
        
        if ((i + 1) % 20 === 0 || i === targetImages.length - 1) {
            console.log(`Progress: ${i + 1} / ${targetImages.length} images scanned.`);
        }
    }
    
    await worker.terminate();
    
    console.log("\n==========================================");
    console.log(`OCR Audit Complete: ${resultsWithText.length} images with price/page text found.`);
    console.log("==========================================");
    
    if (resultsWithText.length > 0) {
        console.log(JSON.stringify(resultsWithText, null, 2));
    }
}

main().catch(console.error);
