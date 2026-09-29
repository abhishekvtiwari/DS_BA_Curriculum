# Generates the SVG figures for Chapter 43. Run from figures/ after checks/ch43_check.py has written
# checks/ch43_results.json:  python3 make_figs43.py
# Every figure is 700 px wide, printed at 493.2 pt, so 1 px = 0.705 pt: text is at least 10.5 px (7.4 pt).
import json, pathlib
from make_figs import *

ORANGE = "#c0662b"; ORANGEBG = "#fbe6d6"; BLUEBG = "#dce9f3"; RED = "#b23b3b"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch43_results.json").read_text())
W = 700


def line(x1, y1, x2, y2, c=RULE, sw=1, dash=None):
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke=c, sw=sw, dash=dash)


def circle(x, y, r, fill, stroke=INK, sw=1.4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def xor_point(x, y, label):
    # 0 = hollow circle, 1 = filled square: the shape and the printed digit carry the meaning, not colour
    if label:
        shape = rect(x - 8, y - 8, 16, 16, fill=ORANGE, stroke=INK, sw=1.2)
    else:
        shape = circle(x, y, 8.5, "#ffffff", ACC, 2.2)
    return shape + text(x + 13, y - 9, str(label), 13, INK, "bold")


def xor_panel(x0, title, with_grid):
    o = []; y0 = 290; size = 220                     # plot square for inputs from -0.2 to 1.2
    X = lambda a: x0 + (a + 0.2) / 1.4 * size
    Y = lambda b: y0 - (b + 0.2) / 1.4 * size
    if with_grid:
        grid = R["xor_grid"]; step = size / 57
        for i, row in enumerate(grid):          # row i: input 2 = (i - 8) / 40; column j: input 1
            j = 0
            while j < 57:
                k = j
                while k < 57 and (row[k] > 0.5) == (row[j] > 0.5):
                    k += 1
                o.append(rect(f"{x0 + j * step:.2f}", f"{y0 - (i + 1) * step:.2f}", f"{(k - j) * step + 0.4:.2f}",
                              f"{step + 0.4:.2f}", fill=ORANGEBG if row[j] > 0.5 else BLUEBG))
                j = k
        o.append(text(X(0.5), Y(0.5) + 4, "predicts 0", 11.5, INK, anchor="middle"))
        o.append(text(X(-0.17), Y(0.78), "predicts 1", 11.5, INK))
        o.append(text(X(0.72), Y(-0.13) + 4, "predicts 1", 11.5, INK))
    else:
        o.append(rect(x0, y0 - size, size, size, fill="#ffffff"))
        o.append(line(X(-0.2), Y(0.62), X(1.2), Y(0.28), RED, 1.8, "6 4"))
        o.append(text(X(0.28), Y(0.92), "one straight line:", 11.5, RED))
        o.append(text(X(0.28), Y(0.92) + 15, "a 1 and a 0 end up", 11.5, RED))
        o.append(text(X(0.28), Y(0.92) + 30, "on the same side", 11.5, RED))
    o.append(rect(x0, y0 - size, size, size, stroke=MUTED, sw=1))
    for v in (0, 1):
        o.append(text(X(v), y0 + 17, str(v), 11.5, MUTED, anchor="middle"))
        o.append(text(x0 - 8, Y(v) + 4, str(v), 11.5, MUTED, anchor="end"))
    for a, b, lab in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]:
        o.append(xor_point(X(a), Y(b), lab))
    o.append(text(x0 + size / 2, y0 + 36, "input 1", 11.5, INK, anchor="middle"))
    o.append(f'<text x="{x0 - 30}" y="{y0 - size / 2}" font-size="11.5" fill="{INK}" text-anchor="middle" '
             f'transform="rotate(-90 {x0 - 30} {y0 - size / 2})">input 2</text>')
    o.append(text(x0 + size / 2, 38, title, 13, INK, "bold", anchor="middle", family=HEAD))
    return "".join(o)


def fig_xor():
    body = xor_panel(70, "One neuron: a straight line", False) + xor_panel(420, "One hidden layer: a bent boundary", True)
    legend_y = 355
    body += rect(150, legend_y - 8, 16, 16, fill=ORANGE, stroke=INK, sw=1.2) + text(174, legend_y + 5, "target 1", 11.5, INK)
    body += circle(268, legend_y, 8.5, "#ffffff", ACC, 2.2) + text(284, legend_y + 5, "target 0", 11.5, INK)
    body += rect(380, legend_y - 8, 16, 16, fill=ORANGEBG, stroke=MUTED) + text(404, legend_y + 5, "network predicts 1", 11.5, INK)
    body += rect(540, legend_y - 8, 16, 16, fill=BLUEBG, stroke=MUTED) + text(564, legend_y + 5, "predicts 0", 11.5, INK)
    return svg(W, 372, body)


