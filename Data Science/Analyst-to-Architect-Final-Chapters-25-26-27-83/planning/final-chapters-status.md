# Final Chapters — Status (25, 26, 27, 83 and the Appendices)

Written in the coordinator chat, at the author's instruction of 21 September 2026. Brief: `planning/parts/final-chapters-brief.md`.

## Chapters

| ID | No. | Title | Class | Status | Words | Manuscript |
|---|---|---|---|---|---|---|
| P2-25 | 25 | The Business Analyst Track | C | **Draft v2, awaiting review** (21 Sep 2026) | 11,996 (incl. answers) | `manuscript/ch25-the-business-analyst-track.md` |
| P2-26 | 26 | The Professional Toolkit: Git, Agile, Documentation & AI Assistants | C | **Approved (v1, 21 Sep 2026)** | 11,952 (incl. answers) | `manuscript/ch26-the-professional-toolkit-git-agile-documentation-and-ai-assistants.md` |
| P2-27 | 27 | Capstone: Your Analyst Portfolio | D | **Approved (v1, 21 Sep 2026)** | 12,562 (incl. answers) | `manuscript/ch27-capstone-your-analyst-portfolio.md` |
| PC-83 | 83 | The Long Game | C | **Approved (v1, 21 Sep 2026)** | 6,531 | `manuscript/ch83-the-long-game.md` |
| APX-A…H | | Appendices | | Next — **decision needed on Appendix G first** | | |

---

## Chapter 25 v2 — re-aimed at the data domain (21 Sep 2026)

**The author's instruction.** v1 taught classic software business analysis: SDLC, BRD/FRD/SRS, use cases, UAT, with generic examples. The author's point was that this is a data science book whose confirmed roles are data scientist, data analyst and data engineer, so the chapter has to live in that domain. Business Analyst is one of the ten roles Chapter 7 established, on the analytics track beside the data analyst and the BI developer, so the chapter stays. What changed is what it specifies.

**What v2 does differently.**

1. **§25.1 is now a four-way comparison** (BA, data analyst, data scientist, data engineer) rather than two-way, and says plainly why the other three roles need this chapter: an analyst who cannot elicit builds the wrong dashboard, a scientist who cannot specify delivers a model nobody deploys, an engineer who cannot analyze builds on a source a person edits by hand every Friday.
2. **A new §25.6, "The four things a data team is asked to build"**, is the chapter's centre: a report or dashboard, a pipeline, a model, and a metric definition. Each gets a worked requirement set (BR, FR, NFR), the questions its requirement must answer, and the way it characteristically fails. New figure 25.3.
3. **Non-functional requirements are now data non-functional requirements**: freshness, grain, completeness, reconciliation, timeliness, history, access, volume, with a table and an example of each. These are the ones that get dropped and then cause the incident.
4. **Acceptance criteria gain a fourth kind**, the reconciliation criterion, which is what separates a dashboard people trust from one they check against a spreadsheet before every meeting.
5. **§25.10 on UAT gains its data half**: QA cannot tell whether a number is right, so a data UAT plan reconciles one complete period at more than one level of aggregation, against a source the business already trusts.
6. **The swimlane section now carries a second lesson**: every handoff is where a data quality problem is born, tied forward to Chapter 14's cleaning work. Step 4 is where the wrong product code enters, step 8 is why delivery dates are missing, step 9 is why payments sit against the wrong invoice.
7. **The project** now requires the winner to be specified as one of the four data products, with at least two data non-functional requirements and a reconciliation criterion.
8. **The story keeps its shape and gains one line**: the dashboard reconciled to the rupee and still failed UAT, which makes its point sharper. Correct numbers are not a useful product.

**Chapter 76B stays fully covered.** All eight of the bank's sections are still taught, now with data examples rather than generic software ones. The BRD/FRD/SRS, SDLC, use case and UAT material is intact, so nothing in the bank is orphaned.

**Length.** 11,996 words including answers, 29-page PDF, 5 figures, 15 exercises. Up from 9,387 in v1 because §25.6 and the data non-functional requirements are new material. Still inside the 2× stop rule relative to Part II's median chapter, though now 2.4× the blueprint's 5,000-word figure, which was written before the four-product framing existed.

