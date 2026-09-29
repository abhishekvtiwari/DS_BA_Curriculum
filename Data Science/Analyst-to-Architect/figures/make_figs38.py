# Generates the SVG figures for Chapter 38. Run from figures/ after checks/ch38_check.py has written ch38_results.json.
# Every figure prints at the text width (493.2 pt): a font of s px on a W px canvas prints at s * 493.2 / W pt,
# so each figure keeps its smallest text at or above 7 pt (checked with tools/pdf/fig_check.py).
import json, pathlib
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from make_figs import *
PALE = "#eef1f5"; BAND = "#fdf3dc"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch38_results.json").read_text())
# one colour, one marker shape per k-means cluster, the same in every figure; the colours differ in lightness
# as well as hue, and the shapes carry the meaning in black and white
CLUSTER_COLORS = {0: "#0f5c8c", 1: "#c0662b", 2: "#6fb3a6", 3: "#6b3f93"}
NAMES = {0: "Growing regulars", 1: "Key accounts", 2: "Occasional buyers", 3: "Drifting away"}
SHAPES = {0: "circle", 1: "square", 2: "triangle", 3: "diamond"}


def line(x1, y1, x2, y2, c=RULE, sw=1, dash=None):
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke=c, sw=sw, dash=dash)


def poly(pts, c, sw=2.6):
    return path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), stroke=c, sw=sw)


def marker(x, y, cid, r=3.0, opacity=0.8):
    c = CLUSTER_COLORS[cid]; shape = SHAPES[cid]
    if shape == "circle":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" opacity="{opacity}"/>'
    if shape == "square":
        return f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r:.1f}" height="{2 * r:.1f}" fill="{c}" opacity="{opacity}"/>'
    if shape == "triangle":
        h = r * 1.25
        return f'<path d="M{x:.1f},{y - h:.1f} L{x + h:.1f},{y + h * 0.8:.1f} L{x - h:.1f},{y + h * 0.8:.1f} Z" fill="{c}" opacity="{opacity}"/>'
    h = r * 1.3
    return f'<path d="M{x:.1f},{y - h:.1f} L{x + h:.1f},{y:.1f} L{x:.1f},{y + h:.1f} L{x - h:.1f},{y:.1f} Z" fill="{c}" opacity="{opacity}"/>'


def fig_choose_k():
    """Two stacked panels sharing the k axis: inertia on top, silhouette below (no dual axis, no colour-only lines)."""
    o = []; W = 900; X0 = 120; PW = 600; data = R["k"]
    X = lambda k: X0 + (k - 2) / 6 * PW
    panels = [("Inertia (lower = tighter clusters)", 1, 13000, 26500, [15000, 20000, 25000], lambda v: f"{v / 1000:.0f}k", 40),
              ("Silhouette (higher = better separated)", 2, 0.15, 0.30, [0.15, 0.20, 0.25, 0.30], lambda v: f"{v:.2f}", 250)]
    # the k = 4 band, drawn first so everything sits on top of it
    o.append(rect(X(4) - 22, 30, 44, 400, fill=BAND))
    for title, idx, lo, hi, ticks, fmt, top in panels:
        H = 150; bottom = top + H
        Y = lambda v: bottom - (v - lo) / (hi - lo) * H
        o.append(text(X0 - 70, top - 12, title, 15, INK, "bold", family=HEAD))
        for v in ticks:
            o.append(line(X0, Y(v), X0 + PW, Y(v), PALE))
            o.append(text(X0 - 10, Y(v) + 5, fmt(v), 13.5, MUTED, anchor="end"))
        o.append(line(X0, bottom, X0 + PW, bottom, INK, 1.2))
        pts = [(X(k), Y(row[idx])) for k, *_ in data for row in [next(r for r in data if r[0] == k)]]
        o.append(poly(pts, ACC))
        for (k, *_), (x, y) in zip(data, pts):
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{ACC}"/>')
        if idx == 1:
            o.append(text(X(8) + 14, Y(data[-1][1]) + 5, f"{data[-1][1]:,.0f}", 13.5, INK))
            o.append(text(X(2) + 14, Y(data[0][1]) + 5, f"{data[0][1]:,.0f}", 13.5, INK))
            o.append(text(X(5) + 30, top + 28, "falls smoothly: no clear elbow", 14, MUTED, style="italic"))
        else:
            s2 = data[0][2]; s4 = data[2][2]
            o.append(line(X(2) + 6, Y(s2) - 4, X(2) + 60, Y(s2) - 22, MUTED, 1))
            o.append(text(X(2) + 64, Y(s2) - 20, f"highest at k = 2 ({s2:.3f})", 14, INK, "bold"))
            o.append(text(X(4) + 10, Y(s4) + 26, f"{s4:.3f}", 13.5, INK))
    for k, *_ in data:
        o.append(text(X(k), 425, str(k), 14, INK, anchor="middle"))
    o.append(text(X0 + PW / 2, 452, "Number of clusters (k)", 14, INK, anchor="middle"))
    o.append(text(X(4) + 30, 26, "k = 4 chosen: stable, and four groups the sales team can act on", 14, INK, "bold"))
    o.append(line(X(4), 30, X(4) + 26, 21, MUTED, 1))
    return svg(W, 470, "".join(o))


