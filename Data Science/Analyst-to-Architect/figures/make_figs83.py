# Generates the SVG figures for Chapter 83. Run: python3 make_figs83.py
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


# ---------- Figure 83.1: the arithmetic of the book ----------
def hours():
    """The hours come from tools/hours_table.py, the one source for Chapter 6 section 6.1 and
    Chapter 83 section 83.1 (theme T12), so this figure can't drift from the tables."""
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
    import hours_table
    return hours_table


def fig_arithmetic():
    ht = hours(); t = ht.totals()
    p = {name: (lo, hi) for name, a, b, lo, hi in t["parts"]}
    parts = [
        ("Parts 0 and 1", "Ch 1–9") + t["foundations"] + (GREY,),
        ("Part 2, The Analyst", "Ch 10–27") + p["Part 2"] + (ACC,),
        ("Part 3", "Ch 28–34") + p["Part 3"] + (GREY,),
        ("Part 4", "Ch 35–44") + p["Part 4"] + (GREY,),
        ("Part 5", "Ch 45–52") + p["Part 5"] + (GREY,),
        ("Part 6", "Ch 53–59") + p["Part 6"] + (GREY,),
        ("Part 7", "Ch 60–67") + p["Part 7"] + (GREY,),
    ]
    x0, y0, W = 42, 104, 1040
    o = [text(x0, 38, "What this book actually costs, in hours",
              15.5, INK, "bold", family=HEAD),
         text(x0, 62, "Added up from the Time needed line of all sixty-seven teaching chapters. Bars show the low and high estimate.",
              12.5, MUTED, style="italic")]
    LAB, BARX, BARW = 226, 300, 470
    maxv = 380.0
    o.append(text(x0, y0 - 14, "Part", 11, MUTED, "bold"))
    o.append(text(x0 + BARX, y0 - 14, "Hours", 11, MUTED, "bold"))
    o.append(text(x0 + BARX + BARW + 34, y0 - 14, "At 6 hours a week", 11, MUTED, "bold"))
    for i, (name, chs, lo, hi, c) in enumerate(parts):
        y = y0 + i * 42
        o.append(text(x0, y + 14, name, 12.5, INK, "bold" if c == ACC else "normal"))
        o.append(text(x0 + LAB - 76, y + 14, chs, 11, MUTED, family=MONO))
        o.append(rect(x0 + BARX, y + 2, BARW, 22, fill="#f2f5f9", rx=4))
        llo = int(BARW * lo / maxv); lhi = int(BARW * hi / maxv)
        o.append(rect(x0 + BARX, y + 2, lhi, 22, fill=c, extra=' opacity="0.32"', rx=4))
        o.append(rect(x0 + BARX, y + 2, llo, 22, fill=c, rx=4))
        o.append(text(x0 + BARX + lhi + 10, y + 18, f"{lo}–{hi}", 11.5, c, "bold", family=MONO))
        wk = ht.span(lo, hi, 6, "weeks")
        o.append(text(x0 + BARX + BARW + 34, y + 18, wk, 11.5, MUTED, family=MONO))
    yb = y0 + len(parts) * 42 + 6
    o.append(path(f"M{x0},{yb} H{x0+W}", stroke=RULE, sw=1.2))
    (jl, jh), (al, ah) = t["job_ready"], t["all"]
    rows = [("Job-ready: Parts 0–2", "Ch 1–27", f"{jl}–{jh} hours", ht.span(jl, jh, 6, "months"), ACC),
            ("The whole map", "Ch 1–67", f"{al}–{ah} hours", ht.span(al, ah, 6, "years"), INK)]
    for k, (name, chs, hrs, wk, c) in enumerate(rows):
        y = yb + 26 + k * 32
        o.append(text(x0, y, name, 13, c, "bold"))
        o.append(text(x0 + LAB - 6, y, chs, 11, MUTED, family=MONO))
        o.append(text(x0 + BARX, y, hrs, 12.5, c, "bold", family=MONO))
        o.append(text(x0 + BARX + BARW + 34, y, wk, 12.5, c, "bold", family=MONO))
    yf = yb + 26 + len(rows) * 32 + 14
    o.append(text(x0, yf,
                  "Being hirable is a quarter of the book. That is the number nobody is given, and it is the one you can plan against.",
                  12.5, INK, "bold"))
    return svg(x0 * 2 + W, yf + 24, "".join(o))


