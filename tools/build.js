/* SUPERSEDED — original one-time de-bundler that produced the first version of
   the site from the Claude Design bundle. index.html, styles.css, and main.js are
   now hand-maintained (semantic classes, no inline styles). DO NOT re-run this: it
   would overwrite the hand-authored files with the old inline-styled output.
   Kept for reference / reproducibility of the initial import only.

   Original purpose: emits ../index.html, ../assets/css/styles.css, ../assets/js/main.js. */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const bundle = fs.readFileSync(path.join(__dirname, 'source-bundle.html'), 'utf8');

function grab(type) {
  const open = `<script type="__bundler/${type}">`;
  const start = bundle.indexOf(open, 6000);
  const from = start + open.length;
  const end = bundle.indexOf('</script>', from);
  return bundle.slice(from, end);
}
const template = JSON.parse(grab('template'));

// --- 1. Pull out the global (non-font) <style> block from the template head ---
const styleBlocks = [...template.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(m => m[1]);
const globalCss = styleBlocks[1].trim(); // [0] = embedded fonts (replaced by local), [1] = global

// --- 2. Extract the body: inner content of <x-dc> ... </x-dc> ---
let body = template.slice(template.indexOf('<x-dc>') + '<x-dc>'.length, template.indexOf('</x-dc>'));
// Drop the <helmet>...</helmet> head block; we rebuild <head> by hand.
body = body.slice(body.indexOf('</helmet>') + '</helmet>'.length).trim();

// --- 3. Resolve the DC template bindings ---
body = body
  .replace(/\{\{\s*accent\s*\}\}/g, '#A8501F')
  .replace(/\s*\{\{\s*navFloatClass\s*\}\}/g, '')
  .replace(/\s*\{\{\s*menuOpenClass\s*\}\}/g, '')
  .replace(/\s*onclick="\{\{\s*toggleMenu\s*\}\}"/g, '')
  .replace(/\s*onclick="\{\{\s*closeMenu\s*\}\}"/g, '');

// JS hooks for the nav
body = body.replace('<button class="ac3-hamb" aria-label="Abrir menú">',
                    '<button class="ac3-hamb" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">');
body = body.replace('<div class="ac3-navlinks " ', '<div class="ac3-navlinks" id="navLinks" ');
body = body.replace('<div class="ac3-navlinks" ', '<div class="ac3-navlinks" id="navLinks" '); // fallback if space already collapsed

// --- 4. Lower the hero h1 minimum for small screens (audit R3) ---
body = body.replace('font-size:clamp(52px,10vw,118px)', 'font-size:clamp(40px,11vw,118px)');

// --- 5. Replace the 3 image UUIDs with responsive <picture> elements ---
const pictures = {
  '8955a739-ee69-48f5-a435-c99bbadc2446': {
    cls: 'ac-img ac-img--hero', loading: 'eager', fetchpriority: 'high',
    name: 'hero', sizes: '(max-width:900px) 92vw, 46vw', responsive: false,
    alt: 'Ana Carolina respirando al sol junto al mar, en calma',
  },
  'b5c57aa4-487b-4946-9a0e-4e92f4c49276': {
    cls: 'ac-img ac-img--quees', loading: 'lazy', name: 'quees', sizes: '(max-width:768px) 92vw, 50vw',
    responsive: true, alt: 'Ana Carolina trabajando con una clienta en una sesión de neuroentrenamiento',
  },
  '8c317678-497c-4bc4-96f5-12e3e5e392a5': {
    cls: 'ac-img ac-img--sobre', loading: 'lazy', name: 'sobre', sizes: '(max-width:768px) 92vw, 42vw',
    responsive: true, alt: 'Retrato de Ana Carolina, fundadora del método ALMAVIVA',
  },
};
for (const [uuid, p] of Object.entries(pictures)) {
  // Match the whole <img ... src="uuid" ... > tag
  const re = new RegExp(`<img\\s+src="${uuid}"[^>]*>`, 'i');
  let pic;
  if (p.responsive) {
    pic = `<picture>
            <source type="image/webp" sizes="${p.sizes}" srcset="assets/img/${p.name}-800.webp 800w, assets/img/${p.name}-1200.webp 1200w">
            <img class="${p.cls}" src="assets/img/${p.name}-1200.jpg" srcset="assets/img/${p.name}-800.jpg 800w, assets/img/${p.name}-1200.jpg 1200w" sizes="${p.sizes}" loading="${p.loading}" decoding="async" alt="${p.alt}">
          </picture>`;
  } else {
    pic = `<picture>
            <source type="image/webp" srcset="assets/img/${p.name}-800.webp">
            <img class="${p.cls}" src="assets/img/${p.name}-800.jpg" loading="${p.loading}" fetchpriority="${p.fetchpriority}" decoding="async" alt="${p.alt}">
          </picture>`;
  }
  body = body.replace(re, pic);
}

// --- 6. Convert every style-hover="..." into a generated :hover class ---
const hoverRules = [];
let hoverN = 0;
const tagRe = /<([a-zA-Z0-9]+)((?:[^>"']|"[^"]*"|'[^']*')*?)\sstyle-hover="([^"]*)"((?:[^>"']|"[^"]*"|'[^']*')*?)>/g;
body = body.replace(tagRe, (full, tag, before, hover, after) => {
  const cls = `ach${++hoverN}`;
  hoverRules.push(`.${cls}:hover{${hover.replace(/;?$/, '')};}`);
  let attrs = before + after;
  if (/\sclass="/.test(attrs)) {
    attrs = attrs.replace(/(\sclass=")([^"]*)(")/, `$1$2 ${cls}$3`);
  } else {
    attrs = ` class="${cls}"` + attrs;
  }
  return `<${tag}${attrs}>`;
});

// --- 7. Add rel="noopener noreferrer" to every target="_blank" link (audit SS2) ---
body = body.replace(/<a\s+([^>]*?)target="_blank"([^>]*?)>/g, (full, b, a) => {
  if (/rel=/.test(b + a)) return full;
  return `<a ${b}target="_blank" rel="noopener noreferrer"${a}>`;
});

// --- 8. Tidy the wrapper: it carried a data-screen-label dev attribute ---
body = body.replace(/\s*data-screen-label="[^"]*"/, '');

// --- 9. Assemble styles.css ---
const fontsCss = fs.readFileSync(path.join(__dirname, 'fonts.generated.css'), 'utf8');
const extraCss = `
/* --- Self-hosted responsive images (audit R7, P1, I1/I2) --- */
.ac-img{display:block;width:100%;object-fit:cover;border:1px solid #DCD6C7;box-shadow:0 24px 50px -28px rgba(35,39,30,.45);}
.ac-img--hero{height:560px;object-position:50% 14%;border-color:#E2D8C8;box-shadow:0 26px 54px -30px rgba(35,39,30,.4);}
.ac-img--quees{height:480px;object-position:50% 20%;}
.ac-img--sobre{height:500px;object-position:50% 18%;}
picture{display:block;width:100%;}
@media (max-width:768px){
  .ac-img{height:auto !important;aspect-ratio:4/5;}
}

/* --- Generated hover styles (replace the DC runtime's style-hover) --- */
${hoverRules.join('\n')}
`;
const css = `${fontsCss}\n\n${globalCss}\n${extraCss}`;
fs.mkdirSync(path.join(ROOT, 'assets', 'css'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'assets', 'css', 'styles.css'), css);

// --- 10. main.js: floating nav on scroll + hamburger toggle ---
const js = `// ALMAVIVA — minimal nav behavior (replaces the Claude Design runtime)
(function () {
  var nav = document.querySelector('.ac3-nav');
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');

  // Floating nav after a little scroll
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('floating', window.scrollY > 60);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Hamburger menu
  if (toggle && links) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close when a link is tapped
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();
`;
fs.mkdirSync(path.join(ROOT, 'assets', 'js'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'assets', 'js', 'main.js'), js);

// --- 11. Assemble index.html ---
const SITE = 'https://anacarolinas.com';
const head = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ana Carolina S — Neurotraining y Coaching para Transformación Personal</title>
  <meta name="description" content="ALMAVIVA Neurotraining: neurociencia aplicada, prácticas somáticas y coaching para entrenar tu cerebro y transformar tu manera de vivir.">
  <link rel="canonical" href="${SITE}/">

  <meta property="og:type" content="website">
  <meta property="og:url" content="${SITE}/">
  <meta property="og:title" content="Ana Carolina S — ALMAVIVA Neurotraining">
  <meta property="og:description" content="Programa de neurociencia aplicada y coaching para entrenar tu cerebro y transformar tu manera de vivir.">
  <meta property="og:image" content="${SITE}/assets/img/quees-1200.jpg">
  <meta property="og:locale" content="es_ES">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Ana Carolina S — ALMAVIVA Neurotraining">
  <meta name="twitter:description" content="Programa de neurociencia aplicada y coaching para entrenar tu cerebro y transformar tu manera de vivir.">
  <meta name="twitter:image" content="${SITE}/assets/img/quees-1200.jpg">

  <meta name="theme-color" content="#3A4429">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">

  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/mulish-400-normal-latin.woff2" crossorigin>
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/spectral-600-normal-latin.woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
`;
const tail = `
<script src="assets/js/main.js" defer></script>
</body>
</html>
`;
fs.writeFileSync(path.join(ROOT, 'index.html'), head + body + '\n' + tail);

console.log(`Built index.html (${(head + body + tail).length} bytes), ${hoverN} hover rules, styles.css (${css.length} bytes)`);
