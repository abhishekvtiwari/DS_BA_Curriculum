# Real data figure for Chapter 64 (fairness audit). Run: python3 make_figs64_chart.py
import pathlib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch64"
INK, MUTED, ACC, ORANGE, GREEN, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color=LIGHT, lw=0.8); ax.set_axisbelow(True)

df = pd.read_csv(D / "leads_scored_2025.csv")
order = ["West", "South", "North", "East"]

fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.6))
overall = df.groupby("region")["lead_score"].mean().reindex(order)
colors = [ACC, ACC, ACC, RED]
a.bar(overall.index, overall.values, color=colors)
for i, v in enumerate(overall.values):
    a.text(i, v + 1.5, f"{v:.1f}", ha="center", fontweight="bold", color=INK, fontsize=9.5)
a.set_ylim(0, 72); a.set_ylabel("mean lead score"); tidy(a)
a.set_title("Overall: East scores 13 points below West")

sub = df[df.company_size_band == 2]
cond = sub.groupby("region")["lead_score"].mean().reindex(order)
b.bar(cond.index, cond.values, color=[ACC, ACC, ACC, GREEN])
for i, v in enumerate(cond.values):
    b.text(i, v + 1.5, f"{v:.1f}", ha="center", fontweight="bold", color=INK, fontsize=9.5)
b.set_ylim(0, 72); tidy(b)
b.set_title("Same company size (band 2): the gap nearly vanishes")

fig.subplots_adjust(wspace=0.2)
fig.savefig("fig64-3-fairness-audit.svg", format="svg", bbox_inches="tight")
plt.close(fig)
print("ok")
