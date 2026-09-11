#!/usr/bin/env python3
"""Measurable content gates for controlled theory chapters (ISS-010).

Replaces the chapter self-audit, which verified heading presence only and
therefore certified template output as complete (ISS-009).

Every gate measures content that a generator cannot satisfy by emitting
headings. Usage:

    python tools/content_gates.py production/drafts/BA-M02/BA-M02-C01.md
    python tools/content_gates.py --all --quiet
    python tools/content_gates.py <new chapter> --strict

Gates carry a severity. BLOCKING gates are failed by 0 of the 10 BA-M01/BA-M02
benchmark chapters, so a failure is a regression and sets the exit code.
ADVISORY gates are failed by the benchmark too; they report a standard the
repository has never met and do not set the exit code unless --strict is given.

Exit code 0 = no blocking failure. 1 = at least one blocking failure, or any
failure when --strict is used. Use --strict for rebuilt and new chapters.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

CORPUS = 'production/drafts/BA-M*/BA-M*-C*.md'
CONTRACTS = 'contracts/business-analyst/BA-M*-contract.json'
CHAPTER_FILE = re.compile(r'^BA-M\d+-C\d+\.md$')

# Chapter subjects that imply executable or notational content must be shown.
NOTATION = {
    'sql': r'\bSELECT\b',
    'python': r'\b(import |def |pd\.)',
    'spreadsheet': r'=[A-Z]+\(',
    'excel': r'=[A-Z]+\(',
    'bpmn': r'```',
    'visualization': r'```',
}
ACRONYMS = ['bpmn', 'sql', 'uat', 'kpi', 'dmaic', 'scrum', 'kanban', 'python',
            'npv', 'roi', 'tco']


def paragraphs(text):
    return [p.strip() for p in text.split('\n\n')
            if p.strip() and not p.strip().startswith(('#', '|', '**', '>'))]


def topic_ids(text):
    return sorted(set(re.findall(r'BA-\d+-C\d+-T\d+', text)))


def topic_names(text):
    """The chapter's own topic labels, e.g. 'risk identification', 'joins'."""
    return sorted(set(n.strip() for n in
                      re.findall(r'^#{2,3} BA-\d+-C\d+-T\d+ - (.+?)\s*$', text, re.M)),
                  key=len, reverse=True)


def skeletons(text):
    """Body paragraphs with the chapter's own topic names masked out.

    Template substitution ("Apply <topic> by documenting...") evades exact
    matching. Masking the substituted token exposes the shared skeleton, which
    is the defect measured in ISS-009.
    """
    names = topic_names(text)
    out = []
    for p in paragraphs(text):
        for n in names:
            if n:
                p = re.sub(r'\b%s\b' % re.escape(n), '<T>', p, flags=re.I)
        out.append(p)
    return out


def contract_titles():
    out = {}
    for cf in glob.glob(CONTRACTS):
        mid = re.search(r'(BA-M\d+)', cf).group(1)
        try:
            c = json.load(open(cf, encoding='utf-8'))
        except Exception:
            continue
        title = c.get('module_title') or c.get('title')
        if title:
            out[mid] = title
    return out


def gate_distinct_paragraphs(text, **_):
    """G1 - at least 90 percent of body paragraphs must be distinct.

    Measured after masking the chapter's own topic names, so that paragraphs
    differing only by a substituted token count as one.
    """
    ps = skeletons(text)
    if not ps:
        return False, 'no body paragraphs'
    ratio = len(set(ps)) / len(ps)
    return ratio >= 0.90, ('distinct paragraph ratio %.2f after masking topic names '
                           '(need >= 0.90)' % ratio)


def gate_no_template_body(text, **_):
    """G2 - no single paragraph skeleton may fill more than 15 percent of the body."""
    ps = skeletons(text)
    if not ps:
        return False, 'no body paragraphs'
    _, n = collections.Counter(ps).most_common(1)[0]
    share = n / len(ps)
    return share <= 0.15, ('most-repeated paragraph skeleton used %dx '
                           '(%.0f%% of body, need <= 15%%)' % (n, 100 * share))


