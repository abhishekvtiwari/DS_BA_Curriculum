# Generates the figures for Chapter 15 (SVG, via matplotlib). Run: python3 make_figs15.py
# Data: companion/ch15/chart_data/*.csv, built by companion/ch15/build_ch15_data.py from the full Riverstone dataset.
import pathlib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch15" / "chart_data"
INK="#1d2330"; MUTED="#5b6475"; ACC="#0f5c8c"; RULE="#c9d3df"; GREY="#b8c0cc"; LIGHT="#dfe5ec"
ORANGE="#c0662b"; GREEN="#2f7d6d"; RED="#b23b3b"; PURPLE="#7a4fa0"; GOLD="#b7791f"
OKABE=["#0072B2","#E69F00","#009E73","#CC79A7","#56B4E9","#D55E00","#F0E442","#000000"]
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":RULE,"axes.labelcolor":MUTED,"xtick.color":MUTED,
    "ytick.color":MUTED,"axes.titlesize":10.5,"axes.titleweight":"bold","axes.titlecolor":INK,"axes.titlelocation":"left",
    "svg.fonttype":"path","figure.dpi":100})
def tidy(ax, grid="y"):
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    if grid: ax.grid(axis=grid, color=LIGHT, lw=0.8); ax.set_axisbelow(True)
def cr(v, _=None): return f"₹{v/1e7:,.1f} cr" if abs(v) >= 1e7 else f"₹{v/1e5:,.0f} L"
def crf(v, _=None): return f"{v/1e7:,.0f}"
def save(fig, name):
    if len(fig.axes) > 1 and not fig.get_tight_layout(): fig.subplots_adjust(wspace=0.32)
    fig.savefig(name, format="svg", bbox_inches="tight"); plt.close(fig)
MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

seg = pd.read_csv(D/"segment_2025.csv"); mon = pd.read_csv(D/"monthly_2023_2025.csv"); ov = pd.read_csv(D/"order_values_2025.csv")
cu = pd.read_csv(D/"customers_2025.csv"); br = pd.read_csv(D/"bridge_2024_2025.csv"); hm = pd.read_csv(D/"region_month_2025.csv").set_index("region")
cat = pd.read_csv(D/"category_month_2025.csv").set_index("month").fillna(0); reg = pd.read_csv(D/"region_2025.csv")
prod = pd.read_csv(D/"product_2025.csv"); rep = pd.read_csv(D/"rep_month_2025.csv").set_index("month"); gm = pd.read_csv(D/"margin_by_year.csv")
ans = pd.read_csv(D/"anscombe.csv"); city = pd.read_csv(D/"city_2025.csv")

# 15-1 pie vs bar
def f1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios":[1,1.35]})
    a.pie(seg.net_revenue, labels=seg.segment, colors=[ACC, GREEN, GOLD], startangle=90, counterclock=False,
          wedgeprops={"edgecolor":"white","linewidth":2}, textprops={"color":INK})
    a.set_title("Pie: is Wholesale bigger than\nHospitality?")
    s = seg.sort_values("net_revenue")
    b.barh(s.segment, s.net_revenue/1e7, color=[GOLD, GREEN, ACC], height=0.6)
    for y, v, p in zip(range(3), s.net_revenue/1e7, s.share_pct): b.text(v+1, y, f"₹{v:,.1f} cr ({p}%)", va="center", color=INK, fontsize=9.5)
    b.set_xlim(0, 72); b.set_xlabel("Net revenue, 2025 (₹ crore)"); tidy(b, "x"); b.set_title("Bar: the same data, compared by length")
    save(fig, "fig15-1-pie-vs-bar.svg")

# 15-3 bars: unsorted vertical vs sorted horizontal
def f3():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.9))
    p = prod.sort_values("product_name")
    a.bar(p.product_name, p.net_revenue/1e7, color=OKABE[:8]); a.set_xticks(range(8)); a.set_xticklabels(p.product_name, rotation=45, ha="right", fontsize=8.5)
    a.set_title("Before: alphabetical, rotated labels, rainbow"); tidy(a); a.set_ylabel("₹ crore")
    q = prod.sort_values("net_revenue")
    b.barh(q.product_name, q.net_revenue/1e7, color=GREY, height=0.65)
    top = q.net_revenue.idxmax()
    for i, (n, v) in enumerate(zip(q.product_name, q.net_revenue/1e7)):
        b.text(v+0.4, i, f"{v:,.1f}", va="center", fontsize=9, color=INK)
    b.set_title("After: sorted, horizontal, labeled, one color"); tidy(b, None); b.set_xticks([]); b.spines["bottom"].set_visible(False)
    b.set_xlabel("Net revenue, 2025 (₹ crore)")
    save(fig, "fig15-3-sorted-bars.svg")

