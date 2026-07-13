#!/usr/bin/env python3
"""ALMAVIVA secure-by-design build gate (Python standard library only).

Validates the built HTML in a dist directory and the Cloudflare `_headers` CSP
against ALMAVIVA's strict security contract, using a real HTML parser rather
than fragile grep patterns. Fails CLOSED (non-zero exit) on any violation.

Usage:
    python scripts/check-security.py [DIST_DIR] [--headers HEADERS_FILE] [--baseline JSON]
    python scripts/check-security.py [DIST_DIR] --dump-baseline   # print JSON to stdout

Defaults: DIST_DIR=dist ; HEADERS_FILE=<DIST_DIR>/_headers (falls back to ./_headers) ;
          BASELINE = scripts/security-inline-style-baseline.json (next to this script).

Known-debt quarantine — structural fingerprint ratchet
------------------------------------------------------
Three legacy pages still carry inline styles pending the same inline-style ->
scoped-CSS migration that intensivo.html received. Each tolerated inline style is
recorded (in the tracked JSON baseline) as a normalized FINGERPRINT:

    <structural-locator>|<tag>#<id>|.<sorted classes>|<normalized declaration>

where <structural-locator> is the element's DOM path built while parsing —
`tag#id` for id-bearing ancestors, else `tag:nth-of-type(n)` — e.g.
`html:nth-of-type(1)>body:nth-of-type(1)>section#que-es>div:nth-of-type(2)>p:nth-of-type(1)`.
The locator gives every styled element a unique structural identity, so moving a
style between two otherwise identical elements changes its fingerprint.

On every build:
  * an inline style whose fingerprint is NOT in the baseline (a NEW style, a
    CHANGED declaration, or one MOVED to any other element/position) -> HARD FAIL;
  * more occurrences of a fingerprint than recorded -> HARD FAIL;
  * a recorded fingerprint now MISSING or REDUCED (debt removed or relocated) ->
    HARD FAIL as a STALE BASELINE requiring an explicit baseline edit.
The tracked JSON baseline is the single source of truth: debt can only shrink, and
shrinking forces an explicit, reviewable file change. `--dump-baseline` only PRINTS
a candidate baseline; it never writes the tracked file. Every OTHER violation type
on those pages, and ALL violations on every other page (strict by default), fail.
Regenerate after a legitimate migration:  --dump-baseline > <baseline JSON>.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Policy configuration
# ---------------------------------------------------------------------------

DEFAULT_BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "security-inline-style-baseline.json")

# Absolute resource URLs are only expected in metadata (canonical / OG), never in
# real subresources. If a subresource ever uses an absolute same-origin URL, these
# hosts are accepted; anything else is treated as an external resource.
ALLOWED_RESOURCE_HOSTS = {
    "anacarolinas-com.pages.dev",
    "anacarolinas.com",
    "www.anacarolinas.com",
}

# Inline <script> is forbidden UNLESS it is a non-executable data block that the
# CSP does not run. JSON-LD structured data is the ONLY permitted exception.
SAFE_INLINE_SCRIPT_TYPES = {
    "application/ld+json",
}

# Elements that fetch a subresource -> URL-bearing attributes.
RESOURCE_ELEMENTS = {
    "img": ["src"],
    "source": ["src"],
    "audio": ["src"],
    "video": ["src", "poster"],
    "track": ["src"],
}
# <link rel="..."> values that fetch a subresource (vs. metadata like canonical).
LINK_FETCH_RELS = {
    "stylesheet", "preload", "prefetch", "modulepreload",
    "icon", "shortcut icon", "apple-touch-icon", "mask-icon",
    "manifest", "preconnect", "dns-prefetch",
}
EMBED_ELEMENTS = {"object", "embed", "iframe"}          # none allowlisted
URL_ATTRS = {"href", "src", "action", "formaction", "data", "poster", "xlink:href"}
IMAGE_CONTEXT_TAGS = {"img", "source", "video"}         # data: URIs allowed (CSP img-src data:)
EMPTY_URL_TAGS = {"img", "script", "source", "iframe", "embed", "audio", "video", "track"}
# Void elements never have children; they must not be pushed onto the element stack.
VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}


def normalize_style(decl: str) -> str:
    """Order-independent, whitespace-insensitive normalization of a style value.

    'color:#FFF; MARGIN: 0  auto' -> 'color:#fff;margin:0 auto' (properties sorted,
    property names lower-cased, values whitespace-collapsed, value case preserved).
    """
    parts = []
    for chunk in decl.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            prop, value = chunk.split(":", 1)
            parts.append(prop.strip().lower() + ":" + " ".join(value.split()))
        else:
            parts.append(" ".join(chunk.split()).lower())
    return ";".join(sorted(parts))


def _segment(tag: str, el_id: str, nth: int) -> str:
    """One structural-locator segment: id-anchored when possible, else nth-of-type."""
    return f"{tag}#{el_id}" if el_id else f"{tag}:nth-of-type({nth})"


class SecurityHTMLParser(HTMLParser):
    """Collects security violations and structurally-located inline-style fingerprints."""

    def __init__(self, filename: str):
        super().__init__(convert_charrefs=True)
        self.filename = filename
        self.violations: list[dict] = []        # non-style violations (always blocking)
        self.styles: list[dict] = []            # {line, tag, fp} per style="" attribute
        self.stack: list[dict] = []             # open-element frames (for the locator)
        self.root_children: Counter = Counter()  # nth-of-type counter for top-level elements

    def _add(self, tag, attr, kind, reason):
        self.violations.append({
            "line": self.getpos()[0], "tag": tag, "attr": attr,
            "kind": kind, "reason": reason,
        })

    def handle_starttag(self, tag, attrs):
        self._enter(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._enter(tag, attrs, self_closing=True)

    def handle_endtag(self, tag):
        tag = tag.lower()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def _enter(self, tag, attrs, self_closing):
        tag = tag.lower()
        adict = {}
        style_value = None
        for name, value in attrs:
            n = name.lower()
            v = value if value is not None else ""
            adict[n] = v
            if n == "style":
                style_value = v
            elif n.startswith("on") and len(n) > 2:
                self._add(tag, n, "event-handler",
                          f"inline event-handler attribute '{n}' (CSP script-src blocks it)")
            if n in URL_ATTRS and v.strip().lower().startswith("javascript:"):
                self._add(tag, n, "javascript-url", f"javascript: URL in {n} attribute")

        el_id = adict.get("id", "").strip()
        classes = " ".join(sorted(adict.get("class", "").split()))

        # nth-of-type among same-tag siblings + full structural locator.
        if self.stack:
            parent = self.stack[-1]
            parent["children"][tag] += 1
            nth = parent["children"][tag]
            parent_locator = parent["locator"]
        else:
            self.root_children[tag] += 1
            nth = self.root_children[tag]
            parent_locator = ""
        seg = _segment(tag, el_id, nth)
        locator = (parent_locator + ">" + seg) if parent_locator else seg

        if style_value is not None:
            self.styles.append({
                "line": self.getpos()[0], "tag": tag,
                "fp": f"{locator}|{tag}#{el_id}|.{classes}|{normalize_style(style_value)}",
            })

        if tag == "style":
            self._add(tag, None, "inline-style-block",
                      "inline <style> block (deployed CSP style-src 'self' blocks it)")

        if tag == "script":
            if "src" not in adict:
                stype = adict.get("type", "").strip().lower()
                if stype not in SAFE_INLINE_SCRIPT_TYPES:
                    self._add(tag, None, "inline-script",
                              f"inline <script> without src (type={stype or 'javascript'}; only application/ld+json is allowed)")
            else:
                self._check_url(tag, "src", adict["src"])

        if tag in EMBED_ELEMENTS:
            self._add(tag, None, "embedded-content", f"<{tag}> element is not allowlisted")

        if tag in RESOURCE_ELEMENTS:
            for a in RESOURCE_ELEMENTS[tag]:
                if a in adict:
                    self._check_url(tag, a, adict[a])
            if "srcset" in adict:
                for part in adict["srcset"].split(","):
                    url = part.strip().split()[0] if part.strip() else ""
                    if url:
                        self._check_url(tag, "srcset", url)

        if tag == "link":
            rel = adict.get("rel", "").strip().lower()
            if rel in LINK_FETCH_RELS:
                href = adict.get("href")
                if href is None or href.strip() == "":
                    self._add(tag, "href", "empty-url", f"<link rel={rel}> with empty href")
                else:
                    self._check_url(tag, "href", href)

        if tag == "a" and adict.get("target", "").strip().lower() == "_blank":
            if "noopener" not in adict.get("rel", "").lower():
                self._add(tag, "target", "blank-noopener",
                          "target=_blank without rel containing noopener (reverse-tabnabbing risk)")

        for a in ("src",):
            if tag in EMPTY_URL_TAGS and a in adict and adict[a].strip() == "":
                self._add(tag, a, "empty-url", f"empty {a} attribute could trigger an unintended request")
        if tag == "a" and "href" in adict and adict["href"].strip() == "":
            self._add(tag, "href", "empty-url", "empty href on <a> could reload the page unintentionally")

        # Push a frame for elements that can contain children.
        if not self_closing and tag not in VOID_ELEMENTS:
            self.stack.append({"tag": tag, "id": el_id, "classes": classes,
                               "children": Counter(), "locator": locator})

    def _check_url(self, tag, attr, value):
        v = (value or "").strip()
        if v == "":
            self._add(tag, attr, "empty-url", f"empty {attr} could trigger an unintended request")
            return
        low = v.lower()
        if low.startswith("javascript:"):
            self._add(tag, attr, "javascript-url", f"javascript: URL in {tag} {attr}")
            return
        if low.startswith("data:"):
            if tag not in IMAGE_CONTEXT_TAGS:
                self._add(tag, attr, "data-url", f"data: URL in {tag} {attr} (only allowed for images)")
            return
        if low.startswith("http://"):
            self._add(tag, attr, "insecure-http", f"insecure http:// resource in {tag} {attr}")
            return
        if low.startswith("https://") or v.startswith("//"):
            host = urlparse(v if low.startswith("https://") else "https:" + v).netloc.lower()
            if host and host not in ALLOWED_RESOURCE_HOSTS:
                self._add(tag, attr, "external-resource",
                          f"external resource host '{host}' in {tag} {attr} (not self-hosted / not allowlisted)")
            return
        # relative URL -> same-origin -> OK


# ---------------------------------------------------------------------------
# CSP validation
# ---------------------------------------------------------------------------

def load_csp(headers_path: str):
    for raw in open(headers_path, encoding="utf-8").read().splitlines():
        line = raw.strip()
        if line.lower().startswith("content-security-policy:"):
            return line.split(":", 1)[1].strip()
    return None


def check_csp(headers_path: str):
    if not os.path.isfile(headers_path):
        return [f"_headers file not found at '{headers_path}'"], None
    csp = load_csp(headers_path)
    if not csp:
        return ["no Content-Security-Policy header found in _headers"], None

    directives = {}
    for part in csp.split(";"):
        toks = part.split()
        if toks:
            directives[toks[0].lower()] = [t.lower() for t in toks[1:]]

    problems = []
    if "'self'" not in directives.get("default-src", []):
        problems.append("default-src must include 'self'")

    if "style-src" not in directives:
        problems.append("missing style-src")
    else:
        if "'self'" not in directives["style-src"]:
            problems.append("style-src must include 'self'")
        if "'unsafe-inline'" in directives["style-src"]:
            problems.append("style-src must NOT include 'unsafe-inline'")

    if "script-src" not in directives:
        problems.append("missing script-src")
    else:
        if "'self'" not in directives["script-src"]:
            problems.append("script-src must include 'self'")
        if "'unsafe-inline'" in directives["script-src"]:
            problems.append("script-src must NOT include 'unsafe-inline'")
        if "'unsafe-eval'" in directives["script-src"]:
            problems.append("script-src must NOT include 'unsafe-eval'")

    if directives.get("object-src") != ["'none'"]:
        problems.append("object-src must be 'none'")

    fa = directives.get("frame-ancestors")
    if not fa:
        problems.append("must set frame-ancestors")
    elif "*" in fa:
        problems.append("frame-ancestors must not be '*'")

    if "upgrade-insecure-requests" not in directives:
        problems.append("must retain upgrade-insecure-requests")

    if "'unsafe-inline'" in csp.lower():
        problems.append("policy contains 'unsafe-inline' (forbidden)")
    if "'unsafe-eval'" in csp.lower():
        problems.append("policy contains 'unsafe-eval' (forbidden)")

    return problems, csp


# ---------------------------------------------------------------------------
# Baseline (tracked JSON)
# ---------------------------------------------------------------------------

def load_baseline(path: str):
    if not os.path.isfile(path):
        return {}, f"baseline file not found at '{path}' (treating every page as strict)"
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"baseline file '{path}' is not valid JSON: {exc}"
    if not isinstance(data, dict):
        return None, f"baseline file '{path}' must be a JSON object of {{page: {{fingerprint: count}}}}"
    return data, None


def parse_html_file(path: str) -> SecurityHTMLParser:
    parser = SecurityHTMLParser(os.path.basename(path))
    parser.feed(open(path, encoding="utf-8").read())
    return parser


def dump_baseline(html_files) -> int:
    """Print a candidate baseline as JSON. Never writes the tracked file."""
    out = {}
    for f in html_files:
        base = os.path.basename(f)
        try:
            fps = Counter(s["fp"] for s in parse_html_file(f).styles)
        except Exception as exc:  # noqa: BLE001
            print(f"// {base}: parse error: {exc}", file=sys.stderr)
            continue
        if fps:
            out[base] = dict(sorted(fps.items()))
    print(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="ALMAVIVA secure-by-design build gate")
    ap.add_argument("dist", nargs="?", default="dist", help="built output directory (default: dist)")
    ap.add_argument("--headers", default=None, help="path to _headers (default: <dist>/_headers or ./_headers)")
    ap.add_argument("--baseline", default=DEFAULT_BASELINE, help="path to the tracked inline-style baseline JSON")
    ap.add_argument("--dump-baseline", action="store_true",
                    help="print a candidate baseline JSON to stdout and exit (does not write any file)")
    args = ap.parse_args()

    dist = args.dist
    if not os.path.isdir(dist):
        print(f"ERROR: dist directory '{dist}' not found. Run the build first.", file=sys.stderr)
        return 2

    html_files = sorted(glob.glob(os.path.join(dist, "*.html")))

    if args.dump_baseline:
        return dump_baseline(html_files)

    baseline_data, baseline_note = load_baseline(args.baseline)
    if baseline_data is None:
        print(f"ERROR: {baseline_note}", file=sys.stderr)
        return 2

    headers_path = args.headers
    if headers_path is None:
        candidate = os.path.join(dist, "_headers")
        headers_path = candidate if os.path.isfile(candidate) else "_headers"

    hard_fail: list[tuple[str, dict]] = []
    quarantined_by_page: Counter = Counter()
    by_kind: Counter = Counter()

    for f in html_files:
        base = os.path.basename(f)
        try:
            parser = parse_html_file(f)
        except Exception as exc:  # noqa: BLE001 - report any parse failure as a violation
            hard_fail.append((base, {"line": 0, "tag": None, "attr": None,
                                     "kind": "parse-error", "reason": f"HTML parse error: {exc}"}))
            continue

        for v in parser.violations:
            by_kind[v["kind"]] += 1
            hard_fail.append((base, v))

        by_kind["inline-style-attr"] += len(parser.styles)
        baseline = Counter(baseline_data.get(base, {}))
        actual = Counter(s["fp"] for s in parser.styles)
        rep = {}
        for s in parser.styles:
            rep.setdefault(s["fp"], s)

        if not baseline:
            for s in parser.styles:
                hard_fail.append((base, {"line": s["line"], "tag": s["tag"], "attr": "style",
                                         "kind": "inline-style-attr",
                                         "reason": "inline style attribute (page not in the tracked baseline)"}))
            continue

        for fp, n in actual.items():
            allowed = baseline.get(fp, 0)
            quarantined_by_page[base] += min(n, allowed)
            if n > allowed:
                s = rep[fp]
                reason = ("inline style not in the tracked baseline "
                          "(new, changed, or relocated)" if allowed == 0
                          else f"{n - allowed} more occurrence(s) than the baseline records")
                hard_fail.append((base, {"line": s["line"], "tag": s["tag"], "attr": "style",
                                         "kind": "inline-style-unrecognized",
                                         "reason": f"{reason}: {fp}"}))
        for fp, n in baseline.items():
            present = actual.get(fp, 0)
            if present < n:
                hard_fail.append((base, {"line": 0, "tag": None, "attr": None,
                                         "kind": "stale-baseline",
                                         "reason": (f"baseline records {n}x but {present}x present of {fp} "
                                                    f"-> reduce/remove this entry in the tracked baseline")}))

    csp_problems, csp = check_csp(headers_path)
    for p in csp_problems:
        by_kind["csp"] += 1
        hard_fail.append(("_headers", {"line": 0, "tag": None, "attr": None, "kind": "csp", "reason": p}))

    # ---- report ----
    print("=" * 72)
    print("ALMAVIVA security check")
    print(f"  HTML files checked : {len(html_files)}")
    print(f"  CSP source         : {headers_path}")
    print(f"  Baseline           : {args.baseline}")
    if baseline_note:
        print(f"  NOTE               : {baseline_note}")
    if csp:
        print(f"  CSP                : {csp}")
    print("=" * 72)

    if quarantined_by_page:
        print()
        print("KNOWN DEBT - quarantined inline styles (structural-fingerprint-matched; reported, NOT failing):")
        for base in sorted(quarantined_by_page):
            recorded = sum(baseline_data.get(base, {}).values())
            print(f"  ! {base}: {quarantined_by_page[base]} inline style(s) matched the tracked baseline ({recorded} recorded)")
        print("  -> Migrate to scoped CSS (docs/SECURE-DEVELOPMENT.md); regenerate with --dump-baseline > baseline JSON.")
        print("     A page auto-enforces the instant it reaches 0 recorded fingerprints.")

    if by_kind:
        print()
        print("Violations by type (all pages, incl. quarantined inline styles):")
        for k in sorted(by_kind):
            print(f"  {k}: {by_kind[k]}")

    if hard_fail:
        print()
        print(f"BLOCKING violations: {len(hard_fail)}")
        for base, v in hard_fail:
            loc = f"{base}:{v['line']}" if v["line"] else base
            el = ""
            if v["tag"]:
                el = f" <{v['tag']}" + (f" {v['attr']}" if v["attr"] else "") + ">"
            print(f"  X [{v['kind']}] {loc}{el} - {v['reason']}")
        print()
        print("SECURITY CHECK FAILED")
        return 1

    print()
    print("Blocking violations: 0" + (" (only quarantined known-debt above)" if quarantined_by_page else ""))
    print("SECURITY CHECK PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
