# Real data figures for Chapter 65 (65.1 cost breakdown, 65.2 NFR check). Run: python3 make_figs65_charts.py
# Reads companion/ch65/monthly_cost_model.csv; prints at 174 mm (493.2 pt), so every font below is >= 8 pt at print.
import pathlib, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch65"
INK, MUTED, ACC, RED, GREEN, LIGHT, PALE = "#1d2330", "#5b6475", "#0f5c8c", "#b23b3b", "#2f7d6d", "#dfe5ec", "#8fb3cc"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax, axis):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis=axis, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

df = pd.read_csv(D / "monthly_cost_model.csv").sort_values("monthly_inr", ascending=True)
total = df.monthly_inr.sum()
warehouse = df.component.str.startswith("Warehouse compute") | df.component.str.startswith("Warehouse storage")

# Figure 65.1: one series, the warehouse's two lines darker and named in a note (not colour alone)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
bars = ax.barh(df.component, df.monthly_inr, color=[ACC if w else PALE for w in warehouse], height=0.62)
for bar, v in zip(bars, df.monthly_inr):
    ax.text(v + 250, bar.get_y() + bar.get_height() / 2, f"₹{v:,.0f}" if v else "₹0 (free)",
            va="center", fontsize=8.5, fontweight="bold", color=INK)
ax.set_xlabel("₹ a month, at ₹87 to the dollar"); tidy(ax, "x")
ax.set_xlim(0, df.monthly_inr.max() * 1.22)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
share = df.loc[warehouse, "monthly_inr"].sum() / total
llm = df.loc[df.component.str.contains("LLM"), "monthly_inr"].sum() / total
ax.text(df.monthly_inr.max() * 1.21, 3.2, f"Dark bars, the warehouse:\n{share:.1%} of the bill\n\nBoth LLM APIs: {llm:.1%}",
        ha="right", va="center", fontsize=8.5, color=INK)
ax.set_title(f"Riverstone's infrastructure bill: ₹{total:,.0f} a month, and where it goes")
fig.savefig("fig65-1-cost-breakdown.svg", format="svg", bbox_inches="tight")
plt.close(fig)

# Figure 65.2: dots on a log scale (a bar's height from an arbitrary floor means nothing on a log axis)
lines = 87_011 / 12
per1000 = total / (lines / 1000)
marginal = 1120 / lines * 1000 * df.set_index("component").loc["PO-intake (LLM API)", "monthly_inr"] / 1120
pts = [("Chapter 60's NFR\n(never costed)", 0.50, RED),
       ("Marginal cost\n(this chapter)", marginal, GREEN),
       ("Fully-loaded cost\n(this chapter)", per1000, ACC)]
fig2, ax2 = plt.subplots(figsize=(6.4, 2.3))
for i, (label, v, c) in enumerate(pts):
    ax2.hlines(i, 0.1, v, color=LIGHT, lw=2)
    ax2.plot(v, i, "o", ms=9, color=c)
    ax2.text(v * 1.6, i, f"₹{v:,.2f}", va="center", fontsize=9, fontweight="bold", color=INK)
ax2.set_yticks(range(3)); ax2.set_yticklabels([p[0] for p in pts])
ax2.set_xscale("log"); ax2.set_xlim(0.1, 1e5); ax2.set_ylim(-0.6, 2.6)
ax2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"₹{x:,.10g}"))
ax2.set_xlabel("₹ per 1,000 order lines (log scale: each step is 10 times the last)")
tidy(ax2, "x")
ax2.set_title(f"An NFR set without a cost model was off by about 10,000 times ({per1000 / 0.5:,.0f}×)")
fig2.savefig("fig65-2-nfr-reality-check.svg", format="svg", bbox_inches="tight")
plt.close(fig2)
print("ok")
