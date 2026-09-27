# The Coherence Pass — reviewing Parts 0 to VI as one reader's journey

*Coordinator, 20 September 2026. This is the method and the commands. Nothing in it is executed yet: Part VII is built first, and the pass runs on Parts 0 to VI while that happens, then absorbs VII and VIII when they land.*

---

## 1. Why this pass exists

Fifty-six chapters and 639,000 words were written by seven different chats, in parallel, each holding only its own part in context. Every chapter passed its own Definition of Done. Nobody has yet read the book the way a reader will: front to back, as one person learning one thing after another.

That is the whole purpose of this pass. It is not a quality-control sweep looking for mistakes in chapters. It is a **reading**, by someone who does not already know the material, asking four questions in order:

1. **Does the sequence hold?** Is anything used before it is taught?
2. **Does it overwhelm?** Can a beginner survive the first two hundred pages without quitting?
3. **Can an experienced reader find things?** Is it usable as a reference, not only as a course?
4. **Is the code actually taught?** Line by line, setting by setting, as §6.5 requires.

The fourth is the one you raised first and it is the one with hard numbers behind it. The first three are what turn 56 good chapters into one book.

---

## 2. What the pass must not do

Three rules, from your own instruction of 18 September:

- **Read before editing.** Fable reads and reports. It does not change a single manuscript. Every finding names a cause, not a symptom.
- **Fix in place, by the owner.** A finding is applied by the chat that owns that part, because only that chat can re-run the check scripts, regenerate the figures and rebuild the PDF. Fable produces the diagnosis; the part chat performs the surgery.
- **A flag is a question, not a verdict.** Both the checker and Fable's findings are pointers to places worth reading. A deliberate exception, recorded with one line of reasoning, closes a finding as surely as a fix does.

---

## 3. Two Fable chats, by pass type

**Fable A: the Reader's Journey.** Reads all 56 chapters in reading order, as a beginner would. Owns sequence, overwhelm, findability, promises and story arcs. Produces `review/journey-findings.md`.

**Fable B: the Teaching Layer.** Works chapter by chapter through the code, formulas and settings. Owns §6.5: line-by-line explanation, settings tables, measured what-ifs, over-long blocks, first-use-is-explained-use. Produces `review/teaching-findings.md` and, for each chapter, a concrete patch list.

They are separate because they are different kinds of judgment. A reader's-journey finding needs someone holding 600,000 words loosely. A teaching finding needs someone looking hard at eleven lines of Python. Mixing them produces a chat that does neither well.

They run in parallel. Neither blocks the other. Both finish before any part chat starts applying fixes.

### The three phases

| Phase | Who | Output | Ends when |
|---|---|---|---|
| 1. Diagnose | Fable A and Fable B, in parallel | Two findings files, every finding with an owner and a severity | Both files delivered to the coordinator |
| 2. Triage | Coordinator (this chat) | One work order per part, merging both files, with your decisions on anything that changes the book's shape | You approve the work orders |
| 3. Repair | Each part's own chat, under §15.1 | Fixed chapters, re-verified, PDFs rebuilt, a report of what changed and what was deliberately left alone | The coordinator re-runs the checks and signs the part off |

---

## 4. What Fable A is actually looking for

### 4.1 The first-appearance ledger

The core artifact of the whole pass. One row per term, tool, function, file format and concept:

| Thing | First **used** | First **explained** | Verdict |
|---|---|---|---|
| `GROUP BY` | Ch 10 §10.9 | Ch 13 §13.4 | used 3 chapters early |

Anything where "first used" comes before "first explained" is a sequence break. Anything explained twice at full length is duplication. Anything explained nowhere is a hole.

This is mechanical enough to script and important enough to be worth scripting. Fable A builds it once, for the whole book, in reading order.

### 4.2 The overwhelm profile

The book states its own study time: **762 hours** across the chapters that declare one. That is a two-year evening commitment. It is honest, and it is also the single biggest risk of the reader closing the book in week three.

Fable A measures, per chapter: new terms introduced, new tools required to be installed, word count, stated time needed, and number of exercises. Then it looks for:

- **Spikes.** Chapter lengths run from 4,904 words (Ch 44) to 32,273 (Ch 12), a 6.6× spread. Where a chapter is three times its neighbours, the reader feels it.
- **Cliffs.** A chapter that needs four new tools installed before anything runs.
- **Flat stretches.** Long runs with no win, no finished artifact, no "you can now do this".
- **Missing rest.** After a hard chapter, is there a lighter one, a project, a recap?

The output is not "Chapter 12 is too long". It is "the reader arrives at Chapter 12 having installed two databases and having written no code of their own; the chapter then runs 32,000 words before its first project."

### 4.3 The promise ledger

