import re, os

pages = [
    ('zh/mattress/index.html', 'zh'),
    ('mattress/index.html', 'en')
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

        # Clean description of any price text
        clean_desc = re.sub(r'，?市场价[:：]?\s*\$[\d,]+', '', p_text)
        clean_desc = re.sub(r'，?折后[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', clean_desc)
        clean_desc = re.sub(r'，?折后[:：]?\s*\$[\d,]+起?', '', clean_desc)
        clean_desc = re.sub(r'，?55%?\s*OFF', '', clean_desc, flags=re.I)
        clean_desc = re.sub(r',?\s*MSRP[:：]?\s*\$[\d,]+', '', clean_desc, flags=re.I)
        clean_desc = re.sub(r',?\s*Sale[:：]?\s*(?:[TFQKtfqk][:：]\s*\$[\d,]+[，,\s|]*)+', '', clean_desc, flags=re.I)
        clean_desc = re.sub(r',?\s*Sale[:：]?\s*\$[\d,]+', '', clean_desc, flags=re.I)
        clean_desc = re.sub(r'[，,]\s*$', '', clean_desc.strip()).strip()

        # Specific polished descriptions for Beautyrest and Sealy
        if 'BEAUTYREST' in h3_text.upper():
            if lang == 'zh':
                clean_desc = "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress 美国席梦思床垫，美国制造，质保 20 年。King size(78''x80'')"
                tags = ['55% OFF', '质保20年', '美国制造']
            else:
                clean_desc = "288-Beautyrest -Black Series II-14''2 Pillow Top Mattress Made in USA, 20-Year Warranty. King size (78\"x80\")"
                tags = ['55% OFF', '20-Yr Warranty', 'Made in USA']
        elif 'LUXURY DEEP SLEEP' in h3_text.upper() or 'SEALY' in p_text.upper():
            if lang == 'zh':
                clean_desc = "美国 Sealy 品牌记忆棉床垫 CHINO 388-9'' (39''x75'') 丝涟品牌床垫，独立袋装弹簧，高透气记忆棉支撑。"
                tags = ['SEALY 品牌', '特惠']
            else:
                clean_desc = "USA Sealy Memory Foam Mattress CHINO 388-9\" (39\"x75\"), pocketed coil system with breathable memory foam support."
                tags = ['Sealy Brand', 'Special Sale']
        else:
            tags = []
            existing_tags = re.findall(r'<span class=["\']detail-tag["\']>(.*?)</span>', card_str)
            for t in existing_tags:
                t = t.strip()
                if t and t not in tags and not any(w in t for w in ['折后', 'Sale', '$', '起']):
                    tags.append(t)

        tags_str = '\n                    '.join([f'<span class="detail-tag">{t}</span>' for t in tags])

        # NO price tags at all for mattress!
        details_html = f"""<div class="sofa-details">
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
    print(f"[OK] Cleaned & Zero Prices in {filepath}")

print("Mattress pages completely cleaned of all prices and purified!")
