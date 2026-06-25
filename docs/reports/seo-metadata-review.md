# AV-PROMPT-011 — SEO & Metadata Review

**Date:** 2026-06-25
**Auditor:** Claude (Opus 4.8, automated static analysis + live production check)
**Commit audited:** `07d3aba` (master, production)
**Branch:** `audit/seo-metadata-review`
**Build command:** `bash scripts/build-pages.sh`
**Build result:** PASS — 9 pages, `editorial.css` only in dist, `privacidad.html` noindex, no internal folders leaked
**Production check:** `https://anacarolinas-com.pages.dev/` is LIVE and reflects commit `07d3aba` (sobre-ana timeline + 2-col credentials render; sitemap serves 8 pages). No stale-CSS issue observed.

---

## 1. Executive Summary

### SEO readiness rating

**Ready with minor fixes** for private review. **Needs metadata implementation before public launch.**

The site has a solid metadata foundation: every page has a unique title, a unique and mostly specific meta description, a canonical tag, clean single-H1 heading structure, and meaningful image alt text. The homepage carries OG/Twitter tags and valid JSON-LD. There is no keyword stuffing and no medical/therapy/price claims. This is well above the baseline for a small static site.

The gaps are concentrated in four areas, none of which block private review but all of which should be resolved before the custom domain goes public.

### Top 5 SEO / metadata risks

1. **Domain signal contradiction (P1).** Every page's `canonical`, `og:url`, and JSON-LD `@id`/`url` point to `https://anacarolinas.com/` (custom domain, **not connected**), while `sitemap.xml` and `robots.txt` point to `https://anacarolinas-com.pages.dev/` (the live preview). Crawlers following the sitemap to a live pages.dev page are told by its canonical that the "real" page is on a domain that does not resolve yet. This produces confused indexing signals.
2. **Name inconsistency (P1).** Titles, meta, OG, and JSON-LD use the abbreviated **"Ana Carolina S"**; only the Sobre Ana `<h1>` uses the full **"Ana Carolina Segura."** For a personal brand whose name is a primary search term, the truncated form weakens entity recognition and looks like placeholder text.
3. **Homepage title is long, hype-leaning, and not brand-first (P1).** `Ana Carolina S — Neurotraining y Coaching para Transformación Personal` is ~70 characters (truncates in search results), leads with the abbreviated name instead of the brand, and uses "Transformación Personal," an outcome-promise phrase the project's own guardrails steer away from.
4. **Open Graph only on the homepage (P1).** The 7 inner public pages have **no** OG or Twitter tags. Any inner page shared on WhatsApp, LinkedIn, Instagram, or Facebook renders with no preview card (or a scraped fallback), which undercuts the warm, editorial brand at exactly the sharing moment.
5. **JSON-LD contains an unsupported audience claim (P2).** The `ProfessionalService` description says "coaching para personas **y empresas**," but there is **zero** corporate/B2B content anywhere on the site. This is an accuracy gap in structured data that search engines may surface.

### Should the custom domain be connected now?

**No.** The privacy page remains a launch blocker (tracked separately, out of scope here). Independently, the domain-signal strategy (risk 1) should be decided and implemented before connection so the custom domain inherits clean signals from day one.

### Is SEO good enough for private review?

**Yes.** Titles, descriptions, headings, alt text, and structured data are all present and credible. Nothing prevents stakeholders from reviewing the site on the Pages URL.

### Should metadata be implemented before public launch?

**Yes** — the P1 items (domain strategy, name standardization, homepage title, inner-page OG) should ship as `AV-PROMPT-012` before the custom domain is connected. P2/P3 items can follow.

---

## 2. Page-by-Page Metadata Review

Length targets: titles ≤ ~60 chars (SERP truncation), descriptions ~140–160 chars.

