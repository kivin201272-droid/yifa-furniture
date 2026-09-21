#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganize product catalog into dedicated functional categories:
1. Tables & Chairs Collection (dining/)
2. Sofas Collection (living-room/)
3. Beds Collection (bedroom/)
4. Wardrobes & Cabinets / Storage Collection (cabinets/)
5. Classic Mattresses (mattress/)
6. Massage Chairs (massage-chair/)
"""

import os
import re
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_cards_from_git(relpath):
    text = subprocess.check_output(["git", "show", f"HEAD:{relpath}"], text=True)
    cards = []
    idx = 0
    while True:
        pos = text.find('<div class="sofa-card', idx)
        if pos == -1:
            pos = text.find("<div class='sofa-card", idx)
        if pos == -1:
            pos = text.find('<div class="product-card', idx)
        if pos == -1:
            break
        
        depth = 0
        i = pos
        end = -1
        while i < len(text):
            if text[i:i+4] == "<div":
                depth += 1
                i += 4
            elif text[i:i+5] == "</div":
                depth -= 1
                i += 5
                if depth == 0:
                    end = text.find(">", i) + 1
                    break
            else:
                i += 1
        if end != -1:
            card_html = text[pos:end].strip()
            cards.append(card_html)
            idx = end
        else:
            break
    items = []
    for c in cards:
        m_title = re.search(r'<h3>(.*?)</h3>', c)
        title = m_title.group(1).strip() if m_title else ''
        items.append({'title': title, 'html': c})
    return items

def extract_wardrobe_cards(fpath, divider_marker):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    divider_pos = text.find(divider_marker)
    if divider_pos == -1:
        divider_pos = text.find("category-divider")
    block = text[text.find('<div class="sofa-grid">') + len('<div class="sofa-grid">'):divider_pos]
    raw_cards = re.split(r"(?=<div class=[\"\']sofa-card)", block)
    cards = []
    for rc in raw_cards:
        rc = rc.strip()
        if not rc:
            continue
        if rc.count("<div") == rc.count("</div") + 1:
            rc = rc + "\n        </div>"
        cards.append(rc)
    return cards

def run_migration():
    print("=== Starting Product Catalog Reorganization (Clean Balanced Divs) ===")

    # 1. Read existing cards from git HEAD
    dining_en_cards = extract_cards_from_git('dining/index.html')
    dining_zh_cards = extract_cards_from_git('zh/dining/index.html')

    office_en_cards = extract_cards_from_git('office/index.html')
    office_zh_cards = extract_cards_from_git('zh/office/index.html')

    living_en_cards = extract_cards_from_git('living-room/index.html')
    living_zh_cards = extract_cards_from_git('zh/living-room/index.html')

    bath_en_cards = extract_cards_from_git('bathroom-accessories/index.html')
    bath_zh_cards = extract_cards_from_git('zh/bathroom-accessories/index.html')

    # Read original 9 wardrobe cards
    existing_cabinets_en = extract_wardrobe_cards(os.path.join(BASE_DIR, 'cabinets/index.html'), '<!-- SECTION:')
    existing_cabinets_zh = extract_wardrobe_cards(os.path.join(BASE_DIR, 'zh/cabinets/index.html'), '<!-- 分类区隔：')

    print(f"Read counts -> Dining: {len(dining_en_cards)}, Office: {len(office_en_cards)}, Living: {len(living_en_cards)}, Cabinets: {len(existing_cabinets_en)}, Bath: {len(bath_en_cards)}")

    # 2. Extract items
    # Dining: 0-42 (43 items) tables & chairs; 43-46 (4 items) microwave/pantry cabinets
    dining_pure_tables_en = [c['html'] for c in dining_en_cards[:43]]
    dining_pure_tables_zh = [c['html'] for c in dining_zh_cards[:43]]

    dining_cabinets_en = [c['html'] for c in dining_en_cards[43:47]]
    dining_cabinets_zh = [c['html'] for c in dining_zh_cards[43:47]]

    # Office: 0-12, 14-23 (23 items) desks & chairs; index 13 (1 item) 2006GRAY filing cabinet
    office_desks_chairs_en = [c['html'] for i, c in enumerate(office_en_cards) if i != 13]
    office_desks_chairs_zh = [c['html'] for i, c in enumerate(office_zh_cards) if i != 13]

    office_filing_cabinet_en = [office_en_cards[13]['html']]
    office_filing_cabinet_zh = [office_zh_cards[13]['html']]

    # Living room: 0-87 (88 items) sofas; 88-116 (29 items) TV stands, bookcases, racks, carts
    living_pure_sofas_en = [c['html'] for c in living_en_cards[:88]]
    living_pure_sofas_zh = [c['html'] for c in living_zh_cards[:88]]

    living_cabinets_en = [c['html'] for c in living_en_cards[88:]]
    living_cabinets_zh = [c['html'] for c in living_zh_cards[88:]]

    # Bath: all 13 items are storage & space savers
    bath_storage_en = [c['html'] for c in bath_en_cards]
    bath_storage_zh = [c['html'] for c in bath_zh_cards]

    print(f"Divided items ->")
    print(f"  Dining tables & chairs: {len(dining_pure_tables_en)}")
    print(f"  Office desks & chairs: {len(office_desks_chairs_en)}")
    print(f"  Total Tables & Chairs: {len(dining_pure_tables_en) + len(office_desks_chairs_en)}")
    print(f"  Living pure sofas: {len(living_pure_sofas_en)}")
    print(f"  Total Cabinets & Storage: {len(existing_cabinets_en)} + {len(living_cabinets_en)} + {len(dining_cabinets_en)} + {len(office_filing_cabinet_en)} + {len(bath_storage_en)} = {len(existing_cabinets_en) + len(living_cabinets_en) + len(dining_cabinets_en) + len(office_filing_cabinet_en) + len(bath_storage_en)}")

    # 3. Build Tables & Chairs Pages (dining/index.html and zh/dining/index.html)
    divider_en = """
        <!-- SECTION: DESKS & OFFICE CHAIRS -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">Desks & Ergonomic Office Chairs</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">23 Items in Stock</span>
        </div>
