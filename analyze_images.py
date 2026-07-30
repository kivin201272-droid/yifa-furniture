import re
import os
from PIL import Image

def is_structure_image(filepath):
    try:
        with Image.open(filepath) as im:
            # Convert to grayscale
            gray = im.convert('L')
            # Count pixels > 240 (very white)
            histogram = gray.histogram()
            white_pixels = sum(histogram[240:])
            total_pixels = im.width * im.height
            white_ratio = white_pixels / total_pixels
            return white_ratio > 0.8  # If >80% is white, probably a structure diagram
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

with open('zh/living-room/index.html', 'r') as f:
    content = f.read()

products = re.findall(r'<div class="sofa-card reveal">.*?</div>\s*</div>\s*</div>', content, re.DOTALL)

for i, product in enumerate(products):
    images = re.findall(r'src="../../assets/images/(pdf[123]/[^"]+)"', product)
    if not images:
        continue
    # Remove duplicates
    unique_images = []
    for img in images:
        if img not in unique_images:
            unique_images.append(img)
            
    if not unique_images:
        continue
        
    first_image = unique_images[0]
    filepath = os.path.join('assets/images', first_image)
    if os.path.exists(filepath):
        if is_structure_image(filepath):
            print(f"Product {i+1} has structure image FIRST: {first_image}")
            # Find the first non-structure image to use instead
            better_image = None
            for img in unique_images[1:]:
                img_path = os.path.join('assets/images', img)
                if os.path.exists(img_path) and not is_structure_image(img_path):
                    better_image = img
                    break
            print(f"  -> Better image would be: {better_image}")

