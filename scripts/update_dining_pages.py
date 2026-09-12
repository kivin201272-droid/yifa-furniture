#!/usr/bin/env python3
"""
scripts/update_dining_pages.py
Updates formal dining pages (dining/index.html and zh/dining/index.html)
with the 5 verified standalone SKUs from Dining Batch 1 (P41-P43).
"""

import json
import re

MANIFEST_PATH = "reports/manifest_v2_dining_batch1.json"

def update_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        item["ai_visual_reviewed"] = True
        item["human_reviewed"] = True
        item["verification_status"] = "approved_lifestyle_reference"
        item["status_reason"] = "Lifestyle scene reference approved by user. Visual highlight frame and disclaimer present."
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("[UPDATED] Manifest status set to approved_lifestyle_reference")

def build_en_card(item):
    price_display = f"${item['price']}"
    if item["pack"] == "2" or "CHAIR" in item["product_type"]:
        price_display += " / 2-pack"
    
    return f'''        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../{item['output_image']}" alt="{item['product_name_en']}" class="main-sofa-img" loading="lazy">
            </div>
            <div class="sofa-info">
                <h3>{item['product_name_en']}</h3>
                <p>PDF Spec: {item['dimensions']}</p>
                <p style="color:#b45309; font-size:0.82rem; margin-top:4px;">{item['staging_disclaimer_en']}</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">Sale Price {price_display}</span>
                    <span class="detail-tag">{item['dimensions']}</span>
                    <span class="detail-tag">PACK: {item['pack']}</span>
                </div>
            </div>
        </div>'''

def build_zh_card(item):
    price_display = f"${item['price']}"
    if item["pack"] == "2" or "CHAIR" in item["product_type"]:
        price_display += " / 2把装"
        
    return f'''        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="../../{item['output_image']}" alt="{item['product_name_zh']}" class="main-sofa-img" loading="lazy">
            </div>
            <div class="sofa-info">
                <h3>{item['product_name_zh']}</h3>
                <p>规格：{item['dimensions']}</p>
                <p style="color:#b45309; font-size:0.82rem; margin-top:4px;">{item['staging_disclaimer_zh']}</p>
                <div class="sofa-details">
                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">特惠价 {price_display}</span>
                    <span class="detail-tag">{item['dimensions']}</span>
                    <span class="detail-tag">PACK: {item['pack']}</span>
                </div>
            </div>
        </div>'''

def update_html():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # 1. Update English Page
    with open("dining/index.html", "r", encoding="utf-8") as f:
        en_html = f.read()
        
    # Replace old merged card
    old_en_card_pattern = r'<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\./assets/images/pj_dining/p6_img_10_204\.jpg".*?</div>\s*</div>\s*</div>'
    new_en_cards = "\n\n".join([build_en_card(item) for item in data])
    
    en_html_new, count_en = re.subn(old_en_card_pattern, new_en_cards, en_html, flags=re.DOTALL)
    assert count_en == 1, f"Expected 1 match in dining/index.html, got {count_en}"
    with open("dining/index.html", "w", encoding="utf-8") as f:
        f.write(en_html_new)
    print("[UPDATED] dining/index.html updated with 5 separate cards")

    # 2. Update Chinese Page
    with open("zh/dining/index.html", "r", encoding="utf-8") as f:
        zh_html = f.read()
        
    old_zh_card_pattern = r'<div class="sofa-card reveal">\s*<div class="sofa-img-container">\s*<img src="\.\./\.\./assets/images/pj_dining/p6_img_10_204\.jpg".*?</div>\s*</div>\s*</div>'
    new_zh_cards = "\n\n".join([build_zh_card(item) for item in data])
    
    zh_html_new, count_zh = re.subn(old_zh_card_pattern, new_zh_cards, zh_html, flags=re.DOTALL)
    assert count_zh == 1, f"Expected 1 match in zh/dining/index.html, got {count_zh}"
    with open("zh/dining/index.html", "w", encoding="utf-8") as f:
        f.write(zh_html_new)
    print("[UPDATED] zh/dining/index.html updated with 5 separate cards")

if __name__ == "__main__":
    update_manifest()
    update_html()
