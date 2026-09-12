import os
import re

# ==========================================
# 1. UPDATE DINING PAGES (ZH & EN)
# ==========================================

zh_dining_cards = [
    # TH Products (no prices)
    {
        'main_img': '../../assets/images/th/TH-BZ0396-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-BZ0396-main.jpg?v=20260907', 'Main')],
        'title_zh': 'BZ-0396 / BY-0396',
        'title_en': 'BZ-0396 / BY-0396',
        'desc_zh': 'BZ-0396 大理石纹折叠伸缩餐桌 + BY-0396 餐椅套组',
        'desc_en': 'BZ-0396 Marble Extendable Dining Table & BY-0396 Chairs Set',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['1+6组合', '精选'],
        'tags_en': ['1+6 Set', 'Featured'],
        'id': 'th-bz0396-main'
    },
    {
        'main_img': '../../assets/images/th/TH-BZ2192-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-BZ2192-main.jpg?v=20260907', 'Main')],
        'title_zh': 'BZ-2192 / RJ-366',
        'title_en': 'BZ-2192 / RJ-366',
        'desc_zh': 'BZ-2192 奶油白轻奢圆变方伸缩餐桌 + RJ-366 餐椅套组',
        'desc_en': 'BZ-2192 Cream Round-to-Square Dining Table & RJ-366 Chairs Set',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['1+6组合', '极简岩板'],
        'tags_en': ['1+6 Set', 'Sintered Stone'],
        'id': 'th-bz2192-main'
    },
    {
        'main_img': '../../assets/images/th/TH-BZ0296-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-BZ0296-main.jpg?v=20260907', 'Main')],
        'title_zh': 'BZ-0296 / BY-0296',
        'title_en': 'BZ-0296 / BY-0296',
        'desc_zh': 'BZ-0296 现代岩板储物柱转盘餐桌 + BY-0296 餐椅套组',
        'desc_en': 'BZ-0296 Sintered Stone Turntable Dining Table & BY-0296 Chairs Set',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['1+6组合', '轻奢'],
        'tags_en': ['1+6 Set', 'Luxury'],
        'id': 'th-bz0296-main'
    },
    {
        'main_img': '../../assets/images/th/TH-DT04-1-main.jpg?v=20260907',
        'thumbs': [
            ('../../assets/images/th/TH-DT04-1-main.jpg?v=20260907', 'Square Mode'),
            ('../../assets/images/th/TH-DT04-2-main.jpg?v=20260907', 'Round Mode')
        ],
        'title_zh': 'TH-DT04',
        'title_en': 'TH-DT04',
        'desc_zh': 'TH-DT04 轻奢旋转转盘圆方两用伸缩餐桌 (配4椅2凳全套)',
        'desc_en': 'TH-DT04 Luxury Extendable Round/Square Dining Table Set',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['奢石台面', '1+6组合'],
        'tags_en': ['Luxury Stone', '1+6 Set'],
        'id': 'th-dt04-main'
    },
    # 2026 PJ Dining Products
    {
        'main_img': '../../assets/images/pdf3/img-141.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-141.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-142.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-143.jpg', 'Detail')
        ],
        'title_zh': '4160 / 4110 GREEN',
        'title_en': '4160 / 4110 GREEN',
        'desc_zh': '4160 经典实木餐桌与 4110 绿色软包实木餐椅组合，原木质感，坚固耐用。',
        'desc_en': '4160 Solid Wood Dining Table with 4110 Green Upholstered Chairs.',
        'price_zh': '折后 餐桌: $139.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $139.00 | Chair: $59.95/ea',
        'tags_zh': ['实木餐桌', '精选'],
        'tags_en': ['Solid Wood', 'Featured'],
        'id': 'pdf3-set-26-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-144.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-144.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-145.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-146.jpg', 'Detail')
        ],
        'title_zh': '4130 / 4110 GREEN',
        'title_en': '4130 / 4110 GREEN',
        'desc_zh': '4130 紧凑型实木餐桌与 4110 绿色实木餐椅组合，适合中小户型。',
        'desc_en': '4130 Compact Solid Wood Dining Table with 4110 Green Chairs.',
        'price_zh': '折后 餐桌: $109.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $109.00 | Chair: $59.95/ea',
        'tags_zh': ['实木餐桌', '紧凑户型'],
        'tags_en': ['Solid Wood', 'Compact'],
        'id': 'pdf3-set-27-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-147.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-147.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-148.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-149.jpg', 'Detail')
        ],
        'title_zh': '4160 / 4110 IVY',
        'title_en': '4160 / 4110 IVY',
        'desc_zh': '4160 实木餐桌搭配 4110 象牙白软包实木餐椅，优雅温馨。',
        'desc_en': '4160 Solid Wood Dining Table with 4110 Ivory Chairs.',
        'price_zh': '折后 餐桌: $139.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $139.00 | Chair: $59.95/ea',
        'tags_zh': ['象牙白', '实木餐桌'],
        'tags_en': ['Ivory', 'Solid Wood'],
        'id': 'pdf3-set-28-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-150.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-150.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-151.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-152.jpg', 'Detail')
        ],
        'title_zh': '4130 / 4110 IVY',
        'title_en': '4130 / 4110 IVY',
        'desc_zh': '4130 紧凑型实木餐桌搭配 4110 象牙白餐椅，简约百搭。',
        'desc_en': '4130 Solid Wood Dining Table with 4110 Ivory Chairs.',
        'price_zh': '折后 餐桌: $109.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $109.00 | Chair: $59.95/ea',
        'tags_zh': ['简约实木', '精选'],
        'tags_en': ['Solid Wood', 'Featured'],
        'id': 'pdf3-set-29-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-153.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-153.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-154.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-155.jpg', 'Detail')
        ],
        'title_zh': '4160 / 4110 GRAY',
        'title_en': '4160 / 4110 GRAY',
        'desc_zh': '4160 实木餐桌搭配 4110 现代灰软包实木餐椅，质朴耐看。',
        'desc_en': '4160 Solid Wood Dining Table with 4110 Gray Chairs.',
        'price_zh': '折后 餐桌: $139.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $139.00 | Chair: $59.95/ea',
        'tags_zh': ['现代灰', '实木全套'],
        'tags_en': ['Gray', 'Solid Wood'],
        'id': 'pdf3-set-30-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-156.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-156.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-157.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-158.jpg', 'Detail')
        ],
        'title_zh': '4130 / 4110 GRAY',
        'title_en': '4130 / 4110 GRAY',
        'desc_zh': '4130 实木餐桌搭配 4110 现代灰餐椅，小空间理想之选。',
        'desc_en': '4130 Solid Wood Dining Table with 4110 Gray Chairs.',
        'price_zh': '折后 餐桌: $109.00 | 餐椅: $59.95/把',
        'price_en': 'Sale: Table: $109.00 | Chair: $59.95/ea',
        'tags_zh': ['小空间推荐', '精选'],
        'tags_en': ['Compact', 'Featured'],
        'id': 'pdf3-set-31-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-159.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-159.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-160.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-161.jpg', 'Detail')
        ],
        'title_zh': '3016T / 3000WH',
        'title_en': '3016T / 3000WH',
        'desc_zh': '轻奢白大理石金属餐桌，搭配 1600WH-GOLD / 1500WH-GOLD 轻奢餐椅。',
        'desc_en': 'Luxury White Marble Dining Table with Gold Stainless Steel Chairs.',
        'price_zh': '折后 大理石餐桌: $549.00 | 餐椅: $99.00 - $149.00/把',
        'price_en': 'Sale: Marble Table: $549.00 | Chairs: $99.00 - $149.00/ea',
        'tags_zh': ['大理石台面', '轻奢镀金'],
        'tags_en': ['Marble Top', 'Gold Finish'],
        'id': 'pdf3-set-32-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-165.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-165.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-166.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-167.jpg', 'Detail')
        ],
        'title_zh': '3011T / 3000BK',
        'title_en': '3011T / 3000BK',
        'desc_zh': '黑大理石轻奢金属餐桌，搭配 1003BK-GOLD / 2680BK-GOLD 黑金轻奢餐椅。',
        'desc_en': 'Luxury Black Marble Dining Table with Black & Gold Chairs.',
        'price_zh': '折后 大理石餐桌: $549.00 | 餐椅: $85.00 - $149.00/把',
        'price_en': 'Sale: Marble Table: $549.00 | Chairs: $85.00 - $149.00/ea',
        'tags_zh': ['黑大理石', '黑金轻奢'],
        'tags_en': ['Black Marble', 'Luxury Gold'],
        'id': 'pdf3-set-33-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-168.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-168.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-169.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-170.jpg', 'Detail')
        ],
        'title_zh': '3010T / 3000BK & 3002BK',
        'title_en': '3010T / 3000BK & 3002BK',
        'desc_zh': '黑大理石 / 黑钢化玻璃台面金属餐桌，沉稳大气，配 1003BK-GOLD 餐椅。',
        'desc_en': 'Black Marble / Glass Dining Table with Metal Base & Luxury Chairs.',
        'price_zh': '折后 餐桌: $499.00 | 餐椅: $149.00/把',
        'price_en': 'Sale: Table: $499.00 | Chair: $149.00/ea',
        'tags_zh': ['大理石/玻璃可选', '精选'],
        'tags_en': ['Marble/Glass', 'Featured'],
        'id': 'pdf3-set-34-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-172.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-172.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-173.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-175.jpg', 'Detail')
        ],
        'title_zh': '3010T / 3000WH & 3002WH',
        'title_en': '3010T / 3000WH & 3002WH',
        'desc_zh': '白大理石 / 白钢化玻璃台面金属餐桌，配 1002WH-GOLD 白金轻奢餐椅。',
        'desc_en': 'White Marble / Glass Dining Table with Gold Stainless Chairs.',
        'price_zh': '折后 餐桌: $499.00 | 餐椅: $149.00/把',
        'price_en': 'Sale: Table: $499.00 | Chair: $149.00/ea',
        'tags_zh': ['白大理石/白玻璃', '轻奢'],
        'tags_en': ['White Marble/Glass', 'Luxury'],
        'id': 'pdf3-set-35-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-176.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-176.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-177.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-178.jpg', 'Detail')
        ],
        'title_zh': '3012T / 3000GRAY',
        'title_en': '3012T / 3000GRAY',
        'desc_zh': '灰大理石台面不锈钢镀铬餐桌，搭配 2680GRAY-CHROME 铬框餐椅。',
        'desc_en': 'Gray Marble Dining Table with Chrome Frame Chairs.',
        'price_zh': '折后 大理石餐桌: $499.00 | 餐椅: $79.00/把',
        'price_en': 'Sale: Marble Table: $499.00 | Chair: $79.00/ea',
        'tags_zh': ['灰大理石', '镀铬不锈钢'],
        'tags_en': ['Gray Marble', 'Chrome Frame'],
        'id': 'pdf3-set-36-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-179.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-179.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-181.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-182.jpg', 'Detail')
        ],
        'title_zh': '3000T / 3000GRAY',
        'title_en': '3000T / 3000GRAY',
        'desc_zh': '现代灰大理石餐桌，搭配 1200GRAY 灰色软包餐椅。',
        'desc_en': 'Gray Marble Dining Table with 1200GRAY Chairs.',
        'price_zh': '折后 大理石餐桌: $399.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Marble Table: $399.00 | Chair: $89.00/ea',
        'tags_zh': ['灰大理石', '现代极简'],
        'tags_en': ['Gray Marble', 'Minimalist'],
        'id': 'pdf3-set-37-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-183.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-183.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-184.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-185.jpg', 'Detail')
        ],
        'title_zh': '3000T / 3002WH & 3000BK',
        'title_en': '3000T / 3002WH & 3000BK',
        'desc_zh': '现代白玻璃 / 黑大理石餐桌，简约时尚，配 1500 CHROME 餐椅。',
        'desc_en': 'Modern Glass / Marble Top Dining Table with Chairs.',
        'price_zh': '折后 玻璃桌: $349.00 | 大理石桌: $399.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Glass Table: $349.00 | Marble Table: $399.00 | Chair: $89.00/ea',
        'tags_zh': ['玻璃/大理石', '精选'],
        'tags_en': ['Glass/Marble', 'Featured'],
        'id': 'pdf3-set-38-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-188.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-188.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-189.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-190.jpg', 'Detail')
        ],
        'title_zh': '3000T / 3000BK',
        'title_en': '3000T / 3000BK',
        'desc_zh': '黑大理石餐桌搭配 1500GRAY / 1301BK 铬色/黑色现代餐椅。',
        'desc_en': 'Black Marble Dining Table with Modern Chairs.',
        'price_zh': '折后 大理石餐桌: $399.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Marble Table: $399.00 | Chair: $89.00/ea',
        'tags_zh': ['黑大理石', '精选'],
        'tags_en': ['Black Marble', 'Featured'],
        'id': 'pdf3-set-39-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-191.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-191.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-192.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-193.jpg', 'Detail')
        ],
        'title_zh': '3000T / 3000GRAY',
        'title_en': '3000T / 3000GRAY',
        'desc_zh': '灰大理石餐桌搭配 1500GRAY-CHROME / 1301BK 铬框餐椅组合。',
        'desc_en': 'Gray Marble Dining Table with Chrome Chairs.',
        'price_zh': '折后 大理石餐桌: $399.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Marble Table: $399.00 | Chair: $89.00/ea',
        'tags_zh': ['灰大理石', '精选'],
        'tags_en': ['Gray Marble', 'Featured'],
        'id': 'pdf3-set-40-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-194.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-194.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-195.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-196.jpg', 'Detail')
        ],
        'title_zh': '3000T / 3002BK',
        'title_en': '3000T / 3002BK',
        'desc_zh': '黑钢化玻璃台面餐桌，搭配 1500GRAY / 1301BK 现代不锈钢餐椅。',
        'desc_en': 'Black Tempered Glass Dining Table with Stainless Chairs.',
        'price_zh': '折后 玻璃餐桌: $349.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Glass Table: $349.00 | Chair: $89.00/ea',
        'tags_zh': ['黑钢化玻璃', '精选'],
        'tags_en': ['Glass Top', 'Featured'],
        'id': 'pdf3-set-41-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-197.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-197.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-198.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-199.jpg', 'Detail')
        ],
        'title_zh': '3000T / 1001BK',
        'title_en': '3000T / 1001BK',
        'desc_zh': '大理石/玻璃餐桌搭配 1001BK 奢华黑金餐椅。',
        'desc_en': 'Marble / Glass Dining Table with 1001BK Luxury Chairs.',
        'price_zh': '折后 餐桌: $349.00 - $399.00 | 餐椅: $149.00/把',
        'price_en': 'Sale: Table: $349.00 - $399.00 | Chair: $149.00/ea',
        'tags_zh': ['奢华黑金', '精选'],
        'tags_en': ['Black Gold', 'Featured'],
        'id': 'pdf3-set-42-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-200.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-200.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-201.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-203.jpg', 'Detail')
        ],
        'title_zh': '3008T / 3008GRAY',
        'title_en': '3008T / 3008GRAY',
        'desc_zh': '圆形大理石台面餐桌，质感温润细腻，配 1500GRAY-CHROME / 1200GRAY 餐椅。',
        'desc_en': 'Round Gray Marble Dining Table with Chrome Frame Chairs.',
        'price_zh': '折后 圆大理石桌: $399.00 | 餐椅: $89.00/把',
        'price_en': 'Sale: Round Marble Table: $399.00 | Chair: $89.00/ea',
        'tags_zh': ['圆大理石桌', '精选'],
        'tags_en': ['Round Marble', 'Featured'],
        'id': 'pdf3-set-43-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-205.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-205.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-206.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-207.jpg', 'Detail')
        ],
        'title_zh': '3007T / 3007WH',
        'title_en': '3007T / 3007WH',
        'desc_zh': '圆形白玻璃餐桌，搭配 1403WH-GOLD / 1401BK 轻奢金属餐椅。',
        'desc_en': 'Round White Glass Dining Table with Luxury Chairs.',
        'price_zh': '折后 圆玻璃桌: $349.00 | 餐椅: $99.00/把',
        'price_en': 'Sale: Round Glass Table: $349.00 | Chair: $99.00/ea',
        'tags_zh': ['圆玻璃桌', '轻奢'],
        'tags_en': ['Round Glass', 'Luxury'],
        'id': 'pdf3-set-44-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-208.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-208.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-209.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-211.jpg', 'Detail')
        ],
        'title_zh': '3102T',
        'title_en': '3102T',
        'desc_zh': '36"x60" 长方形钢化玻璃餐桌，搭配 2680 焊接不锈钢镀铬餐椅。',
        'desc_en': '36"x60" Tempered Glass Dining Table with 2680 Chrome Chairs.',
        'price_zh': '折后 玻璃桌: $149.00 | 餐椅: $79.00/把',
        'price_en': 'Sale: Glass Table: $149.00 | Chair: $79.00/ea',
        'tags_zh': ['钢化玻璃', '不锈钢脚'],
        'tags_en': ['Glass Top', 'Stainless Steel'],
        'id': 'pdf3-set-45-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-215.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-215.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-217.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-219.jpg', 'Detail')
        ],
        'title_zh': '2240 / 2250',
        'title_en': '2240 / 2250',
        'desc_zh': '2240 现代岩板餐桌 / 2250 玻璃餐桌，搭配 2800BLACK-GRAY 餐椅。',
        'desc_en': '2240 Sintered Stone / 2250 Glass Dining Table with Chairs.',
        'price_zh': '折后 2240岩板: $75.00 | 2250玻璃: $59.00 | 餐椅: $30.00/把',
        'price_en': 'Sale: 2240 Stone: $75.00 | 2250 Glass: $59.00 | Chair: $30.00/ea',
        'tags_zh': ['岩板/玻璃', '高性价比'],
        'tags_en': ['Stone/Glass', 'Best Value'],
        'id': 'pdf3-set-46-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-221.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-221.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-223.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-225.jpg', 'Detail')
        ],
        'title_zh': '3101T / 3112T / 3102T',
        'title_en': '3101T / 3112T / 3102T',
        'desc_zh': '钢化玻璃餐桌系列（43"圆桌 / 30"x48" / 36"x60"可选），配 2800 镀铬餐椅。',
        'desc_en': 'Glass Dining Table Series (43" Round / 30"x48" / 36"x60").',
        'price_zh': '折后 3101T(圆): $129.00 | 3112T: $119.00 | 3102T: $149.00 | 餐椅: $35.00/把',
        'price_en': 'Sale: 3101T(Round): $129.00 | 3112T: $119.00 | 3102T: $149.00 | Chair: $35.00/ea',
        'tags_zh': ['多尺寸可选', '精选'],
        'tags_en': ['Multi-Size', 'Featured'],
        'id': 'pdf3-set-47-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-227.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-227.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-229.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-231.jpg', 'Detail')
        ],
        'title_zh': '3105T / 3114T / 3104T',
        'title_en': '3105T / 3114T / 3104T',
        'desc_zh': '轻奢金框钢化玻璃餐桌系列（43"圆桌 / 30"x48" / 36"x60"可选），配 2800 镀金餐椅。',
        'desc_en': 'Gold Frame Glass Dining Table Series (43" Round / 30"x48" / 36"x60").',
        'price_zh': '折后 3105T(圆): $119.00 - $139.00 | 3114T: $129.00 | 3104T: $159.00 | 餐椅: $40.00/把',
        'price_en': 'Sale: 3105T(Round): $119.00 - $139.00 | 3114T: $129.00 | 3104T: $159.00 | Chair: $40.00/ea',
        'tags_zh': ['镀金轻奢', '精选'],
        'tags_en': ['Gold Finish', 'Featured'],
        'id': 'pdf3-set-48-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-232.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-232.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-233.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-234.jpg', 'Detail')
        ],
        'title_zh': '3103T / 3106T / 4031T',
        'title_en': '3103T / 3106T / 4031T',
        'desc_zh': '3103T (43"圆) / 3106T (36"x60") 玻璃餐桌与 4031T 仿大理石餐桌，搭配 2650 / 4026CA 餐椅。',
        'desc_en': 'Glass Dining Tables & 4031T Faux Marble Dining Table with Chairs.',
        'price_zh': '折后 3103T: $139.00 | 3106T: $139.00 | 4031T: $139.00 | 餐椅: $49.95 - $69.00/把',
        'price_en': 'Sale: 3103T: $139.00 | 3106T: $139.00 | 4031T: $139.00 | Chairs: $49.95 - $69.00/ea',
        'tags_zh': ['仿大理石/玻璃', '精选'],
        'tags_en': ['Marble/Glass', 'Featured'],
        'id': 'pdf3-set-49-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-272.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-272.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-274.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-278.jpg', 'Detail')
        ],
        'title_zh': '2206 / 2216 / 4003 / 4114',
        'title_en': '2206 / 2216 / 4003 / 4114',
        'desc_zh': '多功能早餐桌、吧台桌及 1+4 / 1+2 组合套件，经济实用。',
        'desc_en': 'Breakfast & Bar Table Sets (Table & Chairs Complete Sets).',
        'price_zh': '折后 4003三件套: $119.00 | 4114五件套: $179.00 | 2206/2216套组: $199.00',
        'price_en': 'Sale: 4003 3-PC Set: $119.00 | 4114 5-PC Set: $179.00 | 2206/2216 Set: $199.00',
        'tags_zh': ['整套组合', '高性价比'],
        'tags_en': ['Complete Sets', 'Best Value'],
        'id': 'pdf3-set-51-main'
    }
]

