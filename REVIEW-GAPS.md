# Readiness: what is complete, what was closed, what is left

Audited and closed 28 September 2026 against the whole repository. The aim was to leave nothing
between opening this repo and working on the book itself.

## Everything needed for the fix run is here

Verified by measurement, not by reading a manifest.

| Thing | State |
|---|---|
| Content review | All 85 chapters. `review/content/ch10.md` to `ch83.md`, plus `review/part-0-and-I/findings.md` for Chapters 1 to 9 |
| Visual review | All 85 chapters, `review/visual/ch01.md` to `ch83.md` |
| Visual snapshots | 762 PNGs. Every chapter has at least three; none has zero |
| Register | `tracker/register.csv`, 3,822 rows (3,758 from the review + 64 Reader's Journey). 2,534 content, 1,224 visual, 64 reader-journey. 29 Approved |
| Chapter PDFs | 175. Every part has one per chapter, and all 85 match what the review read |
| Manuscript | 87 Markdown files, `ch01` to `ch83` including `ch72a`, `ch76a`, `ch76b` |
| Figures | 262 SVGs, 69 draw scripts. **All 254 image references in the chapters resolve to a real file** |
| Riverstone data | Complete. The data pack was compared file by file: all 15 files byte-identical to `companion/full/`. Nothing was missing |
| Companion code | 52 per-chapter folders, 8 `generate_riverstone_*.py` scripts, `full/`, MySQL and PostgreSQL setup |
| Build tooling | `tools/pdf/` builder, stylesheet and templates, 63 check scripts, 4 verifiers, code-teaching checker |

## Closed

| # | Gap | What was done |
|---|---|---|
| 1 | Part IV and Part VIII shipped without their `pdf/` folders, so two parts had no PDF for a visual finding to cite | Added the corrected bundles: 10 chapter PDFs plus a collated file for Part IV, 17 plus a collated file for Part VIII |
| 2 | The standalone set held **Ch 12 v3 at 70 pages** while the visual review was done on **v4 at 96 pages**, so every Ch 12 page reference pointed into a file that did not have those pages | `Analyst-to-Architect-PDFs-Ch01-34/Ch12-…pdf` is now v4, 96 pages. v3 is untouched in the Part II bundle and in git history |
| 3 | The Reader's Journey strand existed only in a local folder | Added at `review/reader-journey/` with a README, and its 130 findings extracted into `register-candidates.csv` in the register's own schema, ready to append on a decision |
| 4 | The sources were believed missing and needing a phone upload | They were already here. `source/SOURCES-LOCATION.md` records where, with the commands |
| 5 | **The PDF builder could not run outside the sandbox the book was written in.** It hardcoded `/home/claude/book/pdf`, read its templates from the wrong place, wrote output to `/mnt/user-data/outputs`, and named 16 chapter sources by absolute sandbox path | Rewired to resolve everything from its own location, with `BOOK_BUILD_DIR` and `BOOK_OUT_DIR` overrides. The original is kept as `build.py.orig-sandbox` |
| 6 | **The builder covered only 12 of 85 chapters.** The rest were built by scripts from other sessions that are not in this repo, so 73 chapters could not be rebuilt at all | Added a generic path that derives the cover from each chapter's own H1 and part line. All 85 chapters now resolve and build. `--list` and `all-chapters` added |
| 7 | Rebuilt filenames would not have matched the reviewed PDFs | Pinned. All 85 derived names now equal the released filenames exactly, via a small `NAMES` table for the eight chapters whose released name is shorter than their title |
| 8 | No build documentation | `source/BUILD.md`: the four-stage pipeline, requirements, commands, what changed, what is still unknown |
| 9 | `TRACKER.md` was the copy shipped in the kit | Regenerated from the CSV by `tracker/make_tracker.py`. Reads 0 of 3,758 closed, which is correct |
| 10 | Filling `DECISIONS.md` meant facing 3,758 rows with no sense of what each theme covers | `DECISIONS-BRIEFING.md`: every one of the 26 themes with an approximate row count, its High/Medium/Low split and two real examples. Regenerate with `tracker/make_briefing.py` |

## Left, and who owns it

*Updated 28 September 2026 by the setup PR.*

### 1. `DECISIONS.md` has a draft awaiting approval. Yours, and it blocks everything.

Claude Code filled in a recommendation for every item in the "Draft decisions" pull request. Edit
what you disagree with; merging it is the approval. Until then, only the 29 Part 0 and I rows
already approved may be fixed.

### 2. Reading order: two sources disagree. Yours.

`planning/chapter-map.md` (17 Sep) and `review/sequence-map.md` (25 Sep) give different orders for
Parts II and III, and 46 findings depend on which one holds. Everything is listed in
[`review/reading-order-conflicts.md`](review/reading-order-conflicts.md) and asked in the setup PR.

### 3. Build: done, verified.

Ch 12 rebuilds with the same 96 pages as v4. All 85 chapters rebuild with the same page counts and
identical body text. See [`source/BUILD.md`](source/BUILD.md). Install with
`bash source/setup-toolchain.sh`.

### 4. Reader's Journey: merged, still unfinished at Part VIII.

The 130 findings were reconciled into the register: 64 new rows, 66 duplicates recorded against their
originals (see [`review/reader-journey/README.md`](review/reader-journey/README.md)). The strand
still stops at Chapter 67, so its checks B and C and the 764 to 980 hour claim remain unverified. The
register itself covers all 85 chapters, so the fix run is not blocked.

### 5. Five parts have no collated whole-part PDF.

Parts 0, I, IV and VIII have one. Parts II, III, V, VI and VII do not, because only Parts 0 and I have
collated markdown in `manuscript/`. The toolchain can now build them once collated markdown exists.
Cosmetic for the fix run.

## Noted, no action

| Thing | Why it is fine |
|---|---|
| Ch07, Ch08, Ch09 exist as two renders | Same page counts; the text differs only by a trailing period in the title |
| Ch12 v4 is named `v4-for-review` | The version rule makes the latest final, and the review used v4. The filename is stale, not the file |
| Ch29's only PDF is `v1.1-for-review` | No later version exists, so it is the operative one, and the standalone set matches it |
| Part II has 16 PDFs for 15 chapters | Both Ch 12 versions are kept there deliberately |
| `S3-48` is missing from the journey findings | A numbering gap in the document, not a lost finding. 130 of 131 IDs exist and all 130 were extracted |
| `build/` holds only a README | Correct. Gitignored scratch; final PDFs go to `fixed/` |
| `source/` is empty | Deliberate. See `source/SOURCES-LOCATION.md` |
| Theme counts in the briefing are approximate | Keyword-matched. `CLAUDE.md` still requires the agent to map each row by reading it |

## The order to start in

1. Merge (or edit, then merge) the "Draft decisions" PR.
2. Answer the reading-order questions in the setup PR, then merge it.
3. Then the style pass, the Riverstone fact sheet, and the per-part pull requests, per `CLAUDE.md` section 5.
