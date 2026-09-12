const fs = require('fs');
const path = require('path');

// 1. Load Price CSV data
const csvPath = path.join(__dirname, '../素材库/价钱/Furniture_Price_List_Adjusted.csv');
let priceCsvRows = [];
if (fs.existsSync(csvPath)) {
  const content = fs.readFileSync(csvPath, 'utf8').replace(/^\uFEFF/, '');
  const lines = content.split('\n').filter(l => l.trim());
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',');
    if (cols.length >= 6) {
      priceCsvRows.push({
        source: cols[0].trim(),
        page: cols[1].trim(),
        code: cols[2].trim(),
        description: cols[3].trim(),
        originalPrice: parseFloat(cols[4]) || 0,
        newPrice: parseFloat(cols[5]) || 0
      });
    }
  }
}

// 2. Load product_prices.json and src/data/products.json
const productPrices = JSON.parse(fs.readFileSync(path.join(__dirname, '../product_prices.json'), 'utf8') || '{}');
const productsJson = JSON.parse(fs.readFileSync(path.join(__dirname, '../src/data/products.json'), 'utf8') || '[]');

// Curated catalog dictionary for exact codes
const CURATED_PRICING = {
  // TH Bedroom Series
  'TH2506': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 499 }, { code: 'K', size: 'King', price: 599 }] },
  'TH2503': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 529 }, { code: 'K', size: 'King', price: 629 }] },
  'TH2608': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 489 }, { code: 'K', size: 'King', price: 589 }] },
  '818': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 299 }, { code: 'F', size: 'Full', price: 349 }, { code: 'Q', size: 'Queen', price: 399 }] },
  'IB-108Q': { type: 'single', price: 299, label: 'Queen' },
  'B-0188': { type: 'single', price: 329, label: 'Queen' },
  'B1902': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 459 }, { code: 'K', size: 'King', price: 559 }] },
  '836': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 429 }, { code: 'K', size: 'King', price: 529 }] },
  '839': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 439 }, { code: 'K', size: 'King', price: 539 }] },
  'B230': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 469 }, { code: '5-PC', size: '5-Piece Set', price: 1280 }] },
  'TH9903': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 559 }, { code: 'K', size: 'King', price: 659 }] },
  '838': { type: 'variants', variants: [{ code: 'Q', size: 'Queen', price: 429 }, { code: 'K', size: 'King', price: 529 }] },

  // Mattresses
  'BEAUTYREST BLACK': { type: 'single', price: 1380, label: 'King', tagline: '🔥 55% OFF 特惠' },
  'LUXURY DEEP SLEEP': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 299 }, { code: 'F', size: 'Full', price: 499 }, { code: 'Q', size: 'Queen', price: 599 }, { code: 'K', size: 'King', price: 888 }] },
  '163': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 189 }, { code: 'F', size: 'Full', price: 239 }, { code: 'Q', size: 'Queen', price: 269 }], tagline: '🌿 天然椰棕护脊' },
  '163# 半棕垫': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 189 }, { code: 'F', size: 'Full', price: 239 }, { code: 'Q', size: 'Queen', price: 269 }], tagline: '🌿 天然椰棕护脊' },
  'TH318': { type: 'variants', variants: [{ code: 'F', size: 'Full', price: 399 }, { code: 'Q', size: 'Queen', price: 459 }, { code: 'K', size: 'King', price: 599 }], tagline: '✨ 五星云感乳胶' },
  'N6001': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 159 }, { code: 'F', size: 'Full', price: 199 }, { code: 'Q', size: 'Queen', price: 229 }] },
  'M6010': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 179 }, { code: 'F', size: 'Full', price: 219 }, { code: 'Q', size: 'Queen', price: 249 }] },
  'M6100': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 199 }, { code: 'F', size: 'Full', price: 239 }, { code: 'Q', size: 'Queen', price: 269 }, { code: 'K', size: 'King', price: 359 }] },
  'M6101': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 219 }, { code: 'F', size: 'Full', price: 259 }, { code: 'Q', size: 'Queen', price: 289 }, { code: 'K', size: 'King', price: 379 }] },
  'M6102': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 239 }, { code: 'F', size: 'Full', price: 279 }, { code: 'Q', size: 'Queen', price: 309 }, { code: 'K', size: 'King', price: 399 }] },
  'M6103': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 249 }, { code: 'F', size: 'Full', price: 289 }, { code: 'Q', size: 'Queen', price: 329 }, { code: 'K', size: 'King', price: 419 }] },
  'M6104': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 269 }, { code: 'F', size: 'Full', price: 309 }, { code: 'Q', size: 'Queen', price: 349 }, { code: 'K', size: 'King', price: 439 }] },
  'M6105': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 289 }, { code: 'F', size: 'Full', price: 329 }, { code: 'Q', size: 'Queen', price: 369 }, { code: 'K', size: 'King', price: 459 }] },
  'M6106': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 299 }, { code: 'F', size: 'Full', price: 339 }, { code: 'Q', size: 'Queen', price: 379 }, { code: 'K', size: 'King', price: 469 }] },
  'M6011': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 229 }, { code: 'F', size: 'Full', price: 269 }, { code: 'Q', size: 'Queen', price: 299 }] },
  'M6107': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 209 }, { code: 'F', size: 'Full', price: 249 }, { code: 'Q', size: 'Queen', price: 279 }, { code: 'K', size: 'King', price: 369 }] },
  'M6108': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 259 }, { code: 'F', size: 'Full', price: 299 }, { code: 'Q', size: 'Queen', price: 339 }, { code: 'K', size: 'King', price: 429 }] },
  'M6109': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 279 }, { code: 'F', size: 'Full', price: 319 }, { code: 'Q', size: 'Queen', price: 359 }, { code: 'K', size: 'King', price: 449 }] },
  'M6012': { type: 'variants', variants: [{ code: 'T', size: 'Twin', price: 199 }, { code: 'F', size: 'Full', price: 239 }, { code: 'Q', size: 'Queen', price: 269 }] },

  // Dining
  'BZ-0396': { type: 'single', price: 680, label: '1+6套组' },
  'BZ-2192': { type: 'single', price: 780, label: '1+6套组' },
  'BZ-0296': { type: 'single', price: 720, label: '1+6套组' },
  'TH-DT04': { type: 'single', price: 860, label: '奢石套组' },

  // Office & Massage
  'F3050': { type: 'single', price: 1460, label: '大班台' },
  'F3051': { type: 'single', price: 1460, label: '大班台' },
  'F3052': { type: 'single', price: 1460, label: '大班台' },
  'D09': { type: 'single', price: 1980, label: '豪华版', tagline: '💆 智能4D零重力' }
};

