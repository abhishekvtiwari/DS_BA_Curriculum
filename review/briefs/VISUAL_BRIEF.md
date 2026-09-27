# Visual / layout review brief — "Analyst to Architect"

You are a senior book designer and technical editor. Review the PRINTED APPEARANCE of the PDF pages you're given: what a first-time reader sees on the page. Content correctness has already been reviewed separately; only note content issues that are visible on the page (e.g., a caption that doesn't match its figure, a figure number out of order, a heading that disagrees with the contents page).

## Tools available (Linux)
- `pdftoppm -r 110 -png -f N -l N file.pdf out` renders a page; `-r 200` plus ImageMagick `convert in.png -crop WxH+X+Y out.png` to zoom in on anything small (figure labels, table cells, code).
- `montage` (ImageMagick) to build contact sheets; view images with the Read tool.
- `pdftotext -layout -f N -l N`, `pdftotext -bbox-layout` (word boxes: detect text running past the margins or overlapping boxes), `pdffonts`, `pdfimages -list`, `pdfinfo`.
- python3 with PIL.

Look at EVERY page. Contact sheets (4 pages side by side) are fine for a first pass, but zoom into every figure, every table, every code block, and every page where something looks off. Don't guess from a thumbnail.

## What to check (and anything else a reader would notice)
1. **Figures/images/diagrams:** text too small to read at print size (below ~7 pt equivalent), labels overlapping each other or boxes, clipped/cut-off labels, arrows missing or pointing wrongly, low resolution/blurry, stretched aspect ratio, colour contrast too low, colours that can't be distinguished by colour-blind readers (red/green pairs), legends missing, axis labels missing or overlapping, figure crossing the margin, figure number/caption mismatch or out of sequence, caption separated from its figure on another page.
2. **Tables:** broken across pages without a repeated header row, rows split across pages, column too narrow causing mid-word or mid-token wraps (e.g., "--no-\nverify", "on-\neline"), text overflowing cells, misaligned numbers (numbers should be right-aligned), inconsistent table styles, tables wider than the text block.
3. **Text:** overlapping text, characters missing or shown as boxes/"?" (tofu), wrong glyphs (₹, Hindi, emoji, maths symbols), soft-hyphen artifacts, hyphenation of code or identifiers, widows/orphans (a single line at top/bottom of page), a heading stranded at the bottom of a page with its body on the next ("keep with next"), large unexplained blank areas (half-empty pages), inconsistent spacing between paragraphs, text running into margins/footers.
4. **Code blocks:** lines cut off at the right edge, wrapped mid-token without a continuation marker, block split across pages awkwardly (e.g., 1–2 lines on the next page), lost indentation, font too small, poor contrast of syntax colours, output blocks not visually distinct from input.
5. **Maths and money:** dollar amounts or formulas rendered as garbled math (e.g., "0.023perGB"), inconsistent formula styling, fractions/superscripts unreadable.
6. **Structure and consistency:** heading hierarchy and numbering consistent; contents page matches headings and has page numbers (flag if no page numbers); running header/footer and page numbering consistent and correct; chapter opener/cover pages consistent across chapters (and any "Draft", version or date labels visible to readers); callout boxes (Watch out, Try it, Simplification note, Real-life example, Interview extra point) styled consistently; lists and bullets consistent; exercises/answers formatting; page size and margins consistent; hyperlinks/cross-references visibly marked.
7. **Accessibility/print:** body text size and line length comfortable; light-grey text on white; reliance on colour alone; how the page would print in greyscale.
8. **Anything else** that looks unprofessional or confusing on the page.

## Output
One markdown file per chapter/PDF at the path given. Structure:

```
# Visual review — <file name> (<pages> pages)
Verdict: <2–3 sentences>
Automated checks: fonts (embedded? fallback fonts?), images (raster? resolution), text-outside-margin hits, other scans run.

## Issues
| ID | Page(s) | Element (figure/table/code/text/structure) | Issue | Sev | Change needed |
|---|---|---|---|---|---|
| V<ch>.1 | 6 | Table "The settings on git commit" | "--no-verify" wraps as "--no-/verify" | Low | Widen col 1 to ≥ 28 mm or set monospace cells to no-wrap |

## Patterns (things that repeat on many pages — describe once, list pages)
## Snapshots
- Save crops for every High and Medium issue as PNG in the snapshot folder given, named V<ch>.<n>_p<page>.png, and list them here.
```
Severity: **High** = content unreadable, missing, cut off, or misleading; **Medium** = clearly unprofessional or slows reading (broken tables, stranded headings, big blank areas, tiny figure text); **Low** = polish.

When finished, reply with the file path(s), issue counts by severity, and the top 3 findings (one line each).
