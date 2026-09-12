import os, re

# Update custom-gallery.css to give first-class styling to .price-tag, .price-current, and .sofa-details
with open('assets/css/custom-gallery.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make sure .price-tag and .price-current are styled bold red and aligned nicely with tags
price_css = """
.sofa-details {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: auto;
  padding-top: 10px;
  margin-bottom: 12px;
}

.price-tag, .price-current {
  font-size: 1.05rem;
  font-weight: 700;
  color: #e63946 !important;
  margin-right: 6px;
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.detail-tag, .spec-tag {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent-deep, #78644c);
  background: var(--bg-soft, #f4f0eb);
  padding: 4px 10px;
  border-radius: 4px;
  letter-spacing: 0.03em;
  display: inline-flex;
  align-items: center;
}
"""

if '.price-tag, .price-current' not in css:
    css += '\n' + price_css
    with open('assets/css/custom-gallery.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Updated assets/css/custom-gallery.css with unified price tag styles.")

# Let's clean and standardize cards across all 5 categories (ZH & EN)
pages = [
    ('zh/bedroom/index.html', 'bedroom/index.html', 'Bedroom'),
    ('zh/living-room/index.html', 'living-room/index.html', 'Living Room'),
    ('zh/dining/index.html', 'dining/index.html', 'Dining'),
    ('zh/office/index.html', 'office/index.html', 'Office'),
    ('zh/mattress/index.html', 'mattress/index.html', 'Mattress'),
]

# Refined concise price mappings for suites and multi-component items
suite_refinements = [
    ('8910', '折后 5件套 $799.00 | Queen床 $499.00', '5-PC Set: $799.00 | Queen Bed: $499.00'),
    ('8003', '折后 5件套 $799.00 | Queen床 $220.00', '5-PC Set: $799.00 | Queen Bed: $220.00'),
    ('8010', '折后 5件套 $649.00 | Full/Queen $180.00', '5-PC Set: $649.00 | Full/Queen: $180.00'),
    ('8009', '折后 5件套 $579.00 | Full/Queen $175.00', '5-PC Set: $579.00 | Full/Queen: $175.00'),
    ('8008', '折后 5件套 $579.00 | Full/Queen $175.00', '5-PC Set: $579.00 | Full/Queen: $175.00'),
    ('4160 / 4130', '折后 餐桌: $109 - $139 | 餐椅: $59.95/把', 'Table: $109 - $139 | Chair: $59.95/ea'),
    ('3016T / 3000WH', '折后 餐桌: $549.00 | 餐椅: $99 - $149', 'Table: $549.00 | Chair: $99 - $149'),
    ('3010T / 3011T', '折后 餐桌: $499 - $549 | 餐椅: $85 - $149', 'Table: $499 - $549 | Chair: $85 - $149'),
    ('3012T', '折后 餐桌: $499.00 | 餐椅: $79.00', 'Table: $499.00 | Chair: $79.00'),
    ('3000T / 3002', '折后 大理石桌: $399 | 玻璃桌: $349 | 餐椅: $89 - $149', 'Marble: $399 | Glass: $349 | Chair: $89 - $149'),
    ('3008T / 3007T', '折后 餐桌: $349 - $399 | 餐椅: $89 - $99', 'Table: $349 - $399 | Chair: $89 - $99'),
    ('3102T / 3112T / 3101T', '折后 玻璃餐桌: $119 - $149 | 餐椅: $35 - $79', 'Glass Table: $119 - $149 | Chair: $35 - $79'),
    ('3104T / 3114T / 3103T', '折后 镀金餐桌: $119 - $159 | 餐椅: $40 - $69', 'Gold Table: $119 - $159 | Chair: $40 - $69'),
    ('2240 / 2250', '折后 餐桌: $59 - $75 | 餐椅: $30.00', 'Table: $59 - $75 | Chair: $30.00'),
    ('4031T / 3003T', '折后 3003T: $179 | 4031T: $139 | 餐椅: $49.95 - $65', '3003T: $179 | 4031T: $139 | Chair: $49.95 - $65'),
    ('2206T / 2216T', '折后 一桌四椅: $199.00 | 单桌: $89.00', '5-PC Set: $199.00 | Table: $89.00'),
    ('4002 / 4154 / 4158', '折后 餐桌: $85 - $95 | 餐椅: $39.95 - $42', 'Table: $85 - $95 | Chair: $39.95 - $42'),
    ('4003 / 4114 / 4009', '折后 5件套: $179.00 | 3件套: $89 - $119', '5-PC: $179.00 | 3-PC: $89 - $119'),
    ('2391 / 2235', '折后 吧台桌: $45 - $129 | 吧椅: $29.95 - $45', 'Bar Table: $45 - $129 | Stool: $29.95 - $45'),
    ('4220 / 4218 / 4216', '折后 5层: $35 - $45 | 4层: $25 - $35 | 3层: $19.95 - $25', '5-Tier: $35 - $45 | 4-Tier: $25 - $35 | 3-Tier: $19.95 - $25'),
    ('4202 - 4208', '折后 模块收纳架: $17.95 - $49.95', 'Modular Shelves: $17.95 - $49.95'),
]

for zh_path, en_path, cat in pages:
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_content = f.read()
    with open(en_path, 'r', encoding='utf-8') as f:
        en_content = f.read()

    # Function to rewrite .sofa-details cleanly inside each card
    def standardize_card_details(html_str, is_zh=True):
        # find all sofa-card blocks
        def fix_card(match):
            card_html = match.group(0)
            
            # Extract title
            tm = re.search(r'<h3>(.*?)</h3>', card_html, re.DOTALL)
            title = tm.group(1).strip() if tm else ''
            
            # Check if any suite refinement matches title
            refined_price = None
            for pat, z_pr, e_pr in suite_refinements:
                if re.search(pat, title, re.I):
                    refined_price = z_pr if is_zh else e_pr
                    break
            
            # Extract existing price if not refined
            if not refined_price:
                pm = re.search(r'<(?:span|div)\s+class=[\"\'](?:price-current|price-tag)[\"\'][^>]*>(.*?)</(?:span|div)>', card_html, re.DOTALL)
                if pm:
                    refined_price = pm.group(1).strip()
            
            # Extract all tags
            tags = re.findall(r'<span\s+class=[\"\'](?:detail-tag|spec-tag)[\"\'][^>]*>(.*?)</span>', card_html)
            
            # Build standardized sofa-details
            if refined_price or tags:
                price_html = f'<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{refined_price}</span>' if refined_price else ''
                tags_html = '\n'.join([f'                    <span class="detail-tag">{t.strip()}</span>' for t in tags if t.strip()])
                new_details = f"""<div class="sofa-details">
                    {price_html}
{tags_html}
                </div>"""
                
                # Replace existing sofa-details
                card_html = re.sub(r'<div\s+class=[\"\']sofa-details[\"\'][\s\S]*?</div>', new_details, card_html, count=1)
                
            return card_html

        # Apply to all cards
        pattern = re.compile(r'<div\s+class=[\"\']sofa-card[^\"\']*[\"\'][\s\S]*?</div>\s*</div>')
        return pattern.sub(fix_card, html_str)

    zh_new = standardize_card_details(zh_content, is_zh=True)
    en_new = standardize_card_details(en_content, is_zh=False)

    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_new)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_new)
        
    print(f"Standardized price bars and tags for {cat} ({zh_path} & {en_path}).")

print("\n=== ALL CATEGORY PAGES STANDARDIZED ACCORDING TO REFERENCE FORMAT ===")
