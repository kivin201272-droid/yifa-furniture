import re, os

# Define incremental cards to add per category
# (title_zh, title_en, desc_zh, desc_en, img_rel, price_zh, price_en, tags_zh, tags_en)

dining_extra = [
    ('4160 / 4130 木餐桌 + 4110 实木餐椅', '4160 / 4130 Dining Table + 4110 Dining Chairs', '经典实木纹理餐桌，搭配高密度实木餐椅 (GREEN / IVY / GRAY)，温润质感与稳固支撑。', 'Solid wood dining table with matching high-density dining chairs in Green, Ivy, or Gray.', 'pj_dining/p6_img_10_204.jpg', '折后 4160木餐桌: $139.00 | 4130木餐桌: $109.00 | 4110实木餐椅: $59.95/把', '4160 Table: $139.00 | 4130 Table: $109.00 | 4110 Chair: $59.95/ea', ['实木餐桌椅', '经典款'], ['Solid Wood', 'Classic']),
    ('3016T / 3000WH 轻奢大理石餐桌组合', '3016T / 3000WH Luxury Marble Dining Set', '轻奢纯白大理石台面餐桌，搭配 1600 / 1003 / 1500 镀金轻奢软包餐椅，优雅奢华。', 'Luxury white marble top dining table paired with premium gold-framed upholstered chairs.', 'pj_dining/p6_img_11_205.jpg', '折后 3016T餐桌: $549.00 | 1600/1003餐椅: $149.00 | 1500餐椅: $99.00', '3016T Table: $549.00 | 1600/1003 Chair: $149.00 | 1500 Chair: $99.00', ['大理石餐桌', '轻奢镀金'], ['Marble Top', 'Gold Frame']),
    ('3010T / 3011T 黑白大理石餐桌组合', '3010T / 3011T Marble Dining Collection', '现代黑白双色大理石餐台，配 1003BK / 2680BK / 1002WH 镀金轻奢餐椅。', 'Modern black and white marble dining tables with gold-plated designer chairs.', 'pj_dining/p6_img_12_207.jpg', '折后 3011T餐桌: $549.00 | 3010T餐桌: $499.00 | 餐椅: $85.00 - $149.00', '3011T Table: $549.00 | 3010T Table: $499.00 | Chairs: $85.00 - $149.00', ['天然大理石', '黑白经典'], ['Marble Top', 'Modern']),
    ('3012T 现代大理石餐桌组合', '3012T Modern Marble Dining Set', '现代纯白/深灰大理石台面，配 2680 镀铬金属脚软包餐椅。', 'Contemporary marble dining table with chrome frame upholstered dining chairs.', 'pj_dining/p6_img_13_209.jpg', '折后 3012T餐桌: $499.00 | 2680餐椅: $79.00', '3012T Table: $499.00 | 2680 Chair: $79.00', ['灰白大理石', '镀铬金属'], ['Marble Top', 'Chrome']),
    ('3000T / 3002 大理石与钢化玻璃餐桌组合', '3000T / 3002 Marble & Glass Dining Collection', '多款式大理石与加厚钢化玻璃餐台，配 1200 / 1500 / 1301 / 1001 舒适皮艺餐椅。', 'Versatile marble and tempered glass dining tables with ergonomic dining chairs.', 'pj_dining/p6_img_14_211.jpg', '折后 3000T大理石餐桌: $399.00 | 3002玻璃餐桌: $349.00 | 餐椅: $89.00 - $149.00', '3000T Marble: $399.00 | 3002 Glass: $349.00 | Chairs: $89.00 - $149.00', ['玻璃/大理石', '多款可选'], ['Glass / Marble', 'Popular']),
    ('3008T / 3007T 现代大理石与玻璃餐桌', '3008T / 3007T Dining Set with Marble & Glass', '22mm 加厚灰大理石与 12mm 纯白钢化玻璃台面，配 1401BK / 1200GRAY 优质餐椅。', '22mm gray marble and 12mm white glass top dining tables with modern dining chairs.', 'pj_dining/p7_img_10_250.jpg', '折后 3008T餐桌: $399.00 | 3007T餐桌: $349.00 | 餐椅: $89.00 - $99.00', '3008T Table: $399.00 | 3007T Table: $349.00 | Chairs: $89.00 - $99.00', ['加厚台面', '精湛工艺'], ['Thick Top', 'Premium']),
    ('3102T / 3112T / 3101T 现代钢化玻璃餐桌组合', '3102T / 3112T / 3101T Glass Dining Sets', '多尺寸钢化玻璃餐桌 (30x48 / 36x60)，配 2680 / 2800 镀铬餐椅。', 'Various sizes tempered glass dining tables with chrome welded dining chairs.', 'pj_dining/p7_img_11_252.jpg', '折后 3102T: $149.00 | 3101T: $129.00 | 3112T: $119.00 | 餐椅: $35.00 - $79.00', '3102T: $149.00 | 3101T: $129.00 | 3112T: $119.00 | Chairs: $35.00 - $79.00', ['钢化玻璃', '多规格'], ['Tempered Glass', 'Multi-Size']),
    ('3104T / 3114T / 3103T / 3105T / 3106T 镀金轻奢玻璃餐桌', '3104T / 3114T / 3103T / 3105T / 3106T Gold Glass Dining Sets', '轻奢镀金金属脚钢化玻璃餐桌，配 2650 / 2800 镀金高背餐椅。', 'Gold frame tempered glass dining tables with matching gold-accented high-back chairs.', 'pj_dining/p7_img_12_253.jpg', '折后 3104T: $159.00 | 3103T: $139.00 | 3106T: $139.00 | 3114T: $129.00 | 3105T: $119.00', '3104T: $159.00 | 3103T: $139.00 | 3106T: $139.00 | 3114T: $129.00 | 3105T: $119.00', ['轻奢镀金', '高背餐椅'], ['Gold Frame', 'Luxury']),
    ('2240 / 2250 简约钢木玻璃餐桌', '2240 / 2250 Minimalist Glass Dining Sets', '简约现代钢化玻璃餐桌，搭配 2800 黑色金属餐椅，经济实用。', 'Clean modern tempered glass dining tables with sturdy 2800 black metal chairs.', 'pj_dining/p7_img_13_255.jpg', '折后 2240餐桌: $75.00 | 2250餐桌: $59.00 | 2800餐椅: $30.00', '2240 Table: $75.00 | 2250 Table: $59.00 | 2800 Chair: $30.00', ['高性价比', '经济实用'], ['Value', 'Durable']),
    ('4031T 仿大理石餐桌 & 3003T 大理石餐桌', '4031T / 3003T Faux & Real Marble Dining Sets', '4031T 经典仿大理石餐台与 3003T 豪华大理石餐台，配 4026CA 实木椅与 2650BK 金属椅。', 'Classic faux marble and genuine marble dining tables with matching solid wood & metal chairs.', 'pj_dining/p8_img_10_282.jpg', '折后 3003T: $179.00 | 4031T: $139.00 | 4026CA餐椅: $49.95 | 2650BK餐椅: $65.00', '3003T: $179.00 | 4031T: $139.00 | 4026CA Chair: $49.95 | 2650BK Chair: $65.00', ['大理石质感', '稳固承重'], ['Marble Finish', 'Sturdy']),
    ('2206T / 2216T 经典一桌四椅套组', '2206T / 2216T Classic 5-PC Dining Sets', '经典餐厅一桌四椅完整套组，高性价比家庭用餐首选。', 'Complete 5-piece dining sets with 1 table and 4 matching chairs for family dining.', 'pj_dining/p8_img_11_284.jpg', '折后 一桌四椅套组: $199.00 | 单餐桌: $89.00 | 单餐椅: $39.00', '5-PC Set: $199.00 | Table: $89.00 | Chair: $39.00', ['一桌四椅', '畅销套装'], ['5-PC Set', 'Best Value']),
    ('4002 / 4154 / 4158 / 4159 / 4138 现代实木与折叠餐桌系列', '4002 / 4154 / 4158 / 4159 / 4138 Wood & Folding Dining Tables', '包含 4138 折叠圆桌、4158/4159 实木餐桌与 4002 紧凑型餐桌，配 4102/4108/4109 实木餐椅。', 'Versatile selection of folding and solid wood dining tables with matching wooden chairs.', 'pj_dining/p8_img_12_285.jpg', '折后 4154: $95.00 | 4138折叠桌: $92.00 | 4158/4159: $89.00 | 4002: $85.00 | 配套餐椅: $39.95 - $42.00', '4154: $95.00 | 4138 Folding: $92.00 | 4158/4159: $89.00 | 4002: $85.00 | Chairs: $39.95 - $42.00', ['折叠/实木', '空间灵动'], ['Folding / Wood', 'Space Saving']),
    ('4003 / 4114 / 4009 多功能简易早餐桌椅套组', '4003 / 4114 / 4009 Breakfast Nook Table Sets', '多款式 3 件套与 5 件套早餐吧台桌椅组合，小户型与公寓厨房绝配。', 'Compact 3-piece and 5-piece breakfast nook table sets ideal for apartments and breakfast spaces.', 'pj_dining/p8_img_13_287.jpg', '折后 4114 5件套: $179.00 | 4003 3件套: $119.00 | 4009 3件套: $89.00', '4114 5-PC: $179.00 | 4003 3-PC: $119.00 | 4009 3-PC: $89.00', ['早餐吧台', '3/5件套'], ['Breakfast Set', '3/5-PC']),
    ('2391 / 2235 现代金属吧台桌与 2370 / 2371 升降吧台椅', '2391 / 2235 Bar Tables & 2370 / 2371 Bar Stools', '高脚圆形/矩形金属吧台桌，搭配多色升降旋转皮艺高脚吧台椅。', 'High-top metal bar tables with height-adjustable swivel bar stools in multiple colors.', 'pj_dining/p9_img_10_318.jpg', '折后 2235吧台桌: $129.00 | 2391吧台桌: $45.00 | 2371吧椅: $45.00 | 2370吧椅: $29.95', '2235 Bar Table: $129.00 | 2391 Bar Table: $45.00 | 2371 Stool: $45.00 | 2370 Stool: $29.95', ['升降吧椅', '现代吧台'], ['Bar Stool', 'Bar Table']),
    ('2524 (ESP / BK / WH) 现代多功能微波炉置物柜', '2524 (ESP / BK / WH) Microwave Cart', '多层多格大容量收纳，上层微波炉专属台面，下层双门储物柜。', 'Multi-tier microwave storage cabinet with spacious countertop and bottom cabinet doors.', 'pj_dining/pj-2524.jpg', '折后 $65.00', '$65.00', ['微波炉柜', '大容量'], ['Microwave Cart', 'Storage']),
    ('2526 (BK / WH) 双层微波炉收纳推车', '2526 (BK / WH) Rolling Microwave Cart', '带万向静音刹车轮，移动灵巧，双层隔板收纳锅具与小家电。', 'Compact rolling microwave cart with lockable casters for kitchen convenience.', 'pj_dining/pj-2526.jpg', '折后 $49.95', '$49.95', ['移动滚轮', '双层收纳'], ['Rolling Wheels', 'Compact']),
    ('4405 (WH / N) 实用厨房微波炉柜', '4405 (WH / N) Kitchen Microwave Cabinet', '现代双门带抽屉微波炉多功能高柜，防潮防污易打理。', 'Versatile tall kitchen cabinet with drawer and microwave shelf, moisture resistant.', 'pj_dining/pj-4405.jpg', '折后 $65.00', '$65.00', ['多功能抽屉', '厨房储物'], ['With Drawer', 'Kitchen Storage']),
    ('4406 (N / WH) 现代厨房双门收纳高柜', '4406 (N / WH) Tall Kitchen Pantry Cabinet', '双门多层加高收纳柜，大容量收纳干货餐具，厨房整洁利落。', 'Tall double-door pantry cabinet with adjustable shelving for generous kitchen storage.', 'pj_dining/pj-4406.jpg', '折后 $99.95', '$99.95', ['双门高柜', '大容量'], ['Pantry Cabinet', 'Generous Space']),
]

