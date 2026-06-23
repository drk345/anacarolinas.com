from pathlib import Path
import re, sys

root = Path(r'C:\dev\anacarolinas').resolve()
files = [root / 'index.html'] + list((root / 'assets/css').glob('*.css'))
missing = []

for file in files:
    text = file.read_text(encoding='utf-8')
    for ref in re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text):
        if ref.startswith(('#', 'http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        ref = ref.split('?', 1)[0]
        target = (file.parent / ref).resolve()
        if not target.exists():
            missing.append(f"{file.name}: {ref}")

    for ref in re.findall(r'url\(["\']?([^"\')\s]+)["\']?\)', text):
        if ref.startswith(('http://', 'https://', 'data:')):
            continue
        ref = ref.split('?', 1)[0]
        target = (file.parent / ref).resolve()
        if not target.exists():
            missing.append(f"{file.name}: {ref}")

if missing:
    print('FAIL - Missing local references:')
    for m in missing:
        print(f"  {m}")
    sys.exit(1)
print('PASS: no missing local references found')
