# Briefing for `DECISIONS.md`

A triage aid, so section B can be filled without reading 3,758 rows. For each theme: roughly how
many rows look like it, the High / Medium / Low split, and two real examples.

**These counts are approximate.** They come from keyword-matching the `issue` text, and a row can
match more than one theme, so the numbers do not sum to 3,758. `CLAUDE.md` section 4 still requires
the agent to map each row to its theme by reading it, and to leave a row `Open` when the fit is
unclear. Use this to decide *which themes to approve*, not as the mapping itself.

Register: **3758 rows**, 501 High, 1702 Medium, 1553 Low. 29 already Approved.

| Theme | What it covers | Rows | H / M / L |
|---|---|---:|---|
| **T1** | Code shown before it is taught (sequence rule) | 41 | 20 / 19 / 2 |
| **T2** | Tools and libraries never installed | 83 | 33 / 28 / 21 |
| **T3** | Big code blocks with many new ideas | 16 | 6 / 9 / 1 |
| **T4** | No by-hand example before the method | 32 | 5 / 22 / 5 |
| **T5** | Foundations the book never teaches | 149 | 39 / 83 / 27 |
| **T6** | Hidden companion code / black-box outputs | 46 | 16 / 14 / 16 |
| **T7** | Printed outputs that are errors | 4 | 1 / 1 / 2 |
| **T8** | Wrong chapter/section cross-references | 96 | 8 / 49 / 39 |
| **T9** | Part VIII pointers and numbering | 63 | 9 / 20 / 34 |
| **T10** | Riverstone facts that disagree | 298 | 58 / 124 / 116 |
| **T11** | Drafting and authoring leftovers | 77 | 20 / 7 / 50 |
| **T12** | Time needed estimates too low | 12 | 1 / 6 / 5 |
| **T13** | Claims needing outside verification | 53 | 14 / 25 / 14 |
| **T14** | Integrity of examples and advice | 33 | 7 / 13 / 13 |
| **V1** | Covers: draft/approval badges, versions, dates | 24 | 3 / 17 / 4 |
| **V2** | Contents pages: add page numbers | 14 | 1 / 6 / 7 |
| **V3** | Figure text under 7 pt | 210 | 44 / 155 / 11 |
| **V4** | Figures contradicting the text or overlapping | 26 | 17 / 8 / 1 |
| **V5** | Figures out of number order | 11 | 1 / 6 / 4 |
| **V6** | Colour-only meaning | 20 | 4 / 11 / 5 |
| **V7** | Page breaks, stranded headings and lead-ins | 73 | 0 / 53 / 20 |
| **V8** | Code lines wrapping badly | 94 | 8 / 45 / 41 |
| **V9** | Two-digit list numbers clipped | 58 | 2 / 35 / 21 |
| **V10** | Tables: wraps, alignment, white-on-white | 333 | 68 / 144 / 121 |
| **V11** | Rendering: $, formulas, markdown, the rupee glyph | 115 | 32 / 54 / 29 |
| **V12** | Scale and resolution | 53 | 7 / 25 / 21 |
| *(unmatched)* | Matched no theme by keyword; needs reading | 2086 | 197 / 888 / 1000 |

---

## Examples per theme

### T1 — Code shown before it is taught (sequence rule)

Roughly **41 rows** (20 / 19 / 2 High/Medium/Low).

- **S.1**, Ch All (High, Sequence): Code shown before it is taught (table above). "You don't need to read this yet" labels don't fix it.
- **14.2**, Ch 14 (High, Sequence): Python/pandas before Ch 17–18 (M.2). It is not only §14.13: about 15 pandas mentions and snippets are spread across the chapter, including a whole column of the §14.3 tool table.

### T2 — Tools and libraries never installed

Roughly **83 rows** (33 / 28 / 21 High/Medium/Low).

