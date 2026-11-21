# Sum up 21 November 2026 world news in one image

make.fun bounty: news-image-20261121

Account: @steady-comet-66 (Solana wallet fbmh...o9ER, full address not shown on profile)

Deadline: Mon 23 Nov 2026 07:00 WIB

## How it works

`main.py` is a deterministic Python 3.12 program, standard library
only, no network. It draws a 1024x1024 newspaper front page with its
own 5x7 bitmap font and its own PNG encoder (zlib/struct), and writes `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` locally).

Run locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Design

A newspaper front page: masthead with a "9 STORIES" badge; a lead
story with a cracked-Earth visual, an overtime clock, a thermometer
and a NO DEAL banner, plus a verified quote from the summit
president and a gold fact strip; a "WHERE IT HAPPENED" world-map
strip with numbered dots for the 5 main stories and small numbered
dots for the 4 brief stories (the numbers match the story kickers
and the numbered footer lines); a 2x2 grid of numbered stories
whose icons carry big glanceable numbers (6.8, -3.7%); and a footer
with one numbered line per brief story.

Verified 21 Nov 2026 (afternoon quality pass): two runs write
byte-identical PNGs, SHA256
c74318effad4c29bd91c7e6e958398dacfeb07831b98529b962081be0fbd0334,
1024x1024, 24,610 bytes, ~0.8 s per run.

## Stories in the image (all Sat 21 Nov 2026)

- Lead: COP31 talks miss their deadline and run into overtime —
  no deal; the draft drops all fossil-fuel language and admits
  the world will miss 1.5C; a third draft is due on Saturday
- Three Houthi missiles aimed at Riyadh intercepted early on
  Saturday, the third straight day of alerts in the capital
- Magnitude 6.8 earthquake shakes central Peru (Junín), felt
  320 km away in Lima; no deaths or major damage reported
- Wall Street in correction: S&P 500 down 3.7%, Nasdaq down
  5.28% on Friday; Nvidia fell 13.8%
- NATO chief Mark Rutte heads to Warsaw after Russian missiles
  and a drone crashed in Poland; Warsaw calls it a provocation
- Also: KL Rahul first Indian opener with Test 100s in all SENA
  countries; record foreign-investor inflow into Indian shares;
  Nigeria boat capsize kills at least 4; Trump threatens a tax
  on AI data centres built abroad

Full facts and sources: see NOTES.md. Research notes, including
the stories deliberately excluded as not 21 Nov stories, are in
`../NEWS-RESEARCH.md`.
