"""Build DECISIONS-BRIEFING.md: per-theme row counts and examples, so DECISIONS.md can be
filled quickly. Mapping is keyword-based and approximate, by design: CLAUDE.md asks the agent
to map each row to its theme by reading the issue text. This is triage, not the mapping."""
import csv, collections, re, sys, io

REG = 'tracker/register.csv'
OUT = 'DECISIONS-BRIEFING.md'

THEMES = [
 ("T1", "Code shown before it is taught (sequence rule)",
  lambda r: 'sequence' in r['test'].lower() and re.search(r'\bcode|snippet|function|library|import\b', r['issue'], re.I)),
 ("T2", "Tools and libraries never installed",
  lambda r: re.search(r'\binstall|pip |conda|never set up|no setup|venv\b', r['issue'], re.I)),
 ("T3", "Big code blocks with many new ideas",
  lambda r: re.search(r'block.{0,40}(new|idea|long|split)|many new ideas|one idea per cell|split .{0,20}block', r['issue'], re.I)),
 ("T4", "No by-hand example before the method",
  lambda r: 'by-hand' in r['test'].lower() or re.search(r'by hand|worked by hand|no hand example', r['issue'], re.I)),
 ("T5", "Foundations the book never teaches",
  lambda r: re.search(r'\bnever (taught|defined|explained|introduced)|undefined term|chain rule|logarithm|\bregex\b|\bYAML\b|\bclasses?\b.{0,30}never', r['issue'], re.I)),
 ("T6", "Hidden companion code / black-box outputs",
  lambda r: re.search(r'companion|black.?box|not shown on the page|hidden code|off.?page', r['issue'], re.I)),
 ("T7", "Printed outputs that are errors",
  lambda r: re.search(r'\b(Error|Traceback|Exception)\b', r['issue'])),
 ("T8", "Wrong chapter/section cross-references",
  lambda r: re.search(r'cross.?ref|xref', r['test'], re.I) or re.search(r'points to Chapter|wrong chapter|no such (chapter|section)|refers to Chapter', r['issue'], re.I)),
 ("T9", "Part VIII pointers and numbering",
  lambda r: re.search(r'renumber|question code|stable code|points to (a )?(teaching|chapter)|no teaching section|72A|76A|76B', r['issue'], re.I)),
 ("T10", "Riverstone facts that disagree",
  lambda r: re.search(r'Riverstone|Meera|Anita|Vikram|Farah|hourly rate|timeline|revenue|₹', r['issue'])),
 ("T11", "Drafting and authoring leftovers",
  lambda r: re.search(r'Appendix G|this chat|coordinator|blueprint|first edition|draft badge|build script', r['issue'], re.I)),
 ("T12", "Time needed estimates too low",
  lambda r: re.search(r'Time needed|hours?\b.{0,25}(low|under|estimate)|re-?estimate', r['issue'], re.I)),
 ("T13", "Claims needing outside verification",
  lambda r: re.search(r'price|salary|\blaw\b|GDPR|DPDP|AI Act|regulation|vendor|cost per', r['issue'], re.I)),
 ("T14", "Integrity of examples and advice",
  lambda r: re.search(r'simulated|invented|fabricat|made up|advice|portfolio claim', r['issue'], re.I)),
 ("V1", "Covers: draft/approval badges, versions, dates",
  lambda r: re.search(r'cover', r['issue'], re.I) and re.search(r'badge|draft|version|approved|date', r['issue'], re.I)),
 ("V2", "Contents pages: add page numbers",
  lambda r: re.search(r'contents', r['issue'], re.I)),
 ("V3", "Figure text under 7 pt",
  lambda r: re.search(r'\b[0-6](\.\d)?\s?pt\b|text too small|tiny text|under 7', r['issue'], re.I)),
 ("V4", "Figures contradicting the text or overlapping",
  lambda r: re.search(r'figure', r['issue'], re.I) and re.search(r'overlap|contradict|clip|collide|cut off', r['issue'], re.I)),
 ("V5", "Figures out of number order",
  lambda r: re.search(r'figure.{0,30}(order|numbered|out of sequence)|Figure \d+\.\d+ appears', r['issue'], re.I)),
 ("V6", "Colour-only meaning",
  lambda r: re.search(r'colour|color', r['issue'], re.I) and re.search(r'only|greyscale|grayscale|legend', r['issue'], re.I)),
 ("V7", "Page breaks, stranded headings and lead-ins",
  lambda r: re.search(r'page break|stranded|orphan|widow|half.?empty|split across pages|heading at the bottom', r['issue'], re.I)),
 ("V8", "Code lines wrapping badly",
  lambda r: re.search(r'wrap', r['issue'], re.I) and re.search(r'code|line|continuation', r['issue'], re.I)),
 ("V9", "Two-digit list numbers clipped",
  lambda r: re.search(r'list number|two.?digit|indent', r['issue'], re.I)),
 ("V10", "Tables: wraps, alignment, white-on-white",
  lambda r: re.search(r'table', r['issue'], re.I)),
 ("V11", "Rendering: $, formulas, markdown, the rupee glyph",
  lambda r: re.search(r'\$|formula|LaTeX|renders? as|literal markdown|glyph|₹.{0,20}(missing|box)', r['issue'])),
 ("V12", "Scale and resolution",
  lambda r: re.search(r'resolution|ppi|dpi|screenshot|\b2×|\b100%|blurry|raster', r['issue'], re.I)),
]