"""
    divider_zh = """
        <!-- 分类区隔：办公书桌与人体工学电脑椅 -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">办公书桌与人体工学电脑椅</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">23 款现货直供</span>
        </div>
"""
    combined_tables_en_html = "\n".join(dining_pure_tables_en) + divider_en + "\n".join(office_desks_chairs_en)
    combined_tables_zh_html = "\n".join(dining_pure_tables_zh) + divider_zh + "\n".join(office_desks_chairs_zh)

    with open(os.path.join(BASE_DIR, 'dining/index.html'), 'r', encoding='utf-8') as f:
        din_en_text = f.read()
    with open(os.path.join(BASE_DIR, 'zh/dining/index.html'), 'r', encoding='utf-8') as f:
        din_zh_text = f.read()

    # In dining EN:
    din_en_text = re.sub(r'<title>.*?</title>', '<title>Tables & Chairs Collection | Modern Dining Sets, Desks & Office Chairs | Yifa</title>', din_en_text)
    din_en_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="Explore Yifa\'s Tables & Chairs Collection: modern marble dining tables, dining chairs, bar stools, ergonomic office chairs and study desks, wholesale from Brooklyn, NY.">', din_en_text)
    din_en_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="Tables & Chairs Collection | Modern Dining Sets, Desks & Office Chairs | Yifa"', din_en_text)
    din_en_text = re.sub(r'<span class=eyebrow>.*?</span>\s*<h2>.*?</h2>', '<span class=eyebrow>TABLES & CHAIRS</span>\n<h2>Tables & Chairs Collection</h2>', din_en_text)
    din_en_text = re.sub(r'<h1>.*?</h1>', '<h1>Tables & Chairs Collection</h1>', din_en_text)

    din_en_grid_start = din_en_text.find('<div class="sofa-grid">')
    new_din_en = din_en_text[:din_en_grid_start + len('<div class="sofa-grid">')] + "\n" + combined_tables_en_html + "\n    </div>\n</main>" + din_en_text[din_en_text.find('<footer class=site-footer>', din_en_grid_start):]

    # In dining ZH:
    din_zh_text = re.sub(r'<title>.*?</title>', '<title>桌椅系列 | 现代餐桌椅、办公书桌与人体工学电脑椅 | 易发家具</title>', din_zh_text)
    din_zh_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="易发家具桌椅系列：精选意式轻奢大理石餐桌、伸缩折叠餐桌、现代软包餐椅、实木餐台、学习书桌、电脑桌、人体工学办公椅及吧台桌椅，纽约布鲁克林现货批发直销。">', din_zh_text)
    din_zh_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="桌椅系列 | 现代餐桌椅、办公书桌与人体工学电脑椅 | 易发家具"', din_zh_text)
    din_zh_text = re.sub(r'<span class=eyebrow>.*?</span>\s*<h2>.*?</h2>', '<span class=eyebrow>精选桌椅</span>\n<h2>桌椅系列</h2>', din_zh_text)
    din_zh_text = re.sub(r'<h1>.*?</h1>', '<h1>桌椅系列</h1>', din_zh_text)

    din_zh_grid_start = din_zh_text.find('<div class="sofa-grid">')
    new_din_zh = din_zh_text[:din_zh_grid_start + len('<div class="sofa-grid">')] + "\n" + combined_tables_zh_html + "\n    </div>\n</main>" + din_zh_text[din_zh_text.find('<footer class=site-footer>', din_zh_grid_start):]

    with open(os.path.join(BASE_DIR, 'dining/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_din_en)
    with open(os.path.join(BASE_DIR, 'zh/dining/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_din_zh)
    print("Updated dining/index.html and zh/dining/index.html successfully!")

    # 4. Build Cleaned Sofas Pages (living-room/index.html and zh/living-room/index.html)
    with open(os.path.join(BASE_DIR, 'living-room/index.html'), 'r', encoding='utf-8') as f:
        liv_en_text = f.read()
    with open(os.path.join(BASE_DIR, 'zh/living-room/index.html'), 'r', encoding='utf-8') as f:
        liv_zh_text = f.read()

    liv_en_text = re.sub(r'<title>.*?</title>', '<title>Sofas Collection | Modern Sectionals, Power Recliners & Sleeper Sofas | Yifa</title>', liv_en_text)
    liv_en_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="Explore Yifa\'s Sofas Collection: modern leather sofas, fabric sectionals, first-class power reclining sofas, and sleeper sofa beds, imported and distributed wholesale from Brooklyn, NY.">', liv_en_text)
    liv_en_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="Sofas Collection | Modern Sectionals, Power Recliners & Sleeper Sofas | Yifa"', liv_en_text)

    liv_zh_text = re.sub(r'<title>.*?</title>', '<title>沙发系列 | 现代真皮沙发、电动多功能转角沙发与沙发床 | 易发家具</title>', liv_zh_text)
    liv_zh_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="易发家具沙发系列：精选头等舱电动功能沙发、转角L型真皮沙发、高档科技布沙发及多功能折叠沙发床，纽约布鲁克林现货批发直销。">', liv_zh_text)
    liv_zh_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="沙发系列 | 现代真皮沙发、电动多功能转角沙发与沙发床 | 易发家具"', liv_zh_text)

    liv_en_grid_start = liv_en_text.find('<div class="sofa-grid">')
    new_liv_en = liv_en_text[:liv_en_grid_start + len('<div class="sofa-grid">')] + "\n" + "\n".join(living_pure_sofas_en) + "\n    </div>\n</main>" + liv_en_text[liv_en_text.find('<footer class=site-footer>', liv_en_grid_start):]

    liv_zh_grid_start = liv_zh_text.find('<div class="sofa-grid">')
    new_liv_zh = liv_zh_text[:liv_zh_grid_start + len('<div class="sofa-grid">')] + "\n" + "\n".join(living_pure_sofas_zh) + "\n    </div>\n</main>" + liv_zh_text[liv_zh_text.find('<footer class=site-footer>', liv_zh_grid_start):]

    with open(os.path.join(BASE_DIR, 'living-room/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_liv_en)
    with open(os.path.join(BASE_DIR, 'zh/living-room/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_liv_zh)
    print("Updated living-room/index.html and zh/living-room/index.html successfully!")

    # 5. Build Beds Pages (bedroom/index.html and zh/bedroom/index.html)
    with open(os.path.join(BASE_DIR, 'bedroom/index.html'), 'r', encoding='utf-8') as f:
        bed_en_text = f.read()
    with open(os.path.join(BASE_DIR, 'zh/bedroom/index.html'), 'r', encoding='utf-8') as f:
        bed_zh_text = f.read()

    bed_en_text = re.sub(r'<title>.*?</title>', '<title>Beds & Bedframes Collection | Upholstered Beds, Platform Beds & Bunk Beds | Yifa</title>', bed_en_text)
    bed_en_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="Explore Yifa\'s Beds Collection: Italian leather soft beds, solid wood platform beds, LED storage beds, and heavy-duty bunk beds, wholesale from Brooklyn, NY.">', bed_en_text)
    bed_en_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="Beds & Bedframes Collection | Upholstered Beds, Platform Beds & Bunk Beds | Yifa"', bed_en_text)

    bed_zh_text = re.sub(r'<title>.*?</title>', '<title>床系列 | 意式皮艺软床、现代实木储物床与LED氛围灯床 | 易发家具</title>', bed_zh_text)
    bed_zh_text = re.sub(r'<meta name=description content=\".*?\">', '<meta name=description content="易发家具床系列：意式极简皮艺软床、现代实木储物套房床、LED氛围灯平台床及双层高低床，纽约布鲁克林现货批发直销。">', bed_zh_text)
    bed_zh_text = re.sub(r'property=\"og:title\" content=\".*?\"', 'property="og:title" content="床系列 | 意式皮艺软床、现代实木储物床与LED氛围灯床 | 易发家具"', bed_zh_text)

    with open(os.path.join(BASE_DIR, 'bedroom/index.html'), 'w', encoding='utf-8') as f:
        f.write(bed_en_text)
    with open(os.path.join(BASE_DIR, 'zh/bedroom/index.html'), 'w', encoding='utf-8') as f:
        f.write(bed_zh_text)
    print("Updated bedroom/index.html and zh/bedroom/index.html titles successfully!")

    # 6. Build Cabinets Pages (cabinets/index.html and zh/cabinets/index.html)
    cab_divider_tv_en = """
        <!-- SECTION: TV STANDS & MEDIA CONSOLES -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">TV Stands & Media Entertainment Consoles</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">12 Items</span>
        </div>