| Page | Current title quality | Current description quality | Main issue | Recommended title | Recommended meta description | Priority |
|---|---|---|---|---|---|---|
| **index.html** | Weak — ~70 chars (truncates), abbreviated name, "Transformación Personal" hype, not brand-first | Fair — specific but ends on "transformar tu manera de vivir" (outcome promise) | Title too long + hype; name abbreviated | `ALMAVIVA Neurotraining \| Ana Carolina Segura` | `ALMAVIVA integra neuroeducación, coaching, regulación emocional y prácticas cuerpo-mente para entrenar nuevas formas de responder con más conciencia.` (~148) | **P1** |
| **programas.html** | Good — clear, concise | Good — specific, lists the four programmes | Abbreviated name suffix only | `Programas ALMAVIVA \| Neurotraining y bienestar` | Keep current (142 chars, specific and claim-free) | P2 |
| **sesiones-individuales.html** | Good | Good but ~167 chars (slightly long) | Description trims for length; name suffix | `Sesiones individuales \| Ana Carolina Segura` | `Un espacio flexible de coaching para ganar claridad, hacer una pausa consciente y orientarte en tu momento, sin un proceso estructurado.` (~135) | P2 |
| **conecta.html** | Good | Good (~161, slightly long) | Name suffix; minor trim | `ALMAVIVA Conecta \| Programa grupal` | `Programa grupal de neuroeducación para comprender cómo funciona tu cerebro y empezar a entrenar nuevas respuestas, junto a otras personas.` (~140) | P2 |
| **foco.html** | Good | Good — specific, claim-free | Name suffix only | `ALMAVIVA Foco \| Acompañamiento individual` | Keep current (151 chars, accurate) | P2 |
| **intensivo.html** | Good | **Too long** — ~183 chars, truncates | Description length; name suffix | `ALMAVIVA Intensivo \| Proceso individual 1:1` | `El recorrido completo por los cinco pilares del Método ALMAVIVA: un proceso individual de neuroeducación, práctica somática y coaching, de principio a fin.` (~153) | **P1** (length) |
| **sobre-ana.html** | Fair — good structure, but "Sobre Ana Carolina" (no surname) | Fair — uses "Ana Carolina S" + "neurociencia aplicada al bienestar" | Name; soften neuroscience descriptor | `Sobre Ana Carolina Segura \| ALMAVIVA` | `La historia de Ana Carolina Segura y el camino personal que dio origen a ALMAVIVA: coaching integrativo, neuroeducación y prácticas cuerpo-mente.` (~146) | P2 |
| **contacto.html** | Good | Good but short (~118 chars) | Name suffix; could expand | `Contacto \| Ana Carolina Segura` | `Agenda una conversación inicial con Ana Carolina Segura: un espacio breve y sin compromiso para encontrar el camino ALMAVIVA que encaja contigo.` (~145) | P2 |
| **privacidad.html** | OK (noindex — low priority) | OK (noindex) | None — correctly noindexed, excluded from sitemap | `Política de privacidad \| Ana Carolina Segura` (optional) | Leave as-is — noindex page, no SEO value needed | P3 |

**Cross-cutting title note:** Current titles use an em-dash separator and append "· Ana Carolina S". The recommended system leads with the brand/programme and standardizes on a pipe `|` separator with the **full name "Ana Carolina Segura."** Adopting it gives consistent, brand-first, correctly-named titles — and every recommended title is ≤ 47 chars, eliminating the two current truncation problems (home, intensivo).

---

## 3. Structured Data Review

**Current status:** One JSON-LD block on `index.html` only, using `@graph` with a `Person` and a `ProfessionalService` entity. Schema types are appropriate. No `Rating`, `Review`, `Offer`, `price`, or medical schema is present — correct and safe.

**What is correct:**
- `areaServed: "DK"` — fixed in AV-PROMPT-010, now accurate (Denmark).
- `sameAs` social links match the footer links on every page (Instagram `ana.carolina.coach`, LinkedIn `anacarolinasegura`, YouTube `@AnaCarolinaCoach`).
- `email` and `telephone` match the site's contact channels.
- Person/ProfessionalService linked via `founder` → clean entity graph.
- No testimonials, ratings, prices, or credential claims in structured data.

