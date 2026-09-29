# Part 4: questions for Abhishek

The chapter agents' questions, in reading order, trimmed to the decision each one needs. Nothing here blocks the
Part 4 PDF: every chapter builds, and the text as it stands takes the option named "now".

## Story and facts (wait on the fact sheet, PR #3)

1. **Ch 35: full CRM in February.** Meera now uses the full CRM (3,410 matured 2025 enquiries, 7.3% won) in
   February 2026, a month before Ch 36's March story opens it for modelling. The export is dated 31 Dec 2025, so it
   fits. Is that acceptable? (RJ-S2-16, the book calendar, stays Open.)
2. **Ch 40: Deepak's story is dated July 2026**, and **Ch 43's is October 2026**. They stay as they are until the book
   calendar is approved.
3. **Ch 41: Priya Menon (support lead) vs Priya Nambiar (Ch 33, accounts executive).** Are they two people? (C15;
   RJ-S3-46 stays Open.)
4. **Ch 42: the "e-commerce contractor" story (September 2026)** is unchanged, pending the fact sheet.
5. **Fact sheet correction:** its Baskets row (34,017 orders, 92,465 lines) should read **34,013 orders, 92,337
   lines** (see question 8).

## The vendor stories

6. **Ch 35 → 39, the vendor pilot (RJ-S3-41).** Ch 36 says the pilot is running; Ch 39's "In the real world" now
   closes it in one sentence with no numbers: the vendor's scores didn't beat the in-house model, and Anita kept
   Riverstone's own. Is that the outcome you want? (The finding's "0.21 against 0.19" couldn't be computed, so it
   isn't used.)
7. **Repeated vendor stories (RJ-S3-47).** Ch 43's vendor is gone (now Vikram's question after a conference talk);
   Ch 37's AutoML story stays because Ch 43 refers back to it. Drop or reshape any other (Ch 38 agency, Ch 42
   contractor)?

## Data generators

8. **Ch 38 / 42: the basket data could not be rebuilt.** The generator walked a Python set, whose order changes
   between runs (33,636 to 34,017 orders). One line (`sorted(basket)`) makes it reproducible: 34,013 orders and 92,337
   lines on every run. Both chapters now print the new, re-run numbers (lift 3.44, was 3.49). Accept?
9. **Ch 36: five "won" leads whose stage history ends "Lost".** The CRM generator's `never_contacted` can hit won
   leads. Ch 36 reports it as a two-table disagreement (a teaching moment). Keep, or fix the generator (which would
   change numbers in Ch 36, 37, 39 and 44)?
10. **Ch 41: the tickets generator** now plants repeat contacts from a second seed (20242), so the story can quote
    a computed 53% vs 21%. Acceptable?
11. **Ch 40: the sensor generator's `--full` mode** (4.8 million rows) is used by no chapter now. Keep or remove?

## Content choices

12. **Ch 37: "37.0 Setting up, and the data"** stays numbered 37.0, like 10.0, 16.0, 17.0, 26.0, 31.0 and 34.0. OK?
13. **Ch 37, finding 37.50:** the finding said GaussianNB doesn't need scaling. A real run shows a small effect
    (AUC 0.740 scaled vs 0.732 unscaled, through `var_smoothing`), so the table says "No (in scikit-learn,
    slightly)" and §37.5 shows both runs. Fine?
14. **Length.** The approved by-hand steps grew the chapters: Ch 37 48 → 70 pages (20–24 h), Ch 38 33 → 50 (11–14 h),
    Ch 39 → 55 (16–20 h), Ch 40 37 → 52 (16–20 h). Part 4 is now 134–170 hours. Split Ch 37 later, or is its
    Part A / Part B checkpoint enough? The review also suggested moving §40.10 (sensor anomalies) to Ch 50; that
    wasn't an approved finding, so it stays.
15. **Ch 38: silhouette bands** are Kaufman & Rousseeuw, *Finding Groups in Data* (Wiley, 1990). The chapter names the
    authors only. Add a full citation to a bibliography?
16. **Ch 39: lakh in prose, thousands in program output.** Prose says ₹24.5 lakh; Python output prints ₹2,448,060.
    One sentence in §39.3 explains the difference. Acceptable?
17. **Ch 39's new tuning section** was drafted as "39.6a". It is now **§39.7 Tuning honestly**, so interpretation is
    §39.8, fairness §39.9 and model cards §39.10. Ch 41's reference is updated; Ch 74, 76A and 80 are updated in
    Part 8. (Done, for your information.)
18. **Ch 42, exercise 13 (LightFM).** Marked optional (option a), but LightFM doesn't install on current Python.
    Replace it with option (b), an exercise using only installed tools?
19. **Ch 42: two unused figures** (fig42-1 method comparison, fig42-2 segment preferences) were redrawn on the new
    numbers. Place fig42-1 under the §42.7 scoreboard, or delete both?
20. **Ch 43: the transfer-learning demo now shows no win.** With a controlled, seeded comparison (5 runs per size),
    training from scratch beats transfer from the small 0–4 base by 2–3 points at every size; the old "transfer
    helps" came from one noisy run. The chapter reports this and keeps the lesson ("transfer is only as good as its
    base model"). Happy with that?
21. **Ch 44: which churn model?** Ch 37 now recommends logistic regression with four engineered features (test AUC
    0.850); Ch 39, 43 and 44 use Ch 37's hand-set gradient boosting (test 0.829), the model Ch 39 explains. Keep
    boosting in the capstone, or switch it (all numbers recomputed)?
22. **Ch 44: rehearsal, not a live list.** The accounts file has only 2024 features, so the capstone rehearses on
    2025 outcomes (option a). A real 2026 list would need 2025 features in the shared accounts generator. Want that?

## Not done here, for later passes

- **Glossary (Appendix A):** new key terms from Ch 40 (additive model, seasonal index, ADF statistic, AIC,
  over-differencing, exponentially weighted mean, half-life …) and Ch 44 (expected margin at risk, save rate,
  break-even per account, rehearsal).
- **Story bible:** add Deepak Nair, production planner (Ch 40).
- **Hours tables (T12, final pass):** Part 4 is now 134–170 hours (was 86–121); Ch 6, 9 and 83 are recomputed then.
