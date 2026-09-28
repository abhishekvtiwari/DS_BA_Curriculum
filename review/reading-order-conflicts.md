# Reading order: where the two sources disagree

Written for the setup PR, 28 September 2026.

**Abhishek's answers (28 Sep).**
1. Follow P, `planning/chapter-map.md`.
2. **Keep D1 and the move of Python out of Ch 14/15** ("d1 keep them"). So the approved order is P with one change: Ch 14–16 come before Python (17–18).
3. **Renumber Parts II and III** to the reading order ("Renumbering yes"), in the final pass.

| | Approved order |
|---|---|
| Part II | 10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20, 21–27 |
| Part III | 28, 34, 29, 32, 33, 30, 31 |

| Old | 10 | 11 | 19 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 20–27 | 28 | 34 | 29 | 32 | 33 | 30 | 31 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **New** | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20–27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 |

What that did to the 46 findings below (register notes carry the reason for each):
- **Approved (19):** valid under the approved order because 14–16 come first: 14.1, 14.2, 14.22, 14.23, 15.1, 15.3, 15.10, 16.2, 16.3, 16.4, 18.3, 18.10, 18.11, 18.24, 18.27, 18.43, 18.45, 18.49, 26.33.
- **Held, recommend Reject (20):** they assume Ch 19 comes after Python (19.1, 19.10, 19.15, 19.16, 19.21, 19.35) or Ch 34 after 29–33 (29.1, 29.2, 32.1, 32.17, 32.24, 33.21, 34.2, 34.12, 34.15, 34.19, 34.20), or they would undo the renumbering (17.31, 18.44, 20.22).
- **Held, newly (6):** approved earlier but written for P without D1: RJ-S1-1, RJ-S1-5, RJ-S2-10, RJ-S3-9, RJ-S3-10, 14.32.
- **Unchanged:** RJ-S1-11 and 0.1 stay approved.

## 1. The orders themselves

| Stretch | P (chapter-map, 17 Sep) | S (sequence-map, 25 Sep, and CLAUDE.md §3) |
|---|---|---|
| Part II spreadsheets and automation | 10, 11, **19** (VBA before SQL) | 10, 11; Ch 19 comes after Python (19–25 in number order) |
| Part II SQL | 12, 13 | 12, 13 |
| Python vs cleaning, visualization, BI | **17, 18 before 14, 15, 16** ("pandas examples in them are legitimate") | **14, 15, 16 before 17, 18**. Power BI before Python (D1); pandas in §14.13 and §15.14 moves to Ch 18 |
| Rest of Part II | 20, then 21–27 | 19–25, then 34 essentials (as §26.0), 26, 27 |
| Part III | 28, **34**, 29, **32, 33, 30, 31** | 28, 29, 30, 31, 32, 33, 34 (Linux and networking only; terminal essentials moved to Ch 26 §26.0, D2) |
| Parts IV–VIII | Number order | Number order |

P also says chapter files keep their numbers until "the coordinator renumbers the whole book in one
pass at assembly". S says "one order; chapter number = reading order" (M.1). The two differ on
whether there will be a Part II/III renumbering at all.

## 2. Findings whose verdict or fix depends on the order

Scope: every row of `tracker/register.csv` plus the 130 Reader's Journey rows. Only chapter pairs
that change position between P and S can be affected: 19 vs 12–18, {17, 18} vs {14, 15, 16}, 34 vs
29–33, and {32, 33} vs {30, 31}. No finding about 30/31 vs 32/33 turned out to depend on the order.