**Accuracy concerns:**
1. **`name: "Ana Carolina S"` (P1)** — should be `"Ana Carolina Segura"` to match the Sobre Ana H1 and consolidate the personal-brand entity.
2. **`"coaching para personas y empresas"` (P2)** — no corporate/B2B offering exists anywhere on the site. Recommend dropping "y empresas" unless Ana confirms she offers corporate services. As written it is an unsupported claim in machine-readable data.
3. **`jobTitle: "Coach integrativa · neurociencia del bienestar"` (P2)** — "neurociencia del bienestar" sits close to the guardrail phrase "especialista en neurociencia del bienestar." Recommend softening to a defensible descriptor that matches the site's own language, e.g. `"Coach integrativa · neuroeducación y bienestar"`. The site consistently frames the work as *neuroeducación / neuroentrenamiento*, not as practising neuroscience.
4. **Domain in `@id`/`url`/`image` (P1)** — all use `https://anacarolinas.com/...` (see §4 strategy). JSON-LD should match whatever canonical strategy is chosen.

**Recommendation:** **Keep** the structured data (it adds real value for a personal brand and a local service), with the four corrections above. Do not expand to additional schema types before launch — the current Person + ProfessionalService graph is right-sized. The `anacarolinas.com` URLs inside JSON-LD should be migrated together with canonical/OG as one coordinated change (§4).

---

## 4. Sitemap and Robots Review

**Current state:**

| Signal | Value | Live? |
|---|---|---|
| `sitemap.xml` (8 URLs) | `https://anacarolinas-com.pages.dev/...` | ✓ live, verified in production |
| `robots.txt` `Sitemap:` | `https://anacarolinas-com.pages.dev/sitemap.xml` | ✓ |
| `robots.txt` rule | `User-agent: * / Allow: /` | ✓ fully crawlable |
| All pages `canonical` | `https://anacarolinas.com/...` | ✗ domain not connected |
| `index.html` `og:url` + JSON-LD URLs | `https://anacarolinas.com/...` | ✗ domain not connected |

**Findings:**
- **Sitemap coverage is correct:** all 8 indexable pages are listed; `privacidad.html` is correctly excluded while noindex. Production sitemap matches the repo. ✓
- **`privacidad.html` is correctly `noindex`** and absent from the sitemap. ✓
- **The contradiction (P1):** sitemap/robots advertise pages.dev as indexable, but each page's canonical disavows pages.dev in favor of the unconnected custom domain. This is the single most important SEO decision to make before launch.

**Two coherent strategies — pick one in AV-PROMPT-012:**

**Strategy A — Consolidate on the custom domain + gate the preview (recommended).**
- Keep canonical / OG / JSON-LD on `https://anacarolinas.com/` (already the case).
- Revert `sitemap.xml` and `robots.txt` to the `anacarolinas.com` domain **and** prevent the preview from being indexed in the meantime — either `Disallow: /` in a preview-only robots, or a temporary `noindex` on the pages.dev deployment.
- At launch: connect the domain, drop the indexing gate. Every signal already points to the right place; no migration churn, no authority wasted on a throwaway host.
- Best for a personal brand: the custom domain accrues all ranking signal from day one.

**Strategy B — Index the preview now, migrate at launch (lower effort, more churn).**
- Change canonical / OG / JSON-LD to `https://anacarolinas-com.pages.dev/` to match the sitemap.
- At launch: switch all five signal types back to `anacarolinas.com` and add 301 redirects pages.dev → custom domain.
- Downside: the preview (with its still-placeholder privacy page) gets indexed, then you migrate; brief authority leak to a `.pages.dev` host you don't want ranking.

**Recommendation:** **Strategy A.** It matches the existing canonical/OG/JSON-LD, avoids indexing a pre-launch site, and gives the custom domain a clean start. The only work is reverting sitemap+robots to the custom domain and adding a temporary indexing gate on the preview.

