# AV-PROMPT-008 — Privacy Page Draft

## 1. Summary

**What was changed:** `privacidad.html` was rewritten from a short placeholder with `[CONFIRMAR...]` stub text into a complete 12-section privacy policy draft in Spanish, written in ALMAVIVA's warm editorial tone using the existing `editorial.css?v=2` class system.

**Why the page remains noindex:** The draft is substantive and accurate to current site behaviour, but it has not been reviewed by a legal professional. The `<meta name="robots" content="noindex">` remains in place until Ana and/or legal counsel sign off on the content and until the custom domain is connected.

**What is still pending:** Full legal review before the noindex can be removed and before the custom domain (`anacarolinas.com`) can be connected. See Section 3.

---

## 2. Facts reflected

| Fact | Source |
|---|---|
| Static Cloudflare Pages site | `_headers`, build script |
| No forms (contact, newsletter, registration) | All HTML pages — no `<form>` elements |
| No analytics tools | All HTML/CSS/JS — no GA, Matomo, Plausible, etc. |
| No tracking pixels | All HTML — no Meta Pixel, LinkedIn Insight, etc. |
| No intentional cookies from site code | No `document.cookie` writes found |
| Cloudflare Pages hosting | `_headers`, Cloudflare project |
| Contact email: `info@anacarolinas.com` | `contacto.html`, `index.html` JSON-LD |
| WhatsApp: `https://wa.me/4522256143` | `contacto.html`, footer on all pages |
| Instagram: `ana.carolina.coach` | All footers, JSON-LD |
| LinkedIn: `anacarolinasegura` | All footers, JSON-LD |
| YouTube: `@AnaCarolinaCoach` | All footers, JSON-LD |
| Google Drive PDFs linked | `conecta.html`, `foco.html`, `intensivo.html`, `sesiones-individuales.html` |
| Location: Copenhagen, Denmark | `areaServed: "DK"` in JSON-LD, Danish phone prefix (+45) |
| No embedded third-party scripts | `_headers` CSP: `script-src 'self'` |

---

## 3. Legal review needed

Before the noindex can be removed and the custom domain connected, Ana and/or legal counsel must confirm:

- **Responsible person / legal entity:** Current draft uses "Ana Carolina Segura / ALMAVIVA Neurotraining" — confirm if a formal legal entity name, company number, or registered business applies
- **Contact details:** Confirm `info@anacarolinas.com` is the correct and permanent privacy contact
- **Postal address:** Draft does not include a street address — confirm if one is legally required for the jurisdiction
- **Legal entity type:** Individual, sole trader, or registered entity — affects how the "responsable" section is worded
- **Legal basis wording (Section 04):** The draft uses "consentimiento implícito en el contacto" and "interés legítimo" — legal counsel should confirm the correct GDPR basis for each processing activity
- **Retention approach (Section 07):** No specific retention period is stated — counsel may want to add one
- **WhatsApp and social media contact:** Confirm whether GDPR obligations apply when someone sends a WhatsApp message, and if any specific wording is needed
- **Google Drive PDFs (Section 06):** Confirm whether hosting programme PDFs on Google Drive constitutes a data processing relationship that needs a DPA or additional disclosure
- **Datatilsynet reference (Section 09):** The draft mentions Datatilsynet as the supervisory authority — confirm this is correct given Ana's location and where processing occurs
- **Whether `ed-therapy` disclaimer in Section 12 should remain or be styled differently**

---

## 4. Launch status

| Item | Status |
|---|---|
| Privacy page: Cloudflare Pages preview URL | ✓ Accessible (noindex keeps it out of search) |
| noindex in `privacidad.html` | ✓ Present — must remain until legal approval |
| `privacidad.html` in sitemap | ✗ Not listed — correct |
| Custom domain (`anacarolinas.com`) | ✗ Not connected — blocked until legal review done |
| Custom domain URL switch (all canonical/OG/JSON-LD) | ✗ Pending — must happen when domain connects |

The page is available at `https://anacarolinas-com.pages.dev/privacidad.html` for Ana to review privately. It will not appear in search results while noindex is active.
