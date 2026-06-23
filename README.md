# Ana Carolina S — ALMAVIVA Neurotraining

Production static site (single page, Spanish). Converted from a Claude Design
export into clean, dependency-free HTML/CSS/JS.

## Structure

```
index.html              The page — hand-maintained, semantic HTML (no inline styles)
favicon.svg             Favicon ("A" monogram + accent dot)
robots.txt, sitemap.xml SEO
_headers                Cloudflare Pages caching + security headers (HSTS, CSP)
assets/
  css/styles.css        @font-face + all site styles (section-scoped classes, media queries)
  js/main.js            Floating nav on scroll + hamburger menu
  fonts/*.woff2         Self-hosted Mulish 400 + Spectral 400/500/600 (Latin + Latin-ext)
  img/*.{webp,jpg}      Responsive images (800w / 1200w), WebP + JPEG fallback; og-card.jpg (1200×630 share card)
tools/                  Source scripts for one-time asset generation — NOT part of the served site
  extract.js            Extracts fonts + optimizes images from the original bundle
  og-card.js            Generates the 1200×630 Open Graph share card
  build.js              ORIGINAL de-bundler (superseded — do not re-run)
  site.css              Source of the hand-authored CSS (concat with fonts → styles.css)
  source-bundle.html    The original Claude Design bundle (gitignored; kept for reference)
```

## Editing the site

`index.html` and `assets/css/styles.css` are the **canonical, hand-maintained
source** — edit them directly. `tools/build.js` is superseded and kept only for
reference; **do not re-run it**, as it would overwrite the hand-authored files.

### Font note

Only `mulish-400` woff2 files are self-hosted. CSS uses `font-weight: 500–800`
throughout, so browsers apply synthetic bold via `font-synthesis` (on by default).
Visual quality is acceptable for a sans-serif like Mulish. To eliminate synthesis,
add the missing woff2 files from Google Fonts and restore the corresponding
`@font-face` blocks in `assets/css/styles.css` and `tools/fonts.generated.css`.

### Regenerating assets (fonts / images / share card)

```bash
cd tools
npm install            # installs sharp
node extract.js        # fonts -> assets/fonts, optimized photos -> assets/img
node og-card.js        # regenerates assets/img/og-card.jpg
# styles.css = fonts + hand CSS:
cat fonts.generated.css site.css > ../assets/css/styles.css
```

## Local preview

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Deploy (Cloudflare Pages)

### Git integration (planned)

Connect this repo with:
- Build command: *(none)*
- Build output directory: `/`

**Note:** only specific files within `tools/` are gitignored (`node_modules/`,
`source-bundle.html`, `*.generated.css`). The build scripts themselves are
committed and will be included in a Git-based deploy. They are static JS files
and serve no function on production, but they are harmless. For a clean deploy
that excludes `tools/` and `.claude/`, use the Wrangler CLI instead:

```bash
npx wrangler pages deploy . \
  --project-name=anacarolinas \
  --exclude=tools \
  --exclude=.claude \
  --exclude=README.md
```

### Staged rollout rule

Do **not** point `anacarolinas.com` DNS to Cloudflare until the site is verified
on the `*.pages.dev` staging URL.

## Performance targets

| Asset | Target | Notes |
|-------|--------|-------|
| `assets/js/main.js` | < 10 KB | No framework or library dependencies |
| `assets/css/styles.css` | < 50 KB | Self-hosted fonts declared via @font-face |
| Hero image | Served from cache | WebP with JPEG fallback; explicit width/height on `<img>` |
| External scripts | 0 | No analytics, tag managers, or CDN fonts |
| Font 404s | 0 | Only declare @font-face for files that exist in assets/fonts |

## Content architecture debt (TODO)

- **Program cards** link to Google Drive PDFs. These should become first-party
  pages on anacarolinas.com when content is ready — improves trust, SEO, and
  conversion tracking.
- **"Mi historia" CTA** (Sobre mí section) also links to a Google Drive file.
- **Testimonials** section was removed pending real client testimonials. Re-add
  when content is available.
- **Hero photo** is 373 px wide at source — will appear soft on desktop/retina.
  Replace `assets/img/hero-*` with a higher-resolution image from Ana.
- **Privacy policy + cookie banner**: deferred — no analytics are active yet.
  Required before adding any tracking.