# 15-4 lines
def f4():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.8))
    x = np.arange(36)
    a.plot(x, mon.net_revenue/1e7, color=ACC, lw=2)
    a.set_xticks([0,12,24]); a.set_xticklabels(["Jan 2023","Jan 2024","Jan 2025"]); tidy(a); a.set_ylim(0, 20); a.set_ylabel("₹ crore")
    a.set_title("One line, 36 months: growth plus a yearly cycle")
    i = mon.net_revenue.idxmax(); a.annotate("Oct 2025: ₹18.1 cr", (i, mon.net_revenue[i]/1e7), xytext=(15, 18.5), fontsize=9, color=INK,
                                             arrowprops={"arrowstyle":"-","color":MUTED})
    for y, c, lw in [(2023, GREY, 1.6), (2024, "#7fa7c4", 1.8), (2025, ACC, 2.6)]:
        d = mon[mon.year == y]; b.plot(range(12), d.net_revenue/1e7, color=c, lw=lw)
        b.text(11.2, d.net_revenue.iloc[-1]/1e7, str(y), color=c, va="center", fontsize=9.5, fontweight="bold")
    b.set_xticks(range(12)); b.set_xticklabels(MON, fontsize=8.5); b.set_xlim(-0.3, 12.2); b.set_ylim(0, 20); tidy(b)
    b.set_title("One line per year: October peaks")
    save(fig, "fig15-4-lines.svg")

# 15-5 histograms with three bin widths
def f5():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.2), sharey=False)
    for ax, w, t in zip(axs, [1000, 5000, 25000], ["₹1,000 bins: noisy", "₹5,000 bins: the shape", "₹25,000 bins: too coarse"]):
        bins = np.arange(0, 150001, w); ax.hist(ov.order_value, bins=bins, color=ACC, edgecolor="white", lw=0.3 if w==1000 else 0.8)
        ax.set_title(t); tidy(ax); ax.set_xlim(0, 150000); ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
        ax.set_xlabel("Order value (₹)")
    axs[0].set_ylabel("Orders, 2025")
    save(fig, "fig15-5-histogram-bins.svg")

# 15-6 box plots by segment
def f6():
    fig, ax = plt.subplots(figsize=(9, 3.4))
    order = ["Hospitality", "Retail", "Wholesale"]
    data = [ov[ov.segment == s].order_value/1000 for s in order]
    bp = ax.boxplot(data, vert=False, widths=0.5, patch_artist=True, flierprops={"marker":"o","markersize":2.5,"markerfacecolor":GREY,"markeredgecolor":"none","alpha":0.6},
                    medianprops={"color":ORANGE,"lw":2.2}, boxprops={"facecolor":"#e3edf5","edgecolor":ACC}, whiskerprops={"color":ACC}, capprops={"color":ACC})
    ax.set_yticks([1,2,3]); ax.set_yticklabels(order)
    for i, s in enumerate(order, 1):
        med = ov[ov.segment == s].order_value.median(); ax.text(med/1000, i+0.36, f"median ₹{med:,.0f}", ha="center", fontsize=8.8, color=ORANGE)
    ax.set_xlabel("Order value, 2025 (₹ thousand)"); tidy(ax, "x"); ax.set_xlim(0, 150)
    ax.set_title("Wholesale orders are larger and more spread out; dots are orders beyond the whiskers")
    save(fig, "fig15-6-box-plots.svg")

