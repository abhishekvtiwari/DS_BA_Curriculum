"""Extract the Reader's Journey findings and emit them as candidate register rows,
mapped to the themes in DECISIONS.md. Nothing is added to tracker/register.csv.

Two formats appear in journey-findings.md:
  1. Parts 0 and I: table rows  | S1-1 | chapter | what the reader experiences | cause | fix | ... |
  2. Parts II-VII:  bold prose  **S1-10. Headline.** Body...
"""
import re, csv, collections, io, pathlib

SRC = pathlib.Path('review/reader-journey/journey-findings.md')
OUT_CSV = pathlib.Path('review/reader-journey/register-candidates.csv')
OUT_MD = pathlib.Path('review/reader-journey/register-candidates.md')

lines = SRC.read_text(encoding='utf-8').splitlines()

part_of, cur = [], '0-I'
for l in lines:
    m = re.match(r'^## Part ([0IVX]+(?:\s*and\s*[0IVX]+)?)', l, re.I)
    if m:
        cur = re.sub(r'\s+', ' ', m.group(1)).strip()
    part_of.append(cur)

ID = r'(S[1-4]-\d+)'
found = {}

# format 2: bold prose, separator '.' or an em/en dash
for i, l in enumerate(lines):
    m = re.match(r'^\*\*' + ID + r'\s*[.—–-]\s*(.+?)\*\*\s*(.*)$', l.strip())
    if not m:
        continue
    fid, headline, rest = m.group(1), m.group(2), m.group(3)
    body, j = rest, i + 1
    while j < len(lines) and lines[j].strip() and not re.match(r'^\s*(\*\*S[1-4]-|#|\|)', lines[j]):
        body += ' ' + lines[j].strip(); j += 1
    found[fid] = dict(fid=fid, part=part_of[i], headline=headline.strip(),
                      body=re.sub(r'\s+', ' ', body).strip(), fix='')

# format 1: table rows in Parts 0 and I
for i, l in enumerate(lines):
    if not l.startswith('|'):
        continue
    cells = [c.strip() for c in l.strip().strip('|').split('|')]
    if not cells:
        continue
    m = re.match(r'^' + ID, cells[0])
    if not m:
        continue
    fid = m.group(1)
    if fid in found:
        continue
    ch = cells[1] if len(cells) > 1 else ''
    exp = cells[2] if len(cells) > 2 else ''
    cause = cells[3] if len(cells) > 3 else ''
    fix = cells[4] if len(cells) > 4 else ''
    found[fid] = dict(fid=fid, part=part_of[i], headline=f'{ch}: {exp}'[:300],
                      body=(f'{exp} CAUSE: {cause}' if cause else exp), fix=fix)

def keyfn(f):
    a, b = f.split('-')
    return (a, int(b))

items = [found[k] for k in sorted(found, key=keyfn)]
SEV = {'S1': 'High', 'S2': 'High', 'S3': 'Medium', 'S4': 'Low'}

THEME = [
 ('T7',  r'\b(Error|Traceback|Exception)\b|prints an|printed output|prints a'),
 ('T8',  r'cross-ref|points (to|at)|no such (chapter|section)|misattribut|stale title|wrong chapter|near-miss|citation|pointer'),
 ('T9',  r'renumber|Part VIII|question bank|72A|76A|76B|appendices'),
 ('T10', r'Riverstone|Meera|Anita|Vikram|Farah|Imran|calendar|timeline|hourly rate|revenue|dataset|universe|org chart|₹'),
 ('T11', r'Appendix G|this chat|coordinator|blueprint|first edition|leftover|author.s (voice|run date)|training data'),
 ('T12', r'Time needed|hours'),
 ('T13', r'price|salary|\blaw\b|regulation|landscape|model name'),
 ('T14', r'simulated|invented|stand-in|constructed teaching example'),
 ('T5',  r'never (taught|defined|explained)|before .{0,25}defin|first-appearance|ledger|undefined'),
 ('T3',  r'one idea per cell|split .{0,20}block|too many|wall by itself'),
 ('T6',  r'companion|not shown|hidden'),
 ('T2',  r'install|set up|setup'),
 ('T1',  r'sequence|before the section that teaches|reading order'),
 ('V4',  r'\bfigure\b|caption|fig\d'),
 ('V10', r'\btable\b'),
]

