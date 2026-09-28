# Figures for Chapter 22. Run: python3 make_figs22.py   (reads companion/ch21 and companion/ch22)
# Every figure prints at the full text width, 174 mm = 493.2 pt. matplotlib writes text as paths, so
# tools/pdf/fig_check.py can't measure it: printed_sizes() below reports the smallest printed text size.
import pathlib, re, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
from scipy import stats
D = pathlib.Path(__file__).resolve().parent.parent / "companion"
OUT = pathlib.Path(__file__).resolve().parent
INK, MUTED, ACC, ORANGE, GREEN, PURPLE, RED, LIGHT = "#1d2330", "#5b6475", "#0f5c8c", "#c0662b", "#2f7d6d", "#7a4fa0", "#b23b3b", "#dfe5ec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 8, "ytick.labelsize": 8,
                     "legend.fontsize": 8, "axes.edgecolor": "#c9d3df", "svg.fonttype": "path"})
PRINT_PT = 493.2
REPORT = []

def tidy(ax, axis="y"):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis=axis, color=LIGHT, lw=0.8); ax.set_axisbelow(True)

def save(fig, name):
    path = OUT / name
    fig.savefig(path, format="svg", bbox_inches="tight")
    fig.canvas.draw()
    sizes = [(t.get_fontsize(), t.get_text()) for t in fig.findobj(mtext.Text)
             if t.get_visible() and t.get_text().strip() and t.get_window_extent().width > 0]
    W = float(re.search(r'<svg[^>]*width="([\d.]+)pt"', path.read_text()).group(1))
    lo = min(sizes)
    REPORT.append((name, W, round(lo[0] * PRINT_PT / W, 2), lo[1]))
    plt.close(fig)

def f1():
    d = pd.read_csv(D / "ch21" / "delivery_times_2025.csv")
    pop = d.order_value.to_numpy(); truth = pop.mean()
    rng = np.random.default_rng(22)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    misses = 0
    for i in range(60):
        s = rng.choice(pop, 200, replace=False)
        half = stats.t.ppf(0.975, 199) * s.std(ddof=1) / np.sqrt(200)
        lo, hi = s.mean() - half, s.mean() + half
        covers = lo <= truth <= hi
        misses += not covers
        ax.plot([lo/1000, hi/1000], [i, i], color=ACC if covers else RED, lw=1.5 if covers else 2.2, alpha=0.9)
        ax.plot(s.mean()/1000, i, "o", ms=2.4, color=ACC if covers else RED)
        if not covers:   # label the misses at their far end, so red is not the only cue
            left = s.mean() < truth
            ax.text(lo/1000 - 0.2 if left else hi/1000 + 0.2, i, "misses", va="center",
                    ha="right" if left else "left", color=RED, fontsize=8, fontweight="bold")
    ax.axvline(truth/1000, color=INK, lw=1.8)
    ax.set_ylim(-1.5, 64.5); ax.set_xlim(17.2, 32.4)
    ax.annotate(f"the true mean, ₹{truth:,.0f}", xy=(truth/1000, 61.5), xytext=(truth/1000 + 2.2, 62.3),
                color=INK, fontsize=8.5, fontweight="bold", va="center",
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"),
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_yticks([]); ax.set_xlabel("95% confidence interval for the mean order value (₹ thousand)")
    ax.set_title(f"Sixty samples of 200 orders: {60-misses} intervals contain the truth, {misses} miss it", pad=8)
    tidy(ax, "x"); ax.spines["left"].set_visible(False)
    save(fig, "fig22-1-confidence-intervals.svg")

def f2():
    ab = pd.read_csv(D / "ch22" / "ab_test_2026.csv")
    a, b = ab[ab.variant == "A"], ab[ab.variant == "B"]
    n = len(a); rng = np.random.default_rng(222)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))
    for ax, col, title, xlabel, fmt in [
            (ax1, "opened", "Open rate: hard to get by chance", "difference in open rate (points)", "+{:.1f}"),
            (ax2, "ordered", "Order rate: an ordinary gap", "difference in order rate (points)", "+{:.2f}")]:
        observed = b[col].mean() - a[col].mean(); pooled = ab[col].mean()
        null = (rng.binomial(n, pooled, 20000)/n) - (rng.binomial(n, pooled, 20000)/n)
        ax.hist(null*100, bins=60, color="#b8c0cc", edgecolor="white", lw=0.3)
        ax.axvline(observed*100, color=ORANGE, lw=2.2)
        ax.text(observed*100, ax.get_ylim()[1]*1.02, "observed\n" + fmt.format(observed*100) + " points",
                color=ORANGE, fontsize=8.5, fontweight="bold", ha="right" if col == "opened" else "left", va="bottom")
        ax.set_xlabel(xlabel); ax.set_title(title, pad=24); tidy(ax); ax.set_yticks([])
    ax1.text(0.02, 0.95, "chance alone", transform=ax1.transAxes, color=MUTED, fontsize=8, va="top")
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig22-2-null-distribution.svg")

