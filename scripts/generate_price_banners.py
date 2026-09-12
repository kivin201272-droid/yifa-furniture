#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Batch Image Price Banner Generator (Python Pillow)
-----------------------------------------------------------
Bakes a customer-centric frosted glass multi-variant price banner (Twin / Full / Queen)
directly onto product images.

Features:
- Semi-transparent frosted glass gradient overlay at the bottom (~12-15% of image height)
- Top glass highlight line (translucent white)
- Left: Core slogan / selling point ("🔥 一件也是批发价" / "Factory Direct")
- Right: Horizontal multi-variant prices with Queen size highlighted in golden amber
- Auto-balances single, double, or triple specification variants
- Crisp anti-aliased typography (falls back to clean built-in fonts if custom TTF not found)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(size=24, bold=False):
    """Attempt to load a system or modern font, fallback to default."""
    font_paths = [
        # macOS PingFang / Helvetica / Arial
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # Windows
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_frosted_banner(
    img: Image.Image,
    variants: list,
    tagline: str = "🔥 一件也是批发价",
    lang: str = "zh"
) -> Image.Image:
    """
    Draws a bottom frosted glass multi-variant price banner on an image.
    """
    img = img.convert("RGBA")
    w, h = img.size

    # Banner height is proportional to image height (~14% or min 48px, max 120px)
    banner_h = max(48, min(120, int(h * 0.14)))
    banner_y = h - banner_h

    # Create overlay for gradient + blur effect
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # 1. Draw subtle frosted dark gradient banner (dark slate/stone with 82-90% opacity)
    for i in range(banner_h):
        alpha = int(190 + (i / banner_h) * 45)  # 190 to 235 (approx 75% to 92% opacity)
        draw_overlay.line(
            [(0, banner_y + i), (w, banner_y + i)],
            fill=(18, 18, 22, alpha)
        )

    # 2. Draw top glass highlight border (1-2px subtle white/cyan line)
    draw_overlay.line([(0, banner_y), (w, banner_y)], fill=(255, 255, 255, 60), width=1)
    draw_overlay.line([(0, banner_y + 1), (w, banner_y + 1)], fill=(255, 255, 255, 30), width=1)

    # Composite banner over image
    composed = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(composed)

    # 3. Typography setup
    base_font_size = max(14, int(banner_h * 0.32))
    tagline_font = get_font(int(base_font_size * 0.95), bold=True)
    price_font_bold = get_font(int(base_font_size * 1.08), bold=True)
    price_font_reg = get_font(int(base_font_size * 0.92), bold=False)

    padding_x = max(16, int(w * 0.035))
    center_y = banner_y + (banner_h // 2)

    # 4. Draw Left Slogan / Tagline
    draw.text(
        (padding_x, center_y),
        tagline,
        fill=(251, 191, 36, 255),  # Amber-400
        font=tagline_font,
        anchor="lm"
    )

    # 5. Format & Draw Right Multi-Variant Prices
    # Filter valid variants
    valid_variants = [v for v in variants if isinstance(v, dict) and "price" in v]
    if not valid_variants:
        return composed.convert("RGB")

    # Build price segments (from right to left)
    # Queen is highlighted, others are clean white/light gray
    items = []
    for v in valid_variants:
        code = str(v.get("code", "")).strip().upper()
        size = str(v.get("size", "")).strip()
        price = v.get("price", 0)
        if isinstance(price, int):
            price_str = f"${price}"
        elif isinstance(price, float) and price.is_integer():
            price_str = f"${int(price)}"
        else:
            price_str = f"${price:.2f}"
        
        # Display label
        label = code if len(code) <= 2 else (size if len(size) <= 6 else code)
        is_queen = code == "Q" or "queen" in size.lower()
        items.append({
            "label": f"{label}:",
            "price": price_str,
            "is_queen": is_queen
        })

    # Render items from right to left
    cur_x = w - padding_x
    divider_gap = max(8, int(w * 0.015))

    for idx, item in enumerate(reversed(items)):
        # Price text
        p_text = item["price"]
        l_text = item["label"]
        is_q = item["is_queen"]

        p_font = price_font_bold if is_q else price_font_reg
        p_color = (252, 211, 77, 255) if is_q else (255, 255, 255, 255) # Bright amber-300 or White
        l_color = (214, 211, 209, 230) # Stone-300

        # Measure widths
        p_bbox = draw.textbbox((0, 0), p_text, font=p_font)
        p_w = p_bbox[2] - p_bbox[0]

        l_bbox = draw.textbbox((0, 0), l_text, font=price_font_reg)
        l_w = l_bbox[2] - l_bbox[0]

        # Draw price
        cur_x -= p_w
        draw.text((cur_x, center_y), p_text, fill=p_color, font=p_font, anchor="lm")

        # Draw label
        cur_x -= (l_w + 3)
        draw.text((cur_x, center_y), l_text, fill=l_color, font=price_font_reg, anchor="lm")

        # Draw subtle vertical divider if not first from right
        if idx < len(items) - 1:
            cur_x -= divider_gap
            div_h = int(banner_h * 0.28)
            draw.line(
                [(cur_x, center_y - div_h // 2), (cur_x, center_y + div_h // 2)],
                fill=(255, 255, 255, 60),
                width=1
            )
            cur_x -= divider_gap

    return composed.convert("RGB")

def batch_process(products_json_path: str, output_dir: str, base_dir: str = "."):
    """Batch generate images for all products in products.json"""
    with open(products_json_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    count = 0

    for prod in products:
        img_rel = prod.get("image", "").lstrip("/")
        if not img_rel:
            continue

        img_path = os.path.join(base_dir, img_rel)
        if not os.path.exists(img_path):
            continue

        try:
            with Image.open(img_path) as im:
                variants = prod.get("variants", [])
                tagline = "🔥 一件也是批发价"
                out_img = draw_frosted_banner(im, variants, tagline=tagline)

                out_filename = f"{prod['id']}_banner.jpg"
                out_file_path = os.path.join(output_dir, out_filename)
                out_img.save(out_file_path, "JPEG", quality=92)
                print(f"[OK] Generated: {out_file_path}")
                count += 1
        except Exception as e:
            print(f"[Error] Failed processing {img_path}: {e}")

    print(f"\nCompleted! Generated {count} images with frosted price banners.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate frosted glass price banners on product images.")
    parser.add_argument("--input", "-i", type=str, help="Single image input path")
    parser.add_argument("--output", "-o", type=str, help="Single image output path or output folder")
    parser.add_argument("--json", "-j", type=str, default="src/data/products.json", help="Path to products.json")
    parser.add_argument("--batch", action="store_true", help="Batch process all products from products.json")

    args = parser.parse_args()

    if args.batch or not args.input:
        out_dir = args.output or "assets/images/with_price_banner"
        batch_process(args.json, out_dir)
    else:
        # Single image demo
        variants_example = [
            {"code": "T", "size": "Twin", "price": 149},
            {"code": "F", "size": "Full", "price": 179},
            {"code": "Q", "size": "Queen", "price": 199}
        ]
        with Image.open(args.input) as im:
            res = draw_frosted_banner(im, variants_example)
            out_p = args.output or "output_banner_demo.jpg"
            res.save(out_p, "JPEG", quality=95)
            print(f"[OK] Saved demo image: {out_p}")
