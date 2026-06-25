# AV-PROMPT-016 — Site Visual Harmonization

Implemented: `fix/site-visual-harmonization` · 25 June 2026
Rollback tag: `pre-site-harmonization-2026-06-25`
Source branch: `fix/site-visual-harmonization` off `master` @ `dfdd27f`

---

## 1. Summary

**What was harmonized:**
- Programas blue band converted from dominant Salvia block to cream2 background with a 3px Salvia accent top border — blue is now a subtle signal, not a structural color
- Programas panel scrim lightened (0.62 → 0.50 max opacity) — cards feel more human and natural
- Sobre Ana CTA unified from "Agendar una conversación inicial" → "Agendar conversación inicial" (two occurrences)
- Sesiones includes box de-boxed (full border removed; top border retained as editorial anchor)
- CSS version bumped v=5 → v=6 on all 9 pages

**What was not changed:**
- Home page: no empty placeholder image boxes found — all 4 images are real photography ✓
- No page redesign of any kind
- No copy changes beyond CTA unification
- No new fonts, no inline styles, no external resources
- `noindex` in `privacidad.html` — preserved
- Custom domain not connected, DNS/Cloudflare unchanged
- All programme pages preserved (foco, intensivo, sesiones, conecta)

**Production status:**
- Merged to master and pushed
- Cloudflare Pages deployment triggered from master
- Custom domain was not connected or changed

---

## 2. Council findings addressed

| Finding | Action taken | Status |
|---|---|---|
| Programas blue band too dominant — felt like separate coastal campaign | Converted `ed-sec--haze` → `ed-sec--cream2` on band section; added 3px `#B7C9CD` top border as accent | ✓ Done |
| Card overlays too heavy / poster-like | Lightened scrim gradient from max 62% → 50% opacity | ✓ Done |
| Card clarity — Foco vs Intensivo distinction not clear enough | One-sentence desc added per card (015D) | ✓ Already done in 015D |
| Redundant cierre CTA section | Removed "¿Lista para iniciar?" section (015D) | ✓ Already done in 015D |
| CTA wording inconsistency site-wide | sobre-ana.html "Agendar una conversación inicial" → "Agendar conversación inicial" (×2); all other pages already unified in 015D | ✓ Done |
| Home placeholder image boxes | Checked — none found; all 4 images are real photography | ✓ No action needed |
| Sesiones includes box clinical border | `border: 1px solid var(--line)` → `border-top: 2px solid var(--line)` | ✓ Done (light) |
| Offer architecture documented | Below in section 4 | ✓ Done |
| Design system frozen | Below in section 3 | ✓ Done |

---

## 3. Design system note — frozen rule

**Primary color system:**
- Cream / warm off-white (`#F4EFE6`, `#F7F3EB`, `#EDE7DB`) = primary backgrounds
- Terracotta (`#A8501F`) = emotional emphasis and main CTA accent
- Olive (`#3A4429`, `#4E5A37`) = grounding, footers, closing sections
- Blue = accent only — never dominant

**Blue usage rule:**
- Salvia `#B7C9CD` and Haze marino `#95A8AD` may appear as: thin borders, small labels, subtle background tints
- Must NOT appear as a full dominant section background
- Example of correct usage: the Salvia `3px border-top` on the Programas band bridge

**Typography rule:**
- Spectral 600 = headings, editorial H1/H2, CTA strip titles
- Spectral 400 italic = pull quotes, Sobre Ana story sections, bridge quotes
- Mulish 400 = body text everywhere
- No new display fonts, no external fonts

**CTA system — one main phrase:**
`"Agendar conversación inicial"` — all conversion CTAs across all pages

Secondary action labels (unchanged):
- "Conocer Foco" / "Conocer Intensivo" (panel CTAs)
- "Ver programas ALMAVIVA" / "Conocer programas" (navigation CTAs)
- "Saber más sobre Ana" / "Info sobre las sesiones" (navigation CTAs)
- "Reservar" (nav button only — intentionally brief for nav UI)

