from PIL import Image, ImageDraw

def fix_image(filename):
    path = 'assets/images/pdf6/' + filename
    try:
        with Image.open(path) as im:
            # The logo is in the top-left to top-center.
            # It's on a black background. Let's sample top-left pixel.
            bg_color = im.getpixel((50, 50))
            
            # The logo is roughly top 18% and left 60% of width.
            # Wait, "BETTER SLEEP, BETTER LIFE" is also there.
            # Let's just draw a rectangle over the logo. 
            # Height of image is 3025. The logo is above "BETTER SLEEP, BETTER LIFE"
            # Looking at proportions, logo is from y=0 to y=600 roughly.
            # Let's fill a rectangle from (0, 0) to (width * 0.55, height * 0.17).
            
            draw = ImageDraw.Draw(im)
            draw.rectangle([0, 0, int(im.width * 0.6), int(im.height * 0.17)], fill=bg_color)
            
            im.save(path)
            print(f"Fixed {filename}")
    except Exception as e:
        print(f"Failed {filename}: {e}")

fix_image('img-040.jpg')
fix_image('img-041.jpg')

