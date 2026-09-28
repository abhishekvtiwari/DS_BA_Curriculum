"""Put a chapter's closing sections into the book's five-stage order (decision D8, 28 Sep 2026).

    python tools/restructure.py manuscript/ch01-*.md        # rewrite in place, report what moved
    python tools/restructure.py --check manuscript/ch*.md   # report only

Every chapter reads Start (Why this matters, In plain English), Learn (the numbered sections),
Apply, Review, Practise, Next. This script touches only the closing sections, which follow the
last numbered section:

    Apply     Common mistakes · In the real world · Project (with "Tools you'll need") · Timed challenge
    Review    Recap · Key terms · Check yourself · Final-week revision list
    Practise  Exercises · Answers
    Next      Where this leads

Three headings are renamed ("Common mistakes and how to spot them" -> "Common mistakes",
"You've got it when…" -> "Check yourself", "Practice exercises" -> "Exercises",
"Answers to practice exercises" -> "Answers", "The project: …" -> "Project: …"), and the old
"Tools" section moves, word for word, to the top of the project as "### Tools you'll need".
No other text changes. A chapter with a closing heading this script doesn't know is left alone.
"""
import re, sys, pathlib, glob

ORDER = [  # (match on the old or new heading, new heading, stage)
    (r"Common mistakes( and how to spot them)?$", 'Common mistakes', 'Apply'),
    (r"In the real world\b", None, 'Apply'),
    (r"Tools$", None, 'Apply'),
    (r"(The project|Project)\b", None, 'Apply'),
    (r"Timed challenge\b", None, 'Apply'),
    (r"Recap$", None, 'Review'),
    (r"Key terms$", None, 'Review'),
    (r"(You've got it when…|Check yourself)$", 'Check yourself', 'Review'),
    (r"Final-week revision list$", None, 'Review'),
    (r"(Practice exercises|Exercises)$", 'Exercises', 'Practise'),
    (r"(Answers to practice exercises|Answers)$", 'Answers', 'Practise'),
    (r"Where this leads$", None, 'Next'),
]
STAGES = {h: s for _, h, s in ORDER if h}


def slot(title):
    for i, (pat, _, _) in enumerate(ORDER):
        if re.match(pat, title):
            return i
    return None


def sections(md):
    """Split into the text before the first H2 and a list of [title, body] H2 sections (fences respected)."""
    lines, fence, cuts = md.split('\n'), False, []
    for i, l in enumerate(lines):
        if l.lstrip().startswith('```'):
            fence = not fence
        elif not fence and l.startswith('## '):
            cuts.append(i)
    if not cuts:
        return md, []
    head = '\n'.join(lines[:cuts[0]])
    secs = []
    for a, b in zip(cuts, cuts[1:] + [len(lines)]):
        secs.append([lines[a][3:].strip(), '\n'.join(lines[a + 1:b])])
    return head, secs


def strip_rule(body):
    """Body without its trailing blank lines and '---' separator."""
    return re.sub(r'(\s*\n---\s*)+\s*$', '', body.rstrip()).rstrip()


def restructure(md):
    head, secs = sections(md)
    first = next((i for i, (t, _) in enumerate(secs) if slot(t) is not None), None)
    if first is None:
        return md, 'no closing sections'
    tail = secs[first:]
    unknown = [t for t, _ in tail if slot(t) is None]
    if unknown:
        return md, 'left alone: unknown closing heading(s) %s' % unknown
    ruled = any(re.search(r'\n---\s*$', b.rstrip() + '\n') for _, b in secs)
    sep = '\n\n---\n\n' if ruled else '\n\n'
    tail = sorted(tail, key=lambda s: slot(s[0]))
    notes = []
    tools = next((s for s in tail if re.match(r'Tools$', s[0])), None)
    proj = next((s for s in tail if re.match(r'(The project|Project)\b', s[0])), None)
    if tools and proj:
        tail.remove(tools)
        body = strip_rule(proj[1]).lstrip('\n')
        block = "### Tools you'll need\n\n" + strip_rule(tools[1]).strip()
        m = re.match(r'(\*\*Goal:\*\*[^\n]*(?:\n(?!\n)[^\n]*)*)\n\n', body)   # after the Goal paragraph
        body = (m.group(1) + '\n\n' + block + '\n\n' + body[m.end():]) if m else (block + '\n\n' + body)
        proj[1] = '\n\n' + body
        notes.append('Tools folded into the project')
    for s in tail:
        new = next((h for p, h, _ in ORDER if h and re.match(p, s[0])), None)
        if new and s[0] != new:
            notes.append('%s -> %s' % (s[0], new)); s[0] = new
        m = re.match(r'The project(:.*)?$', s[0])
        if m:
            new = 'Project' + (m.group(1) or '')
            notes.append('%s -> %s' % (s[0], new)); s[0] = new
    before = secs[:first]
    out = head.rstrip('\n') + '\n\n' if head.strip() else ''
    parts = ['## %s\n\n%s' % (t, b.strip('\n')) for t, b in before]
    # the learn sections keep their own separators exactly as written
    body_before = '\n\n'.join(p.rstrip() for p in parts)
    if before and not re.search(r'\n---\s*$', body_before) and ruled:
        body_before = body_before + '\n\n---'
    closing = sep.join('## %s\n\n%s' % (t, strip_rule(b).strip('\n')) for t, b in tail)
    new_md = out + (body_before + '\n\n' if before else '') + closing + '\n'
    old_order = [t for t, _ in secs[first:]]
    if [t for t, _ in tail] != old_order or notes:
        notes.insert(0, 'order: ' + ' > '.join(t.split(':')[0] for t, _ in tail))
    return new_md, '; '.join(notes) or 'already in order'


if __name__ == '__main__':
    args = sys.argv[1:]
    check = '--check' in args
    for a in [x for x in args if x != '--check']:
        for f in sorted(glob.glob(a)):
            p = pathlib.Path(f)
            old = p.read_text(encoding='utf-8')
            new, note = restructure(old)
            if not check and new != old:
                p.write_text(new, encoding='utf-8')
            print('%-28s %s' % (p.name[:28], note[:160]))
