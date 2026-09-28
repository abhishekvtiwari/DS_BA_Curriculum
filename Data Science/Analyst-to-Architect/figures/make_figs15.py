# Generates the figures for Chapter 15 (SVG, via matplotlib). Run: python3 make_figs15.py
# Data: companion/ch15/chart_data/*.csv, built by companion/ch15/build_ch15_data.py from the full Riverstone dataset.
#
# Print size (V3, V15.1-V15.7): every figure prints at the full text width, 174 mm = 493.2 pt. The figures are drawn
# 6.85 in (493 pt) wide, so a font of s pt prints at about s pt; the smallest font used is 7.6 pt. matplotlib writes
# text as paths, which tools/pdf/fig_check.py can't read, so save() measures every figure's printed text size itself
# and the run ends with a report (every figure must print all its text at 7.0 pt or more).
import pathlib, re, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch15" / "chart_data"
INK="#1d2330"; MUTED="#5b6475"; ACC="#0f5c8c"; RULE="#c9d3df"; GREY="#b8c0cc"; LIGHT="#dfe5ec"
ORANGE="#c0662b"; GREEN="#2f7d6d"; RED="#b23b3b"; PURPLE="#7a4fa0"; GOLD="#b7791f"
OKABE=["#0072B2","#E69F00","#009E73","#CC79A7","#56B4E9","#D55E00","#F0E442","#000000"]
W_IN = 6.85                       # figure width in inches = the printed text width
FS = 8.0                          # body text in figures (pt, prints at about the same size)
SM = 7.6                          # smallest text used anywhere
TT = 8.6                          # panel titles
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":FS,"axes.edgecolor":RULE,"axes.labelcolor":MUTED,"xtick.color":MUTED,
    "ytick.color":MUTED,"xtick.labelsize":SM,"ytick.labelsize":SM,"legend.fontsize":SM,"axes.labelsize":FS,
    "axes.titlesize":TT,"axes.titleweight":"bold","axes.titlecolor":INK,"axes.titlelocation":"left",
    "svg.fonttype":"path","figure.dpi":100})
def tidy(ax, grid="y"):
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    if grid: ax.grid(axis=grid, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

PRINT_PT = 493.2          # the printed text width in pt (tools/pdf/fig_check.py)
REPORT = []
def printed_sizes(fig, svg_path):
    """Smallest and largest text size (pt) as the figure prints: font pt x 493.2 / SVG width pt."""
    fig.canvas.draw()
    sizes = [(t.get_fontsize(), t.get_text()) for t in fig.findobj(mtext.Text)
             if t.get_visible() and t.get_text().strip() and t.get_window_extent().width > 0]
    W = float(re.search(r'<svg[^>]*width="([\d.]+)pt"', pathlib.Path(svg_path).read_text()).group(1))
    lo = min(sizes); hi = max(sizes)
    return W, round(lo[0] * PRINT_PT / W, 2), lo[1], round(hi[0] * PRINT_PT / W, 2)
def save(fig, name):
    fig.savefig(name, format="svg", bbox_inches="tight", pad_inches=0.04, dpi=300)   # 300 ppi for embedded rasters (V12)
    W, lo, lo_txt, hi = printed_sizes(fig, name); plt.close(fig)
    REPORT.append((name, W, lo, lo_txt, hi))
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

seg = pd.read_csv(D/"segment_2025.csv"); mon = pd.read_csv(D/"monthly_2023_2025.csv"); ov = pd.read_csv(D/"order_values_2025.csv")
cu = pd.read_csv(D/"customers_2025.csv"); br = pd.read_csv(D/"bridge_2024_2025.csv"); hm = pd.read_csv(D/"region_month_2025.csv").set_index("region")
cat = pd.read_csv(D/"category_month_2025.csv").set_index("month").fillna(0); reg = pd.read_csv(D/"region_2025.csv")
prod = pd.read_csv(D/"product_2025.csv"); rep = pd.read_csv(D/"rep_month_2025.csv").set_index("month"); gm = pd.read_csv(D/"margin_by_year.csv")
ans = pd.read_csv(D/"anscombe.csv")
MISSING = "City missing"          # the no-city bucket, one label everywhere (V15.16)
REGIONS = ["West", "South", "North", "East"]

# 15.1 pie vs bar
def f1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.45), gridspec_kw={"width_ratios":[1,1.45]})
    a.pie(seg.net_revenue, labels=seg.segment, colors=[ACC, GREEN, GOLD], startangle=90, counterclock=False,
          wedgeprops={"edgecolor":"white","linewidth":1.5}, textprops={"color":INK, "fontsize":FS})
    a.set_title("Pie: is Wholesale bigger\nthan Hospitality?")
    s = seg.sort_values("net_revenue")
    b.barh(s.segment, s.net_revenue/1e7, color=[GOLD, GREEN, ACC], height=0.6)
    for y, v, p in zip(range(3), s.net_revenue/1e7, s.share_pct): b.text(v+1, y, f"₹{v:,.1f} cr ({p}%)", va="center", color=INK)
    b.set_xlim(0, 85); b.set_xlabel("Net revenue, 2025 (₹ crore)"); tidy(b, "x"); b.set_title("Bar: the same data, compared by length")
    fig.subplots_adjust(wspace=0.45)
    save(fig, "fig15-1-pie-vs-bar.svg")

