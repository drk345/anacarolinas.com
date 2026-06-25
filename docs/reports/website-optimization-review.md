# AV-PROMPT-013 — Website Optimization Review

Audited: `60d54eb` (master) · 25 June 2026

---

## 1. Executive Summary

**Rating: Ready with minor fixes**

The site is well-built. CSP is strict and clean, image markup is complete and correct, JS is minimal (975 bytes), security headers are solid, and the build pipeline correctly excludes all internal material. No P0 blockers exist.

The main actionable issue is ~613KB of orphaned image files and ~43KB of orphaned font files that are deployed to production but never requested by any browser — pure waste that can be removed with no visual impact.

### Top 5 optimization risks

1. **6 orphaned image files in dist** — `hero-800.*` and `quees-*.jpg/webp` total ~570KB; zero pages reference them; browser never fetches them but they consume deploy bandwidth and storage
2. **2 orphaned font files in dist** — `spectral-500-normal-latin*.woff2` (~43KB) have no `@font-face` declaration in `editorial.css`; never requested
3. **Sitemap and `robots.txt` Sitemap URL still point to Pages URL** — must be updated atomically when custom domain connects (known, documented in prior reports)
4. **`<button>` elements missing `type="button"`** — all 9 hamburger buttons; not broken but semantically incomplete
5. **Spectral 400 italic not preloaded** — used above-fold on all inner pages (hero lead paragraph) but not in `<link rel="preload">` hints

### Custom domain recommendation
**Do not connect yet.** `privacidad.html` is still noindex pending legal review. When legal approval arrives, the domain connection should be paired with the URL-swap prompt (canonical, OG, JSON-LD, sitemap, robots — all pointing to Pages URL currently). Cloudflare Pages URL is fine for private review.

---

## 2. Findings by Priority

### P0 — Blocks launch

None.

---

### P1 — Should fix before public launch

#### P1-A — Orphaned images in dist (~570KB)

| File | Size | Referenced by? |
|---|---|---|
| `assets/img/hero-800.jpg` | 28.5KB | **No page** |
| `assets/img/hero-800.webp` | 18.6KB | **No page** |
| `assets/img/quees-1200.jpg` | 191.6KB | **No page** |
| `assets/img/quees-1200.webp` | 152.5KB | **No page** |
| `assets/img/quees-800.jpg` | 98.3KB | **No page** |
| `assets/img/quees-800.webp` | 80.9KB | **No page** |
| **Total** | **~570KB** | |

- `hero-800.*` appear to be pre-rename artifacts; the homepage now uses `home-hero-800.*`
- `quees-*` appear to be from an earlier "qué es ALMAVIVA" section that was removed from `index.html`
- `grep -RniE 'hero-800|quees' *.html` → zero matches confirmed

**Why it matters:** ~570KB shipped to every deploy for nothing. Not a performance risk (browsers only fetch referenced files), but wastes deploy storage and creates confusion about what is current.

**Recommended fix:** Delete `assets/img/hero-800.jpg`, `assets/img/hero-800.webp`, `assets/img/quees-*.jpg`, `assets/img/quees-*.webp`. No CSS or HTML changes needed.

**Risk level:** Very low — no page references these files. Deletion is safe.

**Changes visual design:** No.

---

#### P1-B — Orphaned font files in dist (~43KB)

| File | Size | @font-face in editorial.css? |
|---|---|---|
| `assets/fonts/spectral-500-normal-latin.woff2` | 22.8KB | **No** |
| `assets/fonts/spectral-500-normal-latin-ext.woff2` | 20.6KB | **No** |
| **Total** | **~43KB** | |

- `editorial.css` declares `@font-face` for Spectral: 400 normal, 400 italic, 500 italic, 600 normal
- There is **no** `@font-face` for Spectral 500 normal — `grep` confirms zero hits
- These files may originate from `styles.css` or `prototype.css` (both excluded from dist) and were retained when migrating to the editorial system

**Why it matters:** Deployed to production with zero chance of being fetched. ~43KB of clutter.

