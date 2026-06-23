/* One-off: extract assets from the Claude Design bundle (zip/index.html),
   self-host Latin fonts, and emit optimized responsive images.
   Outputs go to ../assets/. Re-runnable. */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const sharp = require('sharp');

const ROOT = path.resolve(__dirname, '..');
const BUNDLE = path.join(__dirname, 'source-bundle.html');
const FONT_DIR = path.join(ROOT, 'assets', 'fonts');
const IMG_DIR = path.join(ROOT, 'assets', 'img');
fs.mkdirSync(FONT_DIR, { recursive: true });
fs.mkdirSync(IMG_DIR, { recursive: true });

const html = fs.readFileSync(BUNDLE, 'utf8');

function grab(type) {
  const open = `<script type="__bundler/${type}">`;
  const start = html.indexOf(open, 6000); // skip the loader region
  const from = start + open.length;
  const end = html.indexOf('</script>', from);
  return html.slice(from, end);
}
const manifest = JSON.parse(grab('manifest'));
const template = JSON.parse(grab('template'));

function bytesOf(uuid) {
  const e = manifest[uuid];
  let buf = Buffer.from(e.data, 'base64');
  if (e.compressed) buf = zlib.gunzipSync(buf);
  return buf;
}

// ---- FONTS: parse @font-face blocks, keep latin + latin-ext only ----
const KEEP = new Set(['latin', 'latin-ext']);
const faceRe = /\/\*\s*([\w-]+)\s*\*\/\s*@font-face\s*\{([\s\S]*?)\}/g;
let m;
const faces = [];
const fontFiles = new Map(); // uuid -> filename
while ((m = faceRe.exec(template))) {
  const subset = m[1];
  const block = m[2];
  if (!KEEP.has(subset)) continue;
  const family = (block.match(/font-family:\s*'([^']+)'/) || [])[1];
  const style = (block.match(/font-style:\s*(\w+)/) || [])[1] || 'normal';
  const weight = (block.match(/font-weight:\s*(\d+)/) || [])[1] || '400';
  const uuid = (block.match(/url\("([^"]+)"\)/) || [])[1];
  const range = (block.match(/unicode-range:\s*([^;]+);/) || [])[1].trim();
  const fname = `${family.toLowerCase()}-${weight}-${style}-${subset}.woff2`;
  if (!fontFiles.has(uuid)) {
    fs.writeFileSync(path.join(FONT_DIR, fname), bytesOf(uuid));
    fontFiles.set(uuid, fname);
  }
  faces.push({ family, style, weight, subset, range, fname });
}
const fontCss = faces.map(f => `/* ${f.subset} */
@font-face {
  font-family: '${f.family}';
  font-style: ${f.style};
  font-weight: ${f.weight};
  font-display: swap;
  src: url("../fonts/${f.fname}") format('woff2');
  unicode-range: ${f.range};
}`).join('\n');
fs.writeFileSync(path.join(__dirname, 'fonts.generated.css'), fontCss);
console.log(`Fonts: wrote ${fontFiles.size} woff2 files (latin + latin-ext) for ${faces.length} faces`);

// ---- IMAGES: optimize the 3 photos into responsive webp + jpg ----
const IMAGES = {
  '8955a739-ee69-48f5-a435-c99bbadc2446': 'hero',
  'b5c57aa4-487b-4946-9a0e-4e92f4c49276': 'quees',
  '8c317678-497c-4bc4-96f5-12e3e5e392a5': 'sobre',
};
const WIDTHS = [800, 1200];
const imgMeta = {};

(async () => {
  for (const [uuid, name] of Object.entries(IMAGES)) {
    const input = bytesOf(uuid);
    const meta = await sharp(input).metadata();
    imgMeta[name] = { srcW: meta.width, srcH: meta.height, ratio: meta.width / meta.height };
    for (const w of WIDTHS) {
      const pipe = sharp(input).resize({ width: w, withoutEnlargement: true });
      await pipe.clone().webp({ quality: 80 }).toFile(path.join(IMG_DIR, `${name}-${w}.webp`));
      await pipe.clone().jpeg({ quality: 82, mozjpeg: true }).toFile(path.join(IMG_DIR, `${name}-${w}.jpg`));
    }
    console.log(`Image ${name}: source ${meta.width}x${meta.height} -> ${WIDTHS.join('/')}w webp+jpg`);
  }
  fs.writeFileSync(path.join(__dirname, 'img-meta.json'), JSON.stringify(imgMeta, null, 2));
  console.log('Done. img-meta.json written.');
})();
