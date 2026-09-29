# Diagrams for Chapter 66. Run: python3 make_figs66.py (from the figures folder)
# Every figure prints at the full text width (493.2 pt). All canvases are 680 px wide, so
# 1 px = 0.725 pt: the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
# Text is wrapped by measuring it with the DejaVu Sans metrics the PDF uses, so no label runs
# past its box. Figure 66.1's scores are read from companion/ch66/maturity_scorecard.csv.
# Figure 66.2 (the ROI chart) is drawn by make_figs66_chart.py.
import math, os
import pandas as pd
from PIL import ImageFont
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; GOLD = "#b7791f"; BLUE2 = "#2f6690"; GREY = "#8a93a3"
SOFT = "#eef2f7"; LIGHT = "#dfe5ec"
W = 680
MIN = 10.5
HERE = os.path.dirname(os.path.abspath(__file__))
SCORECARD = os.path.join(HERE, "..", "companion", "ch66", "maturity_scorecard.csv")

_fonts = {}
def width(s, size, bold=False):
    if bold not in _fonts:
        _fonts[bold] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" +
                                          ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), 100)
    return _fonts[bold].getlength(s) * size / 100

def wrap(s, size, max_w, bold=False):
    lines, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if width(trial, size, bold) <= max_w or not line:
            line = trial
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    for l in lines:
        assert width(l, size, bold) <= max_w + 0.5, f"too wide: {l!r}"
    return lines

def lines_at(x, y, lines, size, fill=INK, weight="normal", anchor="start", lead=None):
    lead = lead or size * 1.3
    return "".join(text(x, y + i * lead, l, size, fill, weight, anchor=anchor) for i, l in enumerate(lines))

