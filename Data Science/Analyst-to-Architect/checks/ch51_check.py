# Analyst to Architect - Chapter 51 checks. Run from the book root:
#   python3 checks/ch51_check.py     (needs riverstone_2025 loaded; reset_ch51 recreates riverstone_source)
# Checks the numbers the chapter's prose states against a real run of the companion code.
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys
os.chdir('companion/ch51'); sys.path.insert(0, '.')
from reset_ch51 import reset
import sync_leads as sl
ok = True
def check(label, got, exp):
    global ok
    good = (got == exp); ok &= good
    print(('OK  ' if good else 'FAIL'), label, got, '' if good else f'(expected {exp})')

reset()
scores = sl.lead_scores()
check('total leads scored', len(scores), 43)
check('lead 2 (Bright Kitchens, Quoted 55 + Website 10 + recency 0)', scores['2']['score'], 65)
check('lead 6 (Delta Hospitality, Lost)', scores['6']['score'], 0)
check('lead 7 (Elite Mart, Won, capped at 100)', scores['7']['score'], 100)
check('lead 4 (the lead section 51.4 changes)', scores['4']['score'], 20)
# exercise 4, from the tables in section 51.2: Contacted 30 + Trade fair 20 + recency 10
check('exercise 4 hand computation', 30 + 20 + 10, 60)
flags = sl.follow_up_flags()
check('customers with a flag', len(flags), 24)
check('follow-up-due customer ids', sorted([c for c, v in flags.items() if v], key=int), ['2', '8', '9', '13', '20', '22'])
check('run keys: same run, same key', sl.run_key('leads/4', {'score': 20}, '2026-01-06'),
      sl.run_key('leads/4', {'score': 20}, '2026-01-06'))
check('run keys: new run, new key', sl.run_key('leads/4', {'score': 20}, '2026-01-06')
      != sl.run_key('leads/4', {'score': 20}, '2026-01-07'), True)
check('content key ignores dict order', sl.idempotency_key('leads/2', {'score': 65, 'stage': 'Quoted'}),
      sl.idempotency_key('leads/2', {'stage': 'Quoted', 'score': 65}))
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
