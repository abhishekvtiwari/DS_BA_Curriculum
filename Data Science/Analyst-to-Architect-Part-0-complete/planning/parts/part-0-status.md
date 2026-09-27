# Part 0 status — First Principles: Data from Zero

Written by the Part 0 chat (which is also the coordinating chat). **Part 0 is complete: Chapters 1–6 approved (17 Sep 2026).**

## Chapters

| ID | No. | Title | Status | Words | Manuscript |
|---|---|---|---|---|---|
| P0-01 | 1 | What Is Data? | Approved (v1) | ~7,950 | `manuscript/ch01-what-is-data.md` |
| P0-02 | 2 | How Computers Store, Move and Protect Data | Approved (v1) | ~9,470 | `manuscript/ch02-how-computers-store-move-protect-data.md` |
| P0-03 | 3 | How a Business Runs on Data | Approved (v1), 16 Sep 2026 | ~8,400 | `manuscript/ch03-how-a-business-runs-on-data.md` |
| P0-04 | 4 | Numbers Without Fear | Approved (v1), 16 Sep 2026 | ~8,400 | `manuscript/ch04-numbers-without-fear.md` |
| P0-05 | 5 | Thinking Like an Analyst | Approved (v1), 17 Sep 2026 | ~8,000 | `manuscript/ch05-thinking-like-an-analyst.md` |
| P0-06 | 6 | Setting Up to Learn | Approved (v1), 17 Sep 2026 | ~7,600 | `manuscript/ch06-setting-up-to-learn.md` |

## Chapter 3 report (16 Sep 2026)

- **Class C.** Blueprint 4,500 words; written at ~8,400 (counting tables and answers) because the brief adds plants, systems, and the first appearance of the manual-work thread. Same size as approved Chapters 1 and 2.
- **Files:** manuscript; `figures/make_figs03.py` (Figures 3.1 departments, 3.2 order 5001 in ten steps, 3.3 booked/billed/collected, 3.4 manual steps marked); `checks/ch03_check.py`. No companion files and no code blocks (nothing for the SQL/Python verifiers).
- **Verification:** every number recomputed from the mini database by `checks/ch03_check.py` (monthly booked/billed/collected, reconciliations, 9 KPIs, overdue by invoice, average days to collect, order 5001 lines and dates, February/March detail, discounts by order, crate margins at 0/12/15%, time estimates). Style checks: no em dashes in prose, no banned words; "cancelled" and "instalments" kept to match Chapters 12–13. Figures rendered and inspected; PDF (24 pages) checked page by page.
- **Sources checked (product names in §3.3):** TallyPrime (tallysolutions.com/tally-prime), Zoho People (zoho.com/people), Keka HR; others (SAP, Oracle NetSuite, Microsoft Dynamics 365, Odoo, Salesforce, HubSpot, Zoho CRM, Workday, Shopify, WooCommerce, Zendesk, Freshdesk, diagrams.net) are long-established names used only as examples.
- **Manual checks for the author:** none required.
- **Promises delivered:** Ch 1 and Ch 2 promises (follow one order through every system; capture once at the source; automation thread starts); Ch 12's "Before you start: Chapter 3".
- **Promises made to later chapters:** Ch 4 (percentages/averages behind the KPIs); Ch 5 (turning "why is January low?" into precise questions); Ch 10 and 12 (booked/billed/collected calculated in tools); Ch 19–20 (automate the monthly report); Ch 23 (full KPI tree for Riverstone, DSO); Ch 25 (formal order-to-cash process map, readers keep their project map for it); Ch 45 and 51 (connect ERP and CRM, send data back); Ch 49 (data warehouse); Ch 58 (AI intake of emailed purchase orders); Ch 15–16 (dashboards); Ch 75–76 (metric definition and business-process questions).

## Chapter 4 report (16 Sep 2026)

