const fs = require('fs');
const path = require('path');

// The 138 newly added files
const newFilesStr = `PDF3/img-024.jpg
PDF3/img-026.jpg
PDF3/img-028.jpg
PDF3/img-030.jpg
PDF3/img-032.jpg
PDF3/img-037.jpg
PDF3/img-039.jpg
PDF3/img-047.jpg
PDF3/img-049.jpg
PDF3/img-051.jpg
PDF3/img-053.jpg
PDF3/img-062.jpg
PDF3/img-070.jpg
PDF3/img-073.jpg
PDF3/img-076.jpg
PDF3/img-127.jpg
PDF3/img-129.jpg
PDF3/img-133.jpg
PDF3/img-148.jpg
PDF3/img-163.jpg
PDF3/img-164.jpg
PDF3/img-183.jpg
PDF3/img-202.jpg
PDF3/img-204.jpg
PDF3/img-210.jpg
PDF3/img-212.jpg
PDF3/img-216.jpg
PDF3/img-218.jpg
PDF3/img-220.jpg
PDF3/img-222.jpg
PDF3/img-224.jpg
PDF3/img-226.jpg
PDF3/img-228.jpg
PDF3/img-230.jpg
PDF3/img-235.jpg
PDF3/img-241.jpg
PDF3/img-248.jpg
PDF3/img-261.jpg
PDF3/img-262.jpg
PDF3/img-273.jpg
PDF3/img-275.jpg
PDF3/img-280.jpg
PDF3/img-322.jpg
PDF3/img-349.jpg
PDF3/img-351.jpg
PDF3/img-356.jpg
PDF3/img-359.jpg
PDF3/img-361.jpg
PDF3/img-383.jpg
PDF6/img-002.jpg
PDF6/img-028.jpg
PDF7/img-002.jpg
PDF7/img-003.jpg
PDF7/img-004.jpg
PDF7/img-005.jpg
PDF7/img-006.jpg
PDF7/img-007.jpg
PDF7/img-008.jpg
PDF7/img-009.jpg
PDF7/img-010.jpg
PDF7/img-011.jpg
PDF7/img-012.jpg
PDF7/img-013.jpg
PDF7/img-014.jpg
PDF7/img-015.jpg
PDF7/img-016.jpg
PDF7/img-017.jpg
PDF7/img-018.jpg
PDF7/img-019.jpg
PDF7/img-020.jpg
PDF7/img-021.jpg
PDF7/img-022.jpg
PDF7/img-023.jpg
PDF7/img-024.jpg
PDF7/img-025.jpg
PDF7/img-026.jpg
PDF7/img-027.jpg
PDF7/img-028.jpg
PDF7/img-029.jpg
PDF7/img-030.jpg
PDF7/img-031.jpg
PDF7/img-032.jpg
PDF7/img-033.jpg
PDF7/img-034.jpg
PDF7/img-035.jpg
PDF7/img-036.jpg
PDF7/img-037.jpg
PDF7/img-038.jpg
PDF7/img-039.jpg
PDF7/img-040.jpg
PDF7/img-041.jpg
PDF7/img-042.jpg
PDF7/img-043.jpg
PDF7/img-044.jpg
PDF7/img-045.jpg
PDF7/img-046.jpg
PDF7/img-047.jpg
PDF7/img-048.jpg
PDF7/img-049.jpg
PDF7/img-050.jpg
PDF7/img-051.jpg
PDF7/img-052.jpg
PDF7/img-053.jpg
PDF7/img-054.jpg
PDF7/img-055.jpg
PDF7/img-056.jpg
PDF7/img-057.jpg
PDF7/img-058.jpg
PDF7/img-059.jpg
PDF7/img-060.jpg
PDF7/img-061.jpg
PDF7/img-062.jpg
PDF7/img-064.jpg
PDF7/img-065.jpg
PDF7/img-066.jpg
PDF7/img-067.jpg
PDF7/img-068.jpg
PDF7/img-069.jpg
PDF7/img-070.jpg
PDF7/img-072.jpg
PDF7/img-073.jpg
PDF7/img-074.jpg
PDF7/img-075.jpg
PDF7/img-076.jpg
PDF7/img-077.jpg
PDF7/img-078.jpg
PDF7/img-079.jpg
PDF7/img-080.jpg
PDF7/img-081.jpg
PDF7/img-082.jpg
PDF7/img-083.jpg
PDF7/img-084.jpg
PDF7/img-085.jpg
PDF7/img-086.jpg
PDF7/img-087.jpg
PDF7/img-088.jpg
PDF8/img-018.jpg
PDF10/img-229.jpg`;
const newFiles = new Set(newFilesStr.split('\n').filter(s=>s).map(s => s.toLowerCase()));

// 1. Read existing mapping
const oldMapping = JSON.parse(fs.readFileSync('product_mapping.json', 'utf-8'));
const newMapping = {};

// 2. Reconstruct the old array of files for each PDF
const pdfs = ['pdf1', 'pdf2', 'pdf3', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'pdf10'];
for (const pdf of pdfs) {
    const pdfDir = path.join(__dirname, 'assets', 'images', pdf);
    if (!fs.existsSync(pdfDir)) continue;
    
    let allFiles = fs.readdirSync(pdfDir).filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
    
    // Filter out the "newFiles" to simulate the state BEFORE the copy
    let oldStateFiles = allFiles.filter(f => !newFiles.has(`${pdf}/${f}`.toLowerCase()));
    
    // Apply the size filter
    oldStateFiles = oldStateFiles.filter(f => fs.statSync(path.join(pdfDir, f)).size >= 30000);
    
    // Sort
    oldStateFiles.sort((a, b) => (parseInt(a.replace(/\D/g, '')) || 0) - (parseInt(b.replace(/\D/g, '')) || 0));
    
    // Map the old indices to the mainImg filename
    for (let i = 0; i < oldStateFiles.length; i += 3) {
        const setIndex = i / 3;
        const setId = `${pdf}-set-${setIndex}`;
        const mainImg = oldStateFiles[i];
        
        // If this setId had a mapping, translate it to the mainImg
        if (oldMapping[setId]) {
            newMapping[`${pdf}-${mainImg}`] = oldMapping[setId];
        }
    }
}

// 3. Save the new mapping
fs.writeFileSync('product_mapping_by_img.json', JSON.stringify(newMapping, null, 2));
console.log("Translated mapping to product_mapping_by_img.json");
