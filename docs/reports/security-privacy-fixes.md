# AV-PROMPT-010 — Security & Privacy Technical Fixes

**Date:** 2026-06-25
**Source branch:** `fix/security-privacy-technical`
**Based on audit:** `docs/reports/security-privacy-review.md` (AV-PROMPT-009, commit `7bf7e4b`)
**Build result:** PASS

---

## 1. Summary

All non-legal technical findings from AV-PROMPT-009 have been implemented. The privacy page placeholder was intentionally left unchanged (P0 legal blocker — requires legal professional input). Custom domain remains disconnected.

**Custom domain remains blocked** pending privacy page finalization.

---

## 2. Fixes implemented

| Finding | Action taken | Files changed | Status |
|---|---|---|---|
| P1-1 CSS cache fragility | Lowered CSS/JS `max-age` from 86400 (24h) to 3600 (1h) + `must-revalidate`; `editorial.css?v=2` unchanged since CSS not edited | `_headers` | Done |
| P1-2 Workflow comment in HTML source | Removed `<!-- Pending Ana decision: CTA canonical name -->` from `contacto.html:36` | `contacto.html` | Done |
| P1-3 Unused CSS in dist | Build script now removes `home.css`, `prototype.css`, `styles.css` from `dist/assets/css/` after copy; `editorial.css` only in production | `scripts/build-pages.sh` | Done |
| P2-1 `areaServed:"ES"` wrong | Changed to `"areaServed": "DK"` (Denmark) in JSON-LD | `index.html` | Done |
| P2-2 Sitemap only 1 page | Updated to include all 8 public pages at `anacarolinas-com.pages.dev` URLs; `privacidad.html` excluded | `sitemap.xml` | Done |
| P2-3 Invalid nested `<p>` on 3 pages | Replaced `<p class="ed-prose"><p>…</p></p>` → `<div class="ed-prose"><p>…</p></div>` on `conecta.html:63`, `contacto.html:77`, `programas.html:82` | `conecta.html`, `contacto.html`, `programas.html` | Done |
| P2-4 Social/contact consistency | Verified consistent across all 9 pages — see note below | — | Verified; awaits Ana confirmation |
| P2-5 PDF content review | PDF links remain as secondary CTAs with correct `rel="noopener noreferrer"`; content review required from Ana | — | Documented; awaits Ana review |
| P3-5 robots.txt sitemap URL | Updated `Sitemap:` directive to reference `anacarolinas-com.pages.dev/sitemap.xml` (not the unconnected custom domain) | `robots.txt` | Done |

**Items intentionally not changed:**
- P0-1 Privacy page legal text — requires legal professional input
- P3-1 HSTS preload — defer until custom domain is connected and HTTPS is permanent
- P3-2 OG tags on inner pages — deferred to AV-PROMPT-012 SEO audit
- P3-3 JSON-LD + CSP informational — no action needed
- P3-4 Redundant X-Frame-Options — harmless, no action needed
- P3-6 `og-card.jpg` quality — deferred

---

## 3. Remaining blockers

### Must resolve before custom-domain public launch

| # | Blocker | Owner |
|---|---|---|
| 1 | **Privacy page legal text** — `privacidad.html` still contains `[CONFIRMAR]` placeholders and explicit notice of incompleteness. Requires legal professional familiar with Danish/EU GDPR. | Ana + legal professional |
| 2 | **Ana must confirm contact details are correct and active** — WhatsApp `+45 22 25 61 43`, email `info@anacarolinas.com`, Instagram `ana.carolina.coach`, LinkedIn `anacarolinasegura`, YouTube `@AnaCarolinaCoach`. All are currently consistent across all 9 pages. If any are wrong, fix before launch. | Ana |
| 3 | **Google Drive PDFs require content review** — 4 PDFs linked from Conecta, Foco, Intensivo, Sesiones Individuales. Risk: prices, outdated claims, personal data, draft markings. Ana must review each PDF before public launch. | Ana |
| 4 | **CTA canonical name in contacto.html** — The internal comment about `sesión de exploración / conversación inicial / sesión de descubrimiento` was removed. Ana's final decision on the CTA name should be reflected in visible copy if the current wording is provisional. | Ana |

---

## 4. Cache strategy note

### Current CSS version

All 9 pages link to `editorial.css?v=2`.

The CSS (`editorial.css`) was **not modified** in this prompt. The version string remains `?v=2`.

### Updated cache TTL

`_headers` now sets CSS and JS to `Cache-Control: public, max-age=3600, must-revalidate` (1 hour, must-revalidate).

Previous value was `max-age=86400` (24 hours). This caused the stale-CSS incident after AV-PROMPT-006 where the new Sobre Ana styles were invisible on Cloudflare for up to 24 hours.

With `max-age=3600`, the worst-case staleness window is 1 hour. `must-revalidate` prevents serving stale content beyond that.

### When to bump the CSS version string

**Bump `?v=N` every time `editorial.css` changes and is deployed to production.**

Process:
1. After editing `editorial.css`, find the current version: `grep "editorial.css?v=" *.html | head -1`
2. Increment N by 1 across all 9 pages: `sed -i 's/editorial.css?v=N/editorial.css?v=N+1/g' *.html` (or use a PowerShell replace)
3. Commit and push

Even with the shorter 1-hour TTL, failing to bump the version string will cause a 1-hour window where users with a cached copy see old CSS with new HTML. Always bump on CSS deploys.

### Future improvement

The version string is still a manual process. When the project is ready for a build-system upgrade, consider appending a git short hash automatically. This would make stale CSS impossible regardless of TTL.

---

## 5. Launch recommendation

**`anacarolinas-com.pages.dev` is okay for private review.** The site is clean, secure, and technically sound.

**The custom domain (`anacarolinas.com`) must remain disconnected until:**
1. The privacy page is legally finalized (P0 hard blocker)
2. Ana confirms all contact details are correct
3. Ana reviews and confirms all linked PDFs

Once those three items are resolved, the technical implementation is ready for custom-domain launch.
