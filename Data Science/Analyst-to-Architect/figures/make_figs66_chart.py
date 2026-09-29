# Real data figure for Chapter 66: Figure 66.2, the ROI case. Run: python3 make_figs66_chart.py
# Reads companion/ch66/roi_case.csv, so the chart always matches the numbers the chapter's code prints.
# Drawn at 6.8 x 2.9 inches and printed at the text width (6.85 in), so 8 pt text prints at about 8 pt.
import pathlib, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = pathlib.Path(__file__).resolve().parent
roi = pd.read_csv(HERE.parent / "companion" / "ch66" / "roi_case.csv").set_index("item_id")["amount_rs"]
INK, MUTED, ACC, GREEN, GOLD, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#2f7d6d", "#b7791f", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5,
                     "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": INK,
                     "axes.edgecolor": "#c9d3df", "svg.fonttype": "path", "hatch.color": GOLD})

def lakh(v):
    return f"₹{v / 1e5:.2f} lakh"

def indian(n):                     # 100750 -> "1,00,750" (Indian digit grouping)
    s = f"{int(round(n)):d}"
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    return ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail

platform = roi["platform_cost"]
flash, macro, po = roi["flash"], roi["macro"], roi["po_intake"]
measured = flash + macro
fig, ax = plt.subplots(figsize=(6.8, 2.9))
ax.barh(1, platform, color=RED, height=0.5)
ax.text(platform / 2, 1, f"Platform, a year: {lakh(platform)}", ha="center", va="center",
        color="white", fontweight="bold")
ax.barh(0, flash, color=GREEN, height=0.5)
ax.barh(0, macro, left=flash, color=GREEN, height=0.5)
ax.barh(0, po, left=measured, color="white", edgecolor=GOLD, hatch="///", height=0.5, lw=1.2)
ax.add_patch(Rectangle((measured + po, -0.25), platform - measured - po, 0.5, fill=False,
                       ls="--", ec=MUTED, lw=1))
ax.text(flash / 2, 0, f"Flash\n₹{indian(flash)}", ha="center", va="center", color="white", fontweight="bold")
ax.text(measured + po / 2, 0, "PO intake\n(conditional)", ha="center", va="center",
        color=INK, fontweight="bold", bbox=dict(fc="white", ec="none", pad=1.5))
ax.text(measured + po + (platform - measured - po) / 2, 0, "Unmeasured ceiling:\nnamed, not priced",
        ha="center", va="center", color=MUTED)
ax.annotate(f"measured {measured / platform:.0%}\n(Flash + macro ₹{macro:.0f})", xy=(measured, -0.27),
            xytext=(measured - 4000, -0.62), ha="right", va="top", color=GREEN, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=GREEN, lw=1))
ax.annotate(f"with PO intake {(measured + po) / platform:.0%}\n(₹{indian(po)}, only if ≥97% caught)",
            xy=(measured + po, -0.27), xytext=(measured + po + 4000, -0.62), ha="left", va="top", color=GOLD, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=1))
ax.set_yticks([1, 0], ["Cost", "Savings"])
ax.set_ylim(-1.35, 1.45)
ax.set_xlim(0, platform * 1.02)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"₹{v / 1e5:.0f} lakh" if v else "0"))
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1e5))
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
ax.set_title(f"Measured savings cover {measured / platform:.0%} of the platform's cost; "
             f"PO intake could take it to {(measured + po) / platform:.0%}")
fig.savefig(HERE / "fig66-2-roi-case.svg", format="svg", bbox_inches="tight")
plt.close(fig)
print("ok")
