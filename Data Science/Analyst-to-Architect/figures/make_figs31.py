# Generates the SVG figures for Chapter 31. Run: python3 make_figs31.py
# Every canvas is 700 px wide and prints at 174 mm (493.2 pt), so 10 px of text prints at 7.05 pt;
# the smallest text here is 10.5 px (7.4 pt).
# Every number drawn is computed here from companion/ch31/causal_data (seed 31), with the same
# models as the chapter's code, so a figure can't drift from the text.
import math, pathlib
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from scipy.optimize import minimize
from make_figs import *

GREEN = "#2f7d6d"; PURPLE = "#7a4fa0"; ORANGE = "#c0662b"; RED = "#b23b3b"
W = 700
MINUS = "−"
DATA = pathlib.Path(__file__).resolve().parents[1] / "companion" / "ch31" / "causal_data"

panel = pd.read_csv(DATA / "region_month.csv", parse_dates=["month"])
panel["log_orders"] = np.log(panel["orders"])
panel["treated"] = (panel["region"] == "North").astype(int)
wide_panel = panel.pivot_table(index="month", columns="region", values="log_orders")
MONTHS = list(wide_panel.index)
CHANGE = MONTHS.index(pd.Timestamp("2025-10-01"))


def pct(x, d=1):
    """A signed percentage with a real minus sign: -0.07 -> '−7.0%'."""
    s = f"{100 * x:+.{d}f}%"
    return s.replace("-", MINUS)


def signed(x, d=1):
    return f"{x:+.{d}f}".replace("-", MINUS)


def month_axis(o, px, y0):
    for i, m in enumerate(MONTHS):
        if m.month in (1, 7):
            o.append(path(f"M{px(i):.1f},{y0} v5", stroke=MUTED, sw=1))
            o.append(text(px(i), y0 + 18, m.strftime("%b %Y"), 10.5, MUTED, anchor="middle"))


def y_title(o, x, y_mid, label):
    o.append(f'<text x="{x}" y="{y_mid:.0f}" font-size="11" fill="{INK}" text-anchor="middle" '
             f'transform="rotate(-90 {x} {y_mid:.0f})">{label}</text>')