**Summary**
- 46 findings are order-dependent: 36 in `tracker/register.csv` and 10 in the RJ candidates. Sources scanned: 3,758 register rows and 130 RJ rows. Only the pairs that change position were counted: 19 vs 12–18, {17,18} vs {14,15,16}, 34 vs 29–33, and {32,33} vs {30,31}.
- **25 are valid only under S.** In 21 the whole verdict depends on S: pandas/Python in 14–16, Ch 16's "Python came first", Ch 19 as a second language after Python, and Ch 34 as a forward prerequisite of 29/32/33. In 4 only part of the verdict depends on S (14.1, 14.22, 15.10, 32.24).
- **11 more have a verdict that holds under both orders, but a fix that assumes S.** Their fixes write back-references to Ch 14/15/16 or 18 into Ch 18/19, write "like Python" into Ch 19, or write "Chapters 29 and 32 had you…" into Ch 34.
- **7 are valid only under P**, and 5 of those cite chapter-map.md or "the map" as the authority: RJ-S1-1, RJ-S1-5, RJ-S2-10, RJ-S3-9, RJ-S3-10. The other 2 (14.32 and RJ-S3-13) have no effect under S, because the pandas column is removed. **3 are split between the orders:** RJ-S1-11 (Ch 34 body under P, Ch 29 header under S), RJ-S2-13 (only its aside depends on P) and 0.1 (the content of Figure 6.2 depends on the map).
- Explicit S citations: M.1/D1 (16.2), M.2 (14.2, 15.1, 16.4, 18.10, 18.11, 26.33), M.4/D2 (29.1, 32.1), and "approved/reading order" (19.1, 19.35, 34.19). No finding in 30↔31 vs 32↔33 turned out to depend on the order.

