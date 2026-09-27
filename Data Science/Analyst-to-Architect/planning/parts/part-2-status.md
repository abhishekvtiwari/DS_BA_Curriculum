# Part II — The Analyst — status

Chat: Part II-A (Chapters 10, 11, 14–24). Chapters 12 and 13 were written in the coordinator chat. Follows `planning/chapter-writing-instructions.md` §14.1.

**Coordinator merge, 19 September 2026.** The Part II-A bundle (Ch 10, 11, 14–24) was received and merged, and the two SQL chapters written in the coordinator chat (Ch 12, 13) were added, so the Part II file set is now complete for every chapter written so far. Still unwritten: Ch 25 (The Business Analyst Track), Ch 26, Ch 27. Renumbering to the reading order below happens at final assembly, not now.

### Reading order for Part II (decided 17 September 2026)

Chapters keep their current numbers while writing. The teaching order is: **10 → 11 → 19 → 12 → 13 → 17 → 18 → 14 → 15 → 16 → 20 → 21 → 22 → 23 → 24**, so that each tool is learned end to end (spreadsheets with their automation, then SQL, then Python) before the cross-tool chapters.

## Chapters

| ID | No. | Title | Status | Words | Manuscript |
|---|---|---|---|---|---|
| P2-10 | 10 | Spreadsheet Fundamentals: Excel & Google Sheets | **Approved v2 (16 Sep 2026)** | 18,914 (incl. answers) | `manuscript/ch10-spreadsheet-fundamentals-excel-and-google-sheets.md` |
| P2-11 | 11 | The Spreadsheet, Mastered: Excel & Google Sheets | **Approved v2 (17 Sep 2026)** | 26,030 (incl. answers) | `manuscript/ch11-the-spreadsheet-mastered-excel-and-google-sheets.md` |
| P2-12 | 12 | Databases & SQL Foundations | **v3 approved (16 Sep 2026); v4 awaiting review** (adds §12.13 "Building and changing a database", exercises 23–29) | ~30,000 (incl. answers) | `manuscript/ch12-databases-and-sql-foundations.md` |
| P2-13 | 13 | SQL for Real Analysis | **Approved v1.1 (16 Sep 2026)** | ~16,500 (incl. answers) | `manuscript/ch13-sql-for-real-analysis.md` |
| P2-14 | 14 | Data Cleaning & Preparation | **Approved v1 (17 Sep 2026)** | 17,339 (incl. answers) | `manuscript/ch14-data-cleaning-and-preparation.md` |
| P2-15 | 15 | Data Visualization Principles | **Approved v1 (17 Sep 2026)** | 14,075 (incl. answers) | `manuscript/ch15-data-visualization-principles.md` |
| P2-16 | 16 | Business Intelligence with Power BI | **Approved v1 (18 Sep 2026)** | 12,143 (incl. answers) | `manuscript/ch16-business-intelligence-with-power-bi.md` |
| P2-17 | 17 | Python from Zero | **Approved v1 (18 Sep 2026)** | 10,591 (incl. answers) | `manuscript/ch17-python-from-zero.md` |
| P2-18 | 18 | Python for Analysts: pandas & Automation | **Approved v1 (18 Sep 2026)** | 10,035 (incl. answers) | `manuscript/ch18-python-for-analysts-pandas-and-automation.md` |
| P2-19 | 19 | Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script | **Approved v1 (18 Sep 2026)** | 11,452 (incl. answers) | `manuscript/ch19-spreadsheet-automation.md` |
| P2-20 | 20 | Automating Reports & Delivering Insights | **Approved v1 (18 Sep 2026)** | 9,622 (incl. answers) | `manuscript/ch20-automating-reports-and-delivering-insights.md` |
| P2-21 | 21 | Descriptive Statistics & Probability | **Approved v1 (18 Sep 2026)** | 8,574 (incl. answers) | `manuscript/ch21-descriptive-statistics-and-probability.md` |
| P2-22 | 22 | Statistics Without Fooling Yourself | **Approved v1 (18 Sep 2026)** | 8,495 (incl. answers) | `manuscript/ch22-statistics-without-fooling-yourself.md` |
| P2-23 | 23 | Business Acumen, KPIs & Metrics | **Approved v1 (18 Sep 2026)** | 10,668 (incl. answers) | `manuscript/ch23-business-acumen-kpis-and-metrics.md` |
| P2-24 | 24 | Requirements, Storytelling & Stakeholders | **Approved v1 (18 Sep 2026)** | 8,118 (incl. answers) | `manuscript/ch24-requirements-storytelling-and-stakeholders.md` |

## Chapter 24 approval

Approved by the author on 18 Sep 2026 (draft v1), at 8,118 words (against a 4,000-word brief — see the length flag below). Approved PDF: `Ch24-Requirements-Storytelling-and-Stakeholders-v1-approved.pdf`. No manual checks outstanding.

## Chapter 24 report (draft v1)

**Ownership note:** judgment-block chapter, written here at the author's request.

**Depth:** 8,118 words (incl. answers), 22-page PDF, against a brief of 4,000 words ("EXPANDED from draft Ch 9"). Given the depth of Chapters 21–23, written at judgment-block scale rather than the smaller brief figure — flag for the coordinator if 4,000 was a hard constraint. 9 numbered sections, 4 figures (stakeholder power-interest grid, the pyramid principle, one-message-per-slide before/after, a "handling pushback" decision flow), 12-row mistakes table, real-world story *The meeting that never needed to happen*, the brief's project (memo + three-slide story), timed-challenge-style practice retained as standard exercises (this chapter has no timed challenge — it's a writing/communication chapter, not a computational one), 22 exercises with worked answers.

**Sections:** 24.1 turning an ask into a question · 24.2 documenting business rules · 24.3 mapping stakeholders (power–interest grid + RACI) · 24.4 BLUF / the pyramid principle · 24.5 one message per slide · 24.6 the one-page memo · 24.7 presenting to executives · 24.8 handling "can you just change the number?" · 24.9 bringing it together (full worked arc).

**No new invented data.** This chapter is entirely built on Chapter 23's real December 2025 revenue-drop diagnosis (₹15.60cr → ₹8.73cr, −44.1%, AOV-led) as its running worked example — no new companion dataset was needed. `companion/ch24/` holds four reusable templates: a clarifying-questions bank, a blank memo template, the fully worked December memo, and a three-slide outline — all text/markdown, ready to adapt.

