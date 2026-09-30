# Generates the SVG figures for Chapter 83. Run: python3 make_figs83.py
# Both figures print at the full text width (493.2 pt) from a 700 px canvas, so 1 px prints at
# 0.705 pt and the smallest text (10.2 px) prints at 7.2 pt.
from make_figs import *

GREEN = "#2f7d6d"; RED = "#b23b3b"; GREY = "#5b6475"
W = 700
SMALL = 10.2


def hours():
    """The hours come from tools/hours_table.py, the one source for Chapter 6 section 6.1 and
    Chapter 83 section 83.1 (theme T12), so these figures can't drift from the tables."""
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
    import hours_table
    return hours_table


def comma(n):
    return f"{n:,}"


def hatch(pid, colour):
    return (f'<defs><pattern id="{pid}" patternUnits="userSpaceOnUse" width="7" height="7" '
            f'patternTransform="rotate(45)"><rect width="7" height="7" fill="#ffffff"/>'
            f'<line x1="0" y1="0" x2="0" y2="7" stroke="{colour}" stroke-width="2.4"/></pattern></defs>')


# ---------- Figure 83.1: where the hours go ----------
def fig_arithmetic():
    """The teaching chapters laid end to end, once with the low estimates and once with the high.
    The table in section 83.1 gives each part's hours; this figure shows the proportions and where
    the years fall at six hours a week, which the table does not."""
    ht = hours(); t = ht.totals()
    p = {name: (lo, hi) for name, a, b, lo, hi in t["parts"]}
    segs = [("Parts 0–2", t["job_ready"])] + [(f"Part {k}", p[f"Part {k}"]) for k in range(3, 8)]
    (jl, jh), (al, ah) = t["job_ready"], t["all"]
    MAXH = 1250
    x0, BX, BW = 24, 104, 520          # bar track from x0+BX, 520 px for 0..1250 hours
    def px(h): return x0 + BX + BW * h / MAXH
    o = [text(x0, 30, "Where the hours go: job-ready is two fifths of the climb", 15, INK, "bold", family=HEAD),
         text(x0, 50, "Every teaching chapter's Time needed, laid end to end, low estimates and high.",
              11.2, MUTED, style="italic")]
    ytop, BH, GAP = 98, 34, 58
    ybot = ytop + BH + GAP
    # years at six hours a week (312 hours a year), behind the bars
    for yr in (1, 2, 3):
        x = px(312 * yr)
        o.append(path(f"M{x},{ytop - 16} V{ybot + BH + 8}", stroke="#9aa6b6", sw=1.1, dash="4 4"))
        o.append(text(x, ytop - 22, f"{yr} year{'s' if yr > 1 else ''}", SMALL, MUTED, "bold", anchor="middle"))
    o.append(text(x0, ytop - 22, "At 6 hours a week:", SMALL, MUTED, "bold"))
    for label, y, k in (("Low estimate", ytop, 0), ("High estimate", ybot, 1)):
        o.append(text(x0, y + BH / 2 + 4, label, 11.2, INK, "bold"))
        start = 0
        for i, (name, rng) in enumerate(segs):
            h = rng[k]
            xa, xb = px(start), px(start + h)
            fill = ACC if i == 0 else ("#dfe5ed" if i % 2 else "#c3ccd8")
            o.append(rect(xa, y, xb - xa, BH, fill=fill, stroke="#ffffff", sw=1.5))
            lab = name if (xb - xa) > len(name) * SMALL * 0.62 + 6 else name.split()[-1]
            o.append(text((xa + xb) / 2, y + BH / 2 + 4, lab, SMALL if i else 11.2,
                          "#ffffff" if i == 0 else INK, "bold", anchor="middle"))
            start += h
        o.append(text(px(start) + 6, y + BH / 2 + 4, f"{comma(start)} h", 11.2, INK, "bold"))
        # the job-ready mark under the bar
        jr = (jl, jh)[k]; tot = (al, ah)[k]
        o.append(path(f"M{px(jr)},{y + BH} V{y + BH + 12}", stroke=ACC, sw=2))
        lab = f"job-ready at {jr} h, {jr / tot:.0%} of the way"
        o.append(rect(px(jr) + 3, y + BH + 4, len(lab) * SMALL * 0.63, 14, fill="#ffffff"))
        o.append(text(px(jr) + 6, y + BH + 14, lab, SMALL, ACC, "bold"))
    # hours axis
    ya = ybot + BH + 34
    o.append(path(f"M{px(0)},{ya} H{px(MAXH)}", stroke=RULE, sw=1.2))
    for h in range(0, MAXH + 1, 250):
        o.append(path(f"M{px(h)},{ya} V{ya + 5}", stroke=RULE, sw=1.2))
        o.append(text(px(h), ya + 18, comma(h), SMALL, MUTED, anchor="middle", family=MONO))
    o.append(text(px(MAXH / 2), ya + 34, "hours from the first page", SMALL, MUTED, anchor="middle"))
    yf = ya + 60
    o.append(text(x0, yf, "Being hirable is about two fifths of the book. The rest is the rest of a career.",
                  11.6, INK, "bold"))
    return svg(W, yf + 16, "".join(o))


