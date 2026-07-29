const fs = require('fs');

function addNormalMattress(filePath, isZh) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Find the magical mattress section
    const magicMatch = isZh ? '浏览神奇床垫</a></p></div></div>' : 'Explore Magical Mattress</a></p></div></div>';
    
    if (content.includes(magicMatch)) {
        const normalSection = isZh ? `
<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../../assets/images/pdf6/N6001.png" alt="普通床垫" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">经典系列</span>
<h2>普通床垫</h2>
<p>优质普通床垫系列，为您提供舒适的基础睡眠体验。</p>
<ul class="tick-list">
<li>多款硬度可选</li>
<li>高性价比之选</li>
<li>经典绗缝设计</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../mattress/">浏览普通床垫</a></p>
</div>
</div>` : `
<div class="split reverse" style="margin-bottom:84px;">
<div class="split-media reveal">
<img src="../assets/images/pdf6/N6001.png" alt="Normal Mattress" width="900" height="900" loading="lazy">
</div>
<div class="split-body reveal">
<span class="eyebrow">Classic Collection</span>
<h2>Normal Mattress</h2>
<p>High-quality normal mattress collection, providing a comfortable foundation for your sleep.</p>
<ul class="tick-list">
<li>Multiple firmness options</li>
<li>High cost-performance</li>
<li>Classic quilted design</li>
</ul>
<p style="margin-top:24px"><a class="btn btn-outline" href="../mattress/">Explore Normal Mattress</a></p>
</div>
</div>`;

        // Don't add twice
        if (!content.includes('href=../mattress/>浏览普通床垫') && !content.includes('href="../mattress/">Explore Normal Mattress')) {
            content = content.replace(magicMatch, magicMatch + normalSection);
            fs.writeFileSync(filePath, content);
            console.log('Updated', filePath);
        }
    }
}

addNormalMattress('zh/products/index.html', true);
addNormalMattress('products/index.html', false);
