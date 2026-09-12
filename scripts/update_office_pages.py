import json
import re

office_data = [
    {
        'sku': '2715',
        'title_zh': '2715 折叠书桌',
        'title_en': '2715 Folding Study Desk',
        'img': '../../assets/images/pj_office/pj-2715.jpg',
        'img_en': '../assets/images/pj_office/pj-2715.jpg',
        'dim': '47"W x 24"D x 29"H',
        'price': '49.95',
        'color': '',
        'pack': '1',
        'note_zh': '说明：图片中的办公椅仅为场景展示，不包含在本商品内。',
        'note_en': 'Note: Office chair shown for staging only; not included.',
        'pdf_spec': 'STUDY DESK | FOLDING TABLE'
    },
    {
        'sku': '2716',
        'title_zh': '2716 折叠书桌',
        'title_en': '2716 Folding Study Desk',
        'img': '../../assets/images/pj_office/pj-2716.jpg',
        'img_en': '../assets/images/pj_office/pj-2716.jpg',
        'dim': '47"W x 24"D x 29"H',
        'price': '59.95',
        'color': '',
        'pack': '1',
        'note_zh': '说明：图片中的办公椅仅为场景展示，不包含在本商品内。',
        'note_en': 'Note: Office chair shown for staging only; not included.',
        'pdf_spec': 'STUDY DESK | FOLDING TABLE'
    },
    {
        'sku': '4500TAUPE',
        'title_zh': '4500TAUPE 灰褐色书桌',
        'title_en': '4500TAUPE Taupe Study Desk',
        'img': '../../assets/images/pj_office/pj-4500taupe.jpg',
        'img_en': '../assets/images/pj_office/pj-4500taupe.jpg',
        'dim': '45"W x 18"D x 29"H',
        'price': '39.95',
        'color': 'TAUPE',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'STUDY DESK'
    },
    {
        'sku': '4500CA',
        'title_zh': '4500CA 咖啡色书桌',
        'title_en': '4500CA Cappuccino Study Desk',
        'img': '../../assets/images/pj_office/pj-4500ca.jpg',
        'img_en': '../assets/images/pj_office/pj-4500ca.jpg',
        'dim': '45"W x 18"D x 29"H',
        'price': '39.95',
        'color': 'CAPPUCCINO',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'STUDY DESK'
    },
    {
        'sku': '2704WH',
        'title_zh': '2704WH 白色框架书桌',
        'title_en': '2704WH Study Desk with White Frame',
        'img': '../../assets/images/pj_office/pj-2704wh.jpg',
        'img_en': '../assets/images/pj_office/pj-2704wh.jpg',
        'dim': '47.25"W x 24"D x 30"H',
        'price': '19.95',
        'color': 'WHITE',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'STUDY DESK'
    },
    {
        'sku': '2704BK',
        'title_zh': '2704BK 黑色框架书桌',
        'title_en': '2704BK Study Desk with Black Frame',
        'img': '../../assets/images/pj_office/pj-2704bk.jpg',
        'img_en': '../assets/images/pj_office/pj-2704bk.jpg',
        'dim': '47.25"W x 24"D x 30"H',
        'price': '19.95',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'STUDY DESK'
    },
    {
        'sku': '2709',
        'title_zh': '2709 带书架电脑桌',
        'title_en': '2709 Computer Desk with Upper Shelves',
        'img': '../../assets/images/pj_office/pj-2709.jpg',
        'img_en': '../assets/images/pj_office/pj-2709.jpg',
        'dim': '33"W x 18"D x 56"H',
        'price': '49.95',
        'color': '',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER DESK'
    },
    {
        'sku': '2714',
        'title_zh': '2714 玻璃台面多层电脑桌',
        'title_en': '2714 Multi-Level Computer Desk with Glass Top',
        'img': '../../assets/images/pj_office/pj-2714.jpg',
        'img_en': '../assets/images/pj_office/pj-2714.jpg',
        'dim': '24"W x 18"D x 29"H',
        'price': '39.95',
        'color': '',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER DESK WITH GLASS TOP'
    },
    {
        'sku': '2006GRAY',
        'title_zh': '2006GRAY 金属移动文件柜',
        'title_en': '2006GRAY Metal Filing Cabinet',
        'img': '../../assets/images/pj_office/pj-2006gray.jpg',
        'img_en': '../assets/images/pj_office/pj-2006gray.jpg',
        'dim': '11"W x 16.25"D x 27.25"H',
        'price': '49.95',
        'color': 'GRAY/WHITE',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'METAL CABINET'
    },
    {
        'sku': '2706',
        'title_zh': '2706 黑色软包电脑椅',
        'title_en': '2706 Black Padded Computer Chair',
        'img': '../../assets/images/pj_office/pj-2706.jpg',
        'img_en': '../assets/images/pj_office/pj-2706.jpg',
        'dim': '23.65"W x 24"D x 40.16"H',
        'price': '55.00',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2707',
        'title_zh': '2707 红黑电脑椅',
        'title_en': '2707 Red and Black Computer Chair',
        'img': '../../assets/images/pj_office/pj-2707.jpg',
        'img_en': '../assets/images/pj_office/pj-2707.jpg',
        'dim': '22"W x 21"D x 33-38"H',
        'price': '35.00',
        'color': 'BLACK/RED',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2708BK',
        'title_zh': '2708BK 网布主管椅',
        'title_en': '2708BK Director\'s Chair with Mesh Back',
        'img': '../../assets/images/pj_office/pj-2708bk.jpg',
        'img_en': '../assets/images/pj_office/pj-2708bk.jpg',
        'dim': '25"W x 25"D x 43-47"H',
        'price': '69.95',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'DIRECTOR\'S CHAIR WITH MESH BACK'
    },
    {
        'sku': '2720BK-RD',
        'title_zh': '2720BK-RD 电脑椅 (红黑)',
        'title_en': '2720BK-RD Computer Chair (Black-Red)',
        'img': '../../assets/images/pj_office/pj-2720bk-rd.jpg',
        'img_en': '../assets/images/pj_office/pj-2720bk-rd.jpg',
        'dim': '25"W x 24"D x 42"-46"H',
        'price': '85.00',
        'color': 'BLACK-RED',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2721BK-GRAY',
        'title_zh': '2721BK-GRAY 电脑椅 (灰黑)',
        'title_en': '2721BK-GRAY Computer Chair (Black-Gray)',
        'img': '../../assets/images/pj_office/pj-2721bk-gray.jpg',
        'img_en': '../assets/images/pj_office/pj-2721bk-gray.jpg',
        'dim': '25"W x 24"D x 42"-46"H',
        'price': '85.00',
        'color': 'BLACK-GRAY',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2722RD',
        'title_zh': '2722RD 电脑椅 (红色)',
        'title_en': '2722RD Computer Chair (Red)',
        'img': '../../assets/images/pj_office/pj-2722rd.jpg',
        'img_en': '../assets/images/pj_office/pj-2722rd.jpg',
        'dim': '28"W x 28"D x 43.5-47.5"H',
        'price': '109.95',
        'color': 'RED',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2723BK',
        'title_zh': '2723BK 电脑椅 (黑色)',
        'title_en': '2723BK Computer Chair (Black)',
        'img': '../../assets/images/pj_office/pj-2723bk.jpg',
        'img_en': '../assets/images/pj_office/pj-2723bk.jpg',
        'dim': '28"W x 28"D x 43.5-47.5"H',
        'price': '109.95',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2724BK',
        'title_zh': '2724BK 电脑椅 (黑色)',
        'title_en': '2724BK Computer Chair (Black)',
        'img': '../../assets/images/pj_office/pj-2724bk.jpg',
        'img_en': '../assets/images/pj_office/pj-2724bk.jpg',
        'dim': '25"W x 25"D x 43-46"H',
        'price': '99.95',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2724GRAY',
        'title_zh': '2724GRAY 电脑椅 (灰色)',
        'title_en': '2724GRAY Computer Chair (Gray)',
        'img': '../../assets/images/pj_office/pj-2724gray.jpg',
        'img_en': '../assets/images/pj_office/pj-2724gray.jpg',
        'dim': '25"W x 25"D x 43-46"H',
        'price': '99.95',
        'color': 'GRAY',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    },
    {
        'sku': '2725BK',
        'title_zh': '2725BK 办公电脑椅 (黑色)',
        'title_en': '2725BK Computer Chair (Black)',
        'img': '../../assets/images/pj_office/pj-2725bk.jpg',
        'img_en': '../assets/images/pj_office/pj-2725bk.jpg',
        'dim': '23"W x 22.5"D x 36.2-40"H',
        'price': '59.95',
        'color': 'BLACK',
        'pack': '1',
        'note_zh': '',
        'note_en': '',
        'pdf_spec': 'COMPUTER CHAIR'
    }
]

