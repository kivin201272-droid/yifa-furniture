import re, os, json

# 1. Exact Whitelist from user specification
PJ_WHITELIST = {
    # T / F / Q Beds
    '7602-GRAY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 129}, {'code': 'F', 'price': 149}, {'code': 'Q', 'price': 159}]},
    '7602Q-GRAY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 129}, {'code': 'F', 'price': 149}, {'code': 'Q', 'price': 159}]},
    '7602-IVY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 129}, {'code': 'F', 'price': 149}, {'code': 'Q', 'price': 159}]},
    '7602Q-IVY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 129}, {'code': 'F', 'price': 149}, {'code': 'Q', 'price': 159}]},
    '7602-PINK': {'type': 'variants', 'variants': [{'code': 'T', 'price': 129}, {'code': 'F', 'price': 149}, {'code': 'Q', 'price': 159}]},
    '7011GRAY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 119}, {'code': 'F', 'price': 139}, {'code': 'Q', 'price': 149}]},
    '7011-GRAY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 119}, {'code': 'F', 'price': 139}, {'code': 'Q', 'price': 149}]},
    '7011CHAR': {'type': 'variants', 'variants': [{'code': 'T', 'price': 119}, {'code': 'F', 'price': 139}, {'code': 'Q', 'price': 149}]},
    '7011-CHAR': {'type': 'variants', 'variants': [{'code': 'T', 'price': 119}, {'code': 'F', 'price': 139}, {'code': 'Q', 'price': 149}]},
    '7100': {'type': 'variants', 'variants': [{'code': 'T', 'price': 75}, {'code': 'F', 'price': 85}, {'code': 'Q', 'price': 95}]},
    '7100-GRAY': {'type': 'variants', 'variants': [{'code': 'T', 'price': 75}, {'code': 'F', 'price': 85}, {'code': 'Q', 'price': 95}]},
    '7013': {'type': 'variants', 'variants': [{'code': 'T', 'price': 99}, {'code': 'F', 'price': 119}, {'code': 'Q', 'price': 129}]},
    '1901': {'type': 'variants', 'variants': [{'code': 'T', 'price': 59}, {'code': 'F', 'price': 79}, {'code': 'Q', 'price': 89}]},
    '7202': {'type': 'variants', 'variants': [{'code': 'T', 'price': 99}, {'code': 'F', 'price': 119}, {'code': 'Q', 'price': 129}]},
    '7203': {'type': 'variants', 'variants': [{'code': 'T', 'price': 99}, {'code': 'F', 'price': 119}, {'code': 'Q', 'price': 129}]},
    '7009': {'type': 'variants', 'variants': [{'code': 'T', 'price': 79}, {'code': 'F', 'price': 99}, {'code': 'Q', 'price': 109}]},
    '7001': {'type': 'variants', 'variants': [{'code': 'T', 'price': 95}, {'code': 'F', 'price': 119}, {'code': 'Q', 'price': 129}]},
    '7002': {'type': 'variants', 'variants': [{'code': 'T', 'price': 79}, {'code': 'F', 'price': 99}, {'code': 'Q', 'price': 109}]},

    # F / Q Beds
    '7603': {'type': 'variants', 'variants': [{'code': 'F', 'price': 179}, {'code': 'Q', 'price': 199}]},
    '7405WH': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7405-WH': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7500-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7500F/Q-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7403GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7403-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7404BK': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7404-BK': {'type': 'variants', 'variants': [{'code': 'F', 'price': 299}, {'code': 'Q', 'price': 299}]},
    '7102 BROWN': {'type': 'variants', 'variants': [{'code': 'F', 'price': 109}, {'code': 'Q', 'price': 119}]},
    '7102-BROWN': {'type': 'variants', 'variants': [{'code': 'F', 'price': 109}, {'code': 'Q', 'price': 119}]},
    '7102 GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 109}, {'code': 'Q', 'price': 119}]},
    '7102-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 109}, {'code': 'Q', 'price': 119}]},
    '7806-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 199}, {'code': 'Q', 'price': 229}]},
    '7804 GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 249}, {'code': 'Q', 'price': 269}]},
    '7804-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 249}, {'code': 'Q', 'price': 269}]},
    '7020WH': {'type': 'variants', 'variants': [{'code': 'F', 'price': 199}, {'code': 'Q', 'price': 219}]},
    '7021BK': {'type': 'variants', 'variants': [{'code': 'F', 'price': 199}, {'code': 'Q', 'price': 219}]},
    '7016-GRAY': {'type': 'variants', 'variants': [{'code': 'F', 'price': 99}, {'code': 'Q', 'price': 109}]},

    # T / F Beds
    '7901CA-T/F': {'type': 'variants', 'variants': [{'code': 'T', 'price': 109}, {'code': 'F', 'price': 129}]},
    '7901WH-T/F': {'type': 'variants', 'variants': [{'code': 'T', 'price': 109}, {'code': 'F', 'price': 129}]},
    '7003T-BK/F-BK': {'type': 'variants', 'variants': [{'code': 'T', 'price': 69}, {'code': 'F', 'price': 89}]},
    '7003T-WH/F-WH': {'type': 'variants', 'variants': [{'code': 'T', 'price': 69}, {'code': 'F', 'price': 89}]},

    # Single Specs
    '7600Q-IVY': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 300}]},
    '7401Q-BK': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 499}]},
    '7402Q-WH': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 499}]},
    '2331': {'type': 'single', 'price': 119},
    '7701CA': {'type': 'single', 'price': 219},
    '7701WH': {'type': 'single', 'price': 219},
    '7702CA': {'type': 'single', 'price': 279},
    '7702WH': {'type': 'single', 'price': 279},
    '7005BK': {'type': 'single', 'price': 149},
    '7004BK': {'type': 'single', 'price': 169},

    # 2. Existing Original Products with Prices
    'BEAUTYREST BLACK': {
        'type': 'single', 
        'price': 1380, 
        'desc_zh': "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress 美国席梦思床垫，美国制造，质保 20 年。King size(78''x80'')", 
        'desc_en': "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress Made in USA, 20-Year Warranty. King size (78\"x80\")", 
        'tags_zh': ['55% OFF', '质保20年', '美国制造'], 
        'tags_en': ['55% OFF', '20-Yr Warranty', 'Made in USA']
    },
    'LUXURY DEEP SLEEP': {
        'type': 'variants', 
        'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 499}, {'code': 'Q', 'price': 599}, {'code': 'K', 'price': 888}], 
        'desc_zh': "美国 Sealy 品牌记忆棉床垫 CHINO 388-9'' (39''x75'') 丝涟品牌床垫，独立袋装弹簧，高透气记忆棉支撑。", 
        'desc_en': "USA Sealy Memory Foam Mattress CHINO 388-9\" (39\"x75\"), pocketed coil system with breathable memory foam support.", 
        'tags_zh': ['55% OFF', 'SEALY 品牌', '特惠'], 
        'tags_en': ['55% OFF', 'Sealy Brand', 'Special Sale']
    }
}

