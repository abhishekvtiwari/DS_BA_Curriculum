# Parts 2 and 3: questions for Abhishek

Collected from the chapter agents' question files, in reading order. Each chapter's detailed record is in `changelog/chNN.md`; its one-page summary in `changelog/chNN-summary.md`. Integration questions are at the end.

## Chapter 10

### Questions for Abhishek

1. **Power Query in Excel for the web (10.21).** In a search on 28 Sep 2026, Microsoft Support's "Use Power Query in Excel for the Web" said the full Power Query experience needs a Business or Enterprise Microsoft 365 plan. Only the search snippet could be read, because the proxy blocks support.microsoft.com. §10.4 therefore has a conditional Tool note: "check whether Transform Data is offered; if not, use the Sheets route". §10.0 also names desktop Excel as the only route with every feature. Please confirm the licensing wording before print.
2. **RJ-S2-9 (story date).** Meera's story is still dated "the second week of January 2026". Staggering it needs the story calendar in the fact sheet, which isn't approved yet. The row stays `Open`.
3. **Status bar and formula results in lakh style.** Formula results are printed exactly as the app returns them (`4398121`), with the lakh-grouped rupee value beside them where the prose needs it (₹43,98,121). The Tool note in §10.5 now says the book uses lakh grouping, and that spreadsheets group digits the way the reader's settings say. Please confirm this split is what option 67.9 intends for a spreadsheet chapter.
4. **The desktop-Excel "free preview ended July 2026" note** (in Ch 6's parked Step 1) was not carried into §10.0. It's a dated product fact I couldn't verify, and §10.0 was meant to stay short. Add it back if you want it.

## Chapter 11

1. **Split Chapter 11? (11.1, alternative 4).** Even with the second-pass markers, the chapter is 77 pages and 35–45 hours. The review offers a split: Ch 11 "Formulas, lookups and pivots" (§11.1–11.6, 11.12) and Ch 11A "Refreshable workbooks" (§11.7–11.11, 11.13, project). I applied the main fix (new time, core/second pass, sitting plan) and did not split. Do you want the split?
2. **Story date (RJ-S2-9).** "In the real world" opens "In the first week of January 2026". The fix staggers story dates across January–April 2026, which needs the book calendar in `review/riverstone-facts.md` (not yet approved). Left Open until the fact sheet is approved.
3. **Numbers stored as text in IFS criteria (11.15).** The review says Excel/Sheets COUNTIF treat the text "101" as matching 101 "in most cases". LibreOffice counts only the number. I couldn't test Excel or Sheets here (no Windows, and Microsoft's documentation site is blocked by the proxy), so the new sentence says the behaviour "differs between apps, so don't rely on it either way". Please confirm in Excel if you want a firmer statement.
4. **Riverstone Rewards case (11.24).** The review suggests relocating the Rewards timed case to Chapter 27 (portfolio) or Chapter 70 (interview bank) with a pointer here. It now sits inside the optional Timed challenge; do you want it moved?

## Chapter 19

1. **Please run the chapter's code in the real apps before print (19.24).**
   - VBA needs Excel for Windows, Office Scripts need Excel on the web with a business plan, and Apps Script needs a Google Sheet. None of these runs here.
   - Each output in the chapter comes from a real run:
     - LibreOffice 24.2's VBA-compatibility mode on the companion files, for 14 test procedures, including the full consolidation, the 13-file failure and LogLine;
     - Node with small mocks of the Excel and Google services, for the TypeScript and JavaScript;
     - Python on the companion data.
   - Behaviour that Excel alone decides was checked against Microsoft's documentation. That covers the Dir order, the delete prompt, ByRef, Err.Raise, ChrW, Worksheet.Delete, `.Show = -1` and `getWorksheet` returning `undefined`.
   - Please check these in Excel, because LibreOffice can't run them: CleanMaster, CleanStatusFast, the Dictionary half of ArrayDemo, BuildSummaryPivot, SaveSummaryAsPdf, EmailSummary and AskForMonth/PickFolder.
   - Please also run the Apps Script in a Google Sheet. `escapeHtml` uses `String.replaceAll`, which needs the V8 runtime; that's the default for new projects, but I couldn't confirm it here.
   - When that's done, 19.24 can close.
2. **19.16 (held): the month totals.** The project, answer 12 and the Timed challenge still give October and November rounded to the rupee (₹18,06,20,103.00 and ₹15,59,85,902.00). So the three months add up to 75 paise more than the quarter. The companion's exact values are ₹18,06,20,102.75 and ₹15,59,85,901.50. The fix doesn't depend on the reading order. May I un-hold it and print the exact values?
3. **19.10 and 19.21 (held).** Their Python-based fixes don't fit a reader who hasn't met Python. Test 2 still requires every TypeScript and JavaScript line to be explained, so I added:
   - a short "Reading TypeScript when you know VBA" table in §19.11;
   - line-by-line notes under each TypeScript and JavaScript block;
   - the 0-based `Array` and 1-based range-grid explanations in §19.4 and §19.10.

   Keep these, or do you want them reworked?
