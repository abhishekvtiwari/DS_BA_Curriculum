"""
Analyst to Architect — Chapter 23: Business Acumen, KPIs & Metrics
build_ch23_files.py — builds Riverstone's financial statements for calendar
2025 (January to December) and a marketing/customer metrics table. Sales, gross margin, and delivery metrics are
NOT invented here: they come straight from the real dataset (companion/full,
companion/ch21). Only the P&L lines below gross profit, the balance sheet, the
cash flow statement, and marketing spend/CAC/NPS are invented, because
Riverstone's ERP data has no ledger, no balance sheet and no marketing system.
Seed 202301, so every number is reproducible. Riverstone Supplies is fictional;
every name and number is invented.

Run from this folder:  python3 build_ch23_files.py   (needs pandas, numpy, pyarrow)
Reads ../full/*.parquet and ../ch21/delivery_times_2025.csv.

Creates:
  financials_2025.md             P&L, balance sheet, cash flow statement (calendar 2025, ₹)
  monthly_revenue_2025.csv       the real monthly revenue/orders/customers/AOV series
  marketing_2025.csv             monthly marketing spend, leads, CAC, ROAS (invented)
  working_capital_quarters_2025.csv  quarter-end receivables, inventory, payables and
                                 DSO/DIO/DPO/CCC (invented balances; used by the chapter's
                                 "In the real world" story)
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
rng = np.random.default_rng(202301)

O = pd.read_parquet(FULL / "orders.parquet")
I = pd.read_parquet(FULL / "order_items.parquet")
C = pd.read_parquet(FULL / "customers.parquet")
P = pd.read_parquet(FULL / "products.parquet")
lines = I.merge(O, on="order_id").merge(P[["product_id", "unit_cost"]], on="product_id")
lines["net_revenue"] = lines.quantity * lines.unit_price * (1 - lines.discount_pct / 100)
lines["cost"] = lines.quantity * lines.unit_cost
not_cancelled = lines[lines.status != "Cancelled"]
sales = not_cancelled[(not_cancelled.order_date >= "2025-01-01") & (not_cancelled.order_date < "2026-01-01")].copy()
sales_2024 = not_cancelled[(not_cancelled.order_date >= "2024-01-01") & (not_cancelled.order_date < "2025-01-01")]

# ---- 1. the real monthly series (revenue, orders, customers, AOV) ------------------------------
sales["month"] = sales.order_date.dt.to_period("M").astype(str)
monthly = (sales.groupby("month")
           .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"), customers=("customer_id", "nunique"))
           .reset_index())
monthly["aov"] = (monthly.net_revenue / monthly.orders).round(2)
monthly.to_csv(HERE / "monthly_revenue_2025.csv", index=False)

REVENUE = round(sales.net_revenue.sum())
COGS = round(sales.cost.sum())
GROSS_PROFIT = REVENUE - COGS
GROSS_MARGIN = GROSS_PROFIT / REVENUE

# ---- 2. 2025 P&L (below gross profit is invented, sized to a plausible mid-size manufacturer and distributor)
selling_dist = round(REVENUE * 0.052)         # freight, warehousing, sales salaries & commission
marketing = round(REVENUE * 0.018)
admin = round(REVENUE * 0.041)                # office, IT, finance/HR overhead
depreciation = round(REVENUE * 0.014)
opex = selling_dist + marketing + admin + depreciation
ebit = GROSS_PROFIT - opex
interest = round(REVENUE * 0.009)             # working-capital loan interest
pbt = ebit - interest
tax = round(pbt * 0.25)
pat = pbt - tax

# ---- 3. balance sheet (year-end, invented but consistent with the P&L) --------------------------
DSO, DPO, DIO = 42, 38, 55                    # days sales/payable/inventory outstanding
receivables = round(REVENUE / 365 * DSO)
payables = round(COGS / 365 * DPO)
inventory = round(COGS / 365 * DIO)
cash = round(REVENUE * 0.061)
other_current_assets = round(REVENUE * 0.015)
current_assets = cash + receivables + inventory + other_current_assets
ppe = round(REVENUE * 0.31)                   # plant, warehouse, vehicles (net of depreciation)
other_non_current = round(REVENUE * 0.02)
total_assets = current_assets + ppe + other_non_current

short_term_debt = round(REVENUE * 0.085)
other_current_liab = round(REVENUE * 0.03)
current_liabilities = payables + short_term_debt + other_current_liab
long_term_debt = round(REVENUE * 0.11)
total_liabilities = current_liabilities + long_term_debt
DIVIDEND_PAYOUT = 0.35                        # 35% of profit distributed to the owning family
equity = total_assets - total_liabilities     # forced by the accounting identity: assets = liabilities + equity
dividend = round(pat * DIVIDEND_PAYOUT)
retained_this_year = pat - dividend
equity_opening = equity - retained_this_year  # so opening equity + retained profit = closing equity, exactly

working_capital = current_assets - current_liabilities
cash_conversion_cycle = DIO + DSO - DPO

# ---- 4. cash flow statement (indirect method, invented) -----------------------------------------
capex = round(REVENUE * 0.045)
receivables_change = round(REVENUE * 0.004)   # receivables grew a little this year
inventory_change = round(REVENUE * 0.006)
payables_change = round(REVENUE * 0.003)
cfo = pat + depreciation - receivables_change - inventory_change + payables_change
cfi = -capex
debt_drawn = round(REVENUE * 0.02)
cff = debt_drawn - dividend - round(REVENUE * 0.008)   # scheduled loan repayment
net_change = cfo + cfi + cff
cash_opening = cash - net_change

# ---- 5. customers (real) --------------------------------------------------------------------------
# Both years exclude cancelled orders, exactly as the chapter's section 23.9 does.
active_2024 = set(sales_2024.customer_id)
active_2025 = set(sales.customer_id)
retained = active_2024 & active_2025
churned = active_2024 - active_2025
new_2025 = active_2025 - active_2024

# ---- 6. marketing (fully invented: no marketing system in the ERP) --------------------------------
base_leads = np.array([420, 390, 470, 510, 480, 340, 300, 410, 560, 690, 640, 460])
spend = np.round(base_leads * rng.uniform(950, 1250, 12)).astype(int)
conv = rng.uniform(0.16, 0.24, 12)
new_customers_raw = base_leads * conv
# scaled so the annual total ties to the real count of customers new to Riverstone in 2025
# (largest-remainder rounding, so the twelve months add up to it exactly)
share = new_customers_raw / new_customers_raw.sum() * len(new_2025)
new_customers = np.floor(share).astype(int)
new_customers[np.argsort(-(share - new_customers))[: len(new_2025) - new_customers.sum()]] += 1
mk = pd.DataFrame({"month": monthly.month, "leads": base_leads, "marketing_spend": spend, "new_customers": new_customers})
mk["cac"] = (mk.marketing_spend / mk.new_customers).round(0)
# ROAS is measured on revenue from the new customers marketing brought in, not total company revenue
mk["attributed_revenue"] = (mk.new_customers * 45000 * rng.uniform(0.85, 1.15, 12)).round(0)  # first-year run-rate per new B2B account
mk["roas"] = (mk.attributed_revenue / mk.marketing_spend).round(2)
mk.to_csv(HERE / "marketing_2025.csv", index=False)

retention_rate = len(retained) / len(active_2024)
churn_rate = 1 - retention_rate

avg_customer_life_years_naive = 1 / churn_rate     # the textbook formula: 1 / churn
LTV_HORIZON_YEARS = 5                              # capped: nobody should bank on decades of retention
# LTV is computed for a NEW customer (the kind CAC buys), not the average of the whole base
# (which includes large legacy accounts signed up years before any marketing spend existed).
new_cust_annual_revenue = sales[sales.customer_id.isin(new_2025)].groupby("customer_id").net_revenue.sum().mean()
avg_annual_revenue_per_customer = sales.groupby("customer_id").net_revenue.sum().mean()
LTV_MARGIN = round(GROSS_MARGIN, 3)                # 27.5%, as the chapter uses it
ltv_naive = new_cust_annual_revenue * LTV_MARGIN * avg_customer_life_years_naive
ltv = new_cust_annual_revenue * LTV_MARGIN * LTV_HORIZON_YEARS
avg_cac = mk.marketing_spend.sum() / mk.new_customers.sum()
nps = 34   # invented: % promoters (9-10) minus % detractors (0-6) from a quarterly survey

md = f"""# Riverstone Supplies — FY2025 financial statements

