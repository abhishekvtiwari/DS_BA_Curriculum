"""
Analyst to Architect — Chapter 64: Security, Privacy, Governance & Responsible AI
build_ch64_files.py — builds the fairness-audit dataset for section 64.7.

The lead-scoring model itself is invented for this chapter (Part VI's CRM sync mentions
lead scoring but never specifies a model); built to contain a REALISTIC, EXPLAINABLE proxy-
discrimination pattern: the score never uses region as a feature, but correlates with company
size, and company size correlates with region because Riverstone's historically bigger
branches (Mumbai HO, Bengaluru) have more large accounts in the training data. This is the
single most common real-world fairness failure — proxy discrimination through a legitimate-
looking feature — and it's built here so the audit in section 64.7 has something real to find.
Seed 202401. Riverstone Supplies is fictional; every name and number is invented.

Run from this folder:  python3 build_ch64_files.py   (needs pandas, numpy)
Creates: leads_scored_2025.csv
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
rng = np.random.default_rng(202401)

REGION_MIX = {  # region -> (n_leads, mean company_size_band [1-5], noise)
    "West":  (620, 3.1, 1.0),
    "South": (540, 2.9, 1.0),
    "North": (410, 2.5, 1.0),
    "East":  (260, 1.9, 1.0),   # Kolkata/East: historically smaller accounts (established in earlier chapters)
}

rows = []
lead_id = 1
for region, (n, mean_size, noise) in REGION_MIX.items():
    size_band = np.clip(np.round(rng.normal(mean_size, noise, n)), 1, 5).astype(int)
    days_since_signup = rng.integers(1, 365, n)
    industry = rng.choice(["Retail", "Hospitality", "Wholesale"], n, p=[0.5, 0.25, 0.25])
    # the model: score depends on size_band and recency, NEVER on region directly —
    # but size_band's distribution differs sharply by region, so the score does too.
    base = 30 + size_band * 12 - (days_since_signup / 365) * 15
    lead_score = np.clip(np.round(base + rng.normal(0, 6, n)), 5, 95).astype(int)
    for i in range(n):
        rows.append({"lead_id": lead_id, "region": region, "company_size_band": size_band[i],
                     "days_since_signup": days_since_signup[i], "industry": industry[i],
                     "lead_score": lead_score[i]})
        lead_id += 1

df = pd.DataFrame(rows).sample(frac=1, random_state=64).reset_index(drop=True)
df["lead_id"] = range(1, len(df) + 1)
df.to_csv(HERE / "leads_scored_2025.csv", index=False)

print(f"{len(df):,} scored leads")
print(df.groupby("region")["lead_score"].agg(["count", "mean", "median"]).round(1))
print("\ncorrelation, score vs size_band:", round(df["lead_score"].corr(df["company_size_band"]), 3))
print("region never used as a feature; score is driven entirely by size_band and recency")