// Helper to find variants / price for a product
function findProductPricing(codeOrTitle, description = '', category = '') {
  const cleanCode = (codeOrTitle || '').replace('#', '').trim().toUpperCase();
  
  // 1. Check CURATED_PRICING direct dictionary
  for (const [key, val] of Object.entries(CURATED_PRICING)) {
    if (cleanCode === key || cleanCode.includes(key) || key.includes(cleanCode)) {
      return val;
    }
  }

  // 2. Check productsJson (rich bedroom dataset)
  for (const p of productsJson) {
    const pCode = (p.code || '').toUpperCase();
    const pId = (p.id || '').toUpperCase();
    const pName = (p.name || '').toUpperCase();
    const pNameZh = (p.nameZh || '').toUpperCase();
    if (pCode === cleanCode || pId === cleanCode || pName.includes(cleanCode) || pNameZh.includes(cleanCode)) {
      return {
        type: 'variants',
        variants: p.variants.map(v => ({
          code: v.code,
          size: v.size,
          price: v.price
        }))
      };
    }
  }

  // 3. Check CSV PJ Warehouse / Other rows
  const matchingCsv = priceCsvRows.filter(r => {
    const rCode = r.code.toUpperCase();
    return rCode === cleanCode || rCode.startsWith(cleanCode) || cleanCode.startsWith(rCode);
  });

  if (matchingCsv.length > 0) {
    const variants = [];
    matchingCsv.forEach(r => {
      const desc = r.description.toLowerCase();
      let sizeCode = 'Q';
      if (desc.includes('twin')) sizeCode = 'T';
      else if (desc.includes('full')) sizeCode = 'F';
      else if (desc.includes('queen')) sizeCode = 'Q';
      else if (desc.includes('king')) sizeCode = 'King';
      else sizeCode = r.code;

      const price = r.originalPrice > 0 ? r.originalPrice : r.newPrice;
      if (price > 0 && !variants.some(v => v.code === sizeCode)) {
        variants.push({
          code: sizeCode,
          size: sizeCode,
          price: price
        });
      }
    });

    if (variants.length > 0) {
      const order = { 'T': 1, 'F': 2, 'Q': 3, 'King': 4 };
      variants.sort((a, b) => (order[a.code] || 99) - (order[b.code] || 99));
      return {
        type: 'variants',
        variants: variants
      };
    }
  }

  // 4. Check productPrices.json
  if (productPrices[cleanCode]) {
    return {
      type: 'single',
      price: productPrices[cleanCode]
    };
  }

  // 5. Pattern matches on F3030~F3049
  if (/^F30[3-4]\d/.test(cleanCode)) {
    return { type: 'single', price: 1460, label: '1+6套组' };
  }

  // 6. Check description for price patterns
  const fullMatch = description.match(/折后\s*(?:F[:：]\s*\$?(\d+)[，,\s]*Q[:：]\s*\$?(\d+)(?:[，,\s]*K[:：]\s*\$?(\d+))?)/i);
  if (fullMatch) {
    const vars = [];
    if (fullMatch[1]) vars.push({ code: 'F', size: 'Full', price: parseInt(fullMatch[1], 10) });
    if (fullMatch[2]) vars.push({ code: 'Q', size: 'Queen', price: parseInt(fullMatch[2], 10) });
    if (fullMatch[3]) vars.push({ code: 'K', size: 'King', price: parseInt(fullMatch[3], 10) });
    return { type: 'variants', variants: vars };
  }

  const singleMatch = description.match(/折后\s*\$?([\d,]+)/i) || description.match(/Sale\s*[:$]\s*([\d,]+)/i);
  if (singleMatch) {
    const pVal = parseInt(singleMatch[1].replace(/,/g, ''), 10);
    return { type: 'single', price: pVal };
  }

  return null;
}