def clean_description_text(desc_text):
    """Purifies description of any price/discount mentions"""
    cleaned = re.sub(r'，?市场价[:：]?\s*\$[\d,]+', '', desc_text)
    cleaned = re.sub(r'，?折后[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', cleaned)
    cleaned = re.sub(r'，?折后[:：]?\s*\$[\d,]+起?', '', cleaned)
    cleaned = re.sub(r'，?55%?\s*OFF', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*MSRP[:：]?\s*\$[\d,]+', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*Sale[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', cleaned, flags=re.I)
    cleaned = re.sub(r',?\s*Sale[:：]?\s*\$[\d,]+', '', cleaned, flags=re.I)
    cleaned = re.sub(r'[，,]\s*$', '', cleaned.strip())
    return cleaned.strip()

def match_product(title, category=''):
    clean_t = re.sub(r'[#\s]', '', title).upper()
    # Normalize common prefix/suffix
    for k, v in PJ_WHITELIST.items():
        clean_k = re.sub(r'[#\s]', '', k).upper()
        if clean_k == clean_t:
            return v
        # Specific model code matching
        if clean_t.startswith(clean_k) or clean_t == clean_k.replace('-', ''):
            if len(clean_k) >= 4 and clean_t[:len(clean_k)] == clean_k:
                return v
    return None

