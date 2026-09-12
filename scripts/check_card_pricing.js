const fs = require('fs');
const { findProductPricing } = require('./inspect_and_update_banners');

const files = [
  'zh/bedroom/index.html',
  'zh/mattress/index.html',
  'zh/dining/index.html',
  'zh/office/index.html',
  'zh/massage-chair/index.html'
];

files.forEach(f => {
  const html = fs.readFileSync(f, 'utf8');
  const cardRegex = /<div class=["']sofa-card reveal["']>([\s\S]*?)<\/div>\s*<\/div>/g;
  let m;
  let idx = 0;
  console.log(`\n=== File: ${f} ===`);
  while ((m = cardRegex.exec(html)) !== null) {
    const card = m[1];
    const h3 = (card.match(/<h3>(.*?)<\/h3>/) || [])[1] || '';
    const p = (card.match(/<p>(.*?)<\/p>/) || [])[1] || '';
    const pricing = findProductPricing(h3, p, '');
    const hasBanner = card.includes('image-price-banner');
    idx++;
    console.log(`Card ${idx}: Title='${h3}' | HasBanner=${hasBanner} | FoundPricing=${!!pricing}`);
  }
});