def fig_profiles():
    o = []; W = 860; X0 = 262; Y0 = 62; rowh = 88
    prof = R["profile"]
    cols = [("revenue", "Median revenue", lambda v: "₹" + lakh(v)), ("orders", "Orders (median)", lambda v: f"{v:.0f}"),
            ("recency", "Days since order", lambda v: f"{v:.0f}"), ("churn", "Churn rate, 2025", lambda v: f"{v:.1%}")]
    maxes = {key: max(p[key] for p in prof.values()) for key, *_ in cols}
    cw = (W - X0 - 10) / 4
    for j, (_, label, _) in enumerate(cols):
        o.append(text(X0 + j * cw, Y0 - 18, label, 13.5, MUTED, "bold"))
    for i, (cid, p) in enumerate(sorted(prof.items(), key=lambda kv: -kv[1]["revenue"])):
        y = Y0 + i * rowh; c = CLUSTER_COLORS[int(cid)]
        if i % 2 == 0:
            o.append(rect(8, y - 8, W - 16, rowh - 6, fill="#f6f9fc"))
        o.append(marker(22, y + 16, int(cid), r=6, opacity=1))
        o.append(text(38, y + 22, NAMES[int(cid)], 16, INK, "bold", family=HEAD))
        o.append(text(38, y + 44, f"{p['size']:,} accounts", 13.5, MUTED))
        o.append(text(38, y + 64, f"{p['revenue_share']:.1%} of 2024 revenue", 13.5, MUTED))
        for j, (key, _, fmt) in enumerate(cols):
            w = max(3, p[key] / maxes[key] * (cw - 22))
            o.append(rect(X0 + j * cw, y + 8, w, 22, fill=c, rx=3))
            o.append(text(X0 + j * cw, y + 52, fmt(p[key]), 14, INK))
    return svg(W, Y0 + 4 * rowh - 4, "".join(o))


def lakh(v):
    s = f"{v:.0f}"
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = [head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]
    return ",".join(parts) + "," + tail


def fig_six_dendro():
    """Figure 38.3: the six accounts merged by single linkage, drawn from the hand table."""
    o = []; W = 700; X0 = 110; Y0 = 250; H = 200; top = 8.0
    Y = lambda h: Y0 - h / top * H
    order = ["A", "B", "E", "C", "D", "F"]
    xs = {n: X0 + 30 + i * 90 for i, n in enumerate(order)}
    for v in [0, 2, 4, 6, 8]:
        o.append(line(X0, Y(v), W - 30, Y(v), PALE))
        o.append(text(X0 - 10, Y(v) + 5, f"{v}", 13.5, MUTED, anchor="end"))
    o.append(text(X0 - 45, Y(top) - 14, "Merge height (distance)", 14, INK, "bold"))
    def join(a, ha, b, hb, h, c):
        o.append(path(f"M{a:.1f},{Y(ha):.1f} V{Y(h):.1f} H{b:.1f} V{Y(hb):.1f}", stroke=c, sw=2.4))
        return (a + b) / 2
    left = ACC; right = "#c0662b"
    ab = join(xs["A"], 0, xs["B"], 0, 0.54, left)
    abe = join(ab, 0.54, xs["E"], 0, 1.30, left)
    cd = join(xs["C"], 0, xs["D"], 0, 3.00, right)
    cdf = join(cd, 3.00, xs["F"], 0, 3.16, right)
    join(abe, 1.30, cdf, 3.16, 7.12, INK)
    for label, x, h in [("0.54", ab, 0.54), ("1.30", abe, 1.30), ("3.00", cd, 3.00), ("3.16", cdf, 3.16), ("7.12", (abe + cdf) / 2, 7.12)]:
        o.append(text(x, Y(h) - 7, label, 13.5, INK, anchor="middle"))
    o.append(line(X0, Y(5), W - 30, Y(5), "#b23b3b", 1.6, dash="6 4"))
    o.append(text(W - 32, Y(5) - 7, "cut at 5: two groups", 13.5, "#b23b3b", "bold", anchor="end"))
    for n, x in xs.items():
        o.append(text(x, Y0 + 22, n, 15, INK, "bold", anchor="middle", family=HEAD))
    o.append(text(xs["B"], Y0 + 44, "{A, B, E}", 13.5, left, "bold", anchor="middle"))
    o.append(text(xs["D"], Y0 + 44, "{C, D, F}", 13.5, right, "bold", anchor="middle"))
    return svg(W, Y0 + 56, "".join(o))


