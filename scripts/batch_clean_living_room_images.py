#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import cv2
import numpy as np

VISION_SCRIPT = """
import Foundation
import Vision
import AppKit

let dir = "/Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/living_room_named"
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter { 
    ($0.hasSuffix(".jpg") || $0.hasSuffix(".png")) && !$0.contains("_clean") 
}.sorted()

struct BoxInfo: Codable {
    let text: String
    let x: Double
    let y: Double
    let w: Double
    let h: Double
}

struct ImageResult: Codable {
    let filename: String
    let width: Int
    let height: Int
    let boxes: [BoxInfo]
}

var allResults: [ImageResult] = []

for file in files {
    let path = "\\(dir)/\\(file)"
    let url = URL(fileURLWithPath: path)
    guard let image = NSImage(contentsOf: url),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        continue
    }
    let width = cgImage.width
    let height = cgImage.height
    let wF = Double(width)
    let hF = Double(height)
    
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    let results = request.results ?? []
    
    var boxes: [BoxInfo] = []
    for res in results {
        let box = res.boundingBox
        let x = box.origin.x * wF
        let y = (1.0 - box.origin.y - box.size.height) * hF
        let w = box.size.width * wF
        let h = box.size.height * hF
        let text = res.topCandidates(1).first?.string ?? ""
        boxes.append(BoxInfo(text: text, x: x, y: y, w: w, h: h))
    }
    
    allResults.append(ImageResult(filename: file, width: width, height: height, boxes: boxes))
}

let encoder = JSONEncoder()
let data = try! encoder.encode(allResults)
print(String(data: data, encoding: .utf8)!)
"""

def get_text_boxes():
    print("Running Vision OCR on all living room images...")
    p = subprocess.Popen(["/usr/bin/swift", "-e", VISION_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    if p.returncode != 0:
        print("Error running Swift script:", err)
        sys.exit(1)
    return json.loads(out)

def clean_image(img_path, boxes, out_path):
    img = cv2.imread(img_path)
    if img is None:
        return False
    h, w, _ = img.shape
    out = img.copy()
    
    # Sort boxes from top to bottom
    for b in boxes:
        bx, by, bw, bh = b['x'], b['y'], b['w'], b['h']
        
        # Pad bounding box slightly to cover glyph edges
        pad_x = 4
        pad_y = 4
        x1 = max(0, int(bx - pad_x))
        y1 = max(0, int(by - pad_y))
        x2 = min(w, int(bx + bw + pad_x))
        y2 = min(h, int(by + bh + pad_y))
        
        # Check surrounding pixels
        surround_y1 = max(0, y1 - 6)
        surround_y2 = min(h, y2 + 6)
        surround_x1 = max(0, x1 - 6)
        surround_x2 = min(w, x2 + 6)
        
        # Sample border pixels (excluding the text box itself)
        border_pixels = []
        if y1 > surround_y1:
            border_pixels.append(out[surround_y1:y1, surround_x1:surround_x2].reshape(-1, 3))
        if y2 < surround_y2:
            border_pixels.append(out[y2:surround_y2, surround_x1:surround_x2].reshape(-1, 3))
        if x1 > surround_x1:
            border_pixels.append(out[surround_y1:surround_y2, surround_x1:x1].reshape(-1, 3))
        if x2 < surround_x2:
            border_pixels.append(out[surround_y1:surround_y2, x2:surround_x2].reshape(-1, 3))
            
        if border_pixels:
            borders = np.concatenate(border_pixels, axis=0)
            mean_color = np.mean(borders, axis=0)
            std_color = np.std(borders, axis=0)
            
            # If the background is near-white (> 235 on average) or uniform (std < 10)
            if np.all(mean_color > 235):
                out[y1:y2, x1:x2] = [255, 255, 255]
            elif np.all(std_color < 12):
                out[y1:y2, x1:x2] = np.round(mean_color).astype(np.uint8)
            else:
                # Use inpainting with Telea algorithm
                mask = np.zeros((h, w), dtype=np.uint8)
                mask[y1:y2, x1:x2] = 255
                # Dilate mask 2px
                kernel = np.ones((3,3), np.uint8)
                mask = cv2.dilate(mask, kernel, iterations=1)
                out = cv2.inpaint(out, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        else:
            out[y1:y2, x1:x2] = [255, 255, 255]
            
    cv2.imwrite(out_path, out, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    return True

def main():
    items = get_text_boxes()
    print(f"Total scanned images: {len(items)}")
    
    clean_count = 0
    skipped_count = 0
    
    img_dir = "assets/images/living_room_named"
    
    cleaned_mapping = {}
    
    for item in items:
        filename = item['filename']
        boxes = item['boxes']
        base_name, ext = os.path.splitext(filename)
        clean_name = f"{base_name}_clean{ext}"
        
        in_file = os.path.join(img_dir, filename)
        out_file = os.path.join(img_dir, clean_name)
        
        if not boxes:
            # Already clean, just copy or alias
            skipped_count += 1
            # We can also generate _clean.jpg for consistency
            clean_image(in_file, [], out_file)
            cleaned_mapping[filename] = clean_name
            continue
            
        print(f"Cleaning {filename} ({len(boxes)} text regions)...")
        clean_image(in_file, boxes, out_file)
        cleaned_mapping[filename] = clean_name
        clean_count += 1
        
    print(f"\nProcessing Complete!")
    print(f"Cleaned images with text/prices: {clean_count}")
    print(f"Images already clean: {skipped_count}")
    
    # Save mapping
    with open("scratch/cleaned_living_mapping.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_mapping, f, indent=2)

if __name__ == "__main__":
    main()
