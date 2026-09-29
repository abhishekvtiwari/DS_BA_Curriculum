# Wireframes for Chapter 70's dashboard critiques (Q70-069, Q70-070). Run: python3 make_figs70.py
# Canvas 680 px wide prints at 174 mm, so 10 px of text prints at 7.25 pt; nothing here is smaller.
import math
from make_figs import *
SOFT = "#eef2f7"; LIGHT = "#dfe5ec"; RED = "#b23b3b"
W = 680


def note(x, y, s):
    return text(x, y, s, 11, RED, "bold")


def frame(h, title):
    return (rect(10, 10, W - 20, h - 20, fill="#fff", stroke=MUTED, sw=1.4, rx=6)
            + rect(10, 10, W - 20, 30, fill=SOFT, rx=6) + text(24, 31, title, 12.5, INK, "bold", family=HEAD))


def slice_path(cx, cy, r, a0, a1, fill, ry=None, dx=0, dy=0):
    ry = ry or r
    x0, y0 = cx + dx + r * math.cos(a0), cy + dy + ry * math.sin(a0)
    x1, y1 = cx + dx + r * math.cos(a1), cy + dy + ry * math.sin(a1)
    large = 1 if a1 - a0 > math.pi else 0
    return (f'<path d="M{cx + dx:.1f},{cy + dy:.1f} L{x0:.1f},{y0:.1f} A{r},{ry} 0 {large} 1 {x1:.1f},{y1:.1f} Z" '
            f'fill="{fill}" stroke="#fff" stroke-width="1"/>')


def fig1():
    H = 360
    o = [frame(H, "Sales dashboard (all time)")]
    # two identical big-number cards
    for i, (lab, val) in enumerate([("Revenue this year", "₹ xx.x lakh"), ("Revenue last year", "₹ xx.x lakh")]):
        x = 26 + i * 158
        o.append(rect(x, 54, 146, 74, fill="#fff", stroke=ACC, sw=1.2, rx=4))
        o.append(text(x + 73, 76, lab, 10.5, MUTED, anchor="middle"))
        o.append(text(x + 73, 110, val, 20, INK, "bold", anchor="middle"))
    o.append(note(26, 146, "Same size, same style: which is which?"))
    # 14-slice pie
    cx, cy, r = 510, 120, 66
    shares = [16, 13, 11, 10, 9, 8, 7, 6, 5, 4, 4, 3, 2, 2]
    tones = [ACC, "#2f7d6d", "#b7791f", "#7a4fa0", "#c0662b", "#2f6690", "#8a9a5b", "#b23b3b",
             "#4f6d7a", "#a0522d", "#6b8e23", "#556b8d", "#9c6644", "#708090"]
    a = -math.pi / 2
    for s, t in zip(shares, tones):
        b = a + 2 * math.pi * s / sum(shares)
        o.append(slice_path(cx, cy, r, a, b, t)); a = b
    o.append(text(cx, 206, "Revenue by product: 14 slices", 10.5, INK, anchor="middle"))
    # raw table
    y0 = 222
    o.append(rect(26, y0, W - 52, 96, fill="#fff", stroke=LIGHT, sw=1))
    o.append(rect(26, y0, W - 52, 18, fill=SOFT))
    for j, h in enumerate(["order_id", "order_date", "customer", "product", "quantity", "net_revenue"]):
        o.append(text(34 + j * 104, y0 + 13, h, 10, MUTED, "bold"))
    for k in range(4):
        o.append(path(f"M26,{y0 + 36 + k * 18} H{W - 26}", stroke=LIGHT, sw=1))
    o.append(text(W / 2, y0 + 88, "… 3,000 rows, scroll to read …", 10.5, MUTED, anchor="middle", style="italic"))
    o.append(note(26, 342, "No filters, no date range: always all-time data"))
    return svg(W, H, "".join(o))


def gauge(x, y, pct, colour, label):
    r = 34
    o = [f'<path d="M{x - r},{y} A{r},{r} 0 0 1 {x + r},{y}" fill="none" stroke="{LIGHT}" stroke-width="12"/>']
    a = math.pi * (1 - pct)
    ex, ey = x + r * math.cos(a), y - r * math.sin(a)
    o.append(f'<path d="M{x - r},{y} A{r},{r} 0 0 1 {ex:.1f},{ey:.1f}" fill="none" stroke="{colour}" stroke-width="12"/>')
    o.append(text(x, y - 4, f"{round(pct * 100)}%", 11, INK, "bold", anchor="middle"))
    o.append(text(x, y + 16, label, 10.5, MUTED, anchor="middle"))
    return "".join(o)


def fig2():
    H = 350
    o = [frame(H, "Regional performance (live)")]
    regions = [("Region A", .92, "#c0662b"), ("Region B", .78, "#2f7d6d"), ("Region C", .64, "#7a4fa0"),
               ("Region D", .85, "#b23b3b"), ("Region E", .71, "#b7791f"), ("Region F", .58, ACC)]
    for i, (n, p, c) in enumerate(regions):
        o.append(gauge(72 + i * 107, 102, p, c, n))
    o.append(note(26, 146, "Six gauges, six colour schemes: one number each, read by angle"))
    # 3D exploded pie: a squashed ellipse with a rim, slices pulled apart
    cx, cy, rx, ry = 250, 238, 110, 44
    reps = [("Rep 1", .30, "#1b9e77"), ("Rep 2", .26, "#d95f02"), ("Rep 3", .22, "#7570b3"), ("Others", .22, "#e7298a")]
    a = -math.pi / 2
    parts = []
    for n, s, c in reps:
        b = a + 2 * math.pi * s
        mid = (a + b) / 2
        dx, dy = 12 * math.cos(mid), 6 * math.sin(mid)
        parts.append((a, b, c, dx, dy, n, mid)); a = b
    for a0, a1, c, dx, dy, n, mid in parts:      # rim first, then tops
        o.append(slice_path(cx, cy + 16, rx, a0, a1, "#9aa5b1", ry=ry, dx=dx, dy=dy))
    for a0, a1, c, dx, dy, n, mid in parts:
        o.append(slice_path(cx, cy, rx, a0, a1, c, ry=ry, dx=dx, dy=dy))
        lx, ly = cx + dx + (rx + 36) * math.cos(mid), cy + dy + (ry + 22) * math.sin(mid)
        o.append(text(lx, ly + 4, n, 10.5, INK, "bold", anchor="middle"))
    o.append(text(cx, 322, "Revenue by sales rep: 3D, exploded", 10.5, INK, anchor="middle"))
    o.append(rect(440, 190, 212, 92, fill="#fff", stroke=RED, sw=1.2, rx=4))
    o.append(text(452, 212, "Data source:", 11, INK, "bold"))
    o.append(text(452, 232, "production database,", 11, INK))
    o.append(text(452, 250, "DirectQuery, live on", 11, INK))
    o.append(text(452, 268, "every click", 11, INK))
    return svg(W, H, "".join(o))


if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).resolve().parent
    (here / "fig70-1-one-page-dashboard.svg").write_text(fig1(), encoding="utf-8")
    (here / "fig70-2-gauges-dashboard.svg").write_text(fig2(), encoding="utf-8")
    print("wrote fig70-1-one-page-dashboard.svg, fig70-2-gauges-dashboard.svg")