"""
    cab_divider_tv_zh = """
        <!-- 分类区隔：电视柜与影音娱乐控制台 -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">电视柜与影音娱乐控制台</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">12 款现货</span>
        </div>
"""
    cab_divider_pantry_en = """
        <!-- SECTION: KITCHEN MICROWAVE CARTS & PANTRY CABINETS -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">Kitchen Microwave Carts & Pantry Cabinets</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">4 Items</span>
        </div>
"""
    cab_divider_pantry_zh = """
        <!-- 分类区隔：厨房微波炉收纳柜与储物高柜 -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">厨房微波炉收纳柜与储物高柜</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">4 款现货</span>
        </div>
"""
    cab_divider_racks_en = """
        <!-- SECTION: BOOKCASES, WIRE SHELVING, CARTS & GARMENT RACKS -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">Bookcases, Shelving Units, Carts & Garment Racks</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">18 Items</span>
        </div>
"""
    cab_divider_racks_zh = """
        <!-- 分类区隔：书架、置物货架、移动推车与重型衣物架 -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">书架、置物货架、移动推车与重型衣物架</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">18 款现货</span>
        </div>
"""
    cab_divider_bath_en = """
        <!-- SECTION: BATHROOM SPACE SAVERS & MODULAR SHELVING -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">Bathroom Space Savers & Modular Storage Shelving</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">13 Items</span>
        </div>
