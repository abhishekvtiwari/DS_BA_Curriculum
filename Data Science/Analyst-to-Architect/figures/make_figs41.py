# Generates the SVG figures for Chapter 41. Run from figures/ after checks/ch41_check.py has written ch41_results.json.
# Figures print at the full text width (493.2 pt), so on a 720 px canvas every font must be >= 10.3 px (7 pt).
import json, pathlib
import numpy as np
from make_figs import *

GREEN = "#2f7d6d"; ORANGE = "#b35a1f"; GREY = "#5b6475"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch41_results.json").read_text())
W = 720
SMALL = 11          # smallest text on the page: 11 px on 720 px = 7.5 pt


def heatmap(x0, y0, title, cross, topics, labels):
    """One panel: rows = real categories, columns = discovered topics, cells = row share."""
    o = [text(x0, y0, title, 13, INK, "bold", family=HEAD)]
    lab_w, cw, rh = 108, 47, 25
    top = y0 + 30
    for j in range(5):
        o.append(text(x0 + lab_w + j * cw + (cw - 4) / 2, top - 8, f"topic {j}", SMALL, MUTED, anchor="middle"))
    for i, lab in enumerate(labels):
        y = top + i * rh
        o.append(text(x0 + lab_w - 8, y + 16, lab, SMALL, INK, anchor="end"))
        total = sum(cross[i])
        for j in range(5):
            share = cross[i][j] / total
            x = x0 + lab_w + j * cw
            o.append(rect(x, y, cw - 4, rh - 4, fill=ACC, rx=3, extra=f'fill-opacity="{0.06 + 0.84 * share:.2f}"'))
            if cross[i][j]:
                label = f"{share:.0%}" if share >= 0.005 else "<1%"
                colour = "#ffffff" if share >= 0.45 else INK
                o.append(text(x + (cw - 4) / 2, y + 15.5, label, SMALL, colour, "bold" if share >= 0.45 else "normal", anchor="middle"))
    # the topic key: each topic's strongest words ("order" is in every topic, so it's left out)
    ky = top + 5 * rh + 22
    o.append(text(x0, ky, "Strongest words in each topic", SMALL, MUTED, "bold"))
    for j, ws in enumerate(topics):
        shown = [w for w in ws if w != "order"][:5]
        o.append(text(x0, ky + 17 + j * 16, f"topic {j}: " + ", ".join(shown), SMALL, INK))
    return "".join(o), ky + 17 + 4 * 16 + 8


def fig_topics():
    labels = R["topics_order"]
    left, h1 = heatmap(8, 22, "LDA: share of each category", R["cross_lda"], R["lda_topics"], labels)
    right, h2 = heatmap(372, 22, "NMF: share of each category", R["cross_nmf"], R["nmf_topics"], labels)
    return svg(W, max(h1, h2), left + right)


GROUPS = {"defect words": (GREEN, "circle", ["broken", "crack", "damaged"]),
          "money words": (ORANGE, "square", ["invoice", "gst", "refund"]),
          "delivery words": (ACC, "triangle", ["delivery", "dispatch", "tracking"]),
          "other ticket words": (GREY, "diamond", ["order", "cancel", "address", "bulk", "pricing", "catalogue"])}


def marker(shape, x, y, colour, r=6):
    if shape == "circle":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{colour}"/>'
    if shape == "square":
        return rect(round(x - r + 0.5, 1), round(y - r + 0.5, 1), 2 * r - 1, 2 * r - 1, fill=colour)
    if shape == "triangle":
        return f'<path d="M{x:.1f},{y - r - 1:.1f} L{x + r + 1:.1f},{y + r - 1:.1f} L{x - r - 1:.1f},{y + r - 1:.1f} Z" fill="{colour}"/>'
    return f'<path d="M{x:.1f},{y - r - 1:.1f} L{x + r + 1:.1f},{y:.1f} L{x:.1f},{y + r + 1:.1f} L{x - r - 1:.1f},{y:.1f} Z" fill="{colour}"/>'


def fig_embed():
    pts = np.array(R["coords"]); words = R["vocab_words"]
    X0, Y0, PW, PH = 30, 50, 470, 280          # plot area: left, top, width, height
    lo, hi = pts.min(0) - 0.5, pts.max(0) + 0.5
    X = lambda v: X0 + (v - lo[0]) / (hi[0] - lo[0]) * PW
    Y = lambda v: Y0 + PH - (v - lo[1]) / (hi[1] - lo[1]) * PH
    style = {w: (c, s, g) for g, (c, s, ws) in GROUPS.items() for w in ws}
    o = [rect(X0 - 18, Y0 - 16, PW + 36, PH + 32, fill="none", stroke=RULE),
         text(X0 - 18, 22, "Fifteen ticket words, placed by their word2vec vectors (PCA, two components)", 13, INK, "bold", family=HEAD)]
    # place each label on the side (right, left, above, below) that collides least with other points and labels
    boxes = [(X(x) - 7, Y(y) - 7, X(x) + 7, Y(y) + 7) for x, y in pts]
    size = 12.5; cw = 0.6 * size
    def clash(b):
        return sum(not (b[2] < c[0] or b[0] > c[2] or b[3] < c[1] or b[1] > c[3]) for c in boxes)
    labels = []
    for w, (x, y) in zip(words, pts):
        px, py = X(x), Y(y); tw = cw * len(w)
        options = [(px + 10, py + 4.5, "start"), (px - 10, py + 4.5, "end"), (px, py - 11, "middle"), (px, py + 20, "middle")]
        def box(opt):
            tx, ty, a = opt
            left = tx if a == "start" else tx - tw if a == "end" else tx - tw / 2
            return (left - 1, ty - size + 2, left + tw + 1, ty + 3)
        best = min(options, key=lambda opt: (clash(box(opt)) - 1, options.index(opt)))  # -1: its own point
        boxes.append(box(best)); labels.append((w, best))
    for w, (x, y) in zip(words, pts):
        c, s, _ = style[w]
        o.append(marker(s, X(x), Y(y), c))
    for w, (tx, ty, a) in labels:
        o.append(text(round(tx, 1), round(ty, 1), w, size, INK, "normal", anchor=a))
    # key
    kx, ky = X0 + PW + 36, Y0 + 10
    o.append(text(kx, ky, "Key: groups by meaning", SMALL, MUTED, "bold"))
    for i, (g, (c, s, ws)) in enumerate(GROUPS.items()):
        y = ky + 26 + i * 24
        o.append(marker(s, kx + 7, y - 4, c))
        o.append(text(kx + 20, y, g, 12, INK))
    o.append(text(kx, ky + 26 + 4 * 24 + 10, "Axes are PCA directions:", SMALL, MUTED))
    o.append(text(kx, ky + 26 + 4 * 24 + 26, "only closeness matters.", SMALL, MUTED))
    return svg(W, Y0 + PH + 26, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig41-1-topic-models.svg", fig_topics), ("fig41-2-word-embeddings.svg", fig_embed)]:
        open(name, "w").write(fn())
    print("ok")
