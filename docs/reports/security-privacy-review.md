# AV-PROMPT-009 — Security & Privacy Review

**Date:** 2026-06-25
**Auditor:** Claude (automated static analysis)
**Commit audited:** `8ff4862` (master, production)
**Branch:** `audit/security-privacy-review`
**Build command:** `bash scripts/build-pages.sh`
**Build result:** PASS — 9 pages, all assets present, no internal folders leaked

---

## 1. Executive Summary

### Overall launch readiness

**Not ready for custom-domain public launch** — one P0 blocker (privacy page).
**Ready for continued private review** on `anacarolinas-com.pages.dev`.

### Top 5 risks

1. **Privacy page is placeholder** — contains `[CONFIRMAR]` legal markers; explicitly states it needs legal drafting before launch. P0 blocker for GDPR compliance.
2. **CSS/JS cache fragility** — `max-age=86400` (24 hours) with manual `?v=N` bumping; stale cache issue already occurred once (AV-PROMPT-006). P1.
3. **Internal HTML comment in production source** — `contacto.html` line 36 contains `<!-- Pending Ana decision: CTA canonical name -->`, visible to anyone who inspects source. P1.
4. **Unused CSS files shipped to `dist/`** — `home.css`, `prototype.css`, `styles.css` are accessible by direct URL at `/assets/css/` but not linked; they expose prototype-era comments. P1.
5. **`areaServed: "ES"` in JSON-LD** — states service is in Spain (`ES`) when Ana is based in Copenhagen, Denmark (`DK`). P2 SEO/accuracy error.

### Should custom domain be connected now?

**No.** The privacy page must be legally finalized first. Everything else is private-review acceptable. Once the P0 is resolved, the custom domain can be connected.

### Are security headers acceptable?

**Yes, strong.** CSP, HSTS, X-Frame, Referrer-Policy, X-Content-Type-Options, Permissions-Policy all present and correctly configured. No `unsafe-inline`, no `unsafe-eval`, no external origins. Fonts and JS are fully self-hosted.

### Is the privacy page launch-ready?

**No.** See P0 finding.

---

## 2. Findings by Priority

### P0 — Blocks custom-domain launch

#### P0-1 — Privacy page contains unresolved legal placeholders

**Finding:** `privacidad.html` contains explicit placeholder markers and is not final legal text.

**Evidence:**
- `privacidad.html:43–46`: A prominent warning block reads *"Esta página requiere redacción legal antes de publicarse"*
- `privacidad.html:55`: `<strong>Nombre o denominación:</strong> Ana Carolina S [CONFIRMAR nombre legal completo]`
- `privacidad.html:58`: `<strong>Jurisdicción:</strong> [CONFIRMAR — Dinamarca / UE]`
- Data sections are explicitly marked as placeholder text pending finalization
- `noindex` meta tag is correctly present, so the page will not be indexed, but it IS accessible

**Why it matters:** Under GDPR (EU Regulation 2016/679), a site collecting personal data (email, phone via contact forms/WhatsApp, coaching client data) must have a valid, accurate, site-specific privacy policy accessible to users before that data is processed. Publishing to a custom public domain without a final privacy page creates legal risk.

**Recommended fix:** Engage a legal professional familiar with EU/Danish GDPR requirements to draft the final text. The current page structure is good scaffolding — the legal drafter has clear sections to fill in.

**Requires Ana/legal input:** Yes — legal name, jurisdiction (DK/EU), exact data flows, retention periods, and rights-exercise procedure must be confirmed.

---

### P1 — Should fix before launch

#### P1-1 — CSS/JS cache TTL is 24 hours with manual version bumping

**Finding:** `_headers` sets `Cache-Control: public, max-age=86400` for `/assets/css/*` and `/assets/js/*`. Version bumping (`?v=N`) must be done manually in every HTML file before each deploy.

**Evidence:** `_headers` lines 18–21. The stale-CSS issue (AV-PROMPT-006) already occurred once because this was not in place, delaying the Sobre Ana visual balance fix from appearing on Cloudflare for up to 24 hours.

