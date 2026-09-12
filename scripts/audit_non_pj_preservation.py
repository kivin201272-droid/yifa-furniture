#!/usr/bin/env python3
"""
scripts/audit_non_pj_preservation.py
Position-independent SKU-level audit and 3-way hash verification
across root baseline (11157499), intermediate (0e00e8be), and HEAD.
"""

import json
import os
import re
import subprocess
import hashlib

ROOT_BASELINE = "11157499"
INTERMEDIATE_COMMIT = "0e00e8be"

OFFICE_PROTECTED_SKUS = ["F3046", "F3049", "F3050", "F3051", "F3052"]

def extract_cards(html):
    return re.findall(r'<div class="sofa-card reveal">.*?</div>\s*</div>\s*</div>', html, flags=re.DOTALL)

def sha256_text(text):
    clean = text.strip().replace("\r\n", "\n")
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()

def extract_canonical_sku(card):
    m_h3 = re.search(r"<h3>(.*?)</h3>", card)
    if not m_h3:
        return "UNKNOWN"
    title = m_h3.group(1).strip()
    
    if "4031T" in title and "3003T" in title:
        return "4031T / 3003T"
    if "2391" in title and "2235" in title:
        return "2391 / 2235"
        
    m_sku = re.match(r"^([A-Z0-9\-_]+(?:\s*/\s*[A-Z0-9\-_]+)*)", title)
    if m_sku:
        return m_sku.group(1).strip()
    return title.split()[0]

def extract_card_details(card, base_dir):
    sku = extract_canonical_sku(card)
    m_title = re.search(r"<h3>(.*?)</h3>", card)
    title = m_title.group(1).strip() if m_title else "UNKNOWN"
    
    m_desc = re.search(r"<p>(.*?)</p>", card)
    desc = m_desc.group(1).strip() if m_desc else "NONE"
    
    m_img = re.search(r"<img\s+[^>]*src=[\"']([^\"']+)[\"']", card)
    img_src = m_img.group(1) if m_img else "NONE"
    
    thumbs = re.findall(r"<div class=\"sofa-thumb[^\"]*\">\s*<img\s+[^>]*src=[\"']([^\"']+)[\"']", card)
    
    m_price = re.search(r"<span class=\"price-tag\"[^>]*>(.*?)</span>", card)
    price = m_price.group(1).strip() if m_price else "NONE"
    
    tags = re.findall(r"<span class=\"detail-tag\"[^>]*>(.*?)</span>", card)
    card_hash = sha256_text(card)
    
    # Resolved image file paths
    all_raw_imgs = re.findall(r"<img\s+[^>]*src=[\"']([^\"']+)[\"']", card)
    resolved_imgs = [os.path.normpath(os.path.join(base_dir, s.split("?")[0].strip())) for s in all_raw_imgs]
    
    return {
        "sku": sku,
        "title": title,
        "desc": desc,
        "img_src": img_src,
        "thumbs": thumbs,
        "price": price,
        "tags": tags,
        "hash": card_hash,
        "image_files": resolved_imgs,
        "raw": card
    }

def get_git_tree_blobs(commit):
    out = subprocess.check_output(["git", "ls-tree", "-r", commit]).decode("utf-8")
    blobs = {}
    for line in out.splitlines():
        if line.strip():
            parts = line.split(None, 3)
            if len(parts) == 4 and parts[1] == "blob":
                blobs[parts[3]] = parts[2]
    return blobs

def build_sku_map(cards, base_dir):
    sku_map = {}
    duplicate_skus = []
    for c in cards:
        det = extract_card_details(c, base_dir)
        sku = det["sku"]
        if sku in sku_map:
            duplicate_skus.append(sku)
        sku_map[sku] = det
    return sku_map, duplicate_skus

def get_dining_protected_skus():
    en_html = subprocess.check_output(["git", "show", f"{ROOT_BASELINE}:dining/index.html"]).decode("utf-8")
    cards = extract_cards(en_html)
    protected_skus = []
    for c in cards:
        sku = extract_canonical_sku(c)
        if sku != "4160 / 4130":
            protected_skus.append(sku)
    return protected_skus