**Programas role:**
Decision page, not a separate campaign microsite. Warm cream editorial, not coastal blue campaign.

---

## 4. Offer architecture note

**Current state:**
- Programas presents Foco and Intensivo as the two primary pathways (main cards with images, descriptions, and dedicated CTAs)
- Sesiones individuales and Conecta are referenced as a quiet secondary note in the distinction bridge: "Si buscas un primer espacio más puntual o una experiencia grupal, también puedes explorar Sesiones individuales o Conecta"
- All four programme pages (`foco.html`, `intensivo.html`, `sesiones-individuales.html`, `conecta.html`) still exist and are reachable from the nav

**Ana must confirm:**
- Whether Foco + Intensivo as the two primary paths on Programas is the intended final offer architecture
- Whether Sesiones and Conecta should remain as quiet secondary references on Programas, or be removed from Programas entirely and exist only via direct nav links
- Whether Sesiones and Conecta should be merged, retired, or promoted at some future point

**This implementation does not decide this.** No pages were deleted, no routes removed.

---

## 5. Validation

### Build
`bash scripts/build-pages.sh` → ✓ PASS — 9 pages, no leakage, no docs/reports in dist

### Nav label scan
`grep -RniE 'Sesiones 1:1|Sob</a>'` → ✓ CLEAN

### Programas band scan
- `ed-sec--haze` in `programas.html` → ABSENT ✓ (converted to `ed-sec--cream2`)
- "Lista para iniciar" → ABSENT ✓
- "Conozcámonos" → ABSENT ✓
- ALMAVIVA Foco present (alt text on panel image) ✓
- ALMAVIVA Intensivo present (alt text on panel image) ✓
- Sesiones individuales: nav link (line 40) + quiet bridge note (line 109) only ✓

### CTA scan — all 9 pages
All conversion CTAs use "Agendar conversación inicial" ✓
"Conozcámonos" → ABSENT from all pages ✓
"Reservar" remains in nav only (intentional) ✓

### CSP/artifact scan → ✓ CLEAN

### Forbidden terms → ✓ CLEAN

### Internal note scan
All hits are legitimate content: "Todos los programas" (false positive from `TODO` substring in Spanish), "método" content. No workflow leakage.

### CSS version uniformity
All 9 pages: `editorial.css?v=6` ✓

### Privacy
- `<meta name="robots" content="noindex">` in `privacidad.html` → ✓ PRESERVED
- `privacidad.html` not in sitemap → ✓ CONFIRMED

### DOM QA (live preview)

| Check | Expected | Confirmed |
|---|---|---|
| Band section class | `ed-sec--cream2` | ✓ |
| Band background color | `rgb(247, 243, 235)` (cream2) | ✓ |
| Band accent border | `rgb(183, 201, 205) 3px solid` (Salvia) | ✓ |
| Panel scrim max opacity | ~50% (was 62%) | ✓ |
| "una conversación" in sobre-ana.html | ABSENT | ✓ |

---

## 6. Remaining Ana decisions

| Decision | Notes |
|---|---|
| Offer architecture: 2 primary paths vs 4 | Programas currently shows Foco + Intensivo as primary; Sesiones + Conecta as secondary quiet note. Ana must confirm. |
| Sesiones / Conecta on Programas | Secondary note currently reads: "también puedes explorar Sesiones individuales o Conecta." Ana may want to remove or reword. |
| Final CTA phrase | "Agendar conversación inicial" is now sitewide. Ana may shorten to "Agendar conversación" if preferred. |
| Final blue accent level | Salvia 3px top border on Programas band bridge — Ana may want more or less. |
| Privacy page legal review | `noindex` must remain until legal review; custom domain blocked by this |
| Custom domain timing | Connect `anacarolinas.com` after legal review of `privacidad.html` |
