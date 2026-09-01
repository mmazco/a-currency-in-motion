#!/usr/bin/env python3
"""Move the JS-generated markup into the HTML.

Elliot's point on stellar-docs#2807: with JS off, the contract addresses,
the file stack, the benefit columns and the requirement notes all render as
empty boxes — which is most of the page, and it affects how agents and
crawlers read it.

Rather than hand-transcribe, this takes Chrome's own render of the page and
splices those five containers back into the source as static markup, then
deletes the code that built them. What ships is exactly what the browser was
producing.
"""
import re, subprocess, pathlib, sys

SRC = pathlib.Path('access-lab.html')
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CONTAINERS = ['stack', 'files', 'desc', 'ids', 'notes']

def render(path):
    out = subprocess.run([CHROME, '--headless', '--disable-gpu',
                          '--virtual-time-budget=3000', '--dump-dom',
                          f'file://{pathlib.Path(path).resolve()}'],
                         capture_output=True, text=True)
    if not out.stdout.strip():
        sys.exit('empty render')
    return out.stdout

def grab(dom, cid):
    """The element with this id, balanced to its closing tag."""
    m = re.search(rf'<(\w+)([^>]*\bid="{cid}"[^>]*)>', dom)
    if not m: sys.exit(f'{cid} not in render')
    tag, i = m.group(1), m.end()
    depth, pos = 1, i
    for t in re.finditer(rf'</?{tag}\b[^>]*>', dom[i:]):
        depth += -1 if t.group(0).startswith('</') else 1
        if depth == 0:
            pos = i + t.end(); break
    return m.group(0), dom[i:pos - len(f'</{tag}>')], dom[m.start():pos]

dom = render(SRC)
s = SRC.read_text()

for cid in CONTAINERS:
    opentag, inner, whole = grab(dom, cid)
    # the source has the same element, empty
    pat = re.compile(rf'<(\w+)([^>]*\bid="{cid}"[^>]*)>\s*</\1>')
    m = pat.search(s)
    if not m:
        sys.exit(f'{cid}: no empty container in source to fill')
    s = s[:m.start()] + whole + s[m.end():]
    print(f'  filled #{cid}  ({len(inner):,} bytes of markup)')

SRC.write_text(s)
print('\n  containers filled — generator code still present, removed next')