def arrow(x1, y1, x2, y2, c=MUTED, sw=1.5):
    a = math.atan2(y2 - y1, x2 - x1); s = 7
    p1 = (x2 - s * math.cos(a - 0.45), y2 - s * math.sin(a - 0.45))
    p2 = (x2 - s * math.cos(a + 0.45), y2 - s * math.sin(a + 0.45))
    return (path(f"M{x1},{y1} L{x2},{y2}", stroke=c, sw=sw)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>')

def title(s):
    return text(20, 26, s, 14, INK, "bold", family=HEAD)


def f1():
    """Six dimensions on the five-stage scale; technical ones are circles, organizational diamonds."""
    m = pd.read_csv(SCORECARD)
    m["score"] = m.stage_met + m.next_met / 5
    m = m.sort_values("score", ascending=False)
    technical = {"Data quality & reliability", "Architecture & platform", "Security & access"}
    o = [title("Riverstone's maturity, six dimensions, scored against written criteria")]
    x0, cw, y0 = 200, 94, 62                       # stage columns: x0 .. x0 + 5*cw = 670
    stages = ["1 Ad hoc", "2 Reactive", "3 Proactive", "4 Managed", "5 Optimized"]
    rh = 34
    top, bottom = y0 - 4, y0 + len(m) * rh
    for i, s in enumerate(stages):
        if i == 2:
            o.append(rect(x0 + i * cw, top, cw, bottom - top, fill="#f3f7fb"))
        o.append(text(x0 + i * cw + cw / 2, y0 - 14, s, 10.5, MUTED, "bold", anchor="middle"))
        o.append(path(f"M{x0 + i * cw},{top} V{bottom}", stroke=LIGHT, sw=1))
    o.append(path(f"M{x0 + 5 * cw},{top} V{bottom}", stroke=LIGHT, sw=1))
    for j, row in enumerate(m.itertuples()):
        y = y0 + j * rh + rh / 2
        o.append(path(f"M{x0},{y} H{x0 + 5 * cw}", stroke="#eef1f5", sw=1))
        o.append(text(20, y + 4, row.dimension, 11, INK, "bold"))
        cx = x0 + (row.score - 1) * cw
        tech = row.dimension in technical
        c = ACC if tech else GOLD
        if tech:
            o.append(f'<circle cx="{cx:.1f}" cy="{y}" r="7" fill="{c}"/>')
        else:
            o.append(f'<path d="M{cx:.1f},{y - 8} L{cx + 8:.1f},{y} L{cx:.1f},{y + 8} L{cx - 8:.1f},{y} Z" fill="{c}"/>')
        o.append(text(cx + 13, y + 4, f"{row.score:.1f}", 11, c, "bold"))
    ly = bottom + 24
    o.append(f'<circle cx="26" cy="{ly - 4}" r="6" fill="{ACC}"/>')
    o.append(text(38, ly, "technical dimension", 10.5, MUTED))
    o.append(f'<path d="M190,{ly - 11} L197,{ly - 4} L190,{ly + 3} L183,{ly - 4} Z" fill="{GOLD}"/>')
    o.append(text(203, ly, "organizational dimension", 10.5, MUTED))
    note = ("Score = the highest stage whose five criteria are all met, plus one-fifth for each "
            "criterion of the next stage that is met. The technical dimensions sit in stage 3; "
            "the organizational ones lag in stages 1 and 2. Read the lowest score first.")
    ls = wrap(note, 10.5, W - 40)
    o.append(lines_at(20, ly + 24, ls, 10.5, MUTED))
    return svg(W, ly + 24 + len(ls) * 13.7 + 8, "".join(o))


def box(x, y, w, h, head, c, body):
    o = [rect(x + 2, y + 3, w, h, fill=SOFT, rx=6), rect(x, y, w, h, fill="#fff", stroke=c, sw=1.5, rx=6)]
    hl = wrap(head, 11, w - 16, bold=True)
    hh = 10 + len(hl) * 14
    o.append(f'<path d="M{x},{y + 6} a6,6 0 0 1 6,-6 H{x + w - 6} a6,6 0 0 1 6,6 V{y + hh} H{x} Z" fill="{c}"/>')
    o.append(lines_at(x + w / 2, y + 17, hl, 11, "#fff", "bold", anchor="middle", lead=14))
    bl = wrap(body, 10.5, w - 18)
    o.append(lines_at(x + 9, y + hh + 17, bl, 10.5, INK, lead=13.8))
    return "".join(o), hh + 17 + len(bl) * 13.8


def f2():
    """Team structure, one hire at a time (Figure 66.3)."""
    o = [title("Team structure: from four people to a function, one hire at a time")]
    cols = [("At Chapter 60: a four-person team", ACC,
             "Meera (Head of Data Platform) and three others. Centralized: serves the whole "
             "company, so every request queues behind every other."),
            ("Then: one domain hire", GREEN,
             "The Taloja plant's own data analyst (Ch 62). The mesh check reran at 12 of 25: "
             "not a mesh, but one plant data product owned by the plant."),
            ("Proposed next: catalog and governance owner", GOLD,
             "For the weakest dimension in section 66.2, catalog and discoverability (1.8). "
             "Not another generalist: the specific gap the maturity scores found.")]
    bw, gap, y = 196, 26, 48
    parts = [box(20 + i * (bw + gap), y, bw, 0, h, c, b) for i, (h, c, b) in enumerate(cols)]
    hmax = max(h for _, h in parts) + 8
    for i, (h, c, b) in enumerate(cols):
        svgpart, _ = box(20 + i * (bw + gap), y, bw, hmax, h, c, b)
        o.append(svgpart)
    for i in range(2):
        x1 = 20 + (i + 1) * bw + i * gap + 3
        o.append(arrow(x1, y + hmax / 2, x1 + gap - 6, y + hmax / 2))
    note = ("Each hire is justified by a specific, named gap this book already found, "
            "not headcount added because growth “felt right.”")
    nl = wrap(note, 10.5, W - 40)
    o.append(lines_at(20, y + hmax + 26, nl, 10.5, MUTED))
    return svg(W, y + hmax + 26 + len(nl) * 13.7 + 6, "".join(o))


def f3():
    """Build vs buy scorecard for a managed data catalog (Figure 66.4)."""
    o = [title("Build vs. buy: a managed data catalog, scored honestly")]
    rows = [("Time to a working solution", "Weeks", "Months of a 4-person team's time", "Buy"),
            ("Fit to Riverstone's exact needs", "Good enough", "Perfect, eventually", "Build (eventually)"),
            ("Ongoing maintenance", "The vendor's problem", "The 4-person team's problem, forever", "Buy"),
            ("Cost at current scale", "A predictable subscription", "Engineering time, not on any bill", "Buy"),
            ("Lock-in risk", "Real: switching is expensive", "Worse: one person understands it", "Buy, narrowly")]
    xs = [20, 200, 360, 540]; ws = [172, 152, 172, 120]
    y = 44
    o.append(rect(20, y, W - 40, 24, fill=INK, rx=3))
    for h, x in zip(["Dimension", "Buy", "Build", "Edge to"], xs):
        o.append(text(x + 6, y + 16, h, 11, "#fff", "bold"))
    y += 24
    for k, (dim, buy, build, edge) in enumerate(rows):
        cells = [wrap(dim, 10.5, ws[0] - 10, bold=True), wrap(buy, 10.5, ws[1] - 10),
                 wrap(build, 10.5, ws[2] - 10), wrap(edge, 10.5, ws[3] - 10, bold=True)]
        n = max(len(c) for c in cells)
        h = 12 + n * 13.8
        o.append(rect(20, y, W - 40, h, fill="#fff" if k % 2 == 0 else "#f6f9fc"))
        build_wins = edge.startswith("Build")
        for i, c in enumerate(cells):
            fill = INK if i == 0 else (MUTED if i < 3 else (GOLD if build_wins else ACC))
            o.append(lines_at(xs[i] + 6, y + 18, c, 10.5, fill, "bold" if i in (0, 3) else "normal", lead=13.8))
        y += h
    o.append(path(f"M20,{y} H{W - 20}", stroke=RULE, sw=1))
    note = ("Buy wins on four of five dimensions. Build wins only on fit, and only eventually: "
            "worth it when Riverstone's needs are genuinely unlike anyone else's, which a "
            "catalog's needs, honestly, are not.")
    nl = wrap(note, 10.5, W - 40)
    o.append(lines_at(20, y + 22, nl, 10.5, MUTED))
    return svg(W, y + 22 + len(nl) * 13.7 + 6, "".join(o))


if __name__ == "__main__":
    for n, f in [("fig66-1-maturity-model.svg", f1), ("fig66-3-team-evolution.svg", f2),
                 ("fig66-4-build-vs-buy.svg", f3)]:
        open(os.path.join(HERE, n), "w").write(f())
    print("ok")
