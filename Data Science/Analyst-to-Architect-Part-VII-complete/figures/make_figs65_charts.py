# Real data figures for Chapter 65. Run: python3 make_figs65_charts.py
import pathlib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch65"
INK, MUTED, ACC, ORANGE, GREEN, RED, PURPLE, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#b23b3b", "#7a4fa0", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax, axis="y"):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis=axis, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

df = pd.read_csv(D / "monthly_cost_model.csv")
df = df.sort_values("monthly_inr", ascending=True)
short = {"RDS PostgreSQL (db.m5.large, Single-AZ)": "Warehouse compute (RDS)",
        "RDS storage (gp3)": "Warehouse storage",
        "RDS automated backups": "Backups (free tier)",
        "S3 Standard (sensor archive, hot)": "Sensor archive (hot, 90d)",
        "S3 Glacier Deep Archive (sensor archive, cold)": "Sensor archive (cold)",
        "Data transfer out (dashboards, API, email)": "Data transfer out",
        "Dagster orchestration compute (small EC2 fleet)": "Orchestration compute",
        "Defect-model serving (FastAPI, small EC2)": "Defect-model serving",
        "PO-intake extraction (mid-tier model, e.g. Sonnet-5-class)": "PO-intake (LLM API)",
        "Support RAG assistant (small/flash-tier model)": "RAG assistant (LLM API)"}
df["label"] = df.component.map(short)

fig, ax = plt.subplots(figsize=(9.5, 4.2))
colors = [ACC if "Warehouse" in l else (PURPLE if "LLM" in l or "RAG" in l or "PO-intake" in l else GREEN) for l in df.label]
bars = ax.barh(df.label, df.monthly_inr, color=colors)
for bar, v in zip(bars, df.monthly_inr):
    ax.text(v + 250, bar.get_y() + bar.get_height()/2, f"Rs {v:,.0f}", va="center", fontsize=9, fontweight="bold", color=INK)
ax.set_xlabel("Monthly cost (Rs)"); tidy(ax, "x")
total = df.monthly_inr.sum()
ax.set_title(f"Riverstone's platform: Rs {total:,.0f}/month, and where it actually goes")
ax.set_xlim(0, df.monthly_inr.max()*1.25)
fig.savefig("fig65-1-cost-breakdown.svg", format="svg", bbox_inches="tight")
plt.close(fig)

# NFR reality check
fig2, ax2 = plt.subplots(figsize=(7, 3.6))
vals = [0.50, 2182.58]
labels = ["Ch 60's original NFR\n(never costed)", "What it actually costs\n(this chapter's bottom-up model)"]
bars2 = ax2.bar(labels, vals, color=[RED, ACC], width=0.5)
ax2.set_yscale("log")
for bar, v in zip(bars2, vals):
    ax2.text(bar.get_x()+bar.get_width()/2, v*1.3, f"Rs {v:,.2f}", ha="center", fontweight="bold", color=INK, fontsize=10)
ax2.set_ylabel("Rs per 1,000 order lines (log scale)")
tidy(ax2)
ax2.set_title("An NFR set without a cost model was off by about 4,400x")
fig2.savefig("fig65-2-nfr-reality-check.svg", format="svg", bbox_inches="tight")
plt.close(fig2)
print("ok")
