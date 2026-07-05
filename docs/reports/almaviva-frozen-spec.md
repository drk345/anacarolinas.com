# ALMAVIVA Frozen Visual Spec

Status: FROZEN after AV-PROMPT-016 harmonization · 25 June 2026
Do not change without explicit Ana sign-off.

> **⚠ SUPERSEDED AS DEFAULT SOURCE OF TRUTH — 2026-07-02.**
> This file is kept for historical reference only. The canonical, current reference is now
> [`docs/reference/ALMAVIVA-MASTER-REFERENCE.md`](../reference/ALMAVIVA-MASTER-REFERENCE.md).
> In particular, **Section 5 below ("Programas page — frozen state") is outdated**: the
> "2 programs only" rule and the "Ana must decide" framing on Conecta have been resolved —
> the confirmed offer structure is 3 co-equal programs (Conecta, Foco, Intensivo). See
> Section 5 of the master reference for the current, correct structure. All other sections
> of this file (colors, typography, CTA system, page rhythm, image treatment, CSP, forbidden
> terms) remain accurate and were carried forward into the master reference unchanged.

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
| Headings H1/H2 | Spectral | 600 | Normal | Uppercase where established (Programas panels, CTA strip titles) |
| Pull quotes / bridge | Spectral | 400 | Italic | Used in bridge sections, Sobre Ana narrative |
| Body text | Mulish | 400 | Normal | All running copy |
| Eyebrow labels | Mulish | 800 | Uppercase | `11px`, `2.5px` letter-spacing |

**No new display fonts. No external fonts (CDNs). No Google Fonts.**
Both Spectral and Mulish are self-hosted from `assets/fonts/`.

---

## 3. CTA system

**Primary CTA phrase (one, sitewide):**
`"Agendar conversación inicial"`

Use this for all conversion-intent links to `contacto.html`.

**Secondary action labels (navigation / exploration):**
- `"Conocer Foco"` / `"Conocer Intensivo"` — programme card CTAs on Programas
- `"Ver programas ALMAVIVA"` / `"Conocer programas"` — navigation from other pages
- `"Saber más sobre Ana"` / `"Info sobre las sesiones"` — navigation CTAs
- `"Reservar"` — nav button only (intentionally brief for nav UI)

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

## 5. Programas page — frozen state

> **⚠ OUTDATED — superseded 2026-07-02.** This entire section describes a 2-program state
> that is no longer current. The confirmed offer structure is 3 co-equal programs: ALMAVIVA
> Conecta, ALMAVIVA Foco, ALMAVIVA Intensivo. The "offer architecture note" below is resolved
> — Conecta is now a main program, not an open decision. Kept below verbatim for historical
> record of the 25-June-2026 state; see `docs/reference/ALMAVIVA-MASTER-REFERENCE.md` §5 for
> the current, correct structure.

**What is on the page:**
- 2-col hero (white bg, Spectral H1, sub sentence, "Agendar conversación inicial" CTA)
- "Dos caminos" band (cream2 bg, 3px Salvia top border accent, Spectral H2, lead text)
- 2 programme cards: Foco + Intensivo (one-sentence desc each, "Conocer Foco" / "Conocer Intensivo" CTAs)
- Distinction bridge (cream2 bg, Spectral italic quote: "Ambos caminos comparten la misma base...")
- Therapy disclaimer (`ed-therapy`)
- Olive CTA strip ("¿Por dónde empezamos?", "Agendar conversación inicial")

**What is NOT on the page and must not be re-added without Ana approval:**
- Sesiones individuales card or panel
- Conecta card or panel
- A secondary note linking to Sesiones / Conecta from Programas
- Comparison table
- Decision matrix
- "¿Lista para iniciar tu proceso?" section
- "Conozcámonos" CTA
- "¿Cuál es para ti?" decision helper

**Offer architecture note (unresolved — Ana must decide):**
Programas currently presents Foco and Intensivo as the only visible pathways. Sesiones individuales and Conecta remain active pages reachable via the top navigation. Whether these should be cross-referenced from Programas as secondary paths, or remain separate, is Ana's decision. Do not resolve this in code.

---

## 6. Image treatment

- All images: real photography — no illustrations, no icon-led layouts
- `picture`/`srcset`/WebP+JPEG pairs, 800w + 1200w variants
- `object-fit: cover` on all panel images
- Panels (Foco/Intensivo): scrim max opacity ~50% — images must feel natural, not over-darkened
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

## 9. Remaining blockers (as of 25 June 2026)

| Blocker | What's needed |
|---|---|
| Connect `anacarolinas.com` | Legal review + Ana approval |
| Remove `noindex` from `privacidad.html` | Legal review of privacy page |
| Update canonical/OG/sitemap to `anacarolinas.com` | After domain connection |
| Offer architecture: Sesiones / Conecta on Programas | Ana must decide |
| Nav "Sobre mí" vs "Sobre Ana" | Ana preference (current: "Sobre mí") |
