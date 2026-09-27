# Analyst to Architect - Chapter 51 checks. Run from the book root:
#   PYTHONPATH=companion/ch51 python3 checks/ch51_check.py     (needs riverstone_2025 loaded)
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
check('lead 2 (Bright Kitchens, Quoted, Website, not recent)', scores['2']['score'], 65)
check('lead 6 (Delta Hospitality, Lost)', scores['6']['score'], 0)
check('lead 7 (Elite Mart, Won, capped at 100)', scores['7']['score'], 100)
# hand-computation from section 51.2's stated rule, exercise 4
STAGE, SOURCE = sl.STAGE_POINTS, sl.SOURCE_POINTS
ex4 = STAGE['Contacted'] + SOURCE['Trade Show'] + 10
check('exercise 4 hand computation', ex4, 60)
overdue = sl.overdue_flags()
check('customers in the 45-75 day bucket', len(overdue), 4)
check('overdue customer ids', sorted(overdue, key=int), ['2', '8', '20', '22'])
check('lead 4 mismatch arithmetic (20 vs 21)', scores['4']['score'] + 1, 21)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