def render_cards(cards, is_zh=True):
    out = []
    for c in cards:
        prefix = '../../' if is_zh else '../'
        main_img = c['main_img']
        if not is_zh:
            main_img = main_img.replace('../../', '../')
        
        cid = c['id']
        thumbs_html = []
        for t_src, t_alt in c['thumbs']:
            src = t_src if is_zh else t_src.replace('../../', '../')
            active_cls = ' active' if t_src == c['thumbs'][0][0] else ''
            thumbs_html.append(f'                <img src="{src}" alt="{t_alt}" class="sofa-thumb{active_cls}" onclick="changeImage(this, \'{cid}\')">')
        
        title = c['title_zh'] if is_zh else c['title_en']
        desc = c['desc_zh'] if is_zh else c['desc_en']
        price = c['price_zh'] if is_zh else c['price_en']
        tags = c['tags_zh'] if is_zh else c['tags_en']
        
        details_html = []
        if price:
            details_html.append(f'                    <span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">{price}</span>')
        for tag in tags:
            details_html.append(f'                    <span class="detail-tag">{tag}</span>')
        
        card_html = f'''        <div class="sofa-card reveal">
            <div class="sofa-img-container">
                <img src="{main_img}" alt="{title}" class="main-sofa-img" id="{cid}" loading="lazy">
            </div>
            <div class="sofa-thumbnails">
{chr(10).join(thumbs_html)}
            </div>
            <div class="sofa-info">
                <h3>{title}</h3>
                <p>{desc}</p>
                <div class="sofa-details">
{chr(10).join(details_html)}
                </div>
            </div>
        </div>'''
        out.append(card_html)
    return '\n\n'.join(out)

