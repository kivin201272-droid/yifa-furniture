import os
import subprocess
from PIL import Image

workspace_dir = os.path.abspath(os.path.dirname(__file__))
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 1. HTML for Mattress Banner (Mobile - 750x1200)
html_mattress = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 750px;
    height: 1200px;
    background: radial-gradient(circle at 50% 30%, #0d6efd 0%, #01438e 100%);
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "STHeiti", sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 50px 60px 44px;
    color: #fff;
    position: relative;
    overflow: hidden;
  }}
  .brand-title {{
    font-size: 96px;
    font-weight: 900;
    color: #e51b24;
    text-shadow: 
      -4px -4px 0 #fff,  
       4px -4px 0 #fff,
      -4px  4px 0 #fff,
       4px  4px 0 #fff,
       0 8px 20px rgba(0,0,0,0.6);
    letter-spacing: 0.08em;
    line-height: 1.1;
    margin-top: 6px;
  }}
  .red-bar {{
    width: 100%;
    background: #e51b24;
    padding: 18px 10px;
    text-align: center;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    margin: 16px 0;
  }}
  .red-bar h2 {{
    font-size: 46px;
    font-weight: 900;
    color: #fff;
    letter-spacing: 0.05em;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    white-space: nowrap;
  }}
  .magical-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin: 12px 0 20px;
  }}
  .magical-title {{
    font-size: 50px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 0.06em;
    text-shadow: 0 2px 8px rgba(0,0,0,0.6);
  }}
  .discount-badge {{
    background: #fedc00;
    color: #d9000d;
    font-size: 34px;
    font-weight: 900;
    padding: 8px 20px;
    border-radius: 30px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    border: 2px solid #fff;
  }}
  .logos-card {{
    background: #fff;
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    width: 100%;
    margin-bottom: 20px;
  }}
  .logos-card img {{
    width: 100%;
    max-height: 84px;
    object-fit: contain;
  }}
  .footer-info {{
    width: 100%;
    text-align: center;
    background: rgba(0, 0, 0, 0.45);
    border-radius: 12px;
    padding: 18px 14px;
    font-size: 23px;
    line-height: 1.55;
    color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255,255,255,0.25);
  }}
</style>
</head>
<body>
  <div class="brand-title">易发家具</div>
  <div class="red-bar">
    <h2>美国品牌床垫特卖场</h2>
  </div>
  <div class="magical-row">
    <span class="magical-title">神奇床垫</span>
    <span class="discount-badge">50% OFF</span>
  </div>
  <div class="logos-card">
    <img src="{workspace_dir}/assets/images/promo_elements/logos_white_bg.png">
  </div>
  <div class="footer-info">
    <p><strong>营业时间：</strong>周一至周六 11:30AM - 4:30PM | 周日休息</p>
    <p><strong>服务热线：</strong>917-771-5493 | <strong>地址：</strong>6410 8th Ave, Brooklyn</p>
  </div>
