# Chapter 70 — one-page summary

**What changed.** The chapter is now reader-facing and every formula answer is reproducible. The drafting notes in the glance box are gone; it has Before you start and Time needed. A new §70.0 prints the practice table (six Riverstone order lines, real products and list prices, a status column with one cancelled order) and explains levels and roles. Every question has a level, roles and a section-level "Learn it in" pointer checked against the current Part 2 chapters (rapid-fire tables gained a "Level · learn it in" column). Four wrong model answers were corrected ("(blank)" in pivots, the Min/Max calculated field, conditional-formatting precedence, Append = UNION ALL), along with the doubtful ones (Top-N ties, flush(), SUMIFS in ARRAYFORMULA, USERPRINCIPALNAME, REMOVEFILTERS/ALL). Every revenue answer now excludes cancelled orders. Tags follow Ch 69's twelve (`**[+Tag]**`), one move per line. The Apps Script code uses Ch 19's JavaScript, and the fast version really is equivalent to the slow one. The dashboard critiques are numbered §70.8 and have two wireframe figures. A new rapid-fire row, Q70-071, covers VBA vs Office Scripts.

**Code and numbers verified.**
- checks/ch70_lo.py (LibreOffice 24.2 headless): 12 formulas and 2 tier columns match the text. VBA ran in VBA-compatibility mode: `last row: 7`, and MarkLargeOrders writes Large in K5 only.
- checks/ch70_check.py covers what LibreOffice can't run: XLOOKUP 750 and UNIQUE(FILTER) through the `formulas` engine; QUERY (25200 / 21372.5 / 4600) and ARRAYFORMULA through pandas; and the DAX January 2025 figures in SQL (33.0%).
- checks/ch70_run_apps_script.js (Node mock): the slow and fast versions agree, including a pre-filled K cell and a header-only sheet. The broken script sends 3 then 3; the fixed one sends 3 then 0.
- No mismatches are left.
- Not run here (no Excel or Power BI): real Excel, Google Sheets, and the DAX in Power BI Desktop.
- check_code_teaching reports only "no what-if table", which doesn't apply to a question bank.

**Build.** 27 pages. layout_check is clean: map 12/12, no stranded or sparse pages, tofu 0. fig_check: 0 figures under 7 pt. restructure --check: already in order.

**Option picks.** Option (a) wherever a row offered alternatives: print the table (70.3), keep existing K values (70.24), add wireframe figures (70.34). Where option (a) would have edited a Part 2 chapter (70.16 ALLEXCEPT, 70.18 bridge tables), the in-chapter alternative was taken and the change is listed for the integrator.

**Skipped or left.**
- 70.44 is left for the D2 renumbering pass.
- 70.4 is only partly done: real Excel, Sheets and Power BI runs remain for Abhishek (the outputs come from LibreOffice, a Node mock and Ch 16's SQL-checked figures).

**Time needed.** New: 4–6 hours for a first pass, plus 1 hour for the final-week list. The chapter had no estimate before; this one comes from the review's per-question rate, about 5 minutes per core question and 1–2 per rapid-fire row across 22 core questions, 47 rapid-fire rows and 2 critiques.