`planning/promises-from-approved-chapters.md` holds 1,933 forward references. Fable A checks a sample and every promise that carries a specific claim: was it kept, in the chapter named, in the form promised? Unkept promises are the most damaging kind of error, because the reader remembers being told.

### 4.4 The findability audit

For the reader who bought this to look things up, not to read it:

- Does every chapter have a usable *at a glance*, *key terms*, *recap* and *where this leads*?
- Are the cross-references specific (a section number) rather than vague (a chapter)?
- Is there a path to a topic without reading the part it sits in?
- What belongs in an index, and what belongs in a "if you already know X, start here" table at the front?

### 4.5 The arcs

Meera, Farah, Anita, Vikram and the rest run through the whole book. Fable A tracks each person's arc in reading order and flags contradictions, resets and disappearances. Cross-part issues 3, 6 and 13 are already open examples.

---

## 5. What Fable B is actually looking for

The numbers are already measured, in `planning/code-teaching-baseline.md`. The headline: **one chapter in 56 contains the settings table §6.5 requires.**

| Part | Code blocks | Blocks flagged | Chapters with a settings table |
|---|---|---|---|
| Part 0 | 5 | 2 | 0 of 6 |
| Part I | 0 | 0 | 0 of 3 |
| Part II | 499 | 148 | 0 of 15 |
| Part III | 303 | 153 | 0 of 7 |
| Part IV | 247 | 182 | 1 of 10 |
| Part V | 102 | 52 | 0 of 8 |
| Part VI | 116 | 61 | 0 of 7 |

Fable B's job, per chapter, is to turn each flag into one of three things:

1. **A patch**: the exact settings table, the exact "How it works" bullets, or the exact split of an over-long block, written out and ready for the part chat to drop in.
2. **A measured what-if**: named precisely: which setting, which values, what has to be re-run to get the real output.
3. **A deliberate exception**: one line saying why this block does not need it (a repeat of something already taught, an output-only block, a recap explicitly labelled as such).

Priority order, by density of flags rather than raw count: **Part IV** (182 of 247 blocks), then **Part VI** (61 of 116), **Part III** (153 of 303), **Part V** (52 of 102), **Part II** (148 of 499). Inside Part IV, Chapter 37 first: it never names `random_state`, `stratify`, `test_size`, `cv`, `n_neighbors`, `alphas` or `handle_unknown` in its prose, and nine of its blocks run over 25 lines.

---

## 6. The severity scale, used by both

| Level | Meaning | Handling |
|---|---|---|
| **S1 — breaks the reader** | Something is used before it is taught, a promise is unkept, an instruction does not work | Fix before publication, no exceptions |
| **S2 — loses the reader** | Overwhelm spike, unexplained setting in a first-use block, a 70-line block presented as one step | Fix in the part's review pass |
| **S3 — costs polish** | Vague cross-reference, missing key term, style drift | Batch and fix in one sweep |
| **S4 — noted, no action** | A deliberate exception, or a flag the reading shows is fine | Recorded with one line of reasoning |

Every finding carries: severity, chapter and section, what a reader experiences, **the cause**, the proposed fix, and the owner.

---

## 7. The commands

Two kickoff commands, then one command per part. Paste them as written. They assume the chat can read the bundle files; attach the relevant part bundles at the start.

### 7.1 Fable A — kickoff

