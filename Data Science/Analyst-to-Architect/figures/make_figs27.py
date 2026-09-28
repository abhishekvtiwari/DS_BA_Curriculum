# Generates the SVG figures for Chapter 27. Run: python3 make_figs27.py
#
# Every figure is drawn on a 600 px canvas. It prints at the full text width (493.2 pt), so
# 1 px = 0.822 pt and the smallest text used here, 9 px, prints at 7.4 pt (visual standard: >= 7 pt).
# The figures carry no in-figure title: the caption under each one says what it shows.
# Every number drawn here is printed by a query or a script in the chapter (sections 27.2-27.5).
from make_figs import *
from PIL import ImageFont

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#b35a1f"; RED = "#b23b3b"; TEAL = "#1f6fa3"; GREY = "#5b6475"
W = 600
FONTS = {
    ("normal", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ("bold", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ("normal", "italic"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    ("bold", "italic"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
    ("mono", ""): "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}
_cache = {}


def width(s, size, weight="normal", style=""):
    """Width in px of s set in DejaVu Sans (the figures' font) at size px."""
    key = (weight, style)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[key], size=100)
    return _cache[key].getlength(s) * size / 100


def fit(s, maxw, size, weight="normal", style=""):
    """Break s into lines no wider than maxw px."""
    lines, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if cur and width(trial, size, weight, style) > maxw:
            lines.append(cur); cur = w
        else:
            cur = trial
    lines.append(cur)
    return lines


def lines_at(x, y, lines, size, fill=INK, lh=None, weight="normal", style="", family=None):
    lh = lh or round(size * 1.35, 1)
    return "".join(text(x, y + i * lh, l, size, fill, weight, family=family, style=style)
                   for i, l in enumerate(lines))


def arrow(x1, y1, x2, y2, colour=MUTED, sw=1.6):
    """A straight arrow from (x1, y1) to (x2, y2), horizontal or vertical."""
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        head = f"M{x2-6*d},{y2-4} L{x2},{y2} L{x2-6*d},{y2+4} Z"
        return path(f"M{x1},{y1} H{x2-5*d}", stroke=colour, sw=sw) + f'<path d="{head}" fill="{colour}"/>'
    d = 1 if y2 > y1 else -1
    head = f"M{x2-4},{y2-6*d} L{x2},{y2} L{x2+4},{y2-6*d} Z"
    return path(f"M{x1},{y1} V{y2-5*d}", stroke=colour, sw=sw) + f'<path d="{head}" fill="{colour}"/>'


# ---------- Figure 27.1: the analyst arc (3 x 2 cards) ----------
def fig_arc():
    stages = [
        ("SQL", ACC, "Get the headline out of the database", "14.8 orders vs 9.3", "Chapters 12, 13"),
        ("Cleaning", ORANGE, "Decide, log the decision, measure whether it mattered",
         "48 duplicates: headline moves 0.2 orders", "Chapter 14"),
        ("The check", RED, "Split it by the thing that could explain both",
         "662 of 681 are Wholesale", "Chapters 21, 22"),
        ("Python", GREEN, "Turn your choices into parameters so they can be argued with",
         "band_cut 3 / 5 / 8", "Chapters 17, 18, 20"),
        ("Dashboard", TEAL, "One page, one decision, one named reader", "4 objects, nothing else",
         "Chapters 15, 16"),
        ("Memo", PURPLE, "Recommendation first, and what did not support it", "Recommendation: no",
         "Chapters 23, 24"),
    ]
    x0, G, CW = 8, 20, 181                       # 3 cards of 181 px, gaps of 20 px: 8 + 583 + 9 = 600
    pad, body, chip, ref = 9, 10, 9.5, 9
    # measure every card, then use the tallest so the rows line up
    parts = []
    for name, c, what, produced, chs in stages:
        wl = fit(what, CW - 2 * pad, body)
        pl = fit(produced, CW - 2 * pad - 12, chip, "bold")
        parts.append((wl, pl))
    head = 24
    ch_h = max(len(pl) for _, pl in parts) * 13 + 10
    CH = head + 10 + max(len(wl) for wl, _ in parts) * 13.5 + 6 + ch_h + 8 + 12 + 8
    rows_y = [4, 4 + CH + 30]
    o = []
    for i, ((name, c, what, produced, chs), (wl, pl)) in enumerate(zip(stages, parts)):
        col, row = i % 3, i // 3
        x, y = x0 + col * (CW + G), rows_y[row]
        key = (i == 2)
        o.append(rect(x, y, CW, CH, fill="#fff", stroke=c, sw=2.6 if key else 1.3, rx=7))
        o.append(f'<path d="M{x},{y+7} a7,7 0 0 1 7,-7 H{x+CW-7} a7,7 0 0 1 7,7 V{y+head} H{x} Z" fill="{c}"/>')
        label = f"{i+1}  {name}" + ("  · often skipped" if key else "")
        o.append(text(x + pad, y + 16.5, label, 10.5 if not key else 10, "#fff", "bold"))
        o.append(lines_at(x + pad, y + head + 16, wl, body, INK, 13.5))
        cy = y + head + 10 + len(wl) * 13.5 + 6
        cy = y + head + 10 + max(len(p[0]) for p in parts) * 13.5 + 6
        o.append(rect(x + pad, cy, CW - 2 * pad, ch_h, fill="#f6f9fc", stroke=RULE, sw=1, rx=4))
        o.append(lines_at(x + pad + 6, cy + 14, pl, chip, c, 13, "bold"))
        o.append(text(x + pad, y + CH - 9, chs, ref, MUTED, style="italic"))
        if col < 2:
            o.append(arrow(x + CW + 2, y + CH / 2, x + CW + G - 1, y + CH / 2))
    # connector from card 3 down and back to card 4
    x3 = x0 + 2 * (CW + G) + CW / 2; x4 = x0 + CW / 2
    ymid = rows_y[0] + CH + 15
    o.append(path(f"M{x3},{rows_y[0]+CH+1} V{ymid} H{x4}", stroke=MUTED, sw=1.6))
    o.append(arrow(x4, ymid, x4, rows_y[1] - 1))
    yb = rows_y[1] + CH + 20
    foot = fit("Stage 3 is the one that separates a capstone from a tutorial. "
               "It is also the one nobody can tell you skipped.", W - 2 * x0, 10.5, "bold")
    o.append(lines_at(x0, yb, foot, 10.5, INK, 14, "bold"))
    return svg(W, yb + (len(foot) - 1) * 14 + 8, "".join(o))


# ---------- Figure 27.2: the finding that did not survive (three stacked panels) ----------
def fig_not_survive():
    x0 = 6
    PW = W - 2 * x0
    LBL, BX, BMAX, MAXV = 14, 236, 300, 18.0     # label x offset, bar start, bar length for 18 orders
    RH = 19
    panels = [
        ("1. The headline", "all customers, split at 5% discount",
         [("5% or deeper", "681 customers", 14.8, ACC),
          ("under 5%", "3,918 customers", 9.3, GREY)],
         "True, quotable, and about segment rather than discount.", RED),
        ("2. Split by segment", "the same two bands, per segment",
         [("Hospitality, 5% or deeper", "9", 1.2, ORANGE),
          ("Hospitality, under 5%", "1,363", 9.1, GREY),
          ("Retail, 5% or deeper", "10", 1.1, ORANGE),
          ("Retail, under 5%", "2,555", 9.3, GREY),
          ("Wholesale, 5% or deeper", "662", 15.2, ACC)],
         "Wholesale has no under-5% row: no Wholesale customer is below 5%. The bands were segments.", RED),
        ("3. Inside Wholesale", "662 customers, by discount quartile",
         [("Q1, average discount 7.9%", "166", 14.1, GREEN),
          ("Q2, 8.5%", "166", 16.7, GREEN),
          ("Q3, 9.0%", "165", 16.4, GREEN),
          ("Q4, average discount 9.7%", "165", 13.6, GREEN)],
         "Q4 − Q1 = −0.48 orders, 95% CI [−1.89, 0.92]. No ladder.", GREEN),
    ]
    o = []
    y = 4
    for title, sub, bars, note, notec in panels:
        nl = fit(note, PW - 2 * LBL, 9.5, "bold")
        ph = 44 + len(bars) * RH + 8 + len(nl) * 13 + 6
        o.append(rect(x0, y, PW, ph, fill="#fff", stroke=RULE, sw=1.2, rx=7))
        o.append(text(x0 + LBL, y + 18, title, 11, INK, "bold"))
        o.append(text(x0 + LBL + width(title, 11, "bold") + 8, y + 18, sub, 9.5, MUTED, style="italic"))
        o.append(text(x0 + BX - 8, y + 34, "customers", 9, MUTED, anchor="end"))
        o.append(text(x0 + BX, y + 34, "average orders per customer", 9, MUTED))
        by = y + 42
        for k, (label, n, val, col) in enumerate(bars):
            yy = by + k * RH
            ln = BMAX * val / MAXV
            o.append(text(x0 + LBL, yy + 12, label, 9.5, INK))
            o.append(text(x0 + BX - 8, yy + 12, n.replace(" customers", ""), 9.5, MUTED, anchor="end"))
            o.append(rect(x0 + BX, yy + 2, BMAX, 13, fill="#f2f5f9", rx=3))
            o.append(rect(x0 + BX, yy + 2, ln, 13, fill=col, rx=3))
            o.append(text(x0 + BX + ln + 5, yy + 12.5, f"{val:.1f}", 9.5, INK, "bold"))
        ny = by + len(bars) * RH + 4
        o.append(path(f"M{x0+LBL},{ny} H{x0+PW-LBL}", stroke=RULE, sw=1, dash="3 3"))
        o.append(lines_at(x0 + LBL, ny + 14, nl, 9.5, notec, 13, "bold"))
        y += ph + 8
    foot = fit("Customers' 2025 orders; the bars share one scale, from 0 to 18 orders. "
               "Deeper discounts do not buy more orders. Panel 1 is what a portfolio shows when the "
               "analyst stops one query early.", W - 2 * x0, 9.5)
    o.append(lines_at(x0, y + 10, foot, 9.5, MUTED, 13))
    return svg(W, y + 10 + (len(foot) - 1) * 13 + 7, "".join(o))


# ---------- Figure 27.3: the ninety-second scan ----------
def fig_scan():
    x0 = 6
    rows = [
        (0, 15, "The README's first paragraph", ACC,
         "Is there a question here, or a dataset?", "Write it as the question and the answer."),
        (15, 30, "One chart or table", ORANGE,
         "Can this person present a number to a human?", "Put the finding in the title."),
        (30, 50, "One file of code", GREEN,
         "Do they write for a reader or a machine?", "Comment why, never what."),
        (50, 75, "The commit history", PURPLE,
         "Two weeks of work, or one upload an hour ago?", "Commit from day one. It cannot be faked later."),
        (75, 90, "Anything saying what you did NOT find", RED,
         "Should I trust the rest of this?", "A FINDINGS.md file. Almost nobody has one."),
    ]
    RH, CHIP, TX = 50, 62, 104
    o = [rect(x0 + CHIP + 14, 8, 6, len(rows) * RH - 16, fill="#e6ebf2", rx=3)]
    for i, (a, b, what, c, concludes, fix) in enumerate(rows):
        y = 4 + i * RH
        o.append(rect(x0, y, CHIP, 22, fill=c, rx=5))
        o.append(text(x0 + CHIP / 2, y + 15, f"{a}–{b} s", 10, "#fff", "bold", anchor="middle"))
        o.append(f'<circle cx="{x0+CHIP+17}" cy="{y+11}" r="5.5" fill="#fff" stroke="{c}" stroke-width="2.2"/>')
        o.append(text(x0 + TX, y + 11, what, 10.5, INK, "bold"))
        o.append(text(x0 + TX, y + 26, "They conclude:  " + concludes, 9.5, MUTED))
        o.append(text(x0 + TX, y + 40, "So:  " + fix, 9.5, c, "bold"))
    yb = 4 + len(rows) * RH + 2
    o.append(path(f"M{x0},{yb} H{W-x0}", stroke=RULE, sw=1.2, dash="4 4"))
    foot = fit("Three of the five are writing, and one is a habit you cannot add at the end. "
               "Only one is the analysis.", W - 2 * x0, 10, "bold")
    o.append(lines_at(x0, yb + 18, foot, 10, INK, 13.5, "bold"))
    return svg(W, yb + 18 + (len(foot) - 1) * 13.5 + 8, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig27-1-the-analyst-arc.svg", fig_arc),
                     ("fig27-2-the-finding-that-did-not-survive.svg", fig_not_survive),
                     ("fig27-3-the-ninety-second-scan.svg", fig_scan)]:
        open(name, "w").write(fn())
    print("ok")
