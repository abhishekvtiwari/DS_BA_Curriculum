# The books

The whole of *Analyst to Architect*, bound as books rather than parts. Rebuild them with
`python tools/pdf/books.py` from `Data Science/Analyst-to-Architect/`, as described in `source/BUILD.md`.

| File | What it is |
|---|---|
| `Analyst-to-Architect-Volume-1-From-Zero-to-Job-Ready.pdf` | The main book, Volume 1: How to Use This Book, then Part 0 (First Principles), Part 1 (The Map) and Part 2 (The Analyst). This volume covers the job-ready path. |
| `Analyst-to-Architect-Volume-2-From-Analyst-to-Architect.pdf` | The main book, Volume 2: Parts 3 to 7, then the closing chapter, The Long Game. Its page numbers continue from Volume 1. |
| `The-Interview-Playbook.pdf` | Part 8 as its own book: how data hiring works, the extra-points method, the question banks, take-home assignments and mock interviews. |
| `Analyst-to-Architect-Book-Overview.pdf` | Internal. Covers every part and chapter: the skills it covers, the time it needs, what it builds on, and its sections. It also has a figure of how the parts flow, the reading order, and the routes by role from Chapter 8. It is generated from the chapters by `tools/make_overview.py`. |

How the books are laid out:

- **Cover:** each book has its own.
- **"The whole book":** both volumes open with this map. It lists every part and chapter with its volume and
  page.
- **Contents:** each volume has its own, listing every chapter's numbered sections with their page numbers.
- **Parts:** every part starts with an opening page listing its chapters and their time needed.
- **Chapters:** every chapter starts on a new page. It opens with a "Chapter at a glance" box: what you will
  learn, what to read first, the time needed and the tools. A chapter map follows the box, showing the six
  stages (Start, Learn, Apply, Review, Practise, Next) with page numbers.
- **Footers:** the running footer names the part or chapter.

The main book is in two volumes because as one file it would be about 150 MB, over GitHub's 100 MB limit.
The split falls at the job-ready line, the end of Part 2.
