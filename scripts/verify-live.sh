#!/usr/bin/env bash
# ALMAVIVA live-deployment security & version verification.
#
# Fetches the deployed site with a unique cache-busting query and confirms the
# production CSP, the absence of inline styles / executable inline scripts,
# versioned asset references, and that deployed CSS matches local source.
#
# Usage:
#   bash scripts/verify-live.sh [BASE_URL]
# Default BASE_URL: https://anacarolinas-com.pages.dev
#
# Exit code is non-zero if any check fails.

set -uo pipefail

BASE="${1:-https://anacarolinas-com.pages.dev}"
BASE="${BASE%/}"
CB="cb=$(date +%s%N)"
FAIL=0

PAGES=(index.html intensivo.html)

note() { printf '%s\n' "$*"; }
ok()   { printf '  [ok]   %s\n' "$*"; }
bad()  { printf '  [FAIL] %s\n' "$*"; FAIL=1; }

note "ALMAVIVA live verification"
note "  target: $BASE"
note "======================================================================"

# --- 1. CSP + security headers (from the site root) ---
note "CSP / security headers:"
HDRS="$(curl -sSIL "$BASE/?$CB" 2>/dev/null)"
CSP="$(printf '%s' "$HDRS" | grep -i '^content-security-policy:' | tail -1 | sed 's/\r$//')"
if [ -z "$CSP" ]; then
  bad "no Content-Security-Policy header present"
else
  ok "Content-Security-Policy present"
  printf '%s' "$CSP" | grep -qi "default-src 'self'"  && ok "default-src 'self'"  || bad "default-src 'self' missing"
  printf '%s' "$CSP" | grep -qi "style-src 'self'"    && ok "style-src 'self'"    || bad "style-src 'self' missing"
  printf '%s' "$CSP" | grep -qi "script-src 'self'"   && ok "script-src 'self'"   || bad "script-src 'self' missing"
  printf '%s' "$CSP" | grep -qi "object-src 'none'"   && ok "object-src 'none'"   || bad "object-src 'none' missing"
  if printf '%s' "$CSP" | grep -qi "unsafe-inline"; then bad "CSP contains unsafe-inline"; else ok "no unsafe-inline"; fi
  if printf '%s' "$CSP" | grep -qi "unsafe-eval";   then bad "CSP contains unsafe-eval";   else ok "no unsafe-eval";   fi
fi

# --- 2. Per-page HTML checks ---
for page in "${PAGES[@]}"; do
  note ""
  note "$page:"
  BODY="$(curl -sSL "$BASE/$page?$CB" 2>/dev/null)"
  if [ -z "$BODY" ]; then bad "empty response for $page"; continue; fi

  N_STYLE="$(printf '%s' "$BODY" | grep -oE 'style="[^"]*"' | wc -l | tr -d ' ')"
  [ "$N_STYLE" = "0" ] && ok "0 inline style attributes" || bad "$N_STYLE inline style attribute(s)"

  # inline <script> without src, excluding non-executable JSON-LD data blocks
  N_SCRIPT="$(printf '%s' "$BODY" | grep -oE '<script[^>]*>' | grep -v 'src=' | grep -vi 'application/ld+json' | wc -l | tr -d ' ')"
  [ "$N_SCRIPT" = "0" ] && ok "0 executable inline scripts" || bad "$N_SCRIPT executable inline script(s)"

  printf '%s' "$BODY" | grep -qE '\.css\?v=[0-9]+' && ok "references versioned CSS (?v=)" || bad "no versioned CSS reference"
  printf '%s' "$BODY" | grep -qE '\.js\?v=[0-9]+'  && ok "references versioned JS (?v=)"  || bad "no versioned JS reference"

  # CSS hash: compare each locally-known linked stylesheet against the deployed copy
  for cssref in $(printf '%s' "$BODY" | grep -oE 'assets/css/[A-Za-z0-9._-]+\.css' | sort -u); do
    if [ -f "$cssref" ]; then
      DHASH="$(curl -sSL "$BASE/$cssref?$CB" 2>/dev/null | tr -d '\r' | sha256sum | cut -d' ' -f1)"
      LHASH="$(tr -d '\r' < "$cssref" | sha256sum | cut -d' ' -f1)"
      if [ "$DHASH" = "$LHASH" ]; then ok "CSS hash match: $cssref"; else bad "CSS hash MISMATCH: $cssref (deployed != local)"; fi
    else
      note "  [skip] $cssref not found locally (cannot hash-compare)"
    fi
  done
done

note ""
note "======================================================================"
if [ "$FAIL" = "0" ]; then
  note "LIVE VERIFICATION PASSED"
else
  note "LIVE VERIFICATION FAILED"
fi
exit "$FAIL"
