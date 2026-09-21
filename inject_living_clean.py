import re, os

living_extra = [
    # Sofas from PDF p.4
    ('9701BR 多功能储物布艺沙发床', '9701BR Multifunctional Storage Sofa Bed', '厚实座包与宽大靠背，下层隐藏式大容量储物抽屉，一秒展开变舒适双人床。', 'Converts smoothly into a spacious sleeper with convenient hidden under-seat storage.', 'pj_living/pj-9701br.jpg', '特价 $299.00', '$299.00', ['坐卧两用', '隐藏储物'], ['Sleeper Sofa', 'Storage']),
    ('2406 (IVY / GRAY / BL) 现代布艺沙发床', '2406 Modern Fabric Sofa Bed', '三种时尚配色 (象牙白/现代灰/深邃蓝)，高密度回弹海绵座垫，三档可调节靠背。', 'Available in Ivy, Gray, and Blue with 3-position adjustable split-back mechanism.', 'pj_living/pj-2406.jpg', '特价 $169.00', '$169.00', ['三档调节', '三色可选'], ['Adjustable Back', 'Multi-Color']),
    ('2402 (RD / GR / BL) 极简折叠沙发床', '2402 Foldable Compact Sofa Bed', '时尚红/灰/蓝多色，轻巧灵活，小户型与公寓高性价比首选。', 'Compact and versatile fold-out sleeper sofa in Red, Gray, or Blue.', 'pj_living/pj-2402.jpg', '特价 $149.00', '$149.00', ['特惠精选', '小户型首选'], ['Best Value', 'Compact']),
    ('9211 / 9212 / 9213 现代布艺成套沙发', '9211 / 9212 / 9213 Fabric Living Room Sofa Set', '单人位 / 双人位 / 三人位自由组合，立体线条搭配实木稳固沙发脚。', 'Complete living room seating collection available in Single, Loveseat, and 3-Seat Sofa.', 'pj_living/pj-9211.jpg', '特价 单人: $185.00 | 双人: $265.00 | 三人: $295.00 | 2+3组合: $549.00', 'Chair: $185.00 | Loveseat: $265.00 | Sofa: $295.00 | 2+3 Set: $549.00', ['可单买/可组合', '2+3特惠'], ['Modular', '2+3 Set Deal']),
    ('9910GRAY 灰色现代 L 型贵妃榻储物沙发', '9910GRAY Gray Sectional Sofa with Chaise & Storage', '高级灰科技布面料，加宽加长贵妃榻，榻下带气压杆助力大储物箱。', 'L-shaped sectional in contemporary gray fabric with gas-lift storage chaise.', 'pj_living/pj-9910.jpg', '特价 $549.00', '$549.00', ['L型转角', '带大储物箱'], ['L-Sectional', 'Storage Chaise']),
    ('9900BK 黑色现代 L 型贵妃榻储物沙发', '9900BK Black Sectional Sofa with Chaise & Storage', '经典黑皮质感，超宽贵妃榻，坐卧两用带大容量储物箱。', 'Classic black leatherette L-shaped sectional featuring lift-up storage chaise.', 'pj_living/pj-9900.jpg', '特价 $549.00', '$549.00', ['黑色经典', '储物贵妃榻'], ['Black Leather', 'Storage Chaise']),
    ('9921 / 9922 / 9923 现代深灰皮质沙发系列', '9921 / 9922 / 9923 Dark Gray Faux Leather Sofa Collection', '深灰耐磨皮革，宽厚靠背与扶手设计，单人/双人/三人/2+3组合可选。', 'Dark gray durable faux leather sofa collection available in Chair, Loveseat, Sofa, or 2+3 Set.', 'pj_living/pj-9921.jpg', '特价 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | 2+3 Set: $479.00', ['耐磨皮革', '2+3套装特惠'], ['Faux Leather', 'Set Deal']),
    ('9931 / 9932 / 9933 现代棕色皮质沙发系列', '9931 / 9932 / 9933 Brown Faux Leather Sofa Collection', '暖棕复古皮革质感，饱满坐感，单人/双人/三人/2+3组合可选。', 'Warm brown faux leather sofa series offering plush comfort and lasting durability.', 'pj_living/pj-9931.jpg', '特价 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | 2+3 Set: $479.00', ['暖棕皮革', '2+3套装特惠'], ['Brown Leather', 'Set Deal']),
    ('9941 / 9942 / 9943 现代黑色皮质沙发系列', '9941 / 9942 / 9943 Black Faux Leather Sofa Collection', '纯黑极简现代皮艺，沉稳耐脏，单人/双人/三人/2+3组合可选。', 'Sleek black faux leather living room group available in individual pieces or 2+3 Set.', 'pj_living/pj-9941.jpg', '特价 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | 2+3 Set: $479.00', ['纯黑极简', '2+3套装特惠'], ['Black Leather', 'Set Deal']),

    # TV Stands & Fireplaces
    ('4420 / 4421 现代简约电视柜系列', '4420 / 4421 Contemporary TV Stand Series', '现代木纹台面搭配开放式多格收纳，4420款与4421款双尺寸可选。', 'Modern media console with open audio/video compartments in two versatile sizes.', 'pj_living/pj-4420-4421.jpg', '特价 4420款: $79.00 | 4421款: $99.00', '4420 Model: $79.00 | 4421 Model: $99.00', ['双尺寸可选', '多格收纳'], ['Dual Size', 'Media Console']),
    ('4422 现代多功能大尺寸电视柜', '4422 Large Screen Entertainment Center', '支持大尺寸电视放置，配封闭式储物门与走线孔。', 'Extra wide TV stand supporting large flat screens with cable management cutouts.', 'pj_living/pj-4422.jpg', '特价 $129.00', '$129.00', ['大屏适用', '整洁走线'], ['Large Screen', 'Storage']),
    ('4432CA 咖啡色现代实木电视柜', '4432CA Cappuccino Wooden TV Stand', '经典摩卡咖啡色调，紧凑实用，适合客厅与卧室。', 'Warm cappuccino finish media stand with spacious shelves.', 'pj_living/pj-4432.jpg', '特价 $49.95', '$49.95', ['经典咖啡色', '高性价比'], ['Cappuccino', 'Best Value']),
    ('4801 现代多功能电视柜/餐边储物柜', '4801 Multi-Purpose Media Buffet Console', '集电视机柜与餐边储物柜于一体，双门多层大容量。', 'Versatile multi-purpose buffet and TV stand with double cabinet doors.', 'pj_living/pj-4801.jpg', '特价 $99.95', '$99.95', ['电视/餐边两用', '双门储物'], ['Multi-Purpose', 'Spacious']),
    ('2766 现代紧凑型电视柜', '2766 Compact Modern TV Stand', '轻巧造型，分层置物，专为小户型打造。', 'Space-efficient entertainment console tailored for apartments.', 'pj_living/pj-2766.jpg', '特价 $65.00', '$65.00', ['紧凑灵巧', '小户型优选'], ['Compact', 'Apartment']),
    ('2767 现代置物电视柜', '2767 Modern Media Stand with Shelves', '加厚稳固台面，多层开敞收纳，便于游戏机与音响摆放。', 'Sturdy TV console with tiered shelving for gaming consoles and speakers.', 'pj_living/pj-2767.jpg', '特价 $75.00', '$75.00', ['多层置物', '稳固承重'], ['Tiered Storage', 'Sturdy']),
    ('2769 现代大容量多格电视柜', '2769 Wide Multi-Compartment TV Console', '宽屏设计，多格分类收纳，金属拉手与现代质感。', 'Wide profile media credenza with multi-zone storage and sleek hardware.', 'pj_living/pj-2769.jpg', '特价 $129.00', '$129.00', ['宽屏大容量', '多格分类'], ['Wide Profile', 'Generous Storage']),
    ('4337BK / 4338BK 现代黑色电子壁炉电视柜', '4337BK / 4338BK Black Electric Fireplace TV Stand', '内置逼真3D火焰特效电壁炉，独立发热取暖与观赏两用。', 'Modern black TV console featuring built-in electric fireplace with 3D flame effect.', 'pj_living/pj-4337-4338.jpg', '特价 4337款: $85.00 | 4338款: $69.00', '4337 Model: $85.00 | 4338 Model: $69.00', ['3D火焰壁炉', '取暖观赏两用'], ['Electric Fireplace', '3D Flame']),
    ('4333 / 4334 现代雅致壁炉电视柜', '4333 / 4334 Elegant Electric Fireplace TV Stand', '雅致木纹边框，嵌入式安全电壁炉，冬日温馨氛围感。', 'Warm wood textured entertainment center with integrated safety fireplace insert.', 'pj_living/pj-4333-4334.jpg', '特价 4333款: $85.00 | 4334款: $69.00', '4333 Model: $85.00 | 4334 Model: $69.00', ['雅致木纹', '安全取暖'], ['Wood Grain', 'Fireplace']),
    ('4331 / 4332 现代简约壁炉电视柜', '4331 / 4332 Modern Minimalist Fireplace Console', '极简流畅轮廓，自带多档温控与火焰调节壁炉。', 'Streamlined media mantel with multi-level temperature and flame brightness control.', 'pj_living/pj-4331-4332.jpg', '特价 4331款: $85.00 | 4332款: $69.00', '4331 Model: $85.00 | 4332 Model: $69.00', ['温控调节', '极简轮廓'], ['Remote Control', 'Modern']),
    ('4335 / 4336 现代豪华壁炉电视柜', '4335 / 4336 Deluxe Fireplace Media Console', '豪华尺寸台面与宽幅电壁炉，客厅视觉焦点。', 'Deluxe wide fireplace console creating a striking focal point for living rooms.', 'pj_living/pj-4335-4336.jpg', '特价 4335款: $89.00 | 4336款: $75.00', '4335 Model: $89.00 | 4336 Model: $75.00', ['豪华宽幅', '视觉焦点'], ['Deluxe Wide', 'Living Room Focus']),
    ('4337WH / 4338WH 现代纯白电子壁炉电视柜', '4337WH / 4338WH Pure White Fireplace Console', '纯白典雅烤漆质感，明亮温馨，现代轻奢风客厅首选。', 'Crisp white finish fireplace TV console for bright modern interior aesthetics.', 'pj_living/pj-4337wh.jpg', '特价 4337款: $85.00 | 4338款: $69.00', '4337 Model: $85.00 | 4338 Model: $69.00', ['纯白典雅', '现代轻奢'], ['Pure White', 'Electric Fireplace']),

    # Bookcases & Storage
    ('4220 / 4218 / 4216 经典多层书柜收纳系列', '4220 / 4218 / 4216 Multipurpose Bookcase Series', '提供 3层 / 4层 / 5层及带门/无门多款配置，五色可选 (CA/BK/CH/N/WH)。', 'Available in 3-tier, 4-tier, and 5-tier configurations with optional cabinet doors.', 'pj_living/pj-4220-4218.jpg', '特价 5层带门/无门: $45.00 / $35.00 | 4层带门/无门: $35.00 / $25.00 | 3层带门/无门: $25.00 / $19.95', '5-Shelf: $45.00 / $35.00 | 4-Shelf: $35.00 / $25.00 | 3-Shelf: $25.00 / $19.95', ['3/4/5层可选', '带门/无门'], ['3/4/5-Tier', 'Optional Doors']),
    ('4316 / 4320 (CA / WH) 现代三层实木书架', '4316 / 4320 Solid Wood 3-Tier Bookcase', '实木稳固结构，开放式三层展示架，咖啡色与纯白色可选。', 'Solid wood 3-tier open shelving bookcase in Cappuccino or White.', 'pj_living/pj-4316-4320.jpg', '特价 4316款: $29.95 | 4320款: $49.95', '4316 Model: $29.95 | 4320 Model: $49.95', ['实木三层', '双色可选'], ['Solid Wood', '3-Tier']),
    ('5115 / 5116 (CA / WH) 实木多层花架', '5115 / 5116 Solid Wood Plant Stand', '精巧阶梯式花架，实木材质，为绿植盆栽增添自然美感。', 'Tiered solid wood plant stands designed to showcase floral and greenery arrangements.', 'pj_living/pj-5115-5116.jpg', '特价 5115款: $21.95 | 5116款: $25.95', '5115 Model: $21.95 | 5116 Model: $25.95', ['实木花架', '阶梯美学'], ['Solid Wood', 'Plant Stand']),
    ('2036 (WH / PK / CH) 现代落地全身穿衣镜', '2036 Modern Free-Standing Floor Mirror', '高清防爆大视野银镜，自带稳固三角支撑脚，白/粉/棕三色可选。', 'High-definition shatter-proof full-length standing mirror with sturdy easel stand.', 'pj_living/pj-2036.jpg', '特价 $49.95', '$49.95', ['全身穿衣镜', '防爆银镜'], ['Floor Mirror', 'Full Length']),
    ('4411 (CA / N / CH) 经典电话桌/边几', '4411 Classic Telephone Table & Accent Stand', '经典置物边几，带小巧抽屉与下层杂志置物架。', 'Traditional phone and accent stand featuring a utility drawer and bottom shelf.', 'pj_living/pj-4411.jpg', '特价 $22.00', '$22.00', ['经典边几', '带小抽屉'], ['Accent Table', 'With Drawer']),
    ('5107 豪华实木落地挂衣架', '5107 Deluxe Solid Wood Coat Rack', '加粗实木主杆，多向防滑挂钩与稳固重型圆盘底座。', 'Heavy-duty solid wood freestanding coat tree with multi-tier hanging hooks.', 'pj_living/pj-5107.jpg', '特价 $49.95', '$49.95', ['实木衣帽架', '重型底座'], ['Solid Wood', 'Coat Tree']),
    ('2052BK 现代金属落地挂衣架', '2052BK Modern Metal Coat Rack', '防锈哑光黑金属管材，现代几何挂钩分布。', 'Matte black metal coat rack with geometric hook branches.', 'pj_living/pj-2052.jpg', '特价 $23.00', '$23.00', ['金属防锈', '几何挂钩'], ['Metal Frame', 'Coat Rack']),
    ('2050 (WH / BK / CHROME) 挂衣架', '2050 Freestanding Metal Coat Rack', '提供喷涂黑/白款与豪华电镀镀铬款，结构紧凑承重力强。', 'Available in black/white coated finish and polished chrome finish.', 'pj_living/pj-2050.jpg', '特价 喷涂款: $19.95 | 镀铬款: $21.95', 'Coated: $19.95 | Chrome: $21.95', ['喷涂/镀铬', '承重稳固'], ['Coated / Chrome', 'Sturdy']),
    ('2051BK 简易金属挂衣架', '2051BK Simple Metal Coat Stand', '经济实惠，安装极简，适合玄关与卧室角隅。', 'Budget-friendly and lightweight freestanding metal garment organizer.', 'pj_living/pj-2051.jpg', '特价 $12.95', '$12.95', ['超值简易', '轻巧便携'], ['Best Value', 'Simple']),
    ('2047BK / 2048WH 现代经典金属挂衣架', '2047BK / 2048WH Classic Metal Coat Stand', '经典黑白双色，顶部伞架设计与圆润防刮挂钩。', 'Classic coat rack with umbrella holder ring and garment-safe hook ends.', 'pj_living/pj-2047-2048.jpg', '特价 $22.00', '$22.00', ['带伞架功能', '黑白经典'], ['With Umbrella Ring', 'Classic']),
    ('2772 落地多层金属鞋架', '2772 Multi-Tier Metal Shoe Rack', '高强度金属网层板，通风透气，分类收纳鞋履。', 'Sturdy wire shelf shoe rack with generous clearance for footwear.', 'pj_living/pj-2772.jpg', '特价 $21.95', '$21.95', ['金属网板', '通风透气'], ['Wire Shelf', 'Shoe Rack']),
    ('2083 (WH / BK) 三层移动置物小推车', '2083 3-Tier Rolling Utility Cart', '配静音万向轮与双刹车，三层金属沥水置物篮，厨房客厅两相宜。', '3-tier mesh utility rolling cart with heavy-duty casters and lock brakes.', 'pj_living/pj-2083.jpg', '特价 $19.95', '$19.95', ['移动推车', '万向刹车轮'], ['Rolling Cart', 'Lockable Casters']),
    ('2773 / 2771 落地带鞋网衣帽架', '2773 / 2771 Garment Rack with Shoe Net', '顶部加宽挂衣横杆，底部透气鞋网，一架解决穿搭收纳。', 'Freestanding clothing rack with overhead hanging rod and lower shoe storage net.', 'pj_living/pj-2773-2771.jpg', '特价 2773款: $21.95 | 2771款: $19.95', '2773 Model: $21.95 | 2771 Model: $19.95', ['衣物/鞋架一体', '加宽挂杆'], ['Garment Rack', 'Shoe Net']),
    ('2825 / 2826 镀铬金属多层衣柜架 (含防尘罩)', '2825 / 2826 Covered Chrome Wire Wardrobe', '重型镀铬钢丝架，配拉链式全封闭环保防尘罩，3层/6层可选。', 'Heavy-duty chrome steel wardrobe rack with zip-up protective dust cover.', 'pj_living/pj-2825-2826.jpg', '特价 3层款: $49.95 | 6层款: $69.95', '3-Tier: $49.95 | 6-Tier: $69.95', ['带防尘罩', '重型镀铬'], ['With Cover', 'Heavy Duty']),
    ('2813 / 2814 / 2815 多层金属置物架', '2813 / 2814 / 2815 Multi-Tier Storage Wire Shelves', '可自由调节层高，工业级承重，3层/4层/5层多规格可选 (镀铬/黑漆)。', 'Adjustable height commercial grade wire shelving in 3, 4, or 5 tier options.', 'pj_living/pj-2813-2814.jpg', '特价 3层款: $24.95 | 4层款: $29.95 | 5层款: $36.95', '3-Tier: $24.95 | 4-Tier: $29.95 | 5-Tier: $36.95', ['工业级承重', '层高可调'], ['Adjustable', 'Wire Shelving']),
    ('2810 10抽屉多功能移动收纳推车', '2810 10-Drawer Mobile Organizer Cart', '10个透明收纳抽屉，半透磨砂质感，文具手工与杂物分类神器。', '10-drawer rolling craft and office organizer with smooth chrome frame.', 'pj_living/pj-2810.jpg', '特价 $39.95', '$39.95', ['10抽大容量', '移动滑轮'], ['10-Drawer', 'Organizer Cart']),
    ('2824 / 2823 重型镀铬金属衣物架', '2824 / 2823 Heavy Duty Commercial Garment Rack', '商用级镀铬加粗管径，超强挂重能力，服装店与大户型首选。', 'Commercial grade heavy-duty chrome garment rack with high weight capacity.', 'pj_living/pj-2824-2823.jpg', '特价 2824款: $49.95 | 2823款: $59.95', '2824 Model: $49.95 | 2823 Model: $59.95', ['商用重型', '高承重'], ['Commercial Grade', 'Heavy Duty']),
    ('4202 - 4208 多规格实用置物收纳架', '4202 - 4208 Multi-Size Storage Shelf Units', '从 2格 到 8格 多种组合方式，自由拼装搭配，小物件收纳得心应手。', 'Modular storage cubes and shelf units available from 2-cube to 8-cube layouts.', 'pj_living/pj-4220-4218.jpg', '特价 $17.95 - $49.95', '$17.95 - $49.95', ['模块化自由组合', '多规格可选'], ['Modular Cube', 'Multi-Size']),
    ('4217 (WAL / BK / WH) 现代多功能矮柜/电视柜', '4217 Low-Profile TV & Storage Stand', '多格对称开放收纳，低矮台面，胡桃木/黑/白三色可选。', 'Low-profile symmetrical open media console in Walnut, Black, or White.', 'pj_living/pj-4432.jpg', '特价 $25.00', '$25.00', ['多功能矮柜', '三色可选'], ['Low Profile', 'Storage Stand']),
    ('4412 / 4413 现代浴室马桶上方置物收纳架', '4412 / 4413 Over-The-Toilet Bathroom Space Saver', '巧妙利用马桶上方垂直空间，三层置物板收纳洗漱用品与毛巾。', '3-tier over-the-toilet space saver shelf maximizing vertical bathroom storage.', 'pj_dining/pj-2524.jpg', '特价 $49.95', '$49.95', ['马桶上方收纳', '浴室神器'], ['Space Saver', 'Over-The-Toilet']),
    ('2012BK / 2008BK / 2007 现代浴室金属置物架/毛巾架', '2012BK / 2008BK / 2007 Bathroom Racks & Towel Stands', '防锈金属管件，轻巧稳固，干湿分离收纳卫浴用品。', 'Rust-resistant metal bathroom accessory shelves and towel storage racks.', 'pj_living/pj-2051.jpg', '特价 $19.95 - $21.95', '$19.95 - $21.95', ['防锈金属', '卫浴干湿收纳'], ['Rust Resistant', 'Bathroom Rack']),
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

    zh_extra_str = '\n'.join([make_card_html(c[0], c[2], c[4], c[5], c[7], is_zh=True) for c in extra_cards])
    en_extra_str = '\n'.join([make_card_html(c[1], c[3], c[4], c[6], c[8], is_zh=False) for c in extra_cards])
    
    zh_updated = re.sub(r'(\s*</div>\s*</main>)', r'\n' + zh_extra_str + r'\1', zh_html, count=1)
    en_updated = re.sub(r'(\s*</div>\s*</main>)', r'\n' + en_extra_str + r'\1', en_html, count=1)

    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(zh_updated)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_updated)
    print(f"Updated {zh_path} and {en_path} with {len(extra_cards)} cards.")

update_page_with_cards('zh/living-room/index.html', 'living-room/index.html', living_extra)
