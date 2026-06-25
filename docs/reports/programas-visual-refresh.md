# AV-PROMPT-015 — Programas Page Visual Refresh

Implemented: `fix/programas-visual-refresh` · 25 June 2026
Based on: Claude Design handoff `WEB PROGRAMAS-handoff.zip`
Rollback tag: `pre-programas-visual-refresh-2026-06-25`

---

## 1. Summary

**What changed:** Full visual redesign of `programas.html` — from a structured catalogue with an accent-coloured hero to a premium editorial layout with a full-bleed 2-column hero, a haze marino intro band, and four image-led programme panels. All existing content (decision helper, comparison table, FAQ, therapy note, CTA strip) is preserved.

**What was intentionally not changed:**
- No copy changes on other pages
- `noindex` remains in `privacidad.html`
- Custom domain not connected, DNS/Cloudflare settings unchanged
- No analytics, cookies, tracking, external fonts, or third-party scripts added
- CSP not weakened — zero inline `style=""` attributes, zero `<style>` blocks
- All programme page links unchanged

**Design source:** `C:\Users\FRBRA2\Downloads\handoff-extract\web-programas\project\Programas.dc.html`

**Custom domain:** Still not connected. Cloudflare Pages URL (`https://anacarolinas-com.pages.dev/`) remains active for private review. Custom domain is blocked by pending legal review of `privacidad.html`.

---

## 2. Design decisions

### Hero heading
Kept verbatim from the Claude Design handoff: **"Encuentra el camino que acompaña tu momento"**, rendered in four lines with `<br>` breaks to match the design's narrow-column intention. Applied `text-transform: uppercase` via CSS (not HTML) using Spectral 600 weight.

### CTA choice
**"Agendar conversación inicial"** was chosen over the design's shorter **"Agendar conversación"** for consistency with the rest of the site (the CTA strip on all inner pages uses this exact phrase) and because "inicial" sets proper expectations — a short introductory conversation, not a full session commitment. A secondary outline-dark button ("Explorar programas ↓") provides a soft scroll to the panels section.

### Blue accent (Haze marino `#95A8AD`)
Used exclusively for the intro band between the hero and the programme panels (`ed-sec--haze`). This creates visual breathing room and editorial rhythm without making the blue a dominant brand colour. The global footer remains olive green (unchanged). No other elements use the haze colour.

### Programme panels — four images
The Claude Design handoff only showed two panels (Foco + Intensivo). All four programmes are shown:
- **Sesiones individuales**: `programas-sesiones-*` (from `cierre.jpg` source)
- **ALMAVIVA Conecta**: reuses existing `home-cursos-*` images — the only programme without a dedicated new photo; the existing image (Ana in a relaxed studio/home setting) suits the group/community feel of Conecta
- **ALMAVIVA Foco**: `programas-foco-*` (from `foco.jpg` source)
- **ALMAVIVA Intensivo**: `programas-intensivo-*` (from `intensivo.jpg` source)

### Design bugs NOT reproduced
| Design bug | Production choice |
|---|---|
| Nav link "Sesiones 1:1" | Correct label "Sesiones individuales" (already in production) |
| Footer "Sesiones 1:1" | Olive footer with correct links (unchanged) |
| Footer background `#C2D6DB` | Olive footer (unchanged — blue only used for intro band) |
| `href="#"` placeholder links | All links point to real pages |
| Google Fonts CDN (`fonts.googleapis.com`) | Self-hosted fonts only |
| `support.js` Claude Design runtime | Not included |
| Inline `style=""` everywhere | Zero inline styles — all class-based |
| Band text "Dos caminos" | Updated to "Cuatro caminos" (four programmes, not two) |

---

## 3. New files and assets

### Image assets (in `assets/img/`)
All optimised with Sharp (Node.js), resized from 5–7MB source JPEGs to 800w and 1200w WebP + JPEG pairs.

| File | Format | Size |
|---|---|---|
| `programas-hero-800.webp` | 800×1067 WebP | 102KB |
| `programas-hero-800.jpg` | 800×1067 JPEG | 142KB |
| `programas-hero-1200.webp` | 1200×1600 WebP | 197KB |
| `programas-hero-1200.jpg` | 1200×1600 JPEG | 289KB |
| `programas-sesiones-800.webp` | 800×1067 WebP | 73KB |
| `programas-sesiones-800.jpg` | 800×1067 JPEG | 120KB |
| `programas-sesiones-1200.webp` | 1200×1600 WebP | 136KB |
| `programas-sesiones-1200.jpg` | 1200×1600 JPEG | 232KB |
| `programas-foco-800.webp` | 800×1067 WebP | 82KB |
| `programas-foco-800.jpg` | 800×1067 JPEG | 129KB |
| `programas-foco-1200.webp` | 1200×1600 WebP | 150KB |
| `programas-foco-1200.jpg` | 1200×1600 JPEG | 249KB |
| `programas-intensivo-800.webp` | 800×1067 WebP | 101KB |
| `programas-intensivo-800.jpg` | 800×1067 JPEG | 142KB |
| `programas-intensivo-1200.webp` | 1200×1600 WebP | 207KB |
| `programas-intensivo-1200.jpg` | 1200×1600 JPEG | 288KB |

Source mapping: `hero.jpg` → programas-hero, `cierre.jpg` → programas-sesiones, `foco.jpg` → programas-foco, `intensivo.jpg` → programas-intensivo. All from `tools/preview-programas/assets/` (extracted from ZIP).

