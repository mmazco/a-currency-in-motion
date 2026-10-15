#!/usr/bin/env python3
"""Build the stellar-docs copy of the page from access-lab.html.

The docs copy differs from the artifact/Pages copy in three ways, all of them
consequences of where it is hosted:

  * fonts are self-hosted. developers.stellar.org makes no third-party font
    requests, and this page should not be the one that starts.
  * Google Tag Manager and GA4 are inlined. Docusaurus injects these at build
    time on every page it renders; a file in static/ bypasses the build, so
    without this the page is invisible in their reporting. Same IDs as the
    rest of the site, so this is parity, not a new tracker.
  * a full document skeleton, canonical and og:url, because this one has a
    permanent address.

Everything else is byte-identical to access-lab.html.
"""
import html, json, re, pathlib

SRC  = pathlib.Path('access-lab.html')
OUT  = pathlib.Path('usdt0-launch.html')
URL  = 'https://developers.stellar.org/launch/usdt0'
GTM  = 'GTM-M2JLH37'
GA4  = 'G-ZCT4GYX8KN'
FONT_DIR = '/assets/launch/fonts'

s = SRC.read_text()

# --- split head from body at the LAST </style> ---
# The page carries two stylesheets now: the inlined Stellar Design System and
# the page's own. Splitting on the first would cut the head in the wrong place.
assert s.count('</style>') == 2, f"expected 2 style blocks, found {s.count('</style>')}"
cut = s.rindex('</style>') + len('</style>')
head, body = s[:cut], s[cut:]
assert body.lstrip().startswith('<div class="sheet">')

# --- self-hosted faces replace the Google Fonts links ---
# Matched narrowly: the SDS <style> sits between the preconnects and the font
# link, and a greedy span would swallow it.
pre = re.search(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
                r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n', head)
assert pre, 'font preconnects not found'
gf = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">\n', head)
assert gf, 'Google Fonts link not found'
faces = pathlib.Path('fonts/faces.css').read_text().strip()
head = head.replace(pre.group(0), '')
head = head.replace(gf.group(0), f'<style>\n{faces}\n</style>\n')
assert 'fonts.googleapis.com' not in head and 'fonts.gstatic.com' not in head

# --- on the docs domain these are same-origin, so drop the hostname ---
head = head.replace('https://developers.stellar.org/img/docusaurus/favicon-96x96.png',
                    '/img/docusaurus/favicon-96x96.png')

# --- this copy has a permanent address ---
CARD = '<meta name="twitter:card" content="summary_large_image">'
assert CARD in head, "twitter:card anchor missing - canonical would be skipped"
head = head.replace(CARD,
    f'{CARD}\n'
    f'<meta property="og:url" content="{URL}">\n'
    f'<link rel="canonical" href="{URL}">')

# Structured data: tells a machine what this page is, so search and AI
# systems have something unambiguous to cite rather than inferring it.
LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "USDT0 on Stellar",
    "description": "A guide to USDT0 on Stellar: how it arrives, what it "
                   "unlocks, which partners support it, and how to integrate.",
    "url": URL,
    "datePublished": "2026-09-01",
    "inLanguage": "en",
    "about": {"@type": "Thing", "name": "USDT0 on Stellar Network"},
    "publisher": {"@type": "Organization", "name": "Stellar Development Foundation",
                  "url": "https://stellar.org"},
}, separators=(',', ':'))
head = head.replace('</title>',
    f'</title>\n<script type="application/ld+json">{LD}</script>', 1)

# FAQPage schema, derived from the FAQ markup rather than written out again, so
# the structured data cannot drift from what the page actually says. This is the
# format search and AI systems read for direct answers.
def _text(fragment):
    t = re.sub(r'<[^>]+>', '', fragment)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()

qa = []
for block in re.findall(r'<details class="faq">(.*?)</details>', body, re.S):
    q = re.search(r'<span class="fq">(.*?)</span>', block, re.S)
    a = re.search(r'<div class="fa">(.*?)</div>', block, re.S)
    if q and a:
        qa.append({
            "@type": "Question",
            "name": _text(q.group(1)),
            "acceptedAnswer": {"@type": "Answer", "text": _text(a.group(1))},
        })

if qa:
    FAQ_LD = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "url": URL,
        "mainEntity": qa,
    }, separators=(',', ':'))
    head = head.replace('</title>',
        f'</title>\n<script type="application/ld+json">{FAQ_LD}</script>', 1)
    print(f"  FAQPage schema: {len(qa)} questions")

gtm_head = (
 "<!-- Google Tag Manager: same container the rest of developers.stellar.org "
 "loads. Inlined because static/ files skip the Docusaurus build. -->\n"
 "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':"
 "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],"
 "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
 "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;"
 f"f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');</script>\n"
 f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>\n'
 "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}\n"
 f"gtag('js',new Date());gtag('config','{GA4}',{{anonymize_ip:true}});</script>"
)
gtm_body = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}"\n'
            f'  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>')

# Links to developers.stellar.org are internal once the page is served from
# that host, so they become root-relative and open in the same tab. The source
# keeps absolute URLs because the artifact and GitHub Pages copies live on
# other hosts, where a root-relative path would break.
body = re.sub(r"<a href='https://developers\.stellar\.org(/[^']*)'[^>]*>",
              lambda m: "<a href='" + m.group(1) + "'>", body)
body = re.sub(r'<a href="https://developers\.stellar\.org(/[^"]*)"[^>]*>',
              lambda m: '<a href="' + m.group(1) + '">', body)

OUT.write_text(
 '<!doctype html>\n<html lang="en">\n<head>\n'
 + head.strip() + '\n' + gtm_head + '\n'
 + '</head>\n<body>\n' + gtm_body + '\n'
 + body.strip() + '\n</body>\n</html>\n')
print(f'wrote {OUT} ({OUT.stat().st_size:,} bytes)')
