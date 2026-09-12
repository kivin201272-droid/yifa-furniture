import re, os

# Bedroom Incremental Products
bedroom_extra = [
    # Suites
    ('8910 现代轻奢灰木纹套房家具 5件套', '8910 Modern Gray Wood Bedroom Suite (5-PC)', '现代高级灰木纹质感，包含大容量抽屉梳妆台、双抽床头柜与五斗柜。', 'Modern gray wood grain finish with generous storage dresser, mirror, nightstand, and chest.', 'pj_bedroom/pj-8910.jpg', '折后 Queen床: $499.00 | 床头柜: $90.00 | 镜子: $60.00 | 梳妆台: $260.00 | 五斗柜: $195.00', 'Queen Bed: $499.00 | Nightstand: $90.00 | Mirror: $60.00 | Dresser: $260.00 | Chest: $195.00', ['卧室套房', '5件套'], ['Bedroom Suite', '5-PC Set']),
    ('8003 豪华经典实木套房家具 5件套', '8003 Luxury Solid Wood Bedroom Suite (5-PC)', '精工雕琢实木床头与收纳柜体，沉稳大气，全套特惠。', 'Masterfully crafted solid wood suite with durable hardware and classic finishes.', 'pj_bedroom/pj-8003.jpg', '折后 Queen床: $220.00 | 床头柜: $90.00 | 镜子: $70.00 | 梳妆台: $260.00 | 五斗柜: $195.00 | Queen五件套: $799.00', 'Queen Bed: $220.00 | Nightstand: $90.00 | Mirror: $70.00 | Dresser: $260.00 | Chest: $195.00 | Queen 5-PC Set: $799.00', ['实木套房', '超值套装'], ['Solid Wood', '5-PC Set']),
    ('8010 现代雅致卧室套房家具 5件套', '8010 Contemporary Bedroom Suite (5-PC)', '现代简约线条，环保耐磨板材，配梳妆镜与多层斗柜。', 'Contemporary clean lines with scratch-resistant surfaces and spacious drawers.', 'pj_bedroom/pj-8010.jpg', '折后 Full/Queen床: $180.00 | 床头柜: $85.00 | 镜子: $60.00 | 梳妆台: $225.00 | 五斗柜: $170.00 | 5件套: $649.00', 'Full/Queen Bed: $180.00 | Nightstand: $85.00 | Mirror: $60.00 | Dresser: $225.00 | Chest: $170.00 | 5-PC Set: $649.00', ['简约现代', '5件套组'], ['Contemporary', '5-PC Set']),
    ('8009 简约现代卧室套房家具 5件套', '8009 Modern Bedroom Suite (5-PC)', '温润暖色木纹，圆润边角安全设计，高性价比套房之选。', 'Warm wood tones with rounded safety edges, offering exceptional comfort and storage.', 'pj_bedroom/pj-8009.jpg', '折后 Full/Queen床: $175.00 | 床头柜: $75.00 | 镜子: $55.00 | 梳妆台: $205.00 | 五斗柜: $170.00 | 5件套: $579.00', 'Full/Queen Bed: $175.00 | Nightstand: $75.00 | Mirror: $55.00 | Dresser: $205.00 | Chest: $170.00 | 5-PC Set: $579.00', ['高性价比', '套房特惠'], ['Best Value', '5-PC Set']),
    ('8008 现代原木风卧室套房家具 5件套', '8008 Natural Wood Tone Bedroom Suite (5-PC)', '原木自然风情，多抽屉分类收纳，营造温馨卧室氛围。', 'Natural organic aesthetic with multi-drawer organizational layout.', 'pj_bedroom/pj-8008.jpg', '折后 Full/Queen床: $175.00 | 床头柜: $75.00 | 镜子: $55.00 | 梳妆台: $205.00 | 五斗柜: $170.00 | 5件套: $579.00', 'Full/Queen Bed: $175.00 | Nightstand: $75.00 | Mirror: $55.00 | Dresser: $205.00 | Chest: $170.00 | 5-PC Set: $579.00', ['原木风情', '5件套组'], ['Natural Wood', '5-PC Set']),
    
    # Platform Beds
    ('7402Q-WH 白色轻奢软包平台床', '7402Q-WH White Upholstered Platform Bed', '纯白轻奢皮革软包床头，高密度回弹海绵，无异响静音排骨架。', 'Luxury white faux leather upholstered headboard with solid wooden slat system.', 'pj_bedroom/pj-7402q.jpg', '折后 Queen: $499.00', 'Queen: $499.00', ['纯白轻奢', '软包床头'], ['White Leather', 'Platform Bed']),
    ('7401Q-BK 黑色轻奢软包平台床', '7401Q-BK Black Upholstered Platform Bed', '高档黑色皮艺软包，现代轻奢弧线造型，彰显尊贵品味。', 'Premium black upholstered platform bed with elegant curved silhouette.', 'pj_bedroom/pj-7401q.jpg', '折后 Queen: $499.00', 'Queen: $499.00', ['经典黑皮', '尊贵现代'], ['Black Leather', 'Platform Bed']),
    ('7405WH 现代纯白极简平台床', '7405WH Modern White Minimalist Platform Bed', '极简无床头板设计或纯白几何床头，平整稳固承重。', 'Minimalist low-profile platform bed in clean crisp white finish.', 'pj_bedroom/pj-7405wh.jpg', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00', ['纯白极简', '稳固承重'], ['Pure White', 'Sturdy']),
    ('7403GRAY 优雅灰调布艺平台床', '7403GRAY Elegant Gray Fabric Platform Bed', '高级灰细织麻布面料，透气亲肤，稳固实木床腿支撑。', 'Elegant gray linen upholstered platform bed with solid wood tapered legs.', 'pj_bedroom/pj-7403gray.jpg', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00', ['高级灰布', '透气亲肤'], ['Gray Fabric', 'Comfortable']),
    ('7602Q-GRAY 现代灰色软包带抽屉平台床', '7602Q-GRAY Gray Platform Bed with Drawers', '灰色布艺软包床头，床底配备实用大容量储物抽屉。', 'Modern gray upholstered platform bed featuring convenient built-in storage drawers.', 'pj_bedroom/pj-7602q-gray.jpg', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00', ['带储物抽屉', '灰色布艺'], ['With Drawers', 'Storage Bed']),
    ('7602Q-IVY 象牙白软包带抽屉平台床', '7602Q-IVY Ivory Platform Bed with Drawers', '象牙白温馨色调，柔软靠背与大容量隐藏储物空间。', 'Warm ivory fabric platform bed with spacious under-bed storage drawers.', 'pj_bedroom/pj-7602q-ivy.jpg', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00', ['象牙白', '储物抽屉'], ['Ivory Fabric', 'Storage Bed']),
    ('7602-PINK 甜美粉色软包平台床', '7602-PINK Sweet Pink Upholstered Platform Bed', '甜美柔粉色布艺，儿童房与少女心卧室的梦幻之选。', 'Charming blush pink upholstered platform bed perfect for youth or guest rooms.', 'pj_bedroom/pj-7602-pink.jpg', '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'Twin: $129.00 | Full: $149.00 | Queen: $159.00', ['柔美粉色', '少女儿童'], ['Pink Fabric', 'Youth Bed']),
    ('7404BK 经典黑色皮艺平台床', '7404BK Classic Black Faux Leather Bed', '耐磨易打理黑色皮革，简约现代床头造型。', 'Durable black faux leather platform bed with clean rectangular headboard.', 'pj_bedroom/pj-7404bk.jpg', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00', ['耐磨皮革', '现代百搭'], ['Black Leather', 'Modern']),
    ('7500F/7500Q-GRAY 现代灰色平台床', '7500 Gray Contemporary Platform Bed', '现代中性灰色调，加厚稳固床排骨架，无需弹簧盒。', 'Neutral gray platform bed with reinforced wooden slat support system.', 'pj_bedroom/pj-7500.jpg', '折后 Full: $299.00 | Queen: $299.00', 'Full: $299.00 | Queen: $299.00', ['免弹簧盒', '中性灰色'], ['No Box Spring', 'Platform']),
    ('7600Q-IVY 象牙白经典拉扣平台床', '7600Q-IVY Classic Tufted Ivory Platform Bed', '手工经典拉扣工艺床头，丰盈饱满靠感，浪漫优雅。', 'Hand-tufted diamond patterned headboard with rich padded cushioning.', 'pj_bedroom/pj-7600q.jpg', '折后 Queen: $399.00', 'Queen: $399.00', ['经典拉扣', '法式优雅'], ['Tufted Headboard', 'Luxury']),
    ('7603 经典方格拉扣软包平台床', '7603 Grid Tufted Upholstered Bed', '立体方格绗缝床头，现代利落，多尺寸可选。', 'Geometric grid tufted headboard offering tailored sophistication.', 'pj_bedroom/pj-7603.jpg', '折后 Full: $179.00 | Queen: $199.00', 'Full: $179.00 | Queen: $199.00', ['方格拉扣', '立体软包'], ['Grid Tufted', 'Modern']),

    # Bunk Beds & Metal Beds
    ('7806-GRAY 现代高级灰布艺床', '7806-GRAY Modern Gray Upholstered Bed', '雅致灰色细麻布，简约现代床头，稳固防滑床腿。', 'Tailored gray linen platform bed with sturdy wooden inner framing.', 'pj_bedroom/pj-7806.jpg', '折后 Full: $199.00 | Queen: $229.00', 'Full: $199.00 | Queen: $229.00', ['高级灰布', '雅致百搭'], ['Gray Linen', 'Platform Bed']),
    ('7102 GRAY 现代深灰简约实木床', '7102 GRAY Solid Wood Panel Bed in Gray', '优质实木横条床头，深灰沉稳色调，承重优异。', 'Solid wood horizontal slat panel bed in rich modern dark gray finish.', 'pj_bedroom/pj-7102.jpg', '折后 Full: $109.00 | Queen: $119.00', 'Full: $109.00 | Queen: $119.00', ['深灰实木', '横条床头'], ['Solid Wood', 'Dark Gray']),
    ('7102 BROWN 经典棕色实木床', '7102 BROWN Solid Wood Panel Bed in Brown', '经典美式暖棕色实木床架，质朴温润，坚固耐用。', 'Classic warm brown finish solid wood panel bed with reliable support.', 'pj_bedroom/pj-7102.jpg', '折后 Full: $109.00 | Queen: $119.00', 'Full: $109.00 | Queen: $119.00', ['美式暖棕', '实木床架'], ['Solid Wood', 'Warm Brown']),
    ('7100 极简实木床架系列', '7100 Minimalist Solid Wood Bed Series', '超高性价比实木床架，T/F/Q 三种常用规格全覆盖。', 'Exceptional value solid wood platform bed available in Twin, Full, and Queen.', 'pj_bedroom/pj-7100.jpg', '折后 T: $75.00 | F: $85.00 | Q: $95.00', 'Twin: $75.00 | Full: $85.00 | Queen: $95.00', ['全尺寸覆盖', '超高性价比'], ['All Sizes', 'Value Choice']),
    ('7804 GRAY 现代浅灰布艺床', '7804 GRAY Light Gray Fabric Bed', '清爽浅灰织物，加厚海绵软包，触感温和舒适。', 'Light gray woven fabric bed frame with plush padded headboard.', 'pj_bedroom/pj-7804.jpg', '折后 Full: $249.00 | Queen: $269.00', 'Full: $249.00 | Queen: $269.00', ['浅灰织物', '舒适软包'], ['Light Gray', 'Fabric Bed']),
    ('7011GRAY 现代灰色实木床', '7011GRAY Solid Wood Bed in Gray', '现代灰色实木工艺，结实耐用，防潮耐磨。', 'Sturdy wooden bed with clean horizontal panel headboard in gray.', 'pj_bedroom/pj-7011.jpg', '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'Twin: $119.00 | Full: $139.00 | Queen: $149.00', ['实木框架', '灰色饰面'], ['Solid Wood', 'Gray Finish']),
    ('7011CHAR 炭黑色经典实木床', '7011CHAR Solid Wood Bed in Charcoal Black', '沉稳炭黑色实木质感，经典耐看，结构坚固。', 'Bold charcoal black finish wooden bed with durable support slats.', 'pj_bedroom/pj-7011.jpg', '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'Twin: $119.00 | Full: $139.00 | Queen: $149.00', ['炭黑实木', '坚固沉稳'], ['Solid Wood', 'Charcoal']),
    ('7016-GRAY 现代灰布艺床', '7016-GRAY Modern Fabric Bed', '简约现代灰布艺床，性价比高，安装便捷。', 'Simple and sleek gray upholstered bed with easy assembly.', 'pj_bedroom/pj-7016.jpg', '折后 Full: $99.00 | Queen: $109.00', 'Full: $99.00 | Queen: $109.00', ['超值布艺', '安装便捷'], ['Fabric Bed', 'Easy Setup']),
    ('2331 便携折叠床 (带高弹海绵床垫)', '2331 Portable Folding Bed with Foam Mattress', '折叠即收，带万向轮随心推移，附赠高密度海绵床垫。', 'Space-saving rollaway folding bed equipped with thick comfort foam mattress.', 'pj_bedroom/pj-2331.jpg', '折后 $119.00', '$119.00', ['折叠便携', '配海绵垫'], ['Folding Bed', 'With Mattress']),
    ('7005BK 现代黑色双层铁架床 (Twin/Twin)', '7005BK Metal Bunk Bed (Twin/Twin)', '加粗重型钢管焊接，上下双层 Twin 规格，配全防护护栏与爬梯。', 'Heavy-duty steel construction twin-over-twin bunk bed with safety guardrails.', 'pj_bedroom/pj-7005bk.jpg', '折后 $149.00', '$149.00', ['重型铁架', '上下双层'], ['Metal Bunk Bed', 'Twin/Twin']),
    ('7004BK 现代黑色双层铁架床 (Twin/Full)', '7004BK Metal Bunk Bed (Twin/Full)', '上层单人 Twin + 下层双人 Full，多人口家庭与客房理想之选。', 'Versatile twin-over-full metal bunk bed providing maximum sleeping accommodations.', 'pj_bedroom/pj-7004bk.jpg', '折后 $169.00', '$169.00', ['子母铁架', 'Twin/Full'], ['Bunk Bed', 'Twin/Full']),
    ('7701WH 纯白实木双层儿童床 (Twin/Twin)', '7701WH Solid Wood Bunk Bed in White', '优质实木环保白漆，上层全包围安全护栏，稳固实木直梯。', 'Solid pine wood twin-over-twin bunk bed in non-toxic white finish.', 'pj_bedroom/pj-7701wh.jpg', '折后 $219.00', '$219.00', ['实木双层', '纯白环保'], ['Solid Wood', 'White Bunk Bed']),
    ('7702WH 纯白实木子母双层床 (Full/Twin)', '7702WH Solid Wood Bunk Bed (Full/Twin)', '上层单人 + 下层双人加宽实木床，温润白漆质感。', 'Spacious full-over-twin solid wood bunk bed in clean white lacquer finish.', 'pj_bedroom/pj-7702wh.jpg', '折后 $279.00', '$279.00', ['实木子母床', '纯白典雅'], ['Solid Wood', 'Full/Twin Bunk']),
    ('7702CA 咖啡色实木子母双层床 (Full/Twin)', '7702CA Solid Wood Bunk Bed in Cappuccino', '经典摩卡咖啡色实木打造，耐磨防刮，结构沉稳。', 'Warm cappuccino finish solid wood full-over-twin bunk bed.', 'pj_bedroom/pj-7702ca.jpg', '折后 $279.00', '$279.00', ['咖啡色实木', '子母双层'], ['Solid Wood', 'Cappuccino']),
    ('7701CA 咖啡色实木双层儿童床 (Twin/Twin)', '7701CA Solid Wood Bunk Bed in Cappuccino', '经典咖啡色实木上下铺，圆弧倒角防磕碰设计。', 'Twin-over-twin wooden bunk bed in classic cappuccino with safety rounded edges.', 'pj_bedroom/pj-7701ca.jpg', '折后 $219.00', '$219.00', ['安全倒角', '实木双层'], ['Solid Wood', 'Twin/Twin']),
    ('7020WH 纯白现代实木床', '7020WH Solid Wood Bed in Pure White', '纯白极简线条，高品质实木排骨架，带来整洁明亮视觉。', 'Clean modern white solid wood bed frame with reinforced slat support.', 'pj_bedroom/pj-7020-7021.jpg', '折后 Full: $199.00 | Queen: $219.00', 'Full: $199.00 | Queen: $219.00', ['纯白实木', '整洁明亮'], ['Solid Wood', 'Pure White']),
    ('7021BK 纯黑现代实木床', '7021BK Solid Wood Bed in Black', '纯黑哑光木纹质感，现代硬朗工业风与极简风皆宜。', 'Bold matte black solid wood bed with sleek contemporary headboard.', 'pj_bedroom/pj-7020-7021.jpg', '折后 Full: $199.00 | Queen: $219.00', 'Full: $199.00 | Queen: $219.00', ['纯黑木纹', '硬朗极简'], ['Solid Wood', 'Black Finish']),
    ('7013 现代条纹实木床架', '7013 Slat Wood Platform Bed', '经典格栅条纹床头，实木排骨架直接承托床垫。', 'Classic vertical slat headboard wood platform bed requiring no box spring.', 'pj_bedroom/pj-7013.jpg', '折后 Twin: $99.00 | Full: $119.00 | Queen: $129.00', 'Twin: $99.00 | Full: $119.00 | Queen: $129.00', ['条纹格栅', '全规格覆盖'], ['Slat Design', 'Multi-Size']),
    ('7901CA-T/F 咖啡色经典金属床架', '7901CA Metal Bed in Cappuccino', '复古摩卡棕金属弯管床头，轻巧稳固，防锈静电喷涂。', 'Vintage styled metal arched headboard bed frame with anti-rust coating.', 'pj_bedroom/pj-7901.jpg', '折后 Twin: $109.00 | Full: $129.00', 'Twin: $109.00 | Full: $129.00', ['复古金属', '防锈喷涂'], ['Metal Frame', 'Vintage']),
    ('7901WH-T/F 纯白现代金属床架', '7901WH Metal Bed in Pure White', '清新纯白金属弧线床头，轻盈通透，适合清新田园与现代卧室。', 'Fresh white curved metal bed frame with sturdy steel slats.', 'pj_bedroom/pj-7901.jpg', '折后 Twin: $109.00 | Full: $129.00', 'Twin: $109.00 | Full: $129.00', ['纯白金属', '清新轻盈'], ['White Metal', 'Modern']),
    ('1901 极简折叠金属床架系列', '1901 Foldable Metal Platform Base', '加重高承重折叠金属底架，超快展开免工具组装，床底储物空间充足。', 'Heavy-duty tool-free foldable steel mattress foundation with generous under-bed clearance.', 'pj_bedroom/pj-1901.jpg', '折后 T: $59.00 | F: $79.00 | Q: $89.00', 'Twin: $59.00 | Full: $79.00 | Queen: $89.00', ['折叠免工具', '床底大储物'], ['Tool-Free', 'Underbed Storage']),
    ('7800 / 7801 金属床架与可推拉床底架', '7800 / 7801 Metal Bed & Trundle System', '包含 7800Q/7801F 金属床架及配套可隐藏式滚轮抽拉床底架。', 'Metal daybed / platform bed with roll-out pop-up under-bed trundle.', 'pj_bedroom/pj-7800-7801.jpg', '折后 7800Q: $99.00 | 7801F: $99.00 | 抽拉床架: $55.00 / $85.00', '7800Q: $99.00 | 7801F: $99.00 | Trundle: $55.00 / $85.00', ['滚轮抽拉', '客房神器'], ['Trundle Bed', 'Space Saving']),

    # Wardrobes & Storage
    ('4224 (BK / CH / N / WH) 实用双门大衣柜', '4224 2-Door Wardrobe Armoire', '双开门挂衣大空间，内置金属挂衣杆与顶部储物隔层，四色可选。', 'Spacious 2-door wardrobe with heavy-duty clothes hanging rail and top shelf.', 'pj_bedroom/pj-4224-4225.jpg', '折后 $95.00', '$95.00', ['双门大衣柜', '四色可选'], ['2-Door Wardrobe', 'Multi-Color']),
    ('4225 (BK / CH / N / WH) 双门双抽屉大衣柜', '4225 2-Door 2-Drawer Wardrobe Armoire', '上层悬挂衣物，下层双宽幅滑轨抽屉收纳叠放衣物，分区科学。', '2-door wardrobe with 2 smooth gliding bottom drawers for organized storage.', 'pj_bedroom/pj-4224-4225.jpg', '折后 $105.00', '$105.00', ['双门双抽', '分区收纳'], ['2-Door 2-Drawer', 'Organized']),
    ('4226 (BK / CH / N / WH) 豪华双门加高大衣柜', '4226 Tall 2-Door 2-Drawer Wardrobe', '加高大容量尺寸，防尘闭合，满足大件长衣悬挂需求。', 'Extra tall 2-door 2-drawer wardrobe designed for long garments and suits.', 'pj_bedroom/pj-4226.jpg', '折后 $135.00', '$135.00', ['加高大容量', '长衣无忧'], ['Extra Tall', 'Spacious']),
    ('4227CH 豪华三门两抽实木大衣柜', '4227CH 3-Door 2-Drawer Large Wardrobe', '三门多仓大容量，左侧长衣区，右侧多层叠放区与底部双抽。', 'Generous 3-door wardrobe with dedicated hanging space, interior shelves, and 2 bottom drawers.', 'pj_bedroom/pj-4227.jpg', '折后 $185.00', '$185.00', ['三门两抽', '全功能衣柜'], ['3-Door Armoire', 'Master Wardrobe']),
    ('4228 现代简约实用大鞋柜', '4228 Modern Entryway Shoes Cabinet', '多层大容量斜插/平放鞋位，透气开门设计，玄关整洁大方。', 'Multi-tier shoe storage cabinet with ventilated doors for fresh organized entryways.', 'pj_bedroom/pj-4228.jpg', '折后 $75.00', '$75.00', ['大容量鞋柜', '玄关利器'], ['Shoe Cabinet', 'Entryway']),
    ('4424CA 双门双抽屉带台面玄关鞋柜', '4424CA 2-Drawer 2-Door Shoes Cabinet in Cappuccino', '顶部双抽屉收纳钥匙杂物，下方双门多层鞋架，美观实用。', 'Cappuccino shoe cabinet with 2 top utility drawers and lower 2-door shoe compartment.', 'pj_bedroom/pj-4424.jpg', '折后 $89.00', '$89.00', ['带杂物抽屉', '双门鞋柜'], ['With Drawers', 'Shoe Cabinet']),
    ('4229 (WH / GRAY) 现代简易收纳斗柜', '4229 Modern Compact Storage Chest', '简约纯白/灰调配色，顺滑导轨，小巧身形多处适用。', 'Compact 3-tier storage chest in white or gray with smooth-glide metal tracks.', 'pj_bedroom/pj-4229.jpg', '折后 $55.00', '$55.00', ['简约斗柜', '顺滑滑轨'], ['Storage Chest', 'Compact']),
    ('4322 / 4323 现代三层/四层储物抽屉柜', '4322 / 4323 3-Drawer / 4-Drawer Chest', '大容量深抽屉，加厚板材，承重强抗变形。', 'Deep-drawer storage chests in 3-drawer and 4-drawer configurations.', 'pj_bedroom/pj-4322-4323.jpg', '折后 4322款: $65.00 | 4323款: $75.00', '4322 Model: $65.00 | 4323 Model: $75.00', ['多层深抽', '加厚板材'], ['Multi-Drawer', 'Heavy Duty']),
    ('4223 (N / BK / CH / WH) 现代经典五斗抽屉柜', '4223 5-Drawer Vertical Chest', '垂直加高五斗柜，占地仅0.3平米，纵向释放海量收纳空间。', 'Vertical 5-drawer chest designed for maximum vertical clothing storage.', 'pj_bedroom/pj-4223.jpg', '折后 $85.00', '$85.00', ['经典五斗柜', '立式省地'], ['5-Drawer Chest', 'Space Saver']),
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

update_page_with_cards('zh/bedroom/index.html', 'bedroom/index.html', bedroom_extra)
