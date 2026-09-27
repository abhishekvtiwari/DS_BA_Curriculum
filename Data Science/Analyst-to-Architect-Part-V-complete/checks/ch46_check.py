# Analyst to Architect - Chapter 46 checks (prose numbers and exercise answers).
# Riverstone Supplies is fictional; every name and number is invented.
from decimal import Decimal as D
from datetime import datetime, timedelta, timezone
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
o10176 = 40*D('430.00') + 120*D('115.00')*(1-D('5.00')/100)
o10177 = 6*D('1400.00')
check('10176 revenue', o10176, D('30310.0000'))
check('day 1 Flash', o10176+o10177, D('38710.0000'))
check('naive doubled', 2*(o10176+o10177), D('77420.0000'))
check('Ex4 four rows', 4*(o10176+o10177), D('154840.0000'))
check('day 2 Flash (10178)', 25*D('750.00'), D('18750.00'))
check('late correction', o10176+7*D('1400.00'), D('40110.0000'))
check('correction difference', D('40110')-D('38710'), D('1400'))
ist=timezone(timedelta(hours=5,minutes=30))
t=datetime(2026,1,6,1,0,tzinfo=timezone.utc).astimezone(ist)
check('Ex2 01:00 UTC in IST', t.strftime('%H:%M %d'), '06:30 06')
t2=datetime(2026,1,5,20,0,tzinfo=timezone.utc).astimezone(ist)
check('Ex2 trap 20:00 UTC', t2.strftime('%H:%M %d'), '01:30 06')
t3=datetime(2026,1,6,3,0,tzinfo=ist).astimezone(timezone.utc)
check('3am IST is previous UTC day', t3.strftime('%d'), '05')
check('Jan 3 2026 weekday', datetime(2026,1,3).strftime('%A'), 'Saturday')
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