*Companion data for Chapter 23. Revenue, cost of goods sold, and gross margin come directly from the
real order data (`companion/full/`) and match every earlier chapter exactly. Everything from operating
expenses downward — the P&L below gross profit, the whole balance sheet, the cash flow statement, and
all marketing and NPS figures — is invented for this chapter, sized to a plausible mid-size B2B
distributor and built by `build_ch23_files.py` (seed 202301). Riverstone Supplies is fictional.*

## Profit & loss, FY2025 (₹)

| Line | ₹ | % of revenue |
|---|---:|---:|
| Net revenue | {REVENUE:,} | 100.0% |
| Cost of goods sold | ({COGS:,}) | {COGS/REVENUE*100:.1f}% |
| **Gross profit** | **{GROSS_PROFIT:,}** | **{GROSS_MARGIN*100:.1f}%** |
| Selling & distribution | ({selling_dist:,}) | {selling_dist/REVENUE*100:.1f}% |
| Marketing | ({marketing:,}) | {marketing/REVENUE*100:.1f}% |
| Administration | ({admin:,}) | {admin/REVENUE*100:.1f}% |
| Depreciation & amortisation | ({depreciation:,}) | {depreciation/REVENUE*100:.1f}% |
| **EBIT (operating profit)** | **{ebit:,}** | **{ebit/REVENUE*100:.1f}%** |
| Interest expense | ({interest:,}) | {interest/REVENUE*100:.1f}% |
| **Profit before tax** | **{pbt:,}** | **{pbt/REVENUE*100:.1f}%** |
| Tax (25%) | ({tax:,}) | {tax/REVENUE*100:.1f}% |
| **Profit after tax (net profit)** | **{pat:,}** | **{pat/REVENUE*100:.1f}%** |