</body>
</html>
"""

# 2. HTML for Sofa Promo Banner (Mobile - 750x1200)
html_sofa = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 750px;
    height: 1200px;
    background: #fedc00;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "STHeiti", sans-serif;
    display: flex;
    flex-direction: column;
    padding: 24px 44px 22px;
    color: #111;
    position: relative;
    overflow: hidden;
    justify-content: space-between;
  }}
  .header-wrap {{
    position: relative;
    text-align: center;
    margin-bottom: 2px;
  }}
  .headline-year {{
    font-size: 54px;
    font-weight: 900;
    color: #e51b24;
    line-height: 1.1;
    letter-spacing: 0.02em;
    text-shadow: 1px 1px 0 #fff;
  }}
  .headline-event {{
    font-size: 46px;
    font-weight: 900;
    color: #e51b24;
    line-height: 1.1;
    letter-spacing: 0.02em;
    margin-top: 2px;
  }}
  .star-badge {{
    position: absolute;
    left: 4px;
    top: -4px;
    width: 100px;
    height: 100px;
    background: #e51b24;
    clip-path: polygon(50% 0%, 65% 15%, 85% 6%, 86% 27%, 100% 38%, 90% 55%, 100% 70%, 82% 78%, 82% 98%, 62% 88%, 50% 100%, 38% 88%, 18% 98%, 18% 78%, 0% 70%, 10% 55%, 0% 38%, 14% 27%, 15% 6%, 35% 15%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 22px;
    font-weight: 900;
    text-align: center;
    line-height: 1.15;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  }}
  .logos-bar {{
    background: #fff;
    border-radius: 8px;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    margin: 6px 0 8px;
  }}
  .logos-bar img {{
    width: 100%;
    max-height: 40px;
    object-fit: contain;
  }}
  .card {{
    background: #fff;
    border-radius: 10px;
    padding: 10px 12px;
    display: flex;
    gap: 14px;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    border: 2px solid #fff;
  }}
  .card-img {{
    width: 215px;
    height: 145px;
    border-radius: 6px;
    object-fit: cover;
    flex-shrink: 0;
  }}
  .card-info {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .card-title {{
    font-size: 27px;
    font-weight: 900;
    color: #222;
    line-height: 1.2;
    margin-bottom: 2px;
  }}
  .card-subtitle {{
    font-size: 20px;
    color: #555;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .card-price-orig {{
    font-size: 20px;
    color: #666;
    text-decoration: line-through;
    margin-right: 8px;
  }}
  .card-price-special {{
    font-size: 36px;
    font-weight: 900;
    color: #e51b24;
    line-height: 1;
  }}
  .card-unit {{
    font-size: 20px;
    color: #444;
    font-weight: 700;
  }}
  .red-banner {{
    background: #e51b24;
    color: #fff;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    font-size: 40px;
    font-weight: 900;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin: 6px 0;
  }}
  .bottom-sub {{
    text-align: center;
    color: #e51b24;
    font-size: 40px;
    font-weight: 900;
    letter-spacing: 0.05em;
    margin: 2px 0 2px;
  }}
  .footer-box {{
    background: #fff;
    border-radius: 8px;
    padding: 10px 12px;
    text-align: center;
    font-size: 19.5px;
    font-weight: 700;
    color: #333;
    line-height: 1.4;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }}
</style>
</head>
<body>
  <div class="header-wrap">
    <div class="star-badge">送<br>茶几</div>
    <div class="headline-year">2026 易发家具</div>
    <div class="headline-event">第33届沙发抢购节</div>
  </div>

  <div class="logos-bar">
    <img src="{workspace_dir}/assets/images/promo_elements/logos_white_bg.png">
  </div>

  <!-- Product 1: Sealy 记忆棉床垫 -->
  <div class="card">
    <img class="card-img" src="{workspace_dir}/assets/images/promo_elements/mattress_girl.png">
    <div class="card-info">
      <div class="card-title">Sealy 9寸 60"x80"</div>
      <div class="card-subtitle">记忆棉床垫</div>
      <div>
        <span class="card-price-orig">市场价$1780</span>
      </div>
      <div>
        <span class="card-price-special">特惠价 $599</span><span class="card-unit">/张</span>
      </div>
    </div>
  </div>

  <!-- Red Highlight Bar -->
  <div class="red-banner">神奇床垫 50% OFF</div>

  <!-- Product 2: 意大利真皮沙发 -->
  <div class="card">
    <img class="card-img" src="{workspace_dir}/assets/images/promo_elements/sofa_clean_perfect.png">
    <div class="card-info">
      <div class="card-title">意大利真皮沙发</div>
      <div class="card-subtitle">（附送精美茶几）</div>
      <div>
        <span class="card-price-orig">原价$4689/套</span>
      </div>
      <div>
        <span class="card-price-special">$2350</span><span class="card-unit">/套</span>
      </div>
    </div>
  </div>

  <div class="bottom-sub">美国品牌床垫特卖场</div>

  <div class="footer-box">
    <div>周一至周六: 11:30AM - 4:30PM &nbsp;|&nbsp; 周日: 休息</div>
    <div>电话: 917-771-5493 &nbsp;|&nbsp; 地址: 6410 8th Ave, Brooklyn, NY</div>
  </div>
</body>
</html>
"""

