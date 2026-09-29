# Chapter 59, Industry Case Studies: summary

**What changed.** The chapter keeps its nine cases and its voice. Its framing now matches its own evidence, its cross-references are right, and it has the closing sections every other chapter has.

- **Structure (D8).** The Learn sections are numbered: §59.1 How to read a case study, §59.2–59.10 the nine cases ("59.2 Case 1 · …"), §59.11 What the nine have in common, §59.12 What changes by industry. New closing sections in stage order: Project: your own case card (with Tools you'll need), Check yourself, Exercises (six, in Warm-up / Core / Think about it) and Answers. `restructure.py --check`: already in order, and the builder now draws the chapter map (18/18 page numbers).
- **Honest framing** (59.1, 59.17): two Riverstone cases (1 and 9), measured on the book's simulated line and order data, and seven composites.
- **Case 1 retold as Ch 53 and Ch 56 tell it** (59.7, RJ-S2-24): two incidents, the day-shift model (a return three weeks after a two-week trial) and the flash from the new mould (a silent drift monitor). Each has its own fix. The 97.5% (116 of 119) is Ch 53's printed figure.
- **Case 9** (59.11): one chapter list; "several years"; the unsourced month-end claim dropped; the near-miss sentence reworded; the automatic segment worded as the rewritten Ch 58 now has it ("once fresh data confirms them").
- **Patterns** (59.8–59.10, 59.15, 59.16): pattern 4 now says "mostly organizational" and names the three modeling errors (day shift, leakage, and the confounded price history of Case 4, which the finding's text left out). Pattern 1 names its exception (lead scoring). Pattern 3's "eleven investigations a fortnight" is fixed. Pattern 5 adds the alert budget and the silent error rate. The Recap follows.
- **Cross-references** (59.2–59.6): Ch 40 (seasonal naive, safety stock), Ch 36 §36.7 (leakage), Ch 39 (precision, AUC), Ch 67 (first 90 days), Part 7 = Ch 60–67, Ch 75 and Ch 82 titles.
- **Glosses** (59.13, 59.14): FMCG, SKU, safety stock, vehicle routing solver, operations research, geocoding; precision at a fixed review capacity explained against AUC.
- **Figures** (V59.1, V59.2): both redrawn at 7.6–9.4 pt. Figure 59.2 is now cases × patterns with counts that match the text (8, 7, 8, 7, 6 of 9). Ticks are shapes, not colour alone. Figure 59.1's box 3 is drawn smaller, as its caption says.
- **Tables** (V59.7): the label column is the same width in all ten case cards.

**Skipped, and why.** Nothing in Ch 59 was left undone. RJ-S3-57 is a multi-chapter row. Its Ch 59 part is done, and the stale Ch 64/74 titles left are in Ch 56 (For the integrator).

**Option picks.** 59.1: (A), keep Case 7 a composite (no option is marked as recommended). 59.7: the optional Ch 56 line added, but told as Ch 56 tells it: a customer found the flash, and the 2% audit is the fix. 59.8: the finding's rewrite, extended to Case 4. 59.11: drop the month-end claim. 59.17: both notes, briefly. V59.2: case numbers and names.

**Time needed.** "3–4 hours to read, and a useful afternoon" → **6–8 hours over a week**: about 3 h for the cases, 3–4 h for the project, and 1–2 h for the exercises. The chapter grew from about 4,950 to 6,800 words, mostly the project, exercises and answers.

**Verification.**
- No code blocks (`check_code_teaching.py`: 0 blocks). New `checks/ch59_check.py`: **23 checks pass**. It checks every quoted number against the current source chapter (Ch 53: 97.5% = 116/119, ₹13,840, ₹40,080, 476/6,000, three weeks; Ch 56: flash, 2% audit, change log, lamp alert; Ch 58: 88% = 53/60, 19%, about half an hour, the 62% segment; Ch 44: ₹12.0 and ₹3.9 lakh, AUC 0.829), plus the composite arithmetic (75 reviews per analyst, a tenth), and it checks that Figure 59.2's counts match the text.
- Build: 17 pages. `layout_check`: no stranded headings or lead-ins, no sparse pages, no small text, no clipped lists, tofu 0, map numbers 18/18. The only draft labels flagged are "a coordinator's half hour" (reader text). `prescan`: no sparse pages, nothing near the edge. `fig_check`: 0 figures under 7 pt. Every page viewed at 80 dpi.
