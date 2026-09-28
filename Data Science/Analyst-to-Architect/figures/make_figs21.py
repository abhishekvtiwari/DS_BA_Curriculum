# Figures for Chapter 21. Run from this folder: python3 make_figs21.py  (reads companion/ch21)
#
# Print size (V3, V21.8): every figure prints at the full text width, 174 mm = 493.2 pt. The matplotlib figures are
# drawn 6.85 in (493 pt) wide, so a font of s pt prints at about s pt; the smallest font used is 7.6 pt. matplotlib
# writes text as paths, which tools/pdf/fig_check.py can't read, so save() measures each figure's printed text size
# itself and the run ends with a report (every figure must print all its text at 7.0 pt or more).
# Figure 21.4 (the Bayes tree) is plain SVG with real <text> elements, which fig_check.py measures directly.
import pathlib, re, numpy as np, pandas as pd, matplotlib
from html import escape as esc
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
from scipy import stats
D = pathlib.Path(__file__).resolve().parent.parent / "companion"
INK, MUTED, ACC, ORANGE, GREEN, PURPLE, LIGHT, GREY = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#7a4fa0", "#dfe5ec", "#b8c0cc"
W_IN = 6.85                       # figure width in inches = the printed text width
FS, SM, TT = 8.0, 7.6, 8.6        # body text, smallest text, panel titles (pt; print at about the same size)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FS, "axes.titlesize": TT, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED, "axes.labelsize": FS,
                     "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": SM, "ytick.labelsize": SM,
                     "axes.edgecolor": "#c9d3df", "svg.fonttype": "path", "figure.dpi": 100})
PRINT_PT = 493.2
REPORT = []
def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
def printed_sizes(fig, svg_path):
    """Smallest and largest text size (pt) as the figure prints: font pt x 493.2 / SVG width pt."""
    fig.canvas.draw()
    sizes = [(t.get_fontsize(), t.get_text()) for t in fig.findobj(mtext.Text)
             if t.get_visible() and t.get_text().strip() and t.get_window_extent().width > 0]
    W = float(re.search(r'<svg[^>]*width="([\d.]+)pt"', pathlib.Path(svg_path).read_text()).group(1))
    lo, hi = min(sizes), max(sizes)
    return W, round(lo[0] * PRINT_PT / W, 2), lo[1], round(hi[0] * PRINT_PT / W, 2)
def save(fig, name):
    fig.savefig(name, format="svg", bbox_inches="tight", pad_inches=0.04)
    W, lo, lo_txt, hi = printed_sizes(fig, name); plt.close(fig)
    REPORT.append((name, W, lo, lo_txt, hi))

d = pd.read_csv(D / "ch21" / "delivery_times_2025.csv")

def mark(ax, value, color, ls, label, y, side):
    """A reference line with its label beside it: side='right' puts the label right of the line, 'left' left of it."""
    ax.axvline(value, color=color, lw=1.8, ls=ls)
    dx = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.015
    ax.text(value + dx if side == "right" else value - dx, y, label, color=color, fontsize=FS, fontweight="bold",
            ha="left" if side == "right" else "right", va="center",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0, "alpha": 0.9})

# 21.1 mean vs median (V21.6: each label on its own line's side, clear of the other line; solid vs dashed, not colour alone)
def f1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.55))
    v = d.order_value / 1000
    a.hist(v, bins=np.arange(0, 150, 2.5), color=ACC, edgecolor="white", lw=0.3)
    a.set_xlim(0, 150); top = a.get_ylim()[1] * 1.32; a.set_ylim(0, top)      # headroom: labels sit above the bars
    mark(a, v.mean(), ORANGE, "-", f"mean\n₹{d.order_value.mean():,.0f}", top * 0.87, "right")
    mark(a, v.median(), GREEN, "--", f"median\n₹{d.order_value.median():,.0f}", top * 0.87, "left")
    a.set_xlabel("Order value (₹ thousand)"); a.set_ylabel("Orders"); a.set_yticks(range(0, 3501, 500)); tidy(a)
    a.set_title("Order values: the mean sits\nabove the median")
    t = d.delivery_days
    b.hist(t, bins=np.arange(0, 20, 0.5), color=ACC, edgecolor="white", lw=0.3)
    b.set_xlim(0, 20); top = b.get_ylim()[1] * 1.32; b.set_ylim(0, top)
    mark(b, t.mean(), ORANGE, "-", f"mean\n{t.mean():.2f} days", top * 0.87, "right")
    mark(b, t.median(), GREEN, "--", f"median\n{t.median():.1f} days", top * 0.87, "left")
    b.set_xlabel("Delivery time (days)"); tidy(b)
    b.set_title("Delivery times: a long right\ntail pulls the mean")
    fig.subplots_adjust(left=0.08, right=0.99, wspace=0.22)
    save(fig, "fig21-1-mean-vs-median.svg")

