# Ch 76A changelog: Data Analyst & Data Scientist Question Bank

Option picks: none of the rows offer options except 76A.7 (recommended: rename Ch 76B's IDs to Q76B-xxx and cite them) and 76A.12 (option a: cite what the book's data shows). Level labels: Fresher/Mid/Senior (row 76A.20 suggested "Entry"; Ch 70 and Ch 72A already use Fresher, and the row asks for the same labels across banks).

Question IDs after 76A.6: Q76A-012B → Q76A-013; old Q76A-013…026 → Q76A-014…027 (Q76A-001…012 unchanged).

- 76A.1 · Q76A-012's worked answer rewritten to match Ch 36–39: 90-day target predicted 24 h after arrival; the Q76A-007 rule as baseline (test AUC 0.727, Ch 36 §36.10); logistic 0.838 vs tuned boosting 0.830 on test, logistic better log loss (Ch 37 §37.12), simpler model kept; cost threshold ₹1,500 vs ≈₹30,000 won-lead margin → ≈5% (Ch 39 §39.5). Extra point "[+Trade-offs] reporting that the complex model lost"; follow-up "why didn't boosting win?" (additive signal, 576 wins) · §76A.3 · review's 0.832 corrected to the current 0.830
- 76A.2 · Resume line now "raised conversion … from 7% to 12%"; Strong tier says "5 percentage points, about 71% relative (Chapter 4, §4.2)" · §76A.5 Q76A-022
- 76A.3 · Q76A-022 worked answer rewritten: like-for-like comparison (leads called first under the rule vs the same number under first-come order), selection trap named, total conversion checked, seasonality checked, reps-tried-harder confound admitted, randomized holdout proposed; Strong row "baseline, like-for-like comparison, at least one confound"; Learn it in Ch 4 §4.2, Ch 22 §22.5 and §22.7, Ch 30 §30.8, Ch 31 §31.2. The review's "from x% to y%" placeholders were not filled with invented numbers ("it rose too") · §76A.5
- 76A.4 · Q76A-027: "trained on one year of account activity, predicting whether an account places no order in the following year … monthly call list of 40 accounts … ranked by expected margin at risk (churn probability × last year's revenue × margin)" (Ch 44's term) · §76A.6
- 76A.5 · The numbering note paragraph deleted; opening is now a "Chapter at a glance" box like Ch 70/72A · opening
- 76A.6 · Q76A012B → Q76A-013, later IDs shifted by one; Final-week list updated · §76A.3–76A.6, Final-week list. Inbound: Ch 81 cites Q76A-023 → now Q76A-024 (for the integrator)
- 76A.7 · Cites "Chapter 76B, Q76B-001" and "Q76B-033"; teaching pointers added: Ch 24 §24.1, Ch 25 §25.3 (Q76A-017); Ch 24 §24.8 (Q76A-019) · §76A.4 · recommended option; depends on Ch 76B's own renumbering (row 76B.9)
- 76A.8 · Q76A-017's extra point is now **[+Clarify]** with the prescribed wording; the 76B cross-reference moved to the Learn-it-in / Practise-it-with line. Every other "[Learn it in]" used as a tag in the rapid-fire tables replaced by a real Ch 69 tag, pointers moved to a "Level · learn it in" column · all sections
- 76A.9 · "Chapter 70, §70.11" → "Chapter 70, §70.8 (Q70-069/070)" in Q76A-017 and Q76A-021; teaching pointers Ch 15 §15.2, §15.12, Ch 16 §16.7 · §76A.4
- 76A.10 · Two-part pointers ("Learn it in" teaching section, then "Practise it with" bank): Q76A-001/003 → Ch 7 §7.2 + Ch 25 §25.1; Q76A-006 → Ch 12–13, Ch 7 §7.2 (practise Ch 71); Q76A-007 → Ch 24 §24.4–24.6, Ch 27 §27.10, Ch 36 §36.10 (practise Ch 69 §69.4); Q76A-012 → Ch 36 §36.1/36.10, Ch 37 §37.12, Ch 39 §39.5 (practise Ch 74 §74.7); Q76A-013 → Ch 37 §37.10 (practise Q74-001); Q76A-014 → Ch 39 §39.5, Ch 44 §44.6; Q76A-022 → as 76A.3 (practise Ch 69 Move 7); Q76A-027 → Ch 44 §44.3–44.4, Ch 30 §30.8 (practise Ch 73 §73.4) · all sections
- 76A.11 · Q76A-007 is the DA version (a rule from win rates by source); Q76A-012 opens "the same lead problem as Q76A-007 … the analyst's rule became the baseline"; Q76A-022 says "scoring rule" · §76A.2, 76A.3, 76A.5
- 76A.12 · Q76A-007 now quotes the book's data: referral leads won about 19%, marketplace about 3% (Ch 36 exercise 5, 2023–24); "bigger companies won more often too" checked on the CRM data (closed leads to 2 Oct 2025: 200+ staff 17.7%, 1–10 staff 3.2%) · §76A.2 · option (a)
- 76A.13 · Passes rows rewritten as prescribed for Q76A-007, Q76A-012, Q76A-017 · §76A.2–76A.4
- 76A.14 · "No, it's expected of both" → "It's expected of both:" · Q76A-016
- 76A.15 · Q76A-004 must-have list now points to Ch 8 §8.5 (in the Level · learn it in column) · §76A.1
- 76A.16 · Q76A-002 Learn it in → Ch 8 §8.9 and Ch 7 §7.8 (replaces the §68.6 pointer, so NOTES' §68.6→§68.7 edit is moot) · §76A.1
- 76A.17 · Follow-up now says "(Drift monitoring: Chapter 56, §56.8.)" · Q76A-012
- 76A.18 · Where this leads: "Chapters 36–39 (lead scoring) and Chapter 44 (the churn call list) are the projects behind this chapter's DS examples; if you did them, you can tell these stories as your own practice work." · Where this leads
- 76A.19 · Before you start and Time needed (2–2.5 h + 3–4 h project) added · Chapter at a glance
- 76A.20 · Level (Fresher/Mid/Senior) and Roles on every core question; level per rapid-fire row; key in the glance box · all sections
- 76A.21 · §76A.6 heading → "Full scenarios, talked through live" · §76A.6
- 76A.22 · Q76A-020 → Ch 39 §39.9 (fairness checks: performance by group; §39.8 after Ch 39's renumbering) and Ch 44 §44.7 · §76A.4
- 76A.23 · Q76A-026 adds the own-or-public code caveat and "I can't show that, but here's the same technique on public data" · §76A.5
- 76A.24 · Key terms "cost-based threshold (referenced)" → "cost-based threshold" · Key terms
- NOTES (Ch 39) · SHAP pointers §39.7 → §39.8 (Q76A-016, Q76A-018; old 015/017); fairness §39.8 → §39.9 (Q76A-020; old 019)
- Tags · every tag in Ch 69's `**[+Tag]**` form; [Structure] → [+Signpost]; [Real evidence] → [+Limits] where the text is about admitting a limit (Q76A-010, Q76A-027); [Red flag] in Q76A-025 kept as a plain label
- V76A.1 · High · numbering note gone (see 76A.5) · p. 2 · before/after: img/ch76a-V76A.1-before.png, img/ch76a-V76A.1-after.png
- V76A.6 · Q76A-012B gone; IDs sequential · p. 6–7
- V76A.7 · 76A now cites Q76B-xxx; aligned once Ch 76B renumbers (row 76B.9)
- V76A.2, V76A.8, V76A.10 (style pass) · re-checked in the rebuilt PDF: IDs don't wrap, no stranded lines, tier tables whole
- V76A.3, V76A.4, V76A.5, V76A.9, V76A.11 · already Verified by the style pass; layout_check clean

---

# 3 October 2026 · Four situational sections

Chapter 76A was the thinnest major bank in Part VIII at 27 questions, and it is the one Abhishek
named as the focus: data science *and* data analysis, combined. **27 to 75.**

The existing sections (76A.1–76A.6) are about work you have already finished — walking through a
project, defending a number on your résumé. The four new ones are about **work that has just landed
on you**, which is where an interviewer finds out whether someone has held the job or studied for
it.

| | |
|---|---|
| **76A.7 The analyst's Tuesday** | Requests as they actually arrive |
| **76A.8 The data scientist's Tuesday** | The same, with the problems that come from probabilistic work |
| **76A.9 Working with everyone else** | Engineering, Finance, Product, Legal |
| **76A.10 What changes as you get senior** | The level questions |

48 questions, Q76A-028 to 075. Nothing renumbered.

## The organising idea

**The request as stated is rarely the request.** Q76A-028 — *"can you just pull me a list of all our
customers?"* — has four defensible readings giving four different numbers, and the question that
resolves it is not "which do you mean" but "what will you do with it", because they can answer the
second.

That runs through the whole set: Q76A-029's revenue gap is a definitional difference rather than an
error, and the move is to find a cut of the data equal to the difference. Q76A-031's unused
dashboard is usually answering a question nobody has. Q76A-058's slow query is a symptom of an
access pattern, and the senior move is asking to be given a statement timeout.

## Deliberate non-overlap

Chapter 75 owns metrics, cases and guesstimates; Chapter 81 owns STAR, HR and offers; Chapter 76B
owns requirements. None is repeated. Where a question touches their ground it points at them —
Q76A-062 to Chapter 30's holdout, Q76A-075 to Chapter 81's weakness question.

## Running total

Part VIII: **863 questions to 911.**
