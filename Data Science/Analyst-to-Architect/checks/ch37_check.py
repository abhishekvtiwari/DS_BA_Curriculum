"""Analyst to Architect · Chapter 37 · number check.
Recomputes the numbers quoted in Chapter 37's prose (hand calculations and model results) and writes
checks/ch37_results.json, which figures/make_figs37.py reads. Run from checks/: python3 ch37_check.py
Needs companion/accounts/accounts.csv (python3 companion/generate_riverstone_accounts.py).
Takes about 2 minutes on one CPU core. Riverstone Supplies is fictional; every name and number is invented."""
import json, math, pathlib, warnings
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, learning_curve, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

# ---- ceiling AUC from the generator's true probabilities (section 37.0) ----
src = (COMP / "generate_riverstone_accounts.py").read_text().replace("df.to_csv", "pass  # ").replace('print(f"', 'pass  # print(f"')
ns = {"__file__": str(COMP / "generate_riverstone_accounts.py")}
exec(src, ns)
acc = pd.read_csv(COMP / "accounts" / "accounts.csv"); acc["rep_id"] = acc["rep_id"].astype(str)
p_true = pd.Series(ns["p_churn"], index=acc.index)
ok("ceiling AUC, all", round(roc_auc_score(acc.churned_2025, p_true), 3), 0.858)
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2024", "avg_discount_pct", "late_payment_days",
        "complaints_2024", "categories_bought", "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]
rest, test = train_test_split(acc, test_size=0.2, random_state=37, stratify=acc.churned_2025)
tr, va = train_test_split(rest, test_size=0.25, random_state=37, stratify=rest.churned_2025)
ok("ceiling AUC, test", round(roc_auc_score(test.churned_2025, p_true[test.index]), 3), 0.858)
ok("churners", int(acc.churned_2025.sum()), 484); ok("valid churners", int(va.churned_2025.sum()), 97)
ok("train churners", int(tr.churned_2025.sum()), 290); ok("rest churners ~390", round(rest.churned_2025.sum(), -1), 390)
ok("late_payment_days blanks (all, train)", (int(acc.late_payment_days.isna().sum()), int(tr.late_payment_days.isna().sum())), (150, 97))
ok("first account (id, revenue_2023, revenue_2024)", (int(acc.account_id[0]), acc.revenue_2023[0], acc.revenue_2024[0]), (5001, 107200.0, 146400.0))
stayed = acc[acc.churned_2025 == 0]; ok("stayed", len(stayed), 4516)

# ---- section 37.1 hand arithmetic ----
ok("weighted sums", (round(0.2 + 11.0, 2), round(0.2 + 12.0 - 0.05 * 2, 2), round(0.2 + 10.5 - 0.05, 2)), (11.2, 12.1, 10.65))
ok("ln table", tuple(round(math.log(v), 2) for v in (1e4, 1e5, 1e6)), (9.21, 11.51, 13.82))
ok("ln step and 10k vs 10 lakh", (round(math.log(10), 2), round(math.log(1e6) - math.log(1e4), 1)), (2.3, 4.6))
ok("1.10^1.013", round(1.10 ** 1.013, 4), 1.1014)
ok("MAE example", round((10_000 + 30_000 + 0) / 3), 13333)
s2 = stayed.copy()
for c in ["revenue_2024", "units_2024", "orders_2024", "revenue_2025"]: s2["log_" + c] = np.log(s2[c])
rtr, rte = train_test_split(s2, test_size=0.25, random_state=37)
lr = LinearRegression().fit(rtr[["log_revenue_2024"]], rtr.log_revenue_2025)
ex = rte.iloc[0]; z = lr.intercept_ + lr.coef_[0] * math.log(ex.revenue_2024)
ok("ln 65500", round(math.log(65500), 4), 11.0898); ok("rounded coef calc", round(-0.140 + 1.013 * 11.0898, 4), 11.094)
ok("exact log pred", round(z, 5), 11.09065); ok("exp pred", round(math.exp(z)), 65555)
ok("retail factor", round(math.exp(-0.097), 3), 0.908)
ok("SD log revenue 2024 ~1.09", round(rtr.log_revenue_2024.std(), 2), 1.09); ok("1.099/1.09", round(1.099 / 1.09, 2), 1.01)

# ---- section 37.2 ridge / lasso by hand ----
x = np.array([[-1.5], [-0.5], [0.5], [1.5]]); y = np.array([-2.9, -1.2, 0.8, 3.3])
ok("sums", (round(float((x[:, 0] * y).sum()), 2), float((x ** 2).sum())), (10.3, 5.0))
ok("ridge hand", (round(10.3 / 5, 2), round(10.3 / 6, 3), round(10.3 / 10, 2)), (2.06, 1.717, 1.03))
ok("ridge sklearn", tuple(round(Ridge(alpha=a, fit_intercept=False).fit(x, y).coef_[0], 3) for a in (1, 5)), (1.717, 1.03))
ok("lasso hand", tuple(round(max(0, (2.575 - a) / 1.25), 2) for a in (0.5, 1, 3)), (1.66, 1.26, 0))
ok("lasso sklearn", tuple(round(Lasso(alpha=a, fit_intercept=False).fit(x, y).coef_[0], 2) for a in (0.5, 1, 3)), (1.66, 1.26, 0.0))

