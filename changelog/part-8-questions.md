# Part 8 and the Closing: questions for Abhishek

These are the chapter agents' questions in reading order, grouped and trimmed to the decision each needs. None of
them blocks the Part 8 PDF: every chapter builds, and the text as it stands uses the option described.

## One decision for all the banks

1. **One level scale for every bank (rows 71.23, 72A.28, 73.27, 75.19, 76A.20, 76B.24).**
   - Fresher / Mid / Senior plus role codes: Ch 70, 72A, 73, 74, 75, 76A, 76B, 77, 78 and 79. Ch 80 uses Mid /
     Senior only.
   - Warm-up / Core / Advanced: Ch 71 and 72, as their findings asked.

   Pick one, and it will be applied mechanically in the final pass. The role codes in use are DA, DS, BA, BI, PA,
   AUT, DE, MLE, AIE, ARCH/ARC and LEAD; "AIE" (AI engineer) and "ARCH" (data architect) are new. OK?
2. **A Start stage for the banks?** D8 gives every chapter "Why this matters" and "In plain English", but the banks
   have neither. restructure.py accepts that. Keep the banks exempt?
3. **Question IDs in page order (row 78.17, final pass).** Ch 71, 72, 76A and 81 renumbered their IDs. Ch 78 and 80
   kept theirs stable, so other chapters' citations still hold. Renumber every bank in page order during D2?

## Content choices

4. **Ch 74 lacks topics earlier chapters promise.** Ch 35–43 and 53 tell readers Ch 74 covers PCA, gradient
   descent, k-means and DBSCAN, SHAP and SMOTE, backpropagation and transformers, and TF-IDF, but it has no
   questions on them.
   - The integrator softened those pointers, which is option (a).
   - The agent recommends option (b): add a roughly 12-row rapid-fire §74.8.

   Which do you want?
5. **Topics the book never teaches are marked "Beyond the book".**
   - Ch 72: mutable defaults, closures, `*args`, writing a decorator, and more (row 72.3, option b).
   - Ch 72A: four primers, on two pointers, merge sort, linked lists and binary search trees. The findings
     recommended new sections in Ch 33 instead.
   - Ch 74: adjusted R², frequency encoding and hashing.
   - Ch 77: a junk-dimension note was added to Ch 28 §28.9 (option a).

   Keep them in the banks, or move the teaching into Ch 22, 33 and 36?
6. **Ch 70:**
   - The VBA and Apps Script ran in LibreOffice and a Node mock, not in real Excel or Google Sheets. Re-run them
     once in the real tools before print?
   - The practice table is redesigned, so the results are new.
   - Please check the Senior level tags.
7. **Ch 72, row 72.17:** Python doesn't warn on `x is []`, only on `n is 1000`, so the text quotes the real warning.
8. **Ch 76A:** the story figures in Q76A-007 and Q76A-022 (3 h → 20 min; 7% → 12%) are the candidate's claims and
   can't be computed from the book. Keep them?
9. **Ch 76B:** Q76B-013 uses Ch 25's rule-based at-risk list, because the review's "0.30 threshold in Ch 39 §39.5"
   doesn't exist. OK?
10. **Ch 77, Q77-035:** it allows an automatic merge at very high confidence, but Ch 14 §14.4 says never to
    auto-merge in the CRM. Reconcile?
11. **Ch 79:** the chunking demo now uses Riverstone's real returns policy from Ch 55 (15 days, a 10% restocking
    fee) in place of an invented 30-day policy. Keep it?
12. **Ch 80, Q80-016:** at the book's ₹300 an hour it now makes an honest 18-month payback case. Keep it, or lower
    the build quote?
13. **Ch 82:**
    - The Data Engineer mock is the borderline pass.
    - The Data Analyst and Data Scientist mocks are "extra-points level (mostly 4s)", which follows Ch 69's rule.
    - The Data Analyst memo now recommends reviewing crate discounts before any Industrial push; this comes from
      real `riverstone_2025` queries.

    Acceptable in your voice?

## Names and story

14. **Names:**
    - Ch 69's story uses Ishita, because Kiran is already in Ch 28.
    - Ch 75's uses Kabir.
    - Ch 80's architect is Siddharth, because Vikram clashed with Vikram Singh.
    - Karan still appears in Ch 72 and 72A, as two different candidates.

    OK?
15. **Farah across Part 8 (Ch 81).** The story bank uses her stories from Ch 8, 27, 44, 73 and 76B. Ch 73 places her
    "at a mid-size company". This waits on fact-sheet item C19.
16. **Ch 83, Meera's span:** "About a year, an hour most mornings" between the Friday file and the posting. No
    dates are added; that waits on the calendar.

## Facts that need a source (blocked here)

17. **Ch 68:** the PayScale Data Scientist and Data Engineer rows (retrieved 16 Sep 2026) couldn't be re-checked,
    because payscale.com is blocked. ECBA and LinkedIn "Open to Work" were checked only through search results.
18. **Ch 75:** "30 crore households" stays a labelled assumption, because the census sites are blocked. The Mumbai
    and India population figures come from census CSVs mirrored on GitHub.
19. **Ch 81:** the CTC breakup is illustrative. It states no PF percentage, wage ceiling or gratuity period,
    because the labour and EPFO sites were blocked.

## The hours (T12)

20. **The book's hours grew.** The totals are now 957–1,193 h for Chapters 1–67 (was 762–978). Job-ready (Parts 0–2)
    is 394–488 h, about 15–19 months at 6 h a week.
    - Ch 83 §83.1 pastes `tools/hours_table.py` exactly.
    - The integrator made Ch 6, Ch 9 and "How to Use This Book" match it.

    The front of the book now tells readers 15–19 months to job-ready. OK?

## Not done here, for later passes

- **The Part 8 renumbering (D2) and the cross-reference index (T8):** 72A → 73 and so on, including Q-ID prefixes
  (rows 72A.2, 72A.26, 73.28, 74.25, 83.3).
- **Glossary (Appendix A):** there is no appendix file, so row 83.4 stays Open. New terms are listed in each
  chapter's changelog.
