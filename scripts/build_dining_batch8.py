#!/usr/bin/env python3
"""
scripts/build_dining_batch8.py
Extracts raw text, builds Batch 8 Manifest, generates contact sheet,
and updates frozen text hashes for Dining Batch 8 (P62-P64 / DINETTE 119-124).
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
    
    for pno in [61, 62, 63]:
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
                xref = img[0]
                base_img = doc.extract_image(xref)
                img_bytes = base_img["image"]
                img_sha = hashlib.sha256(img_bytes).hexdigest()
                rects = p.get_image_rects(xref)
                bbox_str = f"[{rects[0].x0:.2f}, {rects[0].y0:.2f}, {rects[0].x1:.2f}, {rects[0].y1:.2f}]" if rects else "[]"
                f.write(f"Image xref={xref}, bbox={bbox_str}, width={base_img['width']}, height={base_img['height']}, ext={base_img['ext']}, sha256={img_sha}\n")
        
        with open(out_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        hashes[out_path] = {
            "sha256": h,
            "byte_size": os.path.getsize(out_path)
        }
        print(f"Wrote and hashed {out_path}: {h}")
        
    with open("reports/frozen_raw_text_hashes.json", "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)
    print(f"Updated reports/frozen_raw_text_hashes.json (total {len(hashes)} files)")

def extract_images():
    doc = fitz.open(PDF_PATH)
    os.makedirs("reports/dining_batch8_draft_images", exist_ok=True)
    os.makedirs("reports/dining_batch8_evidence/regions", exist_ok=True)
    
    # Save full page spreads
    for pno in [61, 62, 63]:
        p = doc[pno]
        pix = p.get_pixmap(dpi=150)
        pix.save(f"reports/dining_batch8_evidence/page_{pno+1}_spread.jpg")
        
    # Crop visual regions
    regions = [
        ("p62_d119_left_3101t_2800bk_chrome", 61, fitz.Rect(0, 0, 850, 680)),
        ("p62_d120_right_3112t_3102t_2800bk_chrome", 61, fitz.Rect(850, 0, 1700.79, 680)),
        ("p63_d121_left_3103t_2800bk_gold", 62, fitz.Rect(0, 0, 850, 680)),
        ("p63_d122_right_3114t_3104t_2800bk_gold", 62, fitz.Rect(850, 0, 1700.79, 680)),
        ("p64_d123_left_3105t_2800bk_gray", 63, fitz.Rect(0, 0, 850, 680)),
        ("p64_d124_right_3106t_2800bk_gray", 63, fitz.Rect(850, 0, 1700.79, 680)),
    ]
    for name, pno, clip in regions:
        p = doc[pno]
        pix = p.get_pixmap(clip=clip, dpi=150)
        pix.save(f"reports/dining_batch8_evidence/regions/{name}.jpg")
        
    # Extract draft images for SKUs
    sku_crops = [
        ("draft-2800bk-chrome.jpg", 61, fitz.Rect(33, 0, 851, 562)),
        ("draft-2800bk-gold.jpg", 62, fitz.Rect(33, 0, 851, 562)),
        ("draft-3105t.jpg", 63, fitz.Rect(33, 0, 851, 562)),
        ("draft-2800bk-gray.jpg", 63, fitz.Rect(33, 0, 851, 562)),
        ("draft-3106t.jpg", 63, fitz.Rect(847, 0, 1665, 562)),
    ]
    for out_name, pno, clip in sku_crops:
        p = doc[pno]
        pix = p.get_pixmap(clip=clip, dpi=150)
        out_path = f"reports/dining_batch8_draft_images/{out_name}"
        pix.save(out_path)
        print(f"Saved {out_path}")

def build_manifest():
    manifest = [
        # =========================================================================
        # 1. 2800BK-CHROME (Canonical Product - Dining Chair)
        # =========================================================================
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800BK-CHROME",
            "sku": "2800BK-CHROME",
            "component_skus": ["2800BK-CHROME"],
            "product_identity": "dining chair with chrome frame",
            "components_verified": True,
            "pdf_physical_page": 62,
            "first_seen": {
                "physical_page": 62,
                "print_page": "DINETTE 119",
                "section": "DINETTE 119 left"
            },
            "occurrences": 2,
            "evidence_pages": [62],
            "source_text_regions": [
                {
                    "page": 62,
                    "print_page": "DINETTE 119",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3101T/2800BK-CHROME\n3112T/2800BK-CHROME\n3102T/2800BK-CHROME",
                    "region": [72.3, 599.5, 378.1, 637.1],
                    "verbatim_text": "2800BK-CHROME  |  CHAIR (WELED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 62,
                    "print_page": "DINETTE 120",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3101T/2800BK-CHROME\n3112T/2800BK-CHROME\n3102T/2800BK-CHROME",
                    "region": [1367.8, 624.5, 1629.0, 662.1],
                    "verbatim_text": "2800BK-CHROME  |  CHAIR    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "3101T/2800BK-CHROME",
            "raw_model_text": "2800BK-CHROME",
            "raw_color_text": "BK-CHROME",
            "resolved_color": "BLACK / CHROME",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$35.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [780.9, 737.3, 885.4, 770.0],
                "exact_row_text": "2800BK-CHROME Chair (Weled) $35.00",
                "previous_row_text": "3101T Glass Dining Table $129.00",
                "next_row_text": "Page 120",
                "component_skus": ["2800BK-CHROME"],
                "resolved_price": "$35.00",
                "price": "$35.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $35.00 without unit"
            },
            "output_image": "reports/dining_batch8_draft_images/draft-2800bk-chrome.jpg",
            "image_xref": 1444,
            "image_pixel_size": "819x563",
            "image_sha256": "981410724da49a946aa53837f0541f5c9c9dc774a372d726e9ffb93995b2c262",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "ordinary_scene_props": False,
            "catalog_product_overlap": True,
            "shared_layout_with_other_products": True,
            "shared_scene_for_multiple_skus": True,
            "displayed_model_uncertain": False,
            "evidence_only": True,
            "eligible_as_product_image": False,
            "shared_products_in_scene": ["3101T", "3112T", "3102T"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 62, printed pages DINETTE 119 and DINETTE 120.",
            "visual_review_notes": "Cropped from P62 scene. Overlaps with 3101T table in lifestyle scene.",
            "interpretation_notes": "Dining chair (welded) 2800BK-CHROME. PACK: 4/1 CARTON. Price list lists $35.00 without unit. Marked price_unit_status: unverified and publish: false.",
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
            "candidate_title_zh": "2800BK-CHROME 黑色铬架焊接餐椅",
            "candidate_title_en": "2800BK-CHROME Black Chrome Frame Welded Dining Chair"
        },
        
        # =========================================================================
        # 2. 2800BK-GOLD (Canonical Product - Dining Chair)
        # =========================================================================
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800BK-GOLD",
            "sku": "2800BK-GOLD",
            "component_skus": ["2800BK-GOLD"],
            "product_identity": "dining chair with gold frame",
            "components_verified": True,
            "pdf_physical_page": 63,
            "first_seen": {
                "physical_page": 63,
                "print_page": "DINETTE 121",
                "section": "DINETTE 121 left"
            },
            "occurrences": 2,
            "evidence_pages": [63],
            "source_text_regions": [
                {
                    "page": 63,
                    "print_page": "DINETTE 121",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800BK-GOLD\n3114T/2800BK-GOLD\n3104T/2800BK-GOLD",
                    "region": [72.3, 599.5, 360.5, 637.1],
                    "verbatim_text": "2800BK-GOLD  |  CHAIR (WELED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 63,
                    "print_page": "DINETTE 122",
                    "heading_region": [69.5, 505.9, 1626.2, 546.7],
                    "verbatim_heading": "3103T/2800BK-GOLD\n3114T/2800BK-GOLD\n3104T/2800BK-GOLD",
                    "region": [1385.4, 624.5, 1629.0, 662.1],
                    "verbatim_text": "2800BK-GOLD  |  CHAIR    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "3103T/2800BK-GOLD",
            "raw_model_text": "2800BK-GOLD",
            "raw_color_text": "BK-GOLD",
            "resolved_color": "BLACK / GOLD",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$40.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [1071.5, 234.2, 1177.1, 266.9],
                "exact_row_text": "2800BK-GOLD Chair (Weled) $40.00",
                "previous_row_text": "3103T Glass Dining Table $139.00",
                "next_row_text": "Page 122",
                "component_skus": ["2800BK-GOLD"],
                "resolved_price": "$40.00",
                "price": "$40.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $40.00 without unit"
            },
            "output_image": "reports/dining_batch8_draft_images/draft-2800bk-gold.jpg",
            "image_xref": 1459,
            "image_pixel_size": "819x564",
            "image_sha256": "f370be51f9c735d10aeea15a9ac0af360157d46587ca462a89d19b0a20061504",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "ordinary_scene_props": False,
            "catalog_product_overlap": True,
            "shared_layout_with_other_products": True,
            "shared_scene_for_multiple_skus": True,
            "displayed_model_uncertain": False,
            "evidence_only": True,
            "eligible_as_product_image": False,
            "shared_products_in_scene": ["3103T", "3114T", "3104T"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 63, printed pages DINETTE 121 and DINETTE 122.",
            "visual_review_notes": "Cropped from P63 scene. Overlaps with 3103T table in lifestyle scene.",
            "interpretation_notes": "Dining chair (welded) 2800BK-GOLD. PACK: 4/1 CARTON. Price list lists $40.00 without unit. Marked price_unit_status: unverified and publish: false.",
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
            "candidate_title_zh": "2800BK-GOLD 黑色金架焊接餐椅",
            "candidate_title_en": "2800BK-GOLD Black Gold Frame Welded Dining Chair"
        },

        # =========================================================================
        # 3. 3105T (Canonical Product - Dining Table)
        # =========================================================================
        {
            "record_type": "canonical_product",
            "canonical_sku": "3105T",
            "sku": "3105T",
            "component_skus": ["3105T"],
            "product_identity": "one complete round glass dining table with black frame",
            "components_verified": True,
            "pdf_physical_page": 64,
            "first_seen": {
                "physical_page": 64,
                "print_page": "DINETTE 123",
                "section": "DINETTE 123 left"
            },
            "occurrences": 1,
            "evidence_pages": [64],
            "source_text_regions": [
                {
                    "page": 64,
                    "print_page": "DINETTE 123",
                    "heading_region": [69.5, 518.2, 1626.2, 544.5],
                    "verbatim_heading": "3105T/2800BK-GRAY\n3106T/2800BK-GRAY",
                    "region": [72.3, 578.5, 343.4, 595.1],
                    "verbatim_text": "3105T  |  GLASS DINING TABLE    DIA  43\" x 30\"H"
                }
            ],
            "raw_heading_text": "3105T/2800BK-GRAY",
            "raw_model_text": "3105T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": "BLACK",
            "raw_dimensions_text": "DIA 43\" x 30\"H",
            "resolved_dimensions": "DIA 43\" x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$119.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [1068.8, 447.8, 1173.2, 478.1],
                "exact_row_text": "3105T Glass Dining Table $119.00",
                "previous_row_text": "Page 123",
                "next_row_text": "2800BK-GRAY Chair (Weled) $30.00",
                "component_skus": ["3105T"],
                "resolved_price": "$119.00",
                "price": "$119.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch8_draft_images/draft-3105t.jpg",
            "image_xref": 1474,
            "image_pixel_size": "817x563",
            "image_sha256": "481550636ab03f550b7cf924580f1de78f1fba58d820f99f312d2ab7aba3288a",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "ordinary_scene_props": False,
            "catalog_product_overlap": True,
            "shared_layout_with_other_products": True,
            "shared_scene_for_multiple_skus": False,
            "displayed_model_uncertain": False,
            "evidence_only": True,
            "eligible_as_product_image": False,
            "shared_products_in_scene": ["2800BK-GRAY"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 64, printed page DINETTE 123 left.",
            "visual_review_notes": "Cropped from P64 left scene. Overlaps with 2800BK-GRAY chairs.",
            "interpretation_notes": "Round glass dining table 3105T (DIA 43x30H) with black legs. Price list lists $119.00.",
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
            "candidate_title_zh": "3105T 43英寸圆形黑色玻璃餐桌",
            "candidate_title_en": "3105T 43\" Round Black Glass Dining Table"
        },

        # =========================================================================
        # 4. 2800BK-GRAY (Canonical Product - Dining Chair)
        # =========================================================================
        {
            "record_type": "canonical_product",
            "canonical_sku": "2800BK-GRAY",
            "sku": "2800BK-GRAY",
            "component_skus": ["2800BK-GRAY"],
            "product_identity": "dining chair with black frame",
            "components_verified": True,
            "pdf_physical_page": 64,
            "first_seen": {
                "physical_page": 64,
                "print_page": "DINETTE 123",
                "section": "DINETTE 123 left"
            },
            "occurrences": 2,
            "evidence_pages": [64],
            "source_text_regions": [
                {
                    "page": 64,
                    "print_page": "DINETTE 123",
                    "heading_region": [69.5, 518.2, 1626.2, 544.5],
                    "verbatim_heading": "3105T/2800BK-GRAY\n3106T/2800BK-GRAY",
                    "region": [72.3, 599.5, 359.6, 637.1],
                    "verbatim_text": "2800BK-GRAY  |  CHAIR (WELED)    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                },
                {
                    "page": 64,
                    "print_page": "DINETTE 124",
                    "heading_region": [69.5, 518.2, 1626.2, 544.5],
                    "verbatim_heading": "3105T/2800BK-GRAY\n3106T/2800BK-GRAY",
                    "region": [1386.3, 603.5, 1629.0, 641.1],
                    "verbatim_text": "2800BK-GRAY  |  CHAIR    17\"W x 19\"D x 38\"H\nPACK: 4/1 CARTON"
                }
            ],
            "raw_heading_text": "3105T/2800BK-GRAY",
            "raw_model_text": "2800BK-GRAY",
            "raw_color_text": "BK-GRAY",
            "resolved_color": "BLACK / GRAY",
            "raw_dimensions_text": "17\"W x 19\"D x 38\"H",
            "resolved_dimensions": "17\"W x 19\"D x 38\"H",
            "raw_pack_text": "PACK: 4/1 CARTON",
            "raw_price_text": "$30.00",
            "price_unit_status": "unverified",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [1068.8, 483.8, 1173.9, 516.4],
                "exact_row_text": "2800BK-GRAY Chair (Weled) $30.00",
                "previous_row_text": "3105T Glass Dining Table $119.00",
                "next_row_text": "Page 124",
                "component_skus": ["2800BK-GRAY"],
                "resolved_price": "$30.00",
                "price": "$30.00",
                "unit_text": "PACK: 4/1 CARTON in catalog; Price list lists $30.00 without unit"
            },
            "output_image": "reports/dining_batch8_draft_images/draft-2800bk-gray.jpg",
            "image_xref": 1474,
            "image_pixel_size": "817x563",
            "image_sha256": "481550636ab03f550b7cf924580f1de78f1fba58d820f99f312d2ab7aba3288a",
            "category": "DINING CHAIR",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "ordinary_scene_props": False,
            "catalog_product_overlap": True,
            "shared_layout_with_other_products": True,
            "shared_scene_for_multiple_skus": True,
            "displayed_model_uncertain": False,
            "evidence_only": True,
            "eligible_as_product_image": False,
            "shared_products_in_scene": ["3105T", "3106T"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 64, printed pages DINETTE 123 and DINETTE 124.",
            "visual_review_notes": "Cropped from P64 scene. Overlaps with 3105T table.",
            "interpretation_notes": "Dining chair (welded) 2800BK-GRAY. PACK: 4/1 CARTON. Price list lists $30.00 without specifying unit. Marked price_unit_status: unverified and publish: false.",
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
            "candidate_title_zh": "2800BK-GRAY 黑色灰面焊接餐椅",
            "candidate_title_en": "2800BK-GRAY Black Frame Gray Seat Welded Dining Chair"
        },

        # =========================================================================
        # 5. 3106T (Canonical Product - Dining Table)
        # =========================================================================
        {
            "record_type": "canonical_product",
            "canonical_sku": "3106T",
            "sku": "3106T",
            "component_skus": ["3106T"],
            "product_identity": "one complete rectangular glass dining table with black frame",
            "components_verified": True,
            "pdf_physical_page": 64,
            "first_seen": {
                "physical_page": 64,
                "print_page": "DINETTE 124",
                "section": "DINETTE 124 right"
            },
            "occurrences": 1,
            "evidence_pages": [64],
            "source_text_regions": [
                {
                    "page": 64,
                    "print_page": "DINETTE 124",
                    "heading_region": [69.5, 518.2, 1626.2, 544.5],
                    "verbatim_heading": "3105T/2800BK-GRAY\n3106T/2800BK-GRAY",
                    "region": [1348.5, 582.5, 1629.0, 599.1],
                    "verbatim_text": "3106T  |  GLASS DINING TABLE    36\"W x 60\"D x 30\"H"
                }
            ],
            "raw_heading_text": "3106T/2800BK-GRAY",
            "raw_model_text": "3106T",
            "raw_color_text": "GLASS DINING TABLE",
            "resolved_color": "BLACK",
            "raw_dimensions_text": "36\"W x 60\"D x 30\"H",
            "resolved_dimensions": "36\"W x 60\"D x 30\"H",
            "raw_pack_text": "",
            "raw_price_text": "$139.00",
            "price_unit_status": "verified_table",
            "price_evidence": {
                "price_list_page": 7,
                "price_row_bbox": [1070.7, 569.4, 1172.4, 600.0],
                "exact_row_text": "3106T Dining Table $139.00",
                "previous_row_text": "Page 124",
                "next_row_text": "2800BK-GRAY Dining Chair $30.00",
                "component_skus": ["3106T"],
                "resolved_price": "$139.00",
                "price": "$139.00",
                "unit_text": "1 complete table"
            },
            "output_image": "reports/dining_batch8_draft_images/draft-3106t.jpg",
            "image_xref": 1475,
            "image_pixel_size": "819x562",
            "image_sha256": "973c193d5a28dfcd2adb5e41e6dcbf9acb81fe1b3bb46899d8580acb516df23a",
            "category": "DINING TABLE",
            "classification": ["MULTI_PRODUCT_SCENE"],
            "ordinary_scene_props": False,
            "catalog_product_overlap": True,
            "shared_layout_with_other_products": True,
            "shared_scene_for_multiple_skus": False,
            "displayed_model_uncertain": False,
            "evidence_only": True,
            "eligible_as_product_image": False,
            "shared_products_in_scene": ["2800BK-GRAY"],
            "crop_contains_target_only": False,
            "crop_contains_other_products": True,
            "source_is_lifestyle_scene": True,
            "standalone_crop_possible": False,
            "source_notes": "Physical spread 64, printed page DINETTE 124 right.",
            "visual_review_notes": "Cropped from P64 right scene. Overlaps with 2800BK-GRAY chairs.",
            "interpretation_notes": "Rectangular glass dining table 3106T (36x60x30H) with black legs. Price list lists $139.00.",
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
            "candidate_title_zh": "3106T 60英寸长方形黑色玻璃餐桌",
            "candidate_title_en": "3106T 60\" Rectangular Black Glass Dining Table"
        },

        # =========================================================================
        # Occurrences (Cross-Batch References):
        # =========================================================================
        # 6. 3101T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3101T",
            "sku": "3101T",
            "product_identity": "one complete round glass dining table",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 62,
                    "print_page": "DINETTE 119",
                    "section": "DINETTE 119 left",
                    "raw_heading_text": "3101T/2800BK-CHROME",
                    "raw_dimensions_text": "DIA 43\" x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3101T  |  GLASS DINING TABLE    DIA  43\" x 30\"H",
                    "scene_chairs": "2800BK-CHROME",
                    "image_xref": 1444
                }
            ],
            "notes": "Occurrence #2 of 3101T. P62 DINETTE 119 left repeated table with 2800BK-CHROME chairs. Canonical record in Batch 7 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        },
        # 7. 3112T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3112T",
            "sku": "3112T",
            "product_identity": "one complete rectangular glass dining table",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 62,
                    "print_page": "DINETTE 120",
                    "section": "DINETTE 120 right",
                    "raw_heading_text": "3112T/2800BK-CHROME\n3102T/2800BK-CHROME",
                    "raw_dimensions_text": "30\"W x 48\"D x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3112T  |  GLASS DINING TABLE    30\"W x 48\"D x 30\"H",
                    "scene_chairs": "2800BK-CHROME",
                    "image_xref": 1445,
                    "visual_identity_status": "ambiguous",
                    "shared_scene_for_multiple_skus": True,
                    "displayed_model_uncertain": True
                }
            ],
            "notes": "Occurrence #2 of 3112T. P62 DINETTE 120 right shared scene with 3102T. Canonical record in Batch 7 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        },
        # 8. 3102T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3102T",
            "sku": "3102T",
            "product_identity": "one complete rectangular glass dining table",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 62,
                    "print_page": "DINETTE 120",
                    "section": "DINETTE 120 right",
                    "raw_heading_text": "3112T/2800BK-CHROME\n3102T/2800BK-CHROME",
                    "raw_dimensions_text": "36\"W x 60\"D x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3102T  |  GLASS DINING TABLE    36\"W x 60\"D x 30\"H",
                    "scene_chairs": "2800BK-CHROME",
                    "image_xref": 1445,
                    "visual_identity_status": "ambiguous",
                    "shared_scene_for_multiple_skus": True,
                    "displayed_model_uncertain": True
                }
            ],
            "notes": "Occurrence #5 of 3102T. P62 DINETTE 120 right shared scene with 3112T. Canonical record in Batch 6 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        },
        # 9. 3103T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3103T",
            "sku": "3103T",
            "product_identity": "one complete round glass dining table with gold frame",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 63,
                    "print_page": "DINETTE 121",
                    "section": "DINETTE 121 left",
                    "raw_heading_text": "3103T/2800BK-GOLD",
                    "raw_dimensions_text": "DIA 43\" x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3103T  |  GLASS DINING TABLE    DIA  43\" x 30\"H",
                    "scene_chairs": "2800BK-GOLD",
                    "image_xref": 1459
                }
            ],
            "notes": "Occurrence #2 of 3103T. P63 DINETTE 121 left repeated table with 2800BK-GOLD chairs. Canonical record in Batch 7 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        },
        # 10. 3114T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3114T",
            "sku": "3114T",
            "product_identity": "one complete rectangular glass dining table with gold frame",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 63,
                    "print_page": "DINETTE 122",
                    "section": "DINETTE 122 right",
                    "raw_heading_text": "3114T/2800BK-GOLD\n3104T/2800BK-GOLD",
                    "raw_dimensions_text": "30\"W x 48\"D x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "New 3114T  |  GLASS DINING TABLE    30\"W x 48\"D x 30\"H",
                    "scene_chairs": "2800BK-GOLD",
                    "image_xref": 1460,
                    "visual_identity_status": "ambiguous",
                    "shared_scene_for_multiple_skus": True,
                    "displayed_model_uncertain": True
                }
            ],
            "notes": "Occurrence #2 of 3114T. P63 DINETTE 122 right shared scene with 3104T. Canonical record in Batch 7 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        },
        # 11. 3104T (Occurrence Reference)
        {
            "record_type": "occurrence_reference",
            "canonical_sku": "3104T",
            "sku": "3104T",
            "product_identity": "one complete rectangular glass dining table with gold frame",
            "batch_occurrence_count": 1,
            "batch_page_evidence": [
                {
                    "physical_page": 63,
                    "print_page": "DINETTE 122",
                    "section": "DINETTE 122 right",
                    "raw_heading_text": "3114T/2800BK-GOLD\n3104T/2800BK-GOLD",
                    "raw_dimensions_text": "36\"W x 60\"D x 30\"H",
                    "raw_pack_text": "",
                    "raw_body_text": "3104T  |  GLASS DINING TABLE    36\"W x 60\"D x 30\"H",
                    "scene_chairs": "2800BK-GOLD",
                    "image_xref": 1460,
                    "visual_identity_status": "ambiguous",
                    "shared_scene_for_multiple_skus": True,
                    "displayed_model_uncertain": True
                }
            ],
            "notes": "Occurrence #2 of 3104T. P63 DINETTE 122 right shared scene with 3114T. Canonical record in Batch 7 maintained.",
            "source_catalog": "PJ 2026",
            "source_pdf_sha256": EXPECTED_SHA256,
            "human_reviewed": True,
            "publish": False,
            "review_result": "occurrence_only"
        }
    ]
    
    # Dynamically compute live disk hashes and PDF XObject hashes
    doc = fitz.open(PDF_PATH)
    for item in manifest:
        if item.get("record_type") == "occurrence_reference":
            continue
        out_img = item.get("output_image") or item.get("target_crop_image")
        if out_img and os.path.exists(out_img):
            with open(out_img, "rb") as f:
                disk_sha = hashlib.sha256(f.read()).hexdigest()
            item["output_image_sha256"] = disk_sha
            item["image_sha256"] = disk_sha
            
            xref = item.get("image_xref")
            if xref:
                try:
                    img_dict = doc.extract_image(xref)
                    if img_dict and "image" in img_dict:
                        item["source_image_sha256"] = hashlib.sha256(img_dict["image"]).hexdigest()
                except Exception:
                    pass
        item["price_unit_status"] = "unresolved"
        if "price_evidence" in item and item["price_evidence"]:
            item["price_evidence"]["unit_text"] = None

    out_path = "reports/manifest_v2_dining_batch8.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path} ({len(manifest)} items: 5 canonical, 6 occurrences)")

def build_contact_sheet():
    regions = [
        ("reports/dining_batch8_evidence/regions/p62_d119_left_3101t_2800bk_chrome.jpg", "P62 / DINETTE 119 Left", "3101T / 2800BK-CHROME", "Table: 3101T ($129.00) | Chair: 2800BK-CHROME ($35.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch8_evidence/regions/p62_d120_right_3112t_3102t_2800bk_chrome.jpg", "P62 / DINETTE 120 Right", "3112T / 3102T / 2800BK-CHROME", "Tables: 3112T ($119.00), 3102T ($149.00) | Chair: 2800BK-CHROME ($35.00)\nClass: C (MULTI_PRODUCT_SCENE) [Ambiguous Table] | publish: false"),
        ("reports/dining_batch8_evidence/regions/p63_d121_left_3103t_2800bk_gold.jpg", "P63 / DINETTE 121 Left", "3103T / 2800BK-GOLD", "Table: 3103T ($139.00) | Chair: 2800BK-GOLD ($40.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch8_evidence/regions/p63_d122_right_3114t_3104t_2800bk_gold.jpg", "P63 / DINETTE 122 Right", "3114T / 3104T / 2800BK-GOLD", "Tables: 3114T ($129.00), 3104T ($159.00) | Chair: 2800BK-GOLD ($40.00)\nClass: C (MULTI_PRODUCT_SCENE) [Ambiguous Table] | publish: false"),
        ("reports/dining_batch8_evidence/regions/p64_d123_left_3105t_2800bk_gray.jpg", "P64 / DINETTE 123 Left", "3105T / 2800BK-GRAY", "Table: 3105T ($119.00) | Chair: 2800BK-GRAY ($30.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
        ("reports/dining_batch8_evidence/regions/p64_d124_right_3106t_2800bk_gray.jpg", "P64 / DINETTE 124 Right", "3106T / 2800BK-GRAY", "Table: 3106T ($139.00) | Chair: 2800BK-GRAY ($30.00)\nClass: C (MULTI_PRODUCT_SCENE) | publish: false"),
    ]
    
    # 2 columns x 3 rows grid
    cell_w, cell_h = 750, 560
    sheet_w, sheet_h = cell_w * 2 + 60, cell_h * 3 + 120
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 248))
    draw = ImageDraw.Draw(sheet)
    
    # Header
    draw.rectangle([(0, 0), (sheet_w, 60)], fill=(30, 35, 45))
    draw.text((30, 18), "DINING BATCH 8 AUDIT CONTACT SHEET (P62-P64 / DINETTE 119-124)", fill=(255, 255, 255))
    
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
        
    sheet.save("reports/dining_batch8_contact_sheet.jpg", quality=90)
    print("Wrote reports/dining_batch8_contact_sheet.jpg")

if __name__ == "__main__":
    freeze_raw_texts()
    extract_images()
    build_manifest()
    build_contact_sheet()
