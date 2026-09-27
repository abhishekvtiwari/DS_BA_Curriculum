# Figures for Chapter 21. Run: python3 make_figs21.py  (reads companion/ch21 + companion/full)
import pathlib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
D = pathlib.Path(__file__).resolve().parent.parent / "companion"
INK, MUTED, ACC, ORANGE, GREEN, PURPLE, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#7a4fa0", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
d = pd.read_csv(D / "ch21" / "delivery_times_2025.csv")

def f1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.4))
    v = d.order_value / 1000
    a.hist(v, bins=np.arange(0, 150, 2.5), color=ACC, edgecolor="white", lw=0.4)
    for value, color, label, frac in [(v.mean(), ORANGE, f"mean ₹{d.order_value.mean():,.0f}", 0.92),
                                      (v.median(), GREEN, f"median ₹{d.order_value.median():,.0f}", 0.74)]:
        a.axvline(value, color=color, lw=2.2)
        a.text(value + 3, a.get_ylim()[1]*frac, label, color=color, fontsize=9.5, fontweight="bold")
    a.set_xlim(0, 150); a.set_xlabel("Order value (₹ thousand)"); a.set_ylabel("Orders"); tidy(a)
    a.set_title("Order values: the mean sits above the median")
    t = d.delivery_days
    b.hist(t, bins=np.arange(0, 20, 0.5), color=ACC, edgecolor="white", lw=0.4)
    for value, color, label, frac in [(t.mean(), ORANGE, f"mean {t.mean():.2f} days", 0.92), (t.median(), GREEN, f"median {t.median():.1f} days", 0.74)]:
        b.axvline(value, color=color, lw=2.2)
        b.text(value + 0.4, b.get_ylim()[1]*frac, label, color=color, fontsize=9.5, fontweight="bold")
    b.set_xlim(0, 20); b.set_xlabel("Delivery time (days)"); tidy(b)
    b.set_title("Delivery times: a long right tail pulls the mean")
    fig.subplots_adjust(wspace=0.25); fig.savefig("fig21-1-mean-vs-median.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f2():
    fig, ax = plt.subplots(figsize=(10, 3.4))
    order = ["Mumbai HO", "Bengaluru", "Delhi", "Kolkata"]
    data = [d[d.branch == b].delivery_days for b in order]
    bp = ax.boxplot(data, vert=False, widths=0.55, patch_artist=True,
                    flierprops={"marker": "o", "markersize": 2, "markerfacecolor": "#b8c0cc", "markeredgecolor": "none", "alpha": 0.4},
                    medianprops={"color": ORANGE, "lw": 2.2}, boxprops={"facecolor": "#e3edf5", "edgecolor": ACC},
                    whiskerprops={"color": ACC}, capprops={"color": ACC})
    for i, b in enumerate(order, 1):
        s = d[d.branch == b].delivery_days
        q1, q3 = s.quantile(.25), s.quantile(.75)
        ax.text(s.median(), i + 0.34, f"median {s.median():.1f}", color=ORANGE, fontsize=8.6, ha="center")
        ax.text(19.6, i, f"IQR {q3-q1:.1f} d  ·  p95 {s.quantile(.95):.1f} d", va="center", fontsize=8.6, color=MUTED)
        ax.plot([d[d.branch==b].promised_days.iloc[0]]*2, [i-0.32, i+0.32], color=PURPLE, lw=1.8, ls="--")
    ax.set_yticks(range(1, 5)); ax.set_yticklabels(order); ax.set_xlim(0, 26); ax.set_xlabel("Delivery time (days)")
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="x", color=LIGHT, lw=0.8); ax.set_axisbelow(True)
    ax.set_title("Delivery time by branch: the box is the middle half, the dashed line is the promise")
    fig.savefig("fig21-2-spread-by-branch.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f3():
    fig, axs = plt.subplots(1, 4, figsize=(12.5, 2.9))
    x = np.linspace(-4, 4, 400)
    axs[0].plot(x*2.28 + 4.37, stats.norm.pdf(x)/2.28, color=ACC, lw=2.2); axs[0].fill_between(x*2.28+4.37, stats.norm.pdf(x)/2.28, color=ACC, alpha=0.1)
    axs[0].set_title("Normal\nheights, measurement error"); axs[0].set_xlabel("value"); axs[0].set_yticks([])
    k = np.arange(0, 16)
    axs[1].bar(k, stats.binom.pmf(k, 40, 0.18), color=GREEN)
    axs[1].set_title("Binomial\n40 deliveries, 18% late"); axs[1].set_xlabel("late deliveries"); axs[1].set_yticks([])
    k2 = np.arange(0, 20)
    axs[2].bar(k2, stats.poisson.pmf(k2, 9.4), color=PURPLE)
    axs[2].set_title("Poisson\ncomplaints per week"); axs[2].set_xlabel("count"); axs[2].set_yticks([])
    axs[3].bar([1, 2, 3, 4, 5, 6], [1/6]*6, color=ORANGE)
    axs[3].set_title("Uniform\nevery outcome equally likely"); axs[3].set_xlabel("outcome"); axs[3].set_yticks([])
    for a in axs: a.spines[["top", "right", "left"]].set_visible(False)
    fig.subplots_adjust(wspace=0.25); fig.savefig("fig21-3-distributions.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f4():
    rng = np.random.default_rng(21)
    population = d.order_value.to_numpy()
    fig, axs = plt.subplots(1, 4, figsize=(12.5, 2.9), sharey=False)
    axs[0].hist(population/1000, bins=np.arange(0, 150, 3), color="#b8c0cc", edgecolor="white", lw=0.3)
    axs[0].set_title(f"The orders themselves\nmean ₹{population.mean():,.0f}, skew {pd.Series(population).skew():.2f}")
    axs[0].set_xlabel("₹ thousand")
    for ax, n in zip(axs[1:], [5, 30, 100]):
        means = rng.choice(population, size=(4000, n)).mean(axis=1) / 1000
        ax.hist(means, bins=40, color=ACC, edgecolor="white", lw=0.3)
        ax.set_title(f"Means of samples of {n}\nspread {means.std():.2f}k")
        ax.set_xlabel("sample mean (₹ thousand)")
    for a in axs: a.spines[["top", "right"]].set_visible(False); a.set_yticks([]); a.grid(axis="y", color=LIGHT, lw=0.8); a.set_axisbelow(True)
    fig.subplots_adjust(wspace=0.22); fig.savefig("fig21-4-central-limit.svg", format="svg", bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    f1(); f2(); f3(); f4(); print("ok")
