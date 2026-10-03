# Chapter 70. Excel, Google Sheets, VBA & BI Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the spreadsheet, automation, and BI questions that come up across screening calls, live exercises, and case interviews for analyst, BA, BI, and automation-track roles · check every formula answer on a small practice table you can type in two minutes · read a broken macro and fix it live · critique a dashboard the way a hiring manager would · walk out with a 20-question final-week revision list.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Chapters 10, 11, 15, 16 and 19, with a few links to Chapter 12 (joins, `UNION ALL`, `GROUP BY`). This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 5–7 hours for a first pass (about 5 minutes per core question, 1–2 minutes per rapid-fire row), plus 1 hour for the final-week list. Section 70.9 adds about an hour and is best done with a spreadsheet open, since four of its questions ask you to confirm a behaviour in your own copy of Excel.
>
> **How this chapter is built.** Every **core question** gives a memory hook ("Remember it as…"), a one-line answer you can recall under pressure, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, one per line, tagged the same way: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Every **rapid-fire section** is a scan table: question, one-line answer, one extra point, level, and where to learn it. Every formula result comes from the practice table in section 70.0.

---

## 70.0 The practice table, and how to use this bank

Every formula answer below was worked on this six-row table of Riverstone order lines. Type it into a blank sheet starting at cell **A1** (header in row 1, data in rows 2 to 7), or open `companion/ch70/ch70_practice.xlsx` (sheet **Orders**; `ch70_practice.csv` imports into Google Sheets). The products and list prices are the ones in Chapters 10 and 11.

Columns A to E:

| Row | A order_id | B order_date | C customer_name | D category | E product_name |
|---|---|---|---|---|---|
| 2 | 1001 | 2025-01-06 | Sharma Hardware | Storage | Storage Box 10L |
| 3 | 1002 | 2025-01-07 | Metro Mart | Kitchen | Water Bottle 1L |
| 4 | 1003 | 2025-01-09 | Sharma Hardware | Storage | Stackable Bin |
| 5 | 1004 | 2025-01-13 | Coastal Foods | Industrial | Industrial Crate |
| 6 | 1005 | 2025-01-20 | Metro Mart | Storage | Storage Box 25L |
| 7 | 1006 | 2025-02-03 | Sharma Hardware | Storage | Storage Box 10L |

Columns F to J, same rows:

| Row | F quantity | G unit_price | H discount_pct | I net_revenue | J status |
|---|---|---|---|---|---|
| 2 | 25 | 430 | 5 | 10212.5 | Delivered |
| 3 | 40 | 115 | 0 | 4600 | Delivered |
| 4 | 30 | 290 | 5 | 8265 | Cancelled |
| 5 | 20 | 1400 | 10 | 25200 | Delivered |
| 6 | 8 | 750 | 0 | 6000 | Shipped |
| 7 | 12 | 430 | 0 | 5160 | Delivered |

Row 1 holds the headers (the column names above, without the letters).

`net_revenue` is `quantity × unit_price × (1 − discount_pct/100)`, as in Chapter 10: for order 1001, 25 × 430 × 0.95 = 10,212.50. The six lines add up to ₹59,437.50; without the cancelled order 1003 (₹8,265), ₹51,172.50. The book's revenue rule holds here too: **a cancelled order is not a sale**, so every revenue answer below leaves it out. Columns K and L are empty; the macro questions write into K.

**Levels and roles.** Each question carries a level and the roles that usually ask it:

- **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds.
- **DA** data analyst · **BA** business analyst · **BI** BI developer · **AUT** automation (macro and script) roles.

Within each section the core questions run from easier to harder. If you're preparing for a first analyst job, do every Fresher question first, then come back for the Mid ones.

---

## 70.1 Formulas, lookups, and logic

### Q70-001 · Total revenue for one customer, with a minimum-quantity filter

**Level:** Fresher · **Roles:** DA, BA, BI

**Remember it as:** *SUMIFS: sum range first, because the condition pairs can repeat after it. SUMIF: sum range last, because it's optional.*

**Answer in one line:** `SUMIFS` with the sum range first, then one range–condition pair per condition, including the one that drops cancelled orders:

```excel
=SUMIFS(I2:I7, C2:C7, "Sharma Hardware", F2:F7, ">=20", J2:J7, "<>Cancelled")     → 10212.5
```

By hand: Sharma Hardware has three lines. Order 1001 (25 units, Delivered) counts: ₹10,212.50. Order 1003 has 30 units but was cancelled, so `"<>Cancelled"` (not equal to Cancelled) drops it. Order 1006 has only 12 units, so `">=20"` drops it. Without the status condition the formula returns 18477.5, which counts a cancelled order as revenue.

| Tier | What to say |
|---|---|
| Passes | Filter by hand and add up, or use `SUMIF` (it takes only one condition) |
| Strong | `SUMIFS` handles several AND conditions; the sum range comes first, unlike `SUMIF` |
| Extra points | **[+Clarify]** "Total revenue including or excluding cancelled orders?"<br>**[+Validate]** cross-check against a pivot table filtered the same way<br>**[+Scale]** use a Table reference (`Orders[net_revenue]`) so new rows are picked up automatically |

**Likely follow-ups:** Same with `COUNTIFS`? Different in Google Sheets? "Top customer," not a named one?
**Red flag:** filtering by hand instead of a formula; nesting `SUMIF`s for several conditions.
**Learn it in:** Chapter 10, section 10.8 (the `IFS` family); Chapter 11, section 11.2 (criteria in depth).

### Q70-002 · `XLOOKUP` vs `INDEX`/`MATCH` vs `VLOOKUP`

**Level:** Fresher · **Roles:** DA, BA, BI

**Remember it as:** *VLOOKUP only looks right and defaults to "close enough." XLOOKUP looks any direction and defaults to exact.*

**Answer in one line:** `VLOOKUP` looks only to the right and uses approximate match unless you pass `FALSE`; `INDEX`/`MATCH` looks in any direction; `XLOOKUP` does `INDEX`/`MATCH`'s job in one function, exact match by default.

```excel
=XLOOKUP("Storage Box 25L", E2:E7, G2:G7)                  → 750
=INDEX(G2:G7, MATCH("Storage Box 25L", E2:E7, 0))          → 750
=VLOOKUP("Storage Box 25L", E2:G7, 3, FALSE)               → 750
```

`MATCH`'s third argument, `0`, asks for an exact match and returns the position, 5; `INDEX` returns the 5th price. `VLOOKUP`'s `3` is the column number counted from E, and `FALSE` switches off approximate match.

| Tier | What to say |
|---|---|
| Passes | "XLOOKUP is the newer, better version of VLOOKUP" |
| Strong | `VLOOKUP` breaks when a column is inserted (the column number is typed in); always pass `FALSE` for exact match |
| Extra points | **[+Edge cases]** `VLOOKUP`'s silent approximate-match default is the most common source of wrong-but-plausible results<br>**[+Trade-offs]** use `INDEX`/`MATCH` in files that may open in an Excel older than 2021<br>**[+Validate]** handle "not found" on purpose: `XLOOKUP`'s `if_not_found` argument or `IFNA`, not a blanket `IFERROR` (see Q70-008) |

**Likely follow-ups:** Duplicate lookup values? What does `MATCH`'s third argument do? Can plain `VLOOKUP` look to the left?
**Red flag:** claiming `VLOOKUP` can look to the left; not knowing the approximate-match default.
**Learn it in:** Chapter 10, section 10.10 (a first lookup); Chapter 11, sections 11.3 (`IFNA`) and 11.4 (lookups in depth).

### Q70-003 · Absolute vs. relative references

**Level:** Fresher · **Roles:** DA, BA, BI

**Remember it as:** *`$` = stays put when copied. No `$` = shifts with the copy. F4 cycles through all four combinations.*

**Answer in one line:** `B2` shifts when copied (relative); `$B$2` never moves (absolute); `$B2` and `B$2` lock only the column or only the row (mixed).

| Tier | What to say |
|---|---|
| Passes | "`$` locks a reference" |
| Strong | A concrete failure: a tax-rate cell referenced as `B2` instead of `$B$2`, copied down a column, silently multiplies by the wrong cell on every row, with no error |
| Extra points | **[+Edge cases]** copying across *and* down needs a mixed reference in each direction, not one absolute lock<br>**[+Validate]** spot-check the *last* cell after copying, not just the first |

**Likely follow-ups:** What does F4 do? Named ranges vs. absolute references? Table references?
**Red flag:** can't give a concrete example of what breaks.
**Learn it in:** Chapter 10, section 10.6.

### Q70-004 · Classify each order into a size tier

**Level:** Fresher · **Roles:** DA, BA

**Remember it as:** *Nested IFs: most restrictive condition first, or the wrong tier wins.*

**Answer in one line:** check Large before Medium. In `L2`, filled down to `L7`:

```excel
=IF(I2>20000, "Large", IF(I2>5000, "Medium", "Small"))
```

On the practice table this gives Medium, Small, Medium, **Large**, Medium, Medium: order 1004 (₹25,200) is the only Large one, and order 1002 (₹4,600) the only Small one.

| Tier | What to say |
|---|---|
| Common wrong answer | `=IF(I2>5000, "Medium", IF(I2>20000, "Large", "Small"))`: it never returns "Large", because anything over 20,000 is caught by `>5000` first. Order 1004 comes out Medium |
| Passes | The fixed order above, with no mention of what happens at the boundaries |
| Strong | The fixed order, explained: the first true test wins, so the most restrictive goes first |
| Extra points | **[+Edge cases]** what happens at exactly 20,000? `>` excludes it; ask whether the boundary is inclusive<br>**[+Trade-offs]** past two or three tiers, switch to `IFS` or a lookup table with approximate match |

**Likely follow-ups:** Same with `IFS`? With a lookup table? The tier boundary changes next quarter?
**Red flag:** ordering the conditions least restrictive first (exactly the wrong answer above); not testing the boundaries.
**Learn it in:** Chapter 10, section 10.8 (`IF`, `IFS`); Chapter 11, section 11.4 (approximate match: bands and tiers).

