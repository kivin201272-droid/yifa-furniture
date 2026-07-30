from PIL import Image

path = 'assets/images/pdf6/img-001.jpg'
with Image.open(path) as im:
    if im.mode == 'CMYK':
        im = im.convert('RGB')
    print(f'Mode: {im.mode}')
    print(f'Top-left pixel: {im.getpixel((10,10))}')
    print(f'Middle-left pixel: {im.getpixel((10, im.height//2))}')