- **S.3**, Ch 6 (High, Sequence): Setup chapter too early: Python installed Ch 6, first used Ch 17 (~150+ study hours later); Git → Ch 26; Power BI → Ch 16; reader runs terminal/venv/PowerShell policy before knowing what Python is; 3–4 h of installing at the weakest moment; Ch 7–9 use no softw
- **14.1**, Ch 14 (High, Sequence / First-time reader): The first action in the chapter is two terminal commands, including changing directory and client flags. The terminal is not taught until Ch 26 §26.0 (M.4). Readers set up databases through DBeaver in Ch 12 §12.3. The riverstone_full databases themselves are n

### T3 — Big code blocks with many new ideas

Roughly **16 rows** (6 / 9 / 1 High/Medium/Low).

- **11.7**, Ch 11 (High, Line-by-line): A 30-line M block with ~12 new functions and options: Folder.Files, Table.SelectRows, each, Text.Lower, Table.AddColumn, Csv.Document with Delimiter/Encoding 65001/QuoteStyle, Table.PromoteHeaders, [PromoteAllScalars = true], Table.Combine, Parsed[Data], Table
- **19.19**, Ch 19 (High, Line-by-line): The block chains about 12 new JS ideas: slice(1), date arithmetic, an arrow-function predicate, filter, forEach with the \ | \ | accumulator, Object.keys().sort().map().join(), toLocaleString('en-IN'), a nested template literal with a ternary, MailApp.sendEmai

### T4 — No by-hand example before the method

Roughly **32 rows** (5 / 22 / 5 High/Medium/Low).

- **21.2**, Ch 21 (High, First-time reader / Flow): No by-hand step and no spreadsheet step. The book's principle is idea → by hand → known tool → new tool. Here the reader never computes a mean, median, variance or quartile on numbers they can see.
- **37.24**, Ch 37 (High, First-time reader): No by-hand step. The idea ("share of the k nearest that churned") is never computed on numbers, though it is the easiest algorithm in the chapter to do by hand.

### T5 — Foundations the book never teaches

Roughly **149 rows** (39 / 83 / 27 High/Medium/Low).

