const fs = require('fs');
const path = require('path');

// ==========================================
// 1. UPDATE MATTRESS PAGES (ZH & EN)
// ==========================================
function updateMattress() {
    const zhPath = path.join(__dirname, 'zh/mattress/index.html');
    const enPath = path.join(__dirname, 'mattress/index.html');

    const zhMattressCards = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/mattress/beautyrest-black-front.jpg?v=20260907" alt="Beautyrest BLACK" class="main-sofa-img" id="mattress-beautyrest-black-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/mattress/beautyrest-black-front.jpg?v=20260907" alt="Front View" class="sofa-thumb active" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
                <img src="../../assets/images/mattress/beautyrest-black-detail.jpg?v=20260907" alt="Top Detail" class="sofa-thumb" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
                <img src="../../assets/images/mattress/beautyrest-black.jpg?v=20260907" alt="Room View" class="sofa-thumb" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
            </div>
            <div class="sofa-info">
                <h3>Beautyrest BLACK</h3>
                <p>黑标顶级奢华护脊床垫</p>
                <div class="sofa-details">
                    <span class="detail-tag">旗舰款</span>
                    <span class="detail-tag">50% OFF</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/mattress/classic-luxury-ocean.jpg?v=20260907" alt="Luxury Deep Sleep" class="main-sofa-img" id="mattress-luxury-ocean-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/mattress/classic-luxury-ocean.jpg?v=20260907" alt="Detail" class="sofa-thumb active" onclick="changeImage(this, 'mattress-luxury-ocean-main')">
            </div>
            <div class="sofa-info">
                <h3>Luxury Deep Sleep</h3>
                <p>星级酒店尊享舒压床垫</p>
                <div class="sofa-details">
                    <span class="detail-tag">热销</span>
                    <span class="detail-tag">精选</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/mattress/TH-163.jpg?v=20260907" alt="163# 半棕垫" class="main-sofa-img" id="mattress-th-163-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/mattress/TH-163.jpg?v=20260907" alt="163#" class="sofa-thumb active" onclick="changeImage(this, 'mattress-th-163-main')">
            </div>
            <div class="sofa-info">
                <h3>163# 半棕垫</h3>
                <p>天然环保护脊硬棕床垫 (2寸/4寸可选)</p>
                <div class="sofa-details">
                    <span class="detail-tag">护脊护腰</span>
                    <span class="detail-tag">天然椰棕</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/mattress/TH-318.jpg?v=20260907" alt="TH318#" class="main-sofa-img" id="mattress-th-318-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/mattress/TH-318.jpg?v=20260907" alt="TH318#" class="sofa-thumb active" onclick="changeImage(this, 'mattress-th-318-main')">
            </div>
            <div class="sofa-info">
                <h3>TH318#</h3>
                <p>五星级奢华云感乳胶独立弹簧床垫</p>
                <div class="sofa-details">
                    <span class="detail-tag">云感承托</span>
                    <span class="detail-tag">独立弹簧</span>
                </div>
            </div>
        </div>`;

    const enMattressCards = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../assets/images/mattress/beautyrest-black-front.jpg?v=20260907" alt="Beautyrest BLACK" class="main-sofa-img" id="mattress-beautyrest-black-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../assets/images/mattress/beautyrest-black-front.jpg?v=20260907" alt="Front View" class="sofa-thumb active" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
                <img src="../assets/images/mattress/beautyrest-black-detail.jpg?v=20260907" alt="Top Detail" class="sofa-thumb" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
                <img src="../assets/images/mattress/beautyrest-black.jpg?v=20260907" alt="Room View" class="sofa-thumb" onclick="changeImage(this, 'mattress-beautyrest-black-main')">
            </div>
            <div class="sofa-info">
                <h3>Beautyrest BLACK</h3>
                <p>Ultra Luxury Spine Support Mattress</p>
                <div class="sofa-details">
                    <span class="detail-tag">Flagship</span>
                    <span class="detail-tag">50% OFF</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../assets/images/mattress/classic-luxury-ocean.jpg?v=20260907" alt="Luxury Deep Sleep" class="main-sofa-img" id="mattress-luxury-ocean-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../assets/images/mattress/classic-luxury-ocean.jpg?v=20260907" alt="Detail" class="sofa-thumb active" onclick="changeImage(this, 'mattress-luxury-ocean-main')">
            </div>
            <div class="sofa-info">
                <h3>Luxury Deep Sleep</h3>
                <p>Hotel Quality Pressure Relief Mattress</p>
                <div class="sofa-details">
                    <span class="detail-tag">Popular</span>
                    <span class="detail-tag">Featured</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../assets/images/mattress/TH-163.jpg?v=20260907" alt="163# Coir Mattress" class="main-sofa-img" id="mattress-th-163-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../assets/images/mattress/TH-163.jpg?v=20260907" alt="163#" class="sofa-thumb active" onclick="changeImage(this, 'mattress-th-163-main')">
            </div>
            <div class="sofa-info">
                <h3>163# Natural Coir Mattress</h3>
                <p>Firm Spine Support Coconut Palm Mattress (2" / 4")</p>
                <div class="sofa-details">
                    <span class="detail-tag">Firm Support</span>
                    <span class="detail-tag">Natural Coir</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../assets/images/mattress/TH-318.jpg?v=20260907" alt="TH318#" class="main-sofa-img" id="mattress-th-318-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../assets/images/mattress/TH-318.jpg?v=20260907" alt="TH318#" class="sofa-thumb active" onclick="changeImage(this, 'mattress-th-318-main')">
            </div>
            <div class="sofa-info">
                <h3>TH318#</h3>
                <p>Five-Star Luxury Latex Pocket Spring Pillow Top</p>
                <div class="sofa-details">
                    <span class="detail-tag">Latex Pillow Top</span>
                    <span class="detail-tag">Pocket Spring</span>
                </div>
            </div>
        </div>`;

    // Replace top cards in zh
    let zhHtml = fs.readFileSync(zhPath, 'utf8');
    const zhPattern = /<div class="sofa-grid">[\s\S]*?<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\.\/\.\.\/assets\/images\/pdf6\/N6001\.png"/;
    zhHtml = zhHtml.replace(zhPattern, `<div class="sofa-grid">${zhMattressCards}\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/pdf6/N6001.png"`);
    fs.writeFileSync(zhPath, zhHtml, 'utf8');
    console.log("Updated zh/mattress/index.html");

    // Replace top cards in en
    let enHtml = fs.readFileSync(enPath, 'utf8');
    const enPattern = /<div class="sofa-grid">[\s\S]*?<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\.\/assets\/images\/pdf6\/N6001\.png"/;
    enHtml = enHtml.replace(enPattern, `<div class="sofa-grid">${enMattressCards}\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/pdf6/N6001.png"`);
    fs.writeFileSync(enPath, enHtml, 'utf8');
    console.log("Updated mattress/index.html");
}