```
You are Fable A, reviewing the book "Analyst to Architect" as a reader's journey.
Fifty-six chapters, about 639,000 words, written by seven separate chats in parallel.
Every chapter passed its own quality bar. Nobody has read them as one book. That is your job.

READ FIRST, in this order:
  1. planning/chapter-writing-instructions.md  (the whole thing, especially sections 4, 5, 6.5 and 15.1)
  2. planning/chapter-map.md                    (note the reading order at the top: it is NOT the chapter numbers)
  3. planning/blueprint.md                      (what the book set out to be)
  4. planning/cross-part-issues.md              (19 issues already known; do not re-report them, extend them)
  5. planning/promises-from-approved-chapters.md
  6. planning/code-teaching-baseline.md         (Fable B owns this; read it only so you don't duplicate that work)

YOUR ROLE: you are the reader. Specifically two readers at once.
  Reader 1 is a complete beginner. They have never written a line of code. They bought this to change careers.
  Reader 2 already works in data. They bought this to fill gaps and prepare for interviews. They will not read
  it front to back; they will look things up.
  Every finding must say which reader it hurts.

METHOD, and this order is not optional:
  1. Read the whole book in READING ORDER (planning/chapter-map.md, top table), start to finish, EDITING NOTHING.
     Take notes as you go. Do not stop to analyse. Read it the way a person reads a book.
  2. Only then build the first-appearance ledger: one row per term, tool, function, file format and concept,
     with where it is first USED and where it is first EXPLAINED. Script this; do not do it by hand.
  3. Then the overwhelm profile: per chapter, new terms, new tools to install, word count, stated time needed,
     exercise count. Find the spikes, the cliffs, the flat stretches, and the places with no rest after hard work.
  4. Then the promise ledger: check every promise that carries a specific claim. Was it kept, where it said,
     in the form it said?
  5. Then the findability audit: at-a-glance, key terms, recap, where-this-leads, cross-reference precision,
     and what a front-of-book "if you already know X, start here" table would need to contain.
  6. Then the character arcs: Meera, Farah, Anita, Vikram, Neha, Rahul, Suresh, Imran/Irfan, and the rest.
     Track each person in reading order. Flag contradictions, resets and disappearances.

RULES:
  - You do not edit any manuscript. Not one line. You diagnose; the part chats operate.
  - Every finding names a CAUSE, not a symptom. "Chapter 17 is confusing" is not a finding.
    "Chapter 17 uses a list comprehension in section 17.4 and first explains one in 17.9" is a finding.
  - Severity S1 to S4, per the scale in planning/coherence-pass-strategy.md section 6.
  - Do not propose rewriting chapters. Propose the smallest change that fixes the cause.
  - Where the fix is structural (a chapter split, a section moved between chapters, a new bridging section),
    say so plainly and stop there: that is the author's decision, not yours.

OUTPUT: review/journey-findings.md, in this shape:

  ## Summary
  - The three things that most damage the reader's journey, in order.
  - What the book does unusually well, so the repair does not destroy it.

  ## S1 findings
  | # | Chapter and section | What the reader experiences | Cause | Proposed fix | Reader hurt | Owner |

  ## S2 findings  (same table)
  ## S3 findings  (same table)

  ## The first-appearance ledger
  (the full table, plus a short list of every row where used-before-explained)

  ## The overwhelm profile
  (the per-chapter table, plus the spikes, cliffs and flat stretches named)

  ## Promises checked
  ## Findability
  ## Character arcs
  ## Structural questions for the author
  (anything that changes the book's shape: chapter splits, merges, moves, or a new chapter)

Start with Part 0 and Part I and send me a short interim note when you reach Chapter 10, so I can
tell early whether the method is working. Then keep going without stopping.
```

### 7.2 Fable B — kickoff

```
You are Fable B, auditing how the book "Analyst to Architect" teaches code, formulas and settings.
Fifty-six chapters, 1,272 code blocks. Your standard is section 6.5 of the writing instructions.

READ FIRST:
  1. planning/chapter-writing-instructions.md, section 6.5 in full, then sections 5 and 15.1
  2. planning/code-teaching-baseline.md   (the measured starting point: which blocks are flagged, per chapter)
  3. tools/check_code_teaching.py         (so you know exactly what the flags mean and where the tool is blunt)
  4. planning/note-to-part-chats-code-teaching.md

THE PROBLEM, in the author's words: "if supervised learning code is written, it's not explained what each
line means, what does what, which parameter to change will do what and how. The basic question of a
first-time reader is missing."

THE MEASURED FACT: one chapter in 56 contains the settings table section 6.5 requires (Chapter 44).
Every other chapter shows code that works, and does not tell the reader which parts of it they may change.

METHOD, per chapter, in priority order (Part IV first, then VI, III, V, II, 0):
  1. Run: python3 tools/check_code_teaching.py <manuscript>
  2. Read the chapter's code sections properly. The checker is a pointer, not a verdict. Do not act on a flag
     you have not read the surrounding pages for.
  3. Turn every flag into exactly one of three things:
     (a) A PATCH, written out in full and ready to drop in: the settings table, the "How it works" bullets,
         or the split of an over-long block into steps that each get their own explanation.
     (b) A MEASURED WHAT-IF that must be run: name the setting, the values to try, the code to re-run, and
         what output has to be captured. You do not run it; the part chat does, because only it has the data.
     (c) A DELIBERATE EXCEPTION: one line saying why this block needs nothing (already taught, output-only,
         an explicitly labelled recap).
  4. For every chapter, list the settings that appear in code and never in prose. This list is the chapter's
     real gap. In Chapter 37, for example: random_state, stratify, test_size, cv, n_neighbors, alphas,
     handle_unknown, strategy, add_indicator.

WHAT A GOOD SETTINGS TABLE LOOKS LIKE (from section 6.5):

  | Setting | What it means in plain words | Value used here | What happens if you change it |
  |---|---|---|---|
  | `test_size=0.2` | share of rows held back to test the model | 0.2 (20%) | smaller: less reliable test; larger: less data to learn from |

  Then at least one changed version actually run, with the real output pasted. Asserted effects do not count.

RULES:
  - You do not edit any manuscript. You write patches; the part chats apply and re-verify them.
  - Write the patch text in the book's voice: American spelling, no em dashes in prose, no "just", "simply",
    "easy", "obviously", "powerful", "genuinely", "honestly", "straightforward".
  - Never invent an output. If a what-if needs a real run, say so and hand it to the part chat.
  - A block over 25 lines is not fixed by adding bullets. It is fixed by splitting it into steps.

OUTPUT: review/teaching-findings.md

  ## Summary
  - The five chapters where this matters most, and why.
  - The settings that recur across the book and deserve one canonical explanation, referenced afterwards.

  ## Per chapter
  ### Chapter NN
  - Blocks flagged: N of M. Blocks needing a patch: N. Exceptions: N.
  - Settings used but never explained: (list)
  - PATCHES: (each one written out in full, with the section it goes in)
  - WHAT-IFS TO RUN: (each with the setting, the values, and the output to capture)
  - EXCEPTIONS: (one line each)

  ## A proposed "Code words you met in this part" table for each part
  (section 6.5 asks for one per class A and B chapter; propose the per-part version too)

Send me Chapter 37 alone first, as a worked sample, before doing anything else. If that one is right,
the rest of the book follows the same shape.
```