# 21.2 spread by branch (V21.7: annotations in their own column right of the plot, clear of the outlier dots)
def f2():
    fig, ax = plt.subplots(figsize=(W_IN, 2.7))
    fig.subplots_adjust(left=0.13, right=0.76)
    order = ["Mumbai HO", "Bengaluru", "Delhi", "Kolkata"]
    data = [d[d.branch == b].delivery_days for b in order]
    ax.boxplot(data, orientation="horizontal", widths=0.5, patch_artist=True,
               flierprops={"marker": "o", "markersize": 2, "markerfacecolor": GREY, "markeredgecolor": "none", "alpha": 0.4},
               medianprops={"color": ORANGE, "lw": 2.0}, boxprops={"facecolor": "#e3edf5", "edgecolor": ACC},
               whiskerprops={"color": ACC}, capprops={"color": ACC})
    XMAX = 26
    for i, b in enumerate(order, 1):
        s = d[d.branch == b].delivery_days
        q1, q3 = s.quantile(.25), s.quantile(.75)
        ax.text(s.median(), i + 0.33, f"median {s.median():.1f}", color=ORANGE, fontsize=SM, ha="center", va="bottom")
        ax.text(XMAX + 0.8, i, f"IQR {q3-q1:.1f} d · p95 {s.quantile(.95):.1f} d", va="center", fontsize=SM, color=INK,
                clip_on=False)
        promise = d[d.branch == b].promised_days.iloc[0]
        ax.plot([promise] * 2, [i - 0.34, i + 0.34], color=PURPLE, lw=1.6, ls="--")
    ax.text(XMAX + 0.8, 4.62, "middle half · 95th pct", fontsize=SM, color=MUTED, va="bottom", clip_on=False)
    ax.set_yticks(range(1, 5)); ax.set_yticklabels(order); ax.set_xlim(0, XMAX); ax.set_ylim(0.45, 4.75)
    ax.set_xlabel("Delivery time (days); dots are single slow deliveries beyond the whiskers")
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="x", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
    ax.set_title("Delivery time by branch: the box is the middle half, the solid\nline in it the median, the dashed line the promise")
    save(fig, "fig21-2-spread-by-branch.svg")

# 21.3 four distributions (normal panel now shows the crate weights used in section 21.5)
def f3():
    fig, axs = plt.subplots(1, 4, figsize=(W_IN, 1.95))
    x = np.linspace(484, 516, 400)
    axs[0].plot(x, stats.norm.pdf(x, 500, 4), color=ACC, lw=1.8); axs[0].fill_between(x, stats.norm.pdf(x, 500, 4), color=ACC, alpha=0.12)
    axs[0].set_title("Normal\ncrate weight"); axs[0].set_xlabel("grams"); axs[0].set_xticks([488, 500, 512])
    k = np.arange(0, 17)
    axs[1].bar(k, stats.binom.pmf(k, 40, 0.182), color=GREEN, width=0.8)
    axs[1].set_title("Binomial\nlate, of 40"); axs[1].set_xlabel("late deliveries"); axs[1].set_xticks([0, 5, 10, 15])
    k2 = np.arange(0, 21)
    axs[2].bar(k2, stats.poisson.pmf(k2, 9.4), color=PURPLE, width=0.8)
    axs[2].set_title("Poisson\ncomplaints/week"); axs[2].set_xlabel("complaints"); axs[2].set_xticks([0, 5, 10, 15, 20])
    axs[3].bar([1, 2, 3, 4, 5, 6], [1/6]*6, color=ORANGE, width=0.7)
    axs[3].set_title("Uniform\none die roll"); axs[3].set_xlabel("face"); axs[3].set_xticks([1, 2, 3, 4, 5, 6])
    for a in axs:
        a.spines[["top", "right", "left"]].set_visible(False); a.set_yticks([])
    fig.subplots_adjust(left=0.01, right=0.99, wspace=0.12)
    save(fig, "fig21-3-distributions.svg")

