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

---

## PR body (paste as-is)

Applies the Stellar Design System to `/launch/usdt0`, and swaps the social card to match.

### What changes

- `@stellar/design-system` v4 stylesheet, consumed rather than recreated
- **Inter** and **Inconsolata** loaded from Google Fonts; IBM Plex Mono dropped. Both verified loading rather than falling back to system fonts
- Every colour in the page's CSS now resolves to an `--sds-*` token. Zero hex values, zero `rgb()`, no colour keywords
- **Lilac is the interactive colour** — links, hovers, focus rings, nav state. Gold is retired from the page
- The hand-built dark palette is gone. SDS owns both themes via `.sds-theme-light` / `.sds-theme-dark`
- Emoji removed from the Soroswap note
- `static/assets/launch/usdt0-og.png` replaced with a lilac card, same filename and dimensions so existing shares pick it up as caches expire

### On the colour

`--sds-clr-gold-09` is `#fdda24` — the exact yellow this page already used. So the accent was always on-system; what changed is its role. The skill reserves gold as an accent and makes lilac the primary interactive colour, and rule 6 specifically warns against carrying stellar.org's marketing style onto product surfaces. On a page that sits beside the docs, Lab and skills, lilac is what makes it look like it belongs.

### Two things to flag rather than have found

**SDS components are not adopted.** Step 1 of the skill asks for SDS components before custom ones; this is a token-level restyle, so the page keeps its own components and only resolves their colours and fonts to SDS variables. There is no SDS `Button`, `Card` or `Badge` here. For a bespoke landing page that seems a reasonable exception, but it is a deviation and worth naming.

**The structured data is still a generated artefact from outside this repo**, which is the same objection raised on #2856. Nothing in this PR improves that — the page is produced by a script that does not live here, so the `FAQPage` and `TechArticle` blocks remain a second copy with no in-repo generator. It is the strongest argument for porting the page to `src/pages/launch/usdt0/index.tsx`, and SDS tokens would be considerably easier to apply there too.

### Checked

- Zero colour values outside tokens
- Inter + Inconsolata actually load
- Both themes readable; toggle verified switching
- Contrast: 0 failures across 118 visible elements in both themes
- One h1, no heading skips
- Addresses in monospace with copy affordances
- No horizontal overflow at 375px

### After merge

The card needs a re-scrape so existing shares refresh: X Card Validator and LinkedIn Post Inspector.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