**What must change at custom-domain connection (either strategy):**
- All `canonical`, `og:url`, JSON-LD `@id`/`url`/`image` → final `https://anacarolinas.com/` (Strategy A: already done).
- `sitemap.xml` `<loc>` and `robots.txt` `Sitemap:` → `https://anacarolinas.com/`.
- Remove the preview indexing gate (Strategy A) or add 301s (Strategy B).
- Re-add `privacidad.html` to the sitemap **only after** it is finalized and `noindex` is removed.
- Submit the sitemap in Google Search Console under the custom domain.

---

## 5. Open Graph / Social Sharing Review

**Current OG status:**
- `index.html`: full set — `og:type`, `og:url`, `og:title`, `og:description`, `og:image` (+`width`/`height`), `og:locale` (`es_ES`), and Twitter `summary_large_image` with title/description/image. Solid.
- **All 7 other public pages: none.** No `og:*` and no `twitter:*`.

**Findings:**
- **Inner pages need page-specific OG (P1).** Sharing `/programas.html`, `/sobre-ana.html`, `/contacto.html`, or any programme page produces no rich preview. For a brand that will be shared one-to-one (WhatsApp, DMs) this is the highest-visibility gap after the domain question.
- **`og:image` quality (P3).** `og-card.jpg` is a valid 1200×630 progressive JPEG but only ~36 KB, which is light for that resolution — some platforms may show visible compression. Optional: regenerate at higher quality (~100–200 KB).
- **Homepage OG copy** repeats the "transformar tu manera de vivir" outcome phrase (see §8); soften alongside the meta description.
- **Missing nice-to-haves (P3):** `og:site_name` ("ALMAVIVA Neurotraining"), `og:image:alt`, and `twitter:site`/`twitter:creator` (if Ana has an X handle — none is currently linked, so likely skip).

**Recommendation (for AV-PROMPT-012):** add a minimal page-specific OG block to each of the 7 inner pages — `og:type=website`, `og:url` (per chosen domain strategy), `og:title` (mirror the new `<title>`), `og:description` (mirror the new meta description), and a shared `og:image` (reuse `og-card.jpg` until per-page images exist). Add Twitter card tags mirroring OG. This is mechanical, low-risk, and high-impact for sharing.

---

## 6. Image SEO / Alt Text Review

**Inventory:** Only 3 pages carry content images — `index.html` (4: hero, cursos, sesiones, sobre portrait), `sesiones-individuales.html` (1), `sobre-ana.html` (1 portrait). The four programme pages and contacto are text-only (no images), so no alt-text exposure there.

**Alt text quality — good:**
| File:line | Alt text | Assessment |
|---|---|---|
| index.html:108 | "Ana Carolina sentada con calma en su estudio" | Descriptive, natural, not stuffed ✓ |
| index.html:138 | "Ana Carolina en casa, trabajando con calma" | ✓ |
| index.html:150 | "Ana Carolina en una sesión, sentada con su portátil" | ✓ |
| index.html:180 | "Retrato de Ana Carolina, fundadora del método ALMAVIVA" | ✓ — includes brand context appropriately |
| sesiones-individuales.html:61 | "Ana Carolina en una sesión, sentada con su portátil" | ✓ |
| sobre-ana.html:46 | "Retrato de Ana Carolina, fundadora del método ALMAVIVA" | ✓ |

**Findings:**
- Alt text is meaningful, human, and keyword-appropriate without stuffing. No decorative image is over-described. No empty/missing alt on content images. **No action required.**
- All content images use responsive `srcset` + `sizes`, explicit `width`/`height` (prevents layout shift / good CLS), and correct `loading` (hero `eager`+`fetchpriority="high"`, below-fold `lazy`). This is strong technical image SEO already.
- **Minor (P3):** alt text uses "Ana Carolina" (no surname) — consistent with keeping alt natural; optional to use "Ana Carolina Segura" on the two portrait images for entity reinforcement, but not necessary.
- **Filenames** (`home-hero`, `home-sobre`, `og-card`, etc.) are clean, lowercase, hyphenated, descriptive — fine.

