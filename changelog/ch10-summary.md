# Chapter 10 summary: Spreadsheet Fundamentals (Part 2 build)

**What changed.** The chapter now starts at the keyboard: a new §10.0 gets a free spreadsheet running (Google Sheets, Excel for the web or desktop), proves it with one explained formula (`=ROUND(A1,0)` → 3, then 2.4 → 2), and opens both practice workbooks. Formulas and functions are no longer used before they are taught: a short primer opens §10.3, the §10.4 import checks are in words until §10.7 gives the formulas, Flash Fill's formula version is built cell by cell in §10.9, TIME is introduced with its arguments, MAXIFS moved after the segment column exists, the November SUMIFS is built one pair at a time, and the lookup demo uses XLOOKUP. Old §10.7 (about 20 functions) is split into §10.7 "Totals, counts, and rounding" and §10.8 "Decisions and conditions", so old §10.8–10.15 are now §10.9–10.16. §10.8 ends with "Back to Chapter 4", which redoes Chapter 4's averages, percentages, compound growth (with `^` and `RRI`) and significant figures on `numbers_practice.xlsx`. Wrong counts fixed (125 wrong dates, not 135). References to "Chapter 13's" revenue now point to Chapter 4. The four SQL/pandas preview boxes are gone. All five figures were redrawn at ≥ 7.25 pt with ✓/✗ marks, so their meaning isn't carried by colour alone. Rupees are in lakh grouping.

**Numbers.** 33 content findings and 7 open visual findings for Ch 10 were applied. RJ-S2-9 was not applied (it needs the unapproved story calendar). RJ-S2-6 needs no change in Ch 10.

**Option picks.** No finding marks a recommended option, so option (a) was used each time: 10.8 (formulas deferred to §10.7), 10.11 (move MAXIFS), 10.16 (keep the Orders column, with a note), 10.26 (add `0005` as Cell detective A8), 10.28 (a note under the table).

**Skipped or partial.**
- RJ-S2-9: left `Open`. The story's date needs the fact sheet.
- 10.21: applied as a conditional Tool note. Microsoft's page on Excel-for-the-web Power Query licensing could only be seen in search results (the proxy blocks it), so this is a question.
- 10.20: the moved content belongs in Ch 12 and Ch 18. It is listed for the integrator.
- 10.2(d): the weighted average (SUMPRODUCT) and MODE stay for Ch 11. They are listed for the integrator.

**Time needed.** Was 14–17 h over two weeks; now 18–22 h over two to three weeks, as finding 10.22 asked. This is honest after the new §10.0, the Chapter 4 block, the cell-by-cell examples and a new exercise. It fits a plan of 10 sittings of about 2 hours, which is now printed in the glance box. The Ch 6 hours table and the Ch 9/83 totals need the new figure (T12, final pass).

**Code verification.** There is no SQL or Python in the chapter. Every new or changed formula result (about 90 of them) was computed in LibreOffice 24.2 by `checks/ch10_formula_tests_v3.py` on the regenerated companion workbooks and `numbers_practice.xlsx`, and no result was typed by hand. There are no mismatches. XLOOKUP cannot run in LibreOffice 24.2, so it was checked through the equivalent INDEX/MATCH and pandas. The date-damage counts (125/10/195) and the rounded months (₹43,35,473) were rechecked in Python. `check_code_teaching.py`: 39 blocks, 0 flagged. `restructure.py --check`: in order. `fig_check.py`: 0 figures under 7 pt. Build: 55 pages. `layout_check`: clean. `prescan`: no draft labels, tofu 0.