- **Class C.** Blueprint 4,500 words; written at ~8,400 (within class C's 1.5–2× guide).
- **Files:** manuscript; `figures/make_figs04.py` (4.1 rises and falls don't cancel, 4.2 average growth vs compound path, 4.3 order-value histogram with mean and median, 4.4 same margins on truncated and zero axes); `checks/ch04_check.py`; `companion/ch04/make_ch04_workbook.py`, which builds `numbers_practice.xlsx` (sheets monthly, orders, discounts, segments) from `riverstone_2025`. The workbook itself isn't saved to the project (binary); regenerate it with the script.
- **Verification:** every number recomputed from `riverstone_2025` (and the mini DB for exercise 4) by `checks/ch04_check.py`; an automated scan confirmed every number in the text is either in the check output or a stated input. Workbook formulas recalculated headlessly in LibreOffice 24.2 and read back: percent changes, margin points, % of target, `AVERAGE` of monthly changes (0.1307), compound rate and `RRI` (0.0730; 0.1144), `AVERAGE`/`MEDIAN`/`COUNTIF` on orders (25,060.53; 21,375; 70), `SUMPRODUCT` weighted discount (4.688%), rounded segment shares (sum 99). No code in the chapter (brief: Python only to check). Style checks clean.
- **Sources checked:** RRI in Excel (Microsoft Support, support.microsoft.com/en-us/office/rri-function-6f5822d8-7ef1-4233-944c-79e8172930f4) and Google Sheets (Docs Editors Help, support.google.com/docs/answer/9368238).
- **Manual checks for the author:** none required (optionally open `numbers_practice.xlsx` in Excel or Sheets; `RRI` was verified in LibreOffice).
- **Promises delivered:** Ch 1 (percentages, growth, averages), Ch 3 (math behind the §3.5 KPIs).
- **Promises made:** Ch 5 (turn one checked claim into an analyst's question; *of what / compared with what* as a method); Ch 10–11 (percentages, SUMPRODUCT, pivot shares); Ch 15 (honest charts, axes); Ch 21 (spread, percentiles, Bayes' rule); Ch 22 (is a rate difference real or chance); Ch 23 (growth rates and margins on financial statements); Ch 73 and 75 (percentage, growth, probability, guesstimate questions).
- **New Riverstone facts:** none. The ₹60 lakh 2028 goal and the board-slide draft are story scenarios only.

## Chapter 5 report (17 Sep 2026)

- **Class C.** Blueprint 3,500 words; written at ~8,000 including tables and answers (trimmed from 8,800). That's above the 1.5–2× guide; the extra is the fully worked March issue tree and the hiring story. Can be cut further if the author prefers.
- **Files:** manuscript; `figures/make_figs05.py` (5.1 vague to precise question, 5.2 hypothesis loop, 5.3 MECE bad vs good split of the 8 customers, 5.4 March issue tree with results); `checks/ch05_check.py`. No code or companion files.
- **Verification:** every number recomputed from the mini DB (March tree, balances, reorder gaps, discounts by line size, crate margin at 5% off) and the one-year DB (unique leads, never contacted, days to contact, per-rep and per-source counts, orders per rep) by `checks/ch05_check.py`; automated scan found no number in the text without a source in the check output or Chapter 3. Style checks clean; figures rendered and inspected; PDF (23 pages) checked.
- **Sources checked:** none needed (no fast-changing facts).
- **Manual checks for the author:** none.
- **Promises delivered:** Ch 3 ("why is January low?" made precise, the way Meera did); Ch 4 (project: turn a checked claim into an analyst's question; *of what / compared with what* as a method); Ch 1 §1.2's March question worked in full.
- **Promises made:** Ch 6 (tools and study plan); Ch 10–13 (tests for issue-tree branches); Ch 14 (data-quality branch); Ch 20 (daily follow-up reminder for leads); Ch 22 (is "3 of 8 vs 3 of 14" bigger than chance); Ch 23 (KPI trees, careful decomposition of a revenue change); Ch 24 (memos; handling "find numbers that support this"); Ch 26 (working with AI assistants); Ch 30–31 (experiments and causal inference); Ch 36 and 40 (predictive questions); Ch 75–76 (case and structuring questions).
- **New Riverstone facts:** none canonical. Story details (Vikram's hiring request in January 2026; Meera's recommendation) are scenario only. Note for later parts: in the 2025 data, Farah handled 64 orders, Rahul 53, Neha 46, and Neha owned 15 of 30 unique leads.

## Chapter 6 report (17 Sep 2026)

- **Class C.** Blueprint 2,500 words; written at ~7,600 including tables and answers. Longer than the 1.5–2× guide because install steps, the documentation example, the study plan, and 15 exercises are all practical; can be trimmed if the author prefers.
- **Files:** manuscript; `figures/make_figs06.py` (6.1 toolkit, 6.2 six-month plan, 6.3 weekly rhythm); `companion/ch06/check_setup.py`.
- **Verification:** `verify_sql.py` 4 statements, 4 outputs, 0 mismatches (PostgreSQL 16, MySQL 8.0.46); `verify_python.py` 1/1; `check_setup.py` run on Python 3.13.13 (pandas 3.0.5, openpyxl 3.1.5, matplotlib 3.11.2, jupyterlab 4.6.3) and on 3.11.15 with packages missing, outputs pasted; exercise 6 rounding cases (4.5) run in all tools; spreadsheet ROUND checked in LibreOffice 24.2.
- **Sources checked (17 Sep 2026):** PostgreSQL versioning policy (18.6 current, EOL Nov 2030) and Windows/macOS download pages; python.org downloads (3.14.4) and devguide versions (3.15 due 2026-10-01); Python docs "Using Python on Windows" (install manager, full installer deprecated) and "Using Python on macOS" (Install Certificates); Python venv docs (PowerShell execution policy); Python/PostgreSQL/MySQL 8.4 docs for rounding; Microsoft Learn Power BI Desktop requirements (Windows only, Store, 2 GB/4 GB RAM, 1440×900); Microsoft Q&A on Mac options; Power BI service sign-up (work or school account); Power BI Desktop product page ("for free"); Excel for the web free (5 GB OneDrive) and end of free desktop editing preview (24 Jul 2026); Microsoft ROUND docs; DBeaver download (26.2.0, 30 Aug 2026, bundles OpenJDK); VS Code requirements and Jupyter docs; Git install pages (2.55.0; macOS via xcode-select/Homebrew). MySQL 9.7 LTS from Ch 12's checked facts.
- **Manual checks for the author:** Google Sheets `=ROUND(2.5,0)` returning 3 (verified in LibreOffice and consistent with Microsoft's ROUND docs, not run in Sheets); Windows `py install 3.14` and PowerShell activation (from official docs, not run on Windows); Mac shortcut Option+Cmd+C for copying a path.
- **Promises delivered:** Ch 1 (installing everything else), Ch 3 (installs the mini database), Ch 5 (tools and study plan); Appendix B/E references kept.
- **Promises made:** Ch 7–9 (landscape, career tree, learning science behind review from memory); Ch 10–11 (desktop-only Excel features flagged); Ch 16 (Power BI; Mac options; Tableau/Looker translation); Ch 17 (virtual environments explained properly); Ch 26 (Git, AI assistants at work); Ch 34 (command line); Ch 54–55 (how AI assistants work); Ch 64 (data privacy); Ch 68, 81 (hiring, talking about learning); Appendix B (current install steps), E (download address, all files), G (answers).
- **Coordinator note:** reader setup standard added to instructions §2.
- **New Riverstone facts:** none. Story detail: Meera studies for an analyst role (scenario).

## New Riverstone facts

Registered directly in `planning/riverstone-bible-additions.md` (this chat is the coordinator): plants and warehouse, departments, systems, Suresh Menon, order 5001 history, discount approval limits, meeting rhythm, "sales" vocabulary.

## Requests for the coordinator

- Promises file regenerated after Chapter 3's approval (done, 16 Sep 2026).