---

## Chapter 25 report (draft v1, superseded by v2)

**Depth.** 9,387 words including answers (about 8,190 of chapter, 1,195 of answers), 24-page PDF, against a blueprint of 5,000. The overrun is deliberate and is explained below. 12 numbered sections, 4 figures, a 13-row mistakes table, a real-world story, a six-part project, 14 exercises with worked answers.

**Sections.** 25.1 what a BA does and how it differs from a data analyst · 25.2 the SDLC and the BA's work in all six phases · 25.3 mapping a process: flowchart, swimlane, BPMN, as-is before to-be · 25.4 from a vague ask to a written requirement · 25.5 business, functional and non-functional requirements · 25.6 BRD, FRD, SRS and the traceability matrix · 25.7 use cases and user stories with acceptance criteria · 25.8 gap analysis · 25.9 user acceptance testing · 25.10 working with IT and with vendors · 25.11 domain knowledge · 25.12 finding, ranking and specifying an automation.

**Why it is longer than 5,000 words.** Chapter 76B, the Business Analyst question bank, was approved before this chapter existed and tests eight distinct areas, each of which says "Learn it in: Chapter 25". Delivering all eight at a level where the bank's answers are earned rather than asserted does not fit 5,000 words. The chapter is still inside the 2× stop rule, and it sits below Part II's median chapter length (10,205 words).

**Built on existing material, no new data.** Every number comes from Chapter 3 and was verified there: the ten steps of order 5001, the dates from 22 October 2025 to 3 February 2026, enquiry to cash 103 days, order to invoice 1 day, invoice to payment 27 days, order to cash 28 days, invoice 9001 for ₹14,700, and the six manual steps of section 3.7. No database was queried and no new companion file was created, which is correct for a class C chapter about a method rather than a tool.

**Figures** (`figures/make_figs25.py`, regenerated clean):

- `fig25-1-sdlc-and-the-ba.svg` — the six SDLC phases with the BA's work and relative effort in each.
- `fig25-2-order-to-cash-swimlane.svg` — Chapter 3's ten steps in four lanes, with the five lane crossings marked as handoffs.
- `fig25-3-user-story-anatomy.svg` — a story's three clauses and four acceptance criteria, each labeled with what it contributes.
- `fig25-4-gap-analysis.svg` — one gap analysis row worked end to end: as-is, gap, to-be, root cause, requirement, dependency.

Figures were renumbered so they appear in reading order, and all four were rendered to PNG and inspected.

**Verification.**

- Style scan (code blocks, tables, figure captions and the part line excluded): **0 em dashes in prose, 0 banned words, 0 British spellings**. Three soft words (*just*, *easy*) and one `labelled` were found and fixed.
- `tools/check_code_teaching.py`: **0 code blocks, 0 flagged**. The chapter has no code, which is right for its subject; its artifacts are documents and diagrams.
- Cross-references checked against the chapter map and the manuscripts: Chapters 3, 8, 11, 23, 24, 26, 27, 47, 51, 58, 60, 63, 76B all exist and say what this chapter claims they say.
- Every figure reference resolves.
- PDF built and spot-checked. One real defect found and fixed: two paragraphs were being promoted into the table of contents as setext headings, because a horizontal rule followed a paragraph with no blank line between them. Worth knowing for anyone assembling chapters from parts.

**Chapter 76B alignment.** The bank's eight sections were used as the specification. Every one is now taught:

| 76B section | Taught in |
|---|---|
| 76.1 requirements gathering | 25.4 |
| 76.2 BRD / FRD / SRS, requirement against user story | 25.6, 25.7 |
| 76.3 user stories and acceptance criteria | 25.7 |
| 76.4 process mapping, swimlanes, BPMN, as-is against to-be | 25.3 |
| 76.5 SDLC and where a BA fits | 25.2 |
| 76.6 gap analysis and UAT | 25.8, 25.9 |
| 76.7 stakeholder management and pushback | Chapter 24, by design; 25.1 says so |
| 76.8 the live invoice-matching scenario | 25.12, which supplies the worked requirement the bank talks through |