office_extra = [
    ('2715 现代简易电脑桌', '2715 Modern Minimalist Computer Desk', '极简金属框架与耐磨防水木纹台面，稳固耐用。', 'Minimalist metal frame desk with durable water-resistant tabletop.', 'pj_office/pj-2715.jpg', '折后 $49.95', '$49.95', ['金属框架', '稳固耐用'], ['Metal Frame', 'Durable']),
    ('2716 双层多功能电脑桌', '2716 Dual-Tier Multifunctional Desk', '自带上层置物台，便于放置显示器或打印机，提升办公效率。', 'Dual-tier desk with elevated monitor shelf for enhanced ergonomics.', 'pj_office/pj-2716.jpg', '折后 $59.95', '$59.95', ['双层台面', '显示器架'], ['Dual Tier', 'Ergonomic']),
    ('4500 (TAUPE / CA) 转角电脑桌', '4500 (TAUPE / CA) L-Shaped Corner Desk', 'L型转角布局，充分利用角落空间，办公游戏双重享受。', 'L-shaped corner computer desk designed to maximize corner work space.', 'pj_office/pj-4500.jpg', '折后 $39.95', '$39.95', ['L型转角', '节省空间'], ['L-Shaped', 'Space Saving']),
    ('2714 钢化玻璃台面电脑桌', '2714 Tempered Glass Computer Desk', '现代高强度钢化玻璃台面，时尚通透，易清洁耐刮擦。', 'Sleek tempered glass computer desk with high weight capacity.', 'pj_office/pj-2714.jpg', '折后 $39.95', '$39.95', ['钢化玻璃', '现代时尚'], ['Tempered Glass', 'Modern']),
    ('2704 (WH / BK) 紧凑型电脑桌', '2704 (WH / BK) Compact Computer Desk', '轻巧紧凑设计，专为学生公寓与小户型书房打造。', 'Compact study desk designed for apartments and dorm rooms.', 'pj_office/pj-2704.jpg', '折后 $19.95', '$19.95', ['超值特惠', '轻巧紧凑'], ['Best Value', 'Compact']),
    ('2709 现代置物架书桌组合', '2709 Desk with Integrated Bookshelf', '侧边一体式多层书架，文具图书触手可及。', 'Integrated side shelving unit provides easy access to books and office supplies.', 'pj_office/pj-2709.jpg', '折后 $89.00', '$89.00', ['一体书架', '大容量'], ['Bookshelf Desk', 'Storage']),
    ('2006GRAY 金属文件收纳柜', '2006GRAY Metal Filing & Storage Cabinet', '坚固冷轧钢板制造，多层分格带锁安全收纳。', 'Heavy-duty cold-rolled steel filing cabinet with secure lock system.', 'pj_office/pj-2006.jpg', '折后 $49.95', '$49.95', ['冷轧钢板', '安全带锁'], ['Steel Cabinet', 'Secure Lock']),
    ('2707 透气网布升降办公椅', '2707 Breathable Mesh Task Chair', '高弹透气网布靠背，SGS认证气压升降，静音滑轮。', 'Breathable mesh task chair with pneumatic height adjustment and smooth casters.', 'pj_office/pj-2707.jpg', '折后 $35.00', '$35.00', ['透气网布', '气压升降'], ['Mesh Back', 'Pneumatic Lift']),
    ('2720 / 2721 电竞人体工学椅', '2720 / 2721 Ergonomic Gaming Chair', '赛车级人体工学包覆，加厚定型海绵，红黑/灰黑炫酷配色。', 'Racing-style gaming chair with thick molded foam and dynamic color accents.', 'pj_office/pj-2720-2721.jpg', '折后 $85.00', '$85.00', ['人体工学', '电竞专享'], ['Ergonomic', 'Gaming Chair']),
    ('2722RD / 2723BK 豪华高背电竞椅', '2722RD / 2723BK High-Back Gaming Chair', '加高头枕与腰靠支撑，大角度后仰逍遥调节，头等舱坐感。', 'High-back executive gaming chair with lumbar support and deep recline feature.', 'pj_office/pj-2722-2723.jpg', '折后 $109.95', '$109.95', ['加高靠背', '大角度后仰'], ['High Back', 'Reclining']),
    ('2725BK 现代中背网布办公椅', '2725BK Mid-Back Mesh Office Chair', '贴合脊柱曲线的腰部支撑，加宽加厚座垫，久坐不累。', 'Mid-back office chair with contoured lumbar support and thick cushion.', 'pj_office/pj-2725.jpg', '折后 $59.95', '$59.95', ['护腰设计', '加厚座垫'], ['Lumbar Support', 'Comfortable']),
    ('2706 实用旋转升降电脑椅', '2706 Swivel Height-Adjustable Desk Chair', '经典耐用皮革座垫，360度旋转底盘，灵活移动。', 'Durable leatherette swivel task chair with 360-degree rotation.', 'pj_office/pj-2706.jpg', '折后 $55.00', '$55.00', ['360度旋转', '耐磨皮艺'], ['360 Swivel', 'Durable']),
    ('2708BK 经典横纹皮艺主管椅', '2708BK Ribbed Leather Executive Chair', '现代横纹绗缝皮艺，镀铬扶手与金属五星脚，沉稳大气。', 'Mid-century ribbed leather executive chair with chrome arms and base.', 'pj_office/pj-2708.jpg', '折后 $69.95', '$69.95', ['横纹皮艺', '商务主管'], ['Ribbed Leather', 'Executive']),
    ('2724 (BK / GRAY) 加厚舒适旋转扶手椅', '2724 (BK / GRAY) Padded Swivel Armchair', '加厚羽绒感软包靠背与扶手，兼具沙发般舒适与办公便利。', 'Plush padded swivel armchair providing couch-like comfort for work spaces.', 'pj_office/pj-2724.jpg', '折后 $99.95', '$99.95', ['加厚软包', '沙发坐感'], ['Plush Padded', 'Luxury']),
]

