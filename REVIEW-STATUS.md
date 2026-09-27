# Book review status — Analyst to Architect

Agreed process (Abhishek, 2026-09-25): review the WHOLE book part by part first, recording detailed findings and changes; no rewriting. After all parts are reviewed, Abhishek reviews all action points in sequence; only then fix instructions and rewrites.

Version rule (Abhishek, 2026-09-27): where a chapter exists in several versions (v1, v1.1, v2, v3, v4…), the latest is final. Blueprint files (Analyst-to-Executive-Blueprint, Blueprint-v3) are out of scope.
- Checked: every chapter PDF in Drive folder "To be reviewed" matches the 25 Sep manuscript (Part PDFs) used for the content review, except Ch 12: the folder holds Draft v3 (70 pp, 15–18 h); the latest is Draft v4 (96 pp, 19–23 h, expanded §12.13; Drive id 10BehGJBNmLTmpZ-sRjFK2xwXKoVqX4JH), which matches the manuscript. Ch 12 visual review redone on v4.

Content review (2026-09-25): ALL PARTS REVIEWED (Ch 1–83). 2,534 findings: 406 High, 1,071 Medium, 1,055 Low.
- Index, per-chapter verdicts, themes: `claude/full-book-review-index.md`
- Parts 0–I findings: `claude/findings-part-0-and-I.md`; sequence map: `claude/sequence-map.md`
- Draft fix instructions Parts 0–I: `claude/fix-instructions-part-0-and-I.md` — PARKED.

Visual/layout review (2026-09-27): COMPLETE on final versions. 85 chapters, 2,455 pages. 1,224 findings: 95 High, 631 Medium, 498 Low. Summary, themes, all High findings: `claude/visual-review-summary.md`.

Combined action register (Book-Review-Action-Register.xlsx, delivered in session 2026-09-27): 3,758 rows — 501 High, 1,702 Medium, 1,553 Low.

FIXING PLAN (agreed 2026-09-27): fixes happen in a private GitHub repo worked by Claude Code (Abhishek uploads from phone; no local folder linked to this project chat). Starter kit delivered in session 2026-09-27:
- kit-1-repo.zip (3 MB): CLAUDE.md (full instructions for Claude Code: reader lens, 7 tests, approved decisions, approval gate, order of work, per-chapter fix procedure, PR rules), DECISIONS.md (Abhishek fills: global rule A1/A2/A3, 26 themes T1–T14 + V1–V12, structural decisions D1–D5, 34 option-pick rows), tracker/register.csv (all 3,758 findings, status column; Part 0/I content rows already Approved), tracker/make_tracker.py → TRACKER.md, review/ (content per chapter, visual per chapter, sequence map, briefs, prescan.py, xlsx), source/ (for book sources), fixed/, changelog/, build/.
- kit-2-snapshots.zip (20 MB): review/visual/snaps (762 PNGs).
- Order of work in CLAUDE.md: bootstrap (unzip, document build in source/BUILD.md, test-build Ch 12) → style pass for whole book → Riverstone fact sheet PR → content fixes one PR per part (0 → Closing) → cross-refs, Time needed tables, Part VIII renumbering.
- Blocker: book source files (chapter text + build/stylesheet + figure scripts) must be uploaded to source/ (zips ≤25 MB each). Drive has Analyst-to-Architect-Part-II-complete-bundle.zip (30 MB) that may contain sources.

NEXT: Abhishek creates the private repo, connects Claude Code (Claude GitHub app), uploads the two kits + source zips, fills DECISIONS.md.

Approved decisions so far: Part 0/I findings; just-in-time tool setup (Ch 6 tool-free); D1 Power BI before Python; D2 Ch 34 split (terminal essentials → Ch 26 §26.0); D3 regression basics = new final section of Ch 22.

---

*Added when this document was committed, 28 September 2026. The text above is the record as written and is unchanged.*

Two things in it are now out of date:

- **The `claude/` paths** refer to files delivered in the review chat. In this repo they are: `claude/full-book-review-index.md` → [`review/content-review-index.md`](review/content-review-index.md); `claude/findings-part-0-and-I.md` → [`review/part-0-and-I/findings.md`](review/part-0-and-I/findings.md); `claude/sequence-map.md` → [`review/sequence-map.md`](review/sequence-map.md); `claude/visual-review-summary.md` → [`review/visual-review-summary.md`](review/visual-review-summary.md); `claude/fix-instructions-part-0-and-I.md` → [`review/part-0-and-I/fix-instructions-DRAFT-parked.md`](review/part-0-and-I/fix-instructions-DRAFT-parked.md).
- **The blocker is cleared.** The book's sources, including the build script and stylesheet, were pushed to this repo before the kits and are at `Data Science/Analyst-to-Architect/`. Nothing needs uploading from a phone. See [`source/SOURCES-LOCATION.md`](source/SOURCES-LOCATION.md), which also records one real obstacle: `tools/pdf/build.py` hardcodes a sandbox path and must be made relative before any build will run.

Both kits are unpacked here, so bootstrap steps 1 and 2 in `CLAUDE.md` are done. Steps 3 to 5, running `make_tracker.py`, writing `source/BUILD.md` with a test build of Ch 12, and opening the `setup` PR, are still outstanding.
