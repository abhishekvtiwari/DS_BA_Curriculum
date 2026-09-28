# Riverstone Supplies — financial statements for calendar 2025

*Companion data for Chapter 23. The statements cover calendar 2025, 1 January to 31 December, so that
they line up with the order data; they are not India's April–March financial year from Chapter 16.
Revenue, cost of goods sold, gross margin, and the customer counts come directly from the real order
data (`companion/full/`) and match Chapter 16's 2025 figures. Everything from operating expenses
downward (the P&L below gross profit, the whole balance sheet, the cash flow statement, the quarter-end
balances) and all marketing and NPS figures are invented for this chapter, sized to a plausible
mid-size B2B manufacturer and distributor, and built by a seeded script in this folder (seed 202301).
Riverstone Supplies is fictional.*

## Profit & loss, calendar 2025 (₹)

| Line | ₹ | % of revenue |
|---|---:|---:|
| Net revenue | 1,146,641,651 | 100.0% |
| Cost of goods sold | (831,803,000) | 72.5% |
| **Gross profit** | **314,838,651** | **27.5%** |
| Selling & distribution | (59,625,366) | 5.2% |
| Marketing | (20,639,550) | 1.8% |
| Administration | (47,012,308) | 4.1% |
| Depreciation & amortisation | (16,052,983) | 1.4% |
| **EBIT (operating profit)** | **171,508,444** | **15.0%** |
| Interest expense | (10,319,775) | 0.9% |
| **Profit before tax** | **161,188,669** | **14.1%** |
| Tax (25%) | (40,297,167) | 3.5% |
| **Profit after tax (net profit)** | **120,891,502** | **10.5%** |

## Balance sheet, 31 December 2025 (year-end, ₹)

| Assets | ₹ | | Liabilities & equity | ₹ |
|---|---:|---|---|---:|
| Cash & bank | 69,945,141 | | Trade payables | 86,598,668 |
| Trade receivables | 131,942,327 | | Short-term debt | 97,464,540 |
| Inventory | 125,340,178 | | Other current liabilities | 34,399,250 |
| Other current assets | 17,199,625 | | **Total current liabilities** | **218,462,458** |
| **Total current assets** | **344,427,271** | | Long-term debt | 126,130,582 |
| Property, plant & equipment (net) | 355,458,912 | | **Total liabilities** | **344,593,040** |
| Other non-current assets | 22,932,833 | | Shareholders' equity | 378,225,976 |
| **Total assets** | **722,819,016** | | **Total liabilities & equity** | **722,819,016** |

**Working capital** = current assets − current liabilities = ₹125,964,813
**Liabilities-to-equity** = total liabilities ÷ equity = 0.91

**Days on the cycle** (year-end balances stand in for the year's averages):

- DIO = inventory ÷ COGS × 365 = 125,340,178 ÷ 831,803,000 × 365 = 55.0 days
- DSO = receivables ÷ revenue × 365 = 131,942,327 ÷ 1,146,641,651 × 365 = 42.0 days
- DPO = payables ÷ COGS × 365 = 86,598,668 ÷ 831,803,000 × 365 = 38.0 days
- **Cash conversion cycle** = DIO + DSO − DPO = 55 + 42 − 38 = **59 days**

## Cash flow statement, calendar 2025 (₹, indirect method)

| Line | ₹ |
|---|---:|
| Profit after tax | 120,891,502 |
| + Depreciation | 16,052,983 |
| − Increase in receivables | (4,586,567) |
| − Increase in inventory | (6,879,850) |
| + Increase in payables | 3,439,925 |
| **Cash flow from operations (CFO)** | **128,917,993** |
| Capital expenditure | (51,598,874) |
| **Cash flow from investing (CFI)** | **(51,598,874)** |
| Debt drawn | 22,932,833 |
| Dividend paid | (42,312,026) |
| Loan repayment | (9,173,133) |
| **Cash flow from financing (CFF)** | **-28,552,326** |
| **Net change in cash** | **48,766,793** |
| Cash, opening | 21,178,348 |
| Cash, closing | 69,945,141 |

## Customer and marketing metrics, 2025

| Metric | Value |
|---|---:|
| Active customers, 2024 | 4,104 |
| Active customers, 2025 | 4,599 |
| Retained (active both years) | 3,827 |
| Churned (active 2024, not 2025) | 277 |
| New in 2025 | 772 |
| Retention rate | 93.3% |
| Churn rate | 6.7% |
| Implied average customer lifetime (1/churn, uncapped) | 14.8 years |
| Average first-year revenue, new 2025 customers | ₹157,617 |
| Average annual revenue, all active customers | ₹249,324 |
| Gross margin (for LTV) | 27.5% |
| LTV, naive formula (revenue × margin × 1/churn) | ₹642,189 |
| **LTV, 5-year-capped (recommended)** | **₹216,723** |
| 2025 marketing spend | ₹6,284,762 |
| 2025 new customers (the count CAC divides by) | 772 |
| **Customer acquisition cost (CAC)** | **₹8,141** |
| **LTV : CAC** | **26.6 : 1** |
| Net Promoter Score (quarterly survey, invented) | +34 |

## Quarter-end working capital, 2025 (invented balances)

Each ratio uses the quarter-end balance and the twelve months of sales (DSO) or cost of sales (DIO, DPO)
up to that date. The 31 December row is the balance sheet above.

| Quarter end | Receivables | Inventory | Payables | DSO | DIO | DPO | CCC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2025-03-31 | 95,366,799 | 102,718,592 | 73,088,229 | 36 | 52 | 37 | 51 |
| 2025-06-30 | 106,439,080 | 109,827,907 | 76,672,312 | 38 | 53 | 37 | 54 |
| 2025-09-30 | 117,338,030 | 116,351,433 | 81,876,934 | 40 | 54 | 38 | 56 |
| 2025-12-31 | 131,942,327 | 125,340,178 | 86,598,668 | 42 | 55 | 38 | 59 |
