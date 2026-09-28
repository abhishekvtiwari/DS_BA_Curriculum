# Reader's Journey findings as candidate register rows

`register-candidates.csv` holds every numbered finding from `journey-findings.md` in the same
schema as `tracker/register.csv`, ready to append if you decide to merge the strand.
**Nothing has been added to the register.** Every row is `Open` with an empty `decision_source`,
and `kind` is `reader-journey` so these can never be confused with the 2,534 content or 1,224
visual rows.

Extracted **130 findings**: 53 High, 77 Medium, 0 Low. S1 and S2 map to High, S3 to Medium, S4 to Low.

The 25 structural questions are deliberately not here. They are questions for you, not fixes,
and they belong next to sections C and D of `DECISIONS.md`.

## Candidate theme, by keyword

Approximate. A finding can match several themes, so these do not sum to the total.

| Theme | Candidate rows |
|---|---:|
| T10 | 49 |
| V10 | 29 |
| (none) | 21 |
| T8 | 20 |
| V4 | 18 |
| T9 | 12 |
| T11 | 11 |
| T1 | 8 |
| T7 | 8 |
| T2 | 6 |
| T12 | 6 |
| T13 | 4 |
| T6 | 4 |
| T14 | 3 |
| T5 | 2 |
| T3 | 1 |

21 matched no theme and need reading.

## Per part

| Part | Findings |
|---|---:|
| 0-I | 19 |
| II | 24 |
| III | 18 |
| IV | 17 |
| V | 13 |
| VI | 18 |
| VII | 21 |

## Every High finding

