#!/usr/bin/env python3
"""PJ sofa image/model/price fix (9910GRAY, 9921, 9931, 9941), EN + ZH living-room.

Usage: fix_pj_sofa_cards.py transform <in> <out> <en|zh>
Images are extracted losslessly (no resize) from the original catalog PDF.
"""
import sys

PRICE_9931 = {
    "en": "Chair 9931: $228.00 | Loveseat 9932: $299.00 | Sofa 9933: $349.00 | Loveseat + Sofa Set (9932 + 9933): $639.00",
    "zh": "单人 9931: $228.00 | 双人 9932: $299.00 | 三人 9933: $349.00 | 双人+三人套装 (9932 + 9933): $639.00",
}
OLD_PRICE = {
    "en": "Chair: $170.00 | Loveseat: $220.00 | Sofa: $260.00 | 2+3 Set: $479.00",
    "zh": "单人: $170.00 | 双人: $220.00 | 三人: $260.00 | 2+3组合: $479.00",
}

# (lang) -> list of (old, new) applied inside the card whose image is pj-<id>.jpg
EDITS = {
    "9910": {"en": [], "zh": []},
    "9921": {
        "en": [("Dark Gray Faux Leather Sofa Collection", "Gray PU Sofa Collection"),
               ("Dark gray durable faux leather", "Gray durable PU")],
        "zh": [("现代深灰皮质沙发系列", "现代灰色PU皮沙发系列"),
               ("深灰耐磨皮革", "灰色耐磨PU皮革")],
    },
    "9931": {
        "en": [("Brown Faux Leather Sofa Collection", "Black PU Sofa Collection"),
               ("Warm brown faux leather sofa series offering plush comfort and lasting durability.",
                "Black PU sofa set in Chair, Loveseat and Sofa, plus a Loveseat + Sofa set price."),
               (OLD_PRICE["en"], PRICE_9931["en"]),
               (">Brown Leather<", ">Black PU<"),
               (">Set Deal<", ">Loveseat + Sofa Set<")],
        "zh": [("现代棕色皮质沙发系列", "现代黑色PU皮沙发系列"),
               ("暖棕复古皮革质感，饱满坐感，单人/双人/三人/2+3组合可选。",
                "黑色PU皮沙发，单人/双人/三人可选，另有双人+三人套装价。"),
               (OLD_PRICE["zh"], PRICE_9931["zh"]),
               (">暖棕皮革<", ">黑色PU<"),
               (">2+3套装特惠<", ">双人+三人套装<")],
    },
    "9941": {
        "en": [("Black Faux Leather Sofa Collection", "Red & Black PU Sofa Collection"),
               ("Sleek black faux leather living room group", "Red and black PU living room group"),
               (">Black Leather<", ">Red/Black PU<")],
        "zh": [("现代黑色皮质沙发系列", "现代红黑PU皮沙发系列"),
               ("纯黑极简现代皮艺，沉稳耐脏", "红黑撞色PU皮艺，沉稳耐脏"),
               (">纯黑极简<", ">红黑撞色<")],
    },
}


def transform(text, lang):
    for pid, per in EDITS.items():
        old_src = f"pj_living/pj-{pid}.jpg"
        new_src = f"pj_living/pj-{pid}-pdf.jpg"
        i = text.index(old_src)
        start = text.rfind('<div class="sofa-card', 0, i)
        end = text.index('<div class="sofa-card', i) if '<div class="sofa-card' in text[i:] else len(text)
        block = text[start:end]
        assert block.count(old_src) == 1
        block = block.replace(old_src, new_src)
        for old, new in per[lang]:
            assert block.count(old) >= 1, (pid, lang, old)
            block = block.replace(old, new)
        text = text[:start] + block + text[end:]
    return text


if __name__ == "__main__":
    _, mode, src, dst, lang = sys.argv
    with open(src, "r", encoding="utf-8", newline="") as f:
        t = f.read()
    out = transform(t, lang)
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(out)