# 15-7 scatter
def f7():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    a.scatter(cu.orders, cu.net_revenue/1e5, s=12, color=ACC); a.set_title("Before: 4,599 dots on top of each other"); tidy(a, "both")
    a.set_xlabel("Orders in 2025"); a.set_ylabel("Net revenue, 2025 (₹ lakh)")
    rng = np.random.default_rng(15)
    for s, c in [("Retail", ACC), ("Hospitality", GOLD), ("Wholesale", GREEN)]:
        d = cu[cu.segment == s]; b.scatter(d.orders + rng.uniform(-0.3, 0.3, len(d)), d.net_revenue/1e5, s=7, alpha=0.35, color=c, label=s, edgecolors="none")
    b.legend(frameon=False, markerscale=2.5, loc="upper left"); tidy(b, "both"); b.set_xlabel("Orders in 2025 (jittered)")
    b.set_title("After: transparency, jitter, and color by segment")
    save(fig, "fig15-8-scatter.svg")

# 15-8 composition: stacked vs 100% and waterfall
def f8():
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 3.9))
    cols = ["Storage", "Kitchen", "Industrial", "Furniture"]; colors = [ACC, "#6c9bc0", GREEN, GOLD]
    bottom = np.zeros(12)
    for c, col in zip(cols, colors):
        a.bar(range(12), cat[c]/1e7, bottom=bottom, color=col, label=c, width=0.75); bottom += cat[c].values/1e7
    a.set_xticks(range(12)); a.set_xticklabels([m[0] for m in MON]); tidy(a); a.legend(frameon=False, fontsize=8.5, ncol=4, loc="upper left")
    a.set_ylabel("₹ crore"); a.set_ylim(0, 23); a.set_title("Stacked: totals clear, middles hard")
    b2024 = br[["segment","2024"]]; start = br["2024"].sum()/1e7; end = br["2025"].sum()/1e7
    steps = [("2024", start, None)] + [(s, ch/1e7, None) for s, ch in br.sort_values("change", ascending=False)[["segment","change"]].itertuples(index=False)] + [("2025", end, None)]
    run = 0
    for i, (lab, v, _) in enumerate(steps):
        if i == 0 or i == len(steps)-1:
            b.bar(i, v, color=ACC, width=0.6); b.text(i, v+1.5, f"{v:,.1f}", ha="center", fontsize=9, color=INK); run = v
        else:
            b.bar(i, v, bottom=run, color=GREEN, width=0.6); b.text(i, run+v+1.5, f"+{v:,.1f}", ha="center", fontsize=9, color=GREEN)
            b.plot([i-0.7, i-0.3], [run, run], color=MUTED, lw=0.8); run += v
    b.plot([len(steps)-1.7, len(steps)-1.3], [run, run], color=MUTED, lw=0.8)
    b.set_xticks(range(len(steps))); b.set_xticklabels([s[0] for s in steps], fontsize=8.5); tidy(b); b.set_ylim(0, 128); b.set_ylabel("₹ crore")
    b.set_title("Waterfall: where growth came from")
    save(fig, "fig15-9-composition.svg")

# 15-9 heatmaps
def f9():
    fig, (a, b) = plt.subplots(2, 1, figsize=(10, 5.4), gridspec_kw={"height_ratios":[5,3.2]})
    h = hm.loc[["West","South","North","East","Unknown"]]/1e7
    im = a.imshow(h.values, aspect="auto", cmap="Blues", vmin=0)
    for i in range(h.shape[0]):
        for j in range(12):
            v = h.values[i, j]; a.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=8.5, color="white" if v > 3.2 else INK)
    a.set_xticks(range(12)); a.set_xticklabels(MON); a.set_yticks(range(5)); a.set_yticklabels(h.index)
    a.set_title("Sequential: revenue by region and month, 2025 (₹ crore); darker = more"); a.tick_params(length=0)
    for s in a.spines.values(): s.set_visible(False)
    att = mon.pivot(index="year", columns="month", values="attainment_pct")
    im2 = b.imshow(att.values, aspect="auto", cmap="RdBu", vmin=85, vmax=115)
    for i in range(3):
        for j in range(12):
            v = att.values[i, j]; b.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8.5, color="white" if abs(v-100) > 9 else INK)
    b.set_xticks(range(12)); b.set_xticklabels(MON); b.set_yticks(range(3)); b.set_yticklabels(att.index); b.tick_params(length=0)
    for s in b.spines.values(): s.set_visible(False)
    b.set_title("Diverging: % of target, centered on 100 (red below, blue above)")
    fig.tight_layout(); save(fig, "fig15-10-heatmaps.svg")

