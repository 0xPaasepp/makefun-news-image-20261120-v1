#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261120.

Draws a one-page newspaper image (1024x1024) summing up Friday
20 November 2026 in 36 verified stories: 3 equal leads, 10 cards,
a world map with numbered pins 1-13, 23 ALSO briefs (bullets only),
a DATE CHECK band and a sources footer.

All artwork is flat vector drawing done in code with Pillow.
Type is Liberation Serif (headlines, decks) and Liberation Sans
(labels, kickers, ALSO) only.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BG = (247, 243, 232)
INK = (26, 26, 26)
RED = (164, 30, 34)
DARKRED = (122, 20, 24)
NAVY = (22, 42, 66)
DARKNAVY = (16, 30, 50)
BLUE = (43, 92, 140)
SKY = (178, 214, 235)
LIGHTBLUE = (210, 228, 240)
TAN = (214, 196, 160)
LAND = (216, 200, 164)
GOLD = (198, 148, 42)
GREEN = (46, 110, 70)
DARKGREEN = (24, 66, 44)
GREY = (96, 96, 96)
LIGHTGREY = (220, 218, 210)
MINT = (214, 232, 220)
WHITE = (255, 255, 255)
CREAM = (247, 243, 232)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS_I = os.path.join(FONT_DIR, "LiberationSans-Italic.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def para(d, x, y, lines, font, fill=INK, leading=None):
    """Draw lines of text starting at (x, y); returns bottom y."""
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def checkmark(d, cx, top, h, fill=RED, width=2):
    """Draw a check mark with two line segments (no font glyph)."""
    d.line([(cx - h * 0.42, top + h * 0.45),
            (cx - h * 0.14, top + h * 0.80)], fill=fill, width=width)
    d.line([(cx - h * 0.14, top + h * 0.80),
            (cx + h * 0.50, top + h * 0.10)], fill=fill, width=width)


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- panels
def spiral(d, cx, cy, r_max, color, width=3):
    """Cyclone spiral: concentric arcs with rotating start angles."""
    for i, r in enumerate(range(10, r_max + 1, 9)):
        a0 = 200 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 300,
              fill=color, width=width)


def panel_lead_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 110, 150))
    # land (Odisha coast) on the left, sea on the right
    d.polygon([(x, y), (x + int(w * 0.34), y), (x + int(w * 0.22), y + h),
               (x, y + h)], fill=(196, 178, 138))
    d.polygon([(x, y + h), (x + int(w * 0.22), y + h),
               (x + int(w * 0.30), y + int(h * 0.62)),
               (x + int(w * 0.10), y + int(h * 0.55))], fill=(150, 178, 110))
    # coastline
    d.line([(x + int(w * 0.34), y), (x + int(w * 0.22), y + h)],
           fill=(120, 90, 60), width=2)
    cx, cy = x + int(w * 0.62), y + int(h * 0.44)
    spiral(d, cx, cy, 42, WHITE, 4)
    spiral(d, cx, cy, 26, (220, 235, 245), 3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # Gopalpur marker on the coast
    gx, gy = x + int(w * 0.30), y + int(h * 0.42)
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED,
              outline=WHITE, width=2)
    d.text((gx + 9, gy - 7), "GOPALPUR", font=F(SANS_B, 11), fill=WHITE)
    d.text((x + 10, y + 8), "BAY OF BENGAL", font=F(SANS_B, 11),
           fill=(220, 235, 245))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + h - 16), "LANDFALL  ·  GUSTS 90 KM/H",
           font=F(SANS_B, 12), fill=WHITE)
    d.text((x + w - 10, y + h - 16), "CYCLONE AKVAN",
           font=F(SANS_B, 12), fill=(255, 214, 100), anchor="ra")


