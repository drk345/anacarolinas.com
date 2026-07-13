# ALMAVIVA — Secure development workflow

ALMAVIVA is **secure by design**. The production Content-Security-Policy (CSP) is
the development contract, not a post-deployment afterthought. This document
explains why a plain local preview is misleading, the workflow that prevents the
class of failure it caused, and the guardrails that enforce it automatically.

---

## Why a plain local preview is NOT production-equivalent

Cloudflare Pages serves every response with a strict CSP (see `_headers`):

```
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none';
  frame-ancestors 'self'; img-src 'self' data:; font-src 'self'; style-src 'self';
  script-src 'self'; connect-src 'self'; form-action 'self'; upgrade-insecure-requests
```

Under `style-src 'self'` (no `unsafe-inline`), the browser **refuses every inline
`style=""` attribute** and every `<style>` block. Under `script-src 'self'`, it
refuses every inline `<script>`.

A plain static server (e.g. `python -m http.server`) sends **no CSP**, so those
same inline styles/scripts apply locally. The result: a page can look perfect
locally and render broken in production. This actually happened — inline styles
on Intensivo collapsed the progression layout and lost the hero CTA color on the
live site while looking correct locally. **We make that impossible to publish
again** with the guardrails below.

---

## The secure development workflow

```
1. Edit source (HTML / CSS / JS).
2. Run:  bash scripts/build-pages.sh
3. The build SECURITY GATE must pass (it runs automatically; the build fails
   closed if any rule is violated).
4. Run:  python scripts/serve-production.py
5. Open the CSP-equivalent preview and check mobile + desktop:
      http://127.0.0.1:8099/
   Inline styles/scripts are blocked here exactly as in production, so what you
   see is what deploys.
6. Commit and push (Cloudflare deploys from origin/master).
7. Run:  bash scripts/verify-live.sh
8. Confirm the live visual + console smoke tests (no CSP/console errors).
```

---

## 1. Build security gate — `scripts/check-security.py`

Runs automatically at the end of `scripts/build-pages.sh` against the built
`dist/`. It uses a real HTML parser (not fragile grep) and **fails the build
closed** (non-zero exit) on any violation. Run it standalone with:

```
python scripts/check-security.py dist
```

It rejects, in active production HTML:

- any `style` attribute;
- any inline `<style>` block;
- any inline `<script>` **without** `src` — except non-executable data blocks
  such as `type="application/ld+json"`, which the CSP does not execute;
- any `on*` event-handler attribute (`onclick`, `onload`, `onerror`, …);
- any `javascript:` URL;
- any insecure `http://` resource URL;
- any `<object>`, `<embed>`, or `<iframe>` (none are allowlisted);
- any `target="_blank"` link without `rel` containing `noopener`;
- external script / stylesheet / font / image / media resources that are not
  self-hosted (metadata such as `<link rel="canonical">` and OpenGraph tags are
  correctly ignored — they are not fetched subresources);
- empty `src`/`href` attributes that could trigger unintended requests.

It also validates `_headers` and fails if the CSP is missing or weakened:
`default-src 'self'`, `style-src 'self'` (no `unsafe-inline`), `script-src 'self'`
(no `unsafe-inline`/`unsafe-eval`), `object-src 'none'`, a restricted
`frame-ancestors`, and `upgrade-insecure-requests` present.

### Known-debt quarantine (temporary, structural-fingerprint-based)

Three legacy pages still carry inline styles pending the same migration Intensivo
received: `foco.html`, `sesiones-individuales.html`, `sobre-ana.html`. Each
tolerated inline style is recorded in the tracked JSON baseline
`scripts/security-inline-style-baseline.json` as a normalized **structural
fingerprint** — not merely a per-page count:

```
<structural-locator>|<tag>#<id>|.<sorted-classes>|<normalized-declaration>
```