# 15-10 highlight one line
def f10():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for i, c in enumerate(rep.columns): a.plot(range(12), rep[c]/1e7, lw=1.5, color=plt.cm.tab20(i), label=c)
    a.legend(fontsize=6.8, ncol=2, frameon=False, loc="upper left"); a.set_title("Before: 11 colors, one legend to decode"); tidy(a)
    a.set_xticks(range(12)); a.set_xticklabels([m[0] for m in MON]); a.set_ylabel("₹ crore")
    for c in rep.columns:
        if c != "Rahul Mehta": b.plot(range(12), rep[c]/1e7, lw=1.1, color=LIGHT)
    b.plot(range(12), rep["Rahul Mehta"]/1e7, lw=2.6, color=ORANGE)
    b.text(11.2, rep["Rahul Mehta"].iloc[-1]/1e7, "Rahul Mehta", color=ORANGE, va="center", fontsize=9.5, fontweight="bold")
    b.text(11.2, rep.drop(columns="Rahul Mehta").iloc[-1].median()/1e7, "10 other reps", color=MUTED, va="center", fontsize=9)
    b.set_xticks(range(12)); b.set_xticklabels([m[0] for m in MON]); b.set_xlim(-0.3, 13.8); tidy(b)
    b.set_title("After: gray for context, one color for the story")
    save(fig, "fig15-11-highlight.svg")

# 15-11 title that states the finding
def f11():
    fig, (a, b) = plt.subplots(2, 1, figsize=(9.5, 6.6))
    d = mon[mon.year == 2025]
    for ax in (a, b):
        ax.plot(range(12), d.net_revenue/1e7, color=ACC, lw=2.4, marker="o", ms=4)
        ax.plot(range(12), d.target_revenue/1e7, color=MUTED, lw=1.4, ls="--")
        ax.set_xticks(range(12)); ax.set_xticklabels(MON); ax.set_ylim(0, 22); tidy(ax)
    a.set_title("Monthly Revenue vs Target 2025"); a.legend(["Actual", "Target"], frameon=False, loc="upper left"); a.set_ylabel("Revenue")
    b.set_title("2025 finished at 98.3% of target: a strong January–February, then a Q4 short of an ambitious plan")
    b.text(11.15, d.net_revenue.iloc[-1]/1e7-0.9, "Actual", color=ACC, fontsize=9.5, fontweight="bold")
    b.text(11.15, d.target_revenue.iloc[-1]/1e7+0.6, "Target", color=MUTED, fontsize=9.5)
    b.annotate("October: ₹18.1 cr, a record month,\nbut 92% of its ₹19.6 cr target", (9, 18.06), xytext=(3.6, 18.2), fontsize=9, color=INK,
               arrowprops={"arrowstyle":"-","color":MUTED})
    b.set_ylabel("Net revenue (₹ crore)"); b.set_xlim(-0.3, 12.3)
    fig.tight_layout(h_pad=2.5); save(fig, "fig15-12-titles.svg")

# 15-12 misleading: truncated axis and dual axis
def f12():
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(12, 3.6))
    names = ["Delhi", "Bengaluru"]; vals = [101831086, 101788506]
    a.bar(names, np.array(vals)/1e7, color=[ORANGE, ACC], width=0.55); a.set_ylim(10.175, 10.1835); tidy(a)
    a.set_title("Truncated axis: looks like a big gap"); a.yaxis.set_major_formatter(lambda v, _: f"{v:.3f}"); a.set_ylabel("₹ crore")
    b.bar(names, np.array(vals)/1e7, color=[ORANGE, ACC], width=0.55); b.set_ylim(0, 11); tidy(b)
    b.set_title("Zero baseline: the gap is 0.04%"); b.set_ylabel("₹ crore")
    x = gm.year.astype(str)
    c.bar(x, gm.net_revenue/1e7, color=LIGHT, width=0.55); c.set_ylim(55, 118); c.set_ylabel("Revenue (₹ crore)"); tidy(c)
    c2 = c.twinx(); c2.plot(x, gm.gross_margin_pct, color=RED, marker="o", lw=2.2); c2.set_ylim(20, 28.5); c2.set_ylabel("Gross margin %", color=RED)
    c2.spines["top"].set_visible(False); c.set_title("Dual axis: two scales chosen to agree")
    fig.tight_layout(); save(fig, "fig15-13-misleading.svg")

