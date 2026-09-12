const fs = require('fs');
const path = require('path');
const { findProductPricing, renderBannerHtml } = require('./inspect_and_update_banners');

const pages = [
  { file: 'zh/bedroom/index.html', lang: 'zh', cat: 'Bedroom' },
  { file: 'bedroom/index.html', lang: 'en', cat: 'Bedroom' },
  { file: 'zh/mattress/index.html', lang: 'zh', cat: 'Mattress' },
  { file: 'mattress/index.html', lang: 'en', cat: 'Mattress' },
  { file: 'zh/living-room/index.html', lang: 'zh', cat: 'Living Room' },
  { file: 'living-room/index.html', lang: 'en', cat: 'Living Room' },
  { file: 'zh/dining/index.html', lang: 'zh', cat: 'Dining' },
  { file: 'dining/index.html', lang: 'en', cat: 'Dining' },
  { file: 'zh/office/index.html', lang: 'zh', cat: 'Office' },
  { file: 'office/index.html', lang: 'en', cat: 'Office' },
  { file: 'zh/massage-chair/index.html', lang: 'zh', cat: 'Massage Chair' },
  { file: 'massage-chair/index.html', lang: 'en', cat: 'Massage Chair' },
];

let totalBannersAdded = 0;

pages.forEach(({ file, lang, cat }) => {
  const filePath = path.join(__dirname, '..', file);
  if (!fs.existsSync(filePath)) {
    console.log(`[Skip] File not found: ${file}`);
    return;
  }

  let html = fs.readFileSync(filePath, 'utf8');

  // Regex to match each sofa-card
  // A sofa-card contains sofa-img-container and sofa-info (h3, p)
  const cardRegex = /(<div class=["']sofa-card reveal["']>[\s\S]*?<div class=["']sofa-img-container["']>)([\s\S]*?)(<\/div>[\s\S]*?<div class=["']sofa-info["']>[\s\S]*?<h3>(.*?)<\/h3>[\s\S]*?<p>(.*?)<\/p>)/g;

  let pageBannerCount = 0;

  const newHtml = html.replace(cardRegex, (fullMatch, cardHead, imgContainerContent, cardTail, h3Text, pText) => {
    // Check if image-price-banner already exists inside imgContainerContent
    let cleanImgContent = imgContainerContent.replace(/<div class=["']image-price-banner["']>[\s\S]*?<\/div>\s*<\/div>/g, '');
    cleanImgContent = cleanImgContent.replace(/<div class=["']image-price-banner["']>[\s\S]*?<\/div>/g, '').trim();

    // Look up pricing
    const pricing = findProductPricing(h3Text, pText, cat);
    if (!pricing) {
      // Fallback default pricing if available
      return fullMatch;
    }

    const bannerHtml = renderBannerHtml(pricing, lang);
    if (!bannerHtml) return fullMatch;

    pageBannerCount++;
    totalBannersAdded++;

    return `${cardHead}\n                ${cleanImgContent}${bannerHtml}\n            ${cardTail}`;
  });

  fs.writeFileSync(filePath, newHtml, 'utf8');
  console.log(`[OK] ${file}: Embedded/Updated ${pageBannerCount} frosted glass price banners.`);
});

console.log(`\n🎉 Completed! Total ${totalBannersAdded} price banners embedded across all real category pages.`);
