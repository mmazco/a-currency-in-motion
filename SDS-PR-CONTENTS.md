# SDS PR — what goes in it

Push **after** #2856 (the FAQ) merges, so the generated page carries the FAQ
and the diff stays restyle-only.

## Files

| path in stellar-docs | source here | note |
|---|---|---|
| `static/launch/usdt0.html` | regenerate with `build-docs-page.py` | SDS tokens, fonts, theme classes |
| `static/assets/launch/usdt0-og.png` | `usdt0-og.png` | lilac card, same name and 2400x1260, so existing shares pick it up |

## What changes on the page

- `@stellar/design-system` v4 stylesheet (CDN link in the docs copy)
- Inter + Inconsolata loaded from Google Fonts; IBM Plex Mono dropped
- All 12 local colour variables resolve to `--sds-*` tokens; zero hex, zero rgb()
- Lilac is the interactive colour (`--link` -> `lilac-11`); gold retired
- `.sds-theme-light` / `.sds-theme-dark` classes replace the hand-built dark palette,
  bridged to the page's existing toggle
- Emoji removed from the Soroswap note (SDS forbids emoji as icons)

## Declare in the PR body

SDS *components* are not adopted — this is a token-level restyle. Step 1 of the
skill asks for SDS components first; a bespoke landing page is a reasonable
exception, but say it rather than let a reviewer find it.

## After merge

Re-scrape the card so existing shares refresh:
- X: https://cards-dev.twitter.com/validator
- LinkedIn: https://www.linkedin.com/post-inspector/
