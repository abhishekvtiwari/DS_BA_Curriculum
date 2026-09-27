"""
Analyst to Architect — Chapter 66: Data Strategy, Maturity & Building Data Teams
build_ch66_files.py — builds the maturity scorecard and the ROI/business-case model.

Reuses real figures already established elsewhere in this book: Chapter 65's real monthly
platform cost (Rs 38,014), Chapter 20's real Daily Flash savings (325 hrs/year at a Rs 300/hr
loaded rate, from Chapter 58's own stated rate), and Chapter 19's real branch-macro time saving.
The proposed new hire's salary is a reasonable, invented, clearly-labelled figure for a mid-size
Indian company's data-governance role -- not a disclosed real salary. Riverstone Supplies is
fictional; every name and number is invented.

Run from this folder: python3 build_ch66_files.py
Creates: maturity_scorecard.csv, roi_case.csv
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent

# ---- 1. Maturity scorecard: five dimensions, stage 1-5, with evidence -------------------------
maturity = pd.DataFrame([
    {"dimension": "Data quality & reliability", "stage": 3.6,
     "evidence": "Automated tests (Ch 47), reconciled pipelines (Ch 14), but not every source has a contract yet"},
    {"dimension": "Architecture & platform", "stage": 3.2,
     "evidence": "A designed, documented platform (Ch 60-62) — still centralized, still young"},
    {"dimension": "Governance & security", "stage": 3.4,
     "evidence": "A real access model and fairness audits exist (Ch 63-64) — not yet company-wide habit"},
    {"dimension": "Cost discipline", "stage": 2.6,
     "evidence": "A real cost model exists (Ch 65) — but it was built once, not yet a routine practice"},
    {"dimension": "Data-driven culture", "stage": 2.2,
     "evidence": "Individual wins (Ch 19, 24) — most decisions still made by habit and hierarchy, not routinely by data"},
])
maturity.to_csv(HERE / "maturity_scorecard.csv", index=False)

# ---- 2. ROI case for the proposed next hire (a data governance / catalog owner) ----------------
LOADED_HOURLY_RATE = 300         # Rs/hour, Chapter 58's own stated coordinator rate, reused
PROPOSED_ANNUAL_SALARY = 900_000  # Rs, a reasonable mid-size-company data-governance hire

flash_savings_hrs_year = 325      # Chapter 20's real, computed figure
flash_savings_rs = flash_savings_hrs_year * LOADED_HOURLY_RATE

# Chapter 19: branch macro saved ~4 min manual -> 9 sec automated, "hundreds of runs a year"
# conservative: 300 runs/year, saving ~3.85 minutes each
branch_macro_runs_year = 300
branch_macro_minutes_saved = 3 + 51/60  # 4:00 - 0:09
branch_macro_savings_rs = branch_macro_runs_year * (branch_macro_minutes_saved/60) * LOADED_HOURLY_RATE

# Chapter 65's real platform cost, annualized
platform_annual_cost = 38_014 * 12

# Chapter 58 (Part VI): PO-intake assisted mode Rs 198/day vs manual Rs 600/day, ~250 working days/year
po_intake_savings_rs = (600 - 198) * 250

known_quantified_savings_partial = flash_savings_rs + branch_macro_savings_rs
known_quantified_savings_full = known_quantified_savings_partial + po_intake_savings_rs

roi = pd.DataFrame([
    {"item": "Riverstone platform, annual cost (Ch 65)", "amount_rs": platform_annual_cost},
    {"item": "Daily Flash time saved, annual value (Ch 20)", "amount_rs": round(flash_savings_rs)},
    {"item": "Branch macro time saved, annual value (Ch 19, conservative)", "amount_rs": round(branch_macro_savings_rs)},
    {"item": "PO-intake assisted-mode saving vs. fully manual, annual (Ch 58)", "amount_rs": round(po_intake_savings_rs)},
    {"item": "Quantified savings, two automations only (incomplete case)", "amount_rs": round(known_quantified_savings_partial)},
    {"item": "Quantified savings, three known automations (still incomplete)", "amount_rs": round(known_quantified_savings_full)},
    {"item": "Platform pays for itself, two automations only (x)", "amount_rs": round(known_quantified_savings_partial/platform_annual_cost, 2)},
    {"item": "Platform pays for itself, three known automations (x)", "amount_rs": round(known_quantified_savings_full/platform_annual_cost, 2)},
    {"item": "Proposed new hire: data governance / catalog owner, annual salary", "amount_rs": PROPOSED_ANNUAL_SALARY},
])
roi.to_csv(HERE / "roi_case.csv", index=False)

print(maturity.to_string(index=False))
print()
print(roi.to_string(index=False))