"""
    cab_divider_bath_zh = """
        <!-- 分类区隔：浴室马桶置物架与模块收纳矮柜 -->
        <div class="category-divider reveal" style="grid-column: 1 / -1; margin: 48px 0 24px; padding-bottom: 14px; border-bottom: 2px solid var(--accent); display: flex; align-items: baseline; justify-content: space-between;">
            <h2 style="font-size: 1.6rem; margin: 0; color: var(--ink);">浴室马桶置物架与模块收纳矮柜</h2>
            <span style="font-size: 0.95rem; color: var(--muted); font-weight: 500;">13 款现货</span>
        </div>
"""

    living_tv_en = living_cabinets_en[:12]
    living_tv_zh = living_cabinets_zh[:12]

    living_shelves_en = living_cabinets_en[12:]
    living_shelves_zh = living_cabinets_zh[12:]

    shelves_and_carts_en = living_shelves_en + office_filing_cabinet_en
    shelves_and_carts_zh = living_shelves_zh + office_filing_cabinet_zh

    all_cabinets_en_content = "\n".join(existing_cabinets_en) + \
                             cab_divider_tv_en + "\n".join(living_tv_en) + \
                             cab_divider_pantry_en + "\n".join(dining_cabinets_en) + \
                             cab_divider_racks_en + "\n".join(shelves_and_carts_en) + \
                             cab_divider_bath_en + "\n".join(bath_storage_en)

    all_cabinets_zh_content = "\n".join(existing_cabinets_zh) + \
                             cab_divider_tv_zh + "\n".join(living_tv_zh) + \
                             cab_divider_pantry_zh + "\n".join(dining_cabinets_zh) + \
                             cab_divider_racks_zh + "\n".join(shelves_and_carts_zh) + \
                             cab_divider_bath_zh + "\n".join(bath_storage_zh)

    with open(os.path.join(BASE_DIR, 'cabinets/index.html'), 'r', encoding='utf-8') as f:
        cab_en_text = f.read()
    with open(os.path.join(BASE_DIR, 'zh/cabinets/index.html'), 'r', encoding='utf-8') as f:
        cab_zh_text = f.read()

    cab_en_grid_start = cab_en_text.find('<div class="sofa-grid">')
    new_cab_en = cab_en_text[:cab_en_grid_start + len('<div class="sofa-grid">')] + "\n" + all_cabinets_en_content + "\n    </div>\n</main>" + cab_en_text[cab_en_text.find('<footer class=site-footer>', cab_en_grid_start):]

    cab_zh_grid_start = cab_zh_text.find('<div class="sofa-grid">')
    new_cab_zh = cab_zh_text[:cab_zh_grid_start + len('<div class="sofa-grid">')] + "\n" + all_cabinets_zh_content + "\n    </div>\n</main>" + cab_zh_text[cab_zh_text.find('<footer class=site-footer>', cab_zh_grid_start):]

    with open(os.path.join(BASE_DIR, 'cabinets/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_cab_en)
    with open(os.path.join(BASE_DIR, 'zh/cabinets/index.html'), 'w', encoding='utf-8') as f:
        f.write(new_cab_zh)
    print("Updated cabinets/index.html and zh/cabinets/index.html with all 56 storage products!")

    # 7. Update office pages with clear redirect notices
    office_notice_en = """<!doctype html><html lang=en><head>