- **S.2**, Ch 6 (High, Sequence): Tests PostgreSQL double precision / MySQL approximate-value rounding never taught. Typo: part (e) ROUND(45E1) = 450, answer treats it as 4.5 (45E-1).
- **14.3**, Ch 14 (High, Line-by-line / Sequence): Regular expressions are used in about 20 places in the chapter (~, !~, regexp_replace with 'g'/'i' flags, ^ $ [0-9] [^0-9] \d{2} \s+ + ? \ | , M's Text.Select range, Excel's REGEXREPLACE) but are never taught. Ch 10–13 never used them (Ch 11 only mentions that

### T6 — Hidden companion code / black-box outputs

Roughly **46 rows** (16 / 14 / 16 High/Medium/Low).

- **10.1**, Ch 10 (High, Flow / First-time reader): Setup is a three-sentence paragraph buried in §10.1. It has no first-run check and doesn't say how to open a companion .xlsx in the free web apps. "In Excel, double-click the file" (§10.1 tour) doesn't work in Excel for the web, which is the free route the cha
- **14.4**, Ch 14 (High, Line-by-line / Flow): The chapter never shows how clean_order_lines, clean_customers or dq_order_issues are built. It says "the companion script builds" them and shows fragments. Their columns (date_repaired, entered_at_ist, match_key, email_invalid, signup_in_future, action, issue

### T7 — Printed outputs that are errors

Roughly **4 rows** (1 / 1 / 2 High/Medium/Low).

- **19.10**, Ch 19 (High, Line-by-line): TypeScript and JavaScript are never taught. The code uses function main(workbook: ExcelScript.Workbook), const/let, type annotations, { [key: string]: string }, for (let r = 1; …; r++), ++, ===/!==, 0-based values[r][8], template literals ${…}, arrow functions

### T8 — Wrong chapter/section cross-references

Roughly **96 rows** (8 / 49 / 39 High/Medium/Low).

- **22.24**, Ch 22 (High, Consistency (cross-ref)): All four cross-references are wrong. Ch 23 = Business Acumen/KPIs; storytelling is Ch 24; forecasting is Ch 40; experimentation is Ch 30 (Inference & Experiments) and Ch 31 (causal inference); Ch 27 is the portfolio capstone; ethics/responsible data is Ch 64. 
- **30.1**, Ch 30 (High, Consistency (cross-ref) / Sequence): Known wrong cross-reference (M.5): Ch 19 is VBA. Under D3, regression basics are taught in the new Ch 22 §22.10 (per finding 22.30). Prediction comes later, in Ch 37.

### T9 — Part VIII pointers and numbering

Roughly **63 rows** (9 / 20 / 34 High/Medium/Low).

- **72A.2**, Ch 72A (High, Consistency): Part VIII numbering (proposal for the whole part). The part uses 68–72, 72A, 73–75, 76A, 76B, 77–82, and there is no Chapter 76. Earlier chapters already cite "Chapter 76" for the BA bank (Ch 1 l.809, Ch 3 l.1038, Ch 5 l.572/841, Ch 14 l.1536, Ch 15 l.942, Ch 
- **72A.11**, Ch 72A (High, Correctness): The BFS keeps visited as a list, so every membership check is O(n) and BFS becomes O(V²). That contradicts Q72A-014 ("a list checks every element one by one"), Ch 33 §33.4 (which uses a set) and this chapter's own "Common mistakes" row. An interviewer would fl

### T10 — Riverstone facts that disagree

Roughly **298 rows** (58 / 124 / 116 High/Medium/Low).

- **0.1**, Ch 6 (High, Consistency): Plan says Parts 0–II take 6 months at 8 h/week (~208 h); book's own estimates total 319–396 h; Closing says 12–15 months at 6 h/week. Meera's "nine months at 6 h" also wrong.
- **10.3**, Ch 10 (High, Consistency): Wrong count. Figure 10.3 says 125 wrong + 10 right by luck + 195 text = 330. The text says 135 wrong, *plus* 10 lucky, plus 195, which is 340. 135 is the number of real dates (COUNT = 135 = 125 wrong + 10 right). The error repeats in "The 135 wrong dates are r

### T11 — Drafting and authoring leftovers

Roughly **77 rows** (20 / 7 / 50 High/Medium/Low).

- **I.1**, Ch 8 (High, Polish): Drafting history addressed to reader: "The draft of this book introduced…", "fix for the first edition's tier order", "rules from the first edition still hold", "first edition saved this topic for its closing chapter", "as the first edition did".
- **I.2**, Ch 8 (High, Polish): Author's build scripts named as reader resources: checks/ch08_check.py, figures/make_figs08.py, checks/ch09_check.py, figures/make_figs09.py.

### T12 — Time needed estimates too low

Roughly **12 rows** (1 / 6 / 5 High/Medium/Low).

- **68.3**, Ch 68 (High, Consistency / Load): Load/consistency with the book's own timeline method. Ch 12–13 + 16 + 19–20 are 90–112 hours by their own Time needed lines (19–23 + 15–20 + 18–22 + 20–25 + 18–22). In 8 weeks that's 11–14 h/week. Ch 9 §9.1 calls 6 h/week "realistic alongside a full-time job",

### T13 — Claims needing outside verification

Roughly **53 rows** (14 / 25 / 14 High/Medium/Low).

- **18.10**, Ch 18 (High, Sequence): After the approved move, Ch 14 no longer has pandas. §14.13's content (exact-duplicate count 137, status spellings table, price value_counts, customer_code length check, clean_orders_pandas.py, "37 logged issues", dq_order_issues_pandas.csv) must land here.
- **21.1**, Ch 21 (High, First-time reader): False promise. No formula is ever written in symbols: no mean x̄ = Σxᵢ/n, no variance/SD, no z = (x − x̄)/s, no CV, no SE = s/√n, no binomial/Poisson formula, no law of total probability. Σ notation has never been taught (Ch 4 does arithmetic only). A beginner

### T14 — Integrity of examples and advice

Roughly **33 rows** (7 / 13 / 13 High/Medium/Low).

- **23.17**, Ch 23 (High, Consistency / Correctness): False. Ch 21 says the delivery times are invented by a seeded model because "the ERP data has no delivery dates". This breaks the chapter's own promise to label real vs invented, and misleads the reader about data provenance.
- **51.6**, Ch 51 (High, Correctness): A content-only key has a real bug: a value that returns to an earlier value can never be re-sent. Say lead 4's score goes 20 → 21 → back to 20. The key for (4, 20, stage) was already used in the first sync, so the CRM replays it and the field stays at 21 for g

### V1 — Covers: draft/approval badges, versions, dates

Roughly **24 rows** (3 / 17 / 4 High/Medium/Low).

- **34.1**, Ch 34 (High, Sequence): Decision D2: terminal essentials move to Ch 26 §26.0 (spec in part2/ch26.md), and Linux and networking stay here. As written, Ch 34 re-teaches everything §26.0 now covers, and the chapter's opening promise is out of date.
- **52.21**, Ch 52 (High, Line-by-line): The explanation covers only the 5 resources and the output. Not explained: the terraform {} / required_providers block; source = "hashicorp/aws"; version = "~> 5.0" (≥5.0, <6.0); the provider block and where credentials come from (never in the file: environmen

### V2 — Contents pages: add page numbers

Roughly **14 rows** (1 / 6 / 7 High/Medium/Low).

- **28.4**, Ch 28 (High, Line-by-line / Sequence / First-time reader): The terminal part is mostly covered by §26.0 (cd, running a script with arguments). But: (a) Tools says "migrate.py calls the psql client", which the reader doesn't have on PATH (28.3); (b) how it connects is never said (user, password, host), and it will fail

### V3 — Figure text under 7 pt

Roughly **210 rows** (44 / 155 / 11 High/Medium/Low).

- **V1.2**, Ch 1 (High, Visual): Receipt and table text is 4.9–5.4 pt. The table's column headers and cells, the chapter's first data table, are unreadable in print.
- **V1.3**, Ch 1 (High, Visual): All three panels are 4.9–5.2 pt, including the JSON and email text the prose tells readers to look at ("the middle panel… every value has a name").

### V4 — Figures contradicting the text or overlapping

Roughly **26 rows** (17 / 8 / 1 High/Medium/Low).

- **11.5**, Ch 11 (High, Line-by-line / Consistency): The model instructions contradict themselves, and the measures won't run as written. (a) Step 2 loads RiverstoneSales (from §11.7: 326 rows, cancelled already removed, segment already merged). Then it says to use the practice file's plain Sales columns A–I ins
- **V24.1**, Ch 24 (High, Visual): Several drawing and placement defects: (a) "POWER" is drawn twice, horizontally and rotated, so the two copies overprint as a smudge. (b) "INTEREST →" overprints the footnote line ("…share findings, don't ask for time…"). (c) The label "Board / owning fam" is 

### V5 — Figures out of number order

Roughly **11 rows** (1 / 6 / 4 High/Medium/Low).

- **V62.1**, Ch 62 (High, Visual): The GOLD — Modelled / Marts box is clipped at the figure's right edge: its right border and the right end of its note strip are missing.

### V6 — Colour-only meaning

Roughly **20 rows** (4 / 11 / 5 High/Medium/Low).

- **V31.2**, Ch 31 (High, Visual): Before and after are shown only by red versus green dots, the classic colour-blind pair. The x-axis has no scale (only "0" and a "0.1 rule of thumb" label at the band edge). Text is 4.8–5.3 pt.
- **V41.1**, Ch 41 (High, Visual): The labels "pricing" and "cancel" overprint each other, so neither word is readable. The dots are coloured in four groups (blue, orange, green, grey), but no legend or caption explains the colours.

### V7 — Page breaks, stranded headings and lead-ins

Roughly **73 rows** (0 / 53 / 20 High/Medium/Low).

- **V1.6**, Ch 1 (Medium, Visual): Stranded alone at the foot of p. 6; the bullet list is on p. 7.
- **V1.11**, Ch 1 (Low, Visual): A one-line widow ("twelve rows tell a manager nothing.") sits at the top of p. 6.

### V8 — Code lines wrapping badly

Roughly **94 rows** (8 / 45 / 41 High/Medium/Low).

- **V1.1**, Ch 1 (High, Visual): All 8 data rows and the header wrap: "…│ Station" / "stall │ No", "…│ shop" / "│ necessary". The dashed rule also breaks onto a second line. The table readers are asked to copy no longer reads as a table.
- **V28.1**, Ch 28 (High, Visual): The result is wider than the code block. The header "is_current" wraps to a second line, the dashed rule wraps, and every row's f/t value falls alone to column 0 on the next line. The table can no longer be read.

### V9 — Two-digit list numbers clipped

Roughly **58 rows** (2 / 35 / 21 High/Medium/Low).

- **26.18**, Ch 26 (High, First-time reader / Line-by-line): YAML is never introduced (the only mention is "YAML reads 3.10 as the number 3.1"). The reader is not told that indentation is meaningful and must be spaces, what key: value is, what a - list item is, or why with: is indented under a step. The extracted listin
- **32.5**, Ch 32 (High, First-time reader / Line-by-line): YAML is used far beyond Ch 26's primer (26.18: key: value, indentation, - lists, [a, b]). New here: lists of maps (- name: orders with nested columns:), inline maps {count: 24, period: hour}, version: 2, quoted numbers '1.0.0', the + config prefix, >- folded t

### V10 — Tables: wraps, alignment, white-on-white

Roughly **333 rows** (68 / 144 / 121 High/Medium/Low).

- **S.1**, Ch All (High, Sequence): Code shown before it is taught (table above). "You don't need to read this yet" labels don't fix it.
- **V1.1**, Ch 1 (High, Visual): All 8 data rows and the header wrap: "…│ Station" / "stall │ No", "…│ shop" / "│ necessary". The dashed rule also breaks onto a second line. The table readers are asked to copy no longer reads as a table.

### V11 — Rendering: $, formulas, markdown, the rupee glyph

Roughly **115 rows** (32 / 54 / 29 High/Medium/Low).

- **11.3**, Ch 11 (High, Line-by-line): One formula, five new ideas: a test on a whole range makes an array of TRUE/FALSE; TRUE×1 = 1; + as OR; >0 to stop double counting; * as AND. The "How it works" bullets explain it after the fact. There's no intermediate result the reader can see.
- **11.8**, Ch 11 (High, Correctness): Formula bug. The denominator groups rows by name and status. A customer with both Delivered and Shipped (or Pending) lines gets 1 from each status group, so they're counted twice. There are 3 Shipped and 1 Pending lines, so any customer holding one of them tog

### V12 — Scale and resolution

Roughly **53 rows** (7 / 25 / 21 High/Medium/Low).

- **39.2**, Ch 39 (High, First-time reader): Metrics are defined from real model output, with no tiny by-hand example first. The first code block does five new things: helper import, sys.path, fit, predict_proba(...)[:, 1], and a summary of predicted probabilities. The reader meets TP/FP/FN/TN only as a 
- **42.1**, Ch 42 (High, Correctness / Consistency): The metric is misnamed throughout. With one held-out item per account, evaluate returns hits ÷ accounts, which is the hit rate@5 (= recall@5 when there is one relevant item). True precision@5 = hits ÷ (5 × accounts), so the figures should be popularity 12.3%, 

