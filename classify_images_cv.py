import cv2
import numpy as np
import os
import shutil
from pathlib import Path

# Paths
REF_DIR = Path('素材库/图片正确分类')
SRC_DIRS = [Path(f'assets/images/pdf{i}') for i in [1,2,3,5,6,7,8,10]]
OUT_DIR = Path('assets/images/classified_products')

categories = ['bedroom', 'living room', 'diningroom', 'mattress']

# Initialize SIFT detector
sift = cv2.SIFT_create()

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

print("Loading reference images...")
# 1. Load reference images and compute descriptors
ref_data = {} # category -> [(img_path, kp, des)]
for cat in categories:
    cat_dir = REF_DIR / cat
    ref_data[cat] = []
    if not cat_dir.exists(): continue
    for f in cat_dir.glob('*.png'):
        img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
        if img is None: continue
        kp, des = sift.detectAndCompute(img, None)
        if des is not None:
            ref_data[cat].append((f.name, kp, des))
            print(f"  Loaded {f.name} in {cat} ({len(kp)} keypoints)")

print("\nMatching source images...")
# 2. Iterate through source images and match
MIN_MATCH_COUNT = 15

for src_dir in SRC_DIRS:
    if not src_dir.exists(): continue
    for src_file in src_dir.glob('*.jpg'):
        img_src = cv2.imread(str(src_file), cv2.IMREAD_GRAYSCALE)
        if img_src is None: continue
        kp_src, des_src = sift.detectAndCompute(img_src, None)
        if des_src is None or len(kp_src) < MIN_MATCH_COUNT:
            continue
            
        best_cat = None
        best_matches = 0
        
        for cat in categories:
            for ref_name, kp_ref, des_ref in ref_data[cat]:
                try:
                    # Need at least 2 descriptors to use knnMatch with k=2
                    if len(des_ref) < 2 or len(des_src) < 2:
                        continue
                        
                    matches = flann.knnMatch(des_src, des_ref, k=2)
                    good = []
                    for match_pair in matches:
                        if len(match_pair) == 2:
                            m, n = match_pair
                            if m.distance < 0.7 * n.distance:
                                good.append(m)
                    if len(good) > best_matches and len(good) > MIN_MATCH_COUNT:
                        best_matches = len(good)
                        best_cat = cat
                except Exception as e:
                    pass
                    
        if best_cat:
            print(f"Matched {src_dir.name}/{src_file.name} to {best_cat} with {best_matches} matches")
            out_cat_dir = OUT_DIR / best_cat
            out_cat_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(src_file), str(out_cat_dir / f"{src_dir.name}_{src_file.name}"))
            
print("\nClassification complete.")
