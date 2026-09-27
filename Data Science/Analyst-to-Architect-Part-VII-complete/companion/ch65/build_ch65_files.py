"""
Analyst to Architect — Chapter 65: FinOps: The Economics of Data Platforms
build_ch65_files.py — builds Riverstone's monthly platform cost model.

Infrastructure unit prices are anchored to real, searched AWS ap-south-1 (Mumbai) rates as of
August 2026 (RDS db.m5.large Postgres $0.253/hr; gp3 storage $0.131/GB-month; S3 Standard
$0.023/GB-month; S3 Glacier Deep Archive $0.002/GB-month; data transfer out $0.09/GB after the
free tier) -- see the chapter's Tools section for sources. LLM API prices reuse Part VI Chapter
54's already-searched September 2026 figures (per 1M tokens) so the whole book stays internally
consistent. Volumes (order lines, PO emails, RAG questions, defect-model predictions) are the
real, established Riverstone facts from Chapters 16, 54, 55, 56, and 58. Everything else in this
file -- which specific instance sizes Riverstone runs, exact storage volumes -- is a reasonable,
invented sizing for a company this scale, not a verified fact. Riverstone Supplies is fictional.

Run from this folder: python3 build_ch65_files.py
Creates: monthly_cost_model.csv, unit_economics.csv
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
USD_INR = 87.0   # illustrative conversion rate used throughout this chapter, stated once here

# ---- 1. Infrastructure: real ap-south-1 (Mumbai) rates, Riverstone-sized ----------------------
infra = [
    # component, unit, unit_price_usd, quantity, monthly_usd, notes
    ("RDS PostgreSQL (db.m5.large, Single-AZ)", "instance-hours", 0.253, 730, None, "warehouse primary"),
    ("RDS storage (gp3)", "GB-month", 0.131, 800, None, "800 GB provisioned"),
    ("RDS automated backups", "GB-month", 0.0, 800, 0.0, "free up to provisioned size"),
    ("S3 Standard (sensor archive, hot)", "GB-month", 0.023, 1200, None, "recent 90 days, Delta Lake"),
    ("S3 Glacier Deep Archive (sensor archive, cold)", "GB-month", 0.002, 9800, None, "older than 90 days"),
    ("Data transfer out (dashboards, API, email)", "GB", 0.09, 180, None, "180 GB/month egress"),
    ("Dagster orchestration compute (small EC2 fleet)", "instance-hours", 0.052, 730, None, "t3.large, ingestion + scheduling"),
    ("Defect-model serving (FastAPI, small EC2)", "instance-hours", 0.052, 730, None, "t3.large, always-on for line speed"),
]
rows = []
for name, unit, price, qty, monthly, notes in infra:
    m = monthly if monthly is not None else round(price * qty, 2)
    rows.append({"component": name, "unit": unit, "unit_price_usd": price, "quantity": qty,
                "monthly_usd": m, "notes": notes})
infra_df = pd.DataFrame(rows)

# ---- 2. LLM API costs: real Sep 2026 prices from Chapter 54, real Riverstone volumes ----------
# PO-intake: ~30 emails/day (Ch54: 20-40/day), assume ~900/month; extraction uses a mid-tier model
# RAG assistant: modest support volume, ~25 questions/day = 750/month
llm = [
    ("PO-intake extraction (mid-tier model, e.g. Sonnet-5-class)", 900, 1800, 350, 2.0, 10.0),
    ("Support RAG assistant (small/flash-tier model)", 750, 2200, 180, 0.75, 3.75),
]
llm_rows = []
for name, calls, in_tok, out_tok, price_in, price_out in llm:
    monthly_in_cost = calls * in_tok / 1_000_000 * price_in
    monthly_out_cost = calls * out_tok / 1_000_000 * price_out
    llm_rows.append({"component": name, "calls_per_month": calls, "avg_input_tokens": in_tok,
                     "avg_output_tokens": out_tok, "price_per_1m_input_usd": price_in,
                     "price_per_1m_output_usd": price_out,
                     "monthly_usd": round(monthly_in_cost + monthly_out_cost, 2)})
llm_df = pd.DataFrame(llm_rows)

full = pd.concat([infra_df[["component", "monthly_usd", "notes"]],
                  llm_df[["component", "monthly_usd"]].assign(notes="LLM API, Ch 54 Sep 2026 rates")],
                 ignore_index=True)
full["monthly_inr"] = (full["monthly_usd"] * USD_INR).round(0)
full.to_csv(HERE / "monthly_cost_model.csv", index=False)

total_usd = full["monthly_usd"].sum()
total_inr = full["monthly_inr"].sum()

# ---- 3. Unit economics, tied to Chapter 60's NFR (< Rs 0.50 per 1,000 order lines) -------------
order_lines_per_month = 209_006 / 12 * (46_356 / 46_356)  # ~ monthly order-line volume, from the real dataset
order_lines_per_month = round(17_417)  # 2025's 209,006 annual order lines / 12
flash_sends_per_month = 26  # business days
defect_predictions_per_month = 12000 / 6  # Ch53: 12,000 parts over 24 weeks -> ~2,000/week -> scale to a month
po_intake_emails_per_month = 900
rag_questions_per_month = 750

unit = pd.DataFrame([
    {"metric": "Total platform cost / month", "value_inr": round(total_inr), "value_usd": round(total_usd, 2)},
    {"metric": "Cost per 1,000 order lines processed", "value_inr": round(total_inr / (order_lines_per_month/1000), 3),
     "value_usd": round(total_usd / (order_lines_per_month/1000), 4)},
    {"metric": "Cost per Daily Flash send", "value_inr": round((total_inr*0.05) / flash_sends_per_month, 2),
     "value_usd": None},
    {"metric": "Cost per defect-model prediction", "value_inr": round((infra_df.loc[infra_df.component.str.contains('Defect'), 'monthly_usd'].sum()*USD_INR) / defect_predictions_per_month, 4),
     "value_usd": None},
    {"metric": "Cost per PO-intake email processed", "value_inr": round((llm_df.loc[0,'monthly_usd']*USD_INR) / po_intake_emails_per_month, 2),
     "value_usd": None},
    {"metric": "Cost per RAG assistant question answered", "value_inr": round((llm_df.loc[1,'monthly_usd']*USD_INR) / rag_questions_per_month, 3),
     "value_usd": None},
])
unit.to_csv(HERE / "unit_economics.csv", index=False)

print(f"Total monthly platform cost: ${total_usd:,.2f} (Rs {total_inr:,.0f})")
print(f"Cost per 1,000 order lines: Rs {total_inr/(order_lines_per_month/1000):.3f}")
print(f"Chapter 60's NFR target: under Rs 0.50 per 1,000 order lines")
print(unit.to_string(index=False))