# ---------- Figure 83.2: consistency beats intensity ----------
def fig_consistency():
    ht = hours(); t = ht.totals()
    (jl, jh), (al, ah) = t["job_ready"], t["all"]
    x0, y0 = 58, 76
    PW, PH = 612, 230
    WEEKS, MAXH = 208, 1250
    def px(w): return x0 + PW * w / WEEKS
    def py(h): return y0 + PH - PH * h / MAXH

    o = [hatch("jr", "#8fc1b4"),
         text(24, 28, "Six hours a week beats twenty-five, and the crossover is week 50", 15, INK, "bold", family=HEAD),
         text(24, 48, "Cumulative hours. The sprinter holds twenty-five hours a week for twelve weeks, then stops.",
              11.2, MUTED, style="italic")]
    # grid and axes
    for h in range(0, MAXH + 1, 250):
        o.append(path(f"M{x0 - 5},{py(h)} H{x0 + PW}", stroke="#eef2f7", sw=1))
        o.append(text(x0 - 9, py(h) + 4, comma(h), SMALL, MUTED, anchor="end", family=MONO))
    # the whole-book band: outline only
    o.append(rect(x0, py(ah), PW, py(al) - py(ah), fill="none", stroke=GREY, sw=1.2, extra='stroke-dasharray="5 4"'))
    o.append(text(x0 + 8, py(ah) + 15, f"the whole book: {al}–{comma(ah)} hours", SMALL, GREY, "bold"))
    # the job-ready band: hatched and outlined, labelled on the band itself
    o.append(rect(x0, py(jh), PW, py(jl) - py(jh), fill="url(#jr)", stroke=GREEN, sw=1.4))
    o.append(rect(x0 + PW - 298, py(jh) + 2.5, 292, py(jl) - py(jh) - 5, fill="#ffffff", rx=3))
    o.append(text(x0 + PW - 292, (py(jh) + py(jl)) / 2 + 4, f"job-ready band: {jl}–{jh} hours (end of Part 2)",
                  SMALL, GREEN, "bold"))
    o.append(path(f"M{x0},{y0} V{y0 + PH} H{x0 + PW}", stroke=RULE, sw=1.4))
    for w in (0, 52, 104, 156, 208):
        o.append(path(f"M{px(w)},{y0 + PH} V{y0 + PH + 5}", stroke=RULE, sw=1.2))
        o.append(text(px(w), y0 + PH + 18, str(w), SMALL, MUTED, anchor="middle", family=MONO))
        if w:
            o.append(text(px(w), y0 + PH + 31, f"year {w // 52}", SMALL, MUTED, anchor="middle"))
    o.append(text(x0 + PW / 2, y0 + PH + 48, "weeks since starting", SMALL, MUTED, anchor="middle"))
    o.append(text(x0 - 34, y0 - 12, "cumulative hours", SMALL, MUTED))

    # steady: 6 h a week, solid; sprinter: 25 h a week to week 12, then flat at 300, dashed
    o.append(path(f"M{px(0)},{py(0)} L{px(WEEKS)},{py(6 * WEEKS)}", stroke=ACC, sw=3))
    o.append(path(f"M{px(0)},{py(0)} L{px(12)},{py(300)} L{px(WEEKS)},{py(300)}", stroke=RED, sw=3, dash="9 5"))

    # where the steady line crosses the job-ready band
    wl, wh = ht.weeks(jl, 6), ht.weeks(jh, 6)
    for w in (wl, wh):
        o.append(f'<circle cx="{px(w)}" cy="{py(6 * w)}" r="4" fill="{ACC}"/>')
    o.append(text(px(100), py(jh) - 5, f"the steady one gets there in weeks {wl}–{wh}", SMALL, ACC, "bold"))

    # crossover
    o.append(path(f"M{px(50)},{py(300)} V{y0 + PH}", stroke=MUTED, sw=1.2, dash="4 4"))
    o.append(f'<circle cx="{px(50)}" cy="{py(300)}" r="6" fill="#fff" stroke="{INK}" stroke-width="2.4"/>')
    o.append(text(px(50) + 10, py(300) + 22, "week 50: the crossover,", 11.2, INK, "bold"))
    o.append(text(px(50) + 10, py(300) + 36, "both at 300 hours", SMALL, MUTED))

    # burnout: between the line and the job-ready band, so it is never read as part of the band
    o.append(f'<rect x="{px(12) - 5}" y="{py(300) - 5}" width="10" height="10" fill="{RED}"/>')
    o.append(text(x0 + 6, py(300) - 7, "week 12: burnout", SMALL, RED, "bold"))

    # line labels
    o.append(text(px(WEEKS) - 4, py(300) + 20, "the sprinter (dashed): stops at 300", 11.2, RED, "bold", anchor="end"))
    o.append(text(px(128), py(6 * 128) + 26, "the steady one (solid), 6 hours a week", 11.2, ACC, "bold"))

    yf = y0 + PH + 72
    o.append(text(24, yf, "Nothing dramatic happens in any single week of the solid line. That is the entire point of it.",
                  11.6, INK, "bold"))
    return svg(W, yf + 16, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig83-1-the-arithmetic.svg", fig_arithmetic),
                     ("fig83-2-consistency-beats-intensity.svg", fig_consistency)]:
        open(name, "w").write(fn())
    print("ok")
