# USDT0 visuals

> **Draft, for review.** Three figures are still unconfirmed with the team —
> the network count, total moved via USDT0, and how widely USDT is held.
> Treat the copy as provisional. Final version ships as a PR to
> [stellar-docs](https://github.com/stellar/stellar-docs).

Single self-contained pages, no build step. Open the HTML file directly.

| File | What it is |
|---|---|
| `usdt0-atlas.html` | The page. Currently out for review. |
| `palette-lab.html` | Same page + a live palette switcher, for choosing a colour direction. Not for sharing as the real thing. |

## Palette

The whole colour system is CSS custom properties in `:root` — a theme is
about a dozen values. Three accent roles, because they are not
interchangeable:

- `--accent` — fills, strokes, borders
- `--accent-ink` — accent-coloured **text** on the page ground
- `--on-accent` — text sitting **on top of** an accent fill

That split exists so a palette can use a colour that works as a fill but
not as type. Stellar's brand yellow `#FDDA24` is the case in point: fine
behind black text, unusable as a link colour.

## Contrast

Every candidate palette clears WCAG AA (4.5:1) on body text, secondary
text, small labels, accent text, and text-on-accent. The lab shows those
five ratios live for whichever theme is active — check it before changing
any colour. An earlier version shipped `--ink-3` at 3.54:1, which failed.

## Hosting

Target is `developers.stellar.org/releases/usdt0`, served as a static file
from the `stellar-docs` repo (`static/releases/usdt0/index.html`).
That repo is Docusaurus with `baseUrl: "/"`, so `static/` lands at the site
root and the page ships as-is — no port to MDX, no docs chrome.

## Credits

The visual language — the drafting-paper ground, the hairline figure
chrome, the isometric-atlas approach to the diagrams and the animated
flow markers — draws on
[inkboard/system-atlas](https://github.com/inkboard/system-atlas).
