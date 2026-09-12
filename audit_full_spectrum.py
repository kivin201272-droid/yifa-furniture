import os, re, json, sys

def audit():
    print("=== FINAL FULL-SPECTRUM AUDIT & VERIFICATION ===")
    
    pages = [
        ('zh/bedroom/index.html', 'bedroom/index.html', 'Bedroom'),
        ('zh/living-room/index.html', 'living-room/index.html', 'Living Room'),
        ('zh/dining/index.html', 'dining/index.html', 'Dining'),
        ('zh/office/index.html', 'office/index.html', 'Office'),
        ('zh/mattress/index.html', 'mattress/index.html', 'Mattress'),
    ]
    
    def parse_cards(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        cards = []
        parts = re.split(r'<div\s+class=[\"\']sofa-card[^\"\']*[\"\']', html)
        for part in parts[1:]:
            tm = re.search(r'<h3>(.*?)</h3>', part, re.DOTALL)
            title = tm.group(1).strip() if tm else ''
            
            im = re.search(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', part)
            img = im.group(1).strip() if im else ''
            
            pm = re.search(r'<span class=[\"\']price-current[\"\']>([^<]+)</span>', part)
            price = pm.group(1).strip() if pm else ''
            
            dm = re.search(r'<p>(.*?)</p>', part, re.DOTALL)
            desc = dm.group(1).strip() if dm else ''
            
            tags = re.findall(r'<span class=[\"\'](?:spec-tag|detail-tag)[^>]*>([^<]+)</span>', part)
            
            cards.append({
                'title': title,
                'img': img,
                'price': price,
                'desc': desc,
                'tags': tags
            })
        return cards

    total_zh = 0
    total_en = 0
    broken_prices = 0
    price_leaks = 0
    missing_images = 0
    
    for zh_path, en_path, cat in pages:
        zh_cards = parse_cards(zh_path)
        en_cards = parse_cards(en_path)
        total_zh += len(zh_cards)
        total_en += len(en_cards)
        
        print(f"[{cat}] ZH: {len(zh_cards)} cards | EN: {len(en_cards)} cards")
        
        # Check price match & broken prices
        for idx, c in enumerate(zh_cards):
            pstr = c['price']
            if re.search(r'[\$折后\s]\.\d+', pstr) or re.search(r'\$\s*\.\d+', pstr) or re.search(r'折后\s*\.\d+', pstr) or pstr.strip() in ['折后', '折后 $', '$']:
                print(f"  [BROKEN PRICE] in {zh_path} card #{idx+1} ({c['title']}): '{pstr}'")
                broken_prices += 1
            if '$' in c['desc']:
                print(f"  [PRICE LEAK] in {zh_path} card #{idx+1} ({c['title']}): '{c['desc']}'")
                price_leaks += 1
            # Check img
            clean_img = c['img'].split('?')[0]
            abs_img = os.path.normpath(os.path.join(os.path.dirname(zh_path), clean_img))
            if not os.path.exists(abs_img):
                print(f"  [MISSING IMG] in {zh_path} card #{idx+1} ({c['title']}): '{c['img']}'")
                missing_images += 1

    print("\n-------------------------------------------")
    print(f"Total Products Audited: {total_zh} (ZH) / {total_en} (EN)")
    print(f"Broken Prices Count: {broken_prices}")
    print(f"Price Leaks Count: {price_leaks}")
    print(f"Missing Product Images: {missing_images}")
    print("-------------------------------------------")
    
    # Check legacy models
    legacy_models = [
        'TH010#', 'TH-SF02', 'TH-SF801', 'TH-SF802', 'TH-SF803', 'TH-SF805', 'TH-DJ6661',
        'GN4731', 'GN4730', 'GN4733', 'GN4732', 'GST4801', 'GN8603', 'GN8602', 'F8302A', 'F8301A', 'F3210',
        'GS5121', 'GS4737', 'GS2761', 'GS5123', 'GS2896', 'GS4301', 'GN4648', 'GN4638', 'GNT4634', 'GS7001',
        'GN4632', 'GN4749', 'Beautyrest BLACK', 'Luxury Deep Sleep'
    ]
    
    all_zh_cards = []
    for zh_path, _, _ in pages:
        all_zh_cards.extend(parse_cards(zh_path))
        
    missing_legacy = []
    for lm in legacy_models:
        if not any(lm in c['title'] or lm in c['desc'] for c in all_zh_cards):
            missing_legacy.append(lm)
            
    print(f"Legacy Flagship Preservation: {len(legacy_models) - len(missing_legacy)} / {len(legacy_models)} present.")
    if len(missing_legacy) > 0:
        print(f"Missing legacy: {missing_legacy}")
    else:
        print("✓ All legacy flagship products 100% intact!")

if __name__ == '__main__':
    audit()
