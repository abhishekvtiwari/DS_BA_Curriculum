#!/usr/bin/env python3
"""ch57_check.py - checks Chapter 57's numbers: prompt scores, the provider upgrade, cost, caching, fallback, drift."""
import os, pathlib, random, sys
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch57')
os.chdir(C); sys.path.insert(0, str(C))
from pipeline import Cache, PROMPTS, call_with_fallback, evaluate, load_emails, normalize_date
from provider import Meter, call
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, float) and isinstance(got, float):
        assert abs(got - want) <= tol + 1e-9, f'{label}: {got} != {want}'
    else:
        assert got == want, f'{label}: {got} != {want}'
    ok += 1
truth, emails = load_emails()
check('golden set size', len(truth), 60)
check('prompt v1', evaluate('v1')['exact'], 21)
check('prompt v2', evaluate('v2')['exact'], 35)
check('prompt v3', evaluate('v3')['exact'], 47)
check('v3 parses cleanly', evaluate('v3')['unparseable'], 0)
check('provider upgrade breaks the old parser', evaluate('v3', model='v2', tolerant=False)['unparseable'], 60)
check('and scores nothing', evaluate('v3', model='v2', tolerant=False)['exact'], 0)
check('tolerant parser restores it', evaluate('v3', model='v2')['exact'], 47)
check('date normalization', normalize_date('04-03-2026'), '2026-03-04')
check('iso dates pass through', normalize_date('2026-03-04'), '2026-03-04')
meter = Meter(); evaluate('v3', meter=meter)
check('calls per golden run', meter.calls, 60)
check('input tokens', meter.input_tokens, 11006)
check('output tokens', meter.output_tokens, 3184)
check('cost per golden run', round(meter.cost_rupees(), 2), 4.74, tol=0.01)
names = list(truth); rng = random.Random(57)
traffic = [rng.choice(names[:20]) if rng.random() < 0.45 else rng.choice(names) for _ in range(300)]
cache, cached_meter, plain_meter = Cache(), Meter(), Meter()
for name in traffic:
    prompt = PROMPTS['v3'].format(name=name) + '\nEMAIL:\n' + emails[name]
    cache.get_or_call(prompt, model='v1', meter=cached_meter)
    call(prompt, model='v1', meter=plain_meter)
check('cache hits', cache.hits, 243); check('cache misses', cache.misses, 57)
check('cache hit rate', round(cache.hit_rate, 2), 0.81, tol=0.005)
check('cache saves cost', round(1 - cached_meter.cost_rupees() / plain_meter.cost_rupees(), 2), 0.81, tol=0.01)
fallback_meter = Meter(); routes = {'primary': 0, 'fallback': 0, 'failed': 0}
for name in truth:
    _, route = call_with_fallback(PROMPTS['v3'].format(name=name) + '\nEMAIL:\n' + emails[name],
                                  fallback_meter, failure_rate=0.2)
    routes[route] += 1
check('served by the primary model', routes['primary'], 48)
check('served by the fallback', routes['fallback'], 9)
check('escalated honestly', routes['failed'], 3)
check('provider errors absorbed', fallback_meter.failures, 29)
sys.path.insert(0, str(C.parent / 'ch55')); os.chdir(C.parent / 'ch55')
from assistant import SupportAssistant
from questions_stream import build
assistant, stream = SupportAssistant(), build()
def refusal_rate(week):
    rows = [q for q in stream if q['week'] == week]
    return round(sum(1 for q in rows if not assistant.answer(q['question'])['grounded']) / len(rows), 2)
check('refusal rate in week 1', refusal_rate(1), 0.15)
check('refusal rate in week 7', refusal_rate(7), 0.42)
check('new-topic questions appear in week 5', min(q['week'] for q in stream if q['topic'] == 'new'), 5)
print(f'ch57_check.py: {ok} checks passed')