- **RJ-S1-1** (Ch 6, 14, 19, 20): Ch 6, Figure 6.2 and §6.8 bullets 2–3; Figure 6.1: Follows the six-month plan; reaches Chapter 14 in month 4 and meets pandas; Python is scheduled for month 5. Meets Chapter 19 last, though it was rewritten to come before Python..
- **RJ-S1-2** (Ch 2, 3, 7, 20): Ch 2, "In the real world" last paragraph and Where-this-leads bullet 5; Ch 3 §3.7 last paragraph and Where-this-leads bullet 4: Is told Chapter 20 "takes this exact report and automates it end to end" (the Friday file) and, in Cha
- **RJ-S1-3** (Ch 2, 4, 6): Ch 2 at-a-glance and Tools; Ch 4 at-a-glance; Ch 6 §6.4: Cannot do Chapter 2's project, open Chapter 4's workbook, or run Chapter 6's checks, because the only pointer is "Appendix E", which is unwritten.. Cannot do Chapter 2's pro
- **RJ-S1-4** (Ch 1, 3, 6, 7): Ch 6 "In the real world"; Ch 7 "In the real world": In Chapter 6 (set after February 2026: it cites the Chapter 3 reconciliation) Meera "wants to become an analyst properly" and installs PostgreSQL from scratch. One chapter later,
- **RJ-S1-5** (Ch 14, 15, 16, 17, 18, 19): Ch 19 at-a-glance and Practice data; Ch 17 "Why this matters" (line 21), §17.5, §17.7, §17.8, §17.11, §17.12 ×2, §17.13 ×2, mistakes table, story, ex. 27 (twelve references to Ch 14, two to Ch 16); Ch 18 at-a-glance, §18.2, §18.3,
- **RJ-S1-6** (Ch 18): Ch 18 §18.8 (two code blocks), §18.12 read-back block: Types `pd.pivot_table(sales2025, index="segment", columns=sales2025["order_date"].dt.quarter, …)` and gets `TypeError: unhashable type: 'Series'`, printed in the book as the o
- **RJ-S1-7** (Ch 6): Ch 6 Figure 6.2 and §6.8; every Part II at-a-glance "Time needed": Reads "about 8 hours a week for 26 weeks" for Parts 0–II. The chapters claim 27–36 hours (Parts 0–I) plus 290–357 (Part II): 317–393 hours, or 40–49 weeks at 8 hou
- **RJ-S1-8** (Ch 16, 20, 21, 22, 23, 24): Ch 16 Where-this-leads bullet 2; Ch 20 bullet 2; Ch 21 bullet 4; Ch 22 bullets 1, 2, 3, 4; Ch 23 last bullet; Ch 24 last bullet: Is sent to "Chapter 23, Data Storytelling" (it is Business Acumen; storytelling is Chapter 24), "Chap
- **RJ-S1-9** (Ch 13, 23): Ch 23 §23.5, table rows "Win rate" and "Conversion by stage", the paragraph "Two-thirds of Riverstone's 43 leads…", answer 9, timed-challenge bonus: Reads that Riverstone had 43 leads, a 14% win rate, and "21 of 43 never get conta
- **RJ-S1-10** (Ch 19, 22, 30, 31, 37, 40): Chapters 30 and 31 cite a regression chapter that does not exist before them.. Where: Ch 30 §30.11 opening line "Chapter 19 used regression to predict. Here it's used to explain"; Ch 31 at-a-glance "Chapter 19's regression mechani
- **RJ-S1-11** (Ch 2, 6, 29, 34): Chapter 34 is written after Chapter 29 and placed before it.. Where: the map reads 28 → 34 → 29. Ch 34's own header requires only Chapter 6 and Chapter 2, which is right for its position. Its body then mentions Chapter 29 fourteen
- **RJ-S1-12** (Ch 17, 18, 19, 30, 31, 33): Seven stale titles and five wrong pandas pointers in Part III's navigation.. Extends S1-8. Stale titles, all in "Where this leads" or headers, with the actual chapter under that number: - Ch 30: "Chapter 42, Digital & Web Analytic
- **RJ-S1-13** (Ch 23, 30, 36, 38, 39, 40): Part IV's forward pointers describe a Part V that no longer exists.. Extends S1-8 and S1-12. Where, with the actual chapter under each number: - "Chapter 52, Deploying and Monitoring Models" or "Chapter 52 covers deploying it": Ch
- **RJ-S1-14** (Ch 42): Chapter 42, answer 9, prints a traceback as its output.. Extends S1-6. Where: Ch 42 answers, exercise 9 ("find the pair of different products with the highest description similarity"). The code block's output is `ValueError: under
- **RJ-S1-15** (Ch 51): Chapter 51 prints `NameError` as the output of six code blocks and narrates results that never appeared.. Extends S1-6 and S1-14. Where: §51.2 (two blocks: `NameError: name 'sl' is not defined`), §51.3 "A first sync", §51.4 "A wri
- **RJ-S1-16** (Ch 46, 50): Chapter 46's printed outputs contradict its prose from §46.6 onward.. Extends S1-6. Where: §46.5 ends its last code block with `api.shutdown()` (line 512). Every later run's `raw_crm_leads` step calls a server that is no longer th
- **RJ-S1-17** (Ch 49, 52): Chapter 49's storage estimate multiplies by 365 twice, and Chapter 52 inherits the result.. Where: Ch 49 §49.8: "one year across 40 machines: about 126 million readings a day-equivalent … 126,000,000 × 365 ÷ 216,000 × 1.3 MB ≈ 277
- **RJ-S1-18** (Ch 58): Ch 58's recap and story contradict its own measured segment result.. §58.8 measures accuracy by email style and its headline is "not where anyone would have guessed": bulleted, forwarded and terse emails are 37 of 37 correct, whil
- **RJ-S1-19** (Ch 6, 59, 67, 79, 80, 83): Ch 59 points to "Chapter 79, The First 90 Days", which does not exist.. Ch 79 is the GenAI, LLM & MLOps Question Bank. No chapter in the manuscript is titled The First 90 Days; the phrase occurs only as a topic inside Ch 6, Ch 67 
- **RJ-S1-20** (Ch 66): Ch 66 §66.3 prints an `IndexError` as its output.. The ROI block ends `IndexError: single positional indexer is out-of-bounds` and never prints the "Three real, quantified automations cover 45%" line the prose quotes. CAUSE: the f
- **RJ-S1-21** (Ch 64): Ch 64 §64.7 prints "Is region a feature the model uses directly? True", and the prose says the model never uses region.. The variable is `region_never_used = "region" not in [...]`, so `True` means *not* used, but the printed ques
- **RJ-S1-22** (Ch 65): Ch 65 §65.3 prints "Cost per defect-model prediction 1.6513" and the prose table two paragraphs later says ₹0.17.. One of them is wrong by a factor of ten. CAUSE: the CSV was regenerated with a different prediction volume after th
- **RJ-S1-23** (Ch 48, 49, 65): Ch 65's sensor archive sizes contradict Ch 49 and inherit S1-17.. Ch 65 prices "1,200 GB hot (90 days)" and "9,800 GB cold" for the sensor archive. Ch 49 §49.8 says 277 GB for a year, which S1-17 already showed is 365× too large; 
- **RJ-S1-24** (Ch 54, 64, 67): Ch 67 §67.5 tells the reader the book was written by a model.. "This book's own Chapter 64 had to verify two facts by live search because the world had changed since its training data." No other sentence in the manuscript refers t
- **RJ-S2-1** (Ch 6): Ch 6 §6.3, steps 2, 3 and 6: Installs PostgreSQL, MySQL, DBeaver, Python, a virtual environment and four packages, VS Code, Git and Power BI in month one. Uses a spreadsheet for the next two chapters. First runs Python in month fi
- **RJ-S2-2** (Ch 6, 12): Ch 6 §6.3 step 2: Is sent to "Chapter 12, section 12.3" for the database install. Opens the longest chapter in the book (32,273 words) in month one to find a 1,265-word section.. Is sent to "Chapter 12, section 12.3" for the datab
- **RJ-S2-3** (Ch 1, 6): Ch 1–9 projects; Ch 6 §6.8: Is scheduled to finish Chapters 1–9 in month one (Figure 6.2, ~32 hours) and is assigned nine projects in those chapters: a seven-day spending log, five file formats, a process map, five checked statist
- **RJ-S2-4** (Ch 1, 2, 3, 6, 12): Ch 2 §2.1: Meets bits, bytes, ASCII, Unicode, UTF-8, garbled encodings, floating point, pixels and sound storage in the first section of the second chapter, none of it usable until Chapter 6's rounding puzzle and Chapter 12's `NUM
- **RJ-S2-5** (Ch 8): Ch 8 §8.7: Reader 2 reaches Chapter 8, roughly 60,000 words in, and finds the row "Already an analyst: skim Parts 0–II; start fully at Part III". There was no way to know this on page one.. Reader 2 reaches Chapter 8, roughly 60,0
- **RJ-S2-6** (Ch 6, 8, 9, 10): Ch 8 §8.7 pathways table and automation-thread table; Ch 6 Figure 6.2; Ch 9 §9.5 portfolio table: Ranges such as "Ch 10–16, 19–27", "Chapters 14–16", "12–20", "46–47" are written on old numbers. After renumbering, old 10–16 become
- **RJ-S2-7** (Ch 14, 16, 17, 18, 20, 25): Ch 17 §17.13 table, project stretch, Where-this-leads; Ch 18 §18.15, Where-this-leads; Ch 20 Where-this-leads; Ch 16 §16.13 and Where-this-leads; Ch 26 Where-this-leads; Ch 27 Where-this-leads; Ch 25 Where-this-leads; Ch 14, 15, 2
- **RJ-S2-8** (Ch 12, 13, 14, 15, 17, 18): Ch 27 §27.2 (two), §27.3 (two), §27.4 (two), §27.5 (two), §27.6, ex. 11: Follows the capstone's pointers back into Part II and lands in the wrong place ten times out of nineteen: "Chapter 13 section 13.4 explains why BETWEEN on a 
- **RJ-S2-9** (Ch 10, 11, 13, 14, 15, 22): "In the real world" of Ch 10, 11, 13, 14, 15, 24; also 22: Meets Meera in "the second week of January 2026" (Ch 10, the two Januaries), "the first week of January 2026" (Ch 11, the month-end pack; Ch 15, the October collapse), "6 
- **RJ-S2-10** (Ch 11, 12): Reading order 11 → 19 → 12 → 13 → 17 → 18; Ch 12 §12.13: Enters a six-chapter stretch claiming 25–30, 20–25, 19–23, 15–20, 25–30 and 30–35 hours (134–163 hours) with no light chapter, where the old order gave 14 (20–25) and then 1
- **RJ-S2-11** (Ch 18, 29): Chapter 29's "before" script is still not Chapter 18's script, and the story now offers the fix.. Extends CPI-9; not a re-report. Where: Ch 29 header "Chapter 18 (pandas and the monthly report)"; §29.1 presents `start/monthly_repo
- **RJ-S2-12** (Ch 28, 31, 32): Chapter 32's snapshot demo reverses a Chapter 28 fact and stamps the author's run date on the story.. Where: Ch 32, "Watch it work. Metro Mart moves from Mumbai to Thane", followed by `update raw_crm.customers set city = 'Thane' w
- **RJ-S2-13** (Ch 27, 28, 34): Chapter 28 is a wall by itself.. Extends S2-10. Where: Chapter 28 profiles at 23,793 words, 82 key terms, 129 code blocks, 22 exercises and 18–24 hours. Part II's six-chapter wall (S2-10) was about six chapters in a row with no br
- **RJ-S2-14** (Ch 13, 23, 35, 36): Chapters 35 and 36 disagree about how many leads Riverstone receives, and Chapter 35's story reasons from the wrong number.. Extends S3-21. Where: Ch 35 §35.7 "In 2025 Riverstone received 30 real sales enquiries"; Ch 35's story (f
- **RJ-S2-15** (Ch 14, 20, 28, 33, 35, 36): Part IV's Riverstone datasets do not reconcile with the database the reader built in Part II, and nothing says they are not meant to.. Extends S3-34, structural question 6, and CPI-10. Where: Part IV generates five new Riverstone 
- **RJ-S2-16** (Ch 28, 29, 30, 31, 35, 36): The story calendar: Part IV's month-per-chapter scheme collides with Part III's, and Chapter 44's memo predates the model it uses.. Extends S2-9 and S2-13. Where: Part IV's stories are dated February 2026 (Ch 35), March (36), Apri
- **RJ-S2-17** (Ch 44): The capstone's reusable function ignores one of its three settings, and the "break-even rule" its exercises cite is never stated.. Where: Ch 44 §44.6 `def build_call_list(accounts_df, call_cost=1200, margin=0.15, capacity=40)`: `c
- **RJ-S2-18** (Ch 45, 46, 47, 48, 49, 50): Part V's stories are undated, its Riverstone runs at a third scale, and it adds four unnamed engineers and a second Imran.. Extends S2-15 and S2-16. Where: Ch 45's story: "Riverstone's first proper data pipeline went live in Febru
- **RJ-S2-19** (Ch 50): Chapter 50's late-data demonstration says the six late readings were counted and then says they were the row that was dropped.. Where: §50.5 "Late data that still counts": batch 2 carries 6 late M-07 readings from 00:02; "they wer
- **RJ-S2-20** (Ch 51): Chapter 51 states a scoring rule whose point values are never given, then sets an exercise on them.. Where: §51.2 gives the rule in words ("points for the lead's current stage + points for how it arrived + a recency bonus … capped
- **RJ-S2-21** (Ch 57, 58): Ch 57 story says the extraction pipeline was loading orders straight into the ERP in October; Ch 58 says intake went live in assisted mode in November and that straight-through was rejected.. Ch 57 §In the real world: "Riverstone'
- **RJ-S2-22** (Ch 55, 59): Ch 59 miscounts and mislabels its own cases.. The introduction says "Three are Riverstone's… The other six are composites". Only Cases 1 and 9 are headed "Riverstone's own"; Case 7 (support automation) is headed "A composite… repr
- **RJ-S2-23** (Ch 1, 3, 58, 62, 64): Ch 58's sales head is male; the book's Sales Head is Anita Rao.. "the sales head wants it switched off. His complaint is specific". Anita Rao is Sales Head in Ch 1, Ch 3 and the bible, and drives the Ch 62 and Ch 64 stories. CAUSE
- **RJ-S2-24** (Ch 53, 56, 59): Ch 59 Case 1 retells Ch 53/56 with the wrong incident.. Case 1 says the day-shift-only model was "Found by a customer return, six weeks later" and fixed with night-shift images, brightness augmentation and a brightness monitor. In
- **RJ-S2-25** (Ch 1, 6, 7, 8, 60): Meera's timeline breaks in Ch 60.. "By January 2026, Meera Iyer had spent four years building pieces of what was now … a genuine platform." Ch 1 has her join as a sales coordinator; Ch 6 has her write a nine-month plan; Ch 8 says 
- **RJ-S2-26** (Ch 58, 60, 61, 62, 63, 64): Part VII's calendar precedes the Part VI systems it depends on. (table above). Ch 60's January 2026 platform includes the PO-intake pipeline, defect model and assistant; those go live in Part VI between March and November 2026. Ch
- **RJ-S2-27** (Ch 3, 63): Ch 63 §63.3 cites `DATA_SPEC.md`'s note about Kolkata's legacy billing system.. `DATA_SPEC.md` is a companion/planning file; the manuscript never describes a Kolkata legacy billing system anywhere else, so the reader meets both th
- **RJ-S2-28** (Ch 67, 80): Ch 67's closing pointer to the interview material is wrong in three ways.. "The Question Banks in the appendices (Chapters 70 through 79)": they are chapters, not appendices; the banks run 70–80 (72A and 76A/B included); and "a de
- **RJ-S2-29** (Ch 51, 64): Ch 64 says the book has no lead-scoring model; Part IV built one.. The Tools note: "Riverstone's ERP and CRM data … contain no real lead-scoring model — Part VI's reverse-ETL sync mentions lead scoring only in passing." Chapters 3