// ==========================================
// 2. UPDATE BEDROOM PAGES (ZH & EN)
// ==========================================
function updateBedroom() {
    const zhPath = path.join(__dirname, 'zh/bedroom/index.html');
    const enPath = path.join(__dirname, 'bedroom/index.html');

    const zhBedroomCards = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-818-main.jpg?v=20260907" alt="818#" class="main-sofa-img" id="th-818-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-818-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-818-main')">
                <img src="../../assets/images/th/TH-818-detail-1.jpg?v=20260907" alt="Drawers" class="sofa-thumb" onclick="changeImage(this, 'th-818-main')">
                <img src="../../assets/images/th/TH-818-detail-2.jpg?v=20260907" alt="Bed Front" class="sofa-thumb" onclick="changeImage(this, 'th-818-main')">
            </div>
            <div class="sofa-info">
                <h3>818#</h3>
                <p>818# 原木实木抽屉储物床组</p>
                <div class="sofa-details">
                    <span class="detail-tag">实木储物</span>
                    <span class="detail-tag">Queen/Full/Twin</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-IB108Q-main.jpg?v=20260907" alt="IB-108Q" class="main-sofa-img" id="th-ib108q-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-IB108Q-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-ib108q-main')">
            </div>
            <div class="sofa-info">
                <h3>IB-108Q</h3>
                <p>IB-108Q 现代金属皮艺软包床架</p>
                <div class="sofa-details">
                    <span class="detail-tag">金属框架</span>
                    <span class="detail-tag">稳固耐用</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-B0188-main.jpg?v=20260907" alt="B-0188" class="main-sofa-img" id="th-b0188-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-B0188-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-b0188-main')">
            </div>
            <div class="sofa-info">
                <h3>B-0188</h3>
                <p>B-0188 极简轻奢金属软包双人床</p>
                <div class="sofa-details">
                    <span class="detail-tag">现代极简</span>
                    <span class="detail-tag">精选</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-B1902-main.jpg?v=20260907" alt="B1902#" class="main-sofa-img" id="th-b1902-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-B1902-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-b1902-main')">
                <img src="../../assets/images/th/TH-B1902-detail-1.jpg?v=20260907" alt="Headboard" class="sofa-thumb" onclick="changeImage(this, 'th-b1902-main')">
                <img src="../../assets/images/th/TH-B1902-detail-2.jpg?v=20260907" alt="Bed Front" class="sofa-thumb" onclick="changeImage(this, 'th-b1902-main')">
                <img src="../../assets/images/th/TH-B1902-detail-3.jpg?v=20260907" alt="Drawer" class="sofa-thumb" onclick="changeImage(this, 'th-b1902-main')">
            </div>
            <div class="sofa-info">
                <h3>B1902#</h3>
                <p>B1902# 经典实木抽屉储物套房系列</p>
                <div class="sofa-details">
                    <span class="detail-tag">实木全套</span>
                    <span class="detail-tag">热销</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-836-main.jpg?v=20260907" alt="836#" class="main-sofa-img" id="th-836-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-836-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-836-main')">
                <img src="../../assets/images/th/TH-836-detail-1.jpg?v=20260907" alt="Nightstand" class="sofa-thumb" onclick="changeImage(this, 'th-836-main')">
            </div>
            <div class="sofa-info">
                <h3>836#</h3>
                <p>836# 经典弧形屏实木储物床组</p>
                <div class="sofa-details">
                    <span class="detail-tag">实木储物</span>
                    <span class="detail-tag">Queen/Full</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-839-main.jpg?v=20260907" alt="839#" class="main-sofa-img" id="th-839-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-839-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-839-main')">
                <img src="../../assets/images/th/TH-839-detail-1.jpg?v=20260907" alt="Dresser" class="sofa-thumb" onclick="changeImage(this, 'th-839-main')">
            </div>
            <div class="sofa-info">
                <h3>839#</h3>
                <p>839# 波浪顶实木储物双人床组</p>
                <div class="sofa-details">
                    <span class="detail-tag">实木精选</span>
                    <span class="detail-tag">全尺寸</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-B230-main.jpg?v=20260907" alt="B230#" class="main-sofa-img" id="th-b230-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-B230-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-b230-main')">
                <img src="../../assets/images/th/TH-B230-detail-1.jpg?v=20260907" alt="Wardrobe" class="sofa-thumb" onclick="changeImage(this, 'th-b230-main')">
                <img src="../../assets/images/th/TH-B230-detail-2.jpg?v=20260907" alt="Chest" class="sofa-thumb" onclick="changeImage(this, 'th-b230-main')">
                <img src="../../assets/images/th/TH-B230-detail-3.jpg?v=20260907" alt="Dresser" class="sofa-thumb" onclick="changeImage(this, 'th-b230-main')">
                <img src="../../assets/images/th/TH-B230-detail-4.jpg?v=20260907" alt="Bed Front" class="sofa-thumb" onclick="changeImage(this, 'th-b230-main')">
            </div>
            <div class="sofa-info">
                <h3>B230#</h3>
                <p>B230# 栅栏顶实木储物床与衣柜五件套</p>
                <div class="sofa-details">
                    <span class="detail-tag">大容量储物</span>
                    <span class="detail-tag">实木全套</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-9903-main.jpg?v=20260907" alt="TH9903#" class="main-sofa-img" id="th-9903-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-9903-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-9903-main')">
                <img src="../../assets/images/th/TH-9903-detail-1.jpg?v=20260907" alt="Showroom" class="sofa-thumb" onclick="changeImage(this, 'th-9903-main')">
            </div>
            <div class="sofa-info">
                <h3>TH9903#</h3>
                <p>TH9903# 欧式优雅拉扣白皮实木床组</p>
                <div class="sofa-details">
                    <span class="detail-tag">欧式轻奢</span>
                    <span class="detail-tag">热销</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-838-main.jpg?v=20260907" alt="838#" class="main-sofa-img" id="th-838-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-838-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-838-main')">
                <img src="../../assets/images/th/TH-838-detail-1.jpg?v=20260907" alt="Nightstand" class="sofa-thumb" onclick="changeImage(this, 'th-838-main')">
                <img src="../../assets/images/th/TH-838-detail-2.jpg?v=20260907" alt="Dresser" class="sofa-thumb" onclick="changeImage(this, 'th-838-main')">
            </div>
            <div class="sofa-info">
                <h3>838#</h3>
                <p>838# 现代简约实木储物床组</p>
                <div class="sofa-details">
                    <span class="detail-tag">实木大容量</span>
                    <span class="detail-tag">精选</span>
                </div>
            </div>
        </div>

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
        </div>

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
                <p>TH2506# 意式极简头层真皮软包床</p>
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
                <p>TH2503# 智能无线充皮艺软包床</p>
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
                <p>TH2608# 菱格纹意式轻奢皮艺齐边床</p>
                <div class="sofa-details">
                    <span class="detail-tag">意式轻奢</span>
                    <span class="detail-tag">菱格绗缝</span>
                </div>
            </div>
        </div>`;

    const enBedroomCards = zhBedroomCards
        .replace(/\.\.\/\.\.\/assets/g, '../assets')
        .replace(/原木实木抽屉储物床组/g, 'Solid Wood Storage Bedroom Set')
        .replace(/现代金属皮艺软包床架/g, 'Modern Metal Frame Upholstered Bed')
        .replace(/极简轻奢金属软包双人床/g, 'Minimalist Metal & Padded Headboard Bed')
        .replace(/经典实木抽屉储物套房系列/g, 'Classic Wood Storage Bedroom Suite')
        .replace(/经典弧形屏实木储物床组/g, 'Classic Arched Wood Storage Bed Suite')
        .replace(/波浪顶实木储物双人床组/g, 'Wave Top Wood Storage Bed Suite')
        .replace(/栅栏顶实木储物床与衣柜五件套/g, 'Slat Wood Storage Bedroom & Wardrobe Suite')
        .replace(/欧式优雅拉扣白皮实木床组/g, 'Classic Tufted Leather Bed Suite')
        .replace(/现代简约实木储物床组/g, 'Modern Wood Storage Bedroom Suite')
        .replace(/日式多功能折叠沙发床/g, 'Japanese Folding Futon Sofa Bed')
        .replace(/意式极简头层真皮软包床/g, 'Italian Minimalist Leather Soft Bed')
        .replace(/智能无线充皮艺软包床/g, 'Smart Leather Bed with Wireless Charger')
        .replace(/菱格纹意式轻奢皮艺齐边床/g, 'Diamond Quilted Leather Platform Bed')
        .replace(/实木储物/g, 'Storage')
        .replace(/金属框架/g, 'Metal Frame')
        .replace(/稳固耐用/g, 'Durable')
        .replace(/现代极简/g, 'Minimalist')
        .replace(/精选/g, 'Featured')
        .replace(/实木全套/g, 'Solid Wood')
        .replace(/热销/g, 'Popular')
        .replace(/实木精选/g, 'Solid Wood')
        .replace(/全尺寸/g, 'All Sizes')
        .replace(/大容量储物/g, 'Extra Storage')
        .replace(/欧式轻奢/g, 'Luxury')
        .replace(/实木大容量/g, 'Storage')
        .replace(/坐卧两用/g, 'Dual Mode')
        .replace(/节省空间/g, 'Space Saving')
        .replace(/极简意式/g, 'Italian Design')
        .replace(/头层真皮/g, 'Genuine Leather')
        .replace(/智能充电柜/g, 'Smart Charger')
        .replace(/轻奢皮艺/g, 'Leather Soft')
        .replace(/意式轻奢/g, 'Modern Luxury')
        .replace(/菱格绗缝/g, 'Diamond Tufted');

    // Insert after TH Collection Special Card in zh
    let zhHtml = fs.readFileSync(zhPath, 'utf8');
    const zhSpecialEnd = '<!-- TH Collection Special Card -->';
    const zhSplitPoint = zhHtml.indexOf('</div>\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/pdf3/img-008.jpg"');
    
    if (zhSplitPoint !== -1) {
        zhHtml = zhHtml.slice(0, zhSplitPoint + 6) + '\n' + zhBedroomCards + zhHtml.slice(zhSplitPoint + 6);
        fs.writeFileSync(zhPath, zhHtml, 'utf8');
        console.log("Updated zh/bedroom/index.html");
    }

    // Insert in en
    let enHtml = fs.readFileSync(enPath, 'utf8');
    const enSplitPoint = enHtml.indexOf('</div>\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/pdf3/img-008.jpg"');
    if (enSplitPoint !== -1) {
        enHtml = enHtml.slice(0, enSplitPoint + 6) + '\n' + enBedroomCards + enHtml.slice(enSplitPoint + 6);
        fs.writeFileSync(enPath, enHtml, 'utf8');
        console.log("Updated bedroom/index.html");
    }
}

// ==========================================
// 3. UPDATE LIVING ROOM PAGES (ZH & EN)
// ==========================================
function updateLivingRoom() {
    const zhPath = path.join(__dirname, 'zh/living-room/index.html');
    const enPath = path.join(__dirname, 'living-room/index.html');

    const zhLivingCards = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/massage-chair/D09.png?v=20260907" alt="D09 豪华按摩椅" class="main-sofa-img" id="massage-chair-D09-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/massage-chair/D09.png?v=20260907" alt="D09" class="sofa-thumb active" onclick="changeImage(this, 'massage-chair-D09-main')">
            </div>
            <div class="sofa-info">
                <h3>D09</h3>
                <p>豪华多功能全自动按摩椅</p>
                <div class="sofa-details">
                    <span class="detail-tag">按摩椅系列</span>
                    <span class="detail-tag">新品上市</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/massage-chair/989.png?v=20260907" alt="989 太空舱按摩椅" class="main-sofa-img" id="massage-chair-989-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/massage-chair/989.png?v=20260907" alt="989" class="sofa-thumb active" onclick="changeImage(this, 'massage-chair-989-main')">
            </div>
            <div class="sofa-info">
                <h3>989</h3>
                <p>太空舱零重力智能按摩椅</p>
                <div class="sofa-details">
                    <span class="detail-tag">按摩椅系列</span>
                    <span class="detail-tag">新品上市</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-SF02-main.jpg?v=20260907" alt="TH-SF02" class="main-sofa-img" id="th-sf02-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-SF02-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-sf02-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-SF02</h3>
                <p>TH-SF02 多功能拉伸储物充电沙发床</p>
                <div class="sofa-details">
                    <span class="detail-tag">坐卧两用</span>
                    <span class="detail-tag">USB充电</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-SF801-3-main.jpg?v=20260907" alt="TH-SF801" class="main-sofa-img" id="th-sf801-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-SF801-3-main.jpg?v=20260907" alt="3-Seater" class="sofa-thumb active" onclick="changeImage(this, 'th-sf801-main')">
                <img src="../../assets/images/th/TH-SF801-2-main.jpg?v=20260907" alt="2-Seater" class="sofa-thumb" onclick="changeImage(this, 'th-sf801-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-SF801</h3>
                <p>TH-SF801 现代简约舒适皮艺三人位/双人位沙发</p>
                <div class="sofa-details">
                    <span class="detail-tag">头层牛皮</span>
                    <span class="detail-tag">3+2套组</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-SF802-main.jpg?v=20260907" alt="TH-SF802" class="main-sofa-img" id="th-sf802-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-SF802-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-sf802-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-SF802</h3>
                <p>TH-SF802 现代极简真皮L型转角贵妃沙发</p>
                <div class="sofa-details">
                    <span class="detail-tag">可调头枕</span>
                    <span class="detail-tag">极简金属脚</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-SF803-main.jpg?v=20260907" alt="TH-SF803" class="main-sofa-img" id="th-sf803-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-SF803-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-sf803-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-SF803</h3>
                <p>TH-SF803 豪华头等舱电动真皮转角功能沙发</p>
                <div class="sofa-details">
                    <span class="detail-tag">电动躺位</span>
                    <span class="detail-tag">头等舱体验</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-DJ6661-main.jpg?v=20260907" alt="DJ-6661" class="main-sofa-img" id="th-dj6661-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-DJ6661-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-dj6661-main')">
            </div>
            <div class="sofa-info">
                <h3>DJ-6661</h3>
                <p>DJ-6661 多功能真皮/PVC电动可调节转角沙发</p>
                <div class="sofa-details">
                    <span class="detail-tag">单电机电动位</span>
                    <span class="detail-tag">3头枕调节</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-SF805-main.jpg?v=20260907" alt="TH-SF805" class="main-sofa-img" id="th-sf805-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-SF805-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-sf805-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-SF805</h3>
                <p>TH-SF805 弧形大转角头等舱双电动躺位真皮沙发</p>
                <div class="sofa-details">
                    <span class="detail-tag">双电动躺位</span>
                    <span class="detail-tag">超宽大转角</span>
                </div>
            </div>
        </div>`;

    const enLivingCards = zhLivingCards
        .replace(/\.\.\/\.\.\/assets/g, '../assets')
        .replace(/豪华多功能全自动按摩椅/g, 'Luxury Full-Body Automatic Massage Chair')
        .replace(/太空舱零重力智能按摩椅/g, 'Zero-Gravity Smart Capsule Massage Chair')
        .replace(/多功能拉伸储物充电沙发床/g, 'Multifunctional Pull-Out Sofa Bed with USB Charging')
        .replace(/现代简约舒适皮艺三人位\/双人位沙发/g, 'Modern Leather 3-Seater & Loveseat Sofa Set')
        .replace(/现代极简真皮L型转角贵妃沙发/g, 'Modern Minimalist Leather L-Shape Sectional Sofa')
        .replace(/豪华头等舱电动真皮转角功能沙发/g, 'Luxury First-Class Power Reclining Sectional Sofa')
        .replace(/多功能真皮\/PVC电动可调节转角沙发/g, 'Leather/PVC Power Reclining Sectional Sofa')
        .replace(/弧形大转角头等舱双电动躺位真皮沙发/g, 'Curved Corner Dual Power Reclining Leather Sofa')
        .replace(/按摩椅系列/g, 'Massage Chair')
        .replace(/新品上市/g, 'New Arrival')
        .replace(/坐卧两用/g, 'Dual Function')
        .replace(/USB充电/g, 'USB Charging')
        .replace(/头层牛皮/g, 'Top-Grain Leather')
        .replace(/3\+2套组/g, '3+2 Set')
        .replace(/可调头枕/g, 'Adjustable Headrests')
        .replace(/极简金属脚/g, 'Metal Legs')
        .replace(/电动躺位/g, 'Power Recliner')
        .replace(/头等舱体验/g, 'First-Class')
        .replace(/单电机电动位/g, 'Power Motor')
        .replace(/3头枕调节/g, '3 Adjustable Headrests')
        .replace(/双电动躺位/g, 'Dual Power Recliners')
        .replace(/超宽大转角/g, 'Curved Sectional');

    // Replace cards in zh living room
    let zhHtml = fs.readFileSync(zhPath, 'utf8');
    const zhTopPattern = /<div class="sofa-grid">\s*<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?请点击查看更多产品<\/a>\s*<\/div>\s*<\/div>[\s\S]*?<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\.\/\.\.\/assets\/images\/pdf1\/img-001\.jpg"/;
    
    const zhThBanner = `<div class="sofa-card reveal" style="grid-column: 1 / -1; display: flex; flex-direction: row; border: 2px solid var(--accent); border-radius: 8px; overflow: hidden; background: #fff;">
            <div style="flex: 0.75; position: relative;">
                <img src="../../assets/images/th-living-room.png" alt="TH 系列产品" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="sofa-info" style="text-align: center; padding: 40px 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="margin-bottom: 20px; font-size: 1.8rem; font-weight: 700;">TH 系列产品</h3>
                <a href="https://th-nycfurniture.com/#cat-btn-1" target="_blank" class="btn btn-primary" style="padding: 16px 32px; font-size: 1.15rem; font-weight: bold; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">请点击查看更多产品</a>
            </div>
        </div>`;

    zhHtml = zhHtml.replace(zhTopPattern, `<div class="sofa-grid">\n        ${zhThBanner}\n${zhLivingCards}\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../../assets/images/pdf1/img-001.jpg"`);
    fs.writeFileSync(zhPath, zhHtml, 'utf8');
    console.log("Updated zh/living-room/index.html");

    // Replace cards in en living room
    let enHtml = fs.readFileSync(enPath, 'utf8');
    const enTopPattern = /<div class="sofa-grid">\s*<div class="sofa-card reveal" style="grid-column: 1 \/ -1;[\s\S]*?Click to view more products<\/a>\s*<\/div>\s*<\/div>[\s\S]*?<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\.\/assets\/images\/pdf1\/img-001\.jpg"/;
    
    const enThBanner = `<div class="sofa-card reveal" style="grid-column: 1 / -1; display: flex; flex-direction: row; border: 2px solid var(--accent); border-radius: 8px; overflow: hidden; background: #fff;">
            <div style="flex: 0.75; position: relative;">
                <img src="../assets/images/th-living-room.png" alt="TH Collection Products" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="sofa-info" style="text-align: center; padding: 40px 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="margin-bottom: 20px; font-size: 1.8rem; font-weight: 700;">TH Collection Products</h3>
                <a href="https://th-nycfurniture.com/#cat-btn-1" target="_blank" class="btn btn-primary" style="padding: 16px 32px; font-size: 1.15rem; font-weight: bold; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">Click to view more products</a>
            </div>
        </div>`;

    enHtml = enHtml.replace(enTopPattern, `<div class="sofa-grid">\n        ${enThBanner}\n${enLivingCards}\n        <div class="sofa-card reveal">\n            <div class="sofa-img-container">\n                <img src="../assets/images/pdf1/img-001.jpg"`);
    fs.writeFileSync(enPath, enHtml, 'utf8');
    console.log("Updated living-room/index.html");
}