// Generate Frosted Glass HTML Banner
function renderBannerHtml(pricing, lang = 'zh') {
  if (!pricing) return '';
  const isZh = lang === 'zh';
  const tagline = pricing.tagline || (isZh ? '🔥 工厂直销价' : '🔥 FACTORY DIRECT');

  let pricesHtml = '';
  if (pricing.type === 'variants' && pricing.variants && pricing.variants.length > 0) {
    const pills = pricing.variants.map((v) => {
      const isQueen = v.code === 'Q' || (v.size && v.size.toLowerCase().includes('queen'));
      const queenClass = isQueen ? ' queen' : '';
      const formattedPrice = Number.isInteger(v.price) ? `$${v.price}` : `$${v.price.toFixed(2)}`;
      return `<span class="price-pill${queenClass}"><span class="pill-label">${v.code}:</span><span class="pill-val">${formattedPrice}</span></span>`;
    });
    pricesHtml = pills.join('<span class="divider"></span>');
  } else if (pricing.price) {
    const formattedPrice = `$${pricing.price.toLocaleString()}`;
    const label = pricing.label || (isZh ? '特惠' : 'Sale');
    pricesHtml = `<span class="price-pill queen"><span class="pill-label">${label}:</span><span class="pill-val">${formattedPrice}</span></span>`;
  } else {
    return '';
  }

  return `\n                <div class="image-price-banner">\n                    <span class="banner-tagline">${tagline}</span>\n                    <div class="banner-prices">\n                        ${pricesHtml}\n                    </div>\n                </div>`;
}

module.exports = { findProductPricing, renderBannerHtml };
