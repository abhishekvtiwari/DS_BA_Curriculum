# Parked: blocks moved out of Chapter 13 (Part 2 build, 28 Sep 2026)

Finding 13.1 (theme M.7): recursive CTEs are taught in Chapter 28, not in Chapter 13. Chapter 13 now uses a
calendar table (`calendar_months`, `calendar_days`, created by `companion/ch13/calendar_tables_*.sql`) as its
date spine in both databases. The blocks below are kept **verbatim** as they stood in Chapter 13 before the
move. The Chapter 28 build places them in its recursive-CTE section, with a pointer back to Chapter 13
Pattern 5 ("Pattern 5 used a calendar table; here is how to build the same list of months when you don't have
one"), and deletes them from this file. Rupee amounts are as they stood before the lakh-grouping pass: convert
them when the block is placed (₹439,824 → ₹4,39,824).

---

## 1. Ch 13 §13.8 "A date spine with a recursive CTE" (block, output, explanation, watch-out)

**→ Ch 28, recursive CTEs section** (with a pointer back to Ch 13 Pattern 5). Its outputs were real MySQL
runs on `riverstone_2025` and still match (28 Sep 2026).

**Landed** in Ch 28 §28.2, "A list of months when there's no calendar table", with the pointer back to Pattern 5 (Part 2/3 build). Kept here for the record.

### A date spine with a recursive CTE

MySQL has no `generate_series`, but it can build the list of months with a **recursive CTE**: a CTE that refers to itself. Here is Pattern 5's Garden Chair query in MySQL:

```mysql
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month           -- the first month
    UNION ALL
    SELECT month + INTERVAL 1 MONTH             -- add one month...
    FROM months
    WHERE month < DATE '2025-12-01'             -- ...until December
),
furniture AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(net_revenue)                                  AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
filled AS (
    SELECT m.month,
           COALESCE(f.revenue, 0)                              AS revenue,
           LAG(COALESCE(f.revenue, 0)) OVER (ORDER BY m.month) AS previous_month
    FROM months AS m
    LEFT JOIN furniture AS f ON f.month = m.month
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(previous_month, 0) AS previous_month
FROM filled
WHERE month BETWEEN '2025-02-01' AND '2025-06-01'
ORDER BY month;
```

```
+------------+---------+----------------+
| month      | revenue | previous_month |
+------------+---------+----------------+
| 2025-02-01 |       0 |              0 |
| 2025-03-01 |   16388 |              0 |
| 2025-04-01 |       0 |          16388 |
| 2025-05-01 |   17250 |              0 |
| 2025-06-01 |       0 |          17250 |
+------------+---------+----------------+
```

**How the recursive CTE works.** Read `months` as a loop in two parts joined by `UNION ALL`:

1. **The starting row** (`SELECT DATE '2025-01-01'`) runs once and produces January.
2. **The recursive part** (`SELECT month + INTERVAL 1 MONTH FROM months …`) reads the row just produced and adds a month. It keeps running on each new row until its `WHERE` stops being true. After it produces December, `month < '2025-12-01'` is false, and the loop ends.

The rest of the query is unchanged from Pattern 5. `WITH RECURSIVE` is written once, at the start of the `WITH` clause, even though only the first CTE is recursive. `WITH RECURSIVE` works in PostgreSQL too (there the step is written `month + INTERVAL '1 month'`), so a recursive CTE is the date-spine method you can take to either database with the smallest change. Chapter 28 uses recursive CTEs for another classic job: walking an org chart from the managing director down, however many levels deep it goes.

> **Watch out: MySQL's 1,000-row safety limit.** To stop a badly written recursive CTE from running forever, MySQL aborts one that goes past 1,000 steps, with *"Recursive query aborted after 1001 iterations"*. A monthly spine is far below that, but a **daily** spine for three years needs 1,096 rows and fails. For a longer spine, raise the limit for your session first:
>
> ```
> SET SESSION cte_max_recursion_depth = 5000;
> ```
>
> Better still, for dates you'll use again and again, ask whether your company has a permanent calendar table, as section 13.7 suggests.

---

## 2. Ch 13 exercise 16 and its answer (recursive daily spine, MySQL)

**→ Ch 28, as an exercise in the recursive-CTE section** (optional). Chapter 13's exercise 16 now uses the
`calendar_days` table and gives the same answer (31 / 17 / 439824).

**Landed** in Ch 28 as exercise 23 and its answer (Part 2/3 build). Kept here for the record.

16. *(MySQL, one-year database.)* Build a **daily** date spine for December 2025 with a recursive CTE. Use it to show how many days the month had, how many of those days had no orders, and the month's total revenue. Check the total against section 13.6.

**16.** *(MySQL.)* A recursive CTE produces the 31 days; a left join keeps the days with no sales:

```mysql
WITH RECURSIVE days AS (
    SELECT DATE '2025-12-01' AS day
    UNION ALL
    SELECT day + INTERVAL 1 DAY
    FROM days
    WHERE day < DATE '2025-12-31'
),
daily_sales AS (
    SELECT order_date, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01'
    GROUP BY order_date
)
SELECT COUNT(*)                                          AS days_in_month,
       SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END) AS days_without_orders,
       ROUND(SUM(COALESCE(s.revenue, 0)), 0)             AS month_revenue
FROM days AS d
LEFT JOIN daily_sales AS s ON s.order_date = d.day;
```

```
+---------------+---------------------+---------------+
| days_in_month | days_without_orders | month_revenue |
+---------------+---------------------+---------------+
|            31 |                  17 |        439824 |
+---------------+---------------------+---------------+
```

The revenue matches December in section 13.6 (₹439,824). ✓ Orders came in on only 14 of December's 31 days, which is normal for a B2B supplier whose customers order every few weeks, and a reason daily charts for this kind of business need a date spine: without one, the 17 empty days would simply vanish. `SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END)` counts the unmatched days. A 31-row spine is well within MySQL's 1,000-step recursion limit, so no setting needs changing.
