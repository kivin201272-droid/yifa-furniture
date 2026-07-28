const fs = require('fs');

function replaceInFile(filePath, search, replace) {
    if (!fs.existsSync(filePath)) return;
    let content = fs.readFileSync(filePath, 'utf-8');
    if (content.includes(search)) {
        content = content.split(search).join(replace);
        fs.writeFileSync(filePath, content);
        console.log(`Updated ${filePath}`);
    } else {
        console.log(`Search string not found in ${filePath}`);
    }
}

// 1. Fix breadcrumbs
replaceInFile('zh/office/index.html', '<span>/</span>优质床垫</nav>', '<span>/</span>优质办公系列</nav>');
replaceInFile('office/index.html', '<span>/</span>Mattress</nav>', '<span>/</span>Office</nav>');

// 2. Add Office card to index.html collection-grid
const enOfficeCard = `</article><article class="collection-card reveal"><div class=cc-img><img src="./assets/images/pdf3/img-260.jpg" alt="Office Furniture" width=900 height=900 loading=lazy></div><div class=cc-body><h3>Office</h3><p>Modern office desks, bookcases, cabinets, and shelving units to enhance productivity.</p><a class=cc-link href=./office/>View Office</a></div></article></div>`;
replaceInFile('index.html', '</article></div></div></section>', enOfficeCard + '</div></section>');

const zhOfficeCard = `</article><article class="collection-card reveal"><div class=cc-img><img src="./assets/images/pdf3/img-260.jpg" alt="优质办公系列" width=900 height=900 loading=lazy></div><div class=cc-body><h3>办公系列</h3><p>现代办公桌、书架、文件柜及置物架，为您打造高效舒适的工作空间。</p><a class=cc-link href=./office/>浏览办公系列</a></div></article></div>`;
replaceInFile('zh/index.html', '</article></div></div></section>', zhOfficeCard + '</div></section>');

// 3. Add Office split block to products/index.html
const enOfficeSplit = `</div><div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../assets/images/pdf3/img-260.jpg" alt="Modern Office Furniture" width=900 height=900 loading=lazy></div><div class="split-body reveal"><span class=eyebrow>Collection 05</span><h2>Office</h2><p>Modern office furniture designed for productivity and ultimate comfort.</p><ul class=tick-list><li>Office Desks</li><li>Bookcases</li><li>File Cabinets</li><li>Shelving Units</li></ul><p style=margin-top:24px><a class="btn btn-outline" href=../office/>Explore Office</a></p></div></div>`;
replaceInFile('products/index.html', '</div></div></section>', enOfficeSplit + '</section>');

const zhOfficeSplit = `</div><div class="split" style="margin-bottom:84px;"><div class="split-media reveal"><img src="../../assets/images/pdf3/img-260.jpg" alt="现代办公家具" width=900 height=900 loading=lazy></div><div class="split-body reveal"><span class=eyebrow>核心系列 05</span><h2>办公系列</h2><p>全系列高品质办公家具，人体工学设计，为您带来舒适高效的工作体验。</p><ul class=tick-list><li>现代办公桌</li><li>多层书架</li><li>配套文件柜</li><li>实用置物架</li></ul><p style=margin-top:24px><a class="btn btn-outline" href=../office/>探索办公系列</a></p></div></div>`;
replaceInFile('zh/products/index.html', '</div></div></section>', zhOfficeSplit + '</section>');

console.log("Injection complete.");
