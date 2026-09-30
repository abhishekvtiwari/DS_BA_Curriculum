# Analyst to Architect - Chapter 9 number checks. Run: python3 checks/ch09_check.py (from the book root)
# Riverstone Supplies is fictional; every name and number is invented.
import sys; sys.path.insert(0,'figures')
from make_figs09 import MINUTES, CHECK
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
check('total minutes',sum(MINUTES),2800)
check('total hours',round(sum(MINUTES)/60,1),46.7)
check('weeks 5-8 minutes',sum(MINUTES[4:8]),1010)
check('weeks 5-8 score change (week 4 6 -> week 8 6)',CHECK[7]-CHECK[3],0)
check('weeks 1-4 minutes',sum(MINUTES[0:4]),810)
check('weeks 1-4 score change (week1 3 -> week4 6)',CHECK[3]-CHECK[0],3)
check('weeks 9-12 minutes',sum(MINUTES[8:12]),980)
check('weeks 9-12 score change from week 8 (6 -> 9)',CHECK[11]-CHECK[7],3)
check('week 7 vs week 4 minutes increase %',round(100*(270/220-1),1),22.7)
check('avg minutes weeks 9-12',sum(MINUTES[8:12])/4,245.0)
check('avg minutes weeks 5-7',round(sum(MINUTES[4:7])/3,1),256.7)
# chapter time estimates, read from the chapters' own Time needed lines (the first range: Ch 12's
# PostgreSQL core 22-26 h, Ch 13 15-20 h); Chapter 6's table (tools/hours_table.py) adds Ch 12's 6-10 h
import re; sys.path.insert(0,'tools'); import hours_table
first=lambda n: tuple(int(x) for x in re.search(r'(\d+)\s*[–-]\s*(\d+)\s+hours',hours_table.time_needed_line(n)).groups())
(a12,b12),(a13,b13)=first(12),first(13)
lo,hi=a12+a13,b12+b13
check('Ch12 core line',(a12,b12),(22,26)); check('Ch13 line',(a13,b13),(15,20))
check('Ch12+13 hours low',lo,37); check('Ch12+13 hours high',hi,46)
t12=hours_table.chapter_hours(12); check('Ch 6 table count for Ch 12+13',(t12[0]+a13,t12[1]+b13),(43,56))
check('weeks at 6 h/wk low',round(lo/6,1),6.2); check('weeks at 6 h/wk high',round(hi/6,1),7.7)
check('weeks at 10 h/wk low',round(lo/10,1),3.7); check('weeks at 10 h/wk high',round(hi/10,1),4.6)
check('Farah 46.7 h is slightly more than the high estimate',46.7>hi and 46.7-hi<1,True)
# exercises
check('Ex 4: 45 min x 5 days x 8 weeks, hours',45*5*8/60,30.0)
check('Ex 4: hours short of 37',lo-30,7)
check('Ex 4: extra weeks at 3.75 h/wk',round(7/(45*5/60),1),1.9)
check('Ex 5: 20 min/day x 365 days hours',round(20*365/60,1),121.7)
check('Ex 5: one 3-hour Sunday x 52 weeks',3*52,156)
check('Ex 6: rate w1..w12 check from 3 to 9 (+%)',round(100*(9/3-1)),200)
check('wrong answers weeks 5-7',sum(10-x for x in CHECK[4:7]),12)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