def run_full_audit():
    dining_protected_skus = get_dining_protected_skus()
    
    blobs_root = get_git_tree_blobs(ROOT_BASELINE)
    blobs_0e0 = get_git_tree_blobs(INTERMEDIATE_COMMIT)
    blobs_head = get_git_tree_blobs("HEAD")
    
    # Audit Office & Dining
    configs = [
        ("Office", "EN", "office/index.html", OFFICE_PROTECTED_SKUS),
        ("Office", "ZH", "zh/office/index.html", OFFICE_PROTECTED_SKUS),
        ("Dining", "EN", "dining/index.html", dining_protected_skus),
        ("Dining", "ZH", "zh/dining/index.html", dining_protected_skus)
    ]
    
    all_card_audits = []
    all_referenced_images = set()
    
    for category, lang, fpath, protected_whitelist in configs:
        base_dir = os.path.dirname(fpath)
        
        # Load 3 HTML versions
        html_root = subprocess.check_output(["git", "show", f"{ROOT_BASELINE}:{fpath}"]).decode("utf-8")
        html_0e0 = subprocess.check_output(["git", "show", f"{INTERMEDIATE_COMMIT}:{fpath}"]).decode("utf-8")
        html_head = open(fpath, "r", encoding="utf-8").read()
        
        map_root, dup_root = build_sku_map(extract_cards(html_root), base_dir)
        map_0e0, dup_0e0 = build_sku_map(extract_cards(html_0e0), base_dir)
        map_head, dup_head = build_sku_map(extract_cards(html_head), base_dir)
        
        assert len(dup_head) == 0, f"[{category} {lang}] Duplicate SKUs in HEAD: {dup_head}"
        
        for sku in protected_whitelist:
            assert sku in map_root, f"[{category} {lang}] Protected SKU {sku} missing in root baseline"
            assert sku in map_head, f"[{category} {lang}] Protected SKU {sku} missing in HEAD"
            
            c_root = map_root[sku]
            c_0e0 = map_0e0.get(sku)
            c_head = map_head[sku]
            
            hash_root = c_root["hash"]
            hash_0e0 = c_0e0["hash"] if c_0e0 else None
            hash_head = c_head["hash"]
            
            match_root_0e = (hash_root == hash_0e0)
            match_root_head = (hash_root == hash_head)
            
            for img in c_root["image_files"]:
                all_referenced_images.add(img)
                
            all_card_audits.append({
                "category": category,
                "lang": lang,
                "sku": sku,
                "root_sha256": hash_root,
                "base0e_sha256": hash_0e0,
                "head_sha256": hash_head,
                "title": c_head["title"],
                "price": c_head["price"],
                "image_count": len(c_head["image_files"]),
                "identical_to_root": match_root_head,
                "all_three_identical": match_root_0e and match_root_head
            })
            
    # Audit Images (115 files)
    all_image_audits = []
    for img_path in sorted(all_referenced_images):
        b_root = blobs_root.get(img_path)
        b_0e0 = blobs_0e0.get(img_path)
        b_head = blobs_head.get(img_path)
        
        exists_on_disk = os.path.exists(img_path)
        disk_size = os.path.getsize(img_path) if exists_on_disk else 0
        with open(img_path, "rb") as f:
            disk_sha256 = hashlib.sha256(f.read()).hexdigest() if exists_on_disk else None
            
        is_missing = (b_head is None) or not exists_on_disk
        is_zero_byte = (disk_size == 0)
        is_changed = (b_root != b_head) or (b_root != b_0e0)
        
        all_image_audits.append({
            "path": img_path,
            "blob_root": b_root,
            "blob_0e0": b_0e0,
            "blob_head": b_head,
            "disk_sha256": disk_sha256,
            "disk_size_bytes": disk_size,
            "is_missing": is_missing,
            "is_changed": is_changed,
            "is_zero_byte": is_zero_byte,
            "pass": not is_missing and not is_changed and not is_zero_byte and (b_root == b_head == b_0e0)
        })
        
    summary = {
        "protected_cards_total": len(all_card_audits),
        "office_protected_cards": len([c for c in all_card_audits if c["category"] == "Office"]),
        "dining_protected_cards": len([c for c in all_card_audits if c["category"] == "Dining"]),
        "protected_cards_pass": sum(1 for c in all_card_audits if c["identical_to_root"]),
        "protected_images_total": len(all_image_audits),
        "protected_images_missing": sum(1 for img in all_image_audits if img["is_missing"]),
        "protected_images_changed": sum(1 for img in all_image_audits if img["is_changed"]),
        "protected_images_zero_byte": sum(1 for img in all_image_audits if img["is_zero_byte"]),
        "protected_images_pass": sum(1 for img in all_image_audits if img["pass"]),
        "office_skus": OFFICE_PROTECTED_SKUS,
        "dining_skus": dining_protected_skus,
        "overall_cards_result": "PASS" if len(all_card_audits) == 104 and all(c["identical_to_root"] for c in all_card_audits) else "FAIL",
        "overall_images_result": "PASS" if len(all_image_audits) > 0 and all(img["pass"] for img in all_image_audits) else "FAIL"
    }
    
    with open("reports/three_way_preservation_audit.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary,
            "cards": all_card_audits,
            "images": all_image_audits
        }, f, indent=2, ensure_ascii=False)
        
    print("=" * 70)
    print("POSITION-INDEPENDENT SKU & IMAGE PRESERVATION AUDIT SUMMARY:")
    print(f"  Protected cards audited: {summary['protected_cards_total']} (Office: {summary['office_protected_cards']}, Dining: {summary['dining_protected_cards']})")
    print(f"  Protected cards 100% identical to 11157499: {summary['protected_cards_pass']}/{summary['protected_cards_total']} ({summary['overall_cards_result']})")
    print(f"  Protected unique images audited: {summary['protected_images_total']}")
    print(f"  Protected images missing: {summary['protected_images_missing']}")
    print(f"  Protected images changed: {summary['protected_images_changed']}")
    print(f"  Protected images zero-byte: {summary['protected_images_zero_byte']}")
    print(f"  Protected image files pass: {summary['protected_images_pass']}/{summary['protected_images_total']} ({summary['overall_images_result']})")
    print("=" * 70)
    
    return summary, all_card_audits, all_image_audits

if __name__ == "__main__":
    run_full_audit()
