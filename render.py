#!/usr/bin/env python3
"""Render the front page of THE DAILY GLOBE for Tuesday 24 November 2026.

Draws a one-page newspaper summing up the day's world news with Pillow:
masthead, lead story, four more stories with drawn illustrations, and an
IN BRIEF strip. Output: entry.png, 1024x1024, under 1 MiB.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (179, 32, 44)
BLUE = (28, 68, 128)
GREEN = (20, 120, 60)
GREY = (90, 90, 90)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def fit(d, text, name, max_size, width):
    """Largest font size (<= max_size) at which text fits width."""
    size = max_size
    while size > 10 and d.textlength(text, font=font(name, size)) > width:
        size -= 2
    return font(name, size)


DATE_F = font("DejaVuSans-Bold.ttf", 18)
KICK = font("DejaVuSans-Bold.ttf", 16)
HEAD2 = font("DejaVuSerif-Bold.ttf", 30)
HEAD3 = font("DejaVuSerif-Bold.ttf", 24)
SUB = font("DejaVuSerif.ttf", 24)
BODY = font("DejaVuSerif.ttf", 17)
BODY16 = font("DejaVuSerif.ttf", 16)
BRIEF = font("DejaVuSans.ttf", 15)
BRIEF_B = font("DejaVuSans-Bold.ttf", 15)
FOOT = font("DejaVuSans.ttf", 13)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, text, f, x, y, width, leading=None):
    leading = leading or int(f.size * 1.35)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def rule(d, x, y, w, weight=2, color=INK):
    d.line([(x, y), (x + w, y)], fill=color, width=weight)


def one_line(d, text, f, x, y, width):
    """Draw text on one line, shrinking then truncating until it fits."""
    size = f.size
    while size > 11 and d.textlength(text, font=font("DejaVuSans.ttf", size)) > width:
        size -= 1
    ff = font("DejaVuSans.ttf", size)
    while d.textlength(text, font=ff) > width and len(text) > 4:
        text = text[:-2].rstrip() + "…"
    d.text((x, y), text, font=ff, fill=INK)
    return d.textlength(text, font=ff)


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(1, 4):
        gy = y + h * i // 4
        d.line([(x, gy), (x + w, gy)], fill=(220, 220, 220), width=1)
    pts = [(x + 12, y + h - 30), (x + 55, y + h - 55), (x + 95, y + h - 42),
           (x + 140, y + h - 80), (x + 185, y + h - 95), (x + 235, y + h - 70),
           (x + 285, y + h - 130), (x + w - 14, y + 26)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax - 16, ay + 4), (ax + 2, ay - 12), (ax + 10, ay + 10)], fill=GREEN)
    d.text((x + 12, y + 8), "NVDA  +31%", font=font("DejaVuSans-Bold.ttf", 20), fill=GREEN)
    d.text((x + 12, y + h - 26), "12 NOV", font=font("DejaVuSans.ttf", 13), fill=GREY)
    d.text((x + w - 78, y + h - 26), "23 NOV", font=font("DejaVuSans.ttf", 13), fill=GREY)
    d.text((x + w - 118, y + 34), "+$1tn", font=font("DejaVuSans-Bold.ttf", 26), fill=RED)


def draw_globe(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2 + 4, h // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 220), outline=INK, width=2)
    d.ellipse([cx - r + 10, cy - r + 12, cx - 8, cy - 2], fill=GREEN)
    d.ellipse([cx + 2, cy + 4, cx + r - 8, cy + r - 10], fill=GREEN)
    d.ellipse([cx - r + 18, cy + 6, cx - 2, cy + r - 16], fill=GREEN)
    d.line([(cx - 6, cy - r), (cx + 8, cy - 10), (cx - 4, cy + 12), (cx + 10, cy + r)],
           fill=RED, width=4)


def draw_ball(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, h // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=2)
    pent = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pent.append((cx + 15 * math.cos(a), cy + 15 * math.sin(a)))
    d.polygon(pent, fill=INK)
    for i in range(5):
        a = math.radians(-90 + i * 72)
        ex, ey = cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)
        d.line([(cx + 15 * math.cos(a), cy + 15 * math.sin(a)), (ex, ey)],
               fill=INK, width=2)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=INK)


def draw_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240), outline=INK, width=2)
    for (sx, sy, sr) in [(x + w - 70, y + 6, 11), (x + w - 48, y + 2, 8),
                         (x + w - 88, y + 12, 7)]:
        d.ellipse([sx, sy, sx + sr * 2, sy + sr], fill=(120, 120, 120))
    for i, c in enumerate([(200, 40, 40), (40, 90, 160), (220, 140, 30)]):
        d.rectangle([x + 20 + i * 46, y + h - 74, x + 62 + i * 46, y + h - 50],
                    fill=c, outline=INK, width=1)
    d.polygon([(x + 8, y + h - 50), (x + w - 8, y + h - 50),
               (x + w - 30, y + h - 20), (x + 30, y + h - 20)], fill=(40, 40, 40))
    for (fx, fy, s) in [(x + 60, y + h - 50, 16), (x + 84, y + h - 50, 20)]:
        d.polygon([(fx - s, fy), (fx, fy - s * 1.7), (fx + s, fy)], fill=(230, 110, 20))
        d.polygon([(fx - s // 2, fy), (fx, fy - s), (fx + s // 2, fy)], fill=(250, 200, 40))
    for i in range(3):
        wx = x + 20 + i * 90
        d.arc([wx, y + h - 14, wx + 60, y + h + 4], 180, 360, fill=BLUE, width=3)


def draw_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220), outline=INK, width=2)
    d.rectangle([x + 20, y + h - 42, x + w - 20, y + h - 10], fill=(120, 110, 95),
                outline=INK, width=2)
    for i in range(3):
        wx = x + 30 + i * 36
        d.rectangle([wx, y + h - 36, wx + 22, y + h - 22], fill=(250, 230, 150),
                    outline=INK, width=1)
    for (fx, fy, s) in [(x + 48, y + h - 44, 20), (x + 84, y + h - 46, 24),
                        (x + 116, y + h - 42, 17)]:
        d.polygon([(fx - s, fy), (fx, fy - s * 1.6), (fx + s, fy)], fill=(230, 110, 20))
        d.polygon([(fx - s // 2, fy), (fx, fy - s), (fx + s // 2, fy)], fill=(250, 200, 40))
    d.ellipse([x + w - 46, y + 6, x + w - 24, y + 18], fill=(150, 150, 150))


def draw_chess(d, x, y, w, h):
    s = 14
    ox, oy = x + 4, y + 2
    for r in range(4):
        for c in range(4):
            col = (255, 255, 255) if (r + c) % 2 == 0 else INK
            d.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s, oy + (r + 1) * s],
                        fill=col, outline=INK, width=1)
    kx, ky = x + w - 46, y + 8
    d.ellipse([kx, ky, kx + 24, ky + 20], fill=(255, 255, 255), outline=INK, width=2)
    d.polygon([(kx + 3, ky + 18), (kx + 21, ky + 18), (kx + 26, ky + 44),
               (kx - 2, ky + 44)], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([kx + 5, ky + 44, kx + 19, ky + 50], fill=INK)
    d.line([(kx + 12, ky - 5), (kx + 12, ky + 2)], fill=INK, width=3)
    d.line([(kx + 7, ky), (kx + 17, ky)], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    # ---- masthead ----
    mast = fit(d, "THE DAILY GLOBE", "DejaVuSerif-Bold.ttf", 88, W - 2 * M)
    d.text((M, 14), "THE DAILY GLOBE", font=mast, fill=INK)
    rule(d, M, 124, W - 2 * M, 3, RED)
    rule(d, M, 130, W - 2 * M, 1)
    d.text((M, 138), "No. 328", font=DATE_F, fill=INK)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=DATE_F)) / 2, 138), date, font=DATE_F, fill=RED)
    right = "ONE DAY, ONE PAGE"
    d.text((W - M - d.textlength(right, font=DATE_F), 138), right, font=DATE_F, fill=INK)
    rule(d, M, 166, W - 2 * M, 2)
    # ---- lead story ----
    y = 178
    d.text((M, y), "MARKETS  •  WALL STREET", font=KICK, fill=RED)
    y += 24
    head1 = fit(d, "HUANG IS BACK", "DejaVuSerif-Bold.ttf", 76, W - 2 * M)
    d.text((M, y), "HUANG IS BACK", font=head1, fill=INK)
    y += 88
    y = para(d, "Nvidia reinstates Jensen Huang as chief executive, twelve days after "
                "his resignation — and the market erupts.",
             SUB, M, y, 560, leading=30)
    y += 4
    para(d, "Shares in the chipmaker soar 31% in a single session, adding almost "
            "$1 trillion in value, the largest one-day gain ever. The Nasdaq jumps "
            "6.5%, its second-biggest rise on record, as the AI rally roars back. "
            "The board acted after President Trump urged Huang's return.",
         BODY16, M, y, 560, leading=21)
    draw_chart(d, 640, 296, 348, 140)
    d.text((640, 442), "The Nasdaq-100 was set for a $2 trillion surge.  •  Reuters",
           font=FOOT, fill=GREY)
    rule(d, M, 466, W - 2 * M, 2)
    # ---- three-column row ----
    colw = (W - 2 * M - 2 * 24) // 3
    xs = [M, M + colw + 24, M + 2 * (colw + 24)]
    stories = [
        ("CLIMATE  •  ANTALYA", "COP31 COLLAPSES",
         "Two weeks of climate talks end with no deal as the draft pact drops "
         "every mention of fossil fuels. Nearly 90 nations refuse to sign.",
         draw_globe),
        ("FOOTBALL  •  FIFA", "WORLD CUP HOSTS NAMED",
         "The 2031 Women's World Cup goes to the USA, Mexico, Costa Rica and "
         "Jamaica; 2035 to England, Scotland, Wales and Northern Ireland.",
         draw_ball),
        ("WAR  •  THE BALTIC", "SHIP AFIRE, TOWED HOME",
         "The Russian cargo ship Sparta II, struck by drones in the Gulf of "
         "Finland, reaches St Petersburg under tow as Kyiv region is hit again.",
         draw_ship),
    ]
    y0 = 480
    for (kick, head, body, art), x in zip(stories, xs):
        d.text((x, y0), kick, font=KICK, fill=RED)
        yy = y0 + 24
        for line in wrap(d, head, HEAD2, colw):
            d.text((x, yy), line, font=HEAD2, fill=INK)
            yy += 36
        yy += 2
        yy = para(d, body, BODY16, x, yy, colw, leading=21)
        art(d, x, yy + 2, colw, 56)
    rule(d, M, 756, W - 2 * M, 2)
    # ---- second row: two stories ----
    y1 = 770
    half = (W - 2 * M - 24) // 2
    d.text((M, y1), "ASIA  •  INDONESIA", font=KICK, fill=RED)
    d.text((M, y1 + 22), "24 DEAD IN FACTORY FIRE", font=HEAD3, fill=INK)
    para(d, "Rescuers search the ruins of a candy factory in Banten for about 30 "
            "workers still missing.",
         BODY16, M, y1 + 56, half - 168, leading=20)
    draw_fire(d, M + half - 140, y1 + 46, 130, 56)
    x2 = M + half + 24
    d.text((x2, y1), "SPORT  •  CHESS", font=KICK, fill=RED)
    d.text((x2, y1 + 22), "CHESS CROWN ON THE LINE", font=HEAD3, fill=INK)
    para(d, "D. Gukesh begins his world title defence against Javokhir Sindarov "
            "in Geneva today.",
         BODY16, x2, y1 + 56, half - 168, leading=20)
    draw_chess(d, x2 + half - 140, y1 + 46, 130, 56)
    rule(d, M, 894, W - 2 * M, 2)
    # ---- IN BRIEF ----
    y2 = 906
    d.text((M, y2), "IN BRIEF", font=font("DejaVuSans-Bold.ttf", 18), fill=RED)
    y2 += 26
    briefs = [
        ("INDIA–NEPAL:", "Modi and Nepal's PM flag off the Saryu–Kamala Express."),
        ("LISBON:", "Thousands march against the rising cost of living."),
        ("TENNIS:", "Alcaraz wins his first ATP Finals title, beating Zverev."),
        ("MOTOR RACING:", "Verstappen wins the Las Vegas Grand Prix."),
        ("CRICKET:", "India–New Zealand first Test ends in a draw."),
        ("USA:", "Appeals court opens path to erase hush-money conviction."),
    ]
    bh = (W - 2 * M - 24) // 2
    for i, (tag, txt) in enumerate(briefs):
        bx = M if i % 2 == 0 else M + bh + 24
        by = y2 + (i // 2) * 22
        d.text((bx, by), "• " + tag, font=BRIEF_B, fill=INK)
        tw = d.textlength("• " + tag + " ", font=BRIEF_B)
        one_line(d, txt, BRIEF, bx + tw, by, bh - tw)
    rule(d, M, 999, W - 2 * M, 1)
    d.text((M, 1007), "Sources: Reuters, CNN, FIFA, AP  •  All stories reported 23–24 November 2026",
           font=FOOT, fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