// ==========================================
// 4. UPDATE DINING PAGES (ZH & EN)
// ==========================================
function updateDining() {
    const zhPath = path.join(__dirname, 'zh/dining/index.html');
    const enPath = path.join(__dirname, 'dining/index.html');

    const zhDiningCards = `
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-BZ0396-main.jpg?v=20260907" alt="BZ-0396" class="main-sofa-img" id="th-bz0396-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-BZ0396-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-bz0396-main')">
            </div>
            <div class="sofa-info">
                <h3>BZ-0396 / BY-0396</h3>
                <p>BZ-0396 大理石纹折叠伸缩餐桌 + BY-0396 餐椅套组</p>
                <div class="sofa-details">
                    <span class="detail-tag">可伸缩折叠</span>
                    <span class="detail-tag">1350*(800-1250)</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-BZ2192-main.jpg?v=20260907" alt="BZ-2192" class="main-sofa-img" id="th-bz2192-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-BZ2192-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-bz2192-main')">
            </div>
            <div class="sofa-info">
                <h3>BZ-2192 / RJ-366</h3>
                <p>BZ-2192 奶油白轻奢圆变方伸缩餐桌 + RJ-366 餐椅套组</p>
                <div class="sofa-details">
                    <span class="detail-tag">圆桌变方桌</span>
                    <span class="detail-tag">1300*(800-1300)</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-BZ0296-main.jpg?v=20260907" alt="BZ-0296" class="main-sofa-img" id="th-bz0296-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-BZ0296-main.jpg?v=20260907" alt="Main" class="sofa-thumb active" onclick="changeImage(this, 'th-bz0296-main')">
            </div>
            <div class="sofa-info">
                <h3>BZ-0296 / BY-0296</h3>
                <p>BZ-0296 现代岩板储物柱转盘餐桌 + BY-0296 餐椅套组</p>
                <div class="sofa-details">
                    <span class="detail-tag">中央储物柱</span>
                    <span class="detail-tag">岩板转盘</span>
                </div>
            </div>
        </div>

        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../assets/images/th/TH-DT04-1-main.jpg?v=20260907" alt="TH-DT04" class="main-sofa-img" id="th-dt04-main" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
                <img src="../../assets/images/th/TH-DT04-1-main.jpg?v=20260907" alt="Square Mode" class="sofa-thumb active" onclick="changeImage(this, 'th-dt04-main')">
                <img src="../../assets/images/th/TH-DT04-2-main.jpg?v=20260907" alt="Round Mode" class="sofa-thumb" onclick="changeImage(this, 'th-dt04-main')">
            </div>
            <div class="sofa-info">
                <h3>TH-DT04</h3>
                <p>TH-DT04 轻奢旋转转盘圆方两用伸缩餐桌 (配4椅2凳全套)</p>
                <div class="sofa-details">
                    <span class="detail-tag">圆方两用</span>
                    <span class="detail-tag">含转盘椅凳全套</span>
                </div>
            </div>
        </div>`;

    const enDiningCards = zhDiningCards
        .replace(/\.\.\/\.\.\/assets/g, '../assets')
        .replace(/大理石纹折叠伸缩餐桌 \+ BY-0396 餐椅套组/g, 'Marble Extendable Dining Table & BY-0396 Chairs Set')
        .replace(/奶油白轻奢圆变方伸缩餐桌 \+ RJ-366 餐椅套组/g, 'Cream Round-to-Square Dining Table & RJ-366 Chairs Set')
        .replace(/现代岩板储物柱转盘餐桌 \+ BY-0296 餐椅套组/g, 'Ceramic Pedestal Storage Lazy Susan Table & Chairs Set')
        .replace(/轻奢旋转转盘圆方两用伸缩餐桌 \(配4椅2凳全套\)/g, 'Dual-Mode Extendable Lazy Susan Table with 4 Chairs & 2 Stools')
        .replace(/可伸缩折叠/g, 'Extendable')
        .replace(/圆桌变方桌/g, 'Round to Square')
        .replace(/中央储物柱/g, 'Pedestal Storage')
        .replace(/岩板转盘/g, 'Lazy Susan')
        .replace(/圆方两用/g, 'Dual Mode')
        .replace(/含转盘椅凳全套/g, 'Full Set with Stools');

    // Insert at top of sofa-grid in zh dining
    let zhHtml = fs.readFileSync(zhPath, 'utf8');
    const zhSplitPoint = zhHtml.indexOf('<div class="sofa-grid">');
    if (zhSplitPoint !== -1) {
        // Check if TH dining cards are already added
        if (!zhHtml.includes('TH-BZ0396')) {
            zhHtml = zhHtml.replace('<div class="sofa-grid">', `<div class="sofa-grid">\n${zhDiningCards}`);
            fs.writeFileSync(zhPath, zhHtml, 'utf8');
            console.log("Updated zh/dining/index.html");
        }
    }

    // Insert at top of sofa-grid in en dining
    let enHtml = fs.readFileSync(enPath, 'utf8');
    const enSplitPoint = enHtml.indexOf('<div class="sofa-grid">');
    if (enSplitPoint !== -1) {
        if (!enHtml.includes('TH-BZ0396')) {
            enHtml = enHtml.replace('<div class="sofa-grid">', `<div class="sofa-grid">\n${enDiningCards}`);
            fs.writeFileSync(enPath, enHtml, 'utf8');
            console.log("Updated dining/index.html");
        }
    }
}

updateMattress();
updateBedroom();
updateLivingRoom();
updateDining();
console.log("--- All products successfully integrated! ---");