**Recommended fix:** Delete `assets/fonts/spectral-500-normal-latin.woff2` and `assets/fonts/spectral-500-normal-latin-ext.woff2`. No CSS or HTML changes needed.

**Risk level:** Very low — confirmed no CSS reference exists.

**Changes visual design:** No.

---

### P2 — Recommended improvement

#### P2-A — `<button>` missing `type="button"`

All 9 hamburger buttons: `<button id="navToggle" aria-label="Abrir menú" aria-expanded="false" ...>` have no `type` attribute.

**Why it matters:** A `<button>` without `type` defaults to `type="submit"` when inside a `<form>`. Currently no forms exist so this is not broken, but it's incorrect semantics and a future-safety hazard.

**Recommended fix:** Add `type="button"` to every `navToggle` button across all 9 pages.

**Risk level:** Zero visual change. 9-file edit (can be done with a single build-time sed or per-page edit).

---

#### P2-B — `<nav>` missing `aria-label`

`<nav class="site-nav__in">` has no `aria-label` attribute.

**Why it matters:** Screen readers announce unlabeled `<nav>` as simply "navigation". If a page ever gains a second nav landmark (e.g., breadcrumb), both would read as "navigation" with no distinction. Adding `aria-label="Navegación principal"` is a small improvement with no visual impact.

**Recommended fix:** `<nav class="site-nav__in" aria-label="Navegación principal">` across all pages.

---

#### P2-C — Spectral 400 italic not preloaded

All pages preload: `mulish-400-normal-latin.woff2` and `spectral-600-normal-latin.woff2`.

Not preloaded: `spectral-400-italic-latin.woff2` — but this font is used for:
- `.ed-pg-hero__lead` (hero italic lead paragraph — above the fold on every inner page)
- `.ed-sobre-hero__opening` (above fold on sobre-ana)
- Body text italics

**Why it matters:** This font is render-critical for the above-fold italic paragraph visible on every inner page hero. Without a preload hint, the browser discovers it only after parsing CSS and applying styles, causing a potential flash of unstyled/fallback text before the font loads.

**Recommended fix:** Add to all pages' `<head>`:
```html
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/spectral-400-italic-latin.woff2" crossorigin>
```

**Risk level:** Safe. Does not change any rendering, only instructs browser to fetch font sooner.

---

#### P2-D — `index.html` "Inicio" nav link missing `is-active`

On the homepage, `<a class="ed-nl" href="index.html">Inicio</a>` has no `is-active` class. All other pages correctly apply `is-active` to their corresponding nav entry.

**Why it matters:** Cosmetic inconsistency. Visitors on the homepage have no visual indicator of which page they're on.

**Recommended fix:** Add `is-active` to the "Inicio" link in `index.html`'s nav.

---

#### P2-E — No explicit HTML cache-control header

`_headers` defines cache rules for fonts, images, CSS, and JS — but has no explicit rule for `/*.html`.

**Why it matters:** Cloudflare Pages defaults to short-lived/revalidating for HTML, which is correct, but documenting it explicitly in `_headers` prevents ambiguity and makes the intent clear.

**Recommended fix:** Add to `_headers`:
```
/*.html
  Cache-Control: no-cache
```
This makes the intent explicit without changing behavior.

---

### P3 — Optional polish

#### P3-A — OG image quality

`og-card.jpg` is 36KB at 1200×630. This is light for the resolution and may look compressed in some social preview environments.

**Recommended fix:** Regenerate at quality 85–90, targeting ~80–120KB.

---

#### P3-B — CSP `img-src 'self' data:`

Current CSP allows `data:` URIs for images. This site has no data URI images. Tightening to `img-src 'self'` removes an unnecessary attack surface.

**Recommended fix:** Remove `data:` from `img-src` in `_headers`.

---

#### P3-C — HSTS `preload` not set

Current HSTS: `max-age=31536000; includeSubDomains`. The `preload` directive is not set.

