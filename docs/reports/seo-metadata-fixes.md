# AV-PROMPT-012 — SEO & Metadata Fixes

**Date:** 2026-06-25
**Branch:** `fix/seo-metadata`
**Base commit:** `07d3aba` (master)
**Rollback tag:** `pre-seo-metadata-fixes-2026-06-25`

---

## 1. Summary

### What was fixed
- Titles standardised across all 9 pages: brand-first, pipe separator, full name "Ana Carolina Segura", no truncation
- Meta descriptions updated on all 9 pages: claim-free, capability-framed, 90–160 chars
- Canonical URLs updated on all 8 public pages: from `anacarolinas.com` (unconnected) to `https://anacarolinas-com.pages.dev/`
- Open Graph + Twitter card tags added to all 7 inner public pages (previously homepage-only)
- `og:site_name` and `og:image:alt` added to all OG blocks (homepage and inner pages)
- JSON-LD on `index.html` fixed: name → "Ana Carolina Segura", jobTitle softened, URLs updated to Pages URL, "y empresas" removed from service description
- `og:url`, `og:image`, `og:description` on homepage updated to Pages URL and capability-framed language
- `meta name="author"` updated to "Ana Carolina Segura"

### What was intentionally not fixed
- Page body copy not changed (out of scope)
- `privacidad.html` remains `noindex`, body placeholder text unchanged (legal review required)
- No CSS changes (no `?v=N` bump needed)
- Custom domain not connected, DNS not changed, Cloudflare settings not changed
- `og-card.jpg` quality unchanged (P3 — future task)
- Footer link list not expanded (P3 — future task)
- Portrait alt text surnames not changed (P3 — optional)

### Custom domain status
Custom domain `anacarolinas.com` is **not connected**. All technical SEO signals now consistently use `https://anacarolinas-com.pages.dev/`. Sitemap and robots were already using the Pages URL and required no changes.

---

## 2. Metadata changes

| Page | Title updated | Description updated | Canonical updated | OG added/fixed | Notes |
|---|---|---|---|---|---|
| `index.html` | ✓ | ✓ | ✓ | ✓ fixed | Added `og:site_name`, `og:image:alt`; updated URLs; Twitter updated |
| `programas.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new |
| `sesiones-individuales.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new |
| `conecta.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new |
| `foco.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new |
| `intensivo.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new; description shortened (was 183 chars, now 88 chars) |
| `sobre-ana.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new |
| `contacto.html` | ✓ | ✓ | ✓ | ✓ added | OG + Twitter block new; description expanded (was 118 chars, now 92 chars) |
| `privacidad.html` | ✓ | ✓ | n/a | none | Remains `noindex`; no canonical; no OG |

---

## 3. Structured data changes (index.html JSON-LD)

| Field | Before | After |
|---|---|---|
| `Person.name` | `"Ana Carolina S"` | `"Ana Carolina Segura"` |
| `Person.jobTitle` | `"Coach integrativa · neurociencia del bienestar"` | `"Coach integrativa · neuroeducación y bienestar"` |
| `Person.@id` | `https://anacarolinas.com/#ana` | `https://anacarolinas-com.pages.dev/#ana` |
| `Person.url` | `https://anacarolinas.com/` | `https://anacarolinas-com.pages.dev/` |
| `Person.image` | `https://anacarolinas.com/assets/img/sobre-1200.jpg` | `https://anacarolinas-com.pages.dev/assets/img/sobre-1200.jpg` |
| `ProfessionalService.@id` | `https://anacarolinas.com/#almaviva` | `https://anacarolinas-com.pages.dev/#almaviva` |
| `ProfessionalService.url` | `https://anacarolinas.com/` | `https://anacarolinas-com.pages.dev/` |
| `ProfessionalService.image` | `https://anacarolinas.com/assets/img/og-card.jpg` | `https://anacarolinas-com.pages.dev/assets/img/og-card.jpg` |
| `ProfessionalService.description` | `"...coaching para personas y empresas."` | `"Neuroeducación, autoconocimiento, regulación del sistema nervioso y coaching integrativo para el bienestar."` |
| `ProfessionalService.founder.@id` | `https://anacarolinas.com/#ana` | `https://anacarolinas-com.pages.dev/#ana` |

---

## 4. Domain strategy note

**Current state:** All metadata (canonical, og:url, JSON-LD `@id`/`url`/`image`) now consistently uses `https://anacarolinas-com.pages.dev/`. Sitemap and robots were already on the Pages URL — no change needed.

**At custom domain connection, the following must be updated:**
- All `<link rel="canonical">` URLs across 8 public pages
- All `og:url` and `og:image` URLs across all pages
- All JSON-LD `@id`, `url`, `image` values in `index.html`
- `sitemap.xml` `<loc>` entries (8 URLs)
- `robots.txt` `Sitemap:` directive
- `og-card.jpg` URL path in OG and Twitter tags

This is a coordinated find-and-replace from `https://anacarolinas-com.pages.dev/` to `https://anacarolinas.com/`.

---

## 5. Remaining SEO tasks

- **Privacy page (launch blocker):** `privacidad.html` remains `noindex` with placeholder legal text. Requires Ana + legal review before the custom domain is connected. Do not add to sitemap while noindex.
- **OG image quality (P3):** `og-card.jpg` is ~36 KB at 1200×630 — light for the resolution. Regenerate at higher quality (~100–200 KB) before public launch.
- **Custom-domain URL switch:** When `anacarolinas.com` is connected, all canonical/OG/JSON-LD/sitemap/robots URLs must be updated. Recommended as a single coordinated `AV-PROMPT-013` or domain-launch prompt.
- **Ana must confirm social/contact details:** Instagram, LinkedIn, YouTube, email, telephone in JSON-LD should be verified against current Ana-maintained channels.
- **PDF content review:** If any downloadable PDFs are added, they will need their own metadata strategy.
- **Footer link list (P3):** Adding Programas, Sobre mí, Contacto to the footer would marginally improve crawlability and UX.