## Balance sheet, 31 March 2026 (year-end, ₹)

| Assets | ₹ | | Liabilities & equity | ₹ |
|---|---:|---|---|---:|
| Cash & bank | {cash:,} | | Trade payables | {payables:,} |
| Trade receivables | {receivables:,} | | Short-term debt | {short_term_debt:,} |
| Inventory | {inventory:,} | | Other current liabilities | {other_current_liab:,} |
| Other current assets | {other_current_assets:,} | | **Total current liabilities** | **{current_liabilities:,}** |
| **Total current assets** | **{current_assets:,}** | | Long-term debt | {long_term_debt:,} |
| Property, plant & equipment (net) | {ppe:,} | | **Total liabilities** | **{total_liabilities:,}** |
| Other non-current assets | {other_non_current:,} | | Shareholders' equity | {equity:,} |
| **Total assets** | **{total_assets:,}** | | **Total liabilities & equity** | **{total_assets:,}** |

**Working capital** = current assets − current liabilities = ₹{working_capital:,}
**Cash conversion cycle** = DIO ({DIO}d) + DSO ({DSO}d) − DPO ({DPO}d) = **{cash_conversion_cycle} days**

## Cash flow statement, FY2025 (₹, indirect method)

| Line | ₹ |
|---|---:|
| Profit after tax | {pat:,} |
| + Depreciation | {depreciation:,} |
| − Increase in receivables | ({receivables_change:,}) |
| − Increase in inventory | ({inventory_change:,}) |
| + Increase in payables | {payables_change:,} |
| **Cash flow from operations (CFO)** | **{cfo:,}** |
| Capital expenditure | ({capex:,}) |
| **Cash flow from investing (CFI)** | **({capex:,})** |
| Debt drawn | {debt_drawn:,} |
| Dividend paid | ({dividend:,}) |
| Loan repayment | ({round(REVENUE*0.008):,}) |
| **Cash flow from financing (CFF)** | **{cff:,}** |
| **Net change in cash** | **{net_change:,}** |
| Cash, opening | {cash_opening:,} |
| Cash, closing | {cash:,} |

## Customer and marketing metrics, FY2025

| Metric | Value |
|---|---:|
| Active customers, 2024 | {len(active_2024):,} |
| Active customers, 2025 | {len(active_2025):,} |
| Retained (active both years) | {len(retained):,} |
| Churned (active 2024, not 2025) | {len(churned):,} |
| New in 2025 | {len(new_2025):,} |
| Retention rate | {retention_rate*100:.1f}% |
| Churn rate | {churn_rate*100:.1f}% |
| Implied average customer lifetime (1/churn, uncapped) | {avg_customer_life_years_naive:.1f} years |
| Average first-year revenue, new 2025 customers | ₹{new_cust_annual_revenue:,.0f} |
| Average annual revenue, all active customers | ₹{avg_annual_revenue_per_customer:,.0f} |
| Gross margin (for LTV) | {GROSS_MARGIN*100:.1f}% |
| LTV, naive formula (revenue × margin × 1/churn) | ₹{ltv_naive:,.0f} |
| **LTV, 5-year-capped (recommended)** | **₹{ltv:,.0f}** |
| 2025 marketing spend | ₹{mk.marketing_spend.sum():,} |
| 2025 new customers (marketing-attributed) | {mk.new_customers.sum():,} |
| **Customer acquisition cost (CAC)** | **₹{avg_cac:,.0f}** |
| **LTV : CAC** | **{ltv/avg_cac:.1f} : 1** |
| Net Promoter Score (quarterly survey, invented) | {nps:+d} |
"""
(HERE / "financials_fy2025.md").write_text(md, encoding="utf-8")

print(f"Revenue {REVENUE:,}  COGS {COGS:,}  Gross margin {GROSS_MARGIN*100:.1f}%")
print(f"EBIT {ebit:,} ({ebit/REVENUE*100:.1f}%)  PAT {pat:,} ({pat/REVENUE*100:.1f}%)")
print(f"Total assets {total_assets:,}  Equity {equity:,}  Working capital {working_capital:,}")
print(f"CCC {cash_conversion_cycle}d  Retention {retention_rate*100:.1f}%  LTV:CAC {ltv/avg_cac:.1f}")
print(f"new-customer annual revenue {new_cust_annual_revenue:,.0f}  all-customer annual revenue {avg_annual_revenue_per_customer:,.0f}")
print(f"naive LTV (1/churn = {avg_customer_life_years_naive:.1f}y): {ltv_naive:,.0f}  |  5-year-capped LTV: {ltv:,.0f}  |  LTV:CAC (capped) {ltv/avg_cac:.1f}")