4. **19.1, 19.15 and 19.35 (held).** I recommend Reject. The order-neutral part of each is done: the prerequisites are now Ch 10–11 only, the Ch 14 and Ch 17 references are gone, and the forward references to Ch 18 and 20 are correct in the approved order.
5. **The email uses Western grouping.** VBA's `Format` has no lakh grouping, so the Outlook email body shows 423,872,808.00, and the text says so. Is that acceptable? The alternative is a lakh-formatting helper function, which adds code to teach.
6. **Time needed** is now 25–30 hours over three weeks (was 20–25): VBA 13–16 h, Office Scripts and Apps Script 6–8 h, and the project about 6 h. Please confirm, for the Ch 6/9/83 tables (T12).

## Chapter 12

### Questions for Abhishek

1. **Tested versions (12.41).** The finding asked for "Tested on PostgreSQL 16–18 and MySQL 8.4 LTS / 9.7 LTS". Only PostgreSQL 16.13 and MySQL 8.0.46 were available to run, so §12.3 now says "Every query in this chapter was run on PostgreSQL 16 and MySQL 8.0, and uses only features that work the same way in the newer versions", while recommending PostgreSQL 18 and MySQL 9.7 LTS for install. Is that wording acceptable, or do you want a re-run on 18 / 9.7 before print? (It also means the chapter tells readers to avoid 8.0 while being tested on it.)
2. **MySQL 9.7 dates.** "Released in April 2026 and supported until 2034" was confirmed only through search results (GA 21 April 2026; support to April 2034); dev.mysql.com, endoflife.date and InfoQ are blocked by the proxy. Please confirm on dev.mysql.com before print. Search also shows a MySQL 26.7 Innovation release (August 2026); the chapter's "avoid Innovation releases" already covers it.
3. **MySQL manual wording (12.30).** The PostgreSQL quote was checked word for word against the PostgreSQL 18 documentation source. The MySQL *Rounding Behavior* wording was checked through search snippets only (exact values: "round half up", i.e. away from zero; approximate values: "the result depends on the C library … 'round to nearest even'"). Please check it against the 9.7 manual page 14.26.4.
4. **12.38 under D8.** "In the real world" can't move before §12.16 without breaking D8's stage order, so the fix moved the MySQL monthly report out of §12.16 and after the PostgreSQL original instead. OK?
5. **Chapter length.** The rebuilt PDF is 126 pages (was 96). Every addition comes from an approved finding, but the chapter is now the longest by far. Consider, for a later pass, the review's optional idea of boxing §12.13 Steps 10–11 as "Reference", or splitting the chapter.
6. **Chapter 7's query placement.** The parked block asked for the Chapter 7 query "next to §12.15's mini-database version"; finding 12.32 makes it exercise 30 ("predict first"). I put a "Back to Chapter 7" box next to Question 1 and the full query (both databases) in answer 30, so the exercise isn't given away. OK?

### Screenshots to take (V12, no raster images in this chapter yet)

- §12.3, box "Running your first query in DBeaver": DBeaver with an SQL editor on the `riverstone` connection, `SELECT 1;` typed, the result grid below showing one column and the value 1 (finding 12.1).
- §12.13, "Loading rows from a CSV file": DBeaver's Import Data wizard, column-mapping page, `new_suppliers.csv` mapped to `supplier_name`, `city`, `onboarded_on`, with `supplier_id` left unmapped (finding 12.27).

## Chapter 13

### Questions for Abhishek

1. **Finding 13.8, where Pattern 10 goes.** The finding splits the ten patterns into §13.7 "ranking, shares and
   clean-up" (1, 2, 3, 4, **10**) and §13.8 "over time" (5–9). Chapters 8, 20, 25, 28 and 29 cite Ch 13's patterns
   by number ("Pattern 3", "Pattern 6"), so I kept the numbers and their order, and left Pattern 10 (data-quality
   checks) at the end of §13.8, now titled "Patterns over time, and a final check". Is that acceptable, or do you
   want Pattern 10 moved into §13.7 (then either renumbered as Pattern 5, with Patterns 5–9 becoming 6–10 and every
   citation in other chapters updated, or kept as "Pattern 10" out of sequence)?
2. **Finding 13.15, upper-case email.** The finding offers two fixes: plant an upper-case email in the setup data
   (lead 21 `NovaSupermart@example.com`), or say in the text that the emails happen to be lower-case already. I
   used the sentence. Planting the email changes the shared `riverstone_2025` data, and with it any count of
   distinct emails done without `LOWER()`: Ch 23's lead figures and Ch 29's API example read the same leads. Do you
   want the planted email anyway? If so, the setup scripts (both engines), `leads.parquet` and those chapters need
   re-running together.
