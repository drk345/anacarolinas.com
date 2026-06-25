# AV-PROMPT-014 — Website Optimization Fixes

Implemented: `fix/website-optimization` · 25 June 2026
Based on audit: `docs/reports/website-optimization-review.md` (AV-PROMPT-013)

---

## 1. Summary

**What was fixed:** 7 items from the AV-PROMPT-013 audit (2 P1, 5 P2) — orphaned image and font files deleted, hamburger button type corrected, nav aria-label added, Spectral 400 italic preloaded, homepage active nav state set, and explicit HTML cache-control header added to `_headers`.

**What was intentionally not changed:**
- No page copy, colors, or layout
- No `editorial.css` modifications → CSS stays at `?v=2`
- `noindex` remains in `privacidad.html`
- Custom domain not connected, DNS/Cloudflare settings unchanged
- No analytics, cookies, tracking, external fonts, or third-party dependencies added
- CSP not weakened

**Custom domain:** Still not connected. Cloudflare Pages URL (`https://anacarolinas-com.pages.dev/`) remains active for private review. Custom domain connection is blocked by pending legal review of `privacidad.html`.

---

## 2. Fixes implemented

| Finding | Action taken | Files changed | Status |
|---|---|---|---|
| P1-A: 6 orphaned image files (~570KB) | Deleted `hero-800.jpg`, `hero-800.webp`, `quees-800.jpg`, `quees-800.webp`, `quees-1200.jpg`, `quees-1200.webp` from `assets/img/` | `assets/img/` (6 deleted) | ✓ Done |
| P1-B: 2 orphaned font files (~43KB) | Deleted `spectral-500-normal-latin.woff2`, `spectral-500-normal-latin-ext.woff2` from `assets/fonts/` | `assets/fonts/` (2 deleted) | ✓ Done |
| P2-A: `<button>` missing `type="button"` | Added `type="button"` to `navToggle` button on all 9 pages | All 9 root HTML pages | ✓ Done |
| P2-B: `<nav>` missing `aria-label` | Added `aria-label="Navegación principal"` to `<nav class="site-nav__in">` on all 9 pages | All 9 root HTML pages | ✓ Done |
| P2-C: Spectral 400 italic not preloaded | Added `<link rel="preload" as="font" type="font/woff2" href="assets/fonts/spectral-400-italic-latin.woff2" crossorigin>` to all 9 pages | All 9 root HTML pages | ✓ Done |
| P2-D: `index.html` Inicio missing `is-active` | Added `is-active` class to `<a class="ed-nl" href="#top">Inicio</a>` in `index.html` | `index.html` | ✓ Done |
| P2-E: No explicit HTML `Cache-Control` header | Added explicit `no-cache` rule for all 10 HTML routes in `_headers` | `_headers` | ✓ Done |

---

## 3. Asset cleanup

### Deleted image files

| File | Size | Reason |
|---|---|---|
| `assets/img/hero-800.jpg` | 28.5KB | Pre-rename artifact; homepage now uses `home-hero-800.jpg` |
| `assets/img/hero-800.webp` | 18.6KB | Same as above |
| `assets/img/quees-800.jpg` | 98.3KB | From a removed "qué es ALMAVIVA" section; no page references it |
| `assets/img/quees-800.webp` | 80.9KB | Same as above |
| `assets/img/quees-1200.jpg` | 191.6KB | Same as above |
| `assets/img/quees-1200.webp` | 152.5KB | Same as above |
| **Total saved** | **~570KB** | |

Verified with `grep -RniE 'hero-800\|quees-' *.html assets/css assets/js scripts sitemap.xml robots.txt` → zero genuine references (only `home-hero-800` in index.html, which is a different kept file with the `home-` prefix).

### Deleted font files

| File | Size | Reason |
|---|---|---|
| `assets/fonts/spectral-500-normal-latin.woff2` | 22.8KB | No `@font-face` declaration in `editorial.css`; only referenced by `styles.css` which is not in dist |
| `assets/fonts/spectral-500-normal-latin-ext.woff2` | 20.6KB | Same as above |
| **Total saved** | **~43KB** | |

Note: `spectral-500-italic-latin.woff2` and `spectral-500-italic-latin-ext.woff2` are **NOT** deleted — they are correctly referenced by an `@font-face` declaration in `editorial.css` (Spectral 500 italic, used for `.ed-italic` styled emphasis in programme content).

### Before vs after dist

| Category | Before | After |
|---|---|---|
| Image files in dist | 27 files (~3.6MB) | 21 files (~3.0MB, −570KB) |
| Font files in dist | 12 files (~270KB) | 10 files (~227KB, −43KB) |
| HTML pages in dist | 9 | 9 (unchanged) |
| CSS in dist | `editorial.css?v=2` | `editorial.css?v=2` (unchanged) |
| JS in dist | `main.js` | `main.js` (unchanged) |
| Total dist | ~4.1MB | ~3.5MB |

---

## 4. Accessibility improvements

