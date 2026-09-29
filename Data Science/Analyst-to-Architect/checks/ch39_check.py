"""Analyst to Architect · Chapter 39 · number check.
Recomputes the numbers quoted in Chapter 39's prose (hand examples, tables, story figures) and writes
checks/ch39_results.json for the figures (figures/make_figs39.py reads it).
Run from checks/: python3 ch39_check.py   (about 1 minute, one CPU core).
It imports the chapter's helpers from companion/ch39/ (lead_data.py, churn_data.py), which read ../crm/ and
../accounts/; set CH39_COMPANION to another copy of companion/ch39 if the data lives elsewhere.
Riverstone Supplies is fictional."""
import json, math, os, pathlib, sys, warnings
import numpy as np, pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import partial_dependence
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix, mean_absolute_error,
                             mean_absolute_percentage_error, precision_recall_curve, r2_score, roc_auc_score,
                             roc_curve, root_mean_squared_error)
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import FunctionTransformer
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("CH39_COMPANION", str(HERE.parent / "companion" / "ch39")))
from lead_data import LEAD_CATS, LEAD_NUMS, load_leads, make_model
from churn_data import CHURN_CATS, CHURN_NUMS, load_accounts, make_churn_model
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

# ---------- 39.1 the ten leads by hand ----------
tp_ = np.array([0.90, 0.80, 0.70, 0.60, 0.45, 0.40, 0.30, 0.20, 0.10, 0.05]); ty = np.array([1, 1, 0, 1, 0, 1, 0, 0, 0, 0])
def counts(t):
    tn, fp, fn, tp = confusion_matrix(ty, (tp_ >= t).astype(int)).ravel(); return int(tp), int(fp), int(fn), int(tn)
ok("toy 0.5 counts", counts(0.5), (3, 1, 1, 5)); ok("toy 0.35 counts", counts(0.35), (4, 2, 0, 4))
ok("toy metrics", (0.8, 0.75, 0.75, round(2 * .75 * .75 / 1.5, 2), round(5 / 6, 3), round(1 / 6, 3)), (0.8, 0.75, 0.75, 0.75, 0.833, 0.167))
ok("F1 0.9/0.1", round(2 * .9 * .1 / 1.0, 2), 0.18); ok("toy 0.35 precision", round(4 / 6, 3), 0.667)
ok("macro/weighted F1", (round((.9 + .8 + .2) / 3, 3), round((.9 * 800 + .8 * 150 + .2 * 50) / 1000, 3)), (0.633, 0.85))
# ---------- 39.2 sweep, AUC by pairs, AP by hand ----------
rows = []
for k in range(1, 11):
    tp, fp = int(ty[:k].sum()), int(k - ty[:k].sum()); rows.append((tp, fp, round(tp / 4, 2), round(fp / 6, 2), round(tp / k, 2)))
ok("sweep table", rows, [(1, 0, .25, 0, 1), (2, 0, .5, 0, 1), (2, 1, .5, .17, .67), (3, 1, .75, .17, .75), (3, 2, .75, .33, .6),
                         (4, 2, 1, .33, .67), (4, 3, 1, .5, .57), (4, 4, 1, .67, .5), (4, 5, 1, .83, .44), (4, 6, 1, 1, .4)])
pairs = sum(int(a > b) for a, ya in zip(tp_, ty) if ya for b, yb in zip(tp_, ty) if not yb)
ok("pairs", (pairs, 6 + 6 + 5 + 4), (21, 21)); ok("toy AUC", round(roc_auc_score(ty, tp_), 3), 0.875)
ok("toy AP", (round((1 + 1 + .75 + 4 / 6) / 4, 3), round(average_precision_score(ty, tp_), 3)), (0.854, 0.854))
# ---------- 39.3 four accounts ----------
ta, tpd = np.array([100, 200, 50, 1000]), np.array([110, 180, 70, 700])
ok("toy MAE/RMSE/MAPE/R2", (mean_absolute_error(ta, tpd), round(root_mean_squared_error(ta, tpd), 1),
                            round(mean_absolute_percentage_error(ta, tpd), 3), round(r2_score(ta, tpd), 3)), (87.5, 150.7, 0.225, 0.848))
