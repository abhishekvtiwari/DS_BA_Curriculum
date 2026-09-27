"""Analyst to Architect · Chapter 37 · number check.
Recomputes the numbers quoted in Chapter 37's prose (hand calculations and model results) and writes
checks/ch37_results.json, which figures/make_figs37.py reads. Run from checks/: python3 ch37_check.py
Takes about 2 minutes on one CPU core. Riverstone Supplies is fictional; every name and number is invented."""
import json, math, pathlib, warnings
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, learning_curve, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

# ceiling AUC from the generator's true probabilities
src = (COMP / "generate_riverstone_accounts.py").read_text().replace("df.to_csv", "pass  # ")
ns = {"__file__": str(COMP / "generate_riverstone_accounts.py")}
exec(src, ns)
ok("ceiling AUC", round(roc_auc_score(ns["churned_2025"], ns["p_churn"]), 3), 0.858)

acc = pd.read_csv(COMP / "accounts" / "accounts.csv"); acc["rep_id"] = acc["rep_id"].astype(str)
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2024", "avg_discount_pct", "late_payment_days",
        "complaints_2024", "categories_bought", "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]
rest, test = train_test_split(acc, test_size=0.2, random_state=37, stratify=acc.churned_2025)
tr, va = train_test_split(rest, test_size=0.25, random_state=37, stratify=rest.churned_2025)
ok("churners", int(acc.churned_2025.sum()), 484); ok("valid churners", int(va.churned_2025.sum()), 97)
ok("train churners", int(tr.churned_2025.sum()), 290); ok("rest churners ~390", round(rest.churned_2025.sum(), -1), 390)
stayed = acc[acc.churned_2025 == 0]; ok("stayed", len(stayed), 4516)

# sigmoid, odds, NB, Gini hand arithmetic
ok("e^2.124", round(math.exp(2.124), 3), 8.365); ok("sigmoid", round(1 / (1 + math.exp(2.124)), 4), 0.1068)
ok("ex1", round(1 / (1 + math.exp(-0.8)), 3), 0.69); ok("ex2 prob", round(0.1 / 0.9 * 1.45 / (1 + 0.1 / 0.9 * 1.45), 3), 0.139)
ok("ex3 entropy", round(-(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75)), 3), 0.811)
y = tr.churned_2025
lsr = (tr.late_payment_days > 25) & (tr.company_size == "Small") & (tr.segment == "Retail"); old = tr.days_since_last_order > 90
pc, ps = y.mean(), 1 - y.mean()
a1, a2 = lsr[y == 1].mean(), lsr[y == 0].mean(); b1, b2 = old[y == 1].mean(), old[y == 0].mean()
ok("NB likelihoods", (round(a1, 3), round(a2, 3), round(b1, 3), round(b2, 3)), (0.207, 0.027, 0.638, 0.159))
churn_score, stay_score = pc * a1 * b1, ps * a2 * b2
ok("NB churn", round(churn_score, 5), 0.01276); ok("NB stay exact", round(stay_score, 5), 0.00392); ok("NB stay rounded", round(0.9033 * 0.027 * 0.159, 5), 0.00388)
ok("NB posterior exact", round(churn_score / (churn_score + stay_score), 3), 0.765); ok("NB posterior rounded", round(0.01276 / (0.01276 + 0.00388), 3), 0.767)
both = tr[lsr & old]; ok("both signals", (int(both.churned_2025.sum()), len(both)), (40, 50))
ok("hand Gini A", round(616 / 3000 * 2 * .3 * .7 + 2384 / 3000 * 2 * .044 * .956, 4), 0.1531)
ok("hand Gini B", round(387 / 3000 * 2 * .23 * .77 + 2613 / 3000 * 2 * .077 * .923, 4), 0.1695)
ok("root Gini", round(2 * pc * ps, 4), 0.1746)
ok("sd days since last order ~80", round(tr.days_since_last_order.std(), -1), 80.0)

# regression example hand check
s2 = stayed.copy(); s2["log_revenue_2024"] = np.log(s2.revenue_2024); s2["log_revenue_2025"] = np.log(s2.revenue_2025)
rtr, rte = train_test_split(s2, test_size=0.25, random_state=37)
lr = LinearRegression().fit(rtr[["log_revenue_2024"]], rtr.log_revenue_2025)
ex = rte.iloc[0]; z = lr.intercept_ + lr.coef_[0] * math.log(ex.revenue_2024)
ok("ln 65500", round(math.log(65500), 4), 11.0898); ok("rounded coef calc", round(-0.140 + 1.013 * 11.0898, 4), 11.094)
ok("exact log pred", round(z, 4), 11.0906); ok("exp pred", round(math.exp(z)), 65555)
ok("retail factor", round(math.exp(-0.097), 3), 0.908)

prep = lambda scale=True: ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), CATS),
    ("n", Pipeline([("f", SimpleImputer(strategy="median", add_indicator=True))] + ([("s", StandardScaler())] if scale else [])), NUMS)])
R = {}
REG = ["log_revenue_2024", "log_units_2024", "log_orders_2024", "tenure_months", "avg_discount_pct", "late_payment_days",
       "complaints_2024", "categories_bought", "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]
for c in ["units_2024", "orders_2024"]: rtr["log_" + c] = np.log(rtr[c]); rte["log_" + c] = np.log(rte[c])
R["lasso"] = []
for alpha in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
    m = Pipeline([("p", ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore", drop="first"), CATS),
                  ("n", Pipeline([("f", SimpleImputer(strategy="median")), ("s", StandardScaler())]), REG)])), ("m", Lasso(alpha=alpha))])
    m.fit(rtr[CATS + REG], rtr.log_revenue_2025)
    R["lasso"].append((alpha, int((m[-1].coef_ != 0).sum()), r2_score(rte.log_revenue_2025, m.predict(rte[CATS + REG]))))
R["depth"] = []
for d in [1, 2, 3, 4, 5, 6, 8, 10, 14, None]:
    t = Pipeline([("p", prep(False)), ("m", DecisionTreeClassifier(max_depth=d, random_state=37))]).fit(tr[CATS + NUMS], y)
    R["depth"].append((d if d else 30, roc_auc_score(y, t.predict_proba(tr[CATS + NUMS])[:, 1]),
                       roc_auc_score(va.churned_2025, t.predict_proba(va[CATS + NUMS])[:, 1])))
folds = StratifiedKFold(5, shuffle=True, random_state=37)
cands = {"logistic": Pipeline([("p", prep()), ("m", LogisticRegression(max_iter=2000))]),
         "boosting": Pipeline([("p", prep(False)), ("m", HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37))])}
R["curves"] = {}
for k, pipe in cands.items():
    n, a, b = learning_curve(pipe, rest[CATS + NUMS], rest.churned_2025, cv=folds, scoring="roc_auc",
                             train_sizes=[0.1, 0.25, 0.5, 0.75, 1.0], shuffle=True, random_state=37)
    R["curves"][k] = [n.tolist(), a.mean(1).tolist(), b.mean(1).tolist()]
ok("LC logistic end", round(R["curves"]["logistic"][2][-1], 3), 0.807); ok("LC boost end", round(R["curves"]["boosting"][2][-1], 3), 0.836)
ok("tree depth4 valid", round(R["depth"][3][2], 3), 0.748); ok("tree none train/valid", (round(R["depth"][-1][1], 3), round(R["depth"][-1][2], 3)), (1.0, 0.557))
(HERE / "ch37_results.json").write_text(json.dumps(R))
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
