"""
Analyst to Architect - Chapter 66: Data Strategy, Maturity & Building Data Teams
build_ch66_files.py - builds the maturity scorecard and the business-case (ROI) inputs.

Only raw inputs go into the CSVs; every subtotal and ratio is computed in the chapter's code
cells, never stored here.

Where each number comes from:
  - Platform cost: Chapter 65's monthly cost model (companion/ch65/monthly_cost_model.csv),
    summed and multiplied by 12.
  - Riverstone's loaded staff cost, Rs 300 an hour (Chapter 20, section 20.14).
  - Daily Sales Flash: 325 hours a year saved (Chapter 20, section 20.14) x Rs 300.
  - Branch consolidation macro: run once a quarter, 4 minutes -> 9 seconds (Chapter 19's story),
    so 4 runs x 231 seconds x Rs 300 an hour (Chapter 63's value table gives the same Rs 77).
  - PO intake, assisted mode: (Rs 600 typing - Rs 197 review and queue) a day x 250 working days
    (Chapter 58, section 58.7; Chapter 63's value table). Labour only, and worth counting only if
    the reviewers catch at least about 97% of wrong drafts (Chapter 58); at a 90% catch rate the
    missed wrong orders turn it into a loss (Chapter 63).
  - Proposed hire: Rs 9,00,000 a year is Riverstone's budget for the role in this story, not a
    quoted market salary.
Riverstone Supplies is fictional; every name and number is invented.

Run from this folder: python3 build_ch66_files.py
Creates: maturity_scorecard.csv, roi_case.csv
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent

# ---- 1. Maturity scorecard ---------------------------------------------------------------
# stage_met: the highest stage whose five criteria are all met.
# next_met:  how many of the next stage's five criteria are met (0-5).
# The chapter computes score = stage_met + next_met / 5.
maturity = pd.DataFrame([
    {"dimension": "Data quality & reliability", "stage_met": 3, "next_met": 3,
     "evidence": "Automated tests and freshness checks (Ch 47), reconciled totals (Ch 14); not every source has a contract yet"},
    {"dimension": "Architecture & platform", "stage_met": 3, "next_met": 1,
     "evidence": "A designed, documented platform (Ch 60-62); still centralized, still young"},
    {"dimension": "Security & access", "stage_met": 3, "next_met": 4,
     "evidence": "Roles, masked views, row-level security and a fairness audit (Ch 64); not yet a company-wide habit"},
    {"dimension": "Catalog & discoverability", "stage_met": 1, "next_met": 4,
     "evidence": "No catalog: finding the right table means asking Meera's team; 11 of 24 automations were unknown to it (Ch 63)"},
    {"dimension": "Cost discipline", "stage_met": 2, "next_met": 3,
     "evidence": "A real cost model (Ch 65), built once, not yet reviewed every month"},
    {"dimension": "Data-driven culture", "stage_met": 2, "next_met": 1,
     "evidence": "Individual wins (Ch 19, 20); most decisions still made by habit and hierarchy"},
])
maturity.to_csv(HERE / "maturity_scorecard.csv", index=False)

# ---- 2. Business-case inputs -------------------------------------------------------------
RATE = 300                    # Rs an hour, Riverstone's loaded staff cost (Chapter 20)
WORKING_DAYS = 250            # the year Chapter 20 and Chapter 63 use

cost65 = pd.read_csv(HERE.parent / "ch65" / "monthly_cost_model.csv")
platform_monthly = int(cost65["monthly_inr"].sum())
platform_annual = platform_monthly * 12

flash = 325 * RATE                                   # Chapter 20, section 20.14
macro = round(4 * (240 - 9) / 3600 * RATE)           # four quarterly runs, 4 min -> 9 s
po_intake = (600 - 197) * WORKING_DAYS               # Chapter 58 / 63, labour only
HIRE_SALARY = 900_000                                # Riverstone's budget for the role

roi = pd.DataFrame([
    {"item_id": "platform_cost", "amount_rs": platform_annual, "kind": "cost",
     "source": f"Ch 65: Rs {platform_monthly:,} a month x 12"},
    {"item_id": "flash", "amount_rs": flash, "kind": "measured saving",
     "source": "Ch 20: 325 hours x Rs 300"},
    {"item_id": "macro", "amount_rs": macro, "kind": "measured saving",
     "source": "Ch 19: 4 runs x 231 s x Rs 300 an hour"},
    {"item_id": "po_intake", "amount_rs": po_intake, "kind": "conditional saving",
     "source": "Ch 58: (Rs 600 - Rs 197) x 250 days; only if 97% caught"},
    {"item_id": "hire_salary", "amount_rs": HIRE_SALARY, "kind": "cost",
     "source": "Proposed catalog owner, a year"},
])
roi.to_csv(HERE / "roi_case.csv", index=False)

if __name__ == "__main__":
    print(maturity.to_string(index=False))
    print()
    print(roi.to_string(index=False))
