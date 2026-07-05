# ALMAVIVA Production Conversion Master Standard — v1.2

*Site-wide conversion standard — Foco proved the method, the rest of the site must follow.*

This is the named, site-wide standard every Claude Design bundled-export page must
follow when converted to production. It was established and proven on the
`foco.html` pilot (checkpoint `9e62a7c`, pilot committed as `110c9d4`, forensic
verification: PASS — 32/32 geometry metrics identical across 1920/1366/390/375,
visible-text SHA-identical, no-JS render hash-identical).

## Conversion order and approval gates

Work page by page; stop at every approval gate; commit only after approval.
Never start a page before the previous one is verified, approved, and committed.

1. `foco.html` — pilot, **committed (110c9d4)**
2. `intensivo.html` — **committed (57c78bc)**; introduced the shared `site-shell.css` header
3. `sesiones-individuales.html` — **committed (84d3b54)**; source of the v1.2 lessons below
4. `sobre-ana.html` — high-risk (large embedded biography photos as CSS backgrounds)
5. `contacto.html` + global shell/header/footer consistency pass
6. Final site-wide QA (all public pages)

## The standard (summary)

1. Preserve the approved visual output exactly — verified by `getBoundingClientRect`
   comparison against the pre-conversion baseline at 1920/1366/390/375, never by
   screenshots alone.
2. Remove 100% of the Claude Design runtime: bundler wrapper/manifest/template,
   unpacking scripts, React/CDN fetches, base64 blobs, Google Fonts references.
3. **Runtime side-effect review (v1.2):** before discarding bundled runtime/component
   code, inspect it for rendered side effects beyond simple bindings. Look for
   injected DOM, decorative ornaments, event-state defaults, image sizing logic,
   conditionals, or layout-affecting scripts. If runtime output exists, reproduce
   the resolved end-state statically and verify it against the live baseline.
4. Clean semantic HTML5: `lang="es"`, one `h1`, `<main>`/`<footer>` landmarks,
   accessible nav (`aria-expanded` hamburger), real `<img>` with alt + dimensions.
5. Self-hosted assets only: fonts byte-deduped against `assets/fonts/`, images
   extracted to `assets/img/<page>/`, shared `assets/js/main.js` for the nav.
6. Page CSS extracted verbatim into `assets/css/<page>.css` (export class names are
   generic — do not merge into `editorial.css` without a collision audit); only
   provably-dead rules may be removed, each asserted unreferenced first. The shared
   `.ed-gnav` header comes from `assets/css/site-shell.css` (do not fork it).
7. Full SEO head per page: title, meta description, canonical, OG/Twitter set.
8. Link integrity: zero `href="#"`, zero `href="programas.html"`, zero `<a>` without
   href; all fragment targets verified to exist.
9. Verification gates before commit: content parity (normalized visible-text hash),
   geometry comparison, **full-page pixel-diff (v1.2)**, console/network clean,
   adversarial multi-lens review.
10. **Full-page pixel-diff gate (v1.2):** add full-page screenshot pixel-diffing after
    geometry checks. Geometry parity is required but not sufficient. Pixel-diffing
    should be used to detect subtle differences in font weight, missing decorative
    elements, image resampling, or render-only changes that do not affect element
    rectangles. Any non-zero diff must be localized and explained. (Viewport-height
    screenshots are not enough — below-the-fold regions must be covered.)

## Process (proven on the pilot, hardened on Sesiones)

backup → 4-viewport baseline measurement → payload extraction → **runtime
side-effect review** → assertion-guarded rebuild → geometry comparison →
content-parity hash → **full-page pixel-diff** → adversarial review → forensic
evidence (screenshots under `docs/verification/<page>-phase-2b/`) → commit per page.

## Conversion lessons (version history)

- **v1.2 (from Sesiones Individuales, commit 84d3b54):** Sesiones Individuales proved
  why these gates are necessary: runtime-injected thread ornaments (the DCLogic
  `addThread()` side effect) were invisible to DOM geometry checks — absolutely
  positioned, thin, and translucent — and a Lato 300 vs 400 font mismatch was found
  only through full-page pixel-diffing. Both were fixed and verified pixel-identical
  before commit.
- **v1.1 (from Intensivo, commit 57c78bc):** shared header CSS belongs in
  `site-shell.css`; runtime accordions/bindings (`sc-if`, moustache, DCLogic state)
  must be resolved to their live-verified end-state, with interactive behavior ported
  to minimal vanilla JS only where the baseline had it.
- **v1.0 (from the Foco pilot, commit 110c9d4):** the base recipe — extraction,
  assertion-guarded rebuild, geometry/parity/no-JS gates, adversarial review.

## Standing follow-ups

- `sobre-ana.html` converts last among the program/about pages: 5 photos are CSS
  backgrounds needing extraction and an explicit treatment decision (background vs
  `<img>`/alt); audit its runtime for side effects per the v1.2 rule before removal.
- `foco.css` still carries its own copy of the `.ed-gnav` block (pre-site-shell);
  migrate it to `site-shell.css` in a future approved shell-consistency pass.
- Dead-CSS pruning of the verbatim page stylesheets (journey/unused-section rules on
  Sesiones, ~30% of that file) is deferred to a future approved cleanup pass.
