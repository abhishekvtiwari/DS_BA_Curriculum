# Journey findings — Fable A, the reader's journey

*Interim note at Chapter 10, 22 September 2026. Covers Part 0 (Chapters 1–6) and Part I (Chapters 7–9), read in reading order, front to back, editing nothing. The method is the one in the coherence-pass command; the sections below are the ones it asks for, filled for these nine chapters and left open for the rest.*

**Scope of this note.** 74,700 words, nine chapters, 9 projects, 131 exercises. Two readers throughout: **Reader 1** is a complete beginner changing careers; **Reader 2** already works in data and is looking things up. Severity is the S1–S4 scale from the strategy file, section 6. Nothing here re-reports a cross-part issue; where a finding touches one, it says "extends CPI-n".

**Is the method working?** Yes, and the evidence is that it found things the checkers could not. Chapter 6's study plan orders Part II against the book's own reading order; nobody has told the reader where to get the practice data; and the most vivid story in Part 0 promises a payoff that Chapter 20 does not deliver. None of those is visible to a per-chapter check. All three are visible on page one of a front-to-back read.

---

## Summary

### The three things that most damage the reader's journey, in order

1. **The study plan in Chapter 6 tells the reader to read Part II in an order the book abandoned on 17 September.** Figure 6.2 and its bullets put cleaning, charts and Power BI (14–16) before Python (17–18), and spreadsheet automation (19–20) *after* Python "because Chapter 20 uses it". The decided order is 10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20: Chapter 19 was rewritten to come *before* Python, and Chapters 14 and 15 now contain pandas because Python precedes them. A beginner who follows the only plan the book gives them meets pandas in Chapter 14 four weeks before the chapter that teaches it. This is the one instruction every Reader 1 is told to follow. (S1-1)

2. **The reader is never told where the companion files are.** Every project from Chapter 2 onward depends on them. Chapter 2 and Chapter 4 point at "Appendix E"; Chapter 6 says "Appendix E gives the address to download them from"; Appendix E does not exist. There is no download address, repository name, or URL anywhere in Chapters 1–9. Chapter 2's project is the first thing in the book a beginner cannot do. (S1-3)

3. **Chapter 2 promises, twice, that Chapter 20 automates "this exact report", the Friday file. It doesn't.** Chapter 20 builds the Daily Sales Flash, a different report with a different cadence and source. Chapter 3 separately promises that Chapters 19–20 automate "the monthly report". Three chapters, three different reports, one chapter that builds one of them. The reader remembers the Friday file: it is the best story in Part 0. (S1-2)

Behind those three: the place a beginner most plausibly quits is **Chapter 6**, which asks them to install eight tools in month one (Python first used four months later), sends them into the longest chapter in the book to find the database steps, and then hands them three chapters of career orientation before they type a formula. (S2-1, S2-2, and the structural question at the end.)

### What the book does unusually well, so the repair does not destroy it

- **Chapter 1 starts at zero and means it.** A shop notebook, a receipt turned into a table, a six-row customer list with six planted faults, and Meera's first week. It is the right first chapter for this book and should not be touched except for the two glosses in S3-3.
- **One company, one quarter, and the numbers reconcile across chapters.** ₹116,210 booked, ₹104,210 billed, ₹0 collected in Chapter 3 return in Chapters 4 and 5; order 5001 runs from Chapter 3 to Chapter 7 to Chapter 25; the nineteen order lines Chapter 6 counts are the twelve orders Chapters 1–5 followed. A reader who checks finds the book right every time, which is the whole basis of trust.
- **Every "In plain English" analogy is real and mapped**, not decorative: the notebook, the paper office, the relay race, the shop sign, the doctor, the kitchen, the hospital, the building, learning to cook.
- **The stories are the spine, and they hold.** Meera from sales coordinator (Ch 1) to the person everyone asks (Ch 7); Farah from a name on an order (Ch 2) to a 13-of-28 score (Ch 8) to a twelve-week plateau and her first portfolio piece (Ch 9). The Farah plateau story in Chapter 9 is the best thing in the first nine chapters.
- **Chapters 4 and 5 are model chapters for Reader 1.** Every claim is worked; every trap is shown with the wrong answer first and the reason it looks right.
- **Honesty about time and money.** Chapter 9's timeline arithmetic and Chapter 8's salary section refuse to promise anything, and say why.
- **Chapter 7 shows real SQL to a reader who cannot read it, and gets away with it** by saying so and walking the query in plain words.

---

## S1 findings — breaks the reader

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S1-1 | Ch 6, Figure 6.2 and §6.8 bullets 2–3; Figure 6.1 | Follows the six-month plan; reaches Chapter 14 in month 4 and meets pandas; Python is scheduled for month 5. Meets Chapter 19 last, though it was rewritten to come before Python. | The plan was drawn before the reading order was decided on 17 September (chapter-map.md, top table) and never redrawn. §6.8 states the old reasoning outright: "Automation (Chapters 19–20) after Python, because Chapter 20 uses it." | Regenerate `fig6-2` to the decided order (10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20, then 21–27); rewrite the two bullets; fix Figure 6.1's "in the order the book first uses them" (Python now precedes 14–16). No prose beyond those bullets changes. | Reader 1 | Part 0 (coordinator) |
| S1-2 | Ch 2, "In the real world" last paragraph and Where-this-leads bullet 5; Ch 3 §3.7 last paragraph and Where-this-leads bullet 4 | Is told Chapter 20 "takes this exact report and automates it end to end" (the Friday file) and, in Chapter 3, that Chapters 19–20 "automate the monthly report". Arrives at Chapter 20 and finds the Daily Sales Flash, which Chapter 7 had also promised. | Chapter 20 was written to Chapter 7's promise; Chapters 2 and 3 were written after Chapter 20 and made their own. Verified: `ch20` line 27 "builds one thing end to end: Riverstone's Daily Sales Flash"; no mention of the Friday file or Imran anywhere in Chapters 19–20. | Four sentences: Chapter 2 and 3 say Chapter 20 automates "a report of exactly this kind, the Daily Sales Flash", or Chapter 20 adds a closing paragraph applying the Flash's method to the Friday file. The first is smaller. | Both; Reader 1 most, because the Friday file is the story they remember | Part 0 (coordinator); Part II-A if Chapter 20 takes it |
| S1-3 | Ch 2 at-a-glance and Tools; Ch 4 at-a-glance; Ch 6 §6.4 | Cannot do Chapter 2's project, open Chapter 4's workbook, or run Chapter 6's checks, because the only pointer is "Appendix E", which is unwritten. | No chapter carries the download address; Chapter 6 defers to the appendix; appendices A–H are not written (README). | One sentence with the address (or an assembly placeholder) in Chapter 1's Tools and Chapter 6 §6.4; Appendix E when it exists. | Reader 1 | Coordinator / assembly |
| S1-4 (extends CPI-6) | Ch 6 "In the real world"; Ch 7 "In the real world" | In Chapter 6 (set after February 2026: it cites the Chapter 3 reconciliation) Meera "wants to become an analyst properly" and installs PostgreSQL from scratch. One chapter later, in a story set at the 2025 year-end, she "had been at Riverstone long enough to … learn SQL". | CPI-6 names the contradiction. The reading adds the cause: the Part 0 stories are dated January–March 2026 and Chapter 7's is dated December 2025, so the reader meets the later events first. Chapter 1's story carries no date at all. | CPI-6's fix (Chapter 6 v1.1: setting up her home computer to go further, not starting SQL), plus one date in Chapter 7's story and one in Chapter 1's ("months earlier", or a month). | Reader 1 | Coordinator |

---

## S2 findings — loses the reader

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S2-1 | Ch 6 §6.3, steps 2, 3 and 6 | Installs PostgreSQL, MySQL, DBeaver, Python, a virtual environment and four packages, VS Code, Git and Power BI in month one. Uses a spreadsheet for the next two chapters. First runs Python in month five; by then the "run the activate line each time" instruction is forgotten and versions have moved. | Setup is designed so every check passes before the reader starts, which is stated as the chapter's philosophy ("Readers who set up properly before they need to get through those chapters in a fraction of the time"). That is a real trade-off, and the author chose it; the cost is that the beginner's first evening of technical work is spent on tools they will not touch for months. | Keep the chapter and its checks. Label steps 2, 3 and 6 "do this when you reach Chapter 12 / 17 / 16", and add a one-line *Before you start* box in those three chapters pointing back to the step. Nothing is rewritten. | Reader 1 | Part 0 (coordinator); one line each in Part II-A |
| S2-2 | Ch 6 §6.3 step 2 | Is sent to "Chapter 12, section 12.3" for the database install. Opens the longest chapter in the book (32,273 words) in month one to find a 1,265-word section. | The install steps were written once, in Chapter 12, and Chapter 6 points at them to avoid duplication. Correct instinct, wrong destination for a beginner. | Point Chapter 6 at Appendix B (which Chapter 6 already says "keeps current instructions") and make §12.3 the source Appendix B is assembled from. If Appendix B stays unwritten, inline the 1,265 words. | Reader 1 | Coordinator / assembly |
| S2-3 | Ch 1–9 projects; Ch 6 §6.8 | Is scheduled to finish Chapters 1–9 in month one (Figure 6.2, ~32 hours) and is assigned nine projects in those chapters: a seven-day spending log, five file formats, a process map, five checked statistics, an issue tree, a 90-day plan, a team map, a door plan ("another 2–3 hours") and a twelve-week learning system. | Each project is right for its chapter. Nobody added them up against the month the plan gives them. | One paragraph in §6.8: which Part 0–I projects to do now (1, 6, 8), which to start and carry (9), and which to return to. Chapter 9 already says its project "runs alongside your learning for 12 weeks"; the others do not say. | Reader 1 | Part 0 (coordinator) |
| S2-4 | Ch 2 §2.1 | Meets bits, bytes, ASCII, Unicode, UTF-8, garbled encodings, floating point, pixels and sound storage in the first section of the second chapter, none of it usable until Chapter 6's rounding puzzle and Chapter 12's `NUMERIC`. Chapter 2 has 75 key terms against Chapter 1's 52 and Chapter 3's 49. | §2.1 teaches storage internals whose payoff is two and ten chapters away, with no forward pointer. The office analogy carries the chapter; §2.1 is the one section the analogy does not reach. | Not a rewrite. One sentence at the floating-point paragraph ("this is why 2.5 rounds two ways in Chapter 6") and cut the pixel arithmetic to two sentences. | Reader 1 | Part 0 (coordinator) |
| S2-5 | Ch 8 §8.7 | Reader 2 reaches Chapter 8, roughly 60,000 words in, and finds the row "Already an analyst: skim Parts 0–II; start fully at Part III". There was no way to know this on page one. | The reader-pathways table is the book's "how to read this book" and it lives in the eighth chapter. | Lift the §8.7 table into front matter as "How to read this book", with the "Complete beginner" and "Already an analyst" rows first. Findability, not content. | Reader 2 | Assembly |
| S2-6 (extends CPI-24) | Ch 8 §8.7 pathways table and automation-thread table; Ch 6 Figure 6.2; Ch 9 §9.5 portfolio table | Ranges such as "Ch 10–16, 19–27", "Chapters 14–16", "12–20", "46–47" are written on old numbers. After renumbering, old 10–16 becomes new 10, 11, 13, 14, 17, 18, 19: not a range. Substitution cannot fix these. | CPI-24 plans to "re-check every forward reference above 72". In Chapters 1–9, references to renumbered Part II and III chapters outnumber references to Part VIII by roughly 150 to 19, and about fourteen of them are ranges. | In the renumbering pass, rewrite every range that spans a renumbered chapter as an explicit list. The list of all 169 moving references in these chapters is below. | Both | Coordinator at assembly |

---

