# Real data figure for Chapter 64 (fairness audit). Run: python3 make_figs64_chart.py
# Reads companion/ch64/leads_scored_2025.csv (made by build_ch64_files.py). The figure is drawn at
# 6.85 in wide, the printed text width (174 mm), so its font sizes print as set: 8 pt and up.
# East is the same colour in both panels, and every bar carries its value, so nothing relies on colour.
import pathlib, matplotlib
import pandas as pd
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch64"
OUT = pathlib.Path(__file__).resolve().parent / "fig64-3-fairness-audit.svg"
INK, MUTED, ACC, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})

def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color=LIGHT, lw=0.8); ax.set_axisbelow(True)

df = pd.read_csv(D / "leads_scored_2025.csv")
order = ["West", "South", "North", "East"]
colors = [ACC, ACC, ACC, RED]
overall = df.groupby("region")["lead_score"].mean().reindex(order)
same = df[df.company_size_band == 2].groupby("region")["lead_score"].mean().reindex(order)
gap = overall["West"] - overall["East"]

fig, (a, b) = plt.subplots(1, 2, figsize=(6.85, 2.7), sharey=True)
for ax, vals in ((a, overall), (b, same)):
    ax.bar(vals.index, vals.values, color=colors, width=0.62)
    for i, v in enumerate(vals.values):
        ax.text(i, v + 0.8, f"{v:.1f}", ha="center", fontweight="bold", color=INK, fontsize=8)
    ax.set_ylim(0, 35); tidy(ax)
a.set_ylabel("mean lead score (same scale in both)")
a.set_title(f"All leads:\nEast scores {gap:.0f} points below West")
b.set_title("Same size only (11–50 employees, band 2):\nno gap")
b.tick_params(labelleft=True)
fig.subplots_adjust(wspace=0.22)
fig.savefig(OUT, format="svg", bbox_inches="tight")
plt.close(fig)
print("ok")