3. **RJ-S2-9, story dates.** The year-end board review is still "In January 2026". It moves when the book calendar
   in `review/riverstone-facts.md` is approved.

## Chapter 14

### Questions for Abhishek

1. **Story date (RJ-S2-9).** The branch league table story is dated "6 January 2026". RJ-S2-9 asks to stagger Meera's January rescues across January–April 2026, but the calendar is a proposal in the unapproved fact sheet. Left unchanged; row stays Open. Which date should Ch 14's story use?
2. **Rupees in words.** On the coordinator's request the story now says "₹1.47 crore", "₹3.3 crore" and "₹24 lakh" instead of "₹14.7 million", "₹33 million", "₹2.4 million". Please confirm crore/lakh wording (not only lakh digit grouping) is the book-wide rule, so other chapters match.
3. **Scope of finding 14.24.** It asked to make SQL the teaching path and point spreadsheet readers to §14.12. I moved the unique spreadsheet content (Power Query profiler, XLOOKUP lookup, M date parsing, the `DATE(2025,11,31)` trap, the checks sheet) into §14.12 rather than deleting it. OK?
4. **Section renumbering inside Ch 14.** Finding 14.4's pipeline section is a new numbered §14.9, so old §14.9–14.12 became §14.10–14.13 (the old §14.13, pandas, left for Ch 18). The chapter ends at §14.13 with no gap. OK?

## Chapter 15

