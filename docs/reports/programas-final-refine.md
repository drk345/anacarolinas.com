# AV-PROMPT-015D — Programas Final Refinement

Implemented: `fix/programas-final-refine` · 25 June 2026
Rollback tag: `pre-programas-final-refine-2026-06-25`
Based on: AV-PROMPT-015D textual spec (8 targeted fixes before Ana's review)

---

## 1. Summary

**What changed:**
- Blue "Dos caminos" band reduced (~25–30% smaller: smaller padding, smaller H2, tighter lead margin)
- Hero support sentence added between H1 and CTA
- Card clarity sentences added inside Foco and Intensivo panels
- Card CTA labels updated: "Conocer más" → "Conocer Foco" / "Conocer Intensivo"
- "¿Lista para iniciar tu proceso?" cierre section removed
- Distinction bridge section added (cream2 background, Spectral italic quote + quiet note)
- CTA strip: sub text updated ("Una conversación inicial…"); button unified to "Agendar conversación inicial"
- Therapy disclaimer kept, not softened (already non-boxed via `ed-therapy`)
- CSS version bumped: v=4 → v=5 on all 9 pages

**What was intentionally not changed:**
- All 8 other HTML pages (no copy or layout changes, only v=5 CSS bump)
- `noindex` in `privacidad.html` — preserved
- Custom domain not connected, DNS/Cloudflare settings unchanged
- No analytics, tracking, inline styles, or external resources added
- CSP not weakened — zero `style=""` attributes, zero `<style>` blocks

---

## 2. Fix-by-fix detail

### Fix 1 — Blue band reduced

| Property | Before | After |
|---|---|---|
| `.ed-programas-band` padding | `18px 24px 72px` | `10px 24px 36px` |
| `.ed-programas-band__h2` font-size | `clamp(24px, 4.8vw, 72px)` | `clamp(20px, 3.6vw, 52px)` |
| `.ed-programas-band__lead` margin | `80px 0 0 40px` | `20px 0 0 40px` |
| `.ed-programas-band__lead` font-size | `18px` | `16px` |
| `@media ≤900px` band padding | `16px 20px 56px` | `10px 20px 28px` |
| `@media ≤900px` lead margin | `40px 0 0 0` | `16px 0 0 0` |

Result: band feels like a brief bridge between hero and panels, not a dominant section block.

### Fix 2 — Card clarity sentences added

Foco panel (after `ed-programas-panel__title`, before CTA):
```html
<p class="ed-programas-panel__desc">Para trabajar un tema concreto con claridad, estructura y acompañamiento cercano.</p>
```

Intensivo panel (same position):
```html
<p class="ed-programas-panel__desc">Para recorrer un proceso más profundo e integrar el método completo.</p>
```

New CSS class:
```css
.ed-programas-panel__desc {
  font-size: 14px;
  line-height: 1.58;
  color: rgba(255,255,255,.82);
  max-width: 22ch;
  margin: 0 0 20px;
  letter-spacing: 0.01em;
}
```

### Fix 3 — Distinction bridge added

Replaced `ed-programas-cierre` section with:
```html
<section class="ed-programas-bridge ed-tex">
  <div class="ed-sec-body--sm">
    <p class="ed-programas-bridge__text">Ambos caminos comparten la misma base. La diferencia está en la profundidad, el ritmo y el momento en el que estás.</p>
    <p class="ed-programas-bridge__note">Si buscas un primer espacio más puntual o una experiencia grupal, también puedes explorar <a href="sesiones-individuales.html">Sesiones individuales</a> o <a href="conecta.html">Conecta</a>.</p>
  </div>
</section>
```

New CSS:
```css
.ed-programas-bridge { background: var(--cream2) }
.ed-programas-bridge__text {
  font-family: 'Spectral', Georgia, serif;
  font-style: italic;
  font-size: clamp(16px, 2vw, 20px);
  line-height: 1.65;
  color: var(--olive2);
  text-align: center;
  max-width: 52ch;
  margin: 0 auto;
  padding: 52px 40px 24px;
}
.ed-programas-bridge__note {
  font-size: 14px;
  line-height: 1.62;
  color: rgba(35,39,30,.55);
  text-align: center;
  max-width: 52ch;
  margin: 0 auto;
  padding: 0 40px 44px;
}
.ed-programas-bridge__note a { color: var(--accent) }
```

### Fix 4 — "¿Lista para iniciar?" cierre removed

Entire `ed-programas-cierre` section (3-col grid with portrait image and "Conozcámonos →" button) removed from HTML. `.ed-programas-cierre` CSS rules retained in stylesheet for rollback safety but are no longer referenced in HTML.

### Fix 5 — CTA labels unified

Hero CTA: already correct ("Agendar conversación inicial") from 015C — no change needed.
Card CTAs: "Conocer más →" → "Conocer Foco →" (Foco panel), "Conocer Intensivo →" (Intensivo panel).
CTA strip button: "Agendar conversación →" → "Agendar conversación inicial →".

### Fix 6 — Hero support sentence

Added between H1 and actions div:
```html
<p class="ed-programas-hero__sub">Dos procesos diseñados para acompañarte según el momento en el que estás: uno más enfocado, otro más profundo.</p>
```

New CSS:
```css
.ed-programas-hero__sub {
  font-size: 17px;
  line-height: 1.65;
  color: var(--ink);
  opacity: 0.75;
  margin-top: 22px;
  max-width: 38ch;
}
```

`margin-top` on `.ed-programas-hero__actions` reduced from 54px → 40px to compensate for the new sub paragraph spacing.

### Fix 7 — CTA strip improved

Sub text: "Una conversación de unos minutos…" → "Una conversación inicial de unos minutos es suficiente para encontrar el camino."
Button: "Agendar conversación →" → "Agendar conversación inicial →"

### Fix 8 — Therapy disclaimer

Kept unchanged. The `.ed-therapy` class already renders without a heavy box — the cream background section with subtle text is not aggressive. No softening needed.

---

## 3. CSS version bump

All 9 pages bumped from `editorial.css?v=4` → `?v=5`:
`index.html`, `programas.html`, `sesiones-individuales.html`, `conecta.html`, `foco.html`, `intensivo.html`, `sobre-ana.html`, `contacto.html`, `privacidad.html`.

---

## 4. Page structure (after 015D)

| Section | Class | Background | Notes |
|---|---|---|---|
| Nav | `site-nav` | Cream | Unchanged |
| Hero | `ed-programas-hero` | White | H1 + sub sentence + "Agendar conversación inicial" |
| Band | `ed-sec--haze` | `#B7C9CD` Salvia | Reduced size; bridge feel |
| Panels | `ed-programas-grid` | Cream3 (gap) | Foco + Intensivo; card descs; updated CTAs |
| Bridge | `ed-programas-bridge` | Cream2 | Spectral italic quote + quiet note |
| Therapy | `ed-sec--cream ed-tex` | Cream | Kept, unchanged |
| CTA strip | `ed-cta-strip ed-sec--olive` | Olive | Updated sub + button |
| Footer | `ed-footer` | Olive2 | Unchanged |

---

## 5. Validation results

| Check | Result |
|---|---|
| Build `bash scripts/build-pages.sh` | ✓ PASS — 9 pages, no leakage |
| Nav label scan | ✓ CLEAN — no truncated or wrong labels |
| `Lista para iniciar` / `Conozcámonos` absent | ✓ CONFIRMED |
| Both CTAs: "Agendar conversación inicial" | ✓ CONFIRMED |
| Card CTAs: "Conocer Foco" / "Conocer Intensivo" | ✓ CONFIRMED |
| Bridge text present | ✓ CONFIRMED |
| `.ed-programas-cierre` absent from DOM | ✓ CONFIRMED |
| `hasDesc: 2` (both card descs present) | ✓ CONFIRMED |
| CSP / inline style / external script scan | ✓ CLEAN |
| Forbidden terms scan | ✓ CLEAN |
| Internal note / artifact scan | ✓ CLEAN (privacidad.html "pendiente" is intentional legal note) |
| CSS version uniformity — all 9 pages `?v=5` | ✓ CONFIRMED |
| `noindex` in `privacidad.html` | ✓ PRESERVED |
| `privacidad.html` absent from sitemap | ✓ CONFIRMED |

### DOM QA (live preview)

| Property | Expected | Confirmed |
|---|---|---|
| `hasBridge` | true | ✓ true |
| `hasCierre` | false | ✓ false |
| `hasHeroSub` | true | ✓ true |
| `hasDesc` | 2 | ✓ 2 |
| `heroCta` | "Agendar conversación inicial →" | ✓ |
| `stripCta` | "Agendar conversación inicial →" | ✓ |
| `bandH2size` | < 72px (reduced) | ✓ 46px at viewport |
| Bridge text | "Ambos caminos comparten..." | ✓ |
| Total sections | 6 (not 7 — cierre gone) | ✓ 6 |

---

## 6. Remaining open items

| Item | Status |
|---|---|
| `privacidad.html` legal review | Blocked — `noindex` must remain until Ana + legal approve |
| Custom domain connection | Blocked — pending legal review |
| Custom domain URL switch | When `anacarolinas.com` connects: update canonical/OG/sitemap/robots on all pages |
| Ana's visual review of programas.html | Ready for Ana to review at Pages URL |
| Therapy note in programas | Optional — Ana may want to remove if she finds it breaks the editorial flow |
