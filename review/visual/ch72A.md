# Visual review — Ch72A-Data-Structures-and-Algorithms-Question-Bank.pdf (19 pages)
Verdict: A clean, consistently set question bank with no figures. Its code blocks are well set, with none clipped and indentation preserved. The serious problem is editorial text meant for the production team printed in the opening callout on p. 3 ("the coordinator should renumber it…", "this chat doesn't have Chapter 72's approved text"). The recurring layout faults are Q-IDs that break in the narrow "#" column of every rapid-fire table ("Q72A-" / "003") and one 41 %-blank page (p. 13).

Page numbers below are **PDF pages**. The printed folio ("n / 18") is PDF page − 1.

Automated checks:
- **Fonts:** all embedded. Lora 10.4 pt body (Type 3); Poppins headings; DejaVu Sans 8.3 pt tables; DejaVu Sans Mono 7.9 pt code (7.6 pt inline). Superscript "²" mixes Lora and DejaVu Sans on the same pages (4, 6), which is barely visible. No tofu.
- **Images / figures:** no raster images and no figures or diagrams in this chapter.
- **Text outside margins:** none detected by the pre-scan or by bbox.
- **Blank-area scan:** p. 2 (contents) 59 % blank; p. 13 41 %; p. 19 80 % (chapter end, 3 bullets).
- **Code-line overflow scan:** no mono line runs past x = 515 pt and no code line wraps to column 0.
- Every page was viewed on 3×2 contact sheets at 70 dpi, and every table, code block and the intro callout were zoomed at 150 dpi.

## Issues
| ID | Page(s) | Element | Issue | Sev | Change needed |
|---|---|---|---|---|---|
| V72A.1 | 3 | Intro callout, "A note on this chapter's numbering" and "Learn it in pointers" | Instructions to the production team are printed for readers: "as a placeholder; **the coordinator should renumber it into the main sequence at final assembly**" and "…at chapter level, since **this chat doesn't have Chapter 72's approved text** to check exact section numbers against." | High | Delete both passages. Resolve the chapter number and the Learn-it-in section references before print. |
| V72A.2 | 13 | Page foot, Q72A-027 | Heading Q72A-027, its "Remember it as" line, then 41 % of the page left blank. The BST code block starts on p. 14. | Medium | Let the code block split, or keep the heading with the code (move both to p. 14 and pull p. 14 text back). |
| V72A.3 | 5, 6, 8, 9, 10, 11, 12 | Rapid-fire tables, "#" column | The question ID breaks at its hyphen in every row: "Q72A-" / "003". Readers cite these IDs (the Final-week list uses them). | Medium | Widen the "#" column to about 16 mm, or set IDs to no-wrap (non-breaking hyphen U+2011). |
| V72A.4 | 1 | Cover | Reader-visible status label "Approved chapter · v1" and date "21 September 2026". Differs from the pilot chapters ("Draft chapter · v1"). | Medium | Remove from the print cover. |
| V72A.5 | 1 | Cover subtitle | The subtitle is truncated mid-list with an ellipsis: "…patterns that actually recur: hash maps,…". | Medium | Shorten the subtitle to fit, or allow more lines; never truncate. |
| V72A.6 | 2 | Contents | No page numbers. | Medium | Add page numbers. |
| V72A.7 | 5, 8, 9, 11 | Inline code pills | Pill padding adds a space before punctuation or inside brackets: "built-in `sort()` ?", "( `x in seen` )", "Verified, `n=28` :", "`heapq.nlargest(k, nums)[-1]` , or a". | Low | Remove outer pill margin, or set a zero-width join before punctuation. |
| V72A.8 | 8, 17 | Widows | The page opens with a one-line paragraph tail: "idea in pandas)." (p. 8) and "Learn it in: Chapter 72." (p. 17, above the next section). | Low | Widow/orphan control of 2 lines. |
| V72A.9 | 6, 12 | Rapid-fire tables | Tables split with only 1 row (p. 6, Q72A-006) or 2 rows (p. 12) on the next page. The header repeats correctly. | Low | Keep tables of 4 rows or fewer together. |
| V72A.10 | 10, 11 | Tier tables | Three-row Tier tables split, leaving only the "Extra points" row (under a repeated header) on the next page. | Low | Keep Tier tables unbroken. |
| V72A.11 | 4 | Table "The common orders" | The "5,000 items, roughly" column holds numbers ("~13 steps", "25,000,000 steps") but is left-aligned. | Low | Right-align the numeric column. |
| V72A.12 | 1 | Cover eyebrow | "ANALYST TO ARCHITECT · PART VIII — THE INTERVIEW" wraps, leaving "PLAYBOOK" alone on line 2. | Low | Shorten, or break after "·". |
| V72A.13 | 4–16 | Code blocks | Python input and its printed output use the same grey left rule and tint, so input and output are distinguished only by position. | Low | Use the dark-blue input rule (as SQL input has in Ch71/77) for Python input. |

## Patterns (things that repeat on many pages — describe once, list pages)
- **Q-ID wraps in the "#" column** of every rapid-fire table (pp. 5–12). The same pattern appears in all Part VIII banks.
- **Tier / rapid-fire tables split** with a repeated header but only 1–2 rows carried over (pp. 6, 10, 11, 12).
- **Code styling:** Python input and output are identical in style (see V72A.13). The code itself is well set: 7.9 pt, no overflow, "# verified" comments are consistent.
- **Folios** "n / 18", chapter-local; the running footer carries the correct chapter title on every page.
- There are no Watch out / Try it callouts. The only callouts are the blue intro box (p. 3) and the tier tables. Tier tables are styled consistently throughout.

## Snapshots
- snaps/V72A.1_p3.png — leaked coordinator / "this chat" notes in intro callout
- snaps/V72A.2_p13.png — 41 % blank page after Q72A-027 heading
- snaps/V72A.3_p5.png — "Q72A-/003" ID wraps in rapid-fire table
- snaps/V72A.4_p1.png — cover label and date
- snaps/V72A.5_p1.png — truncated cover subtitle
- snaps/V72A.6_p2.png — contents without page numbers
