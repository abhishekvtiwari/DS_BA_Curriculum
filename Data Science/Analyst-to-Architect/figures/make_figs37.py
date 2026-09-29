# Generates the SVG figures for Chapter 37. Run from figures/ after checks/ch37_check.py has written ch37_results.json.
# Canvases are 640 px wide and print at 174 mm (493.2 pt), so 1 px = 0.77 pt: every font here is >= 10 px (7.7 pt).
import json, math, pathlib
from make_figs import *
GREEN = "#2f7d6d"; ORANGE = "#b8541a"; PALE = "#e3e8ef"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch37_results.json").read_text())
FS = 11  # tick labels
def line(x1, y1, x2, y2, c=RULE, sw=1, dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke=c, sw=sw, dash=dash)
def dot(x, y, c, r=4.5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
def square(x, y, c, s=8.5): return f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
def poly(pts, c, sw=2.2, dash=None): return path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), stroke=c, sw=sw, dash=dash)
def vlabel(x, y, s, size=11.5): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{INK}" font-family="{SANS}" text-anchor="middle" transform="rotate(-90 {x} {y})">{s}</text>'


def fig_resid():
    o = []; X0, Y0, W, H = 70, 250, 540, 210
    pts = R["resid"]; xs = [p[0] for p in pts]
    lo, hi = math.floor(min(xs)), math.ceil(max(xs))
    X = lambda v: X0 + (v - lo) / (hi - lo) * W; Y = lambda v: Y0 - H / 2 - v / 1.2 * (H / 2)
    for v in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        o.append(line(X0, Y(v), X0 + W, Y(v), PALE)); o.append(text(X0 - 8, Y(v) + 4, f"{v:+.1f}" if v else "0", FS, MUTED, anchor="end"))
    for v in range(lo, hi + 1):
        o.append(text(X(v), Y0 + 18, str(v), FS, MUTED, anchor="middle"))
    for a, b in pts:
        o.append(f'<circle cx="{X(a):.1f}" cy="{Y(max(-1.2, min(1.2, b))):.1f}" r="1.7" fill="{ACC}" fill-opacity="0.45"/>')
    o.append(line(X0, Y(0), X0 + W, Y(0), INK, 1.4, dash="5,4"))
    o.append(text(X0 + W / 2, Y0 + 40, "Predicted log revenue 2025", 11.5, INK, anchor="middle"))
    o.append(vlabel(X0 - 48, Y0 - H / 2, "Residual (log scale)"))
    return svg(640, 300, "".join(o))


def fig_lasso():
    o = []; X0, W = 80, 500; data = R["lasso"]
    lo, hi = math.log10(0.001), math.log10(0.2)
    X = lambda a: X0 + (math.log10(a) - lo) / (hi - lo) * W
    panels = [("Features kept", 30, 150, lambda k: k, 0, 20, [0, 5, 10, 15, 20], "{:.0f}", ACC, dot),
              ("Test R²", 225, 150, lambda r: r, 0.90, 1.00, [0.90, 0.95, 1.00], "{:.2f}", GREEN, square)]
    for title, top, H, get, vmin, vmax, ticks, fmt, col, mark in panels:
        Y0 = top + H; Y = lambda v: Y0 - (v - vmin) / (vmax - vmin) * H
        o.append(text(X0, top - 8, title, 12.5, INK, "bold", family=HEAD))
        for t in ticks:
            o.append(line(X0, Y(t), X0 + W, Y(t), PALE)); o.append(text(X0 - 8, Y(t) + 4, fmt.format(t), FS, MUTED, anchor="end"))
        vals = [(a, k if title == "Features kept" else r) for a, k, r in data]
        o.append(poly([(X(a), Y(v)) for a, v in vals], col))
        for a, v in vals:
            o.append(mark(X(a), Y(v), col))
            lab = f"{v:.0f}" if title == "Features kept" else f"{v:.3f}"
            o.append(text(X(a), Y(v) - 10, lab, 10.5, INK, anchor="middle"))
    for a in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
        o.append(text(X(a), 395, f"{a:g}", FS, MUTED, anchor="middle"))
    o.append(text(X0 + W / 2, 416, "Lasso alpha (log scale)", 11.5, INK, anchor="middle"))
    return svg(640, 425, "".join(o))


