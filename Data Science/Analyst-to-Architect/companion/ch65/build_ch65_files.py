"""
Analyst to Architect, Chapter 65: FinOps: The Economics of Data Platforms
build_ch65_files.py: builds Riverstone's monthly infrastructure bill and its unit economics.

Every unit price is a list price, checked on 29 September 2026 in AWS's public price list
(https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<service>/current/ap-south-1/index.json),
Asia Pacific (Mumbai), on-demand, before tax:
  AmazonRDS (published 24 Sep 2026)      db.m5.large PostgreSQL Single-AZ $0.253/hour;
                                         gp3 storage $0.131/GB-month; backup storage free up to
                                         the provisioned size, then $0.095/GB-month
  AmazonEC2 (published 25 Sep 2026)      t3.large Linux, shared tenancy, $0.0896/hour
  AmazonS3 (published 28 Sep 2026)       S3 Standard $0.025/GB-month (first 50 TB);
                                         S3 Glacier Flexible Retrieval $0.0045/GB-month
  AWSDataTransfer (published 16 Sep 2026) data out to the internet: first 100 GB a month free
                                         (all services together), then $0.1093/GB (first 10 TB)
LLM prices are Chapter 54's workhorse tier ($2 per million input tokens, $10 per million output
tokens, checked 29 Sep 2026), with the token counts Chapter 57 (PO intake) and Chapter 55 (the
support assistant) measured.

The sizing is invented, stated here and in section 65.2: one warehouse instance with 800 GB
provisioned, two small always-on servers, the sensor archive of Chapter 49's plant-wide rollout
a year in (277 GB), 180 GB a month of data out. The volumes come from earlier chapters:
2025's 87,011 order lines (riverstone_full, Chapter 14), 1,120 PO emails a month (Chapter 57),
1,000 support questions a month (Chapter 55), 500 inspected parts a week (Chapter 56) and
250 Flash sends a year (Chapter 20). Riverstone Supplies is fictional.

Run from this folder: python3 build_ch65_files.py
Creates: monthly_cost_model.csv, unit_economics.csv
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
USD_TO_INR = 87          # this chapter's exchange rate, rupees per dollar
HOURS_PER_MONTH = 730    # 24 x 365 / 12

# Chapter 49's rollout archive: 277 GB a year; the last 90 days stay hot, the rest is cold.
ARCHIVE_GB = 277
HOT_GB = round(ARCHIVE_GB * 90 / 365, 1)          # 68.3
COLD_GB = round(ARCHIVE_GB - HOT_GB, 1)            # 208.7

# Chapter 57: 60 golden-set calls used 10,844 input and 3,184 output tokens at $2 / $10 per million.
PO_PER_EMAIL_USD = (10_844 * 2 + 3_184 * 10) / 1_000_000 / 60
# Chapter 55: about 470 input and 60 output tokens a question, same tier.
RAG_PER_QUESTION_USD = (470 * 2 + 60 * 10) / 1_000_000

EGRESS_GB, EGRESS_FREE_GB = 180, 100

rows = [
    # component, owner, unit, unit_price_usd, quantity
    ("Warehouse compute (RDS)", "data platform", "instance-hour", 0.253, HOURS_PER_MONTH),
    ("Warehouse storage (gp3)", "data platform", "GB-month", 0.131, 800),
    ("Warehouse backups", "data platform", "GB-month", 0.0, 800),
    ("Orchestration (Dagster)", "data platform", "instance-hour", 0.0896, HOURS_PER_MONTH),
    ("Defect-model serving", "AI applications", "instance-hour", 0.0896, HOURS_PER_MONTH),
    ("PO-intake (LLM API)", "AI applications", "email", PO_PER_EMAIL_USD, 1_120),
    ("RAG assistant (LLM API)", "AI applications", "question", RAG_PER_QUESTION_USD, 1_000),
    ("Sensor archive, hot (S3)", "plant operations", "GB-month", 0.025, HOT_GB),
    ("Sensor archive, cold (Glacier)", "plant operations", "GB-month", 0.0045, COLD_GB),
    ("Data transfer out", "shared", "GB", 0.1093, EGRESS_GB - EGRESS_FREE_GB),
]
costs = pd.DataFrame(rows, columns=["component", "owner", "unit", "unit_price_usd", "quantity"])
costs["monthly_usd"] = (costs["unit_price_usd"] * costs["quantity"]).round(2)
costs["monthly_inr"] = (costs["monthly_usd"] * USD_TO_INR).round(0).astype(int)
costs["unit_price_usd"] = costs["unit_price_usd"].round(6)
costs.to_csv(HERE / "monthly_cost_model.csv", index=False)

# ---- Unit economics: the same allocation rules as section 65.3 ------------------------------
total = costs["monthly_inr"].sum()
by_name = costs.set_index("component")["monthly_inr"]
volumes = {"order line": 87_011 / 12, "defect prediction": 500 * 52 / 12,
           "PO-intake email": 1_120, "RAG question": 1_000}
flash_hour = (by_name["Warehouse compute (RDS)"] + by_name["Orchestration (Dagster)"]) / HOURS_PER_MONTH
unit = pd.DataFrame([
    ("per 1,000 order lines", total / (volumes["order line"] / 1_000)),
    ("per Daily Flash send", flash_hour * 2 / 60),
    ("per defect prediction", by_name["Defect-model serving"] / volumes["defect prediction"]),
    ("per PO-intake email", by_name["PO-intake (LLM API)"] / volumes["PO-intake email"]),
    ("per RAG question", by_name["RAG assistant (LLM API)"] / volumes["RAG question"]),
], columns=["metric", "value_inr"])
unit["value_inr"] = unit["value_inr"].round(3)
unit.to_csv(HERE / "unit_economics.csv", index=False)

print(costs[["component", "monthly_usd", "monthly_inr"]].to_string(index=False))
print(f"total: ${costs['monthly_usd'].sum():,.2f} = ₹{total:,.0f} a month at ₹{USD_TO_INR} to the dollar")
print(unit.to_string(index=False))
