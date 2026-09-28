# Book structure (D8): stages, part numbers, navigation

Abhishek, 28 Sep 2026: the division and naming of the book's sections was confusing. He chose three
things, recorded as D8 in `DECISIONS.md`. This change applies them to the whole book, not only to
Parts 0 and 1, so every chapter reads the same way from now on.

## 1. Every chapter in six stages

| Stage | Sections, in this order |
|---|---|
| **Start** | Why this matters · In plain English |
| **Learn** | the numbered sections (1.1, 1.2 …) |
| **Apply** | Common mistakes · In the real world · Project (opens with *Tools you'll need*) · Timed challenge, where a chapter has one |
| **Review** | Recap · Key terms · Check yourself · Final-week revision list (Part 8) |
| **Practise** | Exercises · Answers |
| **Next** | Where this leads |

- **Before, the order wandered.**
  - Tools sat between the story and the project.
  - Key terms came after the exercises.
  - "Where this leads" sat between the exercises and their answers.
  - All 22 or so headings looked the same.
- **Now each stage's first heading carries a small label** (START, LEARN, APPLY …), so the reader can see where they are.
- **Headings renamed:**
  - "Common mistakes and how to spot them" → **Common mistakes**
  - "The project: …" → **Project: …**
  - "You've got it when…" → **Check yourself**
  - "Practice exercises" → **Exercises**
  - "Answers to practice exercises" → **Answers**
- **The separate Tools section moved, word for word, into the project** as *Tools you'll need*. The same tools are also listed in the chapter-at-a-glance box.
- **Done by `tools/restructure.py` on 83 chapters.** It moves whole sections, changes no other text, and a test confirmed every line of text survives.
- **Not moved:** Ch 67 ("Questions to sit with") and Ch 83 (three closing sections of its own). They are placed in their part builds.
- **Front section updated.** "How to Use This Book", *How each chapter is laid out*, now describes the six stages.

## 2. Parts numbered 0 to 8

- "Part II" → "Part 2", "Parts 0 and I" → "Parts 0 and 1", "Parts III to VII" → "Parts 3 to 7", and so on.
- **Done by `tools/part_numerals.py` on 385 lines**, covering chapters, parked text, figures and their scripts, companion files, the hours script and the builder's covers.
- **Not changed:** nothing inside code blocks or outputs (none named a part). Internal files keep the Roman numerals: the register, the review files and the branch names.
- **Figure 8.1** ("TIER 6 · PART 7") was redrawn from its script.

## 3. Navigation

- **"In this chapter" map.** It sits under every chapter's glance box and lists the six stages and each numbered section, with page numbers. A single-chapter PDF no longer needs a separate contents page.
- **Two-level contents** in part PDFs: parts, chapters, and each chapter's numbered sections, with page numbers.
- **One page count per part package.**
  - The Part 0 + 1 PDF is rendered as one document.
  - The contents and "How to Use This Book" are numbered i–vii; Part 0 starts at 1 and the count runs through Part 1.
  - Footers name the current part or chapter.
- **Not chosen:** dropping the full stop in "Chapter 1." titles.

## Builder changes (`tools/pdf/`)

- **`build.py`:**
  - `structure()` adds the stage labels, the chapter maps and the contents.
  - `page_numbers()` matches every heading to its PDF bookmark, so contents and maps get page numbers.
  - `build_package()` and `stamp_footers()` produce the part package with running footers.
  - A chapter not in stage order keeps a full contents page instead.
- **`book.css`:** styles for the stage labels, the chapter map, the two-level contents and part openings.
- **`layout.js`:**
  - A table taller than a quarter page may now split, with its header row repeated. Before, "Common mistakes" tables jumped to the next page and left half a page empty.
  - A list whose last item ends in ":" keeps that item with the table or code block it introduces.
- **`layout_check.py`:**
  - Reads each page's printed number from its footer, so roman numerals and running numbers are checked correctly.
  - Checks every chapter map entry as well as the contents.

## Checks

- **Part 0 + 1 PDF:** 93 of 93 contents entries and 128 of 128 map entries point to the right page. No stranded headings or lead-ins, no small text, no missing glyphs.
- **Two pages are still half empty (p. 144 and p. 170).** Figures 7.1 and 8.1 are taller than the space left on the page before them. They could shrink by only 7% before their text drops below 7 pt, which isn't enough, so they need redrawing more compactly. That is listed for Abhishek.
