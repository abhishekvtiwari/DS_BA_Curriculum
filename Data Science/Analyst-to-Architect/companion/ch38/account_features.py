"""
Analyst to Architect · Chapter 38 · account_features.py
Loads Riverstone's accounts and builds the eight standardized features used for clustering.

Use:     from account_features import load_accounts, FEATURES
         accounts, X, Z = load_accounts()   # raw table, feature table, standardized array
Reads:   ../accounts/accounts.csv (build it with ../generate_riverstone_accounts.py)
Tested:  Python 3.12.3, pandas 3.0.2, scikit-learn 1.8.0 (18 September 2026)
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

DATA = pathlib.Path(__file__).resolve().parent.parent / "accounts" / "accounts.csv"
FEATURES = ["revenue_2024", "orders_2024", "tenure_months", "avg_discount_pct",
            "late_payment_days", "complaints_2024", "categories_bought", "days_since_last_order"]


def load_accounts():
    accounts = pd.read_csv(DATA)
    X = accounts[FEATURES].copy()
    X["revenue_2024"] = np.log(X["revenue_2024"])                      # money is skewed (Chapter 35)
    X["late_payment_days"] = X["late_payment_days"].fillna(X["late_payment_days"].median())
    Z = StandardScaler().fit_transform(X)
    return accounts, X, Z