# 15.3 bars: unsorted vertical vs sorted horizontal
def f3():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.9), gridspec_kw={"width_ratios":[1,1.15]})
    p = prod.sort_values("product_name")
    a.bar(range(8), p.net_revenue/1e7, color=OKABE[:8]); a.set_xticks(range(8)); a.set_xticklabels(p.product_name, rotation=50, ha="right")
    a.set_title("Before: alphabetical, rotated\nlabels, rainbow"); tidy(a); a.set_ylabel("₹ crore")
    q = prod.sort_values("net_revenue")
    b.barh(q.product_name, q.net_revenue/1e7, color=GREY, height=0.65)
    for i, v in enumerate(q.net_revenue/1e7): b.text(v+0.4, i, f"{v:,.1f}", va="center", color=INK)
    b.set_title("After: sorted, horizontal,\nlabeled, one color"); tidy(b, None); b.set_xticks([]); b.spines["bottom"].set_visible(False)
    b.set_xlabel("Net revenue, 2025 (₹ crore)"); b.set_xlim(0, 27)
    fig.subplots_adjust(wspace=0.75)
    save(fig, "fig15-3-sorted-bars.svg")

# 15.4 lines
def f4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.6))
    x = np.arange(36)
    a.plot(x, mon.net_revenue/1e7, color=ACC, lw=1.8)
    a.set_xticks([0,12,24]); a.set_xticklabels(["Jan 2023","Jan 2024","Jan 2025"]); tidy(a); a.set_ylim(0, 21); a.set_ylabel("₹ crore")
    a.set_title("One line, 36 months: growth\nplus a yearly cycle")
    i = mon.net_revenue.idxmax(); a.annotate("Oct 2025: ₹18.1 cr", (i, mon.net_revenue[i]/1e7), xytext=(9, 19.3), color=INK,
                                             arrowprops={"arrowstyle":"-","color":MUTED})
    for y, c, lw in [(2023, GREY, 1.4), (2024, "#7fa7c4", 1.6), (2025, ACC, 2.3)]:
        d = mon[mon.year == y]; b.plot(range(12), d.net_revenue/1e7, color=c, lw=lw)
        b.text(11.25, d.net_revenue.iloc[-1]/1e7 + (0.9 if y == 2025 else -0.4 if y == 2024 else -1.0), str(y), color=c if y != 2023 else MUTED, va="center", fontweight="bold")
    b.set_xticks(range(12)); b.set_xticklabels([m[0] for m in MON]); b.set_xlim(-0.3, 12.6); b.set_ylim(0, 21); tidy(b)
    b.set_title("One line per year:\nOctober peaks")
    fig.subplots_adjust(wspace=0.25)
    save(fig, "fig15-4-lines.svg")

