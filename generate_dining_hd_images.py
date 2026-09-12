import fitz
from PIL import Image, ImageEnhance, ImageOps
import os

doc = fitz.open('./素材库/价钱/price list2026 (5_22).pdf')
os.makedirs('assets/images/pj_dining', exist_ok=True)

def crop_hd(page_idx, rect, out_path):
    page = doc[page_idx]
    r = fitz.Rect(rect)
    mat = fitz.Matrix(5.0, 5.0)
    pix = page.get_pixmap(matrix=mat, clip=r)
    tmp_path = 'temp_crop.png'
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
    canvas.save(out_path, quality=95)
    print(f"Generated HD Dining Image: {out_path}")

# Page 6 (Page index 5)
crop_hd(5, (20, 40, 280, 280), 'assets/images/pj_dining/p6_img_10_204.jpg')
crop_hd(5, (20, 290, 280, 530), 'assets/images/pj_dining/p6_img_11_205.jpg')
crop_hd(5, (20, 540, 280, 790), 'assets/images/pj_dining/p6_img_12_207.jpg')
crop_hd(5, (300, 40, 570, 280), 'assets/images/pj_dining/p6_img_13_209.jpg')
crop_hd(5, (300, 290, 570, 790), 'assets/images/pj_dining/p6_img_14_211.jpg')

# Page 7 (Page index 6)
crop_hd(6, (20, 40, 280, 280), 'assets/images/pj_dining/p7_img_10_250.jpg')
crop_hd(6, (20, 290, 280, 530), 'assets/images/pj_dining/p7_img_11_252.jpg')
crop_hd(6, (20, 540, 280, 790), 'assets/images/pj_dining/p7_img_12_253.jpg')
crop_hd(6, (300, 40, 570, 280), 'assets/images/pj_dining/p7_img_13_255.jpg')

# Page 8 (Page index 7)
crop_hd(7, (20, 40, 280, 280), 'assets/images/pj_dining/p8_img_10_282.jpg')
crop_hd(7, (20, 290, 280, 530), 'assets/images/pj_dining/p8_img_11_284.jpg')
crop_hd(7, (20, 540, 280, 790), 'assets/images/pj_dining/p8_img_12_285.jpg')
crop_hd(7, (300, 40, 570, 280), 'assets/images/pj_dining/p8_img_13_287.jpg')

# Page 9 (Page index 8)
crop_hd(8, (20, 40, 280, 280), 'assets/images/pj_dining/p9_img_10_318.jpg')

print("All dining images successfully generated in HD!")
