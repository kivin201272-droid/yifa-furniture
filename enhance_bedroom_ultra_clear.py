import os
import re
from PIL import Image, ImageFilter, ImageEnhance

# 1. Get all image paths used in Bedroom
with open('zh/bedroom/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

images = re.findall(r'src="([^"]+)"', html)
bedroom_imgs = set()
for img in images:
    if 'assets/images' in img and 'logo' not in img:
        clean_path = img.split('?')[0].replace('../../', '').replace('../', '')
        bedroom_imgs.add(clean_path)

print(f"Enhancing {len(bedroom_imgs)} bedroom images...")

def ultra_enhance(im):
    orig_mode = im.mode
    if orig_mode != 'RGB':
        im = im.convert('RGB')
    
    w, h = im.size
    max_dim = max(w, h)
    
    # 1. High-resolution upscaling (minimum 1400px for main, minimum 1000px for details)
    target_dim = 1600
    if max_dim < target_dim:
        scale = target_dim / float(max_dim)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Stage 1 Sharpness (Fine Details)
    im = im.filter(ImageFilter.UnsharpMask(radius=2.0, percent=160, threshold=1))
    
    # 3. Stage 2 Sharpness (Edge Accentuation)
    enhancer_sharp = ImageEnhance.Sharpness(im)
    im = enhancer_sharp.enhance(1.35)
    
    # 4. Color & Contrast Clarity
    enhancer_contrast = ImageEnhance.Contrast(im)
    im = enhancer_contrast.enhance(1.06)
    
    enhancer_color = ImageEnhance.Color(im)
    im = enhancer_color.enhance(1.04)
    
    return im

count = 0
for img_rel in bedroom_imgs:
    if os.path.exists(img_rel):
        try:
            with Image.open(img_rel) as im:
                enhanced = ultra_enhance(im)
                enhanced.save(img_rel, 'JPEG', quality=98, progressive=True)
                count += 1
                print(f"[{count}/{len(bedroom_imgs)}] Ultra-enhanced: {img_rel} -> {enhanced.size}")
        except Exception as e:
            print(f"Error enhancing {img_rel}: {e}")
    else:
        print(f"File not found: {img_rel}")

print(f"\nSuccessfully enhanced {count} bedroom images to ultra-high clarity!")
