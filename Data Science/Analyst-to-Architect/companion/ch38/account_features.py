"""
Analyst to Architect · Chapter 38 · account_features.py
Loads Riverstone's accounts and builds the seven standardized features Chapter 38 clusters on
(section 38.0), so later work can start from the same prepared data in one call.

Use:     from account_features import load_accounts, FEATURES
         accounts, X = load_accounts()   # the accounts table (with log_revenue added), standardized array
Reads:   ../accounts/accounts.csv (build it with ../generate_riverstone_accounts.py)
Tested:  Python 3.11.15, pandas 3.0.6, scikit-learn 1.9.1 (29 September 2026)
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

DATA = pathlib.Path(__file__).resolve().parent.parent / "accounts" / "accounts.csv"
FEATURES = ["log_revenue", "orders_2024", "categories_bought", "avg_discount_pct",
            "late_payment_days", "days_since_last_order", "tenure_months"]


def load_accounts():
    accounts = pd.read_csv(DATA)
    accounts["log_revenue"] = np.log(accounts["revenue_2024"])            # revenue is skewed (section 38.0)
    accounts["late_payment_days"] = accounts["late_payment_days"].fillna(
        accounts["late_payment_days"].median())                           # 150 blanks: no payment history
    X = StandardScaler().fit_transform(accounts[FEATURES])
    return accounts, X