ok("SS_tot, share of squares", (float(((ta - ta.mean()) ** 2).sum()), round(90000 / 90900, 2), round(150.75 / 87.5, 1)), (596875.0, 0.99, 1.7))
ok("WAPE", round(350 / 1350 * 100, 1), 25.9); ok("MAPE asymmetry", (50 / 100, round(50 / 150, 2)), (0.5, 0.33))
# ---------- lead model ----------
train, valid, test = load_leads(); X = LEAD_CATS + LEAD_NUMS
model = make_model(LEAD_CATS, LEAD_NUMS).fit(train[X], train["won"])
p = model.predict_proba(valid[X])[:, 1]; y = valid["won"].to_numpy()
ok("valid", (len(valid), int(y.sum())), (2225, 146)); ok("train", (len(train), int(train.won.sum())), (7291, 576))
tn, fp, fn, tp = confusion_matrix(y, (p >= 0.5).astype(int)).ravel(); ok("0.5 matrix", (tp, fp, fn, tn), (4, 3, 142, 2076))
ok("all-lost vs model accuracy", (round(2079 / 2225, 4), round((4 + 2076) / 2225, 4)), (0.9344, 0.9348))
tn, fp, fn, tp = confusion_matrix(y, (p >= 0.1).astype(int)).ravel(); ok("0.1 matrix", (tp, fp, fn, tn), (100, 386, 46, 1693))
ok("precision/recall/F1/spec/FPR", (round(100 / 486, 3), round(100 / 146, 3), round(2 * .206 * .685 / .891, 3), round(1693 / 2079, 3), round(386 / 2079, 3)),
   (0.206, 0.685, 0.317, 0.814, 0.186))
ok("ROC-AUC, PR-AUC, ratio", (round(roc_auc_score(y, p), 3), round(average_precision_score(y, p), 3), round(0.302 / y.mean(), 1)), (0.823, 0.302, 4.6))
order = np.argsort(-p); ok("top50", int(y[order[:50]].sum()), 22); ok("top400 share", f"{y[order[:400]].sum() / y.sum():.0%}", "63%")
ok("400 share of leads", round(400 / 2225 * 100), 18); ok("7x base", round(0.44 / y.mean(), 1), 6.7)
# ---------- 39.4 calibration ----------
ok("Brier by hand", round(((1 - .8) ** 2 + .1 ** 2 + (1 - .3) ** 2) / 3, 2), 0.18)
ok("log loss by hand", (round(-math.log(.8), 3), round(-math.log(.9), 3), round(-math.log(.3), 3), round(-(math.log(.8) + math.log(.9) + math.log(.3)) / 3, 3)),
   (0.223, 0.105, 1.204, 0.511))
ok("base-rate Brier", (round(0.0656 * 0.9344, 4), round(brier_score_loss(y, np.full(len(y), y.mean())), 4)), (0.0613, 0.0613))
fpos_l, mp_l = calibration_curve(y, p, n_bins=10, strategy="quantile")
ok("logistic bins quoted", [round(float(v), 3) for v in (mp_l[0], fpos_l[0], mp_l[-1], fpos_l[-1], mp_l[5], fpos_l[5], mp_l[6], fpos_l[6])],
   [0.005, 0.004, 0.278, 0.287, 0.044, 0.059, 0.061, 0.027])
to_dense = FunctionTransformer(lambda M: M.toarray() if hasattr(M, "toarray") else M)
nb = make_model(LEAD_CATS, LEAD_NUMS, GaussianNB()); nb.steps.insert(1, ("dense", to_dense))
p_nb = nb.fit(train[X], train["won"]).predict_proba(valid[X])[:, 1]
p_gb = make_model(LEAD_CATS, LEAD_NUMS, HistGradientBoostingClassifier(random_state=39)).fit(train[X], train["won"]).predict_proba(valid[X])[:, 1]
ok("NB mean pred, ROC", (round(p_nb.mean(), 2), round(roc_auc_score(y, p_nb), 3)), (0.18, 0.806))
fpos, mpred = calibration_curve(y, p_nb, n_bins=10, strategy="quantile"); ok("NB top tenth", (round(mpred[-1], 2), round(fpos[-1], 2)), (0.94, 0.27))
ok("boosting mean, AUC", (round(p_gb.mean(), 3), round(roc_auc_score(y, p_gb), 3)), (0.064, 0.781))
# ---------- 39.5 costs ----------
accounts = pd.read_csv(pathlib.Path(sys.path[0]).parent / "accounts" / "accounts.csv")
new = accounts[accounts.tenure_months <= 12]; WIN = new.revenue_2024.median() * 0.15
ok("first-year median", new.revenue_2024.median(), 201700.0); ok("win value", round(WIN), 30255); ok("break-even", round(1500 / WIN, 4), 0.0496)
def profit(t, pp=p, yy=y):
    c = pp >= t; return WIN * yy[c].sum() - 1500 * c.sum(), int(c.sum()), int(yy[c].sum())
