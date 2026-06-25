# AV-PROMPT-015B — Programas Page Correction

Implemented: `fix/programas-correction` · 25 June 2026
Rollback tag: `pre-programas-correction-2026-06-25`
Source of truth: `tools/preview-programas/index.html` (Ana's design preview)

---

## 1. Summary

**What changed:** Corrected `programas.html` and the programas CSS block in `editorial.css` to match Ana's actual design reference. The AV-PROMPT-015 implementation had several visual discrepancies from Ana's file — wrong heading typeface, nav/image collision, wrong band colour, wrong panel alignment, and four panels instead of two. This prompt corrects all of them.

**What was intentionally not changed:**
- All other 8 HTML pages (no copy, colour, or layout changes)
- `noindex` remains in `privacidad.html`
- Custom domain not connected, DNS/Cloudflare settings unchanged
- No analytics, cookies, tracking, external fonts, or third-party scripts added
- CSP not weakened — zero inline `style=""` attributes, zero `<style>` blocks
- Programme subpages (`foco.html`, `intensivo.html`, `sesiones-individuales.html`, `conecta.html`) untouched

---

## 2. Corrections implemented

| Finding | Root cause | Fix |
|---|---|---|
| Hero heading: Spectral 600 | `editorial.css` used Spectral, not Mulish | Changed to `font-family: 'Mulish'; font-weight: 400` |
| Hero image overlaps nav | No `margin-top` on `.ed-programas-hero` | Added `margin-top: 63px` (nav height) |
| Band colour `#95A8AD` (Haze marino) | Wrong colour extracted from design | Changed to `#B7C9CD` (Salvia) |
| Band layout: 2-col Spectral text | Misread the design grid | Full-width Mulish centred H2, `white-space` can wrap |
| Band lead text: wrong style | Spectral italic, wrong colour | Mulish normal, 18px, `#3D4F53`, left-offset below H2 |
| Panels: bottom-aligned text | `justify-content: flex-end` | Changed to `center`; added `align-items: center; text-align: center` |
| Panels: 4 panels (Sesiones + Conecta + Foco + Intensivo) | Expanded beyond design spec | Reduced to 2 panels: Foco + Intensivo only |
| Panel meta: 15px Spectral italic | Wrong size | Corrected to 19px, same family and style |
| Panel title: clamp(20px → 28px) weight 600 | Too small, wrong sizing | Corrected to `clamp(26px, 3.2vw, 38px)`, weight 600 |
| Panel scrim: heavy bottom | Didn't suit centred text | Lighter gradient matching Ana's design |
| No editorial closing section | Not in first implementation | Added 3-col cierre section (H2 + portrait + CTA) |
| Hero: two CTAs + description text | Extra elements not in design | Removed description; reduced to single outline CTA |
| Band headline: "Cuatro caminos" | 015 counted four programmes | Changed to "Dos caminos para un mismo método" |
| Decision helper: 5 items with all programmes | Matched old 4-panel layout | Simplified to 3 items: Foco / Intensivo / Conversación inicial |
| Comparison table | Not in Ana's design | Removed entirely |
| FAQ section | Not in Ana's design | Removed entirely |

---

## 3. Design decisions and deviations

### Nav label: "Sobre mí" vs "Sobre Ana"
Ana's design screenshot showed "Sobre Ana" in the nav. All 8 other production pages use "Sobre mí" consistently (verified via grep). Keeping "Sobre mí" to preserve site-wide consistency. Note this for Ana's review.

### "¿Lista para iniciar tu proceso?" — feminine form
The cierre H2 uses "Lista" (feminine). This matches Ana's design exactly and is appropriate given her audience.

### Therapy note preserved
Ana's design file has no therapy note. Kept in production as protective disclaimer — it's defensive text, not a claim. Ana can remove it once she reviews.

### "Conozcámonos" as cierre CTA
Kept from Ana's design as a softer, more personal CTA distinct from the CTA strip's "Agendar conversación".

### `font-size` on panel title: `clamp(26px, 3.2vw, 38px)` vs design's `38px`
Fixed at 38px, but clamped to prevent overflow on viewports below 1188px. At 1280px: `3.2vw ≈ 41px` → capped at 38px. Matches design at standard viewport.

### Band headline `white-space`
Design used `white-space: nowrap` which would cause horizontal scroll on narrow viewports. Removed from production CSS — the text wraps naturally on mobile.

---

## 4. CSS changes (editorial.css)

Replaced the entire programas CSS block (previously lines 500–683) with corrected declarations:

| Class | Change |
|---|---|
| `.ed-sec--haze` | Background `#95A8AD` → `#B7C9CD`; text `#1C2D30` → `#23291C` |
| `.ed-programas-hero` | Added `margin-top: 63px`, `border-top`, columns `1fr 1.04fr` |
| `.ed-programas-hero__copy` | Padding adjusted: `136px 60px 96px 40px` → `100px 76px 96px 50px` |
| `.ed-programas-hero__title` | Font: Spectral 600 → Mulish 400; clamp 32–62px → 30–56px; line-height 1.12 → 1.28 |
| `.ed-programas-hero__sub` | **Removed** from HTML (CSS class retained but unused) |
| `.ed-programas-hero__actions` | `margin-top` 44px → 54px |
| `.ed-programas-hero__media` | `min-height` 660px (unchanged) |
| `.ed-programas-band` | Removed 2-col grid; padding `80px 40px 88px` → `18px 24px 72px` |
| `.ed-programas-band__h2` | Font: Spectral 600 → Mulish 400; centred; huge clamp; letter-spacing −0.02em; dark ink |
| `.ed-programas-band__lead` | Font: Spectral italic → Mulish normal; 18px; `#3D4F53`; left-offset |
| `.ed-programas-panel` | `justify-content: flex-end` → `center`; added `align-items: center; text-align: center`; `min-height` 560→660px; `padding` 48px 44px → 54px 50px |
| `.ed-programas-panel__scrim` | Lighter gradient (72% → 62% max opacity) |
| `.ed-programas-panel__body` | Added `text-align: center` |
| `.ed-programas-panel__meta` | `font-size` 15px → 19px; `line-height` 1.4 → 1.28 |
| `.ed-programas-panel__title` | `font-size` clamp(20px→28px) → clamp(26px→38px); `font-weight` 600; `line-height` 1.1 → 0.92; `letter-spacing` 0.04em → 0.07em; `margin` 0 22px → 4px 0 26px |
| `.ed-programas-panel__cta` | `border` 1px → 1.5px; `padding` 12px 24px → 15px 30px; `font-size` 12px → 13px; `letter-spacing` 0.14em → 0.16em |
| **NEW** `.ed-programas-cierre` | White section container |
| **NEW** `.ed-programas-cierre__in` | 3-col grid `1fr auto 1fr`, `gap: 48px`, `padding: 104px 50px` |
| **NEW** `.ed-programas-cierre__h2` | Spectral 600, clamp(26px→46px), uppercase, olive |
| **NEW** `.ed-programas-cierre__img` | 210×270px portrait, `object-position: 50% 28%` |
| **NEW** `.ed-programas-cierre__cta` | Flex container, left-aligned |
| Responsive `≤900px` | Hero: 1-col, reduced padding; band: single-col padding; panels: 1-col; cierre: stacked 1-col |
| Responsive `≤480px` | Hero copy: min padding; panels: 440px min-height; cierre: reduced padding |

CSS version: `programas.html` stays at `editorial.css?v=3`. All other 8 pages remain at `?v=2`.

---

## 5. HTML changes (programas.html)

| Section | Change |
|---|---|
| Hero | Removed `ed-programas-hero__sub` paragraph; changed two CTAs → single `ed-btn--outline-dark` "Agendar conversación" |
| Band | Heading: "Cuatro caminos..." → "Dos caminos para un mismo método"; lead text updated |
| Panels | Removed Sesiones Individuales panel; removed Conecta panel; updated Foco + Intensivo meta to `<br>` line breaks; changed CTA from "Conocer Foco / Intensivo →" → "Conocer más →" |
| `aria-label` on `ed-programas-grid` | "Los cuatro programas" → "Los dos programas ALMAVIVA" |
| Decision helper | Simplified from 5 items to 3 items (Foco / Intensivo / Conversación inicial) |
| Comparison table | **Removed** entirely |
| FAQ | **Removed** entirely |
| Cierre section | **Added** — 3-col editorial closing with portrait image (`programas-sesiones-800`) and "Conozcámonos →" CTA |
| Therapy note | Preserved — kept as protective disclaimer |
| CTA strip | Kept; headline "¿Por dónde empezamos?"; CTA "Agendar conversación" (removed "inicial") |

---

## 6. Validation results

| Check | Result |
|---|---|
| Nav labels: Inicio / Programas / Sesiones individuales / Sobre mí / Reservar | ✓ PASS |
| CSS version: programas.html at `?v=3`, other 8 pages at `?v=2` | ✓ PASS |
| Forbidden terms scan | ✓ PASS (false positive: "mé**todo**" in band headline matched `TODO` case-insensitively — benign Spanish word) |
| Inline `style=""` check | ✓ PASS — zero |
| `<style>` block check | ✓ PASS — none |
| External fonts / third-party scripts | ✓ PASS — none |
| `support.js` / `analytics` / tracking | ✓ PASS — none |
| `noindex` in `privacidad.html` | ✓ PASS — preserved |
| Build script (`build-pages.sh`) | ✓ PASS — 9 pages |
| Hero margin-top (nav clearance) | ✓ PASS — computed `63px`; hero section at y=63.7px |
| Hero title: Mulish 400 | ✓ PASS — computed `Mulish, system-ui, sans-serif`, weight `400` |
| Band colour `#B7C9CD` | ✓ PASS — computed `rgb(183, 201, 205)` |
| Band headline: Mulish, centred, ~66px at 1280px viewport | ✓ PASS |
| Panel alignment: centred | ✓ PASS — `justify-content: center`, `align-items: center`, `text-align: center` |
| Cierre 3-col grid | ✓ PASS — computed `417px 210px 417px` at 1264px viewport |
| 2 panels only (Foco + Intensivo) | ✓ PASS — Sesiones and Conecta panels absent from DOM |
| No comparison table, no FAQ | ✓ PASS — absent from DOM |

---

## 7. Page structure (corrected)

| Section | Class | Background | Notes |
|---|---|---|---|
| Nav | `site-nav` | Cream | Unchanged |
| Hero | `ed-programas-hero` | White + border-top | Mulish H1, single CTA, image below nav |
| Band | `ed-sec--haze` | `#B7C9CD` Salvia | "Dos caminos para un mismo método" |
| Panels | `ed-programas-grid` | Cream3 (gap) | Foco + Intensivo only, centred text |
| Decision helper | `ed-sec--cream ed-tex` | Cream | 3 items |
| Cierre | `ed-programas-cierre` | White | 3-col editorial: H2 + portrait + CTA |
| Therapy note | `ed-sec--cream ed-tex` | Cream | Preserved disclaimer |
| CTA strip | `ed-cta-strip ed-sec--olive` | Olive | Unchanged pattern |
| Footer | `ed-footer` | Olive2 | Unchanged |

---

## 8. Remaining open items (unchanged from AV-015)

| Item | Status |
|---|---|
| `privacidad.html` legal review | Blocked — `noindex` must remain until Ana + legal approve |
| Custom domain connection | Blocked — pending legal review |
| Custom domain URL switch | When `anacarolinas.com` connects, update canonical/OG/JSON-LD/sitemap/robots |
| Conecta dedicated photo | Optional — `home-cursos-*` reused on `conecta.html`; Conecta page itself is now off the Programas listing |
| Therapy note in programas | Optional — Ana may want to remove it; kept for now as protective text |
| Nav "Sobre Ana" vs "Sobre mí" | Design spec said "Sobre Ana"; production uses "Sobre mí" site-wide — flag for Ana's decision |
