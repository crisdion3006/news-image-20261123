# The World in Five Frames — 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/crisdion3006/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/crisdion3006/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A make.fun entry: one image summing up the world's news of Monday
23 November 2026, drawn entirely in code.

## The image

A light-paper storyboard — five numbered pastel frames, each with a
small hand-drawn glyph, plus an also-today ticker along the bottom:

1. **Shenzhen, the summit** — Trump, Putin and Xi meet and issue a
   "Declaration toward Peace" on the APEC sidelines.
2. **COP31 fails** — talks collapse as the EU rejects any deal
   without fossil-fuel phase-out language.
3. **Kyiv** — a 7-year-old boy, David, is pulled alive from rubble
   after 14 hours trapped; 10 killed in the Russian drone strike.
4. **Riemann Hypothesis?** — an Anthropic mathematician and Claude
   claim to have proved the 160-year-old problem.
5. **Football** — Liverpool 4–0 Man United on Pochettino's debut;
   Alcaraz wins his first ATP Finals title.

Also today: South Korea exports top $1T, a Russian frigate sinks in
Benghazi, Democrats win big.

## How it is built

`build_image.py` (Python 3, Pillow only) draws `entry.png` from fixed
coordinates — no network, no randomness, no timestamps, so two runs
are byte-identical. `main.ts` (Node 22, stdlib only) copies that
image to `/output/entry.png`.

```sh
python3 build_image.py   # writes entry.png (1024x1024, < 1 MiB)
node main.ts             # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
