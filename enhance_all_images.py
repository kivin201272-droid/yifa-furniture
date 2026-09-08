import os
import sys
from PIL import Image, ImageFilter, ImageEnhance

TARGET_DIRS = [
    "assets/images/th",
    "assets/images/mattress",
    "assets/images/pdf1",
    "assets/images/pdf2",
    "assets/images/pdf3",
    "assets/images/pdf5",
    "assets/images/pdf6",
    "assets/images/pdf7",
    "assets/images/pdf8",
    "assets/images/pdf10",
    "assets/images/magical",
    "assets/images/massage-chair",
    "assets/images/diningroom-classified",
    "assets/images/livingroom-classified",
    "assets/images/mattress-classified",
    "assets/images/priced_collection",
    "assets/images"
]

def enhance_image(im):
    orig_mode = im.mode
    has_alpha = ("A" in orig_mode or orig_mode == "RGBA" or orig_mode == "LA")
    
    if has_alpha:
        # For RGBA, separate alpha channel to enhance RGB without artifacts
        alpha = im.getchannel("A")
        rgb = im.convert("RGB")
    else:
        if orig_mode != "RGB":
            rgb = im.convert("RGB")
        else:
            rgb = im.copy()
        alpha = None

    w, h = rgb.size
    max_dim = max(w, h)
    
    # 1. Upscale if image is smaller than 1400px (standard crisp display size)
    if max_dim < 1400:
        scale = min(2.5, 1400.0 / max_dim)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        rgb = rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
        if alpha:
            alpha = alpha.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Smart Unsharp Mask
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.8, percent=135, threshold=2))
    
    # 3. Fine-grain Sharpness enhancement
    enhancer_sharpness = ImageEnhance.Sharpness(rgb)
    rgb = enhancer_sharpness.enhance(1.22)
    
    # 4. Subtle Contrast boost to eliminate muddy gray tones
    enhancer_contrast = ImageEnhance.Contrast(rgb)
    rgb = enhancer_contrast.enhance(1.04)
    
    # 5. Recombine alpha if needed
    if alpha:
        rgb.putalpha(alpha)
        return rgb
    return rgb

def process_directory(dir_path):
    if not os.path.exists(dir_path):
        return 0
    
    count = 0
    # If dir_path is assets/images, only process direct files (not recursing into subdirs since we list them)
    is_root = (dir_path == "assets/images")
    
    items = os.listdir(dir_path)
    for f in items:
        p = os.path.join(dir_path, f)
        if os.path.isdir(p):
            continue
        
        ext = os.path.splitext(f)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".webp"):
            # Skip video poster or backups if needed, or enhance all
            if "backup" in f:
                continue
            try:
                with Image.open(p) as im:
                    enhanced = enhance_image(im)
                    
                    if ext == ".png":
                        enhanced.save(p, "PNG", optimize=True)
                    elif ext in (".jpg", ".jpeg"):
                        enhanced.save(p, "JPEG", quality=95, progressive=True)
                    elif ext == ".webp":
                        enhanced.save(p, "WEBP", quality=95)
                count += 1
            except Exception as e:
                print(f"Error processing {p}: {e}")
    return count

total = 0
for d in TARGET_DIRS:
    c = process_directory(d)
    print(f"Processed {c} images in {d}")
    total += c

print(f"\nSuccessfully enhanced {total} product and banner images to ultra-clear resolution!")