def format_price_line(pricing, lang='zh'):
    prefix = '折后' if lang == 'zh' else 'Sale'
    if not pricing:
        return ''
    if pricing.get('type') == 'variants':
        vars_list = pricing.get('variants', [])
        if len(vars_list) > 1:
            parts = [f"{v['code']}: ${int(v['price'])}" for v in vars_list]
            return f"{prefix} {' | '.join(parts)}"
        elif len(vars_list) == 1:
            return f"{prefix} {vars_list[0]['code']}: ${int(vars_list[0]['price'])}"
    elif pricing.get('type') == 'single':
        return f"{prefix} ${int(pricing.get('price', 0)):,}"
    return ''

pages = [
    ('zh/mattress/index.html', 'zh', 'Mattress'),
    ('mattress/index.html', 'en', 'Mattress'),
    ('zh/bedroom/index.html', 'zh', 'Bedroom'),
    ('bedroom/index.html', 'en', 'Bedroom'),
    ('zh/living-room/index.html', 'zh', 'Living Room'),
    ('living-room/index.html', 'en', 'Living Room'),
    ('zh/dining/index.html', 'zh', 'Dining'),
    ('dining/index.html', 'en', 'Dining'),
    ('zh/office/index.html', 'zh', 'Office'),
    ('office/index.html', 'en', 'Office'),
    ('zh/massage-chair/index.html', 'zh', 'Massage Chair'),
    ('massage-chair/index.html', 'en', 'Massage Chair'),
]

for filepath, lang, cat in pages:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    cards = re.findall(r'<div class=["\']sofa-card reveal["\']>[\s\S]*?(?=<div class=["\']sofa-card reveal["\']>|</div>\s*</main>|$)', html)
    
    new_html = html
    prices_kept = 0
    prices_removed = 0

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

        # Only check whitelist if in Bedroom or Mattress
        match_info = None
        if cat in ['Bedroom', 'Mattress']:
            match_info = match_product(h3_text, cat)

        # Clean description
        if match_info and ('desc_zh' in match_info or 'desc_en' in match_info):
            clean_desc = match_info.get('desc_zh' if lang == 'zh' else 'desc_en')
        else:
            clean_desc = clean_description_text(p_text)

        # Tags
        tags = []
        if match_info and ('tags_zh' in match_info or 'tags_en' in match_info):
            tags = match_info.get('tags_zh' if lang == 'zh' else 'tags_en', [])
        else:
            existing_tags = re.findall(r'<span class=["\']detail-tag["\']>(.*?)</span>', card_str)
            for t in existing_tags:
                t = t.strip()
                if t and t not in tags and not any(w in t for w in ['折后', 'Sale', '$']):
                    tags.append(t)

        tags_str = '\n                    '.join([f'<span class="detail-tag">{t}</span>' for t in tags])

        # Price Line: ONLY for Whitelist / Original products
        price_text = format_price_line(match_info, lang) if match_info else ''
        
        if price_text:
            prices_kept += 1
            price_tag_html = f'<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{price_text}</span>'
        else:
            prices_removed += 1
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
                <p>{clean_desc}</p>
                {details_html}
            </div>
        </div>"""

        new_html = new_html.replace(card_str.strip(), clean_card)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"[OK] {filepath}: Kept {prices_kept} whitelisted/original prices, cleaned {prices_removed} items.")

print("\n🎉 Strict whitelist applied successfully across all category pages!")
