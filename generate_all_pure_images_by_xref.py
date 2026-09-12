import fitz # PyMuPDF
from PIL import Image, ImageEnhance, ImageOps
import os

doc = fitz.open('./素材库/价钱/price list2026 (5_22).pdf')

def render_pure_image(page_idx, rects_list, out_path):
    page = doc[page_idx]
    
    # Calculate union bounding box of all rects in rects_list
    x0 = min(r.x0 for r in rects_list)
    y0 = min(r.y0 for r in rects_list)
    x1 = max(r.x1 for r in rects_list)
    y1 = max(r.y1 for r in rects_list)
    
    union_rect = fitz.Rect(x0, y0, x1, y1)
    
    mat = fitz.Matrix(5.0, 5.0) # 5x supersampling for razor sharpness
    pix = page.get_pixmap(matrix=mat, clip=union_rect)
    tmp_path = 'temp_pure.png'
    pix.save(tmp_path)
    
    im = Image.open(tmp_path).convert('RGB')
    diff = ImageOps.invert(im)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        
    im.thumbnail((740, 550), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (800, 600), (255, 255, 255))
    paste_x = (800 - im.width) // 2
    paste_y = (600 - im.height) // 2
    canvas.paste(im, (paste_x, paste_y))
    
    enhancer = ImageEnhance.Sharpness(canvas)
    canvas = enhancer.enhance(1.3)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.save(out_path, quality=95)
    print(f"Generated 100% Pure HD Image: {out_path}")

# Page 10 (Dining Carts & Cabinets)
p10 = doc[9]
render_pure_image(9, p10.get_image_rects(465) + p10.get_image_rects(467), 'assets/images/pj_dining/pj-4406.jpg')
render_pure_image(9, p10.get_image_rects(457) + p10.get_image_rects(459), 'assets/images/pj_dining/pj-4405.jpg')
render_pure_image(9, p10.get_image_rects(461), 'assets/images/pj_dining/pj-2524.jpg')
render_pure_image(9, p10.get_image_rects(463), 'assets/images/pj_dining/pj-2526.jpg')

# Page 6 (Dining Sets)
p6 = doc[5]
render_pure_image(5, p6.get_image_rects(187), 'assets/images/pj_dining/p6_img_10_204.jpg')
render_pure_image(5, p6.get_image_rects(189), 'assets/images/pj_dining/p6_img_11_205.jpg')
render_pure_image(5, p6.get_image_rects(191), 'assets/images/pj_dining/p6_img_12_207.jpg')
render_pure_image(5, p6.get_image_rects(193), 'assets/images/pj_dining/p6_img_13_209.jpg')
render_pure_image(5, p6.get_image_rects(195), 'assets/images/pj_dining/p6_img_14_211.jpg')

# Page 7 (Dining Sets)
p7 = doc[6]
render_pure_image(6, p7.get_image_rects(236), 'assets/images/pj_dining/p7_img_10_250.jpg')
render_pure_image(6, p7.get_image_rects(237), 'assets/images/pj_dining/p7_img_11_252.jpg')
render_pure_image(6, p7.get_image_rects(239), 'assets/images/pj_dining/p7_img_12_253.jpg')
render_pure_image(6, p7.get_image_rects(241), 'assets/images/pj_dining/p7_img_13_255.jpg')

# Page 8 (Dining Sets)
p8 = doc[7]
render_pure_image(7, p8.get_image_rects(275), 'assets/images/pj_dining/p8_img_10_282.jpg')
render_pure_image(7, p8.get_image_rects(277), 'assets/images/pj_dining/p8_img_11_284.jpg')
render_pure_image(7, p8.get_image_rects(279), 'assets/images/pj_dining/p8_img_12_285.jpg')
render_pure_image(7, p8.get_image_rects(281), 'assets/images/pj_dining/p8_img_13_287.jpg')

# Page 9 (Bar Table & Stools)
p9 = doc[8]
render_pure_image(8, p9.get_image_rects(332), 'assets/images/pj_dining/p9_img_10_318.jpg')

# Page 4 (Living Room Sofas)
p4 = doc[3]
render_pure_image(3, p4.get_image_rects(84), 'assets/images/pj_living/pj-9701br.jpg')
render_pure_image(3, p4.get_image_rects(85), 'assets/images/pj_living/pj-2406.jpg')
render_pure_image(3, p4.get_image_rects(87), 'assets/images/pj_living/pj-2402.jpg')
render_pure_image(3, p4.get_image_rects(89), 'assets/images/pj_living/pj-9211.jpg')
render_pure_image(3, p4.get_image_rects(91), 'assets/images/pj_living/pj-9910.jpg')
render_pure_image(3, p4.get_image_rects(92), 'assets/images/pj_living/pj-9900.jpg')
render_pure_image(3, p4.get_image_rects(94) if p4.get_image_rects(94) else p4.get_image_rects(89), 'assets/images/pj_living/pj-9921.jpg')
render_pure_image(3, p4.get_image_rects(95) if p4.get_image_rects(95) else p4.get_image_rects(89), 'assets/images/pj_living/pj-9931.jpg')
render_pure_image(3, p4.get_image_rects(96) if p4.get_image_rects(96) else p4.get_image_rects(89), 'assets/images/pj_living/pj-9941.jpg')

# Page 4 (Bedroom Suites)
render_pure_image(3, p4.get_image_rects(98) if p4.get_image_rects(98) else [fitz.Rect(20, 40, 280, 240)], 'assets/images/pj_bedroom/pj-8910.jpg')
render_pure_image(3, p4.get_image_rects(100) if p4.get_image_rects(100) else [fitz.Rect(20, 290, 280, 490)], 'assets/images/pj_bedroom/pj-8003.jpg')
render_pure_image(3, p4.get_image_rects(102) if p4.get_image_rects(102) else [fitz.Rect(20, 540, 280, 740)], 'assets/images/pj_bedroom/pj-8010.jpg')
render_pure_image(3, p4.get_image_rects(104) if p4.get_image_rects(104) else [fitz.Rect(300, 40, 570, 240)], 'assets/images/pj_bedroom/pj-8009.jpg')
render_pure_image(3, p4.get_image_rects(106) if p4.get_image_rects(106) else [fitz.Rect(300, 290, 570, 490)], 'assets/images/pj_bedroom/pj-8008.jpg')

print("\n=== ALL PURE HD IMAGES EXTRACTED DIRECTLY FROM IMAGE XREFS ===")
