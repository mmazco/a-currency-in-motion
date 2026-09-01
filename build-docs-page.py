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
import re, pathlib

SRC  = pathlib.Path('access-lab.html')
OUT  = pathlib.Path('usdt0-launch.html')
URL  = 'https://developers.stellar.org/launch/usdt0'
GTM  = 'GTM-M2JLH37'
GA4  = 'G-ZCT4GYX8KN'
FONT_DIR = '/assets/launch/fonts'

s = SRC.read_text()

# --- split the fragment into head and body at the single </style> ---
assert s.count('</style>') == 1
head, body = s.split('</style>', 1)
head += '</style>'
assert body.lstrip().startswith('<div class="sheet">')

# --- self-hosted faces replace the Google Fonts links ---
gf = re.search(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?'
               r'&display=swap">\n', head, re.S)
assert gf, 'Google Fonts block not found'
faces = pathlib.Path('fonts/faces.css').read_text().strip()
head = head.replace(gf.group(0), f'<style>\n{faces}\n</style>\n')
assert 'fonts.googleapis.com' not in head and 'fonts.gstatic.com' not in head

# --- on the docs domain these are same-origin, so drop the hostname ---
head = head.replace('https://developers.stellar.org/img/docusaurus/favicon-96x96.png',
                    '/img/docusaurus/favicon-96x96.png')

# --- this copy has a permanent address ---
head = head.replace('<meta name="twitter:card" content="summary">',
    f'<meta name="twitter:card" content="summary">\n'
    f'<meta property="og:url" content="{URL}">\n'
    f'<link rel="canonical" href="{URL}">')

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

OUT.write_text(
 '<!doctype html>\n<html lang="en">\n<head>\n'
 + head.strip() + '\n' + gtm_head + '\n'
 + '</head>\n<body>\n' + gtm_body + '\n'
 + body.strip() + '\n</body>\n</html>\n')
print(f'wrote {OUT} ({OUT.stat().st_size:,} bytes)')