### 7.3 The per-part commands

After the kickoff, each part is one short command. For Fable A, parts are read in reading order and never skipped. For Fable B, in the priority order above.

```
Fable A:  Continue the reading. Part <X>, chapters <N to M>, in reading order. Same method, same output
          format, append to review/journey-findings.md. Before you start, re-read your notes on the part
          before it: half of what you are looking for lives in the seam between two parts.

Fable B:  Part <X>, chapters <N to M>. Same method and output format, append to review/teaching-findings.md.
          Start with the chapter that has the highest ratio of flagged blocks to total blocks.
```

### 7.4 When Part VII and Part VIII arrive

Both pass into the same two chats with one added instruction each:

```
Fable A:  Part VII is Architecture, Governance and Leadership: chapters 60 to 67, written for a reader who has
          come all the way from Chapter 1. Check the hardest thing in this book: does a reader who started with
          no background arrive at Chapter 60 able to read it? Trace the ladder from Chapter 8's career tree to
          Chapter 67 and say where a rung is missing.

Fable B:  Part VIII is the Interview Playbook: chapters 68 to 82, fifteen question banks. Its standard is
          different. Every answer must be checkable against the chapter that taught it, and every code answer
          must be runnable. Audit for that, plus section 6.5 where the banks contain code.
```

---

## 8. What the coordinator does with the output

I merge the two findings files into **one work order per part**, so no part chat receives two overlapping lists. Each work order contains:

1. The S1 items, which are not optional.
2. The S2 items, grouped by cause rather than by chapter, because one cause usually produces several symptoms.
3. Fable B's patches for that part, ready to apply.
4. The what-ifs that need real runs, with the data each one needs.
5. The style sweep for that part, already measured.
6. The open cross-part issues that touch it.

Then the part chat runs §15.1 as written: read the part straight through, understand the cause, fix in place, re-verify, rebuild, report.

**Anything structural comes to you first.** If Fable A says Chapter 12 should be split in two, or that a bridging chapter is needed between Part II and Part III, that is your call and nothing moves until you make it.

---

## 9. Sequencing against the build

The pass and the build run at the same time. They only collide if a part chat is asked to repair a part while it is still writing one.

| When | Build | Review |
|---|---|---|
| Now | Part VII is written (Ch 60–67) | Fable A and Fable B start on Parts 0 to VI |
| Part VII approved | Part VIII begins (Ch 68–82) | Findings for Parts 0 to VI delivered; coordinator issues work orders |
| Part VIII in progress | Ch 25, 26, 27 fill the hole in Part II; Ch 83 and the appendices | Repair passes run in the part chats, oldest part first |
| All chapters written | — | Fable A reads the whole book once more, end to end, including VII and VIII |
| After that | Renumbering, assembly, the combined volumes | Final style and cross-reference sweep |

Parts 0 and I are repaired first, not last. They are the chapters a reader meets before deciding whether to keep going, and they are also the shortest, so the repair is cheap and the lesson from it informs the rest.

---

## 10. What "done" means for this pass

- Every S1 finding closed, by a fix or by a recorded decision from you.
- Every S2 finding closed or explicitly deferred with a reason.
- The first-appearance ledger has no used-before-explained rows left, or each remaining one carries a sentence in the text telling the reader where it is taught.
- Every class A and B chapter has its settings tables and at least one measured what-if.
- `planning/code-teaching-baseline.md` re-run, with the flag counts down and the settings-table column reading "yes" across the book.
- One reader can start at Chapter 1 with no background and reach Chapter 83, and another can open the book at Chapter 51 and find what they need.