def f3():
    # the chapter's section 22.4 simulation, exactly: seed 2223, 1,500 pairs for each way of checking
    rng = np.random.default_rng(2223)
    trials, n_max, p = 1500, 4000, 0.25
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
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    labels = ["once", "5 times", "20 times"]
    bars = ax.bar(labels, list(results.values()), color=[GREEN, ORANGE, RED], width=0.55)
    for bar, v in zip(bars, results.values()):
        y = v + 0.6 if v > 8 else 6.2       # the small bar's label sits above the 5% line, not on it
        ax.text(bar.get_x()+bar.get_width()/2, y, f"{v:.1f}%", ha="center", fontweight="bold", color=INK)
    ax.axhline(5, color=MUTED, ls="--", lw=1.2)
    ax.text(2.34, 5.5, "the 5% you\nsigned up for", color=MUTED, fontsize=8, ha="left", va="bottom")
    ax.set_ylim(0, 29); ax.set_xlim(-0.45, 2.95)
    ax.set_xlabel("number of times the test is checked before it ends")
    ax.set_ylabel("false 'winners' (%)"); tidy(ax)
    ax.set_title("Two identical variants, 1,500 tests per bar: how often peeking declares a winner", pad=8)
    save(fig, "fig22-3-peeking.svg")

def f4():
    tr = pd.read_csv(D / "ch22" / "transporters_q4_2025.csv")
    overall = tr.groupby("transporter").on_time.mean()*100
    by_route = tr.groupby(["transporter", "route"]).on_time.mean().unstack()*100
    mix = (tr.groupby(["transporter", "route"]).size()/tr.groupby("transporter").size()).unstack()*100
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(7.0, 3.0))
    cols = {"BlueCart": ACC, "SwiftLine": GREEN}
    a1.bar(overall.index, overall.values, color=[cols[t] for t in overall.index], width=0.55)
    for i, v in enumerate(overall.values): a1.text(i, v+1.5, f"{v:.1f}%", ha="center", fontweight="bold")
    a1.set_ylim(0, 108); a1.set_title("1. Overall:\nSwiftLine looks better"); tidy(a1)
    a1.set_ylabel("on time (%)")
    x = np.arange(2); w = 0.38
    for k, t in enumerate(by_route.index):
        a2.bar(x + (k-0.5)*w, by_route.loc[t].values, width=w, color=cols[t])
        for i, v in enumerate(by_route.loc[t].values):
            a2.text(x[i]+(k-0.5)*w, v+1.5, f"{v:.1f}", ha="center", fontsize=7.5)
            a2.text(x[i]+(k-0.5)*w, 6, t[0], ha="center", color="white", fontweight="bold", fontsize=8)
    a2.set_xticks(x); a2.set_xticklabels(by_route.columns); a2.set_ylim(0, 108)
    a2.set_title("2. By route:\nBlueCart (B) wins both"); tidy(a2)
    bottom = np.zeros(2)
    shades = {"Metro": "#c8b6dd", "Upcountry": PURPLE}
    for route in ["Upcountry", "Metro"]:
        vals = mix[route].values
        a3.bar(mix.index, vals, bottom=bottom, color=shades[route], width=0.8, edgecolor="white", lw=1)
        for i, v in enumerate(vals):
            a3.text(i, bottom[i] + v/2, f"{v:.0f}%\n{route.lower()}", ha="center", va="center", fontsize=7,
                    color="white" if route == "Upcountry" else INK, fontweight="bold")
        bottom += vals
    a3.set_ylim(0, 108); a3.set_title("3. Why:\nthe route mix differs"); tidy(a3)
    a3.set_ylabel("share of deliveries (%)")
    fig.subplots_adjust(wspace=0.42)
    save(fig, "fig22-4-simpsons-paradox.svg")