# 15-13 showing missing data
def f13():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    r = reg[reg.region != "Unknown"]
    a.barh(r.region[::-1], r.net_revenue[::-1]/1e7, color=ACC, height=0.6); tidy(a, "x"); a.set_title("Before: the Unknown region silently dropped")
    a.set_xlabel("₹ crore, 2025"); a.set_xlim(0, 42)
    rr = reg.copy(); rr["label"] = rr.region.replace({"Unknown": "City missing"})
    known = rr[rr.region != "Unknown"].sort_values("net_revenue")
    rr = pd.concat([rr[rr.region == "Unknown"], known])      # barh draws bottom-up: City missing at the bottom
    b.barh(rr.label, rr.net_revenue/1e7, color=[GREY if l == "City missing" else ACC for l in rr.label], height=0.6, hatch=None)
    for i, v in enumerate(rr.net_revenue/1e7): b.text(v+0.5, i, f"{v:,.1f}", va="center", fontsize=9)
    tidy(b, None); b.set_xticks([]); b.spines["bottom"].set_visible(False); b.set_xlim(0, 42)
    b.set_title("After: ₹2.3 cr with no city shown, in gray, at the bottom")
    save(fig, "fig15-14-missing-data.svg")

# 15-14 Anscombe
def f14():
    fig, axs = plt.subplots(1, 4, figsize=(12, 3.0), sharey=True)
    sets = [(ans.x_1_2_3, ans.y1), (ans.x_1_2_3, ans.y2), (ans.x_1_2_3, ans.y3), (ans.x4, ans.y4)]
    for k, (ax, (x, y)) in enumerate(zip(axs, sets), 1):
        ax.scatter(x, y, color=ACC, s=22); m, c0 = np.polyfit(x, y, 1); xs = np.array([3, 20]); ax.plot(xs, m*xs+c0, color=ORANGE, lw=1.3)
        ax.set_title(f"Dataset {k}"); ax.set_xlim(2, 20); ax.set_ylim(2, 14); tidy(ax, "both")
    fig.suptitle("Same means, variances, correlation (0.82), and trend line; four different stories", x=0.07, ha="left", fontsize=11.5, fontweight="bold", color=INK, y=1.05)
    save(fig, "fig15-7-anscombe.svg")

# project: five "before" charts from the old management pack
def project_before():
    fig, axs = plt.subplots(2, 3, figsize=(13, 7.6))
    a = axs[0,0]; p = prod
    a.pie(p.net_revenue, labels=p.product_name, colors=plt.cm.rainbow(np.linspace(0,1,8)), explode=[0.08]*8, shadow=True, startangle=20, textprops={"fontsize":7.5})
    a.set_title("Chart A: Product Mix", fontsize=10.5)
    b = axs[0,1]; b.bar(gm.year.astype(str), gm.net_revenue/1e7, color="#4f81bd"); b.set_ylim(55, 118)
    b2 = b.twinx(); b2.plot(gm.year.astype(str), gm.gross_margin_pct, color="#c0504d", marker="s", lw=3); b2.set_ylim(20, 28.5)
    b.set_title("Chart B: Revenue & Margin", fontsize=10.5)
    c = axs[0,2]; r = reg[reg.region != "Unknown"]
    c.bar(r.region, r.net_revenue/1e7, color=["#9bbb59","#4bacc6","#f79646","#8064a2"]); c.set_ylim(13, 39); c.grid(True, color="#999999", lw=0.8)
    c.set_title("Chart C: Region Performance", fontsize=10.5)
    d = axs[1,0]; d.stackplot(range(12), (rep/1e7).T.values, colors=plt.cm.gist_rainbow(np.linspace(0,1,11)), labels=rep.columns)
    d.legend(fontsize=5.5, ncol=2, loc="upper left"); d.set_xticks(range(12)); d.set_xticklabels(MON, fontsize=7); d.set_title("Chart D: Sales by Rep", fontsize=10.5)
    e = axs[1,1]; h = hm.loc[["West","South","North","East"]]/1e7; w = 0.2
    for k, reg_ in enumerate(h.index):
        bars = e.bar(np.arange(12)+(k-1.5)*w, h.loc[reg_], width=w, label=reg_)
        for bb in bars: e.text(bb.get_x()+w/2, bb.get_height()+0.1, f"{bb.get_height():.1f}", ha="center", fontsize=4.2, rotation=90)
    e.grid(True, color="#999999", lw=0.8); e.set_xticks(range(12)); e.set_xticklabels(MON, fontsize=7); e.legend(fontsize=6, ncol=4)
    e.set_title("Chart E: Monthly Region Sales", fontsize=10.5)
    axs[1,2].axis("off")
    fig.tight_layout(); save(fig, "fig15-15-project-before.svg")

