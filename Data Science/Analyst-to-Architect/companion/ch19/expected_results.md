# Chapter 19 — what the consolidation must produce

Built by `build_ch19_files.py` from Riverstone's Q4 2025 order lines. Rupee amounts use Indian grouping (₹42,38,72,808.00).
Riverstone Supplies is fictional; every name and number is invented.

## The twelve files

| file                              | branch    | month   |   rows |   non_cancelled | net_revenue     |
|:----------------------------------|:----------|:--------|-------:|----------------:|:----------------|
| Riverstone_Bengaluru_2025-10.xlsx | Bengaluru | 2025-10 |   2631 |            2532 | ₹5,16,05,379.25 |
| Riverstone_Bengaluru_2025-11.xlsx | Bengaluru | 2025-11 |   2481 |            2367 | ₹4,29,36,836.00 |
| Riverstone_Bengaluru_2025-12.xlsx | Bengaluru | 2025-12 |   2073 |            1990 | ₹2,31,84,311.75 |
| Riverstone_Delhi_2025-10.xlsx     | Delhi     | 2025-10 |   2211 |            2109 | ₹4,34,03,273.50 |
| Riverstone_Delhi_2025-11.xlsx     | Delhi     | 2025-11 |   2220 |            2121 | ₹3,83,00,645.75 |
| Riverstone_Delhi_2025-12.xlsx     | Delhi     | 2025-12 |   1843 |            1747 | ₹2,12,62,908.75 |
| Riverstone_Kolkata_2025-10.xlsx   | Kolkata   | 2025-10 |   1117 |            1065 | ₹2,16,47,307.75 |
| Riverstone_Kolkata_2025-11.xlsx   | Kolkata   | 2025-11 |   1099 |            1051 | ₹1,88,41,553.00 |
| Riverstone_Kolkata_2025-12.xlsx   | Kolkata   | 2025-12 |    994 |             958 | ₹1,16,32,073.00 |
| Riverstone_Mumbai_HO_2025-10.xlsx | Mumbai HO | 2025-10 |   3297 |            3175 | ₹6,39,64,142.25 |
| Riverstone_Mumbai_HO_2025-11.xlsx | Mumbai HO | 2025-11 |   3167 |            3040 | ₹5,59,06,866.75 |
| Riverstone_Mumbai_HO_2025-12.xlsx | Mumbai HO | 2025-12 |   2699 |            2583 | ₹3,11,87,510.25 |

## After consolidating all twelve

- Data rows: **25,832** (plus one header row per file, which the macro must not copy)
- Non-cancelled rows: **24,738**
- Net revenue, non-cancelled: **₹42,38,72,808.00**
- Net revenue, all rows including cancelled: **₹44,25,77,334.00**
- Distinct orders: **14,372**  ·  distinct customers: **4,237**

### By branch (non-cancelled)

| branch    |   rows | net_revenue      |
|:----------|-------:|:-----------------|
| Bengaluru |   6889 | ₹11,77,26,527.00 |
| Delhi     |   5977 | ₹10,29,66,828.00 |
| Kolkata   |   3074 | ₹5,21,20,933.75  |
| Mumbai HO |   8798 | ₹15,10,58,519.25 |

### By month (non-cancelled)

| month   |   rows | net_revenue      |
|:--------|-------:|:-----------------|
| 2025-10 |   8881 | ₹18,06,20,102.75 |
| 2025-11 |   8579 | ₹15,59,85,901.50 |
| 2025-12 |   7278 | ₹8,72,66,803.75  |

### Rows by status (all rows)

| status    |   rows |
|:----------|-------:|
| Delivered |  22434 |
| Pending   |   1166 |
| Shipped   |   1138 |
| Cancelled |   1094 |