# 15.5 histograms with three bin widths
def f5():
    fig, axs = plt.subplots(1, 3, figsize=(W_IN, 2.2))
    for ax, w, t in zip(axs, [1000, 5000, 25000], ["₹1,000 bins: noisy", "₹5,000 bins: the shape", "₹25,000 bins: too coarse"]):
        bins = np.arange(0, 150001, w); ax.hist(ov.order_value, bins=bins, color=ACC, edgecolor="white", lw=0.2 if w==1000 else 0.6)
        ax.set_title(t); tidy(ax); ax.set_xlim(0, 150000); ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
        ax.set_xticks([0, 50000, 100000, 150000]); ax.set_xlabel("Order value (₹)")
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.0f}")
    axs[0].set_ylabel("Orders, 2025")
    fig.subplots_adjust(wspace=0.45)
    save(fig, "fig15-5-histogram-bins.svg")

# 15.6 box plots by segment
def f6():
    fig, ax = plt.subplots(figsize=(W_IN, 2.5))
    order = ["Hospitality", "Retail", "Wholesale"]
    data = [ov[ov.segment == s].order_value/1000 for s in order]
    ax.boxplot(data, vert=False, widths=0.5, patch_artist=True, flierprops={"marker":"o","markersize":2.5,"markerfacecolor":GREY,"markeredgecolor":"none","alpha":0.6},
               medianprops={"color":ORANGE,"lw":2.2}, boxprops={"facecolor":"#e3edf5","edgecolor":ACC}, whiskerprops={"color":ACC}, capprops={"color":ACC})
    ax.set_yticks([1,2,3]); ax.set_yticklabels(order, fontsize=FS)
    for i, s in enumerate(order, 1):
        med = ov[ov.segment == s].order_value.median(); ax.text(med/1000, i+0.38, f"median ₹{med:,.0f}", ha="center", color=ORANGE)
    ax.set_xlabel("Order value, 2025 (₹ thousand)"); tidy(ax, "x"); ax.set_xlim(0, 150); ax.set_ylim(0.5, 3.65)
    ax.set_title("Wholesale orders are larger and more spread out; dots are orders beyond the whiskers")
    save(fig, "fig15-6-box-plots.svg")

# 15.8 scatter
def f7():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.7), sharey=True)
    a.scatter(cu.orders, cu.net_revenue/1e5, s=9, color=ACC); a.set_title("Before: 4,599 dots on\ntop of each other"); tidy(a, "both")
    a.set_xlabel("Orders in 2025"); a.set_ylabel("Net revenue, 2025 (₹ lakh)")
    rng = np.random.default_rng(15)
    for s, c, mk in [("Retail", ACC, "o"), ("Hospitality", GOLD, "s"), ("Wholesale", GREEN, "^")]:
        d = cu[cu.segment == s]; b.scatter(d.orders + rng.uniform(-0.3, 0.3, len(d)), d.net_revenue/1e5, s=6, alpha=0.35, color=c, marker=mk, label=s, edgecolors="none")
    leg = b.legend(frameon=False, markerscale=2.2, loc="upper left")
    for h in leg.legend_handles: h.set_alpha(1)          # full-strength legend markers (V15.15)
    tidy(b, "both"); b.set_xlabel("Orders in 2025 (jittered)")
    b.set_title("After: transparency, jitter,\nand color by segment")
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig15-8-scatter.svg")

# 15.9 composition: stacked columns and waterfall
def f8():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.9))
    cols = ["Storage", "Kitchen", "Industrial", "Furniture"]; colors = [ACC, "#6c9bc0", GREEN, GOLD]
    bottom = np.zeros(12)
    for c, col in zip(cols, colors):
        a.bar(range(12), cat[c]/1e7, bottom=bottom, color=col, label=c, width=0.75); bottom += cat[c].values/1e7
    a.set_xticks(range(12)); a.set_xticklabels([m[0] for m in MON]); tidy(a); a.legend(frameon=False, ncol=2, loc="upper left", handlelength=1.2, columnspacing=0.8)
    a.set_ylabel("₹ crore"); a.set_ylim(0, 26); a.set_title("Stacked: totals clear,\nmiddles hard")
    start = br["2024"].sum()/1e7; end = br["2025"].sum()/1e7
    steps = [("2024", start)] + [(s, ch/1e7) for s, ch in br.sort_values("change", ascending=False)[["segment","change"]].itertuples(index=False)] + [("2025", end)]
    run = 0
    for i, (lab, v) in enumerate(steps):
        if i == 0 or i == len(steps)-1:
            b.bar(i, v, color=ACC, width=0.6); b.text(i, v+2, f"{v:,.1f}", ha="center", color=INK); run = v
        else:
            b.bar(i, v, bottom=run, color=GREEN, width=0.6); b.text(i, run+v+2, f"+{v:,.1f}", ha="center", color=GREEN)
            b.plot([i-0.7, i-0.3], [run, run], color=MUTED, lw=0.8); run += v
    b.plot([len(steps)-1.7, len(steps)-1.3], [run, run], color=MUTED, lw=0.8)
    b.set_xticks(range(len(steps))); tidy(b); b.set_ylim(0, 130); b.set_ylabel("₹ crore")
    b.set_xticklabels([("Hospi-\ntality" if s[0] == "Hospitality" else "Whole-\nsale" if s[0] == "Wholesale" else s[0]) for s in steps])
    b.set_title("Waterfall: where growth\ncame from")
    fig.subplots_adjust(wspace=0.3)
    save(fig, "fig15-9-composition.svg")