# 21.5 central limit theorem
def f5():
    rng = np.random.default_rng(21)
    population = d.order_value.to_numpy()
    fig, axs = plt.subplots(1, 4, figsize=(W_IN, 2.05))
    axs[0].hist(population/1000, bins=np.arange(0, 150, 3), color=GREY, edgecolor="white", lw=0.3)
    axs[0].set_title(f"The orders\nskew {pd.Series(population).skew():.2f}")
    axs[0].set_xlabel("₹ thousand"); axs[0].set_xticks([0, 50, 100, 150])
    for ax, n in zip(axs[1:], [5, 30, 100]):
        means = rng.choice(population, size=(4000, n)).mean(axis=1) / 1000
        ax.hist(means, bins=np.arange(0, 60.5, 1), color=ACC, edgecolor="white", lw=0.3)
        ax.set_title(f"Means of {n}\nsd ₹{means.std():.1f}k")
        ax.set_xlabel("₹ thousand"); ax.set_xlim(0, 60); ax.set_xticks([0, 25, 50])
    for a in axs:
        a.spines[["top", "right", "left"]].set_visible(False); a.set_yticks([])
    fig.subplots_adjust(left=0.01, right=0.99, wspace=0.12)
    save(fig, "fig21-5-central-limit.svg")

# 21.4 Bayes tree of counts (SVG with real text; canvas 720 px -> 1 px prints at 0.685 pt, so 11 px = 7.53 pt)
def svg_text(x, y, s, size=12, fill=INK, weight="normal", anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'
def box(x, y, w, h, lines, flagged=False):
    fill, stroke, sw = ("#e3edf5", ACC, 2.0) if flagged else ("#ffffff", "#9aa6b5", 1.0)
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    for i, (t, bold) in enumerate(lines):
        o.append(svg_text(x + w / 2, y + 19 + i * 16, t, size=12.5 if i == 0 else 11.5, weight="bold" if bold else "normal",
                          anchor="middle", fill=INK if i == 0 else MUTED))
    return "".join(o)
def edge(x1, y1, x2, y2, label, above=True):
    """A curved branch from (x1, y1) to (x2, y2), labelled just before the box it leads to, clear of the curve."""
    mx = (x1 + x2) / 2
    return (f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" fill="none" stroke="#9aa6b5" stroke-width="1.4"/>'
            + svg_text(x2 - 6, y2 + (-6 if above else 16), label, size=11.5, fill=MUTED, anchor="end"))
def f4():
    W, H = 720, 300
    o = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    bw, bh, lw = 118, 44, 140
    PX, LX = 185, 405                                  # x of the middle boxes and of the leaves
    o.append(box(8, 119, 104, bh, [("10,000 crates", True)]))
    o.append(box(PX, 37, bw, bh, [("200 defective", True), ("2%", False)]))
    o.append(box(PX, 201, bw, bh, [("9,800 good", True), ("98%", False)]))
    o.append(edge(112, 141, PX, 59, "2% defective"))
    o.append(edge(112, 141, PX, 223, "98% good", above=False))
    leaves = [(8, "180 flagged", "defective and flagged", True, 59, "flags 90%"),
              (66, "20 not flagged", "defective, missed", False, 59, "misses 10%"),
              (172, "490 flagged", "good but flagged", True, 223, "flags 5%"),
              (230, "9,310 not flagged", "good, passed", False, 223, "passes 95%")]
    for y, t1, t2, fl, py, lab in leaves:
        o.append(box(LX, y, lw, bh, [(t1, True), (t2, False)], flagged=fl))
        o.append(edge(PX + bw, py, LX, y + bh / 2, lab, above=(y + bh / 2 < py)))
    bx = LX + lw + 10                                  # bracket joining the two flagged leaves
    o.append(f'<path d="M{bx},30 H{bx+12} V194 H{bx}" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
    o.append(f'<path d="M{bx+12},112 H{bx+22}" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
    o.append(svg_text(bx + 27, 98, "670 flagged", size=12.5, weight="bold"))
    o.append(svg_text(bx + 27, 116, "180 defective:", size=11.5, fill=MUTED))
    o.append(svg_text(bx + 27, 133, "180 ÷ 670 = 26.9%", size=11.5, weight="bold", fill=ACC))
    o.append(svg_text(8, 292, "Flagged crates are the two boxes with a thick border. Counts out of 10,000 crates.", size=11, fill=MUTED))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="DejaVu Sans, Arial, sans-serif">' + "".join(o) + "</svg>")
    pathlib.Path("fig21-4-bayes-tree.svg").write_text(svg, encoding="utf-8")
    REPORT.append(("fig21-4-bayes-tree.svg", W, round(11 * PRINT_PT / W, 2), "caption line", round(12.5 * PRINT_PT / W, 2)))

if __name__ == "__main__":
    f1(); f2(); f3(); f4(); f5()
    bad = 0
    for name, W, lo, lo_txt, hi in REPORT:
        ok = lo >= 7.0; bad += not ok
        print(f"{'OK   ' if ok else 'SMALL'} {name}: canvas {W:.0f} pt, text prints {lo}-{hi} pt (smallest: {lo_txt!r})")
    print(f"{bad} figure(s) with text under 7 pt")