**Note:** `preload` should only be added after the custom domain is connected, HSTS is verified stable, and the decision to join the HSTS preload list is deliberate. Not urgent.

---

#### P3-D — Image filename versioning for cache busting

Images use 1-year immutable cache (`max-age=31536000, immutable`). If a photo is replaced with the same filename, browsers that have cached the old image will show it for up to 1 year.

**Recommended fix (post-launch):** Use content-hashed image filenames (e.g., `home-hero-1200.abc123.jpg`) in a future Sharp pipeline pass. For now, accept the trade-off and rename files if they're replaced.

---

## 3. Performance Review

### HTML
- 9 pages, 9–18KB each — excellent
- Semantic structure correct; one `<h1>` per page ✓
- Heading hierarchy: H1 → H2 → H3 (sobre-ana) — logical ✓
- No render-blocking resources; `defer` on JS ✓
- CSS `<link>` in `<head>` correct ✓
- Font preloads in `<head>` ✓ (gap: Spectral italic, see P2-C)
- No duplicate metadata ✓
- Total HTML across all pages: ~125KB uncompressed; with brotli ~25-30KB

### CSS
- `editorial.css`: 33KB uncompressed → ~7KB brotli (estimated)
- One shared file for all pages — appropriate for this site size
- `?v=2` cache-busting strategy works; manual bump required on CSS changes
- `home.css`, `prototype.css`, `styles.css` correctly excluded from dist ✓
- Not minified — no visual impact since Cloudflare compresses at edge

### JavaScript
- `main.js`: 975 bytes — essentially zero overhead ✓
- IIFE wrapper, passive scroll listener, correct `aria-expanded` management ✓
- `defer` attribute on all pages ✓
- No external scripts ✓
- No inline JS ✓

### Images
- All images have responsive `<picture>` + `<source type="image/webp">` + JPEG fallback ✓
- All `<img>` have `width`, `height`, `alt`, `loading`, `decoding` ✓
- Hero images use `loading="eager" fetchpriority="high"` ✓
- Below-fold images use `loading="lazy" decoding="async"` ✓
- Largest image: `home-sobre-1200.jpg` at 324KB — acceptable for a hero-scale portrait
- All non-hero images under 250KB ✓
- **6 orphaned files: 570KB** (see P1-A)

### Fonts
- All fonts self-hosted, no CDN ✓
- `font-display: swap` on all `@font-face` declarations ✓
- Active fonts: Mulish 400, Spectral 400/500italic/600 — 10 files, ~220KB total
- Fonts cached 1yr immutable ✓
- **2 orphaned font files: 43KB** (see P1-B)
- Missing preload for Spectral 400 italic (see P2-C)

### Caching
| Asset type | TTL | Strategy | Assessment |
|---|---|---|---|
| Fonts | 1 year immutable | Correct — fonts don't change without new filenames | ✓ Good |
| Images | 1 year immutable | Acceptable; risk if image is replaced with same name | ✓ Acceptable |
| CSS | 1 hour + must-revalidate | Paired with `?v=N` query string — correct | ✓ Good |
| JS | 1 hour + must-revalidate | Correct given small file + infrequent changes | ✓ Good |
| HTML | Not explicit | Cloudflare default (effectively no-cache) — fine | △ Recommend explicit |

---

## 4. Accessibility Review

| Check | Result |
|---|---|
| One H1 per page | ✓ All 9 pages |
| Heading order (H1→H2→H3) | ✓ Logical on all pages |
| All `<img>` have `alt` | ✓ Confirmed |
| Decorative SVG icons marked `aria-hidden="true"` | ✓ WhatsApp floater, contact icons |
| Nav toggle `aria-label`, `aria-expanded`, `aria-controls` | ✓ All pages |
| `<html lang="es">` | ✓ All pages |
| `<meta name="viewport">` | ✓ All pages |
| External links `rel="noopener noreferrer"` | ✓ All blank targets confirmed |
| WhatsApp floating button `aria-label` | ✓ "Escríbeme por WhatsApp" |
| Footer privacy link visible | ✓ All pages |
| `focus-visible` styles in CSS | ✓ `outline: 3px solid var(--accent)` defined |
| `<button type="button">` | **✗** Missing `type` attribute (see P2-A) |
| `<nav aria-label>` | **△** No label (see P2-B) |
| Active nav state on homepage | **△** `is-active` missing on "Inicio" (see P2-D) |
| Contact icon SVGs have accessible text | △ Icons `aria-hidden` but parent `<a>` has no `aria-label` on index contact rows — visible text present, acceptable |

