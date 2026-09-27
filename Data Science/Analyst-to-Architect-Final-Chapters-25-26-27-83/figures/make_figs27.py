# Generates the SVG figures for Chapter 27. Run: python3 make_figs27.py
from make_figs import *
from make_figs01 import wrap

GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; TEAL="#1f6fa3"; GREY="#5b6475"


def wraplines(s, n):
    words = s.split(); lines = []; cur = ""
    for w in words:
        if len(cur + " " + w) > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def arrow_right(x, y, length, colour=MUTED, sw=2):
    return (path(f"M{x},{y} H{x+length-6}", stroke=colour, sw=sw)
            + f'<path d="M{x+length-6},{y-5} L{x+length+1},{y} L{x+length-6},{y+5} Z" fill="{colour}"/>')


# ---------- Figure 27.1: the analyst arc ----------
def fig_arc():
    stages = [
        ("SQL", ACC, "Get the headline out of the database", "14.8 orders vs 9.3", "Ch 12, 13"),
        ("Cleaning", ORANGE, "Decide, log the decision, measure whether it mattered", "48 duplicates merged: +0.2 orders", "Ch 14"),
        ("The check", RED, "Split it by the thing that could explain both", "662 of 681 are Wholesale", "Ch 21, 22"),
        ("Python", GREEN, "Turn your choices into parameters so they can be argued with", "band_cut 3 / 5 / 8", "Ch 17, 18, 20"),
        ("Dashboard", TEAL, "One page, one decision, one named reader", "4 objects, nothing else", "Ch 15, 16"),
        ("Memo", PURPLE, "Recommendation first, and what did not support it", "Recommendation: no", "Ch 23, 24"),
    ]
    W, H, G, x0, y0 = 208, 196, 16, 32, 78
    o = [text(x0, 36, "The analyst arc, and what each stage produced in this chapter's project",
              15.5, INK, "bold", family=HEAD),
         text(x0, 60, "Nothing here is new. The capstone is the order, and the stage most people skip.",
              12.5, MUTED, style="italic")]
    for i, (name, c, what, produced, chs) in enumerate(stages):
        x = x0 + i * (W + G)
        o.append(rect(x + 2, y0 + 3, W, H, fill="#e9eef4", rx=8))
        o.append(rect(x, y0, W, H, fill="#fff", stroke=c, sw=1.6 if i != 2 else 2.6, rx=8))
        o.append(f'<path d="M{x},{y0+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y0+34} H{x} Z" fill="{c}"/>')
        o.append(text(x + 12, y0 + 23, f"{i+1}  {name}", 13.5, "#fff", "bold", family=HEAD))
        o.append(wrap(x + 12, y0 + 58, wraplines(what, 28), 11.5, INK, 17))
        o.append(rect(x + 12, y0 + H - 66, W - 24, 34, fill="#f6f9fc", stroke=RULE, sw=1, rx=5))
        o.append(wrap(x + 20, y0 + H - 48, wraplines(produced, 26), 10.5, c, 14))
        o.append(text(x + 12, y0 + H - 14, chs, 10.5, MUTED, style="italic"))
        if i < len(stages) - 1:
            o.append(arrow_right(x + W + 1, y0 + H / 2, G, MUTED, 2))
    ybot = y0 + H
    o.append(path(f"M{x0},{ybot+30} H{x0+6*(W+G)-G}", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(x0, ybot + 56,
                  "Stage 3 is the one that separates a capstone from a tutorial. It is also the one nobody can tell you skipped.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + 6 * W + 5 * G, ybot + 76, "".join(o))


# ---------- Figure 27.2: the finding that did not survive ----------
def fig_not_survive():
    x0, y0 = 36, 86
    PW, PH, G = 360, 250, 44
    o = [text(x0, 36, "The same data, asked three ways. Only the third one answers the question.",
              15.5, INK, "bold", family=HEAD),
         text(x0, 60, "Average orders per customer, 2025. Every bar is true.",
              12.5, MUTED, style="italic")]

    def panel(px, title, subtitle, bars, note, notec, maxv=18.0):
        b = [rect(px + 2, y0 + 3, PW, PH, fill="#e9eef4", rx=8),
             rect(px, y0, PW, PH, fill="#fff", stroke=RULE, sw=1.4, rx=8),
             text(px + 16, y0 + 26, title, 13, INK, "bold", family=HEAD),
             text(px + 16, y0 + 45, subtitle, 11, MUTED, style="italic")]
        bx, by, bw = px + 22, y0 + 64, PW - 44
        n = len(bars)
        slot = (PH - 118) / n
        for k, (label, val, col, sub) in enumerate(bars):
            yy = by + k * slot
            ln = int((bw - 168) * min(val, maxv) / maxv)
            b.append(text(bx, yy + 11, label, 11, INK))
            b.append(text(bx, yy + 26, sub, 9.5, MUTED))
            b.append(rect(bx + 118, yy + 2, bw - 168, 20, fill="#f2f5f9", rx=4))
            b.append(rect(bx + 118, yy + 2, ln, 20, fill=col, rx=4))
            b.append(text(bx + 118 + ln + 8, yy + 17, f"{val:.1f}", 11, col, "bold", family=MONO))
        b.append(path(f"M{px+16},{y0+PH-44} H{px+PW-16}", stroke=RULE, sw=1, dash="3 3"))
        b.append(wrap(px + 16, y0 + PH - 26, wraplines(note, 52), 11, notec, 15))
        return "".join(b)

    o.append(panel(x0, "1. The headline", "All customers, split at 5% discount",
                   [("5% or deeper", 14.8, ACC, "681 customers"),
                    ("under 5%", 9.3, GREY, "3,918 customers")],
                   "True, quotable, and about segment rather than discount.", RED))
    o.append(panel(x0 + PW + G, "2. Split by segment", "The same two bands, per segment",
                   [("Wholesale, 5%+", 15.2, ACC, "662 customers"),
                    ("Retail, 5%+", 1.1, ORANGE, "10 customers"),
                    ("Retail, under 5%", 9.3, GREY, "2,555 customers"),
                    ("Hospitality, 5%+", 1.2, ORANGE, "9 customers")],
                   "No Wholesale customer is below 5%. The bands were segments.", RED))
    o.append(panel(x0 + 2 * (PW + G), "3. Inside Wholesale", "662 customers, by discount quartile",
                   [("Q1  7.9% discount", 14.1, GREEN, "166 customers"),
                    ("Q2  8.5%", 16.7, GREEN, "166 customers"),
                    ("Q3  9.0%", 16.4, GREEN, "165 customers"),
                    ("Q4  9.7% discount", 13.6, GREEN, "165 customers")],
                   "Q4 - Q1 = -0.48 orders, 95% CI [-1.89, 0.92]. No ladder.", GREEN))

    yb = y0 + PH + 40
    o.append(text(x0, yb, "Deeper discounts do not buy more orders. Panel 1 is what a portfolio shows when the analyst stops one query early.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + 3 * PW + 2 * G, yb + 24, "".join(o))


# ---------- Figure 27.3: the ninety-second scan ----------
def fig_scan():
    x0, y0, W = 40, 92, 980
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
    o = [text(x0, 38, "Ninety seconds: what a hiring manager reads, in order",
              15.5, INK, "bold", family=HEAD),
         text(x0, 62, "Then they either read properly or they close the tab. The order is predictable, so build for it.",
              12.5, MUTED, style="italic")]
    RH, TL = 76, 132
    o.append(rect(x0 + TL - 22, y0, 8, len(rows) * RH - 12, fill="#e6ebf2", rx=4))
    for i, (a, b, what, c, concludes, fix) in enumerate(rows):
        y = y0 + i * RH
        o.append(rect(x0, y, TL - 44, 30, fill=c, rx=6))
        o.append(text(x0 + (TL - 44) / 2, y + 20, f"{a}–{b}s", 12, "#fff", "bold",
                      anchor="middle", family=MONO))
        o.append(f'<circle cx="{x0+TL-18}" cy="{y+15}" r="7" fill="#fff" stroke="{c}" stroke-width="2.6"/>')
        o.append(text(x0 + TL, y + 12, what, 13, INK, "bold"))
        o.append(text(x0 + TL, y + 32, "They conclude:  " + concludes, 11.5, MUTED))
        o.append(text(x0 + TL, y + 52, "So:  " + fix, 11.5, c))
    yb = y0 + len(rows) * RH + 6
    o.append(path(f"M{x0},{yb} H{x0+W}", stroke=RULE, sw=1.2, dash="4 4"))
    o.append(text(x0, yb + 28,
                  "Three of the five are writing, and one is a habit you cannot add at the end. Only one is the analysis.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + W, yb + 48, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig27-1-the-analyst-arc.svg", fig_arc),
                     ("fig27-2-the-finding-that-did-not-survive.svg", fig_not_survive),
                     ("fig27-3-the-ninety-second-scan.svg", fig_scan)]:
        open(name, "w").write(fn())
    print("ok")