### Q70-005 · `SUMPRODUCT`, and when to reach for it over `SUMIFS`

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *SUMPRODUCT multiplies row by row, then adds: quantity × price × (1 − discount) for every row, summed.*

**Answer in one line:** it multiplies arrays item by item and adds the results, so it can total a calculation without a helper column:

```excel
=SUMPRODUCT(F2:F7, G2:G7, 1-H2:H7/100)                                  → 59437.5
=SUMPRODUCT(F2:F7 * G2:G7 * (1-H2:H7/100) * (J2:J7<>"Cancelled"))       → 51172.5
```

The first line works row by row: 25 × 430 × 0.95 = 10,212.50 for order 1001, 40 × 115 × 1 = 4,600 for order 1002, and so on, then adds all six: the same 59,437.50 as `=SUM(I2:I7)`. The second line multiplies by one more array, `(J2:J7<>"Cancelled")`, which is TRUE (1) for a valid line and FALSE (0) for the cancelled one, so order 1003 contributes nothing. It matches `=SUMIFS(I2:I7, J2:J7, "<>Cancelled")`, 51172.5. (If you've read Chapter 35: with two arrays, `SUMPRODUCT` is exactly a dot product.)

| Tier | What to say |
|---|---|
| Passes | "It multiplies things and adds them up" |
| Strong | It's array arithmetic: no helper column needed, and the result reconciles to the helper-column total |
| Extra points | **[+Trade-offs]** for simple conditions `SUMIFS` is easier to read; `SUMPRODUCT` earns its place for weighted totals or OR across columns, which `SUMIFS` can't express<br>**[+Edge cases]** every array must be the same size, or it returns `#VALUE!` |

**Likely follow-ups:** A weighted average with `SUMPRODUCT`? The old Excel array-formula version (`{}`)? The Python equivalent?
**Red flag:** no mention of it being array arithmetic; a total that quietly includes cancelled orders.
**Learn it in:** Chapter 11, section 11.2 (`SUMPRODUCT`: conditions the `IFS` family can't express).

### Rapid-fire, 70.1

Roles: DA, BA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-006 | `COUNT` vs `COUNTA` vs `COUNTBLANK`? | Numeric cells only / any non-empty cell / empty cells | **[+Edge cases]** a formula returning `""` looks empty but isn't; `COUNTA` still counts it | Fresher · 10.7 |
| Q70-007 | Formula for "days since this order"? | `=TODAY()-B2`, formatted as a number, not a date | **[+Edge cases]** if it shows as a date, reformat as General or Number | Fresher · 10.9 |
| Q70-008 | `IFERROR` vs `IFNA`? | Catches every error type / catches only `#N/A` | **[+Business]** `IFERROR` used broadly can hide a real bug behind a friendly blank | Fresher · 11.3 |
| Q70-009 | `FILTER` and `UNIQUE` together? | `=UNIQUE(FILTER(C2:C7, D2:D7="Storage"))` spills Sharma Hardware, Metro Mart | **[+Edge cases]** the cells it spills into must be empty, or `#SPILL!` | Fresher · 11.6 |
| Q70-010 | `TEXT` function, one use? | `=TEXT(B2, "MMMM")` → January | **[+Edge cases]** the result is text now: no more date arithmetic on it | Fresher · 10.9 |
| Q70-011 | Named range: why use one? | A reusable name for a cell or range, e.g. `TaxRate` for `$B$2` | **[+Scale]** name a Table column (`Orders[net_revenue]`) rather than a fixed range, so it grows with the data | Fresher · 10.6 |
| Q70-012 | A common cause of `#REF!`? | A formula refers to a cell, row or column that's since been deleted | **[+Validate]** trace precedents to find the source, not just the symptom | Fresher · 10.6 |
| Q70-013 | Flag near-duplicate names (spacing, case)? | A helper column of cleaned names, `=TRIM(LOWER(C2))`, then `=COUNTIF(clean_range, TRIM(LOWER(C2)))>1` | **[+Business]** near-duplicates quietly split one customer into two rows of a pivot | Mid · 10.9, 10.8 |
| Q70-014 | Conditional formatting "Stop If True"? | When a rule with Stop If True matches, the rules below it aren't applied to that cell (rule order goes beyond Chapter 10) | **[+Edge cases]** without it, formats that don't clash (fill and font colour) stack; when they clash, the rule higher in the list wins, so order the rules on purpose | Mid · 10.12 |
| Q70-015 | Table (Ctrl+T) vs. a plain range? | Formulas and formatting extend as rows are added; structured references | **[+Scale]** building dashboards on Tables, not fixed ranges, is the easiest way to survive new data | Fresher · 10.11 |

---

## 70.2 Pivot tables and data analysis

### Q70-016 · Pivot grand total doesn't match a manual `SUM`

**Level:** Fresher · **Roles:** DA, BA, BI

**Remember it as:** *Refresh, then filters, then aggregation type: in that order.*

**Answer in one line:** three usual suspects, checked in order: the source range doesn't cover new rows → a hidden filter or slicer is active → the value field defaulted to Count instead of Sum (one stray text value in a numeric column does this).

| Tier | What to say |
|---|---|
| Passes | "Check the source range" |
| Strong | The three suspects above, in order |
| Extra points | **[+Validate]** refresh first, then check for active filters, before assuming the data is wrong<br>**[+Scale]** build the pivot on a Table to remove the first cause for good |

**Likely follow-ups:** Change the default summary? Calculated field vs. calculated item? Show values as % of total?
**Red flag:** jumping to "the data must be wrong" without checking the pivot's own settings first.
**Learn it in:** Chapter 11, section 11.5 (Refresh, and the traps that come with it).

### Q70-017 · Revenue by customer by month, with a running total

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *"Show Values As → Running Total In": the pivot does it natively; don't build it by hand.*

**Answer in one line:** customer in Rows, month (grouped from the date field) in Columns, net revenue in Values twice, the second set to **Show Values As → Running Total In** by month.

| Tier | What to say |
|---|---|
| Passes | "Customer in Rows, months in Columns, revenue in Values" (misses the running total) |
| Strong | Add the field a second time and set **Show Values As → Running Total In** |
| Extra points | **[+Edge cases]** grouping by Months alone across two years merges January 2024 with January 2025 unless Years is grouped too<br>**[+Validate]** the running total's last value should equal a plain `SUMIFS` for that customer |

**Likely follow-ups:** A slicer for region? Grouping vs. a calculated field? % of the customer's own annual total instead?
**Red flag:** not knowing Show Values As exists; building the running total with manual formulas.
**Learn it in:** Chapter 11, section 11.5 (Grouping dates; More ways to show values).

### Q70-018 · A calculated field's aggregation trap

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *A calculated field runs AFTER the summing, not before. Averaging a ratio this way is almost always wrong.*

**Answer in one line:** a calculated field's formula works on the already-summed totals in each cell, not row by row: fine for `net_revenue / quantity`, wrong if you expect it to average a percentage column.

| Tier | What to say |
|---|---|
| Passes | "A formula field inside the pivot" |
| Strong | It computes on the totals, which is right for a ratio of sums and wrong for anything that must be worked out row by row first |
| Extra points | **[+Edge cases]** the classic case: the average of `discount_pct` across lines ≠ total discount ÷ total list value<br>**[+Validate]** check a ratio field's grand total against a hand calculation from the raw totals |

**Likely follow-ups:** Calculated item vs. calculated field? Does DAX have the same trap? *(Yes: it's why `CALCULATE` and filter context matter, section 70.7.)*
**Red flag:** not knowing that calculated fields work on sums.
**Learn it in:** Chapter 11, section 11.5 (Calculated fields, and why ratios need care).

### Rapid-fire, 70.2

Roles: DA, BA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-019 | Slicer vs. filter? | A visual control that can drive several pivots and charts at once / affects only its own pivot | **[+Business]** slicers make a report usable for a non-technical viewer | Fresher · 11.5 |
| Q70-020 | Top 3 customers by revenue in a pivot? | **Value Filters → Top 10…**, changed to 3, on the summed field | **[+Edge cases]** customers tied at the cut-off are all included, so "Top 3" can show 4 rows; say how you'd break the tie (e.g. by order count) | Fresher · 11.5 |
| Q70-021 | Pivot chart vs. a normal chart on pivot data? | Linked, updates with the pivot / needs rebuilding if the pivot's shape changes | **[+Trade-offs]** pivot charts are easier to maintain, harder to customize fully | Mid · 11.5 |
| Q70-022 | Refresh all pivots at once? | **Data → Refresh All**; in VBA, `ThisWorkbook.RefreshAll` (one line; not covered in Chapter 19) | **[+Scale]** set "Refresh data when opening the file" so nobody sees stale numbers | Mid · 11.5, 11.7 |
| Q70-023 | "(blank)" appears in the row labels: why? | Some source rows have an empty value in that field; the pivot groups them under (blank) instead of dropping them | **[+Validate]** count them and trace them to the source rows: a data-quality signal (Chapter 11's pivot found ₹2,04,502.50 of revenue with no rep this way) | Mid · 11.5 |
| Q70-024 | Each customer's revenue as a % of the grand total? | Add revenue again → **Show Values As → % of Grand Total** | **[+Business]** the fastest way to answer "who matters most" with no manual maths | Fresher · 11.5 |
| Q70-025 | A pivot average, with blanks in the data? | Blanks are left out of the count, not treated as zero | **[+Edge cases]** text mixed into a numeric column can flip the field to Count instead (Q70-016) | Mid · 11.5 |
| Q70-026 | "Days between first and most recent order" per customer? | Customer in Rows, `order_date` in Values twice (Min and Max), then Max − Min in a plain formula beside the pivot (`GETPIVOTDATA`); or skip the pivot: `=MAXIFS(B2:B7, C2:C7, "Sharma Hardware") - MINIFS(B2:B7, C2:C7, "Sharma Hardware")` → 28 | **[+Edge cases]** a calculated field can't do this, because it works on sums (Q70-018). If you've read Part 4, it's a spreadsheet version of Chapter 36's recency features (section 36.6) | Mid · 11.2, 11.5 |

---

## 70.3 Power Query

### Q70-027 · Combine 12 monthly files into one clean table

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *"From Folder" once, refresh forever. Copy-paste once, redo forever.*

**Answer in one line:** **Get Data → From Folder** → **Combine & Transform** stacks every file with matching columns into one table; clean once in the Power Query Editor, and every step replays on refresh, including on a 13th file dropped into the folder later.

| Tier | What to say |
|---|---|
| Passes | "Copy-paste all 12 files into one sheet" (works once, not repeatable) |
| Strong | From Folder + Combine & Transform, with the cleaning steps recorded once |
| Extra points | **[+Scale]** the whole point: next month's refresh needs no manual work<br>**[+Edge cases]** select columns by name, not position, so a reordered column in one file doesn't silently misalign<br>**[+Validate]** check that the combined row count equals the sum of the 12 files' row counts, to catch a skipped file |

**Likely follow-ups:** Different column orders across files? A file that fails to load? How does this compare with a VBA macro doing the same thing?
**Red flag:** manual copy-paste as the final answer, no mention of repeatability.
**Learn it in:** Chapter 11, section 11.7 (compare with Chapter 19, section 19.6, the VBA version).

### Q70-028 · Power Query "Merge" vs. "Append"

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *Append = SQL UNION ALL (stack rows, keep duplicates). Merge = SQL JOIN (add columns).*

**Answer in one line:** Append stacks tables (same columns, more rows, every row kept); Merge joins tables side by side on a key (new columns), with the join kinds SQL has: left, right, inner, full outer, anti.

| Tier | What to say |
|---|---|
| Passes | "They both combine tables" |
| Strong | Append = `UNION ALL`, same columns; Merge = join on a matching key, and its join-kind list is Chapter 12's SQL joins |
| Extra points | **[+Edge cases]** a Merge on a key that repeats on the right side fans rows out, exactly Chapter 12's fan-out trap<br>**[+Validate]** check the row count after a Merge against what you expect |

**Likely follow-ups:** An anti-join in Power Query? What does "expand" do after a Merge? The SQL equivalent, and why not plain `UNION`?
**Red flag:** confusing Merge and Append; saying Append is `UNION` (which removes duplicates).
**Learn it in:** Chapter 11, section 11.7 (Step 5, the merge; Power Query in depth, Append); Chapter 12, sections 12.10 (the fan-out trap) and 12.12 (`UNION` vs `UNION ALL`).

### Rapid-fire, 70.3

Roles: DA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-029 | What's a Power Query "step"? | A named, reorderable transformation recorded in Applied Steps; each step runs on the previous step's output | **[+Edge cases]** renaming a column, then referring to the old name in a later step, breaks the query | Fresher · 11.7 |
| Q70-030 | Split "City, State" into two columns? | **Split Column → By Delimiter** (comma) | **[+Edge cases]** when some values hold extra commas, choose **Split at: Right-most delimiter** so the extra commas stay in the first part; trim spaces first | Fresher · 11.7 |
| Q70-031 | What does "Unpivot Columns" do? | Wide data → long data; Power Query's version of pandas' `melt` | **[+Business]** exports arrive wide (for people); analysis wants long, so this is often the first real cleaning step | Fresher · 11.7, 18.8 |
| Q70-032 | Change a column's data type: why does it matter? | Right-click the header → **Change Type**; later number or date steps fail on a column still typed as text | **[+Validate]** look for new errors on rows that didn't convert | Fresher · 11.7 |
| Q70-033 | "Close & Load" vs. "Close & Load To…"? | Loads a table to a new sheet / lets you choose: table, PivotTable, or connection only | **[+Scale]** "Only Create Connection" for staging queries keeps the workbook lean | Fresher · 11.7 |

---

## 70.4 Google Sheets: QUERY, ARRAYFORMULA, and IMPORTRANGE

### Q70-034 · Total revenue by category, sorted, with `QUERY`

**Level:** Mid · **Roles:** DA, BA

**Remember it as:** *QUERY is SQL in a spreadsheet: column letters instead of names, otherwise the same rules.*

**Answer in one line:**

```excel
=QUERY(A1:J7,
  "select D, sum(I)
   where J <> 'Cancelled'
   group by D
   order by sum(I) desc
   label sum(I) 'net_revenue'", 1)
```

The result spills into a small table under the headers `category` and `net_revenue`: Industrial 25200, Storage 21372.5, Kitchen 4600. Storage is orders 1001, 1005 and 1006 (10,212.50 + 6,000 + 5,160); the cancelled order 1003 is left out by `where`. The final `1` says the range has one header row. `group by` is required whenever you aggregate alongside a column you don't aggregate: the same rule as SQL's `GROUP BY` in Chapter 12.

| Tier | What to say |
|---|---|
| Passes | "I'd build a pivot table instead" (dodges the `QUERY` question) |
| Strong | The formula above, explaining `select`, `where`, `group by`, `order by` and `label` |
| Extra points | **[+Edge cases]** columns are named by their letter in the range, not by header, and a column inserted later shifts the letters<br>**[+Trade-offs]** a pivot is faster for a one-off; `QUERY` wins when the result must feed another formula or chart |

**Likely follow-ups:** Add a date range to the `where`? The `LIMIT` equivalent? How is this different from a pivot's output?
**Red flag:** not knowing `QUERY` exists; confusing column letters with header names; a total that includes cancelled orders.
**Learn it in:** Chapter 11, section 11.10 (QUERY); Chapter 12, section 12.9 (the `GROUP BY` rule).

### Q70-035 · What `ARRAYFORMULA` does, and when it's actually needed

**Level:** Mid · **Roles:** DA, BA, AUT

**Remember it as:** *Functions that already return one answer from a whole range don't need it. Per-row formulas do.*

**Answer in one line:** it makes a per-row formula (`IF`, `&`, arithmetic) work on whole ranges, so one cell fills a column; functions that already return one answer from a whole range (`SUM`, `SUMIFS`, `FILTER`, `UNIQUE`, `QUERY`) don't need it.

```excel
=ARRAYFORMULA(IF(D2:D="", "", IF(D2:D="Storage", "Yes", "No")))
```

In `K2` this fills Yes, No, Yes, No, Yes, Yes down to row 7 and leaves every row below blank. The outer `IF(D2:D="", "", …)` is Chapter 11's guard: without it, the open-ended range `D2:D` would write "No" down every empty row of the sheet.

| Tier | What to say |
|---|---|
| Passes | "It applies a formula to a whole range" |
| Strong | Explains *why*: some functions already work on ranges; plain `IF`, `&` and arithmetic don't, unless wrapped |
| Extra points | **[+Business]** one `ARRAYFORMULA` over an open-ended range covers rows added later, which fixes the most common way a shared sheet quietly breaks: a new row below the last filled-down formula<br>**[+Edge cases]** open-ended ranges can be slow on a very large sheet |

**Likely follow-ups:** How is it different from Excel's dynamic arrays? Why doesn't `SUMIFS` expand inside `ARRAYFORMULA`, and what would you use instead (`SUMIF`, or `QUERY`)?
**Red flag:** not knowing why some formulas need it and others don't.
**Learn it in:** Chapter 11, section 11.10 (ARRAYFORMULA).

### Rapid-fire, 70.4

Roles: DA, BA and AUT for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-036 | `IMPORTRANGE`, and its setup trap? | Pulls a range from another Sheets file by URL; needs a one-time "Allow access" click | **[+Edge cases]** if access to the source is removed, every `IMPORTRANGE` that reads it breaks (`#REF!`) | Fresher · 11.10 |
| Q70-037 | Pull live external data into Sheets? | `GOOGLEFINANCE` for currencies and stocks; `IMPORTXML`/`IMPORTHTML` for public web pages; Apps Script's `UrlFetchApp` for an API that needs a key | **[+Trade-offs]** `IMPORT…` functions are simplest but break when the page changes its layout | Mid · 11.11, 19.13 |
| Q70-038 | `FILTER` vs. `QUERY`'s `where`? | Filters rows with a test and combines with other array formulas / SQL-like, can filter, aggregate and sort in one formula | **[+Trade-offs]** `FILTER` alone is easier to read; `QUERY` avoids nesting two formulas for filter-plus-total | Mid · 11.6, 11.10 |
| Q70-039 | Protect a shared sheet from accidental overwrites? | **Data → Protect sheets and ranges**, limiting who can edit the formula cells | **[+Business]** the cheapest fix for the most common cause of "why are the numbers wrong" on a team sheet | Mid · 10.14 |

---

## 70.5 VBA and Excel macros

### Q70-042 · The VBA object model

**Level:** Mid · **Roles:** AUT, DA, BA

**Remember it as:** *Application → Workbooks → Worksheets → Range. Biggest to smallest, like folders inside folders.*

**Answer in one line:** `Application` (Excel itself) → `Workbooks` (every open file) → one `Workbook` → `Worksheets` → one `Worksheet` → `Range` (one or more cells; `Cells(row, column)` is one cell by number). Full form: `Application.Workbooks("Sales.xlsx").Worksheets("Orders").Range("A1")`; VBA lets you drop the parts it can assume.

| Tier | What to say |
|---|---|
| Passes | "They're all objects in VBA" |
| Strong | The nesting above, with a fully qualified example |
| Extra points | **[+Edge cases]** relying on "the active sheet" is a common cause of a macro that works when run by hand but breaks from a button on another tab<br>**[+Scale]** in any macro you'll reuse, qualify `Range` and `Cells` with an explicit worksheet |

**Likely follow-ups:** `ActiveSheet` vs. `ThisWorkbook.Worksheets("Orders")`? What does `With` do? Referring to a closed workbook?
**Red flag:** relying entirely on whatever sheet and workbook happen to be active.
**Learn it in:** Chapter 19, section 19.5.

### Q70-040 · Find the last used row

**Level:** Mid · **Roles:** AUT, DA

**Remember it as:** *Start from the bottom and go up. Starting from the top and going down stops at the first gap.*

**Answer in one line:** go to the last row of the sheet in column A and press Ctrl+Up, in code:

```vb
Sub ShowLastRow()
    Dim lastRow As Long
    lastRow = Cells(Rows.Count, "A").End(xlUp).Row
    Debug.Print "last row: " & lastRow
End Sub
```

On the practice table, the Immediate window shows:

```
last row: 7
```

`Rows.Count` is the number of the sheet's last row; `Cells(Rows.Count, "A")` is that cell in column A; `.End(xlUp)` jumps up to the first filled cell; `.Row` is its row number. `.End(xlDown)` from `A1` stops at the *first* blank cell instead, so any gap in the column gives too small a number.

| Tier | What to say |
|---|---|
| Common wrong answer | `Range("A1").End(xlDown).Row`: wrong as soon as the column has a gap |
| Passes | The bottom-up line, without saying why it's safer |
| Strong | The bottom-up line, with the reason: a gap can't stop it |
| Extra points | **[+Scale]** `Rows.Count` works whatever the sheet size or file format<br>**[+Validate]** `Debug.Print lastRow` on a small table whose answer you know, like this one |

**Likely follow-ups:** The last used column instead? Data that might sit below a gap? The same thing in Python?
**Red flag:** the top-down version as the final answer, with no mention of the gap problem.
**Learn it in:** Chapter 19, section 19.5 (the five things you'll write constantly).

### Q70-041 · Fix the broken macro (infinite loop)

**Level:** Mid · **Roles:** AUT, DA

**Remember it as:** *A `Do While` loop with no increment is a promise to run forever.*

The interviewer hands you this macro, meant to write "Large" in column K beside every order over ₹20,000:

```vb
' BROKEN: never finishes
Sub MarkLargeOrders()
    Dim i As Integer
    i = 2
    Do While Cells(i, 1).Value <> ""
        If Cells(i, 9).Value > 20000 Then
            Cells(i, 11).Value = "Large"
        End If
    Loop
End Sub
```

**What's wrong:** `i` never increases, so `Cells(i, 1)` is always `A2`, the loop's test never becomes false, and Excel hangs (**Ctrl+Break** stops it).

```vb
' FIXED
Sub MarkLargeOrders()
    Dim i As Long, lastRow As Long
    lastRow = Cells(Rows.Count, "A").End(xlUp).Row
    For i = 2 To lastRow
        If Cells(i, 9).Value > 20000 Then Cells(i, 11).Value = "Large"
    Next i
End Sub
```

Run on the practice table, it writes **Large** in `K5` (order 1004, ₹25,200) and leaves the other cells of column K empty. `For i = 2 To lastRow … Next i` adds 1 to `i` on every pass and stops after the last row, so it can't run forever.

| Tier | What to say |
|---|---|
| Diagnosis | The missing increment inside the `Do While` loop |
| Fix | A bounded `For…Next` loop instead, with `lastRow` worked out first |
| Extra points | **[+Edge cases]** also switch `Integer` to `Long`: `Integer` stops at 32,767, and many files have more rows<br>**[+Scale]** cell by cell is slow on big ranges; read into an array, loop in memory, write back once (Q70-043)<br>**[+Validate]** test on the six-row practice table first, where you know the answer by hand |

**Likely follow-ups:** Speed this up on 50,000 rows? The array version? What if column I holds text instead of a number?
**Red flag:** adding an increment but not checking that the loop stops at the last row (or can run past it).
**Learn it in:** Chapter 19, section 19.4 (loops; `Long` versus `Integer`).

### Q70-043 · Making a VBA macro run faster

**Level:** Mid · **Roles:** AUT

**Remember it as:** *Arrays not cells first (the biggest win), then screen updating off and calculation manual; restore both at the end.*

**Answer in one line:** read the range into an array, loop in memory, and write back in one block; set `Application.ScreenUpdating = False` and `Application.Calculation = xlCalculationManual` at the start and restore both at the end; never `Select` or `Activate`.

| Tier | What to say |
|---|---|
| Passes | "Avoid unnecessary loops" (no concrete technique) |
| Strong | The three changes above, biggest win first |
| Extra points | **[+Scale]** the array rewrite is often 10–100 times faster on tens of thousands of rows, not a marginal gain<br>**[+Validate]** time it with `Timer` before and after each change: measured, not assumed<br>**[+Edge cases]** restore screen updating and calculation even when an error stops the macro (an error handler), or the workbook is left stuck in manual calculation |

**Likely follow-ups:** Show the read–loop–write pattern. What goes wrong if you forget to restore `ScreenUpdating`? How would pandas do it?
**Red flag:** no mention of arrays, screen updating or calculation mode.
**Learn it in:** Chapter 19, section 19.10 (Making macros fast).

### Rapid-fire, 70.5

Roles: AUT for every row; DA and BA for the Mid rows.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-044 | Personal Macro Workbook: why use it? | A hidden `PERSONAL.XLSB` that opens with Excel, so a macro runs from any file | **[+Business]** for your own tools used across many reports, not tied to one workbook | Mid · 19.2 |
| Q70-045 | `On Error Resume Next`: the risk? | Skips a line that errors and carries on | **[+Edge cases]** used broadly it swallows real bugs too; keep it to one line and follow it with `On Error GoTo 0` | Mid · 19.6, 19.9 |
| Q70-046 | A custom worksheet function (UDF): its limits? | A `Function` instead of a `Sub`, returning a value into the calling cell | **[+Trade-offs]** it can't change other cells or formatting; anything beyond a calculation needs a `Sub` | Senior · 19.8 |
| Q70-047 | Workbook-level vs. worksheet-level events? | Whole-file events (`Workbook_Open`, `Workbook_BeforeSave`) / one-sheet events (`Worksheet_Change`); mostly beyond Chapter 19 | **[+Edge cases]** `Worksheet_Change` code that writes to its own sheet triggers itself again unless `Application.EnableEvents = False` | Senior · 19.10 |
| Q70-048 | Consolidate every sheet into one summary? | Loop `ThisWorkbook.Worksheets` with `For Each`, skip the summary sheet by name, append each sheet's used range | **[+Scale]** exclude by name, not by position: sheets get renamed and reordered | Senior · 19.4, 19.6 |
| Q70-049 | UserForm: when to build one? | A custom dialog for structured, validated input from a non-technical user | **[+Business]** trades build time for far fewer "typed the date in the wrong cell" requests | Senior · 19.8 |
| Q70-050 | Debug a VBA macro step by step? | Breakpoint (F9) → run (F5) → step (F8), watching the Locals window or `Debug.Print` | **[+Signpost]** describe it as a workflow in steps: where you stop, what you watch, what you expect to see | Senior · 19.9 |
| Q70-051 | Save the active sheet as PDF and email it through Outlook? | `ActiveSheet.ExportAsFixedFormat Type:=xlTypePDF, Filename:=pdfPath`, then `CreateObject("Outlook.Application")` → a `MailItem` → `.Attachments.Add pdfPath` → `.Send` | **[+Business]** one of the highest-value automations in a real job, and Chapter 19's own project | Senior · 19.6, 19.7 |
| Q70-071 | VBA or Office Scripts? | VBA: desktop Excel, the full object model, Outlook / Office Scripts: Excel on the web, TypeScript, runs in Power Automate flows | **[+Trade-offs]** pick by where the file lives and who runs it | Mid · 19.11 |

---

## 70.6 Google Apps Script

### Q70-052 · Read a range and write results back, without looping cell by cell

**Level:** Mid · **Roles:** AUT

**Remember it as:** *Every getValue() or setValue() is a round trip to Google's servers. Batch them, or the clock (and the quota) runs out.*

The interviewer shows the slow version and asks for a faster one that does the same job:

```javascript
// SLOW: one round trip per cell
function markLargeSlow() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Orders');
  for (let i = 2; i <= sheet.getLastRow(); i++) {
    if (sheet.getRange(i, 9).getValue() > 20000) sheet.getRange(i, 11).setValue('Large');
  }
}
```

On the practice table it reads column I six times, one cell at a time, and writes once, to `K5`.

```javascript
// FAST: one read, work in memory, one write
function markLarge() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Orders');
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;                                    // header only: nothing to do
  const values = sheet.getRange(2, 9, lastRow - 1, 3).getValues();   // I2:K, one read
  const flags = values.map(row => [row[2]]);                  // start from what K already holds
  for (let r = 0; r < values.length; r++) {
    if (values[r][0] > 20000) flags[r][0] = 'Large';
  }
  sheet.getRange(2, 11, flags.length, 1).setValues(flags);    // column K, one write
  Logger.log(`${flags.length} rows checked`);
}
```

The **Execution log** shows:

```
6 rows checked
```

and column K ends exactly as the slow version leaves it: **Large** in `K5`, the other cells unchanged.

- **`getRange(2, 9, lastRow - 1, 3)`** is row 2, column 9 (I), all the data rows, three columns: I, J and K. Reading K as well is what lets the fast version keep whatever K already holds, as the slow one does.
- **`values.map(row => [row[2]])`** makes a one-column copy of K: `row[2]` is the third column read, counting from 0.
- The loop changes only the rows over 20,000, and **`setValues(flags)`** writes column K once.
- **`if (lastRow < 2) return;`** stops on a sheet with only a header row, where `lastRow - 1` would ask for 0 rows and `getRange` would fail.

| Tier | What to say |
|---|---|
| Passes | The slow version: correct, but on a large sheet it runs into the six-minute limit |
| Strong | The batch version: one `getValues()`, work in memory, one `setValues()` |
| Extra points | **[+Scale]** the Apps Script version of Q70-043's VBA array pattern, for the same reason: fewer round trips<br>**[+Edge cases]** a batch write that sets `""` in the rows it doesn't flag would wipe whatever column K held; and a header-only sheet needs the guard<br>**[+Validate]** run both versions on the practice table and compare column K |

**Likely follow-ups:** What's the execution time limit, and what if a job really needs longer? Run this every night?
**Red flag:** cell-by-cell reads and writes with no mention of the time limit.
**Learn it in:** Chapter 19, section 19.12 (Read and write in batches); `map` and `=>` in section 19.13.

### Q70-053 · Fix the broken script (duplicate emails on every trigger run)

**Level:** Mid · **Roles:** AUT

**Remember it as:** *No "already sent" flag means every run re-sends to everyone, forever.*

The **Confirmations** sheet of the practice workbook has `order_id`, `customer_name`, `email` and `status` in columns A to D. A daily trigger runs this:

```javascript
// BROKEN: no memory of what's already been sent
function sendConfirmations() {
  const data = SpreadsheetApp.getActive().getSheetByName('Confirmations').getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    MailApp.sendEmail(data[i][2], 'Order confirmed', 'Thanks for your order!');
  }
}
```

**What's wrong:** nothing records which rows were already emailed, so every run emails every customer again.

```javascript
// FIXED: a per-row "Sent" flag, checked and set
function sendConfirmations() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Confirmations');
  const data = sheet.getDataRange().getValues();
  const statusCol = 4;                                  // column D
  let sent = 0;
  for (let i = 1; i < data.length; i++) {               // row 0 is the header
    if (data[i][statusCol - 1] !== 'Sent') {
      MailApp.sendEmail(data[i][2], 'Order confirmed', 'Thanks for your order!');
      sheet.getRange(i + 1, statusCol).setValue('Sent');
      sent++;
    }
  }
  Logger.log(`${sent} emails sent`);
}
```

Run twice on the three practice rows, the Execution log shows:

```
3 emails sent
0 emails sent
```

`data[i][2]` is the email (column C, counted from 0); `data[i][statusCol - 1]` is column D. `getRange(i + 1, statusCol)` is the same cell in sheet numbering: grid row `i` is sheet row `i + 1`, because the grid counts from 0 and the sheet from 1.

| Tier | What to say |
|---|---|
| Diagnosis | No record of rows already processed |
| Fix | A "Sent" flag, checked before sending and set straight after |
| Extra points | **[+Validate]** run it twice on test data: the second run must send zero<br>**[+Edge cases]** a failure between `sendEmail` and `setValue` re-sends that one row next time, and two overlapping runs can both send; a lock (Apps Script's `LockService`, beyond this book) stops the overlap<br>**[+Business]** duplicate customer emails are the automation bug customers notice |

**Likely follow-ups:** Set up the time-driven trigger itself? What happens after a failure halfway through? `MailApp` or `GmailApp` here?
**Red flag:** not seeing the missing "already processed" record as the root cause.
**Learn it in:** Chapter 19, section 19.13 (Triggers; an acknowledgement email).

### Rapid-fire, 70.6

Roles: AUT for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-054 | `MailApp` vs. `GmailApp`? | Simple, send-only / can also read, search and label, as the user's own Gmail | **[+Trade-offs]** `MailApp` is enough for simple outgoing notifications | Mid · 19.13 |
| Q70-055 | Time-driven vs. "on edit" trigger? | Runs on a schedule / runs when a user edits a cell | **[+Edge cases]** the simple `onEdit(e)` can't send email; that needs an *installable* trigger | Mid · 19.13 |
| Q70-056 | Call an external API from Apps Script? | `UrlFetchApp.fetch(url, options)`, then `JSON.parse()` on the reply | **[+Business]** how a Sheet syncs with a CRM with no server of its own (Chapter 78 goes deeper) | Mid · 19.13 |
| Q70-057 | The six-minute limit: what if a job needs longer? | Save how far it got (e.g. the last row done) with `PropertiesService`, and let the next run carry on from there | **[+Scale]** process in batches that each finish well inside the limit | Mid · 19.12, 19.13 |
| Q70-058 | `SpreadsheetApp.flush()`: when is it needed? | It applies all pending changes now, instead of when the script ends (beyond Chapter 19) | **[+Edge cases]** use it when a user or another script must see a change mid-run, such as a progress cell | Mid · 19.12 |

---

## 70.7 DAX and Power BI modeling

### Q70-059 · Calculated column vs. measure

**Level:** Fresher · **Roles:** BI, DA

**Remember it as:** *Column = stored, one value per row, computed at refresh. Measure = computed live, changes with whatever's filtered.*

**Answer in one line:** a calculated column is computed row by row and stored in the model; a measure is computed when a visual asks for it, under whatever filters (a slicer, a date range) apply at that moment.

| Tier | What to say |
|---|---|
| Passes | "They're both formulas in Power BI" |
| Strong | Net revenue per order line (row-level, stored) is a column; total or average revenue across whatever's filtered is a measure |
| Extra points | **[+Trade-offs]** logic about one row → column; anything that adds up or responds to filters → measure<br>**[+Scale]** calculated columns take memory on large tables, because every row stores a value; measures store nothing<br>**[+Business]** a measure respects whatever the viewer has filtered, with no extra work |

**Likely follow-ups:** Filter context vs. row context? What does `CALCULATE` do? Would you ever need both for the same value?
**Red flag:** treating them as interchangeable; not knowing the storage difference.
**Learn it in:** Chapter 16, section 16.4 (Measures and calculated columns).

### Q70-060 · Revenue this month vs. the same month last year

**Level:** Mid · **Roles:** BI, DA

**Remember it as:** *CALCULATE changes the filter context. Everything else in DAX time intelligence is CALCULATE wearing a costume.*

**Answer in one line:** two measures, the same as Chapter 16's:

```dax
Revenue LY = CALCULATE ( [Net Revenue], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
```

```dax
YoY Growth % = DIVIDE ( [Net Revenue] - [Revenue LY], [Revenue LY] )
```

In Chapter 16's model, the January 2025 row reads Net Revenue ₹8,51,95,521, Revenue LY ₹6,40,63,515 (January 2024) and YoY Growth % **33.0%**, and the same sums in SQL on `riverstone_full` agree.

| Tier | What to say |
|---|---|
| Passes | "You'd filter to last year and compare" (in words, no DAX) |
| Strong | The two measures above, explaining that `CALCULATE` changes the filter context and that time intelligence needs a marked date table |
| Extra points | **[+Signpost]** "Two measures: last year first, then the growth on top of it"<br>**[+Edge cases]** `DIVIDE`, not `/`: `Revenue LY` is blank for the first year of data, and `DIVIDE` returns blank instead of an error<br>**[+Validate]** check one month you can compute another way (SQL, a pivot) before trusting the whole matrix |

**Likely follow-ups:** `SAMEPERIODLASTYEAR` vs. `DATEADD`? What does a date table need to work? What does `REMOVEFILTERS` do inside `CALCULATE` (Q70-064)?
**Red flag:** using `/` instead of `DIVIDE`; no mention of the date table; can't say what `CALCULATE` does.
**Learn it in:** Chapter 16, sections 16.5 (`CALCULATE`) and 16.6 (Time intelligence).

### Q70-061 · Star schema, and why it beats one flat table

**Level:** Mid · **Roles:** BI, DA

**Remember it as:** *One fact table (events), several dimension tables (who, what, when) around it, like a star.*

**Answer in one line:** a central fact table (one row per event, holding the numbers and the keys) surrounded by dimension tables (Customer, Product, Date) in one-to-many relationships: smaller, faster for DAX, and one clear date table for time intelligence.

| Tier | What to say |
|---|---|
| Passes | "It's a way of organizing tables with relationships" |
| Strong | The fact/dimension structure above, and why it beats a flat table |
| Extra points | **[+Scale]** a flat table repeats every attribute on every fact row, which bloats memory and muddles how filters flow<br>**[+Trade-offs]** for a very small dataset, flat can be fine: the star's benefits grow with the data and the time-intelligence needs<br>**[+Evidence]** from your own work, if it's true for you: "On my last report, moving from one flat table to a star schema made the pages load noticeably faster, with no measure rewritten" |

**Likely follow-ups:** A snowflake schema: when? Many-to-many relationships? A bridge table?
**Red flag:** no mention of facts vs. dimensions; claiming flat is always simpler.
**Learn it in:** Chapter 16, section 16.3 (and Chapter 28, section 28.9, for the warehouse version of the same idea).

### Q70-062 · Row-level security (RLS): each manager sees only their own region

**Level:** Senior · **Roles:** BI

**Remember it as:** *RLS is enforced by the service, per signed-in user: not a filter you apply before publishing.*

**Answer in one line:** under **Modeling → Manage roles**, define a role with a DAX filter such as `UserRegion[email] = USERPRINCIPALNAME ()` on a users-and-regions table; once published, each user sees the report filtered to their own identity.

| Tier | What to say |
|---|---|
| Passes | "You'd filter the data by region before publishing" (that isn't RLS at all) |
| Strong | The role and its DAX filter, applied per signed-in user |
| Extra points | **[+Validate]** test with **View as** in Desktop (Other user + the role), then with a real test account after publishing<br>**[+Scale]** dynamic RLS (one table of users and regions) needs no change when people join; a static role per region does<br>**[+Business]** one published report, safely different data per viewer, instead of N copies to maintain |

**Likely follow-ups:** Static vs. dynamic RLS? Why `USERPRINCIPALNAME` rather than `USERNAME`? *(In Desktop, `USERNAME` returns `DOMAIN\user`, not the email, so tests in Desktop and the Service behave differently.)* How would you test it before rollout?
**Red flag:** confusing RLS with a report-level filter.
**Learn it in:** Chapter 16, section 16.10 (Dynamic roles).

### Rapid-fire, 70.7

Roles: BI for every row; DA for the Mid rows.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q70-063 | Import mode vs. DirectQuery? | A compressed copy in memory, fast, as fresh as the last refresh / a live query on every interaction, always current, slower | **[+Trade-offs]** default to Import; DirectQuery only when near-real-time matters more than speed | Mid · 16.2 |
| Q70-064 | What do `REMOVEFILTERS` / `ALL` do inside `CALCULATE`? | Remove filters, so the measure sees the unfiltered total; `REMOVEFILTERS` is the clearer name, `ALL` the older one you'll meet in inherited models | **[+Edge cases]** on a whole table they clear every filter on it; name one column (`REMOVEFILTERS ( Product[category] )`) to clear only that one | Mid · 16.5 |
| Q70-065 | Power BI dashboard vs. report? | Report: one or more interactive pages, built in Desktop / dashboard: one page of visuals pinned from several reports, in the Service | **[+Business]** an executive wants the dashboard glance; an analyst wants the report to dig into | Mid · 16.1, 16.9 |
| Q70-066 | Handle a many-to-many relationship in the model? | Introduce a bridge table, giving two clean one-to-many relationships (or mark the relationship many-to-many); beyond this book, but the idea is Chapter 12's bridge table | **[+Trade-offs]** a bridge table filters more predictably than a native many-to-many relationship | Senior · 12.1 |
| Q70-067 | Power Query vs. DAX: where does a transform belong? | Reshape and clean *before* loading, the same for every user / calculate *in* the model, responding to filters | **[+Trade-offs]** same every time → Power Query; depends on what's selected → DAX | Mid · 16.2, 16.4 |
| Q70-068 | Move a Power BI star schema and its measures to Tableau? | The model carries over; DAX measures become calculated fields; `SAMEPERIODLASTYEAR`-style time intelligence needs more date functions by hand | **[+Trade-offs]** the modelling idea is portable; measure syntax and time intelligence are what change | Senior · 16.12 |

---

## 70.8 Dashboard critiques

### Q70-069 · Critique and rebuild: the "everything on one page, no filters" dashboard

**Level:** Mid · **Roles:** BI, DA, BA

**The dashboard:** one page. Two big numbers the same size (this year's revenue and last year's, nothing to tell them apart). A 14-slice pie chart of revenue by product. A 3,000-row raw table below. No filters, no date range: it always shows all-time data. Figure 70.1 is a sketch of it.

![A wireframe of a one-page dashboard: two identical big-number cards labelled "Revenue this year" and "Revenue last year", a pie chart split into 14 slices, and a long raw table of 3,000 rows below; a note says there are no filters or date range](figures/fig70-1-one-page-dashboard.svg)

*Figure 70.1 — The dashboard in Q70-069, as the interviewer describes it.*

**What's wrong, fast:**

| Problem | Why it matters | Fix |
|---|---|---|
| Two identical "big numbers" | The reader has to reread both labels every time to tell them apart | One large current number, with a small "+X% vs. last year" beside it |
| A 14-slice pie chart | Nobody can compare 14 angles; pies work only for a few parts (about five or six at most) | A sorted horizontal bar chart: the top 8–10 products plus "Other" |
| A 3,000-row table on the dashboard | A data dump, not a summary; it buries the answer in scrolling | Drill-through or export, not shown by default |
| No filters, no date range | It can never answer "how's this quarter?" without a rebuild | A date slicer that drives every visual on the page |

**Extra-point moves shown:** **[+Signpost]** organized by problem, not a stream of thoughts. **[+Business]** every fix ties to what the viewer needs to do. **[+Edge cases]** the "Other" bar and the drill-through both allow for more data than fits on one screen.

**Learn it in:** Chapter 15, sections 15.7 (pies and parts of a whole) and 15.11 (titles and clutter); Chapter 16, section 16.7 (designing the report page).

### Q70-070 · Critique and rebuild: the "six gauges and a 3D pie, live on production" dashboard

**Level:** Senior · **Roles:** BI

**The dashboard:** six gauges across the top, one per region, showing progress to target. Below, a 3D exploded pie chart of revenue by sales rep. Every chart uses a different, unrelated colour palette. It refreshes live through DirectQuery against the production database. Figure 70.2 is a sketch of it.

![A wireframe of a dashboard with six semicircular gauges in a row, one per region, and below them a tilted 3D pie chart with its slices pulled apart, labelled by sales rep; each chart is drawn in a different palette, and a note says the data comes live from the production database through DirectQuery](figures/fig70-2-gauges-dashboard.svg)

*Figure 70.2 — The dashboard in Q70-070, as the interviewer describes it.*

**What's wrong, fast:**

| Problem | Why it matters | Fix |
|---|---|---|
| Six gauges | A lot of ink for one number each, shown by angle; harder to compare than bars on one axis | Six KPI cards, or one bar chart of % of target by region |
| A 3D exploded pie | Perspective makes the near slices look bigger than far slices of the same size; pulling slices apart makes it worse | A plain, sorted 2D bar chart |
| A different palette per chart | The reader must relearn what each colour means on every chart | One palette for the page: the same region in the same colour everywhere |
| Live DirectQuery for a daily check | Slows the production database for no real gain in freshness | Import mode with a scheduled refresh |

**Extra-point moves shown:** **[+Evidence]** naming the specific, known distortion of 3D pies (Chapter 15's rule), not just "pies are bad". **[+Scale]** linking a chart setting to a real risk for the production system. **[+Business]** every fix asks what the viewer needs, not what "looks unprofessional".

**Learn it in:** Chapter 15, sections 15.7 (pies), 15.10 (colour with meaning) and 15.12 (misleading charts); Chapter 16, sections 16.2 (Import or DirectQuery) and 16.7 (gauges, and designing the page).

---

## 70.9 Predict the output: what the grid does behind the number

The rest of this chapter is about building things in a spreadsheet: formulas, pivots, Power Query, macros, models. This section is about the handful of behaviours underneath the grid that decide whether the number in the cell is the number you think it is.

They come up in interviews because they are the difference between someone who uses a spreadsheet and someone who can be trusted to reconcile one. Everything here produces a plausible answer with no error, no warning, and no green triangle in the corner.

Read each one, say the answer out loud, then read on.

**How these were verified, and one honest limitation.** The arithmetic below — date serials, significant digits, floating point, rounding — follows rules that are published and exact, and every figure was computed and printed rather than recalled. **Excel itself was not available to run these in**, so anything that depends on Excel's own implementation rather than on arithmetic is marked **Check in Excel**, with the documented behaviour given and the reason it is worth confirming on your own copy. Four questions carry that mark. The rest are arithmetic and do not need it.

The Python snippets below are there to *compute* the arithmetic the spreadsheet is doing, not to replace it; they need only the standard library:

```python
import decimal
```

### Q70-072 · `=DATE(1900,2,29)` and serial number 60

**Level:** Mid · **Roles:** DA, BA, FA

**Remember it as:** *Excel believes 1900 was a leap year. It was not. Serial 60 is a day that never existed, and every date after it is shifted by one.*

**Answer in one line:** Excel accepts **29 February 1900** as serial number 60 — a date that does not exist, because 1900 was not a leap year — and the error is deliberately preserved for compatibility with Lotus 1-2-3.

| Serial | Excel says | Reality |
|---|---|---|
| 1 | 1 Jan 1900 | 1 Jan 1900 |
| 59 | 28 Feb 1900 | 28 Feb 1900 |
| **60** | **29 Feb 1900** | **does not exist** |
| 61 | 1 Mar 1900 | 1 Mar 1900 |

The leap-year rule is divisible by 4, except centuries, except centuries divisible by 400:

```python
for y in (1900, 2000, 2024):
    print(f"{y}: {(y % 4 == 0 and y % 100 != 0) or y % 400 == 0}")
```

```
1900: False
2000: True
2024: True
```

So 1900 had 365 days and Excel thinks it had 366.

The practical consequences are narrow but sharp:

**Day-of-week calculations before 1 March 1900 are wrong by one.** Irrelevant for business data, relevant for historical or genealogical work.

**Excel and other systems disagree about the same serial number.** Export a date column as a number from Excel and read it anywhere that uses the real calendar, and dates shift by a day — or by two, depending on which epoch the other tool assumes, because the common alternatives are 1899-12-30 and 1899-12-31. This is the actual bug people hit: a CSV of serial numbers rather than formatted dates, and a one-day offset nobody can explain.

**macOS Excel historically used a 1904 epoch**, so a workbook moved between the two systems could shift by 1,462 days. The setting still exists in workbook options, which means a four-year date error is one checkbox away.

The rule that follows: **never move dates between systems as serial numbers.** Export them as text in ISO format — `yyyy-mm-dd` — and parse them explicitly on the other side.

| Tier | What to say |
|---|---|
| Passes | "Excel thinks 1900 was a leap year" |
| Strong | + why it is kept (Lotus 1-2-3 compatibility), and that the real damage is serial numbers crossing between systems rather than the 1900 dates themselves |
| Extra points | **[+Edge cases]** the 1904 epoch option exists in workbook settings and shifts everything by 1,462 days · **[+Business]** a one-day offset in an exported date column is the usual symptom and is very hard to trace back to this · **[+Validate]** export dates as ISO text, never as serials |

**Likely follow-ups:** What is the actual leap-year rule? Why would a date column import one day out? What does Google Sheets do? *(Sheets replicates the bug, for Excel compatibility.)*
**Learn it in:** Chapter 10, section 10.6 (dates in spreadsheets); Chapter 14, section 14.7.

### Q70-073 · A 16-digit order number typed into a cell

**Level:** Mid · **Roles:** DA, BA, FA

**Remember it as:** *A spreadsheet keeps 15 significant digits. The 16th becomes a zero, silently, and two different ids can become one.*

**Answer in one line:** The last digit becomes **0** — `1234567890123456` is stored and displayed as `1234567890123450`, because the number is held to 15 significant digits, and two ids differing only in the 16th digit become identical.

```
typed                    stored and shown
1234567890123456   ->    1234567890123450
1234567890123457   ->    1234567890123450      <- the same
9007199254740993   ->    9007199254740990
1234567890123456789 ->   1234567890123450000
```

Note that this is *not* the same limit as the float64 one in Chapter 77 (2⁵³ ≈ 9.007 × 10¹⁵, about 16 digits). Excel's 15-digit rule is a deliberate display and storage convention applied on top of the double, chosen so that arithmetic looks clean. The effect is the same and arrives sooner.

What makes it dangerous rather than annoying is that the data is not recoverable. Once the cell holds `...450`, the original digit is gone, and no amount of reformatting brings it back. If the file is the only copy, the identifiers are destroyed.

Numbers this long are ordinary: credit-card numbers (16 digits), IMEI numbers (15), Aadhaar (12, safe), GSTIN (15 alphanumeric, safe because it is text), bank account numbers, and any id minted from a timestamp.

The companion behaviour, which is the same class of problem and more common: a long number entered as a plain number displays as **1.23457E+15** in scientific notation, and anything over 11 digits may do so depending on column width. People then widen the column, see the full number return, and conclude nothing was lost — which is true for 15 digits and false for 16.

The fix is to decide at entry: an identifier is **text**. Format the column as Text *before* typing or pasting, or prefix with an apostrophe. Doing it afterwards does not help.

| Tier | What to say |
|---|---|
| Passes | "Excel only keeps 15 digits" |
| Strong | + that the loss is irreversible, that two ids can collapse to one, and that the column must be Text *before* the data arrives |
| Extra points | **[+Business]** card numbers, IMEIs and timestamp-derived ids are all in range, and a destroyed id cannot be reconciled back · **[+Edge cases]** scientific-notation display is a separate, reversible problem, which is why people wrongly assume this one is too · **[+Validate]** check the length of the longest id before a spreadsheet becomes part of a pipeline · **[+Trade-offs]** CSV holds the full value; it is Excel that truncates on open, so the file may be fine and the view is not |

**Likely follow-ups:** How does this relate to the float64 limit? What happens on CSV import? *(The Text Import wizard, or Power Query, lets you set the column type before it loads — that is the fix.)* Why do leading zeros disappear too?
**Learn it in:** Chapter 10, section 10.4 (number formats); Chapter 77, Q77-037.

### Q70-074 · `=0.1+0.2=0.3` and `=(0.1+0.2)-0.3`

**Level:** Mid · **Roles:** DA, BA, FA · **Check in Excel**

**Remember it as:** *The spreadsheet uses the same binary floating point as everything else, and then hides it. So the comparison can say TRUE while the subtraction shows a residue.*

**Answer in one line:** The arithmetic is exact for neither: `0.1 + 0.2` really is `0.30000000000000004`, and the subtraction leaves **5.55E-17** — but Excel applies a cosmetic final-result rounding that can make the direct comparison display `TRUE`, which is why the two formulas appear to contradict each other.

```python
print(f"0.1 + 0.2       = {0.1 + 0.2:.20f}")
print(f"0.1 + 0.2 - 0.3 = {0.1 + 0.2 - 0.3:.20e}")
print(f"equal to 0.3?     {0.1 + 0.2 == 0.3}")
```

```
0.1 + 0.2       = 0.30000000000000004441
0.1 + 0.2 - 0.3 = 5.55111512312578270212e-17
equal to 0.3?     False
```

Those three lines are IEEE 754 and are true in every language, this book's Python chapters included (Chapter 72, Q72-010).

**Check in Excel:** Excel adds a layer the languages do not — a cosmetic rounding applied to a final result when it is very close to a round number — so `=0.1+0.2=0.3` may display `TRUE` while `=(0.1+0.2)-0.3` displays `5.55E-17`. The exact conditions are version-specific. Type both into a cell and see which you get; the point of the question survives either way, and knowing which your own version does is worth ten seconds.

Where it costs money is reconciliation. A check written as `=IF(total_a=total_b,"OK","MISMATCH")` on two columns that were computed by different routes will report a mismatch on figures that agree to the paisa. The fix is a tolerance:

```
=IF(ABS(total_a-total_b)<0.005,"OK","MISMATCH")
```

Or, better for money, work in whole paise as integers and compare exactly.

| Tier | What to say |
|---|---|
| Passes | "Floating point is imprecise" |
| Strong | + the residue value, that it is IEEE 754 rather than an Excel bug, and a tolerance-based reconciliation as the fix |
| Extra points | **[+Business]** an exact-equality reconciliation check reports false mismatches on correct data, and people learn to ignore it · **[+Edge cases]** Excel's cosmetic rounding makes the two formulas disagree, which is what makes this confusing rather than merely known · **[+Trade-offs]** integer paise is exact and is what a database should store (Chapter 12, section 12.8) |

**Likely follow-ups:** What tolerance would you choose, and why? How would you store money properly? Does this affect SUMIFS? *(It affects any comparison; a criteria match on a computed decimal is the same risk.)*
**Learn it in:** Chapter 72, Q72-010 (floating point); Chapter 12, section 12.8.

### Q70-075 · Three cells of 1.004, displayed to two decimals, summed

**Level:** Fresher · **Roles:** DA, BA, FA

**Remember it as:** *Formatting changes what you see, not what is stored. The column shows 1.00 + 1.00 + 1.00 = 3.01, and both numbers are right.*

**Answer in one line:** The column displays **1.00, 1.00, 1.00 and a total of 3.01** — because the sum is computed on the stored 1.004 values (3.012) and only then rounded for display, so the visible figures do not add up to the visible total.

```python
vals = [1.004, 1.004, 1.004]
print(f"stored sum      : {sum(vals):.3f}  -> displayed as {round(sum(vals), 2):.2f}")
print(f"sum of displayed: {1.00 * 3:.2f}")
```

```
stored sum      : 3.012  -> displayed as 3.01
sum of displayed: 3.00
```

This is the single most common "the spreadsheet is wrong" complaint, and the spreadsheet is not wrong. It is the reason a finance review stalls for an hour on a one-paisa discrepancy.

The distinction worth being able to state cleanly:

| | What it does |
|---|---|
| **Number formatting** (2 decimal places) | Changes the display only. The cell still holds 1.004 |
| **`=ROUND(A1,2)`** | Changes the stored value to 1.00. The sum then really is 3.00 |
| **Precision as displayed** (a workbook option) | Permanently rounds every stored value to its displayed precision — and it is irreversible |

Which you want depends on the document. A report that must foot — where the printed column has to add to the printed total — needs `ROUND` applied to the components, accepting that you have changed the numbers. An analysis should keep full precision and round only at the final presentation.

What you should almost never do is tick "Precision as displayed", because it silently rewrites every value in the workbook and cannot be undone.

| Tier | What to say |
|---|---|
| Passes | "It's a display rounding issue" |
| Strong | + distinguishes format from `ROUND` from the workbook option, and says which to use for a report that must foot |
| Extra points | **[+Business]** a report that must foot has to round the components, which means the printed figures are deliberately not the computed ones — say so in a footnote · **[+Edge cases]** "Precision as displayed" is irreversible and rewrites the stored data · **[+Validate]** if a column does not foot, check the stored values before looking for a formula error |

**Likely follow-ups:** How would you make a report foot exactly? What is the largest discrepancy you could get from this? *(It grows with the number of rows.)* Does the same happen in a pivot table? *(Yes — Q70-016.)*
**Learn it in:** Chapter 10, section 10.4 (number formats); Chapter 10, section 10.9.

### Q70-076 · `=ROUND(2.5, 0)` and `=ROUND(-0.5, 0)`

**Level:** Mid · **Roles:** DA, BA, FA · **Check in Excel**

**Remember it as:** *Excel rounds a half away from zero. Python rounds a half to the nearest even number. The same data gives different totals in the two tools.*

**Answer in one line:** Excel gives **3** and **−1** — it rounds halves away from zero — where Python's `round()` gives **2** and **0**, because Python uses banker's rounding, so the same column reconciled in two tools can differ.

```python
for v in (0.5, 1.5, 2.5, 3.5, -0.5):
    half_up = decimal.Decimal(v).quantize(decimal.Decimal('1'),
                                          rounding=decimal.ROUND_HALF_UP)
    print(f"{v:>5}: python round() -> {round(v):>3}    half-away-from-zero -> {half_up:>3}")
```

```
  0.5: python round() ->   0    half-away-from-zero ->   1
  1.5: python round() ->   2    half-away-from-zero ->   2
  2.5: python round() ->   2    half-away-from-zero ->   3
  3.5: python round() ->   4    half-away-from-zero ->   4
 -0.5: python round() ->   0    half-away-from-zero ->  -1
```

They agree on 1.5 and 3.5 and disagree on 0.5 and 2.5, which is exactly why this is hard to spot: the two methods match half the time.

Banker's rounding is not a quirk; it is chosen deliberately because always rounding halves upward introduces a systematic upward bias across many values, and rounding half-to-even cancels it. Over a million rows that bias is real money.

**Check in Excel:** `ROUND(2.675, 2)` is the case worth typing in yourself. The stored double for 2.675 is `2.67499999999999982...`, so a rule applied to the binary value gives 2.67, while Excel's documented decimal-aware behaviour gives 2.68. Most languages give 2.67. The discrepancy is small and the lesson is not: **do not expect two tools to round the same way**, and never reconcile rounded figures across tools without checking.

```python
print(decimal.Decimal(2.675))
```

```
2.67499999999999982236431605997495353221893310546875
```

If you need a specific rule regardless of tool, state it explicitly — `ROUND_HALF_UP` in Python's `decimal`, or `ROUNDUP`/`ROUNDDOWN` in Excel — rather than relying on either default.

| Tier | What to say |
|---|---|
| Passes | "Excel rounds 2.5 up to 3" |
| Strong | + that Python rounds to even and gives 2, that this is deliberate bias-cancellation, and that the two agree half the time |
| Extra points | **[+Business]** reconciling a rounded column between Excel and a Python or SQL pipeline produces differences that look like data errors · **[+Edge cases]** `ROUND(2.675, 2)` differs again, because the stored double is below 2.675 · **[+Trade-offs]** state the rounding rule explicitly in anything that must reconcile; neither default is wrong, and relying on either is |

**Likely follow-ups:** Why does banker's rounding exist? What does SQL's `ROUND` do? *(Engine-dependent — another place to check rather than assume.)* How would you force a specific rule in Python? *(`decimal` with an explicit `rounding=`.)*
**Learn it in:** Chapter 10, section 10.4; Chapter 21, section 21.3.

### Q70-077 · `=VLOOKUP(A2, table, 3)` with the fourth argument left out

**Level:** Fresher · **Roles:** DA, BA, FA · **Check in Excel**

**Remember it as:** *The fourth argument defaults to TRUE, which means approximate match. Leaving it out does not mean "exact"; it means "closest below, and I assume you sorted".*

**Answer in one line:** It performs an **approximate** match, not an exact one — the omitted fourth argument defaults to `TRUE`, which returns the closest value *below* the lookup on data it assumes is sorted ascending, and on unsorted data it returns something arbitrary with no error.

```
=VLOOKUP(A2, table, 3)          approximate  (range_lookup defaults to TRUE)
=VLOOKUP(A2, table, 3, TRUE)    approximate  (the same thing, said out loud)
=VLOOKUP(A2, table, 3, FALSE)   exact        (what people almost always want)
```

This is the most consequential default in the application, because the failure is silent in both directions:

**On sorted data** it returns the nearest value below. Look up customer code 1050 in a table containing 1000 and 1100 and you get 1000's row — a real customer's data attached to the wrong customer. No `#N/A`, no warning, just the wrong name and the wrong revenue.

**On unsorted data** the behaviour is undefined. It uses a binary search that assumes order, so it can return a match, a wrong match, or `#N/A` for a value that is definitely present — which is the same failure as Chapter 71's Q71-043, where a binary search on unsorted data reports "not found" for a row you can see.

`XLOOKUP` fixed this by defaulting to exact match, which is the strongest argument for preferring it (Q70-002). `INDEX`/`MATCH` has the same trap in `MATCH`'s third argument, which also defaults to approximate.

**Check in Excel:** worth typing out once, because the lesson lands differently when you watch it return a wrong name rather than an error. Build a four-row lookup table, leave the argument off, and look up a value that is not present.

When *is* approximate match right? Band lookups — a commission tier, a tax slab, a shipping-weight band — where "the row at or below this value" is exactly the question. In that case pass `TRUE` explicitly, so the next reader knows it was a decision.

| Tier | What to say |
|---|---|
| Passes | "You need FALSE for an exact match" |
| Strong | + that the default is TRUE, what approximate returns, and that on unsorted data it is undefined rather than merely wrong |
| Extra points | **[+Business]** it returns another customer's data rather than an error, so the output looks complete and is wrong · **[+Edge cases]** `MATCH` has the same default in its third argument · **[+Trade-offs]** `XLOOKUP` defaults to exact, which is the real reason to prefer it · **[+Validate]** always pass the fourth argument, even when you want TRUE, so the intent is visible |

**Likely follow-ups:** When would you want approximate match? Why can `VLOOKUP` not look left? How does `XLOOKUP` differ? *(Exact by default, searches any direction, and takes a not-found argument — Q70-002.)*
**Learn it in:** Chapter 10, section 10.7 (lookups); Chapter 70, Q70-002.

### Rapid-fire, 70.9: the grid's quiet behaviours

Roles: DA, BA and FA for every row. Those marked **Check in Excel** depend on Excel's own implementation rather than on arithmetic.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q70-078 | `=COUNTA(A1:A10)` where three cells hold `=""` | Counts them. `COUNTA` counts anything that is not truly empty, and a formula returning an empty string is not empty | **[+Validate]** `COUNTBLANK` counts `""` as blank, so the two disagree — that gap is the test → Q70-006 |
| Q70-079 | `=SUM(A1:A10)` where the numbers were pasted as text | 0, with no error. `SUM` silently skips text; a column of green-triangled "numbers stored as text" adds to nothing | **[+Business]** a total of zero is noticed; a partial total where only some cells are text is not → Ch 10 §10.4 |
| Q70-080 | `=AVERAGE(A1:A5)` with two blanks against two zeros | Blanks are excluded, zeros are included — so the same data gives a different mean depending on how "no value" was recorded | **[+Clarify]** ask whether a missing value means zero before averaging → Ch 73 Q73-038 |
| Q70-081 | Typing `3/4` into a General-formatted cell | Becomes a date (3 April of the current year), not 0.75 or a fraction. Autocorrect is interpreting, not calculating | **[+Business]** the famous gene-name case: `SEPT2` became a date, which is why those genes were renamed → Ch 14 §14.5 |
| Q70-082 | A pivot grand total that does not equal the sum of the rows | Usually `DISTINCTCOUNT` or an average, which do not add up by design. A distinct count of the whole is not the sum of the parts | **[+Validate]** non-additive measures are the first thing to check → Q70-016 |
| Q70-083 | `=A1&""` against a reference to a blank cell | A blank referenced with `=A1` returns 0; with `&""` it returns an empty string. Two different "nothings" | **[+Edge cases]** which is why a blank lookup result shows as 0 in a report → Ch 10 §10.4 |
| Q70-084 | Sorting a range where one column is outside the selection | The sorted columns move and the unselected one does not: every row is now mismatched, with no warning | **[+Business]** this silently corrupts data and is unrecoverable once saved — use a Table (Ctrl+T) → Q70-015 |
| Q70-085 | Merged cells in a column you need to sort or pivot | Sorting refuses or misbehaves, and a pivot treats the merged area as one value with blanks below | **[+Trade-offs]** "Center Across Selection" looks identical and breaks nothing → Ch 10 §10.9 |
| Q70-086 | `=IFERROR(VLOOKUP(...), 0)` wrapped around every lookup | Hides genuine `#N/A`s, so unmatched rows silently become zero and the total is understated with no sign anything failed | **[+Validate]** use `IFNA` to catch only "not found", and let real errors surface → Q70-008 |
| Q70-087 | A CSV of dates opened directly in Excel, `03/04/2025` | Read as 3 April or 4 March depending on the machine's locale, with no prompt. The first twelve days of a month are ambiguous | **[+Business]** the same file read by two colleagues gives two different answers → Ch 77 Q77-036 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `VLOOKUP` with the match type left out | Silent wrong results from approximate matching | Pass `FALSE`, or use `XLOOKUP` or `INDEX`/`MATCH` |
| Nested `IF`s in the wrong order | A middle tier "wins" over a higher one that should fire first | Most restrictive first; `IFS` past two levels |
| A revenue total that includes cancelled orders | The number is plausible, and too high | Add the status condition (`"<>Cancelled"`), and say so out loud |
| Pivot source range misses new rows | The grand total quietly misses recent data | Build pivots on Tables, not fixed ranges |
| VBA looping cell by cell over a large range | The macro is slow or seems to hang | Array read → work in memory → array write |
| Apps Script looping `getValue()`/`setValue()` | The script hits the six-minute limit | Batch with `getValues()`/`setValues()` |
| A DAX calculated column where a measure was needed | The value doesn't respond to report filters | Rewrite it as a measure if it adds up or responds to filters |
| A dashboard with no date filter | Can't answer "how's this quarter?" without a rebuild | A date slicer driving every visual |
| A 3D or heavily decorated chart for simple data | It distorts the comparison it's meant to show | The plainest chart that shows the pattern |

---

## In the real world: the interview that turned on one broken macro

Arjun, a BA candidate, gets a live-coding round: a VBA macro meant to consolidate three regional files, which stops with "Subscript out of range." He's never seen this exact error before, and says so out loud, then reasons through it: "This usually means I'm referring to something, a sheet name, an array index, that doesn't exist. Let me check what the code asks for against what's actually there." The code refers to `Worksheets("Region2")`; the sheet is named "Region 2," with a space.

He fixes the typo, and then adds one more line, unprompted: a message box reporting how many rows came from each file, so a future user notices at once if a file fails to load. In the feedback call after the offer, the hiring manager singled out that line: "you diagnosed a real error methodically, then thought one step past 'it works now.'"

**The lesson:** a broken-macro round isn't testing whether you already know that error message. It's testing whether you have a *method* for one you've never seen, and whether you stop at "it runs" or keep going to "it runs, and it'll tell someone if it fails next time."

---

## Project

**Goal:** one worked example per major topic in this chapter, on your own data or Riverstone's.

### Tools you'll need

**Excel and Google Sheets** (both free at a basic level). **Power BI Desktop** (free to build; publishing has free and paid tiers). **VBA** ships inside Excel; **Google Apps Script** ships inside every Sheet (**Extensions → Apps Script**). Nothing beyond what Chapters 10, 11, 15, 16 and 19 already covered (plus Chapter 12 for the SQL comparisons). The practice table is in `companion/ch70/`.

1. Write three `SUMIFS`/`COUNTIFS` formulas answering real questions, each checked against a pivot table built the slow way.
2. Build one Power Query that combines several files (or several sheets), naming every step for its purpose.
3. Write one VBA macro or Apps Script function that would take over ten minutes by hand; time it before and after.
4. Build one Power BI (or other) dashboard, then critique it yourself in this chapter's problem–why–fix table, honestly, before anyone else does.
5. Write one DAX measure (or a Sheets or Tableau equivalent) that responds correctly to a filter, and prove it by changing the filter.

---

## Key terms

`SUMIFS`/`COUNTIFS` · `XLOOKUP` · `INDEX`/`MATCH` · absolute vs. relative reference · `SUMPRODUCT` · dynamic array (`FILTER`, `UNIQUE`) · pivot table · calculated field (pivot) · Power Query · Merge vs. Append · `QUERY` (Sheets) · `ARRAYFORMULA` · `IMPORTRANGE` · VBA object model · Personal Macro Workbook · `On Error` · UserForm · Office Scripts · Apps Script execution limit · `getValues()`/`setValues()` batching · installable trigger · calculated column vs. measure (DAX) · `CALCULATE` · filter context · star schema · row-level security (RLS) · Import mode vs. DirectQuery · date serial number · the 1900 leap-year bug · 1904 epoch · 15 significant digits · scientific-notation display · banker's rounding against half-away-from-zero · display rounding against `ROUND` · precision as displayed · approximate against exact match (`range_lookup`) · numbers stored as text · `IFNA` against `IFERROR` · locale date parsing

---

## Final-week revision list

Q70-001, Q70-002, Q70-003, Q70-005, Q70-016, Q70-018, Q70-027, Q70-028, Q70-034, Q70-035, Q70-040, Q70-041, Q70-043, Q70-052, Q70-053, Q70-059, Q70-060, Q70-061, Q70-062, Q70-069, Q70-073, Q70-075, Q70-077.

The last three are the ones that put a wrong number in front of a stakeholder with no error anywhere: a 16-digit id losing its last digit (Q70-073), a column that does not foot because formatting is not rounding (Q70-075), and a `VLOOKUP` that returns another customer's row because the fourth argument was left off (Q70-077).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** picks up where section 70.3's Merge and Append and section 70.4's `QUERY` leave off: the same join and aggregation logic, in real SQL.
- **Chapter 78, Automation & Integration Question Bank,** goes further into API integration and scheduling than section 70.6's Apps Script questions.
- **Chapters 10, 11, 15, 16 and 19** teach every technique this bank draws on, in full; this chapter tests them, it doesn't re-teach them.