**Why it matters:** If any future CSS or JS change is deployed without bumping the query string, users will see a broken site (new HTML + old CSS) for up to 24 hours. This is a high-friction, error-prone workflow.

**Recommended fix:**
- Short term (before launch): Lower TTL to `max-age=3600` (1 hour) so any staleness resolves quickly. One-line change to `_headers`.
- Medium term (post-launch): Implement hash-based cache-busting in the build script (append git short hash to CSS/JS filenames or query strings automatically). This eliminates the manual bumping requirement.

**Requires Ana/legal input:** No. Technical change only.

#### P1-2 — Internal workflow comment in contacto.html production source

**Finding:** `contacto.html:36` contains an HTML comment that exposes internal decision-making to anyone who views source.

**Evidence:**
```html
<!-- Pending Ana decision: CTA canonical name (sesión de exploración / conversación inicial / sesión de descubrimiento) -->
```

**Why it matters:** While not a security vulnerability, comments like this are visible in the page source of the production Cloudflare URL. They signal an unfinished state to any developer or curious user who inspects the HTML. If the custom domain launches publicly, this comment would be public.

**Recommended fix:** Once Ana confirms the final CTA name, remove this comment and update the copy. If the decision is pending, the comment should be removed from the live HTML now — the decision can be tracked elsewhere (e.g., git issue or project notes).

**Requires Ana/legal input:** Yes — Ana needs to confirm the CTA canonical name first.

#### P1-3 — Unused CSS files shipped to dist/

**Finding:** Three CSS files are copied into `dist/assets/css/` by the build script but are not linked by any HTML page:
- `home.css` — labelled "Editorial homepage (prototype)" in its comment header
- `prototype.css` — labelled "Prototype-only styles" with prototype review banner styles
- `styles.css` — origin/purpose unclear from context

**Evidence:** `grep -n 'prototype\.css\|home\.css\|styles\.css' *.html` returned no results. All three files appear in `dist/assets/css/` after build.

**Why it matters:** These files are accessible by anyone who knows or guesses their URL (e.g., `https://anacarolinas-com.pages.dev/assets/css/prototype.css`). Their comments expose that the site was built on a prototype scaffold and may confuse content auditors or SEO tools that crawl the asset directory.

**Recommended fix:** Exclude these files from the build output. In `build-pages.sh`, change `cp -R assets dist/assets` to explicitly copy only the CSS files that are actually used, or add a selective exclude for unused CSS. The production CSS is `editorial.css` only — `main.js` is the only JS used.

**Requires Ana/legal input:** No. Technical change only.

---

### P2 — Recommended improvement

#### P2-1 — `areaServed: "ES"` in JSON-LD is incorrect

**Finding:** The JSON-LD structured data on `index.html:59` states `"areaServed": "ES"` — the ISO code for Spain. Ana is based in Copenhagen, Denmark.

**Evidence:** `index.html:59`: `"areaServed": "ES",`

**Why it matters:** Search engines use `areaServed` to determine geographic relevance. Setting it to `ES` (Spain) instead of `DK` (Denmark) may affect local search performance for Danish or Copenhagen-area searches. Additionally, if Ana serves Spanish-speaking clients internationally, the value should reflect that.

**Recommended fix:** Change to `"areaServed": "DK"` (Denmark), or `["DK", "ES"]` if explicitly serving both Spanish and Danish markets. Requires Ana to confirm her intended service geography.

**Requires Ana/legal input:** Yes — confirm primary service geography.

#### P2-2 — Sitemap contains only 1 of 9 pages

**Finding:** `sitemap.xml` only includes the homepage (`https://anacarolinas.com/`). The remaining 7 public pages are missing.

**Evidence:** `sitemap.xml` contains a single `<url>` entry.

**Why it matters:** A sitemap helps search engines discover all pages. Missing pages may be discovered eventually through internal links, but sitemap inclusion accelerates indexing and signals these pages as intentionally public.

**Pages to add:** `programas.html`, `sesiones-individuales.html`, `conecta.html`, `foco.html`, `intensivo.html`, `sobre-ana.html`, `contacto.html`. Do NOT add `privacidad.html` (noindex).