zh_cards_html = []
for item in office_data:
    color_tag = f'<span class="detail-tag">{item["color"]}</span>' if item['color'] else ''
    note_p = f'<p style="color:#b91c1c; font-size:0.85rem; margin-top:4px;">{item["note_zh"]}</p>' if item['note_zh'] else ''
    card = f'''        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="{item['img']}" alt="{item['title_zh']}" class="main-sofa-img" loading="lazy">
            </div>
            <div class="sofa-info">
                <h3>{item['title_zh']}</h3>
                <p>PDF 规格: {item['dim']} {item['color']}</p>
                {note_p}
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">特价 ${item['price']}</span>
                    <span class="detail-tag">{item['dim']}</span>
                    {color_tag}
                    <span class="detail-tag">PACK: {item['pack']}</span>
                </div>
            </div>
        </div>'''
    zh_cards_html.append(card)

en_cards_html = []
for item in office_data:
    color_tag = f'<span class="detail-tag">{item["color"]}</span>' if item['color'] else ''
    note_p = f'<p style="color:#b91c1c; font-size:0.85rem; margin-top:4px;">{item["note_en"]}</p>' if item['note_en'] else ''
    card = f'''        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="{item['img_en']}" alt="{item['title_en']}" class="main-sofa-img" loading="lazy">
            </div>
            <div class="sofa-info">
                <h3>{item['title_en']}</h3>
                <p>PDF Spec: {item['dim']} {item['color']}</p>
                {note_p}
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">Sale Price ${item['price']}</span>
                    <span class="detail-tag">{item['dim']}</span>
                    {color_tag}
                    <span class="detail-tag">PACK: {item['pack']}</span>
                </div>
            </div>
        </div>'''
    en_cards_html.append(card)

