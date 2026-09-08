import os
import shutil
from PIL import Image

USER_UPLOADED = '/Users/kivinwang/.gemini/antigravity-ide/brain/04825edb-fde1-40c0-ac49-90eaed1d2c2f/.user_uploaded'
IMAGES_DIR = '/Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images'
os.makedirs(os.path.join(IMAGES_DIR, 'th'), exist_ok=True)
os.makedirs(os.path.join(IMAGES_DIR, 'mattress'), exist_ok=True)

def save_rgb_jpeg(img, path, quality=95):
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    img.save(path, 'JPEG', quality=quality)

# 1. Restore Collection Banners
print("--- 1. Restoring Collection Banners ---")
shutil.copy2(os.path.join(IMAGES_DIR, 'collection-living-room-backup.jpg'), os.path.join(IMAGES_DIR, 'collection-living-room.jpg'))
shutil.copy2(os.path.join(IMAGES_DIR, 'collection-dining-backup.jpg'), os.path.join(IMAGES_DIR, 'collection-dining.jpg'))
print("Restored collection-living-room.jpg and collection-dining.jpg from backups.")

# 2. Beautyrest BLACK detail image
print("--- 2. Processing Beautyrest BLACK ---")
img_bb = Image.open(os.path.join(USER_UPLOADED, 'media_1788744272755.jpg'))
w, h = img_bb.size
crop_bb = img_bb.crop((0, 0, w, int(h * 0.77)))
save_rgb_jpeg(crop_bb, os.path.join(IMAGES_DIR, 'mattress', 'beautyrest-black-detail.jpg'))
print("Saved assets/images/mattress/beautyrest-black-detail.jpg")

# 3. TH Mattresses
print("--- 3. Processing TH Mattresses ---")
# 163# Coir Mattress
img_163 = Image.open(os.path.join(USER_UPLOADED, 'media_1788745008606.png'))
w, h = img_163.size
crop_163 = img_163.crop((0, int(h * 0.10), w, int(h * 0.84)))
save_rgb_jpeg(crop_163, os.path.join(IMAGES_DIR, 'mattress', 'TH-163.jpg'))
print("Saved assets/images/mattress/TH-163.jpg")

# TH318# Mattress
img_318 = Image.open(os.path.join(USER_UPLOADED, 'media_1788745018441.png'))
w, h = img_318.size
crop_318 = img_318.crop((0, int(h * 0.08), w, int(h * 0.84)))
save_rgb_jpeg(crop_318, os.path.join(IMAGES_DIR, 'mattress', 'TH-318.jpg'))
print("Saved assets/images/mattress/TH-318.jpg")

# 4. TH Living Room Sofa Bed
print("--- 4. Processing TH Living Room Sofa Bed ---")
img_sofabed = Image.open(os.path.join(USER_UPLOADED, 'media_1788745178599.png'))
w, h = img_sofabed.size
crop_sofabed = img_sofabed.crop((0, 0, w, int(h * 0.96)))
save_rgb_jpeg(crop_sofabed, os.path.join(IMAGES_DIR, 'th', 'TH-SF02-main.jpg'))
print("Saved assets/images/th/TH-SF02-main.jpg")

# 5. TH Dining Room Products
print("--- 5. Processing TH Dining Products ---")
dining_items = [
    {
        'file': 'media_1788745225682.png',
        'code': 'TH-BZ0396',
        'crop': (0, int(568 * 0.09), 770, int(568 * 0.86))
    },
    {
        'file': 'media_1788745239528.png',
        'code': 'TH-BZ2192',
        'crop': (0, int(552 * 0.09), 770, int(552 * 0.86))
    },
    {
        'file': 'media_1788745258376.png',
        'code': 'TH-BZ0296',
        'crop': (0, int(548 * 0.09), 770, int(548 * 0.86))
    },
    {
        'file': 'media_1788745293481.png',
        'code': 'TH-DT04-1',
        'crop': (0, int(630 * 0.03), 770, int(630 * 0.88))
    },
    {
        'file': 'media_1788745307160.png',
        'code': 'TH-DT04-2',
        'crop': (0, int(586 * 0.03), 770, int(586 * 0.88))
    }
]

for item in dining_items:
    img = Image.open(os.path.join(USER_UPLOADED, item['file']))
    w, h = img.size
    crop_rect = (0, int(h * 0.08), w, int(h * 0.86))
    crop_img = img.crop(crop_rect)
    save_rgb_jpeg(crop_img, os.path.join(IMAGES_DIR, 'th', f"{item['code']}-main.jpg"))
    print(f"Saved assets/images/th/{item['code']}-main.jpg")

