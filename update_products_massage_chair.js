const fs = require('fs');
const path = require('path');

const zhPath = path.join(__dirname, 'zh/products/index.html');
const enPath = path.join(__dirname, 'products/index.html');

// 1. Update Chinese Products Page
let zh = fs.readFileSync(zhPath, 'utf8');
const zhMassageCard = `<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../../assets/images/massage-chair/D09.png" alt="豪华智能按摩椅" width=900 height=900 loading=lazy></div><div class="split-body reveal"><span class=eyebrow>核心系列 04</span><h2>按摩椅系列</h2><p>全系列高科技零重力智能按摩椅，人体工学太空舱设计，全身气囊与机械手机芯深度按摩，带来极致放松体验。</p><ul class=tick-list><li>豪华多功能全自动按摩</li><li>太空舱零重力智能机芯</li><li>多档力度与气囊全身包裹</li><li>热敷理疗与蓝牙音响系统</li></ul><p style=margin-top:24px><a class="btn btn-outline" href=../massage-chair/>探索按摩椅系列</a></p></div></div>`;

if (!zh.includes('massage-chair/')) {
    zh = zh.replace('<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../../assets/images/pdf3/img-260.jpg"', zhMassageCard + '\n' + '<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../../assets/images/pdf3/img-260.jpg"');
    zh = zh.replace('<li><a href=../office/>办公系列</a></li>', '<li><a href=../massage-chair/>按摩椅系列</a></li>\n<li><a href=../office/>办公系列</a></li>');
    fs.writeFileSync(zhPath, zh, 'utf8');
    console.log('Updated zh/products/index.html');
}

// 2. Update English Products Page
let en = fs.readFileSync(enPath, 'utf8');
const enMassageCard = `<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../assets/images/massage-chair/D09.png" alt="Luxury Massage Chairs" width=900 height=900 loading=lazy></div><div class="split-body reveal"><span class=eyebrow>Core Collection 04</span><h2>Massage Chairs</h2><p>High-tech zero-gravity smart massage chairs with ergonomic capsule design, full-body airbags, and intelligent deep-tissue massage mechanisms.</p><ul class=tick-list><li>Luxury Full-Body Automatic Massage</li><li>Zero-Gravity Smart Capsule System</li><li>Multi-Intensity & Airbag Compression</li><li>Heating Therapy & Bluetooth Audio</li></ul><p style=margin-top:24px><a class="btn btn-outline" href=../massage-chair/>Explore Massage Chairs</a></p></div></div>`;

if (!en.includes('massage-chair/')) {
    en = en.replace('<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../assets/images/pdf3/img-260.jpg"', enMassageCard + '\n' + '<div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../assets/images/pdf3/img-260.jpg"');
    en = en.replace('<li><a href=../office/>Office</a></li>', '<li><a href=../massage-chair/>Massage Chairs</a></li>\n<li><a href=../office/>Office</a></li>');
    fs.writeFileSync(enPath, en, 'utf8');
    console.log('Updated products/index.html');
}
