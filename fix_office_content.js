const fs = require('fs');

function cleanOfficeZh() {
    let html = fs.readFileSync('zh/office/index.html', 'utf-8');
    
    // Fix Hero
    html = html.replace('<h1>优质床垫</h1>', '<h1>优质办公系列</h1>');
    html = html.replace('<p>全系列高品质床垫，科学设计，为您带来优质睡眠体验。</p>', '<p>全系列高品质办公家具，人体工学设计，为您带来舒适高效的工作体验。</p>');
    html = html.replace('Collection 04', 'Collection 05');
    
    // Fix Split Body
    html = html.replace('<h2>现代卧室协调配套套件</h2>', '<h2>现代办公协调配套套件</h2>');
    html = html.replace('<p>我们的卧室系列设计和谐统一。床架、床头柜、梳妆台和储物柜在饰面与比例上高度协调，客户可整套采购，也可逐步添置。</p>', '<p>我们的办公系列设计和谐统一。办公桌、书架和储物柜在饰面与比例上高度协调，客户可整套采购，也可逐步添置。</p>');
    
    // Fix Features
    html = html.replace('<h2>卧室系列包含品类</h2>', '<h2>办公系列包含品类</h2>');
    html = html.replace('<h3>床架</h3><p>平台床、储物床及软包床架，采用现代饰面，符合美国标准尺寸。</p>', '<h3>办公桌</h3><p>现代设计办公桌，宽敞桌面，符合人体工学高度。</p>');
    html = html.replace('<h3>床头柜</h3><p>与我们的床架和梳妆台配套的床头柜和小型储物柜。</p>', '<h3>文件柜</h3><p>与办公桌配套的文件柜和小型储物柜。</p>');
    html = html.replace('<h3>梳妆台与镜子</h3><p>多抽屉梳妆台配套同系列梳妆镜以凑成套。</p>', '<h3>书架</h3><p>多层书架，提供充足的展示和收纳空间。</p>');
    html = html.replace('<span class=fnum>床架</span>', '<span class=fnum>办公桌</span>');
    html = html.replace('<span class=fnum>床头柜</span>', '<span class=fnum>文件柜</span>');
    html = html.replace('<span class=fnum>梳妆台</span>', '<span class=fnum>书架</span>');
    
    html = html.replace('<span class=fnum>五斗柜</span><h3>五斗柜</h3><p>高柜式五斗柜，充分利用垂直空间，不占用地面面积。</p>', '');
    html = html.replace('<span class=fnum>大衣柜</span><h3>大衣柜</h3><p>双门或多门大衣柜，适合没有内置衣橱的卧室。</p>', '');
    html = html.replace('<span class=fnum>床垫系列</span><h3>床垫系列</h3><p>床垫系列完善卧室套件，确保客户的房间家具有一次送达。</p>', '');
    
    // Fix Showcase
    html = html.replace('<img src="../../../assets/images/hero-bedroom.jpg?v=20260516"', '<img src="../../assets/images/pdf3/img-260.jpg"');
    html = html.replace('带平台床与大衣柜的白色高光现代卧室家具套件', '现代办公家具');
    html = html.replace('<strong>高光烤漆饰面</strong>高雅大方的现代白色高光家具套件。', '<strong>现代设计</strong>高雅大方的现代办公家具套件。');
    
    html = html.replace('<img src="../../../assets/images/bedroom-suite.jpg?v=20260516"', '<img src="../../assets/images/pdf3/img-341.jpg"');
    html = html.replace('配备软包纽扣拉点床头与长凳的卧室系列', '实用书架');
    html = html.replace('<strong>软包床架</strong>精美舒适的软包床头板及床架。', '<strong>多层书架</strong>精美实用的储物书架。');
    
    html = html.replace('<img src="../../../assets/images/bedroom-detail.jpg?v=20260516"', '<img src="../../assets/images/pdf3/img-380.jpg"');
    html = html.replace('软包床旁带抽屉的现代床头柜', '置物架');
    html = html.replace('<strong>配套柜类家具</strong>与各床饰面完美呼应的床头柜和储物柜。', '<strong>储物架</strong>实用美观的置物架。');
    
    // Fix Bottom CTA
    html = html.replace('<span class=eyebrow>床垫系列</span><h2>床垫系列完善整套</h2><p class=lead>我们常备床垫产品与卧室家具配套销售。由于床垫具有专属的保养和退换货政策，建议在订购前仔细阅读说明。</p>', '');
    html = html.replace('<span class=eyebrow>卧室系列</span><h2>索取卧室系列报价及库存</h2><p>请联系我们的团队获取最新的卧室家具报价、饰面及库存，或浏览其他系列。</p>', '<span class=eyebrow>办公系列</span><h2>索取办公系列报价及库存</h2><p>请联系我们的团队获取最新的办公家具报价、饰面及库存，或浏览其他系列。</p>');
    
    fs.writeFileSync('zh/office/index.html', html);
}

