#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync navigation, page heroes, products overviews, homepages and footers across the site.
Core Categories:
1. 经典床垫 (Classic Mattresses) -> /mattress/
2. 沙发系列 (Sofas) -> /living-room/
3. 床系列 (Beds) -> /bedroom/
4. 桌椅系列 (Tables & Chairs) -> /dining/
5. 柜子系列 (Wardrobes & Cabinets) -> /cabinets/
6. 按摩椅系列 (Massage Chairs) -> /massage-chair/
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_page_heroes():
    print("--- Updating Page Heroes ---")

    # 1. Dining (Tables & Chairs)
    hero_dining_en = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><a href="../products/">Collections</a><span>/</span>Tables & Chairs</nav>
            <span class="eyebrow">TABLES & CHAIRS</span>
            <h1>Tables & Chairs Collection</h1>
            <p>Explore our complete collection of modern marble & solid wood dining tables, upholstered chairs, breakfast sets, computer desks, study desks, and ergonomic office chairs. Wholesale from Brooklyn, NY.</p>
        </div>
    </section>
"""
    hero_dining_zh = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">首页</a><span>/</span><a href="../products/">全部系列</a><span>/</span>桌椅系列</nav>
            <span class="eyebrow">精选桌椅</span>
            <h1>桌椅系列</h1>
            <p>精选轻奢大理石餐桌、岩板伸缩餐台、现代软包餐椅、实木餐椅、家用学习书桌、电脑桌、人体工学办公转椅及高脚吧椅，款式丰富，全美现货直发，一件也是批发价。</p>
        </div>
    </section>
"""
    with open(os.path.join(BASE_DIR, 'dining/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_dining_en, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'dining/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    with open(os.path.join(BASE_DIR, 'zh/dining/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_dining_zh, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'zh/dining/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    # 2. Living Room (Sofas)
    hero_living_en = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><a href="../products/">Collections</a><span>/</span>Sofas Collection</nav>
            <span class="eyebrow">LIVING ROOM SEATING</span>
            <h1>Sofas Collection</h1>
            <p>Premium genuine leather sofas, high-tech fabric sectionals, first-class power recliners, modular L-shape corner sofas, and multifunctional sleeper sofa beds. Available in stock for fast delivery.</p>
        </div>
    </section>
"""
    hero_living_zh = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">首页</a><span>/</span><a href="../products/">全部系列</a><span>/</span>沙发系列</nav>
            <span class="eyebrow">品质座驾</span>
            <h1>沙发系列</h1>
            <p>汇集意式轻奢真皮沙发、免洗科技布沙发、头等舱双电动多功能转角沙发、模块化组合贵妃榻及大容量储物折叠沙发床，纽约布鲁克林现货供应，一件也是批发价。</p>
        </div>
    </section>
"""
    with open(os.path.join(BASE_DIR, 'living-room/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_living_en, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'living-room/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    with open(os.path.join(BASE_DIR, 'zh/living-room/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_living_zh, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'zh/living-room/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    # 3. Bedroom (Beds)
    hero_bed_en = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><a href="../products/">Collections</a><span>/</span>Beds & Bedframes</nav>
            <span class="eyebrow">BEDROOM FURNITURE</span>
            <h1>Beds & Bedframes Collection</h1>
            <p>Italian minimalist leather soft beds, solid wood storage bed suites, modern LED ambient platform beds, heavy-duty metal bunk beds, and foldable bases. Direct wholesale from Brooklyn, NY.</p>
        </div>
    </section>
"""
    hero_bed_zh = """<main id=main>
    <section class="page-hero">
        <div class="container">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="../">首页</a><span>/</span><a href="../products/">全部系列</a><span>/</span>床系列</nav>
            <span class="eyebrow">舒适睡眠</span>
            <h1>床系列</h1>
            <p>精选意式极简轻奢真皮软床、现代实木高箱储物套房床、智能无线充皮床、LED氛围灯平台床、实木双层高低床及免安装折叠床架，纽约布鲁克林仓库现货，一件也是批发价。</p>
        </div>
    </section>
"""
    with open(os.path.join(BASE_DIR, 'bedroom/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_bed_en, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'bedroom/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    with open(os.path.join(BASE_DIR, 'zh/bedroom/index.html'), 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<main id=main>.*?(?=<div class=\"sofa-grid\">)', hero_bed_zh, c, flags=re.DOTALL)
    with open(os.path.join(BASE_DIR, 'zh/bedroom/index.html'), 'w', encoding='utf-8') as f:
        f.write(c)

    print("Page heroes updated successfully!")

def update_products_pages():
    print("--- Updating products/index.html & zh/products/index.html ---")

    # English products/index.html
    en_path = os.path.join(BASE_DIR, 'products/index.html')
    with open(en_path, 'r', encoding='utf-8') as f:
        en_content = f.read()

    en_splits = """<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/mattress-collection.jpg?v=20260920" alt="Classic Mattresses Collection" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 01</span>
<h2>Classic Mattresses</h2>
<p>Featuring Beautyrest Black, Magical Mattress series, 5-star luxury hotel mattresses, and natural coconut palm spinal support mattresses. Available in soft, medium, and firm comfort levels.</p>
<ul class="tick-list">
<li>Simmons Beautyrest Black & 5-Star Hotel grade quality</li>
<li>Magical Mattress high-resilience memory foam & latex</li>
<li>2.1mm extra-thick silent pocket springs & coconut palm</li>
<li>Direct wholesale prices with up to 20-year warranty</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../mattress/">Explore Mattresses</a></p>
</div>
</div>

<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/collection-living-room.jpg?v=20260907" alt="Sofas Collection" width="900" height="659" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 02</span>
<h2>Sofas Collection</h2>
<p>Modern silhouettes, wear-resistant high-tech fabrics, and top-grain Italian leather sofas engineered for ultimate comfort and living room elegance.</p>
<ul class="tick-list">
<li>First-class power reclining sectionals</li>
<li>Curved & modular L-shape corner sofas</li>
<li>High-tech easy-clean fabric & genuine leather</li>
<li>Multifunctional fold-out sleeper sofa beds with storage</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../living-room/">Explore Sofas</a></p>
</div>
</div>

<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/collection-bedroom.jpg?v=20260921_newbed" alt="Beds Collection" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 03</span>
<h2>Beds & Bedframes Collection</h2>
<p>Complete bedroom sleeping solutions — from Italian minimalist soft beds to solid wood hydraulic storage platform beds and heavy-duty bunk beds.</p>
<ul class="tick-list">
<li>Italian luxury genuine leather & upholstered soft beds</li>
<li>Hydraulic storage & high-box solid wood bed frames</li>
<li>Integrated ambient LED lighting headboards</li>
<li>Solid wood twin & full bunk beds & folding metal bases</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../bedroom/">Explore Beds</a></p>
</div>
</div>

<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/collection-dining.jpg?v=20260907" alt="Tables & Chairs Collection" width="900" height="506" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 04</span>
<h2>Tables & Chairs Collection</h2>
<p>Cohesive modern dining and workspace furniture: marble dining tables, matching upholstered chairs, breakfast nook sets, study desks, and ergonomic office chairs.</p>
<ul class="tick-list">
<li>Real marble & sintered stone extendable dining tables</li>
<li>Designer upholstered dining chairs & bar stools</li>
<li>Study writing desks & computer workstations</li>
<li>Ergonomic mesh & padded executive office swivel chairs</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../dining/">Explore Tables & Chairs</a></p>
</div>
</div>

<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/collection-cabinets.jpg" alt="Wardrobes & Cabinets Collection" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 05</span>
<h2>Wardrobes & Cabinets Collection</h2>
<p>Versatile whole-home storage solutions: multi-door wardrobes with mirrors, breathable shoe cabinets, TV consoles, bookcases, microwave carts, and space-saver units.</p>
<ul class="tick-list">
<li>2-door, 3-door wardrobes & mirrored solid wood armoires</li>
<li>Louvered breathable entryway shoe cabinets & vertical chests</li>
<li>Electric fireplace media consoles & wide TV entertainment centers</li>
<li>Microwave carts, bookcases, garment racks & over-the-toilet space savers</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../cabinets/">Explore Wardrobes & Cabinets</a></p>
</div>
</div>

<div class="split reverse">
<div class="split-media reveal">
<img src="../assets/images/massage-chair/D09.png" alt="Deluxe Massage Chairs Collection" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Core Collection 06</span>
<h2>Massage Chairs Collection</h2>
<p>High-tech zero-gravity luxury smart massage chairs with full-body air bags, intelligent 4D mechanisms, and therapeutic heating for total wellness.</p>
<ul class="tick-list">
<li>Full-body zero-gravity capsule massage systems</li>
<li>Intelligent multi-gear body-scan robotic mechanisms</li>
<li>Therapeutic heat compress & Bluetooth surround sound</li>
<li>Wholesale pricing direct with professional customer support</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../massage-chair/">Explore Massage Chairs</a></p>
</div>
</div>"""

    # Chinese products/index.html
    zh_path = os.path.join(BASE_DIR, 'zh/products/index.html')
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_content = f.read()

    zh_splits = """<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/mattress-collection.jpg?v=20260920" alt="经典床垫系列" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 01</span>
<h2>经典床垫系列</h2>
<p>汇聚美国席梦思黑标 (Beautyrest Black)、美国神奇床垫、五星级酒店专供床垫、天然椰棕护脊硬垫与加厚高弹乳胶独立袋装弹簧床垫，全美现货直发。</p>
<ul class="tick-list">
<li>美国席梦思黑标与五星级酒店专供品质</li>
<li>美国神奇床垫科技睡眠，软、硬、中软三档睡感</li>
<li>天然椰棕强劲护脊与2.1加粗静音独立袋装弹簧</li>
<li>官方质保长达20年，一件也是批发价</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../mattress/">点此探索经典床垫</a></p>
</div>
</div>

<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/collection-living-room.jpg?v=20260907" alt="沙发系列" width="900" height="659" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 02</span>
<h2>沙发系列</h2>
<p>现代意式极简轮廓与耐磨免洗科技布、头层真皮材质，为您客厅打造视觉焦点与极致坐卧享受。</p>
<ul class="tick-list">
<li>头等舱双电动多功能转角沙发</li>
<li>弧形转角皮艺沙发与模块化贵妃榻组合</li>
<li>易打理免洗科技布与意式轻奢真皮面料</li>
<li>大容量储物多功能折叠沙发床</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../living-room/">点此探索沙发系列</a></p>
</div>
</div>

<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/collection-bedroom.jpg?v=20260921_newbed" alt="床系列" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 03</span>
<h2>床系列</h2>
<p>高品质现代卧室床架专场 —— 从意式轻奢皮艺软床、高箱储物床到自带LED氛围灯床架与实木双层高低床。</p>
<ul class="tick-list">
<li>意式极简真皮软包床与高背拉点平台床</li>
<li>实木液压高箱储物床与多抽屉床组</li>
<li>智能无线充电与LED氛围灯科技床架</li>
<li>加粗加厚实木/金属双层高低床与免安装折叠底架</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../bedroom/">点此探索床系列</a></p>
</div>
</div>

<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/collection-dining.jpg?v=20260907" alt="桌椅系列" width="900" height="506" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 04</span>
<h2>桌椅系列</h2>
<p>易于搭配的现代餐厅与工作空间家具，完美适配家庭用餐、开放式厨房、书房与商务办公。</p>
<ul class="tick-list">
<li>大理石与岩板伸缩折叠餐桌、圆变方餐台</li>
<li>精美软包餐椅、高脚吧椅及早餐角转角卡座</li>
<li>现代家用书桌、电脑桌及折叠便携工作台</li>
<li>人体工学透气网布转椅与高级皮革办公转椅</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../dining/">点此探索桌椅系列</a></p>
</div>
</div>

<div class="split" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/collection-cabinets.jpg" alt="柜子与收纳系列" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 05</span>
<h2>柜子与收纳系列</h2>
<p>精选实用双门/三门大衣柜、豪华镜面实木衣柜、玄关百叶鞋柜、现代电视影音柜、多层书架、厨房微波炉柜及浴室置物架。</p>
<ul class="tick-list">
<li>双门/三门带抽屉衣柜与豪华带镜实木大衣柜</li>
<li>玄关百叶防潮透气鞋柜与垂直加高五斗柜</li>
<li>现代壁炉电视柜与超宽平移电视影音控制台</li>
<li>厨房微波炉推车、商用重型衣物架及马桶置物架</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../cabinets/">点此探索柜子系列</a></p>
</div>
</div>

<div class="split reverse">
<div class="split-media reveal">
<img src="../../assets/images/massage-chair/D09.png" alt="豪华智能按摩椅" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">核心系列 06</span>
<h2>按摩椅系列</h2>
<p>全系列高科技零重力智能按摩椅，人体工学太空舱设计，全身气囊与机械手机芯深度按摩，带来极致放松体验。</p>
<ul class="tick-list">
<li>豪华多功能全自动智能按摩系统</li>
<li>太空舱零重力智能机芯与全身气囊包裹</li>
<li>多档力度调节、热敷理疗与蓝牙音响</li>
<li>现货正品，一件也是批发价</li>
</ul>
<p style="margin-top:24px"><a class="btn-red-banner" href="../massage-chair/">点此探索按摩椅系列</a></p>
</div>
</div>"""

    # Inject into EN
    s_en = en_content.find('<div class="container"><div class="split"')
    if s_en == -1:
        s_en = en_content.find('<div class=container><div class="split"')
    e_en = en_content.find('</section></main>', s_en)
    en_new = en_content[:s_en] + '<div class="container">\n' + en_splits + '\n</div>' + en_content[e_en:]
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_new)

    # Inject into ZH
    s_zh = zh_content.find('<div class="container"><div class="split"')
    if s_zh == -1:
        s_zh = zh_content.find('<div class=container><div class="split"')
    e_zh = zh_content.find('</section></main>', s_zh)
    zh_new = zh_content[:s_zh] + '<div class="container">\n' + zh_splits + '\n</div>' + zh_content[e_zh:]
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_new)

    print("Updated products/index.html and zh/products/index.html successfully!")

def update_homepages():
    print("--- Updating index.html & zh/index.html Collection Grids ---")

    home_grid_en = """<div class=collection-grid>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/mattress-collection.jpg?v=20260920" alt="Classic Mattresses" width=900 height=900 loading=lazy></div><div class=cc-body><h3>Classic Mattresses</h3><p>Simmons Beautyrest Black, Magical Mattress series, 5-star hotel mattresses, and natural spinal palm mattresses for deep sleep.</p><a class=cc-link href=./mattress/>View Mattresses</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/collection-bedroom.jpg?v=20260921_newbed" alt="Beds Collection" width=900 height=900 loading=lazy></div><div class=cc-body><h3>Beds</h3><p>Italian luxury leather soft beds, solid wood storage bed frames, ambient LED platform beds, and heavy-duty bunk beds.</p><a class=cc-link href=./bedroom/>View Beds</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/collection-living-room.jpg?v=20260907" alt="Sofas Collection" width=900 height=659 loading=lazy></div><div class=cc-body><h3>Sofas</h3><p>Power reclining sectionals, curved corner sofas, high-tech fabric and Italian genuine leather seating, plus sofa beds.</p><a class=cc-link href=./living-room/>View Sofas</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/collection-dining.jpg?v=20260907" alt="Tables & Chairs Collection" width=900 height=506 loading=lazy></div><div class=cc-body><h3>Tables & Chairs</h3><p>Marble & wood dining tables, upholstered chairs, bar stools, home study desks, and ergonomic office swivel chairs.</p><a class=cc-link href=./dining/>View Tables & Chairs</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/collection-cabinets.jpg" alt="Wardrobes & Cabinets" width=900 height=900 loading=lazy></div><div class=cc-body><h3>Wardrobes & Cabinets</h3><p>Double & triple door wardrobes, mirrored armoires, entryway shoe cabinets, vertical chests, TV stands, and shelving units.</p><a class=cc-link href=./cabinets/>View Cabinets</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="assets/images/massage-chair/D09.png?v=20260921_hd" alt="Deluxe Massage Chairs" width=900 height=900 loading=lazy></div><div class=cc-body><h3>Massage Chairs</h3><p>Zero-gravity luxury smart massage chairs with full-body air bags and intelligent mechanisms for complete relaxation.</p><a class=cc-link href=./massage-chair/>View Massage Chairs</a></div></article>
</div>"""

    home_grid_zh = """<div class=collection-grid>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/mattress-collection.jpg?v=20260920" alt="经典床垫" width=900 height=900 loading=lazy></div><div class=cc-body><h3>经典床垫</h3><p>美国席梦思黑标、神奇科技床垫、五星级酒店床垫与天然椰棕护脊硬垫，尽享极致深睡。</p><a class=cc-link href=./mattress/>查看经典床垫</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/collection-bedroom.jpg?v=20260921_newbed" alt="床系列" width=900 height=900 loading=lazy></div><div class=cc-body><h3>床系列</h3><p>意式极简真皮软床、现代实木储物套房床、智能LED氛围灯平台床及双层高低床。</p><a class=cc-link href=./bedroom/>查看床系列</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/collection-living-room.jpg?v=20260907" alt="沙发系列" width=900 height=659 loading=lazy></div><div class=cc-body><h3>沙发系列</h3><p>头等舱双电动多功能沙发、转角L型真皮沙发、高档免洗科技布沙发及多功能折叠沙发床。</p><a class=cc-link href=./living-room/>查看沙发系列</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/collection-dining.jpg?v=20260907" alt="桌椅系列" width=900 height=506 loading=lazy></div><div class=cc-body><h3>桌椅系列</h3><p>精选大理石餐桌、软包餐椅、吧台桌椅，以及现代学习书桌与人体工学电脑办公转椅。</p><a class=cc-link href=./dining/>查看桌椅系列</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/collection-cabinets.jpg" alt="柜子系列" width=900 height=900 loading=lazy></div><div class=cc-body><h3>柜子系列</h3><p>实用大衣柜、豪华镜面实木衣柜、百叶透气鞋柜、现代电视柜、微波炉柜及置物架。</p><a class=cc-link href=./cabinets/>查看柜子系列</a></div></article>
<article class="collection-card reveal"><div class=cc-img><img src="../assets/images/massage-chair/D09.png?v=20260921_hd" alt="豪华智能按摩椅" width=900 height=900 loading=lazy></div><div class=cc-body><h3>按摩椅系列</h3><p>全系列高科技零重力智能按摩椅，太空舱设计，全身气囊与机械手机芯深度按摩，极致放松。</p><a class=cc-link href=./massage-chair/>查看按摩椅系列</a></div></article>
</div>"""

    # Update index.html
    en_path = os.path.join(BASE_DIR, 'index.html')
    with open(en_path, 'r', encoding='utf-8') as f:
        en_t = f.read()
    en_t = re.sub(r'<div class=collection-grid>.*?</div></div></section>', home_grid_en + '</div></section>', en_t, flags=re.DOTALL)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_t)

    # Update zh/index.html
    zh_path = os.path.join(BASE_DIR, 'zh/index.html')
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_t = f.read()
    zh_t = re.sub(r'<div class=collection-grid>.*?</div></div></section>', home_grid_zh + '</div></section>', zh_t, flags=re.DOTALL)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_t)

    print("Updated index.html and zh/index.html successfully!")

def sync_footers():
    print("--- Syncing Footers Across All HTML Files ---")

    # The footer items in Chinese:
    # <li><a href=.../products/>全部系列</a></li>
    # <li><a href=.../mattress/>经典床垫</a></li>
    # <li><a href=.../living-room/>沙发系列</a></li>
    # <li><a href=.../bedroom/>床系列</a></li>
    # <li><a href=.../dining/>桌椅系列</a></li>
    # <li><a href=.../cabinets/>柜子系列</a></li>
    # <li><a href=.../massage-chair/>按摩椅系列</a></li>

    # The footer items in English:
    # <li><a href=.../products/>Collections</a></li>
    # <li><a href=.../mattress/>Classic Mattresses</a></li>
    # <li><a href=.../living-room/>Sofas</a></li>
    # <li><a href=.../bedroom/>Beds</a></li>
    # <li><a href=.../dining/>Tables & Chairs</a></li>
    # <li><a href=.../cabinets/>Wardrobes & Cabinets</a></li>
    # <li><a href=.../massage-chair/>Massage Chairs</a></li>

    import glob
    html_files = glob.glob(os.path.join(BASE_DIR, '**/*.html'), recursive=True)
    count = 0
    for hf in html_files:
        if 'node_modules' in hf or 'scratch' in hf or '.git' in hf:
            continue
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()

        is_zh = '/zh/' in hf or hf.endswith('/zh/index.html')
        # Determine prefix for footer links
        # Depth calculation
        rel_from_base = os.path.relpath(hf, BASE_DIR)
        depth = len(rel_from_base.split(os.sep)) - 1
        
        if is_zh:
            # Inside zh/
            # If at zh/index.html (depth 1): links are ./products/, ./mattress/, etc.
            # If at zh/bedroom/index.html (depth 2): links are ../products/, ../mattress/, etc.
            pfx = './' if depth == 1 else '../'
            new_list = f"""<ul><li><a href={pfx}products/>全部系列</a></li><li><a href={pfx}mattress/>经典床垫</a></li><li><a href={pfx}living-room/>沙发系列</a></li><li><a href={pfx}bedroom/>床系列</a></li><li><a href={pfx}dining/>桌椅系列</a></li><li><a href={pfx}cabinets/>柜子系列</a></li><li><a href={pfx}massage-chair/>按摩椅系列</a></li></ul>"""
            
            # Replace Chinese footer collections
            pattern = re.compile(r'<h3>产品分类</h3>\s*<ul>.*?</ul>', re.DOTALL)
            if pattern.search(content):
                content = pattern.sub(f'<h3>产品分类</h3>{new_list}', content)
                with open(hf, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
        else:
            # Inside EN
            # If at index.html (depth 0): links are ./products/, ./mattress/, etc.
            # If at bedroom/index.html (depth 1): links are ../products/, ../mattress/, etc.
            pfx = './' if depth == 0 else '../'
            new_list = f"""<ul><li><a href={pfx}products/>Collections</a></li><li><a href={pfx}mattress/>Classic Mattresses</a></li><li><a href={pfx}living-room/>Sofas</a></li><li><a href={pfx}bedroom/>Beds</a></li><li><a href={pfx}dining/>Tables & Chairs</a></li><li><a href={pfx}cabinets/>Wardrobes & Cabinets</a></li><li><a href={pfx}massage-chair/>Massage Chairs</a></li></ul>"""

            pattern = re.compile(r'<h3>(?:Collections|Products)</h3>\s*<ul>.*?</ul>', re.DOTALL)
            if pattern.search(content):
                content = pattern.sub(f'<h3>Collections</h3>{new_list}', content)
                with open(hf, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1

    print(f"Synced footers across {count} HTML files!")

if __name__ == '__main__':
    update_page_heroes()
    update_products_pages()
    update_homepages()
    sync_footers()
    print("=== All Site Updates Completed Successfully ===")
