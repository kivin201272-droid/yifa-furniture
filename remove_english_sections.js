const fs = require('fs');
const path = require('path');

function removeEnglishSections(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Remove "What We Carry" / "Inside the collection"
    html = html.replace(/<section[^>]*>[\s\S]*?(?:What We Carry)[\s\S]*?<\/section>/g, '');

    // Remove "Mattresses" / "Mattresses to finish the set"
    html = html.replace(/<section[^>]*>[\s\S]*?(?:Mattresses to finish the set)[\s\S]*?<\/section>/g, '');

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        console.log(`Updated ${filePath}`);
    }
}

const folders = ['bedroom', 'living-room', 'dining', 'office', 'mattress'];

folders.forEach(folder => {
    removeEnglishSections(path.join(__dirname, folder, 'index.html'));
});
