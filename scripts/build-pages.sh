#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

# Public HTML pages
cp ./*.html dist/

# Public assets
if [ -d assets ]; then
  cp -R assets dist/assets
fi

# Optional Cloudflare/static files if present
for file in _headers _redirects robots.txt sitemap.xml favicon.ico site.webmanifest; do
  if [ -f "$file" ]; then
    cp "$file" "dist/$file"
  fi
done

# Safety: do not copy internal source folders
for forbidden in content source docs reports tools .git .claude node_modules out; do
  if [ -e "dist/$forbidden" ]; then
    echo "ERROR: forbidden internal path copied into dist: $forbidden"
    exit 1
  fi
done

echo "Build complete: dist/"
find dist -maxdepth 2 -type f | sort
