# Generates the SVG figures for Chapter 30. Run: python3 make_figs30.py
# Every figure prints at the full text width, 174 mm = 493.2 pt, so a font of s px on a W px canvas prints at
# s x 493.2 / W pt. The canvases are 680 px wide and the smallest font is 10.5 px, which prints at 7.6 pt.
# Numbers come from the chapter's own results (section 30.9) and statsmodels, not typed by hand.
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
from make_figs import *
GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#b35a1f"; RED = "#9b2c2c"; LIGHT = "#dfe5ec"
W = 680
K = (937, 1035); N = (24036, 23250)            # section 30.9: enquiries and visitors, control then variant_b


def pp(v):
    """A difference in percentage points, with a real minus sign and no '-0.00'."""
    s = f"{v:+.2f}"
    return "0.00" if s in ("-0.00", "+0.00") else s.replace("-", "−")


def fig_ci():
    p1, p2 = K[0] / N[0], K[1] / N[1]
    diff = 100 * (p2 - p1)
    o = [text(16, 26, "The same lift, four sample sizes", 13, INK, "bold", family=HEAD)]
    rows = [(2500, RED, "could be a loss"), (10000, ORANGE, "just touches zero"),
            (25000, GREEN, "the test as run"), (100000, GREEN, "precise, and expensive")]
    x0, x1, lo, hi = 150, 450, -1.0, 2.0
    def px(v): return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    top, step = 62, 52
    bottom = top + step * (len(rows) - 1) + 24
    o.append(path(f"M{px(0)},{top - 16} V{bottom}", stroke=MUTED, sw=1.2, dash="4,4"))
    o.append(text(px(0), top - 22, "no difference", 10.5, MUTED, anchor="middle"))
    o.append(text(x1 + 30, top - 22, "95% interval", 10.5, MUTED, "bold"))
    y = top
    for n, c, note in rows:
        se = 100 * np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
        a, b = diff - 1.96 * se, diff + 1.96 * se
        o.append(text(16, y + 4, f"{n:,} per group", 11, INK))
        o.append(path(f"M{px(a)},{y} H{px(b)}", stroke=c, sw=3))
        for v in (a, b):
            o.append(path(f"M{px(v)},{y - 7} V{y + 7}", stroke=c, sw=2.5))
        o.append(rect(px(diff) - 4, y - 4, 8, 8, fill=c, stroke=c, rx=4))
        o.append(text(x1 + 30, y - 2, f"{pp(a)} to {pp(b)} pp", 11, c, "bold"))
        o.append(text(x1 + 30, y + 13, note, 10.5, MUTED))
        y += step
    for v in (-1, 0, 1, 2):
        o.append(path(f"M{px(v)},{bottom} V{bottom + 5}", stroke=MUTED, sw=1.2))
        o.append(text(px(v), bottom + 19, pp(v).replace(".00", "") + " pp" if v else "0 pp", 10.5, MUTED, anchor="middle"))
    o.append(text(16, bottom + 44, f"Every row measured the same {pp(diff)} points (dot); only the sample size changed.", 10.5, MUTED))
    return svg(W, bottom + 56, "".join(o))


def fig_power():
    o = [text(16, 26, "Power: the chance of catching an effect that is really there", 13, INK, "bold", family=HEAD)]
    h = proportion_effectsize(0.044, 0.039)
    ns = np.arange(1000, 60001, 1000)
    power = NormalIndPower().power(effect_size=h, nobs1=ns, alpha=0.05)
    x0, y0, x1, y1 = 60, 262, 650, 52
    def px(n): return x0 + (n / 60000) * (x1 - x0)
    def py(p): return y0 - p * (y0 - y1)
    for p in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        o.append(path(f"M{x0},{py(p)} H{x1}", stroke=RULE, sw=0.8, dash="3,4"))
        o.append(text(x0 - 8, py(p) + 4, f"{p:.0%}", 10.5, MUTED, anchor="end"))
    o.append(path(f"M{x0},{y0} H{x1}", stroke=MUTED, sw=1.2))
    for n in range(0, 60001, 10000):
        o.append(text(px(n), y0 + 17, f"{n // 1000}k", 10.5, MUTED, anchor="middle"))
    o.append(text((x0 + x1) / 2, y0 + 36, "visitors per group", 11, INK, anchor="middle"))
    d = "M" + " L".join(f"{px(n):.1f},{py(p):.1f}" for n, p in zip(ns, power))
    o.append(path(d, stroke=ACC, sw=2.5))
    p25, p5 = power[ns == 25000][0], power[ns == 5000][0]
    o.append(path(f"M{x0},{py(p25)} H{px(25000)} V{y0}", stroke=GREEN, sw=1.5, dash="5,4"))
    o.append(rect(px(25000) - 5, py(p25) - 5, 10, 10, fill=GREEN, stroke=GREEN, rx=5))
    o.append(text(px(25000) + 10, py(p25) + 22, f"25,000 per group: {p25:.0%} power", 11, GREEN, "bold"))
    o.append(rect(px(5000) - 5, py(p5) - 5, 10, 10, fill=RED, stroke=RED, rx=5))
    o.append(text(px(5000) + 12, py(p5) + 2, f"5,000 per group: {p5:.0%} power, so the", 11, RED))
    o.append(text(px(5000) + 12, py(p5) + 16, "test misses this effect 3 times in 4", 11, RED))
    o.append(text(16, y0 + 60, "+0.5 percentage points on a 3.9% baseline, at the 5% level.", 10.5, MUTED))
    return svg(W, y0 + 72, "".join(o))


