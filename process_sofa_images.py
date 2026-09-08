import os
from PIL import Image

USER_UPLOADED = '/Users/kivinwang/.gemini/antigravity-ide/brain/04825edb-fde1-40c0-ac49-90eaed1d2c2f/.user_uploaded'
IMAGES_DIR = '/Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images'
TH_DIR = os.path.join(IMAGES_DIR, 'th')
os.makedirs(TH_DIR, exist_ok=True)

def save_rgb_jpeg(img, path, quality=95):
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    img.save(path, 'JPEG', quality=quality)

sofa_specs = [
    {
        'file': 'media_1788745336304.png',
        'code': 'TH-SF801-3', # 3-seater sofa
        'crop_ratio': (0.01, 0.12, 0.99, 0.88)
    },
    {
        'file': 'media_1788745354641.png',
        'code': 'TH-SF801-2', # 2-seater loveseat
        'crop_ratio': (0.01, 0.12, 0.99, 0.88)
    },
    {
        'file': 'media_1788745362835.png',
        'code': 'TH-SF802', # Taupe L-shape sectional
        'crop_ratio': (0, 0.20, 1.0, 0.86)
    },
    {
        'file': 'media_1788745384190.png',
        'code': 'TH-SF803', # Power reclining sectional
        'crop_ratio': (0.05, 0.20, 0.96, 0.76)
    },
    {
        'file': 'media_1788745393292.png',
        'code': 'TH-DJ6661', # DJ-6661 sectional
        'crop_ratio': (0, 0.05, 1.0, 0.96)
    },
    {
        'file': 'media_1788745414059.png',
        'code': 'TH-SF805', # Curved reclining sectional
        'crop_ratio': (0, 0.15, 1.0, 0.85)
    }
]

for item in sofa_specs:
    src_path = os.path.join(USER_UPLOADED, item['file'])
    img = Image.open(src_path)
    w, h = img.size
    r = item['crop_ratio']
    crop_img = img.crop((int(w * r[0]), int(h * r[1]), int(w * r[2]), int(h * r[3])))
    out_path = os.path.join(TH_DIR, f"{item['code']}-main.jpg")
    save_rgb_jpeg(crop_img, out_path)
    print(f"Saved {out_path}")

print("--- Living room sofa images processed successfully! ---")