No `@media (prefers-reduced-motion)` rule exists. The site has no declared animations or transitions beyond CSS hover effects (filter, background, padding). Existing hover transitions at 0.2–0.3s are brief and unlikely to affect users with motion sensitivity. Still, adding a reduced-motion media query would be best practice for future additions.

---

## 5. Mobile Review

| Check | Result |
|---|---|
| Hamburger menu at ≤768px | ✓ CSS + JS correct |
| Mobile menu closes on link tap | ✓ Handled in main.js |
| Nav `is-floating` compact state | ✓ Reduces padding on scroll |
| Hero padding on mobile (`padding-top: 106px` at ≤900px) | ✓ Clears nav |
| Text scales with `clamp()` | ✓ Font sizes fluid across breakpoints |
| Images responsive | ✓ `92vw` sizes on mobile |
| Programme cards stack to 1-col at ≤900px | ✓ |
| Check-list 2-col collapses at ≤900px | ✓ |
| Pillar grid collapses at ≤480px | ✓ (→ 1-col) |
| CTA strip padding mobile | ✓ |
| WhatsApp button position | △ Bottom-right fixed at 24px; does not obscure main content but may overlap footer on very small screens during scroll |
| Horizontal overflow | ✓ `overflow-x: hidden` on body |
| Tap target sizes (min 44px) | ✓ Nav links min-height 48px on mobile; buttons 46px |

Pages checked manually via preview: `/`, `/privacidad.html`, `/sobre-ana.html`, `/contacto.html`.

---

## 6. Build and Deployment Hygiene

| Check | Result |
|---|---|
| Build completes without errors | ✓ |
| All 9 HTML pages in dist | ✓ |
| `sitemap.xml`, `robots.txt`, `_headers`, `favicon.svg` in dist | ✓ |
| `home.css`, `prototype.css`, `styles.css` excluded from dist | ✓ (build script explicitly removes) |
| `docs/reports/` not copied | ✓ (build script blocks `docs` and `reports`) |
| `tools/` not copied | ✓ (build script blocks `tools`) |
| `color.html`, `color.js`, `color.css` not in dist or source root | ✓ (on preview branch only) |
| Internal leakage scan | ✓ No leakage — all hits were false positives (normal page content matching grep terms) |
| CSP/artifact scan | ✓ No inline styles, no `<style>` blocks, no Google Fonts CDN |
| **6 orphaned images in dist** | **✗ Remove** (see P1-A) |
| **2 orphaned font files in dist** | **✗ Remove** (see P1-B) |

Total dist size: **4.1MB** (dominated by images). After removing orphaned images: ~3.5MB.

---

## 7. Caching Strategy Recommendation

### Current strategy (`editorial.css?v=2`)
- Manual `?v=N` query string cache-busting for CSS
- CSS TTL: 1 hour (`max-age=3600, must-revalidate`)
- Working correctly; no stale CSS risk

### When to bump to `?v=3`
Bump whenever `editorial.css` changes. The `?v=` query string must be updated across all 9 HTML pages simultaneously (the build doesn't automate this — it's a manual grep-and-replace). Worth automating in a future build step.

### Whether to keep manual versioning
- **Launch and early post-launch:** Keep `?v=N` — simple, reliable, understood
- **Post-launch (3+ months):** Consider adding a content-hash fingerprinting step to the build script (e.g., `editorial.abc123.css`) to eliminate the manual bump requirement and enable truly immutable CSS caching

### Cache policy for launch vs post-launch

