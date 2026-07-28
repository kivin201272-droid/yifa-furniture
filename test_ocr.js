const Tesseract = require('tesseract.js');
const path = require('path');

async function testOcr() {
    console.log("Starting OCR on 图片1.png...");
    const imgPath = path.join(__dirname, '素材库/TH图片文件信夹/图片1.png');
    
    try {
        const result = await Tesseract.recognize(imgPath, 'eng+chi_sim', {
            logger: m => { if (m.status === 'recognizing text' && m.progress % 0.2 < 0.01) console.log(`Progress: ${(m.progress * 100).toFixed(0)}%`) }
        });
        console.log("\n--- OCR Text ---");
        console.log(result.data.text);
        console.log("----------------\n");
    } catch (err) {
        console.error("OCR Failed:", err);
    }
}

testOcr();