def fig_depth():
    o = []; X0, Y0, W, H = 70, 270, 500, 230; data = R["depth"]
    X = lambda i: X0 + i / (len(data) - 1) * W; Y = lambda v: Y0 - (v - 0.5) / 0.5 * H
    for v in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        o.append(line(X0, Y(v), X0 + W, Y(v), PALE)); o.append(text(X0 - 8, Y(v) + 4, f"{v:.1f}", FS, MUTED, anchor="end"))
    for i, (d, _, _) in enumerate(data): o.append(text(X(i), Y0 + 18, "none" if d == 30 else str(d), FS, MUTED, anchor="middle"))
    o.append(poly([(X(i), Y(t)) for i, (_, t, _) in enumerate(data)], ORANGE))
    o.append(poly([(X(i), Y(v)) for i, (_, _, v) in enumerate(data)], ACC, dash="6,3"))
    for i, (_, t, v) in enumerate(data): o.append(dot(X(i), Y(t), ORANGE)); o.append(square(X(i), Y(v), ACC))
    best = max(range(len(data)), key=lambda i: data[i][2])
    bx, by = X(best), Y(data[best][2])
    o.append(line(bx, by - 7, bx + 38, by - 52, INK, 1))
    o.append(text(bx + 42, by - 56, f"best validation: {data[best][2]:.3f} at depth {data[best][0]}", 11, INK, "bold"))
    o.append(text(X(len(data) - 1) + 10, Y(data[-1][1]) + 4, "training", 11.5, ORANGE, "bold"))
    o.append(text(X(len(data) - 1) + 10, Y(data[-1][2]) + 4, "validation", 11.5, ACC, "bold"))
    o.append(text(X0 + W / 2, Y0 + 40, "Maximum tree depth", 11.5, INK, anchor="middle"))
    o.append(vlabel(X0 - 45, Y0 - H / 2, "AUC"))
    return svg(640, 320, "".join(o))


def fig_curves():
    o = []; X0, W, H = 80, 430, 160
    X = lambda v: X0 + v / 3300 * W
    for p, (key, title, top) in enumerate([("logistic", "Logistic regression", 30), ("boosting", "Gradient boosting (tuned)", 245)]):
        n, tr, cv = R["curves"][key]; Y0 = top + H
        Y = lambda v: Y0 - (v - 0.7) / 0.3 * H
        o.append(text(X0, top - 10, title, 12.5, INK, "bold", family=HEAD))
        for v in [0.7, 0.8, 0.9, 1.0]:
            o.append(line(X0, Y(v), X0 + W, Y(v), PALE)); o.append(text(X0 - 8, Y(v) + 4, f"{v:.1f}", FS, MUTED, anchor="end"))
        for v in [0, 800, 1600, 2400, 3200]: o.append(text(X(v), Y0 + 17, f"{v:,}", FS, MUTED, anchor="middle"))
        o.append(poly([(X(a), Y(b)) for a, b in zip(n, tr)], ORANGE)); o.append(poly([(X(a), Y(b)) for a, b in zip(n, cv)], ACC, dash="6,3"))
        for a, b, c in zip(n, tr, cv): o.append(dot(X(a), Y(b), ORANGE)); o.append(square(X(a), Y(c), ACC))
        o.append(text(X(n[-1]) + 10, Y(tr[-1]) + 4, f"training {tr[-1]:.3f}", 11.5, ORANGE, "bold"))
        o.append(text(X(n[-1]) + 10, Y(cv[-1]) + 4, f"CV {cv[-1]:.3f}", 11.5, ACC, "bold"))
        o.append(vlabel(X0 - 45, Y0 - H / 2, "AUC"))
    o.append(text(X0 + W / 2, 470, "Training rows", 11.5, INK, anchor="middle"))
    return svg(640, 480, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig37-1-residuals.svg", fig_resid), ("fig37-2-lasso-path.svg", fig_lasso),
                     ("fig37-3-tree-depth.svg", fig_depth), ("fig37-4-learning-curves.svg", fig_curves)]:
        open(name, "w").write(fn())
    print("ok")
