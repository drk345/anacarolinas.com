/* Generate a branded 1200x630 Open Graph share card, and report the pixel
   dimensions of the served images (for <img> width/height attributes). */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const IMG = path.resolve(__dirname, '..', 'assets', 'img');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#3A4429"/>
  <rect x="0" y="0" width="1200" height="630" fill="url(#g)"/>
  <defs>
    <radialGradient id="g" cx="82%" cy="-10%" r="120%">
      <stop offset="0%" stop-color="#4A5636"/>
      <stop offset="60%" stop-color="#3A4429"/>
    </radialGradient>
  </defs>
  <g transform="translate(90,150)">
    <rect x="0" y="-6" width="46" height="3" fill="#A8501F"/>
    <text x="62" y="0" font-family="Mulish,Arial,sans-serif" font-size="22" font-weight="800" letter-spacing="4" fill="#C7D0AE">NEUROCIENCIA APLICADA · BIENESTAR</text>
    <text x="0" y="130" font-family="Georgia,'Times New Roman',serif" font-size="150" font-weight="700" letter-spacing="-2" fill="#F2EFE6">ALMAVIVA</text>
    <text x="4" y="180" font-family="Mulish,Arial,sans-serif" font-size="30" font-weight="800" letter-spacing="14" fill="#D99A6A">NEUROTRAINING</text>
    <text x="0" y="270" font-family="Georgia,'Times New Roman',serif" font-style="italic" font-size="40" fill="#EDEFE3">Entrena tu cerebro. Transforma tu manera de vivir.</text>
  </g>
  <text x="90" y="560" font-family="Georgia,'Times New Roman',serif" font-size="30" font-weight="600" fill="#FFFFFF">Ana Carolina S</text>
</svg>`;

(async () => {
  await sharp(Buffer.from(svg)).jpeg({ quality: 86, mozjpeg: true }).toFile(path.join(IMG, 'og-card.jpg'));
  const og = await sharp(path.join(IMG, 'og-card.jpg')).metadata();
  console.log(`og-card.jpg ${og.width}x${og.height}`);

  for (const f of ['hero-800.jpg', 'quees-1200.jpg', 'sobre-1200.jpg']) {
    const m = await sharp(path.join(IMG, f)).metadata();
    console.log(`${f} ${m.width}x${m.height}`);
  }
})();
