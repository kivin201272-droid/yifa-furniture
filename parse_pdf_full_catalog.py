import fitz # PyMuPDF
import re, json

doc = fitz.open('./素材库/价钱/price list2026 (5_22).pdf')

# Let's extract all prices and codes from each page
catalog = {}

# Page 2: Platform beds
# 7102 BROWN: Full $109, Queen $119
# 7405WH: Full $299, Queen $299
# 7403GRAY: Full $299, Queen $299
# 7402Q-WH: Queen $499
# 7404BK: Full $299, Queen $299
# 7600Q-IVY: Queen $399
# 7602Q-GRAY: Twin $129, Full $149, Queen $159
# 7602Q-IVY: Twin $129, Full $149, Queen $159
# 7602-PINK: Twin $129, Full $149, Queen $159
# 7603: Full $179, Queen $199
# 7401Q-BK: Queen $499
# 7500F-GRAY / 7500Q-GRAY: Full $299, Queen $299

catalog['7102 BROWN'] = {'price': '折后 F: $109.00 | Q: $119.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7405WH'] = {'price': '折后 F: $299.00 | Q: $299.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7403GRAY'] = {'price': '折后 F: $299.00 | Q: $299.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7402Q-WH'] = {'price': '折后 $499.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7404BK'] = {'price': '折后 F: $299.00 | Q: $299.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7600Q-IVY'] = {'price': '折后 $399.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7602Q-GRAY'] = {'price': '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7602Q-IVY'] = {'price': '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7602-PINK'] = {'price': '折后 T: $129.00 | F: $149.00 | Q: $159.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7603'] = {'price': '折后 F: $179.00 | Q: $199.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7401Q-BK'] = {'price': '折后 $499.00', 'page': 2, 'cat': 'Bedroom'}
catalog['7500F/7500Q'] = {'price': '折后 F: $299.00 | Q: $299.00', 'page': 2, 'cat': 'Bedroom'}

# Page 3: Beds
catalog['7806-GRAY'] = {'price': '折后 F: $199.00 | Q: $229.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7102 GRAY'] = {'price': '折后 F: $109.00 | Q: $119.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7100'] = {'price': '折后 T: $75.00 | F: $85.00 | Q: $95.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7804 GRAY'] = {'price': '折后 F: $249.00 | Q: $269.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7011GRAY'] = {'price': '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7011CHAR'] = {'price': '折后 T: $119.00 | F: $139.00 | Q: $149.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7016-GRAY'] = {'price': '折后 F: $99.00 | Q: $109.00', 'page': 3, 'cat': 'Bedroom'}
catalog['2331'] = {'price': '折后 $119.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7005BK'] = {'price': '折后 $149.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7004BK'] = {'price': '折后 $169.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7701WH'] = {'price': '折后 $219.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7702WH'] = {'price': '折后 $279.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7702CA'] = {'price': '折后 $279.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7701CA'] = {'price': '折后 $219.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7020WH'] = {'price': '折后 F: $199.00 | Q: $219.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7021BK'] = {'price': '折后 F: $199.00 | Q: $219.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7013'] = {'price': '折后 T: $99.00 | F: $119.00 | Q: $129.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7901CA-T/F'] = {'price': '折后 T: $109.00 | F: $129.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7901WH-T/F'] = {'price': '折后 T: $109.00 | F: $129.00', 'page': 3, 'cat': 'Bedroom'}
catalog['1901'] = {'price': '折后 T: $59.00 | F: $79.00 | Q: $89.00', 'page': 3, 'cat': 'Bedroom'}
catalog['7800/7801'] = {'price': '折后 $55.00 - $99.00', 'page': 3, 'cat': 'Bedroom'}

# Page 4: Bedroom Suites & Sofas
catalog['8910'] = {'price': '折后 QB: $499.00 | NS: $90.00 | MR: $60.00 | DS: $260.00 | CH: $195.00', 'page': 4, 'cat': 'Bedroom'}
catalog['8003'] = {'price': '折后 5件套 $799.00 | QB: $220.00 | NS: $90.00 | MR: $70.00 | DS: $260.00 | CH: $195.00', 'page': 4, 'cat': 'Bedroom'}
catalog['8010'] = {'price': '折后 5件套 $649.00 | FB/QB: $180.00 | NS: $85.00 | MR: $60.00 | DS: $225.00 | CH: $170.00', 'page': 4, 'cat': 'Bedroom'}
catalog['8009'] = {'price': '折后 5件套 $579.00 | FB/QB: $175.00 | NS: $75.00 | MR: $55.00 | DS: $205.00 | CH: $170.00', 'page': 4, 'cat': 'Bedroom'}
catalog['8008'] = {'price': '折后 5件套 $579.00 | FB/QB: $175.00 | NS: $75.00 | MR: $55.00 | DS: $205.00 | CH: $170.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7001'] = {'price': '折后 T: $79.00 | F: $99.00 | Q: $109.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7009'] = {'price': '折后 T: $95.00 | F: $119.00 | Q: $129.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7202'] = {'price': '折后 T: $99.00 | F: $119.00 | Q: $129.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7203'] = {'price': '折后 T: $99.00 | F: $119.00 | Q: $129.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7002'] = {'price': '折后 T: $79.00 | F: $99.00 | Q: $109.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7003T-BK/7003F-BK'] = {'price': '折后 T: $69.00 | F: $89.00', 'page': 4, 'cat': 'Bedroom'}
catalog['7003T-WH/7003F-WH'] = {'price': '折后 T: $69.00 | F: $89.00', 'page': 4, 'cat': 'Bedroom'}

