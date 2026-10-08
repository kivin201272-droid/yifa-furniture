import sys

def update_page(path, lang):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add desktop style rule for the 4 PJ sofa cards
    style_rule = """
/* Desktop aspect ratio & full display for PJ sofa collection */
[data-sku="9910GRAY"] .sofa-img-container,
[data-sku="9921"] .sofa-img-container,
[data-sku="9931"] .sofa-img-container,
[data-sku="9941"] .sofa-img-container {
  aspect-ratio: 817 / 563 !important;
  max-height: 380px !important;
  padding: 8px 12px !important;
}
[data-sku="9910GRAY"] .main-sofa-img,
[data-sku="9921"] .main-sofa-img,
[data-sku="9931"] .main-sofa-img,
[data-sku="9941"] .main-sofa-img {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  object-position: center !important;
}
"""
    if '[data-sku="9931"] .sofa-img-container' not in content[:3000]:
        content = content.replace('</style>', style_rule + '</style>', 1)

    # Helper function to replace inside card
    def replace_in_card(img_marker, old_val, new_val):
        nonlocal content
        idx = content.find(img_marker)
        if idx == -1:
            print(f'Error: {img_marker} not found in {path}')
            return
        s = content.rfind('<div class="sofa-card', 0, idx)
        e = content.find('<div class="sofa-card', idx)
        if e == -1: e = content.find('</main>', idx)
        card = content[s:e]
        if old_val not in card:
            print(f'Warning: old_val not in card {img_marker}: {old_val}')
            return
        card_new = card.replace(old_val, new_val)
        content = content[:s] + card_new + content[e:]

    # 2. Update prices for 9910, 9921, 9941
    if lang == 'en':
        # 9910: $549.00 -> $738.00
        replace_in_card('pj-9910-pdf', '$549.00', '$738.00')

        # 9921:
        old_p = 'Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | 2+3 Set: $479.00'
        new_p9921 = 'Chair 9921: $228.00 | Loveseat 9922: $299.00 | Sofa 9923: $349.00 | Loveseat + Sofa Set (9922 + 9923): $639.00'
        replace_in_card('pj-9921-pdf', old_p, new_p9921)
        replace_in_card('pj-9921-pdf', '>Set Deal<', '>Loveseat + Sofa Set<')
        replace_in_card('pj-9921-pdf', '>Faux Leather<', '>Gray PU<')

        # 9941:
        new_p9941 = 'Chair 9941: $228.00 | Loveseat 9942: $299.00 | Sofa 9943: $349.00 | Loveseat + Sofa Set (9942 + 9943): $639.00'
        replace_in_card('pj-9941-pdf', old_p, new_p9941)
        replace_in_card('pj-9941-pdf', '>Set Deal<', '>Loveseat + Sofa Set<')

    else:
        # ZH 9910: $549.00 -> $738.00
        replace_in_card('pj-9910-pdf', '$549.00', '$738.00')

        # ZH 9921:
        old_p_zh = '单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00'
        new_p9921_zh = '单人 9921: $228.00 | 双人 9922: $299.00 | 三人 9923: $349.00 | 双人+三人套装 (9922 + 9923): $639.00'
        replace_in_card('pj-9921-pdf', old_p_zh, new_p9921_zh)
        replace_in_card('pj-9921-pdf', '>耐磨皮革<', '>灰色PU<')
        replace_in_card('pj-9921-pdf', '>2+3套装特惠<', '>双人+三人套装<')

        # ZH 9941:
        new_p9941_zh = '单人 9941: $228.00 | 双人 9942: $299.00 | 三人 9943: $349.00 | 双人+三人套装 (9942 + 9943): $639.00'
        replace_in_card('pj-9941-pdf', old_p_zh, new_p9941_zh)
        replace_in_card('pj-9941-pdf', '>2+3套装特惠<', '>双人+三人套装<')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

update_page('living-room/index.html', 'en')
update_page('zh/living-room/index.html', 'zh')
print('Updated both EN and ZH living-room pages!')