def fig_network():
    n = R["network"]; o = []
    inputs = [(90, 95, "x₁ = 1.0"), (90, 225, "x₂ = 0.5")]
    hidden = [(330, 95), (330, 225)]
    out = (570, 160)
    w1 = [[0.3, -0.2], [0.4, 0.1]]; w2 = [0.5, -0.6]
    # edges first, weight labels near the start of each edge
    for j, (hx, hy) in enumerate(hidden):
        for i, (ix, iy, _) in enumerate(inputs):
            o.append(line(ix + 34, iy, hx - 44, hy, MUTED, 1.3))
            t = 0.28 if i == j else 0.22
            lx = ix + 34 + t * (hx - 44 - ix - 34); ly = iy + t * (hy - iy)
            o.append(rect(lx - 17, ly - 10, 34, 17, fill="#ffffff"))
            o.append(text(lx, ly + 3, f"{w1[j][i]:g}", 11.5, ACC, "bold", anchor="middle"))
    for j, (hx, hy) in enumerate(hidden):
        o.append(line(hx + 44, hy, out[0] - 44, out[1], MUTED, 1.3))
        lx = hx + 44 + 0.45 * (out[0] - 44 - hx - 44); ly = hy + 0.45 * (out[1] - hy)
        o.append(rect(lx - 17, ly - 10, 34, 17, fill="#ffffff"))
        o.append(text(lx, ly + 3, f"{w2[j]:g}", 11.5, ACC, "bold", anchor="middle"))
    for ix, iy, lab in inputs:
        o.append(circle(ix, iy, 34, "#ffffff", INK))
        o.append(text(ix, iy + 4, lab, 11.5, INK, anchor="middle"))
    for j, (hx, hy) in enumerate(hidden):
        o.append(circle(hx, hy, 44, "#eef1f5", INK))
        o.append(text(hx, hy - 12, f"hidden {j + 1}", 10.5, MUTED, anchor="middle"))
        o.append(text(hx, hy + 4, f"z = {n['z1'][j]:.2f}", 11.5, INK, anchor="middle"))
        o.append(text(hx, hy + 19, f"a = {n['a1'][j]:.4f}", 11, INK, anchor="middle"))
        o.append(text(hx, hy + 60 if j else hy - 52, f"bias {[0.1, -0.1][j]:g}", 11, MUTED, anchor="middle"))
    o.append(circle(out[0], out[1], 44, "#fbe6d6", INK))
    o.append(text(out[0], out[1] - 14, "output", 10.5, MUTED, anchor="middle"))
    o.append(text(out[0], out[1] + 3, f"z = {n['z2']:.4f}", 11.5, INK, anchor="middle"))
    o.append(text(out[0], out[1] + 19, f"a = {n['a2']:.4f}", 11, INK, anchor="middle"))
    o.append(text(out[0], out[1] + 62, "bias 0.2", 11, MUTED, anchor="middle"))
    for x, lab in [(90, "inputs"), (330, "hidden layer (tanh)"), (570, "output (sigmoid)")]:
        o.append(text(x, 308, lab, 12, INK, "bold", anchor="middle"))
    return svg(W, 320, "".join(o))


def grid(x0, y0, cell, values, fmt, shade, marks=None, outline=None):
    o = []
    for r, row in enumerate(values):
        for c, v in enumerate(row):
            o.append(rect(x0 + c * cell, y0 + r * cell, cell, cell, fill=shade(v), stroke="#ffffff", sw=1))
            label = fmt(v)
            if label:
                o.append(text(x0 + c * cell + cell / 2, y0 + r * cell + cell / 2 + 4, label, 10.5,
                              "#ffffff" if shade(v) == INK else INK, anchor="middle"))
    if outline:
        r0, c0, k = outline
        o.append(rect(x0 + c0 * cell, y0 + r0 * cell, k * cell, k * cell, stroke=RED, sw=2.4))
    return "".join(o)


def fig_convolution():
    img = R["image"]; fm = R["feature_map"]; o = []
    ink = lambda v: INK if v >= 0.7 else ("#7d8595" if v >= 0.4 else ("#c9ced8" if v >= 0.1 else "#ffffff"))
    o.append(rect(20, 60, 8 * 27, 8 * 27, stroke=MUTED))
    o.append(grid(20, 60, 27, img, lambda v: "", ink, outline=(2, 2, 3)))
    o.append(text(20 + 4 * 27, 44, "the image (8 × 8)", 12.5, INK, "bold", anchor="middle", family=HEAD))
    o.append(text(20 + 4 * 27, 300, "darker = more ink; red box = the", 10.5, MUTED, anchor="middle"))
    o.append(text(20 + 4 * 27, 314, "first position tried (−0.56)", 10.5, MUTED, anchor="middle"))
    kern = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    kx = 272
    o.append(grid(kx, 128, 30, kern, lambda v: f"{v:+d}".replace("-", "−") if v else "0",
                  lambda v: BLUEBG if v < 0 else (ORANGEBG if v > 0 else "#f3f4f6")))
    o.append(text(kx + 45, 112, "the kernel", 12.5, INK, "bold", anchor="middle", family=HEAD))
    o.append(text(kx + 45, 242, "bottom row − top row", 10.5, MUTED, anchor="middle"))
    o.append(path(f"M{kx + 96},{173} L{kx + 128},{173}", stroke=MUTED, sw=1.6))
    o.append(path(f"M{kx + 121},{168} L{kx + 128},{173} L{kx + 121},{178}", stroke=MUTED, sw=1.6))
    o.append(text(kx + 45, 258, "slid over all 36 positions", 10.5, MUTED, anchor="middle"))
    fx = 410; cell = 44
    def shade(v):
        return ORANGEBG if v >= 0.5 else (BLUEBG if v <= -0.5 else "#ffffff")
    def fmt(v):
        mark = "+" if v >= 0.5 else ("−" if v <= -0.5 else "")
        return f"{mark}{abs(v):.1f}" if mark else f"{v:.1f}".replace("-", "−")
    o.append(rect(fx, 60, 6 * cell, 6 * cell, stroke=MUTED))
    o.append(grid(fx, 60, cell, fm, fmt, shade))
    o.append(text(fx + 3 * cell, 44, "the feature map (6 × 6)", 12.5, INK, "bold", anchor="middle", family=HEAD))
    o.append(text(fx + 3 * cell, 344, "+ ink begins going down   − ink ends going down", 10.5, MUTED, anchor="middle"))
    return svg(W, 356, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig43-1-xor.svg", fig_xor), ("fig43-2-network.svg", fig_network),
                     ("fig43-3-convolution.svg", fig_convolution)]:
        open(name, "w").write(fn())
    print("ok")
