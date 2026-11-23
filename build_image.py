#!/usr/bin/env python3
"""news-image-20261123 -- gradient hero + 2x2 card grid poster.

Draws the 23 November 2026 world-news poster with Pillow only.
Layout: full-bleed indigo-to-orange vertical gradient, a giant faded
"23" behind a huge white hero headline, three leader dots, a 2x2 grid
of white story cards, and a dark ticker strip at the bottom.
Everything uses fixed coordinates and fixed text, so every run
produces byte-identical output.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Vertical gradient stops: (position 0..1, RGB).
STOPS = [
    (0.00, (26, 15, 66)),
    (0.28, (74, 30, 138)),
    (0.52, (146, 36, 128)),
    (0.74, (196, 52, 96)),
    (0.92, (228, 84, 48)),
    (1.00, (238, 96, 42)),
]

WHITE = (255, 255, 255)
INK = (18, 18, 26)
SUB = (96, 96, 108)
TICKER_BG = (18, 13, 46)
TICKER_ACCENT = (245, 122, 40)


def load(path, size):
    return ImageFont.truetype(path, size)


def blend(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def gradient_image():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        pos = y / (H - 1)
        colour = STOPS[-1][1]
        for i in range(len(STOPS) - 1):
            p0, col0 = STOPS[i]
            p1, col1 = STOPS[i + 1]
            if p0 <= pos <= p1:
                t = 0.0 if p1 == p0 else (pos - p0) / (p1 - p0)
                colour = blend(col0, col1, t)
                break
        for x in range(W):
            px[x, y] = colour
    return img


def tracked_len(draw, text, font, tracking):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=font) + tracking
    return total - tracking if text else 0


def draw_tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def fit_size(draw, text, start, max_w, tracking=0):
    size = start
    while size > 10:
        fnt = load(BOLD, size)
        if tracked_len(draw, text, fnt, tracking) <= max_w:
            return fnt
        size -= 2
    return load(BOLD, 10)


def wrap_lines(draw, text, font, widths):
    """Greedy wrap; widths is a list of max widths, one per line
    (the last width repeats for any further lines)."""
    words = text.split()
    lines = []
    current = ""
    li = 0
    for word in words:
        trial = word if not current else current + " " + word
        limit = widths[min(li, len(widths) - 1)]
        if draw.textlength(trial, font=font) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
                li += 1
            current = word
    if current:
        lines.append(current)
    return lines


def draw_sun(draw, cx, cy, r, colour, slash=(214, 32, 24)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    for k in range(8):
        ang = k * math.pi / 4.0
        x1 = cx + int((r + 4) * 0.94 * math.cos(ang))
        y1 = cy + int((r + 4) * 0.94 * math.sin(ang))
        x2 = cx + int((r + 14) * math.cos(ang))
        y2 = cy + int((r + 14) * math.sin(ang))
        draw.line([x1, y1, x2, y2], fill=colour, width=4)
    draw.line([cx - r - 12, cy + r + 12, cx + r + 12, cy - r - 12],
              fill=slash, width=6)


def draw_house(draw, x, y, s, colour):
    draw.polygon([(x, y + s * 0.55), (x + s / 2, y), (x + s, y + s * 0.55)],
                 fill=colour)
    draw.rectangle([x + s * 0.08, y + s * 0.5, x + s * 0.92, y + s],
                   fill=colour)
    draw.rectangle([x + s * 0.4, y + s * 0.68, x + s * 0.6, y + s],
                   fill=WHITE)


def draw_ball(draw, cx, cy, r, colour):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    pts = []
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        pts.append((cx + int(r * 0.45 * math.cos(ang)),
                    cy + int(r * 0.45 * math.sin(ang))))
    draw.polygon(pts, fill=WHITE)
    for (px_, py_) in pts:
        draw.line([cx, cy, px_, py_], fill=WHITE, width=3)


def draw_card(draw, x, y, w, h, accent, label, icon, headline, subline):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=WHITE)
    # Accent strip: rounded top corners, square bottom edge.
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=18, fill=accent)
    draw.rectangle([x, y + 12, x + w, y + 30], fill=WHITE)
    labelfont = load(BOLD, 19)
    draw_tracked(draw, (x + 22, y + 30), label, labelfont, accent, 3)
    icon(x + w - 88, y + 26)
    headfont = load(BOLD, 29)
    lines = wrap_lines(draw, headline, headfont, [w - 44 - 84, w - 44])
    hy = y + 58
    for line in lines[:2]:
        draw.text((x + 22, hy), line, font=headfont, fill=INK)
        hy += 36
    subfont = load(REG, 19)
    sublines = wrap_lines(draw, subline, subfont, [w - 44])
    sy = hy + 10
    for line in sublines[:2]:
        draw.text((x + 22, sy), line, font=subfont, fill=SUB)
        sy += 25


def main():
    img = gradient_image()
    draw = ImageDraw.Draw(img)

    # Giant faded "23" behind the hero, cut off at the right edge.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    big = load(BOLD, 460)
    odraw.text((540, 35), "23", font=big, fill=(255, 255, 255, 40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Masthead + kicker.
    draw_tracked(draw, (40, 42), "MONDAY \u2022 23 NOVEMBER 2026",
                 load(BOLD, 29), WHITE, 4)
    draw_tracked(draw, (40, 100), "SHENZHEN \u2014 THE SUMMIT",
                 load(BOLD, 24), (235, 235, 245), 5)

    # Hero headline, fitted to the canvas width.
    hero = ["THREE LEADERS,", "ONE DECLARATION"]
    hfont = fit_size(draw, max(hero, key=len), 100, 940)
    hy = 140
    for line in hero:
        draw.text((40, hy), line, font=hfont, fill=WHITE)
        hy += 106

    # Hero subline.
    subfont = load(REG, 29)
    sublines = wrap_lines(
        draw,
        "Trump, Putin and Xi meet in Shenzhen and issue a "
        "'Declaration toward Peace' on the APEC sidelines.",
        subfont, [940])
    sy = 360
    for line in sublines:
        draw.text((40, sy), line, font=subfont, fill=(245, 245, 250))
        sy += 38

    # Three leader dots: T (red), P (navy), X (gold).
    dots = [(76, (212, 43, 30), "T"), (146, (30, 42, 120), "P"),
            (216, (245, 166, 35), "X")]
    dotfont = load(BOLD, 34)
    for cx, colour, letter in dots:
        draw.ellipse([cx - 36, 426, cx + 36, 498], fill=colour)
        lw = draw.textlength(letter, font=dotfont)
        bb = dotfont.getbbox(letter)
        lh = bb[3] - bb[1]
        draw.text((cx - lw / 2, 462 - lh / 2 - 2), letter,
                  font=dotfont, fill=WHITE)

    # 2x2 grid of white story cards.
    cw, ch = 462, 196
    cards = [
        (36, 520, (232, 93, 31), "CLIMATE \u2022 COP31",
         lambda bx, by: draw_sun(draw, bx + 32, by + 32, 20, (232, 93, 31)),
         "COP31 fails to reach a deal",
         "Talks collapse as the EU rejects a deal without "
         "fossil-fuel phase-out language."),
        (526, 520, (43, 95, 217), "UKRAINE \u2022 KYIV",
         lambda bx, by: draw_house(draw, bx, by, 62, (43, 95, 217)),
         "Boy, 7, pulled alive from rubble",
         "David is rescued after 14 hours trapped; 10 killed in "
         "the Russian drone strike."),
        (36, 732, (123, 63, 228), "SCIENCE \u2022 MATHS",
         lambda bx, by: draw.text((bx, by), "\u03b6",
                                  font=load(BOLD, 64), fill=(123, 63, 228)),
         "A proof of the Riemann Hypothesis?",
         "An Anthropic mathematician and Claude claim a proof of "
         "the 160-year-old problem."),
        (526, 732, (31, 157, 77), "SPORT \u2022 FOOTBALL",
         lambda bx, by: draw_ball(draw, bx + 32, by + 32, 30, (31, 157, 77)),
         "Liverpool 4\u20130 Man United",
         "Pochettino's nightmare debut at Anfield; Alcaraz wins "
         "his first ATP Finals title."),
    ]
    for cx, cy, accent, label, icon, headline, subline in cards:
        draw_card(draw, cx, cy, cw, ch, accent, label, icon,
                  headline, subline)

    # Dark ticker strip.
    draw.rectangle([0, 944, W, H], fill=TICKER_BG)
    tickfont = load(BOLD, 21)
    draw.text((40, 972), "ALSO:", font=tickfont, fill=TICKER_ACCENT)
    tstart = 40 + draw.textlength("ALSO:", font=tickfont) + 14
    ticker = ("SOUTH KOREA EXPORTS TOP $1T  \u2022  FRIGATE SINKS IN "
              "BENGHAZI  \u2022  DEMOCRATS WIN BIG")
    tfont = fit_size(draw, ticker, 21, W - 40 - tstart)
    draw.text((tstart, 972), ticker, font=tfont, fill=WHITE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
