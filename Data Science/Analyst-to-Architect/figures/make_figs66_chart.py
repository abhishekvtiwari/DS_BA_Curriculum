# Real data figure for Chapter 66 (ROI case). Run: python3 make_figs66_chart.py
import pathlib, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch66"
INK, MUTED, ACC, ORANGE, GREEN, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax, axis="y"):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis=axis, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

fig, ax = plt.subplots(figsize=(8.5, 3.8))
items = ["Platform\nannual cost", "Daily Flash\n(Ch 20)", "Branch macro\n(Ch 19)", "PO-intake\n(Ch 58)", "Three known\nautomations, total"]
vals = [456168, 97500, 5775, 100500, 203775]
colors = [RED, GREEN, GREEN, GREEN, ACC]
bars = ax.bar(items, vals, color=colors)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x()+bar.get_width()/2, v+8000, f"Rs {v:,.0f}", ha="center", fontweight="bold", fontsize=9, color=INK)
tidy(ax)
ax.set_ylabel("Rupees per year")
ax.set_title("Three real, quantified automations cover 45% of the platform's cost — not 100%")
ax.set_ylim(0, 500000)
fig.savefig("fig66-4-roi-case.svg", format="svg", bbox_inches="tight")
plt.close(fig)
print("ok")
