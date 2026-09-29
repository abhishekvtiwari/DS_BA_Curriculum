# Generates the SVG figures for Chapter 53. Run from figures/: python3 make_figs53.py
# Needs companion/ch53/defect_data/ (companion/ch53/generate_defect_images.py) and
# checks/ch53_results.json (checks/ch53_check.py), so every drawn number is a real output.
# Figures print at the full text width (493.2 pt); every font here prints at 7 pt or more.
import base64, io, json, pathlib
import numpy as np
from PIL import Image
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; RED = "#b23b3b"
BOOK = pathlib.Path(__file__).resolve().parents[1]
DATA = BOOK / "companion" / "ch53" / "defect_data"
RESULTS = json.loads((BOOK / "checks" / "ch53_results.json").read_text())


def arrow(x1, y, x2, colour, sw=2):
    """A horizontal arrow from x1 to x2 with its head at x2."""
    d = 8 if x2 > x1 else -8
    return (path(f"M{x1},{y} H{x2}", stroke=colour, sw=sw)
            + path(f"M{x2 - d},{y - 6} L{x2},{y} L{x2 - d},{y + 6}", stroke=colour, sw=sw))


def fig_training_step():                       # Figure 53.1, section 53.2
    W = 820
    o = [text(20, 28, "One training step, with the numbers from section 53.2", 15, INK, "bold", family=HEAD)]
    xs = [20, 230, 440, 650]
    fwd = [("inputs", ["x = [1.0, 2.0]"], ACC), ("hidden layer", ["z1 = [2.1, 0.2]", "ReLU: a1 the same"], PURPLE),
           ("output", ["z2 = 1.420"], ACC), ("loss", ["(1.420 - 1.0)²", "= 0.176"], RED)]
    o.append(text(20, 62, "forward pass: predict, then measure how wrong  →", 13, MUTED, "bold"))
    for x, (title, lines, c) in zip(xs, fwd):
        o.append(rect(x, 74, 150, 84, fill="#fff", stroke=c, sw=1.8, rx=8))
        o.append(text(x + 75, 98, title, 13, c, "bold", anchor="middle"))
        for i, line in enumerate(lines):
            o.append(text(x + 75, 122 + i * 19, line, 12, INK, anchor="middle", family=MONO))
    for a, b in zip(xs, xs[1:]):
        o.append(arrow(a + 154, 116, b - 4, INK))
    back = [("dz1", ["[0.588, -0.420]"]), ("dW2", ["[1.764, 0.168]", "db2 = 0.840"]),
            ("dloss/dz2", ["2 × 0.420 = 0.840"])]
    o.append(text(20, 194, "←  backward pass: pass the blame back, in proportion to each input", 13, ORANGE, "bold"))
    o.append(rect(20, 206, 150, 84, fill=PKBG, stroke=ORANGE, sw=1.6, rx=8))
    o.append(text(95, 228, "dW1", 13, ORANGE, "bold", anchor="middle"))
    o.append(text(95, 252, "[[0.588, -0.420],", 12, INK, anchor="middle", family=MONO))
    o.append(text(95, 271, " [1.176, -0.840]]", 12, INK, anchor="middle", family=MONO))
    for x, (title, lines) in zip(xs[1:], back):
        o.append(rect(x, 206, 150, 84, fill=PKBG, stroke=ORANGE, sw=1.6, rx=8))
        o.append(text(x + 75, 228, title, 13, ORANGE, "bold", anchor="middle"))
        for i, line in enumerate(lines):
            o.append(text(x + 75, 252 + i * 19, line, 12, INK, anchor="middle", family=MONO))
    for a, b in zip(xs, xs[1:]):
        o.append(arrow(b - 4, 248, a + 154, ORANGE))
    o.append(rect(20, 312, 780, 62, fill=FKBG, stroke=GREEN, sw=1.6, rx=8))
    o.append(text(38, 337, "update:  weight = weight - 0.05 × gradient, for every weight", 13, GREEN, "bold", family=MONO))
    o.append(text(38, 360, "prediction 1.420 → 1.019,  loss 0.176 → 0.000.  Repeat thousands to millions of times.", 13, INK))
    return svg(W, 388, "".join(o))


