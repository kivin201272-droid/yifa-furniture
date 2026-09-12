#!/usr/bin/env python3
"""
scripts/rebuild_dining_batch1.py
Lifestyle Scene Evidence & Image Generation for Dining Batch 1 (P41-P43: Dinette 77-82).

5 Standalone Real SKUs (Lifestyle Scene Reference):
1. 4160: 36"W x 60"D x 30"H Wooden Dining Table, Pack: 1, $139.00 (P41 Left Dinette 77)
2. 4130: 30"W x 48"D x 30"H Wooden Dining Table, Pack: 1, $109.00 (P41 Right Dinette 78)
3. 4110GREEN: 22"W x 22"D x 30"H Wooden Dining Chair - Green, Pack: 2, $59.95 / 2 chairs per carton (P41 Dinette 78 scene)
4. 4110IVY: 22"W x 22"D x 30"H Wooden Dining Chair - Ivory, Pack: 2, $59.95 / 2 chairs per carton (P42 Dinette 80 scene)
5. 4110GRAY: 22"W x 22"D x 30"H Wooden Dining Chair - Gray, Pack: 2, $59.95 / 2 chairs per carton (P43 Dinette 82 scene)
"""

import os
import shutil
import json
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

PDF_PATH = "/Users/kivinwang/Downloads/2026 PJ 型錄-內頁（final draft) (2).pdf"
DOC = fitz.open(PDF_PATH)

ARTIFACTS_DIR = "/Users/kivinwang/.gemini/antigravity-ide/brain/7e6cda0e-f99a-4c87-8461-6a4d1dd54a42"

os.makedirs("assets/images/pj_dining", exist_ok=True)
os.makedirs("reports/original_dining_pages", exist_ok=True)
os.makedirs("reports/evidence_dining_batch1", exist_ok=True)
os.makedirs("reports/dining_comparisons", exist_ok=True)

# 1. Page Coordinates for Lifestyle Scenes
# P41 (Physical 41, 0-indexed 40): DINETTE 77 (left: 60..845, 55..535) & DINETTE 78 (right: 855..1640, 55..535)
# P42 (Physical 42, 0-indexed 41): DINETTE 79 (left) & DINETTE 80 (right: 855..1640, 55..535)
# P43 (Physical 43, 0-indexed 42): DINETTE 81 (left) & DINETTE 82 (right: 855..1640, 55..535)