rows, unmapped = [], 0
for n, f in enumerate(items, 1):
    blob = f['headline'] + ' ' + f['body']
    hits = [c for c, p in THEME if re.search(p, blob, re.I)]
    if not hits:
        unmapped += 1
    chs = sorted({c.lower() for c in re.findall(r'Ch(?:apter)?\s*(\d+[aAbB]?)', blob)},
                 key=lambda x: (len(x), x))
    rows.append(dict(
        seq=n, part=f['part'],
        chapter=(', '.join(chs[:6]) if chs else 'All'),
        finding_id='RJ-' + f['fid'],
        kind='reader-journey',
        severity=SEV.get(f['fid'].split('-')[0], 'Medium'),
        test="Reader's Journey",
        where=f['part'],
        issue=re.sub(r'\s+', ' ', f['headline'] + '. ' + f['body'])[:1500],
        change_needed=(f['fix'] or 'See review/reader-journey/journey-findings.md for the cause and the smallest fix')[:600],
        status='Open', decision_source='', fixed_in='',
        notes=('candidate theme: ' + '/'.join(hits)) if hits else 'no theme matched; needs reading',
    ))

FIELDS = ['seq','part','chapter','finding_id','kind','severity','test','where','issue',
          'change_needed','status','decision_source','fixed_in','notes']
with OUT_CSV.open('w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)

by_sev = collections.Counter(r['severity'] for r in rows)
by_theme = collections.Counter()
for r in rows:
    if r['notes'].startswith('candidate theme: '):
        for t in r['notes'].split(': ', 1)[1].split('/'):
            by_theme[t] += 1
    else:
        by_theme['(none)'] += 1

o = io.StringIO(); w = o.write
w("# Reader's Journey findings as candidate register rows\n\n")
w("`register-candidates.csv` holds every numbered finding from `journey-findings.md` in the same\n")
w("schema as `tracker/register.csv`, ready to append if you decide to merge the strand.\n")
w("**Nothing has been added to the register.** Every row is `Open` with an empty `decision_source`,\n")
w("and `kind` is `reader-journey` so these can never be confused with the 2,534 content or 1,224\n")
w("visual rows.\n\n")
w(f"Extracted **{len(rows)} findings**: {by_sev.get('High',0)} High, {by_sev.get('Medium',0)} Medium, ")
w(f"{by_sev.get('Low',0)} Low. S1 and S2 map to High, S3 to Medium, S4 to Low.\n\n")
w("The 25 structural questions are deliberately not here. They are questions for you, not fixes,\n")
w("and they belong next to sections C and D of `DECISIONS.md`.\n\n")
w("## Candidate theme, by keyword\n\nApproximate. A finding can match several themes, so these do not sum to the total.\n\n")
w("| Theme | Candidate rows |\n|---|---:|\n")
for t, c in by_theme.most_common():
    w(f"| {t} | {c} |\n")
w(f"\n{unmapped} matched no theme and need reading.\n\n")
w("## Per part\n\n| Part | Findings |\n|---|---:|\n")
for p, c in sorted(collections.Counter(r['part'] for r in rows).items()):
    w(f"| {p} | {c} |\n")
w("\n## Every High finding\n\n")
for r in rows:
    if r['severity'] == 'High':
        w(f"- **{r['finding_id']}** (Ch {r['chapter']}): {r['issue'][:230]}\n")
OUT_MD.write_text(o.getvalue(), encoding='utf-8')
print(f"wrote {len(rows)} candidate rows; unmapped {unmapped}")
print("severity:", dict(by_sev))
print("per part:", dict(collections.Counter(r['part'] for r in rows)))
missing = [f'S{a}-{b}' for a, hi in (('1',24),('2',29),('3',78)) for b in range(1, hi+1)
           if f'S{a}-{b}' not in found]
print(f"IDs in range but not extracted ({len(missing)}):", missing[:20])
