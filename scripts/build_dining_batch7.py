#!/usr/bin/env python3
"""
scripts/build_dining_batch7.py
Extracts raw text, builds Batch 7 Manifest, generates contact sheet,
and updates frozen text hashes for Dining Batch 7 (P59-P61).
"""

import json
import hashlib
import os
import fitz
from PIL import Image, ImageDraw, ImageFont

PDF_PATH = "/Users/kivinwang/Downloads/2026 PJ 型錄-內頁（final draft) (2).pdf"
EXPECTED_SHA256 = "53da4ae32d4a1edebf8a01b1bde667b629071cb707163e09cc6beebe228400f5"

def freeze_raw_texts():
    doc = fitz.open(PDF_PATH)
    os.makedirs("reports", exist_ok=True)
    
    hashes = json.load(open("reports/frozen_raw_text_hashes.json", "r", encoding="utf-8")) if os.path.exists("reports/frozen_raw_text_hashes.json") else {}
    
    for pno in [58, 59, 60]:
        p = doc[pno]
        p_num = pno + 1
        out_path = f"reports/raw_pdf_text_p{p_num}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"=== PHYSICAL PAGE {p_num} (INDEX {pno}) ===\n")
            f.write(f"PAGE RECT: width={p.rect.width}, height={p.rect.height}\n\n")
            f.write("--- FULL GET_TEXT() ---\n")
            f.write(p.get_text())
            f.write("\n\n--- TEXT BLOCKS (BBOXES) ---\n")
            for b in p.get_text("blocks"):
                bbox_str = f"[{b[0]:.2f}, {b[1]:.2f}, {b[2]:.2f}, {b[3]:.2f}]"
                text_clean = b[4].replace("\n", " \\n ")
                f.write(f"Block {b[5]} (type {b[6]}): bbox={bbox_str} -> {text_clean}\n")
            f.write("\n--- IMAGE INFO ---\n")
            for img in p.get_images():
                f.write(f"Image xref={img[0]}, smask={img[1]}, width={img[2]}, height={img[3]}, bpc={img[4]}, colorspace={img[5]}, name={img[7]}, type={img[8]}\n")
        
        with open(out_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        hashes[out_path] = {
            "sha256": h,
            "byte_size": os.path.getsize(out_path)
        }
        print(f"Wrote and hashed {out_path}: {h}")
        
    with open("reports/frozen_raw_text_hashes.json", "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)
    print("Updated reports/frozen_raw_text_hashes.json")

def extract_images():
    doc = fitz.open(PDF_PATH)
    os.makedirs("reports/dining_batch7_draft_images", exist_ok=True)
    os.makedirs("reports/dining_batch7_evidence/regions", exist_ok=True)
    
    # Save full page spreads
    for pno in [58, 59, 60]:
        p = doc[pno]
        pix = p.get_pixmap(dpi=150)
        pix.save(f"reports/dining_batch7_evidence/page_{pno+1}_spread.jpg")
        
    # Crop visual regions
    regions = [
        ("p59_d113_left_2240_2800black_gray", 58, fitz.Rect(0, 0, 850, 680)),
        ("p59_d114_right_2250_2800black_gray", 58, fitz.Rect(850, 0, 1700.79, 680)),
        ("p60_d115_left_3101t_2800wh_chrome", 59, fitz.Rect(0, 0, 850, 680)),
        ("p60_d116_right_3112t_3102t_2800wh_chrome", 59, fitz.Rect(850, 0, 1700.79, 680)),
        ("p61_d117_left_3103t_2800wh_gold", 60, fitz.Rect(0, 0, 850, 680)),
        ("p61_d118_right_3114t_3104t_2800wh_gold", 60, fitz.Rect(850, 0, 1700.79, 680)),
    ]
    for name, pno, clip in regions:
        p = doc[pno]
        pix = p.get_pixmap(clip=clip, dpi=150)
        pix.save(f"reports/dining_batch7_evidence/regions/{name}.jpg")
        
    # Extract draft images for SKUs
    sku_crops = [
        ("draft-2240.jpg", 58, fitz.Rect(33, 0, 851, 562)),
        ("draft-2800black-gray.jpg", 58, fitz.Rect(33, 0, 851, 562)),
        ("draft-2250.jpg", 58, fitz.Rect(849, 0, 1665, 562)),
        ("draft-3101t.jpg", 59, fitz.Rect(33, 0, 851, 562)),
        ("draft-2800wh-chrome.jpg", 59, fitz.Rect(33, 0, 851, 562)),
        ("draft-3112t.jpg", 59, fitz.Rect(848, 0, 1665, 562)),
        ("draft-3103t.jpg", 60, fitz.Rect(33, 0, 851, 562)),
        ("draft-2800wh-gold.jpg", 60, fitz.Rect(33, 0, 851, 562)),
        ("draft-3114t.jpg", 60, fitz.Rect(849, 0, 1665, 562)),
        ("draft-3104t.jpg", 60, fitz.Rect(849, 0, 1665, 562)),
    ]
    for out_name, pno, clip in sku_crops:
        p = doc[pno]
        pix = p.get_pixmap(clip=clip, dpi=150)
        out_path = f"reports/dining_batch7_draft_images/{out_name}"
        pix.save(out_path)
        print(f"Saved {out_path}")

def build_manifest():
    manifest = [
        # 1. 2240 (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "2240",
            "sku": "2240",
            "component_skus": ["2240"],
            "product_identity": "one complete sintered stone dining table",
            "components_verified": True,
            "pdf_physical_page": 59,
            "first_seen": {
                "physical_page": 59,
                "print_page": "DINETTE 113",
                "section": "DINETTE 113 left"
            },
            "occurrences": 1,
            "evidence_pages": [59],
            "source_text_regions": [
                {
                    "page": 59,
                    "print_page": "DINETTE 113",
                    "heading_region": [68.2, 523.3, 235.0, 544.8],
                    "verbatim_heading": "2240/2800BLACK-GRAY",
                    "region": [68.1, 578.5, 408.2, 595.1],
                    "verbatim_text": "2240  |  SINTERED STONE DINING TABLE   47\"W x 28\"D x 30\"H"
                }
            ],
            "raw_heading_text": "2240/2800BLACK-GRAY",
            "raw_model_text": "2240",
            "raw_color_text": "SINTERED STONE DINING TABLE",
            "resolved_color": "SINTERED STONE",
            "raw_dimensions_text": "47\"W x 28\"D x 30\"H",
            "resolved_dimensions": "47\"W x 28\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$75.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [470.0, 701.3, 583.5, 731.6],
                "exact_row_text": "2240 Glass Dining Table $75.00",
                "previous_row_text": "Page 113",
                "next_row_text": "2800BLACK-GRAY Chair $30.00",
                "component_skus": ["2240"],
                "resolved_price": "$75.00",
                "price": "$75.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-2240.jpg",
            "image_xref": 1394,
            "image_pixel_size": "819x564",
            "image_sha256": "36ef9149495393437171e54911ea18770fe4596350e18fc091f868d4a65aee17",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["2800BLACK-GRAY"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 59, printed page DINETTE 113 left.",
            "visual_review_notes": "Cropped from P59 left scene. Overlaps with 2800BLACK-GRAY chairs.",
            "interpretation_notes": "Sintered stone dining table 2240 (47x28x30H). Price list lists $75.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "2240 47英寸岩板餐桌",
            "candidate_title_en": "2240 47\" Sintered Stone Dining Table"
        },
        # 2. 2800BLACK-GRAY (Dining Chair)
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800BLACK-GRAY",
            "sku": "2800BLACK-GRAY",
            "component_skus": ["2800BLACK-GRAY"],
            "product_identity": "dining chair",
            "components_verified": True,
            "pdf_physical_page": 59,
            "first_seen": {
                "physical_page": 59,
                "print_page": "DINETTE 113",
                "section": "DINETTE 113 left"
            },
            "occurrences": 2,
            "evidence_pages": [59],
            "source_text_regions": [
                {
                    "page": 59,
                    "print_page": "DINETTE 113",
                    "heading_region": [68.2, 523.3, 235.0, 544.8],
                    "verbatim_heading": "2240/2800BLACK-GRAY",
                    "region": [68.1, 599.5, 414.1, 637.1],
                    "verbatim_text": "2800BLACK-GRAY | DINING CHAIR(WELDED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 59,
                    "print_page": "DINETTE 114",
                    "heading_region": [1445.5, 523.3, 1612.3, 544.8],
                    "verbatim_heading": "2250/2800BLACK-GRAY",
                    "region": [1263.0, 599.5, 1612.4, 637.1],
                    "verbatim_text": "2800BLACK-GRAY |  DINING CHAIR(WELDED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "2240/2800BLACK-GRAY",
            "raw_model_text": "2800BLACK-GRAY",
            "raw_color_text": "BLACK-GRAY",
            "resolved_color": "BLACK-GRAY",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$30.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [470.0, 737.3, 583.5, 770.0],
                "exact_row_text": "2800BLACK-GRAY Chair $30.00",
                "previous_row_text": "2240 Glass Dining Table $75.00",
                "next_row_text": "Page 114",
                "component_skus": ["2800BLACK-GRAY"],
                "resolved_price": "$30.00",
                "price": "$30.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $30.00 without unit"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-2800black-gray.jpg",
            "image_xref": 1394,
            "image_pixel_size": "819x564",
            "image_sha256": "36ef9149495393437171e54911ea18770fe4596350e18fc091f868d4a65aee17",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["2240", "2250"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 59, printed pages DINETTE 113 and DINETTE 114.",
            "visual_review_notes": "Cropped from P59 scene. Overlaps with 2240 table.",
            "interpretation_notes": "Dining chair (welded) 2800BLACK-GRAY. PACK: 4/1 CARTON. Price list lists $30.00 without specifying unit. Marked price_unit_status: unverified and publish: false.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "2800BLACK-GRAY 黑灰色焊接餐椅",
            "candidate_title_en": "2800BLACK-GRAY Welded Dining Chair"
        },
        # 3. 2250 (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "2250",
            "sku": "2250",
            "component_skus": ["2250"],
            "product_identity": "one complete dining table",
            "components_verified": True,
            "pdf_physical_page": 59,
            "first_seen": {
                "physical_page": 59,
                "print_page": "DINETTE 114",
                "section": "DINETTE 114 right"
            },
            "occurrences": 1,
            "evidence_pages": [59],
            "source_text_regions": [
                {
                    "page": 59,
                    "print_page": "DINETTE 114",
                    "heading_region": [1445.5, 523.3, 1612.3, 544.8],
                    "verbatim_heading": "2250/2800BLACK-GRAY",
                    "region": [1380.2, 578.5, 1615.7, 595.1],
                    "verbatim_text": "2250  |   DINING TABLE   47\"W x 28\"D x 30\"H"
                }
            ],
            "raw_heading_text": "2250/2800BLACK-GRAY",
            "raw_model_text": "2250",
            "raw_color_text": "DINING TABLE",
            "resolved_color": None,
            "raw_dimensions_text": "47\"W x 28\"D x 30\"H",
            "resolved_dimensions": "47\"W x 28\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$59.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [780.5, 67.3, 885.2, 97.6],
                "exact_row_text": "2250 Glass Dining Table $59.00",
                "previous_row_text": "Page 114",
                "next_row_text": "2800BLACK-GRAY Chair (Weled) $30.00",
                "component_skus": ["2250"],
                "resolved_price": "$59.00",
                "price": "$59.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-2250.jpg",
            "image_xref": 1400,
            "image_pixel_size": "817x563",
            "image_sha256": "479427b3b7e7195c80a221f757e7eb343949f69b82141c2c31e9c20a84f3df9b",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["2800BLACK-GRAY"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 59, printed page DINETTE 114 right.",
            "visual_review_notes": "Cropped from P59 right scene. Overlaps with 2800BLACK-GRAY chairs.",
            "interpretation_notes": "Dining table 2250 (47x28x30H). Price list lists $59.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "2250 47英寸餐桌",
            "candidate_title_en": "2250 47\" Dining Table"
        },
        # 4. 3101T (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "3101T",
            "sku": "3101T",
            "component_skus": ["3101T"],
            "product_identity": "one complete round glass dining table",
            "components_verified": True,
            "pdf_physical_page": 60,
            "first_seen": {
                "physical_page": 60,
                "print_page": "DINETTE 115",
                "section": "DINETTE 115 left"
            },
            "occurrences": 1,
            "evidence_pages": [60],
            "source_text_regions": [
                {
                    "page": 60,
                    "print_page": "DINETTE 115",
                    "heading_region": [69.5, 518.2, 250.3, 539.8],
                    "verbatim_heading": "3101T/2800WH-CHROME",
                    "region": [72.3, 578.5, 343.4, 595.1],
                    "verbatim_text": "3101T  |  GLASS DINING TABLE    DIA  43\" x 30\"H"
                }
            ],
            "raw_heading_text": "3101T/2800WH-CHROME",
            "raw_model_text": "3101T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": None,
            "raw_dimensions_text": "DIA 43\" x 30\"H",
            "resolved_dimensions": "DIA 43\" x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$129.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [780.5, 198.2, 885.2, 228.5],
                "exact_row_text": "3101T Glass Dining Table $129.00",
                "previous_row_text": "Page 115",
                "next_row_text": "2800WH-CHROME Chair (Weled) $35.00",
                "component_skus": ["3101T"],
                "resolved_price": "$129.00",
                "price": "$129.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-3101t.jpg",
            "image_xref": 1414,
            "image_pixel_size": "818x563",
            "image_sha256": "3cb4ee27027db944747eb68b35e297825d1e2e92ecbe354ba5f553a948c26bb5",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["2800WH-CHROME"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 60, printed page DINETTE 115 left.",
            "visual_review_notes": "Cropped from P60 left scene. Overlaps with 2800WH-CHROME chairs.",
            "interpretation_notes": "Round glass dining table 3101T (DIA 43x30H). Price list lists $129.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "3101T 43英寸圆形玻璃餐桌",
            "candidate_title_en": "3101T 43\" Round Glass Dining Table"
        },
        # 5. 2800WH-CHROME (Dining Chair)
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800WH-CHROME",
            "sku": "2800WH-CHROME",
            "component_skus": ["2800WH-CHROME"],
            "product_identity": "dining chair",
            "components_verified": True,
            "pdf_physical_page": 60,
            "first_seen": {
                "physical_page": 60,
                "print_page": "DINETTE 115",
                "section": "DINETTE 115 left"
            },
            "occurrences": 2,
            "evidence_pages": [60],
            "source_text_regions": [
                {
                    "page": 60,
                    "print_page": "DINETTE 115",
                    "heading_region": [69.5, 518.2, 250.3, 539.8],
                    "verbatim_heading": "3101T/2800WH-CHROME",
                    "region": [72.3, 599.5, 381.7, 637.1],
                    "verbatim_text": "2800WH-CHROME  |  CHAIR (WELED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 60,
                    "print_page": "DINETTE 116",
                    "heading_region": [1448.3, 510.4, 1629.0, 551.2],
                    "verbatim_heading": "3112T/2800WH-CHROME\n3102T/2800WH-CHROME",
                    "region": [1367.0, 620.5, 1631.8, 658.1],
                    "verbatim_text": "2800WH-CHROME  |  CHAIR    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "3101T/2800WH-CHROME",
            "raw_model_text": "2800WH-CHROME",
            "raw_color_text": "WH-CHROME",
            "resolved_color": "WHITE / CHROME",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$35.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [780.7, 234.2, 885.2, 266.9],
                "exact_row_text": "2800WH-CHROME Chair (Weled) $35.00",
                "previous_row_text": "3101T Glass Dining Table $129.00",
                "next_row_text": "Page 116",
                "component_skus": ["2800WH-CHROME"],
                "resolved_price": "$35.00",
                "price": "$35.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $35.00 without unit"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-2800wh-chrome.jpg",
            "image_xref": 1414,
            "image_pixel_size": "818x563",
            "image_sha256": "3cb4ee27027db944747eb68b35e297825d1e2e92ecbe354ba5f553a948c26bb5",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["3101T", "3112T", "3102T"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 60, printed pages DINETTE 115 and DINETTE 116.",
            "visual_review_notes": "Cropped from P60 scene. Overlaps with 3101T table.",
            "interpretation_notes": "Dining chair (welded) 2800WH-CHROME. PACK: 4/1 CARTON. Price list lists $35.00 without specifying unit. Marked price_unit_status: unverified and publish: false.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "2800WH-CHROME 白色铬架焊接餐椅",
            "candidate_title_en": "2800WH-CHROME White Chrome Frame Welded Dining Chair"
        },
        # 6. 3112T (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "3112T",
            "sku": "3112T",
            "component_skus": ["3112T"],
            "product_identity": "one complete rectangular glass dining table",
            "components_verified": True,
            "pdf_physical_page": 60,
            "first_seen": {
                "physical_page": 60,
                "print_page": "DINETTE 116",
                "section": "DINETTE 116 right"
            },
            "occurrences": 1,
            "evidence_pages": [60],
            "source_text_regions": [
                {
                    "page": 60,
                    "print_page": "DINETTE 116",
                    "heading_region": [1448.3, 510.4, 1629.0, 551.2],
                    "verbatim_heading": "3112T/2800WH-CHROME\n3102T/2800WH-CHROME",
                    "region": [1351.4, 578.5, 1631.8, 595.1],
                    "verbatim_text": "3112T  |  GLASS DINING TABLE    30\"W x 48\"D x 30\"H"
                }
            ],
            "raw_heading_text": "3112T/2800WH-CHROME",
            "raw_model_text": "3112T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": None,
            "raw_dimensions_text": "30\"W x 48\"D x 30\"H",
            "resolved_dimensions": "30\"W x 48\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$119.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [779.6, 319.2, 885.4, 349.6],
                "exact_row_text": "3112T(30” x 48”) Glass Dining Table $119.00",
                "previous_row_text": "Page 116",
                "next_row_text": "3102T (36” x 60” ) Glass Dining Table $149.00",
                "component_skus": ["3112T"],
                "resolved_price": "$119.00",
                "price": "$119.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-3112t.jpg",
            "image_xref": 1415,
            "image_pixel_size": "817x564",
            "image_sha256": "4b6c310461ce7b43f9a9415449755ebaa873130dcfeb81ef77f12a32ea07c132",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["3102T", "2800WH-CHROME"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 60, printed page DINETTE 116 right.",
            "visual_review_notes": "Cropped from P60 right scene. Shared lifestyle scene with 3102T and 2800WH-CHROME.",
            "interpretation_notes": "Rectangular glass dining table 3112T (30x48x30H). Price list lists $119.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "3112T 48英寸长方形玻璃餐桌",
            "candidate_title_en": "3112T 48\" Rectangular Glass Dining Table"
        },
        # 7. 3103T (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "3103T",
            "sku": "3103T",
            "component_skus": ["3103T"],
            "product_identity": "one complete round glass dining table with gold frame",
            "components_verified": True,
            "pdf_physical_page": 61,
            "first_seen": {
                "physical_page": 61,
                "print_page": "DINETTE 117",
                "section": "DINETTE 117 left"
            },
            "occurrences": 1,
            "evidence_pages": [61],
            "source_text_regions": [
                {
                    "page": 61,
                    "print_page": "DINETTE 117",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800WH-GOLD\n3114T/2800WH-GOLD\n3104T/2800WH-GOLD",
                    "region": [72.3, 578.5, 343.4, 595.1],
                    "verbatim_text": "3103T  |  GLASS DINING TABLE    DIA  43\" x 30\"H"
                }
            ],
            "raw_heading_text": "3103T/2800WH-GOLD",
            "raw_model_text": "3103T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": "GOLD",
            "raw_dimensions_text": "DIA 43\" x 30\"H",
            "resolved_dimensions": "DIA 43\" x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$139.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [784.3, 444.0, 889.0, 474.3],
                "exact_row_text": "3103T Glass Dining Table $139.00",
                "previous_row_text": "Page 117",
                "next_row_text": "2800WH-GOLD Chair (Weled) $40.00",
                "component_skus": ["3103T"],
                "resolved_price": "$139.00",
                "price": "$139.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-3103t.jpg",
            "image_xref": 1429,
            "image_pixel_size": "819x564",
            "image_sha256": "278aaef51d02c46fbe85764724b077c44957e8412fc6814c0a520e54d6d6ce3b",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["2800WH-GOLD"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 61, printed page DINETTE 117 left.",
            "visual_review_notes": "Cropped from P61 left scene. Overlaps with 2800WH-GOLD chairs.",
            "interpretation_notes": "Round glass dining table 3103T (DIA 43x30H) with gold legs. Price list lists $139.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "3103T 43英寸圆形金色玻璃餐桌",
            "candidate_title_en": "3103T 43\" Round Gold Glass Dining Table"
        },
        # 8. 2800WH-GOLD (Dining Chair)
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800WH-GOLD",
            "sku": "2800WH-GOLD",
            "component_skus": ["2800WH-GOLD"],
            "product_identity": "dining chair",
            "components_verified": True,
            "pdf_physical_page": 61,
            "first_seen": {
                "physical_page": 61,
                "print_page": "DINETTE 117",
                "section": "DINETTE 117 left"
            },
            "occurrences": 2,
            "evidence_pages": [61],
            "source_text_regions": [
                {
                    "page": 61,
                    "print_page": "DINETTE 117",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800WH-GOLD\n3114T/2800WH-GOLD\n3104T/2800WH-GOLD",
                    "region": [72.3, 599.5, 364.1, 637.1],
                    "verbatim_text": "2800WH-GOLD  |  CHAIR (WELED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 61,
                    "print_page": "DINETTE 118",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800WH-GOLD\n3114T/2800WH-GOLD\n3104T/2800WH-GOLD",
                    "region": [1381.7, 624.5, 1629.0, 662.1],
                    "verbatim_text": "2800WH-GOLD  |  CHAIR    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "3103T/2800WH-GOLD",
            "raw_model_text": "2800WH-GOLD",
            "raw_color_text": "WH-GOLD",
            "resolved_color": "WHITE / GOLD",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$40.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [784.5, 480.0, 889.0, 512.6],
                "exact_row_text": "2800WH-GOLD Chair (Weled) $40.00",
                "previous_row_text": "3103T Glass Dining Table $139.00",
                "next_row_text": "Page 118",
                "component_skus": ["2800WH-GOLD"],
                "resolved_price": "$40.00",
                "price": "$40.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $40.00 without unit"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-2800wh-gold.jpg",
            "image_xref": 1429,
            "image_pixel_size": "819x564",
            "image_sha256": "278aaef51d02c46fbe85764724b077c44957e8412fc6814c0a520e54d6d6ce3b",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["3103T", "3114T", "3104T"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 61, printed pages DINETTE 117 and DINETTE 118.",
            "visual_review_notes": "Cropped from P61 scene. Overlaps with 3103T table.",
            "interpretation_notes": "Dining chair (welded) 2800WH-GOLD. PACK: 4/1 CARTON. Price list lists $40.00 without specifying unit. Marked price_unit_status: unverified and publish: false.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "2800WH-GOLD 白色金架焊接餐椅",
            "candidate_title_en": "2800WH-GOLD White Gold Frame Welded Dining Chair"
        },
        # 9. 3114T (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "3114T",
            "sku": "3114T",
            "component_skus": ["3114T"],
            "product_identity": "one complete rectangular glass dining table with gold frame",
            "components_verified": True,
            "pdf_physical_page": 61,
            "first_seen": {
                "physical_page": 61,
                "print_page": "DINETTE 118",
                "section": "DINETTE 118 right"
            },
            "occurrences": 1,
            "evidence_pages": [61],
            "source_text_regions": [
                {
                    "page": 61,
                    "print_page": "DINETTE 118",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800WH-GOLD\n3114T/2800WH-GOLD\n3104T/2800WH-GOLD",
                    "region": [1348.5, 582.5, 1629.0, 599.1],
                    "verbatim_text": "3114T  |  GLASS DINING TABLE    30\"W x 48\"D x 30\"H"
                }
            ],
            "raw_heading_text": "3114T/2800WH-GOLD",
            "raw_model_text": "3114T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": "GOLD",
            "raw_dimensions_text": "30\"W x 48\"D x 30\"H",
            "resolved_dimensions": "30\"W x 48\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$129.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [781.1, 565.0, 888.9, 594.7],
                "exact_row_text": "Glass Dining Table 3114T(30” x 48”) $129.00",
                "previous_row_text": "Page 118",
                "next_row_text": "3104T(36” x 60”) Glass Dining Table $159.00",
                "component_skus": ["3114T"],
                "resolved_price": "$129.00",
                "price": "$129.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-3114t.jpg",
            "image_xref": 1430,
            "image_pixel_size": "817x564",
            "image_sha256": "4b971d6092d6e32d3e120f4d36ef5571618a80486c12365440d99596b63ea534",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["3104T", "2800WH-GOLD"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 61, printed page DINETTE 118 right.",
            "visual_review_notes": "Cropped from P61 right scene. Overlaps with 3104T and 2800WH-GOLD.",
            "interpretation_notes": "Rectangular glass dining table 3114T (30x48x30H) with gold legs. Price list lists $129.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "3114T 48英寸长方形金色玻璃餐桌",
            "candidate_title_en": "3114T 48\" Rectangular Gold Glass Dining Table"
        },
        # 10. 3104T (Dining Table)
        {
            "record_type": "canonical_product",
            "canonical_sku": "3104T",
            "sku": "3104T",
            "component_skus": ["3104T"],
            "product_identity": "one complete rectangular glass dining table with gold frame",
            "components_verified": True,
            "pdf_physical_page": 61,
            "first_seen": {
                "physical_page": 61,
                "print_page": "DINETTE 118",
                "section": "DINETTE 118 right"
            },
            "occurrences": 1,
            "evidence_pages": [61],
            "source_text_regions": [
                {
                    "page": 61,
                    "print_page": "DINETTE 118",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800WH-GOLD\n3114T/2800WH-GOLD\n3104T/2800WH-GOLD",
                    "region": [1348.5, 603.5, 1625.7, 620.1],
                    "verbatim_text": "3104T  |  GLASS DINING TABLE   36\" W x 60\"D x 30\"H"
                }
            ],
            "raw_heading_text": "3104T/2800WH-GOLD",
            "raw_model_text": "3104T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": "GOLD",
            "raw_dimensions_text": "36\" W x 60\"D x 30\"H",
            "resolved_dimensions": "36\"W x 60\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$159.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [781.1, 593.7, 887.6, 623.5],
                "exact_row_text": "3104T(36” x 60”) Glass Dining Table $159.00",
                "previous_row_text": "Glass Dining Table 3114T(30” x 48”) $129.00",
                "next_row_text": "2800WH-GOLD Chair (Weled) $40.00",
                "component_skus": ["3104T"],
                "resolved_price": "$159.00",
                "price": "$159.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch7_draft_images/draft-3104t.jpg",
            "image_xref": 1430,
            "image_pixel_size": "817x564",
            "image_sha256": "4b971d6092d6e32d3e120f4d36ef5571618a80486c12365440d99596b63ea534",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "shared_layout_with_other_products": True,
            "shared_products_in_scene": ["3114T", "2800WH-GOLD"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 61, printed page DINETTE 118 right.",
            "visual_review_notes": "Cropped from P61 right scene. Overlaps with 3114T and 2800WH-GOLD.",
            "interpretation_notes": "Rectangular glass dining table 3104T (36x60x30H) with gold legs. Price list lists $159.00.",
            "conflict_status": "none",
            "conflict_notes": "None.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "source_verified": True,
            "human_reviewed": True,
            "publish": False,
            "review_result": "rejected_for_publication",
            "rejection_code": ["NO_CLEAN_STANDALONE_IMAGE"],
            "rejection_reason": "PDF only provides a lifestyle scene containing other products; it cannot satisfy the one-SKU-one-product image rule.",
            "candidate_title_zh": "3104T 60英寸长方形金色玻璃餐桌",
            "candidate_title_en": "3104T 60\" Rectangular Gold Glass Dining Table"
        },
        # Occurrences:
        # 11. 3102T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3102T",
            "sku": "3102T",
            "product_identity": "one complete glass dining table",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 60,
                    "print_page": "DINETTE 116",
                    "section": "DINETTE 116 right",
                    "raw_heading_text": "3112T/2800WH-CHROME\n3102T/2800WH-CHROME",
                    "raw_dimensions_text": "36\"W x 60\"D x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3102T  |  GLASS DINING TABLE    36\"W x 60\"D x 30\"H",
                    "scene_chairs": "2800WH-CHROME",
                    "image_xref": 1415
                }
            ],
            "notes": "Occurrence #4 of 3102T. P60 DINETTE 116 right repeated table with 2800WH-CHROME chairs. Canonical record in Batch 6 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        }
    ]
    
    out_path = "reports/manifest_v2_dining_batch7.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path} ({len(manifest)} items: 10 canonical, 1 occurrence)")

def build_contact_sheet():
    regions = [
        ("reports/dining_batch7_evidence/regions/p59_d113_left_2240_2800black_gray.jpg", "P59 / DINETTE 113 Left", "2240 / 2800BLACK-GRAY", "Table: 2240 ($75.00) | Chair: 2800BLACK-GRAY ($30.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch7_evidence/regions/p59_d114_right_2250_2800black_gray.jpg", "P59 / DINETTE 114 Right", "2250 / 2800BLACK-GRAY", "Table: 2250 ($59.00) | Chair: 2800BLACK-GRAY ($30.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch7_evidence/regions/p60_d115_left_3101t_2800wh_chrome.jpg", "P60 / DINETTE 115 Left", "3101T / 2800WH-CHROME", "Table: 3101T ($129.00) | Chair: 2800WH-CHROME ($35.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch7_evidence/regions/p60_d116_right_3112t_3102t_2800wh_chrome.jpg", "P60 / DINETTE 116 Right", "3112T / 3102T / 2800WH-CHROME", "Tables: 3112T ($119.00), 3102T ($149.00) | Chair: 2800WH-CHROME ($35.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch7_evidence/regions/p61_d117_left_3103t_2800wh_gold.jpg", "P61 / DINETTE 117 Left", "3103T / 2800WH-GOLD", "Table: 3103T ($139.00) | Chair: 2800WH-GOLD ($40.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch7_evidence/regions/p61_d118_right_3114t_3104t_2800wh_gold.jpg", "P61 / DINETTE 118 Right", "3114T / 3104T / 2800WH-GOLD", "Tables: 3114T ($129.00), 3104T ($159.00) | Chair: 2800WH-GOLD ($40.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
    ]
    
    # 2 columns x 3 rows grid
    cell_w, cell_h = 750, 560
    sheet_w, sheet_h = cell_w * 2 + 60, cell_h * 3 + 120
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 248))
    draw = ImageDraw.Draw(sheet)
    
    # Header
    draw.rectangle([(0, 0), (sheet_w, 60)], fill=(30, 35, 45))
    draw.text((30, 18), "DINING BATCH 7 AUDIT CONTACT SHEET (P59-P61 / DINETTE 113-118)", fill=(255, 255, 255))
    
    for idx, (img_p, page_txt, heading_txt, desc_txt) in enumerate(regions):
        col = idx % 2
        row = idx // 2
        x0 = 30 + col * (cell_w + 20)
        y0 = 80 + row * (cell_h + 20)
        
        draw.rectangle([(x0, y0), (x0 + cell_w, y0 + cell_h)], fill=(255, 255, 255), outline=(200, 205, 215), width=2)
        
        if os.path.exists(img_p):
            im = Image.open(img_p)
            im.thumbnail((cell_w - 20, cell_h - 130))
            sheet.paste(im, (x0 + 10, y0 + 10))
            
        # Draw red border on crop to indicate multi-product lifestyle scene
        draw.rectangle([(x0 + 10, y0 + 10), (x0 + cell_w - 10, y0 + cell_h - 110)], outline=(220, 50, 50), width=2)
        
        # Text details
        draw.text((x0 + 15, y0 + cell_h - 95), f"{page_txt} | Heading: {heading_txt}", fill=(20, 20, 20))
        draw.text((x0 + 15, y0 + cell_h - 65), desc_txt, fill=(80, 80, 80))
        
    sheet.save("reports/dining_batch7_contact_sheet.jpg", quality=90)
    print("Wrote reports/dining_batch7_contact_sheet.jpg")

if __name__ == "__main__":
    freeze_raw_texts()
    extract_images()
    build_manifest()
    build_contact_sheet()