def fig_parallel():
    north = wide_panel["North"].to_numpy()
    others = wide_panel[["West", "South", "East"]].mean(axis=1).to_numpy()
    fe = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit()
    eff = fe.params["treated:is_after"]; lo, hi = fe.conf_int().loc["treated:is_after"]
    o = [text(20, 26, "North against the other regions: parallel, then a step", 13, INK, "bold", family=HEAD)]
    x0, x1, y0, y1 = 70, 680, 290, 62
    vlo, vhi = 7.2, 8.1
    def px(i): return x0 + i * (x1 - x0) / (len(MONTHS) - 1)
    def py(v): return y0 - (v - vlo) / (vhi - vlo) * (y0 - y1)
    o.append(path(f"M{x0},{y0} H{x1}", stroke=MUTED, sw=1.2)); o.append(path(f"M{x0},{y0} V{y1}", stroke=MUTED, sw=1.2))
    for v in (7.2, 7.4, 7.6, 7.8, 8.0):
        if v > vlo: o.append(path(f"M{x0},{py(v):.1f} H{x1}", stroke="#e6ebf1", sw=1))
        o.append(path(f"M{x0},{py(v):.1f} h-5", stroke=MUTED, sw=1))
        o.append(text(x0 - 8, py(v) + 4, f"{v:.1f}", 10.5, MUTED, anchor="end"))
    y_title(o, 20, (y0 + y1) / 2, "log of monthly orders")
    month_axis(o, px, y0)
    o.append(path(f"M{px(CHANGE):.1f},{y1 - 8} V{y0}", stroke=RED, sw=1.8, dash="6,4"))
    o.append(text(px(CHANGE) - 6, y1 - 12, "1 Oct 2025: prices rise 6% in North", 11, RED, "bold", anchor="end"))
    o.append(path("M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(others)), stroke=ACC, sw=2.4, dash="7,4"))
    o.append(path("M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(north)), stroke=PURPLE, sw=2.4))
    o.append(text(px(1), py(7.97), "other regions, average (dashed)", 11, ACC, "bold"))
    o.append(text(px(1), py(north[1]) + 22, "North (solid)", 11, PURPLE, "bold"))
    o.append(text(20, y0 + 46, "Before the change the gap between the lines wanders without a clear direction; after it, North sits lower.", 11, MUTED))
    o.append(text(20, y0 + 64, f"Difference-in-differences: {pct(np.exp(eff) - 1)} (95% CI {pct(np.exp(lo) - 1)} to {pct(np.exp(hi) - 1)}). "
                               f"True effect built into the data: {MINUS}8%.", 11, INK))
    return svg(W, y0 + 80, "".join(o))


def synthetic_fit():
    pre = wide_panel[wide_panel.index < "2025-10-01"]
    donors = ["West", "South", "East"]
    def loss(w): return float(np.mean((pre["North"].to_numpy() - pre[donors].to_numpy() @ w) ** 2))
    best = minimize(loss, np.repeat(1 / 3, 3), bounds=[(0, 1)] * 3,
                    constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}], method="SLSQP")
    synth = wide_panel[donors].to_numpy() @ best.x
    gap = wide_panel["North"].to_numpy() - synth
    rmse = math.sqrt(np.mean(gap[:CHANGE] ** 2))
    return dict(zip(donors, best.x)), synth, rmse, gap[CHANGE:].mean()


def fig_synth():
    w, synth, rmse, gap_after = synthetic_fit()
    north = wide_panel["North"].to_numpy()
    o = [text(20, 26, "Synthetic North: a blend of the other regions, fitted before the change", 13, INK, "bold", family=HEAD)]
    x0, x1, y0, y1 = 70, 680, 290, 70
    vlo, vhi = 7.35, 7.85
    def px(i): return x0 + i * (x1 - x0) / (len(MONTHS) - 1)
    def py(v): return y0 - (v - vlo) / (vhi - vlo) * (y0 - y1)
    o.append(rect(px(CHANGE), y1 - 8, x1 - px(CHANGE), y0 - y1 + 8, fill=PKBG, stroke="none"))
    o.append(path(f"M{x0},{y0} H{x1}", stroke=MUTED, sw=1.2)); o.append(path(f"M{x0},{y0} V{y1 - 8}", stroke=MUTED, sw=1.2))
    for v in (7.4, 7.5, 7.6, 7.7, 7.8):
        o.append(path(f"M{x0},{py(v):.1f} H{x1}", stroke="#e6ebf1", sw=1))
        o.append(path(f"M{x0},{py(v):.1f} h-5", stroke=MUTED, sw=1))
        o.append(text(x0 - 8, py(v) + 4, f"{v:.1f}", 10.5, MUTED, anchor="end"))
    y_title(o, 20, (y0 + y1) / 2, "log of monthly orders")
    month_axis(o, px, y0)
    o.append(path(f"M{px(CHANGE):.1f},{y1 - 8} V{y0}", stroke=RED, sw=1.8, dash="6,4"))
    o.append(text(px(CHANGE) + 8, y1 + 8, "after the price rise:", 11, RED, "bold"))
    o.append(text(px(CHANGE) + 8, y1 + 23, "the gap is the estimate", 11, RED, "bold"))
    o.append(path("M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(synth)), stroke=ACC, sw=2.4, dash="7,4"))
    o.append(path("M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(north)), stroke=PURPLE, sw=2.4))
    o.append(text(px(1), py(north[1]) + 26, "North, real (solid)", 11, PURPLE, "bold"))
    o.append(text(px(1), py(7.835), "synthetic North (dashed) =", 11, ACC, "bold"))
    o.append(text(px(1), py(7.835) + 15, f"{w['West']:.2f} West + {w['South']:.2f} South + {w['East']:.2f} East", 11, ACC, "bold"))
    o.append(text(20, y0 + 46, f"Weights chosen to track North for the fifteen months before October 2025 (root mean squared error {rmse:.3f}).", 11, MUTED))
    o.append(text(20, y0 + 64, f"Average gap in the shaded months: {pct(np.exp(gap_after) - 1)}, against a true effect of {MINUS}8%.", 11, INK))
    return svg(W, y0 + 80, "".join(o))


def balance_rows():
    qbr = pd.read_csv(DATA / "qbr_program.csv")
    qbr["log_2024"] = np.log(qbr["revenue_2024"])
    m = smf.logit("in_qbr_program ~ log_2024 + growth_2024 + years_as_customer + C(segment)", data=qbr).fit(disp=False)
    qbr["propensity"] = m.predict(qbr)
    available = qbr[qbr["in_qbr_program"] == 0].set_index("customer_id")["propensity"].to_dict()
    ids = []
    for row in qbr[qbr["in_qbr_program"] == 1].sort_values("propensity", ascending=False).itertuples():
        best = min(available, key=lambda c: abs(available[c] - row.propensity))
        if abs(available[best] - row.propensity) <= 0.05:
            ids += [row.customer_id, best]; del available[best]
    matched = qbr[qbr["customer_id"].isin(ids)]
    def smd(d, col):
        a = d.loc[d["in_qbr_program"] == 1, col]; b = d.loc[d["in_qbr_program"] == 0, col]
        return (a.mean() - b.mean()) / math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    names = [("prior revenue (log)", "log_2024"), ("growth in 2024", "growth_2024"),
             ("years as customer", "years_as_customer"), ("propensity score", "propensity")]
    return [(label, smd(qbr, c), smd(matched, c)) for label, c in names]


def fig_balance():
    rows = balance_rows()
    o = [text(20, 26, "Matching is only worth something if it balanced the groups", 13, INK, "bold", family=HEAD)]
    x0, x1 = 190, 670; lo, hi = -0.2, 0.8
    top, bottom = 62, 252
    def px(v): return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    o.append(rect(px(-0.1), top, px(0.1) - px(-0.1), bottom - top, fill=FKBG, stroke="none"))
    o.append(text(px(0.1) + 6, top + 12, "|SMD| under 0.1: balanced", 10.5, GREEN, "bold"))
    o.append(path(f"M{px(0):.1f},{top} V{bottom}", stroke=MUTED, sw=1.2))
    o.append(path(f"M{x0},{bottom} H{x1}", stroke=MUTED, sw=1.2))
    for v in (-0.1, 0, 0.1, 0.2, 0.4, 0.6, 0.8):
        o.append(path(f"M{px(v):.1f},{bottom} v5", stroke=MUTED, sw=1))
        o.append(text(px(v), bottom + 18, f"{v:g}".replace("-", MINUS), 10.5, MUTED, anchor="middle"))
    o.append(text((x0 + x1) / 2, bottom + 36, "standardized mean difference (participants minus others, in standard deviations)", 11, INK, anchor="middle"))
    y = top + 34
    for label, before, after in rows:
        o.append(text(20, y + 4, label, 11, INK))
        o.append(path(f"M{px(before):.1f},{y} L{px(after):.1f},{y}", stroke=RULE, sw=1.4, dash="4,3"))
        o.append(f'<circle cx="{px(before):.1f}" cy="{y}" r="5.5" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
        o.append(rect(px(after) - 5, y - 5, 10, 10, fill=ACC, stroke=ACC))
        o.append(text(px(before) + 10, y - 7, f"{before:.3f}".replace("-", MINUS), 10.5, ORANGE))
        o.append(text(px(after) + 9 if after >= 0 else px(after) - 9, y + 16, f"{after:.3f}".replace("-", MINUS), 10.5, ACC,
                      anchor="start" if after >= 0 else "end"))
        y += 42
    ly = bottom + 62
    o.append(f'<circle cx="30" cy="{ly - 4}" r="5.5" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
    o.append(text(42, ly, "before matching (hollow circle)", 11, INK))
    o.append(rect(260, ly - 9, 10, 10, fill=ACC, stroke=ACC)); o.append(text(278, ly, "after matching (filled square)", 11, INK))
    return svg(W, ly + 14, "".join(o))


def fig_rd():
    orders = pd.read_csv(DATA / "delivery_threshold.csv")
    orders["centred"] = (orders["order_value"] - 25000) / 1000
    wide = orders[orders["centred"].abs() <= 5].copy()
    rd = smf.ols("repeat_within_90_days ~ free_delivery + centred + free_delivery:centred", data=wide).fit()
    b0, b1, b2, b3 = (rd.params[k] for k in ("Intercept", "free_delivery", "centred", "free_delivery:centred"))
    wide["band"] = np.floor(wide["centred"] * 2) / 2                   # [a, a + 0.5), like right=False
    pts = wide[wide["band"] < 5].groupby("band")["repeat_within_90_days"].mean()
    o = [text(20, 26, "Free delivery at ₹25,000: the estimate is the size of the step", 13, INK, "bold", family=HEAD)]
    x0, x1, y0, y1 = 70, 650, 282, 62
    vlo, vhi = 0.2, 0.55
    def px(c): return x0 + (c + 5) / 10 * (x1 - x0)
    def py(p): return y0 - (p - vlo) / (vhi - vlo) * (y0 - y1)
    o.append(path(f"M{x0},{y0} H{x1}", stroke=MUTED, sw=1.2)); o.append(path(f"M{x0},{y0} V{y1}", stroke=MUTED, sw=1.2))
    for p in (0.2, 0.3, 0.4, 0.5):
        if p > vlo: o.append(path(f"M{x0},{py(p):.1f} H{x1}", stroke="#e6ebf1", sw=1))
        o.append(path(f"M{x0},{py(p):.1f} h-5", stroke=MUTED, sw=1))
        o.append(text(x0 - 8, py(p) + 4, f"{p:.0%}", 10.5, MUTED, anchor="end"))
    y_title(o, 20, (y0 + y1) / 2, "reorder within 90 days")
    for c in (-5, -2.5, 0, 2.5, 5):
        o.append(path(f"M{px(c):.1f},{y0} v5", stroke=MUTED, sw=1))
        o.append(text(px(c), y0 + 18, f"₹{25000 + c * 1000:,.0f}", 10.5, MUTED, anchor="middle"))
    o.append(path(f"M{px(0):.1f},{y1 - 6} V{y0}", stroke=RED, sw=1.8, dash="6,4"))
    o.append(text(px(0) + 8, y1 + 4, "₹25,000: free delivery starts", 11, RED, "bold"))
    for c, p in pts.items():
        x, y = px(c + 0.25), py(p)
        if c < 0:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="{PURPLE}" stroke-width="1.8"/>')
        else:
            o.append(rect(round(x - 4, 1), round(y - 4, 1), 8, 8, fill=GREEN, stroke=GREEN))
    o.append(path(f"M{px(-5):.1f},{py(b0 - 5 * b2):.1f} L{px(0):.1f},{py(b0):.1f}", stroke=PURPLE, sw=2.4))
    o.append(path(f"M{px(0):.1f},{py(b0 + b1):.1f} L{px(5):.1f},{py(b0 + b1 + 5 * (b2 + b3)):.1f}", stroke=GREEN, sw=2.4))
    o.append(path(f"M{px(0):.1f},{py(b0):.1f} V{py(b0 + b1):.1f}", stroke=ORANGE, sw=3))
    o.append(text(px(0) - 8, py(b0 + b1 / 2) + 4, f"jump {signed(100 * b1)} points", 11.5, ORANGE, "bold", anchor="end"))
    o.append(text(20, y0 + 44, "Each marker: the reorder rate in a ₹500 band (hollow circles below the cut-off, filled squares above).", 11, MUTED))
    o.append(text(20, y0 + 62, "The slopes are the ordinary link between order size and reordering; only the jump is the rule's effect.", 11, MUTED))
    o.append(text(20, y0 + 80, f"True jump built into the data: +6.0 points.", 11, INK))
    return svg(W, y0 + 96, "".join(o))


def fig_choose():
    o = [text(20, 26, "Which method, and what it costs you", 13, INK, "bold", family=HEAD)]
    rows = [("Can you randomize?", "Run the experiment (Chapter 30)", "you decide who gets it", "strongest", GREEN),
            ("Is there a threshold rule?", "Regression discontinuity", "the answer is local to the cut-off", "strong, local", GREEN),
            ("Before-and-after data for both groups?", "Difference-in-differences", "needs parallel trends", "moderate to strong", ACC),
            ("Many untreated units, one treated?", "Synthetic control", "judge it by the pre-change fit", "moderate to strong", ACC),
            ("Only one snapshot, good covariates?", "Matching / propensity scores", "assumes nothing unmeasured", "moderate", ORANGE),
            ("Shifts the treatment, not the outcome?", "Instrumental variables", "exclusion can't be tested", "strong if valid", ORANGE),
            ("None of the above?", "Describe; don't claim a cause", "say so plainly", "no causal claim", RED)]
    o.append(text(20, 52, "Question", 11, MUTED, "bold")); o.append(text(313, 52, "Method, and its catch", 11, MUTED, "bold"))
    o.append(text(619, 52, "Evidence", 11, MUTED, "bold", anchor="middle"))
    y = 60
    for question, method, caveat, strength, c in rows:
        o.append(rect(20, y, 262, 42, fill=ROWALT, stroke=RULE, rx=5)); o.append(text(30, y + 25, question, 11, INK))
        o.append(path(f"M284,{y + 21} H301", stroke=MUTED, sw=1.6)); o.append(path(f"M294,{y + 16} L301,{y + 21} L294,{y + 26}", stroke=MUTED, sw=1.6))
        o.append(rect(303, y, 245, 42, fill="#fff", stroke=c, sw=1.8, rx=5))
        o.append(text(313, y + 18, method, 11.5, c, "bold")); o.append(text(313, y + 34, caveat, 10.5, MUTED))
        o.append(rect(554, y + 8, 130, 26, fill="#fff", stroke=c, sw=1.2, rx=13))
        o.append(text(619, y + 25, strength, 10.5, c, "bold", anchor="middle"))
        y += 50
    return svg(W, y + 6, "".join(o))


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    for name, fn in [("fig31-1-parallel-trends.svg", fig_parallel), ("fig31-2-synthetic-control.svg", fig_synth),
                     ("fig31-3-matching-balance.svg", fig_balance), ("fig31-4-discontinuity.svg", fig_rd),
                     ("fig31-5-which-method.svg", fig_choose)]:
        (here / name).write_text(fn(), encoding="utf-8")
    print("ok31")
