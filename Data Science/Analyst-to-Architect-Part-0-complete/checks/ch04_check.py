# Chapter 4 number checks. Every figure quoted in the chapter is recomputed here.
import subprocess, statistics as st, math
def q(sql, db='riverstone_2025'):
    r = subprocess.run(['su','postgres','-c',f"psql -X -q -At -F '|' -d {db}"], input=sql, capture_output=True, text=True, cwd='/tmp')
    if r.stderr: print('ERR', r.stderr)
    return [l.split('|') for l in r.stdout.strip().splitlines()]
M = q("SELECT to_char(order_date,'YYYY-MM'), SUM(net_revenue), SUM(product_cost), COUNT(DISTINCT order_id) FROM sales_lines GROUP BY 1 ORDER BY 1;")
rev = [float(r[1]) for r in M]; cost=[float(r[2]) for r in M]; orders=[int(r[3]) for r in M]
print('monthly revenue', [round(x) for x in rev], 'total', round(sum(rev),2))
gm = [ (r-c)/r*100 for r,c in zip(rev,cost)]
print('monthly GM %', [round(x,1) for x in gm], 'year GM', round((sum(rev)-sum(cost))/sum(rev)*100,1))
T = [float(r[1]) for r in q("SELECT target_month, target_revenue FROM sales_targets ORDER BY 1;")]
print('target sum', sum(T), 'pct of target', round(sum(rev)/sum(T)*100,1))
print('monthly pct of target', [round(r/t*100,1) for r,t in zip(rev,T)])
mom = [(rev[i]-rev[i-1])/rev[i-1]*100 for i in range(1,12)]
print('MoM %', [round(x,1) for x in mom], 'arith mean of MoM', round(sum(mom)/11,2))
cmgr = (rev[11]/rev[0])**(1/11)-1
print('CMGR Jan->Dec', round(cmgr*100,2), 'Dec/Jan', round(rev[11]/rev[0],3))
# what the average MoM would predict
print('Jan grown by arith mean 11 times', round(rev[0]*(1+sum(mom)/11/100)**11))
Q=[sum(rev[i:i+3]) for i in (0,3,6,9)]
print('quarters', [round(x) for x in Q], 'Q4 vs Q1 %', round((Q[3]/Q[0]-1)*100,1), 'CQGR', round(((Q[3]/Q[0])**(1/3)-1)*100,1))
print('H1 H2', round(sum(rev[:6])), round(sum(rev[6:])), 'H2 vs H1', round((sum(rev[6:])/sum(rev[:6])-1)*100,1))
# CAGR plan
start=4335471; target=6000000
c=(target/start)**(1/3)-1; print('CAGR needed', round(c*100,2), 'path', [round(start*(1+c)**k) for k in range(4)])
print('simple split', (target-start)/3, 'pct of start', round((target-start)/3/start*100,1), 'mult', round(target/start,3))
print('10% for 3 yrs', round(start*1.1**3), ' rule72 at 12%', 72/12, 'exact', round(math.log(2)/math.log(1.12),2), 'at 8%', 72/8, round(math.log(2)/math.log(1.08),2))
# +50 -50
print('+50 -50', 100*1.5*0.5, ' -20 then +20', 100*0.8*1.2, ' -50 needs', 100/50-1)
# order values
O = q("SELECT order_id, SUM(net_revenue) FROM sales_lines GROUP BY 1 ORDER BY 2;")
vals=[float(v) for _,v in O]; n=len(vals)
print('orders', n, 'mean', round(st.mean(vals),2), 'median', round(st.median(vals),2), 'min', round(min(vals)), 'max', round(max(vals)))
print('sum', round(sum(vals)))
top10=sorted(vals, reverse=True)[:17]; print('top 10% (17) share', round(sum(top10)/sum(vals)*100,1), 'top 17 sum', round(sum(top10)))
above_mean=sum(1 for v in vals if v>st.mean(vals)); print('orders above mean', above_mean, 'pct', round(above_mean/n*100,1))
print('quartiles', [round(x) for x in st.quantiles(vals, n=4)])
print('largest 5', [round(v) for v in sorted(vals)[-5:]], 'smallest 5', [round(v) for v in sorted(vals)[:5]])
# mode: quantity per line, product most ordered, segment
print('mode product by lines', q("SELECT p.product_name, COUNT(*) FROM order_items oi JOIN orders o USING(order_id) JOIN products p USING(product_id) WHERE o.status<>'Cancelled' GROUP BY 1 ORDER BY 2 DESC;"))
print('quantity mode', q("SELECT quantity, COUNT(*) FROM sales_lines GROUP BY 1 ORDER BY 2 DESC, 1 LIMIT 5;"))
print('lines per order dist', q("SELECT lines, COUNT(*) FROM (SELECT order_id, COUNT(*) lines FROM sales_lines GROUP BY 1) x GROUP BY 1 ORDER BY 1;"))
# order value histogram bins of 10k
import collections
b=collections.Counter(int(v//10000) for v in vals); print('hist 10k bins', sorted(b.items()))
# discounts
D=q("SELECT oi.discount_pct, oi.quantity*oi.unit_price FROM order_items oi JOIN orders o USING(order_id) WHERE o.status<>'Cancelled';")
d=[float(a) for a,_ in D]; g=[float(b) for _,b in D]
print('lines', len(d), 'simple avg discount', round(sum(d)/len(d),2), 'weighted by gross', round(sum(x*y for x,y in zip(d,g))/sum(g),2), 'gross', round(sum(g)), 'net check', round(sum(y*(1-x/100) for x,y in zip(d,g))))
print('discount distribution', q("SELECT discount_pct, COUNT(*), SUM(oi.quantity*oi.unit_price) FROM order_items oi JOIN orders o USING(order_id) WHERE o.status<>'Cancelled' GROUP BY 1 ORDER BY 1;"))
# AOV monthly avg vs overall
aov=[r/o for r,o in zip(rev,orders)]
print('monthly AOV', [round(x) for x in aov], 'avg of monthly AOVs', round(sum(aov)/12), 'overall AOV', round(sum(rev)/sum(orders)), 'orders', sum(orders))
# segments
S=q("SELECT c.segment, SUM(net_revenue), COUNT(DISTINCT order_id), COUNT(DISTINCT s.customer_id) FROM sales_lines s JOIN customers c USING(customer_id) GROUP BY 1 ORDER BY 2 DESC;")
tot=sum(float(r[1]) for r in S)
for r in S: print('segment', r[0], round(float(r[1])), 'share', round(float(r[1])/tot*100,1), 'share0', round(float(r[1])/tot*100), 'orders', r[2], 'customers', r[3], 'rev per customer', round(float(r[1])/int(r[3])), 'aov', round(float(r[1])/int(r[2])))
print('rounded shares sum', sum(round(float(r[1])/tot*100) for r in S), sum(round(float(r[1])/tot*100,1) for r in S))
# categories
C=q("SELECT category, SUM(net_revenue), SUM(quantity) FROM sales_lines GROUP BY 1 ORDER BY 2 DESC;")
ct=sum(float(r[1]) for r in C)
for r in C: print('category', r[0], round(float(r[1])), round(float(r[1])/ct*100,2), 'units', r[2], 'avg net price/unit', round(float(r[1])/int(r[2]),2))
print('units total', sum(int(r[2]) for r in C), 'avg price per unit overall', round(ct/sum(int(r[2]) for r in C),2))
# cancellations
print('orders all/cancelled', q("SELECT COUNT(*), COUNT(*) FILTER (WHERE status='Cancelled') FROM orders;"), 'mini', q("SELECT COUNT(*), COUNT(*) FILTER (WHERE status='Cancelled') FROM orders;", 'riverstone'))
p=2/175; print('p cancel', round(p*100,2), 'at least one in 20 orders', round((1-(1-p)**20)*100,1), 'expected in 20', round(20*p,2))
p1=1/12; print('mini rate at least one in 20', round((1-(1-p1)**20)*100,1))
# customers
print('customers top', q("SELECT c.customer_name, SUM(net_revenue) FROM sales_lines s JOIN customers c USING(customer_id) GROUP BY 1 ORDER BY 2 DESC LIMIT 3;"))
print('customer count', q("SELECT COUNT(DISTINCT customer_id) FROM sales_lines;"))
print('Sharma share', round(502775/4335471*100,1))
# weekly and daily rates
print('orders per week', round(173/52,2), 'revenue per day', round(4335471/365), 'per working day (300)', round(4335471/300))
print('lakh', 4335471/1e5, 'crore', 4335471/1e7, 'million', 4335471/1e6)
# ---- round 2 ----
print('GM Oct->Nov points', round(gm[10]-gm[9],2), 'relative %', round((gm[10]-gm[9])/gm[9]*100,1), 'Jan->Feb', round(gm[1]-gm[0],2), round((gm[1]-gm[0])/gm[0]*100,1))
print('exact GM Oct Nov', round(gm[9],3), round(gm[10],3))
big = q("SELECT c.segment, COUNT(*), COUNT(*) FILTER (WHERE v>50000) FROM (SELECT order_id, customer_id, SUM(net_revenue) v FROM sales_lines GROUP BY 1,2) x JOIN customers c USING(customer_id) GROUP BY ROLLUP(1) ORDER BY 1;")
print('orders >50k by segment', big)
print('Oct units', q("SELECT SUM(quantity) FROM sales_lines WHERE order_date BETWEEN '2025-10-01' AND '2025-10-31';"), 'estimate', round(681071/457.57))
print('avg of category unit prices', round((435.22+341.25+1273.33+1121.25)/4,2))
print('Dec vs Jan %', round((rev[11]/rev[0]-1)*100,1))
print('Sep target pct', round(rev[8]/T[8]*100,1), 'Oct', round(rev[9]/T[9]*100,1))
# ---- round 3: text and exercises ----
print('50 then 20 off pay', 0.5*0.8, 'total off', 1-0.5*0.8, ' 10 then 5', round(1-0.9*0.95,4))
print('reverse 1276/0.88', 1276/0.88, 'wrong 1276*1.12', 1276*1.12, '12% of 1450', 0.12*1450)
print('win rate dupes', round(6/43*100,2), 'points', round(20-6/43*100,2), 'relative', round((6/43*100-20)/20*100,1))
print('Sep->Oct target pct points', round(131.0-146.9,1))
print('rev/customer ratio wholesale/hosp', round(283776/127115,2))
print('compound 100 at 10% 3y', round(100*1.1**3,2), 'simple', 130)
print('10% plan shortfall', 6000000-5770512)
print('discount money', 4548725-4335471, round((4548725-4335471)/4548725*100,2))
print('funnel chain', round(22/30*14/22*6/14*100,2), 'rounded chain', round(0.733*0.636*0.429*100,2), 'leads for 10 wins', 10/0.2)
print('P>50k', round(16/173*100,1), 'P>50k|W', round(10/55*100,1), 'P W|>50k', round(10/16*100,1), 'P W', round(55/173*100,1))
print('Oct estimate error', 1625-1488, round((1488-1625)/1625*100,1))
print('Jun->Oct', round((681071/186928-1)*100,1))
# exercises
print('ex1', 0.05*14550, round(26220/58020*100,1), 780*0.92)
print('ex2 kitchen', round((461146/133888-1)*100,1), 'industrial', round((292040/275450-1)*100,1))
print('ex3', round(75.0-66.3,1), round((75.0-66.3)/66.3*100,1))
mini=[14700,73260,16250,14550,14640,32625,23325,76560,20100,11700,26220]
print('ex4 mean', round(st.mean(mini),2), 'median', st.median(mini), 'sorted', sorted(mini), 'sum', sum(mini))
print('ex5', 76560/0.88)
print('ex6', round((32/20)**(1/4)*100-100,2), 'doubling 72/12.47', round(72/12.47,1), 'exact', round(math.log(2)/math.log((32/20)**(1/4)),2))
CG=q("SELECT category, SUM(net_revenue), SUM(product_cost) FROM sales_lines GROUP BY 1 ORDER BY 2 DESC;")
gms=[]
for c,r,k in CG:
    r=float(r);k=float(k); g=(r-k)/r*100; gms.append(g); print('ex7', c, round(r), round(k), round(g,1))
print('ex7 simple avg of category GM', round(sum(gms)/4,1), 'weighted', round((sum(float(r) for _,r,_ in CG)-sum(float(k) for _,_,k in CG))/sum(float(r) for _,r,_ in CG)*100,2))
print('ex8 one-decimal category shares', [round(x,1) for x in (53.0,27.86,18.36,0.78)], round(sum(round(x,1) for x in (53.0,27.86,18.36,0.78)),1))
print('exact cat shares', [round(float(r)/ct*100,3) for _,r,_ in CG])
print('ex9 leads for 15 wins', 15/0.2, 'at least one of 3', round((1-0.8**3)*100,1))
print('ex11 Nov units', q("SELECT SUM(quantity) FROM sales_lines WHERE order_date BETWEEN '2025-11-01' AND '2025-11-30';"), 'estimate', round(633408/457.57))
print('ex11b estimate using 450', round(633408/450), 'Oct', round(681071/450))
# ---- round 4 ----
print('overshoot', 782621-439824, 'rev per customer total', 4335471/23, 'mom sum', round(sum(mom),1))
print('GM exact Jan Feb', round(gm[0],3), round(gm[1],3))
r=[rev[i]/T[i]*100 for i in range(12)]; print('target Sep Oct exact', round(r[8],3), round(r[9],3), 'rel', round((r[9]-r[8])/r[8]*100,1))
print('recover 20 fall', 1/0.8-1, 'gap', 6000000-4335471)
print('1.384 cube root', round(1.384**(1/3),4), 'ratio', round(6000000/4335471,4), round((6000000/4335471)**(1/3),4), '11th root 2.17', round(2.17**(1/11),4))
print('target Aug Sep exact', round(r[7],3), round(r[8],3), 'points', round(r[8]-r[7],2), 'rel', round((r[8]-r[7])/r[7]*100,2))
print('weekly x aov /7', round(173/52*25061/7), 'orders per customer', round(173/23,2))
print('profit 2->8 lakh', (8-2)/2*100, 'risk abs points', (2-1)/10000*100)
print('p 5 of 173 above 65k', sum(1 for v in vals if v>65000))
print('Oct units by category', q("SELECT category, SUM(quantity), ROUND(SUM(net_revenue)) FROM sales_lines WHERE order_date BETWEEN '2025-10-01' AND '2025-10-31' GROUP BY 1 ORDER BY 1;"), 'Oct avg price', round(681071/1625,2))
print('axis heights', (24.0-23)/(27.9-23))
print('p none 20', round((1-2/175)**20,4))
print('ex6 new', round(((40/25)**(1/5)-1)*100,2))
print('discount by line size', q("SELECT CASE WHEN oi.quantity*oi.unit_price>=20000 THEN 'big' ELSE 'small' END, ROUND(AVG(discount_pct),2), COUNT(*) FROM order_items oi JOIN orders o USING(order_id) WHERE o.status<>'Cancelled' GROUP BY 1;"))
print('ex3 new', round(42.0-39.3,1), round((42.0-39.3)/39.3*100,1))
print('ex5 new', round(1.08*0.92,4), round((1.08*0.92-1)*100,2))
print('ex6 doubling', round(72/9.86,1), round(math.log(2)/math.log(1.0986),2))
print('ex11 err', round((1384-1355)/1355*100,1))
q1o=8+10+11; q4o=20+21+18; print('ex12 Q1 aov', round(Q[0]/q1o), 'Q4 aov', round(Q[3]/q4o), 'avg of two', round((Q[0]/q1o+Q[3]/q4o)/2), 'true', round((Q[0]+Q[3])/(q1o+q4o)), 'orders', q1o, q4o)
print('year GM', round((sum(rev)-sum(cost))/sum(rev)*100,2))
print('ex4 typical: orders below mean', sum(1 for v in mini if v<29448.18))