1. **`PERCENTILE_CONT` (finding 15.4).** The finding prefers teaching `PERCENTILE_CONT` in Ch 13 as a short subsection after aggregates. That subsection would cover the median, then quartiles, then the MySQL window-function median (Ch 15's Stretch 21 would move there as the worked example). Ch 15 would then only point back to it. I couldn't edit Ch 13, so Ch 15 now uses the finding's alternative: quartiles in the spreadsheet with `QUARTILE.INC(FILTER(...))`, and the SQL as an optional box with every part explained. Do you want the Ch 13 subsection as well? If you do, the Ch 15 box can shrink to a pointer and Stretch 21 can move.
2. **Story date (RJ-S2-9).** "In the first week of January 2026" is unchanged. It waits for the approved book calendar in `review/riverstone-facts.md`.

## Chapter 16

1. **Screenshot for §16.0 (finding 16.1).** The finding asks for one screenshot of Power BI Desktop's screen, showing the views and the panes. I can't run Power BI here, so §16.0 describes the screen in words. Do you want a screenshot? If yes, please take it on Windows (see below).
2. **Exercise 3 and the work account (16.24).** The finding also asks to mark Ex 3 as "needs a work or school account". Ex 3 is a licensing question that needs no Service, so I left it unmarked. Only the project steps 7–8 and Ex 18–19 say which part needs an account. Is that OK?
3. **Figure 16.3's number.** The old figure said "Wholesale, 2025, West → ₹8.5 crore". Recomputed, it is ₹10.5 crore (₹10,50,46,469), so the figure now says ₹10.5 crore. Please confirm that nothing else relied on the old number.
4. **Story date.** "a Monday in February 2026" in the real-world story is unchanged. It waits for the book calendar in the unapproved fact sheet.
5. **Microsoft Learn was not directly readable.** The proxy blocks learn.microsoft.com. Behaviour claims were checked against search-result text of the Microsoft Learn pages, and against the microsoft.com download and pricing pages, which I fetched directly on 28 Sep 2026. Those claims cover the Store and admin rights, side-by-side installs, the work account, RLS with no role, NOW/UTCNOW, FORMAT commas, SELECTEDVALUE and TOPN. A final check in a browser before print would be prudent.

## Chapter 17

1. **Credit Ch 19's VBA (RJ-S3-10, held Open).** In reading order the reader has just done Chapter 19, so they've already met variables, `If` and loops in VBA. Should §17.1 or §17.3 say so in one sentence ("if you did Chapter 19, …; Python's are the same ideas with less ceremony")? Related: "Where this leads" still lists Chapter 19 as a next step, although the reader has already done it. I left it unchanged because it depends on the same decision.
2. **Python version wording.** §17.0 recommends Python 3.14 (3.14.7, 5 August 2026) and says 3.15, due 1 October 2026, will also work. The source is PEP 745/790, read 28 Sep 2026. If the book goes to print after October, the recommendation could become 3.15. It's one sentence in §17.0 step 2, plus the project's Tools line.
3. **One environment for the book.** §17.0 creates a single `.venv` in `analyst-to-architect/` (as old Ch 6 did), rather than one per project. Chapter 18 then installs pandas into it. Is that what you want, or should each chapter's work folder get its own environment?
4. **Meera's setup episode (parked from Ch 6).** I changed its detail from a "matplotlab" typo to "installed JupyterLab without the environment active", because Ch 17 installs only JupyterLab. Is that OK?

## Chapter 18

### Questions for Abhishek

1. **The last-year check (18.34).** The finding asks for the story's check, "within 20% of the same month last year", to be one of the script's checks. Riverstone's real 2025 growth is 20–34% a month (December +19.8%). A 20% band would fail 11 of 12 months, including October and November. I used a **50%** band and changed the story to match; its failing run, "+61.4%", still fails. Is 50% acceptable, or would you prefer a check against the month's target instead (2025 months ran at 92.1–112.3% of target)?
2. **NumPy placement (18.9).** The finding says to insert NumPy as a new §18.2 and renumber. I put it as the first subsection of §18.1, so no Ch 18 section number changes, because Ch 19, 20 and 27 cite §18.3 and §18.14. Is that fine?
3. **Chapter length.** Ch 18 is now 76 PDF pages (it was 36), and Time needed is 40–45 hours over four weeks. The growth comes from the approved moves (Ch 14 §14.13, Ch 15 §15.14, Ch 2's status codes, the NumPy page), the cell-by-cell splits, and teaching `logging`, `argparse` and `subprocess`, which Ch 17 no longer covers. Should any of it go to Ch 20 (for example the `logging`/`argparse` part of §18.15, or the whole API section)?
4. **The demonstration API.** §18.14 now uses a small local API, `companion/ch18/api_demo.py` on port 8018 with token `demo-token-18`, so every request and every page is real and works offline. The chapter says plainly that it runs on the reader's computer. Is a Ch 18 demo API acceptable next to Ch 2's `api_demo.py`, or should the two be merged into one companion API?
5. **Writing back (§18.13).** `to_sql` now practises on a SQLite file (`sqlite:///ch18_scratch.db`), not on `riverstone_full`. Readers learn that analysts usually can't write to the warehouse, and no reader can damage their practice database. Is that acceptable?

### Screenshots to take (no Excel here)

- **Ch 18, §18.12, after step 4:** the finished `riverstone_2025.xlsx` open in Excel, on the "By month" sheet. It should show the bold title in A1, the blue header row on row 3, the `#,##0` revenue column, the frozen panes (scroll down to show them), and the column chart at E4. Finding 18.29 suggested one screenshot per step; one of the finished file is enough, because steps 1–3 don't save the file until `writer.close()`.

## Chapter 20

### Questions for Abhishek

1. **Rupee grouping in program output.** Prose now uses lakh grouping (₹25,11,819), but the Flash email, its subject line
   and the tiles show Python's `,` grouping (₹2,511,819), because no finding asks to change code output. One sentence in
   §20.5 and one in the project explain the difference. Should `daily_flash.py` format money the Indian way (a small
   `lakh()` helper), so the email matches the book? It would change Figure 20.3, the subject line, and several outputs.
2. **Task Scheduler restart-on-failure (20.17).** Microsoft's schema reference says the task restarts "if the task fails
   for any reason"; community reports say a program that runs and exits non-zero does not count as a failed task. The
   chapter keeps the setting, with a hedge, and makes the script wait for its own data. Keep the hedge, or drop the
   setting from step 5 and rely only on the script?
3. **CRON_TZ (20.3).** The finding suggested `CRON_TZ=Asia/Kolkata`. It works only in cronie (Red Hat/Fedora); Ubuntu
   and Debian cron ignore it (checked in both man pages). The chapter writes the line for a UTC server (01:30 UTC) and
   mentions `CRON_TZ` as the cronie option. OK?
4. **§20.11a.** The assembled Flash is a `###` subsection at the end of §20.11, not a new numbered section, so
   §20.12–20.14 keep their numbers (Ch 63 cites 20.13 and 20.14). OK, or do you want a numbered section and a
   renumber at the final pass?
5. **Loaded rate.** §20.14 now uses the fact-sheet rate ₹300/hour (F1, listed as settled in the build brief):
   ₹97,500 a year instead of ₹3,90,000. Confirm, since it makes the "business case" modest (the text now says the
   41 days are the point).
6. **Manual minutes of the Flash.** Unchanged at 80 (the chapter's own measurement; the fact sheet's 40-minute proposal
   is not approved). No row needed it.

## Chapter 21

1. **Length.** The chapter has grown from 25 to 45 PDF pages. Most of the growth is the hand-worked §21.0, the cell-by-cell code with real outputs, and the Bayes tree. Time needed is now 20–23 h, in two halves with checkpoints. Is that acceptable for one chapter, or should the second half (§21.5–21.9, probability and sampling) become its own chapter in the renumbering pass?
2. **Ch 73 content placed in Ch 21.** Rows 73.4 (recommended option (a): the Monty Hall and birthday puzzles) and 73.13 (mutually exclusive events; expected value) put material into Ch 21. I added it here because Ch 21 is being rebuilt now. Is that all right, or should the puzzles stay in Ch 73 only?
3. **Tied mode.** The real data has two modes for order value, ₹1,725 and ₹5,800, each with 219 orders. The chapter now uses this tie to teach that the mode is fragile for money values (`MODE.SNGL` returns ₹5,800; pandas lists ₹1,725 first). Earlier chapters and the answers quoted only ₹1,725. Keep the tie as a teaching point?

## Chapter 22

### Questions for Abhishek
1. **Length.** Ch 22 grew from 26 to 53 PDF pages. That's the by-hand, spreadsheet and cell-by-cell additions the findings asked for, plus the new §22.10. Time needed is now 20–23 h. Is the Part A / Part B split (with a checkpoint after §22.4) enough, or would you rather move §22.10 into its own sitting?
2. **RJ-S2-9.** The transporter story is still dated "January 2026". I'll restage it once the Riverstone calendar is approved.

## Chapter 23

### Questions for Abhishek

1. **Finding 23.8, the quarter-end DSO table (option a).** The story now shows DSO 36 → 42, DIO 52 → 55, DPO 37 → 38 and CCC 51 → 59 at the four 2025 quarter-ends. The balances are invented (in `companion/ch23/working_capital_quarters_2025.csv`); the sales and cost figures they're divided by are real trailing-twelve-month figures. One loose end: §23.4's cash flow implies receivables of ₹12.74 crore at 31 December 2024, which on 2024's real sales (₹90.3 crore) is a DSO of about 51 days. So a reader who works out the opening figure would see DSO fall from about 51 (December 2024) to 36 (March), then climb back. Seasonally this is plausible: receivables peak after the October–November sales. The story only compares 2025's quarter-ends, so nothing in the text contradicts it. Is that acceptable, or do you want option (b), which changes §23.4's movements and recomputes CFO and the answers that use it?
2. **Finding 23.6.** I used option (a): 0.91 is renamed "liabilities-to-equity" everywhere. Should the chapter also show true debt-to-equity? Interest-bearing debt ÷ equity = (9,74,64,540 + 12,61,30,582) ÷ 37,82,25,976 = 0.59, with one line on "payables are owed but are not borrowing". That was the finding's other option. It adds a term readers will meet in Finance.
3. **CAC changed from ₹8,194 to ₹8,141** (finding 23.20, option a). The companion script had counted five customers as "active in 2024" whose only 2024 orders were cancelled, so it made new customers 767 instead of 772. I regenerated the invented marketing file so it ties to the real 772. Spend and leads are unchanged. LTV:CAC is now 26.6 (was 26.4), and naive LTV:CAC is about 79 (was 78).
4. **Story dates** ("In February 2026") are unchanged. They are fact-sheet proposals and wait for its approval.

## Chapter 24

### Questions for Abhishek
1. **Financial year.** Ch 16 teaches FY2026 = 1 April 2025 to 31 March 2026. Ch 23 labels calendar-2025 statements "FY2025", and Ch 24 said "the FY2026 plan" in January 2026. I replaced Ch 24's "FY2026" with "2026" rather than defining it. Does Riverstone report on April–March years (Ch 16) or calendar years (Ch 23)? Ch 23 needs the same answer.
2. **Finance head's title.** Ch 24 said "Finance Controller"; Ch 1's cast and Ch 3 have Suresh Menon, Finance Manager. I used "Suresh Menon, the Finance Manager" (test 5). Ch 23's real-world story still says "finance controller" (fact sheet C14). OK?
3. **Story date.** The December memo story stays in the first fortnight of January 2026, with only its weekdays fixed (24.6). If the story calendar (RJ-S2-9) moves it, the memo date (9 January 2026) in §24.6 and in companion/ch24 moves with it.

## Chapter 25

### Questions for Abhishek

1. **Vikram's title (25.18, fact sheet C17).** Ch 25 now says "Vikram Singh, the Sales Manager, who looks after the key accounts", which matches Ch 3, Ch 24 and the brief. Finding 25.18 asks for "Sales Manager (Key Accounts)" in Ch 3, 24, 25 and 27, and fact sheet C17 proposes "Sales Manager, Key Accounts" at first mention. Which form do you want? The row stays Open until you decide.
2. **Ayesha Qureshi (RJ-S3-24, fact sheet C42).** Should she be added to the Riverstone bible as a BA who came from the support desk 18 months earlier, or should the story be about Meera? If it's Meera, the story needs rewording: Meera joined as a sales coordinator, not from support. The row stays Open.
3. **Ranking hours (25.8).** The table's "~8 hours" (delivery step, warehouse) and "~6 hours" (stock) are labelled in the text as interview estimates, not data. The ~8 is the old invoicing row's number, reused for the new delivery row. The ~6 is unchanged. Are you happy for them to stand as estimates, or should they come from the fact sheet once it's approved? Applying the new score method also changed the ranking: re-keying is now first (17), then delivery (8), then stock (6). The old table ranked re-keying last with no method. Please confirm you're happy with that.
4. **Figure 25.1 removed (V25.15, option (a) "keep one").** The SDLC card figure repeated the table under it, so I kept the table and added its one extra fact as a "BA effort" column. If you'd rather keep a small figure (effort bars only, option (b)), say so.
5. **New SQL cell in §25.6.** RJ-S3-23 asks for a pointer to Ch 13 Pattern 6 and an explanation of the different multiplier. The brief also asks that every example number come from the data. So §25.6 now runs Pattern 6's rule at 2× and at 1.5× on the 24 key accounts. It adds about a page and is the chapter's only code. `check_code_teaching` flags its length (36 lines), because three of its four steps repeat Pattern 6. Is one query in this otherwise tool-free chapter acceptable?

## Chapter 26

1. **§26.0 title.** It is kept as "The terminal in 20 minutes" (Ch 20 and Ch 28 cite §26.0), and the opening says honestly that reading takes about 20 minutes, while the install and the drill need about an hour. Is that fine, or rename it "The terminal in under an hour"?
2. **Editor default.** The one-time setup uses `core.editor "code --wait"`, with nano as an alternative. The Windows installer's own default is Vim, and the chapter tells readers to switch it. OK?
3. **Parked Ch 6 exercise 2(a)** ("match `git --version` to its tool") wasn't placed: a one-item matching exercise makes no sense alone. Its intent is in Check yourself ("`git --version` prints a version"). OK to drop?
4. **Screenshots to take (new, optional):** a green and a red run of the `checks` workflow on GitHub's Actions tab (§26.8 / project step 6), and the "Compare & pull request" banner (§26.7). The text stands without them.
5. **Branch/PR example changed.** The PR walkthrough uses `add-order-count` (a real change to `monthly_revenue.sql`), not `fix-cancelled-orders`, because the `sales_lines` view already excludes cancelled orders (26.26b). The "fix-cancelled-orders" story now lives only in the PR-description example and in the story, tied to the report script that reads `orders`/`order_items` directly.

## Chapter 27

### Questions for Abhishek
1. **27.4 option.** The finding offers (A) re-run everything on merged-duplicate data or (B) keep the as-loaded numbers and record the decision. Neither is marked "recommended"; the finding argues for B ("simpler, and itself models a recorded decision"), so I applied B. Say if you want A (every figure in §27.4–27.7, the figures and answers would change: 681→674 etc.).
2. **27.1.** NTILE is taught in §27.4 (the finding's minimum alternative). If you prefer the finding's preferred route (add NTILE to Ch 13 §13.4), Ch 13 needs the cell and §27.4 can shrink to a recap.
3. **Margin trend (27.8).** 2023–2025 margin (21.1→27.5%) is computed with today's unit cost for every year, while line prices rose. I flagged it in the text as "part of that rise may be the measurement" and out of scope. Is a cost history intended for the dataset?
4. **Memo date** "12 February 2026" is left as is until the fact sheet's calendar is approved.

## Chapter 28

### Questions for Abhishek
1. **Timings re-measured on a different machine.** Every plan and timing in §28.5–28.6, §28.11, §28.13, Figures 28.3–28.4 and the real-world case now comes from a fresh run of `ch28_perf.py` (4 vCPU, 16 GB, shared with other work), because several findings needed new plans and mixing two machines would have been inconsistent. Ratios moved a little (index ~200× instead of ~380×; EXTRACT vs range ~45× instead of 35×; writes 5.5× instead of 6×). OK to keep, or re-run on a quiet machine before print?
2. **RJ-S2-15 (Open).** Ch 28's `staff` table has three regional sales managers and eight regional executives; Part 4 has three executives (Neha, Farah, Rahul). Keep Ch 28's larger sales org, or trim it to match? Depends on the fact sheet.
3. **RJ-S2-16 (Open).** The real-world case is dated "March 2026". Which month should Part 3's stories use once the fact sheet's book calendar is approved?
4. **Time needed** is now 22–30 h including the project (was 18–24 h); the chapter is 105 pages (was 82). Fine, or should the part consider splitting it (structural question 11 in the journey review)?
5. MySQL: the book's MySQL outputs are from 8.0.46; the chapter now says 8.0 left standard support in April 2026 and points to 8.4/9.7 LTS, but doesn't claim the outputs were re-run there. Re-run on 8.4 before print?

## Chapter 34

1. **Held rows touched by other tests.** 34.2 (Before you start): only the just-in-time part was applied (no "Chapter 6", no venv), and Ch 29 was not added as a prerequisite. 34.12(a): the watch-out now says to load `.env` with `set -a; . ./.env; set +a` or python-dotenv instead of the incorrect "source .env" (test 5); part (b) (Ch 29/32 `export PASSWORD` lines) was not done. 34.15, 34.19 and 34.20 are overtaken by RJ-S1-11: the Ch 29 Try-it is gone, and Why-this-matters and Where-this-leads are rewritten for the approved order. Recommend Reject for 34.15, 34.19 and 34.20 as written. OK?
2. **Title.** 34.1 suggests "The Command Line, Part 2: Text Tools, Linux & Networking". Not changed (file names, part contents, cross-refs). Change it?
3. **Parked Ch 2 Block 6 ("packet" paragraph)** is still unplaced, as instructed. It would fit §34.9 "Networking in plain English" before "Ports". Place it?
4. **Disk story numbers.** 34.17(b) was kept at 84 files by saying the job was switched on on 10 November (84 = 10 Nov–1 Feb). The 2025 files deleted, du total and df line were recomputed (52 files, 21G, 20G used / 21G free / 48%). These are fictional server outputs (the block is `run: none`, as before). OK?
5. **Practice data changed**: LF line endings (header 123 bytes, was 124 with CRLF), 644 permissions, a regenerated log (1 ERROR, 37 WARNING, 149 INFO; logger `daily_summary`), and the `daily_summary.sh` output format "order lines 7, customers 3, revenue …". All outputs were re-run.
6. **Screenshots:** none needed (no rasters in this chapter).

## Chapter 29

### Questions for Abhishek

1. **Python 3.14 for the package (29.7).** `uv init` on Ch 17's Python 3.14 writes `requires-python = ">=3.14"`, and I
   kept it: uv downloads 3.14 for any reader who lacks it. On 3.14, `from __future__ import annotations` does nothing
   the package needs, so I removed it from every module (option (b)) rather than explaining it (option (a), whose
   sentence would be false on 3.14). If you'd rather the package ran on 3.12/3.13 too, the change is one line in
   `pyproject.toml` plus putting the import back in `config.py` with (a)'s explanation.
2. **Shortened terminal outputs.** Some real outputs contain the author's full folder path (uv's "Building … @
   file:///…" lines, pytest's `rootdir` and `-v` platform line). I left out those whole lines, marked `…`, and said so
   under each block; no line was edited. Is that acceptable, or do you want the runs redone in a folder named like the
   reader's (`/home/meera/analyst-to-architect/work/ch29`)? I wasn't allowed to write under `/home/meera`.
3. **29.1 and 29.2** stay Open (reading-order conflicts, recommended Reject). Confirm Reject. The forced edits I made
   are listed in the changelog.
4. **Two variable names for one kind of setting.** Ch 18/20 use `RIVERSTONE_DB` (pointing at `riverstone_full`); the
   Ch 29 package uses `RIVERSTONE_DATABASE_URL` (pointing at `riverstone_2025`). The chapter now says why. Keep, or
   unify book-wide?
5. **Fact sheet dependencies:** RJ-S2-16 (Ch 29's story dates, 3 Feb and 2 Mar 2026) and RJ-S3-35 ("Since Imran left")
   stay Open until `review/riverstone-facts.md` is approved. Ch 29's text needs no change under proposal P-T2.
6. **Page count.** The chapter grew from 43 to 68 pages (class primer, step-by-step pytest, five-step client, CI).
   Time needed is now 20–24 h. Fine?

## Chapter 32

### Questions for Abhishek

1. **32.24 (held Open for reading order) describes CI defects that are real under any order.** Under the approved order, Ch 34 now teaches `./script.sh` and `chmod +x`, so the order-dependent part is gone. What's left:
   - (1) psql in the workflow gets no `PGPASSWORD`;
   - (2) `./load_test_data.sh` is never shown or shipped;
   - (3) `sqlfluff lint` runs before `dbt deps`. This only bites once a `packages.yml` exists, and the chapter now says the project has none yet.

   May I un-hold 32.24 and apply the rest of its fix? That means adding `PGPASSWORD` to the job env, replacing the script with `psql … -f` on the book's riverstone_2025 load scripts, moving `dbt deps` before the lint, and testing the workflow on GitHub.
2. **32.17** is also held. Its Ch 34 parts are moot, but one part doesn't depend on the order. The text sends ingestion ("Fivetran, Airbyte, or your own Python") and "the moving" to Ch 46, and the finding says ingestion is Ch 45. Should I change it to "Chapter 45 handles the moving and Chapter 46 the scheduling"?
3. **32.1** (held): recommend Reject. Ch 34 precedes Ch 32 now.
4. **Timings.** The incremental comparison was re-measured on the test container (4 cores, 16 GB): 2.19 s against 0.55 s, "about four times". The old text said 13.91 s against 0.90 s, "about fifteen times", on "the author's test machine", which I could not reproduce. Ch 28 describes its timing machine as 1 vCPU with 3 GB. If you want the Ch 28 machine for consistency, the numbers need re-running there.
5. **Snapshot demo date.** The real run stamped 2026-09-28, and the text says yours will be the day you run it (RJ-S2-12). The date appears in a real output. If the approved story calendar needs a different date, it can only change by re-running on that date.
6. **32.6.** I used dbt's current-folder profile lookup instead of `export DBT_PROFILES_DIR=.`. The outcome is the same (no `--profiles-dir` anywhere, exercises work) with one setting fewer. Is that OK?

## Chapter 33

### Questions for Abhishek
1. **Scale of the matching data (33.8, RJ-S2-15).** The chapter now says the match data is a synthetic, scaled-up Riverstone (66,667 orders over 2024–Nov 2025, ₹4.42 bn of line revenue), nearly 400 times the one-year database. It still doesn't reconcile with `riverstone_full` (116,194 orders, 2023–2025). Would you rather the generator be re-seeded from `riverstone_full`'s orders (numbers and timings would all change), or keep it declared as synthetic as now?
2. **Logistics partner (33.9).** The partner is left unnamed because the fact sheet's delivery-partner names conflict (C29: Swift Movers / Rapid Wheels vs SwiftLine / BlueCart). Name it once C29 is settled?
3. **33.21** is still held Open (recommend Reject, as listed in reading-order-conflicts.md): Ch 34 now precedes Ch 33, so `| head` in the Tool note is taught.

## Chapter 30

### Questions for Abhishek
1. **Length.** Ch 30 grew from 37 to 55 PDF pages, and Time needed from 14–18 h to 18–22 h (four sittings). Most of the growth is the §30.11 regression and logistic build-up (findings 30.2 and 30.3) and the by-hand steps. Is 55 pages acceptable, or should §30.11's logistic part move to Ch 31 or to Part 4?
2. **RJ-S2-16 (story calendar).** Ch 30's story is still dated 30 January (the plan) and 2–15 February 2026 (the test). That overlaps Ch 29's 3 February and Part 4's February story (Ch 35). I'll restage it once the Riverstone calendar in the fact sheet is approved.
3. **Numbers that differ from the finding's suggested wording** (recomputed, so the book now uses these):
   - 30.27: the interval ends are about 200 and 930 enquiries a month (196 and 932), not 190 and 920. This also changes the memo and §30.9.
   - 30.31/30.29: novelty is now per visitor, week 1 +22% and week 2 +5% (it was +24%/+5% per session).
   - 30.32: 1.3 points (the exact arcsine value is 1.34), not 1.25.

## Chapter 31

### Questions for Abhishek
1. **Story date (RJ-S2-16).** Ch 31's board meeting is in April 2026, which collides with Part 4's month-per-chapter calendar. Re-date it once the fact sheet's book calendar is approved?
2. **Riverstone facts (RJ-S3-35).** Ch 31 introduces four facts the bible doesn't have: North's 6% price rise on 1 Oct 2025, the QBR program (68 of 240 key accounts), free delivery from ₹25,000 (also used by Ch 55), and the Bhiwandi expansion in March 2026 (exercise 15). Add them to the fact sheet?
3. **Margin (31.26).** The story now uses Riverstone's 2025 gross margin of 26.2% (Ch 4, Ch 11 §11.6) and a simple "same cost per order" model to say North's gross profit rose about 14%. Happy with that simplification?
4. **Section order (31.36).** Synthetic control moved from §31.7 to §31.5 (matching → §31.6, RD → §31.7) so Part A is contiguous. No other chapter cites §31.5–31.7, but say if you'd rather keep the old order.

## Integration (Part 2)

1. **Ch 13's calendar tables.** Ch 13 §13.1 now tells the reader to run a second small script (`calendar_tables_*.sql`) after the one-year database. The alternative is to fold the two tables into `riverstone_2025_setup.sql` and its MySQL twin, so one load in Ch 12 §12.3 covers Ch 13 too. That means changing the shared setup scripts, which Ch 28 also builds on. Keep the separate step?
2. **Ch 17 "Where this leads"** still lists Chapter 19 (VBA and Apps Script), which the approved order reads before Ch 12. Ch 18 dropped its Ch 19 bullet for this reason. Drop Ch 17's now, or leave it for the renumbering pass?