**Recommended fix:** Update `sitemap.xml` to include all public pages with appropriate priorities (e.g., homepage 1.0, sobre-ana 0.8, programas 0.8, programme detail pages 0.7, contacto 0.6).

**Requires Ana/legal input:** No. Technical change only.

#### P2-3 — Invalid nested `<p>` elements on three pages

**Finding:** Three pages have a `<p class="ed-prose"><p>…</p></p>` pattern — a `<p>` element nested inside another `<p>` element. This is invalid HTML (a `<p>` element cannot contain another `<p>`).

**Evidence:**
- `conecta.html:63`: `<p class="ed-prose"><p>Los temas del programa…</p></p>`
- `contacto.html:77`: `<p class="ed-prose"><p>Si todavía no tienes claro…</p></p>`
- `programas.html:82`: `<p class="ed-prose"><p>La conversación inicial…</p></p>`

Note: the same issue was fixed in `sobre-ana.html` during AV-PROMPT-006 (changed to `<div class="ed-prose"><p>…</p></div>`).

**Why it matters:** Browsers auto-correct this but in unpredictable ways. The `.ed-prose` class styles do not apply to the inner `<p>`. This causes inconsistent text styling vs other prose sections on those pages.

**Recommended fix:** Apply the same fix as `sobre-ana.html` — change `<p class="ed-prose">` to `<div class="ed-prose">` on these three instances, keeping the inner `<p>` intact.

**Requires Ana/legal input:** No. CSS fix only.

#### P2-4 — Social handles, email, and phone require Ana's explicit confirmation

**Finding:** The following contact details are hardcoded across all 9 pages and in JSON-LD structured data:

| Link | Value |
|---|---|
| WhatsApp | `https://wa.me/4522256143` (+45 22 25 61 43) |
| Email | `info@anacarolinas.com` |
| Instagram | `https://www.instagram.com/ana.carolina.coach` |
| LinkedIn | `https://www.linkedin.com/in/anacarolinasegura/` |
| YouTube | `https://www.youtube.com/@AnaCarolinaCoach` |

**Why it matters:** An incorrect handle or email makes the site unprofessional and breaks contact flows. The phone number is also embedded in JSON-LD structured data (indexed by Google), so verifying it is intentional is important.

**Recommended fix:** Ana should verify each of these is active, correct, and intentionally public before custom-domain launch. Especially confirm the phone number in JSON-LD is acceptable — if she prefers not to have it in search result structured data, remove `"telephone"` from the `ProfessionalService` entity.

**Requires Ana/legal input:** Yes.

#### P2-5 — Google Drive PDFs are publicly accessible

**Finding:** Four programme pages link to Google Drive PDFs:
- `conecta.html:148` — `drive.google.com/file/d/1IF9ZR24Hmg1d7HQb4P8SOrjQUVNSKgVJ/view`
- `foco.html:132` — `drive.google.com/file/d/1UTPB_q7-1EoRiAcBWQpGBF_YmEowUmt6/view`
- `intensivo.html:142` — `drive.google.com/file/d/19-Vb-lsN5QCG73Ye1yAjvYJ8wCsS1cSD/view`
- `sesiones-individuales.html:114` — `drive.google.com/file/d/12sw9XAyzyHTompid0yUE44_PhJaockxi/view`

These are "anyone with the link can view" Drive files — intentionally semi-public for download.

**Why it matters:** Drive files with shared links are public. The concern is their content: if any PDF contains prices, outdated claims, personal contact info beyond what's on the site, draft markings, or internal notes, that content is now publicly accessible. Drive URLs are also not stable long-term.

**Recommended fix:** Ana should review each PDF to confirm it contains only content suitable for public download. Consider hosting PDFs as static assets in `dist/assets/` for more control and stability, removing the Google Drive dependency.

**Requires Ana/legal input:** Yes — Ana must review and confirm each PDF's content.

---

### P3 — Optional hardening

#### P3-1 — HSTS `preload` flag not set

