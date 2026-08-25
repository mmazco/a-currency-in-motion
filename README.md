# a currency in motion

> **Draft, for review.** Three figures are still unconfirmed with the team —
> the network count, total moved via USDT0, and how widely USDT is held.
> Treat the copy as provisional. Final version ships as a PR to
> [stellar-docs](https://github.com/stellar/stellar-docs).

Single self-contained pages, no build step — open either HTML file directly,
or use a link below.

## Where to view

| | Live page | Claude artifact |
|---|---|---|
| **The page** — Arrival, Access, Day one, Deploy. The version under review. | [open](https://mmazco.github.io/a-currency-in-motion/usdt0-atlas.html) | [open](https://claude.ai/code/artifact/0c7e58a1-8583-4261-8b89-0026f56e6465) |
| **Palette lab** — the same page with a live colour switcher and contrast readout, for choosing a direction. Not the real thing. | [open](https://mmazco.github.io/a-currency-in-motion/palette-lab.html) | [open](https://claude.ai/code/artifact/8307c388-39a1-4089-8f58-b02d8fcd027c) |

The **live pages** are open to anyone with the link. The **Claude artifacts**
are private until shared from the share menu on each one, but they take
inline comments — use those if you want feedback threaded against the copy.

Source files: [`usdt0-atlas.html`](usdt0-atlas.html) &middot;
[`palette-lab.html`](palette-lab.html)

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
