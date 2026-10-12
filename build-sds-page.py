"""Generate the SDS-styled page from access-lab.html.

The SDS variant used to be a one-off hand transform, so every content fix made
after it was built silently missed it. Generating it means the two can never
drift again: content lives in access-lab.html, this file owns only the restyle.

  python3 build-sds-page.py
"""
import html, json, pathlib, re

SRC = pathlib.Path('access-lab.html')
OUT = pathlib.Path('usdt0-sds-lilac.html')
SDS = pathlib.Path('vendor/sds-v4.css')

s = SRC.read_text(encoding='utf-8')

# ---- fonts: SDS is Inter + Inconsolata and ships neither ----
s = s.replace(
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap">',
 '<style>/* @stellar/design-system v4 - inlined; the artifact CSP blocks third-party CSS */\n'
 + SDS.read_text(encoding='utf-8') + '\n</style>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@400;500&family=Inter:wght@400;500;600&display=swap">')
for a, b in [('"IBM Plex Mono",ui-monospace,monospace', 'var(--sds-ff-monospace)'),
             ('"IBM Plex Mono",monospace',              'var(--sds-ff-monospace)'),
             ('"Inter","Helvetica Neue",Arial,sans-serif', 'var(--sds-ff-base)'),
             ('"Inter",Arial,sans-serif',               'var(--sds-ff-base)')]:
    s = s.replace(a, b)

# ---- tokens: one hue. Lilac is SDS's interactive colour; gold is retired. ----
root = re.search(r':root\{.*?\}', s, re.S).group(0)
s = s.replace(root, ':root{\n'
  '  --paper:var(--sds-clr-gray-01); --paper-2:var(--sds-clr-gray-02); --paper-3:var(--sds-clr-gray-03);\n'
  '  --ink:var(--sds-clr-gray-12); --ink-2:var(--sds-clr-gray-11); --ink-3:var(--sds-clr-gray-09);\n'
  '  --rule:var(--sds-clr-gray-06); --rule-2:var(--sds-clr-gray-05);\n'
  '  --accent:var(--sds-clr-lilac-09); --accent-soft:var(--sds-clr-lilac-03);\n'
  '  --accent-ink:var(--sds-clr-lilac-11); --on-accent:var(--sds-clr-gray-01);\n'
  '  --link:var(--sds-clr-lilac-11);\n'
  '}')

# ---- SDS owns both themes; drop the hand-built dark palettes ----
def strip(src, pat):
    spans = []
    for m in re.finditer(pat, src):
        b = src.find('{', m.end() - 1); depth, j = 0, b
        while j < len(src):
            if src[j] == '{': depth += 1
            elif src[j] == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        spans.append((m.start(), j + 1))
    for a, b in reversed(spans):
        src = src[:a] + src[b:]
    return src
s = strip(s, r'@media \(prefers-color-scheme:\s*dark\)\s*\{\s*:root(?!\w)')
s = strip(s, r':root\[data-theme="dark"\]\{')

# the toggle's icon swap keys off the same attributes and must survive the strip
if ':root[data-theme="dark"] .themetog .sun' not in s:
    anchor = ':root:not([data-theme="light"]) .themetog .moon{display:none}'
    s = s.replace(anchor,
        ':root[data-theme="dark"] .themetog .sun{display:block}\n'
        ':root[data-theme="dark"] .themetog .moon{display:none}\n'
        '@media (prefers-color-scheme:dark){\n'
        '  :root:not([data-theme="light"]) .themetog .sun{display:block}\n'
        '  :root:not([data-theme="light"]) .themetog .moon{display:none}\n'
        '}')

s = s.replace('&#128161; ', '')                       # SDS: no emoji as icons
s = s.replace('<title>USDT0 on Stellar</title>', '<title>USDT0 on Stellar — SDS</title>')
s = s.replace("const KEY   = 'usdt0-atlas-theme';", "const KEY   = 'usdt0-sds-theme';")

# ---- interactive state goes lilac; everything else keeps the accent role ----
INTERACTIVE = ('.toplink:hover', '.toplink:focus-visible', '.tick:hover',
               '.tick[aria-current="true"]', '.tick:focus-visible', '.d-back:hover',
               '.d-back:focus-visible', '.sources a:hover', '.sources a:focus-visible',
               '.faq summary:hover .fq', '.faq summary:focus-visible', '.dep-link',
               '.dep-link:focus-visible', '.xlink:hover', '.xlink:focus-visible',
               '.file:hover', '.file:focus-visible', '.file[aria-selected="true"]')
blocks = re.findall(r'<style>(.*?)</style>', s, re.S)
page = max(blocks, key=lambda b: b.count('--paper'))
out, new = [], page
for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', page):
    sel, body = m.group(1), m.group(2)
    key = re.sub(r'\s+', ' ', sel.strip())
    if ('var(--accent-ink)' in body and
        (any(k in key for k in INTERACTIVE) or 'a:hover' in key or 'a:focus-visible' in key)):
        out.append((m.start(), m.end(), sel + '{' + body.replace('var(--accent-ink)', 'var(--link)') + '}'))
for a, b, rep in reversed(out):
    new = new[:a] + rep + new[b:]
s = s.replace(page, new)
# footer controls set their own colour and were below AA on dark
s = s.replace('text-transform:inherit;color:var(--ink-3)', 'text-transform:inherit;color:var(--ink-2)')
s = s.replace('.xlink{\n  display:inline-flex;align-items:center;color:var(--ink-3);\n}',
              '.xlink{\n  display:inline-flex;align-items:center;color:var(--ink-2);\n}')

# ---- SDS v4 themes are classes, not a data-theme attribute ----
head = ('<script>(function(){try{'
 "var k=localStorage.getItem('usdt0-sds-theme')||localStorage.getItem('theme');"
 "var d=k?k==='dark':matchMedia('(prefers-color-scheme: dark)').matches;"
 "document.documentElement.classList.add(d?'sds-theme-dark':'sds-theme-light');"
 'if(k)document.documentElement.dataset.theme=k;'
 "}catch(e){document.documentElement.classList.add('sds-theme-light')}})()</script>\n")
bridge = ('\n<script>\n'
 '// SDS v4 switches themes with classes; the page\'s toggle writes data-theme,\n'
 '// so mirror one onto the other.\n'
 '(function(){\n'
 "  const root=document.documentElement, mq=matchMedia('(prefers-color-scheme: dark)');\n"
 "  const apply=()=>{const e=root.dataset.theme, dark=e?e==='dark':mq.matches;\n"
 "    root.classList.toggle('sds-theme-dark',dark); root.classList.toggle('sds-theme-light',!dark);};\n"
 "  new MutationObserver(apply).observe(root,{attributes:true,attributeFilter:['data-theme']});\n"
 "  mq.addEventListener('change',apply); apply();\n"
 '})();\n</script>\n')

OUT.write_text(head + s.rstrip() + bridge, encoding='utf-8')
hexes = re.findall(r'#[0-9a-fA-F]{3,8}\b', max(re.findall(r'<style>(.*?)</style>', OUT.read_text(encoding='utf-8'), re.S), key=lambda b: b.count('--paper')))
print(f'wrote {OUT} ({OUT.stat().st_size:,} bytes)  non-token hex in page CSS: {len(hexes)}')