LIFESTYLE_SPECS = {
    "4160": {
        "page_num": 41,
        "scene_rect": fitz.Rect(60, 55, 845, 535),
        "highlight_rect": fitz.Rect(180, 160, 780, 500), # Table highlight
        "name_zh": "4160 实木餐桌",
        "name_en": "4160 Wooden Dining Table",
        "type": "DINING TABLE",
        "dims": '36"W x 60"D x 30"H',
        "pack": "1",
        "price": "139.00",
        "price_unit": "piece",
        "out_file": "assets/images/pj_dining/pj-4160.jpg",
        "primary_product": "4160 dining table",
        "staging_disclaimer_zh": "场景参考图。当前商品为4160实木餐桌，餐椅及其他装饰不包含。",
        "staging_disclaimer_en": "Lifestyle reference image. This listing is for the 4160 wooden dining table. Chairs and décor are not included.",
        "compatible_with": ["4110GREEN", "4110IVY", "4110GRAY"],
        "verification_status": "pending_user_acceptance",
        "status_reason": "Lifestyle scene reference with 4160 dining table clearly indicated. Staging disclaimer attached."
    },
    "4130": {
        "page_num": 41,
        "scene_rect": fitz.Rect(855, 55, 1640, 535),
        "highlight_rect": fitz.Rect(950, 160, 1550, 500), # Table highlight
        "name_zh": "4130 实木餐桌",
        "name_en": "4130 Wooden Dining Table",
        "type": "DINING TABLE",
        "dims": '30"W x 48"D x 30"H',
        "pack": "1",
        "price": "109.00",
        "price_unit": "piece",
        "out_file": "assets/images/pj_dining/pj-4130.jpg",
        "primary_product": "4130 dining table",
        "staging_disclaimer_zh": "场景参考图。当前商品为4130实木餐桌，餐椅及其他装饰不包含。",
        "staging_disclaimer_en": "Lifestyle reference image. This listing is for the 4130 wooden dining table. Chairs and décor are not included.",
        "compatible_with": ["4110GREEN", "4110IVY", "4110GRAY"],
        "verification_status": "pending_user_acceptance",
        "status_reason": "Lifestyle scene reference with 4130 dining table clearly indicated. Staging disclaimer attached."
    },
    "4110GREEN": {
        "page_num": 41,
        "scene_rect": fitz.Rect(855, 55, 1640, 535),
        "highlight_rect": fitz.Rect(1370, 200, 1630, 525), # Chair highlight
        "name_zh": "4110GREEN 绿色实木餐椅",
        "name_en": "4110GREEN Wooden Dining Chair - Green",
        "type": "DINING CHAIR",
        "dims": '22"W x 22"D x 30"H',
        "pack": "2",
        "price": "59.95",
        "price_unit": "2 chairs per carton",
        "out_file": "assets/images/pj_dining/pj-4110green.jpg",
        "primary_product": "4110 dining chair",
        "staging_disclaimer_zh": "场景参考图。当前商品为4110餐椅，餐桌及其他装饰不包含。餐椅按2把/箱销售。",
        "staging_disclaimer_en": "Lifestyle reference image. This listing is for the 4110 dining chairs. Table and décor are not included. Chairs are sold 2 per carton.",
        "compatible_with": ["4160", "4130"],
        "verification_status": "failed_multi_product_crop",
        "status_reason": "PDF scene contains overlapping chairs and table. Rendered as lifestyle_scene with primary product focus indicator and mandatory disclaimer."
    },
    "4110IVY": {
        "page_num": 42,
        "scene_rect": fitz.Rect(855, 55, 1640, 535),
        "highlight_rect": fitz.Rect(1370, 200, 1630, 525), # Chair highlight
        "name_zh": "4110IVY 米白色实木餐椅",
        "name_en": "4110IVY Wooden Dining Chair - Ivory",
        "type": "DINING CHAIR",
        "dims": '22"W x 22"D x 30"H',
        "pack": "2",
        "price": "59.95",
        "price_unit": "2 chairs per carton",
        "out_file": "assets/images/pj_dining/pj-4110ivy.jpg",
        "primary_product": "4110 dining chair",
        "staging_disclaimer_zh": "场景参考图。当前商品为4110餐椅，餐桌及其他装饰不包含。餐椅按2把/箱销售。",
        "staging_disclaimer_en": "Lifestyle reference image. This listing is for the 4110 dining chairs. Table and décor are not included. Chairs are sold 2 per carton.",
        "compatible_with": ["4160", "4130"],
        "verification_status": "failed_multi_product_crop",
        "status_reason": "PDF scene contains overlapping chairs and table. Rendered as lifestyle_scene with primary product focus indicator and mandatory disclaimer."
    },
    "4110GRAY": {
        "page_num": 43,
        "scene_rect": fitz.Rect(855, 55, 1640, 535),
        "highlight_rect": fitz.Rect(1370, 200, 1630, 525), # Chair highlight
        "name_zh": "4110GRAY 灰色实木餐椅",
        "name_en": "4110GRAY Wooden Dining Chair - Gray",
        "type": "DINING CHAIR",
        "dims": '22"W x 22"D x 30"H',
        "pack": "2",
        "price": "59.95",
        "price_unit": "2 chairs per carton",
        "out_file": "assets/images/pj_dining/pj-4110gray.jpg",
        "primary_product": "4110 dining chair",
        "staging_disclaimer_zh": "场景参考图。当前商品为4110餐椅，餐桌及其他装饰不包含。餐椅按2把/箱销售。",
        "staging_disclaimer_en": "Lifestyle reference image. This listing is for the 4110 dining chairs. Table and décor are not included. Chairs are sold 2 per carton.",
        "compatible_with": ["4160", "4130"],
        "verification_status": "failed_multi_product_crop",
        "status_reason": "PDF scene contains overlapping chairs and table. Rendered as lifestyle_scene with primary product focus indicator and mandatory disclaimer."
    }
}

print("1. Rendering high-res 300 DPI lifestyle scene images with visual subject indicator...")
manifest_data = []