# 6. TH Bedroom products
print("--- 6. Processing TH Bedroom Products ---")
th_bedroom_specs = [
    {
        'file': 'media_1788744734225.png',
        'code': 'TH-818',
        'top_crop_ratio': (0, 0.01, 1.0, 0.69),
        'thumb_ratios': [
            (0.12, 0.72, 0.40, 0.98),
            (0.40, 0.80, 0.64, 0.98)
        ]
    },
    {
        'file': 'media_1788744788776.png',
        'code': 'TH-IB108Q',
        'top_crop_ratio': (0.02, 0.20, 0.98, 0.78),
        'thumb_ratios': []
    },
    {
        'file': 'media_1788744808800.png',
        'code': 'TH-B0188',
        'top_crop_ratio': (0.01, 0.26, 0.99, 0.82),
        'thumb_ratios': []
    },
    {
        'file': 'media_1788744840626.png',
        'code': 'TH-B1902',
        'top_crop_ratio': (0, 0, 1.0, 0.57),
        'thumb_ratios': [
            (0, 0.58, 0.38, 0.78),
            (0.39, 0.58, 0.67, 0.78),
            (0.68, 0.58, 1.0, 0.98)
        ]
    },
    {
        'file': 'media_1788744862453.png',
        'code': 'TH-836',
        'top_crop_ratio': (0, 0, 1.0, 0.67),
        'thumb_ratios': [
            (0.64, 0.68, 1.0, 0.98)
        ]
    },
    {
        'file': 'media_1788744901613.png',
        'code': 'TH-839',
        'top_crop_ratio': (0, 0, 1.0, 0.61),
        'thumb_ratios': [
            (0.14, 0.62, 0.33, 0.98)
        ]
    },
    {
        'file': 'media_1788744909894.png',
        'code': 'TH-B230',
        'top_crop_ratio': (0, 0, 1.0, 0.61),
        'thumb_ratios': [
            (0.17, 0.75, 0.28, 0.98),
            (0.35, 0.82, 0.44, 0.98),
            (0.48, 0.80, 0.58, 0.98),
            (0.61, 0.84, 0.81, 0.98)
        ]
    },
    {
        'file': 'media_1788744925203.png',
        'code': 'TH-9903',
        'top_crop_ratio': (0, 0, 1.0, 0.67),
        'thumb_ratios': [
            (0, 0.68, 0.51, 0.98)
        ]
    },
    {
        'file': 'media_1788744952417.png',
        'code': 'TH-838',
        'top_crop_ratio': (0, 0, 1.0, 0.67),
        'thumb_ratios': [
            (0.13, 0.72, 0.34, 0.98),
            (0.35, 0.72, 0.56, 0.98)
        ]
    },
    {
        'file': 'media_1788744984178.png',
        'code': 'TH-010',
        'top_crop_ratio': (0, 0.28, 1.0, 0.66),
        'thumb_ratios': [
            (0.11, 0.35, 0.43, 0.63),
            (0.56, 0.32, 0.98, 0.64)
        ]
    },
    {
        'file': 'media_1788745098733.png',
        'code': 'TH-2506',
        'top_crop_ratio': (0, 0, 1.0, 0.59),
        'thumb_ratios': [
            (0.15, 0.60, 0.43, 0.82),
            (0.63, 0.52, 0.87, 0.81)
        ]
    },
    {
        'file': 'media_1788745110099.png',
        'code': 'TH-2503',
        'top_crop_ratio': (0, 0, 1.0, 0.66),
        'thumb_ratios': [
            (0.69, 0.77, 0.90, 0.98)
        ]
    },
    {
        'file': 'media_1788745116281.png',
        'code': 'TH-2608',
        'top_crop_ratio': (0, 0, 1.0, 0.67),
        'thumb_ratios': [
            (0.18, 0.70, 0.46, 0.96),
            (0.53, 0.70, 0.78, 0.96)
        ]
    }
]

for item in th_bedroom_specs:
    src_path = os.path.join(USER_UPLOADED, item['file'])
    img = Image.open(src_path)
    w, h = img.size
    
    r = item['top_crop_ratio']
    main_crop = img.crop((int(w * r[0]), int(h * r[1]), int(w * r[2]), int(h * r[3])))
    main_out = os.path.join(IMAGES_DIR, 'th', f"{item['code']}-main.jpg")
    save_rgb_jpeg(main_crop, main_out)
    print(f"Saved {main_out}")
    
    for idx, tr in enumerate(item['thumb_ratios']):
        t_crop = img.crop((int(w * tr[0]), int(h * tr[1]), int(w * tr[2]), int(h * tr[3])))
        t_out = os.path.join(IMAGES_DIR, 'th', f"{item['code']}-detail-{idx+1}.jpg")
        save_rgb_jpeg(t_crop, t_out)
        print(f"Saved detail thumbnail {t_out}")

print("--- All image processing successfully completed! ---")
