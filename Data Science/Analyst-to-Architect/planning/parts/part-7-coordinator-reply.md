# Coordinator reply to the Part VII chat — 20 September 2026

*Paste this into the chat that wrote Part VII (the Part II chat).*

Part VII is received and merged: eight chapters, about 61,900 words, 32 figures, eight approved PDFs. All 32 figure references resolve, every companion file named in the chapters is present, and **Part VII is complete**. With it, the book's narrative arc from Chapter 1 to the architect's chair exists end to end. That is worth saying before anything else.

Two things need fixing, and one of them matters more than its size suggests.

## 1. Chapter 67 is not the final chapter of the book

Chapter 67 says it is, five times: in *Before you start* ("this is the last chapter of the book"), twice in the body ("here, at the end of the book"), in *Where this leads* ("There is no next chapter"), and in its closing line ("sixty-seven chapters of practice"). It also describes Part VIII as "the Question Banks in the appendices (Chapters 70 through 79)".

The chapter map says otherwise:

| What Chapter 67 says | What the map says |
|---|---|
| The book ends at Chapter 67 | **Chapter 83, The Long Game**, is the closing chapter |
| Part VIII is "the appendices" | Part VIII is **Chapters 68–82**, fifteen question banks. The appendices are **A to H** |
| The banks are "Chapters 70 through 79" | They are **68 to 82**. The Architecture & Leadership bank, the one this chapter feeds, is **Chapter 80** |
| — | Appendix A, the Glossary, which the chapter cites, is correct |

I am not asking you to change what Chapter 67 *is*. It is the last chapter of the path, and its ending earns the weight it carries. What has to change is that it stops closing a book that has twenty-six chapters and eight appendices still to come, and instead hands off: to Part VIII's banks, naming Chapter 80 for its own subject, and to Chapter 83.

Five sentences. No content moves. It is logged as cross-part issue 20, and if the author would rather drop Chapter 83 and let 67 close the book, that is his call and I have put it to him that way.

## 2. The style drift, and where it actually comes from

Part VII carries **773 em dashes in prose** and **93 uses of *genuinely* or *honestly***, plus four American-spelling fixes. Instructions §5.2 bans all of these.

| Ch | Em dashes in prose | *genuinely* / *honestly* | Spelling |
|---|---|---|---|
| 60 | 87 | 9 | — |
| 61 | 93 | 6 | — |
| 62 | 120 | 11 | `modelling`, `optimis…` |
| 63 | 117 | 13 | — |
| 64 | 107 | 8 | — |
| 65 | 92 | 13 | `centre`, `modelling`, `optimis…` |
| 66 | 80 | 25 | `labelled`, `optimis…` |
| 67 | 77 | 8 | `optimis…` |

My scan excludes code blocks, tables, figure captions and the part line, so these are all in running prose. The status file records the scans as clean, which means the scan being run is not catching them.

Here is the part worth acting on rather than apologising for: **this is one chat's scan, not eight chapters' writing.** Part II's Chapters 23 and 24, written in this same chat, carry 53 and 84 em dashes. Every other part in the book is between zero and fifteen. Part VI managed zero across 66,400 words. So the fix is not eight chapters of penance; it is one scan, run properly, over all ten of this chat's chapters at once.

Two things to get right when you do it. Replace each em dash with the punctuation the sentence actually needs, which is usually a comma, sometimes a colon, sometimes a full stop, and occasionally parentheses. A blind search and replace will produce worse prose than the em dashes did. And *honestly* appears in section headings as well as sentences, for example "66.2 Maturity models, scored honestly": those need rewording, not deleting.

It is cross-part issue 21, and it supersedes issue 15.

## Accepted

**Chapter 67's departure from the exercises format is approved.** You asked for coordinator sign-off. A chapter whose own project says "there is no answer key" should not carry a drill section, and "Questions to sit with" is the right substitute. Two conditions: keep the *Key terms* list and the recap, which you have, and add one sentence saying why this chapter's format differs, so a reader who has done sixty-six exercise sets does not think something is missing.

**The Part V and Part VI decisions you carried in** are canon and are already in the bible: Dagster as the orchestrator, AWS `ap-south-1`, Delta Lake for the sensor table, plain SQL tests for quality.

**Part VII is almost code-free by design** — seven code blocks in the whole part — so §6.5 barely applies here, and the three flagged blocks are a small job. That is the correct shape for architecture and leadership chapters, not an omission.

## The review pass

Part VII is complete, so §15.1 applies, and for this chat it covers **both** its parts: Part II (Chapters 10–24, plus 25, 26 and 27 when they are written) and Part VII. Run the style scan across all of them in one pass, as above. The other inputs are `planning/code-teaching-baseline.md` for Part II's 148 flagged blocks, and cross-part issues 3, 4, 14, 20 and 21.

One more thing that belongs to you: **Chapters 25, 26 and 27 are still unwritten**, and they are the only hole left in the book's teaching spine. Part VIII cannot honestly claim to cover the analyst track until Chapter 25 exists.
