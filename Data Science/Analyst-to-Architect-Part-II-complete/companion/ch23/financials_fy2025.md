# Riverstone Supplies — FY2025 financial statements

*Companion data for Chapter 23. Revenue, cost of goods sold, and gross margin come directly from the
real order data (`companion/full/`) and match every earlier chapter exactly. Everything from operating
expenses downward — the P&L below gross profit, the whole balance sheet, the cash flow statement, and
all marketing and NPS figures — is invented for this chapter, sized to a plausible mid-size B2B
distributor and built by `build_ch23_files.py` (seed 202301). Riverstone Supplies is fictional.*

## Profit & loss, FY2025 (₹)

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

## Balance sheet, 31 March 2026 (year-end, ₹)

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
**Cash conversion cycle** = DIO (55d) + DSO (42d) − DPO (38d) = **59 days**

## Cash flow statement, FY2025 (₹, indirect method)

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

## Customer and marketing metrics, FY2025

| Metric | Value |
|---|---:|
| Active customers, 2024 | 4,109 |
| Active customers, 2025 | 4,599 |
| Retained (active both years) | 3,832 |
| Churned (active 2024, not 2025) | 277 |
| New in 2025 | 767 |
| Retention rate | 93.3% |
| Churn rate | 6.7% |
| Implied average customer lifetime (1/churn, uncapped) | 14.8 years |
| Average first-year revenue, new 2025 customers | ₹157,720 |
| Average annual revenue, all active customers | ₹249,324 |
| Gross margin (for LTV) | 27.5% |
| LTV, naive formula (revenue × margin × 1/churn) | ₹642,397 |
| **LTV, 5-year-capped (recommended)** | **₹216,530** |
| 2025 marketing spend | ₹6,284,762 |
| 2025 new customers (marketing-attributed) | 767 |
| **Customer acquisition cost (CAC)** | **₹8,194** |
| **LTV : CAC** | **26.4 : 1** |
| Net Promoter Score (quarterly survey, invented) | +34 |