def panel_lead_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 38))
    # stars
    for sx, sy in [(20, 14), (70, 26), (150, 10), (210, 22), (260, 12),
                   (300, 30), (110, 34), (180, 40), (40, 44), (240, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 210, 230))
    # missile trails: parabolic arcs with bright heads
    trails = [((18, 78), (150, 8), (250, 46)),
              ((60, 92), (180, 18), (300, 60)),
              ((120, 100), (220, 30), (305, 78))]
    for (x0, y0), (xc, yc), (x1, y1) in trails:
        pts = []
        for t in [i / 24.0 for i in range(25)]:
            px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * xc + t * t * x1
            py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * yc + t * t * y1
            pts.append((x + px, y + py))
        d.line(pts, fill=(255, 140, 40), width=4)
        for px, py in pts[::6]:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 180, 80))
        d.ellipse([x + x1 - 5, y + y1 - 5, x + x1 + 5, y + y1 + 5],
                  fill=(255, 200, 90))
    # skyline
    base = y + h
    heights = [34, 52, 28, 62, 44, 70, 38, 56, 30, 48, 66, 40, 54, 36]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - hh, bx + bw - 1, base], fill=(5, 8, 18))
        for wy in range(int(base - hh + 6), int(base - 6), 9):
            if (i * 7 + wy) % 2 == 0:
                d.rectangle([bx + 3, wy, bx + 6, wy + 4], fill=(255, 200, 90))
    # fires at the foot of buildings (drawn over the bottom strip)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(0, 0, 0))
    for fx, fr in [(52, 9), (168, 11)]:
        d.ellipse([x + fx - fr, base - fr - 4, x + fx + fr, base - 4],
                  fill=(255, 120, 20))
        d.ellipse([x + fx - fr // 2, base - fr // 2 - 4,
                   x + fx + fr // 2, base - 4], fill=(255, 210, 80))
    d.text((x + 10, y + 8), "KYIV", font=F(SANS_B, 30), fill=WHITE)
    d.rectangle([x + 10, y + 42, x + 178, y + 62], fill=RED)
    d.text((x + 16, y + 45), "MISSILE BARRAGE", font=F(SANS_B, 13), fill=WHITE)
    d.text((x + 10, y + h - 18), "01:25 LOCAL  ·  7 WAVES",
           font=F(SANS_B, 11), fill=WHITE)
    d.text((x + w - 10, y + h - 18), "3 KILLED",
           font=F(SANS_B, 11), fill=(255, 120, 90), anchor="ra")


def panel_lead_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MINT)
    # globe, left
    gx, gy, gr = x + 56, y + 52, 38
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 170))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=NAVY, width=2)
    d.ellipse([gx - 16, gy - 24, gx + 6, gy - 6], fill=(90, 170, 100))
    d.ellipse([gx - 4, gy + 8, gx + 20, gy + 26], fill=(90, 170, 100))
    d.ellipse([gx - 28, gy + 2, gx - 12, gy + 14], fill=(120, 190, 120))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 330, fill=WHITE, width=2)
    d.text((x + 10, y + 6), "UN CLIMATE SUMMIT", font=F(SANS_B, 11), fill=NAVY)
    # red COP31 box, centre
    d.rectangle([x + 112, y + 16, x + w - 76, y + 64], fill=RED)
    d.text((x + 120, y + 20), "COP31", font=F(SANS_B, 24), fill=WHITE)
    d.text((x + 120, y + 46), "FINAL DAY · DEADLOCK",
           font=F(SANS_B, 10), fill=WHITE)
    # thermometer, right
    tx = x + w - 66
    d.rounded_rectangle([tx, y + 10, tx + 24, y + h - 36], radius=12,
                        fill=WHITE, outline=NAVY, width=2)
    d.rectangle([tx + 7, y + 34, tx + 17, y + h - 44], fill=RED)
    d.ellipse([tx - 3, y + h - 50, tx + 27, y + h - 22], fill=RED,
              outline=NAVY, width=2)
    for yy in range(y + 22, y + h - 44, 12):
        d.line([(tx + 24, yy), (tx + 30, yy)], fill=NAVY, width=2)
    d.rectangle([x, y + h - 20, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + h - 16), "ANTALYA · NOV 20",
           font=F(SANS_B, 12), fill=WHITE)
    d.text((x + w - 10, y + h - 16), "$120BN FINANCE GAP",
           font=F(SANS_B, 12), fill=(255, 214, 100), anchor="ra")


def panel_card_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKNAVY)
    d.text((x + 8, y + 5), "NIKKEI −4.8%", font=F(SANS_B, 11), fill=WHITE)
    d.text((x + 8, y + 20), "KOSPI −4.7%", font=F(SANS_B, 11), fill=WHITE)
    d.text((x + w - 8, y + 5), "SOFTBANK −14%",
           font=F(SANS_B, 11), fill=(255, 150, 130), anchor="ra")
    pts = [(x + 8, y + 36), (x + 45, y + 40), (x + 70, y + 38),
           (x + 105, y + 48), (x + 140, y + 52), (x + 172, y + 62)]
    d.line(pts, fill=(255, 70, 60), width=3)
    for px, py in pts[1:-1]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 90))
    d.rectangle([x, y + h - 18, x + 92, y + h], fill=RED)
    d.text((x + 6, y + h - 15), "ASIA −7% WK", font=F(SANS_B, 10), fill=WHITE)