function cleanOfficeEn() {
    let html = fs.readFileSync('office/index.html', 'utf-8');
    
    // Fix Hero
    html = html.replace('<h1>Office</h1>', '<h1>Office Furniture</h1>');
    html = html.replace('<p>Mattresses engineered for scientific sleep and ultimate comfort.</p>', '<p>Office furniture designed for productivity and ultimate comfort.</p>');
    html = html.replace('Collection 04', 'Collection 05');
    
    // Fix Split Body
    html = html.replace('<h2>Modern Coordinated Bedroom Suites</h2>', '<h2>Modern Coordinated Office Suites</h2>');
    html = html.replace('<p>Our bedroom collections are designed with harmony in mind. Beds, nightstands, dressers, and chests are perfectly matched in finish and proportion, allowing you to furnish a complete room or build it piece by piece over time.</p>', '<p>Our office collections are designed with harmony in mind. Desks, bookcases, and cabinets are perfectly matched in finish and proportion, allowing you to furnish a complete workspace or build it piece by piece over time.</p>');
    html = html.replace('<p>Finishes range from sleek high-gloss lacquers to stylish upholstered designs, covering the most sought-after looks in the New York market.</p>', '<p>Finishes range from sleek modern designs to classic wooden styles, covering the most sought-after looks in the New York market.</p>');
    
    // Fix Features
    html = html.replace('<h2>What\'s in a Bedroom Suite?</h2>', '<h2>What\'s in an Office Suite?</h2>');
    html = html.replace('<h3>Beds</h3><p>Platform, storage, and upholstered beds in modern finishes, built to standard US sizing.</p>', '<h3>Desks</h3><p>Modern design office desks with spacious tabletops and ergonomic heights.</p>');
    html = html.replace('<h3>Nightstands</h3><p>Matching bedside tables and compact storage units to pair with our beds.</p>', '<h3>Cabinets</h3><p>Matching file cabinets and compact storage units to pair with our desks.</p>');
    html = html.replace('<h3>Dressers & Mirrors</h3><p>Multi-drawer dressers designed to be paired with matching mirrors for a complete vanity setup.</p>', '<h3>Bookcases</h3><p>Multi-tier bookcases providing ample display and storage space.</p>');
    html = html.replace('<span class=fnum>Beds</span>', '<span class=fnum>Desks</span>');
    html = html.replace('<span class=fnum>Nightstands</span>', '<span class=fnum>Cabinets</span>');
    html = html.replace('<span class=fnum>Dressers</span>', '<span class=fnum>Bookcases</span>');
    
    html = html.replace('<span class=fnum>Chests</span><h3>Chests</h3><p>Tallboy chests that maximize vertical storage without eating up floor space.</p>', '');
    html = html.replace('<span class=fnum>Wardrobes</span><h3>Wardrobes</h3><p>Two or multi-door armoires perfect for bedrooms lacking built-in closets.</p>', '');
    html = html.replace('<span class=fnum>Mattresses</span><h3>Mattresses</h3><p>Complementary mattress collections to ensure your customers get a complete room delivered at once.</p>', '');
    
    // Fix Showcase
    html = html.replace('<img src="../../assets/images/hero-bedroom.jpg?v=20260516"', '<img src="../assets/images/pdf3/img-260.jpg"');
    html = html.replace('<strong>High-Gloss Lacquer</strong>Elegant and modern white high-gloss furniture suites.', '<strong>Modern Design</strong>Elegant and modern office furniture suites.');
    
    html = html.replace('<img src="../../assets/images/bedroom-suite.jpg?v=20260516"', '<img src="../assets/images/pdf3/img-341.jpg"');
    html = html.replace('<strong>Upholstered Beds</strong>Beautiful and comfortable upholstered headboards and frames.', '<strong>Bookcases</strong>Beautiful and practical storage bookcases.');
    
    html = html.replace('<img src="../../assets/images/bedroom-detail.jpg?v=20260516"', '<img src="../assets/images/pdf3/img-380.jpg"');
    html = html.replace('<strong>Case Goods</strong>Nightstands and chests that perfectly echo the finish of each bed.', '<strong>Shelving</strong>Practical and aesthetic shelving units.');
    
    // Fix Bottom CTA
    html = html.replace('<span class=eyebrow>Mattresses</span><h2>Complete the Set with Our Mattresses</h2><p class=lead>We stock mattresses to be sold alongside our bedroom furniture. As mattresses carry specific care and return policies, please review the guidelines before ordering.</p>', '');
    html = html.replace('<span class=eyebrow>Bedroom Collection</span><h2>Request Bedroom Pricing & Inventory</h2><p>Contact our team to get the latest pricing, finishes, and stock status for our bedroom furniture, or explore our other collections.</p>', '<span class=eyebrow>Office Collection</span><h2>Request Office Pricing & Inventory</h2><p>Contact our team to get the latest pricing, finishes, and stock status for our office furniture, or explore our other collections.</p>');
    
    fs.writeFileSync('office/index.html', html);
}

cleanOfficeZh();
cleanOfficeEn();
