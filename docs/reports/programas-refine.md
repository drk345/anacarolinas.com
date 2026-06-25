# AV-PROMPT-015C — Programas Refine

Implemented: `fix/programas-refine` · 25 June 2026
Rollback tag: `pre-programas-refine-2026-06-25`
Based on: Ana's textual direction (AV-PROMPT-015C); screenshots referenced but not visible in session

---

## 1. Summary

**What changed:**
- Hero H1 font switched from Mulish 400 → Spectral 600 (matches site-wide typography)
- Band headline switched from Mulish 400 → Spectral 600 (same reason)
- Hero image `object-position` changed from `50% 30%` → `50% 15%` (shows more of Ana's head/hair)
- Decision helper section ("¿Cuál es para ti?") removed entirely
- Hero CTA changed from "Agendar conversación" → "Agendar conversación inicial"
- CSS version bumped from mixed v=2/v=3 → v=4 consistently across all 9 pages

**What was removed:**
- `ed-decision` section (the three-item Foco / Intensivo / Conversación initial chooser)

**CSS version change:** v=2 (8 pages) and v=3 (programas) → v=4 on all 9 pages.

**What was not changed:**
- Page structure: hero → band → 2 panels → cierre → therapy note → CTA strip
- Foco + Intensivo panels (kept, unchanged)
- No other pages modified beyond CSS version bump
- noindex in privacidad.html preserved
- Custom domain not connected or changed

---

## 2. Main fixes

| Issue | Fix | Status |
|---|---|---|
| Hero H1: Mulish 400 (display font, differs from site) | Changed to Spectral 600 to match all other page headings | ✓ Done |
| Band headline: Mulish 400 giant display text | Changed to Spectral 600 — consistent with site's serif heading system | ✓ Done |
| Hero image crop: `50% 30%` cuts Ana's hair too tight | Changed to `50% 15%` — anchors image 15% from top, showing more head/hair | ✓ Done |
| Decision helper section ("¿Cuál es para ti?") | Removed entirely | ✓ Done |
| Hero CTA inconsistency | Changed to "Agendar conversación inicial" (preferred site phrasing) | ✓ Done |
| CSS version inconsistency (v=3 programas, v=2 others) | Bumped all 9 pages to v=4 | ✓ Done |

---

## 3. Typography detail

**Before (AV-PROMPT-015B):**
```css
.ed-programas-hero__title {
  font-family: 'Mulish', system-ui, sans-serif;
  font-weight: 400;
  font-size: clamp(30px, 4.8vw, 56px);
  line-height: 1.28;
  letter-spacing: 0.01em;
  color: var(--ink);
}
.ed-programas-band__h2 {
  font-family: 'Mulish', system-ui, sans-serif;
  font-weight: 400;
  font-size: clamp(26px, 5.2vw, 88px);
}
```

**After (AV-PROMPT-015C):**
```css
.ed-programas-hero__title {
  font-family: 'Spectral', Georgia, serif;
  font-weight: 600;
  font-size: clamp(28px, 4.5vw, 54px);
  line-height: 1.1;
  letter-spacing: 0.03em;
  color: var(--olive);
}
.ed-programas-band__h2 {
  font-family: 'Spectral', Georgia, serif;
  font-weight: 600;
  font-size: clamp(24px, 4.8vw, 72px);
  letter-spacing: 0.03em;
}
```

The Spectral 600 is already preloaded on the page (`spectral-600-normal-latin.woff2`). No new font assets required.

---

## 4. Hero image crop fix

**Before:** `object-position: 50% 30%`
At a typical 1264px viewport with the hero media column ~644px wide × 620px tall:
- Image (1200×1600 scaled to cover): effectively 858px tall displayed in 620px
- With 30% anchor: 71px hidden above the top of the container → first 133px of original image cropped

**After:** `object-position: 50% 15%`
- With 15% anchor: only 36px hidden above → first 67px of original image cropped
- Result: approximately 66px more of the portrait top is visible — showing more of Ana's head/hair
- No source image re-processing required (the Sharp-generated files contain the full portrait at correct proportions)

---

## 5. Validation

### Build
`bash scripts/build-pages.sh` → ✓ PASS — 9 pages, no leakage

### Nav regression scan
`grep -RniE 'Sesiones 1:1|Sob</a>|Sobr|Sob '` → ✓ CLEAN (all hits are "Sobre mí" — correct label)

### Programas content scan
- `ALMAVIVA Foco` present ✓
- `ALMAVIVA Intensivo` present ✓
- `¿Cuál es para ti?` / `ed-decision` absent ✓
- `Sesiones individuales` appears only in nav (not as a programme card) ✓
- `ALMAVIVA Conecta` absent ✓

### CSP/artifact scan
`grep -RniE 'style=|<style|fonts\.googleapis|support\.js'` → ✓ CLEAN

### CSS version uniformity
All 9 pages: `editorial.css?v=4` ✓

### Forbidden terms
✓ CLEAN

### Privacy noindex
`<meta name="robots" content="noindex">` in privacidad.html ✓

### Visual QA (preview inspection at 1264px viewport)
| Check | Result |
|---|---|
| Hero H1 font: `Spectral, Georgia, serif` weight 600 | ✓ Confirmed |
| Hero H1 size: 54px at viewport | ✓ Confirmed |
| Hero H1 color: `rgb(58, 68, 41)` = `var(--olive)` | ✓ Confirmed |
| Image `object-position: 50% 15%` | ✓ Confirmed |
| Image starts at y=63.7px (below nav) | ✓ Confirmed |
| Band heading: Spectral 600, ~61px | ✓ Confirmed |
| Decision helper `.ed-decision` element: absent | ✓ Confirmed |
| CTA text: "Agendar conversación inicial →" | ✓ Confirmed |
| Total sections: 6 (hero, band, panels, cierre, therapy, CTA) | ✓ Confirmed |
| No console errors | ✓ Confirmed |

---

## 6. Remaining Ana decisions

| Topic | Options | Recommendation |
|---|---|---|
| Hero CTA wording | "Agendar conversación inicial" (current) vs "Agendar conversación" | Current is consistent with site; Ana can shorten if preferred |
| Band section | Currently kept ("Dos caminos para un mismo método" in Spectral on Salvia bg) | Remove if Ana's screenshot doesn't include it |
| Therapy note | Currently kept as protective disclaimer below cierre | Ana may remove once she reviews |
| "¿Lista para iniciar tu proceso?" copy | "Lista" (feminine) matches Ana's design | Confirm this wording is intended |
| Screenshots | Screenshots were referenced but not visible in this session | Ana should verify visually against her reference |

---

## 7. Note on attached screenshots

The AV-PROMPT-015C prompt referenced two attached screenshots (Ana's design suggestion and the current result). These appeared as `[Image: 1170×2532]` placeholders in the session but the image content was not accessible for visual comparison. Implementation was carried out entirely from the detailed textual specification. Ana should visually verify that the output aligns with her reference screenshot, especially the hero image crop.