def panel_card_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKGREEN)
    # candlesticks
    candles = [(0.55, 0.75, 1), (0.70, 0.85, 0), (0.62, 0.80, 1),
               (0.68, 0.88, 0), (0.60, 0.78, 1), (0.72, 0.90, 0)]
    cw = w / len(candles)
    for i, (lo, hi, up) in enumerate(candles):
        cx = x + i * cw + cw / 2
        top = y + 10 + (1 - hi) * (h - 34)
        bot = y + 10 + (1 - lo) * (h - 34)
        col = (90, 200, 120) if up else (230, 70, 60)
        d.line([(cx, y + 6), (cx, y + h - 26)], fill=col, width=1)
        d.rectangle([cx - 6, top, cx + 6, bot], fill=col)
    d.text((x + 8, y + 4), "ANT", font=F(SANS_B, 16), fill=WHITE)
    d.text((x + w - 8, y + 4), "$97.17", font=F(SANS_B, 18),
           fill=(255, 214, 100), anchor="ra")
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 6, y + h - 15), "NASDAQ · FIRST CLOSE",
           font=F(SANS_B, 10), fill=WHITE)
    d.text((x + w - 6, y + h - 15), "+17%", font=F(SANS_B, 11),
           fill=(120, 230, 140), anchor="ra")


def panel_card_cpi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    # bars: Sep 2.1 grey, Oct 2.2 red
    bx0, bw = x + 18, 34
    base = y + h - 20
    h1 = int((h - 38) * 2.1 / 2.6)
    h2 = int((h - 38) * 2.2 / 2.6)
    d.rectangle([bx0, base - h1, bx0 + bw, base], fill=(150, 150, 145))
    d.rectangle([bx0 + 44, base - h2, bx0 + 44 + bw, base], fill=RED)
    d.text((bx0 + bw // 2, base + 4), "SEP", font=F(SANS_B, 9),
           fill=GREY, anchor="ma")
    d.text((bx0 + 44 + bw // 2, base + 4), "OCT", font=F(SANS_B, 9),
           fill=GREY, anchor="ma")
    # 2% target dashed line
    ty = base - int((h - 38) * 2.0 / 2.6)
    for dx in range(x + 8, x + w - 8, 8):
        d.line([(dx, ty), (dx + 5, ty)], fill=NAVY, width=1)
    d.text((x + 8, ty - 13), "2% TARGET", font=F(SANS_B, 8), fill=NAVY)
    d.text((x + w - 10, y + 6), "2.2%", font=F(SERIF_B, 30), fill=RED,
           anchor="ra")
    d.text((x + w - 10, y + 38), "CORE CPI", font=F(SANS_B, 10),
           fill=INK, anchor="ra")


def panel_card_rates(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 240))
    # flat line
    d.line([(x + 10, y + 14), (x + w - 10, y + 14)], fill=RED, width=3)
    for px in range(x + 14, x + w - 8, 22):
        d.ellipse([px - 3, y + 11, px + 3, y + 17], fill=RED)
    d.text((x + 10, y + 20), "1-YR", font=F(SANS_B, 11), fill=GREY)
    d.text((x + w - 10, y + 20), "3.00%", font=F(SANS_B, 14), fill=INK,
           anchor="ra")
    d.text((x + 10, y + 34), "5-YR", font=F(SANS_B, 11), fill=GREY)
    d.text((x + w - 10, y + 34), "3.50%", font=F(SANS_B, 14), fill=INK,
           anchor="ra")
    d.rectangle([x, y + h - 16, x + w, y + h], fill=NAVY)
    d.text((x + w // 2, y + h - 13), "18 MO UNCHANGED",
           font=F(SANS_B, 10), fill=WHITE, anchor="ma")


def panel_card_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 30))
    for sx, sy in [(14, 10), (40, 20), (90, 8), (130, 16), (160, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # dotted trajectory
    for i in range(12):
        t = i / 11.0
        px = x + 12 + t * (w - 90)
        py = y + 18 + t * t * 34
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 214, 100))
    # spacecraft
    sx, sy = x + 18, y + 28
    d.rectangle([sx, sy, sx + 24, sy + 14], fill=(200, 200, 200))
    d.rectangle([sx - 14, sy + 2, sx, sy + 12], fill=GOLD)
    d.rectangle([sx + 24, sy + 2, sx + 38, sy + 12], fill=GOLD)
    d.line([(sx + 12, sy + 14), (sx + 12, sy + 22)], fill=(200, 200, 200),
           width=2)
    # Mercury
    mx, my, mr = x + w - 40, y + 30, 20
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(150, 145, 135))
    for cx, cy, cr in [(mx - 8, my - 6, 4), (mx + 6, my + 3, 5),
                       (mx - 2, my + 9, 3), (mx + 9, my - 9, 2)]:
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 115, 105))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + w // 2, y + h - 15), "6BN MILES · 8 YEARS",
           font=F(SANS_B, 10), fill=WHITE, anchor="ma")


