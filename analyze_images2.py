import re
import os
from PIL import Image
import numpy as np

def is_structure_image(filepath):
    try:
        with Image.open(filepath) as im:
            # Resize for faster processing
            im = im.resize((100, 100))
            # Convert to numpy array
            arr = np.array(im)
            
            if len(arr.shape) == 2:
                # grayscale image -> structure diagram usually
                return True
                
            # If RGB, calculate how much color it has
            # A grayscale image in RGB has R=G=B
            r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
            color_variance = np.var(r - g) + np.var(r - b) + np.var(g - b)
            
            # Count pixels > 240 (very white)
            gray = im.convert('L')
            arr_gray = np.array(gray)
            white_ratio = np.sum(arr_gray > 240) / (im.width * im.height)

            # Structure diagrams have very low color variance AND high white ratio
            if color_variance < 100 and white_ratio > 0.6:
                return True
            return False
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
            print(f"Product {i+1} has structure FIRST: {first_image}")
            better_image = None
            for img in unique_images[1:]:
                img_path = os.path.join('assets/images', img)
                if os.path.exists(img_path) and not is_structure_image(img_path):
                    better_image = img
                    break
            print(f"  -> Better image would be: {better_image}")

