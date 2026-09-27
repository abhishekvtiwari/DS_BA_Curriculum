# Analyst to Architect - Chapter 8 number checks. Run: python3 checks/ch08_check.py (from the book root)
# Riverstone Supplies is fictional; every name and number is invented. Salary figures: PayScale India and
# Indeed India pages as retrieved on 16 September 2026 (see the chapter report).
import sys; sys.path.insert(0,'figures')
from make_figs08 import ROLES, SKILLS
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
col=lambda r: [v[ROLES.index(r)] for _,v in SKILLS]
check('skills in matrix',len(SKILLS),17)
core=lambda r: sum(1 for x in col(r) if x==2)
for r,n in [('Data analyst',5),('Business analyst',4),('Data scientist',6),('Data engineer',7),('Data architect',9),('Automation / integration',6)]:
    check(f'core skills {r}',core(r),n)
check('SQL nonzero for every role',all(v>0 for v in dict(SKILLS)['SQL']),True)
check('roles with ML core',[r for r,v in zip(ROLES,dict(SKILLS)['Machine learning']) if v==2],['Data scientist','ML engineer'])
check('roles with Python core',[r for r,v in zip(ROLES,dict(SKILLS)['Python']) if v==2],['Data scientist','ML engineer','Data engineer','AI engineer','Automation / integration'])
both=lambda a,b: [s for s,v in SKILLS if v[ROLES.index(a)]>0 and v[ROLES.index(b)]>0]
check('DA & BI dev shared skills (ex 12)',len(both('Data analyst','BI developer')),7)
check('DA & data engineer shared skills (ex 12)',len(both('Data analyst','Data engineer')),4)
# gap scores (section 8.5 and exercise 5): must-haves x2, nice-to-haves x1, each scored 0-2
def score(must,nice): return 2*sum(must)+sum(nice), 2*2*len(must)+2*len(nice)
f=score([1,2,0,0,2],[0,0,1,2]); check('Farah score',f,(13,28)); check('Farah %',round(100*f[0]/f[1],1),46.4)
check('Farah must-have coverage %',round(100*sum([1,2,0,0,2])/10),50)
r=score([0,2,1,1,1],[1,0,2,2]); check('Ex5 score',r,(15,28)); check('Ex5 %',round(100*r[0]/r[1],1),53.6)
# salaries (PayScale India, July 2026 updates; Indeed India, 30 Aug 2026)
check('DA entry->early growth %',round(100*(565999/413462-1),1),36.9)
check('DS entry->early growth %',round(100*(1005147/595255-1),1),68.9)
check('DE entry->early growth %',round(100*(810624/518398-1),1),56.4)
check('Indeed DA avg minus PayScale DA avg base',633625-577472,56153)
check('Indeed over PayScale %',round(100*(633625/577472-1),1),9.7)
check('DS median / DA median (577k vs 1m)',round(1000/577,2),1.73)
check('DA entry in lakh',round(413462/1e5,1),4.1)
check('DS early in lakh',round(1005147/1e5,1),10.1)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
