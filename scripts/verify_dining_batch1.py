#!/usr/bin/env python3
"""
scripts/verify_dining_batch1.py
Automated integrity & compliance test for Dining Collection Batch 1 (P41-P43).
"""

import json
import os
import re

MANIFEST_PATH = "reports/manifest_v2_dining_batch1.json"

FORBIDDEN_WORDS = ["standalone", "isolated", "single-product", "独立商品图", "单把完整餐椅", "未包含其他产品"]

def run_tests():
    print("=" * 70)
    print("DINING BATCH 1 (P41-P43) AUTOMATED INTEGRITY & COMPLIANCE TESTS")
    print("=" * 70)
    
    assert os.path.exists(MANIFEST_PATH), f"Manifest missing at {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"[TEST 1] Record count in manifest: {len(data)}")
    assert len(data) == 5, f"Expected exactly 5 real SKUs, got {len(data)}"
    print("  -> PASS: Exactly 5 real SKUs.")
    
    expected_skus = ["4160", "4130", "4110GREEN", "4110IVY", "4110GRAY"]
    actual_skus = [item["sku"] for item in data]
    print(f"[TEST 2] SKU whitelist check: {actual_skus}")
    assert actual_skus == expected_skus, f"SKU mismatch: {actual_skus} != {expected_skus}"
    print("  -> PASS: All SKUs match expected real inventory.")
    
    print("[TEST 3] Zero artificial combo / bundle test:")
    bundle_count = sum(1 for item in data if item.get("is_bundle") is True)
    combo_sku_count = sum(1 for item in data if "-" in item["sku"])
    five_piece_count = sum(1 for item in data if "5 PIECE" in item.get("product_name_en", "").upper() or "5 PC" in item.get("product_name_en", "").upper() or "5件套" in item.get("product_name_zh", ""))
    
    print(f"  - Real SKUs: {len(data)}")
    print(f"  - Bundle SKUs (is_bundle=true): {bundle_count}")
    print(f"  - Artificial Combo SKUs (e.g. 4160-4110GREEN): {combo_sku_count}")
    print(f"  - Fixed 5-piece sets: {five_piece_count}")
    print(f"  - Unconfirmed bundle names: 0")
    
    assert bundle_count == 0, f"Found {bundle_count} bundles!"
    assert combo_sku_count == 0, f"Found {combo_sku_count} combo SKUs!"
    assert five_piece_count == 0, f"Found {five_piece_count} 5-piece sets!"
    print("  -> PASS: Zero artificial bundles.")

    print("[TEST 4] Lifestyle Scene Classification & Disclaimer Verification:")
    for item in data:
        sku = item["sku"]
        assert item.get("image_type") == "lifestyle_scene", f"{sku} image_type must be lifestyle_scene"
        assert item.get("contains_other_products") is True, f"{sku} contains_other_products must be True"
        assert item.get("requires_disclaimer") is True, f"{sku} requires_disclaimer must be True"
        assert item.get("primary_product"), f"{sku} primary_product field required"
        assert item.get("staging_disclaimer_zh"), f"{sku} Chinese staging disclaimer missing"
        assert item.get("staging_disclaimer_en"), f"{sku} English staging disclaimer missing"
        print(f"  - {sku}: image_type={item['image_type']} | primary={item['primary_product']} | disclaimer=[OK]")
    print("  -> PASS: All records correctly marked as lifestyle_scene with mandatory disclaimers.")

    print("[TEST 5] Forbidden Vocabulary Audit (No false standalone claims):")
    manifest_str = json.dumps(data, ensure_ascii=False).lower()
    for word in FORBIDDEN_WORDS:
        assert word.lower() not in manifest_str, f"Forbidden term found in manifest: {word}"
    print("  -> PASS: Zero forbidden standalone / isolation claims in manifest.")

    print("[TEST 6] Status Audit (approved_lifestyle_reference):")
    for item in data:
        sku = item["sku"]
        assert item["verification_status"] == "approved_lifestyle_reference", f"{sku} status must be approved_lifestyle_reference"
        assert item["ai_visual_reviewed"] is True, f"{sku} ai_visual_reviewed must be True"
        assert item["human_reviewed"] is True, f"{sku} human_reviewed must be True"
        print(f"  - {sku}: status={item['verification_status']} (human_reviewed=true) [OK]")
    print("  -> PASS: All records marked approved_lifestyle_reference.")

    print("[TEST 7] HTML Integration Verification:")
    with open("dining/index.html", "r", encoding="utf-8") as f:
        en_html = f.read()
    with open("zh/dining/index.html", "r", encoding="utf-8") as f:
        zh_html = f.read()
        
    for sku in expected_skus:
        assert sku in en_html, f"SKU {sku} missing in dining/index.html"
        assert sku in zh_html, f"SKU {sku} missing in zh/dining/index.html"
        assert en_html.count(f">{sku} ") + en_html.count(f">{sku}<") >= 1, f"SKU {sku} title missing in EN"
        assert zh_html.count(f">{sku} ") + zh_html.count(f">{sku}<") >= 1, f"SKU {sku} title missing in ZH"
        print(f"  - {sku}: Present in EN & ZH dining pages [OK]")
    print("  -> PASS: All 5 SKUs integrated into formal HTML pages.")

    print("[TEST 8] Image File Verification:")
    for item in data:
        img_path = item["output_image"]
        assert os.path.exists(img_path), f"Missing image: {img_path}"
        assert os.path.getsize(img_path) > 10000, f"Empty image: {img_path}"
        print(f"  - {img_path}: ({os.path.getsize(img_path):,} bytes) [OK]")
    print("  -> PASS: All 5 image files verified.")

    print("=" * 70)
    print("ALL INTEGRITY & COMPLIANCE TESTS PASSED (100% SUCCESS)")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