# 15.10 heatmaps
def f9():
    fig, (a, b) = plt.subplots(2, 1, figsize=(W_IN, 4.1), gridspec_kw={"height_ratios":[5,3]})
    h = hm.loc[REGIONS + [MISSING]]/1e7
    a.imshow(h.values, aspect="auto", cmap="Blues", vmin=0)
    for i in range(h.shape[0]):
        for j in range(12):
            v = h.values[i, j]; a.text(j, i, f"{v:.1f}", ha="center", va="center", color="white" if v > 3.2 else INK)
    a.set_xticks(range(12)); a.set_xticklabels(MON); a.set_yticks(range(5)); a.set_yticklabels(h.index, fontsize=FS)
    a.set_title("Sequential: revenue by region and month, 2025 (₹ crore); darker = more"); a.tick_params(length=0)
    for s in a.spines.values(): s.set_visible(False)
    att = mon.pivot(index="year", columns="month", values="attainment_pct")
    b.imshow(att.values, aspect="auto", cmap="RdBu", vmin=85, vmax=115)
    for i in range(3):
        for j in range(12):
            v = att.values[i, j]; b.text(j, i, f"{v:.0f}", ha="center", va="center", color="white" if abs(v-100) > 9 else INK)
    b.set_xticks(range(12)); b.set_xticklabels(MON); b.set_yticks(range(3)); b.set_yticklabels(att.index, fontsize=FS); b.tick_params(length=0)
    for s in b.spines.values(): s.set_visible(False)
    b.set_title("Diverging: % of target, centered on 100 (red below, blue above)")
    fig.tight_layout(h_pad=1.2); save(fig, "fig15-10-heatmaps.svg")

# 15.11 highlight one line
def f10():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 3.5), sharey=True)
    for i, c in enumerate(rep.columns): a.plot(range(12), rep[c]/1e7, lw=1.3, color=plt.cm.tab20(i), label=c)
    a.legend(ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), handlelength=1.2, columnspacing=0.8, labelspacing=0.25)
    a.set_title("Before: 11 colors, one\nlegend to decode"); tidy(a)
    a.set_xticks(range(12)); a.set_xticklabels([m[0] for m in MON]); a.set_ylabel("₹ crore")
    for c in rep.columns:
        if c != "Rahul Mehta": b.plot(range(12), rep[c]/1e7, lw=1.0, color=LIGHT)
    b.plot(range(12), rep["Rahul Mehta"]/1e7, lw=2.4, color=ORANGE)
    b.text(11.2, rep["Rahul Mehta"].iloc[-1]/1e7, "Rahul\nMehta", color=ORANGE, va="center", fontweight="bold")
    b.text(11.2, rep.drop(columns="Rahul Mehta").iloc[-1].median()/1e7, "10 other\nreps", color=MUTED, va="center")
    b.set_xticks(range(12)); b.set_xticklabels([m[0] for m in MON]); b.set_xlim(-0.3, 14.2); tidy(b)
    b.set_title("After: gray for context,\none color for the story")
    fig.subplots_adjust(wspace=0.08)
    save(fig, "fig15-11-highlight.svg")

