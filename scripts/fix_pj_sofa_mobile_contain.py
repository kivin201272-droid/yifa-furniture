import sys
t=open(sys.argv[1],encoding="utf-8",newline="").read()
for sel in (".sofa-img-container",".main-sofa-img"):
    old=f"  [data-sku=\"9941\"] {sel}"
    assert t.count(old)==1
    t=t.replace(old,f"  [data-sku=\"9921\"] {sel},\r\n  [data-sku=\"9931\"] {sel},\r\n"+old) if "\r\n" in t else t.replace(old,f"  [data-sku=\"9921\"] {sel},\n  [data-sku=\"9931\"] {sel},\n"+old)
for pid in ("9921","9931"):
    k=f"pj_living/pj-{pid}-pdf.jpg"; i=t.index(k); s=t.rfind("<div class=\"sofa-card reveal\">",0,i)
    t=t[:s]+f"<div class=\"sofa-card reveal\" data-sku=\"{pid}\">"+t[s+len("<div class=\"sofa-card reveal\">"):]
open(sys.argv[2],"w",encoding="utf-8",newline="").write(t)
