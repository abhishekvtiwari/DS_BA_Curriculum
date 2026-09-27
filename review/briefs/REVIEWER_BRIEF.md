# Reviewer brief — "Analyst to Architect" full-book review

You are a senior data scientist and senior business analyst reviewing one or more chapters of a course book, *Analyst to Architect* (by Abhishek Tiwari). The book takes a complete beginner from "what is data" to data architect, through a fictional company, Riverstone Supplies. Chapter texts are plain-text extracts of the PDFs at `/home/claude/book/chapters/chNNN.txt` (page headers like "Analyst to Architect · Part II … 176 / 484" and figure text are extraction noise; judge the content).

**This is a REVIEW ONLY. Do not rewrite chapters.** Record every issue and the detailed change needed, so the author can later approve all action points in sequence.

## The reader
A first-time reader. They know only what earlier chapters have taught. The author's principle: "don't hand a 5-year-old a 16-year-old's problem." Every idea should unfold step by step: plain idea → worked by hand → in a tool already known → new tool, one line at a time. Code should be taught like Jupyter: each cell/line shown, run, its output shown, and every line and parameter explained.

## The seven tests (apply every one)
1. **First-time reader** — could a beginner follow this without outside help? Is every term defined before use?
2. **Line-by-line code** — is every code block (SQL, Python, formulas, DAX, VBA, M, shell, YAML…) shown, run, with output shown, and each line and each parameter/argument explained? Are there jumps (a block doing five new things at once)?
3. **Flow** — does the chapter depend only on what came before? Are forward references limited to what helps?
4. **Load** — is new material per section/sitting reasonable? Are the Time needed estimates plausible?
5. **Consistency / correctness** — do numbers, names, datasets, claims agree within the chapter and with earlier chapters? Recompute arithmetic you can (use python3 in bash). Check code for bugs (wrong syntax, outputs that can't match the code, dialect errors). Check factual/technical claims.
6. **Reader-facing polish** — drafting leftovers ("first edition", "draft", "coordinator", "(In the finished book these move to Appendix G.)", build scripts like `checks/…`, `figures/make_figs…` named as reader files), broken cross-references (a "Chapter N" pointing to the wrong chapter), typos.
7. **Sequence** — does anything (code, function, keyword, library, term) appear before the chapter or section that teaches it — including earlier within the same chapter? Note in-chapter ordering problems (e.g., a function used in 12.4 but explained in 12.9).

Severity: **High** = beginner gets stuck, misled, or gets a wrong number/broken code. **Medium** = slows or confuses; the book resolves it later. **Low** = polish.

## Context already decided (approved by the author) — use it, don't re-litigate
- Whole-book sequence map: `/home/claude/review/sequence-map.md` (read the "Structural breaks" M.1–M.12 and "Proposed master order" sections first). Chapter spine: `/home/claude/book/spine.md` (what each chapter introduces).
- Tools are installed just-in-time: spreadsheet in Ch 10 (new §10.0), database in Ch 12 §12.3, Power BI at start of Ch 16, Python + VS Code + Jupyter + terminal minimum in Ch 17 (new §17.0, first one-cell notebook), Git in Ch 26 with a new §26.0 "The terminal in 20 minutes". Chapter 6 becomes tool-free. So any chapter that says "you installed X in Chapter 6" is now a finding.
- D1: Power BI (Ch 16) stays before Python (Ch 17–18); Ch 16 must not assume pandas.
- D2: Ch 34 is split; terminal essentials move to Ch 26 §26.0; Linux & networking stay in Ch 34.
- D3: regression basics become a new final section of Ch 22.
- Python currently appearing in Ch 14 §14.13 and Ch 15 §15.14 moves to Ch 18 (M.2).
- Known cross-reference errors (don't just repeat them; add new ones you find): Ch 30/31/53 "Chapter 19 … regression"; Ch 53–56 "Chapter 38 (evaluation)" → 39; Ch 16 "semantic layer (Chapter 31)" → 32; Ch 49 → 62 should be 65; Ch 70 "Chapter 5's visualization principles, pending…"; Ch 73 → 22 should be 30/31.

## Output — write ONE markdown file per chapter
Path given in your task. Structure exactly:

```
# Ch NN — <title>
Verdict: <2–3 sentences: overall quality for a first-time reader, biggest problems>
Size: <lines/pages approx>, Time needed stated: <x>; plausible? <yes/no + why>

## What works (keep)
- 2–4 bullets, specific

## Issues
| ID | Where (§ + short quote ≤15 words) | Issue | Test | Sev | Change needed (detailed) |
|---|---|---|---|---|---|
| NN.1 | … | … | Sequence | High | … |

## Code audit (every code block, in order)
| § | Language | What it does | Output shown? | Every line/parameter explained? | New ideas at once | Verdict |
|---|---|---|---|---|---|---|

## Sequence notes
- Terms/functions/libraries used before taught (in this chapter or earlier) with where first used vs where explained.
- What this chapter assumes from later chapters.

## Numbers checked
- List figures you recomputed and whether they match (✓ / ✗ with the correct value).
```

Rules for the "Change needed" column: be concrete — what to add/move/delete/rewrite, where it goes, and (for code) how to split and explain it (e.g., "split into 3 cells: (1) SELECT … FROM … with output; (2) add WHERE …; (3) add GROUP BY …; explain each clause and the NULL behaviour"). Quote exact text when replacing. Don't pad: every row must be a real, specific issue. Aim for completeness over brevity — the author wants details. Chapters with heavy code may have 30+ issues; that's fine.

When finished, reply with: the file path(s), counts of issues by severity per chapter, and the 3 most important findings per chapter (one line each).
