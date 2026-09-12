import subprocess, time

# Test slide 2, slide 3, slide 4 using chrome with script or evaluation
# We can open local file or url and trigger showSlide
script_eval = """
document.querySelector('.slideshow-next').click();
"""

# Let's take screenshot after clicking next slide
# Using Chrome remote debugging or a quick puppeteer/node or python script
# Let's write a simple HTML test page or use Chrome with a small script