# ---- section 37.3 odds box, sigmoid, checkpoint A ----
ok("odds 10%", round(0.1 / 0.9, 3), 0.111); ok("log-odds", round(math.log(0.1 / 0.9), 3), -2.197)
o2 = 0.1 / 0.9 * 2.10; ok("odds x2.10", (round(o2, 3), round(o2 / (1 + o2), 3)), (0.233, 0.189))
ok("e^2.124", round(math.exp(2.124), 3), 8.365); ok("sigmoid", round(1 / (1 + math.exp(2.124)), 4), 0.1068)
ok("checkpoint A1", (round(1 + math.exp(1.2), 3), round(1 / (1 + math.exp(1.2)), 3)), (4.32, 0.231))
ok("checkpoint A2", (0.25 * 1.5, round(0.375 / 1.375, 3)), (0.375, 0.273))
ok("checkpoint A3", round(0.05 / (0.05 + 0.09), 3), 0.357)
ok("sd days since last order ~80", round(tr.days_since_last_order.std(), -1), 80.0)

# ---- section 37.4 k-NN by hand, exercise 5 ----
P = np.array([[0.2, 0.1], [0.5, 0.4], [1.8, 1.5], [2.0, 2.2], [1.6, 1.9]])
ok("knn distances", tuple(np.sqrt(((P - [1.7, 1.6]) ** 2).sum(1)).round(3)), (2.121, 1.697, 0.141, 0.671, 0.316))
Q = np.array([[1, 1], [2, 3], [4, 4], [3, 2], [5, 1]])
d5 = np.sqrt(((Q - [2, 1]) ** 2).sum(1)).round(3); ok("ex5 distances", tuple(d5), (1.0, 2.0, 3.606, 1.414, 3.0))
ok("ex5 nearest three", tuple(np.argsort(d5)[:3]), (0, 3, 1))

# ---- section 37.5 Naive Bayes ----
y = tr.churned_2025
lsr = (tr.late_payment_days > 25) & (tr.company_size == "Small") & (tr.segment == "Retail"); old = tr.days_since_last_order > 90
pc, ps = y.mean(), 1 - y.mean()
a1, a2 = lsr[y == 1].mean(), lsr[y == 0].mean(); b1, b2 = old[y == 1].mean(), old[y == 0].mean()
ok("NB likelihoods", (round(a1, 3), round(a2, 3), round(b1, 3), round(b2, 3)), (0.207, 0.027, 0.638, 0.159))
ok("NB 60/290", round(60 / 290, 3), 0.207)
churn_score, stay_score = pc * a1 * b1, ps * a2 * b2
ok("NB churn", round(churn_score, 5), 0.01276); ok("NB stay rounded", round(0.9033 * 0.027 * 0.159, 5), 0.00388)
ok("NB posterior exact", round(churn_score / (churn_score + stay_score), 3), 0.765); ok("NB posterior rounded", round(0.01276 / (0.01276 + 0.00388), 3), 0.767)
both = tr[lsr & old]; ok("both signals", (int(both.churned_2025.sum()), len(both)), (40, 50))
g = tr.groupby("churned_2025").days_since_last_order.agg(["mean", "std"]).round(0)
ok("GaussianNB days mean/sd (stayed, churned)", tuple(g.to_numpy().ravel()), (50.0, 67.0, 150.0, 122.0))
ok("balanced weight ratio", round(2710 / 290, 1), 9.3)

# ---- section 37.6 Gini ----
ok("gini warm-up", (0, 2 * 0.5 * 0.5, round(2 * 0.1 * 0.9, 2)), (0, 0.5, 0.18))
ok("hand Gini A", round(616 / 3000 * 2 * .3 * .7 + 2384 / 3000 * 2 * .044 * .956, 4), 0.1531)
ok("hand Gini B", round(387 / 3000 * 2 * .23 * .77 + 2613 / 3000 * 2 * .077 * .923, 4), 0.1695)
ok("root Gini", round(2 * pc * ps, 4), 0.1746)
ok("checkpoint B1", (round(2 * .1 * .9, 2), round(.25 * 2 * .3 * .7 + .75 * 2 * (1 / 30) * (29 / 30), 3)), (0.18, 0.153))

