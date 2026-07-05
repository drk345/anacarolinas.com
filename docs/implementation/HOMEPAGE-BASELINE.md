# Homepage Baseline

Status: **APPROVED** — `index.html` is the approved production landing page.

## Provenance

1. **Original visual baseline**: the verbatim Claude Design HTML export at
   `docs/design/ana-approved-home-reference.html`. `index.html` was copied
   byte-for-byte from this file and confirmed identical (`cmp`) before any
   further work — that copy was the approved visual source of truth.
2. **Current version**: a cleaned static implementation of that same
   baseline — same layout, copy, section order, spacing, colors,
   typography, cards, images, dividers, footer, and rhythm — with the
   Claude Design bundler wrapper, unpacking runtime, embedded
   React/Babel-style logic, and base64/blob assets removed and replaced
   with plain static HTML, external CSS, and real image/font files.

Visual fidelity between the two was verified by direct geometry and
computed-style comparison across ~38 elements spanning every section, at
matching viewports, plus manual mobile/console/network checks.

## Do not redesign without explicit approval

`index.html` is frozen at this visual baseline. Do not change layout,
copy, section order, spacing, colors, typography, image treatment, or
rhythm without explicit approval. Implementation-only changes (further
cleanup, performance, accessibility fixes) that preserve the exact visual
output are fine; visual/content changes are not.

## Reusable classes for future subpages

The homepage CSS lives in `assets/css/editorial.css`, scoped under
`body.ed-home-exact` so its generic class names can't leak into other
pages sharing the stylesheet. A future subpage can reuse the same
components by applying the `ed-home-exact` wrapper class:

- **Header/nav** — `.nav`, `.navin`, `.navlink`, `.brandlink`, `.hamb`
- **Footer** — `.sec-footer`, `.footer-brand`, `.footer-links`, `.footer-link`
- **Buttons** — `.btn`, `.btn-dark`, `.btn-ghost`
- **Cards** — `.fcard`, `.pcard`, `.ccard`
- **Image frames** — `.capimg` (rounded/capsule), `.softimg` (soft rounded)
- **Typography** — `.h1`, `.h2`, `.h3`, `.lead`, `.small`, `.ital`, `.quote`, `.lab`
- **Section rhythm** — `.shell` (1120px content container), `.nodedot` / `.node` (dividers)

## Known baseline carry-overs

These are intentional, literal carry-overs from the approved visual
baseline, not oversights:

- **Programas has 2 cards** (Foco, Intensivo) because the approved visual
  baseline has 2 cards. The site's real offer architecture has a 3rd
  program (Conecta) — see `docs/reference/ALMAVIVA-MASTER-REFERENCE.md` —
  but adding it would be a content/layout change to the frozen baseline,
  so it was not added here without explicit approval.
- **"Saber más sobre mí"** still points to the baseline's external Google
  Drive link (`https://drive.google.com/file/d/1MJGT5_Mex9XDEjgS4zZ-u4hQHZhevofW/view`)
  rather than the site's internal `sobre-ana.html` page, because that's
  what the approved baseline contains.

## Files that make up this conversion

- `index.html`
- `assets/css/editorial.css` (homepage section)
- `assets/img/home/hero.jpg`, `quees.jpg`, `banner.jpg`, `sesiones.jpg`, `sobre.jpg`
- `assets/fonts/cormorant-garamond-400-normal-latin.woff2`
- `assets/fonts/cormorant-garamond-400-italic-latin.woff2`
- `backups/index-before-production-conversion.html` (the verbatim baseline, kept for reference/rollback)