with open('zh/office/index.html', 'r', encoding='utf-8') as f:
    zh_html = f.read()

pattern = r'(<div class="sofa-grid">)[\s\S]*?(</div>\s*</main>)'
new_zh = re.sub(pattern, r'\1\n' + '\n\n'.join(zh_cards_html) + r'\n    \2', zh_html)
with open('zh/office/index.html', 'w', encoding='utf-8') as f:
    f.write(new_zh)
print('Updated zh/office/index.html')

with open('office/index.html', 'r', encoding='utf-8') as f:
    en_html = f.read()

new_en = re.sub(pattern, r'\1\n' + '\n\n'.join(en_cards_html) + r'\n    \2', en_html)
with open('office/index.html', 'w', encoding='utf-8') as f:
    f.write(new_en)
print('Updated office/index.html')

coords_map = {
    '2715': (80, '(425, 140, 630, 440)'),
    '2716': (80, '(635, 140, 850, 440)'),
    '4500TAUPE': (80, '(50, 140, 230, 440)'),
    '4500CA': (80, '(235, 140, 415, 440)'),
    '2704WH': (80, '(880, 50, 1160, 230)'),
    '2704BK': (80, '(1160, 50, 1440, 230)'),
    '2709': (80, '(1230, 280, 1450, 510)'),
    '2714': (80, '(910, 280, 1200, 510)'),
    '2006GRAY': (79, '(1080, 150, 1620, 580)'),
    '2706': (81, '(90, 310, 310, 520)'),
    '2707': (81, '(90, 40, 310, 240)'),
    '2708BK': (81, '(320, 310, 550, 520)'),
    '2720BK-RD': (81, '(1060, 40, 1290, 250)'),
    '2721BK-GRAY': (81, '(1300, 40, 1540, 250)'),
    '2722RD': (81, '(1060, 320, 1290, 540)'),
    '2723BK': (81, '(1300, 320, 1540, 540)'),
    '2724BK': (81, '(560, 40, 780, 240)'),
    '2724GRAY': (81, '(560, 310, 780, 520)'),
    '2725BK': (81, '(320, 40, 550, 240)')
}

manifest_items = []
for item in office_data:
    pno, c_coords = coords_map.get(item['sku'], (80, '(0, 0, 100, 100)'))
    manifest_items.append({
        'sku': item['sku'],
        'sku_normalized': item['sku'],
        'pdf_file_page': pno,
        'crop_coords': c_coords,
        'output_image': f"assets/images/pj_office/pj-{item['sku'].lower()}.jpg",
        'title_zh': item['title_zh'],
        'title_en': item['title_en'],
        'product_type_raw': item['pdf_spec'],
        'dimensions_raw': item['dim'],
        'color_raw': item['color'],
        'pack_raw': item['pack'],
        'price': item['price'],
        'price_source': 'PJ Warehouse Price List 2026',
        'staging_note_zh': item['note_zh'],
        'staging_note_en': item['note_en'],
        'is_same_category': True,
        'status': 'verified_1to1_crop',
        'publish': True,
        'ai_visual_reviewed': False,
        'human_reviewed': False,
        'verification_status': 'failed_visual_description_audit'
    })

with open('reports/manifest_v2_office.json', 'w', encoding='utf-8') as f:
    json.dump(manifest_items, f, ensure_ascii=False, indent=2)

print('Updated reports/manifest_v2_office.json with failed_visual_description_audit.')