| Phase | CSS/JS | Images | HTML |
|---|---|---|---|
| Active development (now) | 1h must-revalidate | 1yr immutable | no-cache default |
| Launch | 1h must-revalidate | 1yr immutable | explicit no-cache |
| Post-launch stable | Consider 24h–7d | 1yr immutable | no-cache |

After custom domain: Cloudflare's CDN layer will additionally cache HTML at the edge (respecting Cache-Control). Review Cloudflare Cache Rules when domain connects.

---

## 8. Recommended Implementation Prompt: AV-PROMPT-014

### AV-PROMPT-014 — Implement Website Optimization Fixes

**Branch:** `fix/website-optimization`

**Scope:** Implement the P1 and P2 findings from the AV-PROMPT-013 audit. Read-only assets deleted, HTML improvements applied, build verified.

#### Implement (in priority order):

**P1-A: Remove orphaned images**
Delete from `assets/img/`:
- `hero-800.jpg`
- `hero-800.webp`
- `quees-1200.jpg`
- `quees-1200.webp`
- `quees-800.jpg`
- `quees-800.webp`

Confirm no page references these before deleting. Run build. Verify dist no longer contains them.

**P1-B: Remove orphaned fonts**
Delete from `assets/fonts/`:
- `spectral-500-normal-latin.woff2`
- `spectral-500-normal-latin-ext.woff2`

Confirm no `@font-face` references these in `editorial.css`. Run build. Verify dist no longer contains them.

**P2-A: Add `type="button"` to hamburger buttons**
On all 9 pages: `<button id="navToggle" ... >` → `<button type="button" id="navToggle" ...>`

**P2-B: Add `aria-label` to `<nav>`**
On all 9 pages: `<nav class="site-nav__in">` → `<nav class="site-nav__in" aria-label="Navegación principal">`

**P2-C: Add Spectral 400 italic preload**
On all 9 pages, in `<head>` after existing preloads:
```html
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/spectral-400-italic-latin.woff2" crossorigin>
```

**P2-D: Add `is-active` to "Inicio" in `index.html`**
In `index.html` nav: `<a class="ed-nl" href="index.html">Inicio</a>` → `<a class="ed-nl is-active" href="index.html">Inicio</a>`

**P2-E: Add explicit HTML cache-control to `_headers`**
Add before the assets sections:
```
/*.html
  Cache-Control: no-cache
```

#### Do not implement in AV-PROMPT-014:
- P3-A (OG image quality) — requires content decision
- P3-B (CSP `data:`) — minor; can be a separate `_headers` tweak
- P3-C (HSTS preload) — only after domain connects
- P3-D (image filename hashing) — future build pipeline work
- Minification — out of scope
- Custom domain URL swap — separate prompt required

#### Validation after each change:
- `bash scripts/build-pages.sh` — must pass
- `find dist -type f | sort` — confirm orphaned files absent
- `grep -RniE 'hero-800|quees|spectral-500-normal' dist/` — must return empty
- Full noindex, forbidden terms, CSP, metadata scans
- Preview QA on `/`, `/sobre-ana.html`, `/privacidad.html`

---

## 9. Final Verdict

**Production is okay for private review** at `https://anacarolinas-com.pages.dev/`.

**Optimization does not block custom-domain launch** — but AV-PROMPT-014 fixes should be applied before connecting the domain. The P1 orphaned assets are harmless to users (browsers never request unreferenced files) but are wasteful and should be cleaned before the site becomes public.

**What must happen before custom-domain launch:**

1. `privacidad.html` legal review and `noindex` removal (AV-PROMPT-008/legal)
2. AV-PROMPT-014 optimization fixes (P1-A, P1-B, P2-A through P2-E)
3. Custom domain URL swap prompt — update all canonical/OG/JSON-LD/sitemap/robots from Pages URL to `anacarolinas.com`
4. Connect `anacarolinas.com` in Cloudflare DNS

Items 2–4 can happen in parallel with item 1 (legal review). Items 3–4 must happen together atomically.
