import re, os, json

with open('src/data/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

# Curated pricing dictionary
CURATED = {
    'TH2506': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 499}, {'code': 'K', 'price': 599}], 'tags': ['意式极简', '头层真皮']},
    'TH2503': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 529}, {'code': 'K', 'price': 629}], 'tags': ['智能充电柜', '轻奢皮艺']},
    'TH2608': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 489}, {'code': 'K', 'price': 589}], 'tags': ['意式轻奢', '菱格绗缝']},
    '818': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 349}, {'code': 'Q', 'price': 399}], 'tags': ['实木储物', '三规格可选']},
    'IB-108Q': {'type': 'single', 'price': 299, 'tags': ['金属框架', '稳固耐用']},
    'B-0188': {'type': 'single', 'price': 329, 'tags': ['现代极简', '精选']},
    'B1902': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 459}, {'code': 'K', 'price': 559}], 'tags': ['实木全套', '热销']},
    '836': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 429}, {'code': 'K', 'price': 529}], 'tags': ['实木储物', '精选']},
    '839': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 439}, {'code': 'K', 'price': 539}], 'tags': ['实木全套', '热销']},
    'B230': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 469}, {'code': '5-PC', 'price': 1280}], 'tags': ['大容量储物', '实木全套']},
    'TH9903': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 559}, {'code': 'K', 'price': 659}], 'tags': ['欧式轻奢', '热销']},
    '838': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 429}, {'code': 'K', 'price': 529}], 'tags': ['实木大容量', '精选']},

    'BEAUTYREST BLACK': {'type': 'single', 'price': 1380, 'desc_zh': "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress 美国席梦思床垫，美国制造，质保 20 年。King size(78''x80'')", 'desc_en': "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress Made in USA, 20-Year Warranty. King size (78\"x80\")", 'tags_zh': ['55% OFF', '质保20年', '美国制造'], 'tags_en': ['55% OFF', '20-Yr Warranty', 'Made in USA']},
    'LUXURY DEEP SLEEP': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 499}, {'code': 'Q', 'price': 599}, {'code': 'K', 'price': 888}], 'desc_zh': "美国 Sealy 品牌记忆棉床垫 CHINO 388-9'' (39''x75'') 丝涟品牌床垫，独立袋装弹簧，高透气记忆棉支撑。", 'desc_en': "USA Sealy Memory Foam Mattress CHINO 388-9\" (39\"x75\"), pocketed coil system with breathable memory foam support.", 'tags_zh': ['55% OFF', 'SEALY 品牌', '特惠'], 'tags_en': ['55% OFF', 'Sealy Brand', 'Special Sale']},
    '163': {'type': 'variants', 'variants': [{'code': 'T', 'price': 189}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}], 'desc_zh': "天然环保护脊硬棕床垫 (2寸/4寸可选)，透气抑菌，护腰护脊。", 'desc_en': "Natural Firm Spine Support Coconut Palm Mattress (2\" / 4\"), breathable and eco-friendly.", 'tags_zh': ['护脊护腰', '天然椰棕'], 'tags_en': ['Firm Support', 'Natural Coir']},
    'TH318': {'type': 'variants', 'variants': [{'code': 'F', 'price': 399}, {'code': 'Q', 'price': 459}, {'code': 'K', 'price': 599}], 'desc_zh': "五星级奢华云感乳胶独立弹簧床垫，双重减震静音，贴合人体工学。", 'desc_en': "Five-Star Luxury Latex Pocket Spring Pillow Top Mattress, ergonomic body support.", 'tags_zh': ['云感承托', '独立弹簧'], 'tags_en': ['Latex Pillow Top', 'Pocket Spring']},
    'N6001': {'type': 'variants', 'variants': [{'code': 'T', 'price': 159}, {'code': 'F', 'price': 199}, {'code': 'Q', 'price': 229}], 'tags_zh': ['精选', '高回弹'], 'tags_en': ['Featured']},
    'M6010': {'type': 'variants', 'variants': [{'code': 'T', 'price': 179}, {'code': 'F', 'price': 219}, {'code': 'Q', 'price': 249}], 'tags_zh': ['精选', '透气'], 'tags_en': ['Featured']},
    'M6100': {'type': 'variants', 'variants': [{'code': 'T', 'price': 199}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}, {'code': 'K', 'price': 359}], 'tags_zh': ['精选', '双向支撑'], 'tags_en': ['Featured']},
    'M6101': {'type': 'variants', 'variants': [{'code': 'T', 'price': 219}, {'code': 'F', 'price': 259}, {'code': 'Q', 'price': 289}, {'code': 'K', 'price': 379}], 'tags_zh': ['精选', '静音弹簧'], 'tags_en': ['Featured']},
    'M6102': {'type': 'variants', 'variants': [{'code': 'T', 'price': 239}, {'code': 'F', 'price': 279}, {'code': 'Q', 'price': 309}, {'code': 'K', 'price': 399}], 'tags_zh': ['精选', '护脊'], 'tags_en': ['Featured']},
    'M6103': {'type': 'variants', 'variants': [{'code': 'T', 'price': 249}, {'code': 'F', 'price': 289}, {'code': 'Q', 'price': 329}, {'code': 'K', 'price': 419}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6104': {'type': 'variants', 'variants': [{'code': 'T', 'price': 269}, {'code': 'F', 'price': 309}, {'code': 'Q', 'price': 349}, {'code': 'K', 'price': 439}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6105': {'type': 'variants', 'variants': [{'code': 'T', 'price': 289}, {'code': 'F', 'price': 329}, {'code': 'Q', 'price': 369}, {'code': 'K', 'price': 459}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6106': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 339}, {'code': 'Q', 'price': 379}, {'code': 'K', 'price': 469}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6011': {'type': 'variants', 'variants': [{'code': 'T', 'price': 229}, {'code': 'F', 'price': 269}, {'code': 'Q', 'price': 299}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6107': {'type': 'variants', 'variants': [{'code': 'T', 'price': 209}, {'code': 'F', 'price': 249}, {'code': 'Q', 'price': 279}, {'code': 'K', 'price': 369}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6108': {'type': 'variants', 'variants': [{'code': 'T', 'price': 259}, {'code': 'F', 'price': 299}, {'code': 'Q', 'price': 339}, {'code': 'K', 'price': 429}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6109': {'type': 'variants', 'variants': [{'code': 'T', 'price': 279}, {'code': 'F', 'price': 319}, {'code': 'Q', 'price': 359}, {'code': 'K', 'price': 449}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},
    'M6012': {'type': 'variants', 'variants': [{'code': 'T', 'price': 199}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}], 'tags_zh': ['精选'], 'tags_en': ['Featured']},

    'BZ-0396': {'type': 'single', 'price': 680, 'tags_zh': ['1+6组合', '精选'], 'tags_en': ['7-PC Set', 'Featured']},
    'BZ-2192': {'type': 'single', 'price': 780, 'tags_zh': ['1+6组合', '极简岩板'], 'tags_en': ['7-PC Set', 'Sintered Stone']},
    'BZ-0296': {'type': 'single', 'price': 720, 'tags_zh': ['1+6组合', '轻奢'], 'tags_en': ['7-PC Set', 'Luxury']},
    'TH-DT04': {'type': 'single', 'price': 860, 'tags_zh': ['奢石台面', '1+6组合'], 'tags_en': ['Luxury Stone', '7-PC Set']},
    'F3050': {'type': 'single', 'price': 1460, 'tags_zh': ['大班台', '现代商务'], 'tags_en': ['Executive Desk', 'Modern']},
    'F3051': {'type': 'single', 'price': 1460, 'tags_zh': ['大班台', '精选'], 'tags_en': ['Executive Desk', 'Featured']},
    'F3052': {'type': 'single', 'price': 1460, 'tags_zh': ['大班台', '精选'], 'tags_en': ['Executive Desk', 'Featured']},
    'D09': {'type': 'single', 'price': 1980, 'tags_zh': ['4D零重力', '智能语音', '热销'], 'tags_en': ['4D Zero Gravity', 'Smart Control', 'Popular']}
}

def clean_desc(desc_text):
    # Strip any market price, discount, or dollar text from description
    cleaned = re.sub(r'，?市场价[:：]?\s*\$[\d,]+', '', desc_text)
    cleaned = re.sub(r'，?折后[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', cleaned)
    cleaned = re.sub(r'，?折后[:：]?\s*\$[\d,]+起?', '', cleaned)
    cleaned = re.sub(r'，?55%?\s*OFF', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*MSRP[:：]?\s*\$[\d,]+', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*Sale[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*Sale[:：]?\s*\$[\d,]+', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[，,]\s*$', '', cleaned.strip())
    return cleaned.strip()

def get_pricing_and_meta(title, desc, lang='zh'):
    clean = re.sub(r'[#\s]', '', title).upper()
    for k, v in CURATED.items():
        k_clean = re.sub(r'[#\s]', '', k).upper()
        if k_clean == clean or k_clean in clean or clean in k_clean:
            return v
    for p in products_data:
        p_code = re.sub(r'[#\s]', '', p.get('code', '')).upper()
        p_id = re.sub(r'[#\s]', '', p.get('id', '')).upper()
        if p_code == clean or p_id == clean:
            return {
                'type': 'variants',
                'variants': [{'code': v['code'], 'price': v['price']} for v in p['variants']],
                'tags_zh': ['工厂直销', '精选'],
                'tags_en': ['Factory Direct', 'Featured']
            }
    if re.match(r'^F30[3-4]\d', clean):
        return {'type': 'single', 'price': 1460, 'tags_zh': ['1+6套组', '精选'], 'tags_en': ['7-PC Set', 'Featured']}
    return None

def format_price_str(pricing, lang='zh'):
    prefix = '折后' if lang == 'zh' else 'Sale'
    if not pricing:
        return ''
    if pricing.get('type') == 'variants' and len(pricing.get('variants', [])) > 1:
        parts = []
        for v in pricing['variants']:
            p_val = v['price']
            p_str = f"${int(p_val)}" if isinstance(p_val, (int, float)) and float(p_val).is_integer() else f"${p_val:.2f}"
            parts.append(f"{v['code']}: {p_str}")
        return f"{prefix} {' | '.join(parts)}"
    else:
        p_val = pricing['variants'][0]['price'] if pricing.get('type') == 'variants' else pricing.get('price', 0)
        p_str = f"${int(p_val):,}" if isinstance(p_val, (int, float)) and float(p_val).is_integer() else f"${p_val:.2f}"
        return f"{prefix} {p_str}"

pages = [
    ('zh/mattress/index.html', 'zh'),
    ('mattress/index.html', 'en'),
    ('zh/bedroom/index.html', 'zh'),
    ('bedroom/index.html', 'en'),
    ('zh/living-room/index.html', 'zh'),
    ('living-room/index.html', 'en'),
    ('zh/dining/index.html', 'zh'),
    ('dining/index.html', 'en'),
    ('zh/office/index.html', 'zh'),
    ('office/index.html', 'en'),
    ('zh/massage-chair/index.html', 'zh'),
    ('massage-chair/index.html', 'en'),
]

for filepath, lang in pages:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    cards = re.findall(r'<div class=["\']sofa-card reveal["\']>[\s\S]*?(?=<div class=["\']sofa-card reveal["\']>|</div>\s*</main>|$)', html)
    
    new_html = html
    for card_str in cards:
        # Extract main img
        img_match = re.search(r'<div class=["\']sofa-img-container["\']>([\s\S]*?)</div>', card_str)
        if not img_match: continue
        raw_img = re.search(r'<img[^>]+>', img_match.group(1))
        if not raw_img: continue
        img_tag = raw_img.group(0)

        # Extract thumbnails
        thumbs_match = re.search(r'<div class=["\']sofa-thumbnails["\']>([\s\S]*?)</div>', card_str)
        thumbs_html = f'\n            <div class="sofa-thumbnails">{thumbs_match.group(1)}</div>' if thumbs_match else ''

        # Extract h3, p
        h3_match = re.search(r'<h3>(.*?)</h3>', card_str)
        p_match = re.search(r'<p>(.*?)</p>', card_str)
        if not h3_match or not p_match: continue
        h3_text = h3_match.group(1)
        p_text = p_match.group(1)

        meta = get_pricing_and_meta(h3_text, p_text, lang)
        
        # Determine cleaned description
        if meta and ('desc_zh' in meta or 'desc_en' in meta):
            clean_description = meta.get('desc_zh' if lang == 'zh' else 'desc_en', clean_desc(p_text))
        else:
            clean_description = clean_desc(p_text)

        # Determine price string
        price_text = format_price_str(meta, lang)

        # Determine tags
        tags = []
        if meta and ('tags_zh' in meta or 'tags_en' in meta):
            tags = meta.get('tags_zh' if lang == 'zh' else 'tags_en', [])
        else:
            existing_tags = re.findall(r'<span class=["\']detail-tag["\']>(.*?)</span>', card_str)
            for t in existing_tags:
                t = t.strip()
                if t and t not in tags and not any(w in t for w in ['折后', 'Sale', '$']):
                    tags.append(t)

        tags_str = '\n                    '.join([f'<span class="detail-tag">{t}</span>' for t in tags])
        
        if price_text:
            price_tag_html = f'<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{price_text}</span>'
        else:
            price_tag_html = ''

        details_html = f"""<div class="sofa-details">
                    {price_tag_html}
                    {tags_str}
                </div>"""

        # Build clean card
        clean_card = f"""<div class="sofa-card reveal">
            <div class="sofa-img-container">
                {img_tag}
            </div>{thumbs_html}
            <div class="sofa-info">
                <h3>{h3_text}</h3>
                <p>{clean_description}</p>
                {details_html}
            </div>
        </div>"""

        new_html = new_html.replace(card_str.strip(), clean_card)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"[OK] Cleaned & Updated: {filepath}")

print("All descriptions purified and bottom price bars perfectly structured!")
