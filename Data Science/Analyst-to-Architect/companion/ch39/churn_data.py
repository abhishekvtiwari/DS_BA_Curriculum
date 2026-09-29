"""
Analyst to Architect · Chapter 39 · churn_data.py
Rebuilds Chapter 37's churn split and its hand-set gradient-boosting model, so Chapter 39 can start from them.

Use:     from churn_data import CHURN_CATS, CHURN_NUMS, load_accounts, make_churn_model
         rest, test_acc = load_accounts()           # run from companion/ch39/
         churn_model = make_churn_model().fit(rest[CHURN_CATS + CHURN_NUMS], rest["churned_2025"])
Reads:   ../accounts/accounts.csv (build it with ../generate_riverstone_accounts.py)
Tested:  Python 3.11.15, pandas 3.0.6, scikit-learn 1.9.1 (29 September 2026)

The split is Chapter 37's (section 37.0): 1,000 accounts held out, stratified by churn, seed 37.
The model is Chapter 37's "HistGradientBoosting tuned" (section 37.8), with the columns left unscaled.
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ACCOUNTS = pathlib.Path(__file__).resolve().parent.parent / "accounts" / "accounts.csv"
CHURN_CATS = ["segment", "city_tier", "company_size", "rep_id"]
CHURN_NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2024", "avg_discount_pct",
              "late_payment_days", "complaints_2024", "categories_bought", "days_since_last_order",
              "website_logins_2024", "catalog_downloads_2024"]


def load_accounts():
    """Chapter 37's accounts: 4,000 to learn from (`rest`) and 1,000 held out (`test_acc`)."""
    accounts = pd.read_csv(ACCOUNTS)
    accounts["rep_id"] = accounts["rep_id"].astype(str)      # a rep is a label, not a quantity
    rest, test_acc = train_test_split(
        accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"]
    )
    return rest, test_acc


def make_churn_model():
    """One-hot the categories, fill numbers with the median (plus was-missing columns), then boosting."""
    prepare = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CHURN_CATS),
        ("num", SimpleImputer(strategy="median", add_indicator=True), CHURN_NUMS),
    ])
    model = HistGradientBoostingClassifier(
        learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37
    )
    return Pipeline([("prepare", prepare), ("model", model)])
