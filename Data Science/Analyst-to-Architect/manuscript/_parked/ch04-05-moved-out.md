# Parked: blocks moved out of Chapters 4 and 5 (Part 0 + I build, 28 Sep 2026)

These blocks were removed from Chapters 4 and 5 under rule R1/R2 (no code or tool preview boxes in
Parts 0 and 1; findings S.1, S.4) and fix instructions 4.1, 4.2 and 5.1. Each is kept **verbatim** below,
labelled with its destination. The destination part's build pulls the block from here, rewrites it to
point **back** ("In Chapter 4 you worked this out by hand; here is the formula"), explains every line,
and deletes it from this file. The rupee amounts are as they stood before the lakh-grouping pass
(option pick 67.9): convert them when the block is placed.

---

## 1. Ch 4 "Chapter at a glance", Tools and Practice data lines (old wording)

**Destination:** Ch 10, first practice file (fix instruction 4.2: "Open numbers_practice.xlsx: every

**Landed** in Ch 10 §10.0 and the Chapter at a glance box (Part 2/3 build).
number from Chapter 4 is here, now with formulas"). The workbook itself is kept.

> **Tools:** a calculator (your phone's is fine), a pen, and a notebook. A spreadsheet is optional; the *Spreadsheet link* notes show each calculation in Excel and Google Sheets.
>
> **Practice data:** Riverstone's 2025 sales from the one-year database: monthly revenue, targets, and margins, and 173 orders. The companion workbook `numbers_practice.xlsx` (Appendix E) holds the same numbers with every formula from this chapter. Every number was checked by script.

---

## 2. Ch 4 §4.1 "Spreadsheet link" box

**Destination:** Ch 10 §10.7 (Essential functions) or Ch 11 §11.3, as a "Back to Chapter 4: now let

**Landed** in Ch 10 §10.8, "Back to Chapter 4" (Part 2/3 build).
the spreadsheet do it" exercise (fix instruction 4.1).

> **Spreadsheet link.** In Excel and Google Sheets, with the old value in B2 and the new value in C2: percent change is `=(C2-B2)/B2`, formatted as a percentage. A list price from a discounted price in B2 is `=B2/(1-12%)`. The `monthly` sheet of `numbers_practice.xlsx` calculates every month's percent change this way.

---

## 3. Ch 4 §4.4 "Spreadsheet link" box (and the sentence that pointed to it)

**Destination:** Ch 10 §10.7 or Ch 11 §11.3, as above (includes `RRI` and `AVERAGE`). Visual finding

**Landed** in Ch 10 §10.8, "Back to Chapter 4" (Part 2/3 build).
V4.11 applies when it is placed: put each formula on its own line as a code block.

Sentence removed from §4.4 (replaced by the plain-words explanation of a root, fix instruction 4.3):

> "The eleventh root" sounds hard. You won't do it by hand; any calculator with a power key does it as `2.17 ^ (1/11)`, and the spreadsheet functions are below.

The box:

> **Spreadsheet link.** Compound growth in both Excel and Google Sheets: `=(end/start)^(1/periods)-1`, or the built-in `=RRI(periods, start, end)`. `=RRI(3, 4335471, 6000000)` returns 0.1144, and `=RRI(11, 202640, 439824)` returns 0.0730. The plain average of monthly changes is `=AVERAGE(F3:F13)` on the `monthly` sheet, which returns the misleading 0.1307.

Also removed from the Common mistakes table (row "Averaging growth rates that compound", Fix column): the words ", or `RRI`".

---

## 4. Ch 4 §4.5 "Spreadsheet link" box

**Destination:** Ch 10 §10.7 or Ch 11 §11.3, as above (includes `AVERAGE`, `MEDIAN`, `COUNTIF`,

**Landed** in Ch 10 §10.8, "Back to Chapter 4", except the weighted average with `SUMPRODUCT` (Ch 11 §11.2) and `MODE` (Ch 11 §11.3, "Back to Chapter 4: the rest of the numbers") (Part 2/3 build).
`SUMPRODUCT`).

> **Spreadsheet link.** `=AVERAGE(B2:B174)` and `=MEDIAN(B2:B174)` on the `orders` sheet give ₹25,061 and ₹21,375; `=COUNTIF(B2:B174,">"&E1)` counts the 70 orders above the mean. A weighted average is `=SUMPRODUCT(values, weights)/SUM(weights)`, which is how the `discounts` sheet gets 4.69%. The functions have the same names in Excel and Google Sheets.

---

## 5. Ch 4 "Tools" section, spreadsheet and workbook bullets

**Destination:** Ch 10 (the workbook's introduction, fix instruction 4.2).

**Landed** in Ch 10 §10.0 and the Chapter at a glance box (Part 2/3 build).

> - **A spreadsheet** (optional). Excel and Google Sheets both have every function used here: `AVERAGE`, `MEDIAN`, `MODE`, `SUMPRODUCT`, `ROUND`, `COUNTIF`, and `RRI`. Chapter 10 teaches them from the beginning.
> - **The companion workbook** `numbers_practice.xlsx` (Appendix E). Its `monthly`, `orders`, `discounts`, and `segments` sheets hold the 2025 numbers from this chapter with the formulas already in place, so you can check every figure and try your own. It was generated from the one-year database, and its formulas were recalculated and compared with this chapter's numbers.

---

## 6. Ch 5 §5.4 "SQL link" box

**Destination:** Ch 12's worked examples, as "The March issue tree from Chapter 5, now as queries"

**Landed** in Ch 12 §12.15, Question 5's introduction (Part 2/3 build).
(fix instruction 5.1).

> **SQL link.** Every number in this walk-through is a short query on the mini database (Chapter 12); Chapter 13's month-over-month and customer patterns do the same at scale.
