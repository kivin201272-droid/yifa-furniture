const fs = require('fs');
const path = require('path');

// ==========================================
// 1. UPDATE FAQ PAGE (zh/faq/index.html)
// ==========================================
function updateFaq() {
    const zhFaq = path.join(__dirname, 'zh/faq/index.html');
    let html = fs.readFileSync(zhFaq, 'utf8');
    html = html.replace(
        /<div class="section-head center reveal"><span class=eyebrow>常见疑问<\/span><h2>合作须知<\/h2><\/div>/g,
        '<div class="section-head center reveal"><h2>常见疑问</h2></div>'
    );
    html = html.replace(
        /<span class=eyebrow>常见疑问<\/span><h2>合作须知<\/h2>/g,
        '<h2>常见疑问</h2>'
    );
    fs.writeFileSync(zhFaq, html, 'utf8');
    console.log("Updated zh/faq/index.html: removed 合作须知 and made 常见疑问 the main header.");
}

// ==========================================
// 2. UPDATE MATTRESS DESCRIPTIONS (ZH & EN)
// ==========================================
function updateMattressDetails() {
    const zhPath = path.join(__dirname, 'zh/mattress/index.html');
    const enPath = path.join(__dirname, 'mattress/index.html');

    // ZH
    let zhHtml = fs.readFileSync(zhPath, 'utf8');
    
    // Beautyrest BLACK
    const zhBeautyrestDesc = `<div class="sofa-info">
                <h3>Beautyrest BLACK</h3>
                <p>288-Beautyrest -Black Series II-14''2 Pillow Top Mattress 美国席梦思床垫，美国制造，质保 20 年。King size(78''x80'') 市场价: $3,280，55%OFF，折后$1,380</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">折后$1,380</span>
                    <span class="detail-tag">55% OFF</span>
                    <span class="detail-tag">质保20年</span>
                </div>
            </div>`;
    zhHtml = zhHtml.replace(/<div class="sofa-info">\s*<h3>Beautyrest BLACK<\/h3>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*classic-luxury-ocean\.jpg/m, `${zhBeautyrestDesc}\n        </div>\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/mattress/classic-luxury-ocean.jpg`);

    // Luxury Deep Sleep
    const zhLuxuryDesc = `<div class="sofa-info">
                <h3>Luxury Deep Sleep</h3>
                <p>美国 Sealy 品牌记忆棉床垫 CHINO 388-9''-T(39''x75'') 丝涟品牌床垫，市场价$1,380，折后$299，市场价$1,780，折后 F:$499，Q:$599，K:$888</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">折后$299起</span>
                    <span class="detail-tag">Sealy 品牌</span>
                    <span class="detail-tag">特惠</span>
                </div>
            </div>`;
    zhHtml = zhHtml.replace(/<div class="sofa-info">\s*<h3>Luxury Deep Sleep<\/h3>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-163\.jpg/m, `${zhLuxuryDesc}\n        </div>\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/mattress/TH-163.jpg`);

    fs.writeFileSync(zhPath, zhHtml, 'utf8');
    console.log("Updated zh/mattress/index.html with exact Beautyrest and Sealy descriptions.");

    // EN
    let enHtml = fs.readFileSync(enPath, 'utf8');
    const enBeautyrestDesc = `<div class="sofa-info">
                <h3>Beautyrest BLACK</h3>
                <p>288-Beautyrest -Black Series II-14''2 Pillow Top Mattress Made in USA, 20-Year Warranty. King size(78''x80'') MSRP: $3,280, 55% OFF, Sale: $1,380</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">Sale $1,380</span>
                    <span class="detail-tag">55% OFF</span>
                    <span class="detail-tag">20-Yr Warranty</span>
                </div>
            </div>`;
    enHtml = enHtml.replace(/<div class="sofa-info">\s*<h3>Beautyrest BLACK<\/h3>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*classic-luxury-ocean\.jpg/m, `${enBeautyrestDesc}\n        </div>\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/mattress/classic-luxury-ocean.jpg`);

    const enLuxuryDesc = `<div class="sofa-info">
                <h3>Luxury Deep Sleep</h3>
                <p>USA Sealy Memory Foam Mattress CHINO 388-9''-T(39''x75'') MSRP: $1,380, Sale: $299; MSRP: $1,780, Sale: F:$499, Q:$599, K:$888</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">From $299</span>
                    <span class="detail-tag">Sealy Brand</span>
                    <span class="detail-tag">Special Sale</span>
                </div>
            </div>`;
    enHtml = enHtml.replace(/<div class="sofa-info">\s*<h3>Luxury Deep Sleep<\/h3>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-163\.jpg/m, `${enLuxuryDesc}\n        </div>\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/mattress/TH-163.jpg`);

    fs.writeFileSync(enPath, enHtml, 'utf8');
    console.log("Updated mattress/index.html descriptions.");
}