rows = list(csv.DictReader(open(REG, newline='', encoding='utf-8')))
assign = collections.defaultdict(list)
for r in rows:
    hit = False
    for code, _, test in THEMES:
        try:
            if test(r):
                assign[code].append(r); hit = True
        except Exception:
            pass
    if not hit:
        assign['(unmatched)'].append(r)

def sev(rs):
    c = collections.Counter(x['severity'] for x in rs)
    return f"{c.get('High',0)} / {c.get('Medium',0)} / {c.get('Low',0)}"

o = io.StringIO()
w = o.write
w("# Briefing for `DECISIONS.md`\n\n")
w("A triage aid, so section B can be filled without reading 3,758 rows. For each theme: roughly how\n")
w("many rows look like it, the High / Medium / Low split, and two real examples.\n\n")
w("**These counts are approximate.** They come from keyword-matching the `issue` text, and a row can\n")
w("match more than one theme, so the numbers do not sum to 3,758. `CLAUDE.md` section 4 still requires\n")
w("the agent to map each row to its theme by reading it, and to leave a row `Open` when the fit is\n")
w("unclear. Use this to decide *which themes to approve*, not as the mapping itself.\n\n")
w(f"Register: **{len(rows)} rows**, {sum(1 for r in rows if r['severity']=='High')} High, ")
w(f"{sum(1 for r in rows if r['severity']=='Medium')} Medium, {sum(1 for r in rows if r['severity']=='Low')} Low. ")
w(f"{sum(1 for r in rows if r['status']=='Approved')} already Approved.\n\n")
w("| Theme | What it covers | Rows | H / M / L |\n|---|---|---:|---|\n")
for code, desc, _ in THEMES:
    rs = assign.get(code, [])
    w(f"| **{code}** | {desc} | {len(rs)} | {sev(rs)} |\n")
w(f"| *(unmatched)* | Matched no theme by keyword; needs reading | {len(assign['(unmatched)'])} | {sev(assign['(unmatched)'])} |\n")
w("\n---\n\n## Examples per theme\n\n")
for code, desc, _ in THEMES:
    rs = assign.get(code, [])
    w(f"### {code} — {desc}\n\n")
    w(f"Roughly **{len(rs)} rows** ({sev(rs)} High/Medium/Low).\n\n")
    if not rs:
        w("_No rows matched by keyword. Either the theme is already clean, or its wording does not appear in the issue text._\n\n")
        continue
    hi = [r for r in rs if r['severity'] == 'High'] or rs
    for r in hi[:2]:
        issue = re.sub(r'\s+', ' ', r['issue'])[:260]
        w(f"- **{r['finding_id']}**, Ch {r['chapter']} ({r['severity']}, {r['test']}): {issue}\n")
    w("\n")
open(OUT, 'w', encoding='utf-8').write(o.getvalue())
print(f"wrote {OUT}: {len(o.getvalue()):,} bytes")
print(f"unmatched rows: {len(assign['(unmatched)'])} of {len(rows)}")
for code, _, _ in THEMES:
    print(f"  {code:<5} {len(assign.get(code,[])):>5}")
