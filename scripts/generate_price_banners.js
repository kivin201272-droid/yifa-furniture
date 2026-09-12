/**
 * Automated Batch Image Price Banner Generator (Node.js)
 * ------------------------------------------------------
 * Generates customer-centric frosted glass banners with Twin/Full/Queen prices.
 * Can be run via:
 *   node scripts/generate_price_banners.js
 * 
 * Works with SVG composite or Sharp/Canvas.
 */

const fs = require('fs');
const path = require('path');

// Helper to create an SVG Frosted Glass Price Banner Overlay
function createBannerSvg(width, height, variants, tagline = '🔥 一件也是批发价') {
  const bannerHeight = Math.max(48, Math.min(120, Math.round(height * 0.14)));
  const bannerY = height - bannerHeight;
  const paddingX = Math.max(16, Math.round(width * 0.035));
  const centerY = bannerY + Math.round(bannerHeight / 2);
  const fontSize = Math.max(14, Math.round(bannerHeight * 0.32));

  // Build price pill SVG elements
  const formatPrice = (p) => (Number.isInteger(p) ? `$${p}` : `$${p.toFixed(2)}`);
  
  let rightElements = '';
  let offsetX = width - paddingX;
  const gap = Math.max(10, Math.round(width * 0.018));

  // Reverse iterate to layout from right to left
  const reversedVariants = [...variants].reverse();

  reversedVariants.forEach((v, idx) => {
    const code = (v.code || '').toString().toUpperCase();
    const size = (v.size || '').toString();
    const isQueen = code === 'Q' || size.toLowerCase().includes('queen');
    const priceStr = formatPrice(v.price);
    const labelStr = code.length <= 2 ? `${code}:` : `${size}:`;

    const textColor = isQueen ? '#fcd34d' : '#ffffff';
    const labelColor = isQueen ? '#fef08a' : '#d6d3d1';
    const fontWeight = isQueen ? '800' : '600';
    const pillBg = isQueen
      ? `<rect x="${offsetX - 85}" y="${centerY - 14}" width="85" height="28" rx="6" fill="rgba(245, 158, 11, 0.25)" stroke="rgba(251, 191, 36, 0.4)" stroke-width="1"/>`
      : '';

    // Estimate width
    const itemWidth = (labelStr.length + priceStr.length) * (fontSize * 0.58) + 12;

    rightElements = `
      <g>
        ${isQueen ? `<rect x="${offsetX - itemWidth}" y="${centerY - fontSize * 0.8}" width="${itemWidth}" height="${fontSize * 1.6}" rx="6" fill="rgba(245, 158, 11, 0.25)" stroke="rgba(251, 191, 36, 0.4)" stroke-width="1"/>` : ''}
        <text x="${offsetX - itemWidth + 6}" y="${centerY + 4}" font-family="system-ui, -apple-system, sans-serif" font-size="${fontSize * 0.85}" fill="${labelColor}" font-weight="500">${labelStr}</text>
        <text x="${offsetX - 6}" y="${centerY + 4}" font-family="system-ui, -apple-system, sans-serif" font-size="${fontSize}" fill="${textColor}" font-weight="${fontWeight}" text-anchor="end">${priceStr}</text>
      </g>
      ${idx < reversedVariants.length - 1 ? `<line x1="${offsetX - itemWidth - gap/2}" y1="${centerY - fontSize*0.5}" x2="${offsetX - itemWidth - gap/2}" y2="${centerY + fontSize*0.5}" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>` : ''}
      ${rightElements}
    `;

    offsetX -= (itemWidth + gap);
  });

  return `
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bannerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#09090b" stop-opacity="0.75" />
          <stop offset="100%" stop-color="#09090b" stop-opacity="0.92" />
        </linearGradient>
      </defs>
      
      <!-- Translucent Glass Banner -->
      <rect x="0" y="${bannerY}" width="${width}" height="${bannerHeight}" fill="url(#bannerGrad)" />
      
      <!-- Top Glass Highlight Line -->
      <line x1="0" y1="${bannerY}" x2="${width}" y2="${bannerY}" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1" />
      
      <!-- Left Tagline -->
      <text x="${paddingX}" y="${centerY + 4}" font-family="system-ui, -apple-system, PingFang SC, sans-serif" font-size="${fontSize * 0.95}" font-weight="700" fill="#fbbf24">
        ${tagline}
      </text>

      <!-- Right Prices -->
      ${rightElements}
    </svg>
  `;
}

// Demo generation
if (require.main === module) {
  const sampleVariants = [
    { code: 'T', size: 'Twin', price: 149 },
    { code: 'F', size: 'Full', price: 179 },
    { code: 'Q', size: 'Queen', price: 199 },
  ];

  const svg = createBannerSvg(800, 600, sampleVariants);
  const outPath = path.join(__dirname, '../assets/images/with_price_banner/demo_overlay.svg');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, svg, 'utf8');
  console.log(`[OK] Generated sample banner overlay SVG at: ${outPath}`);
}

module.exports = { createBannerSvg };