# 15.12 title that states the finding
def f11():
    fig, (a, b) = plt.subplots(2, 1, figsize=(W_IN, 4.9))
    d = mon[mon.year == 2025]
    for ax in (a, b):
        ax.plot(range(12), d.net_revenue/1e7, color=ACC, lw=2.2, marker="o", ms=3.5)
        ax.plot(range(12), d.target_revenue/1e7, color=MUTED, lw=1.3, ls="--")
        ax.set_xticks(range(12)); ax.set_xticklabels(MON); ax.set_ylim(0, 22); tidy(ax)
    a.set_title("Monthly Revenue vs Target 2025"); a.legend(["Actual", "Target"], frameon=False, loc="upper left"); a.set_ylabel("Revenue")
    b.set_title("2025 finished at 98.3% of target: a strong January–February,\nthen a Q4 short of an ambitious plan")
    b.text(11.15, d.net_revenue.iloc[-1]/1e7-1.1, "Actual", color=ACC, fontweight="bold")
    b.text(11.15, d.target_revenue.iloc[-1]/1e7+0.7, "Target", color=MUTED)
    b.annotate("October: ₹18.1 cr, a record month,\nbut 92% of its ₹19.6 cr target", (9, 18.06), xytext=(3.2, 17.6), color=INK,
               arrowprops={"arrowstyle":"-","color":MUTED})
    b.set_ylabel("Net revenue (₹ crore)"); b.set_xlim(-0.3, 12.3)
    fig.tight_layout(h_pad=1.6); save(fig, "fig15-12-titles.svg")

# 15.13 misleading: truncated axis and dual axis (two panels on top, the dual axis below: V15.6)
def f12():
    fig = plt.figure(figsize=(W_IN, 4.9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.55, wspace=0.45)
    a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, :])
    names = ["Delhi", "Bengaluru"]; vals = [101831086, 101788506]
    a.bar(names, np.array(vals)/1e7, color=[ORANGE, ACC], width=0.55); a.set_ylim(10.175, 10.1835); tidy(a)
    a.set_title("Truncated axis: looks\nlike a big gap"); a.yaxis.set_major_formatter(lambda v, _: f"{v:.3f}"); a.set_ylabel("₹ crore")
    b.bar(names, np.array(vals)/1e7, color=[ORANGE, ACC], width=0.55); b.set_ylim(0, 11); tidy(b)
    b.set_title("Zero baseline: the\ngap is 0.04%"); b.set_ylabel("₹ crore")
    x = gm.year.astype(str)
    c.bar(x, gm.net_revenue/1e7, color=LIGHT, width=0.5, label="Revenue (bars, left axis)"); c.set_ylim(55, 118); c.set_ylabel("Revenue (₹ crore)"); tidy(c)
    c2 = c.twinx(); c2.plot(x, gm.gross_margin_pct, color=RED, marker="o", lw=2.0, label="Gross margin (line, right axis)")
    c2.set_ylim(20, 28.5); c2.set_ylabel("Gross margin %", color=RED)
    c2.spines["top"].set_visible(False); c.set_title("Dual axis: two scales chosen to agree (left axis starts at 55, right at 20)")
    h1, l1 = c.get_legend_handles_labels(); h2, l2 = c2.get_legend_handles_labels()
    c.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
    save(fig, "fig15-13-misleading.svg")

# 15.14 showing missing data
def f13():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W_IN, 2.4))
    r = reg[reg.region != MISSING]
    a.barh(r.region[::-1], r.net_revenue[::-1]/1e7, color=ACC, height=0.6); tidy(a, "x"); a.set_title("Before: revenue with no\ncity silently dropped")
    a.set_xlabel("₹ crore, 2025"); a.set_xlim(0, 42)
    known = reg[reg.region != MISSING].sort_values("net_revenue")
    rr = pd.concat([reg[reg.region == MISSING], known])      # barh draws bottom-up: City missing at the bottom
    b.barh(rr.region, rr.net_revenue/1e7, color=[GREY if l == MISSING else ACC for l in rr.region], height=0.6)
    for i, v in enumerate(rr.net_revenue/1e7): b.text(v+0.5, i, f"{v:,.1f}", va="center")
    tidy(b, None); b.set_xticks([]); b.spines["bottom"].set_visible(False); b.set_xlim(0, 44)
    b.set_title("After: ₹2.3 cr with no city\nshown, in gray, at the bottom")
    fig.subplots_adjust(wspace=0.45)
    save(fig, "fig15-14-missing-data.svg")

