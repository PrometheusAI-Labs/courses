#!/usr/bin/env python3
"""Validate local page/asset links and avoid publishing machine-local data."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
checked = 0

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.links.append(value)

for page in ROOT.rglob('*.html'):
    if '.git' in page.parts or 'modules' in page.parts or page.name.startswith('_') or page.name == 'template.html':
        continue
    parser = Links()
    parser.feed(page.read_text())
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (page.parent / unquote(url.path)).resolve()
        checked += 1
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f'{page.relative_to(ROOT)}: missing or escaping link {link}')

secret = re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    if path.name.startswith('.env') or path.suffix in ('.pem', '.key'):
        errors.append(f'Forbidden file: {path.relative_to(ROOT)}')
    text = path.read_text(errors='replace')
    if secret.search(text):
        errors.append(f'Potential credential: {path.relative_to(ROOT)}')
    if str(Path.home()) + '/' in text or 'file:' + '///' in text:
        errors.append(f'Machine-local path: {path.relative_to(ROOT)}')

for error in errors:
    print(error)
print(f'Checked {checked} local links, {len(errors)} errors')
sys.exit(bool(errors))
