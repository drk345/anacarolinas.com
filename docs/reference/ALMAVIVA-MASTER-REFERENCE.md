# ALMAVIVA Master Reference

Status: CANONICAL — current source of truth for brand/technical decisions on the ALMAVIVA site.
Supersedes: `docs/reports/almaviva-frozen-spec.md`

## Change history

- **2026-07-02** — This file created as the canonical reference, superseding `docs/reports/almaviva-frozen-spec.md`. Specifically, the **Programas page / offer architecture section** of the old frozen spec is now outdated and must not be used: it described a "2 programs only" (Foco + Intensivo) structure and left the status of Conecta/Sesiones as an open decision. That decision has since been made. See Section 5 below for the current, confirmed structure. All other sections of the old frozen spec (color system, typography, CTA system, page rhythm, image treatment, CSP constraints, forbidden terms) remain accurate and are carried forward here unchanged. The old file (`docs/reports/almaviva-frozen-spec.md`) is kept in place for historical reference only — do not treat its Programas section as current.

- **2026-07-10** — Ratified **Cormorant Garamond** as the ALMAVIVA display serif, matching the approved homepage and programme hero system. Retired **Lato** and **Playfair Display** from active pages. Current sanctioned families: Cormorant Garamond, Spectral, Mulish. This supersedes the earlier "Headings H1/H2 → Spectral" and "two families only" wording in Section 2.

- **2026-07-12** — Renamed **Método ALMAVIVA Pillar 2** from "Autoconocimiento" to "Observación". The five official pillars are now, in order: **1. Conocimiento · 2. Observación · 3. Intención Clara · 4. Acción Sostenible · 5. Integración**. Applied to the homepage five-pillar diagram + card title and to the Intensivo Pillar 2 copy and its 8-week progression labels. Generic prose uses of the word "autoconocimiento" (self-knowledge as a concept, not the pillar label) were intentionally left unchanged.

---

## 1. Color system

| Role | Color | Hex | Usage |
|---|---|---|---|
| Primary background | Cream | `#F4EFE6` | Page backgrounds, hero sections |
| Secondary background | Cream2 | `#F7F3EB` | Alternating sections, hero cards |
| Tertiary background | Cream3 | `#EDE7DB` | Panel gaps, light accent sections |
| Brand ink | Ink | `#23271E` | Body text, dark headings |
| Primary accent | Terracotta | `#A8501F` | Main CTA buttons, accent headings, emotional emphasis |
| Grounding | Olive | `#3A4429` | Footers, closing CTA strips |
| Secondary olive | Olive2 | `#4E5A37` | Supporting text, bridge quotes |
| Divider | Line | `#DCD6C7` | Borders, separators |

**Blue — accent only:**
- Salvia: `#B7C9CD` — may appear as thin accent borders or subtle labels only
- Haze marino: `#95A8AD` — same restriction
- Rule: blue must NOT appear as a dominant full-section background or structural color

**Terracotta is the visual anchor.** Home and all programme hero pages use terracotta (`ed-sec--accent`) as the emotional/brand signal. Do not replace with cream.

---

## 2. Typography

| Use | Font | Weight | Style | Notes |
|---|---|---|---|---|
| Display / hero headings | Cormorant Garamond | 400–600 | Normal / Italic | The ALMAVIVA display serif: homepage wordmark-style moments, programme hero titles, Sobre Ana hero, large emotional statements, and selected editorial display treatments (e.g. Sobre Ana section headings, Sesiones hero quote). |
| Editorial headings / bridge text | Spectral | 400–600 | Normal / Italic | Default serif for section headings (H2/H3), reflective bridge phrases, pull-quotes, and narrative asides. |
| Body text | Mulish | 400 | Normal | All running copy and long-form explanatory text. |
| Labels / eyebrows / nav / UI | Mulish | 600–800 | Normal / Uppercase | Eyebrow labels (`11px`, `2.5px` tracking), nav links, buttons, captions, form/UI text, and small structured elements. |

**Three self-hosted families only — Cormorant Garamond (display), Spectral (editorial serif), Mulish (body / UI).**
No other display fonts, no external fonts (CDNs), no Google Fonts at runtime. All three are self-hosted from `assets/fonts/`.
**Lato and Playfair Display are retired** and must not be reintroduced.
Adding, removing, or reassigning any family requires updating this section first.

---

## 3. CTA system

**Primary CTA phrase (one, sitewide):**
`"Agendar conversación inicial"`

Use this for all conversion-intent links to `contacto.html`.