## S3 findings — costs polish

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S3-1 | Ch 8 §8.1, §8.2 (twice), answer 1; Ch 9 §9.2, §9.7; Ch 6 §6.9 | "The draft of this book introduced…", "This is the fix for the first edition's tier order…", "kept from the first edition…", "in this draft". Reader 1 wonders what first edition. | Author's notes to the author left in reader prose. | Delete the seven clauses. The sentences stand without them. | Reader 1 | Part I chat; Part 0 for §6.9 |
| S3-2 | Ch 2 §2.8; Ch 2 §2.5 | "sent with the `curl` command-line tool" before the terminal exists (Ch 6 §6.5); "Reading it back with Python's pandas library" before Python (Ch 17). | Incidental tool names in a chapter that is otherwise careful. | Gloss curl in one clause ("a small program typed into a terminal, which Chapter 6 introduces"); drop pandas by name ("a program"). | Reader 1 | Part 0 (coordinator) |
| S3-3 | Ch 1, "Why this matters" line 23 and §1.3 | "the words in SQL" and "from spreadsheets to databases to Python" in the chapter that says "assumes no technical knowledge at all". | Unglossed forward mentions. | One clause each: "SQL, the language for asking a database questions" and "Python, a programming language". | Reader 1 | Part 0 (coordinator) |
| S3-4 | Ch 1 §1.9; Ch 2 (five uses) | "CRM" used in Chapter 1 and throughout Chapter 2 and defined in Chapter 3 §3.3. | Everyday business acronym assumed known. | Gloss at first use in Chapter 1 ("a salesperson updating a CRM, the sales team's contact system"). | Reader 1 | Part 0 (coordinator) |
| S3-5 | Ch 4 §4.9, sanity check 1 | "3.3 orders a week at ₹25,061 each is about ₹11,911 a day." A reader who checks with 3.3 gets ₹11,814, and "within ₹50" becomes ₹64. The figure was computed from the unrounded 173 ÷ 52 = 3.327. | Chapter 4's own rule (§4.6: round at the end) applied invisibly, in the section that tells the reader to check numbers another way. | "(using the unrounded 3.33)" or show 173 ÷ 52 ÷ 7 × ₹25,061. | Reader 1 | Part 0 (coordinator) |
| S3-6 | Ch 8 Where-this-leads; Ch 81 | Chapter 8 teaches CTC and in-hand pay and promises Chapter 81 covers "negotiating on CTC". Chapter 81 negotiates offers (Q81-024 to 026) and never uses either term. | Vocabulary taught in Part I not carried into Part VIII. Kept in substance. | Chapter 81 uses "CTC" and "in-hand" once where it says "total compensation" and "the number"; or Chapter 8 says "negotiating an offer". | Reader 1 (India) | Part VIII chat |
| S3-7 (extends CPI-22) | Ch 8 exercises 5 and 11 | "Rahul scores himself against the Riverstone posting"; "Neha, a sales executive with strong Excel skills and three years of customer contact, wants to become a data analyst". Read as Rahul Mehta and Neha Kulkarni, the two executives from Chapters 3 and 5. Not contradictory (Farah's story says Anita will interview others), but unmarked. | First-name reuse in exercises, the pattern CPI-22 found in Chapters 73 and 80. | Either make it deliberate ("Rahul Mehta, from the sales team") or use names used nowhere else. | Both | Part I chat |
| S3-8 | Ch 4, 5 and 7 "In the real world" | Three Anita-to-Meera stories all set in "the first week of January 2026", read in a row. Plausibility, not error. Chapter 1's story is undated. | Stories written in parallel by different chats, each picking the same plausible week. | Stagger the dates by a week or two; date Chapter 1's story relative to them. | Reader 1 | Coordinator |
| S3-9 | Ch 6 §6.2 Figure 6.1 | "Five tool cards in the order the book first uses them" lists databases (12–13, 14), then Power BI (16), then Python (17–18). After the reorder Python is used before 14, 15 and 16. | Part of S1-1. | Fix with S1-1. | Reader 1 | Part 0 (coordinator) |

---

## S4 — noted, no action

- **Ch 7 §7.6 shows a full SQL query before SQL is taught.** Deliberate, announced ("You don't need to read SQL yet"), walked in plain words, hand-checked. It works for both readers.
- **Ch 1 §1.6 uses mean and median before Chapter 4 defines them**, each glossed in a clause. Fine.
- **Ch 4 §4.4's eleventh root and CAGR.** The one place "Numbers Without Fear" might frighten; the chapter says "You won't do it by hand" and gives the spreadsheet function. Fine.
- **Ch 9 §9.1's 34–43 hours for Chapters 12–13 against Chapter 6's one-month SQL block.** Already CPI-7.
- **"(In the finished book these move to Appendix G.)"** at the head of every answers section. Template-mandated; assembly removes it.
- **The first-appearance ledger raised 113 flags for these nine chapters.** After reading each one, eight are real (S3-2, S3-3, S3-4 and the companion-files pointer in S1-3); the rest are everyday words a bold happened to land on ("you", "exactly", "questions"). The filtered ledger is appended below; the tool now carries a stoplist so the whole-book run is cleaner. A flag is a place to read, and I read them.

---

## The overwhelm profile — Parts 0 and I

| Ch | Words | Key terms | Bold terms | Code / output blocks | Figures | Exercises | Sections | Time claimed | New tools to install |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 7,750 | 52 | 119 | 3 | 4 | 13 | 10 | 3–4 h | none |
| 2 | 9,122 | **75** | **170** | 12 | 4 | 15 | 9 | 4–5 h | text editor, password manager |
| 3 | 8,193 | 49 | 132 | 0 | 4 | 15 | 7 | 3–4 h | none |
| 4 | 8,273 | 36 | 89 | 0 | 4 | 15 | 10 | 4–5 h | calculator |
| 5 | 7,337 | 36 | 100 | 0 | 4 | 15 | 8 | 3–4 h | none |
| 6 | 7,131 | 34 | 103 | **15** | 3 | 15 | 9 | 3–4 h | **8: spreadsheet, PostgreSQL, MySQL, DBeaver, Python + venv + 4 packages, VS Code, Git, Power BI** |
| 7 | 9,481 | 31 | 90 | 4 | 5 | 15 | 8 | 2–3 h | none |
| 8 | **10,387** | 30 | 142 | 0 | 4 | 14 | 9 | 3–4 h (+2–3 project) | none |
| 9 | 7,026 | 20 | 103 | 0 | 4 | 14 | 8 | 2–3 h | none |
| **Total** | **74,700** | **363** | | | | **131** | | **27–36 h (+2–3)** | |

**The spike is Chapter 2.** Seventy-five key terms, the most in either part, immediately after Chapter 1's fifty-two, with the densest section (§2.1) first. See S2-4.

**The cliff is Chapter 6.** It is the first chapter that demands action, fifteen code blocks, eight tools, and it is followed by a flat stretch: Chapters 7, 8 and 9 are 27,000 words of orientation with no keyboard work at all (one shown query in Chapter 7). The reader who has just set everything up is not allowed to use it for three chapters. This is the reverse of "no rest after hard work": it is rest when momentum wanted to go. See the structural question.

**Chapter 8 is the longest sit in Parts 0–I** (10,387 words; the 17×10 skills matrix, the salary table, the pathways table). Reader 2's favourite; Reader 1's longest.

**Chapter 9 is the lightest (20 key terms) and the best placed:** it lands right before the work begins and tells the reader how to keep a log from Chapter 10.

**The time claims are internally consistent.** 27–36 hours for Chapters 1–9 matches Chapter 6's "month 1, Chapters 1–9" at 8 hours a week (32–35 hours). What the claims exclude is the nine projects (S2-3).

**On the 764–980 hours declared across Chapters 1–67:** not checkable until the reading reaches Chapter 83. Chapters 1–9 contribute 27–36 of it, which Chapter 9 §9.1 handles honestly by making the reader estimate with their own weekly hours. Whether the reader arriving at Chapter 83 is prepared for the total will be reported then.

---

## References that break at renumbering — Chapters 1–9

**169 references in these nine chapters point at a chapter that changes number at assembly.** By chapter: 1 (8), 2 (10), 3 (10), 4 (13), 5 (11), 6 (**52**), 7 (14), 8 (25), 9 (26). Chapter 6 alone carries a third of them, because it is the map to the tools.

Two things CPI-24 should know that its wording does not yet cover:

- **Part II and III targets dominate.** Old 12→13 (about 60 references), 13→14 (about 15), 16→19 (about 18), 17→15, 18→16, 14→17, 15→18, 19→12, 34→29, 30→33, 32→31: roughly 150 of the 169. References to Part VIII (73→74, 75→76, 77→79, 78→80, 81→83, 82→84, 83→85) are about 19. "Re-check every forward reference above 72" is the smaller half of the job for these chapters.
- **About fourteen are ranges that substitution cannot renumber:** "Chapters 10–13" (Ch 1, 5), "Chapters 12–13" (Ch 6, 8, 9), "Chapters 14–16" (Ch 6), "Chapters 17–18" (Ch 6), "Chapters 19–20" (Ch 6, 8), "Chapters 10–27" (Ch 8, 9), "Chapters 70–82" (Ch 7). Old 10–16 becomes new 10, 11, 13, 14, 17, 18, 19. Each must be rewritten as a list or re-expressed ("the spreadsheet and SQL chapters").
- **Every section reference moves with its chapter:** "section 12.3" (Ch 6 ×4, Ch 7), "section 12.10" (Ch 9 ×3), "section 12.15" (Ch 7), "section 13.3" (Ch 9).

The per-reference list is in the tool output (`python review/_journey_tools.py 1 2 3 4 5 6 7 8 9`) and will be regenerated for the whole book at the end of the reading.

---

## Promises checked — made by Chapters 1–9, verified in the chapter named

| Promise | Made in | Named chapter | Kept? | Evidence |
|---|---|---|---|---|
| "Turning that unstructured message into a structured order automatically … you'll build one in Chapter 58" | Ch 1 §1.7 | 58 | **Yes** | Ch 58 line 21: "This is the chapter Chapter 1 promised." |
| "Chapter 14 teaches how to find and fix these problems at scale" (§1.10's six faults) | Ch 1 §1.10 | 14 | Yes, in kind | Bombay→Mumbai mapping, Metro Mart similarity matching |
| "Chapter 20 takes this exact report [the Friday file] and automates it end to end" | Ch 2 | 20 | **No** | Ch 20 builds the Daily Sales Flash; Friday file and Imran absent from 19–20 (S1-2) |
| "Chapter 20 shows how to store [API keys] safely" | Ch 2 §2.8 | 20 | Yes | `os.environ` for SMTP host, user, password |
| "as Chapter 12 mentions, many companies give analysts read-only accounts" | Ch 2 §2.9 | 12 | Yes | one mention |
| "Chapters 19 and 20 automate the monthly report" | Ch 3 §3.7, Where-this-leads | 19–20 | **No, as stated** | the Flash is daily (S1-2) |
| "Chapter 25 maps Riverstone's order-to-cash process formally"; "Keep [the project] for Chapter 25" | Ch 3 | 25 | **Yes** | Ch 25 works on order 5001; Figure 25.2 is Figure 3.2 in swim lanes |
| Chapter 13's funnel 30 → 22 → 14 → 6; 43 CRM rows are 30 real enquiries | Ch 4 §4.8, Ch 5 story | 13 | Yes | Ch 13 Pattern table: "30 real enquiries, 20% won; 8 were never contacted" |
| "Chapter 12, section 12.10, explains this exact trap" (LEFT JOIN with a WHERE) | Ch 5, Ch 9 | 12 §12.10 | Yes | §12.10 is JOIN: combining tables |
| "Chapter 12, section 12.3, has full, tested steps for both databases" | Ch 6 §6.3 | 12 §12.3 | Yes | §12.3 Setting up your SQL laboratory, 1,265 words |
| "Chapter 16 also translates the ideas to Tableau and Looker" | Ch 6 §6.2 | 16 | Yes | seven mentions |
| "Chapter 12 … includes a version of it on the mini database (section 12.15)"; "Chapter 13 … Pattern 6" | Ch 7 §7.6 | 12, 13 | Yes | §12.15 exists; Pattern 6 is At-risk customers |
| "Chapter 81 covers … negotiating on CTC" | Ch 8 | 81 | In substance | negotiates offers; never uses CTC or in-hand (S3-6) |
| "Chapter 12 says 19–23 hours … Chapter 13 says 15–20 hours" | Ch 9 §9.1 | 12, 13 | **Yes, exactly** | both at-a-glance lines match |
| "Chapter 83 returns to … the plateaus of later years" | Ch 9 | 83 | Yes | §83.8 The plateaus that come later |
| Appendix B (install steps), E (companion files), G (answers) | Ch 6, 8, 9 | appendices | **No** | not written; known (README), consequence stated in S1-3 |

Two unkept, both the same cause: later chapters promising an earlier chapter's payoff without checking what that chapter built.

---

## Findability — Parts 0 and I

- **At-a-glance blocks:** every chapter has one, and they are good: abilities, not topics; honest hours; tools; data. The "Before you start" lines are accurate for these nine.
- **Key terms:** present and complete in all nine; 363 terms across Parts 0–I, all pointing at an unwritten Appendix A. Chapter 8's list includes three terms (leakage, data contract, architecture decision record) that appear only inside day-in-the-life vignettes with an in-line gloss; fine, but a reader looking them up in Chapter 8 will find a sentence, not a definition.
- **Recap and Where-this-leads:** present, specific, and (with the renumbering caveat) correctly targeted. Chapter 7's "Where this leads" is the best model: it names the chapter, the title, and what it does.
- **Cross-reference precision:** high. Section-level references (12.3, 12.10, 12.15, 13.3, 3.2, 3.5, 3.6, 3.7, 4.6, 4.7, 4.8, 4.10, 5.2–5.8, 6.3–6.9, 8.3–8.9) are used constantly and all resolve. This is a strength that the renumbering pass must protect.
- **What a front-of-book "if you already know X, start here" table must contain:** Chapter 8 §8.7 already is that table, with eleven rows by goal and three columns (read fully / skim / interview chapters). It needs to be at the front, with two additions: a row for "I already use spreadsheets at work" (start at Chapter 12, skim 10–11) and a row for "I already write SQL" (start at Chapter 17, skim 12–13), because those are the two most common Reader 2 profiles and neither is in the table. See S2-5.

---

## Character arcs — as far as Chapter 9

| Chapter | When the story is set | Meera | Farah | Others |
|---|---|---|---|---|
| 1 | undated ("her second day") | joins as sales coordinator; Mumbai customer count | — | Anita asks; Kavya (student) in the project |
| 2 | "before Meera joined" | — | on the CSV (order 5009) | Imran and the Friday file |
| 3 | 3 February 2026 | reconciles January's three numbers | 12% on Northgate needs Anita | Neha, Rahul, Vikram, Suresh, Rakesh |
| 4 | first week of January 2026 | checks Vikram's board slide | — | — |
| 5 | first week of January 2026 (story); 31 March 2026 (worked example) | tests Vikram's hire request | 64 orders, 5 leads, 0 missed | Neha 15 leads, 5 missed; Rahul 10, 3 |
| 6 | after February 2026 (cites Ch 3) | installs the toolkit; "wants to become an analyst properly" | — | — |
| 7 | "the year-end review" (data to 31 Dec 2025) | already fluent in SQL; writes the posting with Anita | — | Anita wants a data scientist |
| 8 | after the posting; "six weeks later" | coaches Farah | scores 13 of 28; builds the Monday email | Vikram asks for the same email |
| 9 | twelve weeks of SQL practice | Friday reviews with Farah | plateau at 6, then 9; first portfolio piece | — |

**Confirmed from the reading: CPI-6.** Chapter 6 has Meera starting SQL; Chapter 7, set earlier, has her fluent. The extension (S1-4) is that the dates run backwards across the Part 0 / Part I seam, and Chapter 1's story has no date to anchor the rest.

**Farah's arc is the strongest thread in the book so far** and nothing contradicts it: sales executive who knows the hospitality customers (Ch 3, 5, 8), 13 of 28 (Ch 8), twelve weeks and a plateau (Ch 9), and Chapter 9 says her first portfolio piece is the hospitality wedding-season question. CPI-25 (Chapter 76B calling her a Business Analyst) contradicts this arc and the reading confirms Chapter 8's arc is canon.

**Sunrise Caterers, as a customer, has an arc a reader can see and the book does not narrate:** regular in the first half of 2025, silent June–December 2025 (Ch 7), orders again on 19 February 2026 (Ch 2, 3), overdue and silent again in March (Ch 5). Consistent; never connected. A half-sentence in Chapter 7 ("the calls that followed brought Sunrise back in February") would turn a coincidence into a thread. S4 unless the author wants it.

**Name reuse in exercises** (Rahul, Neha in Chapter 8): S3-7, extends CPI-22.

**Imran, Kavya, Rakesh, Suresh, Vikram, Neha, Rahul, Anita:** consistent across all appearances in these chapters.

---

## The four explicit checks — status at Chapter 10

- **A. Reading order versus chapter numbers.** Chapters 1–9 are unaffected by the reorder themselves; their *references* into Part II are affected, 169 of them, listed above. The reading of Part II will be done in the map's order (10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20).
- **B. Chapters 25, 26, 27 and 83.** Not yet reached. Noted that Chapter 3's project and Chapter 25's map already agree (promise table).
- **C. The book ends twice.** Not yet reached.
- **D. The first two hundred pages.** Part 0 is reported above in more detail than anything else. The honest answer for Part 0 is: **a true beginner survives Chapters 1–5 comfortably and is most at risk in Chapter 6**, for the reasons in S2-1 to S2-3. Whether they survive Chapter 12 is the next batch's first question.

---

## Structural questions for the author

These are the findings whose smallest fix moves a chapter or a section between chapters. Stated and stopped, as instructed.

1. **Should Chapter 6 sit at the end of Part I rather than the end of Part 0?** Everything Chapter 6 installs is first used in Chapter 10. Chapters 7, 8 and 9 need nothing installed. Moving Chapter 6 to immediately before Chapter 10 would put the install one evening before its first use and let the orientation chapters be read on a phone. Chapter 9's Where-this-leads already points at Chapter 6 as "your study setup", which reads more naturally if Chapter 6 comes after it. The cost is one renumbering inside Part 0–I and a few cross-references.

2. **Should the installs be just-in-time at all?** The alternative to S2-1's labels is to keep Chapter 6 exactly as it is, on the author's stated reasoning. Both are defensible; the finding is that the current version costs the beginner an evening in month one for tools used in month five.

3. **Where should the database install steps live?** Chapter 12 §12.3 today; Appendix B eventually. Chapter 6 should point at whichever one exists when the book ships, and a beginner should not have to open Chapter 12 to find them.

4. **Should Chapter 8 §8.7 be duplicated at the front of the book, or moved there?** Duplicating keeps Chapter 8 whole; moving avoids two copies drifting.

---

## Method note

The reading was done in reading order with no editing, then the scripts, then the checks. Three scripts, all in `review/_journey_tools.py`: the overwhelm profile, the moving-reference audit against `chapter-map.md`'s old-to-new table, and the first-appearance ledger. The ledger's blind spot is that it flags any bold phrase, so its first run produced 113 flags of which eight survived a reading; a stoplist now removes the everyday words. The reference audit's blind spot is that it cannot tell a reference that will be correct after renumbering from one that will not: it lists every reference to a chapter whose number changes, and the renumbering pass decides. Every promise in the table above was verified by opening the chapter named, not by the promises file.

Next: Part II in reading order, starting at Chapter 10, with Chapter 12 read hardest.

---

## Appendix: the first-appearance ledger, Parts 0 and I

*Scripted: 437 bold terms across Chapters 1–9 after the stoplist; 42 used in plain text before the chapter that bolds them. Each was read at both places. Verdicts: **real** means a beginner meets the term with no gloss; **announced** means the earlier chapter names the later one; **table** means the term is defined in an earlier table the script does not read as prose; **sense** means a different meaning of the same word.*

| Term | First used | First bolded | Verdict |
|---|---|---|---|
| SQL, Python | Ch 1 | Ch 2, Ch 6 | **real** — S3-3 |
| CRM | Ch 1 (table), Ch 2 | Ch 3 | **real** — S3-4 |
| companion files | Ch 2 | Ch 6 | **real** — S1-3 (the term is fine; the address is missing) |
| curl, pandas | Ch 2 | Ch 6, Ch 17 | **real** — S3-2 |
| CSV, XML, PDF, Parquet, Excel | Ch 1 | Ch 2 | announced ("Chapter 2 introduces these formats") |
| Google Sheets, Power BI | Ch 1, Ch 2 | Ch 6 | tool names with a pointer to Chapter 10 / 16 |
| AI assistants, data analyst, business analyst, data engineer | Ch 1, Ch 2 | Ch 7 | everyday role names; Chapter 7 defines them |
| dashboard(s), e-commerce, integration | Ch 1, Ch 2 | Ch 3 | everyday; Chapter 3 defines |
| unzip | Ch 2 | Ch 6 | a verb |
| model | Ch 1 | Ch 7 | sense: "DIKW model" |
| pipeline | Ch 3 | Ch 7 | sense: "sales pipeline" |
| tree, track | Ch 3 | Ch 7 | sense: "KPI tree" |
| percentiles | Ch 4 | Ch 8 | announced (Chapter 21) |
| machine learning | Ch 5 | Ch 8 | one mention, in context |
| portfolio, retrieval | Ch 6 | Ch 9 | announced ("Chapter 9 explains why this works") |
| AI / analytics / ML engineer, BI developer | Ch 7 | Ch 8 | table: defined in Chapter 7 §7.2 |
| career tree, skills matrix, reader pathways, day in the life, entry routes, tiers, plateaus, mentors | Ch 7, Ch 8 | Ch 8, Ch 9 | announced in Where-this-leads |

---
---

## Part II (Chapters 10–27) — appended after the reading of Part II, 22 September 2026

*Read in the map's order: 10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20, 21, 22, 23, 24, 25, 26, 27. Same two readers, same severity scale, same rule: every finding names a cause, proposes the smallest fix, and stops where the fix is structural. Numbering of findings continues from Parts 0–I (S1-5 onward). Nothing here re-reports a cross-part issue; "extends CPI-n" marks the ones it touches.*

**Scope of this part.** 225,950 words of chapter body (about 250,000 with the answer sections), eighteen chapters, 1,015 key terms, 466 exercises, 18 projects, 8 timed challenges, 290–357 hours claimed. It is the heart of the book and, on the whole, it is very good: the numbers reconcile across chapters to the paisa, every "In plain English" analogy is real, and Chapters 13, 22, 23 and 27 are as strong as anything in Part 0. The problems are almost all *seams*: the reading order was decided on 17 September and applied to the map and to one chapter header, and the eighteen chapters still talk to each other in the old order, in three different numbering states, and in some places with chapter titles that no longer exist.

### Summary — Part II

**The three things that most damage the reader's journey in Part II, in order**

1. **The reading order breaks the declared prerequisites of the three chapters it moved, and the text of those chapters was never told.** Chapter 19 opens with *"Before you start: … Chapter 14 (cleaning), Chapter 15 (charts)"* and its practice files are "built from Chapter 14's clean Q4 data". Chapter 17 opens with *"Chapter 16 turned the answers into a report that refreshes itself"* and leans on Chapter 14 as known material twelve times. Chapter 18 requires 14 and 15, reconciles to "Chapters 15 and 16 exactly", and §18.10 "rewrites Chapter 14's cleaning pipeline". In the decided order the reader reaches all three *before* 14, 15 and 16. Meanwhile Chapters 14 and 15 do not need Python (their pandas sections are marked "read this as a preview"), and Chapter 16's only use of the word pandas is the sentence saying pandas is assumed. The full dataset the rest of the book runs on is formally introduced in Chapter 14 §14.1 ("From this chapter on…") and first used, unannounced, in Chapters 19 and 18. (S1-5, and structural question 5.)

2. **The plan in Chapter 6 is short by about half.** Part II's own at-a-glance hours add up to 290–357; with Parts 0–I that is 317–393 hours for "the analyst path". Figure 6.2 gives it six months at 8 hours a week, which is 208. At the book's own numbers the six-month plan is a nine- to eleven-month plan. CPI-7 found this for the SQL month; the reading finds it for the whole path. A Reader 1 who trusts the figure will conclude in month four that they are slow. (S1-7, extends CPI-7.)

3. **Six "Where this leads" bullets send the reader to chapters that are something else.** "Chapter 23, Data Storytelling" (16, 20, 22), "Chapter 24, Forecasting" (21, 22), "Chapter 25: experimentation in practice" (22), "Chapter 27: the ethics of analysis" (22), the "Case Study & Guesstimate bank (Chapter 74)" (23), the "Behavioral & Case Interview bank (Chapter 75)" (24). Chapter 23 is Business Acumen, 24 is Requirements, 25 is the BA track, forecasting is Chapter 40, 74 is the machine-learning bank, 75 is Product Sense, and the behavioral bank is 81. These are not renumbering errors: the numbers are the current ones and the titles are from an earlier plan, so the CPI-24 substitution pass will leave every one of them wrong. (S1-8.)

Behind those three: Chapter 18 prints three Python errors as if they were outputs (S1-6); Chapter 23 commits the duplicate-leads mistake that Chapter 13 teaches, on the same table, and gets a different funnel (S1-9); Chapter 27's pointers into Part II land on the wrong section ten times out of nineteen (S2-8); and Meera personally rescues Riverstone eight times in January 2026 (S2-9).

**What Part II does unusually well, so the repair does not destroy it**

- **The numbers hold across eighteen chapters.** ₹4,335,471 and 173 orders (Ch 10, 11, 13, 17); ₹423,561,010.50 cleaned and ₹311,797.50 quarantined (Ch 14, 18); ₹1,146,641,651.25, 46,356 orders, 4,599 customers, ₹24,735.56, 27.5% (Ch 16, 18, 23, 27); the branch league table (Ch 14) reconciles to the regional totals (Ch 16) once the twenty quarantined lines are added back. A reader who checks is right every time, which is what makes Chapter 27's "reconcile to a number you trust" credible.
- **Chapter 12 is the right first SQL chapter for a beginner.** Filing cabinets, a twelve-order database the reader can check by eye, every calculation hand-checked, every trap shown wrong first (AND/OR, `= NULL`, the fan-out, the LEFT JOIN that became an INNER JOIN), and a Monday-morning finale that reconciles four answers to one total.
- **Chapter 13's pattern library and Chapter 27's capstone are the two best-argued chapters in the book so far.** Chapter 27 in particular does the thing the coherence pass exists to protect: it shows the flattering answer, then the check that kills it, then the memo that says so.
- **Chapters 21–24 are written for Reader 1 and do not condescend to Reader 2.** Every formula twice, every p-value with an effect size, every statistic turned into a sentence a manager can act on.
- **Chapters 14, 15 and 16 were written *for* the reading order.** Their Python sections are labelled previews; Chapter 16's header names the order. They are the model for what 17, 18 and 19 need.
- **The two chapters written last (25, 26) are the most compliant with §6.5**: settings tables, line-by-line walks, one measured what-if each. Chapter 27's settings table for `band_cut` is exactly what the standard asks for.

### S1 findings — Part II

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S1-5 (extends S1-1, CPI-24) | Ch 19 at-a-glance and Practice data; Ch 17 "Why this matters" (line 21), §17.5, §17.7, §17.8, §17.11, §17.12 ×2, §17.13 ×2, mistakes table, story, ex. 27 (twelve references to Ch 14, two to Ch 16); Ch 18 at-a-glance, §18.2, §18.3, §18.5, §18.6, §18.9, §18.10, §18.11, Tools, exercises (seventeen references to Ch 14, eight to 15, five to 16); Ch 14 §14.1 "The data for this chapter" | Reader 1, following the map, reaches Chapter 19 and is told to have done 14 and 15 first; reaches 17 and is told what Chapter 16 built; reaches 18 and is asked to reproduce "Chapter 14's pipeline" on "Chapter 14's messy export" and to check against "Chapter 15's figures". Also meets the 209,006-line, ₹278-crore dataset in Chapter 19 (25,832 rows, ₹423.9 million) and Chapter 18 (`../full/orders.parquet`, 116,194 orders) with no introduction: the paragraph that introduces it is in Chapter 14. | The 17 September decision (chapter-map.md, "Reading order decided") moved 19 before Python and 14–16 after it "so all tools come together". Chapters 14 and 15 already worked before Python (§14.13 and §15.14 say "if you haven't reached them yet, read this as a preview"); Chapter 16's header was rewritten ("The Python block comes before this chapter in the reading order, so pandas is assumed knowledge where it appears") but the chapter never uses pandas. Chapters 17, 18 and 19 were approved on 18 September, after the decision, without the corresponding rewrite. Verified by grep: Ch 17 has 12 "Chapter 14" mentions, Ch 18 has 17, Ch 19 has 3 and a data dependency. | **Smallest fix is structural: structural question 5.** The textual alternative is about forty-five sentences across 17, 18 and 19 rewritten as forward references ("Chapter 14 will…"), §18.10 either moved into Chapter 14 or reframed as the reader's first sight of the messy export, and a "Meet the full Riverstone" box placed at the first use of the full dataset in reading order (Chapter 19). | Reader 1 | Coordinator (order); Part II-A (text) |
| S1-6 | Ch 18 §18.8 (two code blocks), §18.12 read-back block | Types `pd.pivot_table(sales2025, index="segment", columns=sales2025["order_date"].dt.quarter, …)` and gets `TypeError: unhashable type: 'Series'`, printed in the book as the output. The next block prints `NameError: name 'pivot' is not defined`. §18.12's "read it back, which is how you check an export" prints `KeyError: 'net_revenue'` (the header row was retitled to "Net Revenue"). The pivot and melt section teaches nothing, and the reader's first thought is that their pandas is broken. | The verifier captured stderr as output and the outputs were pasted without being read. The chapter's own rule ("read every line of anything you keep") was not applied to its own outputs. Fable B's lane, reported here because it stops a Reader 1 dead. | Fix the three cells (a `quarter` column before the pivot; keep `pivot`; read back with `header=2` and the retitled names) and re-run; the settings-table pass on Chapter 18 should re-read every output block. | Both | Part II-A chat / Fable B |
| S1-7 (extends CPI-7) | Ch 6 Figure 6.2 and §6.8; every Part II at-a-glance "Time needed" | Reads "about 8 hours a week for 26 weeks" for Parts 0–II. The chapters claim 27–36 hours (Parts 0–I) plus 290–357 (Part II): 317–393 hours, or 40–49 weeks at 8 hours. Month 2 (Chapters 10–11) alone claims 39–47 hours against 32 available; month 5 (17, 18, 21, 22) claims 85–101. | Each chapter's hours were set by its author; nobody summed them against the plan. CPI-7 caught the SQL month (34–43 hours against 32). The whole path is short by a factor of about 1.7. | Either redraw Figure 6.2 as nine to eleven months at 8 hours a week (Chapter 6 already says "at 5 hours a week, stretch it to nine or ten months", so the wording exists), or print the chapter hours on the figure so the reader can see the arithmetic; or revisit the per-chapter claims (Chapters 17 and 18 at 25–30 and 30–35 hours for 9,700 and 9,200 words look high; 25, 26 and 27 at 5–7, 6–8 and 8–12 for 10,500 words each look low). The first is the smallest. | Reader 1 | Part 0 (coordinator) |
| S1-8 | Ch 16 Where-this-leads bullet 2; Ch 20 bullet 2; Ch 21 bullet 4; Ch 22 bullets 1, 2, 3, 4; Ch 23 last bullet; Ch 24 last bullet | Is sent to "Chapter 23, Data Storytelling" (it is Business Acumen; storytelling is Chapter 24), "Chapter 24, Forecasting" (Requirements; forecasting is Chapter 40), "Chapter 25: experimentation in practice" (the BA track; experiments are old Chapter 30), "Chapter 27: the ethics of analysis, including selective reporting" (the capstone, which does keep the selective-reporting promise in §27.8), the "Case Study & Guesstimate bank (Chapter 74)" (74 is the machine-learning bank; case studies are 75), and the "Behavioral & Case Interview bank (Chapter 75)" (75 is Product Sense; behavioral is 81). | These chapters' closing lists were written against an earlier chapter plan in which 23 was storytelling, 24 forecasting, 25 experimentation and 27 ethics, and in which Part VIII's banks sat one number lower. The numbers survived, the titles did not, and nothing in CPI-24's substitution can detect a right number with a wrong title. | Rewrite the six bullets to the chapters that exist: 16 and 20 → "Chapter 24, Requirements, Storytelling & Stakeholders"; 21 and 22 → "Chapter 40, Time Series & Forecasting"; 22 → "Chapter 30, Inference & Experiments" and "Chapter 27, the capstone, which returns to selective reporting"; 23 → Chapter 75; 24 → Chapter 81. Eight lines. | Both | Part II-A and II-B chats |
| S1-9 (touches CPI-14) | Ch 23 §23.5, table rows "Win rate" and "Conversion by stage", the paragraph "Two-thirds of Riverstone's 43 leads…", answer 9, timed-challenge bonus | Reads that Riverstone had 43 leads, a 14% win rate, and "21 of 43 never get contacted". Ten chapters earlier, Chapter 13 Patterns 3 and 4 showed the same table holds 13 duplicate submissions, that the real funnel is 30 → 22 → 14 → 6, and that counting 43 "would drop the win rate from 20% to 14%, blaming the sales team for a website glitch". Chapter 23 makes exactly that report. | Chapter 23 reads `leads.parquet` raw; Chapter 13 deduplicated on `LOWER(email)` before counting. The two chapters were written by different chats against the same file, and the second did not read the first's pattern. | Add the deduplication (one `drop_duplicates` on the lower-cased email, or Chapter 13's CTE) to §23.5 and update the four numbers, the "two-thirds" sentence (27 of 43 website leads includes the duplicates), answer 9 and the bonus; or, if 43 is kept on purpose, say in one sentence that it includes 13 duplicate submissions and why the marketing view counts them. The first is right. | Both; Reader 2 will notice first | Part II-B chat |

### S2 findings — Part II

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S2-7 (extends CPI-24) | Ch 17 §17.13 table, project stretch, Where-this-leads; Ch 18 §18.15, Where-this-leads; Ch 20 Where-this-leads; Ch 16 §16.13 and Where-this-leads; Ch 26 Where-this-leads; Ch 27 Where-this-leads; Ch 25 Where-this-leads; Ch 14, 15, 20, 23, 24 (and 1, 3, 5, 75, 81) | Part II cites the same chapters in three numbering states. *Old numbers, current titles* (most references). *New numbers already applied:* "Chapter 30, Python as Software" in 17, 18, 20 and "Chapter 31, Analytics Engineering with dbt" in 16, while 26 and 27 call the same chapters 29 and 32 (their file numbers). *Unresolvable:* "the Business Analyst bank (Chapter 76)" in eleven places, against "Chapter 76B" in Chapter 25 and "76A" elsewhere; after renumbering, 76A is 77 and 76B is 78, and a bare "76" cannot be mapped. | The Python and dbt references were written after the map's "old → new" table existed and used the new numbers; everyone else used file numbers. The bare "Chapter 76" predates the split into 76A and 76B. | Before the substitution pass: list every reference that already carries a new number (five found in Part II: `grep -n "Chapter 30, Python\|Chapter 31, Analytics"`), and exclude them; resolve each bare "Chapter 76" by hand (the BA bank is 76B → 78 in every Part II case). The moving-reference list below is the input. | Both | Coordinator at assembly |
| S2-8 | Ch 27 §27.2 (two), §27.3 (two), §27.4 (two), §27.5 (two), §27.6, ex. 11 | Follows the capstone's pointers back into Part II and lands in the wrong place ten times out of nineteen: "Chapter 13 section 13.4 explains why BETWEEN on a timestamp…" (it is Chapter 12 §12.5; 13.4 is ranking); "Chapter 13's fan-out trap" (Chapter 12 §12.10); "Chapter 14 section 14.9 called the cleaning log" (§14.10; 14.9 is validation rules); "Chapter 14 section 14.5 built the matching" (§14.4; 14.5 is categories); "`NTILE(4)` is Chapter 13 section 13.7's window function" (NTILE is taught nowhere in 12–13; Chapter 21's tools line also credits it to Chapter 13); "Chapter 22 section 22.2 is precise about what [a confidence interval] means" (§22.1); "Chapter 22 section 22.3 warned … significance is a statement about sample size" (§22.8); "Chapter 18 section 18.3 shows [string date comparison] going wrong quietly" (18.3 is profiling; nothing there does); "Chapter 15 section 15.6: the title is the finding" (§15.11; 15.6 is scatter plots); "Chapter 17 section 17.8 introduced [`if __name__`]" (§17.14; 17.8 is conditions); "Chapter 22 section 22.6 is the relevant material [for designing the test]" (§22.3; 22.6 is Simpson's paradox). | Chapter 27 was written in the coordinator chat on 21 September from an outline of Part II rather than the approved texts. A scripted check of every other Part II chapter (`review/_section_refs.py`, cross-chapter pointers only) finds all ~60 of theirs resolve to the heading they promise; Chapter 27's are the only wrong ones in the part. | Ten pointer edits, listed above; add a one-line "NTILE is new here" gloss or use `ROW_NUMBER`-based quartiles. Re-run the script after. | Both; Reader 2 loses trust in the capstone | Coordinator chat |
| S2-9 (extends S3-8, CPI-6) | "In the real world" of Ch 10, 11, 13, 14, 15, 24; also 22 | Meets Meera in "the second week of January 2026" (Ch 10, the two Januaries), "the first week of January 2026" (Ch 11, the month-end pack; Ch 15, the October collapse), "6 January 2026" (Ch 14, the branch league table), "January 2026" (Ch 13, the board review; Ch 22, the transporter), and 3–8 January (Ch 24, the December memo). Eight separate rescues by one person, for the same two managers, in about ten days, each ending in a process change. Then February 2026 in 16, 20, 23, 26 and 27 (memo dated 12 February). | The Part II stories were written by different chats, each picking the first plausible date after the 2025 data ends. Individually every story is good; read in order they make Meera a superhero and January 2026 a month with no other work. | Stagger across January–April 2026 (the data supports it: Chapter 12's "today" is 31 March 2026, Chapter 25's project is March). A story-date table is in the character-arc section below; the coordinator can assign months from it in ten minutes. | Reader 1 | Coordinator |
| S2-10 | Reading order 11 → 19 → 12 → 13 → 17 → 18; Ch 12 §12.13 | Enters a six-chapter stretch claiming 25–30, 20–25, 19–23, 15–20, 25–30 and 30–35 hours (134–163 hours) with no light chapter, where the old order gave 14 (20–25) and then 15 (12–15) as a breather. Inside it, Chapter 12 is 29,200 words (32,000 with answers) with 249 code and output blocks, and §12.13 alone is 8,000 words of DDL in two dialects, in a chapter whose header says "you do not need any programming experience". Chapter 11 has 43 exercises and a thirty-minute championship case. | The order was chosen for dependency, not for pace; §12.13 was expanded when MySQL was added as a second track. | Two labels, no rewriting: at the top of §12.13, "First time through, do the PostgreSQL column only; come back for MySQL when you need it", and in Chapter 13's header, "If Chapter 12 took longer than three weeks, do Patterns 1–4 now and 5–10 later." If the order changes (structural question 5), 15 lands between 14 and 16 and the stretch breaks naturally. | Reader 1 | Part II-A |

### S3 findings — Part II

| # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |
|---|---|---|---|---|---|---|
| S3-10 | Ch 12 "Why this matters" line 23; Ch 11 Where-this-leads; Ch 13 Where-this-leads; Ch 17 "starts from zero" | Chapter 12 opens "In Chapters 10 and 11 you worked with spreadsheets" the day after the reader finished Chapter 19; Chapter 11's closing list names 12 as next, not 19; Chapter 13's closing list names 14, 16, 20 and 28 and never 17, which is next; Chapter 17 says it "starts from zero: what a variable is, what a loop is", although the map moved Chapter 19 before it precisely so that the reader would meet variables, `If` and loops in VBA first (§19.4), and Chapter 19's header says so ("before the Python block"). | Every seam in Part II was written to the old sequence; only Chapters 19 and 16 know the new one. | One sentence each: Ch 11 and 13 add the next chapter to their lists; Ch 12 says "and in Chapter 19 you automated one"; Ch 17 §17.1 or §17.5 says "if you did Chapter 19, you have met variables, conditions and loops in VBA; Python's are the same ideas with less ceremony". | Reader 1 | Part II-A |
| S3-11 | Ch 12 §12.13 Step 1, `pg_database` listing | Runs `SELECT datname FROM pg_database WHERE datname LIKE 'riverstone%'` and gets two rows; the book shows three, including `riverstone_2025`, which the reader creates in Chapter 13 §13.1. | Output captured on the author's machine after Chapter 13's setup. | Show two rows, or add "(and `riverstone_2025` once you reach Chapter 13)". | Reader 1 | Part II-A |
| S3-12 | Ch 11 §11.8 (line 1149); Ch 6 §6.1 and story (lines 454, 529) | Chapter 6 tells the Mac reader "The Mac can run everything except Power BI Desktop". Chapter 11 §11.8 then says Power Pivot is Windows-only too ("Power BI Desktop is *also* Windows-only"), so the Mac reader loses §11.8 and the DAX first taste without having been warned. | Chapter 6's tool survey did not check Power Pivot's platform. | One clause in Chapter 6 §6.1: "except Power BI Desktop and Excel's Power Pivot (Chapter 11 §11.8)". | Reader 1 on a Mac | Part 0 |
| S3-13 | Ch 14 §14.3, "Missing values in each tool" table header | Column header "pandas (section 14.11)". §14.11 is the Power Query pipeline; pandas is §14.13. | Section added later; header not updated. | "section 14.13". | Both | Part II-A |
| S3-14 | Ch 20 §20.8, "Say what to do" bullet | The sample alert reads "Storage Box 25L sold 345 units (below 500)"; the table beside it shows the Industrial Crate at 345 and Storage Box 25L at 575 (above the line). | Illustrative text written before the query was run. | "Industrial Crate sold 345 units". | Reader 2 | Part II-A |
| S3-15 (softens S1-2) | Ch 12 "In the real world" last paragraph; Ch 13 project stretch | "Chapter 20 takes this exact query and turns it into a Daily Sales Flash." Chapter 20's Flash queries the day's order lines and the last fourteen days; the monthly sales summary is not scheduled anywhere. Chapter 13's stretch goal says the same of the headline-numbers query. The promise is kept in kind, not "exactly". | Same cause as S1-2: earlier chapters promising what Chapter 20 would build. | "a query of exactly this kind". | Reader 1 | Part II-A |
| S3-16 | Ch 24 at-a-glance Tools, §24.1 last paragraph, §24.4, §24.6, §24.9 | Is told every example uses "Chapter 23's December 2025 revenue diagnosis" and "Chapter 23's own worked example … why did December fall from November". Chapter 23's worked example (§23.11) is May → June; November → December is the answer to exercise 13. The numbers Chapter 24 uses (−₹1.26, −₹1.06, −₹4.55 crore) are right; the pointer is wrong. | Chapter 23's worked example was switched to the June trough and Chapter 24 was written to the December one. | Either Chapter 24 says "Chapter 23's exercise 13" and "the same method as §23.11", or Chapter 23's §23.11 becomes November → December (it is the larger fall). | Both | Part II-B |
| S3-17 | Ch 23 §23.2 and throughout ("FY2025"); Ch 16 §16.3, ex. 23 | Chapter 16 defines the Indian financial year (FY2026 runs from 1 April 2025) and computes "FY2026 revenue to 31 December 2025". Chapter 23 then calls calendar 2025 "FY2025" (revenue ₹1,146,641,651 is the calendar-year figure). | Two chats, two conventions. | Chapter 23 says "calendar 2025" or "CY2025", once, and drops "FY" from the table; or the financials file states that Riverstone reports on calendar years. | Reader 2 | Part II-B |
| S3-18 | Ch 14, 15 ("Python 3.12"); Ch 17, 18, 20–23 ("Python 3.13 or 3.14", then "run here on 3.12"); Ch 26 answer 10 and Ch 27 ("Python 3.11") | Three different Python versions are named as the book's version, sometimes two in one chapter. | Each chapter states what its author installed. | One sentence in Chapter 6 §6.3 or Chapter 17 §17.2 ("any Python from 3.11 works; the book's code was checked on 3.12") and the others defer to it. | Reader 1 | Coordinator |
| S3-19 | Ch 14 §14.2 (first regex at line 150, `!~ '^[0-9]+$'`) through §14.7 | Meets `~`, `!~`, `^[0-9]+$`, `regexp_replace` twenty times in the profiling section before the sentence "The regular expression decides the format" in §14.7. In reading order the phrase "regular expression" has appeared once before (Chapter 11's tool-roadmap line); Chapter 17 §17.13 later calls `re` "Chapter 14's patterns", so Chapter 14 is where the book means to teach it. | The explanation sits with the date parsing, not with the first use. | One clause at the first use in §14.2 ("`~` tests text against a *regular expression*, a pattern: `^[0-9]+$` means 'only digits, start to end'"). | Reader 1 | Part II-A |
| S3-20 | Ch 12 §12.13 (line 1777) → Ch 64 | "DCL (Data Control Language: `GRANT` and `REVOKE`) … Chapter 64 covers it." Chapter 64 covers least privilege and authorization and never uses `GRANT`, `REVOKE` or DCL. Kept in substance, like S3-6. | Vocabulary promised in Part II not carried into Part VII. | Chapter 64 names `GRANT`/`REVOKE` once where it says least privilege, or Chapter 12 says "Chapter 64 covers who may do what". | Reader 2 | Part VII |
| S3-21 | Ch 23 §23.6 marketing table; §23.5 | Reads that marketing produced "5,650 leads → 767 new customers" two pages after the CRM's 43 leads, in the same chapter, with the same word. The chapter says the marketing data is invented and that most revenue never enters the CRM pipeline, but never reconciles the two lead counts. | Two sources, one term. | One sentence: "marketing's leads are web and campaign responses; the CRM holds the 43 that reached a salesperson". | Both | Part II-B |
| S3-22 | Ch 16 §16.8 and story ("91 customers with no city"); Ch 14 §14.3, Ch 18 §18.3 ("100 customers with no city") | Two different counts for the same fault. Both are right (100 records in the customer table; 91 of them ordered in 2025), and neither chapter says so. | Different populations, same sentence. | "91 of the 100 customers with no city ordered in 2025" in Chapter 16. | Reader 2 | Part II-A |
| S3-23 | Ch 25 §25.6 (FR-01, "1.5 times their own average gap"); Ch 13 Pattern 6 ("more than twice the usual gap") | The BA chapter specifies the at-risk dashboard that Chapter 13 Pattern 6 already built as a query, with a different multiplier, and never points at it. | Written in a different chat; Chapter 25 draws on Chapter 3, not 13. | One pointer ("the rule Chapter 13 Pattern 6 implemented") and either the same multiplier or a sentence on why the requirement changed it. | Reader 2 | Coordinator chat |
| S3-24 | Ch 25 story ("Ayesha Qureshi, who had moved into a business analyst role from the customer support desk eighteen months earlier") | A new named Riverstone employee, in the last-written chapter, who appears nowhere else and is not in `riverstone-bible-additions.md`. Sandeep Gill, Arjun Nair, Pooja Desai and Simran Kaur (Ch 14, 15, 16) are in the bible; Ayesha is not. | Chapter 25 was drafted after the bible additions. | Add her to the bible (role, tenure), or make her Meera (Chapter 25 §25.1 already says Meera does all four roles at Riverstone). | Both | Coordinator |

### S4 — noted, no action (Part II)

- **Grammar slips in pointers:** "Chapter 21 and 22" (17, 18, 20), "Chapter 10 and 11" (15), and "Chapter 23 section 13" / "Chapter 25 section 10" (25 ×2, 26) where every other chapter writes "section 23.13". Copy-edit.
- **Ch 26 "Twenty-one chapters of this book point here."** Unverifiable and not worth verifying; "many chapters".
- **Ch 23 §23.13 "excluding the mini-database's Q1 2026 test data."** The mini database is a separate database, not test rows inside `riverstone_full`; a Reader 2 pauses. Delete the clause.
- **Ch 19's monthly totals sum to ₹423,872,808.75 against a stated ₹423,872,808.00.** Rounding of each month; Chapter 15 exercise 18 explains the same 75 paise. Fine.
- **Ch 19's VBA, Office Scripts and Apps Script were not executed; Ch 20's SMTP, webhooks and schedulers were not executed.** Both chapters say so plainly in their Tools notes. Honest; Fable B's lane.
- **Ch 12 §12.4–12.12 carry eight Dialect notes and eleven Watch-outs.** Boxed and skippable; a beginner on the PostgreSQL path is not harmed. The two-dialect problem is §12.13 only (S2-10).
- **The ledger raised 458 flags for Part II.** After reading, the real ones are the Part II-before-Part II terms already covered by S1-5 (UTC, normalize, mapping table, branch sales offices, action title, attainment) and the regex in S3-19; the rest are announced (window function, star schema, fact table and time intelligence in Chapter 11 §11.8 with a pointer to 13 and 16; DataFrame in 17; confidence intervals in 21; BRD/FRD/SRS in 24; Scrum/Kanban in 25) or everyday words. Appendix below.

### The overwhelm profile — Part II, in reading order

| Ch | Words (body) | Key terms | Bold terms | Code / output blocks | Figures | Exercises | Sections | Time claimed |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 10 | 17,873 | 71 | 371 | 26 | 5 | 29 | 15 | 14–17 h |
| 11 | **24,044** | **87** | **451** | 60 | 8 | **43** | 14 | 25–30 h |
| 19 | 10,531 | 67 | 130 | 33 | 0 | 28 | 15 | 20–25 h |
| 12 | **29,199** | 81 | 323 | **249** | 5 | 29 | 16 | 19–23 h |
| 13 | 14,242 | 44 | 109 | 63 | 4 | 16 | 8 | 15–20 h |
| 17 | 9,747 | 76 | 129 | 79 | 3 | 30 | 15 | 25–30 h |
| 18 | 9,163 | 64 | 104 | 85 | 0 | 30 | 16 | **30–35 h** |
| 14 | 15,974 | 52 | 245 | 85 | 4 | 30 | 13 | 20–25 h |
| 15 | 12,687 | 58 | 252 | 14 | **15** | 25 | 14 | 12–15 h |
| 16 | 10,995 | 63 | 214 | 20 | 6 | 27 | 13 | 18–22 h |
| 20 | 8,389 | 60 | 142 | 19 | 4 | 27 | 14 | 18–22 h |
| 21 | 7,421 | 55 | 97 | 34 | 4 | 29 | 9 | 15–18 h |
| 22 | 7,359 | 50 | 98 | 32 | 4 | 29 | 9 | 15–18 h |
| 23 | 9,348 | 58 | 92 | 23 | 4 | 27 | 13 | 15–18 h |
| 24 | 7,066 | 14 | 87 | 0 | 4 | 22 | 9 | 10–12 h |
| 25 | 10,567 | 43 | 147 | 0 | 5 | 15 | 12 | 5–7 h |
| 26 | 10,576 | 50 | 81 | 22 | 3 | 15 | 11 | 6–8 h |
| 27 | 10,769 | 22 | 62 | 17 | 3 | 15 | 11 | 8–12 h |
| **Total** | **225,950** | **1,015** | | | | **466** | | **290–357 h** |

*Words exclude the answers sections (the whole files are about 250,000). Chapter 12's file is 32,300 words with answers.*

**The wall is the first six chapters.** 11, 19, 12, 13, 17, 18: 97,000 words and 134–163 claimed hours before the first chapter under 15 hours. Chapter 11 is the longest sit after 12 and carries the most key terms, the most bold terms and the most exercises in the book so far, and it comes second. Chapter 12 has 249 code and output blocks, ten times Chapter 10's. See S2-10.

**The relief is Chapters 15 and 24.** Twelve to fifteen hours and fourteen key terms respectively; both are placed where a reader needs them least under the current order (15 after the wall, 24 after the statistics).

**The time claims do not fit the plan** (S1-7). They are also uneven relative to length: 17 and 18 claim 25–35 hours for under 10,000 words each (programming is typed, which the chapters say, so this may be right); 25, 26 and 27 claim 5–12 hours for 10,500 words each plus a project that Chapter 27 itself budgets at "a week, not an evening".

**On the 764–980 hours declared across Chapters 1–67:** Parts 0–II contribute 317–393. The remainder is checked at Chapter 83.

### References that break at renumbering — Part II

**433 references in these eighteen chapters point at a chapter that changes number at assembly** (Parts 0–I: 169; running total 602). By chapter: 10 (31), 11 (51), 19 (19), 12 (15), 13 (28), 17 (30), 18 (**59**), 14 (20), 15 (19), 16 (40), 20 (24), 21 (12), 22 (6), 23 (11), 24 (5), 25 (12), 26 (20), 27 (31).

- **Targets are overwhelmingly inside Part II:** old 14→17 (about 25 references), 18→16 (16), 16→19 (12), 13→14 (14), 15→18 (10), 19→12 (7), 12→13 (12), 17→15 (11); Part III targets 30→33, 32→31, 34→29 (about 10); Part VIII targets 82→84 and 76→77/78 (about 15). As in Parts 0–I, "re-check every forward reference above 72" is the smaller half.
- **Three references are ranges:** "Chapters 12–13" (17, 18, 26). Old 12–13 is new 13–14, so these survive as ranges by luck; the pass should still check.
- **Section references move with their chapters:** "section 14.3" (×4), "section 14.5" (×2), "section 13.2" (×2), "section 12.9" (×2), "section 12.16" (×2), "section 18.13", "section 18.14", "section 16.10", "section 12.3", "section 12.11", "section 12.15", "section 13.8", "section 11.8" and the rest listed in the tool output. About forty in Part II.
- **Three numbering states coexist** (S2-7): five references already carry the new number; eleven bare "Chapter 76" references cannot be mapped at all.
- **Six references have the right number and the wrong title** (S1-8) and will survive the substitution pass unchanged and wrong.

The per-reference list: `python review/_journey_tools.py 10 11 19 12 13 17 18 14 15 16 20 21 22 23 24 25 26 27`.

### Promises checked — made in Parts 0–II, verified in the chapter named

| Promise | Made in | Named chapter | Kept? | Evidence |
|---|---|---|---|---|
| Ch 1's "check what a cell really contains"; ₹4,335,471 and 173 orders | Ch 1, Ch 10 | 10, 11, 13, 17 | **Yes, to the rupee** | Ch 13 §13.6 (173, ₹4,335,471); Ch 17 project step 8 and answer 17; Ch 14 §14.1 |
| Chapter 13 builds CTEs, window functions, `RANK()` for ties, `ROW_NUMBER()` for latest-per-group | Ch 12 §12.7, §12.10, §12.12 | 13 | Yes | §13.2, §13.4 |
| "Chapter 20 takes this exact query and turns it into a Daily Sales Flash" | Ch 12 story | 20 | In kind, not "exactly" | the Flash queries the day and the last fourteen days (S3-15) |
| Normalization's formal rules, recursive CTEs, query plans | Ch 12 §12.1, §12.11; Ch 13 §13.8 | 28 | Yes | Ch 28: 12 "normal form", 48 "recursive" mentions |
| ACID | Ch 12 §12.13 | 49 | Yes | 9 mentions |
| DCL: `GRANT` and `REVOKE` | Ch 12 §12.13 | 64 | In substance | least privilege and authorization; the words never appear (S3-20) |
| Chapter 14 is where regular expressions and cleaning are taught | Ch 17 §17.13 | 14 | Yes, unlabelled | §14.7 explains; §14.2 uses first (S3-19) |
| ₹423,561,010.50 from the messy export, "three tools, one answer" | Ch 14 §14.10 | 18 §18.10 | **Yes, to the paisa** | 25,832 lines, 20 quarantined, same total |
| Chapter 15's medians and October's 22.7% | Ch 15 §15.4, §15.5 | 18 §18.9, §18.11 | Yes | 25,762 / 19,425 / 19,122; 180,620,103 vs 147,221,566 |
| Chapter 16's 2025 card values | Ch 16 §16.4, §16.8 | 18, 23, 27 | Yes, everywhere | ₹1,146,641,651.25; 46,356; 4,599; ₹24,735.56; 27.5% |
| Chapter 13's funnel: 30 real enquiries, 8 never contacted | Ch 13 Pattern 4; Ch 4 §4.8 | 23 §23.5 | **No** | Ch 23 reports 43 leads, 14% win rate, 21 never contacted (S1-9) |
| "Chapter 24, Forecasting: prediction intervals" | Ch 21, Ch 22 | 24 | **No** | Ch 24 is Requirements, Storytelling & Stakeholders; forecasting is Ch 40 (S1-8) |
| "Chapter 23, Data Storytelling" | Ch 16, 20, 22 | 23 | **No** | Ch 23 is Business Acumen; the storytelling is in Ch 24 (S1-8) |
| "Chapter 25: experimentation in practice" | Ch 22 | 25 | **No** | Ch 25 is the BA track; experiments are old Ch 30 (S1-8) |
| "Chapter 27: the ethics of analysis, including selective reporting" | Ch 22 | 27 | **Yes** (title wrong) | Ch 27 §27.8: "Chapter 22 promised this section" |
| The memo and the three-slide story | Ch 23 Where-this-leads | 24 | Yes | §24.6, `three_slide_story.md` |
| BRD, FRD, SRS, process mapping, user stories | Ch 24 Where-this-leads | 25 | Yes | §25.4, §25.7, §25.8 |
| Agile, Scrum, Kanban, Jira "as actually run" | Ch 25 §25.2 | 26 | Yes | §26.10 |
| "Chapter 27 turns your Part II projects into a portfolio" | Ch 25, 26 | 27 | Yes | §27.9–27.11 |
| Farah's first portfolio piece: the hospitality wedding-season question | Ch 9 | 27 | **Yes** | Ch 27 story: "the one Chapter 9 followed her building" |
| "Hidden skill: agreeing definitions is stakeholder work, Chapters 23 and 25" | Ch 8 §8.3 | 23, 25 | Yes | §23.13, §25.6 |
| Chapter 58's email-intake pipeline, right 88% of the time | Ch 25 §25.12 | 58 | Yes | 9 mentions of 88% |
| Non-functional requirements at architecture scale | Ch 25 §25.5 | 60 | Yes | 13 mentions |
| "Case Study & Guesstimate bank (Chapter 74)"; "Behavioral & Case Interview bank (Chapter 75)" | Ch 23, Ch 24 | 74, 75 | **No** | 74 is the ML bank; 75 is Product Sense; behavioral is 81 (S1-8) |
| Chapter 76B written to Chapter 25's assumed scope (CPI-23) | — | 25 ↔ 76B | Check at Part VIII | Chapter 25 now exists (draft v2); its scope is §25.1–25.12 |

Five unkept in this part, four of them the same cause as S1-2: a closing list written to a plan rather than to the chapter that was built.

### Findability — Part II

- **At-a-glance blocks:** all eighteen present and honest about hours. Three "Before you start" lines are wrong for the reading order (19, 17, 18: S1-5) and one is vestigial (16: "pandas is assumed knowledge where it appears"; it never appears). Chapter 27's prerequisite list omits 10, 11 and 19, which is right: the capstone does not use them.
- **Key terms:** present in all eighteen; 1,015 terms pointing at the unwritten Appendix A. Chapter 24 has 14 and Chapter 27 has 22, which is correct for chapters that teach method rather than vocabulary.
- **Recap and Where-this-leads:** present in all. The closing lists are where Part II is weakest: six stale titles (S1-8), three numbering states (S2-7), Chapter 13's omission of 17 and Chapter 11's of 19 (S3-10). Chapter 25's and Chapter 26's lists are the best in the part: chapter, title, and what the reader will get there.
- **Cross-reference precision:** with one exception, excellent. Every cross-chapter section pointer in Chapters 10–26 resolves to the heading it promises (scripted: `review/_section_refs.py`). The exception is Chapter 27 (S2-8), and Chapter 14's one internal slip (S3-13).
- **What the front-of-book table must add for Part II readers:** the two rows proposed at Chapter 10 stand ("already use spreadsheets → start at Chapter 12, skim 10–11"; "already write SQL → start at Chapter 17, skim 12–13"). One more: "already use pandas → start at Chapter 14", because in the decided order 14, 15 and 16 come after the Python block, and a Reader 2 who knows pandas would otherwise skip the three chapters that teach cleaning, charts and BI. If structural question 5 is taken, that row becomes "start at Chapter 20".

### Character arcs — Part II

| Chapter | When the story is set | Meera | Farah | Others |
|---|---|---|---|---|
| 10 | second week of January 2026 | reconciles the two Januaries (₹4,335,471) | — | Anita, Vikram |
| 11 | first week of January 2026 | finds the ₹64,596 in the month-end pack | — | Anita preparing the board review; Vikram sends the Summary sheet |
| 19 | undated (Q4 2025 data) | named | — | — |
| 12 | "today" is 31 March 2026 | — | in the `employees` table (Farah Khan, Sales Executive) | Anita's four questions; Vikram, Neha, Rahul in the table |
| 13 | January 2026 | (the "sales coordinator") | — | the managing director's board review |
| 17 | undated Thursday; "the last quarter" | the fifteen-minute rescue (36 files) | — | operations, Finance |
| 18 | undated ("over two weeks") | the report that ran itself | as a rep label | — |
| 14 | 6 January 2026 | checks the branch league table | — | Vikram, Anita; **Sandeep Gill** (RSM North), **Arjun Nair** (RSM South) |
| 15 | first week of January 2026 | checks "the October collapse" | — | **Suresh Menon** (Finance Manager; also Ch 3), Vikram, Anita; **Simran Kaur** (rep, exercises) |
| 16 | a Monday in February 2026, then two months | publishes the first Power BI report | — | Sandeep Gill, Arjun Nair, **Pooja Desai** (RSM West, covers East) |
| 20 | a Monday in February 2026; 4 March; 12 May 2026 | the Flash that stopped | — | Vikram |
| 21 | undated; "six months later" | the seven-day promise | — | sales team, operations head |
| 22 | January 2026, then three months | the transporter that wasn't better | — | logistics head |
| 23 | February 2026 | the profitable company that almost missed payroll | — | finance controller |
| 24 | 3–8 January 2026; the Monday meeting | the meeting that never needed to happen | — | Vikram, Anita, Finance Controller |
| 25 | March 2026 | "at Riverstone that person is currently Meera" (§25.1) | — | **Ayesha Qureshi** (BA, 18 months in; not in the bible), Vikram |
| 26 | February 2026; repository from Monday 2 March 2026 | the rule nobody could date | spots the `.env` on GitHub | Vikram, the finance assistant, the IT contractor; Imran recalled |
| 27 | memo dated 12 February 2026 | — | her first portfolio piece, from Chapter 9 | Vikram, Anita |

**Meera is in seventeen of eighteen chapters and carries fifteen of the stories.** The arc is consistent (sales coordinator → the person who checks every slide → the person who builds the report, the Flash, the repository) and it is the book's spine. The problem is the calendar (S2-9): eight rescues in January 2026, five in February, and Chapter 25 says outright that she is the BA, the analyst, the scientist and the engineer. Farah's arc holds: sales executive (3, 5, 8), 13 of 28 (8), the plateau (9), the `.env` catch (26), the wedding-season portfolio piece (27). CPI-25's "Farah is now a Business Analyst" is contradicted again by Chapters 26 and 27.

**New names in Part II:** Sandeep Gill, Arjun Nair, Pooja Desai, Simran Kaur, Suresh Menon (all in `riverstone-bible-additions.md`), Ayesha Qureshi (not; S3-24), BlueCart and SwiftLine (transporters, invented for Chapter 22 and declared so). Vikram's title is "Sales Manager" (Ch 3, 12) and "the key accounts sales manager" (Ch 25, 27); the bible has "Sales Manager, Key Accounts", so both are right.

**Sunrise Caterers' unnarrated arc continues:** at risk in Chapter 13 Pattern 6 (last order 10 June 2025, 204 days), unpaid and unassigned in Chapter 12 §12.15. Still consistent, still unconnected. S4.

### The four explicit checks — status at the end of Part II

- **A. Reading order versus chapter numbers.** Done for Part II. The order is right for 14, 15, 16 (written for it) and wrong for 17, 18, 19 (written against it): S1-5. The seams are written to the old sequence: S3-10. The references are in three numbering states: S2-7. The list of every reference that will be wrong after renumbering is in the tool output; the ones that will *still* be wrong after renumbering are S1-8 and the eleven bare "Chapter 76" references.
- **B. Chapters 25, 26 and 27, read harder.** *25* (draft v2): clean on facts (order 5001, 103 days, 28 days order-to-cash, the 200-hours arithmetic and the "hidden skill" all check against Chapters 3 and 8); one new unregistered character (S3-24); one missed pointer to Chapter 13 Pattern 6 (S3-23); CPI-23 (76B written to an assumed Chapter 25) can only be closed at Part VIII. *26*: clean; the most §6.5-compliant chapter in the part; its Where-this-leads uses old numbers while 17, 18 and 20 use new ones (S2-7). *27*: the best chapter in Part II and the one whose pointers into it are wrong ten times in nineteen (S2-8); its facts (3,414 orders without a rep, 100 customers without a city, 48 duplicates, Farah's Chapter 9 question, Vikram's title, the tiered discount rule) all check. *83*: not yet reached.
- **C. The book ends twice.** Not yet reached.
- **D. The first two hundred pages, and Chapter 12.** At roughly 350 words a page, two hundred pages is Chapters 1–8, reported at Chapter 10. The explicit question: **does a true beginner survive Chapter 12? Yes, on the PostgreSQL path, and comfortably, through §12.1–12.12 and §12.14–12.15**, which are the best-taught 17,000 words in the book for a Reader 1: every query hand-checked, every trap shown wrong first, one company, twelve orders they can count. The two places they are at risk are **§12.13**, 8,000 words of DDL in two dialects in a chapter that promised no programming experience was needed (S2-10; the fix is a label), and **the position**, arriving after 25–30 hours of Chapter 11 and 20–25 of Chapter 19 with 15–20 hours of Chapter 13 and 55–65 of Python still ahead before any light chapter (S2-10, structural question 5). The beginner who survives Chapter 12 is not the one at risk; the one at risk is the beginner who believed Figure 6.2 and reaches Chapter 12 in month three of a plan that needed month five (S1-7).

### Structural questions for the author — Part II

Stated and stopped, as instructed. Questions 1–4 (Part 0/I) stand.

5. **Should Chapters 14, 15 and 16 come before 19, 17 and 18?** The order 10, 11, 12, 13, 14, 15, 16, 19, 17, 18, 20 satisfies every "Before you start" line in Part II as written (19 needs 10, 11, 14, 15; 17 needs 14 and cites 16; 18 needs 17, 12–13, 14, 15, 11; 16 needs 11, 13, 14, 15; 20 needs 13–19), introduces the full dataset in the chapter that introduces it (14), keeps Chapter 19's "own programming basics before Python" reasoning, and puts the 12–15-hour Chapter 15 between the SQL block and the Python block. The cost is one sentence in Chapter 16's header and the Chapter 6 figure, which S1-1 already redraws. The alternative, keeping the decided order, costs about forty-five sentences in 17, 18 and 19 plus a new dataset introduction, and leaves the six-chapter wall. The reading found no dependency that requires Python before 14–16; the map's rationale ("all tools together") is served either way, since 14 and 15 keep their pandas previews.

6. **Where is the full Riverstone dataset introduced?** Today in Chapter 14 §14.1, one paragraph, for a 250-fold jump in scale (330 lines → 209,006; ₹43 lakh → ₹278 crore). Whichever order is chosen, the first chapter to use `riverstone_full` or `companion/full/` should carry a short "Meet the whole company" box: what changed (5,027 customers, four branch offices, three years), what did not (the 24 key accounts and their ₹4,335,471 are inside it), and where `DATA_SPEC.md` is.

7. **Should §12.13 stay inline?** 8,000 words, two dialects, eleven steps, inside the chapter that also has to teach SELECT to a beginner. Options: a first-pass label (S2-10, smallest); MySQL DDL moved to §12.16 and the companion lab file; or §12.13 as its own short chapter between 12 and 13. The first is enough for the reader; the third is the honest structure.

8. **What horizon does Figure 6.2 promise?** Six months at 8 hours a week, against 317–393 claimed hours for Parts 0–II. Either the figure changes or the chapters' hour claims do. This is the author's call, and it should be made before assembly, because the figure is the first thing a Reader 1 plans their life around.

### Method note — Part II

Same method: the eighteen chapters read in map order without editing, then the three scripts, then the four checks, then every promise verified by opening the named chapter. One script added: `review/_section_refs.py`, which prints every cross-chapter "section X.Y" pointer next to the heading it lands on; it found Chapter 27's ten and confirmed the other seventeen chapters clean. The section pointers were the check that mattered most for B, and it would not have been possible by reading alone. The ledger's stoplist held: 458 flags, about a dozen real, all already inside S1-5 and S3-19.

Next: Part III in reading order (28, 34, 29, 32, 33, 30, 31), with the "Chapter 30 / Chapter 29 Python as Software" reference (S2-7) and CPI-9 ("Chapter 29's before-script no longer matches Chapter 18") checked first, since Chapter 18's script is now known.

### Appendix: the first-appearance ledger, Part II

*Scripted over Parts 0–II in reading order: 1,773 bold terms, 458 used in plain text before the chapter that bolds them. Verdicts as before.*

| Term | First used | First bolded | Verdict |
|---|---|---|---|
| UTC, normalize, action title, mapping table, branch sales offices | Ch 18, 19 | Ch 14, 15 | **real** — the Part II order: S1-5 |
| cartons, header row, missing values, repair | Ch 10 | Ch 14 | everyday, glossed where used |
| regular expression (`~`, `regexp_replace`) | Ch 14 §14.2 | Ch 14 §14.7 | **real** — S3-19 (not a ledger flag; found by reading) |
| attainment | Ch 17 (`targets_2025.csv`) | Ch 15 | real but everyday; the file's README explains it. S4 |
| window function, star schema, fact table, time intelligence, calendar table | Ch 11 §11.8 | Ch 13, 16 | announced ("you'll practice DAX again in Chapter 16"; "Chapter 13 gives it a cleaner tool") |
| DataFrame | Ch 17 §17.7 | Ch 18 | announced ("a DataFrame (Chapter 18)") |
| confidence intervals | Ch 21 §21.8 | Ch 22 | announced ("the bridge to Chapter 22's confidence intervals") |
| requirements gathering; as-is, BRD, FRD, SRS; Scrum, Kanban | Ch 23, 24, 25 | Ch 24, 25, 26 | announced in each chapter's Where-this-leads |
| GitHub Actions | Ch 20 §20.7 | Ch 26 | a product name in a list of schedulers; fine |
| commit | Ch 19 | Ch 26 | sense: everyday verb |
| business requirement | Ch 12 | Ch 25 | sense: "business rule" |
| fan out, fanned out | Ch 12 | Ch 14, 18 | Chapter 12 bolds "fan-out" with a hyphen; tokenization |
| DuckDB | Ch 13 dialect note | Ch 18 | one name in a list; fine |
| population, skew, the IQR rule | Ch 15 §15.5 | Ch 21 | announced ("Chapter 21 … the statistics behind histograms, box plots") |
| aggregates, constraints, schema, subqueries, Google BigQuery | Ch 11 | Ch 12 | Chapter 11's SQL-link boxes name them with a pointer to Chapter 12 |
| Excel for Windows, Excel for Mac, Copilot, ribbon, rename, merge, trim, min, max | Ch 10, 11 | Ch 11, 16, 19 | everyday or product names; noise |


---

## Part III (Chapters 28–34) — appended after the reading of Part III, 22 September 2026

Read in the map's order: 28, 34, 29, 32, 33, 30, 31. Every chapter read in full, nothing edited. Finding numbers continue from Part II (S1-9, S2-10, S3-24); structural questions continue from 8.

### Summary — Part III

Part III is the best-written part so far. Every chapter reconciles to the dataset it uses (₹4,335,471, 326 lines, 173 orders, ₹439,823.50 for December, 3.4 kg of steel tube per chair), the four generated datasets have fixed seeds and stated true answers, and the stories carry one analyst through seven problems that get harder in the right order. Reader 2 will enjoy it. Reader 1 will finish it.

Three things stand between the reader and that experience, and all three are seams, not content:

1. **A prerequisite chapter that no longer exists.** Chapters 30 and 31 lean on regression ("Chapter 19 used regression to predict"; "Chapter 19's regression mechanics help"; "Chapter 19, Regression & Forecasting, shares the machinery"). Chapter 19 is Spreadsheet Automation. No chapter before Chapter 30 teaches regression; the first is Chapter 37 §37.1, in Part IV. Chapter 31 then runs on OLS with interaction terms, fixed effects, logistic propensity scores and discontinuity regressions. This is S1-10.
2. **Chapter 34 is written as if Chapter 29 came first**, fourteen times, while the map places 34 before 29 and Chapter 29's header requires 34. The same seam pattern as Part II's S1-5. This is S1-11.
3. **The navigation lies about titles.** Seven "Where this leads" entries in Chapters 30, 31 and 34 name chapters that do not exist under those numbers (a reader following "Chapter 43, Pricing & Revenue Analytics" lands in deep learning; "Chapter 73, Data Engineering Question Bank" is the statistics bank), and five places say pandas is Chapter 17 when it is Chapter 18. This extends S1-8 and is S1-12.

Below those: Chapter 29 still refactors a script that is not Chapter 18's script (CPI-9 unchanged in the approved text, and the story now supplies a better provenance that would fix it); Chapter 32's snapshot demo moves Metro Mart the opposite way from Chapter 28 and stamps the author's run date on it; and Chapter 28 at 23,800 words and 129 code blocks is a wall on its own.

Reader 1 survives Part III on the analytics path if S1-10 is fixed. Without a regression primer, Reader 1 will finish Chapter 30 and stall in Chapter 31 §31.3.

Part III's arithmetic: 78,400 words, 420 key terms, 364 code blocks, 125 exercises, and 92–122 hours by the chapters' own estimates. Chapter 6's plan (Figure 6.2) stops at Part II, so there is no plan to compare against; the comparison waits for Chapter 83 (check C).

### S1 findings — Part III

**S1-10. Chapters 30 and 31 cite a regression chapter that does not exist before them.**
Where: Ch 30 §30.11 opening line "Chapter 19 used regression to predict. Here it's used to explain"; Ch 31 at-a-glance "Chapter 19's regression mechanics help"; Ch 31 Where-this-leads "Chapter 19, Regression & Forecasting, shares the machinery: the difference is entirely in what you claim from it."
What the reader meets: Chapter 19 is *Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script*. Searching every chapter from 10 to 29 for a regression heading finds one, Chapter 22 §22.7 "regression to the mean", which is a different idea. The first regression teaching in the book is Chapter 37 §37.1 (linear) and §37.3 (logistic); forecasting is Chapter 40. Chapter 30 §30.11 reads an OLS summary table and a logistic odds-ratio table with one explanatory paragraph each, which is survivable. Chapter 31 is not: §31.3 "the coefficient on `treated:is_after` *is* difference-in-differences", fixed effects "absorb" region and month, R-squared 0.991; §31.5 fits `smf.logit` for propensity scores; §31.6 fits a two-slope regression and reads "the jump at the cut-off"; exercise 10 asks for a quadratic on each side. Reader 1 has never seen a coefficient, an interaction term or a dummy variable. Reader 2 knows regression and will simply be annoyed by the wrong pointer.
Cause: an earlier plan had *Regression & Forecasting* as Chapter 19 in Part II. The chapter moved to Part IV (37 and 40) and the citations in 30 and 31 were not revisited, and nothing was put in its place.
Smallest fix: a boxed primer of about 600 words at the top of Ch 30 §30.11 ("Regression in one page: a line through data, a coefficient is a slope, a dummy is a switch, an interaction is a switch that changes a slope, the interval is the same interval as §30.2"), and change the three citations to "Chapter 37 §37.1 teaches the machinery in full; this section uses only what the box gives you." Structural alternative, stated and stopped: move §37.1 and §37.3 into Part III as a short chapter before Chapter 30.

**S1-11. Chapter 34 is written after Chapter 29 and placed before it.**
Where: the map reads 28 → 34 → 29. Ch 34's own header requires only Chapter 6 and Chapter 2, which is right for its position. Its body then mentions Chapter 29 fourteen times as finished work: "Chapter 29's `report` command returns 1", "the alert Chapter 29's package now sends", "the mock CRM API from Chapter 29", "Chapter 29's 200, 401, 429, 503", and the December figure ₹439,823.50 introduced as "the figure Chapter 29's report produces". The first-appearance ledger agrees: *fixtures* and *secrets manager* are used in plain text in Chapter 34 and first put in bold in Chapter 29. Chapter 29's header, meanwhile, lists "Chapter 34 (the terminal, environment variables, exit codes)" as a prerequisite, so each chapter requires the other.
What the reader meets: Reader 1 opens Chapter 34 having never seen a package, a `report` command, a mock API or an HTTP status code, and is told to run things from a project they have not built. Reader 2 recognises the circularity in the two headers.
Cause: the same as S1-5. Chapter 34 was written with Chapter 29 on the desk, then the map (34 → new 29) put the terminal chapter first, which is the right order for a beginner, without the body being turned around.
Smallest fix: pick the direction the map already chose. In Chapter 34, replace each "Chapter 29's X" with a self-contained example (a five-line script that exits 1, `curl` against any public URL for the status codes) and make the pointers forward: "Chapter 29 will wrap this in a package." Remove Chapter 34 from Chapter 29's header only if the map stays 34-before-29; otherwise see structural question 9.

**S1-12. Seven stale titles and five wrong pandas pointers in Part III's navigation.** Extends S1-8.
Stale titles, all in "Where this leads" or headers, with the actual chapter under that number:
- Ch 30: "Chapter 42, Digital & Web Analytics" (actual: *Recommender Systems & Ranking*); "Chapter 55, Machine Learning in Production" (actual: *Building AI Applications: RAG, Agents & Evaluation*).
- Ch 31: "Chapter 43, Pricing & Revenue Analytics" (actual: *A First Look at Deep Learning*); "Chapter 19, Regression & Forecasting" (actual: *Spreadsheet Automation*); "Chapter 55, Machine Learning in Production" (as above).
- Ch 34: "Chapter 50, Cloud Fundamentals" (actual: *Streaming & Real-Time*; the cloud chapter is 52); "Chapter 73, Data Engineering Question Bank" (actual: *Statistics, Probability & Experimentation Bank*; the data-engineering bank is 77).
Wrong pandas pointers: "Chapter 17's pandas is enough to follow the code" (Ch 30 header and Ch 31 header); "pandas and NumPy (Chapter 17)" (Ch 33 Tools); "pandas (`merge`, Chapter 17)" (Ch 33 stretch goals); "Chapter 17, Python for Data Analysis, covers the vectorized alternatives" (Ch 33 Where-this-leads); "pandas (Chapter 17)" at ch34:362 and ch33:752. Chapter 17 is *Python from Zero*; pandas is Chapter 18, *Python for Analysts: pandas & Automation*.
What the reader meets: the "Where this leads" lists are the book's map between parts. A reader who wants pricing analytics after Chapter 31 opens Chapter 43 and finds neurons. A reader who wants to revise pandas before Chapter 30 opens Chapter 17 and finds `print("hello")`.
Cause: two earlier chapter plans survive in the closing lists (one in which 42/43/45/50/55 were analytics-application chapters, one in which 17 was the pandas chapter). The stale-title script (`review/_stale_titles.py`) finds the same pattern in Chapters 39, 40, 52 and 59, which will be reported with their parts.
Smallest fix: the twelve edits above. A one-line rule for the copy-edit: every "Chapter N, Title" citation is checked against the H1 of file N by script, not by eye.

### S2 findings — Part III

**S2-11. Chapter 29's "before" script is still not Chapter 18's script, and the story now offers the fix.** Extends CPI-9; not a re-report.
Where: Ch 29 header "Chapter 18 (pandas and the monthly report)"; §29.1 presents `start/monthly_report.py` (hard-coded password, SQL built by string concatenation, a bare `except`, no functions) as the script to be turned into software. Chapter 18 §18.15's monthly report already has functions, a parameter for the month, and no password in the file. CPI-9's preferred fix (Chapter 29 refactors Chapter 18's actual script) is not in the approved v1 text.
What the reader meets: Reader 2 sees a strawman and discounts the chapter's argument. Reader 1, who wrote Chapter 18's script three weeks ago, wonders which of their two scripts is "the" monthly report.
What changed since CPI-9: the Chapter 29 story now says "Since Imran left, it's a copy of his script", which is a different provenance from Chapter 18's, and a good one.
Smallest fix: use it. In the header and §29.1, replace "Chapter 18's monthly report" with "Imran's original script, which Chapter 18's version was written to replace", and add one sentence: "If you finished Chapter 18, you have already done the first three of these steps; skip to §29.4." That keeps the poor script as a teaching object without claiming it is the reader's.

**S2-12. Chapter 32's snapshot demo reverses a Chapter 28 fact and stamps the author's run date on the story.**
Where: Ch 32, "Watch it work. Metro Mart moves from Mumbai to Thane", followed by `update raw_crm.customers set city = 'Thane' where customer_id = 5` and the result table: Mumbai valid 1900-01-01 to 2026-09-18, Thane valid from 2026-09-18, current.
What contradicts it: Chapter 28's `customer_changes` and Figure 28 side panel: Metro Mart moved *from Thane to Mumbai* on 2025-07-01, and §28.13 spends a page on "as it was / as it is" for exactly that move (January–June 2025 orders count under Thane). Chapter 32 itself reconciles 23 customer versions to Chapter 28's dimension. Then the demo moves Metro Mart back to Thane on 18 September 2026, which is after every date in the story so far (Chapter 31's board meeting is April 2026) and is visibly the day the author ran the command.
What the reader meets: a reader who did Chapter 28's lab now has Metro Mart in Thane again with a valid_from in the future of the story. The "Watch out: a snapshot only knows what it has seen" box that follows is correct and important, and the example under it undermines it.
Cause: the demo was run live and pasted; the customer was chosen for having a known history, which is what makes it collide.
Smallest fix: use a customer with no Chapter 28 history (any of the 20 that did not change), pick a change that fits the story (a segment change is the one the dimension tracks), and add "the date will be the day you run it" under the output. If Metro Mart must stay, move it Mumbai → Navi Mumbai and say so is a new move.

**S2-13. Chapter 28 is a wall by itself.** Extends S2-10.
Where: Chapter 28 profiles at 23,793 words, 82 key terms, 129 code blocks, 22 exercises and 18–24 hours. Part II's six-chapter wall (S2-10) was about six chapters in a row with no break; Chapter 28 is the same problem inside one chapter, and it is the first chapter of the part, immediately after Chapter 27's interview material.
What the reader meets: Reader 1 opens Part III with the longest chapter of the book so far, covering indexes, EXPLAIN, window functions, recursive CTEs, bill-of-materials explosion, normal forms, star schemas, slowly changing dimensions, and migrations. Chapter 34, which follows in the map, is the lightest chapter in the part (8,755 words) and would have made a gentler start.
Cause: two chapters' worth of content (SQL performance; data modelling) under one number, because the plan gave them one row.
Smallest fix that is not structural: a half-page "how to read this chapter" note at the top of Chapter 28 that splits it into two sittings (§28.1–§28.7 performance; §28.8 onward modelling) with a stopping point marked. Structural alternative, stated and stopped: structural question 11.

### S3 findings — Part III

**S3-25. Ch 33 §33.1 points at "section 33.11's project"; there is no §33.11.** Numbered sections end at 33.10; the project is the unnumbered "The project" heading. Fix: "the project at the end of this chapter".

**S3-26. Ch 30 §30.12 gives two monthly numbers for the same lift.** The write-up says "+14% ... roughly 560 extra enquiries a month (the interval's ends are about 190 and 920)", and §30.9 derives 560 correctly from 3,400 visitors a day. The "Instead of / Write" table three paragraphs later says "+14% relative, which is 35 enquiries a month at current traffic". Cause: the table was drafted against an earlier traffic figure. Fix: 560.

**S3-27. Ch 31 §31.6 credits Chapter 3 with a rule Chapter 3 does not contain.** "Riverstone gives free delivery on orders of ₹25,000 or more (Chapter 3)." Chapter 3 has no free-delivery rule and no ₹25,000 threshold; the only chapters that mention free delivery are 31 and 55, and the bible additions file has nothing. Fix: drop "(Chapter 3)" and add the rule to the bible, since Chapter 55 also uses it.

**S3-28. Ch 28's promise to Chapter 49 is not kept.** Ch 28 (line 2222): "warehouses have their own materialized views with automatic refresh (Chapter 49)". Chapter 49, *Storage, Warehouses & Lakehouses*, does not contain the word "materialized". Verified by search; will be re-checked when Part V is read. Fix: point at the chapter that does cover it, or drop the pointer.

**S3-29. Ch 31 §31.4's pre-trend arithmetic understates its own number.** "drifts by −0.18% a month, which over fifteen months comes to less than a third of the effect being measured." 15 × 0.00175 = 0.026 log points against an effect of 0.073, which is 36%: about a third, not less than a third. The conclusion (no meaningful pre-trend) still holds, but this is the chapter that tells readers to check their assumptions, and the check is misreported. Fix: "about a third".

**S3-30. Two different Riverstone org charts, both attributed to Chapter 28.** Ch 33 §33.4 says "Chapter 28 walked these in SQL with recursive CTEs. In Python they're a dictionary of lists" and gives: Arvind Kapoor → Anita Rao and Harpreet Sethi; Anita → Vikram Singh and Farah Khan; Vikram → Neha Kulkarni and Rahul Mehta; Harpreet → Ramesh Patil → Ajay Kumar. Chapter 28's `staff` table, as shown, runs Arvind → Harpreet (Head of Production) → Ramesh (Plant Manager, Taloja) → Ajay (Shift Supervisor) → Gopal Sahu, and its sales branch is Anita → regional managers Arjun Nair, Pooja Desai, Sandeep Gill → sales executives, with Meera as Sales Coordinator under Anita. Farah Khan and Neha Kulkarni are sales reps on Chapter 28's order sheet, not managers. Reader 1 who did both labs has two Riverstone hierarchies. Fix: make Chapter 33's dictionary the five-person production branch Chapter 28 actually printed, which also makes the "Steel tube 3.4 matches Chapter 28's SQL exactly" continuity, which is real and good, the pattern for the whole section.

**S3-31. Chapter 34's vocabulary is used two parts before Chapter 34.** The ledger shows *environment variables* and *exit code* used in plain text in Chapter 17 and Chapter 18 (and Chapter 20 lists "exit code" as a key term) while Chapter 34 is the chapter that puts them in bold. Chapter 34's header needs only Chapters 6 and 2. This is not a defect in Chapter 34; it is evidence for structural question 9 (Chapter 34 could sit directly after Chapter 17).

**S3-32. Ch 30 §30.3's t-test includes the orders Chapter 13 taught the reader to exclude.** The query joins `sales_lines`, `orders` and `customers` and groups by order, with no `WHERE o.status <> 'Cancelled'`. Chapter 13 applies that filter three times and builds the `sales_lines` view around it; the 173-versus-175 distinction is the running reconciliation of Part II. Reader 2 notices; Reader 1 was trained to. Fix: add the filter and re-run the two cells (n, means, p and §30.7's power calculation shift slightly).

**S3-33. Ch 33's story and its project disagree about where the six hours went.** The story: the nested loop accounts for about 75 seconds, and the real cost was re-reading the order file inside the loop (20,000 reads). The project's Option B says "start from `match_slow.py`", and answer 14 says that on `match_slow.py` "the comparisons themselves dominate, while `load` and `csv.DictReader` account for a fraction of the run". So `match_slow.py` does not have the fault the story turns on. Fix: one sentence in the project: "`match_slow.py` has the nested loop but reads the file once; add the re-read inside the loop yourself and profile it to see the story's six hours."

**S3-34. By the end of Part III the reader has seven Riverstone datasets and no list.** Extends structural question 6. Part II: `riverstone` (12 orders), `riverstone_2025` (24 accounts), `riverstone_full` (5,027 customers), and Chapter 14's messy export. Part III adds `riverstone_perf` (Ch 28), `riverstone_web` (Ch 30 Tools, a PostgreSQL load of the web data), Chapter 31's three causal CSVs, and Chapter 33's `match_data`. Each is introduced correctly in its own at-a-glance box; nothing anywhere says which is which or which chapters use which. A findability item: one table in Chapter 6 or Appendix B.

**S3-35. Four Riverstone facts introduced in Part III are not in the bible.** Extends S3-24. The North region's 6% list-price rise on 1 October 2025 (Ch 31, the spine of the chapter); the quarterly-business-review programme for 68 of 240 key accounts (Ch 31); the free-delivery threshold at ₹25,000 (Ch 31, Ch 55); the Bhiwandi warehouse expansion in March 2026 (Ch 31 ex. 15; Bhiwandi itself is in the bible). Chapter 31's story also has a "sales director" and a "regional manager" at the board meeting; the bible has Anita Rao as Sales Head. Chapter 29's "Since Imran left" is a new fact about a Chapter 2 character. None of these contradict anything yet; they will the moment Part IV reuses the regions.

**S3-36. Chapters 30 and 31 cite the same chapter by two numbers across the parts.** Extends S2-7 and CPI-24. Part III consistently uses the old numbers for itself: Ch 30's list says "Chapter 29, Python as Software" and "Chapter 31, Causal Inference"; Ch 33 says "Chapter 29, Python as Software". Part II's Chapters 17, 18 and 20 already say "Chapter 30, Python as Software" (the new number). A reader who follows Chapter 18's pointer to "Chapter 30" and then Chapter 33's pointer to "Chapter 29" is being sent to the same chapter by two names. Nothing to add to the fix in S2-7; this records that Part III is internally in the old state and Part II is half in the new one.

### S4 findings — Part III

- Ch 31 §31.7 "West is twice North's size": 3,335 against 2,032 monthly orders is 1.6×.
- Ch 30 §30.9 "chance alone would produce a gap this large about once in 2,000 tests" for p = 0.0003, which is about once in 3,300.
- Ch 30 story: "the test had a fair chance of detecting only differences of about 1.5 percentage points" at 7,592 visitors; scaling the 0.5-point MDE by √(25,000/3,796) gives about 1.3.
- Ch 33 story: "Read each file once. That alone takes the job from hours to about a minute and a half" against §33.1's 75 seconds; and "It now finishes before you've finished reading the email" is a nice line that the reader cannot check.
- Ch 34 story: "07:40 on a Tuesday" with no date; the only chapter in Part III whose story cannot be placed on the calendar (see character arcs).
- Ch 32's version-check line "checked in September 2026" sits next to the 2026-09-18 snapshot, which is how the author's date got into the story (S2-12).
- Ch 30 §30.2 reports 7,643 enquiring visitors of 176,000 and §30.3 reports 7,711 enquiring *sessions*; the chapter explains the difference (visitor vs session) two paragraphs later, but the two numbers appear before the explanation.

### Overwhelm profile — Part III

Reading order. Words exclude the answer key; hours are the chapters' own at-a-glance estimates.

| Order | Ch | Words | Key terms | Code blocks | Exercises | Hours | Wall / relief |
|---|---|---|---|---|---|---|---|
| 1 | 28 | 23,793 | 82 | 129 | 22 | 18–24 | wall (S2-13) |
| 2 | 34 | 8,755 | 67 | 28 | 16 | 10–14 | relief in length, not in terms (67 keys in 8,800 words) |
| 3 | 29 | 11,322 | 61 | 40 | 15 | 12–16 | |
| 4 | 32 | 9,419 | 57 | 38 | 18 | 16–20 | |
| 5 | 33 | 7,423 | 59 | 36 | 18 | 12–16 | densest terms per word in the book so far (1 per 125) |
| 6 | 30 | 9,801 | 56 | 55 | 18 | 14–18 | |
| 7 | 31 | 7,913 | 38 | 38 | 18 | 10–14 | lightest close |
| | **Part III** | **78,426** | **420** | **364** | **125** | **92–122** | |
| | **Parts 0–III** | **304,376** | **1,435** | | **591** | **409–515** | |

Observations:
- Part III is 78,400 words for 92–122 hours; Part II was 225,950 words for 290–357. Part III is more efficient per hour and its chapters are more even, except Chapter 28.
- Key-term density rises through the part: Chapter 31 is the only chapter under 50 terms. Chapters 33 and 34 introduce a term every 125–130 words, which is the rate of Chapter 12 (S2-10's hardest chapter).
- Code blocks: 364 in seven chapters. Chapter 30 has 55 code blocks in 9,800 words; almost every paragraph is followed by code and output. That is the right design for statistics (every claim measured) and it is also the slowest reading in the part.
- Time claims now total 409–515 hours for Parts 0–III against Chapter 6's 208 hours for the analyst path (S1-7). Chapter 6's plan stops at Part II, so there is nothing in Chapter 6 for Part III to contradict; the whole-book figure is checked at Chapter 83.

### References that break at renumbering — Part III

`_journey_tools.py` counts references inside Part III that point at a chapter whose number changes: Ch 28: 49; Ch 34: 25; Ch 29: 21; Ch 32: 21; Ch 33: 15; Ch 30: 12; Ch 31: 11. **Part III: 154. Running total, Parts 0–III: 756.**

Every one of Part III's self-references uses the old numbers (34 for the terminal chapter, 29 for Python-as-software, 32 for dbt, 33 for computer science, 30 for inference, 31 for causal), consistently. Part II already cites two of them by their new numbers (S3-36). The section-pointer script (`_section_refs.py`) finds every "Chapter N section N.M" pointer in Part III resolving to a real heading, unlike Chapter 27 (S2-8); the only dangling section pointer is Chapter 33's "section 33.11" (S3-25).

### Promises checked — Part III

| Promise (where made) | Kept? | Note |
|---|---|---|
| Ch 12 §12.1 → Ch 28 normal forms | Yes | §28.8 onward |
| Ch 12 §12.10 → Ch 28 grain | Yes | |
| Ch 12 §12.11 → Ch 28 EXPLAIN and indexes | Yes | EXPLAIN ANALYZE throughout §28.1–§28.5 |
| Ch 12 §12.13 → Ch 28 migrations | In substance | Flyway shown, not run; Ch 28 says so |
| Ch 13 → Ch 28 recursive CTE for the org chart | Yes | and the bill of materials |
| Ch 18 → Ch 29 "make the script software" | Yes, on a different script | S2-11 / CPI-9 |
| Ch 20 → Ch 29/34 exit codes and alerts | Yes | Ch 29 §29.x refers back to Ch 20's scheduled jobs correctly |
| Ch 22 → Ch 30 p-values, intervals, Type I/II | Yes | Ch 30 header: "assumed, not repeated"; the ledger confirms Ch 22 uses *p-value*, *chi-square*, *effect size*, *peeking*, *Welch's t-test* and *statsmodels* in plain text before Ch 30 bolds them |
| Ch 22 correlation ≠ causation → Ch 31 | Yes | |
| Ch 28 → Ch 32 dbt rebuilds the star | Yes | 326 lines, ₹4,335,471, 23 customer versions reconcile |
| Ch 28 → Ch 33 hash join, recursive CTE, bill of materials | Yes | 3.4 kg steel tube matches exactly |
| Ch 28 → Ch 49 materialized views | **No** | S3-28 |
| Ch 29 → Ch 33 retry queue, `yield from` | Yes | |
| Ch 29 ↔ Ch 34 | **Circular** | S1-11 |
| Ch 30 → Ch 31 DiD, matching, RD | Yes | |
| Ch 30 → Ch 42 "the same website data for funnels, attribution, cohorts" | **Wrong chapter** | Ch 42 is recommender systems; checked again in Part IV |
| Ch 31 → Ch 3 free delivery ₹25,000 | **No** | S3-27 |
| Ch 31 → Ch 43 pricing | **Wrong chapter** | Ch 43 is deep learning |
| Ch 30, 31 → Ch 73 statistics bank | Title correct | Content checked in Part VIII |
| Ch 32 → Ch 47 data contracts | Title correct | Ch 47 mentions contracts 41 times; checked in Part V |
| Ch 33 → Ch 72 Python bank; Ch 69 Extra-Points Method | Titles correct | Checked in Parts VII–VIII |
| Ch 34 → Ch 50 cloud; Ch 73 DE bank | **Wrong chapters** | S1-12 |
| Ch 30 story → "I'll report [enquiry-to-order] in six weeks" | Open | If any later chapter returns to the enquiry-form test, the six-week result is a promise to keep |

### Findability — Part III

- **The "Where this leads" lists are the book's inter-part map and seven of Part III's entries point at the wrong chapter** (S1-12). Until the stale-title script is run over the whole book and the entries corrected, a reader cannot trust any forward pointer with a title on it.
- **Regression has no home the reader can find** (S1-10). The index will list "regression" under Chapter 30, 31 and 37; the reader of 30 needs to know to read 37 §37.1 first.
- **Datasets** (S3-34): seven by the end of Part III; a single table is missing.
- **Chapter 28 has no internal map.** At 23,800 words with 129 code blocks and sections numbered to 28.13, it needs the "two sittings" note (S2-13) or a section list at the top; a reader returning to look up slowly changing dimensions has to scroll past index tuning.
- **Terminology that is good**: Part III's key-term lists are complete and match the bold terms; "Tools" sections give exact versions; every chapter's companion folder is named. The "Common mistakes" tables in 30, 31 and 33 are the best lookup tables in the book so far.
- **Story dates** are findable in six of seven chapters (see character arcs); Chapter 34's is not.

### Character arcs — Part III

| Character | 28 | 34 | 29 | 32 | 33 | 30 | 31 | Note |
|---|---|---|---|---|---|---|---|---|
| Meera | ✓ March 2026, with Vikram | ✓ "07:40 on a Tuesday", the January report | ✓ 3 Feb 2026; failure 2 March | ✓ two dashboards, undated | ✓ month-end, undated | ✓ 30 Jan plan; 2–15 Feb test; briefs Anita | ✓ April 2026 board | In every chapter of the part |
| Anita Rao | ✓ staff table (Sales Head) | | | | | ✓ | ("sales director"?) | |
| Vikram Singh | ✓ | | | | ✓ (org chart, under Anita) | | | |
| Arvind Kapoor (MD) | ✓ | | ✓ ("the MD forwards") | | ✓ | | | |
| Imran | | | ✓ "Since Imran left" | | | | | New fact about a Ch 2 character; not in bible |
| Priya | | | | | ✓ wrote the matching script "two years ago" | | | In bible additions |
| Farah Khan, Neha Kulkarni | ✓ sales reps on the order sheet | | | | ✓ managers in the org chart | | | S3-30 |
| Eight Sales Executives (CPI-10) | ✓ still present, lines 165–172 and §28.13 | | | | | | | CPI-10 unchanged in v1.1 |
| Marketing agency | | | | | | ✓ | | Unnamed, consistent with Ch 23 |

Meera's calendar, extending S2-9: Chapter 28's staff table makes her a Sales Coordinator, level 3 under Anita. Between January and April 2026 she produces the January report (34), inherits and rewrites Imran's script after 3 February (29), signs an A/B test plan on 30 January and analyses it after 15 February (30), reconciles two dashboards (32), fixes the month-end invoice match (33), and briefs the board on a causal estimate in April (31), while Chapter 28's March story has her building a star schema with Vikram. It is a coherent arc (each chapter's problem is harder and her answers grow more senior) but there is no sign of a promotion, and by Chapter 31 the board asks her, not Anita. One sentence somewhere in Part III ("by spring Meera was the person the MD asked first") would carry it.

### The four checks — status after Part III

- **A (reading order ≠ chapter numbers):** 154 more moving references (running total 756). Part III is internally consistent in the old numbering; Part II is half-migrated (S3-36). Two seams found where the map's order breaks the text's assumptions: 34 before 29 (S1-11) and 30/31 before any regression chapter (S1-10). All Part III section pointers resolve.
- **B (Ch 25, 26, 27, 83 read harder):** 25–27 done in Part II; 83 pending.
- **C (book ends twice):** pending; the 409–515 hours for Parts 0–III are the running figure for the 764–980 comparison.
- **D (first 200 pages):** done in Part II; unchanged.

### Structural questions — added in Part III

**9. Should Chapter 34 (the command line) sit directly after Chapter 17?** Its header requires only Chapters 6 and 2. Chapters 17, 18 and 20 already use *exit code* and *environment variable* in plain text. Chapter 29 requires it. Placing it after Chapter 17 removes S1-11 without rewriting Chapter 34 and gives Part II's Python chapters the terminal they already assume. Stated, not pursued.

**10. Where is regression taught for the reader of Part III?** Three options, in increasing size: a primer box in Chapter 30 §30.11 (S1-10's smallest fix); a forward pointer telling the reader to read §37.1 and §37.3 before Chapter 31; or moving those two sections into Part III as a short chapter. The map's Part III title is "Advanced Analytics & Analytics Engineering", and a part with inference, experiments and causal inference but no regression chapter is the one gap a Reader 2 would name. Stated, not pursued.

**11. Is Chapter 28 two chapters?** §28.1–§28.7 (indexes, EXPLAIN, windows, recursion, performance) and §28.8–§28.13 (normal forms, star schema, slowly changing dimensions, migrations) are each the size of an ordinary chapter and have different prerequisites (the first needs Chapter 13; the second needs Chapter 16's date dimension and Chapter 26's Git for migrations). Splitting would also give the map a lighter first chapter for Part III. Stated, not pursued.

### Method note — Part III

Same method as Parts 0–II: each chapter read in full in the map's order, then the three scripts (`_journey_tools.py` for profile, moving references and the ledger; `_section_refs.py` for section pointers; `_stale_titles.py`, added in this part, for "Chapter N, Title" citations whose title shares no content word with file N's H1), then every promise verified by opening the named chapter, then hand checks of the arithmetic the text asks the reader to trust (DiD table, SRM chi-square, sample-size scaling, the 560-enquiries derivation, the 3.4 kg steel tube, the 4,950 introductions). The stale-title script produces false positives on parenthetical fragments ("Chapter 13, Pattern 3)") and on the deliberately new-numbered Part II citations; all hits were read before being reported. The ledger over Parts 0–III flags 616 of 2,211 bolded terms as used before defined; most are common words the authors put in bold for emphasis ("and", "all", "first"). Filtered to terms first bolded in Part III and longer than five characters, 116 remain; the ones that matter are in the appendix.

### Ledger appendix — Part III (terms first bolded in Part III, used in plain text earlier)

Reading-order chapter where the term is first used → chapter that first bolds it. Only the terms a reader would notice.

- *environment variables*, *exit code* — Ch 17, Ch 18, Ch 20 → Ch 34 (S3-31; structural question 9)
- *type hints*, *linter*, *formatter*, *poetry*, *retrying* — Ch 17 → Ch 29 (Ch 17 previews Ch 29's toolchain by name; harmless, but Ch 17 could say "Chapter 29 sets these up")
- *SQL injection*, *timeouts* — Ch 18 → Ch 29 (Ch 18 warns without the term being taught; acceptable)
- *third normal form* — Ch 12 → Ch 28 (Ch 12 §12.1's explicit forward promise; kept)
- *recursive query* — Ch 13 → Ch 28 (forward promise; kept)
- *idempotent* — Ch 18 → Ch 28 (Ch 18 uses it once in the monthly report; Ch 20 lists it as a key term; Ch 28 bolds it. Three chapters, three treatments; fine for Reader 2, a wobble for Reader 1)
- *date dimension* — Ch 16 → Ch 28 (Ch 16 builds one in Power BI before Ch 28 names the pattern; acceptable, and a good cross-reference to add in Ch 28)
- *incremental*, *semantic layer* — Ch 16 → Ch 32 (BI chapter uses the words; Ch 32 defines them)
- *snapshot*, *snapshots* — Ch 23, Ch 26 → Ch 32 (different senses: a chart snapshot, a Git snapshot, a dbt snapshot; the index should distinguish)
- *p-value*, *chi-square*, *effect size*, *peeking*, *Welch's t-test*, *statsmodels* — Ch 22 → Ch 30 (by design; Ch 30's header says so)
- *confounding* — Ch 27 → Ch 31; *before-and-after* — Ch 15 → Ch 31; *selection* — Ch 5 → Ch 31 (all ordinary-language uses before the technical one)
- *fixtures*, *secrets manager* — Ch 34 → Ch 29 (the S1-11 seam, seen from the ledger)
- *difference-in-differences*, *regression discontinuity* — Ch 30 → Ch 31 (forward pointer in Ch 30's closing list; fine)
- *hash table*, *recursion* — Ch 28 → Ch 33 (Ch 28 says "hash join" and "recursive CTE"; Ch 33 says "this is what Chapter 28 did"; the best-kept promise in the part)
- *regression* — Ch 5 → Ch 30 (used in plain text from Chapter 5 onward, bolded in Chapter 30, taught in Chapter 37: S1-10 in one line)


---

## Part IV (Chapters 35–44) — appended after the reading of Part IV, 22 September 2026

Read in numeric order, which is the map's order for this part. Every chapter read in full, nothing edited. Chapter 44 is the only chapter in the part still marked "Draft v1 awaiting review" in the map; it was read to the same standard. Finding numbers continue (S1-13, S2-14, S3-37); structural questions continue from 11.

### Summary — Part IV

Part IV is the most internally consistent part so far, and the first that tells one story. Ten chapters share one analyst, one sales head, one sales manager, three sales executives, and one calendar: February 2026 (Chapter 35) through October 2026 (Chapter 43), one month per chapter, one problem per month. Every model is compared with a baseline, every score is tested once on held-out data, every "In the real world" is a vendor or a colleague being checked rather than a technique being admired. Reader 2 will recognise a working analytics team. Reader 1 will finish it, because each chapter reuses the previous chapter's pipeline and says so.

What breaks is at the edges of the part, not inside it:

1. **Part IV points forward into a Part V that was re-planned.** Seven pointers to "Chapter 52, Deploying and Monitoring Models" (that chapter is now *The Cloud, Containers & Infrastructure as Code*; the model chapter is 56), three to "Chapter 45, Business Metrics" (now *Data Ingestion & Integration*), one each to "Chapter 47 on data pipelines" (46) and "Chapter 61, Ethics" (64), and Chapter 44's closing paragraph, which describes Part V as "business metrics … experiments … deploying and monitoring models". A reader who turns the page from Chapter 44 expecting money and gets hashes and upserts has been misdirected by the book itself. This is S1-13.
2. **Chapter 42's answer key prints a Python error as an answer** and explains a result that never appeared. S1-14, the pattern of S1-6.
3. **Chapter 35 and Chapter 36 disagree about how many leads Riverstone gets**, by a factor of about 150, and Chapter 35's story reasons from the wrong figure. S2-14.
4. **Part IV's Riverstone is not Part II's Riverstone**: 5,000 accounts against 5,027 customers, 33,931 orders in 2025 against 46,356, 4,516 active accounts against 4,599, products P01–P24 against 101–108, three sales executives against eight. Every dataset is honest about being generated; nothing says how it relates to the database the reader built in Part II. S2-15.
5. **The calendar collides with Part III** (S2-16), and **the capstone's reusable function ignores one of its three settings** (S2-17).

Reader 1 survives Part IV. The regression gap (S1-10) is repaired by Chapter 37 for anyone reading in order, which is the strongest argument for structural question 10.

Part IV's arithmetic: 85,300 words, 424 key terms, 330 code blocks, 148 exercises, 86–121 hours. Running totals for Parts 0–IV: 389,600 words, 1,859 key terms, 739 exercises, 495–636 hours.

### S1 findings — Part IV

**S1-13. Part IV's forward pointers describe a Part V that no longer exists.** Extends S1-8 and S1-12.
Where, with the actual chapter under each number:
- "Chapter 52, Deploying and Monitoring Models" or "Chapter 52 covers deploying it": Ch 36 (§36.8, project stretch goal, Where-this-leads "Chapters 47 and 52"), Ch 38 (§38.3 "Chapter 52's monitoring"), Ch 39 (model card monitoring row; Where-this-leads), Ch 40 (Where-this-leads), Ch 44 (closing paragraph). Actual Chapter 52: *The Cloud, Containers & Infrastructure as Code*, sections 52.1–52.8, no `joblib`, no `predict`. The chapter that deploys and monitors a model is 56, *MLOps: Making Models Survive Production*.
- "Chapter 45, Business Metrics" / "Chapter 45's business metrics put rupee values on both sides": Ch 40 (§40.9 and Where-this-leads), Ch 44 (closing paragraph). Actual Chapter 45: *Data Ingestion & Integration*. No chapter with that title exists; the nearest are Chapter 23 (*Business Acumen, KPIs & Metrics*, Part II) and Chapter 75 (*Product Sense, Metrics, Case Studies & Guesstimates*).
- "Chapter 47 on data pipelines" (Ch 36 Tools) and "Chapters 47 and 52 move feature pipelines into scheduled data pipelines and deployed models" (Ch 36 Where-this-leads): pipelines are Chapter 46; 47 is *Data Quality, Observability & Contracts*.
- "Chapter 61, Ethics and Responsible Data Practice" (Ch 39 Where-this-leads): Chapter 61 is *Distributed Systems & Trade-offs*; the ethics chapter is 64, *Security, Privacy, Governance & Responsible AI*.
- Chapter 44's last section: "Part V moves from single models to the systems and habits that keep them honest and useful over time: business metrics that connect a model's output to money (Chapter 45), experiments … (Chapter 30) … and deploying and monitoring models once they leave a notebook for good (Chapter 52)." Part V is data engineering: ingestion, pipelines, quality, big data, storage, streaming, activation, cloud.
What the reader meets: the hand-off between parts is the one place a reader needs the map to be right. Chapter 44 tells them what comes next and is wrong on all three counts.
Cause: an earlier plan in which Part V was "from models to systems" (metrics, experiments, deployment). The plan moved deployment to Part VI (56) and made Part V the data-engineering part; the pointers were written to the old plan.
Smallest fix: the twelve edits above (52→56 seven times, 45→"Chapter 39 §39.5 and Chapter 44 already do this; Chapter 75 has the interview version", 47→46, 61→64), and a rewritten closing paragraph for Chapter 44 that describes the real Part V in two sentences.

**S1-14. Chapter 42, answer 9, prints a traceback as its output.** Extends S1-6.
Where: Ch 42 answers, exercise 9 ("find the pair of different products with the highest description similarity"). The code block's output is `ValueError: underlying array is read-only`, followed by a paragraph that reads as if the pair had been printed and its descriptions read ("The highest-similarity pair shares several generic descriptive words … plastic, food safe, litre").
What the reader meets: Reader 1 runs the code, gets the error, and finds the book got it too and carried on. The chapter's at-a-glance box says "every output shown is real", which is true and is the problem.
Cause: `np.fill_diagonal(content_no_diagonal.values, 0)` on a DataFrame built from `content_similarity.copy()`; in pandas 3 the `.values` view is read-only. The author ran it, pasted the error, and wrote the explanation from the intended result.
Smallest fix: `sims = content_similarity.copy(); np.fill_diagonal(sims, 0); content_no_diagonal = pd.DataFrame(sims, index=items, columns=items)`, re-run, and paste the pair the prose describes.

### S2 findings — Part IV

**S2-14. Chapters 35 and 36 disagree about how many leads Riverstone receives, and Chapter 35's story reasons from the wrong number.** Extends S3-21.
Where: Ch 35 §35.7 "In 2025 Riverstone received 30 real sales enquiries"; Ch 35's story (first week of February 2026): "How much can 30 leads tell anyone? … If a whole year of leads can't pin down the win rate more tightly than that, a test on a few weeks of leads can't tell a good score from a lucky one … the evaluation needs more leads than Riverstone gets in a month." Ch 36 §36.1, the next chapter: "Enquiries have grown from about 290 a month in 2023 to about 400 in 2025"; the CRM export has 12,294 rows and 826 wins; "This is Riverstone's full CRM, much bigger than the `leads` table in Chapter 13's one-year database, which holds only the enquiries reps logged themselves."
What the reader meets: Chapter 36 reconciles the *tables* correctly and is the first chapter to do so. But Chapter 35's story has already used the 30 as the company's whole year, and its argument to Anita ("a three-month pilot … at the end we compare its log loss with our benchmark of 0.50") is built on a base rate of 20% from 30 leads, when the company's real base rate (Chapter 36) is 7.7% from thousands. A reader who does both chapters in one week sees Meera give the sales head a benchmark that is wrong by a factor of two and a half. The running count of Riverstone's 2025 leads across the book is now: 30 (Ch 13, Ch 35), 43 (Ch 23's CRM), about 4,400 (Ch 36's CRM), 5,650 (Ch 23's marketing report).
Cause: Chapter 35 was written against the one-year database and Chapter 36 against the CRM generator, and the story in 35 was not revisited when 36 introduced the full CRM.
Smallest fix: in Ch 35, say "30 enquiries the reps logged themselves; the marketplace and web leads on the inside desk run to hundreds a month, and Chapter 36 uses all of them", keep the 30 for the hand calculations (they are good teaching numbers), and change the story's benchmark sentence to "on the reps' own leads the benchmark is 0.50; on the full CRM it will be lower, and Chapter 36 computes it."

**S2-15. Part IV's Riverstone datasets do not reconcile with the database the reader built in Part II, and nothing says they are not meant to.** Extends S3-34, structural question 6, and CPI-10.
Where: Part IV generates five new Riverstone universes: the CRM (Ch 36: 12,294 leads, 2023–2025), the accounts (Ch 37: 5,000 accounts, 4,516 stayed in 2025), the baskets (Ch 38, 42: 33,931 orders and 92,359 lines in 2025, 24 products P01–P24, 4,516 accounts), demand (Ch 40: four categories, 2.56 million units in 2025), tickets (Ch 41: 3,000). Part II's `riverstone_full` (Ch 14, Ch 20) has 5,027 customers, 116,194 orders, 46,356 of them in 2025, and 4,599 customers who ordered in 2025; Part II and III's products are 101–108; Chapter 28's staff table numbers reps 100–136 and lists eight Sales Executives; Part IV's reps are `rep_id` 4, 5 and 9 and "three sales executives" (Ch 36 §36.1, Ch 38 story), named Neha, Farah and Rahul (Ch 36, 38, 39, 44).
What the reader meets: Reader 2, who built Chapter 20's dashboard, knows Riverstone had 46,356 orders in 2025 and reads that it had 33,931. The numbers are close enough to look like errors rather than different worlds (5,000 vs 5,027; 4,516 vs 4,599). Reader 1 will not notice until an interviewer asks how big Riverstone is.
The part that helps: Part IV's three sales executives, Neha, Farah and Rahul, match Chapter 33's org chart and Chapter 28's order sheet, and not Chapter 28's eight invented executives. That is evidence for CPI-10's fix, not a new problem.
Cause: each Part IV generator was built to the size its method needs, from a data spec in `planning/data/`, with no rule tying it to `riverstone_full`.
Smallest fix: one paragraph in Chapter 35's at-a-glance box or Chapter 36 §36.1: "Part IV's datasets are generated at the scale each method needs. They share Riverstone's customers, products, and people but are not extracts of the full database from Chapter 14, so counts will not reconcile with Chapter 20's dashboard." Structural alternative, stated and stopped: structural question 13.

**S2-16. The story calendar: Part IV's month-per-chapter scheme collides with Part III's, and Chapter 44's memo predates the model it uses.** Extends S2-9 and S2-13.
Where: Part IV's stories are dated February 2026 (Ch 35), March (36), April (37), May (38), June (39), July (40), August (41), September (42), October (43). Chapter 44's memo is "Re: February 2026 retention call list", built from Chapter 37's churn model, which the arc has Meera build in April. Part III's stories: 3 February 2026 (Ch 29), 30 January to 15 February (Ch 30), March (Ch 28), April (Ch 31). Part II's are January 2026 (S2-9).
What the reader meets: in February 2026 Meera rewrites Imran's script (29), analyses the enquiry-form test (30), evaluates a vendor's lead score (35), and, per Chapter 44, sends a churn call list from a model that does not exist until April. Chapter 39 has the lead model "go live" in April, two months before June, while Chapter 36's March story proposes a one-month pilot; that one is consistent. Part IV's scheme is the only consistent calendar in the book and is worth keeping.
Cause: each part dated its stories independently; Chapter 44's memo was dated for the fiscal moment (a February call list) rather than for the arc.
Smallest fix: date Chapter 44's memo November 2026 and its story "two months later" accordingly; for Part III, give Chapters 28–31 months that do not overlap Part IV's (structural question 14 asks whether the coordinator wants one calendar for the book).

**S2-17. The capstone's reusable function ignores one of its three settings, and the "break-even rule" its exercises cite is never stated.**
Where: Ch 44 §44.6 `def build_call_list(accounts_df, call_cost=1200, margin=0.15, capacity=40)`: `call_cost` appears in the signature and nowhere in the body. §44.3's settings table promises for `CALL_COST`: "Higher: fewer accounts clear the break-even bar; lower: more do"; no code in §44.3–§44.6 applies a break-even bar. Exercise 1 asks whether an account is "worth a ₹1,200 call by the per-account break-even rule from section 44.3"; exercise 3 calls `build_call_list(accounts, call_cost=15000, capacity=40)` and then filters by 15,000 by hand outside the function, and its answer explains the difference between ranking and filtering, which is exactly what the function fails to do.
What the reader meets: the chapter's lesson is "wrap the six steps in one function so nothing is retyped"; the function silently drops the cost. Reader 2 spots it in the signature. Reader 1 runs exercise 3, sees `call_cost=15000` change nothing, and does not know why.
Cause: draft v1; the cost filter was planned and not written. Chapter 44 is the only chapter in Part IV still awaiting review.
Smallest fix: inside the function, `call_list = valid_split[valid_split["value_at_risk"] > call_cost].sort_values(...).head(capacity)`, state the rule in §44.3 in one line ("call an account when its value at risk exceeds the cost of the call"), and re-run the three outputs.

### S3 findings — Part IV

**S3-37. Ch 39 §39.1 says the model's accuracy is "worse" than predicting lost for everyone; its own numbers say the opposite.** "Its accuracy is 93.5%, which is *worse* than predicting 'lost' for everyone (93.4%, since 2,079 ÷ 2,225 = 0.934)." The model: (4 + 2,076) ÷ 2,225 = 93.48%; all-lost: 2,079 ÷ 2,225 = 93.44%. The model is one lead better. The point (accuracy is useless here) stands; the word does not. Fix: "no better than".

**S3-38. Ch 41 §41.7's prose describes a different run from its output.** "The neighbors it finds for 'broken' (*completely*, *received*, *crack*)": the printed output is completely, received, right, down, is. *Crack* appears only in answer 12's `vector_size=10` run. Fix: match the sentence to the output shown.

**S3-39. Ch 40's header cites Chapter 21 for "autocorrelation as an idea"; Chapter 21 does not contain the word.** Fix: drop the parenthesis or add a paragraph to Chapter 21.

**S3-40. Two promises into Chapters 40 and 44 are not kept.** Ch 37's story: "Two months later, Meera does use an open-source AutoML library for a weekend experiment on product demand (Chapter 40)"; Chapter 40 has no AutoML. Ch 40 §40.6: "Chapter 48's sensor work and the capstone use it that way" (ML forecasting with external features) and Where-this-leads: "Chapter 44, Capstone, can take demand forecasting as its end-to-end project"; Chapter 44 is churn only and mentions neither forecasting nor demand. Chapter 48 does use the sensor data (20 mentions), so that half is kept. Fix: delete the two capstone sentences and the AutoML sentence, or add a stretch goal to Chapter 44.

**S3-41. Chapter 35's vendor pilot is never resolved.** Ch 35's story ends with "a three-month pilot … accepted, at no charge" in February; Chapter 36 (March) has Meera build her own lead-scoring model without a word about the vendor, and no later chapter returns to it. Fix: one sentence in Chapter 36's story ("the vendor's pilot ran alongside; by June its log loss was 0.21 against the in-house model's 0.19, and Riverstone kept its own") or in Chapter 39's.

**S3-42. Chapters 37 and 39 send the reader to Chapter 22 for regression-coefficient intervals; the place that reads them is Chapter 30 §30.11.** Extends S1-10. Ch 37 §37.1 "`statsmodels` gives the interval, and Chapter 22 explains how to read it"; Common mistakes "Use `statsmodels` for confidence intervals (Chapter 22)"; Where-this-leads "Chapter 22 (statistical inference) … confidence intervals for coefficients"; Ch 39 Tools "statsmodels for regression with confidence intervals and p-values (Chapter 22)". Chapter 22 teaches confidence intervals for means and proportions; the coefficient table with `[0.025 0.975]` columns is Chapter 30 §30.11. Fix: "Chapter 30 §30.11".

**S3-43. Leftover drafting labels.** Ch 42 §42.3 "The popularity baseline (block F above)"; Ch 44 §44.4 "Then look at block D's output" and §44.6 "In block F's loop, change `[20, 40, 80]`". No code block in the manuscript carries a letter. Fix: "section 42.3's popularity baseline", "section 44.5's output", "the capacity loop above".

**S3-44. Ch 42 answer 12 answers a different exercise from the one asked.** The exercise: "Evaluate every method in this chapter using a time-based holdout … Do the rankings of methods change?" The answer evaluates only the popularity baseline (61.4%) and then says "the ranking of methods typically holds up under a time-based split too". Fix: run the other three (the `time_evaluate` helper is already written) or reword the exercise to ask for the baseline only.

**S3-45. Chapter 44's memo is dated before its own prediction moment makes sense.** The model scores accounts "as of 31 December 2024" for churn in 2025; the memo is "February 2026 retention call list" and asks the team to call accounts whose 2025 outcome is, by February 2026, already known. Chapter 36's first lesson is the prediction moment; Chapter 44's framing table states it and the memo then ignores it. For Reader 2 this is an S2. Fix: present the list as "what we would have sent in January 2025, and did the calls matter?" (a back-test, which is what the data supports), or re-score on 2025 features for 2026 and say the features are the previous year's.

**S3-46. Bible gaps and one name collision.** Extends S3-24 and S3-35. New named people in Part IV: Deepak Nair, production planner (Ch 40); Priya Menon, support lead (Ch 41); the e-commerce contractor (Ch 42); the marketing agency with nine segments (Ch 38). The bible additions list one Priya, under plants and operations; Chapter 33's Priya wrote the accounts team's invoice-matching script "two years ago"; Chapter 41's Priya Menon leads support. Either two Priyas or one Priya with three jobs. Fix: surnames in Chapter 33, and the four names added to the bible.

**S3-47. The one repeated story shape.** Five of Part IV's ten stories are "a vendor, contractor or agency makes a claim and Meera checks it against a baseline" (35 lead score, 37 AutoML, 38 the agency's nine segments, 42 the contractor's recommender, 43 the deep-learning churn platform). Each is good on its own; by Chapter 43 Reader 1 can write the ending before reading it, and Chapter 43's story says so itself ("having learned the pattern from Chapter 37's AutoML story"). Not a defect in any chapter; a note for the coordinator that Part IV's stories could lose one vendor without losing anything.

### S4 findings — Part IV

- Ch 39 §39.5 "The team can't work 660 leads in six months" (627 at the 0.077 threshold); model card "Test Jul–Sep 2025" (Chapter 36's test set runs to 2 October).
- Ch 43 §43.6 prints `digits [np.int64(0), np.int64(1), …]`, a NumPy 2 display artefact in the one output block a beginner will read first.
- Ch 41 §41.4's misclassified example begins "The you was fine but the delivery was late", a generator typo presented as a hard case; §41.1 says the inbox "gets a few thousand tickets a year" against 3,000 tickets in two years.
- Ch 40 and Ch 41 both state generator seed 20241 (sensors and tickets).
- Near-miss titles the stale-title script cannot catch: "Chapter 53, Deep Learning in Practice" (Ch 43; actual *Deep Learning in Depth*); "Chapter 48, Big Data and Distributed Computing" (Ch 40, 42; actual *& Distributed Compute*); "Chapter 50, Streaming and Real-Time Data" (Ch 40; actual *Streaming & Real-Time*).
- Ch 42 §42.3 has two consecutive paragraphs that both begin "**Reading it.**", the second reading the first's output.
- Ch 37 §37.0 "A fact you can't normally know": the 0.858 ceiling is a good device and is used again in §37.10; the reader is never told how it was computed (from the generator's true probabilities); one clause would do.

### Overwhelm profile — Part IV

Numeric order. Words exclude the answer key; hours are the chapters' own estimates.

| Ch | Words | Key terms | Code blocks | Exercises | Hours | Note |
|---|---|---|---|---|---|---|
| 35 | 14,036 | 56 | 34 | 16 | 10–14 | longest in the part; hand arithmetic throughout |
| 36 | 10,002 | 49 | 34 | 16 | 8–12 | |
| 37 | 11,809 | 72 | 46 | 16 | 14–18 | most key terms in the part; nine algorithm families |
| 38 | 8,117 | 47 | 32 | 16 | 8–12 | |
| 39 | 8,525 | 56 | 36 | 16 | 10–14 | |
| 40 | 8,455 | 50 | 36 | 16 | 10–14 | |
| 41 | 7,410 | 33 | 36 | 16 | 8–10 | |
| 42 | 5,985 | 24 | 30 | 16 | 6–9 | |
| 43 | 6,528 | 30 | 32 | 16 | 8–12 | |
| 44 | 4,400 | 7 | 14 | 4 | 4–6 | relief; draft v1 |
| **Part IV** | **85,267** | **424** | **330** | **148** | **86–121** | |
| **Parts 0–IV** | **389,643** | **1,859** | | **739** | **495–636** | |

Observations:
- The part is front-loaded: 35–37 are 36,000 words and 177 key terms in three chapters, then the chapters shorten steadily to the capstone. That is the right shape for a part whose later chapters reuse earlier pipelines, and it is the first part in the book with a shape.
- Key-term density is lower than Part III's (one term per 200 words against one per 125). Chapter 37's 72 terms are the exception and the chapter warns the reader ("It's the longest chapter in Part IV; take it one algorithm at a time").
- Every chapter has exactly 16 exercises in four bands, except the capstone's 4. Reader 1 knows what to expect by Chapter 38.
- Running hours for Parts 0–IV: 495–636 against Chapter 6's 208 for the analyst path (S1-7) and, for Chapter 83, the 764–980 whole-book figure. Parts V–VIII remain.

### References that break at renumbering — Part IV

`_journey_tools.py`: Ch 35: 9; 36: 8; 37: 5; 38: 7; 39: 7; 40: 4; 41: 1; 42: 1; 43: 1; 44: 4. **Part IV: 47. Running total, Parts 0–IV: 803.** Part IV cites Part II and III chapters by their old numbers throughout (13, 17, 18, 30, 31) and the ML bank as "Chapter 74" (new 75), consistently. Both section pointers in the part (37→35.9, 41→38.2) resolve.

### Promises checked — Part IV

| Promise (where made) | Kept? | Note |
|---|---|---|
| Ch 1 → "unstructured text" eventually (recalled by Ch 41) | Yes | Ch 1 line 236 |
| Ch 13's 30 leads, 6 won → Ch 35 | Yes | reused exactly; the 23 customers, 173 orders, ₹4,335,471 reconcile |
| Ch 22 → Ch 35/36 (p-values, samples) | Yes | |
| Ch 30 §30.11 regression → Ch 37 | Yes, in reverse | Ch 37 teaches what Ch 30 used (S1-10) |
| Ch 35 → Ch 36 "leakage-free features Meera worried about" | Yes | §36.5 names the response-time leak from Ch 35's story |
| Ch 35 story → vendor pilot | **Open** | S3-41 |
| Ch 36 → Ch 39 "cost analysis will tell us how many leads to call" | Yes | §39.5, and §39.5 is the best-kept promise in the part |
| Ch 36 ex. 15 feedback loop → Ch 39 §39.8 | Yes | |
| Ch 37 → Ch 39 (SHAP, calibration, imbalance) | Yes | all three delivered |
| Ch 37 story → Ch 40 AutoML weekend | **No** | S3-40 |
| Ch 37 → Ch 43 "stacks logistic regression into a network" | Yes | §43.1 uses Sharma Hardware's vector from Ch 35 |
| Ch 38 → Ch 42 "per-customer recommendations from the basket data" | Yes | |
| Ch 38 → Ch 41 "clusters support tickets" | Partly | Ch 41 uses LDA/NMF, not k-means; the point (judge unsupervised results) is kept |
| Ch 39 → Ch 40 WAPE | Yes | |
| Ch 40 → Ch 44 forecasting capstone | **No** | S3-40 |
| Ch 40 → Ch 48 sensors at scale | Kept by title | 20 sensor mentions in Ch 48; verified in Part V |
| Ch 41 → Ch 54 embeddings | Title correct | verified in Part VI |
| Ch 36/38/39/40/44 → Ch 52 deploy and monitor | **Wrong chapter** | S1-13 |
| Ch 40/44 → Ch 45 business metrics | **Wrong chapter** | S1-13 |
| Ch 39 → Ch 61 ethics | **Wrong chapter** | S1-13 |
| Ch 44 → Part V description | **Wrong** | S1-13 |
| All → Ch 74 ML bank | Title correct | verified in Part VIII |

### Findability — Part IV

- **Within the part, the best navigation in the book.** Every chapter's header names the earlier chapter for each prerequisite; Chapter 44's table (§44.8) says what each of 35–43 contributed; the "In plain English" sections each name the technique being introduced in bold. A reader can find where anything in Part IV was taught.
- **Out of the part, the worst.** Eleven pointers to Parts V and VI are wrong (S1-13). Until they are fixed, the "Where this leads" lists in 36, 38, 39, 40 and 44 send readers to the wrong chapters for deployment, monitoring, ethics, pipelines and business metrics.
- **The calendar is a findability device.** Because each story is dated, a reader can place any Part IV scene in Riverstone's year without a table. Parts II and III cannot be placed that way (S2-16).
- **Datasets (S2-15):** five more generators, each with a data spec in `planning/data/` (crm, accounts, baskets, demand, sensors, tickets, recommenders, deeplearning). Those specs are the table the book lacks; a one-page version belongs in the front matter.
- **Code-block letters** (S3-43) are the only dangling internal pointers in the part.
- **The 0.858 ceiling** (Ch 37 §37.0) is the kind of number a reader will want to find again and cannot, because it has no name in the key terms.

### Character arcs — Part IV

| Character | 35 | 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Meera Iyer | ✓ Feb | ✓ Mar | ✓ Apr | ✓ May | ✓ Jun | ✓ Jul | ✓ Aug | ✓ Sep | ✓ Oct | ✓ "Feb" | every chapter; surname now fixed as Iyer (28 uses) |
| Anita Rao | ✓ | ✓ (§36.1) | ("Anita") | ✓ | | | | | | ✓ memo | |
| Vikram Singh | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | the checker of vendors |
| Farah Khan | | | | | ✓ | | | | | ✓ | the model's "most useful critic" |
| Rahul (Mehta) | | | | | ✓ | | | | | | |
| Neha (Kulkarni) | | ✓ | | ✓ | | | | | | | |
| Deepak Nair | | | | | | ✓ | | | | | new; not in bible |
| Priya Menon | | | | | | | ✓ | | | | new; collides with Ch 33's Priya |
| Vendors / contractors / agency | ✓ | (freelancer) | ✓ | ✓ | | | | ✓ | ✓ | | S3-47 |

Meera's arc in Part IV is coherent and senior: she is asked by Anita in February, by Vikram from March, by the production planner in July and the support lead in August, and by Chapter 43 Vikram has "learned the pattern". Her Chapter 28 title, Sales Coordinator, has not been updated anywhere; by Chapter 44 she signs a memo "From: Analytics".

### The four checks — status after Part IV

- **A (reading order ≠ chapter numbers):** 47 more moving references (running total 803). Part IV is internally in the old numbering, like Part III. Eleven forward pointers into Parts V–VI are wrong by title (S1-13); they are not renumbering casualties but re-planning casualties, and the fix is different (a title check, not a number map).
- **B (Ch 25, 26, 27, 83 read harder):** 25–27 done; 83 pending.
- **C (book ends twice):** pending; 495–636 hours for Parts 0–IV.
- **D (first 200 pages):** done.

### Structural questions — added in Part IV

**12. Where does "business metrics that connect a model's output to money" live now?** Chapter 44's closing paragraph and Chapter 40 both promise it as Chapter 45. In the current plan it is done, well, inside Chapter 39 §39.5 (lead cost and value), Chapter 44 §44.3 (value at risk), Chapter 23 (KPIs, Part II) and Chapter 75 (interview metrics). If the coordinator agrees no chapter is missing, the fix is the pointers (S1-13). If the coordinator thinks Part IV needs a closing chapter on the economics of models, that is a new row in the map. Stated, not pursued.

**13. One Riverstone or several?** Part IV's five generated universes are within a few percent of `riverstone_full`'s figures without matching them (S2-15). Either the generators are re-seeded from the full database's customer and product tables (a companion-code change, no manuscript change beyond the counts), or the book says once that they are separate. The first is better for Reader 2 and costs the most; the second costs a paragraph. Stated, not pursued.

**14. One calendar for the book?** Part IV dates every story and the dates work. Parts II and III date some stories and the dates collide with Part IV's (S2-9, S2-13, S2-16). A one-page timeline in the bible (Meera's 2026, month by month, with each chapter's scene placed) would settle every future collision at the cost of re-dating five or six Part II–III scenes. Stated, not pursued.

### Method note — Part IV

Same method: each chapter read in full in numeric order (the map's order for Part IV), the three scripts, every promise verified by opening the named chapter, hand checks of the arithmetic the reader is asked to trust (the 4,950 introductions, the 593,775 combinations, 0.722 bits, the PCA eigenvalue 351.23, the Naive Bayes posterior 0.767, the Gini 0.1746, the 560 enquiries, the ₹1,079,730 profit at threshold 0, the ₹585,090 model-versus-rule gap, the 93.48%/93.44% accuracy pair, the NDCG discount 0.387, the XOR loss ln 2). The stale-title script's Part IV hits (39, 40, 52 references) were read in context and are reported in S1-13; it cannot catch near-miss titles (S4 list) and a title-word check against every "Chapter N, Title" citation remains the right copy-edit tool. The ledger over Parts 0–IV flags 134 terms first bolded in Part IV and used earlier; the ones that matter are below.

### Ledger appendix — Part IV (terms first bolded in Part IV, used in plain text earlier)

- *linear regression*, *logistic regression*, *log-odds*, *probability distribution* — Ch 30 → Ch 35/37 (S1-10, confirmed by the ledger: Chapter 30 uses all four in plain text before any chapter bolds them)
- *time-series* — Ch 31 → Ch 37; *seasonality* — Ch 13 → Ch 40; *decomposition* — Ch 5 → Ch 40 (ordinary-language uses; harmless)
- *censoring* — Ch 13 → Ch 36 (Chapter 13 uses the word for the 90-day rule without defining it; Chapter 36 defines it. A forward pointer in Ch 13 would help Reader 1)
- *cross-validation*, *false positive*, *early stopping* — Ch 22 → Ch 36/37/39 (Chapter 22 previews; acceptable)
- *baseline*, *date parts*, *scikit-learn* — Ch 18 → Ch 36/35 (Chapter 18 names scikit-learn once as a tool; fine)
- *calibration* — Ch 35 → Ch 36 → taught Ch 39 (three chapters use it before it is taught; Chapter 36 §36.9 says "Chapter 39 calls this calibration", which is the right way to do it)
- *k-means*, *k-nearest neighbors*, *naive bayes*, *decision tree*, *neuron* — Ch 35 → Ch 37/38/43 (Chapter 35's §35.11 map names every later algorithm; by design)
- *gradient boosting*, *xgboost*, *lightgbm*, *random forests*, *roc curve*, *tf-idf*, *backtesting*, *imbalanced-learn* — Ch 36 → Ch 37/39/40/41 (Chapter 36 previews the toolkit; acceptable, and each pointer names its chapter)
- *shap values*, *partial dependence*, *platt scaling*, *dummy variable*, *kernel*, *text classification* — Ch 37 → Ch 39/40/41/43 (same pattern)
- *matrix factorization*, *hidden layer* — Ch 41 → Ch 42/43 (one chapter early; fine)
- *element-by-element arithmetic* — Ch 35 → Ch 44 (Chapter 44 bolds a term Chapter 35 taught; the ledger's direction is reversed here because Ch 35 did not bold it; no action)


---

## Part V (Chapters 45–52) — appended after the reading of Part V, 22 September 2026

Read in numeric order, the map's order for this part. Every chapter read in full, nothing edited. Finding numbers continue (S1-15, S2-18, S3-49); structural questions continue from 14.

### Summary — Part V

Part V is one continuous build: Chapter 45 loads Riverstone's orders, dispatch files and CRM leads; 46 orchestrates them into the Daily Sales Flash; 47 adds tests, write–audit–publish, contracts and incidents; 48 and 49 take the plant's sensor archive to Spark, Parquet and Delta; 50 streams it; 51 writes lead scores back into the CRM; 52 deploys the lot. Each chapter's first section names what the previous chapter left undone, and each "Where this leads" hands on to the next. Within the part, this is the best-joined sequence in the book. The practice environment returns to the one-year database (175 orders, 43 leads, the 2 and 5 January business days), so every number is hand-checkable, and the chapters check them.

What breaks is the same class of defect as in Parts II and IV, now at its worst:

1. **Chapter 51 prints Python errors as the output of six code blocks**, including every demonstration the chapter exists to give (the first sync, the retry that recovers, the replay proof, the reconciliation report), and the prose after each describes results that never appeared. S1-15.
2. **Chapter 46's outputs contradict its prose from §46.6 onward**: the retry demonstration prints a failure and the text calls it a success; the bad-morning alert lists a step as failed that the text says succeeded; the fixed re-run prints "run succeeded: False" under a paragraph saying the report was delivered. One misplaced `api.shutdown()` is the cause. S1-16.
3. **Chapter 49's cost estimate is 365 times too large**, and Chapter 52 builds its total on it. S1-17.
4. **Chapter 50's watermark demonstration says the six late readings were counted and then says they were the row that was dropped.** S2-19.
5. Part V's stories are undated and its Riverstone runs at a third scale (a 300-million-reading archive, ₹3 lakh of bookings a day, Hotel Sai Palace with eleven open orders), with new unnamed contractors and a second Imran. S2-18.

Reader 1 survives Part V as a reader and is failed as a doer: three chapters' code cannot be followed as printed. Reader 2 will find S1-17 with a calculator in under a minute.

Part V's arithmetic: 64,100 words, 278 key terms, 191 code blocks, 112 exercises, 100–132 hours. Running totals for Parts 0–V: 453,700 words, 2,137 key terms, 851 exercises, 595–768 hours.

### S1 findings — Part V

**S1-15. Chapter 51 prints `NameError` as the output of six code blocks and narrates results that never appeared.** Extends S1-6 and S1-14.
Where: §51.2 (two blocks: `NameError: name 'sl' is not defined`), §51.3 "A first sync", §51.4 "A write that fails once, and recovers", §51.4 "A write that's genuinely repeated", §51.7 "Reconciliation for writes" (four blocks: `NameError: name 'scores' is not defined`). After each, the prose reads the intended result: "All six leads updated on the first attempt: `"replayed": False`"; "Lead 7's first attempt hit a `503`; the client waited and retried with the same idempotency key, and the second attempt succeeded"; "Sending it again returns `"replayed": True`"; "Six of seven leads match exactly. Lead 4 doesn't: 21 in the CRM against 20". The two blocks that do print real output (§51.3 setup, §51.6 webhook) sit between them.
What the reader meets: the chapter's argument is "prove a retried write doesn't double up"; the proof is an error message. §51.2's hand-check block also disagrees with its prose: the code prints "source Referral = 15 points" and tests for a score of 80; the prose says Bright Kitchens came from the Website and scores 55 + 10 = 65.
Cause: the setup block (`import sync_leads as sl`, `scores = ...`) is in §51.3, after §51.2's first use of `sl`; `scores` is never assigned anywhere in the printed chapter, so every later block fails. The chapter was pasted from a notebook run in a different order.
Smallest fix: move the setup block to the top of §51.2, add `scores = sl.lead_scores()` to it, re-run the chapter top to bottom, re-paste all eight outputs, and reconcile the Referral/Website hand check with whichever the data says.

**S1-16. Chapter 46's printed outputs contradict its prose from §46.6 onward.** Extends S1-6.
Where: §46.5 ends its last code block with `api.shutdown()` (line 512). Every later run's `raw_crm_leads` step calls a server that is no longer there. §46.6's retry demonstration prints "connection dropped (attempt 1)" and "run succeeded: False"; the prose: "Dagster waited one second, retried, and the second attempt loaded all 43 leads. The run succeeded without anyone being woken up." §46.7's bad-morning output has no `raw_crm_leads` line; the prose: "`raw_crm_leads` succeeded"; the alert two blocks later prints "Failed steps: ['daily_flash_flash_matches_erp', 'raw_crm_leads', 'raw_dispatch']". §46.7's fixed re-run prints "run succeeded: False" under "the report was delivered" (it was: `deliver_flash` does not depend on the CRM step, so the Flash went out while the run as a whole failed, which is the opposite of the chapter's lesson that delivery waits for everything to pass).
What the reader meets: three contradictions in the chapter whose rule is "never judge a pipeline by whether it finished", and no sentence explaining the False. Reader 1 running along gets the same outputs and does not know whether the book or the machine is wrong.
Cause: `api.shutdown()` belongs at the end of the chapter (as `spark.stop()` is at the end of Chapter 50 §50.6) and was placed at the end of §46.5.
Smallest fix: move `api.shutdown()` to the end of §46.7's last block, re-run §46.6–§46.7, re-paste. The alert's step list will then read `['daily_flash_flash_matches_erp', 'raw_dispatch']`, which is the correct teaching output.

**S1-17. Chapter 49's storage estimate multiplies by 365 twice, and Chapter 52 inherits the result.**
Where: Ch 49 §49.8: "one year across 40 machines: about 126 million readings a day-equivalent … 126,000,000 × 365 ÷ 216,000 × 1.3 MB ≈ 277 GB per year." 40 machines × 8,640 readings a day × 365 days is 126,144,000 readings a **year** (the chapter's own figure, mislabelled "a day-equivalent"); multiplying it by 365 again gives 46 billion readings. At the chapter's measured 6 bytes a reading, a year is about 0.76 GB, not 277 GB. Everything downstream carries the factor: "$6.40 a month, or roughly ₹530"; "5.3 GB … $0.027 a run"; "277 GB, about $1.39 a run"; exercise 9's "$41.55 a month" and "$0.80 a month"; Ch 52 §52.7 `storage_month = round(277 * 0.023, 2)`, "storage (Chapter 49): $6.37/month", "total estimate: $7.09/month", and Ch 52's Recap and exercise 8. The lesson (scan a week, not a year: about 52×) survives, because it is a ratio; every rupee and dollar figure does not.
What the reader meets: Reader 2 checks 40 × 8,640 × 365 and stops trusting the section. Reader 1 copies 277 GB into their own project estimate (Ch 49 project step 9, Ch 52 project step 7).
Cause: a units slip ("a day-equivalent") carried into the formula.
Smallest fix: "126 million readings a year … 126,000,000 ÷ 216,000 × 1.3 MB ≈ 0.76 GB per year, or about 3.8 GB over five years"; recompute the four money figures in §49.8, exercise 9, and Ch 52 §52.7 (`storage_month` becomes about $0.02, and the point that "storage is almost never the problem" becomes even stronger).

### S2 findings — Part V

**S2-18. Part V's stories are undated, its Riverstone runs at a third scale, and it adds four unnamed engineers and a second Imran.** Extends S2-15 and S2-16.
Where: Ch 45's story: "Riverstone's first proper data pipeline went live in February, built by a data engineer the company had hired on contract, with Meera as the business owner"; Hotel Sai Palace with "eleven open orders"; 214 orders wrong. Ch 46: "Two months after the pipeline went live"; "₹3,12,400 in bookings" for one day (the only Indian digit grouping in the book; and about ten times the one-year database's median day of ₹27,442.50 that Ch 47 §47.5 computes, and a tenth of `riverstone_full`'s). Ch 47: "on a Thursday … data that stopped on 4 January"; "the analytics engineer who had renamed the column". Ch 48: an archive of "about 300 million readings" (the dataset is 19.87 million) and "the contractor who took the job". Ch 48 §48.5: supervisors Anil Deshmukh, Sunita Rao and **Imran Shaikh**, against Imran of Chapters 2 and 29, who ran sales operations and "left". Ch 49: "One Tuesday … the data engineer". Ch 50: "on a Tuesday"; "the plant manager". Ch 51: "Three months after Riverstone's lead-scoring sync went live … a second sync, built six weeks earlier by a different contractor". Ch 52: "Riverstone's contract data engineer … a previous engineer". No year anywhere in the part.
What the reader meets: if the February is February 2026, Meera is simultaneously the business owner of the first pipeline (45), rewriting Imran's script (29), analysing the A/B test (30) and checking the vendor's lead score (35). If it is 2027, Part V is the only part set there and nothing says so. Hotel Sai Palace is not one of the one-year database's 24 accounts and is not in the bible.
Cause: each chapter dated its own story relative to itself ("two months after") and none anchored to the calendar Part IV established.
Smallest fix: one year marker in Ch 45's story and the four engineers given names in the bible (or one contractor throughout). Structural question 14 (one calendar for the book) covers the rest. The Imran collision is a one-word fix (a different surname or first name in Ch 48).

**S2-19. Chapter 50's late-data demonstration says the six late readings were counted and then says they were the row that was dropped.**
Where: §50.5 "Late data that still counts": batch 2 carries 6 late M-07 readings from 00:02; "they were **still counted**: Bhiwandi Main's 00:00–00:05 window shows **456 readings**, not the 450". Then "Late data that doesn't": batch 3 carries 50 very-late M-09 readings; the window "is unchanged at 456: the newly arrived stragglers were **dropped**". Then the progress block prints "batch 4: rows in 1506, watermark after 00:09:50, dropped as too late 1", and the prose reads it as: "The batch processed 1,506 rows, moved the watermark to 00:09:50, and dropped 1 row as too late … the six stragglers all belonged to one machine's window-and-plant group, so they amounted to a single dropped aggregate row." The 1,506-row batch is batch 2, whose six stragglers were counted three paragraphs earlier; the batch that dropped rows is batch 3 (1,550 rows, M-09). The printed progress is for the wrong query object, and the explanation describes the accepted readings as the dropped ones.
What the reader meets: the one number the chapter asks the reader to trust (456 = 450 + 6) is then explained away. Reader 2 notices that `query` in the progress block is batch 3's query yet reports batch 2's row count, which is the kind of thing that happens when `recentProgress` is read from a restarted query with a shared checkpoint.
Cause: the progress block was written for an earlier run and not re-read after the M-09 batch was added.
Smallest fix: print `recentProgress` for the batch-3 query, which should show 1,550 rows and a dropped state-row count for M-09's window, and rewrite the "six events, one row" explanation for M-09's fifty.

**S2-20. Chapter 51 states a scoring rule whose point values are never given, then sets an exercise on them.**
Where: §51.2 gives the rule in words ("points for the lead's current stage + points for how it arrived + a recency bonus … capped at 100") and prints, in the failed block, "stage Quoted = 55 points", "source Referral = 15 points", "+10". Exercise 4 asks for the score of a Contacted, Trade Show lead entered 3 days ago; the answer uses `STAGE_POINTS["Contacted"]` (30) and `SOURCE_POINTS["Trade Show"]` (20), which appear nowhere in the chapter. The reader cannot do exercise 4 from the text; they must open `sync_leads.py`.
Cause: the tables live in the companion module and the chapter assumed they would be printed by the (failed) hand-check block.
Smallest fix: print both point tables in §51.2 (they are a dozen lines) and reference them from exercise 4.

### S3 findings — Part V

**S3-49. Ch 45's closing list sends data-engineering questions to Chapter 72.** "Part VIII: data engineering and ingestion questions appear in Chapter 72, and system design cases in Chapter 77." Chapter 72 is the Python & pandas bank; the data-engineering bank is 77, which the same sentence cites. Fix: delete "Chapter 72".

**S3-50. Stale titles in Part V's closing lists.** Extends S1-12 and S1-13. "Chapter 63, Designing Automation & Integration Architecture" (Ch 46, 49, 51, 52; actual H1 *Automation Architecture & Governance*); "Chapter 62, The Economics of Data Platforms" (Ch 52) and "Chapter 62 (the economics of data platforms)" (Ch 49; actual *Data Architecture Patterns*). Same cause as S1-13; same one-line copy-edit rule.

**S3-51. Chapter 40's description of Chapter 48's sensor dataset does not match Chapter 48.** Extends S3-40. Ch 40 at-a-glance: "the same generator builds the 4.8-million-row version used in Chapter 48"; Ch 40 Where-this-leads: "Chapter 48 … runs this chapter's anomaly rules on 12 machines and 40 weeks"; Ch 40 Tools: `generate_riverstone_sensors.py --full`. Ch 48: 25 machines, two plants, 1 October to 31 December 2025, one reading every 10 seconds, 19,872,000 readings, built by `make_sensor_data.py`; machine ids `M-07` against Ch 40's `M01`; and Ch 48 never runs Ch 40's anomaly rules (it computes scrap rates and temperature averages). Two generators, two datasets, one claimed to be the other. Fix: make Ch 40's three sentences describe Ch 48's data, or have Ch 48 mention the drift rule once on its data.

**S3-52. Chapter 47's freshness check reads a column Chapter 45's load never created.** §47.5 `freshness_check("raw.dispatch", "file_day", 48)` and the output "newest file_day: 2026-01-02". Ch 45 §45.7 loaded `raw.dispatch` with six declared columns and no `file_day`; its checklist says "plus the file name and load date on every row" but the code does not add them. Ch 46's `ingest.load_dispatch` presumably does. Fix: add `file_day` (or `loaded_for`) to Ch 45's declared columns, which also delivers the checklist item.

**S3-53. Ch 46's Airflow translation and Ch 52's manifests are marked "not executed" correctly; Ch 46's §46.6 sensor block is too; but Ch 46 §46.3's two definition blocks print an empty output fence.** Two code blocks (the ingestion assets and the Flash assets) are followed by empty ``` ``` fences. Chapter 12's convention (S1-6 discussion) was to omit the fence when a block prints nothing. Cosmetic, and a Reader 1 will wonder whether something failed to print. Fix: remove the two empty fences or add `<!-- run: none -->`-style notes.

**S3-54. "The draft of this book made a claim worth repeating"** (Ch 48 §48.1). An author's note about the book's own drafting, in the reader's voice. Fix: "It's a claim worth repeating".

**S3-55. Ch 46's story figures are in Indian digit grouping** ("₹3,12,400", "₹3,24,900"); every other rupee figure in the book is grouped in threes ("₹312,400"). One story, two conventions. Fix: match the book.

### S4 findings — Part V

- Ch 45 §45.7 Parquet paragraph: "Chapter 2 measured the opposite result on large files" was not verified in this pass (see the method note); if Chapter 2 has no measurement, this is a broken backward pointer.
- Ch 48 §48.6 timings table gives "0.00 s" for Polars on one day; a measured zero reads as a typo. "< 0.01 s".
- Ch 49 §49.2 output "day.sqlite 16.3 MB" and prose "12 times smaller"; exercise 2's answer says 12.5. Fine, but the chapter's own rounding rule ("anything close is right") could be stated once.
- Ch 50 §50.2 "M-07 always goes to partition 1"; §50.5 uses M-07 for the counted stragglers and M-09 for the dropped ones; Ch 48 §48.7 uses M-07 for the `collect()` example and Ch 49 §49.5 for the probe correction. M-07 is Part V's favourite machine; harmless.
- Ch 51 §51.6's webhook lead is "Grand Horizon Hotels", deal value ₹350,000; Ch 51 §51.4 adds "Om Sai Provisions" as lead 7 (an existing Ch 13 customer). Consistent with the one-year database.
- Ch 52 §52.1's Figure 52.2 caption and the computed subnets agree exactly; a rare case of a figure that reconciles to its code.
- Ch 52 §52.7 "24.3x" and Recap "about 24 times" agree; exercise 8's answer restates them. After S1-17's fix, `total` becomes about $0.74 and the "about $7 a month" sentence needs rewriting.

### Overwhelm profile — Part V

| Ch | Words | Key terms | Code blocks | Exercises | Hours | Note |
|---|---|---|---|---|---|---|
| 45 | 10,691 | 37 | 44 | 14 | 14–18 | most code blocks in the part |
| 46 | 10,073 | 35 | 30 | 14 | 14–18 | |
| 47 | 8,873 | 34 | 25 | 14 | 12–16 | |
| 48 | 6,451 | 33 | 20 | 14 | 12–16 | needs Java and PySpark installed |
| 49 | 6,499 | 34 | 18 | 14 | 12–16 | |
| 50 | 6,515 | 38 | 19 | 14 | 12–16 | |
| 51 | 6,998 | 27 | 16 | 14 | 12–16 | six blocks print errors (S1-15) |
| 52 | 7,962 | 40 | 19 | 14 | 12–16 | nothing deployed; honestly labelled |
| **Part V** | **64,062** | **278** | **191** | **112** | **100–132** | |
| **Parts 0–V** | **453,705** | **2,137** | | **851** | **595–768** | |

Observations:
- Part V is the lightest part per chapter since Part I (8,000 words a chapter, 35 key terms) and claims the most hours per word: 100–132 hours for 64,000 words, because every chapter's project is a build ("run `reset()`, run your job, `apply_day(1)`, run it again"). The hours look right; Reader 1 will spend them in the terminal, not the book.
- Every chapter has exactly 14 exercises in the same four bands. Every chapter's Tools section lists exact versions and the companion reset script. Every chapter says what was not executed (Airflow, Kafka, Docker, Terraform, CI/CD) and why. That candour is the part's best feature and makes S1-15 and S1-16 more damaging: a reader who trusts "every output shown is from a real run" meets `NameError`.
- Running hours for Parts 0–V: 595–768 against the 764–980 whole-book claim to be checked at Chapter 83, with Parts VI–VIII still to add.

### References that break at renumbering — Part V

`_journey_tools.py`: Ch 45: 14; 46: 5; 47: 12; 48: 3; 49: 3; 50: 1; 51: 2; 52: 3. **Part V: 43. Running total, Parts 0–V: 846.** Part V cites Part II–III chapters by old numbers (12, 13, 14, 18, 29, 32) and the DE bank as "Chapter 77" (new 79), consistently. All three section pointers (46→45.8; 52→49.8 twice) resolve.

### Promises checked — Part V

| Promise (where made) | Kept? | Note |
|---|---|---|
| Ch 1 → Ch 47 "how data teams catch problems automatically" | Yes | Ch 1 line 333 names Chapter 47; Ch 47 recalls it |
| Ch 12 → Ch 45 "loading large and messy files reliably" | Yes | Ch 12 lines 2211 and 3569; §45.7 delivers |
| Ch 2 → Ch 45 hashes | Yes | Ch 2 mentions hashes six times |
| Ch 3 → Ch 46 bookings definition | Yes | Ch 3 line 200; Ch 46's `FLASH_SQL` matches (net of discount, excluding cancelled) |
| Ch 20 → Ch 46 the Flash as a scheduled script | Yes | |
| Ch 29 → Ch 45 API client with retries | Yes | |
| Ch 13 → Ch 45 the 43 leads, 175 orders, 2 cancelled | Yes | reconciles exactly |
| Ch 40 → Ch 48 the sensor dataset | **Not as described** | S3-51 |
| Ch 28 → Ch 49 materialized views | **No** | S3-28 confirmed: Ch 49 has none |
| Ch 32 → Ch 47 data contracts | Yes | §47.7 |
| Ch 45 → Ch 46 → Ch 47 → Ch 49 → Ch 50 → Ch 51 → Ch 52 chain | Yes | every hand-off named and delivered |
| Ch 46 §46.7 "Chapter 47 covers write–audit–publish" | Yes | §47.4, on the same 5 January failure |
| Ch 47 → Ch 49 "rollback by restoring a version" | Yes | §49.5 time travel |
| Ch 36/38/39/40/44 → "Chapter 52, Deploying and Monitoring Models" | **No** | Ch 52 deploys a pipeline, not a model; S1-13 confirmed from this side |
| Ch 40/44 → "Chapter 45, Business Metrics" | **No** | confirmed |
| Ch 45–52 → Ch 63, 62, 65 | Titles stale | S3-50; verified in Part VI |
| Ch 45–52 → Ch 77 DE bank | Title correct | verified in Part VIII |
| Ch 50 → Ch 58 "revisits the alerting decision with AI in the loop" | Title correct | verified in Part VI |

### Findability — Part V

- **Inside the part: the best chain in the book.** Each chapter opens by naming the previous chapter's unfinished business and closes by naming the next chapter's. The "Common mistakes" tables cite sections by number. A reader can find anything in Part V from any chapter in it.
- **The environment is findable.** Every chapter names its companion folder, its reset script, its versions, and which earlier dataset it needs first (Ch 49 and 50: "Generate the Chapter 48 dataset first").
- **Not-executed code is labelled** consistently (`<!-- run: none -->` in Ch 45, 46, 48, 50, 52). This is the convention S1-6/S1-15/S1-16 should be held to: blocks that were run and failed must not be printed as if they succeeded.
- **Out of the part**: 62, 63, 72 pointers wrong (S3-49, S3-50); 52 is the target of nine wrong pointers from Part IV.
- **Dataset reset**: Part V silently returns to the one-year database after Part IV's five larger universes. A sentence at the top of Ch 45 would tell Reader 2 why the CRM has 43 leads again (structural question 15).
- **The four engineers** (contract data engineer, "a different contractor", "the analytics engineer", "a previous engineer") are unnamed; a reader cannot tell whether Ch 45's, 49's and 52's engineer is one person.

### Character arcs — Part V

| Character | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | Note |
|---|---|---|---|---|---|---|---|---|---|
| Meera | ✓ business owner | ✓ reads run history | ✓ traces the stale dashboard | ✓ "asked the one question" | | ✓ (quoted) | ✓ traces the erased discount | ✓ (dashboard fails) | now the data lead in all but title |
| Anita Rao | ✓ | ✓ | ✓ | | | | | | |
| Vikram Singh | ✓ (Hotel Sai Palace) | | ✓ (told a customer the wrong month) | | | | | | |
| Contract data engineer | ✓ | ✓ ("the data engineer") | | | ✓ | | | ✓ ("he") | unnamed; possibly one person |
| A different contractor | | | | ✓ | | | ✓ | | unnamed |
| Analytics engineer | | | ✓ | | | | | | unnamed |
| Plant manager / supervisors | | | | | ✓ | ✓ | | | unnamed |
| Imran Shaikh (supervisor, M-03) | | | | ✓ | | | | | collides with Imran (Ch 2, 29) |
| Hotel Sai Palace | ✓ | | | | | | | | not a Ch 13 account; not in bible |

Meera's Part V arc is consistent with Part IV's: she owns, traces and explains; the engineers build. Nothing says when she stopped being the Sales Coordinator of Chapter 28's staff table. Vikram's arc has a nice reversal: in Part IV he checks vendors; in Part V he is twice the person who spots the wrong number first.

### The four checks — status after Part V

- **A (reading order ≠ chapter numbers):** 43 more moving references (running total 846). Part V is internally in the old numbering. Its pointers into Part VI (62, 63, 65) are stale by title (S3-50); its pointers back into Parts II–III resolve.
- **B (Ch 25, 26, 27, 83 read harder):** 25–27 done; 83 pending.
- **C (book ends twice):** pending; running 595–768 hours.
- **D (first 200 pages):** done.

### Structural questions — added in Part V

**15. Where does the reader learn that Part V's Riverstone is the one-year database again?** Part IV built five larger universes (S2-15) and Part V returns to 175 orders and 43 leads without a word. The right place is the first paragraph of Chapter 45 or the last of Chapter 44 (which needs rewriting anyway, S1-13). One sentence; the question is only which chapter owns it. Stated, not pursued.

**16. Should every chapter's code be re-run top to bottom before the next pass?** Chapters 18 (S1-6), 42 (S1-14), 46 (S1-16) and 51 (S1-15) print errors or contradicted outputs, and in every case the cause is a block run out of order or a resource shut down early. That is not an editing question but a production one: a scripted "run each chapter's blocks in printed order in a fresh session and diff the outputs" pass over the whole book. Stated, not pursued; noted here because the four cases share one cause.

**17. Should Chapter 49 §49.8 and Chapter 52 §52.7 be one worked estimate?** After S1-17's fix they must agree; today Chapter 52 hard-codes Chapter 49's wrong number (`277 * 0.023`). Either Chapter 52 quotes Chapter 49's result by reference only, or the estimate lives in one companion function both chapters call. Stated, not pursued.

### Method note — Part V

Same method: each chapter read in full in numeric order; the three scripts; every backward promise opened (Ch 1, 2, 3, 12, 20, 28, 29, 32, 40 → Part V) and every forward promise recorded for Parts VI–VIII; hand checks of the arithmetic the reader is asked to trust (175 orders, 43 leads, ₹38,710 and ₹18,750 for the two business days, 25 × 92 × 8,640 = 19,872,000, 14.6 ÷ 1.3, 456 = 450 + 6, 65,536 and 256 and 251, the 24.3× compute ratio, and §49.8's 277 GB, which is where S1-17 came from). The `NameError` and "run succeeded: False" outputs were found by reading, not by script; a script that flags any output block containing `Error:` or `Traceback` would have found S1-6, S1-14, S1-15 and S1-16 in seconds and is recommended (structural question 16). One backward pointer (Ch 45 → Ch 2's Parquet measurement) was not verified in this pass and is listed under S4 rather than asserted.

*Verification completed after the section above was drafted:* Chapter 2 does measure Parquet ("Parquet was the smallest file, and about ten times faster than CSV", Ch 2 line 330), so Ch 45 §45.7's backward pointer is kept and the first S4 bullet is withdrawn. Chapter 12 mentions ACID once (Ch 49's "Chapter 12 introduced these" is kept in substance). Chapter 7 introduces RPA (12 mentions) and draws the source-to-decision flow (Ch 51's two backward pointers kept). Chapter 20 has Apps Script triggers (Ch 46 §46.1 kept). Chapter 65's H1 is *FinOps: The Economics of Data Platforms*, so Ch 52's "Chapter 65, FinOps" is right and its "Chapter 62, The Economics of Data Platforms" is Chapter 65's subtitle attached to Chapter 62's number (S3-50 stands). The bible additions have no Hotel Sai Palace, no Anil Deshmukh, no Sunita Rao, no Imran Shaikh, and no contractor (S2-18 stands).

### Ledger appendix — Part V (terms first bolded in Part V, used in plain text earlier)

- *idempotency* — Ch 20 → Ch 46; *alert fatigue*, *incidents* — Ch 20 → Ch 47; *webhooks* — Ch 20 → Ch 51; *transient failures* — Ch 20 → Ch 45 (Chapter 20's automation chapter previews Part V's vocabulary by name; each pointer should name its chapter, and most do)
- *backfill*, *look-back window* — Ch 25 / Ch 45 → Ch 46; *data contracts*, *freshness* — Ch 25 → Ch 47; *late data* — Ch 25 → Ch 50; *reconciliation check* — Ch 25 → Ch 45 (Chapter 25's Business Analyst track uses five Part V terms in plain text; a "these are Part V's" aside would help Reader 1)
- *containers*, *continuous integration* — Ch 26 → Ch 52 (Ch 26's Git chapter mentions CI; fine)
- *lineage*, *column-level lineage*, *observability*, *dependency graph*, *source systems* — Ch 32 → Ch 47/46/45 (dbt's vocabulary arrives one part early; Ch 47 §47.6 says "Chapter 46's pipeline already declares its dependencies, so lineage is free" and could add "as Chapter 32's DAG did")
- *shuffle* — Ch 36 → Ch 48; *small files* — Ch 35 → Ch 50; *lead score* — Ch 35 → Ch 51 (Part IV uses three Part V terms in passing; harmless)
- *partition* — Ch 13 → Ch 46 (SQL window `PARTITION BY` vs pipeline partition: two meanings, one word; the index should distinguish)
- *vacuum* — Ch 28 → Ch 50 (PostgreSQL's `VACUUM` vs Delta's; same word, related idea)
- *time travel* — Ch 47 → Ch 49 (Ch 47 promises it; Ch 49 delivers; by design)
- *hashes*, *fingerprint*, *columnar*, *least privilege*, *authentication* — Ch 2 → Ch 45/49/52 (Chapter 2's previews, all kept)
- *ingestion*, *data contract*, *data test*, *isolation* — Ch 8 → Ch 45/47/49 (Chapter 8's role descriptions use the words; acceptable)
- *orchestrator*, *credentials*, *rate limits*, *audit trail* — Ch 18 → Ch 46/45/51 (Chapter 18's API section previews; acceptable)
- *not executed* — Ch 50 → Ch 52 (the labelling convention itself is first bolded in Chapter 52; Chapter 45 uses it first)


---

## Part VI (Chapters 53–59) — Production ML, Generative AI & MLOps

Read in numeric order (53, 54, 55, 56, 57, 58, 59), which the chapter map confirms is the reading order. No renumbering inside the part. Reader 1 arrives at Ch 53 having (per the book's own account) spent 595–768 hours; Reader 2 will most likely start here or at Ch 54.

### Overwhelm profile

| Ch | Words | Key terms | Code blocks | Exercises | Stated hours | Verdict |
|---|---|---|---|---|---|---|
| 53 Deep Learning | 9,970 | 67 | 28 | 18 | 14–18 | Heaviest chapter of the part; 67 key terms is the highest count since Ch 28 |
| 54 Generative AI & LLMs | 9,577 | 48 | 21 | 18 | 14–18 | Dense but well paced; §54.12 landscape will date first |
| 55 Building AI Applications | 8,894 | 43 | 27 | 18 | 16–20 | Fine; voice slips into first person (see S3-58) |
| 56 MLOps | 7,840 | 50 | 21 | 18 | 16–20 | Fine; one broken table (S3-59) |
| 57 LLMOps | 6,787 | 43 | 16 | 18 | 14–18 | Best-paced chapter in the part |
| 58 Intelligent Automation | 6,721 | 36 | 16 | 18 | 14–18 | Fine, but recap and story contradict its own measured result (S1-18) |
| 59 Industry Case Studies | 5,039 | 26 | 0 | 0 | 3–4 | Reading chapter; retells earlier chapters inaccurately in places (S2-22) |

Part total: 54,828 words, 313 key terms, 129 code blocks, 108 exercises, 91–116 hours. Running totals after Part VI: **508,533 words; 2,450 key terms; 959 exercises; 686–884 hours**. The book's whole-book claim (764–980 hours) is now within reach of Parts VII–VIII, so the check is deferred to Ch 83 as planned.

Both readers: this is the first part where nothing is out of order and nothing is missing. The dependency lines in the "Before you start" boxes are honest. Reader 2 can begin at Ch 54 with Ch 53 §53.1–53.3 as a skim.

### First-appearance ledger

Fifty-six terms are used in Part VI before their defining chapter (filtered to terms longer than five characters). Almost all are benign: the defining chapter is in the same part and the earlier use is in Part V or the Part IV time-series chapter (transformer, embedding, tokens, context window, registry, deploy, retrain). Three deserve a note:

- **"choose the threshold"** is defined by the ledger in Ch 53 but used from Ch 39 onward; that is Ch 39's job and the glossary anchor should move there (S4).
- **"an exception path"** and **"grounding"** are defined in Ch 55 but used in Ch 54's structured-output section, one chapter earlier. Ch 54 §54.7 uses "exception path" as though it were established. Smallest fix: one bracketed gloss at the Ch 54 first use.
- **"pruning"** defined in Ch 53 but used in Ch 48 (tree pruning) — a different sense; the glossary needs two entries or a disambiguation.

### Promise ledger (Part VI)

| Promise | Made in | Kept? |
|---|---|---|
| "This is the chapter Chapter 1 promised" (PO emails retyped) | Ch 58 §Why | Yes: Ch 1 line 244 says customers "still send orders by email or WhatsApp, and someone re-types them". Ch 58 overstates it as "the book opened with" that scene; Ch 1 opens with Meera and the Mumbai customer count. Reword to "Chapter 1 mentioned" (S4). |
| Ch 53 §53.11 "Chapter 56 keeps it alive" | Ch 53 | Yes |
| Ch 54 → Ch 55 assistant, Ch 57 operations | Ch 54 | Yes |
| Ch 56 "Chapter 57 covers the model you don't own" | Ch 56 | Yes |
| Ch 57 "Chapter 58 connects this pipeline to systems that write" | Ch 57 | Yes |
| Ch 59 "Chapter 53, 55 and 58 hold the runnable versions of cases 1, 7 and 9" | Ch 59 | Partly: case 7 is labelled a composite (see S2-22) |
| Ch 59 "Chapter 75, Case Study & Take-Home Bank" | Ch 59 | Title wrong (S3-57) |
| Ch 59 "Chapter 79, The First 90 Days" | Ch 59 | No such chapter (S1-19) |

### Findability audit

Section-number pointers inside Part VI all resolve (Ch 57 → 54.7, 57.5, 57.9; Ch 58 → 58.5, 58.7, 58.8). Cross-part pointers by chapter number are where the damage is, and every one of them is a pre-renumbering number or a wrong attribution:

- Ch 53 header: "Chapter 19 (regression)" ×4 — Ch 19 is Spreadsheet Automation. Regression is Ch 37 (extends S1-10).
- Ch 53 header, §53.9 table and closing: "Chapter 38" for gradient boosting and leakage ×9 — Ch 38 is Unsupervised Learning; boosting is Ch 37/39 territory and leakage is Ch 36 (extends S1-12).
- Ch 53 header: "Chapter 17 (NumPy and pandas)" — Ch 17 is not pandas (extends S1-12, "Chapter 17 = pandas" class).
- Ch 54, 55, 56 headers: "Chapter 38 (evaluation)" — evaluation is Ch 39.
- Ch 59 Case 2: "Chapter 19's seasonal model" — no seasonal model in Ch 19; the seasonality teaching is Ch 23 (KPIs) and the time-series material in Part IV.
- Ch 59 Case 3: "Chapter 38's leakage" — Ch 36.
- Ch 59 Where-this-leads: "Part VII (Chapters 60–68)" — Part VII is 60–67; Ch 68 opens Part VIII.
- All six "Where this leads" lists in 53–58 name "Chapter 64, Responsible AI & Governance" (actual: Security, Privacy, Governance & Responsible AI) and "Chapter 74, Machine Learning & AI Question Bank" (actual: Machine Learning Question Bank; the AI bank is Ch 79).

After renumbering (OLD_TO_NEW), every Part VI chapter keeps its number, so Part VI's internal pointers are safe. The forward pointers to 74, 75 and 79 become 75, 76 and 81 and must be re-pointed at the same time as the titles are fixed.

### Character arcs

- **Meera Iyer** writes the Ch 57 post-mortem (October) and runs the Ch 58 pilot numbers (November–March). Ch 1 introduced her as the sales coordinator who would have been retyping these very orders. Ch 58 never says so. It is the best arc payoff in the book and it is left on the table (S3-62, structural Q19).
- **Anita Rao** (Sales Head, established Ch 1 and Ch 3, "she" throughout) appears in Ch 58's story as "the sales head … His complaint is specific". Either a new, unnamed male sales head or a pronoun error (S2-23).
- **The coordinator** whose job Ch 58 automates is unnamed and female. Given Meera's origin, either she is Meera's successor and should be named, or the book means Meera and the timeline is broken.
- **Riverstone customers**: Ch 54/55/51 use Green Leaf Hotels, Bright Kitchens, Om Sai Provisions and Sunrise Caterers (all in Ch 13's list) but also Delta Hospitality and Grand Horizon, which appear nowhere in Part II (extends S2-15's universe problem; S4 here).

### Story calendar (Part VI)

| Ch | Date evidence | Note |
|---|---|---|
| 53 | "Three weeks later"; tools "September 2026" | Trial on day shift; no month given |
| 56 | Camera "runs quietly from March"; lamps May (week 8); new mould week 16; customer return August; `trained_at 2026-03-02` | Coherent |
| 57 | Extraction pipeline live, "a Monday in October"; nightly golden set switched off in August | Pipeline already writing to ERP straight-through |
| 58 | Intake "goes live in assisted mode in November"; January numbers; straight-through question "comes back in March"; audit log timestamps `2026-03-02` | Conflicts with Ch 57 (S2-24) |
| 59 | "six years of small pieces" (Case 9) | Conflicts with the whole calendar (S3-60) |

### Findings

**S1-18 — Ch 58's recap and story contradict its own measured segment result.** §58.8 measures accuracy by email style and its headline is "not where anyone would have guessed": bulleted, forwarded and terse emails are 37 of 37 correct, while **tables are 7 of 11 and prose 3 of 11**. The text then says the automatic class "is not 'tidy emails' but 'bulleted, forwarded, and terse'". Yet the Recap says "**The table-style emails were extracted perfectly and could go automatic today**", the real-world story ends "the twelve customers who send tidy tables go automatic", and the §58.8 bullet list above the code still proposes "only orders from the five customers who always send the same tidy table, where accuracy is near perfect". Exercise 8's answer gets it right. CAUSE: the measured output was changed (or first produced) after the surrounding prose was written. Reader 1 will trust the recap; Reader 2 will spot the contradiction and stop trusting the chapter. Smallest fix: rewrite the recap bullet, the story's last sentence and the §58.8 bullet to name bulleted/forwarded/terse as the automatic segment (three sentences).

**S1-19 — Ch 59 points to "Chapter 79, The First 90 Days", which does not exist.** Ch 79 is the GenAI, LLM & MLOps Question Bank. No chapter in the manuscript is titled The First 90 Days; the phrase occurs only as a topic inside Ch 6, Ch 67 and Ch 80. CAUSE: stale title from an earlier plan (same class as S1-8, S1-12, S1-13, S3-50). Smallest fix: point to Ch 67 (The Architect as Leader) or Ch 83 (The Long Game), whichever holds the first-90-days material after the structural decision in Q18, and renumber with OLD_TO_NEW.

**S2-21 — Ch 57 story says the extraction pipeline was loading orders straight into the ERP in October; Ch 58 says intake went live in assisted mode in November and that straight-through was rejected.** Ch 57 §In the real world: "Riverstone's extraction pipeline runs at 06:00 every weekday… loads nothing… Nothing wrong was written to the ERP", i.e. an unattended write path in production before Ch 58's pilot exists. Ch 58's whole argument is that unattended writes were never shipped. CAUSE: the two stories were written independently against the same pipeline. Smallest fix: move Ch 57's incident to "the assisted pilot's morning draft run" (the drafts are empty rather than the ERP), which keeps every number, or date it after March when the tidy segment goes automatic. Structural question Q20.

**S2-22 — Ch 59 miscounts and mislabels its own cases.** The introduction says "Three are Riverstone's… The other six are composites". Only Cases 1 and 9 are headed "Riverstone's own"; Case 7 (support automation) is headed "A composite… representative numbers" and set at "a subscription business", yet Where-this-leads says Ch 55 holds "the runnable version" of case 7 and Ch 55 built Riverstone's assistant. Case 7's numbers (35% resolved, thumbs up/down, refusal path) are Ch 55's shape with different figures. CAUSE: Case 7 was Riverstone's in an earlier draft and was genericised without updating the count or the pointer. Smallest fix: either restore Case 7 as Riverstone's with Ch 55's measured numbers, or change "Three" to "Two" and drop Ch 55 from the runnable list.

**S2-23 — Ch 58's sales head is male; the book's Sales Head is Anita Rao.** "the sales head wants it switched off. His complaint is specific". Anita Rao is Sales Head in Ch 1, Ch 3 and the bible, and drives the Ch 62 and Ch 64 stories. CAUSE: story written without the bible. Smallest fix: "Anita wants it switched off. Her complaint is specific" and the closing quote addressed to her.

**S2-24 — Ch 59 Case 1 retells Ch 53/56 with the wrong incident.** Case 1 says the day-shift-only model was "Found by a customer return, six weeks later" and fixed with night-shift images, brightness augmentation and a brightness monitor. In the source chapters these are two different events: Ch 53's story is the day-shift trial caught during the night-shift trial (no customer involved), and Ch 56's August customer return is **flash from the new mould**, which the brightness monitor could not see (that is Ch 56's whole lesson). Case 1 also quotes "97.5% of defects caught", which does not appear in Ch 53 (Ch 53 quotes 95% at threshold 0.1, and the ₹13,840 operating point at 0.01 without a recall figure at that line). CAUSE: the case table was written from memory of the two chapters. Smallest fix: split "What went wrong" into the two events as the chapters tell them, and copy the recall figure from Ch 53's threshold table.

**S3-56 — Ch 53–56 headers misattribute Ch 38 and Ch 19** (details in the findability audit). Extends S1-10 and S1-12; listed here so the fix pass covers 53–56 in one sweep: 53:9, 53:769, 53:776, 53:795, 54:9, 55:9, 56 header, 59:86, 59:107.

**S3-57 — Ch 59 forward titles are near-misses.** "Chapter 75, Case Study & Take-Home Bank" (actual: Product Sense, Metrics, Case Studies & Guesstimates; take-homes are Ch 82); "Chapter 74, Machine Learning & AI Question Bank" ×6 across the part (actual: Machine Learning Question Bank); "Chapter 64, Responsible AI & Governance" ×6 (actual: Security, Privacy, Governance & Responsible AI). CAUSE: titles copied from the plan before the chapters were written. Smallest fix: one `_stale_titles.py` pass over 53–59 with the current H1s.

**S3-58 — Ch 55 speaks in the first person; the rest of the book does not.** "cost me an afternoon", "I can't run one here", "I recommend" (8 hits in Ch 55, 10 in Ch 53, 5 each in 54 and 56, 1–3 in 57–59 and 63/67). Most Ch 53 hits are the reader's checklist "I can…", which is the book's convention; the Ch 55 ones are the author's voice. CAUSE: Ch 55 drafted by a different hand or in a different session. Smallest fix: recast the six authorial sentences in Ch 55 to the book's impersonal register.

**S3-59 — Ch 56 §56.7 monitoring table is split by an inserted figure.** Lines 352–360: the table header row and its body rows are separated by the figure and caption, so the header renders as a one-row table and the body as loose pipe-delimited lines. CAUSE: figure inserted mid-table. Smallest fix: move the figure below the table.

**S3-60 — Ch 59 Case 9 says the order-to-cash project "was six years of small pieces".** Every dated event from Ch 10 to Ch 58 falls between mid-2025 and March 2027, about 21 months. CAUSE: the sentence describes a typical career rather than Riverstone's calendar. Smallest fix: "two years of small pieces", or attribute the six years to the composite pattern rather than to Riverstone.

**S3-61 — Ch 57 figure files and captions are crossed.** Figure 57.2 (caption "cost and failure") loads `fig57-3-cost-and-failure.svg`; Figure 57.3 (topic drift) loads `fig57-2-topic-drift.svg`. The images are right, the file numbers are swapped. CAUSE: sections reordered after the figures were drawn. Smallest fix: rename the two files or renumber the captions.

**S3-62 — Ch 58 never connects the automated coordinator's job to Meera's Ch 1 job.** Ch 1: "Meera Iyer has just joined Riverstone Supplies as a sales coordinator." Ch 58: Meera measures the pilot that changes an unnamed coordinator's job, and the chapter's §58.9 is about talking to that person. One sentence ("the desk Meera sat at in Chapter 1") would close the longest arc in the book. CAUSE: arc not tracked across parts (same class as S2-18's undated stories). Smallest fix: one sentence in §58.9 or the story.

**S3-63 — Ch 58 §58.4 replay counts disagree.** "duplicates ignored on the replay: 53" and, two lines later, "audit entries recording the duplicates: 59"; the prose then says "we ignored 59 duplicate submissions". The 59 is right (53 loaded + 6 awaiting approval are all orders). CAUSE: `run()` counts only loaded-then-duplicated emails under `duplicate_ignored` while the audit log records all 59. Smallest fix: make `run()`'s counter match the audit log, or explain the six in one sentence.

**S3-64 — Ch 58 answer 3 prose does not match its own output.** The query returns the *largest* held order (₹145,800) but the prose says "the smallest held one just above" the limit; the smallest held is ₹100,500 (answer 4). Also answer 9's break-even ("an error would have to cost under about ₹15") does not follow from the chapter's numbers: against assisted, (198 − 47) ÷ 6.7 ≈ ₹23; against manual ≈ ₹83. CAUSE: prose written before the numbers were final. Smallest fix: change the query to `ORDER BY order_value ASC` for the held row, and recompute the ₹15.

**S3-65 — Ch 57 §57.9 code changes directory into `../ch55` and back.** Reader 1 following "Work in `companion/ch57`" hits an `os.chdir` dance that the book has not used anywhere else; if any line fails between the two `chdir`s the reader is left in the wrong folder. CAUSE: the Ch 55 assistant loads its corpus by relative path. Smallest fix: give `SupportAssistant` a `root=` argument (one line in the companion) and drop the `chdir`s.

**S3-66 — Ch 54 §54.12 names live products and prices "as of September 2026", including the model this review runs on.** Nothing wrong today; it will be the first paragraph in the book to be wrong. CAUSE: landscape section in the body rather than an appendix. Smallest fix: move §54.12 to an appendix with its own date stamp, and keep one sentence in the chapter. (Same treatment as the "Tools" sections, which already carry "Checked in September 2026".)

**S3-67 — Ch 58 audit-log timestamps are `2026-03-02` while the story is November.** The pipeline's actor string and Ch 56's `trained_at` share the March date; the story says the pilot went live in November. CAUSE: companion data generated from Ch 56's clock. Smallest fix: parameterise the run date in `intake.py` or say in the story that the demonstration replays a March morning.

### Beginner survival (Reader 1)

Reader 1 survives Part VI better than Part V. The hardest stretch is Ch 53 §53.4–53.6 (convolutions and Sobel filters), where 67 key terms arrive in one chapter and the "In plain English" box does not cover backpropagation before §53.3 uses it. Ch 54 is the best-taught chapter for a beginner in the whole book: every number is computed on the page. Ch 58 is the first chapter that reads like the job the reader is being trained for, and it is where the contradiction in S1-18 will hurt most, because Reader 1 has no way to know which of the two statements to believe.

### Reader 2

Reader 2 starts at Ch 54, reads 55–58 closely, skims 59. They will notice S1-18 and S2-22 immediately and S2-21 on a second read. They will also notice that Ch 57's §57.4 "provider changed the model" simulation and Ch 58's ROI table are the two pieces they would show a manager, and both are internally sound.

### Structural questions (continued)

18. **Where does "The First 90 Days" live?** Ch 59 promises it as a chapter; Ch 6, Ch 67 and Ch 80 each hold a fragment. Decide whether it is a section of Ch 83 (The Long Game) or a chapter of its own in Part VIII, then re-point Ch 59, Ch 6 and Ch 67. Stated; stopped.
19. **Is the Ch 58 coordinator Meera's successor, or Meera?** The answer fixes S3-62 and the Ch 1 → Ch 58 arc. If the book wants Meera in Ch 58 as the architect (which Ch 63's promotion supports), name the successor. Stated; stopped.
20. **Which came first, Ch 57's October incident or Ch 58's November pilot?** One of the two stories has to move. Recommendation: Ch 57's incident becomes the assisted pilot's empty morning drafts, which needs no new numbers. Stated; stopped.
21. **Should §54.12 (the landscape) and the "Checked in September 2026" tool lists be pulled into a dated appendix?** Every Part VI chapter carries one; they will all expire together. Stated; stopped.

### Printed-error scan (Part VI)

The whole-book grep for printed Python errors (structural Q16) finds no hits in 53–59. Every code block in the part prints what its prose says it prints, with the one exception of the S3-63 count mismatch.


---

## Part VII (Chapters 60–67) — Architecture, Governance & Leadership

Read in numeric order (60–67), which the chapter map confirms. No renumbering inside the part. This is the part where the book stops teaching skills and starts telling one continuous story about Meera's platform, so the calendar and the cross-references carry more weight than anywhere since Part II.

### Overwhelm profile

| Ch | Words | Key terms | Code blocks | Exercises | Stated hours | Verdict |
|---|---|---|---|---|---|---|
| 60 Designing Whole Systems | 7,175 | 18 | 0 | 18 | 12–15 | Light and clear; the best-structured chapter in the part |
| 61 Distributed Systems | 6,923 | 27 | 2 | 17 | 10–12 | Fine; one runnable simulation |
| 62 Data Architecture Patterns | 7,071 | 23 | 0 | 20 | 10–12 | Fine; §62.5 inserted later (figure numbering shows it) |
| 63 Automation Architecture | 7,661 | 25 | 1 | 17 | 12–14 | Fine; cites a planning file the reader cannot see (S2-27) |
| 64 Security, Privacy, Governance | 7,835 | 37 | 4 | 17 | 14–16 | Heaviest chapter; the fairness audit is excellent, the printed label contradicts it (S1-21) |
| 65 FinOps | 5,808 | 18 | 4 | 17 | 8–10 | Fine; one printed number contradicts its own table (S1-22) |
| 66 Data Strategy & Teams | 5,647 | 17 | 4 | 17 | 8–10 | Printed IndexError (S1-20) |
| 67 The Architect as Leader | 5,850 | 11 | 0 | 0 | "however long" | Reads as the end of the book (check C) |

Part total: 53,970 words, 176 key terms, 15 code blocks, 123 exercises, 74–89 stated hours. Running totals after Part VII: **562,503 words; 2,626 key terms; 1,082 exercises; 760–973 hours**. The whole-book claim of 764–980 hours is now met before Part VIII begins, so Part VIII's own hours (68: 2–3, 69: 3–4, banks unstated) push the true total past the claim. Reported at Ch 83.

Both readers: pacing is the best in the book. Reader 1 can follow every chapter because nothing depends on code; Reader 2 will read 60–62 and 64–65 closely and skim 63, 66, 67.

### First-appearance ledger

The Part VII ledger run is appended at the end of this file. The terms that matter: **ADR / architecture decision record** is used in Ch 47 and Ch 56 before Ch 60 defines it; **C4** appears nowhere before Ch 60 (good); **PACELC** is defined in Ch 61 and used only after; **semantic layer** is used from Ch 16 and Ch 32 onward but the glossary anchor and every Part VII pointer name Ch 23, where it appears once in a parenthesis (S3-70).

### Promise ledger (Part VII)

| Promise | Made in | Kept? |
|---|---|---|
| Ch 60 open risk "Chapter 64 has not yet defined the access-control model" | 60 §60.5 | Yes, Ch 64 §64.3 and §64.9 close it explicitly |
| Ch 60 NFR "under ₹0.50 per 1,000 order lines" | 60 §60.5 | Yes, Ch 65 §65.3 checks it and rewrites it |
| Ch 60 "Chapter 63 … the eight-container platform, inventoried" | 60 Where-this-leads | Yes |
| Ch 62 trigger "a second domain team asks to own its data" | 62 §62.6 | Yes, Ch 62 story and Ch 66 §66.4 (Taloja analyst) |
| Ch 66 "Chapter 67, the final chapter" | 66 Where-this-leads | Kept, and that is the problem (check C) |
| Ch 67 "the Question Banks in the appendices (Chapters 70 through 79)" | 67 | Wrong: the banks are Chapters 70–80 of Part VIII, not appendices; the Architecture & Leadership bank it names is Ch 80, outside its own range (S2-28) |
| "System Design Question Bank (Chapter 77)" ×3 (60, 61, 62) | 60–62 | Near-miss title: Ch 77 is "Data Engineering & Data System Design Bank" |

### Findability audit

Section pointers inside 60–67 resolve except: Ch 62 "section 60.5.2" (Ch 60 has no numbered subsections); Ch 66 and Ch 67 "section 62.7's Conway's Law" (Conway's Law is §62.8; §62.7 is data products); Ch 67 project steps 4 and 5 "section 67.6's pattern" (the influence and saying-no patterns are §67.4; §67.6 is the 90-day plan); Ch 63 "Chapter 63.8's audit" (section, not chapter). Cross-part pointers: Ch 66 twice attributes the fairness audit to Chapter 62 (it is Ch 64); Ch 65 calls PO-intake "Chapter 54's" (Ch 58); Ch 65 cites "Chapter 61's failure analysis" for row fan-out (Ch 12/28); Ch 64 places the reverse-ETL sync in "Part V" in one place and "Part VI" in another (it is Ch 51, Part V). After renumbering, the only moving targets are the Part VIII pointers (77→79, 80→82), which appear in 60, 61, 62 and 67.

### Character arcs

- **Meera Iyer**: Ch 60 makes her Head of Data Platform in January 2026 after "four years building pieces"; Ch 8 says she joined as a sales coordinator and by Ch 7 "the job title hasn't changed yet". Four years does not fit a story whose dated events run mid-2025 to early 2027 (S2-25).
- **Anita Rao**: Sales Head in Ch 1, Ch 3 and the bible, where the managing director sits above her. In Part VII she creates the Head of Data Platform role (60), receives and declines a vendor's architecture pitch (62), approves the platform hire (66) and sits with "the owning family" as the platform's sponsor (67). The managing director never appears. Either Anita has been promoted off-page or the part has quietly made the Sales Head the CEO (S3-71).
- **Vikram Singh** (Sales Manager): the voice of judgment in 60, 66 and 67, and the resisting stakeholder turned advocate in 67. Consistent and well used.
- **The four-person data platform team**: consistent across 60–66 (14 mentions), and Ch 66 adds the Taloja analyst. Good.
- **A new VP**: appears in Ch 67 unnamed; fine.

### Story calendar (Part VII against Parts IV–VI)

| Ch | Date in text | Depends on | Conflict |
|---|---|---|---|
| 60 | January 2026; "a year later" | PO-intake "the busiest thing she'd ever built", defect model, assistant, warehouse | Ch 58's pilot goes live November 2026; Ch 56's camera runs from March 2026; Ch 57's incident is October 2026 |
| 61 | February 2026 (Zoho outage) | PO-intake in production, reverse-ETL live | Same |
| 62 | March 2026; +9 months → December 2026 | Ch 60's diagram | Same |
| 63 | April 2026, "two months into her role"; +9 months | Ch 58's pipeline in the inventory | Same |
| 64 | June 2026; "+3 months" | Lead scoring live in CRM | — |
| 65 | NFR "six months old" → ~July 2026; prices "August 2026" | Ch 60 | — |
| 66 | undated; "nine months later" | Ch 65 | — |
| 67 | "late 2026"; "eighteen months of honest, checkable work" from Ch 60 | Ch 60 (Jan 2026) | Jan→late 2026 is ten or eleven months, not eighteen |

Part VII's calendar runs January–late 2026 and treats every Part VI system as already in production in January. Part VI's own calendar puts those systems live between March and November 2026. The simplest fix is to shift Part VII by one year (January 2027 onward), which also repairs "a year later" and "eighteen months" without touching Part VI. Structural question Q22.

### Findings

**S1-20 — Ch 66 §66.3 prints an `IndexError` as its output.** The ROI block ends `IndexError: single positional indexer is out-of-bounds` and never prints the "Three real, quantified automations cover 45%" line the prose quotes. CAUSE: the filter `roi.item.str.contains("three known automations, total")` matches nothing, because the CSV row is labelled "Quantified savings, three known automations (still incomplete)". Same class as S1-6/S1-14/S1-15/S1-16. Smallest fix: change the filter string to "three known automations" and re-run; the 45% then prints and matches the prose.

**S1-21 — Ch 64 §64.7 prints "Is region a feature the model uses directly? True", and the prose says the model never uses region.** The variable is `region_never_used = "region" not in [...]`, so `True` means *not* used, but the printed question asks the opposite. Reader 1 takes the output at face value and the chapter's central finding ("proxy discrimination, not direct use") reads as contradicted by its own code. CAUSE: label written after the variable was renamed. Smallest fix: print "Is region among the model's features? False" (or rename the variable `region_used` and negate).

**S1-22 — Ch 65 §65.3 prints "Cost per defect-model prediction 1.6513" and the prose table two paragraphs later says ₹0.17.** One of them is wrong by a factor of ten. CAUSE: the CSV was regenerated with a different prediction volume after the table was written. Smallest fix: recompute one from the other; the table's "₹0.17" and the chapter's own "3,303/month always-on" line imply about 19,000 predictions a month, so check `build_ch65_files.py`.

**S1-23 — Ch 65's sensor archive sizes contradict Ch 49 and inherit S1-17.** Ch 65 prices "1,200 GB hot (90 days)" and "9,800 GB cold" for the sensor archive. Ch 49 §49.8 says 277 GB for a year, which S1-17 already showed is 365× too large; the true annual volume for 19.9 million readings is under 1 GB. Ch 65's 11 TB is 40× Ch 49's already-inflated figure and 14,000× the real one. The two S3 tier costs (₹2,401 and ₹1,705) and exercise 7's "₹2.00/GB versus ₹0.17/GB" all rest on it. CAUSE: the cost model was sized from a guess, not from Ch 48/49's row counts. Smallest fix: once S1-17 is fixed in Ch 49, regenerate `monthly_cost_model.csv` from the corrected archive size; the storage lines will drop to a few rupees and the "storage tiering is the highest-leverage lever" finding (§65.5) will need a different example.

**S1-24 — Ch 67 §67.5 tells the reader the book was written by a model.** "This book's own Chapter 64 had to verify two facts by live search because the world had changed since its training data." No other sentence in the manuscript refers to training data or live search in the author's voice (Ch 54's use is about LLMs in general). CAUSE: an author's process note left in the prose. Smallest fix: "because regulation had moved since the chapter was first drafted."

**S2-25 — Meera's timeline breaks in Ch 60.** "By January 2026, Meera Iyer had spent four years building pieces of what was now … a genuine platform." Ch 1 has her join as a sales coordinator; Ch 6 has her write a nine-month plan; Ch 8 says by Ch 7 her title had not changed; every dated Riverstone event before Part VII falls in 2025–2026. CAUSE: Part VII written with its own internal clock. Smallest fix: "two years", and shift Part VII's dates by a year (see Q22).

**S2-26 — Part VII's calendar precedes the Part VI systems it depends on** (table above). Ch 60's January 2026 platform includes the PO-intake pipeline, defect model and assistant; those go live in Part VI between March and November 2026. Ch 61's February 2026 outage has PO-intake and reverse-ETL running. Ch 63's April 2026 inventory lists Ch 58's pipeline. CAUSE: same as S2-25. Smallest fix: move Part VII to 2027 (Ch 60 January 2027, Ch 61 February 2027, Ch 62 March 2027, Ch 63 April 2027, Ch 64 June 2027, Ch 67 late 2027) and change Ch 67's "eighteen months" to "a year".

**S2-27 — Ch 63 §63.3 cites `DATA_SPEC.md`'s note about Kolkata's legacy billing system.** `DATA_SPEC.md` is a companion/planning file; the manuscript never describes a Kolkata legacy billing system anywhere else, so the reader meets both the file and the fact for the first time in a parenthesis. CAUSE: author's notes used as if they were book content. Smallest fix: state the fact in one sentence ("Kolkata's billing system has no API and still takes a spreadsheet upload") and drop the file name, or introduce the system in Ch 3's systems table.

**S2-28 — Ch 67's closing pointer to the interview material is wrong in three ways.** "The Question Banks in the appendices (Chapters 70 through 79)": they are chapters, not appendices; the banks run 70–80 (72A and 76A/B included); and "a dedicated Architecture & Leadership bank" is Ch 80, outside the range given. After renumbering the range becomes 71–82. CAUSE: written before Part VIII's shape was fixed. Smallest fix: "Part VIII's question banks (Chapters 70 to 80)" with the numbers run through OLD_TO_NEW at the same time as the structural decision in check C.

**S2-29 — Ch 64 says the book has no lead-scoring model; Part IV built one.** The Tools note: "Riverstone's ERP and CRM data … contain no real lead-scoring model — Part VI's reverse-ETL sync mentions lead scoring only in passing." Chapters 35, 36, 37 and 39 build and evaluate a lead-scoring model on the 12,294-lead CRM extract (7–10 mentions each), and Ch 51 (Part V, not VI) syncs its scores to the CRM (17 mentions). Ch 64's audit dataset (1,830 leads, four regions, `company_size_band`) is a different universe from Part IV's. CAUSE: Ch 64 written without Part IV in view. Smallest fix: either audit Part IV's actual model (its features are known; add `region` to the CRM extract) or change the note to say the audit uses a simplified stand-in for the Part IV model, and fix "Part VI" to "Part V".

**S3-68 — Figure numbers and files are crossed or out of order in four chapters.** Ch 60: `fig60-5` is captioned Figure 60.4 and `fig60-4` is Figure 60.5. Ch 62: Figure 62.5 appears before Figure 62.4 (§62.5 was inserted after the figures were numbered). Ch 63: `fig63-2` is Figure 63.1 and `fig63-1` is Figure 63.2. Ch 66: figures run 66.1, 66.4, 66.2, 66.3. Same class as S3-61. Smallest fix: renumber captions in reading order and rename files to match.

**S3-69 — Ch 65 "the warehouse's RDS instance and the defect-model's serving instance … combined ₹22,674/month".** 16,068 + 3,303 = 19,371. The 22,674 figure includes the Dagster fleet as well. Exercise 13 repeats the number. CAUSE: three lines summed, two named. Smallest fix: name all three, or use 19,371.

**S3-70 — The semantic layer is attributed to Chapter 23 throughout Part VII** (62 ×4, 63 ×1, 64 ×1, the Ch 62 key-terms list). Ch 23 mentions "a semantic layer" once, in a list of places to put a definition. The thing Part VII means, the tested `net_revenue` metric and the dbt models, is built in Ch 32 §32.9 and consumed in Ch 16. CAUSE: stale plan ("Ch 23 = metrics layer"). Smallest fix: "Chapter 32's semantic layer (and Chapter 23's metric definitions)".

**S3-71 — Anita Rao's role inflates from Sales Head to de facto chief executive.** In Part VII she creates a platform-head role, adjudicates a company architecture pitch, approves headcount and hosts the owning family's review. Ch 3 and the bible put a managing director above her and never mention a family. CAUSE: Part VII needed an executive sponsor and reused the most familiar name. Smallest fix: introduce the managing director (unnamed in Ch 3) by name in Ch 60's story as the person who creates the role, and let Anita stay the Sales Head who sponsors the East-region audit in Ch 64.

**S3-72 — Ch 61 story misuses ADR-026.** The reverse-ETL sync "kept trying … logging each failure without escalating — exactly as ADR-026 intended". ADR-026 (Ch 60's table) is the PATCH-only, one-system-of-record-per-field rule for CRM writes; it says nothing about retry or escalation. CAUSE: nearest ADR number reached for. Smallest fix: cite the sync's own runbook, or add the retry policy to ADR-026's consequences in Ch 60.

**S3-73 — Ch 61 story gives the PO-intake pipeline a CRM credit-hold check it never had.** Ch 58's pipeline validates against product codes, dates and the ₹100,000 limit; "a customer on credit hold" is a row in Ch 58's exception taxonomy, not a CRM call. Ch 61 makes the CRM lookup the reason two orders were held. CAUSE: story needed a second container to depend on the CRM. Smallest fix: one sentence in Ch 58 §58.6 saying the policy check reads account status from the CRM, or change Ch 61's held orders to reverse-ETL-only consequences.

**S3-74 — Ch 63 §63.2 ROI table quotes "325 hrs/yr saved" and "~₹3.9 lakh" for the Daily Flash; Ch 66's ROI CSV values the same saving at ₹97,500.** 325 hours × ₹300 (Ch 58's loaded rate) is ₹97,500; ₹3.9 lakh implies ₹1,200 an hour. CAUSE: two chapters, two hourly rates. Smallest fix: use one loaded rate across 58, 63 and 66 and state it once.

**S3-75 — Ch 63 and Ch 66 say Chapter 19's macro "ran silently wrong for years" / "unowned for nine years".** Ch 19's story: `MASTER_FINAL_v7_USE_THIS.xlsm` written in 2017 by an analyst who had left; that is nine years to 2026, but Ch 19 does not say it ran *wrong* for those years, only unowned. Reader 1 will look for the "silently wrong" incident and not find it. Smallest fix: "unowned for nine years" in both places.

**S3-76 — Tool-version lines contradict themselves in 64, 65 and 66.** "Python 3.13 or 3.14 … (run here on Python 3.12, pandas 3.0.2)". Parts V–VI say Python 3.12 throughout. Smallest fix: "Python 3.12 or later".

**S3-77 — Ch 62 story's first "Nine months later" and Ch 63's "Nine months later" and Ch 66's "Nine months later" all land in the same season and none is dated.** Three nine-month jumps from March, April and an undated month give three different dates for a single Taloja hire that Ch 62 and Ch 66 both describe. Smallest fix: date the hire once (see Q22).

**S3-78 — Ch 65 §65.5 "Chapter 54's PO-intake pipeline" and "Chapter 61's failure analysis" for fan-out; Ch 66 "reconciled pipelines (Ch 14)" and "the fairness-audit finding (Chapter 62)" ×2; Ch 67 "Chapter 18 could hand you pandas" (correct, Ch 18 is pandas) but "the queries in Part I" (Part I has no SQL; queries begin in Ch 12).** Five small misattributions, one sweep.

### Check C — the book ends twice (extends CPI-20)

CPI-20 is already filed; this is the itemised list of every sentence in Part VII that makes Ch 67 the end of the book, so the fix is mechanical once the structural decision is taken:

- Ch 66 Where-this-leads: "Chapter 67, The Architect as Leader: the final chapter".
- Ch 67 header: "this is the last chapter of the book".
- Ch 67 §Why: "at the start of the last chapter rather than discovering it by surprise at the end".
- Ch 67 §67.3: "Here, at the end of the book".
- Ch 67 §67.7 title "The arc of this book"; "Sixty-six chapters later"; "from the first query to this last sentence".
- Ch 67 Where-this-leads: "There is no next chapter."
- Ch 67 closing italics: "This is the final chapter of Analyst to Architect … sixty-seven chapters of practice".
- Ch 83 line 17: "This is the last chapter".

Recommendation (stated, stopped): keep Ch 67 as the end of the *craft* and make Part VIII an explicitly separate "playbook" with its own opening line in Ch 68 ("The book's teaching ended with Chapter 67; this part is for the weeks before an interview"). Then Ch 67 needs six wording changes ("last chapter of the craft", "eighty-three chapters" or "the teaching chapters"), Ch 66 one, and Ch 83 keeps "last chapter". Structural question Q23.

### Beginner survival (Reader 1)

Reader 1 survives Part VII easily; it is the least technical part since Part I. What will confuse them is the calendar (S2-26) and the three printed contradictions (S1-20, S1-21, S1-22), because this reader has been trained by 60 chapters to trust printed output over prose.

### Reader 2

Reader 2 will find Part VII the most useful part of the book for the job they are in. They will notice the Anita/managing-director inflation, the "four years", and the Ch 64 "no lead-scoring model" note at once.

### Structural questions (continued)

22. **Which year is Part VII set in?** Every dated event in 60–67 is 2026 and every system it governs went live in 2026 per Part VI. Shift Part VII to 2027 or Part VI to 2025; the former is one find-and-replace per chapter. Stated; stopped.
23. **Is Ch 67 the end of the book?** See check C. Stated; stopped.
24. **Who runs Riverstone?** Ch 3 has a managing director; Part VII has Anita and an owning family. Decide once in the bible. Stated; stopped.
25. **Does the fairness audit in Ch 64 use Part IV's lead-scoring model or a stand-in?** Using the real one is a bigger change to the companion but removes S2-29 entirely. Stated; stopped.

### Printed-error scan (Part VII)

The whole-book grep (structural Q16) finds one hit in 60–67: ch66:118 (S1-20). The Part VII list for Q16 is therefore: ch66:118.

### Ledger appendix (Part VII, terms defined in 60–67 but used earlier; filtered to >5 characters)

```
43 terms used before definition, defined in 60-67
  'availability': used 2, defined 60
  'context': used 7, defined 60
  'consequences': used 2, defined 60
  'functional': used 25, defined 60
  'non-functional': used 25, defined 60
  'non-functional requirements': used 25, defined 60
  'consistency': used 1, defined 61
  'latency': used 30, defined 61
  "semantic layer's": used 60, defined 61
  'postgres': used 6, defined 61
  'replication': used 27, defined 61
  'message queues': used 51, defined 61
  'reverse-etl sync': used 51, defined 61
  'po-intake pipeline': used 60, defined 61
  'data mesh': used 60, defined 62
  'organizational': used 22, defined 62
  'a data contract': used 47, defined 62
  'a semantic layer': used 23, defined 62
  'a named owner': used 25, defined 62
  'effort': used 6, defined 63
  'scheduled': used 3, defined 63
  'a runbook': used 46, defined 63
  'encryption at rest': used 2, defined 64
  'encryption in transit': used 2, defined 64
  'secrets management': used 51, defined 64
  'lawful basis': used 45, defined 64
  'data governance': used 7, defined 64
  'compute': used 8, defined 65
  'tagging': used 30, defined 65
  'scheduled versus event-driven': used 63, defined 65
  'marginal': used 44, defined 65
  'a monthly review': used 13, defined 65
  'strategy': used 8, defined 66
  'maturity': used 36, defined 66
  'the business case': used 63, defined 66
  'team structure': used 7, defined 66
  'build versus buy': used 45, defined 66
  'culture': used 14, defined 66
  'the defect-detection model': used 64, defined 66
  'the support assistant': used 55, defined 66

```
