# Measurable Content Gates

**Status:** ADOPTED 2026-09-11 - replaces the chapter self-audit
**Issue:** `ISS-010`
**Tool:** `tools/content_gates.py`

## Why the previous audit was removed

The chapter "Theory completeness audit" marked 364 of 364 topic rows `COVERED` with zero exceptions
across BA-M04 through BA-M15, and stamped every chapter `SELF_AUDIT_PASSED`. It verified that required
headings existed. It never inspected what was under them, so it certified template output as complete.
A check that has never failed is not evidence. All stamps in that scope are voided (`ISS-009`).

## The gates

Run `python tools/content_gates.py --all --quiet`.

Each gate carries a severity, and **only blocking failures set the exit code**:

| Invocation | Exit code driven by | Use for |
|---|---|---|
| `content_gates.py <chapter>` | blocking failures only | existing chapters, CI on the current corpus |
| `content_gates.py <chapter> --strict` | blocking **and** advisory | rebuilt and new chapters |
| `content_gates.py <chapter> --advisory-only` | never non-zero | reporting without enforcement |

Output marks `x` for a blocking failure, `!` for advisory, `.` for pass. A chapter that clears every
blocking gate but fails an advisory one prints `PASS*`. Files that are not controlled theory chapters
(word budgets, checkpoints, audits) are skipped rather than graded.

Verified exit codes, 2026-09-11:

| Scope | Blocking failures | Exit |
|---|---:|---:|
| BA-M01 + BA-M02 (benchmark, 10 ch) | 0 | **0** |
| BA-M03 (parked, 7 ch) | 6 (G9 depth) | 1 |
| Whole corpus (70 ch) | 59 | 1 |
| BA-M02-C01 with `--strict` | 0 blocking, 1 advisory | 1 |

| Gate | Threshold | Defeats |
|---|---|---|
| G1 distinct-paragraphs | **0** | **48** |
| G2 no-template-body | **0** | **48** |
| G3 worked-examples | 15 | 53 |
| G4 inline-citations | 17 | 53 |
| G5 notation-present | 0 | 5 |
| G6 content-tables | 14 | 53 |
| G7 casing | **0** | **8** |
| G8 cross-ref-titles | 4 | 15 |
| G9 depth | **6** | **53** |

## Calibration, measured 2026-09-11

Failures per gate, run against the whole BA corpus. BA-M03 is shown separately because it is parked and
incomplete under `ISS-005`, so it is not part of the benchmark:

| Gate | BA-M01-M02 benchmark (10 ch) | BA-M03 parked (7 ch) | BA-M04-M15 rejected (53 ch) |
|---|---:|---:|---:|
| G1 distinct-paragraphs | **0** | 0 | 48 |
| G2 no-template-body | **0** | 0 | 48 |
| G3 worked-examples | 8 | 7 | 53 |
| G4 inline-citations | 10 | 7 | 53 |
| G5 notation-present | **0** | 0 | 5 |
| G6 content-tables | 7 | 7 | 53 |
| G7 casing | **0** | 0 | 8 |
| G8 cross-ref-titles | 1 | 3 | 15 |
| G9 depth | **0** | 6 | 53 |

The principle: a gate the benchmark passes 10 of 10 can block immediately. A gate the benchmark also
fails records a standard never yet met and cannot block until remediation is funded.

**Blocking now** - G1, G2, G5, G7, G9. Each is failed by **0 of 10** benchmark chapters and by 5 to 53 of
the 53 rejected chapters, so they separate authored work from template output cleanly. G9 additionally
fails 6 of 7 BA-M03 chapters, which is correct: BA-M03 is parked at roughly 18% of its stated allocation.

G1 and G2 measure paragraphs **after masking the chapter's own topic names**. Exact matching alone is
not sufficient: BA-M05-C03 scored a perfect 1.00 on exact matching and 0.79 once the substituted token
was masked. A gate that exact-matches would have passed template output, reproducing the ISS-010 defect.

**Advisory pending owner decision** - G3, G4, G6, G8. These fail the benchmark modules as well. Those failures are real, not false positives:
BA-M02-C01 carries zero inline citations, and BA-M03-C06 cites BA-M07 as "Data Analysis and SQL" when
its contract title is "Agile, Scrum, Kanban, and Waterfall". They record a standard the repository has
never met rather than a regression introduced by the rejected batch.

**Owner decision required:** adopt G3/G4/G6/G8 as blocking for all new and rebuilt chapters and schedule
a remediation pass over BA-M01-M03, or hold them advisory until that pass is funded. Recommendation:
adopt them as blocking for **rebuilt and new** chapters only, which sets the rebuild standard above the
current benchmark without retroactively invalidating BA-M01 and BA-M02.

## Rule

No chapter may be marked `READY FOR REVIEW` while a blocking gate fails. Rebuilt and new chapters are
gated with `--strict`, so advisory gates block them too. The gate output is the evidence; a chapter's
own self-assessment is not.