def png_uri(image, scale=10):
    """A 32x32 image as a PNG data URI, enlarged 10x with nearest-neighbour so pixels stay square."""
    grey = Image.fromarray((np.clip(image, 0, 1) * 255).round().astype(np.uint8), mode="L")
    grey = grey.resize((image.shape[1] * scale, image.shape[0] * scale), Image.NEAREST)
    buf = io.BytesIO(); grey.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def fig_images():                              # Figure 53.2, section 53.6
    images = np.load(DATA / "images.npy"); kinds = np.load(DATA / "defect_types.npy")
    picks = [("good", 0), ("good", 1), ("good", 2), ("scratch", 0), ("void", 0), ("short_shot", 0)]
    W, size, gap, x0 = 960, 145, 12, 15
    o = []
    for n, (kind, which) in enumerate(picks):
        index = int(np.where(kinds == kind)[0][which])
        x = x0 + n * (size + gap)
        colour = GREEN if kind == "good" else RED
        label = ("good part" if kind == "good" else "defect: " + kind.replace("_", " "))
        o.append(text(x + size / 2, 24, label, 15, colour, "bold", anchor="middle"))
        o.append(f'<image x="{x}" y="36" width="{size}" height="{size}" preserveAspectRatio="none" '
                 f'style="image-rendering:pixelated" href="{png_uri(images[index])}"/>')
        o.append(rect(x, 36, size, size, stroke=colour, sw=2 if kind == "good" else 3))
        o.append(text(x + size / 2, 36 + size + 20, f"image {index:,}", 14, MUTED, anchor="middle"))
    return svg(W, 36 + size + 32, "".join(o))


