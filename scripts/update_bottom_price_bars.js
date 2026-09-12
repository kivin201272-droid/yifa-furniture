const fs = require('fs');
const path = require('path');
const { findProductPricing } = require('./inspect_and_update_banners');

const pages = [
  { file: 'zh/mattress/index.html', lang: 'zh', cat: 'Mattress' },
  { file: 'mattress/index.html', lang: 'en', cat: 'Mattress' },
  { file: 'zh/bedroom/index.html', lang: 'zh', cat: 'Bedroom' },
  { file: 'bedroom/index.html', lang: 'en', cat: 'Bedroom' },
  { file: 'zh/living-room/index.html', lang: 'zh', cat: 'Living Room' },
  { file: 'living-room/index.html', lang: 'en', cat: 'Living Room' },
  { file: 'zh/dining/index.html', lang: 'zh', cat: 'Dining' },
  { file: 'dining/index.html', lang: 'en', cat: 'Dining' },
  { file: 'zh/office/index.html', lang: 'zh', cat: 'Office' },
  { file: 'office/index.html', lang: 'en', cat: 'Office' },
  { file: 'zh/massage-chair/index.html', lang: 'zh', cat: 'Massage Chair' },
  { file: 'massage-chair/index.html', lang: 'en', cat: 'Massage Chair' },
];

function renderBottomPriceHtml(pricing, lang = 'zh', existingTags = []) {
  const isZh = lang === 'zh';
  const prefix = isZh ? '折后' : 'Sale';

  let priceHtml = '';
  if (pricing.type === 'variants' && pricing.variants && pricing.variants.length > 1) {
    const specsStr = pricing.variants.map((v) => {
      const formattedPrice = Number.isInteger(v.price) ? `$${v.price}` : `$${v.price.toFixed(2)}`;
      return `${v.code}: ${formattedPrice}`;
    }).join(' | ');

    priceHtml = `<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">${prefix} ${specsStr}</span>`;
  } else {
    let pVal = 0;
    if (pricing.type === 'variants' && pricing.variants && pricing.variants.length === 1) {
      pVal = pricing.variants[0].price;
    } else if (pricing.price) {
      pVal = pricing.price;
    }
    const cleanNum = Number.isInteger(pVal) ? pVal.toLocaleString() : pVal.toFixed(2);
    priceHtml = `<span class="price-tag" style="font-weight:bold; color:#e63946; margin-right:10px;">${prefix}$${cleanNum}</span>`;
  }

  // Combine with existing detail-tags
  const tagsHtml = existingTags.map(t => `<span class="detail-tag">${t}</span>`).join('\n                    ');

  return `<div class="sofa-details">\n                    ${priceHtml}${tagsHtml ? '\n                    ' + tagsHtml : ''}\n                </div>`;
}

pages.forEach(({ file, lang, cat }) => {
  const filePath = path.join(__dirname, '..', file);
  if (!fs.existsSync(filePath)) return;

  let html = fs.readFileSync(filePath, 'utf8');

  // Match each sofa-card
  const cardRegex = /(<div class=["']sofa-card reveal["']>[\s\S]*?<div class=["']sofa-info["']>[\s\S]*?<h3>(.*?)<\/h3>[\s\S]*?<p>(.*?)<\/p>[\s\S]*?)<div class=["']sofa-details["']>([\s\S]*?)<\/div>/g;

  let count = 0;
  const newHtml = html.replace(cardRegex, (fullMatch, cardBeforeDetails, h3Text, pText, existingDetailsInner) => {
    // Extract existing detail tags (excluding old price tags)
    const tagMatches = [];
    const tagRegex = /<span class=["']detail-tag["']>(.*?)<\/span>/g;
    let tm;
    while ((tm = tagRegex.exec(existingDetailsInner)) !== null) {
      const tagTxt = tm[1].trim();
      if (!tagMatches.includes(tagTxt)) {
        tagMatches.push(tagTxt);
      }
    }

    // Look up pricing
    const pricing = findProductPricing(h3Text, pText, cat);
    if (!pricing) {
      return fullMatch;
    }

    count++;
    const newDetailsHtml = renderBottomPriceHtml(pricing, lang, tagMatches);
    return `${cardBeforeDetails}${newDetailsHtml}`;
  });

  fs.writeFileSync(filePath, newHtml, 'utf8');
  console.log(`[OK] ${file}: Updated ${count} card bottom price details rows.`);
});

console.log('Finished updating all bottom price bars!');
