import re, os
from PIL import Image

public_pages = [
    "index.html", "about/index.html", "contact/index.html", "faq/index.html",
    "products/index.html", "mattress/index.html", "magical-mattress/index.html",
    "bedroom/index.html", "living-room/index.html", "dining/index.html", "office/index.html",
    "zh/index.html", "zh/about/index.html", "zh/contact/index.html", "zh/faq/index.html",
    "zh/products/index.html", "zh/mattress/index.html", "zh/magical-mattress/index.html",
    "zh/bedroom/index.html", "zh/living-room/index.html", "zh/dining/index.html", "zh/office/index.html"
]

images_in_pages = set()
for page in public_pages:
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r'src=["\']([^"\'\>]+)["\']', content)
            for m in matches:
                src = m.split("?")[0]
                if "assets/images/" in src:
                    idx = src.find("assets/images/")
                    images_in_pages.add(src[idx:])

print("Total active website images:", len(images_in_pages))
stats = []
for rel in sorted(images_in_pages):
    if os.path.exists(rel):
        with Image.open(rel) as im:
            stats.append((rel, im.size, os.path.getsize(rel)))
    else:
        print("Missing:", rel)

stats.sort(key=lambda x: x[1][0] * x[1][1])
print("Smallest 20 active images:")
for p, sz, bytes_sz in stats[:20]:
    print(f"  {p}: {sz} ({bytes_sz//1024} KB)")

print("\nLargest 10 active images:")
for p, sz, bytes_sz in stats[-10:]:
    print(f"  {p}: {sz} ({bytes_sz//1024} KB)")