def panel_card_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 70))
    # pitch strip
    d.rectangle([x, y + h - 26, x + w, y + h - 18], fill=(214, 196, 160))
    # bat: blade + handle as polygons rotated -28 deg about (32, 30)
    def rot(px, py, cx=32, cy=30, ang=-28):
        a = math.radians(ang)
        return (cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a),
                cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a))

    blade = [(x + px, y + py) for px, py in
             [rot(20, 8), rot(44, 8), rot(44, 52), rot(20, 52)]]
    d.polygon(blade, fill=(222, 196, 150), outline=(120, 90, 50))
    handle = [(x + px, y + py) for px, py in
              [rot(28, 52), rot(36, 52), rot(36, 66), rot(28, 66)]]
    d.polygon(handle, fill=(120, 90, 50))
    # ball, top right
    d.ellipse([x + w - 40, y + 8, x + w - 24, y + 24], fill=RED,
              outline=WHITE, width=1)
    d.arc([x + w - 40, y + 8, x + w - 24, y + 24], 60, 300,
          fill=WHITE, width=1)
    d.text((x + 58, y + 6), "118", font=F(SERIF_B, 34), fill=WHITE)
    d.text((x + w - 8, y + 26), "RECORD", font=F(SANS_B, 10),
           fill=(255, 214, 100), anchor="ra")
    d.text((x + w - 8, y + h - 14), "NZ 368", font=F(SANS_B, 11),
           fill=WHITE, anchor="ra")


def panel_card_vote(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 110, 170))
    # ballot box
    bx, by = x + w // 2 - 34, y + 18
    d.rectangle([bx, by, bx + 68, by + 30], fill=(240, 240, 235),
                outline=NAVY, width=2)
    d.rectangle([bx + 18, by + 4, bx + 50, by + 8], fill=NAVY)
    # ballot paper going in
    d.polygon([(bx + 24, by - 12), (bx + 46, by - 12), (bx + 46, by + 5),
               (bx + 24, by + 5)], fill=WHITE, outline=NAVY)
    checkmark(d, bx + 35, by - 11, 7, fill=RED, width=2)
    d.text((x + 10, y + 4), "THIRD TERM", font=F(SANS_B, 11), fill=WHITE)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=NAVY)
    d.text((x + w // 2, y + h - 15), "VOTE · 28 FEB 2027",
           font=F(SANS_B, 10), fill=WHITE, anchor="ma")


def panel_card_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 215))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(43, 92, 140))
    # waves (single row above the bottom band)
    for wx in range(0, w, 26):
        d.arc([x + wx - 8, y + 40 - 6, x + wx + 12, y + 40 + 6],
              180, 360, fill=WHITE, width=2)
    # pirogue
    hx, hy = x + w // 2 - 58, y + int(h * 0.40)
    d.polygon([(hx, hy), (hx + 116, hy), (hx + 98, hy + 15),
               (hx + 18, hy + 15)], fill=(120, 80, 40))
    d.line([(hx + 58, hy), (hx + 58, hy - 26)], fill=(90, 60, 30), width=3)
    d.polygon([(hx + 58, hy - 26), (hx + 58, hy - 4), (hx + 80, hy - 4)],
              fill=(240, 235, 220))
    d.text((x + 10, y + 6), "YENNE COAST", font=F(SANS_B, 11), fill=NAVY)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(0, 0, 0))
    d.text((x + w // 2, y + h - 15), "50–100 ABOARD",
           font=F(SANS_B, 10), fill=WHITE, anchor="ma")


def panel_card_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    d.rectangle([x, y, x + w, y + 16], fill=RED)
    d.text((x + 8, y + 2), "SCIOPERO", font=F(SANS_B, 11), fill=WHITE)
    # picket line: placards on sticks
    for i, px in enumerate([18, 62, 106, 150]):
        d.line([(x + px + 12, y + 26), (x + px + 12, y + 50)],
               fill=(90, 60, 30), width=2)
        col = [RED, NAVY, GREEN, RED][i]
        d.rectangle([x + px, y + 20, x + px + 26, y + 34], fill=col)
        d.text((x + px + 13, y + 22), "!", font=F(SANS_B, 10), fill=WHITE,
               anchor="ma")
    d.rectangle([x, y + h - 16, x + w, y + h], fill=RED)
    d.text((x + w // 2, y + h - 13), "100 SQUARES",
           font=F(SANS_B, 11), fill=WHITE, anchor="ma")


def panel_card_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 238))
    # capsule
    cx, cy = x + 30, y + 24
    d.rounded_rectangle([cx - 22, cy - 9, cx + 22, cy + 9], radius=9,
                        fill=RED)
    d.rounded_rectangle([cx, cy - 9, cx + 22, cy + 9], radius=9,
                        fill=(240, 240, 235))
    d.rounded_rectangle([cx - 22, cy - 9, cx + 22, cy + 9], radius=9,
                        outline=NAVY, width=1)
    d.text((x + 62, y + 10), "DARAXONRASIB", font=F(SANS_B, 10), fill=NAVY)
    d.text((x + 62, y + 24), "+ CHEMO", font=F(SANS_B, 10), fill=GREY)
    # response bar
    bx, by, bw = x + 12, y + 46, w - 24
    d.rectangle([bx, by, bx + bw, by + 10], fill=(200, 205, 200))
    d.rectangle([bx, by, bx + int(bw * 0.607), by + 10], fill=GREEN)
    d.text((x + w - 10, y + 56), "60.7% RESPONSE",
           font=F(SANS_B, 11), fill=GREEN, anchor="ra")
    d.text((x + 12, y + 56), "61 PATIENTS", font=F(SANS_B, 10), fill=GREY)