def fig_threshold():                           # Figure 53.3, section 53.6
    rows = RESULTS["cv_table"]
    W = 900
    o = [text(20, 28, "The threshold is a business decision, not a modelling one", 15, INK, "bold", family=HEAD)]
    x0, x1, y0, y1 = 100, 540, 340, 84
    lo, hi = 20000, 100000
    def px(i): return x0 + 20 + i * (x1 - x0 - 30) / (len(rows) - 1)
    def py(c): return y0 - (c - lo) / (hi - lo) * (y0 - y1)
    for c in (20000, 40000, 60000, 80000, 100000):
        o.append(path(f"M{x0},{py(c)} H{x1}", stroke=RULE, sw=0.8, dash="3,4"))
        o.append(text(x0 - 10, py(c) + 5, f"₹{c // 1000}k", 13, MUTED, anchor="end"))
    o.append(path(f"M{x0},{y0} H{x1}", stroke=MUTED, sw=1.4)); o.append(path(f"M{x0},{y0} V{y1 - 6}", stroke=MUTED, sw=1.4))
    o.append(text(x0 - 10, y1 - 16, "cost", 13, INK, "bold", anchor="end"))
    costs = [r["cost"] for r in rows]
    best = costs.index(min(costs))
    o.append(path("M" + " L".join(f"{px(i)},{py(c)}" for i, c in enumerate(costs)), stroke=ACC, sw=2.5))
    for i, r in enumerate(rows):
        cheapest = i == best
        col = GREEN if cheapest else ACC
        if cheapest:          # a diamond, so the cheapest point differs by shape as well as colour
            cx, cy = px(i), py(r["cost"])
            o.append(f'<path d="M{cx},{cy - 9} L{cx + 9},{cy} L{cx},{cy + 9} L{cx - 9},{cy} Z" fill="{col}"/>')
        else:
            o.append(rect(px(i) - 5, py(r["cost"]) - 5, 10, 10, fill=col, stroke=col, rx=5))
        o.append(text(px(i), y0 + 20, f"{r['threshold']:g}", 13, INK, anchor="middle"))
        o.append(text(px(i), y0 + 40, f"{100 * r['accuracy']:.1f}%", 13, MUTED, anchor="middle"))
    o.append(text(x0 - 10, y0 + 20, "threshold", 13, INK, "bold", anchor="end"))
    o.append(text(x0 - 10, y0 + 40, "accuracy", 13, MUTED, "bold", anchor="end"))
    bx, by = px(best), py(costs[best])
    o.append(path(f"M{bx},{by - 12} V{by - 70}", stroke=GREEN, sw=1.4))      # leader up to a clear area
    o.append(text(bx, by - 78, f"cheapest: ₹{costs[best]:,}", 13, GREEN, "bold", anchor="middle"))
    first, low = rows[0], rows[best]
    o.append(rect(575, 60, 305, 318, fill=ROWALT, stroke=RULE, rx=8))
    lines = [("A missed defect costs ₹4,000.", INK, "bold"), ("A false alarm costs ₹40.", INK, "bold"), ("", INK, "normal"),
             (f"At {first['threshold']:g}: {first['missed']} missed, {first['false_alarms']} re-inspected,", MUTED, "normal"),
             (f"    ₹{first['cost']:,}", MUTED, "normal"),
             (f"At {low['threshold']:g}: {low['missed']} missed, {low['false_alarms']} re-inspected,", MUTED, "normal"),
             (f"    ₹{low['cost']:,}", MUTED, "normal"), ("", INK, "normal"),
             ("Same model, same 4,500 parts. Only", INK, "normal"), ("the threshold changed, and the bill", INK, "normal"),
             ("fell by about two thirds.", INK, "normal"), ("", INK, "normal"),
             ("Accuracy is highest at the most", INK, "bold"), ("expensive thresholds: it points the", INK, "bold"),
             ("wrong way, so nobody should quote it.", INK, "bold")]
    for i, (s, c, w) in enumerate(lines):
        o.append(text(591, 86 + i * 19.5, s, 13, c, w))
    return svg(W, 400, "".join(o))


def fig_attention():                           # Figure 53.4, section 53.7
    tokens = ["the", "crate", "was", "cracked"]
    weights = RESULTS["attention"]
    W = 820
    o = [text(20, 28, "Attention on four tokens: who listens to whom", 15, INK, "bold", family=HEAD)]
    x0, y0, cell = 160, 104, 74
    o.append(text(x0 + 2 * cell, y0 - 36, "attended to", 13, INK, "bold", anchor="middle"))
    for j, t in enumerate(tokens):
        o.append(text(x0 + j * cell + cell / 2 - 2, y0 - 12, t, 13, MUTED, "bold", anchor="middle"))
    for i, t in enumerate(tokens):
        o.append(text(x0 - 12, y0 + i * cell + cell / 2 + 3, t, 13, MUTED, "bold", anchor="end"))
        for j, w in enumerate(weights[i]):
            k = min(1.0, max(0.0, (w - 0.18) / 0.22))             # 0.18 -> pale, 0.40 -> dark
            r, g, b = (int(236 - 150 * k), int(243 - 120 * k), int(248 - 80 * k))
            o.append(rect(x0 + j * cell, y0 + i * cell, cell - 4, cell - 4, fill=f"rgb({r},{g},{b})", stroke=RULE, rx=5))
            o.append(text(x0 + j * cell + (cell - 4) / 2, y0 + i * cell + (cell - 4) / 2 + 5, f"{w:.3f}", 13,
                          "#ffffff" if k > 0.75 else INK, "bold" if k > 0.75 else "normal", anchor="middle", family=MONO))
    for n, s in enumerate(["the token", "doing the", "looking"]):
        o.append(text(56, y0 + 1.6 * cell + n * 18, s, 13, INK, "bold" if n == 0 else "normal", anchor="middle"))
    notes = [("Each row sums to 1: it is how one token", INK), ("divides its attention over the sentence.", INK), ("", INK),
             ("'cracked' puts 0.396 on 'crate', more", MUTED), ("than on any other token, including", MUTED),
             ("itself. Nothing told the model about", MUTED), ("grammar: the learned query of 'cracked'", MUTED),
             ("lines up with the learned key of 'crate'.", MUTED), ("", INK),
             ("Queries and keys decide who is", INK), ("listened to. Values decide what is heard.", INK)]
    for i, (s, c) in enumerate(notes):
        o.append(text(480, y0 + 8 + i * 21, s, 13, c))
    return svg(W, y0 + 4 * cell + 16, "".join(o))


