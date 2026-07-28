const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '素材库/单图');
const destDir = path.join(__dirname, 'assets/images');

const pdfs = ['PDF1', 'PDF2', 'PDF3', 'PDF5', 'PDF6', 'PDF7', 'PDF8', 'PDF10'];

let missing = [];

for (const pdf of pdfs) {
    const srcPdf = path.join(srcDir, pdf);
    const destPdf = path.join(destDir, pdf.toLowerCase()); // e.g. pdf1
    
    if (fs.existsSync(srcPdf)) {
        const srcFiles = fs.readdirSync(srcPdf).filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
        
        for (const file of srcFiles) {
            const destPath = path.join(destPdf, file);
            if (!fs.existsSync(destPath)) {
                missing.push(`${pdf}/${file}`);
            }
        }
    }
}

if (missing.length > 0) {
    console.log("Missing files found:");
    missing.forEach(m => console.log(m));
} else {
    console.log("All image files from 素材库/单图 are present in assets/images.");
}

// Also check how many sets are generated and if any files are skipped by the size filter
let totalParsedSets = 0;
let skippedFiles = [];
for (const pdf of pdfs) {
    const destPdf = path.join(destDir, pdf.toLowerCase());
    if (fs.existsSync(destPdf)) {
        const destFiles = fs.readdirSync(destPdf).filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
        let validFiles = destFiles.filter(f => {
            const stat = fs.statSync(path.join(destPdf, f));
            if (stat.size < 30000) {
                skippedFiles.push(`${pdf}/${f} (size: ${stat.size})`);
                return false;
            }
            return true;
        });
        
        totalParsedSets += Math.ceil(validFiles.length / 3);
    }
}

console.log(`\nTotal parsed sets: ${totalParsedSets}`);
console.log(`Total skipped files due to size (< 30kb): ${skippedFiles.length}`);
if (skippedFiles.length > 0) {
    console.log("Skipped files sample:");
    console.log(skippedFiles.slice(0, 5));
}
