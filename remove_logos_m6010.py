from PIL import Image, ImageDraw

path = 'assets/images/pdf6/img-001.jpg'
with Image.open(path) as im:
    if im.mode == 'CMYK':
        im = im.convert('RGB')
    
    draw = ImageDraw.Draw(im)
    
    # 1. Top left logo "SLEEPY EDGE INC." + "Premium Mattresses..."
    # The image is 1102x1255. Let's cover the top left region: 
    # x from 0 to 700, y from 0 to 450
    draw.rectangle([0, 0, 750, 450], fill=(0, 0, 0))
    
    # 2. Mattress logo "SLEEPY EDGE"
    # It's at the bottom right, on the yellow mattress surface.
    # The mattress face seems to be a solid yellow/mustard color.
    # Let's sample a pixel near the logo (e.g. x=800, y=850)
    # Actually, the yellow part is at the bottom right. Let's just cover a rectangle
    # x from 750 to 950, y from 800 to 950. We need precise coordinates.
    # We can just look for the black pixels of the logo in that region, and replace them with the median color of that region.
    # Let's do a smart replacement: in region [700:1000, 750:1000], if a pixel is dark (r<100, g<100, b<100), change it to yellow.
    
    # Find the median color of the mattress in that region
    mattress_region = im.crop((700, 750, 1000, 1000))
    pixels = list(mattress_region.getdata())
    # Filter out the black logo pixels to find the background color
    bg_pixels = [p for p in pixels if p[0] > 100 or p[1] > 100]
    
    if bg_pixels:
        # Calculate average color
        avg_r = int(sum(p[0] for p in bg_pixels) / len(bg_pixels))
        avg_g = int(sum(p[1] for p in bg_pixels) / len(bg_pixels))
        avg_b = int(sum(p[2] for p in bg_pixels) / len(bg_pixels))
        bg_color = (avg_r, avg_g, avg_b)
        
        # Now fill the logo area with this color
        # Where exactly is the logo? The user screenshot shows it in the bottom right corner of the mattress.
        # Let's just draw a rectangle over the logo area.
        # x: 750 to 950, y: 750 to 950
        draw.rectangle([720, 750, 950, 930], fill=bg_color)
        
    im.save(path)
    print("Logos removed for M6010")
