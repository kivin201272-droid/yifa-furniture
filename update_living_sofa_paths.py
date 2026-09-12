import re

files = ['zh/living-room/index.html', 'living-room/index.html']

sofa_map = {
    '9701BR': 'pj_living/pj-9701br.jpg',
    '2406': 'pj_living/pj-2406.jpg',
    '2402': 'pj_living/pj-2402.jpg',
    '9211': 'pj_living/pj-9211.jpg',
    '9910': 'pj_living/pj-9910.jpg',
    '9900': 'pj_living/pj-9900.jpg',
    '9921': 'pj_living/pj-9921.jpg',
    '9931': 'pj_living/pj-9931.jpg',
    '9941': 'pj_living/pj-9941.jpg'
}

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    for k, img in sofa_map.items():
        prefix = '../../assets/images/' if 'zh/' in f else '../assets/images/'
        
        def update_card(match):
            card = match.group(0)
            if k in card:
                card = re.sub(r'<img[^>]+src=[\"\'][^\"\']*p6_img_10_204[^\"\']*[\"\']', f'<img src="{prefix}{img}"', card)
            return card
        
        parts = re.split(r'(<div\s+class=[\"\']sofa-card[^\"\']*[\"\'][\s\S]*?</div>\s*</div>)', content)
        content = ''.join([update_card(re.match(r'.*', p)) if '<div class="sofa-card' in p or "<div class='sofa-card" in p else p for p in parts])
        
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(content)

print('Updated living room sofa image paths to dedicated HD files.')
