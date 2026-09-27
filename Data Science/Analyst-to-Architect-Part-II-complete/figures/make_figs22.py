# Figures for Chapter 22. Run: python3 make_figs22.py
import pathlib, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
D = pathlib.Path(__file__).resolve().parent.parent / "companion"
INK, MUTED, ACC, ORANGE, GREEN, PURPLE, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#7a4fa0", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
def tidy(ax, axis="y"):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis=axis, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

def f1():
    d = pd.read_csv(D / "ch21" / "delivery_times_2025.csv")
    pop = d.order_value.to_numpy(); truth = pop.mean()
    rng = np.random.default_rng(22)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    misses = 0
    for i in range(60):
        s = rng.choice(pop, 200, replace=False)
        lo, hi = s.mean() - 1.96*s.std(ddof=1)/np.sqrt(200), s.mean() + 1.96*s.std(ddof=1)/np.sqrt(200)
        covers = lo <= truth <= hi
        misses += not covers
        ax.plot([lo/1000, hi/1000], [i, i], color=ACC if covers else RED, lw=1.6, alpha=0.9)
        ax.plot(s.mean()/1000, i, "o", ms=2.6, color=ACC if covers else RED)
    ax.axvline(truth/1000, color=INK, lw=2)
    ax.text(truth/1000 + 0.15, 58, f"the true mean, ₹{truth:,.0f}", color=INK, fontsize=9.5, fontweight="bold")
    ax.set_yticks([]); ax.set_xlabel("95% confidence interval for the mean order value (₹ thousand)")
    ax.set_title(f"Sixty samples of 200 orders: {60-misses} intervals contain the truth, {misses} miss it")
    tidy(ax, "x"); ax.spines["left"].set_visible(False)
    fig.savefig("fig22-1-confidence-intervals.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f2():
    ab = pd.read_csv(D / "ch22" / "ab_test_2026.csv")
    a, b = ab[ab.variant == "A"], ab[ab.variant == "B"]
    observed = b.opened.mean() - a.opened.mean()
    pooled = ab.opened.mean(); n = len(a)
    rng = np.random.default_rng(222)
    null = (rng.binomial(n, pooled, 20000)/n) - (rng.binomial(n, pooled, 20000)/n)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.3))
    ax1.hist(null*100, bins=60, color="#b8c0cc", edgecolor="white", lw=0.3)
    ax1.axvline(observed*100, color=ORANGE, lw=2.4)
    ax1.text(observed*100 + 0.15, ax1.get_ylim()[1]*0.75, f"observed\n+{observed*100:.1f} points", color=ORANGE, fontsize=9.5, fontweight="bold")
    ax1.set_xlabel("difference in open rate under chance alone (points)")
    ax1.set_title("Open rate: the observed gap is hard to get by chance"); tidy(ax1); ax1.set_yticks([])
    observed2 = b.ordered.mean() - a.ordered.mean()
    pooled2 = ab.ordered.mean()
    null2 = (rng.binomial(n, pooled2, 20000)/n) - (rng.binomial(n, pooled2, 20000)/n)
    ax2.hist(null2*100, bins=60, color="#b8c0cc", edgecolor="white", lw=0.3)
    ax2.axvline(observed2*100, color=ORANGE, lw=2.4)
    ax2.text(observed2*100 + 0.03, ax2.get_ylim()[1]*0.75, f"observed\n+{observed2*100:.2f} points", color=ORANGE, fontsize=9.5, fontweight="bold")
    ax2.set_xlabel("difference in order rate under chance alone (points)")
    ax2.set_title("Order rate: the observed gap is ordinary"); tidy(ax2); ax2.set_yticks([])
    fig.subplots_adjust(wspace=0.2); fig.savefig("fig22-2-null-distribution.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f3():
    rng = np.random.default_rng(2223)
    trials, n_max, p = 3000, 4000, 0.25
    results = {}
    for peeks in (1, 5, 20):
        checkpoints = np.linspace(n_max/peeks, n_max, peeks).astype(int)
        false_positives = 0
        for _ in range(trials):
            a = rng.random(n_max) < p
            b = rng.random(n_max) < p
            for c in checkpoints:
                pa, pb = a[:c].mean(), b[:c].mean()
                se = np.sqrt(pa*(1-pa)/c + pb*(1-pb)/c)
                if se > 0 and abs(pa - pb)/se > 1.96:
                    false_positives += 1
                    break
        results[peeks] = false_positives / trials * 100
    fig, ax = plt.subplots(figsize=(7.5, 3.1))
    bars = ax.bar([str(k) for k in results], list(results.values()), color=[GREEN, ORANGE, RED], width=0.55)
    for bar, v in zip(bars, results.values()):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.4, f"{v:.1f}%", ha="center", fontweight="bold", color=INK)
    ax.axhline(5, color=MUTED, ls="--", lw=1.4)
    ax.text(2.35, 5.4, "the 5% you signed up for", color=MUTED, fontsize=9)
    ax.set_xlabel("number of times the test is checked before it ends")
    ax.set_ylabel("false 'winners' (%)"); tidy(ax)
    ax.set_title("Two identical variants, tested 3,000 times: how often peeking declares a winner")
    fig.savefig("fig22-3-peeking.svg", format="svg", bbox_inches="tight"); plt.close(fig)

def f4():
    tr = pd.read_csv(D / "ch22" / "transporters_q4_2025.csv")
    overall = tr.groupby("transporter").on_time.mean()*100
    by_route = tr.groupby(["transporter", "route"]).on_time.mean().unstack()*100
    mix = (tr.groupby(["transporter", "route"]).size()/tr.groupby("transporter").size()).unstack()*100
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12, 3.2))
    a1.bar(overall.index, overall.values, color=[ACC, GREEN], width=0.5)
    for i, v in enumerate(overall.values): a1.text(i, v+0.6, f"{v:.1f}%", ha="center", fontweight="bold")
    a1.set_ylim(0, 105); a1.set_title("Overall: SwiftLine looks better"); tidy(a1)
    x = np.arange(2); w = 0.36
    for k, t in enumerate(by_route.index):
        a2.bar(x + (k-0.5)*w, by_route.loc[t].values, width=w, label=t, color=[ACC, GREEN][k])
        for i, v in enumerate(by_route.loc[t].values):
            a2.text(x[i]+(k-0.5)*w, v+0.6, f"{v:.1f}", ha="center", fontsize=8.5)
    a2.set_xticks(x); a2.set_xticklabels(by_route.columns); a2.set_ylim(0, 105); a2.legend(frameon=False, fontsize=8.5)
    a2.set_title("By route: BlueCart wins both"); tidy(a2)
    bottom = np.zeros(2)
    for j, route in enumerate(mix.columns):
        a3.bar(mix.index, mix[route].values, bottom=bottom, color=[PURPLE, "#c8b6dd"][j], label=route, width=0.5)
        bottom += mix[route].values
    a3.legend(frameon=False, fontsize=8.5); a3.set_ylim(0, 112); a3.set_title("Why: the route mix differs"); tidy(a3)
    a3.set_ylabel("share of each transporter's work (%)")
    fig.subplots_adjust(wspace=0.28); fig.savefig("fig22-4-simpsons-paradox.svg", format="svg", bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    f1(); f2(); f3(); f4(); print("ok")
