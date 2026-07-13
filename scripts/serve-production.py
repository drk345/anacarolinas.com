#!/usr/bin/env python3
"""ALMAVIVA production-parity local preview (Python standard library only).

Serves dist/ over HTTP while applying the EXACT response headers from the
Cloudflare `_headers` file — most importantly the strict Content-Security-Policy.
This makes local QA reproduce production: inline styles / inline scripts that
Cloudflare would strip are blocked here too, so local and deployed rendering
cannot silently diverge.

Workflow:
    bash scripts/build-pages.sh        # produces dist/ (incl. dist/_headers)
    python scripts/serve-production.py # serve dist/ under the production CSP

Usage:
    python scripts/serve-production.py [PORT]   # default port 8099
"""
from __future__ import annotations

import fnmatch
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

DIST = "dist"
HEADERS_FILE = os.path.join(DIST, "_headers")
DEFAULT_PORT = 8099


def parse_headers(path: str):
    """Parse a Cloudflare `_headers` file into [(pattern, [(name, value), ...]), ...]."""
    rules = []
    pattern = None
    hdrs: list[tuple[str, str]] = []
    for raw in open(path, encoding="utf-8").read().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw[0].isspace():                       # a path pattern line
            if pattern is not None:
                rules.append((pattern, hdrs))
            pattern = raw.strip()
            hdrs = []
        elif ":" in raw:                               # an indented "Name: value" line
            name, value = raw.strip().split(":", 1)
            hdrs.append((name.strip(), value.strip()))
    if pattern is not None:
        rules.append((pattern, hdrs))
    return rules


def _matches(pattern: str, path: str) -> bool:
    if pattern == "/*":
        return True
    if pattern == "/":
        return path in ("/", "/index.html")
    if "*" in pattern:
        return fnmatch.fnmatch(path, pattern)
    return pattern == path


def headers_for(path: str, rules) -> dict:
    """Merge all matching rules; later / more-specific rules override earlier ones."""
    out: dict[str, str] = {}
    for pattern, hdrs in rules:
        if _matches(pattern, path):
            for name, value in hdrs:
                out[name] = value
    return out


class ParityHandler(SimpleHTTPRequestHandler):
    rules: list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST, **kwargs)

    def end_headers(self):
        path = self.path.split("?", 1)[0]
        for name, value in headers_for(path, self.rules).items():
            # Content-Type / Content-Length are managed by the base handler.
            if name.lower() in ("content-type", "content-length"):
                continue
            self.send_header(name, value)
        super().end_headers()

    def log_message(self, fmt, *args):  # quieter, prefixed logging
        sys.stderr.write("  " + (fmt % args) + "\n")


def main() -> int:
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port '{sys.argv[1]}', using default {DEFAULT_PORT}.", file=sys.stderr)

    if not os.path.isdir(DIST):
        print(f"ERROR: '{DIST}/' not found. Run first:  bash scripts/build-pages.sh", file=sys.stderr)
        return 2
    if not os.path.isfile(HEADERS_FILE):
        print(f"ERROR: '{HEADERS_FILE}' not found — the build should copy _headers into dist/.", file=sys.stderr)
        return 2

    ParityHandler.rules = parse_headers(HEADERS_FILE)
    csp = next((v for _, hs in ParityHandler.rules for n, v in hs
                if n.lower() == "content-security-policy"), None)

    httpd = HTTPServer(("127.0.0.1", port), ParityHandler)
    print("=" * 72)
    print("ALMAVIVA production-parity preview")
    print(f"  Serving : {os.path.abspath(DIST)}")
    print(f"  URL     : http://127.0.0.1:{port}/")
    print(f"  Headers : applied from {HEADERS_FILE} (production CSP + security + cache)")
    if csp:
        print(f"  CSP     : {csp}")
    print("  This enforces the SAME CSP as Cloudflare: inline styles/scripts are")
    print("  blocked here exactly as in production. Ctrl+C to stop.")
    print("=" * 72)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
