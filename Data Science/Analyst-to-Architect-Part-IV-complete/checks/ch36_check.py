"""Analyst to Architect · Chapter 36 · number check.
Rebuilds the chapter's lead-scoring data and models from companion/crm/ and checks every number quoted in the prose.
Run from checks/: python3 ch36_check.py  (exit code 0 = all checks pass). figures/make_figs36.py imports results().
Riverstone Supplies is fictional; every name and number is invented."""
import pathlib, warnings, numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, TargetEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore")
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "crm"

def make_model(cat, num, extra=None):
    parts = [("cat", Pipeline([("fill", SimpleImputer(strategy="constant", fill_value="Missing")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat)]
    if extra: parts.append(extra)
    parts.append(("num", Pipeline([("fill", SimpleImputer(strategy="median", add_indicator=True)), ("scale", StandardScaler())]), num))
    return Pipeline([("prepare", ColumnTransformer(parts)), ("model", LogisticRegression(max_iter=1000))])

def results():
    R = {}
    raw = pd.read_csv(D / "leads.csv", parse_dates=["created_at"]); R["rows"] = len(raw); R["open"] = int((raw.status == "Open").sum())
    R["monthly"] = (raw.groupby(raw.created_at.dt.year).size() / 12).round(0).to_dict()
    q4 = raw[raw.created_at >= "2025-10-01"]; R["q4_closed_share"] = (q4.status != "Open").mean()
    L = raw.copy(); L["email_norm"] = L.email.str.lower().str.strip(); L = L.sort_values("created_at")
    gap = L.groupby("email_norm").created_at.diff(); dup = gap.notna() & (gap <= pd.Timedelta(days=2)); R["dups"] = int(dup.sum())
    L = L[~dup]; R["real"] = len(L)
    L = L[L.created_at <= pd.Timestamp("2025-12-31 23:59") - pd.Timedelta(days=90)].copy(); L["won"] = (L.status == "Won").astype(int)
    R["mature"] = len(L); R["wins"] = int(L.won.sum())
    fix = {"bombay": "Mumbai", "mumbai.": "Mumbai", "bangalore": "Bengaluru", "b'lore": "Bengaluru", "new delhi": "Delhi", "delhi ncr": "Delhi",
           "poona": "Pune", "madras": "Chennai", "calcutta": "Kolkata", "panaji": "Goa"}
    cl = L.city.str.strip().str.lower(); L["city_clean"] = cl.map(fix).fillna(cl.str.title())
    t = L.enquiry_text.str.lower()
    L["text_strong"] = t.str.contains("bulk|tender|urgent|monthly|new outlet").astype(int)
    L["text_weak"] = t.str.contains("price list|sample|checking rates|catalogue|price please").astype(int)
    L["free_email"] = L.email_norm.str.endswith("@gmail.com").astype(int)
    L["log_quantity"] = np.log1p(L.est_quantity.where(L.est_quantity <= 50_000))
    L["inside_desk"] = (L.owner_id == 9).astype(int); L["responded_24h"] = (L.first_response_hours <= 24).astype(int)
    L["has_quote"] = L.quote_sent_date.notna().astype(int)
    A = pd.read_csv(D / "activities.csv", parse_dates=["activity_at", "logged_at"])
    dl = L.set_index("lead_id").created_at + pd.Timedelta(hours=24)
    L["activities_24h"] = L.lead_id.map(A[A.logged_at <= A.lead_id.map(dl)].groupby("lead_id").size()).fillna(0)
    L["company_rate_wrong"] = L.company_name.map(L.groupby("company_name").won.mean())
    tr = L[L.created_at < "2025-01-01"]; va = L[(L.created_at >= "2025-01-01") & (L.created_at < "2025-07-01")]; te = L[L.created_at >= "2025-07-01"]
    R.update(n_train=len(tr), n_valid=len(va), n_test=len(te), r_train=tr.won.mean(), r_valid=va.won.mean(), r_test=te.won.mean())
    cats = ["source", "segment", "city_clean", "company_size", "product_interest"]
    nums = ["log_quantity", "website_visits", "free_email", "text_strong", "text_weak", "inside_desk", "activities_24h", "responded_24h"]
    def sc(c, n, a=None, b=None, extra=None):
        a = tr if a is None else a; b = va if b is None else b
        cols = c + n + ([extra[2][0]] if extra else [])
        m = make_model(c, n, extra).fit(a[cols], a.won); p = m.predict_proba(b[cols])[:, 1]
        return roc_auc_score(b.won, p), log_loss(b.won, p), p
    R["honest"] = sc(cats, nums)[:2]
    for leak in ["has_quote", "days_in_pipeline", "first_response_hours"]: R[leak] = sc(cats, nums + [leak])[:2]
    R["te_wrong"] = sc(cats, nums + ["company_rate_wrong"])[:2]
    R["te_right"] = sc(cats, nums, extra=("company", TargetEncoder(random_state=36), ["company_name"]))[:2]
    R["rule_valid"] = roc_auc_score(va.won, va.source.isin(["Referral", "Trade fair", "Partner"]))
    R["base_ll_valid"] = log_loss(va.won, np.full(len(va), tr.won.mean()))
    R["mean_pred_valid"] = sc(cats, nums)[2].mean()
    ft = pd.concat([tr, va]); au, ll, p = sc(cats, nums, ft, te); R["test"] = (au, ll)
    R["rule_test"] = roc_auc_score(te.won, te.source.isin(["Referral", "Trade fair", "Partner"])); R["base_ll_test"] = log_loss(te.won, np.full(len(te), ft.won.mean()))
    bt = L[L.created_at < "2025-07-01"]; rt, rv = train_test_split(bt, test_size=len(va), random_state=36, stratify=bt.won)
    R["random"] = sc(cats, nums, rt, rv)[:2]
    q = L.est_quantity; R["qty_missing_win"] = L.loc[q.isna(), "won"].mean(); R["qty_given_win"] = L.loc[q.notna(), "won"].mean()
    R["mkt_share"] = (L.groupby(L.created_at.dt.year).source.apply(lambda s: (s == "Marketplace").mean()) * 100).round(1).to_dict()
    R["mkt_win"] = (L[L.source == "Marketplace"].groupby(L.created_at.dt.year).won.mean() * 100).round(2).to_dict()
    R["late_log_share"] = ((A.logged_at - A.activity_at) > pd.Timedelta(hours=12)).mean()
    return R

if __name__ == "__main__":
    R = results(); fails = 0
    def ok(label, got, want):
        global fails
        good = got == want
        fails += not good; print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")
    ok("rows", R["rows"], 12294); ok("open", R["open"], 1065); ok("dups", R["dups"], 271); ok("real", R["real"], 12023)
    ok("mature", R["mature"], 10701); ok("wins", R["wins"], 826); ok("base rate", round(R["wins"] / R["mature"] * 100, 1), 7.7)
    ok("monthly 2023~290", round(R["monthly"][2023], -1), 290.0); ok("monthly 2025~400", round(R["monthly"][2025], -2), 400.0)
    ok("Q4 closed < quarter", R["q4_closed_share"] < 0.25, True)
    ok("sizes", (R["n_train"], R["n_valid"], R["n_test"]), (7291, 2225, 1185))
    ok("rates", (round(R["r_train"] * 100, 2), round(R["r_valid"] * 100, 2), round(R["r_test"] * 100, 2)), (7.9, 6.56, 8.78))
    ok("mkt share", R["mkt_share"], {2023: 30.1, 2024: 34.9, 2025: 44.5}); ok("mkt win", R["mkt_win"], {2023: 2.65, 2024: 3.23, 2025: 1.52})
    r3 = lambda t: (round(t[0], 3), round(t[1], 4))
    ok("honest", r3(R["honest"]), (0.823, 0.1948)); ok("has_quote", round(R["has_quote"][0], 3), 0.978)
    ok("days", round(R["days_in_pipeline"][0], 3), 0.875); ok("resp", round(R["first_response_hours"][0], 3), 0.831)
    ok("te wrong", round(R["te_wrong"][0], 3), 0.845); ok("te right", round(R["te_right"][0], 3), 0.823)
    ok("rule valid", round(R["rule_valid"], 3), 0.68); ok("base ll valid", round(R["base_ll_valid"], 4), 0.2435)
    ok("mean pred", round(R["mean_pred_valid"] * 100, 2), 6.9); ok("test", r3(R["test"]), (0.838, 0.2369))
    ok("rule test", round(R["rule_test"], 3), 0.727); ok("base ll test", round(R["base_ll_test"], 4), 0.2983)
    ok("random", r3(R["random"]), (0.791, 0.2269)); ok("qty missing", (round(R["qty_missing_win"] * 100, 2), round(R["qty_given_win"] * 100, 2)), (5.71, 8.06))
    ok("late logging ~1 in 10", round(R["late_log_share"], 1), 0.1); ok("wins in training ~580", round(R["n_train"] * R["r_train"], -1), 580.0)
    ok("has_quote jump", round(R["has_quote"][0] - R["honest"][0], 3), 0.155)
    print("All checks passed." if not fails else f"FAILED: {fails}"); raise SystemExit(1 if fails else 0)
