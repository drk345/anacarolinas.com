# ALMAVIVA Production Conversion Master Standard

*Site-wide conversion standard — Foco is only the pilot.*

This is the named, site-wide standard every Claude Design bundled-export page must
follow when converted to production. It was established and proven on the
`foco.html` pilot (committed on top of checkpoint `9e62a7c`, forensic verification:
PASS — 32/32 geometry metrics identical across 1920/1366/390/375, visible-text
SHA-identical, no-JS render hash-identical).

## Applies to

- `foco.html` (pilot — done)
- `intensivo.html`
- `sesiones-individuales.html`
- `sobre-ana.html`
- `contacto.html` / final shell consistency where relevant

## The standard (summary)

1. Preserve the approved visual output exactly — verified by `getBoundingClientRect`
   comparison against the pre-conversion baseline at 1920/1366/390/375, never by
   screenshots alone.
2. Remove 100% of the Claude Design runtime: bundler wrapper/manifest/template,
   unpacking scripts, React/CDN fetches, base64 blobs, Google Fonts references.
3. Clean semantic HTML5: `lang="es"`, one `h1`, `<main>`/`<footer>` landmarks,
   accessible nav (`aria-expanded` hamburger), real `<img>` with alt + dimensions.
4. Self-hosted assets only: fonts byte-deduped against `assets/fonts/`, images
   extracted to `assets/img/<page>/`, shared `assets/js/main.js` for the nav.
5. Page CSS extracted verbatim into `assets/css/<page>.css` (export class names are
   generic — do not merge into `editorial.css` without a collision audit); only
   provably-dead rules may be removed, each asserted unreferenced first.
6. Full SEO head per page: title, meta description, canonical, OG/Twitter set.
7. Link integrity: zero `href="#"`, zero `href="programas.html"`, zero `<a>` without
   href; all fragment targets verified to exist.
8. Verification gates before commit: content parity (normalized visible-text hash),
   geometry comparison, console/network clean, adversarial multi-lens review.

## Process (proven on the pilot)

backup → 4-viewport baseline measurement → payload extraction → assertion-guarded
rebuild → geometry comparison → content-parity hash → adversarial review → forensic
evidence (screenshots under `docs/verification/<page>-phase-2b/`) → commit per page.

## Standing follow-ups

- On the second conversion (Intensivo): hoist the duplicated `.ed-gnav` header CSS
  block into a shared stylesheet so copies decrease as pages convert.
- `sobre-ana.html` converts last: 5 photos are CSS backgrounds needing extraction
  and an explicit treatment decision (background vs `<img>`/alt).
