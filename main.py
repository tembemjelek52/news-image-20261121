#!/usr/bin/env python3
"""Sum up 21 November 2026 world news in one image.

Deterministic, Python standard library only, no network, no time,
no randomness. Draws a 1024x1024 newspaper front page and writes
it as a PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Layout (quality pass, 21 Nov 2026 afternoon): masthead with a
"9 STORIES" badge; a lead story with a bigger, more dramatic
visual (cracked Earth, clock for overtime, thermometer, NO DEAL
banner), a verified summit-president quote and a gold fact strip
that no longer overlaps the lead visual; a "WHERE IT HAPPENED"
world-map strip with numbered dots for the 5 main stories and
small dots for the 4 brief stories, matching the numbers in the
story kickers and footer; a 2x2 grid of numbered stories with
bigger icons carrying big glanceable numbers; and a footer where
each brief story gets its own numbered line.

News facts (all events of Sat 21 Nov 2026, verified - see NOTES.md):
- COP31 in Antalya missed its scheduled Friday finish and ran
  into overtime; a third draft was due Saturday morning. The
  draft drops all fossil-fuel language and admits the world
  will overshoot the 1.5C Paris limit. Some decisions were
  deferred to next year. Summit president Murat Kurum: "We are
  close to the finish line but not there yet."
- The Saudi-led coalition intercepted three Houthi ballistic
  missiles fired at Riyadh early on Saturday, the third
  straight day of alerts in the capital; it also struck
  Houthi targets at Hodeidah port and in Sanaa.
- A magnitude 6.8 earthquake struck Junin in central Peru
  (Fri 19:09 Peru local = Sat 01:09 UTC / 08:09 WIB),
  felt 320 km away in Lima; no deaths or major damage
  reported so far.
- Wall Street closed Friday in a rout: S and P 500 down 3.7
  percent, Nasdaq down 5.28 percent; both the S and P and
  the Dow are now in correction. Nvidia fell 13.8 percent.
- NATO chief Mark Rutte visits Warsaw on Saturday after
  Russian missiles and a drone crashed in Poland on Friday;
  Warsaw calls it a deliberate provocation and asks NATO
  for more forces.
- Also that day: KL Rahul became the first Indian opener
  with Test centuries in all SENA countries; foreign
  investors set a record inflow into Indian shares; Trump
  threatened a tax on AI data centres built abroad; a boat
  carrying mourners capsized in Nigeria, at least 4 killed.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
WHITE = (255, 255, 255)
NAVY = (20, 33, 61)
NAVY2 = (31, 52, 92)
RED = (192, 57, 43)
TEAL = (15, 118, 110)
GOLD = (201, 162, 39)
BLUE = (31, 95, 140)
GREEN = (39, 110, 70)
INK = (28, 32, 40)
GREY = (92, 102, 116)
LIGHT = (226, 231, 236)
NIGHT = (12, 20, 44)
ORANGE = (232, 126, 32)
SKY = (174, 214, 241)
LAND = (105, 165, 160)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale if text else 0


def wrap_text(text, scale, max_width):
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                i = (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(-(thick // 2), thick // 2 + 1):
                for b in range(-(thick // 2), thick // 2 + 1):
                    self.set(x + a, y + b, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, pts, color):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)), ((x1, y1), (x2, y2)), ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by) or (yy == ymax and yy == max(ay, by)):
                    t = (yy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale, scale, scale, color)
            cx += 6 * scale
        return cx

    def text_center(self, y, s, scale, color):
        self.text((self.w - text_width(s, scale)) // 2, y, s, scale, color)

    def block(self, x, y, s, scale, color, max_width, line_h):
        lines = wrap_text(s, scale, max_width)
        yy = y
        for line in lines:
            self.text(x, yy, line, scale, color)
            yy += line_h
        return yy


def icon_climate_lead(c, x, y, w, h):
    # Lead visual for COP31 overtime: a cracked Earth glowing
    # orange under a night sky, a clock for the missed deadline,
    # a tall red thermometer, and a red NO DEAL banner.
    c.rect(x, y, w, h, NIGHT)
    for sx, sy in ((14, 12), (40, 28), (80, 10), (130, 20), (170, 14),
                   (20, 60), (60, 52), (110, 44), (150, 60), (190, 30),
                   (210, 18), (16, 90), (200, 60)):
        c.rect(x + sx, y + sy, 3, 3, WHITE)
    # clock: the summit ran past its deadline
    ccx, ccy = x + 240, y + 26
    c.circle(ccx, ccy, 16, NAVY)
    c.circle(ccx, ccy, 13, WHITE)
    c.line(ccx, ccy, ccx + 7, ccy - 7, NAVY, 2)
    c.line(ccx, ccy, ccx, ccy - 9, NAVY, 2)
    c.circle(ccx, ccy, 2, NAVY)
    # big Earth with an orange glow and a red crack
    cx, cy = x + 100, y + 92
    c.circle(cx, cy, 70, ORANGE)
    c.circle(cx, cy, 64, SKY)
    c.circle(cx - 26, cy - 18, 16, GREEN)
    c.circle(cx + 26, cy + 16, 18, GREEN)
    c.rect(cx - 30, cy + 4, 28, 10, GREEN)
    c.rect(cx + 12, cy - 30, 22, 10, GREEN)
    crack = [(cx - 56, cy - 12), (cx - 30, cy), (cx - 8, cy - 14),
             (cx + 18, cy + 2), (cx + 42, cy - 10)]
    for (ax, ay), (bx, by) in zip(crack, crack[1:]):
        c.line(ax, ay, bx, by, RED, 3)
    # tall thermometer, right side
    c.rect(x + 228, y + 52, 22, 66, WHITE)
    c.rect(x + 232, y + 78, 14, 38, RED)
    c.circle(x + 239, y + 130, 17, RED)
    c.circle(x + 239, y + 130, 8, WHITE)
    # gold baseline + red NO DEAL banner
    c.line(x + 12, y + 162, x + w - 12, y + 162, GOLD, 3)
    c.rect(x, y + 166, w, 34, RED)
    c.text(x + (w - text_width("NO DEAL", 3)) // 2, y + 171, "NO DEAL", 3, WHITE)


def icon_quake(c, x, y, w, h):
    # A shaking building on cracked ground, with the big 6.8
    # magnitude at top left: ochre sky, a leaning tower with
    # lit windows, a zigzag crack, dust puffs, falling debris.
    c.rect(x, y, w, h, (122, 63, 23))
    c.text(x + 6, y + 8, "6.8", 3, WHITE)
    # leaning tower
    c.rect(x + 52, y + 24, 44, 52, WHITE)
    c.rect(x + 48, y + 18, 52, 8, NAVY)
    for wy in range(y + 30, y + 72, 14):
        for wx in range(x + 58, x + 92, 14):
            c.rect(wx, wy, 6, 7, GOLD)
    # zigzag crack across the ground
    gy = y + 76
    pts = [(x + 6, gy), (x + 30, gy + 8), (x + 52, gy - 2),
           (x + 76, gy + 8), (x + 100, gy), (x + 122, gy + 6)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, NAVY, 4)
    # ground + dust puffs + falling debris
    c.rect(x, y + 82, w, h - 82, (92, 64, 51))
    for dx, dy, r in ((x + 24, y + 86, 6), (x + 104, y + 88, 5),
                      (x + 62, y + 90, 4)):
        c.circle(dx, dy, r, GREY)
    for dx, dy in ((x + 104, y + 28), (x + 114, y + 44), (x + 106, y + 60)):
        c.rect(dx, dy, 4, 4, RED)


def icon_strike(c, x, y, w, h):
    # Night sky over a city under attack: stars, moon, missile
    # trails arcing down, two explosions, skyline with lit windows
    # and fires on the rooftops.
    c.rect(x, y, w, h, NIGHT)
    for sx, sy in ((18, 14), (48, 30), (96, 10), (150, 26), (196, 12),
                   (228, 34), (120, 44), (30, 58), (176, 52), (240, 66)):
        c.rect(x + sx, y + sy, 3, 3, WHITE)
    c.circle(x + w - 52, y + 42, 26, GOLD)
    # missile trails: bright gold lines with white warheads
    for (tx0, ty0, tx1, ty1) in ((14, 8, 84, 78), (66, 4, 128, 66),
                                 (150, 10, 206, 62)):
        c.line(x + tx0, y + ty0, x + tx1, y + ty1, GOLD, 4)
        c.circle(x + tx1, y + ty1, 6, WHITE)
    # explosion starbursts
    for cx, cy, r in ((x + 66, y + 96, 30), (x + 176, y + 118, 24)):
        for dx, dy in ((0, -r), (r * 7 // 10, -r * 7 // 10), (r, 0),
                       (r * 7 // 10, r * 7 // 10), (0, r),
                       (-r * 7 // 10, r * 7 // 10), (-r, 0),
                       (-r * 7 // 10, -r * 7 // 10)):
            c.line(cx, cy, cx + dx, cy + dy, ORANGE, 5)
        c.circle(cx, cy, 11, ORANGE)
        c.circle(cx, cy, 5, GOLD)
    # skyline with lit windows
    for bx, bw, bh in ((16, 52, 78), (84, 60, 108), (160, 52, 62), (212, 36, 92)):
        c.rect(x + bx, y + h - bh, bw, bh, LIGHT)
        for wy in range(y + h - bh + 10, y + h - 8, 16):
            for wx in range(x + bx + 8, x + bx + bw - 8, 14):
                c.rect(wx, wy, 5, 6, GOLD)
    # fires on two rooftops + smoke
    c.triangle(((x + 96, y + h - 108), (x + 132, y + h - 108), (x + 114, y + h - 136)), RED)
    c.triangle(((x + 176, y + h - 62), (x + 196, y + h - 62), (x + 186, y + h - 82)), RED)
    c.rect(x + 110, y + h - 168, 8, 34, GREY)
    c.rect(x + 182, y + h - 112, 8, 32, GREY)


def icon_intercept(c, x, y, w, h):
    # Three red missiles dive from above and burst on a white
    # shield that protects the ground below: an interception.
    c.rect(x, y, w, h, TEAL)
    cx, cy = x + w // 2, y + h // 2 + 8
    # shield
    c.rect(cx - 32, cy - 28, 64, 40, WHITE)
    c.triangle(((cx - 32, cy + 12), (cx + 32, cy + 12), (cx, cy + 38)), WHITE)
    # gold burst where the missiles are stopped, just above the shield
    bx, by = cx, cy - 34
    for dx, dy in ((0, -16), (11, -11), (16, 0), (11, 11), (0, 16),
                   (-11, 11), (-16, 0), (-11, -11)):
        c.line(bx, by, bx + dx, by + dy, GOLD, 4)
    c.circle(bx, by, 7, GOLD)
    # three incoming red missiles converging on the burst
    c.line(bx + 14, by - 12, x + w - 12, y + 8, RED, 5)
    c.triangle(((x + w - 12, y + 8), (x + w - 26, y + 12), (x + w - 16, y + 22)), RED)
    c.line(bx - 10, by - 14, x + 10, y + 4, RED, 5)
    c.triangle(((x + 10, y + 4), (x + 24, y + 8), (x + 14, y + 18)), RED)
    c.line(bx + 2, by - 16, x + w // 2, y + 2, RED, 5)
    # small skyline the shield protects
    c.rect(cx - 20, cy + 8, 12, 18, TEAL)
    c.rect(cx + 2, cy + 2, 14, 24, TEAL)
    c.rect(cx + 20, cy + 12, 8, 14, TEAL)


def icon_poland(c, x, y, w, h):
    # A fighter jet in side view (fuselage, delta wing, tail fin,
    # gold cockpit, engine flame) under a NATO compass star, over
    # a red debris burst: jets scrambled after objects fell in Poland.
    c.rect(x, y, w, h, BLUE)
    # NATO compass star, top right
    sx, sy = x + w - 24, y + 22
    c.line(sx - 11, sy, sx + 11, sy, WHITE, 3)
    c.line(sx, sy - 11, sx, sy + 11, WHITE, 3)
    c.line(sx - 8, sy - 8, sx + 8, sy + 8, WHITE, 3)
    c.line(sx - 8, sy + 8, sx + 8, sy - 8, WHITE, 3)
    c.circle(sx, sy, 4, GOLD)
    # fuselage
    c.triangle(((x + 12, y + 40), (x + 12, y + 54), (x + 102, y + 47)), WHITE)
    # delta wing
    c.triangle(((x + 52, y + 47), (x + 74, y + 22), (x + 86, y + 47)), WHITE)
    # tail fin
    c.triangle(((x + 18, y + 40), (x + 30, y + 22), (x + 40, y + 40)), WHITE)
    # cockpit + engine flame
    c.circle(x + 84, y + 44, 5, GOLD)
    c.triangle(((x + 12, y + 41), (x + 12, y + 53), (x + 2, y + 47)), GOLD)
    # falling debris burst, bottom right
    dx, dy = x + 100, y + 80
    for ddx, ddy in ((0, -9), (6, -6), (9, 0), (6, 6), (0, 9),
                     (-6, 6), (-9, 0), (-6, -6)):
        c.line(dx, dy, dx + ddx, dy + ddy, RED, 3)
    c.circle(dx, dy, 4, RED)
    c.rect(x + 12, y + h - 8, w - 24, 3, WHITE)


def icon_climate(c, x, y, w, h):
    # The Earth beside a red thermometer: a warming world, and a
    # climate summit that dropped its fossil-fuel language.
    c.rect(x, y, w, h, GREEN)
    cx, cy = x + 52, y + 50
    c.circle(cx, cy, 32, SKY)
    c.circle(cx - 12, cy - 8, 9, GREEN)
    c.circle(cx + 12, cy + 8, 11, GREEN)
    c.rect(cx - 20, cy + 2, 16, 7, GREEN)
    # thermometer
    c.rect(x + 100, y + 20, 10, 50, WHITE)
    c.rect(x + 102, y + 34, 6, 34, RED)
    c.circle(x + 105, y + 74, 10, RED)
    c.circle(x + 105, y + 74, 5, WHITE)
    c.line(x + 12, y + h - 12, x + 88, y + h - 12, GOLD, 4)


def icon_chart(c, x, y, w, h):
    # A plunging market line with the big S and P drop at top left.
    c.rect(x, y, w, h, (122, 63, 23))
    c.text(x + 8, y + 8, "-3.7%", 3, WHITE)
    c.line(x + 16, y + 34, x + 16, y + h - 16, WHITE, 3)
    c.line(x + 16, y + h - 16, x + w - 12, y + h - 16, WHITE, 3)
    pts = [(x + 24, y + 40), (x + 50, y + 48), (x + 76, y + 44), (x + 100, y + 62), (x + 116, y + 70)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, RED, 5)
    for (px, py) in pts:
        c.circle(px, py, 5, GOLD)


# ---------------------------------------------------------------- layout
def card(c, x, y, w, h, accent):
    c.rect(x, y, w, h, WHITE)
    c.rect(x, y, w, 8, accent)
    c.rect(x, y, w, h, GREY)  # border via thin rects below (overwritten centre)
    c.rect(x + 2, y + 2, w - 4, h - 4, WHITE)
    c.rect(x, y, w, 8, accent)


def story(c, x, y, w, h, accent, icon, kicker, headline, body):
    card(c, x, y, w, h, accent)
    icon(c, x + 14, y + 14, 128, 96)
    c.text(x + 156, y + 18, kicker, 2, accent)
    c.block(x + 156, y + 44, headline, 3, INK, w - 172, 28)
    c.block(x + 14, y + 120, body, 2, INK, w - 28, 19)


def footer_line(c, y, num, text):
    total = num + " " + text
    x0 = (W - text_width(total, 2)) // 2
    c.text(x0, y, num, 2, GOLD)
    c.text(x0 + text_width(num + " ", 2), y, text, 2, WHITE)


def draw_map(c, x, y, w, h):
    # Stylised world map strip. Continents are light blobs; gold
    # numbered dots mark the 5 main stories (matching the numbers
    # in the kickers and footer), small navy dots mark the 4 briefs.
    for (bx, by, bw, bh) in (
            (110, 430, 160, 16), (130, 446, 140, 12), (200, 458, 110, 10),
            (250, 438, 70, 12), (395, 426, 28, 10),
            (300, 458, 60, 18), (325, 476, 36, 12),
            (540, 430, 50, 12), (555, 442, 34, 10),
            (525, 446, 65, 18), (540, 464, 48, 16),
            (620, 428, 200, 16), (650, 444, 170, 12), (615, 444, 50, 14),
            (700, 456, 90, 10), (790, 440, 90, 12),
            (820, 468, 80, 14), (835, 478, 50, 10), (955, 478, 20, 10)):
        c.rect(bx, by, bw, bh, LAND)
    dots = ((591, 448, "1"), (633, 453, "2"), (315, 470, "3"),
            (318, 446, "4"), (567, 440, "5"))
    for (dx, dy, num) in dots:
        c.circle(dx, dy, 8, GOLD)
        c.text(dx - 3, dy - 4, num, 1, NAVY)
    for (dx, dy, num) in ((968, 483, "6"), (714, 451, "7"),
                           (530, 460, "8"), (300, 456, "9")):
        c.circle(dx, dy, 6, NAVY)
        c.text(dx - 3, dy - 4, num, 1, WHITE)
    c.text(579, 437, "5 WARSAW", 1, INK)
    c.text(288, 430, "4 NEW YORK", 1, INK)
    c.text(556, 464, "1 ANTALYA", 1, INK)
    c.text(642, 466, "2 RIYADH", 1, INK)
    c.text(290, 480, "3 LIMA", 1, INK)


def draw():
    c = Canvas(W, H, PAPER)
    # masthead
    c.rect(0, 0, W, 112, NAVY)
    c.text_center(16, "THE WORLD IN ONE DAY", 5, WHITE)
    c.text_center(64, "SATURDAY 21 NOVEMBER 2026", 3, GOLD)
    c.text(W - 24 - text_width("9 STORIES", 2), 66, "9 STORIES", 2, GOLD)
    c.rect(0, 112, W, 8, RED)
    # lead story
    c.rect(24, 132, 976, 232, WHITE)
    c.rect(24, 132, 976, 8, RED)
    icon_climate_lead(c, 40, 148, 280, 200)
    c.text(336, 152, "1 LEAD STORY  |  CLIMATE", 2, RED)
    c.block(336, 180, "COP31 TALKS MISS DEADLINE, RUN INTO OVERTIME", 4, INK, 648, 38)
    c.block(336, 272, "NO DEAL AS THE SUMMIT MISSED ITS FRIDAY FINISH. THE DRAFT DROPS ALL FOSSIL-FUEL LANGUAGE AND ADMITS THE WORLD WILL MISS 1.5C.", 2, INK, 648, 19)
    c.text(336, 340, "CLOSE TO THE FINISH LINE BUT NOT THERE YET - KURUM", 2, RED)
    # gold fact strip (now clear of the lead visual)
    c.rect(24, 372, 976, 22, GOLD)
    c.text_center(376, "3RD DRAFT DUE SAT | FOSSIL FUELS CUT | 1.5C OVERSHOOT | DECISIONS DEFERRED", 2, NAVY)
    # world map strip
    c.rect(24, 402, 976, 94, WHITE)
    c.rect(24, 402, 976, 8, RED)
    c.rect(24, 402, 976, 94, GREY)
    c.rect(26, 404, 972, 90, WHITE)
    c.rect(24, 402, 976, 8, RED)
    c.text(40, 410, "WHERE IT HAPPENED", 2, RED)
    c.text(984 - text_width("1-5 MAIN STORIES - 6-9 IN BRIEF BELOW", 2), 410,
           "1-5 MAIN STORIES - 6-9 IN BRIEF BELOW", 2, GREY)
    draw_map(c, 24, 402, 976, 94)
    # grid, 2 x 2
    story(c, 24, 508, 476, 182, RED, icon_intercept,
          "2 MIDDLE EAST", "RIYADH MISSILES INTERCEPTED",
          "SAUDI DEFENCES STOPPED THREE HOUTHI MISSILES FIRED AT RIYADH EARLY SATURDAY, THE THIRD NIGHT OF ALERTS.")
    story(c, 524, 508, 476, 182, ORANGE, icon_quake,
          "3 DISASTER", "6.8 QUAKE SHAKES PERU",
          "A 6.8 QUAKE STRUCK JUNIN IN CENTRAL PERU, FELT 320 KM AWAY IN LIMA. NO DEATHS OR MAJOR DAMAGE SO FAR.")
    story(c, 24, 702, 476, 182, GREEN, icon_chart,
          "4 MARKETS", "WALL ST IN CORRECTION",
          "S AND P 500 FELL 3.7 PERCENT, NASDAQ 5.28 PERCENT ON FRIDAY. BOTH IN CORRECTION. NVIDIA FELL 13.8 PERCENT.")
    story(c, 524, 702, 476, 182, BLUE, icon_poland,
          "5 NATO", "RUTTE HEADS TO WARSAW",
          "NATO CHIEF RUTTE VISITS WARSAW ON SATURDAY AFTER RUSSIAN MISSILES AND A DRONE CRASHED IN POLAND.")
    # footer: one numbered line per brief story
    c.rect(0, 896, W, 128, NAVY)
    footer_line(c, 904, "6", "KL RAHUL FIRST INDIAN OPENER WITH 100S IN ALL SENA COUNTRIES")
    footer_line(c, 927, "7", "INDIA RECORD FPI INFLOW 1.22 LAKH CRORE")
    footer_line(c, 950, "8", "NIGERIA BOAT KILLS AT LEAST 4")
    footer_line(c, 973, "9", "TRUMP THREATENS TAX ON AI DATA CENTRES BUILT ABROAD")
    c.text_center(996, "SOURCES: REUTERS, AP, TBS NEWS, THE DAILY SHORT  |  ALL EVENTS 21 NOV 2026", 2, GOLD)
    return c


# ---------------------------------------------------------------- PNG
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(c, path):
    raw = bytearray()
    for yy in range(c.h):
        raw.append(0)
        raw.extend(c.px[yy * c.w * 3:(yy + 1) * c.w * 3])
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    c = draw()
    write_png(c, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