grid = np.linspace(0, 0.5, 501); profits = np.array([profit(t)[0] for t in grid])
ok("best threshold", round(grid[profits.argmax()], 3), 0.077); ok("best profit", round(profits.max()), 2448060)
ok("worked at best", (profit(0.077)[1], 112 + 515), (627, 627)); ok("all leads profit", round(profit(0)[0]), 1079730)
share = profits / profits.max(); within = grid[share >= 0.95]
ok("5% band 0.062-0.089 all within", bool(all(share[(grid > 0.0615) & (grid < 0.0895)] >= 0.95)), True)
ok("5% band edges fail", (bool(share[np.isclose(grid, 0.061)][0] < 0.95), bool(share[np.isclose(grid, 0.090)][0] < 0.95)), (True, True))
ok("0.04-0.10 max drop < 7.5%", bool((1 - share[(grid > 0.0395) & (grid < 0.1005)]).max() < 0.075), True)
ok("scattered 5% points", (round(within.min(), 3), round(within.max(), 3)), (0.045, 0.103))
top = order[:504]; t_cap = p[top].min(); pr, w, wi = profit(t_cap)
ok("capacity", (round(t_cap, 3), w, wi, round(pr)), (0.097, 504, 102, 2330010))
rule = valid.source.isin(["Referral", "Trade fair", "Partner"]).to_numpy()
rp = WIN * y[rule].sum() - 1500 * rule.sum(); ok("rule", (int(rule.sum()), int(y[rule].sum()), round(rp)), (531, 84, 1744920))
ok("model worth 5.9 lakh, 12 lakh a year", (round(pr - rp, -4), round(2 * (pr - rp), -5)), (590000.0, 1200000.0))
ok("lakh prose", (round(1079730 / 1e5, 1), round(2448060 / 1e5, 1), round(2330010 / 1e5, 1), round(1744920 / 1e5, 1), round(3697812 / 1e5)),
   (10.8, 24.5, 23.3, 17.4, 37))
ok("answer 7 fall", (2448060 - 1633500, round((2448060 - 1633500) / 1e5, 1), round((2448060 - 1633500) / 2448060, 2)), (814560, 8.1, 0.33))
# ---------- 39.6 balanced weights ----------
ok("balanced weights", (round(7291 / (2 * 576), 2), round(7291 / (2 * 6715), 2), 576 * 7291 / (2 * 576), 6715 * 7291 / (2 * 6715)), (6.33, 0.54, 3645.5, 3645.5))
# ---------- 39.7 by-hand examples ----------
ref, strong, won = np.array([1, 1, 1, 0, 0, 0]), np.array([1, 0, 1, 0, 1, 0]), np.array([1, 1, 0, 0, 0, 1])
ok("permutation toy", (round((ref == won).mean(), 3), round((ref[::-1] == won).mean(), 3)), (0.667, 0.333))
base = -3 + 1.2 * 0.1 + 0.8 * 0.3
ok("SHAP toy", (round(base, 2), round(1.2 * 0.9, 2), round(0.8 * -0.3, 2), round(base + 1.08 - 0.24, 2), -3 + 1.2), (-2.64, 1.08, -0.24, -1.8, -1.8))
ok("perm rise share of log loss", round(0.0334 / 0.1948, 2), 0.17)
rest, test_acc = load_accounts(); cols = CHURN_CATS + CHURN_NUMS
churn = make_churn_model().fit(rest[cols], rest["churned_2025"])
three = test_acc[cols].head(3).copy(); avgs = []
for d in [30, 120, 200]:
    three["days_since_last_order"] = d; avgs.append(round(float(churn.predict_proba(three)[:, 1].mean()), 3))
ok("PD by hand", avgs, [0.056, 0.206, 0.348])
# ---------- 39.8 fairness ----------
called = p >= 0.05; desk = valid.inside_desk.to_numpy() == 1
rd, rr = called[desk & (y == 1)].mean(), called[~desk & (y == 1)].mean()
ok("recall desk/reps", (round(rd, 2), round(rr, 2)), (0.57, 0.91)); ok("miss rates, ratio", (round(1 - rd, 2), round(1 - rr, 2), round((1 - rd) / (1 - rr), 1)), (0.43, 0.09, 4.8))
ok("share called", (round(called[~desk].mean(), 2), round(called[desk].mean(), 2)), (0.55, 0.21))
ok("no segment", int(valid.segment.isna().sum()), 108)
# ---------- answers ----------
ok("answer 1", (10000 - 300 - 80, 120 / 300, 120 / 200, round(180 / 9800, 3)), (9620, 0.4, 0.6, 0.018))
ok("answer 3", (900 / 12000, 0.06 * 12000 - 900), (0.075, -180.0)); ok("answer 4", round(math.sqrt(math.pi / 2), 2), 1.25)
ok("answer 5 differences", (121 - 112, 904 - 627, 112 - 76, 627 - 291), (9, 277, 36, 336))
# ---------- figure data ----------
fpr, tpr, _ = roc_curve(y, p); prec, rec, _ = precision_recall_curve(y, p)
curves = {n: [list(map(float, a)) for a in calibration_curve(y, q, n_bins=10, strategy="quantile")] for n, q in
          [("logistic regression", p), ("Naive Bayes", p_nb), ("gradient boosting", p_gb)]}
pdr = partial_dependence(churn, test_acc[cols], features=["days_since_last_order"], grid_resolution=40,
                         kind="average", method="brute", response_method="predict_proba")
json.dump({"fpr": fpr.tolist(), "tpr": tpr.tolist(), "prec": prec.tolist(), "rec": rec.tolist(), "calib": curves,
           "grid": grid.tolist(), "profits": profits.tolist(), "pd_x": pdr["grid_values"][0].tolist(), "pd_y": pdr["average"][0].tolist()},
          open(HERE / "ch39_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}"); raise SystemExit(1 if fails else 0)
