"""
Analyst to Architect · Chapter 37 · lead_data.py
Rebuilds Chapter 36's lead-scoring table in one call, so Chapter 37 can start from it.

Use:     from lead_data import load_leads, make_model, LEAD_CATS, LEAD_NUMS
         train, valid, test = load_leads()           # run from companion/ch37/
Reads:   ../crm/leads.csv and ../crm/activities.csv (build them with ../generate_riverstone_crm.py)
Tested:  Python 3.12.3, pandas 3.0.2, scikit-learn 1.8.0 (17 September 2026)

Every step is explained in Chapter 36 (sections 36.2, 36.5, 36.6, 36.8).
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CRM = pathlib.Path(__file__).resolve().parent.parent / "crm"
LEAD_CATS = ["source", "segment", "city_clean", "company_size", "product_interest"]
LEAD_NUMS = ["log_quantity", "website_visits", "free_email", "text_strong", "text_weak",
             "inside_desk", "activities_24h", "responded_24h"]
CITY_FIX = {"bombay": "Mumbai", "mumbai.": "Mumbai", "bangalore": "Bengaluru", "b'lore": "Bengaluru",
            "new delhi": "Delhi", "delhi ncr": "Delhi", "poona": "Pune", "madras": "Chennai",
            "calcutta": "Kolkata", "panaji": "Goa"}


def make_model(categorical, numeric, model=None):
    """Chapter 36's pipeline: fill + one-hot for categories, fill + indicator + scale for numbers."""
    prepare = ColumnTransformer([
        ("cat", Pipeline([("fill", SimpleImputer(strategy="constant", fill_value="Missing")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
        ("num", Pipeline([("fill", SimpleImputer(strategy="median", add_indicator=True)),
                          ("scale", StandardScaler())]), numeric),
    ])
    return Pipeline([("prepare", prepare), ("model", model or LogisticRegression(max_iter=1000))])


def load_leads():
    leads = pd.read_csv(CRM / "leads.csv", parse_dates=["created_at"])
    leads["email_norm"] = leads["email"].str.lower().str.strip()
    leads = leads.sort_values("created_at")
    gap = leads.groupby("email_norm")["created_at"].diff()
    leads = leads[~(gap.notna() & (gap <= pd.Timedelta(days=2)))].copy()
    leads = leads[leads["created_at"] <= pd.Timestamp("2025-12-31 23:59") - pd.Timedelta(days=90)].copy()
    leads["won"] = (leads["status"] == "Won").astype(int)
    city = leads["city"].str.strip().str.lower()
    leads["city_clean"] = city.map(CITY_FIX).fillna(city.str.title())
    text = leads["enquiry_text"].str.lower()
    leads["text_strong"] = text.str.contains("bulk|tender|urgent|monthly|new outlet").astype(int)
    leads["text_weak"] = text.str.contains("price list|sample|checking rates|catalogue|price please").astype(int)
    leads["free_email"] = leads["email_norm"].str.endswith("@gmail.com").astype(int)
    leads["log_quantity"] = np.log1p(leads["est_quantity"].where(leads["est_quantity"] <= 50_000))
    leads["inside_desk"] = (leads["owner_id"] == 9).astype(int)
    leads["responded_24h"] = (leads["first_response_hours"] <= 24).astype(int)
    acts = pd.read_csv(CRM / "activities.csv", parse_dates=["activity_at", "logged_at"])
    deadline = leads.set_index("lead_id")["created_at"] + pd.Timedelta(hours=24)
    visible = acts[acts["logged_at"] <= acts["lead_id"].map(deadline)]
    leads["activities_24h"] = leads["lead_id"].map(visible.groupby("lead_id").size()).fillna(0)
    train = leads[leads["created_at"] < "2025-01-01"]
    valid = leads[(leads["created_at"] >= "2025-01-01") & (leads["created_at"] < "2025-07-01")]
    test = leads[leads["created_at"] >= "2025-07-01"]
    return train, valid, test