# ---------------------------------------------------------------- map
# Rough continent outlines in (lon, lat); drawn equirectangular.
CONTINENTS = {
    "north_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 73),
                      (-95, 80), (-85, 69), (-80, 73), (-65, 62),
                      (-55, 52), (-60, 47), (-70, 42), (-75, 35),
                      (-80, 26), (-85, 20), (-90, 15), (-95, 16),
                      (-105, 20), (-115, 28), (-125, 40), (-125, 49),
                      (-140, 60), (-155, 58), (-165, 60)],
    "south_america": [(-80, 10), (-75, 5), (-70, 0), (-60, -5),
                      (-50, 0), (-35, -8), (-40, -20), (-48, -28),
                      (-55, -35), (-65, -45), (-70, -55), (-73, -40),
                      (-75, -25), (-80, -15), (-81, -5), (-80, 5)],
    "africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32),
               (30, 31), (35, 28), (40, 15), (43, 11), (48, 11),
               (51, 12), (43, 0), (40, -10), (35, -18), (32, -26),
               (28, -33), (20, -35), (15, -27), (12, -18), (13, -5),
               (9, 4), (0, 5), (-8, 5), (-13, 8), (-17, 12)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53),
               (8, 57), (10, 59), (18, 56), (21, 55), (24, 58),
               (28, 60), (30, 62), (30, 70), (25, 71), (18, 69),
               (12, 65), (5, 60), (5, 58), (-5, 50), (-10, 45),
               (-10, 38), (-6, 36)],
    "asia": [(30, 70), (40, 68), (50, 69), (60, 70), (70, 72),
             (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
             (130, 72), (140, 72), (150, 70), (158, 66), (162, 60),
             (158, 52), (150, 59), (142, 50), (140, 40), (135, 35),
             (130, 33), (127, 35), (122, 38), (120, 32), (115, 23),
             (110, 20), (105, 10), (100, 8), (98, 15), (95, 16),
             (92, 21), (88, 22), (85, 19), (80, 15), (77, 8),
             (75, 10), (72, 20), (68, 23), (65, 25), (60, 25),
             (57, 26), (52, 28), (50, 29), (48, 30), (44, 29),
             (40, 31), (36, 36), (30, 36), (28, 41), (30, 45),
             (32, 50), (35, 55), (40, 60), (35, 65), (30, 68)],
    "australia": [(113, -22), (114, -30), (115, -35), (120, -34),
                  (125, -32), (129, -32), (132, -32), (135, -35),
                  (138, -35), (140, -38), (145, -38), (150, -37),
                  (153, -32), (153, -27), (150, -23), (146, -19),
                  (142, -15), (142, -11), (137, -12), (135, -15),
                  (132, -12), (130, -13), (126, -14), (122, -17),
                  (118, -20), (114, -22)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57),
           (0, 53), (1, 51), (-2, 50)],
    "japan": [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37),
              (141, 39), (142, 42), (144, 44), (142, 45), (140, 40),
              (138, 37), (135, 34), (132, 33)],
    "nz": [(167, -45), (170, -43), (173, -41), (175, -38), (178, -37),
           (176, -40), (173, -42), (170, -44), (167, -46)],
}

# Numbered pins: (lon, lat) nudged slightly where labels would collide.
PINS = {
    1: (86, 20), 2: (32, 54), 3: (33, 35), 4: (122, 38),
    5: (-74, 40.7), 6: (144, 30), 7: (108, 48), 9: (168, -41.3),
    10: (-89.2, 13.7), 11: (-17.3, 14.7), 12: (14, 48), 13: (-6, 36),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # faint graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360.0 * w
        d.line([(gx, y), (gx, y + h)], fill=(40, 62, 92), width=1)
    for lat in [-30, 0, 30, 60]:
        gy = y + (75 - lat) / 135.0 * h
        d.line([(x, gy), (x + w, gy)], fill=(40, 62, 92), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w,
                y + (75 - lat) / 135.0 * h)

    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=LAND)
    # pin 8 lives in orbit: badge at the top-right corner of the map
    d.ellipse([x + w - 34, y + 6, x + w - 12, y + 28], fill=RED,
              outline=WHITE, width=2)
    d.text((x + w - 23, y + 9), "8", font=F(SANS_B, 13), fill=WHITE,
           anchor="ma")
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=WHITE, width=2)
        d.text((px, py - 6), str(num), font=F(SANS_B, 9), fill=WHITE,
               anchor="ma")


