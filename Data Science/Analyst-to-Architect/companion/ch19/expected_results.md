# Chapter 19 — what the consolidation must produce

Built by `build_ch19_files.py` from the clean Q4 2025 order lines (the same data as Chapter 14's answer key).
Riverstone Supplies is fictional; every name and number is invented.

## The twelve files

| file                              | branch    | month   |   rows |   non_cancelled | net_revenue    |
|:----------------------------------|:----------|:--------|-------:|----------------:|:---------------|
| Riverstone_Bengaluru_2025-10.xlsx | Bengaluru | 2025-10 |   2631 |            2532 | ₹51,605,379.25 |
| Riverstone_Bengaluru_2025-11.xlsx | Bengaluru | 2025-11 |   2481 |            2367 | ₹42,936,836.00 |
| Riverstone_Bengaluru_2025-12.xlsx | Bengaluru | 2025-12 |   2073 |            1990 | ₹23,184,311.75 |
| Riverstone_Delhi_2025-10.xlsx     | Delhi     | 2025-10 |   2211 |            2109 | ₹43,403,273.50 |
| Riverstone_Delhi_2025-11.xlsx     | Delhi     | 2025-11 |   2220 |            2121 | ₹38,300,645.75 |
| Riverstone_Delhi_2025-12.xlsx     | Delhi     | 2025-12 |   1843 |            1747 | ₹21,262,908.75 |
| Riverstone_Kolkata_2025-10.xlsx   | Kolkata   | 2025-10 |   1117 |            1065 | ₹21,647,307.75 |
| Riverstone_Kolkata_2025-11.xlsx   | Kolkata   | 2025-11 |   1099 |            1051 | ₹18,841,553.00 |
| Riverstone_Kolkata_2025-12.xlsx   | Kolkata   | 2025-12 |    994 |             958 | ₹11,632,073.00 |
| Riverstone_Mumbai_HO_2025-10.xlsx | Mumbai HO | 2025-10 |   3297 |            3175 | ₹63,964,142.25 |
| Riverstone_Mumbai_HO_2025-11.xlsx | Mumbai HO | 2025-11 |   3167 |            3040 | ₹55,906,866.75 |
| Riverstone_Mumbai_HO_2025-12.xlsx | Mumbai HO | 2025-12 |   2699 |            2583 | ₹31,187,510.25 |

## After consolidating all twelve

- Data rows: **25,832** (plus one header row per file, which the macro must not copy)
- Non-cancelled rows: **24,738**
- Net revenue, non-cancelled: **₹423,872,808.00**
- Net revenue, all rows including cancelled: **₹442,577,334.00**
- Distinct orders: **14,372**  ·  distinct customers: **4,237**

### By branch (non-cancelled)

| branch    |   rows | net_revenue     |
|:----------|-------:|:----------------|
| Bengaluru |   6889 | ₹117,726,527.00 |
| Delhi     |   5977 | ₹102,966,828.00 |
| Kolkata   |   3074 | ₹52,120,933.75  |
| Mumbai HO |   8798 | ₹151,058,519.25 |

### By month (non-cancelled)

| month   |   rows | net_revenue     |
|:--------|-------:|:----------------|
| 2025-10 |   8881 | ₹180,620,102.75 |
| 2025-11 |   8579 | ₹155,985,901.50 |
| 2025-12 |   7278 | ₹87,266,803.75  |

### Rows by status (all rows)

| status    |   rows |
|:----------|-------:|
| Delivered |  22434 |
| Pending   |   1166 |
| Shipped   |   1138 |
| Cancelled |   1094 |