# 15.7 Anscombe (2 x 2, V15.7)
def f14():
    fig, axs = plt.subplots(2, 2, figsize=(W_IN, 3.9), sharex=True, sharey=True)
    sets = [(ans.x_1_2_3, ans.y1), (ans.x_1_2_3, ans.y2), (ans.x_1_2_3, ans.y3), (ans.x4, ans.y4)]
    for k, (ax, (x, y)) in enumerate(zip(axs.flat, sets), 1):
        ax.scatter(x, y, color=ACC, s=16); m, c0 = np.polyfit(x, y, 1); xs = np.array([3, 20]); ax.plot(xs, m*xs+c0, color=ORANGE, lw=1.2)
        ax.set_title(f"Dataset {k}"); ax.set_xlim(2, 20); ax.set_ylim(2, 14); tidy(ax, "both")
    for ax in axs[1]: ax.set_xlabel("x")
    for ax in axs[:, 0]: ax.set_ylabel("y")
    fig.suptitle("Same means, correlation (0.82), and trend line; four different stories", x=0.07, ha="left", fontsize=TT, fontweight="bold", color=INK, y=0.99)
    fig.subplots_adjust(hspace=0.45, wspace=0.12, top=0.86)
    save(fig, "fig15-7-anscombe.svg")

# project: five "before" charts from the old management pack (V15.2: bad chart choices, readable type)
def project_before():
    fig = plt.figure(figsize=(W_IN, 7.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1.15, 1.05], hspace=0.55, wspace=0.42)
    a = fig.add_subplot(gs[0, 0]); p = prod
    a.pie(p.net_revenue, labels=p.product_name, colors=plt.cm.rainbow(np.linspace(0,1,8)), explode=[0.08]*8, shadow=True, startangle=100,
          labeldistance=1.18, textprops={"fontsize":SM})
    a.set_title("Chart A: Product Mix", pad=16)
    b = fig.add_subplot(gs[0, 1]); b.bar(gm.year.astype(str), gm.net_revenue/1e7, color="#4f81bd"); b.set_ylim(55, 118)
    b2 = b.twinx(); b2.plot(gm.year.astype(str), gm.gross_margin_pct, color="#c0504d", marker="s", lw=3); b2.set_ylim(20, 28.5)
    b.set_title("Chart B: Revenue & Margin")
    c = fig.add_subplot(gs[1, 0]); r = reg[reg.region != MISSING]
    c.bar(r.region, r.net_revenue/1e7, color=["#9bbb59","#4bacc6","#f79646","#8064a2"]); c.set_ylim(13, 39); c.grid(True, color="#999999", lw=0.8)
    c.set_title("Chart C: Region Performance")
    d = fig.add_subplot(gs[1, 1]); d.stackplot(range(12), (rep/1e7).T.values, colors=plt.cm.gist_rainbow(np.linspace(0,1,11)), labels=rep.columns)
    d.set_ylim(0, 34)      # room for the legend on top of the chart, as in the old pack
    d.legend(ncol=2, loc="upper left", handlelength=1.0, columnspacing=0.6, labelspacing=0.2, fontsize=SM)
    d.set_xticks(range(12)); d.set_xticklabels([m[0] for m in MON]); d.set_title("Chart D: Sales by Rep")
    e = fig.add_subplot(gs[2, :]); h = hm.loc[REGIONS]/1e7; w = 0.2
    for k, reg_ in enumerate(h.index):
        bars = e.bar(np.arange(12)+(k-1.5)*w, h.loc[reg_], width=w, label=reg_)
        for bb in bars: e.text(bb.get_x()+w/2, bb.get_height()+0.15, f"{bb.get_height():.1f}", ha="center", va="bottom", fontsize=SM, rotation=90)
    e.grid(True, color="#999999", lw=0.8); e.set_xticks(range(12)); e.set_xticklabels(MON); e.set_ylim(0, 8.5)
    e.legend(ncol=4, loc="upper left")
    e.set_title("Chart E: Monthly Region Sales")
    save(fig, "fig15-15-project-before.svg")