# ---------------------------------------------------------------- content
LEADS = [
    dict(num="01", kicker="ODISHA, INDIA · CYCLONE",
         headline="Cyclone Akvan makes landfall in eastern India",
         deck="Severe storm crosses near Gopalpur; 300,000+ evacuated, "
              "winds 70–80 gusting 90 km/h, 423 teams out. (IMD)",
         panel=panel_lead_cyclone),
    dict(num="02", kicker="KYIV, UKRAINE · WAR",
         headline="Russia fires wave of ballistic missiles at Kyiv",
         deck="Overnight barrage hits 3 bridges and energy sites; "
              "3 killed, ~15 hurt, fires in three districts. (Reuters)",
         panel=panel_lead_kyiv),
    dict(num="03", kicker="ANTALYA, TÜRKIYE · CLIMATE",
         headline="COP31 reaches its final day deadlocked",
         deck="Closing draft drops fossil-fuel phase-out and the "
              "$120bn target; hosts push “35 by 35”. (Reuters, UN News)",
         panel=panel_lead_cop),
]

CARDS = [
    dict(num="04", kicker="SEOUL/TOKYO · MARKETS",
         headline="AI sell-off sinks Asia to worst week since 2020",
         deck="Nikkei −4.8%, KOSPI −4.7%, SoftBank −14% at intraday "
              "lows; MSCI Asia-Pacific −7% on the week. (Reuters)",
         panel=panel_card_markets),
    dict(num="05", kicker="NEW YORK · MARKETS",
         headline="Anthropic ends first day up 17%",
         deck="Opens $111.50, closes $97.17 — 17% above its $83 "
              "offer — as the Nasdaq falls 2.2%. (Reuters)",
         panel=panel_card_anthropic),
    dict(num="06", kicker="TOKYO · ECONOMY",
         headline="Japan core inflation 2.2%",
         deck="October core CPI rises from 2.1%, a 2nd month above "
              "2%; a BoJ hike to 1.5% is eyed in December. (Reuters)",
         panel=panel_card_cpi),
    dict(num="07", kicker="BEIJING · RATES",
         headline="China holds lending rates for 18th month",
         deck="1-year LPR stays 3.0%, 5-year 3.5%, as expected; both "
              "unchanged since May 2025. (PBOC, Reuters)",
         panel=panel_card_rates),
    dict(num="08", kicker="MERCURY · SPACE",
         headline="BepiColombo reaches Mercury after 8 years",
         deck="ESA/JAXA probe ends a 6bn-mile trip; orbit insertion "
              "set for Saturday. (ESA, BBC)",
         panel=panel_card_space),
    dict(num="09", kicker="WELLINGTON · CRICKET",
         headline="Phillips makes history with 118",
         deck="First batter with centuries in all 3 formats vs India "
              "in a year; NZ 368, Nicholls 175*. (ICC, AP)",
         panel=panel_card_cricket),
    dict(num="10", kicker="SAN SALVADOR · POLITICS",
         headline="Bukele files to run for third term",
         deck="Registers for the 28 Feb 2027 vote after term limits "
              "were scrapped; rights groups object. (Reuters, AP)",
         panel=panel_card_vote),
    dict(num="11", kicker="SENEGAL · MIGRATION",
         headline="Migrant boat capsizes off Senegal",
         deck="Dozens missing from 50–100 aboard off Yenne; 4 bodies "
              "recovered, search goes on. (Reuters, Al Jazeera)",
         panel=panel_card_boat),
    dict(num="12", kicker="ROME · LABOUR",
         headline="Italy’s CGIL holds 24-hour general strike",
         deck="Unions rally in ~100 squares against the 2027 budget; "
              "transport and schools hit. (CGIL, AFP)",
         panel=panel_card_strike),
    dict(num="13", kicker="BARCELONA · HEALTH",
         headline="Pancreatic cancer pill shrinks tumours 60.7%",
         deck="Daraxonrasib + chemo in 61 patients, early trial with "
              "no chemo-only arm. (ENA, Barcelona)",
         panel=panel_card_pill),
]

