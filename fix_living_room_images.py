import re
import os
from PIL import Image

def get_product_score(filepath):
    try:
        with Image.open(filepath) as im:
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im = im.resize((100, 100))
            pixels = im.getdata()
            color_pixels = 0
            white_pixels = 0
            for r, g, b in pixels:
                if max(r,g,b) - min(r,g,b) > 15:
                    color_pixels += 1
                if r > 240 and g > 240 and b > 240:
                    white_pixels += 1
            
            total = len(pixels)
            white_ratio = white_pixels / total
            color_ratio = color_pixels / total
            
            # Higher score = more color, less pure white -> more likely a product photo
            return color_ratio - white_ratio
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

files = ['zh/living-room/index.html', 'living-room/index.html']
for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Find all sofa-card blocks
    # We will use regex to find the blocks, but we must be careful with nested divs.
    # A sofa-card contains sofa-img-container, sofa-thumbnails, sofa-info
    
    # We can split by <div class="sofa-card reveal">
    parts = content.split('<div class="sofa-card reveal">')
    new_content = parts[0]
    
    for part in parts[1:]:
        # Find the thumbnails block
        thumb_match = re.search(r'<div class="sofa-thumbnails">(.*?)</div>', part, re.DOTALL)
        if thumb_match:
            thumbs_html = thumb_match.group(1)
            # Find all img tags in thumbnails
            img_tags = re.findall(r'<img[^>]+>', thumbs_html)
            
            if len(img_tags) > 1:
                # We have multiple images, let's score them
                img_data = []
                for img_tag in img_tags:
                    src_match = re.search(r'src="([^"]+)"', img_tag)
                    if src_match:
                        src = src_match.group(1)
                        # src is like ../../assets/images/pdf1/img-000.jpg
                        filepath = src.replace('../../', '').replace('../', '')
                        if not filepath.startswith('assets'):
                            filepath = 'assets/images/' + filepath.split('/')[-1] # Fallback
                        
                        score = get_product_score(filepath)
                        img_data.append({'tag': img_tag, 'src': src, 'score': score})
                    else:
                        img_data.append({'tag': img_tag, 'src': '', 'score': -999})
                
                # Sort images by score descending
                img_data.sort(key=lambda x: x['score'], reverse=True)
                
                # Update main image
                best_src = img_data[0]['src']
                # The main image is before the thumbnails
                main_img_match = re.search(r'<div class="sofa-img-container">\s*<img src="([^"]+)"', part)
                if main_img_match:
                    old_main_src = main_img_match.group(1)
                    # Replace the src in the main image container
                    part = part.replace(f'src="{old_main_src}"', f'src="{best_src}"', 1)
                
                # Rebuild thumbnails html
                new_thumbs_html = ""
                for i, data in enumerate(img_data):
                    tag = data['tag']
                    # Ensure only the first one has the 'active' class
                    tag = tag.replace(' active', '')
                    if i == 0:
                        tag = tag.replace('class="sofa-thumb"', 'class="sofa-thumb active"')
                    new_thumbs_html += '\n                ' + tag
                new_thumbs_html += '\n            '
                
                # Replace thumbnails in part
                part = part.replace(thumbs_html, new_thumbs_html)
                
        new_content += '<div class="sofa-card reveal">' + part
        
    with open(file, 'w') as f:
        f.write(new_content)

print('Done fixing images in living room pages')
