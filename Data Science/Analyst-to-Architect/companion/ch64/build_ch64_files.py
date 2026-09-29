"""
Analyst to Architect, Chapter 64: Security, Privacy, Governance & Responsible AI
build_ch64_files.py builds the practice files for section 64.7's fairness audit.

What it makes (run from this folder:  python build_ch64_files.py):
  models/lead_model_standin.joblib   the lead-scoring model, as a bundle {"model": ..., "metadata": ...}
                                (the same shape as Chapter 56's model bundle)
  leads_scored_2025.csv         1,830 leads from 2025, each with the score the model gave it
  lead-model-card.md            the model card for that model (section 64.8), with real numbers

The story. Part 4 (Chapters 35 to 39) built a lead-scoring model on Riverstone's CRM extract, and
Chapter 51 synced a simple rule-based score into the CRM. This file is a simplified stand-in for
the Part 4 model: three inputs (company size band, days since signup, industry), a logistic
regression, and a score that is the predicted chance of winning the lead, in percent. The model
never sees the region. Region matters only through company size: the West (Mumbai HO) and South
(Bengaluru) books hold more large accounts than the East (Kolkata). That is the pattern section
64.7's audit has to find. Riverstone Supplies is fictional; every lead, number and name is invented.

Seed 202401 for every random draw, so every run gives the same files.
Needs pandas, numpy, scikit-learn and joblib (all installed by Part 4).
"""
import pathlib

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

HERE = pathlib.Path(__file__).resolve().parent
rng = np.random.default_rng(202401)

# region -> (leads in 2024, leads in 2025, mean company_size_band); bands: 1 = 1-10 employees,
# 2 = 11-50, 3 = 51-200, 4 = 201-500, 5 = more than 500
REGIONS = {
    "West":  (800, 620, 3.1),
    "South": (700, 540, 2.9),
    "North": (530, 410, 2.5),
    "East":  (340, 260, 1.9),
}
FEATURES = ["company_size_band", "days_since_signup", "industry"]


def make_leads(n_col):
    """Draw leads region by region; region shifts company size and nothing else."""
    parts = []
    for region, sizes in REGIONS.items():
        n, mean_size = sizes[n_col], sizes[2]
        parts.append(pd.DataFrame({
            "region": region,
            "company_size_band": np.clip(np.round(rng.normal(mean_size, 1.0, n)), 1, 5).astype(int),
            "days_since_signup": rng.integers(1, 365, n),
            "industry": rng.choice(["Retail", "Hospitality", "Wholesale"], n, p=[0.5, 0.25, 0.25]),
        }))
    return pd.concat(parts, ignore_index=True)


# 1. History: 2024 leads and whether each was won. The chance of winning rises with company
#    size and falls with the days since signup; region and industry play no part.
hist = make_leads(0)
logit = -2.4 + 0.75 * hist["company_size_band"] - 2.0 * hist["days_since_signup"] / 365
hist["won"] = (rng.random(len(hist)) < 1 / (1 + np.exp(-logit))).astype(int)

# 2. The model: one-hot industry, pass the two numbers through, logistic regression.
model = Pipeline([
    ("prep", ColumnTransformer([("industry", OneHotEncoder(handle_unknown="ignore"), ["industry"])],
                               remainder="passthrough")),
    ("clf", LogisticRegression(max_iter=1000)),
])
train = hist.sample(frac=0.75, random_state=64)
test = hist.drop(train.index)
model.fit(train[FEATURES], train["won"])
auc = roc_auc_score(test["won"], model.predict_proba(test[FEATURES])[:, 1])

# 3. Score the 2025 leads: the score is the predicted chance of winning, in percent.
leads = make_leads(1).sample(frac=1, random_state=64).reset_index(drop=True)
leads.insert(0, "lead_id", range(1, len(leads) + 1))
leads["lead_score"] = np.round(model.predict_proba(leads[FEATURES])[:, 1] * 100).astype(int)
leads.to_csv(HERE / "leads_scored_2025.csv", index=False)

# 4. Save the model with its metadata, the way Chapter 56 saves the defect model.
metadata = {
    "name": "lead_score", "version": "stand-in", "trained_on": "2024 leads, 75% sample",
    "features": FEATURES, "target": "won (1 = lead became a customer)",
    "test_auc": round(auc, 3), "owner": "Anita Rao (sales)", "built_by": "Meera Iyer (analytics)",
}
(HERE / "models").mkdir(exist_ok=True)
joblib.dump({"model": model, "metadata": metadata}, HERE / "models" / "lead_model_standin.joblib")

# 5. The model card, with the numbers this run produced.
by_region = leads.groupby("region")["lead_score"].agg(["count", "mean"]).round(1)
by_region = by_region.reindex(["West", "South", "North", "East"])
rows = "\n".join(f"| {r} | {int(c):,} | {m} |" for r, (c, m) in by_region.iterrows())
card = f"""# Model card: lead score (the Chapter 64 stand-in)

Written by `build_ch64_files.py` (Chapter 64, section 64.8), in the format of Chapter 39, section 39.10.
The model is a simplified stand-in for the Part 4 lead-scoring model. The numbers are this run's real output.

| Field | Entry |
|---|---|
| Purpose | Rank new sales leads so reps call the likeliest wins first |
| Not for | Deciding whether a lead is contacted at all; pricing; credit decisions |
| Inputs | {", ".join(FEATURES)} (region is **not** an input) |
| Output | lead_score: predicted chance of winning the lead, in percent (0 to 100) |
| Training data | {len(train):,} leads from 2024 (a 75% sample); {len(test):,} held back for testing |
| Test AUC | {auc:.3f} |
| Owner (business) | Anita Rao, Sales Head |
| Built by | Meera Iyer, analytics |
| Approved by | (a named person who did not build it; filled in at approval) |
| Version | stand-in, file models/lead_model_standin.joblib |

## Score by region, 2025 leads

| Region | Leads | Mean score |
|---|---:|---:|
{rows}

## Known limits

- The score follows company size, and company size differs by region, so East leads score lower
  on average although region is not an input (section 64.7). Use it with the response-priority
  rule, not alone.
- Trained on 2024 leads only; re-check the regional gap every quarter.
"""
(HERE / "lead-model-card.md").write_text(card, encoding="utf-8")

print(f"{len(leads):,} scored leads written to leads_scored_2025.csv")
print(f"model saved to models/lead_model_standin.joblib (test AUC {auc:.3f})")
print("model card written to lead-model-card.md")