def fig_design():
    o = [text(16, 26, "An experiment, in the order the decisions are made", 13, INK, "bold", family=HEAD)]
    steps = [("Before", "Question and change", "the shorter enquiry form", ACC),
             ("Before", "Primary metric, guardrails", "enquiry rate per visitor; pages, sessions, value", ACC),
             ("Before", "MDE and sample size", "0.5 pp → 25,000 per group", PURPLE),
             ("Before", "Duration, stopping rule", "two whole weeks, no interim decisions", PURPLE),
             ("During", "Randomize by visitor", "50/50, and watch the guardrails", GREEN),
             ("After", "Sample-ratio check", "chi-square on group sizes: failed here", ORANGE),
             ("After", "Primary metric with CI", "+0.55 pp (0.19 to 0.91), p = 0.0026", GREEN),
             ("After", "Effect size, decision", "+14% relative; ship, fix the Safari tag", GREEN)]
    y = 44
    for i, (when, title, detail, c) in enumerate(steps):
        if i == 4:
            o.append(path(f"M16,{y + 2} H{W - 16}", stroke=INK, sw=1.6, dash="7,4"))
            o.append(text(W - 16, y - 2, "▲ above the line: written down before any visitor is randomized", 10.5, INK, "bold", anchor="end"))
            y += 12
        o.append(rect(16, y, 70, 30, fill=ROWALT, stroke=RULE, rx=5))
        o.append(text(51, y + 20, when, 10.5, MUTED, "bold", anchor="middle"))
        o.append(rect(94, y, W - 110, 30, fill="#fff", stroke=c, sw=1.4, rx=5))
        o.append(text(106, y + 20, title, 11, c, "bold"))
        o.append(text(300, y + 20, detail, 11, INK))
        y += 36
    return svg(W, y + 6, "".join(o))


def fig_peeking():
    o = [text(16, 26, "Peeking: what daily checks do to a test where nothing is different", 13, INK, "bold", family=HEAD)]
    panels = [(16, "One planned look at the end", 1, "1 in 20 tests calls a false winner: 5%", "#f6f9fc", RULE, GREEN),
              (350, "Looking every day for two weeks", 5, "5 in 20 call a false winner: 25.5%", "#fbeaea", RED, RED)]
    for x, title, bad, note, bg, border, tc in panels:
        o.append(rect(x, 44, 314, 138, fill=bg, stroke=border, sw=1.4, rx=8))
        o.append(text(x + 14, 68, title, 12, tc, "bold"))
        for i in range(20):
            sx, sy = x + 14 + (i % 10) * 29, 82 + (i // 10) * 33
            if i < bad:
                o.append(rect(sx, sy, 25, 27, fill=RED, stroke=RED, rx=3))
                o.append(path(f"M{sx + 7},{sy + 8} L{sx + 18},{sy + 19} M{sx + 18},{sy + 8} L{sx + 7},{sy + 19}", stroke="#fff", sw=2.6))
            else:
                o.append(rect(sx, sy, 25, 27, fill=LIGHT, stroke=RULE, rx=3))
        o.append(text(x + 14, 170, note, 11, INK))
    o.append(rect(16, 196, 14, 14, fill=RED, stroke=RED, rx=2))
    o.append(path("M19,199 L27,207 M27,199 L19,207", stroke="#fff", sw=2))
    o.append(text(36, 207, "a false winner: a test of two identical groups that looked significant", 10.5, INK))
    o.append(rect(16, 216, 14, 14, fill=LIGHT, stroke=RULE, rx=2))
    o.append(text(36, 227, "a test that correctly found nothing", 10.5, INK))
    o.append(text(16, 252, "Simulated in section 30.10: 200 tests, 14 daily looks each, stopping at the first p < 0.05.", 10.5, MUTED))
    return svg(W, 264, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig30-1-confidence-intervals.svg", fig_ci), ("fig30-2-power-curve.svg", fig_power),
                     ("fig30-3-experiment-order.svg", fig_design), ("fig30-4-peeking.svg", fig_peeking)]:
        open(name, "w").write(fn())
    print("ok30")
