"""Draw the front page of THE WORLD TODAY for Tuesday 24 November 2026.

A one-page newspaper front page (1024 x 1024) built from the six
verified headlines of the day. Run it with:

    python3 draw.py

It writes entry.png next to this file. No network, no clock, no
randomness: the same input always draws the same page.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (163, 18, 30)
NAVY = (28, 58, 110)
GREY = (107, 101, 88)
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load(path, size):
    """Load a TrueType font; fall back to the built-in bitmap font."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap_text(draw, text, face, max_width):
    """Split text into lines that each fit inside max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, face, fill, gap):
    """Draw a list of lines, one under the next; return the y below."""
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += face.size + gap
    return y


def hline(draw, x1, x2, y, width=2, fill=INK):
    draw.line([(x1, y), (x2, y)], fill=fill, width=width)


def fit_headline(draw, headline, face_path, start_size, max_width, max_lines):
    """Pick the largest headline size that wraps into max_lines lines."""
    size = start_size
    while size > 20:
        face = load(face_path, size)
        lines = wrap_text(draw, headline, face, max_width)
        if len(lines) <= max_lines:
            return face, lines
        size -= 2
    face = load(face_path, size)
    return face, wrap_text(draw, headline, face, max_width)


def story(draw, x, y, width, kicker, headline, body,
          head_start, head_lines, body_size, body_lines):
    """Draw one story block; return the y just below it."""
    kick = load(SANS_BOLD, 19)
    draw.text((x, y), kicker, font=kick, fill=RED)
    y += 28
    face, lines = fit_headline(draw, headline, SERIF_BOLD,
                               head_start, width, head_lines)
    y = draw_lines(draw, x, y, lines, face, INK, 3)
    y += 5
    body_face = load(SERIF, body_size)
    body_lines_wrapped = wrap_text(draw, body, body_face, width)
    y = draw_lines(draw, x, y, body_lines_wrapped[:body_lines],
                   body_face, INK, 2)
    return y


def draw_ship(draw, x, y, scale=1.0):
    """A small warship with a red flag, drawn from plain shapes."""
    hull = [(x, y + 34 * scale), (x + 150 * scale, y + 34 * scale),
            (x + 132 * scale, y + 62 * scale), (x + 18 * scale, y + 62 * scale)]
    draw.polygon(hull, fill=NAVY)
    draw.rectangle([x + 52 * scale, y + 12 * scale,
                    x + 96 * scale, y + 34 * scale], fill=INK)
    draw.line([(x + 74 * scale, y + 12 * scale),
               (x + 74 * scale, y - 14 * scale)], fill=INK, width=4)
    flag = [(x + 74 * scale, y - 14 * scale),
            (x + 100 * scale, y - 8 * scale),
            (x + 74 * scale, y - 2 * scale)]
    draw.polygon(flag, fill=RED)
    for i, wy in enumerate((y + 74 * scale, y + 86 * scale)):
        draw.arc([x + 6 * scale + i * 8, wy,
                  x + 70 * scale + i * 8, wy + 14 * scale],
                 start=0, end=180, fill=NAVY, width=3)
        draw.arc([x + 78 * scale + i * 8, wy,
                  x + 142 * scale + i * 8, wy + 14 * scale],
                 start=0, end=180, fill=NAVY, width=3)


def draw_bubble(draw, x, y, w=92, h=58):
    """A speech bubble with AI inside it, drawn from plain shapes."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           outline=NAVY, width=3, fill=PAPER)
    tail = [(x + 22, y + h - 2), (x + 44, y + h - 2),
            (x + 30, y + h + 20)]
    draw.polygon(tail, outline=NAVY, fill=PAPER)
    draw.line([(x + 22, y + h - 2), (x + 30, y + h + 20)], fill=NAVY, width=3)
    draw.line([(x + 44, y + h - 2), (x + 30, y + h + 20)], fill=NAVY, width=3)
    face = load(SANS_BOLD, 34)
    label = "AI"
    tw = draw.textlength(label, font=face)
    draw.text((x + (w - tw) / 2, y + 10), label, font=face, fill=NAVY)


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    left = MARGIN
    right = PAGE_W - MARGIN

    # --- masthead ---
    hline(draw, left, right, 24, width=4)
    mast = load(SERIF_BOLD, 84)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((PAGE_W - tw) / 2, 36), title, font=mast, fill=INK)
    hline(draw, left, right, 134, width=2)

    # --- dateline ---
    date_face = load(SANS_BOLD, 22)
    draw.text((left, 146), "TUESDAY, 24 NOVEMBER 2026",
              font=date_face, fill=INK)
    tag = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(tag, font=date_face)
    draw.text((right - tw, 146), tag, font=date_face, fill=INK)
    hline(draw, left, right, 180, width=2)

    # --- lead story: Ukraine sinks a Russian warship ---
    y = 194
    lead_end = story(draw, left, y, 690,
                     "UKRAINE \u00b7 LIBYA",
                     "Ukraine Sinks Russian Warship Off Libya",
                     "Zelensky says Ukrainian sea drones sank the Russian "
                     "corvette Merkury off Libya; seven unmanned boats "
                     "destroyed a Ka-27 helicopter and hit the cargo ship "
                     "MV Angara.",
                     head_start=50, head_lines=2, body_size=21, body_lines=3)
    draw_ship(draw, 800, 250, scale=1.0)
    hline(draw, left, right, lead_end + 10, width=2)

    # --- middle grid: two columns, two stories each ---
    col_w = (CONTENT_W - 30) // 2
    mid_x = left + col_w + 30
    grid_top = lead_end + 24

    y_left = story(draw, left, grid_top, col_w,
                   "TECH \u00b7 CALIFORNIA",
                   "Nvidia Reinstates Huang As CEO After Trump Push",
                   "Nvidia rehires Jensen Huang as chief executive in "
                   "a stunning reversal after Donald Trump intervenes.",
                   head_start=30, head_lines=2, body_size=19, body_lines=3)
    y_right = story(draw, mid_x, grid_top, col_w,
                    "SPACE \u00b7 BRUSSELS",
                    "NATO Vows Space Defence As Russia Plans Launch",
                    "Allies warn Moscow may launch a nuclear space "
                    "weapon next month; NATO vows to defend space.",
                    head_start=30, head_lines=2, body_size=19, body_lines=3)
    row2 = max(y_left, y_right) + 14

    y_left = story(draw, left, row2, col_w,
                   "ASIA \u00b7 MANILA",
                   "Trump Offers Philippines $2.4bn For Self-Defence",
                   "The US president offers Manila $2.4 billion to "
                   "defend itself \u2014 with a catch.",
                   head_start=30, head_lines=2, body_size=19, body_lines=3)
    y_right = story(draw, mid_x, row2, col_w,
                    "BRITAIN \u00b7 CONCERT",
                    "Thousands Evacuated From UK Concert",
                    "Thousands are evacuated from a UK concert after "
                    "an unknown substance is released.",
                    head_start=30, head_lines=2, body_size=19, body_lines=3)
    grid_bottom = max(y_left, y_right)
    draw.line([(mid_x - 15, grid_top), (mid_x - 15, grid_bottom)],
              fill=GREY, width=1)
    hline(draw, left, right, grid_bottom + 12, width=2)

    # --- bottom story: states sue Musk firms ---
    y = grid_bottom + 26
    bottom_end = story(draw, left, y, 700,
                       "TECH \u00b7 LAW",
                       "States Sue Musk Firms Over Grok Images",
                       "US states sue Musk companies over sexualized images "
                       "made with the AI chatbot Grok.",
                       head_start=38, head_lines=2, body_size=20, body_lines=2)
    draw_bubble(draw, 856, y + 8)

    # --- footer ---
    hline(draw, left, right, bottom_end + 12, width=2)
    foot = load(SANS, 17)
    note = ("Headlines verified from SCMP, The Japan Times and "
            "The Manila Times \u00b7 24 November 2026")
    tw = draw.textlength(note, font=foot)
    draw.text(((PAGE_W - tw) / 2, bottom_end + 22), note, font=foot, fill=GREY)

    page.save("entry.png")
    print("wrote entry.png (1024x1024)")
    print("lead_end=%d grid_bottom=%d bottom_end=%d" % (
        lead_end, grid_bottom, bottom_end))


if __name__ == "__main__":
    main()
