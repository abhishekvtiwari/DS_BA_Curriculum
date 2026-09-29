#!/usr/bin/env python3
"""ch57_check.py - checks Chapter 57's numbers against its companion code: prompt scores, the provider
upgrade, the meter, caching, fallback, and topic drift. Run: python3 checks/ch57_check.py [companion/ch57]"""
import pathlib, random, sys
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch57').resolve()
sys.path.insert(0, str(C)); sys.path.insert(0, str(C.parent / 'ch55'))
from pipeline import (Cache, build_prompt, call_with_fallback, emails, evaluate, normalize_date, parse,
                      tolerant_parse, truth)
from provider import NEW_MODEL, PINNED_MODEL, Meter, call
ok = 0
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
check('golden set size', len(truth), 60)
for v, want in (('v1', (13, 3)), ('v2', (35, 0)), ('v3', (47, 0))):
    r = evaluate(v); check(f'prompt {v}', (r['exact'], r['unparseable']), want)
r = evaluate('v3', model=NEW_MODEL); check('new version breaks the old parser', (r['exact'], r['unparseable']), (0, 60))
r = evaluate('v3', model=NEW_MODEL, parser=tolerant_parse); check('tolerant parser restores it', r['exact'], 47)
check('tolerant parser harmless on pinned', evaluate('v3', parser=tolerant_parse)['exact'], 47)
check('date normalization', normalize_date('07-03-2026'), '2026-03-07')
check('untagged fence parses', tolerant_parse('x\n```\n{\n // c\n "a": 1\n}\n```'), {'a': 1})
check('list reply rejected', tolerant_parse('[1]'), None)
m = Meter(); evaluate('v3', meter=m)
check('meter', (m.calls, m.input_tokens, m.output_tokens, round(m.cost_rupees(), 2)), (60, 10844, 3184, 4.71))
per = m.cost_rupees() / 60
check('month', (round(per * 1120), round(per * 3600)), (88, 283))
rng = random.Random(57); day = rng.sample(list(truth), 40)
traffic = day + [rng.choice(day) for _ in range(8)]; rng.shuffle(traffic)
cache, cm, pm = Cache(), Meter(), Meter()
for n in traffic:
    p = build_prompt('v3', emails[n]); cache.get_or_call(p, PINNED_MODEL, cm); call(p, model=PINNED_MODEL, meter=pm)
check('cache day', (cache.hits, cache.misses, round(cm.cost_rupees(), 2), round(pm.cost_rupees(), 2)), (8, 40, 3.19, 3.82))
fm = Meter(); routes = {'primary': 0, 'fallback': 0, 'failed': 0}
for n in truth:
    _, route = call_with_fallback(build_prompt('v3', emails[n]), fm, failure_rate=0.2, backoff=0)
    routes[route] += 1
check('fallback routes', routes, {'primary': 44, 'fallback': 13, 'failed': 3})
check('fallback errors', fm.errors, {'rate limit': 35, 'timeout': 6})
from assistant import SupportAssistant
from questions_stream import build
a, stream = SupportAssistant(), build()
def refusal_rate(week):
    rows = [q for q in stream if q['week'] == week]
    return round(sum(1 for q in rows if not a.answer(q['question'])['grounded']) / len(rows), 3)
check('refusal week 1', refusal_rate(1), 0.15)
check('refusal week 7', refusal_rate(7), 0.425)
check('new topic from week 5', min(q['week'] for q in stream if q['topic'] == 'new'), 5)
print(f'ch57_check.py: {ok} checks passed')
