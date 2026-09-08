const fs = require('fs');
const path = require('path');

const zhBed = path.join(__dirname, 'zh/bedroom/index.html');
const enBed = path.join(__dirname, 'bedroom/index.html');
const zhMat = path.join(__dirname, 'zh/mattress/index.html');
const enMat = path.join(__dirname, 'mattress/index.html');

// 1. Remove from bedroom pages
['TH-2506', 'TH-2503', 'TH-2608'].forEach(code => {
    // ZH
    let zhBedHtml = fs.readFileSync(zhBed, 'utf8');
    const zhRegex = new RegExp(`<div class="sofa-card reveal">\\s*<div class="sofa-img-container">\\s*<img src="[^"]*${code}-main\\.jpg[\\s\\S]*?<\\/div>\\s*<\\/div>\\s*<\\/div>`, 'g');
    zhBedHtml = zhBedHtml.replace(zhRegex, '');
    fs.writeFileSync(zhBed, zhBedHtml, 'utf8');

    // EN
    let enBedHtml = fs.readFileSync(enBed, 'utf8');
    const enRegex = new RegExp(`<div class="sofa-card reveal">\\s*<div class="sofa-img-container">\\s*<img src="[^"]*${code}-main\\.jpg[\\s\\S]*?<\\/div>\\s*<\\/div>\\s*<\\/div>`, 'g');
    enBedHtml = enBedHtml.replace(enRegex, '');
    fs.writeFileSync(enBed, enBedHtml, 'utf8');
});
console.log("Removed TH2506#, TH2503#, TH2608# from bedroom pages.");

// 2. Add to Mattress pages
const zhMattressAdditions = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-2506-main.jpg?v=20260907" alt="TH2506#" class="main-sofa-img" id="th-2506-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-2506-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-2506-main')">
                <img src="../../assets/images/th/TH-2506-detail-1.jpg?v=20260907" alt="Headboard" class="sofa-thumb" onclick="changeImage(this, 'th-2506-main')">
                <img src="../../assets/images/th/TH-2506-detail-2.jpg?v=20260907" alt="Corner" class="sofa-thumb" onclick="changeImage(this, 'th-2506-main')">
            </div>
            <div class="sofa-info">
                <h3>TH2506#</h3>
                <p>TH2506# 意式极简头层真皮软包床垫组</p>
                <div class="sofa-details">
                    <span class="detail-tag">极简意式</span>
                    <span class="detail-tag">头层真皮</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-2503-main.jpg?v=20260907" alt="TH2503#" class="main-sofa-img" id="th-2503-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-2503-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-2503-main')">
                <img src="../../assets/images/th/TH-2503-detail-1.jpg?v=20260907" alt="Smart Table" class="sofa-thumb" onclick="changeImage(this, 'th-2503-main')">
            </div>
            <div class="sofa-info">
                <h3>TH2503#</h3>
                <p>TH2503# 智能无线充皮艺软包床垫组</p>
                <div class="sofa-details">
                    <span class="detail-tag">智能充电柜</span>
                    <span class="detail-tag">轻奢皮艺</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-2608-main.jpg?v=20260907" alt="TH2608#" class="main-sofa-img" id="th-2608-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-2608-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-2608-main')">
                <img src="../../assets/images/th/TH-2608-detail-1.jpg?v=20260907" alt="Base Frame" class="sofa-thumb" onclick="changeImage(this, 'th-2608-main')">
                <img src="../../assets/images/th/TH-2608-detail-2.jpg?v=20260907" alt="Room View" class="sofa-thumb" onclick="changeImage(this, 'th-2608-main')">
            </div>
            <div class="sofa-info">
                <h3>TH2608#</h3>
                <p>TH2608# 菱格纹意式轻奢皮艺齐边床垫组</p>
                <div class="sofa-details">
                    <span class="detail-tag">意式轻奢</span>
                    <span class="detail-tag">菱格绗缝</span>
                </div>
            </div>
        </div>`;

const enMattressAdditions = zhMattressAdditions
    .replace(/\.\.\/\.\.\/assets/g, '../assets')
    .replace(/意式极简头层真皮软包床垫组/g, 'Italian Minimalist Leather Soft Mattress Bed')
    .replace(/智能无线充皮艺软包床垫组/g, 'Smart Leather Soft Mattress Bed with Wireless Charger')
    .replace(/菱格纹意式轻奢皮艺齐边床垫组/g, 'Diamond Quilted Leather Platform Mattress Bed')
    .replace(/极简意式/g, 'Italian Design')
    .replace(/头层真皮/g, 'Genuine Leather')
    .replace(/智能充电柜/g, 'Smart Charger')
    .replace(/轻奢皮艺/g, 'Leather Soft')
    .replace(/意式轻奢/g, 'Modern Luxury')
    .replace(/菱格绗缝/g, 'Diamond Tufted');

let zhMatHtml = fs.readFileSync(zhMat, 'utf8');
if (!zhMatHtml.includes('TH-2506-main.jpg')) {
    zhMatHtml = zhMatHtml.replace(
        /<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-318\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/,
        match => `${match}\n${zhMattressAdditions}`
    );
    fs.writeFileSync(zhMat, zhMatHtml, 'utf8');
    console.log("Added TH2506#, TH2503#, TH2608# to zh/mattress/index.html");
}

let enMatHtml = fs.readFileSync(enMat, 'utf8');
if (!enMatHtml.includes('TH-2506-main.jpg')) {
    enMatHtml = enMatHtml.replace(
        /<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-318\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/,
        match => `${match}\n${enMattressAdditions}`
    );
    fs.writeFileSync(enMat, enMatHtml, 'utf8');
    console.log("Added TH2506#, TH2503#, TH2608# to mattress/index.html");
}
