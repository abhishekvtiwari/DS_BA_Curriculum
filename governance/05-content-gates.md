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

Verified exit codes after the density decision, 2026-09-11:

| Scope | Blocking failures | Exit |
|---|---:|---:|
| BA-M01 + BA-M02 (10 ch) | 3 (G9; deferred under ISS-012) | 1 |
| BA-M03 (7 drafted ch) | 6 (G9; retained under ISS-013) | 1 |
| BA-M04-M15 rejected batch (53 ch) | 53 | 1 |
| Whole corpus (70 ch) | 62 | 1 |
| BA-M02-C01 with `--strict` | 0 blocking, 1 advisory | 1 |

## Gate thresholds and severity

| Gate | Severity for existing chapters | Test |
|---|---|---|
| G1 distinct-paragraphs | BLOCKING | At least 0.90 after masking controlled topic names |
| G2 no-template-body | BLOCKING | No paragraph skeleton exceeds 15% of body paragraphs |
| G3 worked-examples | ADVISORY | At least one worked-example marker per two topics |
| G4 inline-citations | ADVISORY | At least one numeric inline citation per two topics |
| G5 notation-present | BLOCKING | Technical subject notation or a code block is present |
| G6 content-tables | ADVISORY | At least one non-audit content-table row |
| G7 casing | BLOCKING | No known lowercase acronym/proper-noun defect |
| G8 cross-ref-titles | ADVISORY | Referenced module titles match controlled contracts |
| G9 depth | BLOCKING | At least 600 source words per controlled topic |

Under `--strict`, G3, G4, G6, and G8 also determine the exit code.

## Calibration, measured 2026-09-11

The first four columns below are counts of chapters that fail each gate after the density and cross-reference decisions were applied.

| Gate | BA-M01-M02 (10 ch) | BA-M03 (7 ch) | BA-M04-M15 rejected (53 ch) |
|---|---:|---:|---:|
| G1 distinct-paragraphs | 0 | 0 | 48 |
| G2 no-template-body | 0 | 0 | 48 |
| G3 worked-examples | 8 | 7 | 53 |
| G4 inline-citations | 10 | 7 | 53 |
| G5 notation-present | 0 | 0 | 5 |
| G6 content-tables | 7 | 7 | 53 |
| G7 casing | 0 | 0 | 8 |
| G8 cross-ref-titles | 0 | 0 | 0 |
| G9 depth | 3 | 6 | 53 |

G1, G2, G5, and G7 remain blocking because the genuine BA-M01-M03 corpus passes them and the rejected batch does not. G9 is blocking by the owner's density decision: 1,000 words/topic is the planning target and 600 words/topic is the minimum. BA-M01-C03-C05 are genuine but below that floor and are explicitly deferred under `ISS-012`; BA-M03-C01-C06 are genuine but incomplete and retained under `ISS-013`.

G1 and G2 measure paragraphs **after masking the chapter's own topic names**. Exact matching alone is not sufficient: BA-M05-C03 scored a perfect 1.00 on exact matching and 0.79 once the substituted token was masked. A gate that exact-matches would have passed template output, reproducing the ISS-010 defect.

**Advisory for existing chapters; blocking under `--strict` for rebuilt and new chapters** - G3, G4, G6, G8. Existing failures are a remediation backlog. For example, BA-M02-C01 carries zero inline citations, so enforcing G4 retroactively would invalidate an accepted benchmark for a standard it was never asked to meet.

**Owner decision recorded 2026-09-11:** G3, G4, G6, and G8 remain advisory for existing chapters and become blocking through `--strict` for every rebuilt or new chapter.

## Rule

No chapter may be marked `READY FOR REVIEW` while a blocking gate fails. Rebuilt and new chapters are
gated with `--strict`, so advisory gates block them too. The gate output is the evidence; a chapter's
own self-assessment is not.


## Density decision - 2026-09-11

The obsolete flat chapter allocation is abolished. Depth now scales with controlled scope:

- Planning target: 1,000 words per controlled topic.
- Blocking floor: 600 words per controlled topic.
- Counting method: Python `len(text.split())` divided by the number of distinct controlled topic IDs in the chapter source.

G9 is a minimum depth gate, not proof of completeness. A chapter must also pass every other gate applicable to its status. Rebuilt and new chapters must pass `--strict`.