def fig_dendro():
    """Figure 38.4: the 800-account Ward tree, last 30 merges, in the book's style. Each of the four branches
    below the cut is coloured and marked like the k-means cluster most of its accounts belong to."""
    Z = np.array(R["linkage"]); km = np.array(R["sample_kmeans"])
    from scipy.cluster.hierarchy import fcluster
    lab4 = fcluster(Z, t=4, criterion="maxclust")
    cut = (Z[-4, 2] + Z[-3, 2]) / 2
    d = dendrogram(Z, truncate_mode="lastp", p=30, no_plot=True, color_threshold=cut, above_threshold_color="k")
    W = 900; X0 = 90; Y0 = 300; H = 250; top = float(Z[-1, 2]) * 1.05
    xs_all = [x for ic in d["icoord"] for x in ic]; xmin, xmax = min(xs_all), max(xs_all)
    X = lambda v: X0 + 20 + (v - xmin) / (xmax - xmin) * (W - X0 - 60)
    Y = lambda h: Y0 - h / top * H
    o = []
    for v in range(0, int(top) + 1, 10):
        o.append(line(X0, Y(v), W - 30, Y(v), PALE))
        o.append(text(X0 - 10, Y(v) + 5, f"{v}", 13.5, MUTED, anchor="end"))
    o.append(text(X0 - 60, 22, "Merge height (Ward)", 14, INK, "bold"))
    # which k-means cluster dominates each hierarchical cluster, and where its branch sits
    groups = {}
    for g in range(1, 5):
        members = km[lab4 == g]
        top_c = int(np.bincount(members, minlength=4).argmax())
        groups[g] = (len(members), top_c, float((members == top_c).mean()))
    # map scipy's branch colours (C1..C4, left to right) to hierarchical clusters by leaf order
    leaf_groups = []
    for leaf in d["leaves"]:
        rows = [leaf] if leaf < len(km) else None
        leaf_groups.append(leaf)
    branch_colours = []
    for ic, dc, col in zip(d["icoord"], d["dcoord"], d["color_list"]):
        branch_colours.append(col)
    order = []
    for col in branch_colours:
        if col != "k" and col not in order:
            order.append(col)
    # left-to-right order of clusters in the drawing: sort clusters by the mean x of their branches
    xs_by_col = {c: np.mean([np.mean(ic) for ic, cc in zip(d["icoord"], branch_colours) if cc == c]) for c in order}
    cols_lr = sorted(order, key=lambda c: xs_by_col[c])
    # fcluster numbers follow the same left-to-right leaf order, so zip them by position
    g_lr = sorted(groups, key=lambda g: np.mean([i for i, l in enumerate(fcluster(Z, t=4, criterion="maxclust")) if l == g]))
    leaf_ids = dendrogram(Z, no_plot=True)["leaves"]
    pos = {leaf: i for i, leaf in enumerate(leaf_ids)}
    g_lr = sorted(groups, key=lambda g: np.mean([pos[i] for i in np.where(lab4 == g)[0]]))
    colour_of = {c: CLUSTER_COLORS[groups[g][1]] for c, g in zip(cols_lr, g_lr)}
    for ic, dc, col in zip(d["icoord"], d["dcoord"], branch_colours):
        c = colour_of.get(col, INK)
        o.append(path(f"M{X(ic[0]):.1f},{Y(dc[0]):.1f} V{Y(dc[1]):.1f} H{X(ic[2]):.1f} V{Y(dc[3]):.1f}", stroke=c, sw=2))
    o.append(line(X0, Y(cut), W - 30, Y(cut), "#b23b3b", 1.6, dash="6 4"))
    o.append(text(W - 32, Y(cut) - 8, "cut here for 4 clusters", 13.5, "#b23b3b", "bold", anchor="end"))
    for c, g in zip(cols_lr, g_lr):
        n, kc, share = groups[g]
        x = X(xs_by_col[c])
        o.append(marker(x - 50, Y0 + 22, kc, r=5, opacity=1))
        o.append(text(x - 40, Y0 + 27, f"{n} accounts", 13.5, INK, "bold"))
        o.append(text(x - 58, Y0 + 47, f"{share:.0%} {NAMES[kc]}", 13, MUTED))
    return svg(W, Y0 + 60, "".join(o))