def gate_worked_examples(text, **_):
    """G3 - at least one worked example per two controlled topics."""
    n = len(re.findall(
        r'[Ww]orked example|[Ff]or example|[Ff]or instance|Example:|Scenario:', text))
    need = max(1, len(topic_ids(text)) // 2)
    return n >= need, '%d worked examples (need >= %d)' % (n, need)


def gate_inline_citations(text, **_):
    """G4 - claims must be sourced: one inline citation per two topics."""
    n = len(re.findall(r'\[\d+\]', text))
    need = max(1, len(topic_ids(text)) // 2)
    return n >= need, '%d inline citations (need >= %d)' % (n, need)


def gate_notation_present(text, path=None, **_):
    """G5 - a chapter naming a language or notation must demonstrate it."""
    heading = re.search(r'^# (.+)', text, re.M)
    subject = ((heading.group(1) if heading else '') + ' ' +
               os.path.basename(path or '')).lower()
    for key, pattern in NOTATION.items():
        if key in subject:
            if not re.search(pattern, text):
                return False, 'subject is "%s" but the chapter never shows %s' % (key, key)
            if '```' not in text:
                return False, 'subject is "%s" but there is no code block' % key
            return True, 'notation demonstrated for "%s"' % key
    return True, 'not a notation chapter'


def gate_content_tables(text, **_):
    """G6 - at least one table that is not the completeness-audit table."""
    rows = [r for r in re.findall(r'^\|.*$', text, re.M)
            if 'Topic ID' not in r and not r.startswith('|---')
            and 'UNVERIFIED' not in r and 'COVERED' not in r]
    return len(rows) > 0, '%d non-audit table rows (need >= 1)' % len(rows)


def gate_casing(text, **_):
    """G7 - acronyms must not be lowercased by string interpolation."""
    bad = []
    for a in ACRONYMS:
        bad += re.findall(r'(?:^#{1,6} .*|theory for )\b%s\b' % a, text, re.M)
    return not bad, ('lowercase acronym defects: %s' % bad[:2]) if bad else 'no casing defects'


def gate_cross_reference_titles(text, titles=None, **_):
    """G8 - a cited module title must match that module's contract title."""
    bad = []
    for mid, cited in re.findall(r'`?(BA-M\d+)`?\s*-\s*([A-Z][A-Za-z ,]+)', text):
        real = (titles or {}).get(mid)
        if real and cited.strip().rstrip('.') != real:
            bad.append('%s cited as "%s" but contract says "%s"'
                       % (mid, cited.strip(), real))
    return not bad, '; '.join(sorted(set(bad))[:2]) if bad else 'titles match contracts'


def gate_depth(text, **_):
    """G9 - reach 40 percent of the allocation the chapter header declares."""
    m = re.search(r'planning budget:\*\*\s*approximately ([\d,]+) words', text)
    if not m:
        return True, 'no stated allocation'
    target = int(m.group(1).replace(',', ''))
    actual = len(text.split())
    return actual >= 0.40 * target, ('%d words vs stated %d (need >= %d)'
                                     % (actual, target, int(0.40 * target)))


BLOCKING = 'blocking'
ADVISORY = 'advisory'

# Severity is set by calibration, not by preference (governance/05-content-gates.md).
# BLOCKING gates are failed by 0 of the 10 BA-M01/BA-M02 benchmark chapters, so a
# failure is a regression. ADVISORY gates are failed by the benchmark too, so they
# record a standard the repository has never met and must not block existing work.
GATES = [
    ('G1 distinct-paragraphs', gate_distinct_paragraphs, BLOCKING),
    ('G2 no-template-body', gate_no_template_body, BLOCKING),
    ('G3 worked-examples', gate_worked_examples, ADVISORY),
    ('G4 inline-citations', gate_inline_citations, ADVISORY),
    ('G5 notation-present', gate_notation_present, BLOCKING),
    ('G6 content-tables', gate_content_tables, ADVISORY),
    ('G7 casing', gate_casing, BLOCKING),
    ('G8 cross-ref-titles', gate_cross_reference_titles, ADVISORY),
    ('G9 depth', gate_depth, BLOCKING),
]


def check(path, titles):
    """Return [(name, passed, detail, severity)] for one chapter."""
    text = open(path, encoding='utf-8').read()
    results = []
    for name, fn, severity in GATES:
        try:
            ok, detail = fn(text, path=path, titles=titles)
        except Exception as exc:
            ok, detail = False, 'gate error: %s' % exc
        results.append((name, ok, detail, severity))
    return results


def main():
    ap = argparse.ArgumentParser(
        description='Measurable content gates for controlled theory chapters (ISS-010). '
                    'Only blocking-gate failures affect the exit code unless --strict is given.')
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--quiet', action='store_true',
                    help='only print failing chapters and failing gates')
    ap.add_argument('--strict', action='store_true',
                    help='advisory failures also set a non-zero exit code; use for '
                         'rebuilt and new chapters')
    ap.add_argument('--advisory-only', action='store_true',
                    help='report advisory failures without ever setting a non-zero exit code')
    args = ap.parse_args()

    paths = sorted(glob.glob(CORPUS)) if args.all else args.paths
    if not paths:
        ap.error('give chapter paths or --all')

    # These gates grade controlled theory chapters. A word budget, checkpoint or
    # audit file is not a chapter, and grading one would produce a meaningless
    # blocking failure.
    chapters = [p for p in paths if CHAPTER_FILE.search(os.path.basename(p))]
    for skipped in [p for p in paths if p not in chapters]:
        print('SKIP  %s (not a controlled theory chapter)' % skipped)
    if not chapters:
        ap.error('no controlled theory chapters among the given paths')
    paths = chapters
    titles = contract_titles()

    blocked, advised = 0, 0
    for path in paths:
        results = check(path, titles)
        bad_block = [r for r in results if not r[1] and r[3] == BLOCKING]
        bad_adv = [r for r in results if not r[1] and r[3] == ADVISORY]
        if bad_block:
            blocked += 1
        if bad_adv:
            advised += 1

        if bad_block:
            verdict = 'FAIL'
        elif bad_adv:
            verdict = 'PASS*'
        else:
            verdict = 'PASS'
        if args.quiet and not bad_block and not (args.strict and bad_adv):
            continue
        print('%-5s %s' % (verdict, path))
        for name, ok, detail, severity in results:
            if ok and args.quiet:
                continue
            mark = '.' if ok else ('x' if severity == BLOCKING else '!')
            print('    %s %-24s %-9s %s' % (mark, name, severity, detail))

    print('\nblocking: %d of %d chapters failed a blocking gate.' % (blocked, len(paths)))
    print('advisory: %d of %d chapters failed an advisory gate '
          '(does not affect exit code%s).'
          % (advised, len(paths), '' if not args.strict else ' - overridden by --strict'))
    if args.advisory_only:
        return 0
    if args.strict:
        return 1 if (blocked or advised) else 0
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