**Verification**
- This is a communication-skills chapter with minimal code; no Python blocks to run against a database. Every number quoted (December's fall, the three-effect decomposition, the qualified-lead counts in exercise 8: Contacted=22, Quoted=14) was independently re-checked against Chapter 23's and the real leads data.
- Style scan clean (one British-spelling fix applied); cross-references checked (Ch 14, 15, 21–23, 25, 26, 75, 76) and confirmed to exist (§23.11, §23.13).

**Manual checks needed**
1. None requiring external tools — this chapter has no code, no invented data, and no unverifiable claims beyond general communication-practice guidance (Minto's pyramid principle, standard power-interest/RACI frameworks), which are well-established and low-risk.

**Length flag for the coordinator:** brief said 4,000 words; delivered 8,118. If 4,000 is a firm constraint (e.g., for a print page budget), this needs trimming — the exercises/answers section alone is roughly 2,500 words and could move to Appendix G-only with just the questions retained in-chapter, which is already the stated plan ("In the finished book these move to Appendix G").

**Promises delivered:** none explicit from earlier chapters beyond general BA/storytelling groundwork; this chapter itself sets up Ch 25 and Ch 26.

**Promises made:** Ch 25 (requirements gathering formalized into BRD/FRD/process mapping), Ch 15 (chart rules applied to the "why" slide), Ch 26 (documentation habits for business rules), Ch 75/76 (behavioral and BA interview questions on stakeholder pushback).

## Chapter 23 approval

Approved by the author on 18 Sep 2026 (draft v1), at 10,627 words. Approved PDF: `Ch23-Business-Acumen-KPIs-and-Metrics-v1-approved.pdf`. Manual checks 1–2 remain open, including the coordinator's confirmation of the invented financial-statement assumptions.

## Chapter 23 report (draft v1)

**Ownership note:** judgment-block chapter, written here at the author's request ("Chapter 23" / "Go").

**Depth:** class B→A, 10,668 words (incl. answers), 30-page PDF, against a brief of 6,000. 13 numbered sections, 4 figures (operating cycle, P&L waterfall, KPI tree, root-cause bridge), 14-row mistakes table, real-world story *The profitable company that almost missed payroll*, the brief's project (KPI tree + diagnose a revenue dip), timed challenge (40 min, 7 levels + bonus), 27 exercises with worked answers.

**Sections:** 23.1 the operating cycle (DIO/DSO/DPO/CCC) · 23.2 the P&L · 23.3 the balance sheet · 23.4 cash flow (why profit isn't cash) · 23.5 sales metrics (real CRM pipeline data) · 23.6 marketing metrics (CAC, ROAS, attribution) · 23.7 finance metrics · 23.8 operations metrics (reuses Ch21's real delivery data) · 23.9 customer metrics (retention, LTV, LTV:CAC, NPS) · 23.10 KPI trees and the North Star · 23.11 diagnosing a change (chain-linked decomposition) · 23.12 vanity metrics, Goodhart's law, gaming · 23.13 defining a metric so two teams agree.

**What's real vs invented (please confirm with the coordinator):** revenue, COGS, gross margin, all monthly/segment/customer figures, and the real CRM pipeline (43 leads, stages New→Contacted→Quoted→Won/Lost, 60% win rate, 25.5-day cycle) come directly from the existing dataset and match every earlier chapter exactly. **New invented data**, built by `companion/ch23/build_ch23_files.py` (seed 202301) and clearly labelled throughout: the P&L below gross profit, the full balance sheet, the cash flow statement (sized to a plausible mid-size B2B distributor: EBIT margin 15.0%, net margin 10.5%, CCC 59 days), and monthly marketing spend/CAC/ROAS/NPS (blended CAC ₹8,194, ROAS ~5.6x, NPS +34). The marketing-attributed new-customer count is deliberately scaled to tie to the real 767 new-2025-customers figure so the two datasets don't visibly disagree.

**Verification**
- `tools/verify_python.py … --cwd companion/ch23`: **11 blocks run, 11 outputs checked, 0 mismatches**.
- The root-cause decomposition (section 23.11) uses real 2025 order data; the chain-linked method was checked to sum to the total change exactly with no residual.
- **A real error was caught during independent verification of the exercises**: the draft claimed May→June was among the largest revenue falls, but recomputing all 11 month-over-month changes showed November→December is actually the largest percentage fall (−44.1% vs May→June's −40.4%). Exercise 13/14, the timed-challenge Level 5/6 questions, and their answers were rewritten to use the correct Nov→Dec figures and decomposition; the worked example in the chapter body (section 23.11) still uses May→June, which is accurately described only as "a genuine, well-documented seasonal trough," never as "the largest."
- Two other data bugs were caught and fixed while building the companion data (not visible in the final chapter, noted here for the record): an internally-inconsistent balance sheet/dividend plug that implied a dividend larger than annual profit, and a ROAS calculation that compared marketing spend against total company revenue instead of attributed revenue (producing a nonsensical 150–260x ROAS). Both are fixed in the generator; final figures are the corrected ones.
- Style scan clean; cross-references checked (Ch 4, 11, 14, 16, 18, 20–22, 24, 25, 74, 76).

**Manual checks needed**
1. Whether the coordinator accepts the invented financial statements (P&L below gross profit, balance sheet, cash flow) and marketing/NPS data as canon, and the assumptions used to size them (5.2% selling & distribution, 1.8% marketing, 4.1% admin, 1.4% depreciation, 0.9% interest, 25% tax, 35% dividend payout, DSO 42/DPO 38/DIO 55).
2. Excel formula names in the Tools section (none quoted beyond generic ones — low risk).

**Promises delivered:** Ch 4 (percentages and business arithmetic, applied), Ch 14 (the "profile before diagnosing" habit, applied to money), Ch 18 (pandas throughout), Ch 20 (thresholds → now metric ownership and gaming), Ch 21 (skewed averages → CAC/LTV/AOV), Ch 22 (mix effects → Section 23.11's mix check; base rates → Goodhart's law).

**Promises made:** Ch 24 (turning a diagnosis into a memo/story), Ch 25 (process mapping/requirements as how a KPI tree gets built collaboratively), Ch 16 (KPI tree as a dashboard; shared semantic model enforces §23.13's definitions), Part IV (LTV/churn modelling), Ch 74/76 (case-study and BA question banks lean on this chapter heavily).

## Chapter 22 approval

Approved by the author on 18 Sep 2026 (draft v1), at 8,495 words. Approved PDF: `Ch22-Statistics-Without-Fooling-Yourself-v1-approved.pdf`. Manual checks 1–3 remain open, and the coordinator still needs to confirm the invented A/B and transporter datasets (SwiftLine and BlueCart).

## Chapter 22 report (draft v1)

**Ownership note:** judgment-block chapter, written here at the author's request.

**Depth:** class A, 8,495 words (incl. answers), 26-page PDF, against a brief of 5,000. 9 numbered sections, 4 figures, 18-row mistakes table, real-world story *The transporter that wasn't better*, project (audit three claims), timed challenge (40 min, 7 levels + bonus), 29 exercises with worked answers.

**Sections:** 22.1 confidence intervals (means and proportions, Wilson, what they don't mean) · 22.2 hypothesis tests and p-values (with a test-chooser table) · 22.3 A/B design (primary metric, power, sample size, randomization unit, cycles) · 22.4 peeking, multiple comparisons, p-hacking · 22.5 correlation, causation, confounders · 22.6 Simpson's paradox and standardization · 22.7 survivorship, selection, regression to the mean · 22.8 statistical vs practical significance · 22.9 writing up a result.

**New companion data (for canon):** `companion/ch22/build_ch22_files.py` (seed 202201) creates `ab_test_2026.csv` (February 2026 offer email, two subject lines, 4,200 recipients each: opens 23.50% vs 26.95%, orders 1.98% vs 2.31%, revenue per recipient ₹483.70 vs ₹530.31) and `transporters_q4_2025.csv` (11,600 Q4 deliveries, two transporters — **SwiftLine** and **BlueCart** — across Metro/Upcountry routes, containing a genuine Simpson's paradox: SwiftLine 91.1% overall vs BlueCart 79.7%, but BlueCart better on both routes). Both are stated in the chapter as invented for it. **New Riverstone facts:** two named transporters, route types, and a February 2026 email A/B test.

**Verification**
- `tools/verify_python.py … --cwd companion/ch22`: **16 blocks run, 16 outputs checked, 0 mismatches**.
- The claims that are usually asserted in textbooks are simulated here instead: peeking (3,000 simulated tests: 4.8% / 15.3% / 23.7% false winners at 1 / 5 / 20 checks), confidence-interval coverage (60 samples, 56 cover the truth), regression to the mean, and the null distributions in Figure 22.2.
- Every exercise and challenge number recomputed independently (branch Wilson intervals, MDEs — opens ≈ 2.7 points, orders ≈ 0.95 points at 4,200/variant — bootstrap median difference 1.2–1.4 days, sample sizes 13,809 for a 0.5-point order lift). Four write-up figures were corrected in that pass.
- Style scan clean; cross-references checked (Ch 4, 14, 15, 18, 21, 23–25, 27, 73).

**Manual checks needed**
1. Excel function names in the Tools section (`CONFIDENCE.T`, `CHISQ.TEST`, ToolPak items).
2. Whether the coordinator accepts the invented A/B and transporter datasets and the new named transporters.
3. `statsmodels` is recommended but not used in the verified blocks (not installed here); confirm the function names quoted (`proportions_ztest`, power calculators) at publication.

**Promises delivered:** Ch 15 (showing uncertainty), Ch 20 (thresholds and whether a move means anything), Ch 21 (standard error → intervals; base rates → test interpretation).

**Promises made:** Ch 23 (presenting uncertain results), Ch 24 (prediction intervals), Ch 25 (experimentation in practice), Ch 27 (ethics of selective reporting), Part IV (train/test, overfitting), Ch 73 (question bank).

## Chapter 21 approval

Approved by the author on 18 Sep 2026 (draft v1), at 8,561 words. Approved PDF: `Ch21-Descriptive-Statistics-and-Probability-v1-approved.pdf`. Manual checks 1–3 remain open, and the coordinator still needs to confirm the invented delivery-time data and the new lead-time facts it creates.

## Chapter 21 report (draft v1)

**Ownership note:** Chapters 21–27 (the judgment block) are not assigned to this chat in the coordinator's map; written here at the author's request ("continue").

**Depth:** class A, 8,574 words (incl. answers), 25-page PDF, against a brief of 6,000. 9 numbered sections, 4 figures, 14-row mistakes table, real-world story *The seven-day promise*, the brief's project (profile order values and delivery times), timed challenge (40 min, 7 levels + bonus), 29 exercises with worked answers.

**Sections:** 21.1 mean/median/mode (incl. the average-of-averages trap) · 21.2 spread (range, variance, sd, IQR, sample vs population, coefficient of variation) · 21.3 percentiles and service levels · 21.4 shape (skew, kurtosis, outlier rules) · 21.5 the four distributions with scipy worked examples · 21.6 probability rules and conditional probability · 21.7 Bayes' rule, explained as counts · 21.8 sampling, standard error and the central limit theorem by simulation · 21.9 a reusable `profile()` routine, turned into sentences.

**New companion data (please note for canon):** the brief's project needs delivery times, and the ERP dataset has none. `companion/ch21/build_ch21_files.py` (seed 202101) generates `delivery_times_2025.csv`: 45,040 delivered 2025 orders with order value, branch, promised days, actual delivery days and an on-time flag, from a documented lognormal-per-branch model with a festive-season penalty and 1.5% badly failed deliveries. The chapter states plainly that delivery times are invented for it. **New Riverstone facts created:** promised lead times (Mumbai HO and Bengaluru 5 days, Delhi 6, Kolkata 7); median delivery 3.2 / 3.8 / 4.4 / 5.7 days by branch; company on-time 81.8% (Mumbai HO 90.8%, Delhi 80.0%, Bengaluru 78.0%, Kolkata 68.1%); 19.9% of delivered revenue arrived late. If the coordinator prefers different lead times, changing the seed or the medians in the generator is a two-line edit, but the chapter's numbers would all move.

**Verification**
- `tools/verify_python.py … --cwd companion/ch21`: **17 blocks run, 17 outputs checked, 0 mismatches**.
- Every prose and answer figure recomputed independently (probabilities, Bayes counts, binomial and Poisson values, percentiles per branch, IQR-rule counts, standard error and sample-size arithmetic). Four answer numbers were corrected during that pass (mode ₹1,725; binomial 0.18; Poisson 0.0559; Delhi/Kolkata p90 7.2 and 10.2; late revenue share 19.9%; n = 1,329).
- Figures drawn from the same data (mean-vs-median histograms, box plots by branch with the promise marked, the four distributions, a central-limit simulation).
- Style scan clean; cross-references checked (Ch 4, 11, 13–15, 17, 18, 20, 22, 24, 73).

**Manual checks needed**
1. Excel function names and Analysis ToolPak wording in the Tools section.
2. Whether the coordinator accepts the invented delivery-time data and the new lead-time facts (see above).
3. scipy behaviour on the author's Python version (3.13/3.14); nothing version-specific is used.

**Promises delivered:** Ch 4 (averages and spread properly), Ch 14 (outliers as a statistical question), Ch 15 (the statistics behind histograms, box plots, percentiles), Ch 20 (thresholds set from a distribution).

**Promises made:** Ch 22 (confidence intervals, tests, p-values), Ch 24 (forecasting and prediction intervals), Part IV (distributions and sampling in modelling), Ch 73 (statistics question bank).

## Chapter 20 approval

Approved by the author on 18 Sep 2026 (draft v1), at 9,739 words. Approved PDF: `Ch20-Automating-Reports-and-Delivering-Insights-v1-approved.pdf`. Manual checks 1–5 remain open (sending by SMTP/Graph/Gmail, Outlook image rendering, Task Scheduler and cron, chat platform rules, low-code pricing).

## Chapter 20 report (draft v1)

**Ownership note:** as with Chapters 17–19, this chapter belongs to another Part II chat in the coordinator's map; written here at the author's request. **Part II's "all tools together" block (14, 15, 16, 20) and the Python and spreadsheet blocks are now complete in this chat.**

**Depth:** class A, 9,622 words (incl. answers), 29-page PDF, against a brief of 6,000. 14 numbered sections, 4 figures (automation ladder, report-flow map, **a screenshot of the real email the companion script produces**, trustworthiness cards), 19-row mistakes table, real-world story *The flash that stopped*, project (the Daily Sales Flash, from the brief), timed challenge (40 min, 7 levels + bonus), 27 exercises with worked answers.

**Sections:** 20.1 the automation ladder · 20.2 mapping the flow and timing the manual steps · 20.3 choosing the delivery tool · 20.4 output formats · 20.5 the report as an email (KPI tiles, chart embedding, design rules) · 20.6 sending mail safely (SMTP, Graph, Gmail, providers) · 20.7 scheduling (Task Scheduler, cron, cloud, time zones) · 20.8 alerts and exception reports (thresholds, persistence, materiality, fatigue) · 20.9 chat delivery (Teams/Slack webhooks, WhatsApp Business) · 20.10 low-code (Power Automate, n8n, Make, Zapier) · 20.11 trustworthiness (checks, logging, failure alerts, no-data, retries, idempotency) · 20.12 recipients and confidentiality · 20.13 documenting and handover · 20.14 measuring hours saved.

**Companion (`companion/ch20/`):** `daily_flash.py` — the complete Daily Sales Flash (three queries, headline calculations, exception rule, 14-day matplotlib chart, HTML builder with KPI tiles, SMTP sender, failure alert, no-data branch, logging, argparse, exit codes). Running it writes `out/daily_flash_<date>.html`, which is the artifact in Figure 20.3.

**Verification**
- `tools/verify_python.py … --cwd companion/ch20`: 9 blocks run, 8 outputs checked, 0 mismatches (the SMTP/webhook block is marked `run: none`).
- The script itself was run against the live `riverstone_full` database for 18 Dec 2025: net revenue ₹2,511,819.25 · 118 orders · 116 customers · AOV ₹21,287 · margin 27.3% · +2.3% vs 18 Dec 2024 (₹2,454,466) · month to date ₹57,069,985 (₹5.71 cr) · 1 exception (Industrial Crate, 345 units). Figure 20.3 is a real screenshot of that email.
- Trend and threshold figures checked in SQL (14-day high 7 Dec ₹3,782,009, low 9 Dec ₹2,488,217, median ₹3,209,520; at an 800-unit threshold four products flag).
- **A real bug was found and fixed while writing:** the first version computed month-to-date from the 14-day window (₹4.45 cr instead of ₹5.71 cr). The chapter now uses a separate month-to-date query and the exercise answer calls the slip out explicitly.
- Style scan clean; cross-references checked (Ch 13–16, 18–21, 23, 26, 30, 46, 47, 76).

**Manual checks needed (things that need an account someone else controls)**
1. Actually sending: SMTP settings, Microsoft Graph app registration wording, Gmail API/service accounts, and whether basic auth is still disabled by default.
2. Outlook rendering of the email (data URI vs CID images is called out in §20.5; CID is recommended for Outlook and could not be tested here).
3. Task Scheduler wording and cron behaviour on the author's machines; the `date +\%F` escaping.
4. Teams/Slack incoming webhook payloads and the current WhatsApp Business API rules (templates, consent, approved providers).
5. Low-code tool names, pricing models and connector claims at publication (Power Automate licensing, Make's per-operation pricing).

**New Riverstone facts**
- The Daily Sales Flash went live in February 2026: 07:30 IST weekdays, a service account, 14 recipients.
- On 4 March 2026 the ERP load failed at 02:10 and the Flash emailed ₹0; the fixes were checks, a no-data branch, a failure alert, and a dependency on a `load_status` row with retries until 08:30.
- On 12 May 2026 the median check held the email when a branch posted a day of orders against the wrong month.

**Promises delivered:** Ch 16 (subscriptions and alerts in context), Ch 18 (scheduling the script, HTML email, alerts, failure handling, handover), Ch 19 (choosing between VBA, Apps Script, Python and low-code; spreadsheet options covered there, not repeated here).

**Promises made:** Ch 21–22 (statistics behind thresholds), Ch 23 (the commentary sentences), Ch 26 (versioning, .env), Ch 30 (packaging and tests), Ch 46 (orchestration), Ch 47 (data-quality testing), Ch 76 (interview questions on automating and delivering a report).

## Chapter 19 approval

Approved by the author on 18 Sep 2026 (draft v1), at 11,446 words. Approved PDF: `Ch19-Spreadsheet-Automation-v1-approved.pdf`. Manual checks 1–5 remain open and matter more than usual: none of the VBA, Office Scripts or Apps Script code could be run in the writing environment.

## Chapter 19 report (draft v1)

**Ownership note:** as with Chapters 17 and 18, this chapter sits in another Part II chat in the coordinator's map; the author asked for it here.

**Depth:** class A, 11,452 words (incl. answers), 27-page PDF, against a brief of 7,000 (the coordinator's reading-order change added a from-zero programming section). 15 numbered sections, 18-row mistakes table, real-world story *The macro that ran for nine years*, two-part project (VBA consolidation + Google Forms/Apps Script workflow, both from the brief), timed challenge (45 min, 7 levels + bonus), 28 exercises with worked answers.

**Coordinator item 2 (Ch 19 before the Python block): done.** §19.4 teaches programming from zero in VBA — variables and types (incl. the `Integer`/`Long` trap), `If`, `Select Case`, all three loops, arrays, `Scripting.Dictionary`, `Sub`/`Function`, arguments, `ByVal`/`ByRef`, `Const` — with no dependence on Ch 17 or 18. §19.14 shows the same job in VBA, Office Scripts and Apps Script side by side.

**Sections:** 19.1 when spreadsheet automation is right (+ file types, macro security, trusted locations) · 19.2 recording and rewriting · 19.3 the VBA editor · 19.4 programming from zero · 19.5 the object model · 19.6 the everyday toolkit (consolidate a folder, clean via dictionary, pivot, PDF) · 19.7 Outlook email with an HTML body · 19.8 UDFs and forms · 19.9 debugging and error handling · 19.10 making macros fast (arrays, ScreenUpdating) · 19.11 Office Scripts + Power Automate · 19.12 Sheets and Apps Script · 19.13 triggers, MailApp, UrlFetchApp, quotas · 19.14 three languages side by side · 19.15 living with macros responsibly.

**Companion (`companion/ch19/`):** `build_ch19_files.py` builds `branch_files/` — twelve workbooks (4 branch sales offices × Oct/Nov/Dec 2025, from Ch 14's clean truth) plus `_notes.txt`; `expected_results.md` (per-file rows and revenue, and the totals a correct macro must produce); `enquiries_sample.csv`; and the chapter's code extracted to `vba/ch19_modules.bas`, `office_scripts/ch19_office_scripts.ts`, `apps_script/ch19_apps_script.gs`.

**Verification — read this one carefully**
- **No code in this chapter could be executed here:** VBA, Office Scripts and Apps Script need Excel/Microsoft 365/Google accounts. The code was written and reviewed by hand only.
- **What was verified:** the data and every number quoted. The twelve workbooks were generated with pandas/openpyxl from Chapter 14's clean Q4 truth, and `expected_results.md` was computed from the same source: 25,832 data rows (25,833 with header), 24,738 non-cancelled, ₹423,872,808.00; by branch Mumbai HO ₹151,058,519.25 · Bengaluru ₹117,726,527.00 · Delhi ₹102,966,828.00 · Kolkata ₹52,120,933.75; by month Oct ₹180,620,103.00 (42.6% of the quarter) · Nov ₹155,985,902.00 · Dec ₹87,266,803.75; all-status total ₹442,577,334.00. Exercise and challenge answers use these.
- The chapter says this plainly in the Tools section, so readers know the yardstick is the data, not the macros.
- Style scan clean; cross-references checked (Ch 11, 14–20, 26, 46, 70).

**Manual checks needed (high, because nothing ran)**
1. Run every VBA procedure in Excel for Windows against `branch_files/` and confirm the totals above; check `ExportAsFixedFormat`, the pivot code, and the Outlook block on a current build.
2. Menu paths and current wording: Developer tab, Trust Center, trusted locations, Mark of the Web blocking behaviour.
3. Office Scripts availability by Microsoft 365 plan, current API names (`getRangeByIndexes`, `getFormat().getFont()`), and the Power Automate connector.
4. Apps Script: `MailApp` quotas (stated as 100/day consumer, 1,500/day Workspace), the six-minute execution limit, trigger setup wording, `PropertiesService`, and `clasp`.
5. That `Scripting.Dictionary` is available (Windows-only; Mac needs a `Collection`-based alternative) — worth a note if the author wants Mac parity.

**New Riverstone facts**
- The pre-2026 quarterly consolidation ran on `MASTER_FINAL_v7_USE_THIS.xlsm`, written in 2017 by an analyst who left in 2020: 740 lines, no `Option Explicit`, fixed 5,000-row loop, and a duplicate Kolkata November file that would have double-counted ₹18.8 million.
- Branch extracts are produced per branch per month as `Riverstone_<Branch>_<YYYY-MM>.xlsx` with a `Sales` sheet.

**Promises delivered:** Ch 6/11 (automating the spreadsheet), Ch 14 (mapping tables in a third and fourth tool), Ch 17 (this chapter now teaches its own basics, so it can precede Python).

**Promises made:** Ch 20 (scheduling, HTML email at scale, alerts, failure handling, choosing the delivery tool), Ch 26 (versioning exported modules), Ch 46 (when an automation becomes a pipeline), Ch 70 (VBA and object-model interview questions).

## Chapter 18 approval

Approved by the author on 18 Sep 2026 (draft v1), at 10,035 words. Approved PDF: `Ch18-Python-for-Analysts-v1-approved.pdf`. Manual checks 1–4 remain open (Python 3.13/3.14 + latest pandas behaviour, MySQL connection string, the live API pattern, `tabulate` for `to_markdown()`).

## Chapter 18 report (draft v1)

**Ownership note:** as with Chapter 17, this chapter belongs to another Part II chat in the coordinator's map; the author asked for it here on 18 Sep 2026.

**Depth:** class A, 10,035 words (incl. answers), 36-page PDF, against a brief of 8,000. 16 numbered sections, no figures (the chapter's "figures" are its 42 verified code blocks and their real output), 17-row mistakes table, real-world story *The report that ran itself*, project (automate the monthly report, database → checks → Excel → Markdown), timed challenge (40 min, 7 levels + bonus), 30 exercises with worked answers.

**Sections:** 18.1 DataFrames, Series, vectorized thinking · 18.2 reading from anywhere (CSV/Excel/JSON/Parquet/SQL/API) · 18.3 profiling · 18.4 selecting and filtering (loc/iloc, chained assignment) · 18.5 creating columns (.str, .dt, map, np.where, cut, when to avoid apply) · 18.6 groupby and transform · 18.7 merge and concat (match rates, fan-out) · 18.8 pivot_table and melt · 18.9 dates, resample, rolling, shift · 18.10 Chapter 14's cleaning pipeline in pandas, reconciled to ₹423,561,010.50 · 18.11 matplotlib and seaborn with a reusable style function · 18.12 formatted multi-sheet Excel with xlsxwriter, read back and checked · 18.13 SQLAlchemy, bound parameters, to_sql, where work belongs · 18.14 APIs with requests (live call marked `run: none`; parsing runs offline from a saved payload) · 18.15 the whole automation as one script (written, run, output shown) · 18.16 performance, habits, and when to stop using pandas.

**Companion (`companion/ch18/`):** `build_ch18_files.py`, `api_response.json`, `report_template.md`; the chapter writes `monthly_report.py`, `reports/riverstone_2025-12.{xlsx,md}`, three PNG charts and `riverstone_monthly.xlsx` when run. It also reads `companion/full/`, `companion/ch14/orders_q4_2025_export.csv` and `companion/ch17/sales_exports/`.

**Verification**
- `tools/verify_python.py … --cwd companion/ch18`: **42 blocks run, 42 outputs checked, 0 mismatches**, run repeatedly. Two blocks were rewritten to remove non-determinism (timing numbers moved into prose; the generated-at line filtered out of the printed report).
- The database section runs against real PostgreSQL 16.15 through SQLAlchemy 2.0.54 + psycopg 3.3.5 (a `book` login role was created for it; the chapter shows that connection string).
- The Excel section writes a workbook and reads it back, proving sheet names, header row and totals.
- The cleaning section reproduces Chapter 14's ₹423,561,010.50 exactly; every headline (2025 ₹1,146,641,651.25, 46,356 orders, 4,599 customers, AOV ₹24,735.56, December ₹87,266,803.75 from 4,047 orders) matches Chapters 15–16.
- Style scan clean; cross-references checked (Ch 1, 2, 11–17, 19–21, 26, 30, 46, 47, 72).

**Manual checks needed**
1. Behaviour on Python 3.13/3.14 with the latest pandas: the chapter states pandas 3.0.2 and notes pandas 3's stricter chained-assignment behaviour.
2. MySQL connection string and driver (`mysql+mysqlconnector`), which could not be exercised here.
3. The live API block (marked `run: none`) — the pattern, not a real endpoint.
4. `to_markdown()` needs `tabulate`; confirm it is in the install list for readers who use the script's Markdown output.

**Promises delivered:** Ch 6 (Python/Jupyter as the analyst toolkit), Ch 11 (spreadsheet ideas in code), Ch 14 (the cleaning pipeline in a third tool), Ch 15 (chart rules in a style function), Ch 16 (where the work belongs: SQL vs pandas vs BI), Ch 17 (loops give way to vectorized work).

**Promises made:** Ch 19 (when work stays in the spreadsheet), Ch 20 (scheduling, email, alerts, handover), Ch 21–22 (statistics with pandas), Ch 26 (Git, .env), Ch 30 (modules, tests, type hints), Ch 46 (orchestration), Ch 47 (data-quality testing), Part IV (modelling from a DataFrame), Ch 72 (question bank).

**Length note:** 10,035 words against a 13,000–16,000 plan. Every planned section is covered and every claim is a verified run; the chapter is dense with code rather than prose. If the author wants it longer, the additions would be: more `groupby`/window patterns (ABC analysis, cohorts, retention), a fuller seaborn gallery, a testing section, and a worked DuckDB/Polars comparison.

## Chapter 17 approval

Approved by the author on 18 Sep 2026 (draft v1), at 10,444 words. Approved PDF: `Ch17-Python-from-Zero-v1-approved.pdf`. Manual checks 1–4 remain open (installer wording, VS Code menus, behaviour on Python 3.13/3.14, formatter recommendation).

## Chapter 17 report (draft v1)

**Ownership note for the coordinator:** Chapters 17–20 are not assigned to this Part II-A chat; the author asked for Chapter 17 here on 18 Sep 2026, so it was written in this chat to the same standard and workflow. Chapters 18–20 remain unwritten.

**Depth:** class A, 10,591 words (incl. answers), 36-page PDF, against a brief of 6,000 words — a true from-zero programming chapter needs the room, and the author approved the larger size in the plan. 15 numbered sections, 3 figures, 18-row mistakes table, real-world story *The fifteen-minute rescue*, project (summarize a folder of exports), timed challenge (40 min, 7 levels + bonus), 30 exercises with worked answers.

**Sections:** 17.1 what a program is and when to use one · 17.2 installing Python, VS Code, Jupyter (with a troubleshooting table) · 17.3 virtual environments and pip · 17.4 first Python (REPL, script, f-strings) · 17.5 variables and types (incl. float approximation) · 17.6 lists and tuples · 17.7 dictionaries and sets (+ which collection to use) · 17.8 conditions · 17.9 loops and comprehensions · 17.10 functions · 17.11 files and folders (pathlib, text, CSV, JSON) · 17.12 errors, tracebacks, try/except, debugging · 17.13 standard library and packages · 17.14 notebook → script (argparse-style arguments, `__main__`, logging, PEP 8) · 17.15 getting unstuck (including using AI assistants responsibly).

**Companion (`companion/ch17/`):** `build_ch17_files.py` builds `sales_exports/` (12 monthly CSVs of the 24 key accounts' 2025 order lines, 330 lines, plus a README.txt so folder code must filter), `products.json`, `targets_2025.csv` (the key accounts' own targets, ₹4,240,000), and `broken_export.csv` (March plus one unreadable row). The chapter's own code writes `summarize_exports.py`, `scratch.txt`, `month_summary.csv`, and `price_list.json` when run.

**Verification**
- `tools/verify_python.py manuscript/ch17-python-from-zero.md --cwd companion/ch17`: **38 blocks run, 38 outputs checked, 0 mismatches**, run twice to catch anything non-deterministic (one set-printing block was rewritten with `sorted()` for that reason).
- Every exercise and challenge answer computed from the companion files while writing (330 lines, 326 non-cancelled, ₹4,335,471.00 — the same total as Chapters 10, 11, and 13; October highest at ₹681,070.75; 6 of 12 months beat target; year attainment 102.3%).
- Style scan clean; cross-references checked (Ch 2, 6, 10–14, 16, 18–21, 26, 30, 72).

**Manual checks needed**
1. Python 3.13/3.14 installer wording and the "Add python.exe to PATH" checkbox; `brew install python@3.13`; the apt package names.
2. VS Code menu names (Python: Select Interpreter, the Jupyter extension, F5/F10 debugging, breakpoints).
3. That every code block behaves the same on 3.13/3.14 as on the 3.12 used here (nothing version-specific is used; error message wording can vary slightly, and the chapter says so).
4. `ruff`/`black` as the current formatter recommendation, and the PEP 8 line-length advice against house style.

**Promises delivered:** Ch 6 (Python 3.13/3.14, VS Code, Jupyter, virtual environments explained properly; laptop needed from this chapter).

**Promises made:** Ch 18 (pandas replaces the loops; Excel, SQL, APIs, charts), Ch 19 (same ideas in VBA/Apps Script), Ch 20 (scheduling, email, logging, failure handling), Ch 21–22 (simulations), Ch 26 (Git for scripts), Ch 30 (modules, packaging, testing, type hints), Ch 72 (Python & pandas question bank).

## Chapter 16 approval

Approved by the author on 18 Sep 2026 (draft v1), at 12,157 words. Approved PDF: `Ch16-Business-Intelligence-with-Power-BI-v1-approved.pdf`. Manual checks 1–6 remain open, and none of the Power BI steps could be run here, so they need confirming in Desktop and the Service before publication.

## Chapter 16 report (draft v1)

**Depth:** class A, 12,143 words (incl. answers), 35-page PDF. 13 numbered sections, 6 figures (diagrams and a page wireframe — no screenshots, because Power BI's UI changes monthly and cannot be run here), 19-row mistakes table, real-world story *The ₹2.3 crore that vanished*, project (replace the monthly pack with a published, secured, refreshing report), timed challenge *The Q4 branch page* (45 min, 7 levels + bonus), 27 exercises with worked answers.

**Position in the new reading order:** written to be read after Ch 11 (Power Query, Data Model), Ch 13 (SQL), Ch 14 (cleaning), Ch 15 (visualization) and the Python block. It starts from clean data, applies Ch 15's design rules rather than restating them, and refers back rather than reteaching.

**Sections:** 16.1 what Power BI is and what it costs · 16.2 getting the data in (connectors, Import vs DirectQuery, query folding, where cleaning belongs) · 16.3 the model (star schema, date table, hide/rename/format) · 16.4 DAX from zero (measures vs calculated columns, the seven base measures, checking against SQL) · 16.5 CALCULATE and filter context · 16.6 time intelligence · 16.7 report page design (layout, visuals, interaction, themes, accessibility, mobile) · 16.8 worked example: the monthly pack · 16.9 publishing, refresh, gateway, sharing, version control · 16.10 row-level security (static and dynamic) · 16.11 performance and the mistakes that make numbers wrong · 16.12 Tableau, Looker Studio, Metabase/Superset · 16.13 where BI is heading (Q&A/Copilot, semantic layer, Fabric).

**Companion (`companion/ch16/`):** `measures.dax` (every measure), `date_table.dax`, `expected_measures.md` (the expected value of every measure and every figure quoted in the chapter), `ch16_checks_postgresql.sql` and `ch16_checks_mysql.sql` (run to reproduce them), `city_region.csv`, `user_region.csv` (dynamic RLS), `report_checklist.md`.

**Verification**
- `tools/verify_sql.py … --db riverstone_full`: 5 statements, 5 outputs, 0 mismatches.
- Every other number (cards, quarters, regions, segments, products, RLS totals, challenge and exercise answers) computed on `riverstone_full` in PostgreSQL 16.15 and cross-checked in MySQL 8.0.46 via the companion check scripts; all listed in `expected_measures.md`.
- Licensing facts (Pro $14, PPU $24 since 1 April 2025; Fabric F2 ≈ $263/month; F64 for free viewers; P SKUs no longer sold) checked against current sources on 18 Sep 2026 and dated in the text.
- Style scan clean; cross-references checked (Ch 11 §11.8, 13, 14 §14.3/§14.7/§14.10, 15 §15.7/§15.8, 20, 23, 26, 28, 31, 46, 70).

**Manual checks needed (nothing in this chapter could be run: Power BI needs Windows and a Microsoft account)**
1. Every click path and menu name in Desktop (Get data, Transform Data, Mark as date table, Manage roles, View as, Performance analyzer, Themes, Mobile layout, Alt text, Edit interactions, drill-through, tooltip pages, bookmarks).
2. That the DAX in `measures.dax` compiles and returns the expected values in `expected_measures.md`, including `Overview Title`, `Top Customer`, `Revenue FYTD`, and `Last Refreshed`.
3. Service steps: publish, data source credentials, refresh limits (8/day Pro, 48/day PPU), gateway modes, apps, subscriptions, usage metrics, deployment pipelines, `.pbip` project format.
4. RLS behavior as described (workspace contributors bypass RLS; exports and subscriptions honor it; Test as role).
5. Current licence prices and Fabric SKU thresholds at publication, plus the PostgreSQL (Npgsql) and MySQL (Connector/NET) connector requirements.
6. Incremental refresh requirements (RangeStart/RangeEnd, folding) and Auto date/time model-size effect.

**Length note:** the plan said 14,000–17,000 words; the draft is 12,143. The chapter covers every planned section, but it describes UI steps in words instead of screenshots, and leans on Ch 14 and Ch 15 rather than repeating them. If the author wants it at the upper end, the natural additions are more DAX patterns (segmentation with a banding table, basket/co-purchase, ABC analysis), a longer worked drill-through page, and a deeper Fabric/dataflows section.

**New Riverstone facts**
- Riverstone's first Power BI report was published in February 2026; the monthly pack is no longer assembled by hand.
- Regional managers and the Sales Head open the report in the Service; RLS gives Pooja Desai West + East, Arjun Nair South, Sandeep Gill North, Anita Rao everything.
- The report carries an "About this report" page with sources, exclusions (cancelled orders: 1,956 orders worth ₹49,241,854 in 2025), row counts, and a refresh timestamp.

**Promises delivered:** Ch 6/8 (the BI chapter; Desktop is Windows-only; the browser version can't build models), Ch 11 (from Power Pivot/DAX in Excel to a full model), Ch 14 (Power Query pipeline feeding a model, scheduled refresh), Ch 15 (dashboard design, visuals, themes, tooltips, layout).

**Promises made:** Ch 20 (subscriptions, alerts, scheduled delivery, presenting), Ch 23 (storytelling), Ch 28 (star schemas and warehouse modelling), Ch 31 (define measures once, upstream), Ch 46 (orchestration), Ch 70 (DAX and filter-context interview questions).

## Coordinator update: new Part II reading order (17 Sep 2026)

Read and applied. Blocks: A spreadsheets (10, 11, old 19) · B SQL (12, 13) · C Python (17, 18) · D all tools (14, 15, 16, 20) · E judgment (21–27). File numbers stay as they are until the coordinator's renumbering pass.

- **Chapter 14 v1.2 and Chapter 15 v1.1:** each now carries one line in its Python section saying where Python and pandas (and matplotlib/seaborn) are taught, so readers of the current draft aren't lost. No other change; all numbers and outputs unchanged. Approved PDFs rebuilt.
- **Chapter 16 (Power BI), to be written:** now read after Chapter 14 (cleaning), Chapter 15 (visualization), Chapter 11 (Power Query and the Data Model), and the Python block. The plan therefore assumes a cleaned table and visualization principles, refers back to the Chapter 14 pipeline instead of reteaching cleaning, applies Chapter 15's chart choice, color, and titles to report design rather than restating them, and can use the Chapter 15 chart data and pandas where useful. Depth: class A, 14,000–17,000 words. Sections as reported in the plan sent to the author on 17 Sep 2026.
- **East coverage (issue 3, part):** named in `DATA_SPEC.md` — Pooja Desai (RSM West) also covers East (Kolkata) until a fourth RSM is hired. Documentation only; no data change. The two-channel split (Key Accounts team vs regional sales) is still with the author; if chosen, regional orders' `sales_rep_id` needs remapping away from employees 3–5 (revenue unchanged) and Chapter 15's rep figure, project chart D, text, and exercise 22 need updating.

### For the coordinator: old Chapter 19 (spreadsheet automation), not owned by this chat

Now that it precedes the Python block, its brief needs: its own programming basics taught from zero inside the chapter (variables and data types, `If`/`Select Case`, `For`/`Do` loops, arrays or collections, functions and arguments, and debugging with breakpoints, the Immediate window, and `Debug.Print`), in VBA first with the same ideas shown in Office Scripts (TypeScript) and Apps Script (JavaScript); no dependence on Chapter 17 or 18; and a note that Python automation of spreadsheets comes later in the Python block. Expect +2,000–3,000 words for the programming-basics section.

## Coordinator changes (17 Sep 2026, cross-part issues)

- **Issue 1 and 2 (names):** full-dataset employees 9 and 10 renamed Kavitha Reddy (was Kavya Reddy) and Irfan Sheikh (was Imran Sheikh) in `companion/generate_riverstone_full.py`; full dataset, Chapter 14 exports, and Chapter 15 chart data regenerated. Verified: orders, order_items, customers, sales_targets, the CRM export, and `answer_key.json` byte-identical; the order export and chart data identical apart from the two names. No manuscript printed either name. Chapter 15 figures 15.11 and 15.15 regenerated (legends). Databases updated.
- **Issue 4 (one ERP):** Chapter 14 now says one ERP with four branch sales offices whose data entry differs (Kolkata via a spreadsheet upload after migration from an older billing system; Delhi cartons; Mumbai HO and Bengaluru paste prices as text); new paragraph in §14.1 "The data for this chapter"; generator comments updated. Approved PDF rebuilt (v1.1).
- **Issue 3 (sales organization):** awaiting author decision; not implemented. See the note in the chat report: the generator currently assigns Neha Kulkarni, Rahul Mehta, and Farah Khan (employees 3–5) as reps for many regional customers, and Chapter 15 shows Rahul Mehta as the top rep by revenue. If the two-channel structure is chosen, rep assignments for customers 25+ need remapping (revenue unchanged) and Chapter 15's rep figures, text, and answers need updating.

## Chapter 15 approval

Approved by the author on 17 Sep 2026 (draft v1). Approved PDF: `Ch15-Data-Visualization-Principles-v1.1-approved.pdf` (v1.1: pointer to the Python block in §15.14). Manual checks 1–4 remain open for the author to confirm before publication.

## Chapter 15 report (draft v1)

**Depth:** expanded from the brief's 4,000 words to 14,075 (incl. answers), in line with Chapters 10–14 (author said "ch 15" after the plan proposed 12,000–15,000). 14 numbered sections, 16 figures (13 charts from the full dataset, a chart chooser, and the project's before/after sets), 21-row mistakes table, real-world story *The October that looked like a collapse*, project (redesign five charts from the old management pack, with one set of redesigns in the answers), 25 exercises with worked answers. PDF 40 pages.

**Data:** full dataset only (`riverstone_full`). New companion: `companion/ch15/build_ch15_data.py` (reads `companion/full/*.parquet`) → `ch15_chart_data.xlsx` + `chart_data/*.csv` (14 tables incl. Anscombe's quartet). Figures: `figures/make_figs15.py` (matplotlib 3.10.8, SVG) and `figures/make_figs15_diagrams.py`.

**Verification**
- `tools/verify_sql.py … --db riverstone_full`: 5 statements, 5 outputs, 0 mismatches. MySQL median query in answer 21 run on MySQL 8.0.46 (Hospitality 19,122 · Retail 19,425 · Wholesale 25,763; the ₹1 difference from PostgreSQL's 25,762 is rounding of an exact .50 median, checked).
- `tools/verify_python.py … --cwd companion/ch15`: 2 blocks, 2 outputs, 0 mismatches.
- Every number in text, titles, story, and answers computed from the chart data or SQL during writing: segment shares, 2025 monthly attainment (98.3% year; Oct 92.1%, Feb 112.3%), Oct 2025 ₹180,620,103 vs Oct 2024 ₹147,221,566 (+22.7%), Oct target +33% over Oct 2024, Q4 2025 ₹423.9m (+21.8%, 94.7% of ₹447.5m), order-value quartiles by segment, histogram bins, correlation 0.916, Anscombe statistics, bridge (+₹243,626,176; Retail 46.2%), region/month extremes, city-missing share 2.0%, contrast ratios (#c0662b 4.06:1, #1d2330 15.73:1).
- Style scan clean (American spelling); figures in reading order; cross-references checked (Ch 1, 4 §4.7, 10, 11, 13 §13.2, 14 §14.3/§14.6, 16, 18, 20, 21, 22, 70, 76).

**Manual checks needed**
1. Excel menu paths: Insert Statistic Chart (Histogram, Box and Whisker, bin width, quartile method), Insert Waterfall… (Set as total), Maps → Filled Map, Sparklines, Save as Template, Recommended Charts → Templates, Edit Alt Text, Review → Check Accessibility, dynamic chart title from a cell.
2. Google Sheets: Chart editor options (Data labels, Gridlines and ticks, Histogram bucket size, Waterfall subtotals, Format data point, Geo chart, ⋮ → Alt text, Copy chart), no native box plot.
3. Research facts as stated: Cleveland & McGill (1984) ranking; color vision deficiency about 1 in 12 men and 1 in 200 women; WCAG 4.5:1 text and 3:1 large text/graphics; Tufte data-ink (1983); Okabe–Ito palette; Anscombe (1973).
4. External tools named as examples (Coblis, WebAIM contrast checker, ColorBrewer) still available.

**New Riverstone facts**
- Riverstone builds festive inventory from July for the October peak; the stock plan is set in the first week of January.
- Old monthly management pack contained: attainment columns on a 90–115% axis, an exploded product pie, a dual-axis revenue/margin chart, region columns from ₹13 crore, a stacked area by rep, and clustered region-by-month columns.
- Story (January 2026): Suresh Menon proposed a 15% cut in festive stock; Meera's redesign kept the plan; Vikram Singh required action titles and prior-year comparison in every attainment chart.

**Promises delivered**
- Ch 1: bar chart for categories, histogram for continuous amounts (§15.2 levels of measurement, §15.5).
- Ch 4: chart choice and design in depth; honest charts, axes, and §4.7's tricks (§15.12).
- Ch 14: box plots and histograms for outliers; data-quality gaps shown clearly (§15.5, §15.13).

**Promises made**
- Ch 16 (dashboard design, visuals, page layout in Power BI), Ch 18 (matplotlib/seaborn, reusable styles), Ch 20 (charts in automated reports, presenting findings), Ch 21 (statistics behind histograms, box plots, percentiles, correlation, uncertainty bands), Ch 22 (correlation vs causation, showing uncertainty), Ch 70 ("critique this chart"), Ch 76 (presenting findings).

## Chapter 14 approval

Approved by the author on 17 Sep 2026 (draft v1). Approved PDF: `Ch14-Data-Cleaning-and-Preparation-v1.2-approved.pdf` (v1.1: one-ERP wording, coordinator issue 4, and two profiling queries given a deterministic ORDER BY; v1.2: pointer to the Python block in §14.13). Manual checks 1–5 remain open for the author to confirm before publication.

## Chapter 14 report (draft v1)

**Depth:** class A. 13 numbered sections, 4 figures, 20-row mistakes table, real-world story *The branch league table* (a quick pivot on the messy export put Delhi ahead of Bengaluru and understated Q4 by ₹33.0 million), project (clean the export + one-page data-quality report), timed challenge *The CRM clean-up sprint* (40 min, 8 levels), 30 exercises with worked answers. PDF 49 pages. 17,339 words.

**Data:** the full dataset (`companion/full/`, registered above) and the Chapter 14 messy exports built from it.

**Data spec: Chapter 14 messy exports (registered 17 Sep 2026)**
- Generator `companion/ch14/build_ch14_files.py` (seed 20251014; reads `companion/full/*.parquet`).
- `orders_q4_2025_export.csv`: 25,976 rows (+ header) = 25,832 true Q4 2025 order lines + 137 duplicate rows + 6 repeated headers + 1 footer. Planted: dates DD-MM-YYYY / YYYY-MM-DD (all Kolkata, 3,210) / DD/MM/YYYY (1,800) / Excel serial (40) / impossible (9); codes without leading zeros (Kolkata; 533 lines fail to match); discounts as fractions (1,362, Kolkata); quantities in cartons of 10 (141, Delhi); typed extra zero (6); blank quantity (14); blank product (8); prices as currency text (2,300: `Rs. 430`, `₹1,400.00`; Mumbai HO and Bengaluru); 18 status spellings (3,100 lines); 17 branch spellings (1,400); trailing spaces in sales_rep (875 lines); entry timestamps in UTC with 1,598 lines on a different IST date (43 in a different month).
- `customers_crm_export.csv`: 5,027 records; 48 duplicate records (name variants); city old names/case/space variants (700) and missing tokens (100: text NULL 24, N/A 22, - 20, unknown 19, blank 15); 12 segment spellings; 58 emails without @, 150 blank; 400 DD/MM/YYYY signup dates; 5 signup dates in 2060–2065.
- `answer_key.json` (every count), `clean_truth_orders_q4_2025.csv` (the correct clean table), starter `city_map.csv` / `status_map.csv`.
- SQL: `sql/ch14_load_postgresql.sql`, `sql/ch14_clean_postgresql.sql`, `sql/ch14_load_mysql.sql`, `sql/ch14_clean_mysql.sql` (staging tables, 4 mapping tables, `clean_order_lines`, `dq_order_issues`, `clean_customers` in `riverstone_full`). Power Query: `clean_orders.pq`. pandas: `clean_orders_pandas.py`.
- Truth values: true Q4 non-cancelled net revenue ₹423,872,808.00; clean excluding 20 quarantined lines ₹423,561,010.50; quarantined true value ₹311,797.50.

**Verification**
- `checks/ch14_compare_clean.py`: the PostgreSQL, MySQL, and pandas pipelines each produce 25,832 lines matching the truth in every column (order, date, code, product, quantity except quarantined, price, discount, status, rep, branch); revenue difference fully explained.
- `tools/verify_sql.py manuscript/ch14-data-cleaning-and-preparation.md --db riverstone_full`: 39 statements run, 33 outputs checked (PostgreSQL and MySQL blocks), 0 mismatches. (Fragments without output print expected parse notes.)
- `tools/verify_python.py … --cwd companion/ch14`: 5 blocks, 5 outputs, 0 mismatches (Python 3.12, pandas 3.0.2).
- Customer duplicates: 48 match-key groups all in `companion/full/_answer_key_duplicate_customers.csv` (0 false matches); name+city finds 46.
- All other quoted numbers (challenge answers, story league table, exercise answers) computed with SQL on `riverstone_full` during writing.
- Style scan clean; figures in order; cross-references checked (Ch 1, 10–13, 15, 16, 18, 20, 21, 26, 47, 71, 76; §1.10, 10.3, 10.4, 10.11, 11.6, 11.7, 11.10, 12.16, 13.8).
- Tested on PostgreSQL 16.15 (pg_trgm), MySQL 8.0.46, Python 3.12, pandas 3.0.2.

**Manual checks needed**
1. Power Query pipeline `clean_orders.pq` in Excel for Windows (Record.FieldOrDefault with numeric-text field names, DateTimeZone.FromText on `…Z`, Text.TrimStart with ₹); expected: 25,832 rows, 37 issues, ₹423,561,010.50.
2. Power Query column profiling menu names and "entire data set" switch; fuzzy merge option names (similarity threshold, transformation table; Jaccard).
3. Excel `REGEXREPLACE` availability in current Microsoft 365; filter list 10,000-item limit.
4. Google Sheets helper-column formulas in §14.11.
5. MySQL: LOAD DATA settings on a fresh install (local_infile), `CONVERT_TZ` with offsets.

**New Riverstone facts**
- Riverstone has one ERP. Orders come from four **branch sales offices** (Mumbai HO, Bengaluru, Delhi, Kolkata; sales offices, not plants or warehouses) that enter data differently: Kolkata was migrated from an older billing system and loads orders through a spreadsheet upload (ISO dates, codes without leading zeros, fractional discounts); Delhi enters some quantities in cartons of 10; Mumbai HO and Bengaluru paste prices as text. Entry timestamps are stored in UTC. *(Revised 17 Sep 2026, cross-part issue 4.)*
- Branch mapping: West → Mumbai HO, South → Bengaluru, North → Delhi, East → Kolkata; New Delhi is treated as Delhi.
- Q4 2025 clean net revenue by branch (excluding cancelled and 20 quarantined lines): Mumbai HO ₹150,854,187; Bengaluru ₹117,619,062; Delhi ₹102,966,828; Kolkata ₹52,120,934.
- Story: 6 January 2026 quarterly review; Sandeep Gill (North) and Arjun Nair (South); Meera Iyer rebuilt the league table and sent the cleaning log to the ERP team.

**Promises delivered**
- Ch 1: fixes §1.10's problems at scale (six dimensions, Mumbai/Bombay, placeholders, future dates, invalid emails, duplicates).
- Ch 12: messy text (TRIM, case, typos) at scale; "where it doesn't, the data needs fixing".
- Ch 13: duplicates, missing values, messy text beyond Patterns 3 and 10; clean in a separate table, never the source.
- Ch 11 v2 / DATA_SPEC: first use of the full dataset.

**Promises made**
- Ch 15 (box plots/histograms for outliers), Ch 16 (Power Query to data model with refresh), Ch 18 (pandas cleaning, fuzzy libraries), Ch 20 (validation as first step, alerts), Ch 21 (IQR, z-scores), Ch 26 (cleaning log in version control), Ch 47 (dbt tests, Great Expectations), Ch 71/76 (messy-dataset interview questions); Part IV (imputation).

## Data spec: full Riverstone sales dataset (registered 17 Sep 2026)

- **Generator:** `companion/generate_riverstone_full.py` (seed 20230101; reads `generate_riverstone_2025.py`, seed 20251). **Spec:** `companion/full/DATA_SPEC.md`. **Checks:** `checks/full_dataset_checks.py` — 14/14 pass on PostgreSQL 16.15 and MySQL 8.0.46 (key accounts' 2025 orders and lines identical to `riverstone_2025`; customers/products/employees/leads unchanged; no orphan keys; all orders have lines, fall in 2023–2025 and on/after signup; yearly aggregates identical in both engines).
- **Size:** 5,027 customers (incl. 48 planted duplicate records), 16 employees, 116,194 orders, 209,006 order lines, 36 monthly targets. Formats: CSV, Parquet, PostgreSQL and MySQL setup scripts (`riverstone_full`), `sales_lines` view in both.
- **Key numbers:** net revenue 2023 ₹613,833,108 · 2024 ₹903,015,475 · 2025 ₹1,146,641,651; targets achieved 98.8% / 100.8% / 98.3%; gross margin 21.1% / 24.7% / 27.5%.
- **Unavoidable differences (for the coordinator):** company totals and `sales_targets` differ from the one-year database (which describes the 24 key accounts; their 2025 revenue ₹4,335,471 is kept exactly inside the full data); order IDs aren't in date order across the table (key accounts keep 10001–10175, generated orders start at 200001); unit costs constant across years (margins rise because prices do); no invoices/payments (mini only); mini database remains a separate 2026 world.
- **New Riverstone facts:** employees 6–16 — Arjun Nair (Regional Sales Manager, South), Pooja Desai (RSM West), Sandeep Gill (RSM North), and sales executives Kavitha Reddy, Irfan Sheikh, Meenal Joshi, Rohit Verma, Divya Menon, Aakash Jain, Simran Kaur, Tarun Bose; list prices were 92% (2023) and 96% (2024) of today's; Riverstone sells in 39 cities in four regions; ~4,979 customer businesses by end of 2025.

## Chapter 11 approval

Approved by the author on 17 Sep 2026 (draft v2). Approved PDF: `Ch11-The-Spreadsheet-Mastered-Excel-and-Google-Sheets-v2-approved.pdf`. Manual checks 1–20 remain open for the author to confirm in Excel and Google Sheets before publication.

## Chapter 11 v2 changes (author: go much deeper on formulas and Power Query; add a World Championship-style guided exercise)

**Structure now:** 14 sections. New: 11.2 Conditional aggregation in depth (SUMIF/SUMIFS, COUNTIF(S), AVERAGEIF(S), MAXIFS/MINIFS, criteria cookbook, OR logic, SUMPRODUCT, averages by line/order/customer, weekly patterns); 11.3 The everyday function toolkit (IF/IFS/SWITCH/CHOOSE/IFNA; TEXTBEFORE/TEXTAFTER/TEXTSPLIT/TEXTJOIN/SEARCH/EXACT; EDATE/WORKDAY.INTL/NETWORKDAYS.INTL/WEEKNUM/ISOWEEKNUM/DATEDIF; LARGE/SMALL/RANK.EQ/PERCENTILE/MODE/rounding; IS functions). Expanded: 11.4 lookups (XMATCH, multi-criteria, wildcard, case-sensitive, whole row/column, last match in any version, INDIRECT/OFFSET); 11.5 pivots (GETPIVOTDATA in depth, more Show Values As, calculated fields, number bands, report filter pages); 11.6 dynamic arrays (TAKE/DROP/CHOOSECOLS/VSTACK/HSTACK/TOCOL, LAMBDA, MAP/BYROW/BYCOL/SCAN/REDUCE); 11.7 Power Query in depth (column profiling, conditional columns, column from examples, Group By with several aggregations, fuzzy merge, broken-file handling with `pq_practice/`, M basics). New 11.14 Competition-style Excel: MEWC format, how strong players work, the guided 30-minute case **The Riverstone Stockroom** (parse text codes → daily inventory model → data-table search), sanity checks, business lesson, plus the timed practice case **Riverstone Rewards** (45 min, answers in the chapter). Exercises 29–43 added (formula drills + timed case), with worked answers. 8 figures (new: 11.1 SUMIFS anatomy, 11.7 Stockroom model, 11.8 policy chart). PDF 63 pages.

**Note on how v2 was produced:** the workspace already contained an unreviewed expansion of sections 11.2–11.7, the Stockroom case and its checks from an earlier attempt at this request (not visible in this chat). I kept it after verifying it (below), removed a second unverified case ("Bhiwandi", new January 2026 data), added section 11.14, the Rewards case, Figure 11.8, drills and answers, and updated the front and end matter.

**Verification (v2)**
- `checks/ch11_formula_deep_tests.py` and `checks/ch11_formula_tests_v2.py`: classic formulas from 11.2–11.4 evaluated in LibreOffice (INDIRECT on the messy workbook, SUMPRODUCT, AGGREGATE, RANK, WORKDAY.INTL, DATEDIF, etc.) — results match the text. Known LibreOffice differences noted in the scripts (WEEKNUM type 1 for 29 Dec 2025 is 53 in Excel).
- `checks/ch11_modern_tests.py`: XMATCH, XLOOKUP wildcard/multi-criteria, LET, TEXTSPLIT, SCAN, REDUCE, BYROW, LAMBDA, TOCOL, GETPIVOTDATA-equivalents via the `formulas` engine and pandas.
- `checks/ch11_expected_v2.py`: pandas recomputation of drill answers (OR totals, wildcard, averages per line/order, weighted discount, distinct customers, ranks, recency buckets, Group By).
- Automated cross-check: every multi-digit number in sections 11.2–11.7 compared with the test outputs; the only unmatched values were version numbers and band labels, plus three derived values confirmed by hand (142 = 106 + 36; 40–49,999 band 9 lines ₹421,035; 50k+ band 3 lines ₹159,740).
- Stockroom case: `checks/ch11_challenge_sim.py` (pandas simulation) and `checks/ch11_challenge_lo.py` (the classic-formula solution workbook recalculated in LibreOffice for every level) agree: L1 9,475 / product 101 / customer 0012 (250); L2 2025-02-28, −1,785; L3 8 POs, −45 on 2025-10-03; L4 7 days, ROP 150; L5 ROP 50 / Q 150 / ₹84,840; bonus (L=14) ₹112,125. Walkthrough formulas MATCH(TRUE,INDEX(…<0,0),0) and the SUMPRODUCT grid locator also tested in LibreOffice.
- Rewards case: `checks/ch11_rewards_case.py` (pandas) and `challenge/riverstone_rewards_solution.xlsx` recalculated in LibreOffice agree on all 12 answers (0 formula errors).
- Style scan clean; figures in order; section cross-references checked against the 14 headings.

**Sources checked (17 Sep 2026), competitive Excel**
- MEWC rules: https://excel-esports.com/rules/ ; UK rules: https://excel-esports.uk/rules/
- Format descriptions: https://www.howtogeek.com/microsoft-excel-world-championship-new-favorite-esport/ ; https://esports-news.co.uk/2025/12/04/microsoft-excel-world-championship-2025-explainer/ ; https://en.wikipedia.org/wiki/Financial_Modeling_World_Cup
- The Stockroom and Rewards cases are original; no competition case content is reproduced.

**Additional manual checks (v2)**
15. Section 11.2–11.3 Microsoft 365-only functions: TEXTBEFORE/TEXTAFTER/TEXTSPLIT, XMATCH, TAKE/DROP/CHOOSECOLS/VSTACK/HSTACK/TOCOL, LAMBDA/MAP/BYROW/SCAN/REDUCE; Sheets equivalents and Named functions.
16. GETPIVOTDATA with source field name ("net_revenue") vs "Sum of net_revenue"; #REF! when item hidden; Report Filter Pages path.
17. Power Query: column profiling "entire data set" switch; Column From Examples; Group By Advanced; fuzzy merge options; broken-file handling on `pq_practice/sales_export_with_problems.csv`.
18. Stockroom case in Excel: open `challenge/riverstone_stockroom_solution.xlsx`, set Parameters, confirm Results; build the 9×16 Data Table on the Parameters sheet and confirm ₹84,840 at ROP 50 / Q 150 (and ₹112,125 with L = 14); TEXTSPLIT result pieces.
19. Rewards case: open `challenge/riverstone_rewards_solution.xlsx` in Excel and Google Sheets; Answers sheet matches answer 43.
20. The LET/TOCOL "list every winning combination" formula in 11.14.

**New Riverstone facts (v2):** none beyond v1 (the cases use 2025 data only; reorder costs, lead times, and the rewards scheme are case assumptions, not company policy).

## Chapter 11 report (draft v1)

**Depth:** class A. 11 numbered sections, 5 figures, 18-row mistakes table, real-world story *The month-end pack that was almost right* (audit of a copy-paste workbook with four planted errors), project (rebuild so next month is one refresh), 28 exercises with worked answers, one Interview extra point. PDF: 40 pages. 14,929 words.

**Data used:** the one-year 2025 data (seed 20251): 330 lines, 326 valid, ₹4,335,471, target ₹4,240,000, gross margin ₹1,137,221 (26.2%). Totals match Chapters 10 and 13.

**Files**
- `manuscript/ch11-the-spreadsheet-mastered-excel-and-google-sheets.md`
- `figures/make_figs11.py` → `fig11-1` … `fig11-5` (rendered and checked by eye)
- `companion/ch11/build_ch11_files.py` → `ch11_practice.xlsx`, `monthly_exports/sales_2025_01..12.csv`, `month_end_pack_2025_messy.xlsx`, `riverstone_sales.pq`, `riverstone_measures.dax`
- `checks/ch11_expected.py` (pandas: pivots, distinct counts, lookups, rebate bands, FILTER/UNIQUE/GROUPBY results, Power Query row counts and refresh test, unpivot, DAX measures incl. YTD, Goal Seek, data table, messy-workbook error effects)
- `checks/ch11_formula_tests.py` (15 classic formulas evaluated in LibreOffice: INDEX/MATCH exact and approximate, VLOOKUP approximate, SUMIFS grids, gross margin, LOOKUP last match, distinct count via SUMPRODUCT, what-if arithmetic) — all match

**Verification**
- All quoted numbers recomputed in pandas; classic formulas evaluated in LibreOffice; messy workbook recalculated in LibreOffice (Summary total ₹4,270,875, 100.7%; month differences +24,800 Apr, −136,023 Oct, +72 Nov, +46,555 Dec).
- Features that can't run here (XLOOKUP, dynamic arrays, GROUPBY/PIVOTBY, pivot tables, slicers, Power Query, Power Pivot/DAX, Goal Seek, Data Table, QUERY, ARRAYFORMULA, IMPORTRANGE, Connected Sheets): expected results computed independently in pandas; steps listed under manual checks.
- Style scan clean (banned words, em dashes, British spellings). Figures in order. Cross-references checked (Ch 10, 12, 13, 14, 16, 18, 19, 20, 24, 26, 49, 70; §10.4, 10.7, 10.10).
- Tested on: Python 3.12, pandas 3.0.2, openpyxl 3.1.5, LibreOffice 24.2.7.

**Sources checked (17 Sep 2026)**
- GROUPBY: https://support.microsoft.com/en-us/Excel/functions/groupby-function ; PIVOTBY: https://support.microsoft.com/en-US/excel/functions/pivotby-function ; Insider announcement: https://techcommunity.microsoft.com/blog/microsoft365insiderblog/new-aggregation-functions-in-excel-groupby-and-pivotby/4222707
- Power Pivot availability / not on Mac: https://support.microsoft.com/en-us/office/where-is-power-pivot-aa64e217-4b6e-410b-8337-20b87e1c2a4b ; https://learn.microsoft.com/en-us/answers/questions/5537966/why-isn-t-there-an-option-for-power-pivot-and-load
- Connected Sheets limits (500k rows / 10 MB extracts): https://support.google.com/docs/answer/9703214 ; https://docs.cloud.google.com/bigquery/docs/connected-sheets

**Manual checks needed (author, in Excel for Windows / Mac and Google Sheets)**
1. XLOOKUP examples in §11.2 (multi-column return, search_mode −1, match_mode −1 band, nested two-way) in Excel 365 and Sheets.
2. Pivot steps both apps: status filter, Distinct Count via Data Model, COUNTUNIQUE, Show Values As % of Grand Total and Difference From (previous) — June −142,430.75, date grouping (Excel Group; Sheets "Create pivot date group"), Top 3 value filter, slicers/timeline, Sheets slicer menu.
3. Dynamic arrays: SORT(UNIQUE()) = 23 names; SUMIFS with F2#; SORTBY; FILTER Excel and Sheets syntax (15 rows, ₹343,685.50); #CALC! on empty FILTER; SEQUENCE dates; LET result 0.262; Sheets blocked-array #REF! message.
4. GROUPBY/PIVOTBY argument positions (filter as 7th / 10th argument) and availability wording.
5. Power Query: From Folder → Combine & Transform; automatic Changed Type strips zeros; Using Locale English (India) for dd-mm-yyyy; merge dialog "matches 326 of 326"; unpivot; parameters; Query Options type-detection setting path; paste `riverstone_sales.pq` into a Blank Query (en-IN culture in TransformColumnTypes).
6. Refresh test: remove December file → ₹3,895,647.50, Q4 ₹1,314,478.75.
7. Power Pivot: COM add-in path; Design → Date Table → New; Diagram View relationships; Add Measure dialog; measures in `riverstone_measures.dax` give ₹4,335,471, GM ₹1,137,221 / 26.2%, YTD Jun ₹1,460,879.75, Sep ₹2,581,168.75 (month order in pivot).
8. Goal Seek path (Data → Forecast → What-If Analysis) → 87.79; Google "Goal Seek" add-on existence and menu.
9. Data Table dialog (row input B3, column input B2) and "Automatic Except for Data Tables".
10. Sheets QUERY examples (group by/order by/label; pivot L gives Q1–Q4 columns); IMPORTRANGE Allow access; Col-number syntax; VSTACK in both apps.
11. Connected Sheets menu (Data → Data connectors → Connect to BigQuery); Excel Get Data → From Database / From ODBC.
12. Auditing tools: Workbook Statistics, Edit Links/Workbook Links, Inquire availability, Sheets "View → Hidden sheets".
13. §11.9 comparison table (REGEX functions, Python in Excel, Stocks data type, Microsoft Forms link).
14. Open `month_end_pack_2025_messy.xlsx` in Excel: Summary total ₹4,270,875; Go To Special → Constants selects only B14.

**New Riverstone facts (for the coordinator)**
- The ERP also produces one sales export per month (`sales_2025_MM.csv`, same layout as the annual export).
- A copy-paste month-end pack existed for 2025 (Vikram's); Meera rebuilt it with Power Query in January 2026; Anita used the corrected figure in the board pack.
- Illustrative annual volume rebate bands: from ₹0 Standard 0%, ₹250,000 Silver 1%, ₹400,000 Gold 2% (2025: 2 Gold, 6 Silver, 15 Standard; total ₹37,642.03). Flag if this conflicts with Part 0 or later chapters' pricing rules.
- Home Plus placed no orders in 2025 (already true in the data).
- Both cancelled 2025 orders were Retail (10034 April, City Needs Store; 10131 October, Festive Gifts Co).

**Promises delivered**
- Ch 12: pivot Rows/Values ↔ GROUP BY/aggregate (§11.3, Fig 11.2); five-column CASE report ↔ pivot (§11.3 SQL link).
- Ch 10: lookups in depth incl. INDEX/MATCH (§11.2); import as one Refresh (§11.5); QUERY/IMPORTRANGE (§11.8); #SPILL! (§11.4); converting app-only features and alternatives (§11.9).

**Promises made to other chapters**
- Ch 14: full 3-year dataset for SAMEPERIODLASTYEAR; messy data at scale in Power Query/SQL/pandas.
- Ch 16: CALCULATE in depth, filter context, star schema, Power BI scheduled refresh, Looker Studio reading Sheets.
- Ch 18: pandas merge/groupby/pivot_table as equivalents.
- Ch 19: steps Power Query can't do (PDF, email); Apps Script as a Power Query alternative.
- Ch 20: scheduling refresh (Power Automate).
- Ch 24: handling "can you just change the number?" (answer 27).
- Ch 49: data warehouses. Ch 70: pivot/XLOOKUP/Power Query/DAX interview tasks.

## Chapter 10 approval

Approved by the author on 16 Sep 2026 (draft v2). Approved PDF: `Ch10-Spreadsheet-Fundamentals-Excel-and-Google-Sheets-v2-approved.pdf`. The manual checks listed below remain open for the author to confirm in Excel and Google Sheets before publication.

## Chapter 10 v2 changes (author: "misses a few basic things")

Added without renumbering sections: creating, opening, saving, file formats and naming (§10.1); status bar quick totals, inserting/deleting/resizing/hiding rows and columns, sheet management, copy vs cut, paste special, find and replace, undo (§10.2); filling a series, Flash Fill and Smart Fill, Text to Columns / Split text to columns, cell styling and Format Painter, Center Across Selection, times as fractions of a day (§10.5); AutoSum and Insert Function, error values table, named ranges, Trace Precedents / Evaluate Formula, Manual calculation trap (§10.6); MEDIAN, ROUNDUP/ROUNDDOWN/INT, MAXIFS/MINIFS (§10.7); FIND, CONCAT (§10.8); Remove Duplicates, grouping (§10.10); printing and saving as PDF (§10.14, retitled). Shortcut table, mistakes table (+5 rows), checklist, recap, key terms updated. Exercises now 29 (new: error matching, remove duplicates + status bar, print to PDF), renumbered with answers. PDF: 49 pages.

New formulas verified by `checks/ch10_formula_tests_v2.py` (LibreOffice): SUM/AVERAGE/COUNT 4,398,121 / 13,327.64 / 330; named range SUM 4,398,121; MEDIAN 10,212.5; MAXIFS Retail 49,875; ROUNDUP/ROUNDDOWN/INT 32,100 / 32,000 / 32,062; error values #DIV/0!, #VALUE!, #NAME?, #N/A; TIME difference 8.25 h; first/last name split; CONCAT RS-10001; 175 unique order IDs (155 duplicates removed).

Additional manual checks (v2): Mac shortcuts added (Cmd+Shift+T AutoSum, Ctrl+Shift+= / Cmd+- insert/delete, Cmd+= recalc, Ctrl+E Flash Fill); Sheets Smart Fill Ctrl+Shift+Y; Sheets group rows menu path; Sheets print "Repeat frozen rows"; Sheets Remove duplicates dialog wording; Excel status bar right-click options.

## Chapter 10 report (draft v1)

**Depth:** class A. 15 numbered sections, 5 figures, 16-row mistakes table, real-world story *Meera's two Januaries*, project (monthly sales tracker), 26 exercises with worked answers, one Interview extra point. PDF: 41 pages.

**Data used:** the one-year 2025 data from `companion/generate_riverstone_2025.py` (seed 20251), exported as an order-line CSV. Totals match Chapter 13: 330 lines, 175 orders (173 non-cancelled), net revenue ₹4,335,471, 102.3% of target. The full three-year dataset wasn't needed for Chapter 10; it will be built before Chapter 14.

**Files**

- `manuscript/ch10-spreadsheet-fundamentals-excel-and-google-sheets.md`
- `figures/make_figs10.py` → `fig10-1` … `fig10-5` (rendered to PNG and checked by eye)
- `companion/ch10/build_ch10_files.py` → `riverstone_sales_export_2025.csv`, `ch10_practice.xlsx`, `ch10_tracker_solution.xlsx`, `ch10_tracker_check.xlsx` (generated files: regenerate rather than store in the project)
- `checks/ch10_check.py` (pandas recomputation of every quoted number), `checks/ch10_formula_tests.py` (51 formulas from the text evaluated in LibreOffice)

**Verification**

- Every number in prose recomputed in pandas: pass.
- 51 classic formulas evaluated by LibreOffice 24.2 on the chapter data: all results match the text.
- Tracker workbook (INDEX/MATCH twin of the XLOOKUP solution) recalculated in LibreOffice: monthly revenue, orders, reps, and segments match pandas; check row difference 0; 0 formula errors.
- CSV damage measured by importing the CSV in LibreOffice with month-first vs day-first column types: 125 wrong real dates plus 10 right by luck, 195 left as text, 330 codes lost their zeros; damaged January ₹91,649.
- Style scan: no banned words, no em dashes in prose, no British spellings. Figures numbered in order of appearance. Cross-references checked against the chapter map (Ch 1, 2, 3, 11–15, 18, 19, 24, 26, 69, 70; §1.10, 2.1, 2.9, 12.9, 12.13).
- No SQL or Python code blocks in this chapter, so `verify_sql.py` and `verify_python.py` don't apply.
- Tested on: Python 3.12, pandas 3.0.2, openpyxl 3.1.5, LibreOffice 24.2.7.

**Sources checked (16 Sep 2026)**

- Excel automatic data conversion: https://support.microsoft.com/en-us/excel/set-automatic-data-conversions and https://support.microsoft.com/en-US/Excel/data-import-and-analysis-options-in-excel
- Excel leading zeros and 15-digit precision: https://support.microsoft.com/en-us/office/keeping-leading-zeros-and-large-numbers-1bf7b935-36e1-4985-842f-5dfa51f85fe7
- Google Sheets tables: https://support.google.com/docs/answer/14239833, https://support.google.com/docs/answer/15637642, https://workspaceupdates.googleblog.com/2024/05/tables-in-google-sheets.html
- Google Sheets 10 million cell limit: https://support.google.com/drive/answer/37603
- Sheets import option "Convert text to numbers, dates, and formulas": third-party help pages only (Loyverse, Ecwid); confirm in the app.

**Manual checks needed (author, in Excel and Google Sheets)**

1. `XLOOKUP` results in §10.9 and `ch10_tracker_solution.xlsx` (Excel 365 and Sheets): row 2 → Patel Kitchenware; no "not found".
2. Excel: **Data → From Text/CSV → Transform Data → Change Type → Using Locale** with English (India) reads `02-01-2025` as 2 January 2025; wording of the "Do not detect data types" option.
3. Excel: **File → Options → Data → Automatic Data Conversion** path in the current build (older builds: Advanced).
4. Sheets: with locale India and conversion on, importing reads `02-01-2025` (dashes) as 2 January 2025.
5. Sheets: **Format → Convert to table** shortcut Ctrl+Alt+T; `=SUM(Sales[net_revenue])` = 4,398,121.
6. Excel table calculated-column syntax (`[@quantity]`) and Total Row.
7. Combo chart steps in both apps (§10.12).
8. Sheets data validation: "Is between", "Reject the input", custom whole-number formula.
9. Sheets viewers creating temporary filter views (answer 24); Excel for the web viewers filtering without saving.
10. Keyboard shortcut table (§10.15), especially Mac Excel (Ctrl+U, Cmd+T, Cmd+Shift+F, Ctrl+Cmd+V) and **File → Browse Version History** on Mac.
11. §10.14 table: what happens to Excel tables and pivot tables in each direction.
12. Circular reference behavior (Excel: warning and 0; Sheets: `#REF!`).
13. Excel's Sort Warning dialog; Sheets sorting only the selection.
14. Open `ch10_tracker_solution.xlsx` in Excel and Sheets: formulas calculate, check cell `D20` = 0, conditional formatting and chart display correctly.

**New Riverstone facts (for the coordinator)**

- The ERP's sales export writes one row per order line, dates day first (DD-MM-YYYY), and customer codes zero-padded to four digits (customer 2 → `0002`).

**Promises delivered**

- Ch 1: how to check what a cell really contains (§10.3); data types in spreadsheets (§10.3, §10.5).
- Ch 2: importing CSV without losing leading zeros or breaking dates (§10.4).
- Ch 12: `XLOOKUP` fetching a customer's name from another sheet (§10.9); `IF`/`IFS` as the spreadsheet version of `CASE` (§10.7).

**Promises made to other chapters**

- Ch 11: `XLOOKUP` options and `INDEX`/`MATCH` in depth; pivot tables; Power Query refresh of the import steps; `QUERY`/`IMPORTRANGE`.
- Ch 14: mixed date patterns, messy text, validation checks at scale.
- Ch 15: chart choice, color, titles that state the finding.
- Ch 19: Google Form → Apps Script acknowledgement email.
- Ch 24: agreeing report rules ("should cancelled orders count?").
- Ch 69 / 70: reconciling out loud; spreadsheet question bank.

## Requests for the coordinator

- Chapter 10 includes a short first-lookup section so that Chapter 12's line "In Chapter 10 you used `XLOOKUP`" stays true; Chapter 11 still covers lookups in depth.
- This chat can't write to the project (read-only copies), so files are delivered as downloads for the author to upload.
- Chapter 10 is about 15,300 words against the blueprint's 6,000, in line with class A depth.


---

## Coordinator notes on the merge (19 September 2026)

### Chapters 12 and 13 added

Written in the coordinator chat before the part chats were set up; they set the depth standard the other chapters follow.

- **Ch 12 Databases & SQL Foundations.** 58 PostgreSQL outputs verified on PostgreSQL 16, 8 MySQL outputs verified; every query also run through `companion/mysql/ch12_queries_mysql.sql` with identical results except documented NULL ordering. §12.13 (v4) is a hands-on lab in a separate `riverstone_lab` database, verified by running 133 statements in order in both engines with 47 printed outputs matching. Companion: `companion/postgresql/riverstone_setup.sql`, `companion/postgresql/ch12_lab_postgresql.sql`, `companion/mysql/riverstone_setup_mysql.sql`, `ch12_queries_mysql.sql`, `ch12_lab_mysql.sql`, `companion/new_suppliers.csv`. Figures `fig12-1` … `fig12-5` (`figures/make_figs.py`).
- **Ch 13 SQL for Real Analysis.** 40 PostgreSQL outputs and 4 MySQL outputs verified; `companion/mysql/ch13_queries_mysql.sql` runs clean with matching results. Companion: `companion/postgresql/riverstone_2025_setup.sql`, `companion/mysql/riverstone_2025_setup_mysql.sql`. Figures `fig13-1` … `fig13-4` (`figures/make_figs13.py`).
- **Open item:** Ch 12 v4 has not been formally approved. The approved PDF in `pdf-out/` is v3; `Ch12-Databases-and-SQL-Foundations.pdf` is the v4 build.
- **Open item (carried from `planning/cross-part-issues.md`):** Ch 13 needs one sentence saying what the one-year `riverstone_2025` database represents now that the full dataset exists.

### Packaging checks run on the merged part

- All 71 figure references across Chapters 10–24 resolve to a file in `figures/` (one missing PNG, `fig20-3-daily-flash-email.png`, was found in the bundle and restored).
- Every companion file named in the chapters exists, with one naming mismatch: Chapter 16 refers to `ch16_checks.sql` while the companion folder holds `ch16_checks_postgresql.sql` and `ch16_checks_mysql.sql`.
- Independent style scan of all 15 chapters (excluding code blocks, tables, figure captions and the part line):

| Chapter | Em dashes in prose | Banned words | British spellings |
|---|---|---|---|
| 12 | 2 | 0 | 1 (`labelled`) |
| 16 | 0 | 0 | 6 (`modelling`) |
| 18 | 2 | 0 | 1 (`modelling`) |
| 19 | 3 | 0 | 0 |
| 20 | 5 | 0 | 2 (`behaviour`, `colour`) |
| 21 | 12 | 0 | 7 (`centre`) |
| 22 | 4 | 0 | 6 (`behaviour`, `favour`, `modelling`) |
| 23 | 53 | 1 (`genuinely`) | 5 |
| 24 | 84 | 3 (`genuinely`) | 2 |

  Chapters 10, 11, 14, 15 and 17 are clean. These are mechanical style fixes, held for the part-completion review pass (§15.1) rather than applied now.

### Word count

Part II as written (Ch 10–24, including exercise answers): about 217,000 words across 15 chapters.
