import json, os, sys, re
import fitz
from PIL import Image

PDF_PATH = "/Users/kivinwang/Downloads/2026 PJ 型錄-內頁（final draft) (2).pdf"
MANIFEST_PATH = "reports/manifest_v2_office.json"
INVENTORY_PATH = "reports/pj_pdf_inventory.json"
F_AUDIT_PATH = "reports/f_series_audit.json"

print("=" * 70)
print("PJ CATALOG RIGOROUS INTEGRITY & BOUNDARY VERIFIER (V2)")
print("=" * 70)

doc = fitz.open(PDF_PATH)
pdf_pages_scanned = len(doc)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest_items = json.load(f)

errors = []
warnings = []

# 1. Coordinate boundary check against real PDF page dimensions
out_of_bounds_count = 0
for it in manifest_items:
    p_num = it["pdf_file_page"]
    page = doc[p_num - 1]
    pw = page.rect.width
    ph = page.rect.height

    crop_str = it["crop_coords"].replace("(", "").replace(")", "")
    coords = [float(v.strip()) for v in crop_str.split(",")]
    x0, y0, x1, y1 = coords

    if not (0 <= x0 < x1 <= pw):
        err = f"X-Boundary Error in SKU {it['sku']}: x0={x0}, x1={x1} outside [0, {pw}] pt"
        errors.append(err)
        out_of_bounds_count += 1

    if not (0 <= y0 < y1 <= ph):
        err = f"Y-Boundary Error in SKU {it['sku']}: y0={y0}, y1={y1} outside [0, {ph}] pt"
        errors.append(err)
        out_of_bounds_count += 1

# 2. Image content validation (blank image, non-white ratio, aspect ratio)
blank_images_count = 0
aspect_ratio_anomalies = 0
for it in manifest_items:
    fn = it["output_image"]
    if not os.path.exists(fn):
        errors.append(f"Missing image file: {fn} for SKU {it['sku']}")
        continue

    im = Image.open(fn).convert("RGB")
    w, h = im.size

    # Aspect ratio check (between 0.3 and 3.0)
    aspect = w / h
    if aspect < 0.3 or aspect > 3.0:
        err = f"Extreme Aspect Ratio in SKU {it['sku']} ({fn}): aspect={aspect:.2f}"
        errors.append(err)
        aspect_ratio_anomalies += 1

    # Non-white pixel check
    pixels = list(im.getdata())
    non_white = sum(1 for (r, g, b) in pixels if not (r > 240 and g > 240 and b > 240))
    ratio = non_white / (w * h)
    if ratio < 0.05:
        err = f"Blank Image Error in SKU {it['sku']} ({fn}): non-white ratio {ratio*100:.1f}% < 5%"
        errors.append(err)
        blank_images_count += 1

# 3. Check verification status & approval
approved_count = sum(1 for it in manifest_items if it.get("verification_status") == "approved" and it.get("human_reviewed") is True)

# 4. Check category matching
category_mismatches = 0
for it in manifest_items:
    ptype = (it["product_type_raw"] or "").lower()
    fn = it["output_image"].lower()
    if "desk" in ptype and "chair" in fn:
        errors.append(f"Category Mismatch: SKU {it['sku']} ({ptype}) contains chair image: {fn}")
        category_mismatches += 1

# 5. Check legacy pdf3 in office HTML
legacy_pdf3_count = 0
for p in ["zh/office/index.html", "office/index.html"]:
    with open(p, "r", encoding="utf-8") as fp:
        matches = re.findall(r'pdf3/img-[0-9]+\.jpg', fp.read())
        legacy_pdf3_count += len(matches)
if legacy_pdf3_count > 0:
    errors.append(f"Legacy pdf3 references found in Office: {legacy_pdf3_count}")

# Print summary
print(f"PDF pages scanned:            {pdf_pages_scanned}")
print(f"Office SKUs in batch:          {len(manifest_items)}")
print(f"Out-of-bounds coordinate errors: {out_of_bounds_count}")
print(f"Blank image errors:           {blank_images_count}")
print(f"Extreme aspect ratio errors:  {aspect_ratio_anomalies}")
print(f"Category mismatch errors:     {category_mismatches}")
print(f"Legacy pdf3 references:       {legacy_pdf3_count}")
print(f"User approved SKUs:           {approved_count}/{len(manifest_items)}")
print("=" * 70)

if errors:
    print(f"VERIFICATION FAILED: {len(errors)} errors encountered:")
    for e in errors:
        print(f"  [ERROR] {e}")
    sys.exit(1)
else:
    print("ALL INTEGRITY AND BOUNDARY CHECKS PASSED: 0 errors.")
    sys.exit(0)