**Finding:** `Strict-Transport-Security: max-age=31536000; includeSubDomains` is set, but the `preload` flag is absent.

**Why it matters:** The `preload` flag allows the domain to be submitted to browser HSTS preload lists (hardcoded in Chrome, Firefox, Safari). Without it, HSTS only activates after the first visit. With it, HSTS is enforced from the very first visit by any browser.

**Recommended fix:** If/when the domain is stable and HTTPS-only is permanent, add `preload` and submit `anacarolinas.com` to [hstspreload.org](https://hstspreload.org). This is a one-way action — the domain cannot be easily removed from preload lists, so only do this when confident in permanent HTTPS.

**Requires Ana/legal input:** No. Technical decision — confirm HTTPS is permanent first.

#### P3-2 — OG/Twitter social metadata only on homepage

**Finding:** Only `index.html` has Open Graph (`og:`) and Twitter Card meta tags. Direct links to programme pages (`/programas.html`, `/sesiones-individuales.html`, etc.) shared on social media will not show a rich preview card.

**Recommended fix:** Add page-specific `og:title`, `og:description`, `og:url`, and `og:image` meta tags to at least the key landing pages (programas, sobre-ana, contacto) before launch. Lower priority than the P0/P1 issues.

#### P3-3 — JSON-LD inline `<script>` and CSP

**Finding:** `index.html` contains an inline `<script type="application/ld+json">` block. The CSP `script-src 'self'` directive technically governs all `<script>` elements.

**Assessment:** Modern browsers (Chrome 100+, Firefox, Safari) treat `type="application/ld+json"` as non-executable data and do not block it under `script-src`. Googlebot processes JSON-LD from source regardless of CSP. This is **not a blocking issue in practice** but is worth monitoring if browser CSP behavior changes.

**Recommended fix:** None required now. If a future CSP report-only audit flags this, add a nonce to the JSON-LD script or move structured data to a separate file at `/assets/js/ld-home.js`.

#### P3-4 — Redundant framing protection

**Finding:** Both `X-Frame-Options: SAMEORIGIN` and `frame-ancestors 'self'` in CSP are set. They are redundant.

**Assessment:** Not a vulnerability. CSP `frame-ancestors` takes precedence in modern browsers; `X-Frame-Options` provides fallback for older browsers. Having both is harmless belt-and-suspenders protection.

#### P3-5 — `robots.txt` sitemap URL references custom domain before launch

**Finding:** `robots.txt: Sitemap: https://anacarolinas.com/sitemap.xml` — this URL is currently unresolved since the custom domain is not yet connected.

**Assessment:** Not harmful. Crawlers that find the Pages URL will see this sitemap directive, follow the URL, get a 404 (domain not live), and continue without the sitemap. This resolves automatically when the domain is connected.

#### P3-6 — `og-card.jpg` file size is small (36 KB)

**Finding:** The OG card image is declared as 1200×630 but the file is only 36 KB, suggesting heavy JPEG compression. Some social platforms may render it as low quality.

**Recommended fix:** If social sharing preview quality is important, regenerate `og-card.jpg` at a higher quality setting (aim for 100–200 KB for a 1200×630 image).

---

## 3. Security Header Review

Source: `_headers` (root, copied to `dist/_headers`)

| Header | Value | Assessment |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; form-action 'self'; upgrade-insecure-requests` | Strong. No `unsafe-inline`, no `unsafe-eval`, no external origins. |
| `X-Content-Type-Options` | `nosniff` | Correct. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Good balance — sends origin only to same-origin, origin only (no path) to cross-origin HTTPS. |
| `X-Frame-Options` | `SAMEORIGIN` | Correct. Redundant with CSP `frame-ancestors 'self'` but harmless. |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | Good. Explicitly disables sensitive browser APIs. |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Strong. 1-year TTL. Missing `preload` (P3-1). |
| **Cache — HTML** | *(not set — Cloudflare default)* | Cloudflare Pages defaults to short/no-cache for HTML. Acceptable. |
| **Cache — CSS/JS** | `public, max-age=86400` | **Risk** — 24-hour TTL, manual `?v=N` required (P1-1). |
| **Cache — Images** | `public, max-age=31536000, immutable` | Correct for content-addressed images. |
| **Cache — Fonts** | `public, max-age=31536000, immutable` + `Access-Control-Allow-Origin: *` | Correct. `ACAO: *` needed for cross-origin font loading by WOFF2. |

---

## 4. CSP Review

**Status: Strong. No violations found.**

CSP scan results:
- `style=` attributes: **0 hits** — no inline styles
- `<style` tags: **0 hits** — no embedded stylesheets
- `fonts.googleapis.com` / `fonts.gstatic.com`: **0 hits** — all fonts self-hosted in `assets/fonts/`
- `support.js`, `x-dc`, `DCLogic`, template artifacts (`{{ }}`): **0 hits**

Self-hosted assets:
- Fonts: Mulish (latin, latin-ext) + Spectral (6 weights/styles) — all `.woff2`, served from `assets/fonts/`
- JS: Single `main.js` (975 bytes) — IIFE with nav scroll behavior and hamburger menu only. No external calls, no `fetch()`, no `XMLHttpRequest`.
- CSS: `editorial.css` only (via `?v=2` query string)

The CSP is correctly configured for a zero-dependency static site.

---

## 5. Privacy Review

### Current privacy page status

`privacidad.html` exists with:
- `noindex` meta tag ✓ (will not be indexed)
- Clear warning that legal drafting is pending ✓
- Skeleton sections for: responsible party, data collected, user rights ✓
- Unresolved `[CONFIRMAR]` markers for legal name and jurisdiction ✗ (P0 blocker)

### What the final privacy page must include

Before public launch, the privacy page must cover (Spanish/EU GDPR requirements):

| Topic | Status |
|---|---|
| Data controller (full legal name) | ✗ — `[CONFIRMAR nombre legal completo]` |
| Data controller contact email | ✓ — `info@anacarolinas.com` present |
| Website URL | ✓ |
| Jurisdiction (DK/EU) | ✗ — `[CONFIRMAR — Dinamarca / UE]` |
| What data is collected | Partial — placeholder text only |
| How data is collected (email, WhatsApp, coaching sessions) | Not yet |
| Legal basis for processing (consent, contract, etc.) | Not yet |
| Data retention periods | Not yet |
| User rights (access, rectification, deletion, portability, objection, restriction) | Partial — mentioned but not actionable |
| How to exercise rights | Not yet |
| Where data may be processed (if cloud services, third parties involved) | Not yet |
| Third-party services (Cloudflare, WhatsApp, Gmail, Instagram, LinkedIn, YouTube) | Not yet |
| Cookie/analytics policy | Not yet (currently no cookies — state this explicitly) |
| Date of last update | Not yet |

### Third-party services to mention in the privacy policy

| Service | Relevance |
|---|---|
| **Cloudflare Pages** | Hosting infrastructure; Cloudflare processes traffic and may log IPs |
| **WhatsApp (Meta)** | Primary contact channel; data transferred to Meta |
| **Email provider** (e.g. Gmail / Outlook via `info@anacarolinas.com`) | Incoming contact requests; provider processes email data |
| **Instagram / Meta** | Social link; users redirected to Meta platform |
| **LinkedIn (Microsoft)** | Social link; users redirected to Microsoft platform |
| **YouTube (Google)** | Social link; users redirected to Google platform |
| **Google Drive** | PDF downloads linked from 4 programme pages; Google processes access logs |
| **Google Search Console / Analytics** | If added in the future — must be disclosed before adding |

### Cookie/tracking status

**Current status: No cookies. No analytics. No tracking pixels. No embedded videos.**

No cookie banner is required based on the current implementation. This must be reassessed if analytics (e.g., Plausible, Google Analytics), embedded videos (YouTube embeds), or remarketing pixels are added. Document this fact explicitly in the privacy page.

---

## 6. External Link Review

### All external links found

| Destination | Pages | `rel` correct? | Risk |
|---|---|---|---|
| `https://wa.me/4522256143` | All 9 pages (footer + floating button) | ✓ `noopener noreferrer` | Phone number in HTML source — intentional but confirm with Ana |
| `mailto:info@anacarolinas.com` | index.html, contacto.html | No `rel` needed for mailto ✓ | Confirm email is live and monitored |
| `https://www.instagram.com/ana.carolina.coach` | All 9 pages | ✓ | Confirm handle is correct/active |
| `https://www.linkedin.com/in/anacarolinasegura/` | All 9 pages | ✓ | Confirm profile is correct/active |
| `https://www.youtube.com/@AnaCarolinaCoach` | All 9 pages | ✓ | Confirm handle is correct/active |
| `https://drive.google.com/...` (4 PDF links) | conecta, foco, intensivo, sesiones-individuales | ✓ `noopener noreferrer` | Content not reviewed — see P2-5 |
| `https://schema.org` | index.html (JSON-LD `@context`) | No `rel` needed ✓ | Informational only |

**All `target="_blank"` links have `rel="noopener noreferrer"` — no tab-nabbing vulnerability.** ✓

### WhatsApp number exposure

The number `+45 22 25 61 43` appears:
- In `wa.me/` href attributes (all 9 pages, footer + floating button)
- In `index.html` JSON-LD: `"telephone": "+4522256143"`

This is intentional for a public contact site, but Ana should explicitly confirm that having the phone number in structured data (indexed by search engines) is acceptable.

---

## 7. Build/Deployment Review

### Build result

`bash scripts/build-pages.sh` — **PASS**

### `dist/` contents

```
dist/
  _headers
  *.html (9 pages)
  assets/
    css/    editorial.css, home.css, prototype.css, styles.css
    fonts/  mulish-400, spectral-400/500/600 (latin + latin-ext woff2)
    img/    26 image files (jpg + webp, responsive pairs)
    js/     main.js
  robots.txt
  sitemap.xml
  favicon.svg
```

**No internal folders leaked.** The build script explicitly guards against `content/`, `source/`, `docs/`, `reports/`, `tools/`, `.git/`, `.claude/`, `node_modules/`. ✓

### Build script safety

The `scripts/build-pages.sh` script:
- Deletes `dist/` fully before each build (no stale artifacts) ✓
- Copies `*.html` and `assets/` from root ✓
- Copies optional root files (`_headers`, `robots.txt`, etc.) ✓
- Runs an explicit post-copy safety check for forbidden directories ✓
- Exits non-zero if a forbidden path is found ✓

### Unused CSS in dist (P1-3 detail)

| File | Linked by HTML? | Comment |
|---|---|---|
| `editorial.css` | Yes (all 9 pages, `?v=2`) | Production stylesheet ✓ |
| `main.js` | Yes (all 9 pages, `defer`) | Production script ✓ |
| `home.css` | **No** | Prototype-era file, "prototype" in CSS comments |
| `prototype.css` | **No** | Prototype review banner, "prototype" in CSS comments |
| `styles.css` | **No** | Unknown origin/purpose |

These three unused files are accessible by direct URL in production. Recommend excluding them from the build (P1-3).

---

## 8. Claims / Sensitive Language Review

### Claims safety scan

`grep -RniE 'más de 15 años|+15 years|neurocientífica|...|precio|CLP|USD|DKK'`:

**Result: No forbidden terms found.**

`precio` hits (4 instances): All are the intentional disclaimer `"Los precios no se muestran públicamente. Se gestionan en la conversación inicial."` — **acceptable per spec.**

### Internal notes / placeholder scan

`grep -RniE 'por confirmar|pendiente|TODO|FIXME|Claude|ChatGPT|prompt|prototype|...'`:

**Expected false positives confirmed:**
- Spanish `todo/todos` in natural text — harmless
- `prototype` in `home.css:2` and `prototype.css:2-3,7` CSS comments — developer comments in CSS files, not HTML content
- `<!-- EL MÉTODO EN UNA MIRADA -->` HTML section comment in `sobre-ana.html:104` — section label, acceptable
- `scripts/build-pages.sh` safety check code — correct, not in output

**Actual workflow note found (P1-2):**
- `contacto.html:36`: `<!-- Pending Ana decision: CTA canonical name (sesión de exploración / conversación inicial / sesión de descubrimiento) -->` — internal note in production HTML

### CSP artifact scan

`grep -RniE 'style=|<style|fonts.googleapis|...'`:

**Result: CLEAN** — no inline styles, no `<style>` tags, no CDN fonts, no DC artifacts.

---

## 9. Recommended Next Prompts

After resolving P0 and P1 issues, the recommended sequence:

### AV-PROMPT-010 — Create final privacy page

Engage legal/compliance review to finalize `privacidad.html`. The skeleton is ready — needs:
- Legal name of data controller
- Confirmed jurisdiction (Denmark/EU)
- Final sections on data collected, legal basis, retention, rights, third parties, cookies (state: none)
- Remove `noindex` ONLY after legal review confirms the page is final and accurate

### AV-PROMPT-011 — Pre-launch cleanup

Technical fixes before public launch:
- Remove `<!-- Pending Ana decision -->` comment from `contacto.html` once name confirmed
- Fix invalid nested `<p class="ed-prose"><p>` on `conecta.html:63`, `contacto.html:77`, `programas.html:82`
- Lower CSS/JS cache TTL (`max-age=86400` → `max-age=3600`) in `_headers`
- Remove unused CSS files (`home.css`, `prototype.css`, `styles.css`) from build output
- Fix `areaServed: "ES"` → `"DK"` in JSON-LD (after Ana confirms geography)
- Expand `sitemap.xml` to include all 7 public pages

### AV-PROMPT-012 — SEO & metadata audit

Improve discoverability:
- Add page-specific OG/Twitter meta tags to all key pages
- Review and expand sitemap with priorities and `lastmod` dates
- Verify all canonical URLs are correct
- Review and confirm JSON-LD structured data (phone, social handles, areaServed)

### AV-PROMPT-013 — Connect custom domain

Steps for Cloudflare DNS configuration and custom domain activation, only after P0 and P1 are resolved.

---

## 10. Final Verdict

### Is `anacarolinas-com.pages.dev` okay for private review?

**Yes.** The site is secure, clean, and technically sound for private review by Ana and stakeholders. No data is collected, no tracking is present, and no sensitive information is leaked.

### Should the custom domain remain disconnected?

**Yes.** The custom domain (`anacarolinas.com`) should remain disconnected until:
1. ✅ P0-1 resolved: Final privacy page drafted and reviewed by legal professional
2. ✅ P1-1 addressed: CSS/JS cache TTL lowered (30-minute fix)
3. ✅ P1-2 addressed: Workflow comment removed from contacto.html
4. ✅ P1-3 addressed: Unused CSS files removed from build output
5. ✅ P2-3 addressed: Invalid nested `<p>` fixed on 3 pages
6. ✅ P2-1 addressed: `areaServed` corrected in JSON-LD (after Ana confirms)
7. ✅ P2-4: Ana confirms social handles, email, and phone are correct

P3 items are optional — they do not block launch.

### What must happen before public launch

| # | Action | Who | Priority |
|---|---|---|---|
| P0-1 | Final privacy page | Ana + legal professional | P0 — hard blocker |
| P1-1 | Lower CSS/JS cache TTL | Developer | P1 |
| P1-2 | Remove workflow comment from contacto.html | Developer (after Ana confirms CTA name) | P1 |
| P1-3 | Remove unused CSS from build | Developer | P1 |
| P2-1 | Fix `areaServed` in JSON-LD | Developer (after Ana confirms geography) | P2 |
| P2-2 | Expand sitemap.xml | Developer | P2 |
| P2-3 | Fix nested `<p>` HTML on 3 pages | Developer | P2 |
| P2-4 | Confirm all contact details are correct | Ana | P2 |
| P2-5 | Review and confirm PDF content | Ana | P2 |

---

*Report generated: 2026-06-25. Commit audited: `8ff4862`. No production website files were modified. Master branch and Cloudflare production were not changed. Custom domain was not connected.*