### P2-A: Button type attribute
All 9 hamburger toggle buttons now correctly specify `type="button"`:
```html
<!-- Before -->
<button id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">

<!-- After -->
<button type="button" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navLinks">
```
This prevents the button from defaulting to `type="submit"` if ever wrapped in a form, and is semantically correct.

### P2-B: Nav aria-label
All 9 main navigation elements now have a label:
```html
<!-- Before -->
<nav class="site-nav__in">

<!-- After -->
<nav class="site-nav__in" aria-label="Navegación principal">
```
Screen readers now announce "Navegación principal" when entering the navigation landmark.

### P2-C: Spectral 400 italic preload
All 9 pages now preload the latin subset of Spectral 400 italic:
```html
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/spectral-400-italic-latin.woff2" crossorigin>
```
This font is used for `.ed-pg-hero__lead` (the italic lead paragraph visible above the fold on every inner page hero). The latin-ext subset is discovered progressively — preloading the latin cut alone covers the most common above-fold visitors without over-fetching.

Preload verified: `spectral-400-italic-latin.woff2` exists in `assets/fonts/` and has a matching `@font-face` declaration in `editorial.css`.

### P2-D: Homepage active nav state
`index.html` "Inicio" link now has `is-active` consistent with all other pages:
```html
<!-- Before -->
<a class="ed-nl" href="#top">Inicio</a>

<!-- After -->
<a class="ed-nl is-active" href="#top">Inicio</a>
```

---

## 5. Caching changes

### HTML cache policy (new)
Added explicit `Cache-Control: no-cache` for all 10 HTML routes in `_headers`:
- `/` (root)
- `/index.html`
- `/programas.html`
- `/sesiones-individuales.html`
- `/conecta.html`
- `/foco.html`
- `/intensivo.html`
- `/sobre-ana.html`
- `/contacto.html`
- `/privacidad.html`

`no-cache` instructs browsers and CDN to revalidate with the server on every visit, ensuring visitors get fresh HTML immediately after each deploy. The global `/*` block still applies all security headers to HTML routes.

### CSS/JS cache policy (unchanged)
`/assets/css/*` and `/assets/js/*` remain at `public, max-age=3600, must-revalidate` (1-hour TTL). Paired with `editorial.css?v=2` cache-busting query string.

### Image cache policy (unchanged)
`/assets/img/*` remains at `public, max-age=31536000, immutable` (1-year).

### Font cache policy (unchanged)
`/assets/fonts/*` remains at `public, max-age=31536000, immutable` (1-year). CORS header unchanged.

### CSS version
`editorial.css` was not modified. All 9 pages stay on `editorial.css?v=2`.

---

## 6. Remaining optimization items

The following items from AV-PROMPT-013 were intentionally not implemented:

| Item | Priority | Reason deferred |
|---|---|---|
| OG image quality (`og-card.jpg` is 36KB at 1200×630) | P3 | Requires content/photo decision; no technical blocker |
| CSP `img-src 'self' data:` — `data:` not needed | P3 | Negligible security risk on static site; separate `_headers` tweak |
| HSTS `preload` directive | P3 | Must wait until custom domain is connected and verified stable |
| Image filename hash-based cache busting | P3 | Requires build pipeline change; not a current pain point |
| CSS/JS minification | P3 | Cloudflare brotli compression at edge makes this very low priority |
| Spectral 400 italic latin-ext preload | P2 | Latin subset covers most above-fold visitors; ext subset discovered progressively |

### Remaining launch blockers

1. **`privacidad.html` legal review** — `noindex` must remain until Ana and/or legal counsel approve the draft
2. **Custom domain URL swap** — when `anacarolinas.com` is connected, a separate prompt must update all canonical, OG, JSON-LD, sitemap, and robots URLs from `anacarolinas-com.pages.dev` to `anacarolinas.com`
3. **Custom domain DNS connection** — must happen after item 1 is cleared and simultaneously with item 2

---

## 7. Build and scan results

### Build
`bash scripts/build-pages.sh` → ✓ passes, 9 pages, no leakage

### Orphaned asset scan
`grep -RniE 'hero-800|quees-|spectral-500-normal-latin' *.html assets/css assets/js scripts sitemap.xml robots.txt`
→ Only false positives: `home-hero-800` in index.html (kept file with prefix), `spectral-500-normal-latin` in `styles.css` (not in dist)

### Dist content
No orphaned images, no orphaned fonts, no docs/reports, no `spectral-500-normal` files.

### Forbidden terms
CLEAN

### CSP/artifact scan
CLEAN — no inline styles, no `<style>`, no Google Fonts CDN

### Privacy noindex
`<meta name="robots" content="noindex">` present in `privacidad.html`

### Sitemap
`privacidad.html` not listed; 8 public pages listed; URLs point to `anacarolinas-com.pages.dev` (correct until custom domain connects)

### CSS version
All 9 pages: `editorial.css?v=2` — consistent; CSS unchanged