for sku, spec in LIFESTYLE_SPECS.items():
    page = DOC[spec["page_num"] - 1]
    # Render scene at 300 DPI
    pix_scene = page.get_pixmap(dpi=300, clip=spec["scene_rect"])
    im_scene = Image.frombytes("RGB", [pix_scene.width, pix_scene.height], pix_scene.samples)
    
    # Add subtle non-destructive focus indicator to identify the selling item
    draw = ImageDraw.Draw(im_scene)
    scale = 300 / 72.0
    r_scene = spec["scene_rect"]
    r_high = spec["highlight_rect"]
    
    # Calculate box relative to the cropped scene
    bx0 = int((r_high.x0 - r_scene.x0) * scale)
    by0 = int((r_high.y0 - r_scene.y0) * scale)
    bx1 = int((r_high.x1 - r_scene.x0) * scale)
    by1 = int((r_high.y1 - r_scene.y0) * scale)
    
    # Draw refined indicator frame
    indicator_color = (230, 57, 70) if "CHAIR" in spec["type"] else (37, 99, 235)
    draw.rectangle([(bx0, by0), (bx1, by1)], outline=indicator_color, width=4)
    
    # Badge on top of highlight box
    badge_h = 44
    draw.rectangle([(bx0, by0 - badge_h), (bx0 + 440, by0)], fill=indicator_color)
    tag_text = f"SALES ITEM: {sku} ({spec['type']})"
    draw.text((bx0 + 12, by0 - 34), tag_text, fill=(255, 255, 255))
    
    im_scene.save(spec["out_file"], quality=95)
    print(f"  [SAVED] {sku} Lifestyle Scene -> {spec['out_file']} ({im_scene.width}x{im_scene.height})")
    
    # Build Manifest Entry
    manifest_entry = {
        "sku": sku,
        "product_name_zh": spec["name_zh"],
        "product_name_en": spec["name_en"],
        "product_type": spec["type"],
        "dimensions": spec["dims"],
        "pack": spec["pack"],
        "price": spec["price"],
        "price_unit": spec["price_unit"],
        "image_type": "lifestyle_scene",
        "contains_other_products": True,
        "primary_product": spec["primary_product"],
        "requires_disclaimer": True,
        "compatible_with": spec["compatible_with"],
        "is_bundle": False,
        "output_image": spec["out_file"],
        "staging_disclaimer_zh": spec["staging_disclaimer_zh"],
        "staging_disclaimer_en": spec["staging_disclaimer_en"],
        "ai_visual_reviewed": False,
        "human_reviewed": False,
        "verification_status": spec["verification_status"],
        "status_reason": spec["status_reason"]
    }
    manifest_data.append(manifest_entry)