**Secondary action labels (navigation / exploration):**
- `"Conocer Conecta"` / `"Conocer Foco"` / `"Conocer Intensivo"` — programme card CTAs (the 3 main programs, home and Programas page)
- `"Ver programas ALMAVIVA"` / `"Conocer programas"` — navigation from other pages
- `"Saber más sobre Ana"` / `"Info sobre las sesiones"` — navigation CTAs
- `"Reservar"` — nav button only (intentionally brief for nav UI)

**Supporting-offer CTA labels (secondary offerings, never framed as a 4th program):**
- `"Info sobre las sesiones"` — links to Sesiones Individuales
- Language pointing to a Sesión Exploratoria or a Guía (orientation/summary document) is acceptable only as supporting/secondary language — never presented as equal in rank to the 3 main programs.

**Prohibited CTA variants (do not reintroduce):**
- `"Conozcámonos"` — removed in AV-PROMPT-015D
- `"Agendar conversación"` (without "inicial") — unified in AV-PROMPT-016
- `"Agendar una conversación inicial"` — unified in AV-PROMPT-016
- Any price, guarantee, or testimonial-adjacent CTA

---

## 4. Page rhythm (preferred)

1. Hero (terracotta `ed-sec--accent` for programme pages, cream/cream2 for Programas and Sobre Ana)
2. Short bridge / belief statement
3. Main content
4. Small clarity / supporting section
5. Boundary / disclaimer note (`ed-therapy`)
6. Final olive CTA strip (`ed-cta-strip ed-sec--olive`)
7. Footer (`ed-footer`)

---

## 5. Programas page — current, confirmed structure

**This section replaces the "Programas page — frozen state" section of the old frozen spec in full.** The old "2 programs only" rule and the old "cuatro caminos" (4 equal paths) framing are both superseded and must not be reintroduced.

### 5.1 The offer architecture (confirmed)

ALMAVIVA's real offer structure is exactly **3 main programs**, always presented in this fixed order:

1. **ALMAVIVA Conecta**
2. **ALMAVIVA Foco**
3. **ALMAVIVA Intensivo**

These 3 are co-equal main programs — none is subordinate to another, and none should be dropped or reordered.

**Supporting/secondary offerings** (valid as supporting CTA language; must never be presented as a 4th main program or as a replacement for one of the 3):
- **Sesiones Individuales** — one-to-one accompaniment, positioned as a distinct, secondary offering (its own page, `sesiones-individuales.html`, reachable from nav and from a dedicated home section)
- **Sesión Exploratoria** — a supporting/introductory offer, not a program
- **Guía** (where referenced) — a supporting orientation/summary document, not a program

Do not:
- Reduce the main offer set to 2 programs (the old Foco + Intensivo–only framing is retired)
- Inflate the offer set to a "4 caminos" or "cuatro caminos" framing that treats Sesiones/Exploratoria/Guía as equal-rank paths alongside the 3 main programs
- Present Sesiones Individuales, Sesión Exploratoria, or Guía as a card inside the 3-program grid

### 5.2 Homepage: canonical card copy (verified from `index.html`, `#cursos` section)

The homepage presents all 3 programs as cards, in the fixed order above, each with a label/eyebrow (`ed-fcard__label`), title (`ed-fcard__title`), one-sentence description (`ed-fcard__desc`), and CTA (`ed-fcard__cta`). Section intro: eyebrow "Los caminos", H2 "Elige tu camino", lead "ALMAVIVA no es un solo camino. Cada programa responde a un momento distinto. Elige el que haga sentido para ti ahora."

| Order | Label | Title | Description | CTA | Links to |
|---|---|---|---|---|---|
| 1 | En comunidad | ALMAVIVA Conecta | Entrena en grupo y aprende junto a otras personas en un mismo proceso. | Conocer Conecta → | `conecta.html` |
| 2 | Objetivo concreto | ALMAVIVA Foco | Entrenamiento dirigido a un objetivo específico, con foco y resultados claros. | Conocer Foco → | `foco.html` |
| 3 | Inmersión completa | ALMAVIVA Intensivo | El recorrido completo por los cinco pilares para una transformación profunda y sostenida. | Conocer Intensivo → | `intensivo.html` |

This card grid (`ed-home-programs__grid` of `ed-fcard` items) is the canonical copy source. Any future edit to program card copy should update this table to keep it in sync with `index.html`.

Sesiones Individuales appears on the homepage as its own, separate 2-column section (`#sesiones`, cream2 background) below the programs grid — H2 "Sesiones Individuales ALMAVIVA", CTA "Info sobre las sesiones →" to `sesiones-individuales.html`. This confirms its status as a supporting offering, distinct from and outside the 3-program grid.