---

## 7. Heading and Internal Link Review

**Heading structure — clean across all 9 pages:**
- Every page has **exactly one `<h1>`** followed by logical `<h2>` sections. No skipped levels.
- `sobre-ana.html` correctly nests five `<h3>` timeline titles (01–05) under their section `<h2>` — proper hierarchy, not visual-only.
- H1s are distinct and intent-bearing: `ALMAVIVA` (home), `Programas ALMAVIVA`, `Un espacio de pausa y claridad`, `Entiende las bases. En comunidad.`, `Un patrón. Un proceso.`, `El recorrido completo.`, `Soy Ana Carolina Segura`, `Empecemos a hablar.`
- **Minor note (P3):** the homepage `<h1>` is just "ALMAVIVA"; the descriptor "Neurotraining" sits in an adjacent non-heading element. This is fine visually, but the H1's standalone text is a single word. Optional: the recommended `<title>` already supplies "ALMAVIVA Neurotraining," so no change needed — flagging only for awareness.

**Internal linking — sound hub-and-spoke:**
- **Nav (every page):** Inicio, Programas, Sesiones individuales, Sobre mí, Reservar (→ contacto). Consistent and present site-wide.
- **`programas.html` is the hub** linking to all four programme pages (cards + comparison table + decision list). Programme pages cross-link each other and link back to `programas.html`. Good crawl depth — every page is ≤ 2 clicks from home.
- **Sobre Ana → Programas:** present via the `ed-btn--outline` "Ver programas ALMAVIVA" CTA added in AV-PROMPT-006. ✓
- **Contacto** is reachable from the nav CTA on every page and from multiple in-body CTAs. ✓
- **Privacy** is linked once, from the footer on every page. ✓ Appropriate (low prominence, present).

**Findings / recommendations:**
- **Footer is thin (P3).** The footer contains only social links + Privacidad — it does not repeat the main nav. The top nav covers primary navigation, so this is not a problem, but adding a small footer link list (Programas, Sobre mí, Contacto) would marginally help crawlability and UX. Optional.
- **Nav omits direct links to Conecta/Foco/Intensivo (by design).** They live under Programas. Acceptable — keeps the nav clean and routes discovery through the hub.
- No orphan pages, no broken internal links found. Internal linking needs **no P0/P1 work.**

---

## 8. Claims and Safety Review

**Brand/claims scan** (`grep` for forbidden terms): the only hits are the four intentional `precio` disclaimers — *"Los precios no se muestran públicamente. Se gestionan en la conversación inicial."* — which are acceptable per spec. **No** `neurocientífica`, `especialista en neurociencia...`, `más de 15 años`, `transformar vidas`, `tu mejor versión`, `no estás rota`, `trauma`, `adicción`, `depresión`, `testimonio`, or currency/price values. ✓

**Internal-note scan:** no workflow leakage in public HTML. The only matches are Spanish `todo/todos` in body copy (expected, harmless), an HTML section comment in `sobre-ana.html` (`<!-- EL MÉTODO EN UNA MIRADA -->`, harmless), CSS developer comments in source files (not shipped), and the build script's own forbidden-path guard. The previously-flagged `<!-- Pending Ana decision -->` comment in `contacto.html` was removed in AV-PROMPT-010 and is confirmed gone. ✓

**CSP/artifact scan:** clean — no inline styles, no `<style>`, no Google Fonts CDN, no DC artifacts.