| ID | Ch | Sev | What it assumes | Valid under S? | Valid under P? |
|---|---|---|---|---|---|
| **Part 0–I / Ch 6** |||||
| RJ-S1-1 | 6,14,19,20 | High | Redraw Fig 6.2 and §6.8 to the 17-Sep order (10,11,19,12,13,17,18,14…); cites chapter-map.md | No | Yes |
| RJ-S3-9 | 6 | Med | Fig 6.1 "order first used" is wrong because Python now comes before 14–16 | No | Yes |
| 0.1 | 6 | High | Plan hours are wrong (valid either way); the Fig 6.2 redraw "needs map" | Yes | Yes (figure content depends on order) |
| **Ch 11–13** |||||
| RJ-S2-10 | 11,12 | High | "Six-chapter wall" created by the order 11→19→12→13→17→18; it says S's placement of 15 would break the wall | No | Yes |
| RJ-S3-10 | 11,12,13,17,19 | Med | Seams written to the old order: Ch 12 should say "after Ch 19", Ch 13 should list 17 as next, Ch 17 should credit VBA loops | No | Yes |
| **Ch 14** |||||
| 14.1 | 14 | High | psql/cd before the terminal is taught (§26.0); the DBeaver/setup gap applies under both orders | Yes | Partly (under P, Ch 17's terminal comes before 14) |
| 14.2 | 14 | High | pandas is used before Ch 17–18 (M.2); move §14.13 to Ch 18 | Yes | No |
| 14.22 | 14 | Med | The Python check script "the reader can't run yet"; the build-script leftover is a problem either way | Yes | Partly |
| 14.23 | 14 | Med | The stretch goal needs Python (Ch 17–18), which hasn't been taught yet | Yes | No |
| 14.32 | 14 | Low | "pandas (§14.11)" should be §14.13, a moot point once the column goes (14.2) | Moot | Yes |
| RJ-S3-13 | 14 | Med | Same as 14.32 | Moot | Yes |
| **Ch 15** |||||
| 15.1 | 15 | High | pandas/matplotlib in §15.14 come before Python (M.2); move them to §18.11 | Yes | No |
| 15.3 | 15 | Med | A "Python" route is offered before the reader knows Python, and Ex 22 needs matplotlib | Yes | No |
| 15.10 | 15 | Low | A Python build script is offered "in a chapter before Python" | Yes | Partly |
| **Ch 16** |||||
| 16.2 | 16 | High | "Python block comes before this chapter" contradicts D1/M.1 | Yes | No (the sentence is correct under P) |
| 16.3 | 16 | Med | "Notebook" hasn't been introduced; fix says "after Chapter 17" | Yes | No |
| 16.4 | 16 | Med | Python/notebook option in Ch 16; §14.13 moves to Ch 18 (M.2) | Yes | No |
| **Ch 17–19 (cross)** |||||
| RJ-S1-5 | 14–19 | High | Ch 17/18/19 treat 14/15/16 and the full dataset as already done; cites the chapter-map decision | No | Yes |
| **Ch 18** |||||
| 18.10 | 18 | High | §14.13's pandas content must land in §18.10 (move under M.2) | Yes | No |
| 18.11 | 18 | Med | Ch 15's matplotlib preview moves into §18.11 | Yes | No |
| 18.3 | 18 | Med | Fix: "load the 39-city mapping Chapter 16 used" (back-reference to 16) | Verdict yes; fix yes | Verdict yes; fix no |
| 18.24 | 18 | Med | "The ambiguity Ch 15 and 16 warn about" (back-reference) | Yes | Fix wording no |
| 18.27 | 18 | High | Fix: "link Ch 14 §14.7" for regex | Yes | Fix no |
| 18.43 | 18 | Low | Fix: "Chapter 15 rounded to the rupee…" | Yes | Fix no |
| 18.45 | 18 | Low | Fix: "the validation rule from Chapter 14 §14.9"; the list-price check "now here" (M.2) | Yes | Fix no |
| 18.49 | 18 | Low | Fix: re-read "Ch 14's messy file" as a known file | Yes | Fix no |
| **Ch 19** |||||
| 19.1 | 19 | High | Reader arrives from 17–18 "in the approved order"; teach VBA as a second language | Yes | No (P puts 19 before Python) |
| 19.10 | 19 | High | JS is never taught (holds under both orders); fix is a "JS/TS for a Python reader" table | Yes | Fix no |
| 19.21 | 19 | Med | Fix: "Array() starts at 0, like Python" | Yes | Fix no |
| 19.35 | 19 | Med | Ch 18 is listed as forward "but comes before this chapter in the reading order" | Yes | No |
| 19.15 | 19 | Med | Fix: data "built from … Chapter 14 §14.10" (back-reference) | Yes | Fix no (RJ-S1-5 data dependency) |
| 19.16 | 19 | Med | "Ch 18 prints them with round(0)" treated as prior | Yes | Fix no |
| **Ch 26** |||||
| 26.33 | 26 | Low | "After M.2, Ch 14 produces no scripts; cleaning code is in Ch 18" | Yes | No |
| **Ch 28** |||||
| RJ-S2-13 | 27,28,34 | High | Ch 28 is a wall (holds under both orders); aside: "Ch 34, which follows in the map, would be a gentler start" | Verdict yes; aside no | Yes |
| **Ch 29** |||||
| 29.1 | 29 | High | "Chapter 34" is a forward prerequisite (M.4/D2) | Yes | No (34 comes before 29) |
| 29.2 | 29 | Med | find and the pipe "stay in Ch 34", so they aren't taught yet | Yes | No |
| RJ-S1-11 | 2,6,29,34 | High | Map 28→34→29: Ch 34's body cites Ch 29 as done, so the two headers are circular; fix picks P's direction | Header half only | Yes (body half) |
| **Ch 32** |||||
| 32.1 | 32 | High | "Chapter 34" is a forward prerequisite (M.4/D2) | Yes | No |
| 32.17 | 32 | Low | "Chapter 34's $?" should be §26.0; the other references fixed here are correct either way | Yes | No (that reference) |
| 32.24 | 32 | High | (2) "./ is not taught before Ch 34" depends on S; (1) PGPASSWORD and (3) dbt deps hold either way | Yes | Partly |
| **Ch 33** |||||
| 33.21 | 33 | Med | Pipes and head are taught in Ch 34 "after this chapter" | Yes | No |
| **Ch 34** |||||
| 34.2 | 34 | High | Prerequisites must add Ch 29 (and 20), because the chapter "depends heavily" on Ch 29 | Yes | No |
| 34.12 | 34 | Low | Fix: "Chapters 29 and 32 had you type a password into export" | Yes | Fix no |
| 34.15 | 34 | Low | Ch 29's mock CRM, which the reader already knows, needs a standalone start command | Yes | No |
| 34.19 | 34 | Low | "All four chapters (20, 26, 29, 32) come before Ch 34 in the reading order" | Yes | No |
| 34.20 | 34 | Low | Four "leads" (29, 26, 32, 20) are earlier chapters | Yes | No |

Also: **RJ-S3-36** (Part II and Part III cite "Python as Software" by two different numbers) was
recorded as a duplicate of 17.31, 18.44 and 20.22, which change Part II's "Chapter 30" to 29. That
holds under S. Under P, "Python as Software" becomes Chapter 30 after renumbering, and the fix would
run the other way.

## 3. The one cause behind most of the P-only findings

RJ-S1-5 records it. Chapters 17–19 were approved on 18 September without being rewritten for the
reading order decided on 17 September. Applying the S-based fixes (Python out of 14/15, Ch 19 after
Python, terminal in §26.0) would make most P-only findings obsolete. Applying P would instead make
the 25 S-only findings obsolete and need the RJ fixes.
