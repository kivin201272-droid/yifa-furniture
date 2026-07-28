const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '素材库/单图');
const destDir = path.join(__dirname, 'assets/images');

const pdfs = ['PDF1', 'PDF2', 'PDF3', 'PDF5', 'PDF6', 'PDF7', 'PDF8', 'PDF10'];

let copiedCount = 0;

for (const pdf of pdfs) {
    const srcPdf = path.join(srcDir, pdf);
    const destPdf = path.join(destDir, pdf.toLowerCase()); // e.g. pdf1
    
    if (fs.existsSync(srcPdf)) {
        if (!fs.existsSync(destPdf)) {
            fs.mkdirSync(destPdf, { recursive: true });
        }

        const srcFiles = fs.readdirSync(srcPdf).filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
        
        for (const file of srcFiles) {
            const destPath = path.join(destPdf, file);
            const srcPath = path.join(srcPdf, file);
            if (!fs.existsSync(destPath)) {
                fs.copyFileSync(srcPath, destPath);
                copiedCount++;
            }
        }
    }
}

console.log(`Successfully copied ${copiedCount} missing files to assets/images.`);