# ---- sections 37.7-37.8 toy accounts and boosting round 1 by hand ----
toy = tr.sample(8, random_state=321).sort_values("days_since_last_order")
ok("toy days", tuple(toy.days_since_last_order), (1.0, 10.0, 11.0, 25.0, 30.0, 34.0, 40.0, 197.0))
ok("toy churners", tuple(toy.churned_2025), (0, 0, 0, 1, 0, 0, 0, 1))
left = round(-0.75 / 7, 3); ok("round 1 left mean residual", left, -0.107)
p_left, p_right = 0.25 + 0.5 * (-0.75 / 7), 0.25 + 0.5 * 0.75
ok("round 1 predictions", (round(p_left, 3), p_right), (0.196, 0.625))
se1 = ((1 - p_right) ** 2 + (1 - p_left) ** 2 + 6 * p_left ** 2) / 8
ok("round 0 / round 1 squared error", ((2 * .75 ** 2 + 6 * .25 ** 2) / 8, round(se1, 3)), (0.1875, 0.127))
xs, ys = toy[["days_since_last_order"]].to_numpy(), toy.churned_2025.to_numpy().astype(float)
st = DecisionTreeRegressor(max_depth=1, random_state=37).fit(xs, ys - 0.25)
ok("round 1 stump split", float(st.tree_.threshold[0]), 118.5)
# exercise 7 and checkpoint B2
x7, y7 = np.array([[10.], [20.], [100.], [200.]]), np.array([0., 0., 0., 1.])
st7 = DecisionTreeRegressor(max_depth=1).fit(x7, y7 - 0.25); p7 = 0.25 + 0.5 * st7.predict(x7)
ok("ex7 split and predictions", (float(st7.tree_.threshold[0]), tuple(p7)), (150.0, (0.125, 0.125, 0.125, 0.625)))
ok("ex7 squared error", (np.mean((y7 - 0.25) ** 2), round(np.mean((y7 - p7) ** 2), 4)), (0.1875, 0.0469))
# exercise 6 (ridge)
ok("ex6 ridge", (17 / 10, round(17 / 12, 3), 17 / 20), (1.7, 1.417, 0.85))
# SVM margin example
ok("svm margin", ((40 + 120) / 2, (120 - 40) / 2, (60 + 120) / 2), (80.0, 40.0, 90.0))

# ---- figure data ----
R = {}
prep = lambda scale=True: ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), CATS),
    ("n", Pipeline([("f", SimpleImputer(strategy="median", add_indicator=True))] + ([("s", StandardScaler())] if scale else [])), NUMS)])
REG = ["log_revenue_2024", "log_units_2024", "log_orders_2024", "tenure_months", "avg_discount_pct", "late_payment_days",
       "complaints_2024", "categories_bought", "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]
regprep = lambda: ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore", drop="first"), CATS),
                  ("n", Pipeline([("f", SimpleImputer(strategy="median")), ("s", StandardScaler())]), REG)])
ols = Pipeline([("p", regprep()), ("m", LinearRegression())]).fit(rtr[CATS + REG], rtr.log_revenue_2025)
pl = ols.predict(rte[CATS + REG]); res = rte.log_revenue_2025.to_numpy() - pl
R["resid"] = [[round(float(a), 4), round(float(b), 4)] for a, b in zip(pl, res)]
R["lasso"] = []
for alpha in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
    m = Pipeline([("p", regprep()), ("m", Lasso(alpha=alpha))]).fit(rtr[CATS + REG], rtr.log_revenue_2025)
    R["lasso"].append((alpha, int((m[-1].coef_ != 0).sum()), r2_score(rte.log_revenue_2025, m.predict(rte[CATS + REG]))))
ok("lasso kept at 0.001/0.01/0.05/0.2", tuple(k for a, k, _ in R["lasso"] if a in (0.001, 0.01, 0.05, 0.2)), (14, 5, 2, 1))
R["depth"] = []
for d in [1, 2, 3, 4, 5, 6, 8, 10, 14, None]:
    t = Pipeline([("p", prep(False)), ("m", DecisionTreeClassifier(max_depth=d, random_state=37))]).fit(tr[CATS + NUMS], y)
    R["depth"].append((d if d else 30, roc_auc_score(y, t.predict_proba(tr[CATS + NUMS])[:, 1]),
                       roc_auc_score(va.churned_2025, t.predict_proba(va[CATS + NUMS])[:, 1])))
best = max(R["depth"], key=lambda r: r[2]); ok("best depth and valid AUC", (best[0], round(best[2], 3)), (3, 0.752))
folds = StratifiedKFold(5, shuffle=True, random_state=37)
cands = {"logistic": Pipeline([("p", prep()), ("m", LogisticRegression(max_iter=2000))]),
         "boosting": Pipeline([("p", prep(False)), ("m", HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37))])}
R["curves"] = {}
for k, pipe in cands.items():
    n, a, b = learning_curve(pipe, rest[CATS + NUMS], rest.churned_2025, cv=folds, scoring="roc_auc",
                             train_sizes=[0.1, 0.25, 0.5, 0.75, 1.0], shuffle=True, random_state=37)
    R["curves"][k] = [n.tolist(), a.mean(1).tolist(), b.mean(1).tolist()]
ok("LC logistic end", round(R["curves"]["logistic"][2][-1], 3), 0.807); ok("LC boost end", round(R["curves"]["boosting"][2][-1], 3), 0.836)
ok("tree none train/valid", (round(R["depth"][-1][1], 3), round(R["depth"][-1][2], 3)), (1.0, 0.557))
(HERE / "ch37_results.json").write_text(json.dumps(R))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
