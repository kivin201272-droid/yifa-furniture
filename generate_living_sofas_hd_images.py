import fitz
from PIL import Image, ImageEnhance, ImageOps
import os

doc = fitz.open('./素材库/价钱/price list2026 (5_22).pdf')
os.makedirs('assets/images/pj_living', exist_ok=True)

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
    print(f"Generated HD Living Image: {out_path}")

# Page 4 (Page index 3): Living Room Sofas & Sofa Beds
# 9701BR (p.4, x: 600..870, y: 40..170)
crop_hd(3, (600, 40, 870, 170), 'assets/images/pj_living/pj-9701br.jpg')
# 2406 (p.4, x: 600..870, y: 175..295)
crop_hd(3, (600, 175, 870, 295), 'assets/images/pj_living/pj-2406.jpg')
# 2402 (p.4, x: 600..870, y: 300..420)
crop_hd(3, (600, 300, 870, 420), 'assets/images/pj_living/pj-2402.jpg')
# 9211/9212/9213 (p.4, x: 600..870, y: 425..545)
crop_hd(3, (600, 425, 870, 545), 'assets/images/pj_living/pj-9211.jpg')
# 9910GRAY (p.4, x: 600..870, y: 550..670)
crop_hd(3, (600, 550, 870, 670), 'assets/images/pj_living/pj-9910.jpg')
# 9900BK (p.4, x: 600..870, y: 680..795)
crop_hd(3, (600, 680, 870, 795), 'assets/images/pj_living/pj-9900.jpg')
# 9921/9922/9923 (p.4, x: 900..1060, y: 40..280)
crop_hd(3, (900, 40, 1060, 280), 'assets/images/pj_living/pj-9921.jpg')
# 9931/9932/9933 (p.4, x: 900..1060, y: 290..530)
crop_hd(3, (900, 290, 1060, 530), 'assets/images/pj_living/pj-9931.jpg')
# 9941/9942/9943 (p.4, x: 900..1060, y: 540..790)
crop_hd(3, (900, 540, 1060, 790), 'assets/images/pj_living/pj-9941.jpg')

print("All living sofa images successfully generated in HD!")