### 5.3 Programas page (`programas.html`): required structure

For consistency with the homepage, `programas.html` should present the **same 3-program structure**, in the same order (Conecta, Foco, Intensivo), as its main content.

**Resolved 2026-07-02 (Session 007):** `programas.html` now shows all 3 programs — hero sub, band heading ("Tres caminos para un mismo método"), the programme grid (`aria-label="Los tres programas ALMAVIVA"`, Conecta → Foco → Intensivo), and the distinction bridge were all updated to match. The Conecta panel reuses the existing `programas-sesiones-*` photo asset (same editorial-portrait treatment as the Foco/Intensivo panels — no panel photo on this page depicts program content literally, so this is consistent with the existing pattern) pending a dedicated Conecta photo from Ana.

**What belongs on `programas.html` once aligned:**
- Hero (2-col, white/cream bg, Spectral H1, sub sentence, "Agendar conversación inicial" CTA)
- Intro band presenting the 3 programs as a set (heading should reflect 3, not 2 — do not use "dos caminos" language)
- 3 programme cards/panels: Conecta, Foco, Intensivo (one-sentence desc each, "Conocer Conecta" / "Conocer Foco" / "Conocer Intensivo" CTAs), in that order
- Distinction/bridge copy connecting the 3 programs under one shared method
- Therapy disclaimer (`ed-therapy`)
- Olive CTA strip ("¿Por dónde empezamos?", "Agendar conversación inicial")

**What must NOT be (re-)added to `programas.html`:**
- A framing that limits the visible programs to 2 ("dos caminos" copy is retired along with the old 2-program rule)
- A "cuatro caminos" / 4-equal-paths framing that elevates Sesiones Individuales, Sesión Exploratoria, or Guía to main-program rank
- Comparison table
- Decision matrix
- "¿Lista para iniciar tu proceso?" section
- "Conozcámonos" CTA
- "¿Cuál es para ti?" decision helper

**Sesiones Individuales / Sesión Exploratoria / Guía relative to Programas:** these remain secondary, supporting offerings. They may be cross-referenced from Programas as secondary paths (e.g., a small supporting note or link), but must never appear as a 4th card in the main program grid and must never be styled or ranked as equal to Conecta/Foco/Intensivo.

---

## 6. Image treatment

- All images: real photography — no illustrations, no icon-led layouts
- `picture`/`srcset`/WebP+JPEG pairs, 800w + 1200w variants
- `object-fit: cover` on all panel images
- Panels (Conecta/Foco/Intensivo): scrim max opacity ~50% — images must feel natural, not over-darkened
- Hero images: `object-position: 50% 15%` on Programas (preserves Ana's head/hair in the crop)

---

## 7. CSP and technical constraints

- `style-src 'self'` — **no inline `style=""` attributes**, no `<style>` blocks
- **No external fonts or scripts** (no Google Fonts CDN, no analytics, no tracking)
- **No inline scripts** — all JS via `assets/js/main.js`
- `noindex` on `privacidad.html` — must remain until legal review and custom domain connection
- All URLs canonical to `https://anacarolinas-com.pages.dev/` until custom domain connects

---

## 8. Forbidden terms (never add to any page)

`neurocientífica` · `especialista en neurociencia aplicada` · `más de 15 años` · `+15 years`
`transformar vidas` · `tu mejor versión` · `no estás rota`
`adicción` · `depresión` · `trauma` · `rock bottom`
`testimonio` · `testimonial` · prices · `CLP` · `USD` · `DKK`

---

## 9. Remaining blockers / open items

| Blocker | What's needed |
|---|---|
| Connect `anacarolinas.com` | Legal review + Ana approval |
| Remove `noindex` from `privacidad.html` | Legal review of privacy page |
| Update canonical/OG/sitemap to `anacarolinas.com` | After domain connection |
| Conecta panel on `programas.html` uses a reused photo (`programas-sesiones-*`) | Optional — swap for a dedicated Conecta photo if/when Ana supplies one |
| Nav "Sobre mí" vs "Sobre Ana" | Ana preference (current: "Sobre mí") |

---

## 10. Source documents

- Old frozen spec (historical only, Programas section outdated): `docs/reports/almaviva-frozen-spec.md`
- Canonical program card copy source: `index.html` (`#cursos` section, `ed-home-programs__grid`)
- Programas page (pending alignment with 3-program structure): `programas.html`