<meta charset=UTF-8><meta http-equiv="refresh" content="2; url=../dining/">
<title>Redirecting to Tables & Chairs Collection | Yifa</title>
<script>window.location.replace('../dining/');</script>
<link rel=stylesheet href="../assets/css/style.css">
</head><body style="display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;font-family:sans-serif;">
<div>
<h2>Desks & Chairs have moved to our Tables & Chairs Collection</h2>
<p style="color:#666;margin:16px 0 24px;">Redirecting you now...</p>
<a href="../dining/" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#1d1d1f;color:#fff;text-decoration:none;border-radius:4px;">Go to Tables & Chairs Collection</a>
</div>
</body></html>"""

    office_notice_zh = """<!doctype html><html lang=zh><head>
<meta charset=UTF-8><meta http-equiv="refresh" content="2; url=../dining/">
<title>页面跳转中 - 桌椅系列 | 易发家具</title>
<script>window.location.replace('../dining/');</script>
<link rel=stylesheet href="../../assets/css/style.css">
</head><body style="display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;font-family:sans-serif;">
<div>
<h2>办公书桌与电脑椅已统一并入【桌椅系列】</h2>
<p style="color:#666;margin:16px 0 24px;">正在为您自动跳转...</p>
<a href="../dining/" class="btn btn-primary" style="display:inline-block;padding:12px 24px;background:#1d1d1f;color:#fff;text-decoration:none;border-radius:4px;">直接进入【桌椅系列】</a>
</div>
</body></html>"""

    with open(os.path.join(BASE_DIR, 'office/index.html'), 'w', encoding='utf-8') as f:
        f.write(office_notice_en)
    with open(os.path.join(BASE_DIR, 'zh/office/index.html'), 'w', encoding='utf-8') as f:
        f.write(office_notice_zh)
    print("Set office/index.html and zh/office/index.html to redirect to Tables & Chairs!")

    print("=== Core Migration Finished Successfully ===")

if __name__ == '__main__':
    run_migration()