def fig_pr_curve():                            # Figure 53.5, Answer 8
    pr = RESULTS["pr_curve"]; op = RESULTS["operating_point"]
    W = 700
    x0, x1, y0, y1 = 90, 470, 330, 50
    def px(r): return x0 + r * (x1 - x0)
    def py(p): return y0 - p * (y0 - y1)
    o = []
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        o.append(path(f"M{x0},{py(v)} H{x1}", stroke=RULE, sw=0.8, dash="3,4"))
        o.append(text(x0 - 10, py(v) + 5, f"{v:g}", 13, MUTED, anchor="end"))
        o.append(path(f"M{px(v)},{y0} V{y1}", stroke=RULE, sw=0.8, dash="3,4"))
        o.append(text(px(v), y0 + 22, f"{v:g}", 13, MUTED, anchor="middle"))
    o.append(path(f"M{x0},{y0} H{x1} M{x0},{y0} V{y1}", stroke=MUTED, sw=1.4))
    o.append(text((x0 + x1) / 2, y0 + 46, "recall (share of defects caught)", 13, INK, "bold", anchor="middle"))
    o.append(f'<text x="24" y="{(y0 + y1) / 2}" font-size="13" fill="{INK}" font-weight="bold" text-anchor="middle" '
             f'transform="rotate(-90 24 {(y0 + y1) / 2})">precision (flagged parts that are defective)</text>')
    pts = " L".join(f"{px(r):.1f},{py(p):.1f}" for r, p in zip(pr["recall"], pr["precision"]))
    o.append(path("M" + pts, stroke=ACC, sw=2.2))
    cx, cy = px(op["recall"]), py(op["precision"])
    o.append(f'<path d="M{cx},{cy - 8} L{cx + 8},{cy} L{cx},{cy + 8} L{cx - 8},{cy} Z" fill="{INK}"/>')
    o.append(path(f"M{cx - 10},{cy} L{cx - 60},{cy + 40}", stroke=INK, sw=1.2))
    o.append(text(cx - 64, cy + 56, f"threshold {op['threshold']:g}", 13, INK, "bold", anchor="end"))
    o.append(text(cx - 64, cy + 74, f"recall {op['recall']:.1%}, precision {op['precision']:.1%}", 13, INK, anchor="end"))
    notes = ["Out-of-fold predictions for", "the 4,500 training parts.", "",
             "The curve stays high until", "recall is about 0.95, then", "turns steeply down.", "",
             "The cost-chosen point sits", "on the steep part: it gives", "up precision to catch the", "last few defects."]
    for i, s in enumerate(notes):
        o.append(text(500, 70 + i * 20, s, 13, INK if i < 2 else MUTED))
    return svg(W, 390, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig53-1-training-step.svg", fig_training_step), ("fig53-2-defect-images.svg", fig_images),
                     ("fig53-3-threshold-cost.svg", fig_threshold), ("fig53-4-attention.svg", fig_attention),
                     ("fig53-5-pr-curve.svg", fig_pr_curve)]:
        (pathlib.Path(__file__).parent / name).write_text(fn(), encoding="utf-8")
    print("ok53")
