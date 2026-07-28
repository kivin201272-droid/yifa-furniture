const fs = require('fs');

function setupOffice() {
    // English page
    let enHtml = fs.readFileSync('office/index.html', 'utf-8');
    enHtml = enHtml.replace(/<title>Mattress Collection/g, '<title>Office Furniture Collection');
    enHtml = enHtml.replace(/Yifa Furniture's Mattress collection/g, "Yifa Furniture's Office collection");
    enHtml = enHtml.replace(/href="\.\.\/zh\/mattress\/"/g, 'href="../zh/office/"');
    enHtml = enHtml.replace(/<span>Mattress<\/span>/g, '<span>Office</span>');
    enHtml = enHtml.replace(/<h1>Mattress<\/h1>/g, '<h1>Office</h1>');
    fs.writeFileSync('office/index.html', enHtml);

    // Chinese page
    let zhHtml = fs.readFileSync('zh/office/index.html', 'utf-8');
    zhHtml = zhHtml.replace(/<title>Mattress Collection \| 优质床垫系列/g, '<title>Office Furniture Collection | 优质办公系列');
    zhHtml = zhHtml.replace(/Yifa Furniture's Mattress collection/g, "Yifa Furniture's Office collection");
    zhHtml = zhHtml.replace(/href="\.\.\/\.\.\/mattress\/"/g, 'href="../../office/"');
    zhHtml = zhHtml.replace(/<span>床垫<\/span>/g, '<span>办公</span>');
    zhHtml = zhHtml.replace(/<h1>优质床垫系列<\/h1>/g, '<h1>优质办公系列</h1>');
    fs.writeFileSync('zh/office/index.html', zhHtml);
}

setupOffice();