**Borderline language to soften in SEO copy (not forbidden, but off-brand for the "credible, warm, not overclaiming" target):**
1. **`Transformación Personal`** in the homepage `<title>` — outcome-promise phrasing; the recommended title drops it.
2. **`transformar tu manera de vivir`** in the homepage meta description, `og:description`, and `twitter:description` — softer than "transformar vidas" but still an outcome promise. The recommended descriptions replace it with capability language ("entrenar nuevas formas de responder con más conciencia").
3. **JSON-LD `neurociencia del bienestar`** (jobTitle) and **`neurociencia aplicada al bienestar`** (sobre-ana meta) — sit near the guardrail. The body copy's framing of *neuroeducación / neuroentrenamiento* is the safer, on-brand vocabulary; recommend aligning metadata to it.

**Anything to avoid during SEO implementation:** do not introduce any forbidden term to "improve" keyword coverage; do not add ratings/testimonials/price schema; do not claim credentials beyond what `sobre-ana.html` already states; keep all new OG/meta copy in the warm, precise, capability-not-outcome register.

---

## 9. Recommended Implementation Prompt — AV-PROMPT-012

**Title:** Implement SEO and metadata fixes

**Scope (technical, no legal text, no domain connection, preserve CSP & noindex):**

**P1 — before public launch:**
1. **Decide and implement the domain strategy (§4).** Recommended Strategy A: keep canonical/OG/JSON-LD on `anacarolinas.com`; revert `sitemap.xml` + `robots.txt` to `anacarolinas.com`; add a temporary indexing gate on the pages.dev preview (`Disallow: /` in a preview robots, or a build-flag noindex) so the unfinished site is not indexed. Document the launch-day un-gate step.
2. **Standardize the name** to **"Ana Carolina Segura"** across all titles, meta, OG, and JSON-LD `Person.name`.
3. **Rewrite the homepage `<title>`** to `ALMAVIVA Neurotraining | Ana Carolina Segura` and the homepage meta/OG/Twitter description to the capability-framed version in §2 (drop "Transformación Personal" / "transformar tu manera de vivir").
4. **Shorten the intensivo `<title>`/description** to stop SERP truncation (§2).
5. **Add page-specific OG + Twitter tags** to the 7 inner public pages, mirroring each page's new title/description and reusing `og-card.jpg` (§5).
6. **Apply the recommended title system** (pipe separator, brand-first) to all pages (§2).

**P2 — recommended:**
7. JSON-LD: remove **"y empresas"** (or confirm a real corporate offering); soften `jobTitle` to `Coach integrativa · neuroeducación y bienestar`.
8. Trim the slightly-long descriptions (sesiones, conecta) and align `sobre-ana` description to "Ana Carolina Segura" + neuroeducación vocabulary.

**P3 — optional:** regenerate a higher-quality `og-card.jpg`; add `og:site_name` + `og:image:alt`; add a small footer link list (Programas, Sobre mí, Contacto).

**On any CSS change:** none expected in AV-PROMPT-012 (metadata only). If `editorial.css` is touched, bump `?v=2 → ?v=3` across all pages.

**Validation:** rebuild; re-run forbidden-term, internal-note, CSP, metadata, heading, sitemap, and `noindex` scans; confirm one H1/page; confirm canonical/sitemap/robots are internally consistent under the chosen strategy.

---

## 10. Final Verdict

- **Is the Cloudflare Pages URL okay for private review?** **Yes.** Metadata, headings, alt text, structured data, and internal linking are all present and credible; the live deployment matches `07d3aba` with no stale-CSS issue. Stakeholders can review now.
- **Should the custom domain remain disconnected?** **Yes.** The privacy page is still a launch blocker, and the domain-signal strategy (§4) plus the P1 metadata fixes should ship first so the custom domain launches with clean, consistent signals.
- **Should SEO fixes happen before custom-domain launch?** **Yes.** Implement AV-PROMPT-012 (P1 items at minimum) before connecting the domain. The fixes are mechanical and low-risk, and doing them pre-connection means the custom domain is indexed correctly from its first crawl rather than being cleaned up afterward.

---

*Report generated 2026-06-25. Commit audited: `07d3aba`. No production website files were modified. Master branch, Cloudflare settings, and the custom domain were not changed. `privacidad.html` remains noindex.*
