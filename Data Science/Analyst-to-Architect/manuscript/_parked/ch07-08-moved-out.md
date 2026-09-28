# Parked: blocks moved out of Chapters 7 and 8 (Part 0 + I build, 28 Sep 2026)

These blocks were removed from Chapters 7 and 8 under rule R1/R2 (no code or tool preview boxes in
Parts 0 and 1; findings S.1, S.4, I.3) and fix instructions 7.1, 7.4 and 8.7 (finding I.6). Each is kept
**verbatim** below, labelled with its destination. The destination part's build pulls the block from here,
rewrites it to point **back** where needed ("In Chapter 7 you saw the analyst's answer; here is the query
behind it"), and deletes it from this file. Rupee amounts are as they stood before the lakh-grouping pass
(option pick 67.9): convert them when the block is placed.

---

## 1. Ch 7 §7.6 Step 2: the PostgreSQL query and its output

**Destination:** Ch 12 (Part 2 build), next to the mini-database version in §12.15, as "the query behind

**Landed** in Ch 12's answer 30 (exercise 30 asks the reader to write it first), re-run on riverstone_2025 (Part 2/3 build).
Chapter 7's five quiet customers". Rechecked on 28 Sep 2026 against `companion/riverstone_2025_setup.sql`
(loaded into SQLite): the same five customers, 284 / 204 / 162 / 66 days, Home Plus with no order.

> The data analyst writes a query against the one-year database. You don't need to read SQL yet; look at the shape of the question in the code, then at the answer.

```sql
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2025-12-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;
```

```
   customer_name   |   segment   | last_order_date | days_since_last_order
-------------------+-------------+-----------------+-----------------------
 Home Plus         | Retail      |                 |
 City Needs Store  | Retail      | 2025-03-22      |                   284
 Sunrise Caterers  | Hospitality | 2025-06-10      |                   204
 Om Sai Provisions | Retail      | 2025-07-22      |                   162
 Tasty Tiffins     | Hospitality | 2025-10-26      |                    66
(5 rows)
```

> **How it works, in plain words.**
>
> - The query starts from every customer, then looks up each one's orders, ignoring cancelled ones.
> - For each customer, it finds the latest order date, and counts the days from that date to 31 December 2025.
> - It keeps only customers whose latest order was before 1 November, plus customers with no orders at all.
> - The blank dates are Home Plus: it signed up on 18 June 2025 and has never ordered, so there's no date to show.

---

## 2. Ch 7 §7.6 "SQL link" box

**Destination:** Ch 12 §12.15 / Ch 13 Pattern 6 intro, rewritten to point back to Chapter 7.

**Landed** in Ch 12 §12.15 (the "Back to Chapter 7" box after Question 1) and Ch 13 §13.8 (Pattern 6 opens with a pointer back to Chapter 7) (Part 2/3 build).

> **SQL link.** Chapter 12 teaches every clause in this query and includes a version of it on the mini database (section 12.15). Chapter 13 improves the rule itself, comparing each customer's silence with their own usual ordering rhythm (Pattern 6).

---

## 3. Ch 7 §7.6 "Dialect note" and the MySQL query and output

**Destination:** Ch 12 (MySQL column of the same example).

**Landed** in Ch 12's answer 30 (the MySQL version), re-run (Part 2/3 build).

> **Dialect note.** The same question in MySQL needs two changes: `DATEDIFF` instead of subtracting dates, and a manual sort to put the blank dates first, because MySQL has no `NULLS FIRST`. The result is the same five customers.

```mysql
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                         AS last_order_date,
       DATEDIFF('2025-12-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NOT NULL, last_order_date;
```

```
+-------------------+-------------+-----------------+-----------------------+
| customer_name     | segment     | last_order_date | days_since_last_order |
+-------------------+-------------+-----------------+-----------------------+
| Home Plus         | Retail      | NULL            |                  NULL |
| City Needs Store  | Retail      | 2025-03-22      |                   284 |
| Sunrise Caterers  | Hospitality | 2025-06-10      |                   204 |
| Om Sai Provisions | Retail      | 2025-07-22      |                   162 |
| Tasty Tiffins     | Hospitality | 2025-10-26      |                    66 |
+-------------------+-------------+-----------------+-----------------------+
```

---

## 4. Ch 7 Tools: companion file line

**Destination:** Ch 12's companion list (fix instruction 7.4). The file itself stays where it is:

**Landed** in Ch 12's Tools list (Part 2/3 build); the file was merged into `companion/mysql/ch12_queries_mysql.sql`.
`companion/mysql/ch07_queries_mysql.sql` (consider renaming it for Ch 12 in the Part 2 build).

> - **Companion file (optional):** `companion/mysql/ch07_queries_mysql.sql` holds the section 7.6 query in PostgreSQL and MySQL form, for readers who already have the practice databases loaded (Chapter 12, section 12.3, explains the setup).

---

## 5. Ch 8 §8.6: the three-role salary table, the role comparison and the growth discussion (whole old text)

**Destination:** Ch 68 (How Data Hiring Works), where pay is discussed for the job search (fix instruction
8.7, finding I.6). Ch 8 keeps only the data analyst row, re-verified and relabelled "Average base salary"
(finding I.5). **Before placing:** re-verify the Data Scientist and Data Engineer rows against the live
PayScale pages (T13; not re-verified in the Part 0 + I build, only the Data Analyst row was), convert rupee
amounts to lakh grouping, and relabel the last column "Average base salary" (PayScale's headline wording;
its chart marks the same value as the median). The "1.73 times" comparison uses PayScale's rounded figures
(₹1m ÷ ₹577k): if kept, compute it from the same kind of figure for both roles. The Indeed figure below is
stale: on 20 Sep 2026 the page showed ₹6,29,019 from 605 salaries (Ch 8 now uses that). Old exercise 6 (data
engineer growth, answer 56.4%) belongs with this table.

> ### Three roles, as published in 2026
> 
> Here are figures for three roles, as shown on PayScale's India pages (updated in July 2026) when this chapter was written. **Base salary** is fixed yearly pay before bonuses; **total pay** adds bonuses and similar extras.
> 
> | Role (PayScale title) | Salary profiles | Average total pay, under 1 year | Average total pay, 1–4 years | Base salary, 10th–90th percentile | Median base salary |
> |---|---|---|---|---|---|
> | Data Analyst | 2,389 | ₹413,462 | ₹565,999 | about ₹289,000 to ₹1 million | about ₹577,000 |
> | Data Scientist | 1,267 | ₹595,255 | ₹1,005,147 | about ₹312,000 to ₹2 million | about ₹1 million |
> | Data Engineer | 1,284 | ₹518,398 | ₹810,624 | about ₹410,000 to ₹2 million | about ₹975,000 |
> 
> *Source: PayScale India job pages for each title, pages updated 9–14 July 2026, retrieved 16 September 2026. PayScale rounds its percentile figures (for example "₹1m"), so those columns are approximate. Figures change often; check the live pages.*
> 
> In Indian terms, a data analyst's average total pay in the first year works out to about ₹4.1 lakh, and a data scientist's average in years one to four to about ₹10.1 lakh.
> 
> A **percentile** tells you where a value sits in a sorted list. The 10th percentile is the value below which 10% of reported salaries fall; the 90th percentile is the value below which 90% fall. So "₹289,000 to ₹1 million" means the middle 80% of data analyst profiles reported base pay in that range. The **median** is the middle value: half earn less, half earn more.
> 
> ### Reading the table carefully
> 
> **The pattern is clearer than the numbers.** Roles that need more tiers of skill (science and engineering) show higher medians and faster early growth than the analyst role in this data. The data scientist median base salary (about ₹1 million) is roughly 1.73 times the data analyst median (about ₹577,000).
> 
> **Don't read growth as a promise.** Average total pay for data analysts with 1–4 years is 36.9% higher than for those under a year: (₹565,999 ÷ ₹413,462 − 1) × 100 = 36.9%. For data scientists the difference is 68.9%, and for data engineers 56.4%. But these are *different groups of people*, not the same people a few years later. People who left the field, or never reported, aren't in the data.
> 
> **Sources disagree.** For data analysts, Indeed's India page (based on 681 salaries from job postings, updated 30 August 2026) showed an average of ₹633,625 a year. PayScale's average base salary for the same title was ₹577,472. The difference is ₹56,153, with Indeed about 9.7% higher. That's not an error: one counts advertised pay across all experience levels, the other counts reported base salaries.
> 
> **Some roles don't have reliable figures under their own title yet.** Analytics engineer, AI engineer, and integration engineer are newer titles, and many people doing that work are listed under older ones (data engineer, software engineer, BI developer). Business analyst figures mix IT business analysts, finance business analysts, and more. For these, look at live job postings for the work you'd do, not only the title, and compare several sources.
> 

Old exercise 6 and answer 6:

> 6. Using the PayScale table in section 8.6, calculate how much higher average total pay is for data engineers with 1–4 years than for those under a year, as a percentage. Then give one reason why this isn't the pay rise a new data engineer should expect after a few years.

> **6.** (₹810,624 ÷ ₹518,398 − 1) × 100 = **56.4%** higher. It isn't a promised rise because the two figures come from **different groups of people**, not the same people over time. The 1–4 year group also only includes people still in the role who chose to report, and pay depends heavily on city, company, and skills. Any one of these is a good reason.

---