The bank's worked examples match this chapter's: the same order-to-cash swimlane, the same as-is and to-be on the invoicing step, and the same invoice-matching automation. **Issue 23 can be closed** once this chapter is approved. The bank's section-number references to Chapter 25 should be checked once numbering is final.

**One canon conflict found in Chapter 76B.** Its real-world story describes Farah as "now working as a Business Analyst after the career transition Chapters 8, 9, and 68 followed". Chapter 8's story, *Farah's internal move*, has her applying for the **Data Analyst (Sales Analytics and Automation)** posting, and Chapter 9 follows her twelve-week practice log toward that role. Those are different tracks, and this chapter is the one that draws the distinction. Proposed resolution: Chapter 76B's story keeps its shape and changes Farah to a different name, which also settles the same chapter's exposure under cross-part issue 22. Raised as a new item rather than fixed here, since Chapter 76B belongs to the Part VIII chat.

**New Riverstone facts (proposed for the bible).** One: **Ayesha Qureshi**, a business analyst at Riverstone who moved into the role from the customer support desk about eighteen months before March 2026. Used in this chapter's real-world story. The name is used nowhere else in the book. The story itself, a March 2026 at-risk-accounts report that passed QA and failed UAT in eleven minutes, is a story scenario and not canon data.

**Promises delivered.** Chapter 3 ("the full process map in Chapter 25", and "Keep it for Chapter 25") · Chapter 7 (the BA track including finding automation opportunities) · Chapter 8 (the skills-matrix row: mapping processes, finding and prioritizing automation opportunities, writing automation requirements) · Chapter 22 (experimentation in practice, where constraints are organizational; handled in 25.4 and 25.9 as the discipline of testing whether the specification was right) · Chapter 23 (process mapping and requirements as how a KPI tree gets built collaboratively) · Chapter 24 (requirements formalized into process mapping, user stories, BRD, FRD, SRS).