# Page 4 & 5: Living room sofas & occasional tables
catalog['9701BR'] = {'price': '折后 $299.00', 'page': 4, 'cat': 'Living Room'}
catalog['2406'] = {'price': '折后 $169.00', 'page': 4, 'cat': 'Living Room'}
catalog['2402'] = {'price': '折后 $149.00', 'page': 4, 'cat': 'Living Room'}
catalog['9211/9212/9213'] = {'price': '折后 单人: $185.00 | 双人: $265.00 | 三人: $295.00 | 2+3组合: $549.00', 'page': 4, 'cat': 'Living Room'}
catalog['9910GRAY'] = {'price': '折后 $549.00', 'page': 4, 'cat': 'Living Room'}
catalog['9900BK'] = {'price': '折后 $549.00', 'page': 4, 'cat': 'Living Room'}
catalog['9921/9922/9923'] = {'price': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'page': 4, 'cat': 'Living Room'}
catalog['9931/9932/9933'] = {'price': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'page': 4, 'cat': 'Living Room'}
catalog['9941/9942/9943'] = {'price': '折后 单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00', 'page': 4, 'cat': 'Living Room'}
catalog['0021PR/0021GRAY'] = {'price': '折后 $499.00', 'page': 4, 'cat': 'Living Room'}
catalog['0022GRAY/0022PR'] = {'price': '折后 $249.00', 'page': 5, 'cat': 'Living Room'}
catalog['0023GRAY/0023PR'] = {'price': '折后 $189.00', 'page': 5, 'cat': 'Living Room'}
catalog['0026GRAY/0026PR'] = {'price': '折后 $99.00', 'page': 5, 'cat': 'Living Room'}
catalog['0025GRAY/0025PR'] = {'price': '折后 $109.00', 'page': 5, 'cat': 'Living Room'}
catalog['0024GRAY/0024PR'] = {'price': '折后 $119.00', 'page': 5, 'cat': 'Living Room'}
catalog['2511/2512/2513'] = {'price': '折后 茶几: $319.00 | 边几: $219.00 | 条几: $299.00', 'page': 5, 'cat': 'Living Room'}
catalog['2514/2515/2516'] = {'price': '折后 茶几: $299.00 | 边几: $199.00 | 条几: $279.00', 'page': 5, 'cat': 'Living Room'}
catalog['3200/3201'] = {'price': '折后 茶几: $79.00 | 边几: $69.00', 'page': 5, 'cat': 'Living Room'}
catalog['2400/2401 (Gold)'] = {'price': '折后 茶几: $249.00 | 边几: $189.00', 'page': 5, 'cat': 'Living Room'}
catalog['2410/2401 (Chrome)'] = {'price': '折后 茶几: $229.00 | 边几: $169.00', 'page': 5, 'cat': 'Living Room'}
catalog['2412/2413'] = {'price': '折后 茶几: $219.00 | 边几: $169.00', 'page': 5, 'cat': 'Living Room'}
catalog['2437 GOLD/CHROME'] = {'price': '折后 金色3件套: $199.00 | 镀铬3件套: $179.00', 'page': 5, 'cat': 'Living Room'}
catalog['2438/2439 (BK/WH)'] = {'price': '折后 茶几: $199.00 | 边几: $159.00', 'page': 5, 'cat': 'Living Room'}
catalog['2436 GOLD/CHROME'] = {'price': '折后 金色3件套: $219.00 | 镀铬3件套: $199.00', 'page': 5, 'cat': 'Living Room'}
catalog['4200/4201'] = {'price': '折后 咖啡色茶几: $139.00 | 边几: $39.00 | 原木色茶几: $55.00', 'page': 5, 'cat': 'Living Room'}
catalog['2433'] = {'price': '折后 3件套 $129.00', 'page': 5, 'cat': 'Living Room'}
catalog['2021GL'] = {'price': '折后 $79.00', 'page': 5, 'cat': 'Living Room'}
catalog['5501CA/5501RD'] = {'price': '折后 $25.00', 'page': 5, 'cat': 'Living Room'}
catalog['2432BK/RD'] = {'price': '折后 $49.00', 'page': 5, 'cat': 'Living Room'}

