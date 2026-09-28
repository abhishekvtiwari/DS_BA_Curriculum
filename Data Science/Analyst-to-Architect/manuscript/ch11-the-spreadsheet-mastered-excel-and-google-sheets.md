# Chapter 11. The Spreadsheet, Mastered: Excel & Google Sheets

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** answer business questions with the conditional functions (`SUMIF(S)`, `COUNTIF(S)`, `AVERAGEIF(S)`, `MAXIFS`, `MINIFS`) and `SUMPRODUCT`, including OR logic, date ranges, wildcards, weighted averages, and distinct counts · use the everyday toolkit of logical, text, date, and number functions · look up values in every way analysts need (exact, approximate, last match, several columns, two-way) with `XLOOKUP` and `INDEX`/`MATCH` · summarize thousands of rows in seconds with pivot tables, slicers, and pivot charts, and read results out of them with `GETPIVOTDATA` · write formulas that return whole lists with dynamic arrays (`FILTER`, `UNIQUE`, `SORT`, `SEQUENCE`, `LET`, `TAKE`, `VSTACK`, `LAMBDA`, `SCAN`) · combine a folder of monthly files and clean, group, merge, and reshape them with Power Query (including custom columns in M and handling broken files), so next month is one refresh · build a data model with relationships and write your first DAX measures in Power Pivot · answer "what would it take?" with Goal Seek and data tables · use Google Sheets' power features: `QUERY`, `ARRAYFORMULA`, `IMPORTRANGE`, and Connected Sheets · know what each app can't do and what to use instead · audit a workbook and recognize when a job has outgrown the spreadsheet · and, as an optional challenge, solve a championship-style Excel case against the clock.
>
> **Before you start:** Chapter 10.
>
> **Time needed:** 35–45 hours of reading and practice, over five to six weeks: about 12 sittings of 3–4 hours (two for §11.2, one each for §11.1 and §11.3–11.5, one for the core of §11.6 with §11.10–11.11, one for §11.7, one for Goal Seek, §11.12–11.13 and the story, one for the project, one for the exercises, and two for the second pass).
>
> **Core and second pass:** parts marked **Second pass** (the end of §11.6, "Power Query in depth", §11.8 on Power Pivot and DAX, data tables, and the Timed challenge) can wait until after the project; everything else is the core.
>
> **Tools:** Microsoft Excel for Windows (Microsoft 365) for Power Query and Power Pivot; Google Sheets for sections 11.2–11.6, 11.9, and 11.10. Where a feature exists only in one app, or only on Windows, the section says so and gives an alternative.
>
> **Practice data:** `companion/ch11/`: `ch11_practice.xlsx` (Riverstone's 330 order lines for 2025 as a clean Sales table, with Customers, Products, Targets, TargetsWide, and RebateBands sheets), the folder `monthly_exports/` (twelve monthly CSV files), `month_end_pack_2025_messy.xlsx` (the workbook from this chapter's story), `pq_practice/` (a broken export for section 11.7), and `challenge/` (the two competition-style cases in the Timed challenge). Every total matches Chapter 10's tracker: net revenue excluding cancelled orders is ₹43,35,471.

---

## Why this matters

In Chapter 10 you built a monthly tracker by hand. It works, and it's correct. Now imagine next month. A new export arrives. Someone has to import it, paste it under last month's rows, extend every formula, check that the pivot picked up the new rows, and fix the one chart whose range stopped at December. Multiply that by every report a team produces, and you understand why so many analysts spend the first week of each month copying and pasting.