# Update zh/dining/index.html
zh_dining_path = 'zh/dining/index.html'
zh_dining_content = open(zh_dining_path).read()
grid_pattern = r'(<div class="sofa-grid">)[\s\S]*?(<\/div>\s*<\/main>)'
rendered_zh_dining = render_cards(zh_dining_cards, is_zh=True)
zh_dining_content = re.sub(grid_pattern, f'\\1\n\n{rendered_zh_dining}\n    \\2', zh_dining_content)
open(zh_dining_path, 'w').write(zh_dining_content)
print("Updated zh/dining/index.html")

# Update dining/index.html
en_dining_path = 'dining/index.html'
en_dining_content = open(en_dining_path).read()
rendered_en_dining = render_cards(zh_dining_cards, is_zh=False)
en_dining_content = re.sub(grid_pattern, f'\\1\n\n{rendered_en_dining}\n    \\2', en_dining_content)
open(en_dining_path, 'w').write(en_dining_content)
print("Updated dining/index.html")

# ==========================================
# 2. UPDATE LIVING ROOM PAGES (ZH & EN)
# ==========================================

# Let's define the PJ Living Room cards + TH Luxury Suites
living_room_cards = [
    # TH Products (Clean without prices)
    {
        'main_img': '../../assets/images/th/TH-010-main.jpg?v=20260907',
        'thumbs': [
            ('../../assets/images/th/TH-010-main.jpg?v=20260907', 'Main'),
            ('../../assets/images/th/TH-010-detail-1.jpg?v=20260907', 'Bed Mode'),
            ('../../assets/images/th/TH-010-detail-2.jpg?v=20260907', 'Sofa Mode')
        ],
        'title_zh': 'TH010#',
        'title_en': 'TH010#',
        'desc_zh': 'TH010# 日式多功能折叠沙发床',
        'desc_en': 'TH010# Japanese Folding Futon Sofa Bed',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['坐卧两用', '节省空间'],
        'tags_en': ['Dual Mode', 'Space Saving'],
        'id': 'th-010-main'
    },
    {
        'main_img': '../../assets/images/th/TH-SF02-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-SF02-main.jpg?v=20260907', 'Main')],
        'title_zh': 'TH-SF02',
        'title_en': 'TH-SF02',
        'desc_zh': 'TH-SF02 多功能拉伸储物充电沙发床',
        'desc_en': 'TH-SF02 Multi-function Pull-out Sofa Bed with Storage & USB',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['坐卧两用', 'USB充电'],
        'tags_en': ['Dual Mode', 'USB Charging'],
        'id': 'th-sf02-main'
    },
    {
        'main_img': '../../assets/images/th/TH-SF801-3-main.jpg?v=20260907',
        'thumbs': [
            ('../../assets/images/th/TH-SF801-3-main.jpg?v=20260907', '3-Seater'),
            ('../../assets/images/th/TH-SF801-2-main.jpg?v=20260907', '2-Seater')
        ],
        'title_zh': 'TH-SF801',
        'title_en': 'TH-SF801',
        'desc_zh': 'TH-SF801 现代简约舒适皮艺三人位/双人位沙发',
        'desc_en': 'TH-SF801 Modern Leather Sofa Set (3-Seater / 2-Seater)',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['头层牛皮', '3+2套组'],
        'tags_en': ['Top Grain Leather', '3+2 Set'],
        'id': 'th-sf801-main'
    },
    {
        'main_img': '../../assets/images/th/TH-SF802-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-SF802-main.jpg?v=20260907', 'Main')],
        'title_zh': 'TH-SF802',
        'title_en': 'TH-SF802',
        'desc_zh': 'TH-SF802 现代极简真皮L型转角贵妃沙发',
        'desc_en': 'TH-SF802 Minimalist Top Grain Leather Sectional Sofa',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['可调头枕', '极简金属脚'],
        'tags_en': ['Adjustable Headrest', 'Metal Legs'],
        'id': 'th-sf802-main'
    },
    {
        'main_img': '../../assets/images/th/TH-SF803-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-SF803-main.jpg?v=20260907', 'Main')],
        'title_zh': 'TH-SF803',
        'title_en': 'TH-SF803',
        'desc_zh': 'TH-SF803 豪华头等舱电动真皮转角功能沙发',
        'desc_en': 'TH-SF803 Luxury Power Reclining Leather Sectional',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['电动躺位', '头等舱体验'],
        'tags_en': ['Power Recliner', 'First Class'],
        'id': 'th-sf803-main'
    },
    {
        'main_img': '../../assets/images/th/TH-DJ6661-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-DJ6661-main.jpg?v=20260907', 'Main')],
        'title_zh': 'DJ-6661',
        'title_en': 'DJ-6661',
        'desc_zh': 'DJ-6661 多功能真皮/PVC电动可调节转角沙发',
        'desc_en': 'DJ-6661 Power Reclining Sectional Sofa with Adjustable Headrest',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['单电机电动位', '3头枕调节'],
        'tags_en': ['Power Recline', 'Adjustable Headrests'],
        'id': 'th-dj6661-main'
    },
    {
        'main_img': '../../assets/images/th/TH-SF805-main.jpg?v=20260907',
        'thumbs': [('../../assets/images/th/TH-SF805-main.jpg?v=20260907', 'Main')],
        'title_zh': 'TH-SF805',
        'title_en': 'TH-SF805',
        'desc_zh': 'TH-SF805 弧形大转角头等舱双电动躺位真皮沙发',
        'desc_en': 'TH-SF805 Curved Power Reclining Leather Sectional',
        'price_zh': None,
        'price_en': None,
        'tags_zh': ['双电动位', '奢华弧形'],
        'tags_en': ['Dual Power', 'Curved Luxury'],
        'id': 'th-sf805-main'
    },

    # 2026 PJ Sofa Beds & Sofas
    {
        'main_img': '../../assets/images/pdf3/img-102.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-102.jpg', 'Main'),
            ('../../assets/images/pdf3/img-103.jpg', 'Detail')
        ],
        'title_zh': '9701BR',
        'title_en': '9701BR',
        'desc_zh': '9701BR 多功能带储物空间折叠沙发床，坐卧两用，节省空间。',
        'desc_en': '9701BR Multi-functional Sofa Bed with Built-in Storage.',
        'price_zh': '折后 $299.00',
        'price_en': 'Sale: $299.00',
        'tags_zh': ['带储物箱', '沙发床'],
        'tags_en': ['Storage', 'Sofa Bed'],
        'id': 'pj-9701br-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-104.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-104.jpg', 'Main'),
            ('../../assets/images/pdf3/img-105.jpg', 'Detail')
        ],
        'title_zh': '2406 (IVY / GRAY / BL)',
        'title_en': '2406 (IVY / GRAY / BL)',
        'desc_zh': '2406 现代简约布艺折叠沙发床（象牙白 / 灰色 / 蓝色可选），坐卧两用。',
        'desc_en': '2406 Modern Fabric Folding Sofa Bed (Ivory / Gray / Blue).',
        'price_zh': '折后 $169.00',
        'price_en': 'Sale: $169.00',
        'tags_zh': ['三色可选', '布艺沙发床'],
        'tags_en': ['3 Colors', 'Fabric Sofa Bed'],
        'id': 'pj-2406-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-106.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-106.jpg', 'Main'),
            ('../../assets/images/pdf3/img-107.jpg', 'Detail')
        ],
        'title_zh': '2402 (RD / GR / BL)',
        'title_en': '2402 (RD / GR / BL)',
        'desc_zh': '2402 紧凑型折叠沙发床（红色 / 灰色 / 蓝色可选），特惠热销款。',
        'desc_en': '2402 Compact Folding Sofa Bed (Red / Gray / Blue).',
        'price_zh': '折后 $149.00',
        'price_en': 'Sale: $149.00 (Special)',
        'tags_zh': ['特惠款', '折叠两用'],
        'tags_en': ['Special Offer', 'Convertible'],
        'id': 'pj-2402-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-096.jpg',
        'thumbs': [('../../assets/images/pdf3/img-096.jpg', 'Main')],
        'title_zh': '9900BK',
        'title_en': '9900BK',
        'desc_zh': '9900BK 黑色 L 型真皮/仿皮转角贵妃榻大沙发，带大容量储物空间。',
        'desc_en': '9900BK Black L-Shape Sectional Sofa with Storage Chaise.',
        'price_zh': '折后 $549.00',
        'price_en': 'Sale: $549.00',
        'tags_zh': ['L型转角', '大容量储物'],
        'tags_en': ['L-Shape Sectional', 'Storage Chaise'],
        'id': 'pj-9900bk-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-097.jpg',
        'thumbs': [('../../assets/images/pdf3/img-097.jpg', 'Main')],
        'title_zh': '9910GRAY',
        'title_en': '9910GRAY',
        'desc_zh': '9910GRAY 现代高级灰 L 型转角贵妃榻大沙发，带大容量储物箱。',
        'desc_en': '9910GRAY Modern Gray L-Shape Sectional Sofa with Storage Chaise.',
        'price_zh': '折后 $549.00',
        'price_en': 'Sale: $549.00',
        'tags_zh': ['高级灰', '储物贵妃榻'],
        'tags_en': ['Gray Finish', 'Storage Chaise'],
        'id': 'pj-9910gray-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-098.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-098.jpg', 'Main'),
            ('../../assets/images/pdf3/img-099.jpg', 'Detail')
        ],
        'title_zh': '9211 / 9212 / 9213',
        'title_en': '9211 / 9212 / 9213',
        'desc_zh': '9211 单人位、9212 双人位及 9213 三人位现代舒适布艺沙发套组。',
        'desc_en': '9211 / 9212 / 9213 Modern Fabric Sofa Collection (Chair / Loveseat / Sofa).',
        'price_zh': '折后 单人: $185.00 | 双人: $265.00 | 三人: $295.00 | 双人+三人套装: $549.00',
        'price_en': 'Sale: Chair: $185.00 | Loveseat: $265.00 | Sofa: $295.00 | Set(2+3): $549.00',
        'tags_zh': ['布艺套组', '组合优惠'],
        'tags_en': ['Fabric Suite', 'Set Value'],
        'id': 'pj-9211-set-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-100.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-100.jpg', 'Main'),
            ('../../assets/images/pdf3/img-101.jpg', 'Detail')
        ],
        'title_zh': '9921 / 9922 / 9923',
        'title_en': '9921 / 9922 / 9923',
        'desc_zh': '9921 单人、9922 双人及 9923 三人位深灰皮质舒适沙发套组。',
        'desc_en': '9921 / 9922 / 9923 Dark Gray Leatherette Sofa Collection.',
        'price_zh': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 双人+三人套装: $479.00',
        'price_en': 'Sale: Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | Set(2+3): $479.00',
        'tags_zh': ['深灰皮质', '套装特惠'],
        'tags_en': ['Dark Gray', 'Set Special'],
        'id': 'pj-9921-set-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-088.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-088.jpg', 'Main'),
            ('../../assets/images/pdf3/img-089.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-091.jpg', 'Detail')
        ],
        'title_zh': '9931 / 9932 / 9933',
        'title_en': '9931 / 9932 / 9933',
        'desc_zh': '9931 单人、9932 双人及 9933 三人位经典黑色皮质沙发套组。',
        'desc_en': '9931 / 9932 / 9933 Classic Black Leatherette Sofa Collection.',
        'price_zh': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 双人+三人套装: $479.00',
        'price_en': 'Sale: Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | Set(2+3): $479.00',
        'tags_zh': ['经典黑皮', '套装特惠'],
        'tags_en': ['Black Finish', 'Set Special'],
        'id': 'pj-9931-set-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-093.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-093.jpg', 'Main'),
            ('../../assets/images/pdf3/img-094.jpg', 'Detail'),
            ('../../assets/images/pdf3/img-095.jpg', 'Detail')
        ],
        'title_zh': '9941 / 9942 / 9943',
        'title_en': '9941 / 9942 / 9943',
        'desc_zh': '9941 单人、9942 双人及 9943 三人位个性红黑拼色皮质沙发套组。',
        'desc_en': '9941 / 9942 / 9943 Two-Tone Red & Black Sofa Collection.',
        'price_zh': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 双人+三人套装: $479.00',
        'price_en': 'Sale: Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | Set(2+3): $479.00',
        'tags_zh': ['红黑拼色', '套装特惠'],
        'tags_en': ['Red/Black Two-Tone', 'Set Special'],
        'id': 'pj-9941-set-main'
    },

    # 2026 PJ Occasional Tables & Consoles
    {
        'main_img': '../../assets/images/pdf3/img-108.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-108.jpg', 'Pink Rose'),
            ('../../assets/images/pdf3/img-109.jpg', 'Gray Rose')
        ],
        'title_zh': '0021PR / 0021GRAY',
        'title_en': '0021PR / 0021GRAY',
        'desc_zh': '粉红玫瑰 / 灰色大理石台面不锈钢框架轻奢玄关台。',
        'desc_en': 'Pink Rose / Gray Marble Console Table with Stainless Frame.',
        'price_zh': '折后 $499.00',
        'price_en': 'Sale: $499.00',
        'tags_zh': ['大理石玄关台', '轻奢'],
        'tags_en': ['Marble Console', 'Luxury'],
        'id': 'pj-0021-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-122.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-122.jpg', '0022款'),
            ('../../assets/images/pdf3/img-124.jpg', '0023款')
        ],
        'title_zh': '0022 / 0023 (GRAY / PR)',
        'title_en': '0022 / 0023 (GRAY / PR)',
        'desc_zh': '0022 / 0023 灰玫瑰 / 粉玫瑰天然大理石台面客厅咖啡桌。',
        'desc_en': '0022 / 0023 Gray / Pink Marble Coffee Table.',
        'price_zh': '折后 0022款: $249.00 | 0023款: $189.00',
        'price_en': 'Sale: 0022: $249.00 | 0023: $189.00',
        'tags_zh': ['大理石茶几', '精选'],
        'tags_en': ['Marble Table', 'Featured'],
        'id': 'pj-0022-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-126.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-126.jpg', '0026边几'),
            ('../../assets/images/pdf3/img-128.jpg', '0024高花架'),
            ('../../assets/images/pdf3/img-130.jpg', '0025矮花架')
        ],
        'title_zh': '0026 / 0024 / 0025',
        'title_en': '0026 / 0024 / 0025',
        'desc_zh': '大理石边几与高矮立柱花架摆件台（灰色 / 粉色可选）。',
        'desc_en': 'Marble End Table & Pedestal Stand (Gray / Pink Rose).',
        'price_zh': '折后 0026边几: $79.00 | 0024高花架: $119.00 | 0025矮花架: $109.00',
        'price_en': 'Sale: 0026 End Table: $79.00 | 0024 Stand(H): $119.00 | 0025 Stand(L): $109.00',
        'tags_zh': ['大理石边几', '花架摆件'],
        'tags_en': ['Marble End Table', 'Plant Stand'],
        'id': 'pj-0026-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-120.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-120.jpg', 'Main'),
            ('../../assets/images/pdf3/img-121.jpg', 'Detail')
        ],
        'title_zh': '2511 / 2512 / 2513',
        'title_en': '2511 / 2512 / 2513',
        'desc_zh': '黑大理石台面不锈钢镀金框架客厅茶几、边几与玄关台系列。',
        'desc_en': 'Black Marble with Gold Stainless Coffee Table, End Table & Console.',
        'price_zh': '折后 咖啡桌: $319.00 | 边几: $219.00 | 玄关台: $299.00',
        'price_en': 'Sale: Coffee: $319.00 | End Table: $219.00 | Console: $299.00',
        'tags_zh': ['黑大理石金架', '轻奢全套'],
        'tags_en': ['Black Gold Marble', 'Luxury Suite'],
        'id': 'pj-2511-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-131.jpg',
        'thumbs': [('../../assets/images/pdf3/img-131.jpg', 'Main')],
        'title_zh': '2514 / 2515 / 2516',
        'title_en': '2514 / 2515 / 2516',
        'desc_zh': '灰大理石台面不锈钢镀铬框架客厅咖啡桌、边几与玄关台系列。',
        'desc_en': 'Gray Marble with Chrome Stainless Coffee Table, End Table & Console.',
        'price_zh': '折后 咖啡桌: $299.00 | 边几: $199.00 | 玄关台: $279.00',
        'price_en': 'Sale: Coffee: $299.00 | End Table: $199.00 | Console: $279.00',
        'tags_zh': ['灰大理石铬架', '精选'],
        'tags_en': ['Gray Chrome Marble', 'Featured'],
        'id': 'pj-2514-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-114.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-114.jpg', 'Main'),
            ('../../assets/images/pdf3/img-115.jpg', 'Detail')
        ],
        'title_zh': '2412 / 2413',
        'title_en': '2412 / 2413',
        'desc_zh': '18mm 白钢化玻璃台面不锈钢镀金框架咖啡桌与边几。',
        'desc_en': '18mm White Glass Coffee Table & End Table with Gold Frame.',
        'price_zh': '折后 咖啡桌: $219.00 | 边几: $169.00',
        'price_en': 'Sale: Coffee: $219.00 | End Table: $169.00',
        'tags_zh': ['白玻璃金架', '精选'],
        'tags_en': ['White Glass Gold', 'Featured'],
        'id': 'pj-2412-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-116.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-116.jpg', 'Main'),
            ('../../assets/images/pdf3/img-117.jpg', 'Detail')
        ],
        'title_zh': '2400 / 2401 & 2410 / 2411',
        'title_en': '2400 / 2401 & 2410 / 2411',
        'desc_zh': '18mm 白大理石台面不锈钢框架咖啡桌与边几（镀金/镀铬可选）。',
        'desc_en': '18mm White Marble Coffee Table & End Table (Gold / Chrome Frame).',
        'price_zh': '折后 金架咖啡桌: $249.00 | 金架边几: $189.00 | 铬架咖啡桌: $229.00 | 铬架边几: $169.00',
        'price_en': 'Sale: Gold Coffee: $249.00 | Gold End: $189.00 | Chrome Coffee: $229.00 | Chrome End: $169.00',
        'tags_zh': ['白大理石', '金/铬两色'],
        'tags_en': ['White Marble', 'Gold/Chrome'],
        'id': 'pj-2400-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-118.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-118.jpg', 'Main'),
            ('../../assets/images/pdf3/img-119.jpg', 'Detail')
        ],
        'title_zh': '3200 / 3201 (WH / BK)',
        'title_en': '3200 / 3201 (WH / BK)',
        'desc_zh': '现代高光钢琴烤漆客厅咖啡桌与边几（高亮白 / 曜石黑可选）。',
        'desc_en': 'High Gloss Coffee Table & End Table (White / Black).',
        'price_zh': '折后 3200咖啡桌: $79.00 | 3201边几: $69.00',
        'price_en': 'Sale: 3200 Coffee: $79.00 | 3201 End: $69.00',
        'tags_zh': ['高光烤漆', '黑白双色'],
        'tags_en': ['High Gloss', 'Black & White'],
        'id': 'pj-3200-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-134.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-134.jpg', 'Main'),
            ('../../assets/images/pdf3/img-135.jpg', 'Detail')
        ],
        'title_zh': '2437 (GOLD / CHROME)',
        'title_en': '2437 (GOLD / CHROME)',
        'desc_zh': '现代不锈钢茶几与边几三件套组合（镀金架 / 镀铬架可选）。',
        'desc_en': '3-Piece Coffee Table & End Table Set (Gold / Chrome).',
        'price_zh': '折后 镀金三件套: $199.00/套 | 镀铬三件套: $179.00/套',
        'price_en': 'Sale: Gold 3-PC Set: $199.00 | Chrome 3-PC Set: $179.00',
        'tags_zh': ['三件套整包', '精选'],
        'tags_en': ['3-PC Set', 'Featured'],
        'id': 'pj-2437-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-136.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-136.jpg', 'Main'),
            ('../../assets/images/pdf3/img-137.jpg', 'Detail')
        ],
        'title_zh': '2438 / 2439 (WH / BK)',
        'title_en': '2438 / 2439 (WH / BK)',
        'desc_zh': '现代几何造型大理石台面咖啡桌与边几（白色 / 黑色可选）。',
        'desc_en': 'Geometric Marble Coffee Table & End Table (White / Black).',
        'price_zh': '折后 2438几何茶几: $199.00 | 2439边几: $159.00',
        'price_en': 'Sale: 2438 Coffee: $199.00 | 2439 End: $159.00',
        'tags_zh': ['几何造型', '大理石台面'],
        'tags_en': ['Geometric', 'Marble Top'],
        'id': 'pj-2438-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-138.jpg',
        'thumbs': [('../../assets/images/pdf3/img-138.jpg', 'Main')],
        'title_zh': '2436 (GOLD / CHROME)',
        'title_en': '2436 (GOLD / CHROME)',
        'desc_zh': '圆形茶几与双边几三件套组合（镀金架 / 镀铬架可选）。',
        'desc_en': '3-Piece Round Coffee Table & End Table Set (Gold / Chrome).',
        'price_zh': '折后 镀金圆三件套: $219.00/套 | 镀铬圆三件套: $199.00/套',
        'price_en': 'Sale: Gold 3-PC Set: $219.00 | Chrome 3-PC Set: $199.00',
        'tags_zh': ['圆形三件套', '精选'],
        'tags_en': ['Round 3-PC Set', 'Featured'],
        'id': 'pj-2436-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-139.jpg',
        'thumbs': [('../../assets/images/pdf3/img-139.jpg', 'Main')],
        'title_zh': '4200 / 4201 (CA / OAK)',
        'title_en': '4200 / 4201 (CA / OAK)',
        'desc_zh': '经典实木纹理客厅咖啡桌与边几（加州胡桃色 / 橡木色可选）。',
        'desc_en': 'Classic Wood Grain Coffee Table & End Table (California Walnut / Oak).',
        'price_zh': '折后 4200木茶几: $55.00 | 4201边几: $39.00',
        'price_en': 'Sale: 4200 Coffee: $55.00 | 4201 End: $39.00',
        'tags_zh': ['经典实木', '精选'],
        'tags_en': ['Wood Grain', 'Featured'],
        'id': 'pj-4200-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-140.jpg',
        'thumbs': [('../../assets/images/pdf3/img-140.jpg', 'Main')],
        'title_zh': '2433',
        'title_en': '2433',
        'desc_zh': '现代简约茶几与双边几三件套整包组合。',
        'desc_en': 'Modern 3-Piece Coffee Table & End Table Value Pack.',
        'price_zh': '折后 三件套: $129.00/套',
        'price_en': 'Sale: 3-PC Pack: $129.00',
        'tags_zh': ['三件套', '高性价比'],
        'tags_en': ['3-PC Pack', 'Best Value'],
        'id': 'pj-2433-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-255.jpg',
        'thumbs': [
            ('../../assets/images/pdf3/img-255.jpg', 'Main'),
            ('../../assets/images/pdf3/img-285.jpg', 'Detail')
        ],
        'title_zh': '2021GL / 5501 (CA / RD)',
        'title_en': '2021GL / 5501 (CA / RD)',
        'desc_zh': '2021GL 玻璃茶几与 5501 多功能小凳边几（加州色 / 红色）。',
        'desc_en': '2021GL Glass Coffee Table & 5501 Stool/End Table (California / Red).',
        'price_zh': '折后 2021GL茶几: $79.00 | 5501小凳边几: $25.00',
        'price_en': 'Sale: 2021GL Coffee: $79.00 | 5501 Stool: $25.00',
        'tags_zh': ['多功能', '精选'],
        'tags_en': ['Multi-function', 'Featured'],
        'id': 'pj-2021gl-main'
    },
    {
        'main_img': '../../assets/images/pdf3/img-272.jpg',
        'thumbs': [('../../assets/images/pdf3/img-272.jpg', 'Main')],
        'title_zh': '2432 (BK / RD)',
        'title_en': '2432 (BK / RD)',
        'desc_zh': '2432 现代双层钢化玻璃客厅茶几（黑色 / 红色）。',
        'desc_en': '2432 Modern 2-Tier Tempered Glass Coffee Table (Black / Red).',
        'price_zh': '折后 $49.00',
        'price_en': 'Sale: $49.00',
        'tags_zh': ['双层钢化玻璃', '特惠'],
        'tags_en': ['2-Tier Glass', 'Special Offer'],
        'id': 'pj-2432-main'
    }
]

# Update zh/living-room/index.html
zh_lr_path = 'zh/living-room/index.html'
zh_lr_content = open(zh_lr_path).read()
rendered_zh_lr = render_cards(living_room_cards, is_zh=True)
zh_lr_content = re.sub(grid_pattern, f'\\1\n\n{rendered_zh_lr}\n    \\2', zh_lr_content)
open(zh_lr_path, 'w').write(zh_lr_content)
print("Updated zh/living-room/index.html")

# Update living-room/index.html
en_lr_path = 'living-room/index.html'
en_lr_content = open(en_lr_path).read()
rendered_en_lr = render_cards(living_room_cards, is_zh=False)
en_lr_content = re.sub(grid_pattern, f'\\1\n\n{rendered_en_lr}\n    \\2', en_lr_content)
open(en_lr_path, 'w').write(en_lr_content)
print("Updated living-room/index.html")