ALSO = [
    "KHARKIV — Drone hits hospital, 4 hurt, 50+ windows out. (Kyiv Post)",
    "TURIN — Alcaraz–Cobolli, Medvedev–Tiafoe close groups. (ATP)",
    "HORMUZ — Four attacks on vessels in 96 hours. (UKMTO)",
    "SEOUL — Ruling party adopts Cho impeachment as line. (SBS)",
    "TONGA — 27-day drought emergency as El Niño bites. (RNZ)",
    "COPENHAGEN — Greenland defence bill passes 109–0. (AFP)",
    "JAKARTA — Parliament passes asset-forfeiture bill. (Reuters)",
    "CINCINNATI — Hippo Fiona dies after swallowing a hat. (Reuters)",
    "QATAR — Australia stun Argentina 2–0 in U17 opener. (FIFA)",
    "HONG KONG — Hang Seng ~20% off January peak. (Reuters)",
    "TAIPEI — TAIEX sinks 6.8%, worst week since 1990. (Reuters)",
    "LONDON — Gold dips to $3,601, down 0.6% on the day. (Reuters)",
    "LONDON — Brent crude flat at $91.98, third weekly fall. (Reuters)",
    "DAKAR — Navy rescues 1,400+ migrants in 48 hours. (Reuters)",
    "BRAZIL — Lula visits ailing Raoni, 94; land recognised. (Al Jazeera)",
    "ODISHA — 9,341 shelters open; 69 trains cancelled. (The Hindu)",
    "TOKYO — Nikkei intraday low near 56,595, down 4.8%. (Reuters)",
    "TOKYO — SoftBank plunges 14% as AI holdings slide. (Nikkei)",
    "ANTALYA — COP31 talks set to run past Friday deadline. (Reuters)",
    "MERCURY — Planet at greatest western elongation. (ESA)",
    "WELLINGTON — Nicholls 175* in 216-run stand with Phillips. (ICC)",
    "NEW YORK — Anthropic slips 4.7% after hours to $92.60. (Finnhub)",
    "GLOBAL — UN marks World Children’s Day. (UN News)",
]

STATS = [
    ("300,000+", "evacuated as Cyclone Akvan hit"),
    ("3", "killed in Kyiv missile barrage"),
    ("−7%", "MSCI Asia week, worst since 2020"),
    ("2.2%", "Japan Oct core CPI; BoJ hike eyed"),
    ("118", "Phillips’ historic century"),
    ("8 yrs", "BepiColombo’s voyage to Mercury"),
]

REGIONS = [("EUROPE", 10), ("AMERICAS", 5), ("ASIA-PACIFIC", 11),
           ("MIDEAST", 2), ("AFRICA", 2), ("OCEANIA", 3),
           ("WORLD/SPACE", 3)]

DATE_CHECK_LEFT_OUT = (
    "Trump–Xi–Putin Shenzhen summit · Anthropic’s $83 IPO pricing & "
    "Nasdaq debut · ICJ Myanmar Rohingya verdict · GTA VI midnight "
    "launch · Van Gogh $190.4m sale · EU €45bn Ukraine loan · Crimea "
    "bridge strike · Houthi strike on Riyadh · Colombia tax protests · "
    "Han Duck-soo acquittal · Voyager 1 one light-day out · Jeffries "
    "named US Speaker · Fiji drought declaration")