This chapter is about removing that week. The tools here (lookups that don't break, pivot tables, formulas that return whole tables, Power Query, and data models) let you build a workbook **once** and **refresh** it forever after. They're also the tools interviewers test when a job description says "advanced Excel": you'll be asked to build a pivot table live, explain `INDEX`/`MATCH`, or describe how you'd automate a monthly report.

There's a second, quieter reason. Workbooks built by copy and paste accumulate errors nobody sees: a range that stops a few rows short, a number typed in from an email, a formula that includes cancelled orders in some months but not others. This chapter's story is about exactly such a workbook, and the auditing habits in section 11.12 are how you find those errors before your manager does.

Finally, you'll learn where the spreadsheet stops. Knowing when to move a job to SQL, Python, or Power BI is as much a mark of skill as knowing every Excel function.

---

## In plain English

Picture a school office preparing the **annual results**.

**Lookups** are the office assistant with the class register: given a roll number, she finds the student's name, their section, or, for fee concessions, which **band** their family income falls into. Chapter 10 taught her to find exact matches; now she learns to find the right band, the most recent entry, and a value at the crossing of a row and a column.

A **pivot table** is the board on the principal's wall where you slide cards around: put "class" cards down the side, "subject" cards across the top, and every square shows the average mark. Rearrange the cards and the board redraws itself.

**Dynamic arrays** are a photocopier that prints a whole list from one instruction: "every student in section B, sorted by marks". Change a mark and the printout updates.

**Power Query** is a recorded routine for the clerk who collects mark sheets from twelve teachers every term: open each file, fix the date format, remove absentees, stack them into one list. Record it once; next term, drop the new files in the tray and press one button.

A **data model** is a set of linked registers (students, subjects, calendar) instead of one enormous sheet, and **DAX measures** are formulas like "pass percentage" written once and reused on any board.

**Goal Seek** answers the reverse question: "what mark does this student need in the final exam to pass overall?"

Here's the mapping:

- The assistant's lookups are `XLOOKUP` and `INDEX`/`MATCH`; the bands are an **approximate match**.
- The sliding-card board is a **pivot table**: **Rows**, **Columns**, **Values**, and **Filters** areas.
- The photocopier is a **dynamic array** formula that **spills** its results into neighboring cells.
- The recorded routine is a **query** in Power Query, made of **applied steps**.
- The linked registers are a **data model** with **relationships**; "pass percentage" is a **measure**.
- The reverse question is **what-if analysis**.

---

## 11.1 From a tracker to a system

Open `month_end_pack_2025_messy.xlsx`. It's the kind of workbook you'll inherit in your first job: one sheet per month, each pasted from that month's ERP export, and a Summary sheet that pulls each month's total with its own formula. The Summary says Riverstone reached **100.7%** of its 2025 target.

Chapter 10's tracker, built from the same data, says **102.3%**. One of them is wrong, and you'll find out which (and why) in this chapter's story. For now, notice what the structure itself forces on whoever maintains it:

| Manual monthly workbook | Refreshable workbook |
|---|---|
| One sheet per month; data pasted in | One table with every month; data loaded by a query |
| A different formula per month on the Summary | One pivot table or one formula for all months |
| Ranges that must be extended by hand | Tables and queries that grow with the data |
| Rules (exclude cancelled) repeated in every formula | Rules applied once, in one place |
| Checking means re-adding by hand | Check cells that compare totals automatically |
| Next month: an afternoon | Next month: **Data → Refresh All** |

Three design ideas run through the rest of the chapter:

1. **Keep data long, not wide.** One row per order line, with the month as a *column*, not a *sheet*. Every tool in this chapter (pivot tables, `FILTER`, `QUERY`, Power Query, DAX) expects data in this shape.
2. **Separate data, calculations, and outputs.** Raw data on one sheet or query, lookups and rules in another, and the report on its own sheet. Section 11.12 turns this into a checklist.
3. **Make the rules explicit and single.** "Net revenue excludes cancelled orders" should live in exactly one place.

Open `ch11_practice.xlsx`. Its **Sales** sheet already follows these ideas: 330 order lines, 19 columns, one row per line, with the lookups from Chapter 10 filled in as values.

| Column | Field | Column | Field |
|---|---|---|---|
| A | `order_id` | K | `month_start` |
| B | `order_date` | L | `quarter` (Q1–Q4) |
| C | `customer_code` | M | `customer_name` |
| D | `product_id` | N | `segment` |
| E | `quantity` | O | `city` |
| F | `unit_price` | P | `product_name` |
| G | `discount_pct` | Q | `category` |
| H | `status` | R | `unit_cost` |
| I | `sales_rep` | S | `gross_margin` |
| J | `net_revenue` | | |

`gross_margin` is net revenue minus product cost (quantity × unit cost), the same rule as Chapter 3 (section 3.5). Before you start, click inside the data and convert it to a table named **Sales** (**Excel: Insert → Table**, then **Table Design → Table Name**; **Sheets: Format → Convert to table**, then rename it). Most formulas in this chapter refer to it as `Sales[column]`.

The sheet and the table now share a name, so read the punctuation. `Sales!J2:J331` (with `!`) means cells J2 to J331 on the **sheet** called Sales. `Sales[net_revenue]` (with square brackets) means the `net_revenue` column of the **table** called Sales. Here both point at the same numbers; the table version also grows when rows are added.

---

## 11.2 Conditional aggregation in depth: the IFS family and SUMPRODUCT

Chapter 10 introduced `SUMIFS`, `COUNTIFS`, and `AVERAGEIFS`. In real workbooks these functions do more work than any others: most finance and sales reports are grids of them. This section takes them to full depth, adds `SUMPRODUCT` for the questions they can't answer, and ends with the patterns (ranks, running totals, grids, distinct counts) you'll build again and again.

The formulas in this section use plain ranges on the **Sales** sheet (`Sales!J2:J331` and so on), so they work in every version of Excel and in Google Sheets. With the data converted to a table, `Sales[net_revenue]` does the same job and grows with the data. As a reminder: `H` is `status`, `J` is `net_revenue`, `N` is `segment`.

![Anatomy of a SUMIFS formula: the sum range, then pairs of criteria range and criterion, with Riverstone examples of criteria written as text, operators joined to cells, wildcards, and blanks](figures/fig11-1-sumifs-anatomy.svg)

*Figure 11.1 — How `SUMIFS` reads its arguments. Every criteria range must be the same size as the sum range; every criterion is text, even when it compares numbers or dates.*

### The family at a glance

| Function | Arguments | Returns |
|---|---|---|
| `SUMIF` | `(range, criterion, [sum_range])` | Sum where **one** condition holds |
| `SUMIFS` | `(sum_range, criteria_range1, criterion1, …)` | Sum where **all** conditions hold |
| `COUNTIF` | `(range, criterion)` | Count of cells meeting one condition |
| `COUNTIFS` | `(criteria_range1, criterion1, …)` | Count of rows meeting all conditions |
| `AVERAGEIF` | `(range, criterion, [average_range])` | Average where one condition holds |
| `AVERAGEIFS` | `(average_range, criteria_range1, criterion1, …)` | Average where all hold |
| `MAXIFS`, `MINIFS` | `(max_range, criteria_range1, criterion1, …)` | Largest or smallest where all hold (Excel 2019 or later, Sheets) |

> **Watch out: SUMIF and SUMIFS put the sum range in different places.** `SUMIF` takes it **last**; `SUMIFS` takes it **first**. Swapping them is the most common error in this family. Many analysts use only the `S` versions, even for one condition, so the argument order never changes.

```excel
=SUMIF(Sales!N2:N331,"Retail",Sales!J2:J331)                                  → 1551423.75
=SUMIFS(Sales!J2:J331,Sales!N2:N331,"Retail",Sales!H2:H331,"<>Cancelled")     → 1488773.75
```

The first formula has no status condition, so it includes both cancelled orders (both were Retail). The second is the correct Retail revenue. Adding one pair of arguments changed the answer by ₹62,650.

### The criteria cookbook

A criterion is always **text** that describes a test. Once you know the patterns, you can write almost any condition.

| You want | Criterion | Riverstone example | Result |
|---|---|---|---|
| Equal to text | `"Retail"` | Retail lines (all statuses) | `COUNTIF(N, "Retail")` → 118 |
| Not equal to | `"<>Cancelled"` | Valid lines | 326 |
| Compare a number | `">=50000"` | Lines worth ₹50,000 or more | 3 |
| Compare with a cell | `">="&G1` | Lines above the threshold in `G1` | depends on `G1` |
| Between two values | two pairs on the same range | Lines from ₹20,000 to under ₹50,000 (valid) | 59 |
| Between two dates | `">="&DATE(2025,7,1)` and `"<="&DATE(2025,9,30)` | Q3 valid revenue | 11,20,289 |
| Contains text | `"*Box*"` | Lines whose product name contains "Box" | 169 |
| Pattern with single characters | `"Storage Box ??L"` | Storage Box 10L and 25L lines | 125 |
| A literal `*` or `?` | `"~*"` | Cells containing an asterisk | — |
| Blank | `""` | Lines with no sales rep | 19 |
| Not blank | `"<>"` | Lines with a sales rep | 311 |

The full formulas for the less obvious ones:

```excel
=COUNTIFS(Sales!J2:J331,">=20000",Sales!J2:J331,"<50000",Sales!H2:H331,"<>Cancelled")     → 59
=SUMIFS(Sales!J2:J331,Sales!B2:B331,">="&DATE(2025,7,1),Sales!B2:B331,"<="&DATE(2025,9,30),Sales!H2:H331,"<>Cancelled")     → 1120289
=COUNTIF(Sales!P2:P331,"*Box*")               → 169
=COUNTIF(Sales!P2:P331,"Storage Box ??L")     → 125
=COUNTIFS(Sales!I2:I331,"<>")                 → 311
```

Rules that save hours:

- **Operators go inside the quotes; cell references go outside.** `">="&G1` joins the operator to the cell's value. `">=G1"` compares with the text "G1" and returns 0.
- **Criteria aren't case-sensitive.** `"retail"` matches `Retail`. For case-sensitive tests, use `SUMPRODUCT` (below) with `EXACT` (section 11.3).
- **Don't type thousands separators in criteria.** `">=50,000"` is read as text, not as a number. Write `">=50000"`.
- **Dates in criteria need `DATE` or a cell.** `">=01-07-2025"` depends on the computer's regional settings; `">="&DATE(2025,7,1)` doesn't.
- **Fix the types before you count.** Lookups and `SUM` care about type (Chapter 10, sections 10.3 and 10.10): `XLOOKUP` won't match the number 5 to the text `0005`, and `SUM` skips numbers stored as text. Whether the IFS family treats the text `"101"` as the number 101 in a criterion differs between apps, so don't rely on it either way.

### OR conditions

`SUMIFS` combines its conditions with **AND**. For **OR** on the **same** column, give it a list of criteria in curly brackets (an **array constant**) and add up the results:

```excel
=SUM(SUMIFS(Sales!J2:J331,Sales!N2:N331,{"Retail","Hospitality"},Sales!H2:H331,"<>Cancelled"))     → 2632812.5
```

`SUMIFS` returns two numbers, one for Retail (₹14,88,773.75) and one for Hospitality (₹11,44,038.75), and `SUM` adds them. In Google Sheets, wrap the formula in `ARRAYFORMULA` (section 11.10 explains it) or use two `SUMIFS` added together.

For OR across **different** columns, adding two `COUNTIFS` double-counts the rows that meet both conditions. *"How many valid lines are Wholesale OR have a quantity of 50 or more?"*

```excel
=COUNTIFS(Sales!N2:N331,"Wholesale",Sales!H2:H331,"<>Cancelled")+COUNTIFS(Sales!E2:E331,">=50",Sales!H2:H331,"<>Cancelled")     → 151   (wrong)
```

105 Wholesale lines plus 46 large-quantity lines is 151, but 6 lines are both. The right answer needs `SUMPRODUCT`.

### SUMPRODUCT: conditions the IFS family can't express

`SUMPRODUCT` multiplies arrays item by item and adds the results. It works in every version of Excel and in Sheets, and its power comes from one idea: a test on a whole range. Build the OR count above one cell at a time on a spare sheet, and look at each result before adding the next piece.

**Cell 1: a test on a whole range.**

```excel
=SUMPRODUCT(--(Sales!N2:N331="Wholesale"))     → 105
```

- `(Sales!N2:N331="Wholesale")` tests all 330 segment cells at once and makes 330 TRUE or FALSE values, one per line.
- `--` (two minus signs, the **double unary**) turns TRUE into 1 and FALSE into 0. The first minus makes TRUE into −1; the second makes it 1 again.
- `SUMPRODUCT` adds the 1s: **105** Wholesale lines.

**Cell 2: multiplying two tests means AND.**

```excel
=SUMPRODUCT((Sales!N2:N331="Wholesale")*(Sales!H2:H331<>"Cancelled"))     → 105
```

Multiplying also turns TRUE and FALSE into numbers: TRUE × TRUE = 1, and anything × FALSE = 0. So a line counts only when both tests are true. The answer is still 105, because no Wholesale line was cancelled (both cancelled orders were Retail).

**Cell 3: adding two tests is almost OR.**

```excel
=SUMPRODUCT(((Sales!N2:N331="Wholesale")+(Sales!E2:E331>=50))*(Sales!H2:H331<>"Cancelled"))     → 151   (wrong)
```

Adding gives 1 when one test is true and **2** when both are. The 6 valid lines that are Wholesale *and* have 50 or more units are counted twice: 105 + 46 = 151, the same wrong answer as the two `COUNTIFS`.

**Cell 4: `>0` turns 1 and 2 into TRUE.**

```excel
=SUMPRODUCT((((Sales!N2:N331="Wholesale")+(Sales!E2:E331>=50))>0)*(Sales!H2:H331<>"Cancelled"))     → 145
```

Three rows of the Sales sheet show what happens inside:

| Sheet row | segment | quantity | Wholesale test | quantity test | sum | sum > 0 |
|---|---|---|---|---|---|---|
| 3 | Hospitality | 55 | FALSE | TRUE | 1 | TRUE |
| 10 | Wholesale | 25 | TRUE | FALSE | 1 | TRUE |
| 238 | Wholesale | 65 | TRUE | TRUE | 2 | TRUE |

Row 238 counted twice in cell 3; after `>0` it counts once. That's **OR** without double counting, and multiplying by `(Sales!H2:H331<>"Cancelled")` adds the status rule with AND: **145** lines.

Multiply by one more array and `SUMPRODUCT` adds values instead of counting lines. With the net revenue column on the end, it returns the revenue of those 145 lines:

```excel
=SUMPRODUCT((((Sales!N2:N331="Wholesale")+(Sales!E2:E331>=50))>0)*(Sales!H2:H331<>"Cancelled")*Sales!J2:J331)     → 2533048.5
```

That's ₹25,33,048.50.

Other questions only `SUMPRODUCT` (or `FILTER`, section 11.6) can answer:

**A condition on a calculation**, such as the month of a date, without a helper column:

```excel
=SUMPRODUCT((MONTH(Sales!B2:B331)=11)*(Sales!H2:H331<>"Cancelled")*Sales!J2:J331)     → 633408
```

`SUMIFS` can't apply `MONTH` to its criteria range; `SUMPRODUCT` can.

**A weighted average (back to Chapter 4, section 4.5).** *"What was Riverstone's average discount?"* In Chapter 4 you worked it out by hand: 4.69% when each line is weighted by its value, not the plain 4.06%. Chapter 10's "Back to Chapter 4" (section 10.8) left this one for `SUMPRODUCT`; now let the spreadsheet do it. The general form is:

```excel
=SUMPRODUCT(values, weights)/SUM(weights)
```

With two ranges separated by a comma, `SUMPRODUCT` multiplies each value by its weight and adds the products; dividing by `SUM(weights)` turns that total back into an average. Try it on the **discounts** sheet of Chapter 4's `numbers_practice.xlsx`, where `A2:A6` holds the five discount rates (0, 5, 8, 10, and 12%) and `C2:C6` the value before discount of the lines at each rate:

```excel
=SUMPRODUCT(A2:A6, C2:C6)/SUM(C2:C6)     → 4.69
```

Now the same question on the Sales sheet, line by line. The plain average of the discount column treats a ₹546 line and a ₹56,700 line equally:

```excel
=AVERAGEIFS(Sales!G2:G331,Sales!H2:H331,"<>Cancelled")     → 4.06
```

The weighted version is the general form with the status rule built into the weights:

```excel
=SUMPRODUCT((Sales!H2:H331<>"Cancelled")*Sales!E2:E331*Sales!F2:F331*Sales!G2:G331)
 /SUMPRODUCT((Sales!H2:H331<>"Cancelled")*Sales!E2:E331*Sales!F2:F331)     → 4.69
```

- The **values** are the discounts, `Sales!G2:G331`.
- The **weights** are each line's value before discount, quantity × list price: `Sales!E2:E331*Sales!F2:F331`. Multiplying by `(Sales!H2:H331<>"Cancelled")` makes the weight 0 for cancelled lines.
- The top line adds up value × weight; the bottom line adds up the weights. It's a second `SUMPRODUCT`, not a `SUM`, because the weights are calculated inside the formula.

The weighted average discount is **4.69%**, not 4.06%, because the big lines carry the bigger discounts. When someone asks for "the average", ask what it should be weighted by.

**A distinct count.** *"How many orders (not lines) were valid?"*

```excel
=SUMPRODUCT((Sales!H2:H331<>"Cancelled")/COUNTIFS(Sales!A2:A331,Sales!A2:A331))     → 173
```

`COUNTIFS(A, A)` returns, for every row, how many rows share its order ID. An order with three lines gets 3 on each line, so each line contributes 1/3 and the order adds up to 1. The status test works line by line, so this relies on every line of an order having the same status. That's true in this file, because Riverstone cancels whole orders, but check it before you reuse the formula on other data. The same trick with the customer column, `=SUMPRODUCT(1/COUNTIF(Sales!M2:M331,Sales!M2:M331))`, counts **23** customers. Section 11.6 shows a shorter way in Microsoft 365.

> **Watch out: SUMPRODUCT on whole columns.** `SUMPRODUCT((A:A="x")*B:B)` makes Excel multiply a million rows. Use exact ranges or table columns. Every array in a `SUMPRODUCT` must also be the same size, or it returns `#VALUE!`.

### Averages that mean something: line, order, and customer

"Average sale" has at least three meanings, and they give very different answers:

| Question | Formula idea | Result |
|---|---|---|
| Average **line** value (valid) | `AVERAGEIFS(J, H, "<>Cancelled")` | ₹13,298.99 |
| Average **Wholesale line** | `AVERAGEIFS(J, N, "Wholesale", H, "<>Cancelled")` | ₹16,215.80 |
| Average **order** value (AOV) | valid revenue ÷ distinct valid orders | ₹25,060.53 |
| Average **Wholesale order** | Wholesale revenue ÷ distinct Wholesale orders | ₹30,957.43 |

The AOV formula combines the two tools:

```excel
=SUMIFS(Sales!J2:J331,Sales!H2:H331,"<>Cancelled")/SUMPRODUCT((Sales!H2:H331<>"Cancelled")/COUNTIFS(Sales!A2:A331,Sales!A2:A331))     → 25060.53
```

Chapter 23 defines average order value as a KPI; the grain matters there too.

> **Watch out: AVERAGEIFS with no matches.** If no row meets the conditions, `AVERAGEIFS` returns `#DIV/0!`. Wrap it: `=IFERROR(AVERAGEIFS(…),"no sales")`. `AVERAGEIFS` also ignores blank cells in the average range but counts zeros, so a zero typed in place of "no data" pulls averages down.

### MAXIFS and MINIFS

```excel
=MAXIFS(Sales!J2:J331,Sales!N2:N331,"Retail",Sales!H2:H331,"<>Cancelled")     → 49875
=MAXIFS(Sales!B2:B331,Sales!N2:N331,"Wholesale")                             → 2025-12-17
=MINIFS(Sales!G2:G331,Sales!G2:G331,">0")                                    → 5
```

The biggest Retail line was ₹49,875; the last Wholesale order came on 17 December (format the cell as a date); the smallest discount actually given was 5%. `MAXIFS` on a date column is the cleanest way to find "latest order per customer" in a customer list.

### Patterns you'll build every week

Add a new sheet named **Report** for these patterns; later sections reuse what you build on it.

**A two-dimensional grid with mixed references.** On the Report sheet, type the segments down column F (`F16:F18`: Hospitality, Retail, Wholesale) and the quarters across row 15 (`G15:J15`: Q1 to Q4):

```excel
G16:  =SUMIFS(Sales!$J$2:$J$331,Sales!$N$2:$N$331,$F16,Sales!$L$2:$L$331,G$15,Sales!$H$2:$H$331,"<>Cancelled")
```

Fill it across and down. `$F16` always reads the segment column; `G$15` always reads the quarter row. Twelve cells from one formula give the same grid as the pivot table you'll build in section 11.5, and the grid stays exactly where you put it, which is why finance teams often prefer `SUMIFS` grids to pivots for fixed-layout reports.

**A monthly table.** Higher up on the same Report sheet, type the twelve month starts (1 January 2025 to 1 December 2025) in `F2:F13`, and put each month's valid revenue beside them:

```excel
G2:  =SUMIFS(Sales!$J$2:$J$331,Sales!$K$2:$K$331,F2,Sales!$H$2:$H$331,"<>Cancelled")
```

Fill it down to `G13`. January shows **202640**. Sections 11.4 and 11.6 reuse this table.

**A running total (year to date).**

```excel
I2:  =SUMIFS(Sales!$J$2:$J$331,Sales!$B$2:$B$331,"<="&EOMONTH(F2,0),Sales!$H$2:$H$331,"<>Cancelled")
```

`EOMONTH(F2,0)` is the last day of F2's month (Chapter 10), so each row adds every valid line up to the end of its month. September's row shows **₹25,81,168.75** and December's **₹43,35,471**; you'll get the same numbers from a pivot (section 11.5) and from DAX (section 11.8). The alternative, `=SUM($G$2:G2)` on the monthly column, works too, and uses Chapter 10's expanding range.

**A rank.** With the monthly revenue in `G2:G13`:

```excel
H2:  =RANK.EQ(G2,$G$2:$G$13,0)
```

`RANK.EQ(number, ref, [order])` takes the number to rank, the list to rank it in, and the order: `0` (or leaving it out) means the largest value ranks 1; `1` means the smallest ranks 1. October ranks **1** and June **12**. `RANK.EQ` gives tied values the same rank (two lines worth ₹51,520 both rank 2, and the next rank is 4). To rank *within a group*, such as customers within their segment, use `COUNTIFS`: `=COUNTIFS(segment_col,segment_cell,revenue_col,">"&revenue_cell)+1`.

**Share of total.** `=G2/SUM($G$2:$G$13)`, or for a segment, `=SUMIFS(…"Wholesale"…)/SUMIFS(…all valid…)` → 0.393 (39.3%).

**A total that ignores errors.** If a column contains an `#N/A` from a failed lookup, `SUM` returns `#N/A`. `AGGREGATE` can skip errors: `=AGGREGATE(9,6,range)`, where `9` means SUM and `6` means "ignore error values". It also ignores rows hidden by filters with the right option. Use it for display totals, and fix the errors themselves before the report goes out.

---

## 11.3 The everyday function toolkit

Excel has more than 500 functions, but a working analyst uses about 60 of them constantly. Chapter 10 covered the basics. This section covers the rest of that core set, grouped by the job they do. Each table gives the function's arguments (square brackets mean the argument is optional), a Riverstone example, and its result. Type the examples on a spare sheet: every reference starts with `Sales!`, so `Sales!J5` is row 5 of the Sales sheet wherever you type it. The Google Sheets column says whether Sheets has the same function. Functions you'll need less often are collected in a reference card at the end of the section.

### Decisions: IF, IFS, SWITCH, CHOOSE, IFERROR, IFNA

| Function | Example | Result | Sheets |
|---|---|---|---|
| `IF(test, if_true, if_false)` | `=IF(Sales!J5>=30000,"Large","Not large")` | Large (row 5 is ₹32,062.50) | Yes |
| `IFS(test1, value1, …)` | `=IFS(Sales!J2>=30000,"Large",Sales!J2>=10000,"Medium",TRUE,"Small")` | Small (row 2 is ₹2,900) | Yes |
| `SWITCH(value, match1, result1, …, [default])` | `=SWITCH(Sales!H2,"Delivered","Closed","Shipped","In transit","Pending","Open","Cancelled","Void")` | Closed | Yes |
| `CHOOSE(n, item1, item2, …)` | `=CHOOSE(ROUNDUP(MONTH(Sales!B2)/3,0),"Q1","Q2","Q3","Q4")` | Q1 | Yes |
| `IFERROR(value, if_error)` | `=IFERROR(Sales!J2/Sales!E2,0)` | 290 | Yes |
| `IFNA(value, if_na)` | `=IFNA(XLOOKUP("9999",Customers!A2:A25,Customers!B2:B25),"not found")` | not found | Yes |
| `AND`, `OR`, `NOT` | `=NOT(Sales!H2="Cancelled")` | TRUE | Yes |

- **`SWITCH`** compares one value with a list of exact matches, which is neater than nested `IF`s when you're translating codes (status codes, region codes, grades). An optional last argument is the default, returned when nothing matches.
- **`CHOOSE`** picks the *n*th item from a list; here `ROUNDUP(MONTH/3)` turns a month into a quarter number, and `CHOOSE` turns 1–4 into labels.
- **`IFERROR`** here divides row 2's net revenue by its quantity: ₹2,900 for 10 units is ₹290 a unit after discount. If the quantity were blank or 0, the division would give `#DIV/0!`, and `IFERROR` shows 0 instead.
- **`IFNA`** catches only `#N/A`, the "not found" error, and lets other errors through. That's safer than `IFERROR` for lookups, because a typo in a range name still shows up as `#REF!` or `#NAME?`. There's no customer 9999, so the `XLOOKUP` returns `#N/A` and `IFNA` shows "not found".

Applied to all valid lines, the `IFS` size bands give **158** Small (under ₹10,000), **142** Medium, and **26** Large (₹30,000 or more).

### Text: SEARCH, TEXTBEFORE, TEXTAFTER, TEXTSPLIT, TEXTJOIN, REPT, EXACT

| Function | Example | Result | Sheets |
|---|---|---|---|
| `SEARCH(find, within, [start])` | `=SEARCH("box","Lunch Box Set")` | 7 (not case-sensitive, allows wildcards) | Yes |
| `FIND(find, within, [start])` | `=FIND("box","Lunch Box Set")` | `#VALUE!` (case-sensitive) | Yes |
| `TEXTBEFORE(text, delimiter)` | `=TEXTBEFORE("Neha Kulkarni"," ")` | Neha | No (use `LEFT` + `FIND`) |
| `TEXTAFTER(text, delimiter)` | `=TEXTAFTER("Neha Kulkarni"," ")` | Kulkarni | No (use `MID` + `FIND`) |
| `TEXTSPLIT(text, delimiter)` | `=TEXTSPLIT("02.01.2025\|SO10001\|C0002","\|")` | 02.01.2025 · SO10001 · C0002 (three cells) | No (use `SPLIT`) |
| `TEXTJOIN(delimiter, ignore_empty, text1, …)` | `=TEXTJOIN(", ",TRUE,IF(Customers!D2:D25="Wholesale",Customers!B2:B25,""))` | Coastal Foods, Northgate Distributors, … | Yes |
| `REPT(text, times)` | `=REPT("█",ROUND(0.393*20,0))` | ████████ (8 blocks: an in-cell bar for Wholesale's 39.3%) | Yes |
| `EXACT(text1, text2)` | `=EXACT("AB12","ab12")` | FALSE (case-sensitive comparison) | Yes |

`TEXTBEFORE`, `TEXTAFTER`, and `TEXTSPLIT` are Microsoft 365 functions; they replace most `LEFT`/`MID`/`FIND` combinations. `TEXTJOIN`'s second argument, `TRUE`, skips empty pieces; the `IF` inside gives each Wholesale customer's name and an empty text for everyone else, so the example lists every Wholesale customer in one cell: Coastal Foods, Northgate Distributors, Harbour Traders, Deccan Packaging, Western Logistics, Prime Wholesale. In older Excel it needs **Ctrl+Shift+Enter**; in Microsoft 365 it works as typed; in Google Sheets, wrap it in `ARRAYFORMULA` (section 11.10). `REPT` repeats a text: 0.393 × 20 rounds to 8, so a 20-block bar shows Wholesale's share as 8 blocks. The Timed challenge after the project uses these text functions to decode a whole shipment log.

### Dates: EDATE, WORKDAY.INTL, NETWORKDAYS.INTL

| Function | Example | Result | Sheets |
|---|---|---|---|
| `EDATE(start, months)` | `=EDATE(DATE(2025,1,31),1)` | 2025-02-28 | Yes |
| `WORKDAY.INTL(start, days, [weekend], [holidays])` | `=WORKDAY.INTL(DATE(2025,12,24),3,11)` | 2025-12-27 | Yes |
| | `=WORKDAY.INTL(DATE(2025,12,24),3,11,DATE(2025,12,25))` | 2025-12-29 | Yes |
| `NETWORKDAYS.INTL(start, end, [weekend], [holidays])` | `=NETWORKDAYS.INTL(DATE(2025,12,1),DATE(2025,12,31),11)` | 27 | Yes |

- **`EDATE`** adds whole months and clamps to the month's last day: one month after 31 January is 28 February. It's the right tool for "due one month after invoice".
- **`WORKDAY.INTL` and `NETWORKDAYS.INTL`** take a **weekend code**. `1` (the default) is Saturday–Sunday; `11` is **Sunday only**, common for Indian businesses that work six days a week. A delivery promised "3 working days" after 24 December, working Monday to Saturday, lands on 27 December; with 25 December as a holiday, on 29 December. December 2025 has 27 Monday-to-Saturday working days.

### Numbers and statistics: LARGE, SMALL, RANK.EQ, PERCENTILE, MODE, rounding

| Function | Example (all 330 lines, cancelled included) | Result |
|---|---|---|
| `LARGE(array, k)` | `=LARGE(Sales!J2:J331,2)` | 51520 (k = 2: the second-largest line) |
| `SMALL(array, k)` | `=SMALL(Sales!J2:J331,1)` | 546.25 (k = 1: the smallest) |
| `RANK.EQ(number, ref, [order])` | `=RANK.EQ(51520,Sales!J2:J331,0)` | 2 (order 0: the largest ranks 1) |
| `MEDIAN(range)` | `=MEDIAN(Sales!J2:J331)` | 10212.5 |
| `PERCENTILE.INC(array, k)` | `=PERCENTILE.INC(Sales!J2:J331,0.9)` | 26600 (k = 0.9: 90% of lines are at or below this) |
| `QUARTILE.INC(array, quart)` | `=QUARTILE.INC(Sales!J2:J331,1)` | 6127.5 (quart 1: a quarter of lines are at or below this) |
| `MODE.SNGL(range)` | `=MODE.SNGL(Sales!E2:E331)` | 15 (the most common quantity) |
| `CEILING.MATH(number, [significance])` | `=CEILING.MATH(45,10)/10` | 5 (45 rounds up to 50, a multiple of 10: cartons of 10 needed for 45 units) |
| `MOD(number, divisor)` | `=MOD(ROW(),2)=0` | TRUE on even rows (for banding rules) |
| `PMT(rate, nper, pv)` | `=PMT(10%/12,36,-500000)` | 16133.59 |

- **`ROW`, `ROWS`, and `COLUMN`.** The `MOD` example uses `ROW()`, which returns the row number of the cell it's typed in: in row 7 it returns 7. `ROW(A5)` returns 5. `ROWS(range)` counts the rows in a range: `=ROWS(Sales!A2:A331)` returns 330. `COLUMN()` and `COLUMNS(range)` do the same for columns (`COLUMN(C1)` returns 3). `MOD` returns the remainder after division, so `MOD(ROW(),2)` is 0 on even rows.
- **`PMT(rate, nper, pv)`** takes the interest rate per period, the number of periods, and the loan amount (the present value), in that order. It answers a question every business asks: a ₹5,00,000 delivery-van loan at 10% a year over 36 months costs ₹16,133.59 a month. The rate and the number of periods must use the same unit, so the yearly 10% is divided by 12. The loan goes in as −500000 because it's money you receive; the payment then comes back positive. Its relatives `FV`, `PV`, `NPV`, `IRR`, and `XNPV` handle savings, investment, and project decisions, and work the same way in Google Sheets.

Chapter 4 (section 4.5) showed what the median and the mode say and when each is the right summary; Chapter 21 adds percentiles and spread.

### Checking values: ISNUMBER, ISTEXT, ISBLANK, ISERROR, TYPE

Chapter 10 used `ISNUMBER` and `ISTEXT` to see what a cell holds. They're also building blocks: `=SUMPRODUCT(--ISTEXT(Sales!E2:E331))` counts quantities stored as text (0 here), a one-cell data quality check. The `--` from section 11.2 turns TRUE and FALSE into 1 and 0. `ISBLANK` is TRUE only for truly empty cells, not for a formula returning `""`; test `=A2=""` when you mean "looks empty".

### Reference card: functions you'll meet less often

You don't need these on a first reading. Come back when a workbook uses one.

| Function | Example | Result |
|---|---|---|
| `XOR(test1, test2, …)` | `=XOR(Sales!G5>0,Sales!E5>=50)` | TRUE: exactly one test is true (row 5 has a 5% discount and 45 units) |
| `CLEAN(text)` | `=CLEAN(A2)` | A2's text without non-printing characters (such as line breaks from another system) |
| `SUBSTITUTE(text, old, new, [instance])` | `=SUBSTITUTE("SO-10001-A","-","",1)` | SO10001-A (instance 1: only the first dash goes; leave it out to replace every dash) |
| `NUMBERVALUE(text, decimal_sep, group_sep)` | `=NUMBERVALUE("4.335.471,00",",",".")` | 4335471 (European style: a comma for decimals, dots for thousands) |
| `MROUND(number, multiple)` | `=MROUND(47,10)` | 50 (the nearest multiple of 10) |
| `FLOOR.MATH(number, [significance])` | `=FLOOR.MATH(47,10)` | 40 (round down to a multiple of 10) |
| `WEEKNUM(date, [type])` | `=WEEKNUM(DATE(2025,12,29),1)` | 53 |
| `ISOWEEKNUM(date)` | `=ISOWEEKNUM(DATE(2025,12,29))` | 1 |
| `DATEDIF(start, end, unit)` | `=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"m")` | 10 (whole months) |
| | `=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"d")` | 315 (days) |
| | `=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"ym")` | 10 (months left after whole years) |
| | `=DATEDIF(DATE(2025,1,24),DATE(2025,12,5),"md")` | 11 (days left after whole months) |

- **Week numbers are a trap.** `WEEKNUM` (type 1) counts from 1 January, with weeks starting on Sunday, so 29 December 2025 is week **53**. `ISOWEEKNUM` follows the ISO 8601 standard, in which weeks start on Monday and week 1 contains the year's first Thursday, so the same date is week **1** of 2026. Agree on one system before building a weekly report.
- **`DATEDIF`** is an old function that isn't listed in Excel's function menus but still works: Sharma Hardware's first and last 2025 orders were 10 whole months (315 days) apart. Its units are `"y"` (whole years), `"m"` (whole months), `"d"` (days), `"ym"` (months left over after the whole years) and `"md"` (days left over after the whole months). The two dates are less than a year apart, so `"ym"` is also 10; 24 January plus 10 months is 24 November, and 24 November to 5 December is the 11 days `"md"` returns.
- All of these exist in Google Sheets except `NUMBERVALUE`; in Sheets use `SUBSTITUTE` to swap the separators, then `VALUE`.

### Back to Chapter 4: the rest of the numbers

Chapter 4 worked these out by hand. Open its workbook, `numbers_practice.xlsx`, and let the spreadsheet check each one. Say the answer from Chapter 4 before you press Enter.

**Percentage points and percent change (section 4.2).** On the **monthly** sheet, column E holds each month's gross margin: October in `E11` (27.9%) and November in `E12` (24.0%). Chapter 4's answer: a fall of 3.9 points, which is a 14.0% fall.

```excel
=(E12-E11)*100     → -3.9
=(E12-E11)/E11     → -0.140
```

The first formula, `(E12-E11)*100`, is the change in **percentage points**: November's margin minus October's (the margins are stored as fractions, so `*100` turns −0.039 into −3.9; format it with one decimal place). The second, `(E12-E11)/E11`, divides the same change by October's margin to get the **percent change**; format it as a percentage and it shows −14.0%.

**Shares that don't add up to 100% (section 4.6).** On the **segments** sheet, `C2:C4` holds each segment's share of revenue, and column D rounds it to a whole percentage:

```excel
D2:  =ROUND(C2*100,0)     → 39
```

`ROUND(number, digits)` with 0 digits rounds to a whole number, and `C2*100` turns the fraction 0.393 into 39.3 first. Filled down, D3 and D4 show 34 and 26, and `=SUM(D2:D4)` returns **99**, while `=SUM(C2:C4)` returns 1 (100%). Nothing is missing; each share rounded down a little.

**The mode (section 4.5).** Back in `ch11_practice.xlsx`, `=MODE.SNGL(Sales!E2:E331)` returns **15**, the most common quantity on a line, the same answer Chapter 4 found by counting.

**The denominator (section 4.3).** The same numerator over two denominators:

```excel
=SUMIFS(Sales!J2:J331,Sales!N2:N331,"Wholesale",Sales!H2:H331,"<>Cancelled")/COUNTIFS(Sales!N2:N331,"Wholesale",Sales!H2:H331,"<>Cancelled")     → 16215.80
```

That's Wholesale revenue per **line**: ₹17,02,658.50 over 105 lines. Chapter 4's revenue per **customer** divides the same ₹17,02,658.50 by the 6 Wholesale customers: ₹2,83,776.42. Both are correct; they answer different questions, and one is more than 17 times the other. Write the denominator into every label ("per line", "per customer").

> **Interview extra point.** A common live test is "count the customers whose revenue is above average, by segment, without a pivot table". Say the plan before typing: a customer list (with `UNIQUE` from section 11.6, or a copied list), revenue with `SUMIFS`, segment with a lookup, then `COUNTIFS` with a criterion joined to `AVERAGE`. Naming the functions and the order shows structured thinking even if the clock runs out.

---

## 11.4 Lookups in depth

Chapter 10 used `XLOOKUP` for one job: fetch a customer's name for an exact code. Real work needs more: a whole row of details at once, the right band from a price or rebate table, the most recent record, or a value where a row meets a column. Figure 11.2 compares the three lookup styles you'll meet.

![Customers sheet with the lookup column and return column outlined, and three formulas (XLOOKUP, INDEX/MATCH, VLOOKUP) that each return Hyderabad for code 0014](figures/fig11-2-three-lookups.svg)

*Figure 11.2 — Three ways to find the city for customer 0014. `XLOOKUP` and `INDEX`/`MATCH` point at the columns; `VLOOKUP` counts them, which is why it breaks when columns are inserted.*

### XLOOKUP, all its arguments

```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

| Argument | Values | Meaning |
|---|---|---|
| `if_not_found` | any value | What to show when nothing matches (default `#N/A`) |
| `match_mode` | `0` (default) | Exact match |
| | `-1` | Exact match, or the next **smaller** value |
| | `1` | Exact match, or the next **larger** value |
| | `2` | Wildcards: `*` any text, `?` one character (both apps) |
| `search_mode` | `1` (default) | Search from first to last |
| | `-1` | Search from **last to first** |
| | `2`, `-2` | Binary search on sorted data (fast, but wrong if the data isn't sorted) |

Everything below works in Microsoft 365, Excel 2021 or later, Excel for the web, and Google Sheets.

**Return several columns at once.** *"Show name, city, and segment for customer 0014."*

```excel
=XLOOKUP("0014", Customers!A2:A25, Customers!B2:D25)
```

The return array is three columns wide, so the result is three cells: **Deccan Packaging · Hyderabad · Wholesale**. You type the formula in one cell and the other two fill in by themselves, in Excel and in Google Sheets. This is called **spilling**, and section 11.6 explains it; for now, keep the two cells to the right empty.

**The most recent match.** *"When did Sharma Hardware last order?"* The Sales table is sorted by date, so searching from the bottom finds the latest line:

```excel
=XLOOKUP("0001", Sales[customer_code], Sales[order_date], "never", 0, -1)
```

The result is **2025-12-05** (order 10161). With the default `search_mode` of 1, the same formula returns the *first* order, 2025-01-24 (order 10007). Home Plus (`0016`) placed no orders in 2025, so its lookup returns "never".

> **Watch out: "last" means last in the list.** `search_mode` `-1` finds the last matching *row*, not the latest *date*. If the data isn't sorted by date, sort it first, or use `MAXIFS(Sales[order_date], Sales[customer_code], "0001")` (section 10.10), which finds the latest date regardless of order.

### Approximate match: bands and tiers

Many business rules are **bands**: commission rates by sales, freight by order value, tax slabs by income. Riverstone's (illustrative) annual volume rebate works like this, on the **RebateBands** sheet:

| annual_revenue_from | rebate_pct | band |
|---|---|---|
| 0 | 0 | Standard |
| 2,50,000 | 1 | Silver |
| 4,00,000 | 2 | Gold |

A customer with ₹5,02,775 of revenue is in the Gold band, because ₹5,02,775 is at least ₹4,00,000. The lookup must find the **largest threshold that is less than or equal to** the value: exact, or the next smaller.

```excel
=XLOOKUP(502775, RebateBands!A2:A4, RebateBands!C2:C4, , -1)
```

The result is **Gold**. Western Logistics, with ₹2,48,727.50, gets **Standard**: it's ₹1,272.50 short of the Silver threshold.

Applied to all 23 customers who ordered in 2025, 2 are Gold (Sharma Hardware and Harbour Traders), 6 are Silver, and 15 are Standard, and the rebates total **₹37,642.03**.

> **Watch out: blank `if_not_found`.** In `XLOOKUP(value, A, C, , -1)` the two commas leave `if_not_found` empty so that `-1` lands in the `match_mode` position. Count your commas: `XLOOKUP(value, A, C, -1)` would treat `-1` as the "not found" value and do an exact match.

### INDEX and MATCH

Before `XLOOKUP`, analysts combined two functions, and you'll meet this pattern in almost every inherited workbook. It also works in every Excel version.

- `MATCH(value, range, 0)` returns the **position** of a value in a one-column range. `=MATCH("0014", Customers!A2:A25, 0)` returns **14**: `0014` is the 14th code in the list.
- `INDEX(range, position)` returns the item at that position. `=INDEX(Customers!C2:C25, 14)` returns **Hyderabad**.

Put them together:

```excel
=INDEX(Customers!C2:C25, MATCH("0014", Customers!A2:A25, 0))
```

`MATCH`'s last argument is the match type: `0` for exact, `1` for "largest value less than or equal to" (the range must be sorted ascending), and `-1` for "smallest value greater than or equal to" (sorted descending). The rebate band with `INDEX`/`MATCH`:

```excel
=INDEX(RebateBands!C2:C4, MATCH(502775, RebateBands!A2:A4, 1))     → Gold
```

### Two-way lookups

*"What did Wholesale customers buy in October?"* When you have a summary grid with months down the side and segments across the top, you need the value where a row meets a column.

First build the grid, on a new sheet named **Grid**. Type the twelve month starts (1 January 2025 to 1 December 2025) in `A5:A16` and the segments in `B4:D4` (Hospitality, Retail, Wholesale). Then fill one formula across and down `B5:D16`, the mixed-reference grid from section 11.2:

```excel
B5:  =SUMIFS(Sales!$J$2:$J$331,Sales!$K$2:$K$331,$A5,Sales!$N$2:$N$331,B$4,Sales!$H$2:$H$331,"<>Cancelled")
```

Now find the row and the column separately, so you can see each piece:

```excel
=MATCH(DATE(2025,10,1), A5:A16, 0)     → 10
=MATCH("Wholesale", B4:D4, 0)          → 3
```

October is the 10th month in the list, and Wholesale is the 3rd segment. `INDEX` with two positions, a row and a column, returns the cell where they meet:

```excel
=INDEX(B5:D16, MATCH(DATE(2025,10,1), A5:A16, 0), MATCH("Wholesale", B4:D4, 0))     → 207827
```

Wholesale customers bought **₹2,07,827** in October. The `XLOOKUP` version nests one lookup inside another: the inner one returns October's whole row, and the outer one picks the Wholesale column from it.

```excel
=XLOOKUP("Wholesale", B4:D4, XLOOKUP(DATE(2025,10,1), A5:A16, B5:D16))
```

The inner `XLOOKUP(DATE(2025,10,1), A5:A16, B5:D16)` finds October in the month column and returns its three segment values. The outer one looks for "Wholesale" in the header row `B4:D4` and returns the matching value from that row: 207827 again.

### XMATCH: a better MATCH

`XMATCH(value, lookup_array, [match_mode], [search_mode])` is `MATCH` with `XLOOKUP`'s options: exact match by default, wildcards, and searching from the end. `=XMATCH("0014", Customers!A2:A25)` returns **14**. Use it inside `INDEX` exactly as you'd use `MATCH`. (Microsoft 365 and Excel 2021 or later; Google Sheets has `XMATCH` too.)

### Lookups with more than one condition

*"What was the first order in which Harbour Traders bought Industrial Crates?"* No single column identifies the row; two conditions do. Multiply the tests, which gives 1 only where both are true, and look up the 1:

```excel
=XLOOKUP(1, (Sales!M2:M331="Harbour Traders")*(Sales!P2:P331="Industrial Crate"), Sales!A2:A331, "none")
```

The result is **order 10057** (27 May 2025). The same idea with `INDEX`/`MATCH`, for any Excel version:

```excel
=INDEX(Sales!A2:A331, MATCH(1, (Sales!M2:M331="Harbour Traders")*(Sales!P2:P331="Industrial Crate"), 0))
```

In Excel 2019 and older, confirm it with **Ctrl+Shift+Enter** so Excel treats it as an array formula (curly brackets appear around it). In Microsoft 365 and Google Sheets, press Enter; in Sheets, wrap the multiplication in `ARRAYFORMULA` if it returns an error. Harbour Traders bought crates in 7 lines, which `COUNTIFS` confirms.

The older alternative is a **helper key**: a column that joins the fields, such as `=M2&"|"&P2`, and an ordinary lookup on `"Harbour Traders|Industrial Crate"`. It's fast and simple to audit, at the cost of an extra column.

### Wildcard and partial-match lookups

*"What's the code for the customer with 'Bay' in its name?"*

```excel
=XLOOKUP("*Bay*", Customers!B2:B25, Customers!A2:A25, "none", 2)
```

`match_mode` `2` switches on wildcards, and the result is **0008** (Blue Bay Cafe). `INDEX`/`MATCH` supports wildcards with match type 0: `MATCH("*Bay*", Customers!B2:B25, 0)`. Partial matches return the **first** match, so check that the pattern is unique: `COUNTIF(Customers!B2:B25,"*Bay*")` should be 1.

### Case-sensitive lookups

Lookups ignore case: `"metro mart"` finds `Metro Mart`. When case matters (product codes such as `ab12` and `AB12`), use `EXACT` inside the lookup. Try it on a spare sheet: type `ab12` in `A2` and `AB12` in `A3`, and `first` in `B2` and `second` in `B3`.

```excel
=XLOOKUP("AB12", A2:A3, B2:B3)                 → first
=XLOOKUP(TRUE, EXACT(A2:A3, "AB12"), B2:B3)    → second
```

The plain lookup ignores case, so `ab12` in row 2 counts as a match and it returns **first**. `EXACT(A2:A3, "AB12")` compares each code with `AB12`, case and all, and gives FALSE, TRUE; the lookup then finds the first TRUE and returns **second**.

### Returning a whole row or column

`INDEX` with a row or column number of **0** returns the entire column or row, which you can then sum, average, or chart. With the segment-by-quarter grid on the Report sheet from section 11.2 (segments in `F16:F18`, quarters in `G15:J15`, values in `G16:J18`):

```excel
=SUM(INDEX(G16:J18, 0, MATCH("Q2", G15:J15, 0)))          → 726568.25
=SUM(INDEX(G16:J18, MATCH("Wholesale", F16:F18, 0), 0))   → 1702658.5
```

The first adds Q2's column, the second adds Wholesale's row. `XLOOKUP` does the same when the return array is a block: `=SUM(XLOOKUP("Q2", G15:J15, G16:J18))`.

### The last match, in any version

Before `XLOOKUP`'s `search_mode`, analysts used a trick with the old `LOOKUP` function:

```excel
=LOOKUP(2, 1/(Sales!C2:C331="0001"), Sales!A2:A331)     → 10161
```

`1/(test)` gives 1 where the test is true and `#DIV/0!` elsewhere. `LOOKUP` searches for 2, can't find it, ignores the errors, and returns the value for the **last** 1. You'll meet it in older workbooks; in new ones, use `XLOOKUP` with `search_mode` `-1`.

### INDIRECT and OFFSET: references built by formulas

Two functions build references while the formula runs. They're useful, occasionally essential, and the source of many slow and fragile workbooks.

**`INDIRECT(text)`** turns text into a reference. The messy month-end workbook has one sheet per month, named `Jan`, `Feb`, … with the month names in `A4:A15` of its Summary sheet. Build the reference as text first, in a spare column of the Summary sheet (column G, say):

```excel
G4:  ="'"&A4&"'!J2:J100"     → 'Jan'!J2:J100
```

- `"'"` is a single quote typed inside double quotes: a piece of text one character long.
- `&` joins the pieces: a single quote, the sheet name from `A4` (Jan), then `'!J2:J100`.
- The result is the **text** `'Jan'!J2:J100`, exactly what you'd type to point at another sheet. The single quotes protect sheet names that contain spaces; they do no harm when there are none.

`INDIRECT` turns that text into a real reference:

```excel
H4:  =SUM(INDIRECT(G4))     → 202640
```

January's lines total ₹2,02,640. Now put the same idea inside `SUMIFS`, so the cancelled rule applies, and fill it down:

```excel
=SUMIFS(INDIRECT("'"&A4&"'!J2:J100"), INDIRECT("'"&A4&"'!H2:H100"), "<>Cancelled")
```

It returns the correct valid total for every month in which the pasted data is correct, including October's full ₹6,81,070.75 that the hand-built formula missed. (December still shows ₹4,86,378.50, because `INDIRECT` can't know that five rows were pasted twice.)

**`OFFSET(start, rows, cols, [height], [width])`** returns a range a given distance from a starting cell. *"Sum the last three months that have data."* With the monthly revenue on the Report sheet (section 11.2) in `G2:G13`:

```excel
=SUM(OFFSET(G2, COUNT(G2:G13)-3, 0, 3, 1))     → 1754302.25
```

`COUNT` finds 12 months, so the range starts 9 rows below `G2` and is 3 rows tall: October to December.

> **Watch out: volatile and invisible.** `INDIRECT` and `OFFSET` are **volatile**: Excel recalculates them after every change anywhere in the workbook, which slows large files. Their references are text, so renaming a sheet breaks `INDIRECT` silently, and **Trace Precedents** can't follow them. Prefer tables, `INDEX` (`=SUM(INDEX(G2:G13,COUNT(G2:G13)-2):INDEX(G2:G13,COUNT(G2:G13)))` does the same job without being volatile: two `INDEX` results joined by `:` make a range from the 10th to the 12th month), the newer functions in section 11.6, or Power Query's folder combine (section 11.7).

### VLOOKUP and HLOOKUP: recognize, then replace

`VLOOKUP(value, table, column_number, FALSE)` looks in the **first** column of a table and returns the column at position `column_number`. `HLOOKUP` does the same sideways. Three traps:

1. **The fourth argument defaults to approximate.** Leave out `FALSE` and an unsorted list returns plausible wrong answers.
2. **The column number is a count.** Insert a column inside the table and `3` now points at a different column, with no error.
3. **It can only look right.** The lookup column must be the first column of the table.

For bands, `VLOOKUP(value, RebateBands!A2:C4, 3, TRUE)` is legitimate and returns Gold for ₹5,02,775, because that's a deliberate approximate match on a sorted table. For everything else, use `XLOOKUP` or `INDEX`/`MATCH`.

> **Interview extra point.** Asked "`VLOOKUP` or `INDEX`/`MATCH`?", say what breaks: `VLOOKUP` depends on a column count and only looks right; `INDEX`/`MATCH` and `XLOOKUP` point at the columns directly. Then mention approximate matching for bands. That answer shows you've maintained real workbooks, not only learned syntax.

---

## 11.5 Pivot tables

A **pivot table** summarizes a table by dragging fields into four areas. It's the fastest way to answer "how much, by what?" and it's the single most used analysis feature in business spreadsheets. Figure 11.3 shows what each area does.

![Pivot table field list areas (Filters, Rows, Columns, Values), each with the field placed in it and what it does, above the resulting segment by quarter table totaling 43,35,471](figures/fig11-3-pivot-areas-group-by.svg)

*Figure 11.3 — A pivot table's four areas and what each one does. The result shows 2025 net revenue by segment and quarter, excluding cancelled orders.*

### Build your first pivot table

*"How much net revenue did each segment bring in, each quarter?"*

**Excel**

1. Click inside the Sales table. **Insert → PivotTable → From Table/Range**. Check the range says `Sales`, choose **New Worksheet**, and click **OK**.
2. In the **PivotTable Fields** pane, drag `segment` to **Rows**, `quarter` to **Columns**, and `net_revenue` to **Values**. Excel names it *Sum of net_revenue*.
3. Drag `status` to **Filters**. In the filter cell above the pivot, click the arrow, tick **Select Multiple Items**, and clear **Cancelled**.
4. Right-click any number, **Number Format…**, choose **Number** with a thousands separator and 0 decimals.

**Google Sheets**

1. Click inside the Sales data. **Insert → Pivot table**, confirm the range, choose **New sheet**, and click **Create**.
2. In the **Pivot table editor**, next to **Rows** click **Add** and choose `segment`; next to **Columns** add `quarter`; next to **Values** add `net_revenue` (**Summarize by: SUM**).
3. Next to **Filters**, add `status`, open **Status**, and clear **Cancelled** (or **Filter by condition → Text does not contain → Cancelled**).

Both give the table in Figure 11.3:

| segment | Q1 | Q2 | Q3 | Q4 | Grand Total |
|---|---|---|---|---|---|
| Hospitality | 1,49,040.00 | 2,52,170.00 | 3,07,277.50 | 4,35,551.25 | 11,44,038.75 |
| Retail | 3,94,327.50 | 1,98,473.75 | 3,33,972.50 | 5,62,000.00 | 14,88,773.75 |
| Wholesale | 1,90,944.00 | 2,75,924.50 | 4,79,039.00 | 7,56,751.00 | 17,02,658.50 |
| **Grand Total** | **7,34,311.50** | **7,26,568.25** | **11,20,289.00** | **17,54,302.25** | **43,35,471.00** |

The grand total is ₹43,35,471, the same as Chapter 10's tracker. ✓ What would have taken twelve `SUMIFS` formulas took four drags. Retail led in Q1; Wholesale grew every quarter and more than doubled from Q2 to Q4.

### Summaries other than sum

Values don't have to be sums. **Excel:** right-click a value → **Summarize Values By** → **Count**, **Average**, **Max**, **Min**. **Sheets:** in the editor, change **Summarize by**.

> **Watch out: counting lines is not counting orders.** Put `order_id` in Values and choose **Count**, and Wholesale shows **105**: that's order *lines*. Riverstone received **55** Wholesale orders. For distinct counts, **Excel:** when creating the pivot, tick **Add this data to the Data Model**, then **Summarize Values By → More Options → Distinct Count**. **Sheets:** **Summarize by: COUNTUNIQUE**. Distinct orders by segment: Hospitality 59, Retail 59, Wholesale 55, which add to 173. ✓

### Show values as a percentage or a difference

*"What share of revenue does each segment contribute?"* Put `net_revenue` in Values a second time, then:

- **Excel:** right-click it → **Show Values As → % of Grand Total**.
- **Sheets:** in the value's settings, **Show as → % of grand total**.

Wholesale **39.3%**, Retail **34.3%**, Hospitality **26.4%**.

*"How did each month change from the one before?"* With `month_start` in Rows (grouped by month, below), **Excel: Show Values As → Difference From**, **Base field:** `month_start`, **Base item:** **(previous)**. June shows **−1,42,430.75** (₹1,86,928 against May's ₹3,29,358.75). Google Sheets' **Show as** offers only percentages of row, column, and grand total, so in Sheets add a formula beside the pivot or use Chapter 10's tracker for month-on-month changes.

### Grouping dates

Pivot tables can group a date field into months, quarters, or years without helper columns.

- **Excel:** put `order_date` in Rows. Recent versions group it automatically; otherwise right-click a date → **Group…** → select **Months** and **Quarters** (and **Years** if the data spans more than one).
- **Sheets:** put `order_date` in Rows, right-click a date in the pivot → **Create pivot date group** → **Year-Month** or **Quarter**.

The practice table also has `month_start` and `quarter` columns, which are more predictable when a workbook will be used by other people or in both apps.

### Sort, filter, and top N

*"Which three products brought in the most revenue?"* Put `product_name` in Rows and `net_revenue` in Values, then:

- **Excel:** click the Row Labels arrow → **Value Filters → Top 10…** → **Top 3 Items by Sum of net_revenue**. Sort with **More Sort Options → Descending by Sum of net_revenue**.
- **Sheets:** under Rows, set **Order: Descending** and **Sort by: SUM of net_revenue**; read the top three.

The top three: **Storage Box 25L ₹9,08,212.50**, **Storage Box 10L ₹8,60,946.00**, and **Industrial Crate ₹7,95,830.00**. The Garden Chair sold only ₹33,637.50 all year.

### Slicers and timelines

A **slicer** is a set of filter buttons that sits beside a pivot table, which managers find far friendlier than filter dropdowns.

- **Excel:** click the pivot → **PivotTable Analyze → Insert Slicer** → tick `segment` and `sales_rep`. For dates, **PivotTable Analyze → Insert Timeline** → `order_date`. One slicer can control several pivots: right-click it → **Report Connections**.
- **Sheets:** **Data → Add a slicer**, choose the data range and the column. Sheets slicers filter every pivot table and chart built on that range.

*"How did Rahul Mehta's quarters look?"* With a rep-by-quarter pivot, click **Rahul Mehta** on the slicer: Q1 ₹2,78,630, Q2 ₹1,93,720, Q3 ₹3,38,761.50, Q4 **₹6,82,889**, the highest Q4 of any rep.

### Refresh, and the traps that come with it

- **Excel pivot tables don't update by themselves.** After the data changes, click **PivotTable Analyze → Refresh** (**Alt+F5**) or **Data → Refresh All** (**Ctrl+Alt+F5**). To refresh every time the file opens: **PivotTable Options → Data → Refresh data when opening the file**.
- **Build on a table, not a range.** A pivot built on `A1:S331` won't see row 332. A pivot built on the `Sales` table sees every row the table grows to. If a pivot was built on a range, fix it with **PivotTable Analyze → Change Data Source**.
- **Google Sheets pivot tables update automatically** when the source data changes, but their range is fixed too; use an open-ended range such as `Sales!A1:S` or a table.

> **Watch out: a pivot built before the rule was agreed.** If the `status` filter is added later, every number in the pivot changes. Put the filter (or a `valid` column) in from the start, and write the rule in the sheet's title, as in Chapter 10.

### GETPIVOTDATA: reading numbers out of a pivot table

A report page often needs a handful of numbers from a pivot, placed in a fixed layout (a KPI panel, a board-pack table). Typing `=C7` breaks as soon as the pivot is rearranged or a new segment appears. `GETPIVOTDATA` asks the pivot for a value by **field names and items** instead of by position:

```excel
=GETPIVOTDATA("net_revenue", $A$3, "segment", "Wholesale", "quarter", "Q4")     → 756751
```

| Argument | Here | Meaning |
|---|---|---|
| `data_field` | `"net_revenue"` | The value field (the name of the source field; `"Sum of net_revenue"` also works) |
| `pivot_table` | `$A$3` | Any cell inside the pivot table |
| `field1, item1` | `"segment", "Wholesale"` | Which row item |
| `field2, item2` | `"quarter", "Q4"` | Which column item |

Leave out a field to get its total: `=GETPIVOTDATA("net_revenue", $A$3, "segment", "Retail")` returns **14,88,773.75**, Retail's grand total across quarters, and `=GETPIVOTDATA("net_revenue", $A$3)` returns the grand total, 43,35,471.

**Make it dynamic.** Replace the typed items with cells, and one formula fills a whole report grid:

```excel
C6:  =GETPIVOTDATA("net_revenue", Pivot!$A$3, "segment", $B6, "quarter", C$5)
```

With segments in `B6:B8` and quarters in `C5:F5`, fill it across and down. The report now keeps its own layout and formatting, while the pivot underneath can be refreshed, filtered with slicers, or rearranged.

How to get the formula without typing it: in Excel, type `=` and **click a value cell inside the pivot**. Excel writes the `GETPIVOTDATA` for you (if **PivotTable Analyze → Options → Generate GetPivotData** is ticked). Then replace the items with cell references. When you want a plain cell address instead (to copy a formula down beside the pivot, say), untick **Generate GetPivotData** in the same place, and clicking a pivot cell gives `=C7` again.

> **Watch out: GETPIVOTDATA returns #REF! when the item isn't visible.** If a slicer hides Wholesale, or the pivot no longer shows quarters, the formula can't find the cell and returns `#REF!`. Wrap it with `IFERROR(…, 0)` only when a missing item really means zero, and keep the fields it needs in the pivot. Google Sheets has `GETPIVOTDATA` too, with the same idea and argument order: `=GETPIVOTDATA("SUM of net_revenue", A3, "segment", "Wholesale")`.

For pivots built on the Data Model (section 11.8), Excel writes `CUBEVALUE` formulas instead, which do the same job with a different syntax; **PivotTable Analyze → OLAP Tools → Convert to Formulas** turns a whole model pivot into editable `CUBEVALUE` cells.

### More ways to show values

Right-click a value → **Show Values As** (Excel) offers many calculations on top of the sum:

| Option | Riverstone example | Result |
|---|---|---|
| % of Grand Total | Wholesale | 39.3% |
| % of Row Total | Wholesale, Q4 (of Wholesale's year) | 44.4% |
| % of Column Total | Wholesale's share of Q4 | 43.1% |
| Difference From (previous) | June vs May | −1,42,430.75 |
| % Difference From (previous) | June vs May | −43.2% |
| Running Total In (month) | September, year to date | 25,81,168.75 |
| Rank Largest to Smallest (sales_rep) | Rahul Mehta, full year | 1 |

Every segment earned more than a third of its year in Q4 (Hospitality 38.1%, Retail 37.7%, Wholesale 44.4%), which **% of Row Total** shows at a glance. Google Sheets offers **% of row**, **% of column**, and **% of grand total**.

### Calculated fields, and why ratios need care

A **calculated field** adds a formula based on other fields' **totals**. *"What price did Riverstone actually realize per unit, after discounts?"* **Excel: PivotTable Analyze → Fields, Items & Sets → Calculated Field**, name `realized_price`, formula `= net_revenue / quantity`. **Sheets:** under **Values**, **Add → Calculated field**, formula `=SUM(net_revenue)/SUM(quantity)`.

With `product_name` in Rows, Industrial Crate shows **₹1,273.33** a unit against a list price of ₹1,400: 9.0% below list, the bulk discounts on large crate orders in another form. A calculated field divides the **sums**, which is right for a ratio. Averaging a per-line price column instead would weight a 5-unit line the same as a 45-unit line.

### Grouping numbers into bands

Put `net_revenue` in **Rows** as well as Values, right-click a row value → **Group…**, **Starting at** 0, **Ending at** 60000, **By** 10000. Excel groups lines by value band:

| Line value band | Lines | Net revenue (₹) |
|---|---|---|
| 0–9,999 | 158 | 9,12,950.50 |
| 10,000–19,999 | 106 | 14,95,979.50 |
| 20,000–29,999 | 36 | 8,74,648.50 |
| 30,000–39,999 | 14 | 4,71,117.50 |
| 40,000–49,999 | 9 | 4,21,035.00 |
| 50,000–59,999 | 3 | 1,59,740.00 |

Almost half the lines (158 of 326) are under ₹10,000, but they bring in only 21% of revenue. That's a distribution, and Chapter 15 turns it into a proper histogram.

### Report filter pages

**Excel: PivotTable Analyze → Options (dropdown) → Show Report Filter Pages.** With `sales_rep` in Filters, Excel copies the pivot onto a new sheet for **each rep**, filtered to that rep. It's a two-click way to produce one page per region, branch, or manager.

### Pivot charts and layout

**Excel: PivotTable Analyze → PivotChart.** The chart follows the pivot's filters and slicers. **Sheets:** select the pivot table and **Insert → Chart**; it updates with the pivot.

For reports that others will copy, change the layout to a plain table: **Excel: Design → Report Layout → Show in Tabular Form** and **Repeat All Item Labels**; turn off **Subtotals** if you don't need them.

---

## 11.6 Dynamic arrays: formulas that return whole tables

Almost every formula so far has returned one value into one cell; the three-column `XLOOKUP` in section 11.4 was the first exception. A **dynamic array** formula returns a whole list or table from a single cell, and the results **spill** into the cells below and to the right. When the source data changes, the result grows or shrinks by itself. Figure 11.4 shows the idea.

![A single SORT(UNIQUE()) formula in F2 spilling 23 customer names down column F, and the same formula showing #SPILL! because a note in F4 blocks it](figures/fig11-4-dynamic-array-spill.svg)

*Figure 11.4 — One formula, many results. The dashed outline is the spill range; any value typed inside it blocks the spill.*

Only `F2` holds a formula. The cells below show its results and can't be typed into; clear the blocking cell and the list spills again. Google Sheets spills the same way, and shows `#REF!` when a result is blocked.

Dynamic arrays are in Microsoft 365, Excel 2021 and later, Excel for the web, and Google Sheets. Excel 2019 and older can open the file but show only the first result, or an older array-formula version.

### UNIQUE, SORT, and SORTBY

*"List every customer who ordered in 2025, alphabetically."* Add a new sheet named **Lists**, and in `F2`:

```excel
=SORT(UNIQUE(Sales[customer_name]))
```

`UNIQUE(array)` returns each different value once, in the order it first appears; `SORT` puts the list in A-to-Z order. **23** names spill down, from Blue Bay Cafe, City Needs Store, Coastal Foods, Deccan Packaging, Evergreen Mart … Riverstone has 24 customers, but Home Plus didn't order in 2025, so it isn't in the sales data. Count them with `=COUNTA(UNIQUE(Sales[customer_name]))` → 23, or `=ROWS(UNIQUE(Sales[customer_name]))` (section 11.3), which counts the rows of the list.

`SORT` differs between the apps:

| | Excel | Google Sheets |
|---|---|---|
| Syntax | `SORT(array, [sort_index], [sort_order], [by_col])` | `SORT(range, sort_column, is_ascending, …)` |
| Descending by column 2 | `=SORT(A2:B24, 2, -1)` | `=SORT(A2:B24, 2, FALSE)` |
| Sort by another range | `SORTBY(array, by_array, -1)` | `SORT(range, by_range, FALSE)` |

*"Rank customers by revenue."* With the unique names in `F2` of the Lists sheet (the formula above), put their revenue next to them with `SUMIFS`, which accepts a spilled range as its criteria:

```excel
G2:  =SUMIFS(Sales[net_revenue], Sales[customer_name], F2#, Sales[status], "<>Cancelled")
```

In Excel, `F2#` means "the whole spill range that starts at F2", so `G2` spills 23 totals to match. Then `=SORTBY(F2#, G2#, -1)` lists customers from largest to smallest: Sharma Hardware ₹5,02,775, Harbour Traders ₹4,12,680.50, Northgate Distributors ₹3,53,088.50, Green Leaf Hotels ₹3,31,388.75, Metro Mart ₹3,29,297.50 … Google Sheets has no `#` operator; refer to a range that's big enough, such as `F2:F24`, or wrap the formula in `ARRAYFORMULA` (section 11.10).

### FILTER

*"Show November's Wholesale order lines."*

```excel
=FILTER(Sales[[order_id]:[net_revenue]], (Sales[month_start]=DATE(2025,11,1)) * (Sales[segment]="Wholesale"), "no rows")
```

15 rows spill out, starting with order 10139 from Harbour Traders on 6 November. Their net revenue totals **₹3,43,685.50**, matching Chapter 10's `SUMIFS`. ✓

How it works:

- The second argument is an **include** test that's TRUE or FALSE for every row. `(test1) * (test2)` means **AND** (TRUE × TRUE = 1); `(test1) + (test2)` means **OR**.
- The third argument is what to show when nothing matches. Without it, an empty result is a `#CALC!` error in Excel.
- `Sales[[order_id]:[net_revenue]]` is a table reference for the columns from `order_id` to `net_revenue`.

Google Sheets writes each condition as its own argument, and has no "if empty" argument:

```excel
=FILTER(Sales!A2:J331, Sales!K2:K331=DATE(2025,11,1), Sales!N2:N331="Wholesale")
```

`FILTER`'s output is live. Wrap it in `SUM`, `COUNTA`, or `SORT`: `=SUM(FILTER(Sales[net_revenue], Sales[segment]="Wholesale", 0))` works like `SUMIFS`, but `FILTER` can use conditions `SUMIFS` can't, such as `MONTH(Sales[order_date])=11` or `ISNUMBER(SEARCH("Box", Sales[product_name]))`.

### SEQUENCE and LET

`SEQUENCE(rows, [columns], [start], [step])` generates numbers. Twelve month starts for 2025, in one formula:

```excel
=DATE(2025, SEQUENCE(12), 1)
```

`SEQUENCE(12)` makes the numbers 1 to 12 in a column, so `DATE` builds twelve dates, one for each month number. Twelve cells spill down: 2025-01-01, 2025-02-01, … 2025-12-01 (format them as dates, or you'll see serial numbers such as 45658).

`LET` names parts of a formula so it's readable and calculates each part once. Its arguments come in pairs, a name and its value, and the last argument is the calculation that uses the names:

```excel
=LET(
    valid,  Sales[status]<>"Cancelled",
    rev,    FILTER(Sales[net_revenue], valid),
    margin, FILTER(Sales[gross_margin], valid),
    SUM(margin) / SUM(rev)
)
```

- `valid` is the status test: TRUE or FALSE for each of the 330 lines.
- `rev` and `margin` are the net revenue and gross margin of the valid lines, picked out with `FILTER` (above).
- `SUM(margin) / SUM(rev)` is the calculation. It uses the names, so each `FILTER` runs once.

The result is **0.262**: Riverstone's 2025 gross margin was **26.2%** of net revenue (₹11,37,221 on ₹43,35,471). Both apps support `LET`.

### Shaping arrays: TAKE, DROP, CHOOSECOLS, VSTACK, HSTACK, TOCOL

> **Second pass.** The rest of this section (shaping arrays, `LAMBDA` and its helpers, `GROUPBY` and `PIVOTBY`) can wait until after the project. The core ideas of dynamic arrays are above; these functions make them shorter.

Microsoft 365 has functions that cut, pick, and stack arrays, so a report table can be assembled in one formula. The examples use two things you've built: the customer list in `F2#` with its revenue in `G2#` on the **Lists** sheet (above), and the monthly revenue in `G2:G13` on the **Report** sheet (section 11.2).

| Function | Example | What it does |
|---|---|---|
| `TAKE(array, rows, [cols])` | `=TAKE(SORTBY(F2#, G2#, -1), 3)` | First 3 rows (negative numbers take from the end) |
| `DROP(array, rows, [cols])` | `=DROP(Sales!A1:S331, 1)` | Everything except the first row |
| `CHOOSECOLS(array, n, …)` | `=CHOOSECOLS(Sales!A2:S331, 1, 13, 10)` | Columns 1, 13, 10 in that order |
| `CHOOSEROWS(array, n, …)` | `=CHOOSEROWS(Report!G2:G13, 10, 11, 12)` | Rows 10–12 (October to December) |
| `VSTACK(a, b, …)` | `=VSTACK(Jan!A2:I16, Feb!A2:I21)` | Stack ranges on top of each other (the month sheets of the messy workbook) |
| `HSTACK(a, b, …)` | `=HSTACK(F2#, G2#)` | Put arrays side by side |
| `TOCOL(array, [ignore])` | `=TOCOL(Sales!I2:I331, 1)` | One column; ignore code 1 skips blanks |
| `EXPAND`, `WRAPROWS` | `=WRAPROWS(TOCOL(list), 4)` | Reshape a list into a grid |

*"A top-3 customer table with names and revenue, in one cell."*

```excel
=TAKE(SORTBY(HSTACK(F2#, G2#), G2#, -1), 3)
```

Read it from the inside out: `HSTACK` puts names and revenue side by side, `SORTBY` sorts that two-column table by revenue, largest first (`-1`), and `TAKE` keeps the first 3 rows. Result: Sharma Hardware ₹5,02,775.00, Harbour Traders ₹4,12,680.50, Northgate Distributors ₹3,53,088.50. Change the 3 to a cell reference and the reader chooses the length. Google Sheets has `VSTACK`, `HSTACK`, `TOCOL`, `CHOOSECOLS`, `CHOOSEROWS`, `WRAPROWS`, and `EXPAND`; for `TAKE`, use `ARRAY_CONSTRAIN` or `QUERY` with `limit`.

### LAMBDA: write your own functions

`LAMBDA` creates a function from a formula. Its last argument is the calculation; the ones before it are **parameter** names, placeholders for the values the function will be given.

```excel
=LAMBDA(qty, price, disc, qty*price*(1-disc/100))(45, 750, 5)     → 32062.5
```

The values in the second pair of brackets fill the parameters in order:

| Parameter | Value it receives | Used in the calculation as |
|---|---|---|
| `qty` | 45 | 45 units |
| `price` | 750 | ₹750 a unit |
| `disc` | 5 | 5% discount |

So the calculation is 45 × 750 × (1 − 5/100) = 32,062.5, the net revenue of order 10003's second line.

Typed like that, it's a curiosity. Its value comes when you **name** it: **Formulas → Name Manager → New**, name `NETREV`, and in **Refers to** enter `=LAMBDA(qty, price, disc, qty*price*(1-disc/100))`. Now every sheet in the workbook can use `=NETREV(E2, F2, G2)`, and the business rule lives in one place. Google Sheets has the same idea under **Data → Named functions**, where you define the formula and argument names.

### MAP, BYROW, BYCOL, SCAN, REDUCE

These **helper functions** pass each item (or row, or column) of an array to a `LAMBDA`.

| Function | Passes | Riverstone example | Result |
|---|---|---|---|
| `MAP(array, LAMBDA(x, …))` | Each value | `=MAP(Sales!E2:E331, Sales!F2:F331, Sales!G2:G331, NETREV)` | 330 net revenue values |
| `BYROW(array, LAMBDA(row, …))` | Each row | `=BYROW(Report!G16:J18, LAMBDA(r, SUM(r)))` | Segment totals: 11,44,038.75 · 14,88,773.75 · 17,02,658.50 |
| `BYCOL(array, LAMBDA(col, …))` | Each column | `=BYCOL(Report!G16:J18, LAMBDA(c, SUM(c)))` | Quarter totals |
| `SCAN(start, array, LAMBDA(acc, x, …))` | Each value, keeping a running result | `=SCAN(0, Report!G2:G13, LAMBDA(acc, x, acc+x))` | Running total ending 43,35,471 |
| `REDUCE(start, array, LAMBDA(acc, x, …))` | Each value, returning only the final result | see below | |

In `SCAN` and `REDUCE`, `acc` (the **accumulator**) carries the result so far, starting from the first argument, and `x` is the current item.

`REDUCE` needs one more idea first. Subtracting one range from another of the same size works item by item, so shifting the second range up by one row gives each month's change from the month before:

```excel
=Report!G3:G13-Report!G2:G12     → 11 values spill: 51024, 24343.5, … -193584.5
```

That's February minus January (+51,024), March minus February, and so on to December minus November (−1,93,584.50). `REDUCE` walks through those 11 changes and keeps the largest:

```excel
=REDUCE(0, Report!G3:G13-Report!G2:G12, LAMBDA(acc, x, MAX(acc, x)))     → 229032.75
```

It starts `acc` at 0, and for each change `x` keeps `MAX(acc, x)`. The answer, ₹2,29,032.75, is the largest month-on-month rise: September over August.

`SCAN` is the formula version of a running balance, and the championship case in the Timed challenge after the project uses exactly that idea to simulate stock levels day by day. Google Sheets has `MAP`, `BYROW`, `BYCOL`, `SCAN`, `REDUCE`, and `MAKEARRAY` too.

> **Watch out: clever isn't the same as clear.** A single-cell `LET`–`LAMBDA`–`SCAN` formula can replace fifty helper cells, and nobody else in your team may be able to check it. For shared workbooks, prefer visible helper columns or name each step with `LET`, and keep the one-cell versions for places where speed matters more than handover, such as a timed competition.

### GROUPBY and PIVOTBY (newer Microsoft 365 functions)

Microsoft 365 has two newer functions that build a pivot-style summary as a formula. They aren't in Google Sheets or in older perpetual versions of Excel (check Microsoft's GROUPBY help page for the current list), so use them only when every reader has them.

```excel
=GROUPBY(Sales[segment], Sales[net_revenue], SUM, , , , Sales[status]<>"Cancelled")
```

The result is a three-row summary with a total: Hospitality ₹11,44,038.75, Retail ₹14,88,773.75, Wholesale ₹17,02,658.50, total ₹43,35,471. The seventh argument is the filter; the empty arguments in between keep the defaults for headers, totals, and sorting. `PIVOTBY` adds a column field: `=PIVOTBY(Sales[segment], Sales[quarter], Sales[net_revenue], SUM, , , , , , Sales[status]<>"Cancelled")` rebuilds Figure 11.3's grid.

> **Watch out: forgetting the filter.** Without the filter argument, Retail shows ₹15,51,423.75, including cancelled order 10131's ₹37,850 and 10034's ₹24,800. A formula summary is only as correct as its rules, exactly like a pivot.

### Living with spills

- **`#SPILL!`** (Excel) means something is in the way. Click the error's warning icon → **Select Obstructing Cells**, and clear them. Google Sheets shows `#REF!` with the message that the array result wasn't expanded because it would overwrite data.
- **You can't type inside a spill range** or delete one cell of it. Edit or delete the formula in its first cell.
- **Spills and tables don't mix in Excel.** A dynamic array formula can't spill inside an Excel table; put spilled results on a report sheet.
- **`@`** in a formula (Excel) means "one value, not the array". You'll see it when older workbooks are opened in Microsoft 365. It usually reproduces the old behaviour; if you want the whole list, remove the `@` and check the result.

---

## 11.7 Power Query: record the cleanup once, refresh forever

**Power Query** is Excel's built-in tool for getting data from files, folders, databases, and the web, cleaning it with recorded steps, and loading the result into a table. It's the same engine as Power Query in Power BI (Chapter 16). You met it briefly in Chapter 10, where it imported a CSV with the right types. Here you'll use it to replace the month-end copy-paste routine completely. Figure 11.5 shows the query you'll build.

![Six Power Query steps in a row, Source, Combine, Types, Filter, Add column, Load, with row counts 12 files, 330, 330, 326, 326 rows and 43,35,471, and a dashed refresh loop back to the start](figures/fig11-5-power-query-steps.svg)

*Figure 11.5 — The Riverstone query as applied steps. Each step is an instruction, not a change to the files; Refresh replays them on whatever files are in the folder.*

> **Tool note: where Power Query runs.** The full Power Query Editor is in Excel for Windows (Microsoft 365, Excel 2016 and later). Excel for Microsoft 365 for Mac includes the Power Query Editor with fewer data sources, and Excel for the web can refresh and edit some queries. Google Sheets has no Power Query; section 11.11 gives the alternatives. Features in this area change often, so check Microsoft's current "Power Query in Excel" help page for your platform.
>
> **If you're on Google Sheets:** read Steps 1–6 for the ideas, then build the same result by hand. Import each monthly CSV into its own tab (**File → Import → Upload**, **Insert new sheet(s)**, as in Chapter 10, section 10.4), stack the twelve tabs on one `Data` tab with `=VSTACK(Jan!A2:I16, Feb!A2:I21, …)` (section 11.6), and add the net revenue column with one `ARRAYFORMULA` (section 11.10). It isn't a one-click refresh, but the rules still live in one place.

### Step 1: connect to the folder

The folder `monthly_exports/` holds twelve files, `sales_2025_01.csv` to `sales_2025_12.csv`, each with the same nine columns as Chapter 10's export (day-first dates, zero-padded codes). They have 15, 20, 18, 21, 29, 22, 29, 28, 40, 38, 35, and 35 lines: 330 in total.

1. Copy the folder somewhere stable, such as `C:\Riverstone\monthly_exports`.
2. Open `ch11_practice.xlsx` and add a new sheet (the query's result will land in this workbook, next to the Customers data you'll need in Step 5). Then **Data → Get Data → From File → From Folder**, choose the folder, and click **Open**.
3. A preview lists the twelve files. Click **Combine → Combine & Transform Data**.
4. In **Combine Files**, choose the first file as the sample, check that the delimiter is **Comma**, and click **OK**.

The **Power Query Editor** opens with all 330 rows stacked, plus a `Source.Name` column showing which file each row came from. On the left, **Queries** lists your main query and some helper queries (`Transform Sample File` and others) that Excel created to apply the same steps to every file. On the right, **Applied Steps** lists everything done so far.

### Step 2: fix the types (and undo Excel's guess)

Look at the last applied step: **Changed Type**. Power Query guessed the types, and it guessed `customer_code` is a whole number, which strips the zeros, exactly the problem from Chapter 10. It may also have read the dates using your computer's regional settings.

1. Click the ✕ next to **Changed Type** to delete that step.
2. Select `customer_code`, `status`, and `sales_rep`; **Transform → Data Type → Text**.
3. Select `order_id`, `product_id`, and `quantity`; **Data Type → Whole Number**. Select `unit_price` and `discount_pct`; **Data Type → Decimal Number**.
4. Right-click `order_date` → **Change Type → Using Locale…** → **Date**, **English (India)** → **OK**.
5. Right-click `Source.Name` → **Remove** (or keep it as a record of the source file).

> **Watch out: the automatic "Changed Type" step comes back.** Power Query adds a type-detection step after many operations, including combining files and promoting headers. Read every **Changed Type** step it creates. To stop it for new queries, **File → Options and settings → Query Options → Data Load → Type Detection → Never detect column types and headers for unstructured sources**.

### Step 3: apply the business rule

Click the arrow on the `status` header, clear **Cancelled**, and click **OK**. The step **Filtered Rows** appears, and the row count at the bottom left drops to **326**.

### Step 4: add the calculated column

**Add Column → Custom Column.** Name it `net_revenue` and enter:

```
[quantity] * [unit_price] * (1 - [discount_pct] / 100)
```

Then set its type to **Decimal Number**. Power Query's formula language is called **M**; column names go in square brackets, and the formula runs for every row, so there's nothing to fill down.

### Step 5: bring in the customer segment with a merge

A **merge** is a lookup done once for the whole table (a join, in Chapter 12's terms).

1. First load the Customers list as its own query: in the same workbook, click in the Customers data, **Data → From Table/Range**, set `customer_code` to **Text**, and **Home → Close & Load To… → Only Create Connection**. Checkpoint: **Data → Queries & Connections** should now list two queries, the sales query and Customers (plus Excel's helper queries in a folder).
2. Back in the sales query: **Home → Merge Queries**. Choose the Customers query, click `customer_code` in both tables, and choose **Join Kind: Left Outer (all from first, matching from second)**. The dialog reports how many rows matched: it should say 326 of 326.
3. A new column of nested tables appears. Click its expand icon, tick `customer_name` and `segment`, clear **Use original column name as prefix**, and click **OK**.

> **Watch out: a merge that matches fewer rows than you have.** If the merge dialog says "The selection matches 0 of the 326 rows", the key columns have different types (text `0014` against the number 14). Fix the types in both queries before merging.

### Step 6: load and check

**Home → Close & Load.** The query's result lands on a sheet as a table, and **Data → Queries & Connections** lists the query with "326 rows loaded". Check it:

```excel
=SUM(RiverstoneSales[net_revenue])     → 4335471
```

Rename the query and its table `RiverstoneSales` in the Queries pane first. The total matches every other method in this book. ✓

### Next month: refresh

This is the payoff. When January 2026's export arrives, save it into the same folder and click **Data → Refresh All**. Power Query replays every applied step on every file in the folder. Nobody pastes, extends ranges, or re-types a rule.

Try a refresh test now: move `sales_2025_12.csv` out of the folder and click **Refresh All**. The total drops to **₹38,95,647.50** (December's ₹4,39,823.50 is gone) and any pivot built on the table shows Q4 as ₹13,14,478.75 after its own refresh. Move the file back, refresh, and ₹43,35,471 returns.

> **Watch out: a new file with a different layout.** If a month's export has an extra column, a renamed header, or a summary line at the bottom, the combined query can fail or silently put values in the wrong columns. Check the row count after every refresh (section 11.12), and ask the ERP team to keep the export layout fixed.

### More Power Query moves you'll use

**Unpivot: turning wide data into long data.** The **TargetsWide** sheet has one row with a column per month, the way targets often arrive from finance. Pivot tables and joins need one row per month. Load it with **Data → From Table/Range**, select the `year` column, and **Transform → Unpivot Other Columns**. Twelve rows appear, with `Attribute` (the month) and `Value` (the target), totaling ₹42,40,000. Rename the columns `month` and `target`.

**Other everyday steps:** **Remove Duplicates**, **Split Column** (by delimiter), **Replace Values**, **Trim** and **Clean** (under **Transform → Format**), **Fill Down** for blank cells under a group heading, **Group By** (a pivot inside the query), and **Append Queries** to stack two queries with the same columns.

**Parameters.** Hard-coding `C:\Riverstone\monthly_exports` breaks when a colleague runs the file. **Home → Manage Parameters → New Parameter** creates a named value (such as `FolderPath`) that the Source step can use, so the path is changed in one place.

**The M code.** Every click you made above was recorded in Power Query's formula language, **M**. **Home → Advanced Editor** shows the whole query as M code, one line per applied step. You don't need to write M to use Power Query; the Advanced Editor simply shows what your clicks produced, and reading it is a good way to check a query someone else built. The companion file `riverstone_sales.pq` holds a tidied version of this section's query, for when you want to compare. (It skips the Customers merge from Step 5.)

**Loading options.** **Home → Close & Load To…** offers **Table** (a sheet table), **PivotTable Report**, **Only Create Connection** (for helper queries), and **Add this data to the Data Model** (section 11.8). Large data (hundreds of thousands of rows) should go to the Data Model, not to a sheet.

### Power Query in depth

> **Second pass.** Everything from here to the end of section 11.7 can wait until after the project.

The six steps above are the core. The tools below turn Power Query from "a better import" into the place where most of a monthly report's cleanup and shaping happens.

#### See the data before you change it: column profiling

In the Power Query Editor, tick **View → Column quality**, **Column distribution**, and **Column profile**. Then click the status bar text **Column profiling based on top 1000 rows** and switch it to **entire data set**, or the profile describes only a sample.

- **Column quality** shows the percentage of each column that is **Valid**, **Error**, or **Empty**. On the combined sales query, `sales_rep` is 6% empty: the 19 lines with no rep.
- **Column distribution** shows **distinct** and **unique** counts. `customer_code` has 23 distinct values and 0 unique ones (every customer ordered more than once).
- **Column profile** (for the selected column) shows statistics and a value distribution. Click a step before **Filtered Rows** in Applied Steps (your own **Changed Type** step, say), because after the filter there are no cancelled rows left: `status` then has 322 Delivered, 4 Cancelled, 3 Shipped, and 1 Pending line.

Profile every new source before building steps on it. Chapter 14 turns this into a full data-quality routine.

#### Conditional columns and columns from examples

**Add Column → Conditional Column** builds an if-then-else column without writing M. *"Classify each line by size."* New column name `size`; **If** `net_revenue` **is greater than or equal to** `30000` **Then** `Large`; **Else If** `net_revenue` **is greater than or equal to** `10000` **Then** `Medium`; **Else** `Small`. On the 326 valid lines: 158 Small, 142 Medium, 26 Large, the same bands as the `IFS` formula in section 11.3, now calculated once for every refresh.

**Add Column → Column From Examples** lets you type the result you want for a row or two, and Power Query writes the transformation. Type `Neha` next to *Neha Kulkarni* and it proposes **Text Before Delimiter**; accept it and check the formula it shows at the top before clicking **OK**.

#### Group By with several aggregations

**Home → Group By → Advanced.** *"One row per customer with revenue, lines, orders, and first and last order dates."* Group by `customer_name`, then add aggregations:

| New column | Operation | Column |
|---|---|---|
| `revenue` | Sum | `net_revenue` |
| `lines` | Count Rows | — |
| `orders` | Count Distinct Rows | (select `order_id` first, see note) |
| `first_order` | Min | `order_date` |
| `last_order` | Max | `order_date` |

Sharma Hardware's row: ₹5,02,775, 32 lines, 16 orders, first order 24 January, last 5 December.

> **Tool note: distinct counts in Group By.** **Count Distinct Rows** counts distinct *whole rows*, not distinct values of one column. To count distinct orders, the simplest route is a second Group By: first group by `customer_name` and `order_id` (Count Rows), then group that result by `customer_name` (Count Rows again). In the Advanced Editor you can instead write the aggregation as `each List.Count(List.Distinct([order_id]))`: for each group, `[order_id]` is the list of that group's order IDs, `List.Distinct` drops the repeats, and `List.Count` counts what's left.

#### Merge join kinds, including anti-joins

The **Join Kind** in **Merge Queries** decides which rows survive:

| Join kind | Keeps | Riverstone use | Result |
|---|---|---|---|
| Left Outer | All rows from the first table, matches from the second | Sales + Customers (add segment) | 326 rows |
| Right Outer | All rows from the second, matches from the first | Rarely needed; swap the tables instead | — |
| Full Outer | All rows from both | Reconciling two lists | — |
| Inner | Only rows that match in both | Sales lines with a known customer | 326 rows |
| **Left Anti** | Rows in the first with **no** match in the second | Customers with no 2025 sales | 1 row: Home Plus |
| **Right Anti** | Rows in the second with no match in the first | Sales lines with an unknown customer code | 0 rows |

Anti-joins are the quiet heroes of reconciliation. *"Which customers didn't buy this year?"* Merge **Customers** (first) with **Sales** (second) on `customer_code`, **Left Anti**: one row, Home Plus. A **Right Anti** merge that returns rows means the sales data has codes the customer master doesn't know, which should stop a report until someone explains them.

#### Fuzzy merge, briefly

Tick **Use fuzzy matching to perform the merge** in the merge dialog to match text that is similar rather than identical ("Metro Mart" and "Metro Mart Pvt Ltd"). **Fuzzy matching options** set the **Similarity threshold** (0 to 1; higher is stricter) and can ignore case and spaces. Fuzzy merges are useful and risky: always check the matches in a filtered view before trusting them. Chapter 14 uses them on Riverstone's messy customer export.

#### Append, pivot, and split into rows

- **Append Queries** stacks queries with the same columns (this year's query and last year's archive). Columns are matched **by name**; a column missing from one query is filled with nulls.
- **Transform → Pivot Column** is the reverse of unpivot: select `quarter`, choose **Values Column** `net_revenue`, **Advanced options → Aggregate Value Function: Sum**, and the segment-by-quarter grid appears inside the query.
- **Split Column → By Delimiter → Advanced options → Split into Rows** turns a cell holding `"101;105;107"` into three rows, one per product. It's the fix for lists typed into one cell.
- **Transform → Fill → Down** copies a value into the blank cells below it, for reports where a customer name appears only on its first line.

#### When a file breaks the rules: errors, extra columns, and footers

Open `pq_practice/sales_export_with_problems.csv` in Notepad. It's a five-line export with three problems real exports often have: an extra `remarks` column, a quantity typed as `55 pcs`, and a footer line `Total lines: 5`.

1. **Load it** (**Data → From Text/CSV → Transform Data**) and delete the automatic **Changed Type** step. Six rows appear: five lines and the footer.
2. **Remove the footer:** **Home → Remove Rows → Remove Bottom Rows → 1**. Five rows remain. (If footers vary, filter `order_id` to keep only values that are numbers, or use **Remove Rows → Remove Errors** after typing the column.)
3. **Set types.** Changing `quantity` to **Whole Number** turns `55 pcs` into an **Error** cell. **Home → Keep Rows → Keep Errors** shows the one bad row so you can see what went wrong; delete that step afterward.
4. **Fix instead of dropping.** Before the type step, select `quantity` and use **Transform → Extract → Text Before Delimiter** with a space as the delimiter. `55 pcs` becomes 55. Then set the type, and check the row count and the total against the source.
5. **Handle columns you don't need:** **Home → Choose Columns** and keep the nine standard columns. In M, `Table.SelectColumns(Source, {…}, MissingField.UseNull)` also survives a month in which a column is **missing**.

With those steps, the five lines total **₹46,555**, the value of the December lines they were copied from. The same pattern (remove footers, extract digits, choose columns) makes the monthly folder query survive a badly behaved export.

> **Second pass: the same fixes written in M.** You'll meet these in other people's queries. A custom step that keeps only the digits of a quantity:
>
> ```
> Table.TransformColumns(Source, {{"quantity", each Number.From(Text.Select(Text.From(_), {"0".."9"})), Int64.Type}})
> ```
>
> Read it from the inside out. `_` means "the current value" (this cell). `Text.From(_)` turns it into text; `Text.Select(…, {"0".."9"})` keeps only the characters 0 to 9 (`"55 pcs"` becomes `"55"`); `Number.From` turns `"55"` into the number 55; and `Int64.Type` sets the column to whole numbers.
>
> `try … otherwise …` catches errors in a custom column: `each try Number.From([quantity]) otherwise null` tries to turn the quantity into a number and returns null (empty) instead of an error, so a single bad value doesn't stop the refresh. Pair it with a check (a count of nulls) so bad values are noticed.

#### Custom functions: the same steps for every file

When **Combine Files** runs, Excel builds a hidden **function** from the sample file's steps and applies it to each file. You can do this yourself for full control:

1. Build a query that loads **one** monthly file and cleans it (types, footer removal, `net_revenue`).
2. **Home → Manage Parameters → New Parameter**, `FilePath`, type **Text**, current value the file's path. Edit the Source step to use `FilePath` instead of the typed path.
3. Right-click the query → **Create Function…**, name it `fnReadExport`.
4. In the folder query, **Add Column → Invoke Custom Function → fnReadExport**, passing the folder path and file name joined together; then expand the result.

The custom function is easier to read and change than Excel's generated helper queries, and it can be reused for next year's folder.

#### Staging queries and the dependency view

Split big transformations into **staging** queries (load, type, clean) and **reporting** queries that start from them: right-click a query → **Reference** creates a new query whose first step is the other query's result. Set staging queries to **Only Create Connection** so they don't fill sheets. **View → Query Dependencies** draws how queries feed each other, which is the first thing to look at in an inherited workbook.

#### Query folding and performance

When the source is a **database** (Chapter 12), Power Query tries to translate your steps into one SQL query that the database runs, so only the result travels to Excel. This is **query folding**. Right-click a step: if **View Native Query** is available, the steps up to there are folding. Filters, column choices, joins, and grouping usually fold; custom M functions and some text operations stop folding, and every step after that runs on your computer.

Performance habits:

- **Filter rows and remove columns early**, right after the Source step.
- **Don't load helper queries** to sheets.
- **Prefer database views** (Chapter 13) for heavy joins rather than merging large tables in Power Query.
- **Avoid loading hundreds of thousands of rows to a sheet**; load them to the Data Model and pivot from there.
- **Turn off background data previews** for very large sources (**Query Options → Current Workbook → Data Load**).

#### When a refresh fails

| Message or symptom | Usual cause | Fix |
|---|---|---|
| `DataSource.Error: Could not find a part of the path` | Folder moved or the file path is on someone else's computer | Use a parameter for the path; store data on a shared location |
| `Expression.Error: The column 'X' of the table wasn't found` | A header was renamed or removed in the source | Fix the source, or use `MissingField.UseNull`; avoid steps that hard-code every column |
| `DataFormat.Error: We couldn't convert to Number` | Text in a numeric column (`55 pcs`, `-`, `N/A`) | Keep Errors to find it; clean before typing |
| Refresh works but the total is wrong | A file was duplicated in the folder, or a month is half-exported | Add `Source.Name` and count lines per file; compare with the ERP |
| `Formula.Firewall: Query references other queries or steps` | Mixing data sources with different privacy levels in one step | **File → Options and settings → Query Options → Privacy**; separate the sources into staging queries |
| Refresh is very slow | No folding, many merges on large tables, sheets loaded with helper queries | Filter early; load to the Data Model; move heavy joins to the database |

> **Tool note: refresh settings.** In **Data → Queries & Connections**, right-click a query → **Properties** to set **Refresh data when opening the file** or **Refresh every *n* minutes**. A query that refreshes only when someone opens the workbook is still manual; Chapter 20 covers scheduling refreshes with Power Automate, and Chapter 16 with the Power BI service.

---

## 11.8 Power Pivot and a first taste of DAX

> **Second pass.** This whole section can wait until after the project. Chapter 16 teaches DAX again, from the start, in Power BI.

A pivot table on one wide table works well, but real businesses have several related tables: order lines, customers, products, dates. Copying every customer and product column into the sales table (as the practice Sales sheet does) repeats data and grows quickly. **Power Pivot** lets Excel hold several tables in a **data model**, connect them with **relationships**, and calculate with **DAX** (Data Analysis Expressions), the same language Power BI uses (Chapter 16).

> **Tool note: availability.** Power Pivot and the Data Model are in Excel for **Windows** (Microsoft 365 and Excel 2016 or later). They are **not** available in Excel for Mac, and Excel for the web can use existing models only in limited ways. Google Sheets has no equivalent. If you work on a Mac, read this section for the ideas; you'll practice DAX again in Chapter 16 (Power BI Desktop is also Windows-only, so Mac users typically run it in a Windows virtual machine or a cloud PC).
>
> **If you're on a Mac, Excel for the web, or Google Sheets:** read for the ideas, then get the same numbers with formulas you already know. Gross margin %: `=SUMIFS(Sales!S2:S331,Sales!H2:H331,"<>Cancelled")/SUMIFS(Sales!J2:J331,Sales!H2:H331,"<>Cancelled")` (add a segment condition to both for one segment). Year to date: the `SUMIFS` with `"<="&EOMONTH(…)` from section 11.2.

### Turn it on and build the model

1. Enable the add-in if you don't see a **Power Pivot** tab: **File → Options → Add-ins → Manage: COM Add-ins → Go** → tick **Microsoft Power Pivot for Excel**.
2. Load the tables into the model, all from `ch11_practice.xlsx`. On the Sales sheet, select the order columns only, `A1:I331` (330 lines, cancelled ones included; the model will do the joining, so leave out the pre-joined columns). **Data → From Table/Range**, then in the Power Query Editor **Home → Close & Load To… → Only Create Connection**, and tick **Add this data to the Data Model**. In the Power Pivot window (**Power Pivot → Manage**), rename the table **Sales** by double-clicking its tab. Do the same for the Customers and Products sheets, naming the tables **Customers** and **Products**. (In your own work you'd load a cleaned query such as section 11.7's `RiverstoneSales` here instead; this section keeps the cancelled lines so you can see what `CALCULATE` does with them.)
3. Create a date table: **Power Pivot → Manage**, then in the Power Pivot window **Design → Date Table → New**. Excel adds a `Calendar` table covering the dates in the model, and marks it as the date table. (If Excel's automatic table spans more years than you want, filter it later in pivots.)
4. Create relationships: in the Power Pivot window, **Home → Diagram View**, and drag `customer_code` in the sales table onto `customer_code` in Customers, `product_id` onto `product_id` in Products, and `order_date` onto `Date` in Calendar. Or use **Data → Relationships → New** in Excel.

Check the model before writing any measures: insert a pivot from it (**Insert → PivotTable → From Data Model**), put `status` from Sales in Rows and `order_id` in Values (it shows as a count). **Cancelled** should show **4** lines, and the total 330. Those four lines are why the measures below need `CALCULATE`.

Figure 11.6 shows the result.

![Star-shaped data model: Sales fact table in the center with one-to-many relationships from Customers, Products, and Calendar, and a DAX measure explained below](figures/fig11-6-data-model-star.svg)

*Figure 11.6 — Riverstone's data model: one fact table surrounded by lookup tables. Chapter 16 calls this shape a star schema.*

Each relationship is **one-to-many**: one customer, many order lines. Filters flow from the "one" side to the "many" side, so choosing *Wholesale* in Customers filters the sales rows of Wholesale customers.

### Measures versus calculated columns

DAX can calculate in two places, and the difference is the most important idea in this section.

- A **calculated column** is computed once for **each row** and stored in the table, like a spreadsheet column. Example: `line_cost = Sales[quantity] * RELATED(Products[unit_cost])`, where `RELATED` fetches the unit cost across the relationship.
- A **measure** is a formula computed **at the moment it's shown**, for whatever the pivot cell represents: all of Retail, Q3 only, or Rahul Mehta in November. Measures are where business definitions live.

Rule of thumb: if you'd filter or group **by** it (a band, a category), make a column. If you'd **add it up, average it, or divide it**, make a measure.

### Your first measures

Use the pivot from your check (remove `status` and the count). In the **PivotTable Fields** pane, right-click the Sales table → **Add Measure…**, type the name, and enter the formula. (In the Power Pivot window, you can also type measures in the calculation area as `Name := formula`, which is how the companion file `riverstone_measures.dax` lists them.)

```dax
Net Revenue :=
SUMX ( Sales, Sales[quantity] * Sales[unit_price] * ( 1 - Sales[discount_pct] / 100 ) )
```

`SUMX` goes through the table row by row, calculates the expression for each row, and adds the results: the DAX version of Chapter 10's net revenue column plus `SUM`, without the column.

```dax
Valid Net Revenue :=
CALCULATE ( [Net Revenue], Sales[status] <> "Cancelled" )
```

`CALCULATE` evaluates a measure with changed filters: here, "only rows where status isn't Cancelled". It's the most important function in DAX, and Chapter 16 spends a whole section on it. Put `Valid Net Revenue` in Values with `segment` from **Customers** in Rows: Hospitality ₹11,44,038.75, Retail ₹14,88,773.75, Wholesale ₹17,02,658.50, total **₹43,35,471**. ✓ The segment came through the relationship; the Sales table doesn't contain it. `Net Revenue` on its own shows ₹43,98,121, because it still includes the four cancelled lines.

```dax
Gross Margin :=
CALCULATE (
    SUMX ( Sales,
        Sales[quantity] * ( Sales[unit_price] * ( 1 - Sales[discount_pct] / 100 ) - RELATED ( Products[unit_cost] ) ) ),
    Sales[status] <> "Cancelled" )

Gross Margin % :=
DIVIDE ( [Gross Margin], [Valid Net Revenue] )
```

`Gross Margin` has the same shape as `Valid Net Revenue`: `CALCULATE` with the status filter around a `SUMX` over Sales. For each line, the `SUMX` expression takes the net price per unit (`Sales[unit_price]` after `Sales[discount_pct]`), subtracts the product's cost, which `RELATED ( Products[unit_cost] )` fetches across the relationship, and multiplies by `Sales[quantity]`. `DIVIDE` is a safe division that returns blank instead of an error when the denominator is zero. The results reveal something the revenue view hides:

| Segment | Valid net revenue (₹) | Gross margin (₹) | Gross margin % |
|---|---|---|---|
| Hospitality | 11,44,038.75 | 3,70,338.75 | 32.4% |
| Retail | 14,88,773.75 | 4,43,323.75 | 29.8% |
| Wholesale | 17,02,658.50 | 3,23,558.50 | 19.0% |
| **Total** | **43,35,471.00** | **11,37,221.00** | **26.2%** |

Wholesale is Riverstone's biggest segment by revenue and its least profitable: bulk discounts and low-margin Industrial Crates (13.6% gross margin as a category) pull it down. A revenue-only pivot would never show that.

### Filter context, in one paragraph

Why does the same measure give ₹17,02,658.50 in the Wholesale row and ₹43,35,471 in the total row? Because every cell of a pivot has a **filter context**: the set of filters that apply to it (this segment, this quarter, whatever the slicers say). A measure is calculated fresh inside each cell's context. `CALCULATE` changes the context on purpose. That idea is the key to all of DAX, and Chapter 16 builds on it.

### Time intelligence

With a marked date table, DAX has functions for time comparisons:

```dax
Revenue YTD :=
TOTALYTD ( [Valid Net Revenue], Calendar[Date] )
```

`TOTALYTD` takes two arguments: the measure to add up, and the date column of the marked date table. For each pivot cell it adds the measure from 1 January of that year to the last date in the cell.

Put `Calendar[Month]` in Rows (in date order), with `Valid Net Revenue` and `Revenue YTD` in Values. Year to date reaches **₹14,60,879.75** at the end of June, **₹25,81,168.75** at the end of September, and **₹43,35,471** in December. Other common functions: `SAMEPERIODLASTYEAR` for year-on-year comparisons (you'll need more than one year of data, which Chapter 14's full dataset provides) and `DATEADD` for "previous month".

---

## 11.9 What-if analysis

So far you've asked "what happened?" What-if tools ask "what would it take?" and "what if this changes?"

### Goal Seek: work backward to a target

June 2025 was Riverstone's weakest month: ₹1,86,928 against a ₹3,00,000 target. Vikram asks: *"How many extra Industrial Crates, at ₹1,400 with the usual 8% wholesale discount, would June have needed to hit target?"*

Set up a small model on a blank sheet:

| | A | B |
|---|---|---|
| 1 | June net revenue so far | 186928 |
| 2 | Extra crates | 0 |
| 3 | Price per crate | 1400 |
| 4 | Discount % | 8 |
| 5 | June net revenue with extra crates | `=B1+B2*B3*(1-B4/100)` |

**Excel: Data → Forecast → What-If Analysis → Goal Seek.** **Set cell:** `B5`. **To value:** `300000`. **By changing cell:** `B2`. Click **OK**.

Goal Seek changes `B2` until `B5` reaches the target: **87.79** crates. Crates come whole, so the answer is **88**, which gives ₹3,00,272. You can check the logic without Goal Seek: the gap is ₹1,13,072, and each crate nets ₹1,288, so 1,13,072 ÷ 1,288 = 87.79. Goal Seek earns its place when the model is too tangled to rearrange by hand.

**Google Sheets** has no built-in Goal Seek. Google publishes a free **Goal Seek** add-on (**Extensions → Add-ons → Get add-ons**, search "Goal Seek"), or you can solve simple models algebraically as above, or test values in a column and find the first one that reaches the target.

> **Watch out: Goal Seek overwrites your input.** It replaces the value in the changing cell. Note the original, or run it on a copy of the model.

For problems with several changing cells and constraints (a production mix, a delivery schedule), Excel's **Solver** add-in (**File → Options → Add-ins → Excel Add-ins → Solver Add-in**) finds the best combination. It's beyond this chapter, but know it exists.

### Data tables: many answers at once

> **Second pass.** Data tables and Scenario Manager can wait until after the project. Goal Seek, above, is the core.

*"What would 2026 net revenue be if prices rise 0%, 3%, or 5%, and volumes change by −5% to +10%?"* A simple planning model: 2026 revenue = 2025 revenue × (1 + price change) × (1 + volume change).

1. Put 2025's ₹43,35,471 in `B1`, price change in `B2` (0), volume change in `B3` (0), and in `B5`: `=B1*(1+B2)*(1+B3)`.
2. Build a grid: volume changes across row 5 starting in `C5` (−5%, 0%, 5%, 10%), price changes down column B starting in `B6` (0%, 3%, 5%). The formula cell `B5` sits at the grid's top-left corner.
3. Select `B5:F8`. **Excel: Data → What-If Analysis → Data Table.** **Row input cell:** `B3` (volume). **Column input cell:** `B2` (price). **OK**.

| Price change ↓ · Volume change → | −5% | 0% | +5% | +10% |
|---|---|---|---|---|
| 0% | 41,18,697 | 43,35,471 | 45,52,245 | 47,69,018 |
| 3% | 42,42,258 | 44,65,535 | 46,88,812 | 49,12,089 |
| 5% | 43,24,632 | 45,52,245 | 47,79,857 | 50,07,469 |

A 3% price rise with 5% more volume gives about ₹46.9 lakh. Notice that a 5% price rise with 5% fewer orders (₹43,24,632) still ends slightly *below* 2025.

Excel's data table fills the grid with a special `{=TABLE(B3,B2)}` formula. In **Google Sheets** there's no Data Table command; build the same grid with mixed references (Chapter 10): in `C6`, `=$B$1*(1+$B6)*(1+C$5)`, copied across and down. That version also works in Excel and is easier to audit.

> **Watch out: data tables recalculate constantly.** Large data tables slow Excel down. **Formulas → Calculation Options → Automatic Except for Data Tables** keeps everything else fast; press **F9** to update the tables.

### Scenario Manager, briefly

**Data → What-If Analysis → Scenario Manager** saves named sets of input values ("Cautious", "Plan", "Stretch") for the same cells and produces a summary report comparing their results. It's handy for a quick presentation, but the scenarios are hidden inside the dialog. Many analysts prefer a visible **scenario table**: one column per scenario, one row per input, and a drop-down (data validation) that picks which column feeds the model. That approach works in both apps.

---

## 11.10 Google Sheets power features

Google Sheets has several features with no direct Excel equivalent. They're the reason many analysts who live in Google Workspace can do serious work without Power Query.

### QUERY: a small query language inside Sheets

`QUERY(data, query, [headers])` runs a query written in the **Google Visualization API Query Language**: a mini language inside Sheets, made of a few English words (`select`, `where`, `group by`, `order by`, `pivot`, `label`) that describe the table you want back. It refers to columns by their **letters** within the data range.

*"Revenue by segment, excluding cancelled orders, largest first."*

```excel
=QUERY(Sales!A1:S331,
  "select N, sum(J)
   where H <> 'Cancelled'
   group by N
   order by sum(J) desc
   label sum(J) 'net_revenue'", 1)
```

The result spills into a small table: Wholesale 1702658.5, Retail 1488773.75, Hospitality 1144038.75. The final `1` says the range has one header row.

How it works:

- `select N, sum(J)`: column N (segment) and the sum of column J (net revenue).
- `where H <> 'Cancelled'`: text values go in **single** quotes inside the query string, which itself is in double quotes.
- `group by N` makes one row per segment; `order by sum(J) desc` sorts by the total, largest first; `label` renames a column. The words must come in this order.
- **`pivot`** spreads a column across the top: `select N, sum(J) where H <> 'Cancelled' group by N pivot L` rebuilds Figure 11.3's segment-by-quarter grid in one formula.
- Dates use a keyword: `where K = date '2025-11-01'`. Build the string from a cell with `"where K = date '"&TEXT(B1,"yyyy-mm-dd")&"'"`.

> **Watch out: mixed types in a column.** `QUERY` decides each column's type from the majority of its values and treats the minority as empty. A code column with some numbers and some text (`14` and `0014`) will lose one kind silently. Clean types first (Chapter 10, section 10.4).

> **Watch out: QUERY has limits.** It reads one range at a time, so it can't combine two tables, and it names columns by letter, which breaks when a column is inserted. When your `QUERY` formulas start needing data from several tables, the data belongs in a database (Chapter 12).

### ARRAYFORMULA: one formula for a whole column

In Google Sheets, `ARRAYFORMULA` makes a formula work on whole ranges, so one cell fills a column:

```excel
=ARRAYFORMULA(IF(E2:E="", "", E2:E * F2:F * (1 - G2:G/100)))
```

Put it in `J2` and every row with a quantity gets its net revenue, including rows added later. The `IF(E2:E="", "", …)` part leaves empty rows blank instead of showing zeros down the rest of the sheet. Many Sheets functions (including `FILTER`, `SORT`, `UNIQUE`, and `QUERY`) already work on arrays and don't need it. In Excel, ordinary formulas spill in the same way (section 11.6), so `ARRAYFORMULA` isn't needed.

Paste this one formula into the Chapter 10 practice file in Sheets, and you have the net revenue column without filling down. It's the closest Sheets comes to a Power Query calculated column.

### IMPORTRANGE: pull data from another spreadsheet

```excel
=IMPORTRANGE("https://docs.google.com/spreadsheets/d/…", "Sales!A1:S331")
```

The first argument is the source spreadsheet's URL (or its ID), the second is the range as text. The first time, the cell shows `#REF!` with **Allow access**; click it to connect the two files. After that, the data stays live: when the source changes, the import updates.

Combine it with `QUERY` to summarize another team's file without copying it. Inside `QUERY`, imported columns are referred to as `Col1`, `Col2` … instead of letters:

```excel
=QUERY(IMPORTRANGE("https://docs.google.com/spreadsheets/d/…", "Sales!A1:S331"),
  "select Col14, sum(Col10) where Col8 <> 'Cancelled' group by Col14", 1)
```

It's the section's first `QUERY` again, with the letters swapped for positions in `Sales!A1:S331`: `Col14` is column N (segment), `Col10` is column J (net revenue), and `Col8` is column H (status). The link's last part (…) is your source file's address.

> **Watch out: IMPORTRANGE and permissions.** Once access is allowed, **anyone who can edit your file** can import any range from the source file. Don't connect a file with salaries or customer contact details to a widely shared report. Very large imports can also be slow or fail; import only the columns you need.

For stacking several ranges (twelve monthly tabs, say), both apps have `VSTACK`: `=VSTACK(Jan!A2:I16, Feb!A2:I21, …)`. In Sheets, the older `{Jan!A2:I16; Feb!A2:I21}` array syntax does the same.

### Sheets pivot tables and slicers

You built Sheets pivot tables in section 11.5. Two Sheets-specific points: they **update automatically** without a refresh, and **slicers** (**Data → Add a slicer**) filter every chart and pivot on the same data range, which makes a simple interactive dashboard on one sheet. For a proper dashboard, Looker Studio (Chapter 16) reads Google Sheets directly.

### Connecting Sheets to a data warehouse

When data outgrows a spreadsheet, it usually moves to a **data warehouse** (Chapter 49 explains them). **Connected Sheets** lets Google Sheets work with Google BigQuery tables that are far too big for a sheet: **Data → Data connectors → Connect to BigQuery**. Pivot tables, charts, and formulas on a connected sheet run as queries in BigQuery, and you can pull an **extract** of up to 500,000 rows (subject to cell limits) into the sheet. It's available in Google Workspace editions that include it, and you need access to BigQuery through your company.

Excel's equivalent is Power Query's database connectors: **Data → Get Data → From Database** (SQL Server and others, depending on your edition), or **From Other Sources → From ODBC** for databases such as PostgreSQL and MySQL once an ODBC driver is installed. Chapter 12's databases can feed a pivot table this way, with the query running in the database and only the result coming into Excel.

---

## 11.11 What Excel does that Sheets can't (and the other way round)

| Need | Excel | Google Sheets | Sheets alternative |
|---|---|---|---|
| Combine and clean files with recorded steps | Power Query | No | `IMPORTRANGE` + `VSTACK` + `QUERY`; Apps Script (Chapter 19); or clean in SQL or Python first |
| Several related tables with measures | Power Pivot, DAX (Windows) | No | `QUERY` over pre-joined data; Looker Studio or Connected Sheets; Power BI (Chapter 16) |
| Very large data inside the file | Data Model (millions of rows) | 10 million cells | Connected Sheets with BigQuery |
| What-if tools | Goal Seek, Data Table, Scenario Manager, Solver | Goal Seek add-on | Mixed-reference grids; scenario tables |
| Formula summaries | `GROUPBY`, `PIVOTBY` (Microsoft 365) | No | `QUERY` with `group by` and `pivot` |
| Refer to a spill range | `F2#` | No | Open-ended ranges, `ARRAYFORMULA` |
| Macros | VBA, Office Scripts (Chapter 19) | Apps Script (Chapter 19) | — |

And the reverse:

| Need | Google Sheets | Excel | Excel alternative |
|---|---|---|---|
| SQL-like formulas | `QUERY` | No | Power Query; `FILTER` + `GROUPBY`; pivot tables |
| Live link to another file with a formula | `IMPORTRANGE` | External links (fragile when files move) | Power Query **From Workbook** or **From SharePoint Folder** |
| Web data in a formula | `IMPORTHTML`, `IMPORTXML`, `IMPORTDATA`, `GOOGLEFINANCE` | No direct equivalent | Power Query **From Web**; the Stocks data type |
| Real-time co-editing everywhere | Always | Cloud files with AutoSave | Store on OneDrive or SharePoint |
| Forms feeding a sheet | Google Forms | Microsoft Forms (work and school accounts) | — |

> **Simplification note.** Both products change every few months. Microsoft has added `REGEX` functions, Python in Excel, and Copilot features; Google has added tables, AI features, and new connectors. Treat this table as a guide to the *kinds* of differences and check the current help pages before you choose a tool for a team.

---

## 11.12 Spreadsheet hygiene and auditing

A workbook that other people rely on needs the same care as code. These habits prevent most errors and make the rest findable.

### A structure that survives handover

1. **A README sheet first.** What the workbook is for, who owns it, where the data comes from, how to refresh it, the business rules ("net revenue excludes cancelled orders"), and a change log with dates.
2. **Inputs, calculations, outputs.** Raw data and assumptions on their own sheets; calculations in between; the report on its own sheet. Color input cells consistently (a light yellow fill is common) so readers know what they may change.
3. **No hard-coded numbers inside formulas.** `=B5*1.18` hides a tax rate; put `18%` in a labeled input cell or a named range (`tax_rate`) and refer to it.
4. **One formula per column.** Every row of a calculated column should have the same formula. Excel flags a formula that differs from its neighbors with a green triangle (**Inconsistent Formula**); take those warnings seriously.
5. **Tables and queries, not fixed ranges.** They grow with the data (sections 10.11 and 11.7).
6. **Avoid fragile functions** where you can: `INDIRECT` and `OFFSET` build references from text or positions, break silently when sheets are renamed, and recalculate constantly.
7. **Check cells everywhere.** Every summary should have a visible check that compares its total with an independent total, showing 0 or "OK". Chapter 10's tracker did this; section 11.7's refresh test is another.

### Auditing tools

| To do this | Excel | Google Sheets |
|---|---|---|
| See which cells feed a formula | **Formulas → Trace Precedents / Trace Dependents** | Click into the formula; ranges are outlined |
| Step through a formula | **Formulas → Evaluate Formula** | — |
| Show all formulas | **Ctrl+\`** | **Ctrl+\`** |
| Find all formulas, constants, or errors | **Home → Find & Select → Go To Special** | **Ctrl+\`**, then **Find** |
| List queries and connections | **Data → Queries & Connections** | — |
| Find links to other workbooks | **Data → Edit Links** (**Workbook Links** in newer versions) | Search for `IMPORTRANGE` |
| Workbook size and contents | **Review → Workbook Statistics** | — |
| Compare two versions of a file | **Inquire → Compare Files** (Inquire add-in, enterprise editions) | **File → Version history** |
| Find hidden sheets | Right-click a sheet tab → **Unhide** | **View → Hidden sheets** |

### An audit checklist for an inherited workbook

1. **Where does the data come from, and when was it last updated?** Look for pasted data, queries, and links.
2. **Does the headline total reconcile** to an independent source (the database, finance, Chapter 10's tracker)?
3. **Are the rules the same everywhere?** Compare the formulas across months or sections, not only the results.
4. **Are any numbers typed in** where a formula should be? **Go To Special → Constants** in a summary area finds them.
5. **Do the ranges cover all the data?** Check the last row each formula uses against the last row of data.
6. **Are there duplicates or missing periods** in the data?
7. **Are there hidden sheets, rows, or columns** with numbers that feed the report?
8. **Write down what you found** and what you changed, in the README.

The story after this section runs exactly this checklist on `month_end_pack_2025_messy.xlsx`.

---

## 11.13 When to leave the spreadsheet

Spreadsheets are superb for exploring, modeling, and small-to-medium reporting. They're the wrong home for some jobs. Watch for these signals:

| Signal | What it looks like | Better home |
|---|---|---|
| Size | Hundreds of thousands of rows; slow recalculation; files over tens of MB | A database (Chapter 12), Parquet files, the Data Model |
| Many sources joined every time | Lookups across five exports each month | SQL joins (Chapter 12), Power Query at the least |
| Many people changing the data | Conflicting edits; "who changed this?" | A database with access controls; a proper app |
| It must run without a person | "Refresh this every morning at 7" | Scheduled scripts and pipelines (Chapters 18 and 20); the Power BI service (Chapter 16) |
| An error would be costly | Invoices, payroll, regulatory reports | Tested code with version control (Chapters 18 and 26) |
| Logic you can't see | Nested formulas no one can explain | Code with comments, or Power Query steps |
| Interactive dashboards for many users | Pivot-and-slicer sheets emailed around | A BI tool (Chapter 16) |

None of this means abandoning spreadsheets. The usual pattern in a mature team is: data lives in a database or warehouse, SQL or a pipeline prepares it, and Excel or Sheets connects to the prepared data for the last mile of analysis and presentation.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `VLOOKUP` without `FALSE` | Plausible but wrong names or prices | Use `XLOOKUP` (exact by default) or `VLOOKUP(…, FALSE)` |
| `VLOOKUP` column number after inserting a column | A lookup suddenly returns a different field | `XLOOKUP` or `INDEX`/`MATCH`, which point at the return column |
| Approximate match on an unsorted band table | Wrong band for some values | Sort thresholds ascending; test values slightly below and above each threshold |
| Counting `order_id` in a pivot | "105 Wholesale orders" when there were 55 | Distinct Count (Data Model) or `COUNTUNIQUE` in Sheets |
| Forgetting to refresh an Excel pivot | Pivot total doesn't match the data | **Refresh All**; refresh on open; check cells |
| Pivot built on a fixed range | New rows missing from the pivot | Build on a table; **Change Data Source** |
| Typing inside a spill range | `#SPILL!` (Excel) or `#REF!` (Sheets) | Clear the obstruction; keep spill areas empty |
| `FILTER` without an "if empty" value | `#CALC!` when nothing matches | Add the third argument: `"no rows"` |
| Accepting Power Query's automatic **Changed Type** step | Codes lose their zeros; dates misread | Delete it; set types yourself, dates **Using Locale** |
| Merging on columns of different types | "Matches 0 of 326 rows" | Same type on both sides before merging |
| A new export with a changed layout | Refresh fails or columns shift | Check row counts and totals after each refresh; agree a fixed export layout |
| Calculated columns for things that should be measures | Percentages that add up instead of recalculating | Ratios and totals as measures; columns only for per-row attributes |
| Summing a percentage in a pivot | Total row shows 300% | A measure such as `DIVIDE([Gross Margin], [Valid Net Revenue])` |
| Goal Seek overwriting an input | The model's original assumption is lost | Note the value or work on a copy |
| `QUERY` on a column with mixed types | Some values vanish from results | Clean types before querying |
| Sharing a file that uses `IMPORTRANGE` widely | Editors can pull data from the source file | Limit who can edit; import only needed columns |
| Different rules in different months | Some months include cancelled orders | One rule, applied once (query, measure, or single formula) |
| Numbers typed into a summary | A total that doesn't change when data changes | **Go To Special → Constants**; replace with formulas |

---

## In the real world: the month-end pack that was almost right

In the first week of January 2026, Anita Rao, Riverstone's Sales Head, was preparing the sales section of the quarterly board review. Vikram Singh sent her the Summary sheet from `month_end_pack_2025_messy.xlsx`: 2025 net revenue **₹42,70,875**, **100.7%** of target. Two days later, Meera Iyer's Chapter 10 tracker, built from the same ERP data, said **₹43,35,471**, **102.3%**.

The gap was ₹64,596. Anita asked a simple question: *"Which one goes to the board?"*

Meera ran the audit checklist from section 11.12.

**1. Where does the data come from?** Twelve month sheets pasted from the ERP's monthly exports, and a Summary sheet with one formula per month. No queries, no links.

**2. Does the headline reconcile?** No: ₹64,596 short of the tracker. So she compared month by month:

| Month | Summary sheet | Tracker | Difference |
|---|---|---|---|
| Apr | 2,35,081.50 | 2,10,281.50 | +24,800.00 |
| Oct | 5,45,047.75 | 6,81,070.75 | −1,36,023.00 |
| Nov | 6,33,480.00 | 6,33,408.00 | +72.00 |
| Dec | 4,86,378.50 | 4,39,823.50 | +46,555.00 |
| **Year** | **42,70,875.00** | **43,35,471.00** | **−64,596.00** |

The other eight months matched exactly. Four months, four different problems.

**3. Are the rules the same everywhere?** She pressed **Ctrl+\`** on the Summary sheet and read the formulas. Most months used `SUMIFS(…,"<>Cancelled")`. **March and April used `SUM`**, which includes cancelled orders. April had one cancelled order, 10034, worth ₹24,800: that was April's difference. March had no cancelled orders, so its number was right *by luck*, with the wrong formula. The next time a March order was cancelled, the report would be wrong again. She noted it as a defect even though it cost nothing today.

**4. Are any numbers typed in?** **Home → Find & Select → Go To Special → Constants** on the Summary's revenue column selected one cell: **November**, a typed **6,33,480**, with a note "typed from the flash email". The real figure was ₹6,33,408. Two digits had been swapped. A ₹72 difference is harmless on its own, but it proved that the report wasn't connected to its data.

**5. Do the ranges cover the data?** October's formula was `SUMIFS(Oct!J2:J30, Oct!H2:H30, "<>Cancelled")`. The October sheet had **38 lines**, in rows 2 to 39. Someone had built the formula when October's paste was shorter, and the last **9 lines**, worth **₹1,36,023**, were never counted. October showed 104.8% of target when it had really reached 131.0%, Riverstone's best month.

**6. Duplicates?** December's sheet had 40 lines; the ERP export had 35. `COUNTIFS` on order ID and product showed the **last five lines pasted twice**, adding ₹46,555. December showed 128.0% of target instead of 115.7%.

Four errors: a wrong rule in two months (one of them hidden), a typed number, a short range, and a double paste. They partly cancelled each other out, which is why the Summary looked believable.

**7. Fix the process, not the cells.** Correcting four cells would have made 2025 right and left 2026 exposed to the same four errors. Instead, Meera rebuilt the pack as sections 11.5 and 11.7 describe:

- A **Power Query** on the monthly export folder, with types set by hand and the cancelled filter applied once.
- A **pivot table** on the query's table (month in Rows, revenue and target in Values), with a slicer for segment.
- A **check cell**: pivot grand total minus `SUM` of the query's net revenue column, which must be 0, and a row count that must equal the sum of the files' lines.
- A **README** sheet stating the rule, the source folder, and "Data → Refresh All; don't paste".

She tested the refresh by removing December's file (total ₹38,95,647.50) and putting it back (₹43,35,471).

**8. Answer the question.** Her note to Anita:

> *Use ₹43,35,471 (102.3% of target). The ₹42,70,875 version had four errors: October was missing ₹1,36,023 of orders, December had ₹46,555 counted twice, April included a ₹24,800 cancelled order, and November was typed in ₹72 high. The corrected October (131% of target) is our best month, not an average one. The pack is now built from the export folder and refreshes in one click, with checks that flag any difference.*

The board saw the right number. In February, Vikram refreshed the pack himself.

What made the difference:

- Meera **reconciled month by month**, which turned "₹64,596 is missing" into four specific rows.
- She **read the formulas, not only the results**, and caught a bug that happened to cost nothing this year.
- She **looked for typed numbers and short ranges**, the two errors copy-paste workbooks produce most often.
- She **replaced the process** that produced the errors, and **added checks** so the next error announces itself.

---

## Project: rebuild a messy monthly workbook so next month is one refresh

**Goal:** replace a copy-paste monthly workbook with one that loads its data, applies its rules once, checks itself, and updates with **Refresh All**.

### Tools you'll need

- **Microsoft Excel for Windows**, Microsoft 365: everything in this chapter. Power Pivot and the Data Model require Windows. `XLOOKUP`, dynamic arrays, and `LET` need Microsoft 365, Excel 2021, or later; `GROUPBY` and `PIVOTBY` need a current Microsoft 365 version.
- **Excel for Mac** (Microsoft 365): lookups, pivot tables, dynamic arrays, what-if tools, and Power Query with fewer sources. No Power Pivot.
- **Google Sheets**: lookups, pivot tables, slicers, dynamic arrays, `QUERY`, `ARRAYFORMULA`, `IMPORTRANGE`; the Google **Goal Seek** add-on; **Connected Sheets** in Workspace editions that include BigQuery.
- **Free alternative:** LibreOffice Calc has pivot tables (called DataPilot or Pivot Tables), `INDEX`/`MATCH`, Goal Seek, and Multiple Operations (a data table), but no Power Query or Power Pivot.
- **Companion files** (`companion/ch11/`, Appendix E):
  - `ch11_practice.xlsx`: Sales (330 lines, 19 columns), Customers, Products, Targets, TargetsWide, and RebateBands.
  - `monthly_exports/`: `sales_2025_01.csv` to `sales_2025_12.csv`.
  - `month_end_pack_2025_messy.xlsx`: the workbook from the story, with the four planted errors.
  - `riverstone_sales.pq`: the Power Query M code from section 11.7.
  - `riverstone_measures.dax`: the DAX measures from section 11.8.
  - `pq_practice/sales_export_with_problems.csv`: a broken export for section 11.7.
  - `challenge/riverstone_stockroom_case.xlsx` and `riverstone_stockroom_solution.xlsx`: the guided championship case from the Timed challenge and a helper-column solution.
  - `challenge/riverstone_rewards_case.xlsx` and `riverstone_rewards_solution.xlsx`: the timed practice case and its classic-formula solution.

**Option A: your own workbook.** Pick a report you (or your team) rebuild every month. Make a copy, remove confidential data or replace names with codes, and follow the steps.

**Option B: Riverstone's workbook.** Use `month_end_pack_2025_messy.xlsx` and `monthly_exports/`.

**Steps**

1. **Audit first.** Run the section 11.12 checklist on the old workbook. Write down every problem you find, with its effect in rupees. (Riverstone: four problems; the story lists them.)
2. **Load the data with a query.** Excel: **Get Data → From Folder**, combine the twelve files, delete the automatic type step, set types (dates **Using Locale → English (India)**, codes as Text), filter out cancelled orders, add `net_revenue`, and load to a table named `RiverstoneSales`. *Google Sheets version:* import each CSV into a tab, stack them with `VSTACK` on a `Data` tab, and add `net_revenue` with one `ARRAYFORMULA`.
3. **Add the lookups once.** Merge Customers (segment) and Products (category, unit cost) in Power Query, or use `XLOOKUP` in Sheets.
4. **Build the summary as a pivot table** on the query's table: `month_start` in Rows, `net_revenue` in Values, `segment` as a slicer. Add targets with a lookup beside the pivot, or bring the unpivoted **TargetsWide** query into the model. *Sheets:* a pivot table, or one `QUERY` with `group by K`.
5. **Add measures** (Excel for Windows): `Valid Net Revenue`, `Gross Margin %`, and `Revenue YTD`, with the Calendar table and relationships from section 11.8.
6. **Add checks.** Grand total minus `SUM` of the table (must be 0). Rows loaded against the total lines in the files (330, then 326 after the filter). A check that shows "OK" or "CHECK" in large text at the top of the report sheet.
7. **Write the README.** Purpose, owner, source folder, the rules, how to refresh, and the date of the last change.
8. **Test the refresh.** Remove the December file, refresh, and confirm the total becomes ₹38,95,647.50; put it back, refresh, and confirm ₹43,35,471. Then add a fake thirteenth file with a wrong header and see what your checks say.
9. **Compare old and new.** A short table: old total, new total, and each difference explained.

Your rebuilt report should show 2025 net revenue of **₹43,35,471**, **102.3%** of the ₹42,40,000 target, gross margin **₹11,37,221** (**26.2%**), and Wholesale as the largest segment by revenue (39.3%) but the lowest by margin (19.0%).

**Stretch goals**

- Add a `Source.Name` column to the query and a pivot that counts lines per file, so a missing or half-exported month is visible at a glance.
- Replace the hard-coded folder path with a parameter stored in a cell on the README sheet.
- Build the Sheets version end to end and make its totals match the Excel version.
- Add a rebate calculation with an approximate-match lookup and a note on customers within ₹5,000 of the next band.

---

## Timed challenge: competition-style Excel (optional)

> **Optional challenge.** Do this after the project, or on your second pass. It's the hardest practice in the chapter, and nothing later in the book depends on it.

The rest of this chapter has been about building workbooks that last. Competitive Excel tests the other half of mastery: turning an unfamiliar problem into a working model **fast**, under a clock, with no one to ask. It's the most demanding practice you can do with a spreadsheet, and the habits it builds (read the whole problem first, parse data into clean columns, keep inputs in cells, check small cases by hand) are exactly the habits of a strong analyst.

### What competitive Excel looks like

The best-known event is the **Microsoft Excel World Championship (MEWC)**, organized by the Financial Modeling World Cup with Microsoft as a sponsor. At the time of writing, its format works like this:

- Each round is one **case**: a fictional scenario (a game, a puzzle, a simulation) described in a workbook, with a time limit of about **30 minutes**. Finals run longer, and players with the lowest scores are eliminated at intervals.
- Questions are grouped into **levels** that get harder and are worth more points, plus **bonus** questions. A full case is worth around 1,000 points.
- Answers are **numbers or short text** typed into a platform and graded automatically, so any method that gets the right answer is allowed: formulas, helper columns, pivot tables, Power Query, VBA.
- Cases don't need finance or domain knowledge. They test functions, data handling, and logical thinking, and they're written so older Excel versions can solve them, although newer functions are often faster.

The related **Financial Modeling World Cup** runs longer finance-flavored cases, and there's a collegiate championship for students. Rules change between seasons, so read the current rules on the organizer's site before you enter.

> **Tool note.** You don't need to compete to benefit. Past cases and walkthrough videos are published by the organizers and by top players, and working through them, with a timer, is some of the best Excel practice available. Try them after this section.

### How strong players attack a case

1. **Read every level before touching a formula (3 minutes).** Later levels usually reuse the model from earlier ones with a twist. If Level 5 needs a search over many settings, build Level 3's model with its settings in **input cells**, not typed into formulas.
2. **Parse once, into clean columns.** Case data often arrives as codes or text. Turn it into typed columns (dates, numbers, text) on a helper sheet, then never touch the raw text again.
3. **Build one row per unit of time or event.** Simulations become a table with one row per day, turn, or move, where each row's formulas read the row above. That's the running-balance pattern from section 11.2, stretched into a model.
4. **Answer the early levels immediately.** Points are points. Type Level 1's answers as soon as you have them.
5. **Check tiny cases by hand.** Before trusting a 365-row model, trace the first few rows (or one week) on paper.
6. **Search with a data table.** "Which combination is cheapest?" is a two-input data table (section 11.9) over the model's input cells, followed by `MIN` and a two-way lookup.
7. **Keep a scratch area.** Label intermediate answers so you can find them again at minute 28.

### The case: The Riverstone Stockroom

Open `companion/ch11/challenge/riverstone_stockroom_case.xlsx`. **Give yourself 30 minutes** and try it before reading the walkthrough. Its **Case** sheet gives the brief; the **Log** sheet holds Riverstone's 330 order lines for 2025, each squeezed into one text code; **Parameters** holds the settings; **Answers** has cells for your answers.

> *Riverstone's warehouse wants to know whether a simple weekly reorder rule would have kept Storage Box 10L (product 101) in stock in 2025.*
>
> Each log line looks like `02.01.2025|SO10001|C0002|P108x10@290-0%|DEL`: date, order, customer, product × quantity @ price − discount %, status (`DEL` delivered, `SHP` shipped, `PND` pending, `CAN` cancelled).
>
> **Rules** (product 101 only; cancelled lines never ship):
> 1. The model runs day by day from 1 January to 31 December 2025. Demand on a day is the units of product 101 on non-cancelled lines dated that day.
> 2. Opening stock on 1 January is 300 units. Closing stock = opening stock + units received that day − demand. Stock may go negative (a backorder).
> 3. Every **Monday**, if the previous day's closing stock is less than or equal to the **reorder point (ROP)**, a purchase order (PO) for **Q** units is placed.
> 4. A PO placed on day *d* arrives at the start of day *d + L* (L = lead time in days).
> 5. Costs: holding ₹1 per unit per day of positive closing stock; shortage ₹20 per unit per day of negative closing stock; ₹2,000 per PO.
>
> **Level 1 (100 points):** (a) total units on non-cancelled lines, all products; (b) the product ID with the most units; (c) for product 101, the customer code that bought the most units.
> **Level 2 (150):** with no reordering, the first date closing stock goes below zero, and the closing stock on 31 December.
> **Level 3 (200):** with ROP 100, Q 250, L 7: how many POs, the lowest closing stock, and its first date.
> **Level 4 (250):** same settings: how many days is closing stock negative? Keeping Q = 250, the smallest ROP (a multiple of 50) with no negative day.
> **Level 5 (300):** L = 7; ROP can be 0, 50, … 400 and Q can be 50, 100, … 800. The lowest-cost combination and its cost.
> **Bonus (50):** the same search with L = 14; the lowest cost.

Stop here and try it. The walkthrough follows.

---

#### Minutes 0–3: read, and plan the model

Levels 2 to 5 all need the same thing: a table with one row per day, and ROP, Q, and L in input cells. Level 1 needs the log parsed. Figure 11.7 shows the plan.

![Five linked stages from the Log sheet to a daily model: demand from SUMIFS by date, a Monday purchase order flag, receipts L days later, and a running closing balance, with four sample rows from February](figures/fig11-7-stockroom-model.svg)

*Figure 11.7 — The Stockroom model: parse the log once, then one row per day where each column reads the columns and rows before it.*

#### Minutes 3–8: parse the log (and answer Level 1)

On the Log sheet, add typed columns next to the code in column A. The codes have fixed positions for the date, order, customer, and product, and variable lengths after that, so combine `MID` with `FIND`:

```excel
B2  order_date     =DATE(MID(A2,7,4), MID(A2,4,2), LEFT(A2,2))
C2  order_id       =VALUE(MID(A2,14,5))
D2  customer_code  =MID(A2,21,4)
E2  product_id     =VALUE(MID(A2,27,3))
F2  quantity       =VALUE(MID(A2,31,FIND("@",A2)-31))
I2  status         =RIGHT(A2,3)
```

How it works: in `02.01.2025|SO10001|C0002|P108x10@290-0%|DEL`, the year starts at character 7, the order number at 14, the customer code at 21, and the product at 27. The quantity starts at 31 and ends immediately before `@`, so its length is `FIND("@",A2)-31`. Fill all six down to row 331.

In Microsoft 365, one formula can split the whole code into pieces:

```excel
=TEXTSPLIT(A2, {"|","x","@","-","%"})
```

It returns `02.01.2025`, `SO10001`, `C0002`, `P108`, `10`, `290`, `0`, an empty piece (where `%` and `|` sit side by side), and `DEL`. You'd then convert the pieces with `VALUE` and `SUBSTITUTE`. Use whichever you can write fastest and check.

Level 1 is now three quick formulas:

```excel
=SUMIFS(F2:F331, I2:I331, "<>CAN")                                → 9475
=SUMIFS(F2:F331, E2:E331, 101, I2:I331, "<>CAN")                  → 2085
=SUMIFS(F2:F331, E2:E331, 101, D2:D331, "0012", I2:I331, "<>CAN") → 250
```

(a) **9,475** units. (b) A small `UNIQUE` list of product IDs with a `SUMIFS` beside it (or a pivot) shows product **101** leads with 2,085 units, ahead of the Stackable Bin's 1,920. (c) The same pattern by customer code for product 101 gives **0012** (Fresh Bowl Kitchens) with **250** units, ahead of two customers tied on 235.

> **Watch out: the cancelled lines are in the log.** Without `"<>CAN"`, total units come to 9,680. Competition cases hide rules like this in one line of the brief, and business data hides them in one column.

#### Minutes 8–15: build the daily model (and answer Level 2)

Put the settings on a Parameters sheet: opening stock in `B1` (300), product in `B2` (101), ROP in `B3`, Q in `B4`, L in `B5`, and the three costs in `B6:B8`. Then, on a Model sheet with headers in row 1:

```excel
A2  date       =DATE(2025,1,1)
A3             =A2+1                        (fill down to row 366)
B2  weekday    =WEEKDAY(A2,2)               (Monday = 1)
C2  demand     =SUMIFS(Log!$F$2:$F$331,
                   Log!$B$2:$B$331, A2,
                   Log!$E$2:$E$331, Parameters!$B$2,
                   Log!$I$2:$I$331, "<>CAN")
E2  po_placed  0
E3             =IF(AND(B3=1, F2<=Parameters!$B$3), 1, 0)
D2  receipts   =IF(ROW()-Parameters!$B$5>=2,
                   INDEX($E$1:$E$366, ROW()-Parameters!$B$5)
                   * Parameters!$B$4, 0)
F2  closing    =Parameters!$B$1+D2-C2
F3             =F2+D3-C3
```

How it works:

- `demand` is a `SUMIFS` by date (section 11.2), one per day.
- `po_placed` on row 3 reads **yesterday's** closing (`F2`), exactly as rule 3 says. It's 1 only on Mondays when that stock is at or below the ROP.
- `receipts` looks **L rows up** the `po_placed` column: if a PO was placed L days ago, Q units arrive today. `ROW()` (section 11.3) is the current row number, so `ROW()-L` is the row L days earlier, and `INDEX($E$1:$E$366, ROW()-L)` reads it. Trace one cell: in `D10` (9 January) with L = 7, `ROW()` − 7 = 3, so `INDEX($E$1:$E$366, 3)` reads `E3`, the `po_placed` cell for 2 January, 7 days earlier. The `IF` stops the lookup from reaching above the first data row.
- `closing` is the running balance.

For Level 2, set Q to 0 and leave ROP as it is. POs may still be "placed", but nothing arrives, which is the same as no reordering. (Don't set ROP to 0 instead: stock falls far below zero, so a PO would still be triggered.) Then read the answers:

```excel
=INDEX(A2:A366, MATCH(TRUE, INDEX(F2:F366<0,0), 0))    → 2025-02-28
=F366                                                  → -1785
```

The first formula finds the first `TRUE` in the test "closing is below zero"; the inner `INDEX(…,0)` makes it work without **Ctrl+Shift+Enter** in older Excel. Stock first goes negative on **28 February 2025** (−10), and without reordering the year ends at **−1,785**, which is 300 minus the year's 2,085 units of demand. That last check (opening stock minus total demand) proves the model's demand column is complete.

> **Try it.** Trace the first week by hand before trusting the model: 300 units on 1 January, and the first demand for product 101 arrives on 12 January (25 units, order 10003). If your closing stock changes before 12 January, a formula is reading the wrong product or date.

#### Minutes 15–20: Levels 3 and 4

Set ROP = 100, Q = 250, L = 7. Then:

```excel
POs placed       =SUM(Model!E2:E366)                → 8
lowest closing   =MIN(Model!F2:F366)                → -45
date of lowest   =INDEX(Model!A2:A366,
                     MATCH(MIN(Model!F2:F366), Model!F2:F366, 0))
                                                    → 2025-10-03
negative days    =COUNTIF(Model!F2:F366, "<0")      → 7
```

**Level 3:** **8** POs; the lowest closing stock is **−45**, first reached on **3 October 2025**. **Level 4:** stock is negative on **7** days. For the smallest safe ROP, change ROP to 150, 200, … and watch the negative-day count: at **150** it drops to 0 (lowest closing 55). A one-input data table over ROP = 0, 50, … 400 shows the same answer in one step.

Figure 11.8 shows why ROP 100 isn't safe: stock sits above the reorder point on Sunday night, the following week's orders drain it, and the next PO is still a week away from arriving.

![Line chart of Storage Box 10L closing stock through 2025 for two reorder policies, one peaking above 500 units with brief dips below zero, the other staying lower with more frequent small backorders](figures/fig11-8-stockroom-policies.svg)

*Figure 11.8 — Closing stock under the Level 3 policy (ROP 100, Q 250) and the Level 5 winner (ROP 50, Q 150). The cheapest policy runs short more often, because a day of backorder is cheaper than a week of carrying 250 extra boxes.*

#### Minutes 20–28: Level 5 with a data table

Add three cost cells beside the model and a total:

```excel
holding    =SUMIF(Model!F2:F366, ">0") * Parameters!B6
shortage   =-SUMIF(Model!F2:F366, "<0") * Parameters!B7
ordering   =SUM(Model!E2:E366) * Parameters!B8
total      =holding + shortage + ordering
```

At ROP 100, Q 250 the total is **₹1,18,210** (holding ₹98,310, shortage ₹3,900, orders ₹16,000).

Now the search. Build a grid with the total cost cell in its top-left corner, ROP values 0 to 400 down the first column, and Q values 50 to 800 across the first row: 9 rows × 16 columns = 144 combinations. Put the grid on the Parameters sheet, select it, and use **Data → What-If Analysis → Data Table**, with **Row input cell** = the Q cell (`B4`) and **Column input cell** = the ROP cell (`B3`). Excel reruns the whole 365-day model for every cell of the grid.

> **Watch out: data table inputs must be on the same sheet.** Excel's Data Table dialog only accepts input cells on the sheet that holds the table, which is why the grid goes on the Parameters sheet. Google Sheets has no data table: loop the settings with a small Apps Script (Chapter 19) or copy the model once per setting.

Name the grid's parts so the formulas can refer to them (Chapter 10's named ranges): select the 9 ROP values down the first column, type `rop_list` in the **Name Box** and press Enter; do the same for the 16 Q values across the first row (`q_list`) and the 144 result cells (`grid`).

Then find the minimum and where it is. The quick way needs no new formula: `=MIN(grid)` gives the lowest cost, and a conditional-formatting rule on the grid, **Home → Conditional Formatting → New Rule → Use a formula**, with the rule `=D11=MIN(grid)`, where `D11` stands for the grid's top-left result cell (type yours, without $ signs, so the rule moves across the grid), colours the cheapest cell. Read its ROP from the row label and its Q from the column label.

```excel
lowest cost   =MIN(grid)     → 84840
```

The formula way returns the settings directly:

```excel
ROP   =INDEX(rop_list, SUMPRODUCT((grid=MIN(grid))*ROW(grid))-MIN(ROW(grid))+1)
Q     =INDEX(q_list, SUMPRODUCT((grid=MIN(grid))*COLUMN(grid))-MIN(COLUMN(grid))+1)
```

Take the ROP formula one piece at a time:

- `ROW(grid)` gives each cell of the grid its sheet row number.
- `(grid=MIN(grid))` is TRUE only in the cheapest cell, so `(grid=MIN(grid))*ROW(grid)` is 0 everywhere except there, where it's that cell's row number.
- `SUMPRODUCT` adds them up, which picks out that one row number.
- `-MIN(ROW(grid))+1` turns a sheet row into a position in the list: the grid's first row becomes 1, the next 2, and so on. `INDEX(rop_list, position)` returns the ROP.

The Q formula does the same with `COLUMN`. If two combinations tied, the row numbers would add up to nonsense; use the conditional-formatting way then.

In Microsoft 365, one formula lists every winning combination, ties included: `=LET(c, grid, m, MIN(c), TOCOL(IF(c=m, rop_list&" / "&q_list, 1/0), 2))`. The `IF` gives the text "ROP / Q" in the cheapest cells and `1/0`, an error made on purpose, everywhere else; `TOCOL`'s second argument, `2`, skips errors, so only the winners are left.

**Level 5:** **ROP 50, Q 150**, total cost **₹84,840**, with 13 POs and 21 negative days. The next-best combinations are ROP 100/Q 150 (₹95,300) and ROP 100/Q 100 (₹96,165).

**Bonus:** set L = 14 and let the data table recalculate. The lowest cost rises to **₹1,12,125**, at ROP 50, Q 200. A longer lead time costs Riverstone about ₹27,000 a year for this one product.

#### Minutes 28–30: sanity checks before submitting

- Opening stock + all receipts − all demand = the 31 December closing stock (with ROP 100/Q 250: 300 + 8 × 250 − 2,085 = **215** ✓).
- The number of POs × Q equals total receipts.
- The best cost is lower than the Level 3 policy's cost, and the winning settings are inside the search range, not on its edge (if the best Q had been 800, the search range would be too narrow).

### What the case teaches beyond the competition

The winning policy is cheapest *under the costs in the brief*. A shortage cost of ₹20 a day per box ignores lost customers and a sales head's phone calls. A real recommendation would test several shortage costs, show the trade-off between cost and backorder days (Figure 11.8 does exactly that), and let the business choose. Competitions reward the number; analysis work rewards the number plus its assumptions (Chapters 22 and 24).

The model itself is also a template: daily inventory, cash balances, subscription counts, and loyalty points are all "yesterday's value + today's in − today's out" with a decision rule. You'll meet the same pattern in SQL (Chapter 13's running totals) and Python (Chapter 18).

### Your turn: a timed practice case, Riverstone Rewards (45 minutes)

Open `challenge/riverstone_rewards_case.xlsx`. It has a **Rules** sheet, a **Questions** sheet, and a **Lines** sheet with the 330 order lines of 2025 (customer names, not codes, and cancelled lines included). Set a timer for 45 minutes. No walkthrough this time: plan the model yourself. The answers are in the Answers section, after exercise 42.

**Rules**

1. Cancelled orders earn nothing and don't count for any rule.
2. **Order value** = the sum of `net_revenue` over the order's lines.
3. **Base points** = order value ÷ 100, rounded down to a whole number.
4. **Tier** at the time of an order depends on the customer's total order value from their **earlier** orders in 2025 (orders with a smaller `order_id`): below ₹1,00,000 is **Standard** (×1); ₹1,00,000 or more is **Silver** (×1.25); ₹2,50,000 or more is **Gold** (×1.5). **Tier points** = base points × multiplier, rounded down.
5. **Streak bonus:** +200 points on an order if the same customer placed at least one order in the previous calendar month.
6. **Basket bonus:** +100 points on an order with 3 or more lines.
7. **Order points** = tier points + streak bonus + basket bonus.
8. **Expiry** on 31 December 2025: points from orders dated before 1 July 2025 expire, unless the customer ordered on or after 1 October 2025.
9. **Balance** = all order points − expired points.

**Questions**

- **L1:** How many orders earn points, and how many of them are worth ₹25,000 or more?
- **L2:** Total base points? Which customer has the most base points?
- **L3:** How many orders were placed at Gold tier, and how many at Silver?
- **L4:** Total tier points (after multipliers, before bonuses)?
- **L5:** How many orders earn the streak bonus? Total of tier points plus streak bonuses?
- **L6:** Total order points across all orders?
- **L7:** How many customers lose points to expiry, and how many points expire?
- **L8:** The highest balance (customer and points), and how many customers finish with 4,000 points or more?
- **B1:** Which customer's running points (before expiry) first reach 5,000, and on which `order_id`?
- **B2:** Which month earned the most order points, and how many?
- **B3:** How many customers ordered in every month of 2025?
- **B4:** Metro Mart's rank by balance (1 = highest)?

> **Hints, if you're stuck after 10 minutes.** Build an **Orders** sheet with one row per valid order (`UNIQUE(FILTER(...))`, a pivot pasted as values, or Power Query **Group By**). "Earlier orders" is an **expanding range** (`SUMIFS($D$2:D2, $C$2:C2, C2) - D2`). "Previous month" is `COUNTIFS` with `EDATE(month, -1)`. `challenge/riverstone_rewards_solution.xlsx` is a complete solution that uses only classic functions, so it works in every Excel version and in Google Sheets.

---

## Recap

- **Keep data long**, separate data from calculations and outputs, and **state each rule once**. Copy-paste workbooks fail because they repeat rules and ranges by hand.
- The **conditional family** (`SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, `MAXIFS`, `MINIFS`) answers most business questions; criteria are text, joined to cells with `&`. **`SUMPRODUCT`** handles what they can't: OR across columns, calculated conditions, weighted averages, and distinct counts.
- The **everyday toolkit** (`IFS`, `SWITCH`, `TEXTBEFORE`, `EDATE`, `WORKDAY.INTL`, `ISOWEEKNUM`, `RANK.EQ`, rounding) turns raw columns into the fields reports need.
- **`XLOOKUP`** covers exact matches, bands (`match_mode` −1), last matches (`search_mode` −1), several columns, and nested two-way lookups. **`INDEX`/`MATCH`** does the same in every version. **`VLOOKUP`** counts columns and defaults to approximate: recognize it, then replace it.
- **Pivot tables** summarize by dragging fields into four areas: Filters leave rows out first, Rows and Columns make one row or column per value, and Values holds the aggregate in every cell. Use distinct counts for orders, **Show Values As** for shares and differences, slicers for filtering, and **refresh** Excel pivots.
- **Dynamic arrays** (`FILTER`, `UNIQUE`, `SORT`, `SEQUENCE`, `LET`) return whole tables from one formula; results **spill**, and a blocked spill shows `#SPILL!`.
- **Power Query** records cleanup as applied steps: combine a folder, set types yourself (delete the automatic guess), filter, add columns, merge, unpivot, and **refresh**.
- **Power Pivot** holds related tables in a **data model**. **Measures** calculate in each cell's **filter context**; `CALCULATE` changes that context. Riverstone's gross margin is 26.2% overall but only 19.0% in Wholesale.
- **Goal Seek** works backward to a target; **data tables** show many what-if answers at once; mixed-reference grids do the same in Sheets.
- Google Sheets' **`QUERY`**, **`ARRAYFORMULA`**, **`IMPORTRANGE`**, and **Connected Sheets** cover much of what Power Query and Power Pivot do in Excel.
- **Competitive Excel** (the optional Timed challenge) rewards the same habits as good analysis, under a clock: read everything first, parse once, keep settings in input cells, build one row per step, check small cases, and search with data tables.
- **Audit** by reconciling, reading formulas, finding constants, checking ranges, and looking for duplicates. **Leave the spreadsheet** when size, sources, users, scheduling, or risk demand it.

---

## Key terms

double unary (`--`) · weighted average · `ROW` / `ROWS` · lookup array · return array · match mode · search mode · exact match · approximate match · band (tier) table · `INDEX` · `MATCH` · two-way lookup · `VLOOKUP` · `HLOOKUP` · long data · wide data · pivot table · Rows area · Columns area · Values area · Filters area · distinct count · Show Values As · date grouping · value filter · slicer · timeline · `GETPIVOTDATA` · pivot chart · refresh · dynamic array · spill range · `#SPILL!` · spill reference (`#`) · `FILTER` · `UNIQUE` · `SORT` · `SORTBY` · `SEQUENCE` · `LET` · `LAMBDA` · parameter · accumulator · `GROUPBY` · `PIVOTBY` · Power Query · query · applied steps · combine files · data type detection · locale · merge queries · join kind · append queries · unpivot · parameter · M language · load to · Power Pivot · data model · relationship · one-to-many · date table · DAX · calculated column · measure · `SUMX` · `CALCULATE` · `DIVIDE` · `RELATED` · filter context · time intelligence · `TOTALYTD` · what-if analysis · Goal Seek · Solver · data table · Scenario Manager · `QUERY` · Google Visualization API Query Language · `ARRAYFORMULA` · `IMPORTRANGE` · `VSTACK` · Connected Sheets · data warehouse · ODBC · README sheet · inconsistent formula · check cell · Go To Special · Inquire · audit

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can write `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, `MAXIFS`, and `MINIFS` with dates, wildcards, blanks, cell references, and OR logic, and switch to `SUMPRODUCT` when a condition needs a calculation.
- [ ] You know which average a question needs (per line, per order, per customer, weighted) and can calculate each.
- [ ] You can write `XLOOKUP` for an exact match, a band (approximate match), the last match, several return columns, and a two-way lookup, and explain the same lookups with `INDEX`/`MATCH`.
- [ ] You can say why `VLOOKUP` breaks and when approximate matching is correct.
- [ ] You can build a pivot table in both apps in under two minutes, with a filter, a percentage of total, grouped dates, and a slicer, and pull its numbers into a report with `GETPIVOTDATA`.
- [ ] You know the difference between counting lines and distinct counting, and how to do each.
- [ ] You can write `FILTER`, `UNIQUE`, `SORT`, and `LET` formulas and fix a `#SPILL!` error.
- [ ] You can combine a folder of files in Power Query, set types deliberately, filter, add a column, merge, and refresh.
- [ ] You can explain the difference between a calculated column and a measure, and write `SUMX`, `CALCULATE`, `DIVIDE`, and `TOTALYTD` measures.
- [ ] You can use Goal Seek and build a two-input what-if grid.
- [ ] You can write a `QUERY` formula with `where`, `group by`, `order by`, and `pivot`, and connect files with `IMPORTRANGE`.
- [ ] You can audit an inherited workbook with a checklist and find typed numbers, short ranges, duplicates, and inconsistent rules.
- [ ] You can name the signals that a job should move to SQL, Python, or a BI tool.
- [ ] (Optional, Timed challenge) You can solve the Stockroom case in 30 minutes: parse text codes, build a daily model with input cells, and search settings with a data table.

---

## Exercises

Use `ch11_practice.xlsx` (with the Sales data converted to a table named `Sales`) unless an exercise says otherwise.

### Warm-up

1. Match each pivot table area (Filters, Rows, Columns, Values) to what it does: (a) leaves rows out before summarizing, (b) makes one row per value, (c) makes one column per value, (d) holds the number in every cell.
2. `=VLOOKUP(C2, Customers!A2:D25, 4, FALSE)` returns each customer's segment. Someone inserts a new column between `customer_name` and `city` on the Customers sheet. What does the formula return now, and what formula would have kept working?
3. What does `F2#` refer to, and what causes a `#SPILL!` error?
4. For each, say whether it should be a calculated column or a measure: (a) a customer's rebate band, (b) gross margin %, (c) revenue year to date, (d) each line's product cost.
5. Name two things Excel can do that Google Sheets can't, and the Sheets alternative for each; then one thing the other way round.

### Core

6. With one `XLOOKUP`, return the name, city, and segment for customer `0014`.
7. Find Sharma Hardware's (`0001`) first and last order dates with `XLOOKUP`. What does the same lookup return for Home Plus (`0016`), and how would you make it readable?
8. Using the RebateBands sheet and an approximate match, find the band for each customer's 2025 net revenue (excluding cancelled orders). How many customers are in each band, what's the total rebate, and how far is Western Logistics from the next band?
9. Build a pivot table of net revenue by segment (rows) and quarter (columns), excluding cancelled orders. What was Wholesale's Q4 revenue, and what share of the year's revenue did Wholesale contribute?
10. In a pivot, count order lines by segment, then count distinct orders by segment. Give both sets of numbers and explain the difference.
11. Build a pivot of net revenue by sales rep and quarter. Which rep had the highest Q4, and how much revenue had no rep?
12. Use a pivot to find the top three products by net revenue, and the product that sold the least.
13. Write a `FILTER` formula that returns November's Wholesale order lines. How many rows does it return, and what's their total net revenue? Write the Google Sheets version too.
14. Write a formula that lists every customer who ordered in 2025, sorted A to Z. How many names does it return, and why not 24?
15. In Google Sheets, write a `QUERY` that returns net revenue by segment, excluding cancelled orders, largest first. Then change it to spread quarters across the top.
16. (Excel; Sheets alternative: the `VSTACK` route in section 11.7's tool note.) Build the Power Query from section 11.7 on `monthly_exports/`. How many rows does it load before and after the cancelled filter, and what's the total?
17. (Excel; Sheets alternative: delete the Dec tab from your `VSTACK` and watch the total.) Refresh test: remove `sales_2025_12.csv` from the folder and refresh. What are the new total and the new Q4 total? What should you check after every real refresh?
18. (Excel; Sheets alternative: turn the row into a column with `=TOCOL(TargetsWide!B2:M2)` and check the total.) Unpivot the TargetsWide sheet in Power Query. How many rows result, and what do they total?
19. (Excel for Windows; Sheets alternative: the `SUMIFS` ratio in section 11.8's tool note, with a segment or category condition.) In Power Pivot, create `Valid Net Revenue`, `Gross Margin`, and `Gross Margin %`. What's the overall gross margin %, and which segment and which category have the lowest?
20. (Excel for Windows; Sheets alternative: the year-to-date `SUMIFS` with `EOMONTH` from section 11.2.) Create `Revenue YTD` with a date table. What does it show at the end of June and the end of September?
21. Use Goal Seek to find how many extra Industrial Crates (₹1,400, 8% discount) June needed to reach its ₹3,00,000 target. Check the answer.
22. (Any app: use the mixed-reference version in Sheets.) Build the price-by-volume what-if grid from section 11.9. What's the value for a 3% price rise with 5% more volume? Which combination in the grid falls below 2025's revenue even though prices rose?

### Stretch

23. Audit `month_end_pack_2025_messy.xlsx` without reading the story. List every error you find, its effect in rupees, and the corrected total and percentage of target. Which error has no effect on 2025's numbers, and why does it still matter?
24. Using the month-by-segment grid you built in section 11.4, write two-way lookups, with `INDEX`/`MATCH` and with nested `XLOOKUP`, that return Retail's March revenue and Hospitality's July revenue.
25. Write a `GROUPBY` formula (Microsoft 365) that returns revenue by segment excluding cancelled orders. What does Retail show if you leave out the filter, and why?

### Think about it (no spreadsheet needed)

26. The finance team emails a 40-tab workbook every month: one tab per branch, each pasted from a different system, with a Summary tab. Which three changes from this chapter would you make first, and which signals from section 11.13 suggest it should eventually leave Excel?
27. Western Logistics is ₹1,272.50 below the Silver rebate band. The sales rep asks you to "count their cancelled order so they qualify". What do you say, and what information would help the business decide?
28. A manager says the pivot table in last week's report shows a different Q3 total from the one on your screen today, although "nobody changed anything". List three possible explanations and how you'd check each.

### Formula drills (sections 11.2–11.7)

Work these on the Sales table. Write each answer as one formula first, then check it another way (a pivot, a filter, or the status bar).

29. Net revenue from Retail **or** Hospitality customers, excluding cancelled orders. Write it two ways: two `SUMIFS` added together, and one `SUMIFS` with an array constant.
30. Net revenue (excluding cancelled orders) from every product whose name contains "Box", and how many lines that is.
31. For Wholesale and Hospitality, calculate the average net revenue **per line** and the average **per order**. Why are they so different, and which would you quote to a sales head?
32. Calculate gross sales before discount, the simple average discount %, and the revenue-weighted average discount %. Which is the "real" average discount?
33. Count the **distinct customers** who ordered in each segment with `SUMPRODUCT` and `COUNTIFS`.
34. Rank Metro Mart among customers by 2025 net revenue with `RANK.EQ` (or `COUNTIFS`).
35. Find Harbour Traders' first and last order dates with `MINIFS` and `MAXIFS`.
36. As of 31 December 2025, put each customer into a recency bucket (0–30, 31–60, 61–90, over 90 days since their last order). How many customers are in each bucket, and who has gone quiet for more than 90 days?
37. With a two-condition lookup, return the net revenue of the Industrial Crate line (product 105) on order 10107.
38. Build a rep-by-quarter pivot and use `GETPIVOTDATA` to return Farah Khan's Q3 revenue. What happens to your formula if someone removes `quarter` from the pivot?
39. In `month_end_pack_2025_messy.xlsx`, replace the Summary's twelve different formulas with one `SUMIFS(INDIRECT(…))` formula filled down. Which of the four planted errors does it fix, and which remains?
40. (Excel; Sheets alternative: `QUERY` with `group by K, N`.) In Power Query, group the valid sales by `month_start` and `segment` with net revenue, line count, and distinct order count. How many rows result, and what does October's Retail row show?
41. What do `WEEKNUM` (type 1) and `ISOWEEKNUM` return for 29 December 2025, and why does it matter for a weekly report?
42. Create the `NETREV` `LAMBDA` from section 11.6 and use it to calculate order 10003's second line (45 units at ₹750, 5% discount).

---

## Answers

**1.** Filters → (a), rows are left out before anything is summarized. Rows → (b), one row per value. Columns → (c), one column per value. Values → (d), the number (a sum, count, or average) in every cell. Rows and Columns do the same job in two directions, which is why a pivot can be rearranged by dragging a field from one to the other.

**2.** The table `A2:D25` expands to `A2:E25`, but the column number stays 4, which now points at `city` instead of `segment`. The formula returns cities, with no error. `=XLOOKUP(C2, Customers!A2:A25, Customers!E2:E25)` or `=INDEX(Customers!E2:E25, MATCH(C2, Customers!A2:A25, 0))` would have kept working, because Excel updates the column reference (`D` becomes `E`) when the column moves.

**3.** `F2#` refers to the entire spill range of the dynamic array formula in `F2`, whatever size it currently is. `#SPILL!` means the result can't spill because at least one cell in the space it needs isn't empty (a typed value, another formula, or merged cells), or because the formula is inside an Excel table.

**4.** (a) **Calculated column** (or a column in Power Query): it's an attribute you'd filter or group by. (b) **Measure**: a ratio must be recalculated for each pivot cell, not added up. (c) **Measure**: it depends on the dates in the filter context. (d) **Calculated column** is reasonable (`quantity × RELATED(unit_cost)`), though a measure with `SUMX` avoids storing it.

**5.** Excel-only examples: Power Query (Sheets alternative: `IMPORTRANGE`, `VSTACK`, and `QUERY`, or Apps Script, or cleaning in SQL/Python first); Power Pivot and DAX (Sheets alternative: `QUERY` on pre-joined data, Connected Sheets, Looker Studio); Data Table (a mixed-reference grid); `GROUPBY` (`QUERY` with `group by`). Sheets-only examples: `QUERY`, `IMPORTRANGE`, `IMPORTHTML`/`GOOGLEFINANCE`, and Google Forms.

**6.** `=XLOOKUP("0014", Customers!A2:A25, Customers!B2:D25)` returns three cells: **Deccan Packaging · Hyderabad · Wholesale**. In Excel the result spills across; in Sheets it fills three cells.

**7.** First: `=XLOOKUP("0001", Sales[customer_code], Sales[order_date])` → **2025-01-24** (order 10007). Last: `=XLOOKUP("0001", Sales[customer_code], Sales[order_date], "never", 0, -1)` → **2025-12-05** (order 10161). This relies on the table being sorted by date; `MAXIFS(Sales[order_date], Sales[customer_code], "0001")` gives the latest date regardless of order. Home Plus returns `#N/A` without the fourth argument; with `"never"` (or `"no orders in 2025"`) it's readable.

**8.** First calculate each customer's revenue (a pivot, or `SUMIFS` next to `SORT(UNIQUE(...))`), then `=XLOOKUP(G2, RebateBands!A2:A4, RebateBands!C2:C4, , -1)` for the band and `…B2:B4…` for the rate. **Gold 2** (Sharma Hardware ₹5,02,775.00 and Harbour Traders ₹4,12,680.50), **Silver 6** (Northgate Distributors, Green Leaf Hotels, Metro Mart, Coastal Foods, Deccan Packaging, Fresh Bowl Kitchens), **Standard 15**. Total rebate: **₹37,642.03** (for example Sharma Hardware: 2% × ₹5,02,775 = ₹10,055.50). Western Logistics has ₹2,48,727.50, which is **₹1,272.50** short of ₹2,50,000. The common mistake is an exact-match lookup, which returns `#N/A` for every customer.

**9.** Wholesale Q4: **₹7,56,751.00**. Wholesale's share of the year: ₹17,02,658.50 ÷ ₹43,35,471 = **39.3%** (**Show Values As → % of Grand Total** in Excel, **Show as → % of grand total** in Sheets). If your grand total is ₹43,98,121, the cancelled filter is missing.

**10.** Count of `order_id` (lines): Hospitality **107**, Retail **114**, Wholesale **105**, total 326. Distinct count (orders): Hospitality **59**, Retail **59**, Wholesale **55**, total **173**. An order with several products has several lines, so counting lines overstates orders. Excel needs the Data Model for **Distinct Count**; Sheets uses **COUNTUNIQUE**.

**11.** Q4 by rep: Rahul Mehta **₹6,82,889.00**, Farah Khan ₹6,07,959.50, Neha Kulkarni ₹3,67,820.00. **Rahul Mehta** had the highest Q4. Revenue with no rep: **₹2,04,502.50** for the year (it appears as *(blank)* in Excel's pivot). Rahul's Q4 was more than a third of his annual ₹14,94,000.50.

**12.** Top three: **Storage Box 25L ₹9,08,212.50**, **Storage Box 10L ₹8,60,946.00**, **Industrial Crate ₹7,95,830.00**. The least: **Garden Chair ₹33,637.50**.

**13.** Excel: `=FILTER(Sales[[order_id]:[net_revenue]], (Sales[month_start]=DATE(2025,11,1))*(Sales[segment]="Wholesale"), "no rows")`. Sheets: `=FILTER(Sales!A2:J331, Sales!K2:K331=DATE(2025,11,1), Sales!N2:N331="Wholesale")`. **15 rows**, totaling **₹3,43,685.50** (check it with `=SUM(FILTER(Sales[net_revenue], (Sales[month_start]=DATE(2025,11,1))*(Sales[segment]="Wholesale")))`). No November Wholesale lines were cancelled, so no status condition is needed here, but adding `*(Sales[status]<>"Cancelled")` is the safer habit.

**14.** `=SORT(UNIQUE(Sales[customer_name]))` returns **23** names, starting Blue Bay Cafe, City Needs Store, Coastal Foods. Riverstone has 24 customers, but **Home Plus** placed no orders in 2025, so it doesn't appear in the sales data. To list all customers, use the Customers sheet; to find customers with no orders, compare the two lists (a Left Anti merge, section 11.7).

**15.** `=QUERY(Sales!A1:S331, "select N, sum(J) where H <> 'Cancelled' group by N order by sum(J) desc label sum(J) 'net_revenue'", 1)` → Wholesale 1702658.5, Retail 1488773.75, Hospitality 1144038.75. Quarters across the top: `"select N, sum(J) where H <> 'Cancelled' group by N pivot L"`, which gives Q1–Q4 columns matching Figure 11.3.

**16.** **330 rows** before the filter (15 + 20 + 18 + 21 + 29 + 22 + 29 + 28 + 40 + 38 + 35 + 35), **326** after, total **₹43,35,471**. If the total is right but `customer_code` shows `2` instead of `0002`, the automatic **Changed Type** step is still there.

**17.** Without December: total **₹38,95,647.50** (₹43,35,471 − ₹4,39,823.50) and Q4 **₹13,14,478.75** (after refreshing the pivot too). After every real refresh, check the rows loaded against the lines in the files, lines per file (a missing or partial month), the grand total against an independent number, and that no step shows an error.

**18.** Select `year` → **Unpivot Other Columns**: **12 rows** (Jan to Dec), totaling **₹42,40,000**. Rename `Attribute` and `Value` to `month` and `target`, and convert `month` to a real date if you'll join it to the Calendar table.

**19.** Overall **26.2%** (₹11,37,221 on ₹43,35,471). Lowest segment: **Wholesale 19.0%** (Hospitality 32.4%, Retail 29.8%). Lowest category: **Industrial 13.6%** (Kitchen 33.2%, Storage 26.9%, Furniture 24.2%). A common error is summing a gross margin % column, which gives meaningless totals; the measure recalculates for each cell.

**20.** End of June **₹14,60,879.75**; end of September **₹25,81,168.75**; December ₹43,35,471. If YTD equals each month's own revenue, the Calendar table isn't marked as a date table or isn't related to `order_date`.

**21.** Model: `=B1+B2*B3*(1-B4/100)` with B1 = 186928, B3 = 1400, B4 = 8. Goal Seek sets `B5` to 300000 by changing `B2`: **87.79**, so **88 crates**. Check: 88 × ₹1,288 = ₹1,13,344; ₹1,86,928 + ₹1,13,344 = **₹3,00,272**, which reaches the target, while 87 crates give ₹2,98,984, which doesn't.

**22.** Price +3%, volume +5%: **₹46,88,812** (43,35,471 × 1.03 × 1.05). **Price +5% with volume −5%** gives ₹43,24,632, below 2025's ₹43,35,471, because 1.05 × 0.95 = 0.9975. (Price +3% with −5% volume gives ₹42,42,258, also below.) The Sheets version: `=$B$1*(1+$B6)*(1+C$5)` copied across the grid.

**23.** Four errors, as in the story: **October** range stops at row 30 (9 lines, **−₹1,36,023**); **December** last five lines pasted twice (**+₹46,555**); **April** uses `SUM`, including cancelled order 10034 (**+₹24,800**); **November** typed as 6,33,480 (**+₹72**). Net effect −₹64,596. Corrected total **₹43,35,471**, **102.3%** of target (the messy version: ₹42,70,875, 100.7%). **March** also uses `SUM` but had no cancelled orders, so it's right by luck; it matters because the rule is wrong and will fail the first time a March order is cancelled.

**24.** On the Grid sheet (months in `A5:A16`, segments in `B4:D4`): `=INDEX(B5:D16, MATCH(DATE(2025,3,1), A5:A16, 0), MATCH("Retail", B4:D4, 0))` and `=XLOOKUP("Retail", B4:D4, XLOOKUP(DATE(2025,3,1), A5:A16, B5:D16))` both return **₹1,41,800**. For Hospitality in July, change the date to `DATE(2025,7,1)` and the segment to `"Hospitality"`: **₹94,263.75**. The first `MATCH` gives 3 (March) or 7 (July); the second gives 2 (Retail) or 1 (Hospitality).

**25.** `=GROUPBY(Sales[segment], Sales[net_revenue], SUM, , , , Sales[status]<>"Cancelled")` → Hospitality ₹11,44,038.75, Retail ₹14,88,773.75, Wholesale ₹17,02,658.50, total ₹43,35,471. Without the filter, Retail shows **₹15,51,423.75**, because both cancelled orders (10034, ₹24,800, and 10131, ₹37,850) were from Retail customers.

**26.** First changes: (1) load each branch's data with Power Query (or one query per source system) into one long table with a `branch` column, instead of pasted tabs; (2) apply the rules once and build the Summary as a pivot or measures; (3) add check cells and a README with the refresh steps. Signals that it should leave Excel: several source systems joined every month, many people depending on it, a monthly manual refresh that should be scheduled, and the cost of an error in a finance report. A database or warehouse with SQL, feeding Power BI or a refreshable workbook, is the likely destination.

**27.** Say no: a cancelled order isn't revenue under the report's rule, and changing the rule for one customer would make the rebate report inconsistent (and, for a real rebate, it would be paid on sales that didn't happen). Offer what would help the decision instead: how close other customers are to each band, the cost of lowering the Silver threshold or adding a grace margin for everyone, and whether Western Logistics' 2026 orders are on track to reach the band. Chapter 24 covers handling "can you just change the number?"

**28.** Possible explanations: (1) **the pivot was refreshed** after new or corrected data arrived (check the query's last refresh time and the data's row count); (2) **a filter or slicer differs** (for example, cancelled orders included in one version; compare the filter settings and the grand totals); (3) **the source data was changed** (a late order, a corrected discount, a re-exported month; compare the two data snapshots with version history or the file dates). A dated "as of" note and a row-count check cell on the report prevent the argument next time.

**29.** `=SUMIFS(Sales[net_revenue], Sales[segment], "Retail", Sales[status], "<>Cancelled") + SUMIFS(Sales[net_revenue], Sales[segment], "Hospitality", Sales[status], "<>Cancelled")` and `=SUM(SUMIFS(Sales[net_revenue], Sales[segment], {"Retail","Hospitality"}, Sales[status], "<>Cancelled"))`. Both return **₹26,32,812.50** (₹14,88,773.75 + ₹11,44,038.75). The array constant makes `SUMIFS` return two totals, and `SUM` adds them. A common mistake is two criteria pairs on the same column, which asks for rows that are Retail *and* Hospitality at once and returns 0.

**30.** `=SUMIFS(Sales[net_revenue], Sales[product_name], "*Box*", Sales[status], "<>Cancelled")` returns **₹23,15,788.50**, and the matching `COUNTIFS` returns **168** lines: Storage Box 10L, Storage Box 25L, and Lunch Box Set. Wildcards aren't case-sensitive, so "*box*" gives the same result.

**31.** Per line: Wholesale **₹16,215.80**, Hospitality **₹10,691.95** (`AVERAGEIFS`). Per order: Wholesale **₹30,957.43** (₹17,02,658.50 ÷ 55 orders), Hospitality **₹19,390.49** (₹11,44,038.75 ÷ 59). An order has about two lines on average, so per-order values are roughly double. A sales head thinks in orders (and the business-wide average order value is ₹25,060.53), so quote the per-order figure and say how it was calculated.

**32.** Gross sales before discount: `=SUMPRODUCT(Sales[quantity], Sales[unit_price], --(Sales[status]<>"Cancelled"))` → **₹45,48,725**. Simple average discount: `=AVERAGEIFS(Sales[discount_pct], Sales[status], "<>Cancelled")` → **4.06%**. Weighted: `=1 - 4335471/4548725` → **4.69%**. The weighted figure is the real average: it's the share of list value Riverstone gave away, and larger lines carried larger discounts.

**33.** `=SUMPRODUCT((Sales[segment]="Wholesale") * (Sales[status]<>"Cancelled") / COUNTIFS(Sales[customer_name], Sales[customer_name], Sales[status], "<>Cancelled"))` for each segment: Hospitality **9**, Retail **8**, Wholesale **6**, total 23. The `COUNTIFS` counts each customer's valid lines, so each valid line contributes 1 ÷ (that customer's valid lines) and every customer adds up to exactly 1. A common mistake is to group the denominator by status too (`…, Sales[status], Sales[status]`): a customer with Delivered and Shipped lines then counts once per status, and Hospitality comes out as 11. If a customer's only lines were cancelled, the denominator would be 0 for them; wrap the division as `IFERROR((…)/COUNTIFS(…), 0)` (confirm with **Ctrl+Shift+Enter** in Excel 2019 and older). In Microsoft 365, `=ROWS(UNIQUE(FILTER(Sales[customer_name], (Sales[segment]="Wholesale")*(Sales[status]<>"Cancelled"))))` is easier to read.

**34.** With customer names in `F2:F24` and their revenue in `G2:G24`: `=RANK.EQ(G13, $G$2:$G$24, 0)` for Metro Mart gives **5** (after Sharma Hardware, Harbour Traders, Northgate Distributors, and Green Leaf Hotels). `=COUNTIFS($G$2:$G$24, ">"&G13)+1` gives the same rank without `RANK.EQ`.

**35.** `=MINIFS(Sales[order_date], Sales[customer_name], "Harbour Traders", Sales[status], "<>Cancelled")` → **2025-04-09**; `MAXIFS` → **2025-12-14**. Format both cells as dates; `MINIFS` returns a date serial number.

**36.** Last order per customer with `MAXIFS`, then `=DATE(2025,12,31)-last_order` for days, then `=IFS(days<=30,"0-30",days<=60,"31-60",days<=90,"61-90",TRUE,"90+")`. Counts: **0–30: 15**, **31–60: 4**, **61–90: 1**, **90+: 3** (23 customers). Over 90 days: **City Needs Store, Om Sai Provisions, and Sunrise Caterers**. Sharma Hardware, for comparison, last ordered 26 days before year-end.

**37.** `=XLOOKUP(1, (Sales[order_id]=10107) * (Sales[product_id]=105), Sales[net_revenue])` → **₹56,700**. In any version: `=INDEX(Sales[net_revenue], MATCH(1, INDEX((Sales[order_id]=10107)*(Sales[product_id]=105), 0), 0))`. Because the pair is unique, `=SUMIFS(Sales[net_revenue], Sales[order_id], 10107, Sales[product_id], 105)` also works, and it's the fastest to type in a competition.

**38.** `=GETPIVOTDATA("net_revenue", $A$3, "sales_rep", "Farah Khan", "quarter", "Q3")` → **₹4,92,618.75**. If `quarter` is removed from the pivot (or a slicer hides Farah Khan), the item is no longer visible and the formula returns **`#REF!`**. Keep report-feeding pivots on a locked sheet and check `GETPIVOTDATA` cells with `ISERROR` in a check cell.

**39.** With month names in `A4:A15`: `=SUMIFS(INDIRECT("'"&A4&"'!J2:J100"), INDIRECT("'"&A4&"'!H2:H100"), "<>Cancelled")`, filled down. It fixes three errors: **October** (the range now reaches row 100: ₹6,81,070.75), **April** (the same rule everywhere: ₹2,10,281.50), and **November** (no typed number: ₹6,33,408). It doesn't fix **December**'s double paste, because the duplicated lines are real rows on the sheet: December still shows ₹4,86,378.50 instead of ₹4,39,823.50. A formula can only be as right as its data; the duplicate needs a check such as `COUNTIFS(order_id, A2, product_id, D2)>1`.

**40.** **Home → Group By → Advanced**, grouping by `month_start` and `segment`, with **Sum** of `net_revenue`, **Count Rows**, and a distinct count of `order_id` (see the tool note in section 11.7: a second Group By, or `each List.Count(List.Distinct([order_id]))` in the Advanced Editor). **36 rows** (12 months × 3 segments). October Retail: **₹2,83,025**, **12** lines, **7** orders.

**41.** `WEEKNUM(DATE(2025,12,29), 1)` returns **53** (weeks start on Sunday, and week 1 contains 1 January). `ISOWEEKNUM` returns **1**: under the ISO standard, 29 December 2025 belongs to week 1 of 2026. A weekly report that mixes the two splits or merges a week at the year boundary, so agree one system and write it on the report.

**42.** **Formulas → Name Manager → New**, name `NETREV`, refers to `=LAMBDA(q, p, d, q * p * (1 - d/100))`. `=NETREV(45, 750, 5)` returns **32062.5**, matching Chapter 10's hand check. `LAMBDA` is in Microsoft 365 and Google Sheets (via **Data → Named functions**).

**Timed challenge: Riverstone Rewards.** The answers to the practice case:

| Level | Answer |
|---|---|
| L1 | **173** orders; **70** worth ₹25,000 or more |
| L2 | **43,287** base points; **Sharma Hardware** (5,019) |
| L3 | **24** Gold-tier orders; **56** Silver (93 Standard) |
| L4 | **50,403** tier points |
| L5 | **129** streak orders; **76,203** points |
| L6 | **79,703** order points |
| L7 | **3** customers (City Needs Store, Om Sai Provisions, Sunrise Caterers); **2,273** points expire |
| L8 | **Sharma Hardware, 9,794**; **9** customers with 4,000 or more |
| B1 | **Sharma Hardware**, on order **10088** (12 August 2025, running total 5,346) |
| B2 | **October 2025**, **12,446** points |
| B3 | **3** customers (Coastal Foods, Metro Mart, Sharma Hardware) |
| B4 | **4** (Metro Mart, 7,062 points) |

The most common wrong answers come from four traps: counting cancelled order 10131 (it's in the Lines sheet); using a customer's *total* revenue for the tier instead of revenue from earlier orders only (Sharma Hardware's first order is Standard, not Gold); giving the streak bonus to January orders (there's no December 2024 in the data); and expiring points for customers who ordered in Q4. Check L3 by hand for one customer: Sharma Hardware moves to Silver on order 10018 (₹1,12,750 of earlier orders) and to Gold on order 10088 (₹2,60,372.50).

---

## Where this leads

- **Chapter 12, Databases & SQL Foundations:** the pivot table's grouping, the lookup's matching, and `QUERY`'s words in a real database, for data too big or too shared for a spreadsheet.
- **Chapter 13, SQL for Real Analysis:** running totals, rankings, and month-over-month changes with window functions, the SQL versions of **Show Values As** and `TOTALYTD`.
- **Chapter 14, Data Cleaning & Preparation:** the messy data this chapter assumed away (spelling variants, mixed dates, duplicates), in Power Query, SQL, and pandas.
- **Chapter 16, Business Intelligence with Power BI:** the same Power Query and DAX engines, with a star schema, `CALCULATE` in depth, and dashboards that refresh on a schedule.
- **Chapter 18, Python for Analysts:** `pandas.merge`, `groupby`, and `pivot_table`, which do in code what lookups and pivot tables do here.
- **Chapter 19, Spreadsheet Automation:** macros and scripts for the steps Power Query can't do, such as saving a PDF and emailing it.
- **Chapter 20, Automating Reports & Delivering Insights:** scheduling the refresh this chapter still starts by hand.
- **Interview preparation:** the Excel, Google Sheets, VBA & BI Question Bank (Chapter 70) includes live pivot table, `XLOOKUP`, `INDEX`/`MATCH`, Power Query, and DAX tasks, and "how would you automate this monthly report?"
