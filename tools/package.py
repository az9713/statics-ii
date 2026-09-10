"""Validate the standalone reading edition and refresh the offline ZIP."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent.parent

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.counts = Counter()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'script':
            raise AssertionError('Unexpected script dependency')
        if tag in ('img', 'iframe', 'link') and any(
            a.get(k, '').startswith(('http:', 'https:', '//')) for k in ('src', 'href')
        ):
            raise AssertionError('Unexpected remote asset')
        if tag in ('figure', 'mjx-container'):
            self.counts[tag] += 1
        for cls in a.get('class', '').split():
            if cls in ('lecture', 'reading', 'problem', 'prop'):
                self.counts[cls] += 1

def main():
    html = sorted(ROOT.glob('*.html'))
    docs = {p.name: Document(p.read_text(encoding='utf-8')) for p in html}
    assert len(html) == 9
    for name, doc in docs.items():
        assert len(doc.ids) == len(set(doc.ids)), f'Duplicate ID: {name}'
        for href in doc.links:
            u = urlsplit(href)
            if u.scheme or u.netloc:
                assert u.scheme in ('http', 'https'), f'Unexpected URL: {href}'
                continue
            target = (ROOT / unquote(u.path)).resolve() if u.path else ROOT / name
            assert target.is_relative_to(ROOT), 'Link leaves public package'
            if target.name != 'statics-ii-course.zip':
                assert target.is_file(), f'Missing link: {name}: {href}'
            if u.fragment and target.suffix == '.html':
                assert unquote(u.fragment) in docs[target.name].ids, f'Missing anchor: {href}'
    expected = {'lecture':30, 'reading':55, 'problem':75, 'figure':53,
                'mjx-container':376, 'prop':15}
    assert dict(docs['complete-course.html'].counts) == expected
    for p in html:
        content = p.read_text(encoding='utf-8')
        assert not re.search(r'[A-Z]:[\\/]|file:///|/Users/|/home/',content), 'Local path found'
        assert not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN .{0,20}PRIVATE KEY',content), 'Secret-like string found'
        assert 'data-math-slot' not in content and '<mjx-merror' not in content
    receipt = """STATICS II — PUBLIC READING EDITION

30 lecture chapters; 55 reading entries; 75 solved problems;
53 engineering figures; 376 rendered equations; 15 derivation blocks.

PUBLIC PACKAGE CHECKS
All local page links and fragments resolve; no duplicate IDs.
No runtime scripts or remote assets are required.
The complete textbook matches the expected chapter and content inventories.
The archive contains the exact HTML, verification, and third-party notice files.
SHA-256 hashes of the public HTML appear below.

EDITORIAL AUDIT
The preceding course audit reported 1908 structural/link/equilibrium checks,
237 revision assertions, and 64 successful static skill-script runs.
These historical audit checks are not rerun by this public packaging script.
This public export preserves the lecture material, equations, and diagrams;
branding and administrative descriptions were edited for independent sharing.
Standalone SVG figures were raster-inspected during the preceding audit.

LIMITS
Browser layout, animation, responsive, and print behavior remain unverified.
Static package checks are not independent peer review of the mathematics.
No equivalence to unseen third-party course materials is claimed.

REPACKAGE
Run python tools/package.py from the repository root after editing the HTML.

HTML SHA-256
"""
    receipt += '\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in html)+'\n'
    (ROOT/'verification.txt').write_text(receipt,encoding='utf-8',newline='\n')
    items = html + [ROOT/'verification.txt'] + sorted((ROOT/'third-party').glob('*'))
    archive = ROOT/'statics-ii-course.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in items:
            z.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p in items:
            assert z.read(p.relative_to(ROOT).as_posix()) == p.read_bytes()
    print(json.dumps({'pages':len(html),'inventory':expected,'zip_bytes':archive.stat().st_size},indent=2))

if __name__ == '__main__':
    main()
