"""Checks for Chapter 59 (a reading chapter with no code): every number the chapter computes or
quotes from another chapter, and that Figure 59.2's grid agrees with the text.

    python3 checks/ch59_check.py
"""
import pathlib, re, sys
BOOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK / 'figures'))
import make_figs59 as F

ms = lambda n: (BOOK / 'manuscript').glob(f'ch{n}-*.md').__next__().read_text(encoding='utf-8')
ch59, ch53, ch44, ch56, ch58 = ms(59), ms(53), ms(44), ms(56), ms(58)
ok = 0
def check(cond, what):
    global ok
    if not cond: sys.exit('FAIL: ' + what)
    ok += 1; print('ok  ', what)

# Figure 59.2 against the text of section 59.11
counts = [sum(m) for _, m in F.PATTERNS]
check(counts[0] == 8, 'pattern 1 "eight of nine": figure has %d' % counts[0])
check(F.PATTERNS[0][1][2] == 0 and 'The exception is lead scoring' in ch59, 'pattern 1 exception is case 3, named in the text')
check(counts[2] == 8 and F.PATTERNS[2][1][3] == 0, 'pattern 3 "almost always": 8 of 9, not pricing')
check(counts[3] == 7 and F.PATTERNS[3][1][2] == 0 and F.PATTERNS[3][1][3] == 0, 'pattern 4 "mostly organizational": not cases 3 and 4 (leakage, confounding)')
check(counts[4] == 6, 'pattern 5 "in most cases the metric changed": 6 of 9')
check('eight of nine' in ch59 and 'in every successful case' not in ch59, 'Recap wording matches the figure')

# Case 1 against Chapter 53
check('caught 116 of 119 defects (recall 97.5%)' in ch53 and '97.5% of defects caught' in ch59, 'Case 1: 97.5% recall (116/119) is printed in Ch 53')
check(round(116 / 119 * 100, 1) == 97.5, '116 / 119 = 97.5%')
check('cost: 13,840 rupees for 1,500 parts' in ch53 and '₹40,080' in ch53, 'Case 1: ₹13,840 and ₹40,080 are Ch 53 outputs')
check('defective: 476 (7.9%)' in ch53 and round(476 / 6000 * 100, 1) == 7.9, 'Case 1: 476 of 6,000 = 7.9%')
check('Three weeks later a customer returns' in ch53 and 'three weeks after a two-week trial' in ch59 and 'six weeks later' not in ch59, 'Case 1: return three weeks after the trial (Ch 53)')

check('flash, from the new mould' in ch56 and 'A 2% audit of passed parts' in ch56, 'Case 1, second incident: flash from the new mould; the 2% audit is the fix (Ch 56)')
check('change log now goes to whoever owns the model' in ch56 and 'triggers a review' in ch56, 'Case 1: change log to the model owner; a line change triggers a retraining review (Ch 56)')
check('amber since late April**, when the plant replaced the overhead lamps' in ch56, 'Case 1: the drift monitor had been alerting since the lamp change (Ch 56)')

# Case 9 against Chapter 58
check('**88% straight through and 19% silently wrong**' in ch58 and '53 of 60' in ch58, 'Case 9: 88% (53 of 60) and 19% are Ch 58 results')
check(re.search(r'about 2[5-9] minutes of coordinator time against two hours', ch58) is not None, 'Case 9: two hours a day to about half an hour (Ch 58 story)')
check('62% of the volume' in ch58 and 'full automation' in ch59, 'Case 9: the perfectly scoring formats (Ch 58 section 58.8)')
check(round(53 / 60 * 100) == 88 and round(10 / 53 * 100) == 19, '53/60 = 88%, 10/53 = 19%')

# Answer 3 against Chapter 44 (₹1,200,524 and ₹386,008 in lakh)
check('₹1,200,524' in ch44 and '₹386,008' in ch44, 'Ch 44 prints ₹1,200,524 and ₹386,008')
check(f'{1200524 / 1e5:.1f}' == '12.0' and f'{386008 / 1e5:.1f}' == '3.9', 'about ₹12.0 lakh and ₹3.9 lakh')
check('test AUC 0.829' in ch44, 'Ch 44 test AUC 0.829')

# Composite-case arithmetic quoted in the text
check(3000 / 40 == 75, 'Case 5: 3,000 reviews a day / 40 analysts = 75 each')
check(3 / (6 * 5) == 0.1, 'Case 3: 3 days of modeling against 6 weeks (30 working days) of data = a tenth')
print(f'{ok} checks pass')
