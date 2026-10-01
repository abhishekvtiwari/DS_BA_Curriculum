# The Reader's Journey review

A **third review strand**, separate from the content review in `review/content/` and the visual
review in `review/visual/`. **Merged into `tracker/register.csv` on 28 September 2026** (setup PR):
64 findings were added as new rows with `kind` = `reader-journey`, status `Open`. The other 66
duplicate an existing finding, so they were not added twice (see below). Nothing here is approved
until `DECISIONS.md` says so, like any other row.

## What it is

The whole book read in **reading order** rather than chapter order, through two readers at once:

- **Reader 1**, a complete beginner who knows only what earlier chapters taught.
- **Reader 2**, someone already working in data who starts mid-book.

The pass edits nothing. Every finding names a cause and the smallest fix. Structural problems are
stated and stopped rather than solved. It was run per part against a scripted first-appearance
ledger, an overwhelm profile, a promise ledger, a findability audit and the character arcs.

It also carries four standing checks:

| Check | Question |
|---|---|
| A | Reading order is not chapter order. Which references break after renumbering? |
| B | Do Chapters 25, 26, 27 and 83 read harder than their neighbours? |
| C | The book ends twice, at Chapter 67 and at Chapter 83. |
| D | Does a beginner survive the first 200 pages, and Chapter 12? |

## Coverage

| File | Words | Covers |
|---|---|---|
| `journey-findings.md` | 38,670 | Parts 0 and I, then II, III, IV, V, VI, VII |
| `journey-findings.docx` | — | The same document as a review copy |
| `teaching-findings.md` | 13,133 | Code-teaching audit against the §6.5 standard, per chapter |
| `red-team-code-teaching.md` | 6,159 | Why the code-teaching system would fail a first-time reader, and the fixes in priority order |

**Part VIII is not covered.** `journey-findings.md` ends at Part VII, Chapter 67. Chapters 68 to 83
have not been read in this strand, which also means checks B and C are not finished, and the book's
claim of 764 to 980 hours has not been compared against the measured total. At the end of Part VII
the running total stood at 562,503 words, 2,626 key terms, 1,082 exercises and 760 to 973 hours,
already meeting the claim before Part VIII is counted at all.

## Severities and numbering

| Severity | Meaning | Range used |
|---|---|---|
| S1 | Breaks the reader | S1-1 to S1-24 |
| S2 | Loses the reader | S2-1 to S2-29 |
| S3 | Costs polish | S3-1 to S3-78 |
| S4 | Noted, no action | Used as a label, not numbered |

That is 131 numbered findings, plus 25 structural questions for the author, each stated and left
for a decision.

## How this relates to the register

Each of the 130 findings was compared with the register rows of the chapters it names. A text
shortlist was checked by reading both findings. A finding counts as a **duplicate** only when
applying the existing row's fix would fully resolve it.

| Outcome | Count | Where it is recorded |
|---|---:|---|
| New, added to the register | 64 | New rows in `tracker/register.csv` (IDs `RJ-…`). Rows that partly overlap existing findings name them in `notes` as `related: …` |
| Duplicate, not added | 66 | `register-candidates.csv` `notes`: `DUPLICATE of <IDs>`. The original rows' `notes` say `Also raised by RJ-… (Reader's Journey)` |

Rows that name several chapters (for example `6, 14, 19, 20`) keep the full list in `chapter`.
`TRACKER.md` counts them once, on a "Cross-chapter" line per part.

Seven RJ findings assume the 17 September reading order in `planning/chapter-map.md` rather than the
approved sequence map. They are listed in `review/reading-order-conflicts.md` and await a decision.

## The tool scripts

`tools/` holds the three scripts the pass used against the manuscript:

| Script | What it does |
|---|---|
| `_journey_tools.py` | Reading order, the old-to-new chapter map, `profile()`, `moving_refs()`, `ledger()` |
| `_section_refs.py` | Resolves section-number cross-references |
| `_stale_titles.py` | Finds chapter titles cited from an earlier plan |

They expect to run with the manuscript reachable, and they were written against the working tree at
`Data Science/Analyst-to-Architect/`. Paths will need adjusting to run them from here.
