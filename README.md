# a currency in motion

> **Draft, for review.** The Access section was rebuilt on 28 Aug and its copy
> has not been through internal review in this form. Two technical notes need
> an engineer's sign-off, and the network count is sourced but unconfirmed —
> see *Where things stand*. Final version ships as a PR to
> [stellar-docs](https://github.com/stellar/stellar-docs).

Single self-contained pages, no build step — open either HTML file directly,
or use a link below.

## Where to view

| | Live page | Claude artifact |
|---|---|---|
| **The page** — Arrival, Access, Day one, Deploy, Before you build. The version under review. | [open](https://mmazco.github.io/a-currency-in-motion/usdt0-atlas.html) | [open](https://claude.ai/code/artifact/bcb22894-4340-4f73-9730-0d4b6adc49fa) |
| **Palette lab** — the same page with a live colour switcher and contrast readout, for choosing a direction. Not the real thing. | [open](https://mmazco.github.io/a-currency-in-motion/palette-lab.html) | [open](https://claude.ai/code/artifact/8307c388-39a1-4089-8f58-b02d8fcd027c) |

The **live pages** are open to anyone with the link. The **Claude artifacts**
are private until shared from the share menu on each one, but they take
inline comments — use those if you want feedback threaded against the copy.

`usdt0-atlas.html` is a copy of `access-lab.html`, which is the file the
artifact publishes from. Edit `access-lab.html`, then copy it across — that
is the only reason two near-identical files exist. The earlier version of the
atlas, with the click-to-open Access panel and Plex Condensed headlines, is in
the history at `c224f9e`.

Source files: [`access-lab.html`](access-lab.html) &middot;
[`usdt0-atlas.html`](usdt0-atlas.html) &middot;
[`palette-lab.html`](palette-lab.html)

## Where things stand

Live. The copy up to 28 Aug went through internal review twice. The Access
section was then rebuilt — all five files shown at once instead of one at a
time — and most of its copy was rewritten after that review, so it is accurate
as far as it has been checked but has not been re-reviewed in this form.
Open items, roughly in order of urgency:

**Waiting on the team**

- **Cumulative volume.** The spec strip shows USDT in circulation ($183B,
  CoinMarketCap). USDT0's own unified supply is $3.4B (analytics.usdt0.to).
  A cumulative-volume figure *with a definition attached* would be better than
  either — ask Everdawn. Do not label circulation as unified supply; the
  dashboard contradicts it in one click.

  Lead: [everdawn.to](https://everdawn.to/) carries a "$100 billion
  transaction volume" milestone headline. That is plausibly the origin of the
  "$100B+ moved" line cut from an earlier draft. It still arrives without a
  definition or a date range, so it needs one before use — but it is a
  concrete thing to ask them about rather than an open question.
- ~~**"USDT is the stablecoin most of the world's crypto users already hold"**~~
  — no longer rendered. It lived in the click-to-open panel copy, which the
  rebuilt Access section does not display. The string is still in `LAYERS` as
  reference data; delete it or get a formulation approved before reusing it.
- **Day one partners.** Kraken is the only exchange listed. Confirm before
  launch, and decide on Bitso, Crypto.com, BiLira.
- **MiCA.** USDT is not MiCA-compliant and the page names European partners.
  In or out of scope for a builder page?

**Verify with engineering** — the two technical notes in *Before you build*

- **Decimals — corrected after dev review, now confirmed.** Stellar USDT0
  carries 7 decimals ([Stellar
  docs](https://developers.stellar.org/docs/learn/fundamentals/stellar-data-structures/assets));
  LayerZero's OFT normalises cross-chain transfers to `sharedDecimals = 6`
  ([OFT
  reference](https://docs.layerzero.network/v2/concepts/technical-reference/oft-reference)).
  The OFT converts automatically: it floors the local amount to the nearest
  multiple and *refunds the dust to the sender before debiting*. So sending
  1.2345678 moves 1.234567 and 0.0000008 stays put. Devs do not convert by
  hand — they need this for amount arithmetic and display only.

  Two errors were caught here. The note first said "6 decimals on Ethereum",
  conflating USDT's token decimals with the OFT's shared-decimals parameter —
  they happen to coincide at 6, which hid the mistake. It also said "convert
  at the boundary", which is wrong: the OFT does it. Both fixed.
- **Route minimums.** "Each USDT0 token may have minimum transfer amounts
  enforced at the contract level. Check `quoteOFT()` for transfer limits on
  specific routes" — USDT0 developer docs. No threshold is published, so the
  note tells the reader to call `quoteOFT()` rather than naming a number.

**Decisions for the author**

- ~~**Spell out PSP?**~~ — moot for now; the line lived in the click-to-open
  panel and is not rendered. Same caveat as above if the copy comes back.
- **Sharpen the Treasury caveat?** The issuer account is locked — sole signer
  at weight 0, verified on Horizon — so there is no single key at all. The
  caveat currently says "behind a multisig rather than a single key", which is
  true but softer than the facts allow.

**Changed on 28 Aug, after the last review**

- **Access rebuilt** — all five files shown at once as columns beneath the
  folder stack, instead of one at a time on click. Ordered by priority:
  payments, treasury, collateral, distribution, liquidity, set in one `ORDER`
  constant the stack and columns both read.
- **New section, *Before you build*** — six requirement and limitation notes,
  sitting after Deploy with its own marker in the nav.
- **Headlines to Inter**, Plex Condensed dropped. See *Type*.
- **A bug worth knowing about.** An orphaned line survived the Access rebuild
  and threw at load, which silently killed the theme toggle — the last block in
  the script. `node --check` passed it, because it was valid syntax and a
  runtime error. Fixed. The lesson: check the console, not just the parser.

**Follow-on work**

- **Blog: the control structure.** SAC `CBSJ…26YF` → admin contract
  `CA3G…YWGJ` → owner `CBCZ…QKR6`, which holds 5 signers; engineering reports
  a 3-of-5 OneSig multisig. The threshold is deliberately not on the landing
  page — it is a parameter that can change.
- **The stellar-docs PR** — see Hosting below.
- **Figma frames** on the *Web Pages* board are all behind this copy.
- **Never *seen* at 375px.** Measured only. The headline was swept from 320px
  to 1300px and holds a three-line shape from 375px up; the columns and notes
  were measured at 980px and 760px. Nobody has looked at it on a phone.

## Palette

The page ships in the **Stellar palette**, light and dark, with a toggle in
the footer. No stored choice means it follows the reader's OS; clicking sets
an explicit override that persists.

| | Light | Dark |
|---|---|---|
| Ground | `#FFFFFF` | `#0F0F0F` |
| Body text | `#0F0F0F` | `#F5F5F0` |
| Accent | `#FDDA24` | `#FDDA24` |
| Accent as **text** | `#7A5C00` | `#FDDA24` |
| Worst contrast | 5.33 | 5.81 |

The whole system is CSS custom properties in `:root`. Three accent roles,
because they are not interchangeable:

- `--accent` — **fills only**, and only areas big enough to read as a shape
- `--accent-ink` — accent-coloured **text, strokes, borders and small marks**
- `--on-accent` — text sitting **on top of** an accent fill

That split is what makes a yellow accent possible at all. `#FDDA24` on white
is about 1.5:1 — fine behind black text, unusable as type or as a hairline.
So in light mode the yellow fills the nav tick and the folder tab, while
anything thin or textual uses the ochre. On black the same yellow reaches
13.9:1 and can do both, which is why dark mode looks bolder.

`palette-lab.html` keeps all five explored directions — Drafting, Stellar,
Studio, and dark variants of the first two — and is not the page. It has not
been updated since the colour decision: it still shows the pre-28-Aug layout
and copy under its switcher. Use it to compare colour, not content.

## Type

| | |
|---|---|
| **Inter** 600 | The h1, folder and file headlines, cover name, diagram labels |
| **Inter** 400/500 | All body copy |
| **IBM Plex Mono** 400/500 | Labels, identifiers, spec strip, sources, folder tabs |

Two families. IBM Plex Sans Condensed carried the headlines until 28 Aug and
has been removed entirely — Inter now does both display and body. That cost
some width: the h1 breaks over three lines where the condensed face took two,
and it needed its own display tuning (tighter tracking at -.03em, a little
more leading for Inter's taller x-height).

Inter matches stellar.org's primary face. Mono carries the page's chrome,
which is what makes it read as a technical document rather than a marketing
page. Both are open source (Inter under the SIL OFL), so nothing blocks
shipping them.

Note the fonts load from `fonts.googleapis.com` — the only thing in these
files that reaches outside. If the docs site self-hosts or forbids
third-party font hosting, that link is the one thing to swap before the PR.

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