def make_card_html(title, desc, img_path, price, tags, is_zh=True):
    tags_html = '\n'.join([f'                    <span class="detail-tag">{t}</span>' for t in tags])
    prefix = '../../' if is_zh else '../'
    full_img = prefix + 'assets/images/' + img_path
    
    return f"""
        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="{full_img}" alt="{title}" class="main-sofa-img" loading="lazy">
            </div>
            <div class="sofa-info">
                <h3>{title}</h3>
                <p>{desc}</p>
                <div class="sofa-details">
                    <span class="price-current">{price}</span>
{tags_html}
                </div>
            </div>
        </div>"""

def update_page_with_cards(zh_path, en_path, extra_cards):
    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_html = f.read()
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()

    # Find the insertion point before </main> or </section>
    zh_extra_str = '\n'.join([make_card_html(c[0], c[2], c[4], c[5], c[7], is_zh=True) for c in extra_cards])
    en_extra_str = '\n'.join([make_card_html(c[1], c[3], c[4], c[6], c[8], is_zh=False) for c in extra_cards])
    
    # insert before </div>\s*</main>
    zh_updated = re.sub(r'(\s*</div>\s*</main>)', r'\n' + zh_extra_str + r'\1', zh_html, count=1)
    en_updated = re.sub(r'(\s*</div>\s*</main>)', r'\n' + en_extra_str + r'\1', en_html, count=1)

    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_updated)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_updated)
    print(f"Updated {zh_path} and {en_path} with {len(extra_cards)} cards.")

update_page_with_cards('zh/dining/index.html', 'dining/index.html', dining_extra)
update_page_with_cards('zh/office/index.html', 'office/index.html', office_extra)
