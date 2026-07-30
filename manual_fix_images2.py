import re

files = ['zh/living-room/index.html', 'living-room/index.html']
ids_to_fix = [
    'pdf7-set-5-main',
    'pdf7-set-8-main',
    'pdf7-set-25-main',
    'pdf7-set-26-main'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    parts = content.split('<div class="sofa-card reveal">')
    new_content = parts[0]
    
    for part in parts[1:]:
        needs_fix = False
        for pid in ids_to_fix:
            if pid in part:
                needs_fix = True
                break
                
        if needs_fix:
            thumb_match = re.search(r'<div class="sofa-thumbnails">(.*?)</div>', part, re.DOTALL)
            if thumb_match:
                thumbs_html = thumb_match.group(1)
                img_tags = re.findall(r'<img[^>]+>', thumbs_html)
                
                if len(img_tags) > 1:
                    # Move first to last
                    first_img = img_tags.pop(0)
                    img_tags.append(first_img)
                    
                    # Update main image
                    best_src = re.search(r'src="([^"]+)"', img_tags[0]).group(1)
                    main_img_match = re.search(r'<div class="sofa-img-container">\s*<img src="([^"]+)"', part)
                    if main_img_match:
                        old_main_src = main_img_match.group(1)
                        part = part.replace(f'src="{old_main_src}"', f'src="{best_src}"', 1)
                    
                    new_thumbs_html = ""
                    for i, tag in enumerate(img_tags):
                        tag = tag.replace(' active', '')
                        if i == 0:
                            tag = tag.replace('class="sofa-thumb"', 'class="sofa-thumb active"')
                        new_thumbs_html += '\n                ' + tag
                    new_thumbs_html += '\n            '
                    
                    part = part.replace(thumbs_html, new_thumbs_html)
        
        new_content += '<div class="sofa-card reveal">' + part
        
    with open(file, 'w') as f:
        f.write(new_content)

print("Manual fixes applied for GN4648 and GS2886!")