# ---------------------------------------------------------------- layout
def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 26                      # margin
    CW = W - 2 * M              # content width = 972

    # ---- masthead
    text(d, (M, 10), "THE WORLD IN ONE DAY", F(SANS_B, 13), RED)
    text(d, (W - M, 11), "FRIDAY’S NEWS · ONE PAGE · 36 STORIES",
         F(SANS_B, 11), INK, anchor="ra")
    d.line([(M, 30), (W - M, 30)], fill=INK, width=1)

    # ---- title + deck
    text(d, (M, 34), "Friday 20 November 2026", F(SERIF_B, 56), INK)
    text(d, (M, 96),
         "Cyclone Akvan strikes India · Ballistic missiles hit Kyiv · "
         "COP31 deadlocked on final day · Asian AI sell-off",
         F(SERIF_I, 17), RED)
    d.line([(M, 118), (W - M, 118)], fill=INK, width=2)

    # ---- stat strip (6 cells)
    y0, y1 = 124, 158
    cell = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cell
        if i:
            d.line([(cx, y0 + 2), (cx, y1 - 2)], fill=(190, 185, 170), width=1)
        text(d, (cx + 10, y0), num, F(SERIF_B, 24), RED)
        cap_lines = wrap(d, cap, F(SANS, 9), cell - 20)
        para(d, cx + 10, y0 + 27, cap_lines[:1], F(SANS, 9), GREY, 11)
    d.line([(M, y1 + 4), (W - M, y1 + 4)], fill=INK, width=1)

    # ---- region strip
    ry = 168
    rx = M
    for name, n in REGIONS:
        label = "%s %d" % (name, n)
        fw = d.textlength(label, font=F(SANS_B, 10)) + 12
        d.rectangle([rx, ry, rx + fw, ry + 15], fill=NAVY)
        d.text((rx + 6, ry + 2), label, font=F(SANS_B, 10), fill=WHITE)
        rx += fw + 4
    text(d, (W - M, ry + 2), "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE",
         F(SANS_B, 9), GREY, anchor="ra")

    # ---- leads (3 equal columns)
    gap = 8
    lw = (CW - 2 * gap) // 3
    ly, lh = 190, 190
    for i, lead in enumerate(LEADS):
        x = M + i * (lw + gap)
        d.rectangle([x, ly, x + lw, ly + lh], outline=INK, width=1)
        lead["panel"](d, x + 1, ly + 1, lw - 2, 100)
        d.line([(x, ly + 102), (x + lw, ly + 102)], fill=INK, width=1)
        ty = ly + 107
        text(d, (x + 8, ty), "%s · %s" % (lead["num"], lead["kicker"]),
             F(SANS_B, 11), RED)
        hl = wrap(d, lead["headline"], F(SERIF_B, 19), lw - 16)
        para(d, x + 8, ty + 15, hl[:2], F(SERIF_B, 19), INK, 20)
        dl = wrap(d, lead["deck"], F(SERIF, 11), lw - 16)
        para(d, x + 8, ty + 15 + 2 * 20 + 2, dl[:2], F(SERIF, 11), INK, 13)

    # ---- cards (2 rows x 5)
    cw = (CW - 4 * gap) // 5
    for row in range(2):
        cy = 388 + row * 166
        ch = 160
        for col in range(5):
            card = CARDS[row * 5 + col]
            x = M + col * (cw + gap)
            d.rectangle([x, cy, x + cw, cy + ch], outline=INK, width=1)
            card["panel"](d, x + 1, cy + 1, cw - 2, 68)
            d.line([(x, cy + 70), (x + cw, cy + 70)], fill=INK, width=1)
            ty = cy + 74
            text(d, (x + 7, ty), "%s · %s" % (card["num"], card["kicker"]),
                 F(SANS_B, 9), RED)
            hl = wrap(d, card["headline"], F(SERIF_B, 15), cw - 14)
            para(d, x + 7, ty + 12, hl[:2], F(SERIF_B, 15), INK, 16)
            dl = wrap(d, card["deck"], F(SERIF, 10), cw - 14)
            para(d, x + 7, ty + 12 + 2 * 16 + 1, dl[:3], F(SERIF, 10),
                 INK, 11)

    # ---- map + ALSO
    my = 728
    text(d, (M, my), "WHERE IT HAPPENED", F(SANS_B, 12), RED)
    text(d, (M + 332, my), "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES",
         F(SANS_B, 12), RED)
    text(d, (W - M, my), "14–36", F(SANS_B, 11), GREY, anchor="ra")
    d.line([(M, my + 17), (W - M, my + 17)], fill=INK, width=1)
    draw_map(d, M, my + 22, 322, 168)
    d.rectangle([M, my + 22, M + 322, my + 190], outline=INK, width=1)
    text(d, (M, my + 194), "Pins 1–13 mark the lead & feature stories; "
         "8 is in orbit (see card 8). Positions are approximate.",
         F(SANS, 9), GREY)
    ax = M + 332
    col_w = (W - M - ax - 12) // 2
    afont = F(SANS, 9.5)
    for i, item in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        ix = ax + col * (col_w + 12)
        iy = my + 24 + row * 14
        d.text((ix, iy), "•  " + item, font=afont, fill=INK)

    # ---- DATE CHECK band
    dy = 934
    d.rectangle([M, dy, W - M, dy + 52], outline=RED, width=2)
    dc_font = F(SANS_B, 11)
    text(d, (M + 8, dy + 5), "DATE CHECK", dc_font, RED)
    _dc_w = d.textlength("DATE CHECK ", font=dc_font)
    checkmark(d, M + 8 + _dc_w + 4, dy + 5, 9, fill=RED, width=2)
    d.text((M + 108, dy + 5),
           "Every story here happened, or was first reported, on Friday "
           "20 November 2026, in at least one time zone. Market figures "
           "are intraday lows, not closes.",
           font=F(SANS, 10), fill=INK)
    left = wrap(d, "LEFT OUT AS OTHER DAYS’ NEWS: " + DATE_CHECK_LEFT_OUT,
                F(SANS, 10), W - 2 * M - 16)
    para(d, M + 8, dy + 21, left[:2], F(SANS, 10), GREY, 12)

    # ---- footer
    text(d, (M, 994),
         "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, ICC, "
         "EU Council, PBOC. Original drawings, made in code.",
         F(SANS, 9), GREY)
    text(d, (W - M, 994), "Compiled 20 Nov 2026.", F(SANS, 9), GREY,
         anchor="ra")

    img.save(OUT, optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    render()
