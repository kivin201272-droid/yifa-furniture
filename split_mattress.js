const fs = require('fs');
const path = require('path');

function copyAndEmptyGrid(src, dest, titleSearch, titleReplace, langSwitchSearch, langSwitchReplace) {
    if (!fs.existsSync(src)) return;
    let html = fs.readFileSync(src, 'utf8');
    
    // Replace title
    html = html.replace(titleSearch, titleReplace);
    
    // Replace lang switch
    html = html.replace(langSwitchSearch, langSwitchReplace);

    // Empty the grid
    html = html.replace(/<div class="sofa-grid">[\s\S]*?<\/main>/, '<div class="sofa-grid">\n        <!-- Empty grid for now, user will provide items later -->\n    </div>\n</main>');
    
    fs.writeFileSync(dest, html);
    console.log(`Created ${dest}`);
}

function updateFile(filePath) {
    if (!fs.existsSync(filePath)) return;
    let html = fs.readFileSync(filePath, 'utf8');
    let original = html;

    // Update footers - English
    html = html.replace(/<li><a href=\.\.\/mattress\/>Mattress<\/a><\/li>/g, '<li><a href=../magical-mattress/>Magical Mattress</a></li><li><a href=../mattress/>Normal Mattress</a></li>');
    html = html.replace(/<li><a href=\.\/mattress\/>Mattress<\/a><\/li>/g, '<li><a href=./magical-mattress/>Magical Mattress</a></li><li><a href=./mattress/>Normal Mattress</a></li>');
    html = html.replace(/<li><a href=\.\.\/\.\.\/mattress\/>Mattress<\/a><\/li>/g, '<li><a href=../../magical-mattress/>Magical Mattress</a></li><li><a href=../../mattress/>Normal Mattress</a></li>');

    // Update footers - Chinese
    html = html.replace(/<li><a href=\.\.\/mattress\/>床垫系列<\/a><\/li>/g, '<li><a href=../magical-mattress/>神奇床垫</a></li><li><a href=../mattress/>普通床垫</a></li>');
    html = html.replace(/<li><a href=\.\/mattress\/>床垫系列<\/a><\/li>/g, '<li><a href=./magical-mattress/>神奇床垫</a></li><li><a href=./mattress/>普通床垫</a></li>');
    html = html.replace(/<li><a href=\.\.\/\.\.\/mattress\/>床垫系列<\/a><\/li>/g, '<li><a href=../../magical-mattress/>神奇床垫</a></li><li><a href=../../mattress/>普通床垫</a></li>');

    // Update specific links in products/index.html
    html = html.replace(/href=\.\.\/mattress\/>Explore Mattress<\/a>/g, 'href=../magical-mattress/>Explore Magical Mattress</a>');
    html = html.replace(/href=\.\.\/mattress\/>浏览床垫系列<\/a>/g, 'href=../magical-mattress/>浏览神奇床垫</a>');

    if (filePath.includes('/mattress/')) {
        // Change title in normal mattress
        html = html.replace('<title>Mattress Collection | 优质床垫系列 | Yifa</title>', '<title>Normal Mattress Collection | 普通床垫系列 | Yifa</title>');
        html = html.replace('<title>Mattress Collection | Yifa</title>', '<title>Normal Mattress Collection | Yifa</title>');
    }

    if (html !== original) {
        fs.writeFileSync(filePath, html);
        console.log(`Updated ${filePath}`);
    }
}

// 1. Create directories
if (!fs.existsSync('magical-mattress')) fs.mkdirSync('magical-mattress');
if (!fs.existsSync('zh/magical-mattress')) fs.mkdirSync('zh/magical-mattress');

// 2. Create magical-mattress files
copyAndEmptyGrid(
    'mattress/index.html', 
    'magical-mattress/index.html', 
    '<title>Mattress Collection | Yifa</title>', 
    '<title>Magical Mattress Collection | Yifa</title>',
    'href="../zh/mattress/"',
    'href="../zh/magical-mattress/"'
);

copyAndEmptyGrid(
    'zh/mattress/index.html', 
    'zh/magical-mattress/index.html', 
    '<title>Mattress Collection | 优质床垫系列 | Yifa</title>', 
    '<title>Magical Mattress Collection | 神奇床垫系列 | Yifa</title>',
    'href="../../mattress/"',
    'href="../../magical-mattress/"'
);

// 3. Update all files
const dirsToUpdate = [
    './', 'zh/', 'bedroom/', 'zh/bedroom/', 'living-room/', 'zh/living-room/',
    'dining/', 'zh/dining/', 'office/', 'zh/office/', 'mattress/', 'zh/mattress/',
    'products/', 'zh/products/', 'about/', 'zh/about/', 'contact/', 'zh/contact/',
    'faq/', 'zh/faq/', 'magical-mattress/', 'zh/magical-mattress/'
];

dirsToUpdate.forEach(dir => {
    const indexPath = path.join(__dirname, dir, 'index.html');
    updateFile(indexPath);
});