def fig_kdist():
    kd = np.array(R["kdist"]); n = len(kd)
    o = []; W = 900; X0 = 90; Y0 = 250; PW = 640; H = 210; top = 2.6
    X = lambda i: X0 + i / (n - 1) * PW
    Y = lambda v: Y0 - min(v, top) / top * H
    for v in [0, 0.5, 1.0, 1.5, 2.0, 2.5]:
        o.append(line(X0, Y(v), X0 + PW, Y(v), PALE))
        o.append(text(X0 - 10, Y(v) + 5, f"{v:.1f}", 13.5, MUTED, anchor="end"))
    for eps in [0.5, 0.8, 1.0, 1.2]:
        o.append(line(X0, Y(eps), X0 + PW, Y(eps), "#b23b3b", 1.2, dash="3 4"))
        o.append(text(X0 + PW + 10, Y(eps) + 5, f"eps {eps}", 13.5, "#b23b3b"))
    o.append(poly([(X(i), Y(v)) for i, v in enumerate(kd)], ACC, 2.6))
    o.append(line(X0, Y0, X0 + PW, Y0, INK, 1.2))
    for share in [0, 0.25, 0.5, 0.75, 1.0]:
        o.append(text(X(share * (n - 1)), Y0 + 22, f"{share:.0%}", 13.5, MUTED, anchor="middle"))
    o.append(text(X0 + PW / 2, Y0 + 46, "Accounts, sorted by distance to their 14th neighbour", 14, INK, anchor="middle"))
    o.append(text(X0 - 60, 22, "Distance to 14th neighbour", 14, INK, "bold"))
    o.append(text(X(0.30 * (n - 1)), Y(1.9), "a gentle climb, no sharp knee", 14, MUTED, style="italic"))
    return svg(W, Y0 + 58, "".join(o))


def fig_maps():
    o = []; W = 1000; PWID = 280; H = 250
    for panel, (key, title) in enumerate([("pca", "PCA (54.1% of variance)"), ("tsne", "t-SNE"), ("umap", "UMAP")]):
        pts = np.array(R["coords"][key]); labs = R["coords"]["labels"]; X0 = 30 + panel * 330; Y0 = 300
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        X = lambda v: X0 + (v - lo[0]) / (hi[0] - lo[0]) * PWID; Y = lambda v: Y0 - (v - lo[1]) / (hi[1] - lo[1]) * H
        o.append(rect(X0 - 10, Y0 - H - 10, PWID + 20, H + 20, fill="none", stroke=RULE))
        # draw the biggest cluster first so the small ones stay visible on top
        for cid in [2, 0, 1, 3]:
            for (a, b), l in zip(pts, labs):
                if l == cid:
                    o.append(marker(X(a), Y(b), l, 2.4, 0.7))
        o.append(text(X0 - 10, Y0 - H - 20, title, 16, INK, "bold", family=HEAD))
    for i, cid in enumerate([1, 0, 2, 3]):
        x = 40 + i * 245
        o.append(marker(x, 340, cid, 6.5, 1)); o.append(text(x + 14, 346, NAMES[cid], 15, INK))
    return svg(W, 362, "".join(o))


if __name__ == "__main__":
    for name, fn in [("fig38-1-choosing-k.svg", fig_choose_k), ("fig38-2-cluster-profiles.svg", fig_profiles),
                     ("fig38-3-six-account-dendrogram.svg", fig_six_dendro), ("fig38-4-dendrogram.svg", fig_dendro),
                     ("fig38-5-k-distance.svg", fig_kdist), ("fig38-6-pca-tsne-umap.svg", fig_maps)]:
        open(name, "w").write(fn())
    print("ok")