# ---------- Figure 83.2: consistency beats intensity ----------
def fig_consistency():
    x0, y0 = 46, 106
    PW, PH = 720, 330          # plot area
    WEEKS, MAXH = 160, 1000
    def px(w): return x0 + PW * w / WEEKS
    def py(h): return y0 + PH - PH * h / MAXH

    o = [text(x0, 38, "Six hours a week beats twenty-five, and the crossover is week 50",
              15.5, INK, "bold", family=HEAD),
         text(x0, 62, "Cumulative hours. The sprinter holds twenty-five hours a week for twelve weeks, then stops.",
              12.5, MUTED, style="italic")]

    # job-ready band
    jl, jh = hours().totals()["job_ready"]
    o.append(rect(x0, py(jh), PW, py(jl) - py(jh), fill="#e2f3ee"))
    o.append(text(x0 + 10, py(jh) - 10, f"job-ready band: {jl}–{jh} hours (end of Part 2)",
                  11, GREEN, style="italic"))

    # axes
    o.append(path(f"M{x0},{y0} V{y0+PH} H{x0+PW}", stroke=RULE, sw=1.4))
    for h in (0, 250, 500, 750, 1000):
        o.append(path(f"M{x0-5},{py(h)} H{x0+PW}", stroke="#eef2f7", sw=1))
        o.append(text(x0 - 12, py(h) + 4, str(h), 10.5, MUTED, anchor="end", family=MONO))
    for w in (0, 25, 50, 75, 100, 125, 156):
        o.append(text(px(w), y0 + PH + 20, str(w), 10.5, MUTED, anchor="middle", family=MONO))
    o.append(text(x0 + PW / 2, y0 + PH + 42, "weeks", 11.5, MUTED, anchor="middle"))
    o.append(text(x0 - 34, y0 - 16, "cumulative hours", 11.5, MUTED))

    # sprinter: 25 h/wk to week 12, then flat at 300
    o.append(path(f"M{px(0)},{py(0)} L{px(12)},{py(300)} L{px(WEEKS)},{py(300)}", stroke=RED, sw=3))
    # steady: 6 h/wk
    o.append(path(f"M{px(0)},{py(0)} L{px(WEEKS)},{py(6*WEEKS)}", stroke=ACC, sw=3))

    # crossover marker
    o.append(path(f"M{px(50)},{py(300)} V{y0+PH}", stroke=MUTED, sw=1.2, dash="4 4"))
    o.append(f'<circle cx="{px(50)}" cy="{py(300)}" r="7" fill="#fff" stroke="{INK}" stroke-width="2.6"/>')
    o.append(text(px(50) + 14, py(300) + 40, "week 50: the crossover", 12, INK, "bold"))
    o.append(text(px(50) + 14, py(300) + 58, "both at 300 hours", 11, MUTED))

    # labels on lines
    o.append(text(px(WEEKS) - 6, py(300) + 22, "the sprinter, stopped at 300", 12, RED, "bold", anchor="end"))
    o.append(text(px(118), py(6 * 118) - 16, "the steady one, 6 hours a week", 12, ACC, "bold", anchor="end"))
    o.append(f'<circle cx="{px(12)}" cy="{py(300)}" r="5" fill="{RED}"/>')
    o.append(text(px(12) + 10, py(300) - 16, "week 12: burnout", 11, RED))

    # side panel
    bx, by, bw, bh = x0 + PW + 52, y0 + 6, 300, 250
    o.append(rect(bx + 2, by + 3, bw, bh, fill="#e9eef4", rx=8))
    o.append(rect(bx, by, bw, bh, fill="#fff", stroke=RULE, sw=1.4, rx=8))
    o.append(text(bx + 16, by + 26, "At each point", 13, INK, "bold", family=HEAD))
    tbl = [("", "sprinter", "steady"),
           ("week 12", "300", "72"),
           ("week 50", "300", "300"),
           ("week 66", "300", "396"),
           ("year 3", "300", "936")]
    for k, (a, b, c) in enumerate(tbl):
        y = by + 54 + k * 30
        bold = "bold" if k == 0 else "normal"
        o.append(text(bx + 16, y, a, 11.5, MUTED, "bold"))
        o.append(text(bx + 130, y, b, 11.5, RED if k else MUTED, bold, family=MONO if k else None))
        o.append(text(bx + 216, y, c, 11.5, ACC if k else MUTED, bold, family=MONO if k else None))
        if k == 0:
            o.append(path(f"M{bx+12},{y+8} H{bx+bw-12}", stroke=RULE, sw=1))
    o.append(wrap(bx + 16, by + bh - 42, wraplines("300 hours does not reach the end of Part 2. The sprinter stops short of employable.", 34), 11, RED, 16))

    yf = y0 + PH + 66
    o.append(text(x0, yf,
                  "Nothing dramatic happens in any single week of the blue line. That is the entire point of it.",
                  12.5, INK, "bold"))
    return svg(x0 + PW + 52 + bw + 46, yf + 24, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig83-1-the-arithmetic.svg", fig_arithmetic),
                     ("fig83-2-consistency-beats-intensity.svg", fig_consistency)]:
        open(name, "w").write(fn())
    print("ok")