# project: one set of redesigns (V15.1: two per row, the heatmap full width)
def project_after():
    fig = plt.figure(figsize=(W_IN, 7.3))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.1, 1.0, 0.9], hspace=0.7, wspace=0.55)
    a = fig.add_subplot(gs[0, 0]); q = prod.sort_values("net_revenue"); a.barh(q.product_name, q.net_revenue/1e7, color=GREY, height=0.65)
    a.barh(q.product_name.iloc[-1:], q.net_revenue.iloc[-1:]/1e7, color=ACC, height=0.65)
    for i, v in enumerate(q.net_revenue/1e7): a.text(v+0.3, i, f"{v:.1f}", va="center")
    a.set_xticks([]); tidy(a, None); a.spines["bottom"].set_visible(False); a.set_xlim(0, 28)
    a.set_title("A. Storage Box 25L led 2025\n(₹ crore)")
    b = fig.add_subplot(gs[0, 1]); x = gm.year.astype(str); b.bar(x, gm.net_revenue/1e7, color=ACC, width=0.55); b.set_ylim(0, 135); tidy(b, None); b.set_yticks([])
    b.spines["left"].set_visible(False)
    for i, (v, m) in enumerate(zip(gm.net_revenue/1e7, gm.gross_margin_pct)):
        b.text(i, v+3, f"₹{v:.1f} cr", ha="center", color=INK); b.text(i, v/2, f"margin\n{m}%", ha="center", va="center", color="white")
    b.set_title("B. Revenue up 87% since 2023;\nmargin up 6.4 points")
    c = fig.add_subplot(gs[1, 0])
    known = reg[reg.region != MISSING].sort_values("net_revenue"); rr = pd.concat([reg[reg.region == MISSING], known])
    c.barh(rr.region, rr.net_revenue/1e7, color=[GREY if l == MISSING else ACC for l in rr.region], height=0.6)
    for i, v in enumerate(rr.net_revenue/1e7): c.text(v+0.4, i, f"{v:.1f}", va="center")
    c.set_xticks([]); tidy(c, None); c.spines["bottom"].set_visible(False); c.set_xlim(0, 46)
    c.set_title("C. West brings 33% of 2025\nrevenue (₹ crore)")
    d = fig.add_subplot(gs[1, 1])
    for col in rep.columns:
        if col != "Rahul Mehta": d.plot(range(12), rep[col]/1e7, lw=0.9, color=LIGHT)
    d.plot(range(12), rep["Rahul Mehta"]/1e7, lw=2.2, color=ORANGE); d.text(11.2, rep["Rahul Mehta"].iloc[-1]/1e7, "Rahul\nMehta", color=ORANGE, va="center")
    d.set_xticks(range(12)); d.set_xticklabels([m[0] for m in MON]); d.set_xlim(-0.3, 14.3); tidy(d)
    d.set_title("D. Every rep follows the same\nseason; Rahul Mehta leads (₹ crore)")
    e = fig.add_subplot(gs[2, :]); h = hm.loc[REGIONS]/1e7
    e.imshow(h.values, aspect="auto", cmap="Blues", vmin=0)
    for i in range(4):
        for j in range(12): e.text(j, i, f"{h.values[i,j]:.1f}", ha="center", va="center", color="white" if h.values[i,j] > 3.2 else INK)
    e.set_xticks(range(12)); e.set_xticklabels(MON); e.set_yticks(range(4)); e.set_yticklabels(h.index)
    e.tick_params(length=0); [sp.set_visible(False) for sp in e.spines.values()]
    e.set_title("E. October is the peak in every region (₹ crore)")
    save(fig, "fig15-16-project-after.svg")

if __name__ == "__main__":
    for f in [f1, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, project_before, project_after]: f()
    bad = 0
    for name, W, lo, lo_txt, hi in REPORT:
        flag = "OK   " if lo >= 7.0 else "SMALL"; bad += lo < 7.0
        print(f"{flag} {name:32} canvas {W:6.1f}pt  printed text {lo:5.2f}-{hi:5.2f} pt  (smallest: {lo_txt[:24]!r})")
    print(f"{bad} figure(s) with text under 7 pt")