// ==========================================
// 3. MOVE TH010# FROM BEDROOM TO LIVING ROOM
// ==========================================
function moveTH010() {
    const zhBed = path.join(__dirname, 'zh/bedroom/index.html');
    const enBed = path.join(__dirname, 'bedroom/index.html');
    const zhLiv = path.join(__dirname, 'zh/living-room/index.html');
    const enLiv = path.join(__dirname, 'living-room/index.html');

    // Remove from zh bedroom
    let zhBedHtml = fs.readFileSync(zhBed, 'utf8');
    zhBedHtml = zhBedHtml.replace(/<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-010-main\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/, '');
    fs.writeFileSync(zhBed, zhBedHtml, 'utf8');
    console.log("Removed TH010# from zh/bedroom/index.html");

    // Remove from en bedroom
    let enBedHtml = fs.readFileSync(enBed, 'utf8');
    enBedHtml = enBedHtml.replace(/<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-010-main\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/, '');
    fs.writeFileSync(enBed, enBedHtml, 'utf8');
    console.log("Removed TH010# from bedroom/index.html");

    // Add to zh living room (if not already there)
    let zhLivHtml = fs.readFileSync(zhLiv, 'utf8');
    if (!zhLivHtml.includes('TH-010-main.jpg')) {
        const zhTH010Card = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-010-main.jpg?v=20260907" alt="TH010#" class="main-sofa-img" id="th-010-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-010-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-010-main')">
                <img src="../../assets/images/th/TH-010-detail-1.jpg?v=20260907" alt="Bed Mode" class="sofa-thumb" onclick="changeImage(this, 'th-010-main')">
                <img src="../../assets/images/th/TH-010-detail-2.jpg?v=20260907" alt="Sofa Mode" class="sofa-thumb" onclick="changeImage(this, 'th-010-main')">
            </div>
            <div class="sofa-info">
                <h3>TH010#</h3>
                <p>TH010# 日式多功能折叠沙发床</p>
                <div class="sofa-details">
                    <span class="detail-tag">坐卧两用</span>
                    <span class="detail-tag">节省空间</span>
                </div>
            </div>
        </div>`;
        zhLivHtml = zhLivHtml.replace(/<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-SF02-main\.jpg/, `${zhTH010Card}\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/th/TH-SF02-main.jpg`);
        fs.writeFileSync(zhLiv, zhLivHtml, 'utf8');
        console.log("Added TH010# to zh/living-room/index.html");
    }

    // Add to en living room (if not already there)
    let enLivHtml = fs.readFileSync(enLiv, 'utf8');
    if (!enLivHtml.includes('TH-010-main.jpg')) {
        const enTH010Card = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../assets/images/th/TH-010-main.jpg?v=20260907" alt="TH010#" class="main-sofa-img" id="th-010-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../assets/images/th/TH-010-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-010-main')">
                <img src="../assets/images/th/TH-010-detail-1.jpg?v=20260907" alt="Bed Mode" class="sofa-thumb" onclick="changeImage(this, 'th-010-main')">
                <img src="../assets/images/th/TH-010-detail-2.jpg?v=20260907" alt="Sofa Mode" class="sofa-thumb" onclick="changeImage(this, 'th-010-main')">
            </div>
            <div class="sofa-info">
                <h3>TH010#</h3>
                <p>TH010# Japanese Folding Futon Sofa Bed</p>
                <div class="sofa-details">
                    <span class="detail-tag">Dual Mode</span>
                    <span class="detail-tag">Space Saving</span>
                </div>
            </div>
        </div>`;
        enLivHtml = enLivHtml.replace(/<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*TH-SF02-main\.jpg/, `${enTH010Card}\n\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/th/TH-SF02-main.jpg`);
        fs.writeFileSync(enLiv, enLivHtml, 'utf8');
        console.log("Added TH010# to living-room/index.html");
    }
}

updateFaq();
updateMattressDetails();
moveTH010();
console.log("--- All updates applied! ---");
