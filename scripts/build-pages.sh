#!/usr/bin/env bash
set -euo pipefail

# Build a clean Cloudflare Pages output containing ONLY public website files.
# Internal source/copy/review material (content/, source/, tools/, etc.) is
# deliberately excluded so it never reaches the public deploy.

rm -rf dist
mkdir -p dist

# Public HTML pages
cp ./*.html dist/

# Public assets
if [ -d assets ]; then
  cp -R assets dist/assets
  # Remove unused/development CSS files that are not linked by any page
  rm -f dist/assets/css/home.css dist/assets/css/prototype.css dist/assets/css/styles.css
fi

# Optional Cloudflare / static root files, if present
for file in _headers _redirects robots.txt sitemap.xml favicon.svg favicon.ico site.webmanifest; do
  if [ -f "$file" ]; then
    cp "$file" "dist/$file"
  fi
done

# Safety: ensure no internal folder was copied into dist
for forbidden in content source docs reports tools .git .claude node_modules out; do
  if [ -e "dist/$forbidden" ]; then
    echo "ERROR: forbidden internal path copied into dist: $forbidden"
    exit 1
  fi
done

# Secure-by-design gate (fail closed): reject inline styles/scripts, on* handlers,
# javascript:/http:/external resources, unsafe embeds, and any weakened CSP before
# the build can succeed. See scripts/check-security.py and docs/SECURE-DEVELOPMENT.md.
python scripts/check-security.py dist || {
  echo "BUILD ABORTED: security check failed (see violations above)."
  exit 1
}

echo "Build complete: dist/"
find dist -maxdepth 2 -type f | sort
