# Visual review — Ch76A-Data-Analyst-and-Data-Scientist-Question-Bank.pdf (14 pages)
Verdict: A narrative-heavy bank with no code or figures, and consistent callouts and tables. The opening callout tells readers the chapter number is "a placeholder for the coordinator to renumber at final assembly". That is a production note and must not print. The ID scheme is also muddled: this chapter uses "Q76A-", has an odd "Q76A-012B", and cites 76B's questions as "Q76-001".

Page numbers below are **PDF pages**. The printed folio ("n / 13") is PDF page − 1.

Automated checks:
- **Fonts:** all embedded (Lora, Poppins, DejaVu Sans). There is no monospace text in this chapter. No tofu, and no special-glyph fallbacks found.
- **Images / figures:** none.
- **Text outside margins:** none.
- **Blank-area scan:** p. 2 65 %; p. 6 26 %; p. 14 82 % (chapter end, 3 bullets).
- Every page was viewed, and all tables and callouts were zoomed at 150 dpi.

## Issues
| ID | Page(s) | Element | Issue | Sev | Change needed |
|---|---|---|---|---|---|
| V76A.1 | 3 | Intro callout, "A note on this chapter's numbering" | The callout reads: "It's numbered **76A**, a placeholder for the coordinator to renumber at final assembly, exactly the convention already established for Chapter 72A." This production instruction is printed for readers. | High | Delete the note. Fix the final chapter number. |
| V76A.2 | 5, 6, 8, 9, 10, 11 | Rapid-fire "#" column | The longer "Q76A-" prefix breaks on every row ("Q76A-" / "003"). | Medium | Widen the column, or set IDs no-wrap. |
| V76A.3 | 1 | Cover | "Approved chapter · v1" and "21 September 2026" are visible. | Medium | Remove for print. |
| V76A.4 | 1 | Cover subtitle | Truncated: "…at the right level of depth for each role · handle the…". | Medium | Shorten to fit. |
| V76A.5 | 2 | Contents | No page numbers. | Medium | Add page numbers. |
| V76A.6 | 8 | Rapid-fire 76A.3 | The first row's ID is "Q76A-012B", the only lettered sub-ID in the part. It wraps as "Q76A-" / "012B". | Low | Renumber sequentially. |
| V76A.7 | 9, 10 | Cross-references | This chapter cites "Chapter 76B, Q76-001" and "Q76-033". Those IDs follow 76B's un-suffixed scheme (see V76B.2), while this chapter's own IDs carry the letter. Readers see two different conventions side by side. | Low | Align both chapters on one ID scheme. |
| V76A.8 | 10 | Widow | The page opens with a single word, "claim.", the tail of the p. 9 answer. | Low | Widow control (2 lines). |
| V76A.9 | 6→7 | Page break before 76A.3 | 26 % blank at the foot of p. 6. Section 76A.3 starts a fresh page, though no other section in the chapter does. | Low | Let the section start in the remaining space. |
| V76A.10 | 4, 6, 9 | Tier tables | Split so that only the "Extra points" row appears on the next page under a repeated header. | Low | Keep together. |
| V76A.11 | 1 | Cover eyebrow | "PLAYBOOK" is orphaned on line 2. | Low | Rebalance. |

## Patterns (things that repeat on many pages — describe once, list pages)
- **Q-ID wraps**, worse here because of the 5-character prefix "Q76A-".
- **Worked-example callouts** (light blue, dark rule) are consistent on pp. 4, 5, 7, 8, 10, 11.
- **Folios** "n / 13"; the footer is correct.

## Snapshots
- snaps/V76A.1_p3.png — "placeholder for the coordinator to renumber"
- snaps/V76A.2_p5.png — "Q76A-/00x" ID wraps
- snaps/V76A.3_p1.png — cover label
- snaps/V76A.4_p1.png — truncated cover subtitle
- snaps/V76A.5_p2.png — contents without page numbers
