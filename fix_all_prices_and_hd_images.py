import os, re, glob
import fitz # PyMuPDF
from PIL import Image, ImageEnhance

def fix_prices():
    print("=== 1. FIXING ALL MALFORMED PRICES IN HTML FILES ===")
    
    # Define exact price mappings for all PJ items
    # (Regex pattern or model title matching -> correct ZH price string, correct EN price string)
    price_corrections = [
        # Bedroom Suites
        (r'8910', '折后 Queen床: $499.00 | 床头柜: $90.00 | 镜子: $60.00 | 梳妆台: $260.00 | 五斗柜: $195.00', 'Queen Bed: $499.00 | Nightstand: $90.00 | Mirror: $60.00 | Dresser: $260.00 | Chest: $195.00'),
        (r'8003', '折后 Queen床: $220.00 | 床头柜: $90.00 | 镜子: $70.00 | 梳妆台: $260.00 | 五斗柜: $195.00 | Queen五件套: $799.00', 'Queen Bed: $220.00 | Nightstand: $90.00 | Mirror: $70.00 | Dresser: $260.00 | Chest: $195.00 | Queen 5-PC Set: $799.00'),
        (r'8010', '折后 Full/Queen床: $180.00 | 床头柜: $85.00 | 镜子: $60.00 | 梳妆台: $225.00 | 五斗柜: $170.00 | 5件套: $649.00', 'Full/Queen Bed: $180.00 | Nightstand: $85.00 | Mirror: $60.00 | Dresser: $225.00 | Chest: $170.00 | 5-PC Set: $649.00'),
        (r'8009', '折后 Full/Queen床: $175.00 | 床头柜: $75.00 | 镜子: $55.00 | 梳妆台: $205.00 | 五斗柜: $170.00 | 5件套: $579.00', 'Full/Queen Bed: $175.00 | Nightstand: $75.00 | Mirror: $55.00 | Dresser: $205.00 | Chest: $170.00 | 5-PC Set: $579.00'),
        (r'8008', '折后 Full/Queen床: $175.00 | 床头柜: $75.00 | 镜子: $55.00 | 梳妆台: $205.00 | 五斗柜: $170.00 | 5件套: $579.00', 'Full/Queen Bed: $175.00 | Nightstand: $75.00 | Mirror: $55.00 | Dresser: $205.00 | Chest: $170.00 | 5-PC Set: $579.00'),
        
        # Platform Beds
        (r'7402Q-WH', '折后 Queen: $499.00', 'Queen: $499.00'),
        (r'7401Q-BK', '折后 Queen: $499.00', 'Queen: $499.00'),
        (r'7405WH', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00'),
        (r'7403GRAY', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00'),
        (r'7602Q-GRAY', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00'),
        (r'7602Q-IVY', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00'),
        (r'7602-PINK', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00'),
        (r'7404BK', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00'),
        (r'7500F/7500Q', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00'),
        (r'7600Q-IVY', '折后 Queen: $399.00', 'Queen: $399.00'),
        (r'7603', '折后 Full: $179.00 | Queen: $199.00', 'Full: $179.00 | Queen: $199.00'),
        
        # Beds & Bunks
        (r'7806-GRAY', '折后 Full: $199.00 | Queen: $229.00', 'Full: $199.00 | Queen: $229.00'),
        (r'7102 GRAY', '折后 Full: $109.00 | Queen: $119.00', 'Full: $109.00 | Queen: $119.00'),
        (r'7102 BROWN', '折后 Full: $109.00 | Queen: $119.00', 'Full: $109.00 | Queen: $119.00'),
        (r'7100', '折后 T: $75.00 | F: $85.00 | Q: $95.00', 'Twin: $75.00 | Full: $85.00 | Queen: $95.00'),
        (r'7804 GRAY', '折后 Full: $249.00 | Queen: $269.00', 'Full: $249.00 | Queen: $269.00'),
        (r'7011GRAY', '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'Twin: $119.00 | Full: $139.00 | Queen: $149.00'),
        (r'7011CHAR', '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'Twin: $119.00 | Full: $139.00 | Queen: $149.00'),
        (r'7016-GRAY', '折后 Full: $99.00 | Queen: $109.00', 'Full: $99.00 | Queen: $109.00'),
        (r'2331', '折后 $119.00', '$119.00'),
        (r'7005BK', '折后 $149.00', '$149.00'),
        (r'7004BK', '折后 $169.00', '$169.00'),
        (r'7701WH', '折后 $219.00', '$219.00'),
        (r'7702WH', '折后 $279.00', '$279.00'),
        (r'7702CA', '折后 $279.00', '$279.00'),
        (r'7701CA', '折后 $219.00', '$219.00'),
        (r'7020WH', '折后 Full: $199.00 | Queen: $219.00', 'Full: $199.00 | Queen: $219.00'),
        (r'7021BK', '折后 Full: $199.00 | Queen: $219.00', 'Full: $199.00 | Queen: $219.00'),
        (r'7013', '折后 Twin: $99.00 | Full: $119.00 | Queen: $129.00', 'Twin: $99.00 | Full: $119.00 | Queen: $129.00'),
        (r'7901CA-T/F', '折后 Twin: $109.00 | Full: $129.00', 'Twin: $109.00 | Full: $129.00'),
        (r'7901WH-T/F', '折后 Twin: $109.00 | Full: $129.00', 'Twin: $109.00 | Full: $129.00'),
        (r'1901', '折后 T: $59.00 | F: $79.00 | Q: $89.00', 'Twin: $59.00 | Full: $79.00 | Queen: $89.00'),
        (r'7800/7801', '折后 7800Q: $99.00 | 7801F: $99.00 | 抽拉床架: $55.00 / $85.00', '7800Q: $99.00 | 7801F: $99.00 | Trundle: $55.00 / $85.00'),
        (r'7001', '折后 T: $79.00 | F: $99.00 | Q: $109.00', 'Twin: $79.00 | Full: $99.00 | Queen: $109.00'),
        (r'7009', '折后 T: $95.00 | F: $119.00 | Q: $129.00', 'Twin: $95.00 | Full: $119.00 | Queen: $129.00'),
        (r'7202', '折后 T: $99.00 | F: $119.00 | Q: $129.00', 'Twin: $99.00 | Full: $119.00 | Queen: $129.00'),
        (r'7203', '折后 T: $99.00 | F: $119.00 | Q: $129.00', 'Twin: $99.00 | Full: $119.00 | Queen: $129.00'),
        (r'7002', '折后 T: $79.00 | F: $99.00 | Q: $109.00', 'Twin: $79.00 | Full: $99.00 | Queen: $109.00'),
        (r'7003T-BK', '折后 Twin: $69.00 | Full: $89.00', 'Twin: $69.00 | Full: $89.00'),
        (r'7003T-WH', '折后 Twin: $69.00 | Full: $89.00', 'Twin: $69.00 | Full: $89.00'),
        (r'4224', '折后 $95.00', '$95.00'),
        (r'4225', '折后 $105.00', '$105.00'),
        (r'4226', '折后 $135.00', '$135.00'),
        (r'4227CH', '折后 $185.00', '$185.00'),
        (r'4228', '折后 $75.00', '$75.00'),
        (r'4424', '折后 $89.00', '$89.00'),
        (r'4229', '折后 $55.00', '$55.00'),
        (r'4322', '折后 4322款: $65.00 | 4323款: $75.00', '4322 Model: $65.00 | 4323 Model: $75.00'),
        (r'4223', '折后 $85.00', '$85.00'),
        
        # Dining
        (r'2524', '折后 $65.00', '$65.00'),
        (r'2526', '折后 $49.95', '$49.95'),
        (r'4405', '折后 $65.00', '$65.00'),
        (r'4406', '折后 $99.95', '$99.95'),
        
        # Office
        (r'2715', '折后 $49.95', '$49.95'),
        (r'2716', '折后 $59.95', '$59.95'),
        (r'4500', '折后 $39.95', '$39.95'),
        (r'2714', '折后 $39.95', '$39.95'),
        (r'2704', '折后 $19.95', '$19.95'),
        (r'2709', '折后 $89.00', '$89.00'),
        (r'2006GRAY', '折后 $49.95', '$49.95'),
        (r'2707', '折后 $35.00', '$35.00'),
        (r'2720', '折后 $85.00', '$85.00'),
        (r'2722', '折后 $109.95', '$109.95'),
        (r'2725BK', '折后 $59.95', '$59.95'),
        (r'2706', '折后 $55.00', '$55.00'),
        (r'2708BK', '折后 $69.95', '$69.95'),
        (r'2724', '折后 $99.95', '$99.95'),
        
        # Living Room TV & Storage
        (r'4420', '折后 4420款: $79.00 | 4421款: $99.00', '4420 Model: $79.00 | 4421 Model: $99.00'),
        (r'4422', '折后 $129.00', '$129.00'),
        (r'4432CA', '折后 $49.95', '$49.95'),
        (r'4801', '折后 $99.95', '$99.95'),
        (r'2766', '折后 $65.00', '$65.00'),
        (r'2767', '折后 $75.00', '$75.00'),
        (r'2769', '折后 $129.00', '$129.00'),
        (r'4337BK', '折后 4337款: $85.00 | 4338款: $69.00', '4337 Model: $85.00 | 4338 Model: $69.00'),
        (r'4333', '折后 4333款: $85.00 | 4334款: $69.00', '4333 Model: $85.00 | 4334 Model: $69.00'),
        (r'4331', '折后 4331款: $85.00 | 4332款: $69.00', '4331 Model: $85.00 | 4332 Model: $69.00'),
        (r'4335', '折后 4335款: $89.00 | 4336款: $75.00', '4335 Model: $89.00 | 4336 Model: $75.00'),
        (r'4337WH', '折后 4337款: $85.00 | 4338款: $69.00', '4337 Model: $85.00 | 4338 Model: $69.00'),
        (r'4220', '折后 5层带门/无门: $45.00 / $35.00 | 4层带门/无门: $35.00 / $25.00 | 3层带门/无门: $25.00 / $19.95', '5-Shelf with/no door: $45.00 / $35.00 | 4-Shelf with/no door: $35.00 / $25.00 | 3-Shelf with/no door: $25.00 / $19.95'),
        (r'4316', '折后 4316款: $29.95 | 4320款: $49.95', '4316 Model: $29.95 | 4320 Model: $49.95'),
        (r'5115', '折后 5115款: $21.95 | 5116款: $25.95', '5115 Model: $21.95 | 5116 Model: $25.95'),
        (r'2036', '折后 $49.95', '$49.95'),
        (r'4411', '折后 $22.00', '$22.00'),
        (r'5107', '折后 $49.95', '$49.95'),
        (r'2052BK', '折后 $23.00', '$23.00'),
        (r'2050', '折后 喷涂款: $19.95 | 镀铬款: $21.95', 'Coated: $19.95 | Chrome: $21.95'),
        (r'2051BK', '折后 $12.95', '$12.95'),
        (r'2047BK', '折后 $22.00', '$22.00'),
        (r'2772', '折后 $21.95', '$21.95'),
        (r'2083', '折后 $19.95', '$19.95'),
        (r'2773', '折后 2773款: $21.95 | 2771款: $19.95', '2773 Model: $21.95 | 2771 Model: $19.95'),
        (r'2825', '折后 3层款: $49.95 | 6层款: $69.95', '3-Tier: $49.95 | 6-Tier: $69.95'),
        (r'2813', '折后 3层款: $24.95 | 4层款: $29.95 | 5层款: $36.95', '3-Tier: $24.95 | 4-Tier: $29.95 | 5-Tier: $36.95'),
        (r'2810', '折后 $39.95', '$39.95'),
        (r'2824', '折后 2824款: $49.95 | 2823款: $59.95', '2824 Model: $49.95 | 2823 Model: $59.95'),
        (r'4202', '折后 $17.95 - $49.95', '$17.95 - $49.95'),
        (r'4217', '折后 $25.00', '$25.00'),
        (r'4412', '折后 $49.95', '$49.95'),
        (r'2012BK', '折后 $19.95 - $21.95', '$19.95 - $21.95'),
    ]
    
    pages = [
        ('zh/bedroom/index.html', 'bedroom/index.html'),
        ('zh/living-room/index.html', 'living-room/index.html'),
        ('zh/dining/index.html', 'dining/index.html'),
        ('zh/office/index.html', 'office/index.html'),
    ]
    
    for zh_file, en_file in pages:
        with open(zh_file, 'r', encoding='utf-8') as f:
            zh_content = f.read()
        with open(en_file, 'r', encoding='utf-8') as f:
            en_content = f.read()
            
        for pattern, zh_pr, en_pr in price_corrections:
            # Match card in ZH
            # Look for cards whose <h3> contains pattern
            def replace_zh_price(match):
                card = match.group(0)
                if re.search(pattern, card, re.I):
                    # Replace whatever is in price-current or price-tag with zh_pr
                    card = re.sub(r'<span class=[\"\']price-current[\"\']>([^<]*)</span>', f'<span class="price-current">{zh_pr}</span>', card)
                    card = re.sub(r'<span class=[\"\']price-tag[\"\'][^>]*>([^<]*)</span>', f'<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{zh_pr}</span>', card)
                return card

            def replace_en_price(match):
                card = match.group(0)
                if re.search(pattern, card, re.I):
                    card = re.sub(r'<span class=[\"\']price-current[\"\']>([^<]*)</span>', f'<span class="price-current">{en_pr}</span>', card)
                    card = re.sub(r'<span class=[\"\']price-tag[\"\'][^>]*>([^<]*)</span>', f'<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{en_pr}</span>', card)
                return card

            # Card split matching
            zh_parts = re.split(r'(<div\s+class=[\"\']sofa-card[^\"\']*[\"\'][\s\S]*?</div>\s*</div>)', zh_content)
            zh_content = ''.join([replace_zh_price(re.match(r'.*', p)) if '<div class="sofa-card' in p or "<div class='sofa-card" in p else p for p in zh_parts])

            en_parts = re.split(r'(<div\s+class=[\"\']sofa-card[^\"\']*[\"\'][\s\S]*?</div>\s*</div>)', en_content)
            en_content = ''.join([replace_en_price(re.match(r'.*', p)) if '<div class="sofa-card' in p or "<div class='sofa-card" in p else p for p in en_parts])

        with open(zh_file, 'w', encoding='utf-8') as f:
            f.write(zh_content)
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(en_content)
            
    print("✓ Finished updating prices across all HTML pages.")

if __name__ == '__main__':
    fix_prices()
