# The Reader's Journey review

A **third review strand**, separate from the content review in `review/content/` and the visual
review in `review/visual/`. Its findings are **not in `tracker/register.csv`** and are not part of
the 3,758. Nothing here has been approved, and none of it should be fixed under the approval gate
in `CLAUDE.md` section 4 until it has been reconciled into the register or approved another way.

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

Some findings here will duplicate rows already in `tracker/register.csv`, because the content review
covered the same chapters from a different angle. Others are genuinely new, particularly the
cross-part ones: the reading-order references, the story calendar clashing between parts, the two
endings, and the chapter-number and chapter-title citations that were written before renumbering.

Before any of it is acted on, someone has to decide whether to merge these into the register as new
rows or keep the strand separate. Until then, treat this folder as read-only background, the same as
`review/content/`.

## The tool scripts

`tools/` holds the three scripts the pass used against the manuscript:

| Script | What it does |
|---|---|
| `_journey_tools.py` | Reading order, the old-to-new chapter map, `profile()`, `moving_refs()`, `ledger()` |
| `_section_refs.py` | Resolves section-number cross-references |
| `_stale_titles.py` | Finds chapter titles cited from an earlier plan |

They expect to run with the manuscript reachable, and they were written against the working tree at
`Data Science/Analyst-to-Architect/`. Paths will need adjusting to run them from here.