# Page 6, 7, 8, 9: Dining
catalog['4160/4130/4110'] = {'price': '折后 4160餐桌: $139.00 | 4130餐桌: $109.00 | 4110餐椅: $59.95/把', 'page': 6, 'cat': 'Dining'}
catalog['3016T/3000WH'] = {'price': '折后 3016T餐桌: $549.00 | 1600/1003餐椅: $149.00 | 1500餐椅: $99.00', 'page': 6, 'cat': 'Dining'}
catalog['3010T/3011T'] = {'price': '折后 3011T餐桌: $549.00 | 3010T餐桌: $499.00 | 餐椅: $85.00 - $149.00', 'page': 6, 'cat': 'Dining'}
catalog['3012T'] = {'price': '折后 3012T餐桌: $499.00 | 2680餐椅: $79.00', 'page': 6, 'cat': 'Dining'}
catalog['3000T'] = {'price': '折后 3000T大理石餐桌: $399.00 | 3002玻璃餐桌: $349.00 | 餐椅: $89.00 - $149.00', 'page': 6, 'cat': 'Dining'}
catalog['3008T/3007T'] = {'price': '折后 3008T餐桌: $399.00 | 3007T餐桌: $349.00 | 餐椅: $89.00 - $99.00', 'page': 7, 'cat': 'Dining'}
catalog['3102T/3112T/3101T'] = {'price': '折后 3102T: $149.00 | 3101T: $129.00 | 3112T: $119.00 | 餐椅: $35.00 - $79.00', 'page': 7, 'cat': 'Dining'}
catalog['3104T/3114T/3103T/3105T/3106T'] = {'price': '折后 3104T: $159.00 | 3103T: $139.00 | 3106T: $139.00 | 3114T: $129.00 | 3105T: $119.00', 'page': 7, 'cat': 'Dining'}
catalog['2240/2250'] = {'price': '折后 2240餐桌: $75.00 | 2250餐桌: $59.00 | 2800餐椅: $30.00', 'page': 7, 'cat': 'Dining'}
catalog['4031T/3003T/2206/2216'] = {'price': '折后 3003T: $179.00 | 4031T: $139.00 | 2206T/2216T一桌四椅: $199.00', 'page': 8, 'cat': 'Dining'}
catalog['4002/4154/4158/4159/4138'] = {'price': '折后 4154: $95.00 | 4138: $92.00 | 4158/4159: $89.00 | 4002: $85.00 | 餐椅: $39.95 - $42.00', 'page': 8, 'cat': 'Dining'}
catalog['4003/4114/4009 Breakfast Sets'] = {'price': '折后 4114 5件套: $179.00 | 4003 3件套: $119.00 | 4009 3件套: $89.00', 'page': 8, 'cat': 'Dining'}
catalog['2391/2370/2371/2235 Bar Sets'] = {'price': '折后 2235吧台桌: $129.00 | 2391吧台桌: $45.00 | 2371吧椅: $45.00 | 2370吧椅: $29.95', 'page': 9, 'cat': 'Dining'}

# Page 9 & 10: Office
catalog['2715/2716/4500/2714/2704/2709 Desks'] = {'price': '折后 $19.95 - $89.00', 'page': 9, 'cat': 'Office'}
catalog['2707/2706/2708/2725/2720/2722/2724 Chairs'] = {'price': '折后 $35.00 - $109.95', 'page': 9, 'cat': 'Office'}

# Page 10: Microwave / Bathroom / TV Stands
catalog['2524/2526/4405/4406 Carts & Cabinets'] = {'price': '折后 $49.95 - $99.95', 'page': 10, 'cat': 'Dining'}
catalog['4420/4421/4422/4432/4801/2766/2767/2769 TV Stands'] = {'price': '折后 $49.95 - $129.00', 'page': 10, 'cat': 'Living Room'}
catalog['4337/4338/4333/4334/4331/4332 Fireplaces'] = {'price': '折后 $69.00 - $85.00', 'page': 10, 'cat': 'Living Room'}

# Page 11 & 12: Storage, Wardrobes, Racks
catalog['4220/4218/4216 Bookcases'] = {'price': '折后 $19.95 - $45.00', 'page': 11, 'cat': 'Living Room'}
catalog['4224/4225/4226/4227/4228/4424 Wardrobes & Shoes'] = {'price': '折后 $75.00 - $185.00', 'page': 11, 'cat': 'Bedroom'}
catalog['2052/2051/2050/5107 Racks & Shelves'] = {'price': '折后 $12.95 - $69.95', 'page': 12, 'cat': 'Living Room'}

print(f"Catalog contains {len(catalog)} product categories/groupings from PDF.")
