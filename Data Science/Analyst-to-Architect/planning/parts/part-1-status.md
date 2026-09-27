# Part I — The Map · Status

**PART I COMPLETE — all three chapters approved by the author, 16 Sep 2026.** Total ~30,400 words; 13 figures; 3 check scripts (all passing); 1 companion SQL file.

Owner: Part I chat. Chapters 7–9. Instructions: `planning/chapter-writing-instructions.md` v1.0.

| ID | No. | Title | Class | Status | Words (incl. answers) | Manuscript |
|---|---|---|---|---|---|---|
| P1-07 | 7 | The Data Landscape | C | **Approved (v1)** (16 Sep 2026) | ~10,900 (answers ~1,500) | `manuscript/ch07-the-data-landscape.md` |
| P1-08 | 8 | The Career Tree: How Skills Unlock Roles | C | **Approved (v1)** (16 Sep 2026) | ~11,300 (answers ~1,150) | `manuscript/ch08-the-career-tree-how-skills-unlock-roles.md` |
| P1-09 | 9 | How Expertise Actually Forms | C | **Approved (v1)** (16 Sep 2026) | ~8,200 (answers ~1,700) | `manuscript/ch09-how-expertise-actually-forms.md` |

---

## Chapter 7 report — The Data Landscape (v1, approved 16 Sep 2026)

**Approved by the author on 16 Sep 2026.** Approved PDF: `Ch07-The-Data-Landscape-v1-approved.pdf`. Length accepted as is.

### Contents
Why this matters · In plain English (hospital analogy) · 7.1 The four questions (fixes draft "three questions") · 7.2 The tracks and the ten roles (roles table; SQL shared by every role) · 7.3 The field as a tree (science and engineering as peers; order matches parts) · 7.4 The automation and integration track (automation analyst, RPA developer, integration engineer; Daily Sales Flash thread) · 7.5 Team structures (centralized, embedded, hub-and-spoke; comparison table) · 7.6 One request through every role ("Which customers are going quiet?", real query on `riverstone_2025`) · 7.7 How AI assistants change each role · 7.8 Where you are now · Common mistakes (12 rows) · In the real world: *Anita wants to hire a data scientist* · Tools · Project: map the data work around you · You've got it when (10) · Recap · 15 exercises with worked answers · Key terms · Where this leads.

### Length
~10,900 words including SQL, tables, and answers. Above the class C typical range (5,000–9,000) but well under the 2× stop point. Not padded; if the author wants it shorter, trim candidates are the story and 7.6 steps 5–9.

