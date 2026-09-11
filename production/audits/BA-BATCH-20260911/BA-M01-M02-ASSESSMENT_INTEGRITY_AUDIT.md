# BA-M01 and BA-M02 - Phase 2 Assessment Integrity Audit

**Audit ID:** BA-BATCH-20260911-ASSESSMENT
**Scope:** 10 chapter question banks, 400 questions (commit `27ffd95`)
**Result:** `QUARANTINED - ASSESSMENT_INTEGRITY_FAILURE - REBUILD_REQUIRED`
**Issue:** `ISS-008`
**Date:** 2026-09-11

## Finding

The bank has no discriminatory power. It must not be published, piloted or scored.

## Disqualifying defect

The correct answer follows a fixed `A, B, C, D` cycle keyed to question number in **400 of 400**
questions across all ten files:

| Question number mod 4 | Correct answer | Count |
|---|---|---:|
| 1 | A | 100 |
| 2 | B | 100 |
| 3 | C | 100 |
| 0 | D | 100 |

**A learner who notices the pattern scores 100% with no subject knowledge.** The key distribution is
exactly 25/25/25/25, which is the signature of a key assigned by rotation and option text fitted to it
afterwards, not of content-driven authoring.

## Supporting defects

- All ten files are **exactly 749 lines** despite covering different chapters.
- **201** distinct distractor strings across **1,200** distractors. Six strings account for 360 of them.
- **46** distinct explanations across 400 questions; five templates cover 290.
- **154** distinct question stems (after masking topic names) across 400 questions.
- Distractors are transparent giveaways ("gather only evidence that supports it", "confidence is an
  acceptable substitute for provenance"), so the key is recoverable by elimination even without the cycle.
- `BA-01-C01-Q002` asks which statement about **Purpose** is correct; the keyed answer
  ("Organizations face more possible changes than they can fund or absorb") is not a statement about
  Purpose, while all three distractors are. The item is answerable by form alone.

## Required before any Phase 2 work resumes

Randomised keys with a verified distribution, distractors built from real misconceptions rather than
absurdities, per-item topic traceability that a reviewer can test, and the content gates in `ISS-010`.
