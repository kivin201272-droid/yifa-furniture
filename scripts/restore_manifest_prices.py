#!/usr/bin/env python3
"""
scripts/restore_manifest_prices.py
Safely restore exact prices in manifests without shell expansion risk,
and generate SHA-256 audit hashes for frozen raw PDF text files.
"""

import json
import hashlib
import os

PRICE_EVIDENCE_MAP = {
    # Batch 5
    "3000T/3002BK": {
        "price_list_page": 7,
        "price_row_bbox": [182.2, 437.1, 288.1, 467.2],
        "exact_row_text": "3000T/3002BK Dining Table with Black Glass Top $349.00",
        "previous_row_text": "Page 105",
        "next_row_text": "1001BK Dinning Chair $149.00",
        "component_skus": ["3000T", "3002BK"],
        "resolved_price": "$349.00",
        "price": "$349.00",
        "unit_text": "1 complete table"
    },
    "1001BK": {
        "price_list_page": 7,
        "price_row_bbox": [182.8, 483.6, 287.9, 511.2],
        "exact_row_text": "1001BK Dinning Chair $149.00",
        "previous_row_text": "3000T/3002BK Dining Table with Black Glass Top $349.00",
        "next_row_text": "Page 106",
        "component_skus": ["1001BK"],
        "resolved_price": "$149.00",
        "price": "$149.00",
        "unit_text": "PACK: 2/1 CARTON in catalog; Price list lists $149.00 without unit"
    },
    "3008T/3008GRAY": {
        "price_list_page": 7,
        "price_row_bbox": [183.6, 565.0, 288.3, 618.6],
        "exact_row_text": "3008T/3008GRAY Dining Table with 22mm Gray Marble Top $399.00",
        "previous_row_text": "Page 106",
        "next_row_text": "1500GRAY-CHROME Dinning Chair $89.00",
        "component_skus": ["3008T", "3008GRAY"],
        "resolved_price": "$399.00",
        "price": "$399.00",
        "unit_text": "1 complete table"
    },
    # Batch 6
    "3007T/3007WH": {
        "price_list_page": 7,
        "price_row_bbox": [183.6, 691.5, 286.8, 731.6],
        "exact_row_text": "3007T/ 3007WH Dining Table with White Glass Top $399.00",
        "previous_row_text": "Page 107",
        "next_row_text": "1403WH-GOLD Dinning Chair $99.00",
        "component_skus": ["3007T", "3007WH"],
        "resolved_price": "$399.00",
        "price": "$399.00",
        "unit_text": "1 complete table (table base + glass top)"
    },
    "1403WH": {
        "price_list_page": 7,
        "price_row_bbox": [184.6, 729.4, 286.0, 756.2],
        "exact_row_text": "1403WH-GOLD Dinning Chair $99.00",
        "previous_row_text": "3007T/ 3007WH Dining Table with White Glass Top $399.00",
        "next_row_text": "3008T/3007WH Dining Table with 12mm White Glass Top $349.00",
        "component_skus": ["1403WH-GOLD"],
        "resolved_price": "$99.00",
        "price": "$99.00",
        "unit_text": "PACK: 2/1 CARTON in catalog; Price list lists $99.00 without unit"
    },
    "3008T/3007WH": {
        "price_list_page": 7,
        "price_row_bbox": [183.1, 754.3, 286.0, 779.6],
        "exact_row_text": "3008T/3007WH Dining Table with 12mm White Glass Top $349.00",
        "previous_row_text": "1403WH-GOLD Dinning Chair $99.00",
        "next_row_text": "1200GRAY Dinning Chair $89.00",
        "component_skus": ["3008T", "3007WH"],
        "resolved_price": "$349.00",
        "price": "$349.00",
        "unit_text": "1 complete table (table base + glass top)"
    },
    "1401BK": {
        "price_list_page": 7,
        "price_row_bbox": [470.5, 110.0, 577.1, 140.7],
        "exact_row_text": "1401BK Dinning Chair $99.00",
        "previous_row_text": "3007T/3007WH Dining Table with White Glass Top $399.00",
        "next_row_text": "Page 109",
        "component_skus": ["1401BK"],
        "resolved_price": "$99.00",
        "price": "$99.00",
        "unit_text": "PACK: 2/1 CARTON in catalog; Price list lists $99.00 without unit"
    },
    "3102T": {
        "price_list_page": 7,
        "price_row_bbox": [469.4, 314.5, 584.0, 344.9],
        "exact_row_text": "3102T Glass Dining Table $149.00",
        "previous_row_text": "Page 110",
        "next_row_text": "2680GRAY-CHROME Chair (Weled) $79.00",
        "component_skus": ["3102T"],
        "resolved_price": "$149.00",
        "price": "$149.00",
        "unit_text": "1 complete table"
    },
    "2680BK-CHROME": {
        "price_list_page": 7,
        "price_row_bbox": [469.6, 476.4, 583.2, 509.0],
        "exact_row_text": "2680BK-CHROME Chair (Weled) $79.00",
        "previous_row_text": "3102T Glass Dining Table $149.00",
        "next_row_text": "2800WH-GOLD Chair (Weled) $40.00",
        "component_skus": ["2680BK-CHROME"],
        "resolved_price": "$79.00",
        "price": "$79.00",
        "unit_text": "PACK: 2/1 CARTON in catalog; Price list lists $79.00 without unit"
    }
}

def update_manifest(filepath):
    data = json.load(open(filepath, "r", encoding="utf-8"))
    for item in data:
        sku = item.get("sku")
        if sku in PRICE_EVIDENCE_MAP:
            item["price_evidence"] = PRICE_EVIDENCE_MAP[sku]
            if "price" in item:
                item["price"] = PRICE_EVIDENCE_MAP[sku]["price"]
            if "raw_price_text" in item:
                item["raw_price_text"] = PRICE_EVIDENCE_MAP[sku]["price"]
                
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {filepath}")

def generate_frozen_hashes():
    files = [
        "reports/raw_pdf_text_p56.txt",
        "reports/raw_pdf_text_p57.txt",
        "reports/raw_pdf_text_p58.txt"
    ]
    audit_data = {}
    for fpath in files:
        assert os.path.exists(fpath), f"Missing {fpath}"
        with open(fpath, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        audit_data[fpath] = {
            "sha256": h,
            "byte_size": os.path.getsize(fpath)
        }
        print(f"{fpath}: {h}")
        
    out_path = "reports/frozen_raw_text_hashes.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    update_manifest("reports/manifest_v2_dining_batch5.json")
    update_manifest("reports/manifest_v2_dining_batch6.json")
    generate_frozen_hashes()