def f5():
    d = pd.read_csv(D / "ch21" / "delivery_times_2025.csv")
    bc = d.groupby("customer_id").agg(orders=("order_id", "count"), revenue=("order_value", "sum"))
    r = stats.pearsonr(bc.orders, bc.revenue).statistic
    rng = np.random.default_rng(5)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw={"width_ratios": [1.5, 1]})
    a1.scatter(bc.orders + rng.uniform(-0.3, 0.3, len(bc)), bc.revenue/1e5, s=4, alpha=0.25, color=ACC, lw=0)
    a1.set_xlabel("orders in 2025 (jittered)"); a1.set_ylabel("revenue (₹ lakh)")
    a1.set_title(f"{len(bc):,} customers: r = {r:.3f}"); tidy(a1, "both")
    xu = np.arange(-5, 6); yu = xu**2
    a2.plot(xu, yu, color=LIGHT, lw=1.2, zorder=1)
    a2.scatter(xu, yu, s=22, color=ORANGE, zorder=2)
    a2.set_xlabel("x"); a2.set_ylabel("y = x²")
    a2.set_title(f"A perfect U: r = {abs(stats.pearsonr(xu, yu).statistic):.2f}"); tidy(a2, "both")
    fig.subplots_adjust(wspace=0.3)
    save(fig, "fig22-5-correlation.svg")

def f6():
    x = np.array([2, 4, 5, 7, 9, 12]); y = np.array([55, 90, 140, 160, 230, 290])
    fit = stats.linregress(x, y); yhat = fit.intercept + fit.slope * x; e = y - yhat
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.0), gridspec_kw={"width_ratios": [1.35, 1]})
    xs = np.array([0, 13])
    a1.plot(xs, fit.intercept + fit.slope*xs, color=ACC, lw=1.8)
    for xi, yi, fi, ei in zip(x, y, yhat, e):
        a1.plot([xi, xi], [fi, yi], color=ORANGE, lw=1.4)
        a1.text(xi + 0.25, (fi + yi)/2, f"{ei:+.1f}", color=ORANGE, fontsize=7.5, va="center", fontweight="bold")
    a1.scatter(x, y, s=26, color=INK, zorder=3)
    a1.text(0.3, 262, f"ŷ = {fit.intercept:.2f} + {fit.slope:.2f}x", color=ACC, fontsize=8.5, fontweight="bold")
    a1.text(0.3, 238, "orange: residuals", color=ORANGE, fontsize=8)
    a1.set_xlim(0, 13.5); a1.set_ylim(0, 310)
    a1.set_xlabel("orders (x)"); a1.set_ylabel("revenue, ₹ thousand (y)")
    a1.set_title("The least-squares line"); tidy(a1, "both")
    a2.axhline(0, color=MUTED, ls="--", lw=1)
    a2.scatter(x, e, s=26, color=ORANGE, zorder=3)
    a2.set_xlim(0, 13.5); a2.set_ylim(-20, 20)
    a2.set_xlabel("orders (x)"); a2.set_ylabel("residual (₹ thousand)")
    a2.set_title("Residual plot: no pattern"); tidy(a2, "both")
    fig.subplots_adjust(wspace=0.32)
    save(fig, "fig22-6-regression-line.svg")

if __name__ == "__main__":
    f1(); f2(); f3(); f4(); f5(); f6()
    for name, W, lo, txt in REPORT:
        print(f"{name:34s} width {W:6.1f} pt  smallest text prints at {lo:4.2f} pt ({txt[:20]!r})")
