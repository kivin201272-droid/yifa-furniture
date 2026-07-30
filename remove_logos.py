import os
from PIL import Image, ImageDraw

# 1. F3054 (img-386.jpg)
# Fill the bottom half with the background color to erase text
f3054_path = 'assets/images/pdf3/img-386.jpg'
try:
    with Image.open(f3054_path) as im:
        # Sample color at top left (green background)
        bg_color = im.getpixel((10, 10))
        draw = ImageDraw.Draw(im)
        # The text is in the bottom half. Let's fill from y = height * 0.55 to bottom
        height = im.height
        draw.rectangle([0, int(height * 0.55), im.width, height], fill=bg_color)
        im.save(f3054_path)
        print("Processed F3054")
except Exception as e:
    print("Failed F3054:", e)

# 2. Dining Set (collection-dining.jpg)
# Crop the top 35% where the huge PJ WAREHOUSE text is
dining_path = 'assets/images/collection-dining.jpg'
try:
    with Image.open(dining_path) as im:
        crop_y = int(im.height * 0.35)
        im_cropped = im.crop((0, crop_y, im.width, im.height))
        im_cropped.save(dining_path)
        print("Processed Dining Set")
except Exception as e:
    print("Failed Dining Set:", e)

# 3. Classic Mattresses (pdf6/)
# Crop the bottom 12% from all classic mattress images to remove logos
pdf6_dir = 'assets/images/pdf6'
try:
    for filename in os.listdir(pdf6_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            if filename == 'N6001.png': 
                continue # Skip the one I just added if it's fine
            filepath = os.path.join(pdf6_dir, filename)
            with Image.open(filepath) as im:
                crop_y = int(im.height * 0.88)
                im_cropped = im.crop((0, 0, im.width, crop_y))
                im_cropped.save(filepath)
    print("Processed Classic Mattresses")
except Exception as e:
    print("Failed Classic Mattresses:", e)