# 3. HTML for Wholesale Promo Banner (Mobile - 750x1200)
html_wholesale = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 750px;
    height: 1200px;
    background: #f4efe6;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "STHeiti", sans-serif;
    display: flex;
    flex-direction: column;
    padding: 44px 50px 38px;
    color: #2b2520;
    position: relative;
    overflow: hidden;
    justify-content: space-between;
  }}
  .badge-top {{
    display: inline-block;
    align-self: center;
    background: #8e6d3d;
    color: #fff;
    padding: 8px 24px;
    border-radius: 24px;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
  }}
  .main-box {{
    background: #fff;
    border-radius: 12px;
    padding: 24px 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    border: 1px solid #e2ddd3;
    text-align: center;
  }}
  .main-h1 {{
    font-size: 64px;
    font-weight: 900;
    color: #2b2520;
    line-height: 1.15;
    letter-spacing: 0.04em;
  }}
  .main-sub {{
    font-size: 48px;
    font-weight: 800;
    color: #8e6d3d;
    line-height: 1.2;
    margin-top: 8px;
    letter-spacing: 0.02em;
  }}
  .anniversary-box {{
    background: #2b2520;
    color: #fff;
    border-radius: 12px;
    padding: 22px 18px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    margin: 14px 0;
  }}
  .anniversary-title {{
    font-size: 44px;
    font-weight: 900;
    color: #f7d58b;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
  }}
  .action-heading {{
    font-size: 48px;
    font-weight: 900;
    color: #fff;
    letter-spacing: 0.02em;
  }}
  .deadline-tag {{
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #e5dfd5;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 23px;
    margin-top: 12px;
    font-weight: 600;
  }}
  .contact-card {{
    background: #fff;
    border-radius: 12px;
    padding: 22px;
    border: 1px solid #e2ddd3;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
  }}
  .contact-h3 {{
    font-size: 32px;
    font-weight: 800;
    color: #2b2520;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .contact-h3::before {{
    content: "";
    display: inline-block;
    width: 6px;
    height: 26px;
    background: #8e6d3d;
    border-radius: 3px;
  }}
  .contact-p {{
    font-size: 24px;
    color: #5d564f;
    line-height: 1.5;
    margin-bottom: 8px;
  }}
  .contact-bottom {{
    border-top: 1px dashed #dcd6cb;
    padding-top: 10px;
    margin-top: 10px;
    font-size: 23px;
    font-weight: 700;
    color: #2b2520;
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>
  <div class="badge-top">32周年庆 · 典承经典</div>
  
  <div class="main-box">
    <div class="main-h1">家具批发</div>
    <div class="main-sub">一件也是批发价</div>
  </div>

  <div class="anniversary-box">
    <div class="anniversary-title">32周年庆 典承经典</div>
    <div class="action-heading">$100万家具让大行动</div>
    <div class="deadline-tag">活动截止日期: 2026年9月30日</div>
  </div>

  <div class="contact-card">
    <div class="contact-h3">订货与联系方式</div>
    <p class="contact-p">批发价的产品，须提前一周订货，请亲临本店指定地点自提货物。</p>
    <div class="contact-bottom">
      <span>电话: 917-771-5493</span>
      <span>地址: 6410 8th Ave, Brooklyn</span>
    </div>
  </div>
</body>
</html>
"""

with open("assets/images/mobile_banners_temp/banner_mattress.html", "w", encoding="utf-8") as f:
    f.write(html_mattress)

with open("assets/images/mobile_banners_temp/banner_sofa.html", "w", encoding="utf-8") as f:
    f.write(html_sofa)

with open("assets/images/mobile_banners_temp/banner_wholesale.html", "w", encoding="utf-8") as f:
    f.write(html_wholesale)

commands = [
    (
        f"file://{workspace_dir}/assets/images/mobile_banners_temp/banner_mattress.html",
        "assets/images/mattress-brand-banner-mob.png",
        750,
        1200
    ),
    (
        f"file://{workspace_dir}/assets/images/mobile_banners_temp/banner_sofa.html",
        "assets/images/sofa-promo-banner-mob.jpg",
        750,
        1200
    ),
    (
        f"file://{workspace_dir}/assets/images/mobile_banners_temp/banner_wholesale.html",
        "assets/images/wholesale-promo-banner-mob.jpg",
        750,
        1200
    )
]

for url, out_path, w, h in commands:
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={w},{h}",
        f"--screenshot={os.path.abspath(out_path)}",
        url
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated: {out_path} ({w}x{h})")

print("All mobile banners standardized to 750x1200 with safe boundaries!")
