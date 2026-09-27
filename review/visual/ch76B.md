# Visual review — Ch76B-Business-Analyst-Question-Bank.pdf (17 pages)
Verdict: The typography is consistent and there is no code. Three problems stand out:
- The sourcing note on p. 3 is drafting commentary ("not yet written at the time of this draft … Flagged clearly for a re-check once Chapter 25 is drafted").
- The chapter is titled 76B, but its sections are numbered 76.1–76.8 and its questions Q76-001…038, so it cannot be told apart from a "Chapter 76".
- The swimlane worked example is printed as one run-on paragraph, which defeats the point of a swimlane.

Page numbers below are **PDF pages**. The printed folio ("n / 16") is PDF page − 1.

Automated checks:
- **Fonts:** all embedded (Lora, Poppins, DejaVu Sans). "→" falls back to DejaVu Serif / Sans in the swimlane callout (p. 9). "₹" is in DejaVu Sans in a table (p. 5). No tofu.
- **Images / figures:** none. There is no swimlane or process diagram; see V76B.3.
- **Text outside margins:** none.
- **Blank-area scan:** p. 2 61 %; p. 8 17 %; p. 12 22 %; p. 17 63 % (chapter end).
- Every page was viewed, and all tables and callouts were zoomed at 150 dpi.

## Issues
| ID | Page(s) | Element | Issue | Sev | Change needed |
|---|---|---|---|---|---|
| V76B.1 | 3 | Intro callout, "A note on sourcing" | The note reads: "Chapter 25 … **not yet written at the time of this draft** … Flagged clearly for a re-check once Chapter 25 is drafted…" It is internal status text printed for readers. | High | Delete the note. Replace "chapter-level" pointers with real section numbers. |
| V76B.2 | 2–17 | Section and question numbering | The chapter title is "76B", but the Contents and headings read 76.1–76.8, the rapid-fire headings read "Rapid-fire, 76.1", and the IDs read Q76-001…Q76-038. Ch76A uses 76A.x / Q76A-xxx, so a cross-reference to "Q76-001" or "§76.4" (as in Ch76A and Ch78) doesn't say which chapter it means. | Medium | Renumber to 76B.x / Q76B-xxx, or drop the letter from the title if the chapter becomes 76/77. |
| V76B.3 | 9 | Worked example "order-to-cash, swimlane by role" | The four lanes run together in one justified paragraph ("…enters order in CRM **Warehouse lane:** receives order → …"). There are no line breaks and no diagram, so the lanes and handoffs (the point of Q76-018) are not visible. | Medium | Set one line per lane (a 2-column "Lane / Steps" table), or draw a simple swimlane figure. |
| V76B.4 | 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 | Rapid-fire "#" column | IDs break as "Q76-" / "003". | Medium | Widen the column, or set IDs no-wrap. |
| V76B.5 | 1 | Cover | "Approved chapter · v1" and "21 September 2026" are visible. | Medium | Remove for print. |
| V76B.6 | 2 | Contents | No page numbers. | Medium | Add page numbers. |
| V76B.7 | 8→9 | Lead-in | "Worked example, order-to-cash, swimlane by role:" ends p. 8 above a 17 % gap. The callout is on p. 9. | Low | Keep with next. |
| V76B.8 | 3→4 | Lead-in | "Worked example, a real elicitation dialogue:" ends p. 3. The dialogue starts p. 4. | Low | Keep with next. |
| V76B.9 | 16→17 | Key terms | The key-terms paragraph splits, with one line ("as-is vs. to-be · gap analysis · … UAT sign-off") at the top of p. 17. | Low | Widow control. |
| V76B.10 | 5, 6, 8, 9, 10, 12, 14 | Tier / rapid-fire tables | Split with 1–2 rows under a repeated header. | Low | Keep short tables together. |
| V76B.11 | 1 | Cover eyebrow | "PLAYBOOK" is orphaned. | Low | Rebalance. |

## Patterns (things that repeat on many pages — describe once, list pages)
- **Numbering without the "B"** throughout (V76B.2). This also affects inbound references in Ch76A (pp. 9, 10) and Ch78 (pp. 11, 14).
- **Q-ID wraps** in every rapid-fire table.
- **Worked-example callouts** (dialogue, user story with Given/When/Then bullets, gap analysis) use one consistent light-blue style. The user-story callout on p. 6 is well structured, which makes the flat swimlane on p. 9 stand out.
- **Folios** "n / 16"; the footer title "Chapter 76B" is correct.

## Snapshots
- snaps/V76B.1_p3.png — "not yet written at the time of this draft" note
- snaps/V76B.2_p2.png — contents showing 76.x numbering under a 76B title
- snaps/V76B.3_p9.png — swimlane run-on paragraph
- snaps/V76B.4_p5.png — "Q76-/00x" ID wraps
- snaps/V76B.5_p1.png — cover label
- snaps/V76B.6_p2.png — contents without page numbers