**Promises made.** Chapter 26 (Agile, Scrum, Kanban and Jira in practice; Git for the documents and queries this chapter produces) · Chapter 27 (this chapter's requirements pack becomes a portfolio piece) · Chapter 47 (business rules become automated data-quality tests) · Chapter 51 (the integrations that close these gaps) · Chapter 60 (non-functional requirements at architecture scale) · Chapter 63 (governing a portfolio of automations) · Chapter 76B (the question bank).

**Manual checks needed.** None. No external facts are quoted, no tool versions are named, and every number is inherited from an approved chapter.

**Open for the author.**

1. Approve or reject the length: 9,387 words against a 5,000-word blueprint, for the reason above.
2. Accept Ayesha Qureshi into the Riverstone bible.
3. Confirm the Chapter 76B name change for Farah, which the Part VIII chat would make.

---

## Chapter 26 report (v1 — **approved by the author, 21 September 2026**)

**Depth.** 11,952 words including answers, 33-page PDF, against a blueprint of 4,000. 11 numbered sections, 3 figures, a 16-row mistakes table, a real-world story, a six-step project, 15 exercises with worked answers. The overrun is explained below.

**Sections.** 26.1 the three places a file lives · 26.2 your first repository (`init`, `status`, `add`, `commit`) · 26.3 reading the history and reading a change (`log`, `diff`) · 26.4 what must never go into a repository (`.gitignore`, `.env`, `check-ignore`, `rm --cached`) · 26.5 the four undos · 26.6 branches · 26.7 GitHub, pushing, and the pull request · 26.8 one automated check on every push · 26.9 a repository a stranger can run (structure, files Git cannot diff, the README, documentation that survives) · 26.10 how the work is actually planned (Scrum, Kanban, Jira) · 26.11 working with an AI assistant.

**This is the second chapter in the book to meet the section 6.5 standard in full**, which was the explicit instruction in the brief. It carries **three settings tables** (`git commit`: `-m`, `-a`, `--amend`, `--no-verify` · `git log`: `--oneline`, `-n`, `--stat`, `--graph` · the GitHub Actions workflow: `on:`, `runs-on:`, `python-version:`, `@v4`), each with a "What happens if you change it" column; **one measured what-if** comparing `git log -n 2` against `git log --oneline -n 2 --stat` with both real outputs printed; a **predict-before-running** exercise (exercise 6, on a file that is both staged and modified); and line-by-line explanation of every command and every configuration key on first use. `tools/check_code_teaching.py`: **20 code blocks, 0 flagged, 0 findings.**

**Every terminal session in this chapter was actually run.** A real Git repository was built at `/tmp/claude-0/ch26demo`, with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` fixed so the commit hashes are reproducible. Every transcript, including the hashes `dbdb993`, `1bed4f9`, `6489661` and `837e258`, the `MM` short-status code, the `Fast-forward` merge line, and the `git check-ignore -v` output, is captured output rather than invented. The one exception is the `git push` transcript in 26.7, which is labeled in the text as shown rather than run, because it needs a GitHub account.

**Why it is longer than 4,000 words.** Twenty-one chapters point here, with 46 separate references, and they promise different things: version control for SQL and Python (Chapters 12, 13, 17, 18, 20), keeping `.env` out of a repository (Chapters 18, 20, 29, 45), pull requests and code review (Chapters 28, 29, 32), continuous integration (Chapters 29, 32), a portfolio home (Chapters 9, 27), documentation habits (Chapters 23, 24), Agile and Jira in practice (Chapters 24, 25), binary files such as `.pbix` and VBA modules (Chapters 16, 19), and AI assistants at work (Chapters 5, 12). Delivering all of them at the section 6.5 standard does not fit 4,000 words. It sits about 17% above Part II's median chapter (11,952 against roughly 10,200), and inside the 2× stop rule.

**Scope boundaries honored** (from the brief): the command line is Chapter 34's, so this chapter uses a terminal without teaching one · packaging, tests and type hints are Chapter 29's · CI/CD, Docker, Kubernetes and Terraform are Chapter 52's, so 26.8 stops at one workflow file · how LLMs work is Chapters 54 and 55, so 26.11 is only about working with one. The chapter is written to be readable after Parts 0 to II alone.

**Figures** (`figures/make_figs26.py`, all three rendered to PNG and inspected):

- `fig26-1-three-places.svg` — working directory, staging area and history, with the commands that move a file between them in both directions and the three that only look.
- `fig26-2-four-undos.svg` — the four undo situations as four panels, each with where the change currently lives, the command, and whether it destroys work.
- `fig26-3-pull-request-flow.svg` — a branch leaving `main`, gaining commits, becoming a pull request with review and an automated check, then merging back.

**Verification.**

- Style scan (code blocks, tables, figure captions and the part line excluded): **0 em dashes in prose, 0 banned words, 0 British spellings.** Fixed in draft: *genuinely*, *honestly*, four *simply/simple*, one *easy*, two *obvious*, two *just*, and five prose em dashes. "Cancelled" is kept: it is the book's convention (267 uses against 9 of "canceled") and the literal value in the Riverstone `status` column.
- `tools/check_code_teaching.py`: 20 code blocks, 0 flagged, 0 findings.
- Cross-references checked against the chapter map: Chapters 2, 5, 6, 12, 13, 16, 17, 18, 19, 20, 23, 25, 27, 29, 32, 34, 44, 47, 52, 56, 64 and 82 all exist and say what this chapter claims.
- The setext-heading defect found in Chapter 25 was pre-empted at assembly: a blank line is inserted before every horizontal rule. The table of contents is clean.
- PDF built and spot-checked at pages 1, 2, 3, 11 and 12.

**Stale references checked and clear.** Three old promises pointing at "Chapter 26" for normalization rules, indexes and query plans survive only in `ch12.v1.md`, which is superseded. The approved `ch12-databases-and-sql-foundations.md` has none, so no cross-part issue is needed. That material is Chapter 28's.

**New Riverstone material.** No new names and no new canon data. The real-world story uses **Meera Iyer**, **Vikram Singh** and **Farah Khan**, all established, and the story scenario (February 2026: nobody could date the rule that excluded cancelled orders; a `.env` with the database password was pushed and the fix was to change the password) is a story scenario, not canon data. The demo repository's author identity, `Meera Iyer <meera@riverstone.example>`, is used only inside terminal output.

**Promises delivered.** Chapter 2 (Git as the precise form of version history) · Chapter 5 (working with AI assistants) · Chapter 6 (Git was installed there, used here) · Chapters 12 and 13 (versioning queries; the pattern library as one file per pattern in a repository) · Chapter 16 (`.pbip` instead of `.pbix` so Power BI diffs) · Chapters 17, 18 and 20 (versioning scripts; `.env` and `os.environ`; `requirements.txt` committed and `.venv` not) · Chapter 19 (exporting VBA modules to commit them) · Chapters 23 and 24 (documentation that survives; the metric definitions in `docs/metrics.md`) · Chapter 25 (Agile, Scrum, Kanban and Jira in practice) · Chapters 28, 29 and 32 (pull requests, code review, and CI introduced here).

**Promises made.** Chapter 27 (this repository becomes the portfolio) · Chapter 29 (package layout, tests and type hints run by this chapter's check) · Chapter 32 (the same discipline for SQL transformations) · Chapter 34 (the terminal itself) · Chapter 44 · Chapter 47 (checks against the data rather than the code) · Chapter 52 (CI to deployment) · Chapter 56 (versioning models and training data) · Chapter 64 (governance, including what an AI assistant counts as) · Chapter 82 (take-homes graded on 26.9's standards).

**Manual checks needed.** Two, both small and both about third parties whose terms change: the statement that **GitHub free accounts include unlimited public and private repositories**, and that **GitHub Actions is free for public repositories with a monthly allowance for private ones**. Both are written without numbers for that reason, but they should be confirmed at the pre-publication refresh.

**Open for the author.**

1. Approve or reject the length: 11,952 words against a 4,000-word blueprint, for the reason above.
2. Confirm that 26.8 stopping at a single GitHub Actions workflow is the right boundary against Chapter 52.
3. Confirm the AI-assistant section's position: it treats an assistant as normal professional equipment with rules, rather than either a threat or a shortcut.

---

## Chapter 27 report (v1 — **approved by the author, 21 September 2026**)

**Depth.** 12,562 words including answers, 31-page PDF, against a blueprint of 3,000. 11 numbered sections, 3 figures, a 15-row mistakes table, a real-world story, a six-step project, 15 exercises with worked answers. The overrun is the largest in the book relative to blueprint and is argued below.

**Sections.** 27.1 a question worth putting in a portfolio (three tests, and the framing table) - 27.2 SQL: the headline - 27.3 cleaning: the decisions, and whether they mattered - 27.4 the check that changes the answer - 27.5 Python: making the analysis arguable - 27.6 the dashboard: one page, one decision - 27.7 the memo - 27.8 **selective reporting, and why a portfolio is where it starts** - 27.9 what a hiring manager does with your repository - 27.10 telling the story, in two minutes and in ten - 27.11 what job-ready actually looks like.

**Chapter 22's promise is delivered, and it is the spine of the chapter.** The brief said this was the easiest promise to miss and the most interesting thing in the chapter, so it was built into the project rather than bolted on. The chapter's own worked analysis produces a true, quotable, entirely wrong headline in section 27.2, and section 27.4 takes it apart. Section 27.8 then generalizes it into the five moves, why a portfolio has no friction to catch them, four fixes that cost nothing, and the interview version.

**Every number was computed, and both verifiers pass.**

- `tools/verify_sql.py ... --db riverstone_full`: **statements run 4, outputs checked 4, mismatches 0** (PostgreSQL 16).
- `tools/verify_python.py ... --cwd companion/full`: **blocks run 4, outputs checked 3, mismatches 0** (Python 3.11, pandas).
- The three-year database was loaded from `companion/full/riverstone_full_setup_postgresql.sql` and its totals reconciled against `DATA_SPEC.md` before anything was written: 2025 net revenue 1,146,641,651 and gross margins 21.1 / 24.7 / 27.5 match to the rupee and the decimal.

**The verifier found a real defect, which is why it exists.** Two of the three SQL blocks were first written with an elided CTE (`...`) and a reference to `customer_year` that no reader could have run. `verify_sql.py` failed both. They are now self-contained and verified. Anyone assembling a chapter from parts should note that a block which reads fine in context can still be unrunnable.

**Section 6.5.** One settings table (`year`, `segment`, `band_cut`, `min_orders`, each with "what happens if you change it") and one measured what-if, which is the same object as the ethics lesson: moving `band_cut` from 5 to 3 shrinks the reported gap from 5.5 orders to 3.5 on data that did not change. Exercise 5 is the predict-before-running prompt, extending the same measurement to 8 and revealing that the threshold is a dial on segment purity. All code is taught line by line; `tools/check_code_teaching.py` reports **8 code blocks, 0 flagged** after the tool fix below.

**One checker flag read and deliberately left alone** (instruction section 15.1). The NTILE query is 26 lines and the checker asks for it to be split. Twelve of those lines are an exact repeat of the CTE taught bullet by bullet in section 27.2, and the repetition exists because `verify_sql.py` proved that an elided block is not runnable. Splitting it would trade a real defect for a heuristic. The prose says so and points at the view that would remove the repetition.

**Tool fix made in this pass.** `tools/check_code_teaching.py` reported `on` as "a setting never explained in the chapter's prose", and could never have done otherwise: its `IDENT` pattern requires three or more characters, so a two-letter keyword argument (`on=`, `by=`, `ax=`) can never be found in prose and is always flagged. The settings check now skips names shorter than three characters. Chapters 25 and 26 re-checked afterward and are unchanged.

**Distinct from Chapter 44, which the brief required.** Read first, as instructed. Chapter 44 is a machine-learning lifecycle ending in a ranked call list, with a per-chapter "toolkit applied" table and a recommendation to act. This chapter is the analyst arc on the same company with no model, ending in a recommendation **not** to act, and its second half (27.8 to 27.11) has no counterpart anywhere in the book. The framing table, the closing table, the metaphor, the story and the memo's shape are all different. Both chapters contain a memo, which the blueprint requires of both; Chapter 44's proposes an action list, this one declines a proposal and names the test that would settle it.

**Figures** (`figures/make_figs27.py`, all three rendered to PNG and inspected):

- `fig27-1-the-analyst-arc.svg` - the six stages with what each produced in this project and which chapters taught it, with stage 3 marked.
- `fig27-2-the-finding-that-did-not-survive.svg` - three panels of average orders per customer on a shared scale: the headline, the segment split, and the flat within-Wholesale quartiles.
- `fig27-3-the-ninety-second-scan.svg` - what a reviewer reads, in order, with what each moment tells them.

**Verification.**

- Style scan (code, tables, captions and the part line excluded): **0 em dashes in prose, 0 banned words, 0 British spellings.** Fixed in draft: *honestly*, *genuinely*, two *obvious*, one *just*. "Cancelled" is kept as the book's convention and the literal `status` value.
- Cross-references checked: Chapters 3, 9, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 39, 44, 68, 69, 82, 83 all exist and say what this chapter claims. Section-level references (13.2, 13.4, 13.7, 14.5, 14.9, 15.6, 17.8, 18.3, 22.2, 22.3, 22.4, 22.5, 22.6, 24.4, 26.9, 26.11) were checked against the manuscripts.
- Blank line inserted before every rule at assembly, so the Chapter 25 setext defect does not recur. Table of contents clean.
- PDF built and spot-checked at pages 1, 2, 9 and 10.

**New Riverstone material.** No new names. The real-world story uses **Farah Khan** and **Anita Rao**, both established, and extends the portfolio piece Chapter 9 already has her building (hospitality orders before the wedding season). The story does not state whether she got the role, since that is Part I's to decide. Vikram Singh's question in section 27.1 is a story scenario; the analysis answering it is real and reproducible.

**Stale references checked and clear.** Old promises pointing at "Chapter 27" for normalization rules and query plans survive only in `ch12.v2.md`, which is superseded; the approved `ch12-databases-and-sql-foundations.md` has none.

**Promises delivered.** Chapter 8 ("the projects at the end of every chapter in Part II are designed for this, and Chapter 27 turns them into a portfolio"; "a portfolio can stand in for experience") - Chapter 9 ("every chapter project in this book is designed to become a portfolio piece"; the portfolio lives on GitHub) - **Chapter 22 ("the ethics of analysis, including selective reporting")** - Chapter 25 (the requirements pack becomes a portfolio piece; section 27.1 uses its framing) - Chapter 26 (this chapter's repository is the one built by that chapter's project).

**Promises made.** Chapter 28 - Chapter 29 - Chapter 30 (the experiment this chapter's memo proposes) - Chapter 31 - Chapter 39 - Chapter 44 - Chapter 68 - Chapter 69 - Chapter 82 - Chapter 83.

**Manual checks needed.** None. No external facts, no tool versions beyond PostgreSQL 16 and Python 3.11, and every number is computed from the companion data.

**Open for the author.**

1. **Approve or reject the length**: 12,562 words against a 3,000-word blueprint. The case for it: the blueprint line was written before Chapter 22's selective-reporting promise existed and before the chapter had a second half, and 21 chapters of Part II converge here. It is 1.23x Part II's median chapter, which is the measure the 2x stop rule uses, but it is 4.2x its own blueprint, which is the largest ratio in the book. The alternative is to split 27.8 to 27.11 into a separate short chapter, which would make Part II 18 chapters.
2. Confirm that the project's conclusion, a recommendation not to discount, is the right note for Part II to end on. It is deliberate and it is unusual.
3. Confirm the Farah Khan story stops short of saying whether she got the role.

---

## Chapter 83 report (v1 — **approved by the author, 21 September 2026**)

**Depth.** 6,531 words, 17-page PDF, against a blueprint of 2,500. Ten numbered sections, 2 figures, an 11-row mistakes table, a real-world story, a one-week plan, six closing decisions. Deliberately the shortest chapter written in this chat: an ending that outstays its welcome is a worse fault than a short one.

**Sections.** 83.1 the arithmetic, stated plainly - 83.2 consistency beats intensity - 83.3 study just enough to build, then build - 83.4 go deep, then broad - 83.5 choose your own summit - 83.6 the fundamentals are durable, the tools are not - 83.7 you cannot do this alone - 83.8 **the plateaus that come later** - 83.9 the meta-skill: learning how to learn - 83.10 what this book could not give you. Then: the ways people fall off the path - In the real world: how Meera got there - the first week after this book - how you will know it is working - Recap - six decisions - Key terms - Where this leads - the closing lines.

**Kept from the draft's Chapter 33, as instructed.** All seven of the draft's arguments survive, in the same order and often in the same words: consistency beats intensity, study just enough to build, go deep then broad, choose your own summit, durable fundamentals, you cannot do this alone, and learning how to learn. The draft's closing paragraphs are kept almost verbatim, including "The map is not the territory", "The reading is finished. The building begins", and "The mountain is real. You have the map. Go climb." Those lines are the best in the draft and changing them would have been vandalism.

**The plateau material was replaced, not deleted** (coordinator note of 17 September). The draft's "expect plateaus" paragraph now lives in Chapter 9 section 9.7 as Farah's twelve-week log. Section 83.8 refers back to it and then does what the note asked: **the later plateaus**, which are different in kind. The organizing insight is one sentence, and it is new to the book: *a learning plateau is solved by changing how you practice; a career plateau is solved by changing what you are responsible for.* Four are named with a tell, a cause and a move: competence, stack, indispensable, ladder. A fifth item covers the flat stretch that is not a plateau at all but a job you have outgrown.

**Section 83.1 is the chapter's new spine, and every number in it was computed.** A script totalled the *Time needed* line of all sixty-seven teaching chapters: **764 to 980 hours**, of which **319 to 396** reach the end of Part II. At six hours a week that is 12 to 15 months to job-ready and 2.4 to 3.1 years for the whole map. Per-part subtotals are in figure 83.1. Nobody has stated these numbers before and they are checkable against the manuscripts, which is the point: Chapter 9 promised an honest timeline and could only speak in months and years; now it can be exact.

**Section 83.2's arithmetic is also computed, and it is the strongest argument in the chapter.** A sprinter at 25 hours a week for 12 weeks reaches 300 hours and stops. A steady reader at 6 hours a week crosses them at **week 50**, reaches the job-ready band at weeks 53 to 66, and has 936 hours by year 3. The sprinter's 300 hours do not reach the end of Part II, so the sprinter burns out between one and five chapters short of employable. That claim was checked against the per-part totals before it was made and the wording carries the range rather than the flattering end of it.

**Shape.** This is not a teaching chapter and it does not use the full template. There are no exercises, no answer key, no Tools section, and no project in the usual sense. The chapter says so in its own *at a glance* block and gives the reason: the last thing a closing chapter should do is hand the reader more reading. In place of exercises there are **six decisions with no answers**, and in place of a project, **a one-week plan** with a named task for each day. Chapter 67 set the precedent with its "Questions to sit with"; this chapter deliberately does something different, because Chapter 67's questions look backward and these look forward.

**Figures** (`figures/make_figs83.py`, both rendered to PNG and inspected):

- `fig83-1-the-arithmetic.svg` - hours per part as low-high bars, with the job-ready and whole-book summary rows.
- `fig83-2-consistency-beats-intensity.svg` - cumulative hours over 160 weeks for both readers, with the week-50 crossover marked and the job-ready band shaded, so the sprinter's line visibly stops below it.

**Verification.**

- Style scan: **0 em dashes in prose, 0 banned words, 0 British spellings.** Fixed in draft: six *genuinely*, four *honestly*, one *licence*, and one each of *just*, *easy*, *simply*, *obvious*. The draft leaned on those words, which is worth noting for the coherence pass: they cluster in reflective writing.
- `tools/check_code_teaching.py`: 0 code blocks, 0 flagged. Correct for this chapter.
- Every number in sections 83.1 and 83.2 recomputed from the manuscripts and from arithmetic shown in the report above.
- Cross-references checked: Chapters 2, 8, 9 (sections 9.1, 9.3, 9.6, 9.7), 11, 12, 13, 14, 16, 20, 25, 26 (sections 26.7, 26.9, 26.11), 27 (section 27.1), 28, 32, 49, 64, 67, 68, and Part VIII 68 to 82.
- PDF built and spot-checked.

**Promises delivered.** Chapter 9 ("Chapter 83, The Long Game, returns to learning over a whole career, including the plateaus of later years") - Chapter 27 ("about what happens after the first job, which the portfolio exists to get").

**Riverstone.** No new names and no new canon. The story assembles what Chapters 2, 7, 8, 11 and 20 already establish about Meera Iyer: she inherited Imran's Friday file, learned SQL beside it, became the person everyone asks, and then spent forty minutes every morning building the Daily Sales Flash by hand. That last fact, already canon in Chapter 7, **is** the indispensable plateau of section 83.8, which is why the story needed no invention. It also explains why the Chapter 8 job posting has the word *Automation* in its title. The story is set entirely before the book's present and commits nothing about the future.

**Cross-part issue 20 is now ready to apply, and the exact edits are drafted.** Chapter 67 still claims to be the final chapter and misnames Part VIII as "the Question Banks in the appendices (Chapters 70 through 79)". Chapter 83 now exists, so the five framing edits have a destination; they are written out replacement by replacement at the end of `planning/cross-part-issues.md`. The same file records the mirror gap in Chapter 82, whose *Where this leads* ends at Part VIII and does not hand off to Chapter 83. One bullet closes it.

**Manual checks needed.** None.

**Open for the author.**

1. **Approve the length**: 6,531 words against a 2,500-word blueprint. The extra is section 83.1's arithmetic and section 83.8's later plateaus, neither of which existed in the draft, plus the week plan. The draft's own material is about 1,200 words of it and is intact.
2. **Confirm the no-exercises decision.** Every other chapter in the book has them. This one argues that it should not.
3. **Confirm the ending.** The draft's last lines are kept word for word. If the book's title or framing changes before publication, this is the paragraph to re-read.