### CSS additions to `editorial.css` (now `?v=3`)
All new classes prefixed `ed-programas-*` to avoid namespace collision:

| Class | Purpose |
|---|---|
| `--haze: #95A8AD` | New CSS custom property (root token) — not yet in `:root`, used inline in `.ed-sec--haze` |
| `.ed-sec--haze` | Section background `#95A8AD` with dark teal text |
| `.ed-btn--outline-dark` | Olive border/text outline button for white/light backgrounds |
| `.ed-programas-hero` | 2-col grid (`1fr 1.08fr`), white background, overflow hidden |
| `.ed-programas-hero__copy` | Left column: flex col, 136px top padding for nav clearance |
| `.ed-programas-hero__title` | Spectral 600, uppercase, clamp(32px → 62px), olive |
| `.ed-programas-hero__sub` | Mulish, clamp(15px → 18px), ink |
| `.ed-programas-hero__actions` | Flex row, gap 14px, margin-top 44px |
| `.ed-programas-hero__media` | Right column: relative, min-height 660px, overflow hidden |
| `.ed-programas-band` | Intro band inner: max-width, 2-col grid, white text |
| `.ed-programas-band__h2` | Spectral 600, clamp(28px → 52px), white |
| `.ed-programas-band__lead` | Spectral 400 italic, clamp(17px → 21px), white 88% |
| `.ed-programas-grid` | 2×2 image panel grid, 3px gaps, cream3 background |
| `.ed-programas-panel` | Full-bleed link panel, 560px min-height, flex col end |
| `.ed-programas-panel__bg` | Absolute-positioned bg image, object-fit cover, scale hover |
| `.ed-programas-panel__scrim` | Gradient overlay (transparent top → 72% bottom) |
| `.ed-programas-panel__body` | Text content, z-index 2 |
| `.ed-programas-panel__meta` | Spectral italic, 15px, white 82% |
| `.ed-programas-panel__title` | Spectral 600, uppercase, clamp(20px → 28px), white |
| `.ed-programas-panel__cta` | Inline outline pill: 12px caps, cream border |

Responsive breakpoints: `≤900px` stacks hero to 1-col (480px media min-height), stacks band to 1-col, stacks panels to 1-col. `≤480px` reduces hero padding, panel height to 420px.

---

## 4. CSS version bump

`editorial.css` changed → bumped from `?v=2` to `?v=3` on all 9 root HTML pages:
`index.html`, `programas.html`, `sesiones-individuales.html`, `conecta.html`, `foco.html`, `intensivo.html`, `sobre-ana.html`, `contacto.html`, `privacidad.html`.

---

## 5. Page structure (new)

| Section | Class / Element | Background | Notes |
|---|---|---|---|
| Nav | `site-nav` | Cream | Unchanged |
| Hero | `ed-programas-hero` | White `#FFFFFF` | NEW: 2-col, image right |
| Intro band | `ed-sec--haze` | `#95A8AD` haze | NEW: "Cuatro caminos..." |
| Programme panels | `ed-programas-grid` | Cream3 (gap) | NEW: 2×2 image panels |
| Decision helper | `ed-sec--cream ed-tex` | Cream | Preserved |
| Comparison table | `ed-sec--cream3 ed-tex` | Cream3 | Preserved |
| FAQ | `ed-sec--cream2 ed-tex` | Cream2 | Preserved |
| Therapy note | `ed-sec--cream ed-tex` | Cream | Preserved |
| CTA strip | `ed-cta-strip ed-sec--olive` | Olive | Preserved |
| Footer | `ed-footer` | Olive2 | Unchanged |

---

## 6. Validation results

| Check | Result |
|---|---|
| CSS version — all 9 pages at `?v=3` | ✓ PASS |
| Forbidden terms scan | ✓ PASS (false positives from WhatsApp SVG `<path d="...">` coordinate data only) |
| Inline `style=""` check | ✓ PASS — zero inline styles in `programas.html` |
| `<style>` block check | ✓ PASS — none |
| External fonts / third-party scripts | ✓ PASS — none |
| Analytics / tracking | ✓ PASS — none |
| `noindex` in `privacidad.html` | ✓ PASS — preserved |
| New images — all 16 present | ✓ PASS |
| Conecta images (reused) — all 4 present | ✓ PASS |
| New CSS classes in `editorial.css` | ✓ PASS — 20 selectors confirmed |
| Build script (`build-pages.sh`) | ✓ PASS — 9 pages, no leakage |
| DOM layout check (1280px viewport) | ✓ PASS — hero: 608px left / 657px right; 4 panels present |

**Note on forbidden terms false positives:** `grep -niE "CLP|DKK|..."` returns matches in the WhatsApp SVG `<path d="...">` attribute (coordinate data like `2C6.58 2...L2.05...`). These are SVG drawing commands, not page text. Verified manually — no forbidden terms in visible content.

---

## 7. Remaining open items

| Item | Status |
|---|---|
| `privacidad.html` legal review | Blocked — `noindex` must remain until Ana + legal approve |
| Custom domain connection | Blocked — pending legal review |
| Custom domain URL switch | When `anacarolinas.com` connects, update all canonical/OG/JSON-LD/sitemap/robots from Pages URL |
| Conecta dedicated photo | Optional — `home-cursos-*` is currently reused; a dedicated Conecta image could be added later |
| `--haze` as root CSS token | Optional — currently used only as hardcoded value in `.ed-sec--haze`; could be promoted to `:root` if reused elsewhere |
