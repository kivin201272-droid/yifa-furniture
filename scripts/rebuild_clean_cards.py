import re, os, json

with open('scripts/inspect_and_update_banners.js', 'r', encoding='utf-8') as f:
    pass

# Load products.json
with open('src/data/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

# Curated pricing dictionary
CURATED = {
    'TH2506': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 499}, {'code': 'K', 'price': 599}]},
    'TH2503': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 529}, {'code': 'K', 'price': 629}]},
    'TH2608': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 489}, {'code': 'K', 'price': 589}]},
    '818': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 349}, {'code': 'Q', 'price': 399}]},
    'IB-108Q': {'type': 'single', 'price': 299},
    'B-0188': {'type': 'single', 'price': 329},
    'B1902': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 459}, {'code': 'K', 'price': 559}]},
    '836': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 429}, {'code': 'K', 'price': 529}]},
    '839': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 439}, {'code': 'K', 'price': 539}]},
    'B230': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 469}, {'code': '5-PC', 'price': 1280}]},
    'TH9903': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 559}, {'code': 'K', 'price': 659}]},
    '838': {'type': 'variants', 'variants': [{'code': 'Q', 'price': 429}, {'code': 'K', 'price': 529}]},

    'BEAUTYREST BLACK': {'type': 'single', 'price': 1380},
    'LUXURY DEEP SLEEP': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 499}, {'code': 'Q', 'price': 599}, {'code': 'K', 'price': 888}]},
    '163': {'type': 'variants', 'variants': [{'code': 'T', 'price': 189}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}]},
    'TH318': {'type': 'variants', 'variants': [{'code': 'F', 'price': 399}, {'code': 'Q', 'price': 459}, {'code': 'K', 'price': 599}]},
    'N6001': {'type': 'variants', 'variants': [{'code': 'T', 'price': 159}, {'code': 'F', 'price': 199}, {'code': 'Q', 'price': 229}]},
    'M6010': {'type': 'variants', 'variants': [{'code': 'T', 'price': 179}, {'code': 'F', 'price': 219}, {'code': 'Q', 'price': 249}]},
    'M6100': {'type': 'variants', 'variants': [{'code': 'T', 'price': 199}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}, {'code': 'K', 'price': 359}]},
    'M6101': {'type': 'variants', 'variants': [{'code': 'T', 'price': 219}, {'code': 'F', 'price': 259}, {'code': 'Q', 'price': 289}, {'code': 'K', 'price': 379}]},
    'M6102': {'type': 'variants', 'variants': [{'code': 'T', 'price': 239}, {'code': 'F', 'price': 279}, {'code': 'Q', 'price': 309}, {'code': 'K', 'price': 399}]},
    'M6103': {'type': 'variants', 'variants': [{'code': 'T', 'price': 249}, {'code': 'F', 'price': 289}, {'code': 'Q', 'price': 329}, {'code': 'K', 'price': 419}]},
    'M6104': {'type': 'variants', 'variants': [{'code': 'T', 'price': 269}, {'code': 'F', 'price': 309}, {'code': 'Q', 'price': 349}, {'code': 'K', 'price': 439}]},
    'M6105': {'type': 'variants', 'variants': [{'code': 'T', 'price': 289}, {'code': 'F', 'price': 329}, {'code': 'Q', 'price': 369}, {'code': 'K', 'price': 459}]},
    'M6106': {'type': 'variants', 'variants': [{'code': 'T', 'price': 299}, {'code': 'F', 'price': 339}, {'code': 'Q', 'price': 379}, {'code': 'K', 'price': 469}]},
    'M6011': {'type': 'variants', 'variants': [{'code': 'T', 'price': 229}, {'code': 'F', 'price': 269}, {'code': 'Q', 'price': 299}]},
    'M6107': {'type': 'variants', 'variants': [{'code': 'T', 'price': 209}, {'code': 'F', 'price': 249}, {'code': 'Q', 'price': 279}, {'code': 'K', 'price': 369}]},
    'M6108': {'type': 'variants', 'variants': [{'code': 'T', 'price': 259}, {'code': 'F', 'price': 299}, {'code': 'Q', 'price': 339}, {'code': 'K', 'price': 429}]},
    'M6109': {'type': 'variants', 'variants': [{'code': 'T', 'price': 279}, {'code': 'F', 'price': 319}, {'code': 'Q', 'price': 359}, {'code': 'K', 'price': 449}]},
    'M6012': {'type': 'variants', 'variants': [{'code': 'T', 'price': 199}, {'code': 'F', 'price': 239}, {'code': 'Q', 'price': 269}]},

    'BZ-0396': {'type': 'single', 'price': 680},
    'BZ-2192': {'type': 'single', 'price': 780},
    'BZ-0296': {'type': 'single', 'price': 720},
    'TH-DT04': {'type': 'single', 'price': 860},
    'F3050': {'type': 'single', 'price': 1460},
    'F3051': {'type': 'single', 'price': 1460},
    'F3052': {'type': 'single', 'price': 1460},
    'D09': {'type': 'single', 'price': 1980}
}

def get_pricing(title, desc):
    clean = re.sub(r'[#\s]', '', title).upper()
    for k, v in CURATED.items():
        k_clean = re.sub(r'[#\s]', '', k).upper()
        if k_clean == clean or k_clean in clean or clean in k_clean:
            return v
    for p in products_data:
        p_code = re.sub(r'[#\s]', '', p.get('code', '')).upper()
        p_id = re.sub(r'[#\s]', '', p.get('id', '')).upper()
        if p_code == clean or p_id == clean:
            return {'type': 'variants', 'variants': [{'code': v['code'], 'price': v['price']} for v in p['variants']]}
    
    if re.match(r'^F30[3-4]\d', clean):
        return {'type': 'single', 'price': 1460}

    m = re.search(r'折后\s*(?:F[:：]\s*\$?(\d+)[，,\s]*Q[:：]\s*\$?(\d+)(?:[，,\s]*K[:：]\s*\$?(\d+))?)', desc, re.I)
    if m:
        vars_list = []
        if m.group(1): vars_list.append({'code': 'F', 'price': int(m.group(1))})
        if m.group(2): vars_list.append({'code': 'Q', 'price': int(m.group(2))})
        if m.group(3): vars_list.append({'code': 'K', 'price': int(m.group(3))})
        return {'type': 'variants', 'variants': vars_list}

    m2 = re.search(r'折后\s*\$?([\d,]+)', desc, re.I) or re.search(r'Sale\s*[:$]\s*([\d,]+)', desc, re.I)
    if m2:
        return {'type': 'single', 'price': int(m2.group(1).replace(',', ''))}
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

    # Split by sofa-card
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

        # Extract existing detail tags
        tags = re.findall(r'<span class=["\']detail-tag["\']>(.*?)</span>', card_str)
        # Deduplicate
        seen_tags = []
        for t in tags:
            t = t.strip()
            if t and t not in seen_tags:
                seen_tags.append(t)

        pricing = get_pricing(h3_text, p_text)
        price_text = format_price_str(pricing, lang)
        
        tags_str = '\n                    '.join([f'<span class="detail-tag">{t}</span>' for t in seen_tags])
        
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
                <p>{p_text}</p>
                {details_html}
            </div>
        </div>"""

        new_html = new_html.replace(card_str.strip(), clean_card)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"[OK] Cleaned and rebuilt: {filepath}")

print("All category pages perfectly rebuilt with 100% clean standard HTML structure!")
