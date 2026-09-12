import re, os

pages = [
    ('zh/bedroom/index.html', 'bedroom/index.html', 'Bedroom'),
    ('zh/living-room/index.html', 'living-room/index.html', 'Living Room'),
    ('zh/dining/index.html', 'dining/index.html', 'Dining'),
    ('zh/office/index.html', 'office/index.html', 'Office'),
    ('zh/mattress/index.html', 'mattress/index.html', 'Mattress'),
]

def parse(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    cards = []
    parts = re.split(r'<div\s+class=[\"\']sofa-card[^\"\']*[\"\']', html)
    for p in parts[1:]:
        tm = re.search(r'<h3>(.*?)</h3>', p, re.DOTALL)
        title = tm.group(1).strip() if tm else ''
        
        im = re.search(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', p)
        img = im.group(1).strip() if im else ''
        
        pm = re.search(r'<span class=[\"\']price-current[\"\']>([^<]+)</span>', p)
        price = pm.group(1).strip() if pm else ''
        
        dm = re.search(r'<p>(.*?)</p>', p, re.DOTALL)
        desc = dm.group(1).strip() if dm else ''
        
        tags = re.findall(r'<span class=[\"\']spec-tag[^>]*>([^<]+)</span>', p)
        
        cards.append({
            'title': title,
            'img': img,
            'price': price,
            'desc': desc,
            'tags': tags
        })
    return cards

total_issues = 0

for zh_path, en_path, cat in pages:
    zh_cards = parse(zh_path)
    en_cards = parse(en_path)
    
    print(f"\n==========================================")
    print(f" CATEGORY: {cat} (ZH: {len(zh_cards)}, EN: {len(en_cards)})")
    print(f"==========================================")
    
    if len(zh_cards) != len(en_cards):
        print(f"  [ERROR] Card count mismatch between ZH ({len(zh_cards)}) and EN ({len(en_cards)})!")
        total_issues += 1
    
    for i in range(min(len(zh_cards), len(en_cards))):
        zc = zh_cards[i]
        ec = en_cards[i]
        
        # Check price sync
        # extract numeric prices from zc and ec to compare
        z_nums = re.findall(r'\$\s*[\d,.]+', zc['price'])
        e_nums = re.findall(r'\$\s*[\d,.]+', ec['price'])
        
        if z_nums != e_nums and (zc['price'] or ec['price']):
            print(f"  [PRICE MISMATCH] Card #{i+1} [{zc['title']}]:")
            print(f"     ZH Price: '{zc['price']}' -> numbers: {z_nums}")
            print(f"     EN Price: '{ec['price']}' -> numbers: {e_nums}")
            total_issues += 1
            
        # Check image sync
        z_img_clean = zc['img'].split('?')[0].replace('../../', '').replace('../', '')
        e_img_clean = ec['img'].split('?')[0].replace('../../', '').replace('../', '')
        if z_img_clean != e_img_clean:
            print(f"  [IMG MISMATCH] Card #{i+1}: ZH '{zc['img']}' vs EN '{ec['img']}'")
            total_issues += 1

print(f"\nAudit finished with {total_issues} issues found.")
