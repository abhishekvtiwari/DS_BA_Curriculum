#!/usr/bin/env python3
"""Build the DS and BA pathway roadmap page from the module contracts.

The contracts are the source of truth. This script reads them, extracts the
module / chapter / controlled-topic tree, and injects it into
`roadmap-template.html`. The page it produces is a generated view, not
authoritative material (authoring policy 1.9), so it is written under `output/`
which is not tracked.

    python tools/roadmap/build_roadmap.py
    python tools/roadmap/build_roadmap.py --out somewhere/roadmap.html
    python tools/roadmap/build_roadmap.py --check

`--check` rebuilds and reports the counts without writing, so a run can confirm
the page still reconciles against the contracts.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TEMPLATE = os.path.join(HERE, 'roadmap-template.html')
DEFAULT_OUT = os.path.join(ROOT, 'output', 'roadmap', 'curriculum-roadmap.html')

TRACKS = (
    ('DS', 'contracts/data-science/DS-M*-contract.json'),
    ('BA', 'contracts/business-analyst/BA-M*-contract.json'),
)


def read_track(pattern):
    """One pathway as an ordered list of modules with chapters and topics."""
    mods = []
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        c = json.load(open(path, encoding='utf-8'))
        mods.append({
            'id': c.get('module_id'),
            'title': c.get('module_title'),
            'obj': c.get('objective', ''),
            'pre': c.get('prerequisite_modules', []),
            'next': c.get('recommended_next_module'),
            'ch': [{'id': ch.get('id'),
                    'title': ch.get('title'),
                    't': [s.get('title') for s in ch.get('subtopics', [])]}
                   for ch in c.get('chapters', [])],
        })
    return mods


def collect():
    data = {key: read_track(pat) for key, pat in TRACKS}
    problems = []
    for key, mods in data.items():
        if not mods:
            problems.append('%s: no contracts matched' % key)
        for m in mods:
            if not m['id'] or not m['title']:
                problems.append('%s: a contract is missing module_id or module_title' % key)
            for ch in m['ch']:
                if not ch['id'] or not ch['title']:
                    problems.append('%s %s: a chapter is missing id or title' % (key, m['id']))
                if not ch['t']:
                    problems.append('%s %s: %s has no subtopics' % (key, m['id'], ch['id']))
    return data, problems


def counts(mods):
    return len(mods), sum(len(m['ch']) for m in mods), sum(len(c['t']) for m in mods for c in m['ch'])


def build(data):
    tpl = open(TEMPLATE, encoding='utf-8').read()
    if '__DATA__' not in tpl:
        raise SystemExit('template has no /*__DATA__*/ placeholder')
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    out = re.sub(r'/\*__DATA__\*/.*?/\*__END__\*/', lambda m: blob, tpl, flags=re.S)
    if '__DATA__' in out:
        raise SystemExit('data injection failed')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--check', action='store_true',
                    help='report counts and exit without writing')
    args = ap.parse_args()

    data, problems = collect()
    for key, _ in TRACKS:
        m, c, t = counts(data[key])
        print('%s: %d modules, %d chapters, %d controlled topics' % (key, m, c, t))

    if problems:
        print('\nproblems:')
        for p in problems:
            print('  -', p)
        return 1

    if args.check:
        build(data)
        print('\ntemplate renders; nothing written (--check)')
        return 0

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    open(args.out, 'w', encoding='utf-8').write(build(data))
    print('\nwrote %s (%d bytes)' % (args.out, os.path.getsize(args.out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
