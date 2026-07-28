const fs = require('fs');
const path = require('path');

const destDir = path.join(__dirname, 'assets/images');
const pdfs = ['pdf1', 'pdf2', 'pdf3', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf10'];
let mainImages = [];

for (const pdf of pdfs) {
    const pdfDir = path.join(destDir, pdf);
    if (fs.existsSync(pdfDir)) {
        let files = fs.readdirSync(pdfDir).filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
        files = files.filter(f => fs.statSync(path.join(pdfDir, f)).size >= 30000);
        files.sort((a, b) => (parseInt(a.replace(/\D/g, '')) || 0) - (parseInt(b.replace(/\D/g, '')) || 0));
        
        for (let i = 0; i < files.length; i += 3) {
            mainImages.push(`assets/images/${pdf}/${files[i]}`);
        }
    }
}

fs.writeFileSync('main_images_list.txt', mainImages.join('\n'));
console.log(`Generated list of ${mainImages.length} main images.`);
