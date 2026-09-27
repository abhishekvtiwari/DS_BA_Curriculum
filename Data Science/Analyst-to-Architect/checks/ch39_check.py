"""Analyst to Architect · Chapter 39 · number check.
Recomputes the numbers quoted in Chapter 39's prose and writes checks/ch39_results.json for the figures.
Run from checks/: python3 ch39_check.py   (about 1 minute). Riverstone Supplies is fictional."""
import json, pathlib, sys, warnings
import numpy as np, pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import partial_dependence
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix, precision_recall_curve,
                             roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "companion" / "ch39"))
from lead_data import LEAD_CATS, LEAD_NUMS, load_leads, make_model
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

train, valid, test = load_leads(); X = LEAD_CATS + LEAD_NUMS
model = make_model(LEAD_CATS, LEAD_NUMS).fit(train[X], train["won"])
p = model.predict_proba(valid[X])[:, 1]; y = valid["won"].to_numpy()
ok("valid", (len(valid), int(y.sum())), (2225, 146))
tn, fp, fn, tp = confusion_matrix(y, (p >= 0.5).astype(int)).ravel(); ok("0.5 matrix", (tp, fp, fn, tn), (4, 3, 142, 2076))
ok("all-lost accuracy", round(2079 / 2225, 3), 0.934); ok("0.5 accuracy", round((4 + 2076) / 2225, 3), 0.935)
tn, fp, fn, tp = confusion_matrix(y, (p >= 0.1).astype(int)).ravel(); ok("0.1 matrix", (tp, fp, fn, tn), (100, 386, 46, 1693))
ok("precision", round(100 / 486, 3), 0.206); ok("recall", round(100 / 146, 3), 0.685); ok("F1", round(2 * .206 * .685 / .891, 3), 0.317)
ok("specificity", round(1693 / 2079, 3), 0.814); ok("FPR", round(386 / 2079, 3), 0.186)
ok("ROC-AUC", round(roc_auc_score(y, p), 3), 0.823); ok("PR-AUC", round(average_precision_score(y, p), 3), 0.302)
ok("PR ratio", round(0.302 / y.mean(), 1), 4.6)
order = np.argsort(-p); ok("top50", int(y[order[:50]].sum()), 22); ok("top400 share", f"{y[order[:400]].sum() / y.sum():.0%}", "63%")
ok("400 share of leads", round(400 / 2225 * 100), 18)
# calibration
to_dense = FunctionTransformer(lambda M: M.toarray() if hasattr(M, "toarray") else M)
nb = make_model(LEAD_CATS, LEAD_NUMS, GaussianNB()); nb.steps.insert(1, ("dense", to_dense))
p_nb = nb.fit(train[X], train["won"]).predict_proba(valid[X])[:, 1]
p_gb = make_model(LEAD_CATS, LEAD_NUMS, HistGradientBoostingClassifier(random_state=39)).fit(train[X], train["won"]).predict_proba(valid[X])[:, 1]
ok("NB mean pred", round(p_nb.mean(), 2), 0.18); ok("NB ROC", round(roc_auc_score(y, p_nb), 3), 0.806)
fpos, mpred = calibration_curve(y, p_nb, n_bins=10, strategy="quantile"); ok("NB top decile", (round(mpred[-1], 2), round(fpos[-1], 2)), (0.94, 0.27))
ok("base-rate Brier", round(brier_score_loss(y, np.full(len(y), y.mean())), 3), 0.061)
# costs
accounts = pd.read_csv(HERE.parent / "companion" / "accounts" / "accounts.csv")
new = accounts[accounts.tenure_months <= 12]; WIN = new.revenue_2024.median() * 0.15
ok("first-year median", new.revenue_2024.median(), 201700.0); ok("win value", round(WIN), 30255); ok("break-even", round(1500 / WIN, 4), 0.0496)
def profit(t, pp=p, yy=y):
    c = pp >= t; return WIN * yy[c].sum() - 1500 * c.sum(), int(c.sum()), int(yy[c].sum())
grid = np.linspace(0, 0.5, 501); profits = np.array([profit(t)[0] for t in grid])
ok("best threshold", round(grid[profits.argmax()], 3), 0.077); ok("best profit", round(profits.max()), 2448060)
ok("worked at best", profit(0.077)[1], 627); ok("all leads profit", round(profit(0)[0]), 1079730)
ok("within 6%", (round(profit(0.05)[0] / profits.max(), 2), round(profit(0.10)[0] / profits.max(), 2)), (0.94, 0.94))
top = order[:504]; t_cap = p[top].min(); pr, w, wi = profit(t_cap)
ok("capacity", (round(t_cap, 3), w, wi, round(pr)), (0.097, 504, 102, 2330010))
rule = valid.source.isin(["Referral", "Trade fair", "Partner"]).to_numpy()
rp = WIN * y[rule].sum() - 1500 * rule.sum(); ok("rule", (int(rule.sum()), int(y[rule].sum()), round(rp)), (531, 84, 1744920))
ok("model worth ~590,000", round((pr - rp), -4), 590000.0)
# fairness
called = p >= 0.05; desk = valid.inside_desk.to_numpy() == 1
ok("recall desk/reps", (round(called[desk & (y == 1)].mean(), 2), round(called[~desk & (y == 1)].mean(), 2)), (0.57, 0.91))
ok("share called", (round(called[~desk].mean(), 2), round(called[desk].mean(), 2)), (0.55, 0.21))
# figures data
fpr, tpr, _ = roc_curve(y, p); prec, rec, _ = precision_recall_curve(y, p)
curves = {n: [list(map(float, a)) for a in calibration_curve(y, q, n_bins=10, strategy="quantile")] for n, q in
          [("logistic regression", p), ("Naive Bayes", p_nb), ("gradient boosting", p_gb)]}
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2024", "avg_discount_pct", "late_payment_days",
        "complaints_2024", "categories_bought", "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]
accounts["rep_id"] = accounts.rep_id.astype(str)
a_tr, a_te = train_test_split(accounts, test_size=0.2, random_state=37, stratify=accounts.churned_2025)
churn = Pipeline([("prepare", ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATS),
                  ("num", SimpleImputer(strategy="median", add_indicator=True), NUMS)])),
                  ("model", HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37))])
churn.fit(a_tr[CATS + NUMS], a_tr.churned_2025)
names = list(churn.named_steps["prepare"].get_feature_names_out()); Xc = churn.named_steps["prepare"].transform(a_te[CATS + NUMS])
pdr = partial_dependence(churn.named_steps["model"], Xc, features=[names.index("num__days_since_last_order")],
                         grid_resolution=40, kind="average", method="brute", response_method="predict_proba")
json.dump({"fpr": fpr.tolist(), "tpr": tpr.tolist(), "prec": prec.tolist(), "rec": rec.tolist(), "calib": curves,
           "grid": grid.tolist(), "profits": profits.tolist(), "pd_x": pdr["grid_values"][0].tolist(), "pd_y": pdr["average"][0].tolist()},
          open(HERE / "ch39_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}"); raise SystemExit(1 if fails else 0)
