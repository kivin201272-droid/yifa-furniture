import re

zh_bed_path = 'zh/bedroom/index.html'
en_bed_path = 'bedroom/index.html'

with open(zh_bed_path, 'r', encoding='utf-8') as f:
    zh = f.read()

# Remove any existing TH2506, TH2503, TH2608 cards
for code in ['TH-2506', 'TH-2503', 'TH-2608']:
    zh = re.sub(r'<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*' + code + r'-main\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', zh)

zh_top_cards = '''
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
        </div>'''

# Place at top of sofa-grid
zh = zh.replace('<div class="sofa-grid">', '<div class="sofa-grid">\n' + zh_top_cards)
with open(zh_bed_path, 'w', encoding='utf-8') as f:
    f.write(zh)
print('Updated zh/bedroom/index.html with TH2506, TH2503, TH2608 at top!')

with open(en_bed_path, 'r', encoding='utf-8') as f:
    en = f.read()

for code in ['TH-2506', 'TH-2503', 'TH-2608']:
    en = re.sub(r'<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="[^"]*' + code + r'-main\.jpg[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', en)

en_top_cards = zh_top_cards.replace('../../assets', '../assets')\
    .replace('意式极简头层真皮软包床', 'Italian Minimalist Leather Soft Bed')\
    .replace('智能无线充皮艺软包床', 'Smart Leather Soft Bed with Wireless Charger')\
    .replace('菱格纹意式轻奢皮艺齐边床', 'Diamond Quilted Leather Platform Bed')\
    .replace('极简意式', 'Italian Design')\
    .replace('头层真皮', 'Genuine Leather')\
    .replace('智能充电柜', 'Smart Charger')\
    .replace('轻奢皮艺', 'Leather Soft')\
    .replace('意式轻奢', 'Modern Luxury')\
    .replace('菱格绗缝', 'Diamond Tufted')

en = en.replace('<div class="sofa-grid">', '<div class="sofa-grid">\n' + en_top_cards)
with open(en_bed_path, 'w', encoding='utf-8') as f:
    f.write(en)
print('Updated bedroom/index.html with TH2506, TH2503, TH2608 at top!')
