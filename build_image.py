#!/usr/bin/env python3
"""Five-frames news poster for Monday 23 November 2026.

A light-paper storyboard: a masthead, one tall hero frame and four
short frames, each a numbered pastel panel with a small hand-drawn
glyph on the right, and an also-today ticker along the bottom.

Everything is drawn with PIL from fixed coordinates. No network, no
randomness, no timestamps, so two runs write byte-identical PNGs.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (246, 240, 227)
INK = (28, 28, 28)
MUTED = (112, 106, 96)
RULE_RED = (198, 38, 38)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def typeface(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def fit_size(draw, text, sizes, max_w, bold=True):
    """Largest size from `sizes` whose rendered width fits `max_w`."""
    for size in sizes:
        f = typeface(size, bold=bold)
        if draw.textlength(text, font=f) <= max_w:
            return f
    return typeface(sizes[-1], bold=bold)


def wrap_lines(draw, text, font, max_w):
    """Greedy word wrap returning the lines that fit `max_w`."""
    out, current = [], ""
    for word in text.split(" "):
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not current:
            current = trial
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def centered_text(draw, cx, y, text, font, fill):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma")


def badge(draw, cx, cy, number, colour):
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=colour)
    centered_text(draw, cx, cy - 16, str(number),
                  typeface(30, bold=True), (255, 255, 255))


def glyph_leaders(draw, cx, cy):
    """Three overlapping initial discs: T (red), P (blue), X (gold)."""
    specs = [(-42, (198, 38, 38), "T"), (0, (36, 72, 160), "P"),
             (42, (216, 158, 24), "X")]
    for dx, colour, letter in specs:
        x = cx + dx
        draw.ellipse([x - 25, cy - 25, x + 25, cy + 25], fill=colour)
        centered_text(draw, x, cy - 13, letter,
                      typeface(24, bold=True), (255, 255, 255))


def glyph_blocked_sun(draw, cx, cy):
    """Gold sun with rays, struck through by a red diagonal."""
    gold = (232, 164, 32)
    for k in range(8):
        ang = math.pi * k / 4
        x0 = cx + 36 * math.cos(ang)
        y0 = cy + 36 * math.sin(ang)
        x1 = cx + 48 * math.cos(ang)
        y1 = cy + 48 * math.sin(ang)
        draw.line([(x0, y0), (x1, y1)], fill=gold, width=4)
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=gold)
    draw.line([(cx - 32, cy - 40), (cx + 32, cy + 40)],
              fill=RULE_RED, width=5)


def glyph_house(draw, cx, cy):
    """Dark-blue house silhouette with a white door."""
    blue = (36, 72, 160)
    draw.polygon([(cx - 44, cy - 2), (cx, cy - 42), (cx + 44, cy - 2)],
                 fill=blue)
    draw.rectangle([cx - 36, cy - 2, cx + 36, cy + 44], fill=blue)
    draw.rectangle([cx - 9, cy + 18, cx + 9, cy + 44], fill=(255, 255, 255))


def glyph_zeta(draw, cx, cy):
    centered_text(draw, cx, cy - 40, "\u03b6",
                  typeface(76, bold=True), (110, 60, 180))


def glyph_ball(draw, cx, cy):
    """Green ring with a filled pentagon, like a football."""
    green = (30, 130, 70)
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32],
                 outline=green, width=4)
    pts = []
    for k in range(5):
        ang = -math.pi / 2 + 2 * math.pi * k / 5
        pts.append((cx + 16 * math.cos(ang), cy + 16 * math.sin(ang)))
    draw.polygon(pts, fill=green)


def panel(draw, box, fill, number, badge_colour, kicker, headline,
          body, glyph, tall=False):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=fill)
    badge(draw, 54, y0 + (58 if tall else 52), number, badge_colour)
    tx = 102
    draw.text((tx, y0 + 16), kicker, font=typeface(18, bold=True),
              fill=(110, 104, 96))
    head_font = fit_size(draw, headline, [31, 29, 27], 736, bold=True)
    draw.text((tx, y0 + 40), headline, font=head_font, fill=INK)
    body_font = typeface(21 if tall else 20)
    lead = 30 if tall else 26
    by = y0 + (96 if tall else 80)
    for line in wrap_lines(draw, body, body_font, 700):
        draw.text((tx, by), line, font=body_font, fill=INK)
        by += lead
    glyph(draw, 908, y0 + (100 if tall else 66))


def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, 1009, 1009], outline=INK, width=4)

    d.text((48, 30), "MONDAY  \u2022  23 NOVEMBER 2026",
           font=typeface(40, bold=True), fill=INK)
    d.text((48, 80), "THE WORLD IN FIVE FRAMES",
           font=typeface(25), fill=MUTED)
    d.rectangle([48, 116, 976, 122], fill=RULE_RED)

    panel(d, (36, 136, 988, 332), (205, 235, 228), 1, (0, 128, 118),
          "SHENZHEN  \u2022  THE SUMMIT",
          "THREE LEADERS, ONE DECLARATION",
          "Trump, Putin and Xi meet in Shenzhen and issue a "
          "'Declaration toward Peace' on the APEC sidelines.",
          glyph_leaders, tall=True)
    panel(d, (36, 346, 988, 478), (250, 222, 178), 2, (216, 120, 20),
          "CLIMATE  \u2022  COP31",
          "COP31 FAILS TO REACH A DEAL",
          "Talks collapse as the EU rejects any deal without "
          "fossil-fuel phase-out language.",
          glyph_blocked_sun)
    panel(d, (36, 492, 988, 624), (205, 222, 242), 3, (36, 72, 160),
          "UKRAINE  \u2022  KYIV",
          "BOY, 7, PULLED ALIVE FROM RUBBLE",
          "David is rescued after 14 hours trapped; 10 killed in "
          "the Russian drone strike.",
          glyph_house)
    panel(d, (36, 638, 988, 770), (222, 205, 242), 4, (110, 60, 180),
          "SCIENCE  \u2022  MATHS",
          "A PROOF OF THE RIEMANN HYPOTHESIS?",
          "An Anthropic mathematician and Claude claim to have "
          "proved the 160-year-old problem.",
          glyph_zeta)
    panel(d, (36, 784, 988, 916), (205, 235, 205), 5, (30, 130, 70),
          "SPORT  \u2022  FOOTBALL",
          "LIVERPOOL 4\u20130 MAN UNITED",
          "Pochettino's nightmare debut at Anfield; Alcaraz wins "
          "his first ATP Finals title.",
          glyph_ball)

    ticker = ("ALSO: SOUTH KOREA EXPORTS TOP $1T  \u2022  FRIGATE SINKS "
              "IN BENGHAZI  \u2022  DEMOCRATS WIN BIG")
    tick_font = fit_size(d, ticker, [19, 18, 17, 16, 15], 928, bold=True)
    d.text((48, 944), ticker, font=tick_font, fill=INK)
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    with open(out, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"wrote {out}  {os.path.getsize(out)} bytes  sha256={digest}")


if __name__ == "__main__":
    main()