def project_after():
    fig, axs = plt.subplots(2, 3, figsize=(13, 7.4))
    a = axs[0,0]; q = prod.sort_values("net_revenue"); a.barh(q.product_name, q.net_revenue/1e7, color=GREY, height=0.65)
    a.barh(q.product_name.iloc[-1:], q.net_revenue.iloc[-1:]/1e7, color=ACC, height=0.65)
    for i, v in enumerate(q.net_revenue/1e7): a.text(v+0.3, i, f"{v:.1f}", va="center", fontsize=8)
    a.set_xticks([]); tidy(a, None); a.spines["bottom"].set_visible(False); a.tick_params(axis="y", labelsize=8)
    a.set_title("A. Storage Box 25L led 2025 (₹ crore)", fontsize=10)
    b = axs[0,1]; x = gm.year.astype(str); b.bar(x, gm.net_revenue/1e7, color=ACC, width=0.55); b.set_ylim(0, 135); tidy(b, None); b.set_yticks([])
    b.spines["left"].set_visible(False)
    for i, (v, m) in enumerate(zip(gm.net_revenue/1e7, gm.gross_margin_pct)):
        b.text(i, v+3, f"₹{v:.1f} cr", ha="center", fontsize=8.5, color=INK); b.text(i, v/2, f"margin\n{m}%", ha="center", va="center", fontsize=8.5, color="white")
    b.set_title("B. Revenue up 87% since 2023;\nmargin up 6.4 points", fontsize=10)
    c = axs[0,2]; rr = reg.copy(); rr["label"] = rr.region.replace({"Unknown": "City missing"})
    known = rr[rr.region != "Unknown"].sort_values("net_revenue"); rr = pd.concat([rr[rr.region == "Unknown"], known])
    c.barh(rr.label, rr.net_revenue/1e7, color=[GREY if l == "City missing" else ACC for l in rr.label], height=0.6)
    for i, v in enumerate(rr.net_revenue/1e7): c.text(v+0.4, i, f"{v:.1f}", va="center", fontsize=8.5)
    c.set_xticks([]); tidy(c, None); c.spines["bottom"].set_visible(False); c.set_xlim(0, 44)
    c.set_title("C. West brings 33% of 2025 revenue (₹ crore)", fontsize=10)
    d = axs[1,0]
    for col in rep.columns:
        if col != "Rahul Mehta": d.plot(range(12), rep[col]/1e7, lw=1, color=LIGHT)
    d.plot(range(12), rep["Rahul Mehta"]/1e7, lw=2.4, color=ORANGE); d.text(11.2, rep["Rahul Mehta"].iloc[-1]/1e7, "Rahul\nMehta", color=ORANGE, fontsize=8, va="center")
    d.set_xticks(range(12)); d.set_xticklabels([m[0] for m in MON], fontsize=8); d.set_xlim(-0.3, 13); tidy(d)
    d.set_title("D. Every rep follows the same season;\nRahul Mehta leads (₹ crore)", fontsize=10)
    e = axs[1,1]; h = hm.loc[["West","South","North","East"]]/1e7
    e.imshow(h.values, aspect="auto", cmap="Blues", vmin=0)
    for i in range(4):
        for j in range(12): e.text(j, i, f"{h.values[i,j]:.1f}", ha="center", va="center", fontsize=6.8, color="white" if h.values[i,j] > 3.2 else INK)
    e.set_xticks(range(12)); e.set_xticklabels([m[0] for m in MON], fontsize=8); e.set_yticks(range(4)); e.set_yticklabels(h.index, fontsize=8)
    e.tick_params(length=0); [sp.set_visible(False) for sp in e.spines.values()]
    e.set_title("E. October is the peak in every region\n(₹ crore)", fontsize=10)
    axs[1,2].axis("off")
    fig.tight_layout(); save(fig, "fig15-16-project-after.svg")

if __name__ == "__main__":
    for f in [f1, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, project_before, project_after]: f()
    print("ok")
