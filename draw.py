#!/usr/bin/env python3
"""Draw the front page for make.fun news-image-20261124.

Renders the verified world headlines of Tuesday 24 November 2026 as a
one-page newspaper front page (1024x1024 PNG) and writes it to
entry.png beside this file. Run once, locally:

    python3 draw.py

The drawing is fully deterministic: fixed headlines, fixed fonts, fixed
layout, no clock, no randomness, no network. The entry point the
grader runs is main.ts (Node), which copies the finished entry.png to
/output/entry.png byte for byte.

Headlines were verified on 24 November 2026 against SCMP, The Japan
Times and The Manila Times (all dated 24 November 2026); only
headline-level facts are used, and no casualty or damage figures are
given.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 244, 233)   # warm newsprint
INK = (20, 20, 20)
RED = (163, 30, 30)       # kicker accent
GREY = (90, 86, 78)
BLUE = (28, 68, 110)      # sea accent

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, leading):
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_ship(draw, cx, cy):
    """Simple warship on waves, drawn to the right of the lead headline."""
    # hull
    draw.polygon([(cx - 58, cy - 6), (cx + 58, cy - 6), (cx + 44, cy + 16),
                  (cx - 44, cy + 16)], fill=BLUE)
    # superstructure
    draw.rectangle([cx - 26, cy - 30, cx + 10, cy - 6], fill=INK)
    # mast + flag
    draw.line([(cx - 6, cy - 52), (cx - 6, cy - 30)], fill=INK, width=3)
    draw.polygon([(cx - 6, cy - 52), (cx + 16, cy - 47), (cx - 6, cy - 42)],
                 fill=RED)
    # waves
    for dx in (-46, -12, 22):
        draw.arc([cx + dx - 16, cy + 20, cx + dx + 16, cy + 34],
                 start=0, end=180, fill=BLUE, width=3)


def draw_bubble(draw, cx, cy):
    """Chat bubble with AI, drawn to the right of the bottom band."""
    draw.rounded_rectangle([cx - 52, cy - 30, cx + 52, cy + 22],
                           radius=14, outline=BLUE, width=3)
    draw.polygon([(cx - 30, cy + 22), (cx - 38, cy + 36), (cx - 10, cy + 22)],
                 fill=BLUE)
    draw.text((cx, cy - 11), "AI", font=SANS_B(30), fill=BLUE, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- Masthead -----------------------------------------------------
    rule(d, x0, x1, 30, 3)
    d.text((W // 2, 44), "THE WORLD TODAY", font=SERIF_B(84),
           fill=INK, anchor="ma")
    rule(d, x0, x1, 142, 2)
    d.text((x0, 152), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(20),
           fill=INK, anchor="la")
    d.text((x1, 152), "THE WORLD IN ONE PAGE", font=SANS_B(20),
           fill=INK, anchor="ra")
    rule(d, x0, x1, 182, 1)

    # ---- Lead story ---------------------------------------------------
    y = 196
    d.text((x0, y), "UKRAINE  \u00b7  LIBYA", font=SANS_B(22), fill=RED)
    y += 34
    y = draw_wrapped(
        d, x0, y, "Ukraine Sinks Russian Warship Off Libya",
        SERIF_B(44), CONTENT_W - 150, INK, 50)
    draw_ship(d, x1 - 62, 268)
    y += 4
    y = draw_wrapped(
        d, x0, y,
        "Zelensky says Ukrainian sea drones sank the Russian corvette "
        "Merkury off Libya; seven unmanned boats destroyed a Ka-27 "
        "helicopter and hit the cargo ship MV Angara.",
        SANS(22), CONTENT_W, INK, 28)
    rule(d, x0, x1, y + 14, 2)

    # ---- 2 x 2 grid ----------------------------------------------------
    col_w = (CONTENT_W - 24) // 2
    grid = [
        ("TECH  \u00b7  CALIFORNIA",
         "Nvidia Reinstates Huang As CEO After Trump Push",
         "Nvidia rehires Jensen Huang as chief executive in a stunning "
         "reversal after Donald Trump intervenes."),
        ("SPACE  \u00b7  BRUSSELS",
         "NATO Vows Space Defence As Russia Plans Launch",
         "Allies warn Moscow may launch a nuclear space weapon next "
         "month; NATO vows to defend space."),
        ("ASIA  \u00b7  MANILA",
         "Trump Offers Philippines $2.4bn For Self-Defence",
         "The US president offers Manila $2.4 billion to defend itself "
         "\u2014 with a catch."),
        ("BRITAIN  \u00b7  CONCERT",
         "Thousands Evacuated From UK Concert",
         "Thousands are evacuated from a UK concert after an unknown "
         "substance is released."),
    ]
    gy = y + 22
    row_h = 200
    for i, (kicker, headline, dek) in enumerate(grid):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + 24)
        cy = gy + row * row_h
        d.text((cx, cy), kicker, font=SANS_B(18), fill=RED)
        cy = draw_wrapped(d, cx, cy + 26, headline, SERIF_B(28),
                          col_w, INK, 33)
        draw_wrapped(d, cx, cy + 4, dek, SANS(19), col_w, INK, 24)
    # vertical divider between the two columns
    mid_x = x0 + col_w + 12
    d.line([(mid_x, gy), (mid_x, gy + 2 * row_h - 12)], fill=GREY, width=1)

    # ---- Bottom band ---------------------------------------------------
    by = gy + 2 * row_h + 2
    rule(d, x0, x1, by, 2)
    by += 12
    d.text((x0, by), "TECH  \u00b7  LAW", font=SANS_B(20), fill=RED)
    by += 26
    d.text((x0, by), "States Sue Musk Firms Over Grok Images",
           font=SERIF_B(32), fill=INK)
    by += 40
    draw_wrapped(
        d, x0, by,
        "US states sue Musk companies over sexualized images made with "
        "the AI chatbot Grok.",
        SANS(20), CONTENT_W - 150, INK, 26)
    draw_bubble(d, x1 - 62, by + 22)
    by += 62

    # ---- Footer --------------------------------------------------------
    rule(d, x0, x1, 984, 1)
    d.text((W // 2, 992),
           "Headlines verified from SCMP, The Japan Times and The Manila "
           "Times  \u00b7  24 November 2026",
           font=SANS(15), fill=GREY, anchor="ma")

    assert by < 984, f"layout overflow: bottom band ends at {by}"
    img.save(OUT, format="PNG")
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes, {W}x{H})")
    assert size <= 1048576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