### Files
- `manuscript/ch07-the-data-landscape.md`
- `figures/make_figs07.py` → `fig7-1-four-questions-and-roles.svg`, `fig7-2-the-field-as-a-tree.svg`, `fig7-3-source-to-action.svg`, `fig7-4-three-team-structures.svg`, `fig7-5-one-request-every-role.svg` (regenerate; don't save SVGs to the project)
- `checks/ch07_check.py`
- `companion/mysql/ch07_queries_mysql.sql`
- PDF (send, don't store): `Ch07-The-Data-Landscape.pdf`, 27 pages

### Verification
- `verify_sql.py`: 2 blocks run (1 PostgreSQL 16, 1 MySQL 8.0.46), 2 outputs checked, **0 mismatches**.
- `checks/ch07_check.py`: 15 checks, all pass (customer counts, 60- and 90-day lists, revenue of lapsed customers ₹114,072.50 = 2.6% of ₹4,335,471, day counts 66 and 284, hours arithmetic 167 h and 104.2 h).
- MySQL companion file runs end to end; identical 5 rows.
- Figures rendered to PNG and inspected; renumbered to order of appearance.
- Style: no em dashes in prose, no banned words, no British spellings found; all chapter and section references checked against `planning/chapter-map.md` and the blueprint.
- PDF spot-checked (tables, code, figures, callouts, exercises).

### Sources checked (16 Sep 2026)
- Stack Overflow 2025 Developer Survey, press release and AI section: 84% use or plan to use AI tools (76% in 2024); 46% distrust accuracy vs 33% trust; 49,000+ responses. https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/ · https://survey.stackoverflow.co/2025/ai — the 2026 survey opened 23 June 2026; results not yet published at writing (https://stackoverflow.blog/2026/06/23/the-2026-developer-survey-is-now-open-for-human-developers-only/). **Update 7.7 when 2026 results appear.**
- World Economic Forum, Future of Jobs Report 2025: big data specialists and AI/ML specialists among fastest-growing roles; data entry clerks among fastest-declining; analytical thinking the top core skill. https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/ · https://www.weforum.org/stories/2025/01/future-of-jobs-report-2025-the-fastest-growing-and-declining-jobs/
- No salaries in this chapter (Chapter 8 will verify them).

### Manual checks needed
None. Every output and number was run or computed.

### New Riverstone facts (proposed)
1. In the Chapter 7 story, Riverstone's first dedicated data hire is advertised as **Data Analyst (Sales Analytics and Automation)** (Anita and Meera write the ad). Chapter 8 may reuse this as its fictional job description.
2. Story detail: Meera produces the Daily Sales Flash by hand (about 40 minutes each morning) before automation. Consistent with blueprint §5 (Ch 11 manual Flash); flag in case Part II sets a different figure.
3. Section 7.6 describes a hypothetical larger Riverstone with one specialist per role (explicitly labeled a simplification). **Not** proposed as canon.

### Promises made to other chapters
- Ch 8: decode a job description; skills matrix; day in the life; pathways table; entry routes (all already in its scope).
- Ch 6: learning with AI assistants without letting them think for you. Ch 26: using AI assistants at work.
- Ch 12 §12.15 and Ch 13 Pattern 6: referenced as the teaching of the 7.6 query and its rhythm-based refinement (already written).
- Ch 20: overdue-invoice list as scheduled email / low-code flow is offered as one possible approach (exercise 7 answer), not a promise of that exact example.
- Ch 32: a tested `customer_activity`-style model (illustrative name).
- Ch 51: risk flags written into the CRM as tasks without duplicates. Ch 55, 58: AI call brief grounded in company data with human approval. Ch 56: model monitoring and retraining. Ch 63: automation ownership/governance. Ch 66: structuring data teams. Ch 68: interview rounds per role.

---

## Chapter 8 report — The Career Tree: How Skills Unlock Roles (v1, approved 16 Sep 2026)

**Approved by the author on 16 Sep 2026.** Approved PDF: `Ch08-The-Career-Tree-How-Skills-Unlock-Roles-v1-approved.pdf`. Length accepted as is.

### Contents
Why this matters · In plain English (building of locked doors) · 8.1 Skills are keys; roles are doors · 8.2 The tiers (0–6, matching Parts 0–VII; tiers 3 and 4 shown as peers, fixing the draft's tier 3/4 mismatch; automation roles at tiers 1, 2, 4; the three rules kept) · 8.3 Skills matrix (17 skills × 10 roles, table + heatmap) · 8.4 A day in the life of each of the ten roles · 8.5 Decoding a job description (full fictional Riverstone posting from Ch 7's story; seven-step decoding; weighted fit score and must-have coverage worked for Farah; red flags; Interview extra point) · 8.6 Pay: sources and methods, PayScale table for three roles, percentiles/median, Indeed vs PayScale, thin data for new titles, CTC vs in-hand, how to check yourself · 8.7 Reader pathways table (blueprint §5, verbatim content) and automation thread by tier · 8.8 Entry routes: fresher, career switcher, internal move · 8.9 Pick your door, learn backward · Common mistakes (12) · In the real world: *Farah's internal move* · Tools · Project: your door plan · You've got it when (11) · Recap · 14 exercises with worked answers · Key terms · Where this leads.

### Length
~11,300 words including tables and answers. Above class C typical range (5,000–9,000), under the 2× stop point. Heaviest sections: 8.4 (ten days in the life) and 8.7 (two reference tables). Trim candidates if wanted: shorten 8.4 to ~60 words per role.

### Files
- `manuscript/ch08-the-career-tree-how-skills-unlock-roles.md`
- `figures/make_figs08.py` (imports `make_figs07.py`) → `fig8-1-career-tree-tiers.svg`, `fig8-2-skills-matrix.svg`, `fig8-3-decoding-a-job-description.svg`, `fig8-4-three-entry-routes.svg`
- `checks/ch08_check.py` (skills matrix counts and overlaps, fit scores, salary arithmetic; imports the matrix from `figures/make_figs08.py` so table, figure and text share one source)
- PDF (send, don't store): `Ch08-The-Career-Tree-How-Skills-Unlock-Roles.pdf`, 28 pages
- No companion data files; no SQL or Python blocks (verify_sql: 0 blocks, 0 mismatches)

### Verification
- `checks/ch08_check.py`: 25 checks, all pass. (Two first-draft counts were wrong and were corrected from the script before writing: data scientist 6 core skills, data engineer 7, architect 9, DA/BI overlap 7, DA/DE overlap 4.)
- Markdown matrix table generated from the same data as the heatmap.
- Figures rendered and inspected (matrix label clipping fixed). PDF spot-checked page by page.
- Style: no em dashes in prose, no banned words, no British spellings; chapter references checked against the chapter map.

### Sources checked (retrieved 16 Sep 2026)
- PayScale India, Data Analyst: avg base ₹577,472; 10th–90th ₹289k–₹1m; median ₹577k; entry (<1 yr) avg total ₹413,462 (576 salaries); early career (1–4 yrs) ₹565,999 (1,588); 2,389 profiles; updated 10 Jul 2026. https://www.payscale.com/research/IN/Job=Data_Analyst/Salary
- PayScale India, Data Scientist: avg base ₹1,017,652; 10th–90th ₹312k–₹2m; median ₹1m; entry ₹595,255 (307); early ₹1,005,147 (754); 1,267 profiles; updated 9 Jul 2026. https://www.payscale.com/research/IN/Job=Data_Scientist/Salary
- PayScale India, Data Engineer: avg base ₹974,783; 10th–90th ₹410k–₹2m; median ₹975k; entry ₹518,398 (125); early ₹810,624 (965); 1,284 profiles; updated 14 Jul 2026. https://www.payscale.com/research/IN/Job=Data_Engineer/Salary
- Indeed India, Data Analyst: avg ₹633,625/yr from 681 salaries in job postings (past 36 months), updated 30 Aug 2026. https://in.indeed.com/career/data-analyst/salaries
- Many other salary pages found were training-provider blogs with unsourced or inconsistent figures; deliberately not used.
- Other roles (BA, BI developer, analytics engineer, ML/AI engineer, integration/RPA, architect): no figures printed; chapter explains why (new or mixed titles) and teaches how to check. **Refresh all figures before publication.**
- CTC vs in-hand described in general terms only (no tax calculations), framed as general information, not financial advice.

### Manual checks needed
None for code. **Before publication:** re-pull the four salary pages and update the 8.6 table and exercises 6–7 (checks script holds the arithmetic).

### New Riverstone facts (proposed)
1. The full text of the Riverstone posting *Data Analyst (Sales Analytics and Automation)* in section 8.5 (location given only as "head office, hybrid"; 1–3 years, freshers with strong projects considered).
2. Farah Khan (employee 5) has been a sales executive for four years, knows the hospitality customers best, and is working toward the analyst role; she spends Friday afternoons helping Meera and built a Monday at-risk email in Google Sheets/Apps Script. Vikram asked for the same email for his team.
3. Not canon: the ten "day in the life" people and companies are one-off fictional illustrations.

### Promises made to other chapters
- Ch 9: timeline, deliberate practice, portfolio, feedback, plateaus (in scope). Ch 27: portfolio from Part II projects. Ch 13 Pattern 6 (at-risk list), Ch 16 (dashboard), Ch 19–20 (automated report; Apps Script Monday email with time-driven trigger, in Ch 19 scope). Ch 23–24: agreeing definitions / stakeholder work. Ch 25: BA track. Ch 66: hiring and structuring teams. Ch 68: interview rounds, CVs, why decoded JDs land well. Ch 81: offer conversations and CTC negotiation. Ch 82: what fair take-home assignments look like.

---

## Chapter 9 report — How Expertise Actually Forms (v1, approved 16 Sep 2026)

**Approved by the author on 16 Sep 2026.** Approved PDF: `Ch09-How-Expertise-Actually-Forms-v1-approved.pdf`.

### Contents
Why this matters · In plain English (learning to cook) · 9.1 The honest timeline (kept; estimating with chapter hours: Ch 12 + Ch 13 = 34–43 h, at 6 and 10 h/week) · 9.2 Why the long timeline is good news (kept) · 9.3 The three ingredients (kept; knowledge / skill / judgment loop) · 9.4 Deliberate practice (five features; research: Ericsson, the 10,000-hour popularization, Macnamara et al. 2014; methods table; AI-assistant watch-out) · 9.5 Building a portfolio as you learn (seven-part piece; portfolio by stage) · 9.6 Feedback and mentors (sources table; five-part help request; finding a mentor) · 9.7 Handling plateaus (moved forward from Closing; Farah's 12-week log with fixed weekly check; causes; seven responses) · 9.8 How to use this book · Common mistakes (13) · In the real world: *Farah's week seven* · Tools · Project: a 12-week learning system · You've got it when (11) · Recap · 14 exercises with worked answers · Key terms · Where this leads.

### Length
~8,200 words including answers: within the class C typical range.

### Files
- `manuscript/ch09-how-expertise-actually-forms.md`
- `figures/make_figs09.py` (imports `make_figs07.py`) → `fig9-1-three-ingredients.svg`, `fig9-2-naive-vs-deliberate-practice.svg`, `fig9-3-anatomy-of-a-portfolio-piece.svg`, `fig9-4-practice-log-plateau.svg`
- `checks/ch09_check.py` (26 checks: log totals and phases, chapter-hour arithmetic, exercise answers; imports Farah's log from the figure script)
- PDF (send, don't store): `Ch09-How-Expertise-Actually-Forms.pdf`, 21 pages
- No SQL/Python blocks (verify_sql: 0 blocks, 0 mismatches)

### Verification
- `checks/ch09_check.py`: all checks pass. Figures rendered and inspected; renumbered to order of appearance. PDF spot-checked.
- Style: no em dashes in prose, no banned words (several instances of "honestly/just/easy" removed), no British spellings; cross-references checked.

### Sources checked (16 Sep 2026)
- Macnamara, B. N., Hambrick, D. Z., & Oswald, F. L. (2014). Deliberate practice and performance in music, games, sports, education, and professions: A meta-analysis. *Psychological Science*, 25(8), 1608–1618. Deliberate practice explained 26% (games), 21% (music), 18% (sports), 4% (education), <1% (professions) of variance; authors: important but not as important as argued. https://journals.sagepub.com/doi/abs/10.1177/0956797614535810
- Ericsson's deliberate-practice research on musicians (early 1990s), Gladwell's *Outliers* (2008) popularizing "10,000 hours", and Ericsson's later objection: well-established background, stated without numbers.
- Retrieval practice and spacing described qualitatively ("research on learning has repeatedly found"), no statistics.

### Manual checks needed
None.

### New Riverstone facts (proposed)
1. Farah's 12-week SQL practice log (fictional data in section 9.7) and her plateau in weeks 4–8, caused mainly by the LEFT JOIN / filter-placement idea (Ch 12 §12.10).
2. Farah shows Meera one query every Friday; her first portfolio piece compares hospitality customers' orders before this year's and last year's wedding season.
3. Meera "tripped over the same thing when she started" (no date implied).

### Promises made to other chapters
- Ch 6: study setup, sample 6-month plan, learning with AI assistants. Ch 12 §12.10: LEFT JOIN trap (already written). Ch 13 §13.3: window functions (already written). Ch 16: Power BI for Farah's next skill (project Option B). Ch 26: Git/GitHub for portfolios. Ch 27: finished analyst portfolio. Ch 30, 32, 44, 46–47, 60, 63: portfolio pieces by stage (in their scopes). Ch 68: how portfolios are read in hiring. Ch 81: turning projects and plateaus into behavioral answers. Ch 83: learning over a whole career, including later plateaus (blueprint: plateau material also appears early in Ch 9).

---

## Requests for the coordinator
1. **Chapter 3 dependency:** Ch 7 refers to "the ERP" and "the CRM" generically and uses no system names. If Part 0 names Riverstone's systems, Ch 7 can adopt them in a later revision.
2. **Chapter 68 coordination:** use the same ten role names as Ch 7 §7.2 (data analyst, business analyst, BI developer, analytics engineer, data scientist, ML engineer, data engineer, AI engineer, automation analyst / RPA developer / integration engineer, data architect).
3. **Blueprint §5 wording:** the pathways table and Ch 7 now use "Engineering & integration" as the track name covering data engineer, analytics engineer, and the automation roles; Ch 8 will follow this.
4. **Storage:** this chat has no project-write tool. Files are delivered to the author as downloads for manual upload (author approved, 16 Sep 2026).
5. **Chapter 8 salary figures:** date-stamped (retrieved 16 Sep 2026); add to the pre-publication refresh list alongside the Ch 7 survey figures.
6. **Chapter 68 / 81 coordination:** Ch 8 teaches CTC vs in-hand and salary-source reading; banks should point back to section 8.6 rather than repeat it.
7. **Chapter 83 overlap:** plateau material now lives in Ch 9 §9.7 (per blueprint); Ch 83 should refer back rather than repeat it.
8. **Part I complete:** Chapters 7, 8 and 9 all approved by the author on 16 Sep 2026. Please mark P1-07, P1-08 and P1-09 approved in the chapter map and progress tracker.
9. **Update reminder:** refresh the Stack Overflow figures in §7.7 when the 2026 survey results are published.
