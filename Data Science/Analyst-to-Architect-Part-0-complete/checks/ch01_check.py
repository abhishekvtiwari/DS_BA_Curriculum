from statistics import mean, median
# receipt
items=[("Toor dal 1 kg",1,165),("Basmati rice 5 kg",1,540),("Milk 500 ml",4,28),("Bath soap",3,45),("Tea 250 g",1,140)]
lines=[(n,q,p,q*p) for n,q,p in items]; print(lines, sum(l[3] for l in lines))
# DIKW
jan,feb,mar=104210,161700,31800; print('mar vs feb %', round(100*(mar-feb)/feb,1))
# ratings
A=[3,3,3,3,3]; B=[5,5,5,1,1]; print(mean(A),median(A),mean(B),median(B))
# temperature
print(round((40+273.15)/(20+273.15),3))
# spending log
log=[("2026-09-07","08:40","Tea and poha","Food",60,"UPI","Station stall","No"),
("2026-09-07","09:15","Metro card top-up","Transport",500,"UPI","Metro station","Yes"),
("2026-09-07","19:30","Vegetables","Groceries",240,"Cash","Local market","Yes"),
("2026-09-08","13:05","Lunch thali","Food",180,"Card","Canteen","Yes"),
("2026-09-08","21:10","Movie ticket","Entertainment",350,"UPI","Online","No"),
("2026-09-09","08:45","Tea and poha","Food",60,"UPI","Station stall","No"),
("2026-09-09","18:20","Mobile recharge","Bills",299,"UPI","Online","Yes"),
("2026-09-09","20:00","Auto rickshaw","Transport",90,"Cash","Street","Yes")]
tot=sum(r[4] for r in log); print('total',tot)
from collections import defaultdict
c=defaultdict(int); m=defaultdict(int); nn=0
for r in log: c[r[3]]+=r[4]; m[r[5]]+=r[4]; nn+= r[4] if r[7]=="No" else 0
print(dict(c)); print(dict(m)); print('upi share', round(100*m['UPI']/tot,1), 'not necessary', nn, round(100*nn/tot,1))
print('avg per day', round(tot/3,1), 'median txn', median([r[4] for r in log]), 'mean txn', mean([r[4] for r in log]))