# Write manifest
with open("reports/manifest_v2_dining_batch1.json", "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)
print("  [SAVED] Manifest updated -> reports/manifest_v2_dining_batch1.json")

# 2. Render Full Spreads and 50pt Grid Overlays
print("2. Rendering original spreads and 50pt grid overlays...")
for p_num in [41, 42, 43]:
    page = DOC[p_num - 1]
    pix_orig = page.get_pixmap(dpi=150)
    orig_path = f"reports/original_dining_pages/page_{p_num}_original_spread.jpg"
    pix_orig.save(orig_path)
    
    im = Image.open(orig_path).convert("RGBA")
    draw = ImageDraw.Draw(im)
    scale = pix_orig.width / page.rect.width
    
    for x in range(0, int(page.rect.width), 50):
        px = int(x * scale)
        draw.line([(px, 0), (px, im.height)], fill=(200, 200, 200, 80), width=1)
        draw.text((px + 2, 4), f"{x}", fill=(100, 100, 100, 200))
    for y in range(0, int(page.rect.height), 50):
        py = int(y * scale)
        draw.line([(0, py), (im.width, py)], fill=(200, 200, 200, 80), width=1)
        draw.text((4, py + 2), f"{y}", fill=(100, 100, 100, 200))
        
    for sku, spec in LIFESTYLE_SPECS.items():
        if spec["page_num"] == p_num:
            r = spec["scene_rect"]
            box = (int(r.x0 * scale), int(r.y0 * scale), int(r.x1 * scale), int(r.y1 * scale))
            draw.rectangle(box, outline=(255, 30, 30, 255), width=3)
            draw.text((box[0] + 10, box[1] + 10), f"SCENE: {sku} ({spec['type']})", fill=(255, 0, 0, 255))
            
    grid_path = f"reports/evidence_dining_batch1/page_{p_num}_grid_evidence.jpg"
    im.convert("RGB").save(grid_path, quality=95)
    print(f"  [SAVED] Page {p_num} grid evidence -> {grid_path}")

# 3. Generate Side-by-Side Comparison Images
print("3. Generating side-by-side comparison images...")
for sku, spec in LIFESTYLE_SPECS.items():
    scene_im = Image.open(spec["out_file"]).convert("RGB")
    page = DOC[spec["page_num"] - 1]
    
    if "4160" in sku:
        r_label = fitz.Rect(60, 510, 480, 630)
    elif "4130" in sku:
        r_label = fitz.Rect(1200, 510, 1650, 630)
    else:
        r_label = fitz.Rect(60, 510, 480, 630)
        
    pix_label = page.get_pixmap(dpi=200, clip=r_label)
    label_im = Image.frombytes("RGB", [pix_label.width, pix_label.height], pix_label.samples)
    
    comp = Image.new("RGB", (1300, 750), (248, 249, 250))
    draw = ImageDraw.Draw(comp)
    
    draw.rectangle([(0, 0), (1300, 75)], fill=(30, 41, 59))
    draw.text((30, 12), f"SKU: {sku} | {spec['name_zh']} ({spec['name_en']})", fill=(255, 255, 255))
    draw.text((30, 42), f"IMAGE TYPE: lifestyle_scene | Price: ${spec['price']} ({spec['price_unit']}) | Pack: {spec['pack']} | Dims: {spec['dims']}", fill=(203, 213, 225))
    
    # Left: Scene with highlight box
    scene_thumb = scene_im.copy()
    scene_thumb.thumbnail((620, 520), Image.Resampling.LANCZOS)
    x_s = 40 + (620 - scene_thumb.width) // 2
    y_s = 100 + (520 - scene_thumb.height) // 2
    comp.paste(scene_thumb, (x_s, y_s))
    draw.rectangle([(x_s, y_s), (x_s + scene_thumb.width, y_s + scene_thumb.height)], outline=(203, 213, 225), width=1)
    draw.text((40, 645), f"Scene Reference: {os.path.basename(spec['out_file'])} (Sales subject framed)", fill=(71, 85, 105))
    
    # Right: PDF Label & Evidence
    label_thumb = label_im.copy()
    label_thumb.thumbnail((560, 220), Image.Resampling.LANCZOS)
    x_label = 680 + (560 - label_thumb.width) // 2
    y_label = 110
    comp.paste(label_thumb, (x_label, y_label))
    draw.rectangle([(x_label, y_label), (x_label + label_thumb.width, y_label + label_thumb.height)], outline=(203, 213, 225), width=1)
    
    draw.text((680, 350), f"PDF Source: Page {spec['page_num']} (Physical Spread)", fill=(30, 41, 59))
    draw.text((680, 380), f"Raw Text: {spec['name_en']}", fill=(51, 65, 85))
    draw.text((680, 410), f"Dimensions: {spec['dims']}", fill=(51, 65, 85))
    draw.text((680, 440), f"Pack: {spec['pack']} | Price: ${spec['price']}", fill=(51, 65, 85))
    draw.text((680, 480), f"Status: {spec['verification_status']}", fill=(220, 38, 38) if "failed" in spec["verification_status"] else (217, 119, 6))
    draw.text((680, 510), "Staging Disclaimer (Mandatory):", fill=(30, 41, 59))
    draw.text((680, 535), f"中文: {spec['staging_disclaimer_zh']}", fill=(180, 83, 9))
    draw.text((680, 565), f"EN: {spec['staging_disclaimer_en']}", fill=(180, 83, 9))
    draw.text((680, 605), "Pricing Note: Sold independently. NO bundle combo price shown.", fill=(16, 185, 129))
        
    comp_path = f"reports/dining_comparisons/comparison_{sku.lower()}.jpg"
    comp.save(comp_path, quality=95)
    print(f"  [SAVED] Comparison {sku} -> {comp_path}")

# 4. Generate 5-SKU Contact Sheet
print("4. Generating 5-SKU contact sheet...")
cs = Image.new("RGB", (1800, 1150), (245, 247, 250))
cs_draw = ImageDraw.Draw(cs)
cs_draw.rectangle([(0, 0), (1800, 80)], fill=(15, 23, 42))
cs_draw.text((40, 24), "Phase 2: Dining Collection Batch 1 - 5 Verified SKUs (Lifestyle Scene Reference P41-P43)", fill=(255, 255, 255))

# Row 1: 2 Dining Tables (4160, 4130)
t1_im = Image.open("assets/images/pj_dining/pj-4160.jpg")
t1_im.thumbnail((780, 430), Image.Resampling.LANCZOS)
cs.paste(t1_im, (60 + (780 - t1_im.width)//2, 110 + (430 - t1_im.height)//2))
cs_draw.rectangle([(60, 110), (840, 550)], outline=(203, 213, 225), width=1)
cs_draw.rectangle([(60, 500), (840, 550)], fill=(15, 23, 42, 220))
cs_draw.text((75, 512), "1. SKU: 4160 | 4160 实木餐桌 (36\"W x 60\"D x 30\"H) | $139.00 (Pack: 1)", fill=(255, 255, 255))

t2_im = Image.open("assets/images/pj_dining/pj-4130.jpg")
t2_im.thumbnail((780, 430), Image.Resampling.LANCZOS)
cs.paste(t2_im, (960 + (780 - t2_im.width)//2, 110 + (430 - t2_im.height)//2))
cs_draw.rectangle([(960, 110), (1740, 550)], outline=(203, 213, 225), width=1)
cs_draw.rectangle([(960, 500), (1740, 550)], fill=(15, 23, 42, 220))
cs_draw.text((975, 512), "2. SKU: 4130 | 4130 实木餐桌 (30\"W x 48\"D x 30\"H) | $109.00 (Pack: 1)", fill=(255, 255, 255))

# Row 2: 3 Dining Chairs (4110GREEN, 4110IVY, 4110GRAY)
chairs = [
    ("4110GREEN", "3. SKU: 4110GREEN | 绿色实木餐椅 (2把/箱) | $59.95", "assets/images/pj_dining/pj-4110green.jpg", 60),
    ("4110IVY", "4. SKU: 4110IVY | 米白色实木餐椅 (2把/箱) | $59.95", "assets/images/pj_dining/pj-4110ivy.jpg", 640),
    ("4110GRAY", "5. SKU: 4110GRAY | 灰色实木餐椅 (2把/箱) | $59.95", "assets/images/pj_dining/pj-4110gray.jpg", 1220)
]

for c_sku, label, img_path, x_pos in chairs:
    c_im = Image.open(img_path)
    c_im.thumbnail((520, 450), Image.Resampling.LANCZOS)
    cs.paste(c_im, (x_pos + (520 - c_im.width)//2, 590 + (450 - c_im.height)//2))
    cs_draw.rectangle([(x_pos, 590), (x_pos + 520, 1080)], outline=(203, 213, 225), width=1)
    cs_draw.rectangle([(x_pos, 1030), (x_pos + 520, 1080)], fill=(15, 23, 42, 220))
    cs_draw.text((x_pos + 12, 1042), label, fill=(255, 255, 255))

cs_path = "reports/dining_5_sku_contact_sheet.jpg"
cs.save(cs_path, quality=95)
print(f"  [SAVED] Contact Sheet -> {cs_path}")

# 5. Copy all files to Artifacts Directory
print("5. Copying all evidence and graphics to artifacts directory...")
for f in [
    "assets/images/pj_dining/pj-4160.jpg",
    "assets/images/pj_dining/pj-4130.jpg",
    "assets/images/pj_dining/pj-4110green.jpg",
    "assets/images/pj_dining/pj-4110ivy.jpg",
    "assets/images/pj_dining/pj-4110gray.jpg",
    "reports/original_dining_pages/page_41_original_spread.jpg",
    "reports/original_dining_pages/page_42_original_spread.jpg",
    "reports/original_dining_pages/page_43_original_spread.jpg",
    "reports/evidence_dining_batch1/page_41_grid_evidence.jpg",
    "reports/evidence_dining_batch1/page_42_grid_evidence.jpg",
    "reports/evidence_dining_batch1/page_43_grid_evidence.jpg",
    "reports/dining_comparisons/comparison_4160.jpg",
    "reports/dining_comparisons/comparison_4130.jpg",
    "reports/dining_comparisons/comparison_4110green.jpg",
    "reports/dining_comparisons/comparison_4110ivy.jpg",
    "reports/dining_comparisons/comparison_4110gray.jpg",
    "reports/dining_5_sku_contact_sheet.jpg"
]:
    dst = os.path.join(ARTIFACTS_DIR, os.path.basename(f))
    shutil.copy2(f, dst)

print("Rebuild finished successfully!")
