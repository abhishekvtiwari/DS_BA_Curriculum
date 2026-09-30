# Chapter 79 — one-page summary

**What changed.** The drafting note in the glance box is gone ("since this chat doesn't have their approved text…"). The box now has Before you start, Time needed, and a reader-facing "How this chapter is built". Levels and roles, and the note on currency, follow it as ordinary paragraphs so the box fits under the title. Every question has a level (Fresher/Mid/Senior) and roles (AIE, DS, MLE), in the Part 8 bank format. Tags follow Chapter 69's twelve (`**[+Tag]**`), and every rapid-fire table has a "Level · learn it in" column.

The MLOps section no longer contradicts Chapter 56:
- **Q79-028** now treats drift (PSI or the KS statistic D) as the early warning and outcomes as the verdict. It quotes Ch 56's evidence: PSI up to 4.4 with recall holding at 96.8% → 96.5%, then the new mould cutting recall to 84.4%, about 12 points, with no new drift signal. It tells the reader to alert on the size of D or PSI, not on a p-value, and a new cell shows why: 200,000 rows and a 0.03-SD shift give D = 0.016 but p = 3.2e-23.
- **Q79-031** is now "How should you decide when to retrain?": a schedule by default, a performance floor, drift as a prompt to investigate, and business events as the best trigger (Ch 56 §56.9).
- **Q79-039**: the retraining trigger and feature store follow from the Q79-031 and Q79-030 changes.

**Q79-033** prices per million tokens, not per thousand, which removes the 1,000× error. It uses Ch 54's workhorse tier ($2/$10, checked 29 Sep 2026): $0.0025 a call and $5.00 a day (₹440). The volume tier is shown as the routing lever. It quotes Riverstone's real scale: ₹0.079 per email (Ch 57) and 13–14 paise a question (Ch 55).

**Pointers.** Every "Learn it in" pointer is now at section level, checked against the current files. Several of the review's numbers had moved:
- the reranker note is in §55.5;
- pipelines are §36.9;
- relational indexes are §71.9;
- pgvector is in Ch 55's project tools.

Prompt injection now points to Ch 54 §54.11 and Ch 55 §55.10, and the circuit breaker to Ch 78 Q78-021, Ch 57 §57.8 (described there) and Ch 58 §58.6 (built there). Training-serving skew is defined in Q79-030 (Ch 56 §56.11). Multi-agent systems are marked **Beyond the book** with a short explanation.

**Chunking demo.** It now chunks Riverstone's actual returns policy from Ch 55's corpus (15 days, 10% restocking fee). The old text said "30 days", which contradicted Ch 55. The demo shows the real overlap and the mid-word cuts, and that chunk 0 carries "15 days" without the fee.

**Option picks.** None of the rows marks a recommended option, so (a) is used throughout. For 79.16 that means "Beyond the book" in this chapter, with Ch 55 left untouched.

**Skipped.** Nothing. All 24 content rows and V79.1 are applied. V79.2–V79.11 were already done by the style pass and are re-checked here.

**New Time needed.** 3½–4½ hours for a first pass, plus 45 minutes for the final-week list. The chapter had none before. The estimate is 11 core questions at about 10 minutes each, 28 rapid-fire rows at 1–2 minutes, two design cases at 20 minutes, and 45 minutes for the four demos.

**Code and numbers verified.**
- `tools/verify_python.py`: 5 blocks run, 5 outputs checked, **0 mismatches** (Python 3.11, NumPy 2.4.6, SciPy 1.17.1). Each demo starts from a fresh namespace.
- `check_code_teaching`: 0 flags.
- `checks/ch79_check.py`: OK. It checks all 42 cited sections, 48 quoted facts inside their sections, 7 question IDs from other banks with their topics, the prose arithmetic, and the tag set.

**Build.** 24 pages. layout_check is clean: map 11/11, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0, no draft labels. prescan is clean; its only line-end hyphens are real compound words, and its "draft" hit is reader text ("drafts the reply"). No figures. `restructure.py --check`: already in order.