The `<structural-locator>` is the element's DOM path, built while parsing
(`tag#id` for id-bearing ancestors, else `tag:nth-of-type(n)`), e.g.
`html:nth-of-type(1)>body:nth-of-type(1)>section#que-es>div:nth-of-type(2)>p:nth-of-type(1)`.
It gives every styled element a unique identity, so moving a style — even between
two otherwise identical sibling elements — changes its fingerprint. Reordering
declarations or changing whitespace does not (declarations are normalized; only
elements affect `nth-of-type`).

These fingerprints are reported on every build but do not fail it; **everything
else fails closed**:

- a **new** inline style, a **changed** declaration, or one **relocated** to any
  other element/position yields a fingerprint absent from the baseline → build fails;
- **removing** a tolerated style leaves its recorded fingerprint unmatched → build
  fails as a *stale baseline*, forcing an explicit baseline update;
- any inline style on a page **not** listed is blocked (strict by default).

The tracked JSON baseline is the single source of truth, so the debt can only shrink
and shrinking requires an explicit, reviewable file edit. `--dump-baseline` only
prints a candidate — it never writes the tracked file. After a legitimate migration,
regenerate explicitly and review the diff:

```
python scripts/check-security.py dist --dump-baseline > scripts/security-inline-style-baseline.json
```

When a page reaches zero fingerprints its key disappears and it auto-enforces. Every
**other** violation type on those pages, and **every** violation on every other page,
fails the build.

---

## 2. Production-parity preview — `scripts/serve-production.py`

A dependency-free (stdlib only) server that serves `dist/` while applying the
exact headers from `_headers` — most importantly the strict CSP, plus the
security and cache headers. This is the authoritative local QA surface.

```
bash scripts/build-pages.sh        # produces dist/ (incl. dist/_headers)
python scripts/serve-production.py # http://127.0.0.1:8099/  (Ctrl+C to stop)
```

Because it enforces the production CSP, any inline style/script that would be
stripped online is stripped here too. **Do not QA against a plain
`http.server`.**

---

## 3. Live verification — `scripts/verify-live.sh`

Run after every push once Cloudflare has rebuilt (usually 1–3 min):

```
bash scripts/verify-live.sh                    # default anacarolinas-com.pages.dev
bash scripts/verify-live.sh https://your-url   # any deployment
```

It confirms the live CSP (present, strict, no `unsafe-inline`/`unsafe-eval`),
that active HTML has zero inline styles and zero executable inline scripts, that
pages reference versioned (`?v=N`) CSS/JS, and that each deployed stylesheet's
hash matches local source. Non-zero exit on any failure.

---

## Forbidden vs approved patterns

| Forbidden (blocked online + by the gate) | Approved (self-hosted, CSP-safe) |
|---|---|
| `<p style="color:red">` | class in an external stylesheet: `<p class="warn">` |
| `<div style="top:14%">` (fragile inline coordinates) | scoped class: `<div class="wstage wk1">` + CSS `.wstage.wk1{top:14%}` |
| `<style>…</style>` in a page | rules in `assets/css/*.css` |
| `<script>doThing()</script>` | `<script src="assets/js/main.js?v=N" defer></script>` |
| `<button onclick="go()">` | `addEventListener` in `assets/js/main.js` |
| `<a href="javascript:…">` | a real URL or a JS-attached handler |
| `<img src="http://…">` | `<img src="assets/img/…">` (relative, self-hosted) |
| external font/script/style CDN | self-host the asset under `assets/` |
| `<a target="_blank">` (no rel) | `<a target="_blank" rel="noopener noreferrer">` |

`<script type="application/ld+json">…</script>` is **allowed**: it is inert data
(JSON-LD structured data), not executed by the browser, and not blocked by CSP.

Editable content must not depend on brittle fixed coordinates or inline
positioning — put layout in scoped CSS classes so a longer copy edit cannot
collapse the layout, and so nothing is lost when the CSP strips inline styles.

---

## The one rule that is never negotiable

**Never weaken the CSP to fix a visual problem.** Do not add `unsafe-inline`,
`unsafe-eval`, nonces, or hashes as a shortcut. If something renders wrong under
the production CSP, the fix is to move the inline style/script into an external,
self-hosted file — never to relax the policy. The strict CSP is a feature, not an
obstacle.
