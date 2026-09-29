"""Analyst to Architect · Chapter 35 · number check.
Recomputes every number quoted in the prose (hand calculations, tables, reconciliations) from the
companion CSV files. Run from checks/: python3 ch35_check.py   Exit code 0 means every check passed.
Riverstone Supplies is fictional; every name and number is invented."""
import math, pathlib, numpy as np, pandas as pd
from math import comb, exp, factorial, log, log2
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch35"
c = pd.read_csv(D/"customers_2025.csv"); o = pd.read_csv(D/"orders_2025.csv"); l = pd.read_csv(D/"leads_2025.csv")
fails = 0
def ok(label, got, want, tol=0.0051):
    global fails
    good = abs(got - want) <= tol * max(1, abs(want)) if isinstance(want, float) else got == want
    if not good: fails += 1
    print(f"{'OK ' if good else 'BAD'} {label}: {got} (text: {want})")

# 35.1-35.3
ok("customers", len(c), 23); ok("orders", len(o), 173); ok("revenue total", round(o.order_value.sum()), 4335471)
ok("Sharma revenue lakh", round(502775/1e5, 2), 5.03); ok("Sharma length", round(math.hypot(16, 5.03), 2), 16.77)
s = c.set_index("customer_name")[["storage_share","kitchen_share","industrial_share","furniture_share"]]
sh, me, co = s.loc["Sharma Hardware"].values, s.loc["Metro Mart"].values, s.loc["Coastal Foods"].values
ok("Sharma·Metro", round(sh@me, 6), 0.561196, 1e-9); ok("Sharma·Coastal", round(sh@co, 6), 0.315536, 1e-9)
ok("len Sharma", round(np.linalg.norm(sh), 5), 0.72636, 1e-9); ok("len Metro", round(np.linalg.norm(me), 5), 0.77598, 1e-9)
ok("len Coastal", round(np.linalg.norm(co), 5), 0.70762, 1e-9)
ok("cos S-M", round(sh@me/np.linalg.norm(sh)/np.linalg.norm(me), 4), 0.9957, 1e-9)
ok("cos S-C", round(sh@co/np.linalg.norm(sh)/np.linalg.norm(co), 4), 0.6139, 1e-9)
ok("avg order", round(4335471/173, 2), 25060.53, 1e-9); ok("Sharma pred", round(16*4335471/173), 400968)
ok("Sharma error", round(16*4335471/173) - 502775, -101807)
# 35.4-35.6
x = np.array([4,7,8,12.]); y = np.array([66,174,198,297.])
ok("rounded revenues", [round(v/1000) for v in [66399,174148,198278,296876]], [66,174,198,297])
ok("loss(20)", float(np.mean((20*x-y)**2)), 1511.25, 1e-9); ok("dL/dw at 20", float(2*np.mean((20*x-y)*x)), -585.0, 1e-9)
ok("exact w", round(float((x*y).sum()/(x*x).sum()), 2), 24.29, 1e-9); ok("sum xy", float((x*y).sum()), 6630.0); ok("sum x2", float((x*x).sum()), 273.0)
ok("start loss", float(np.mean(y**2)), 40511.25, 1e-9); ok("sum y", float(y.sum()), 735.0)
w=b=0.0; rows=[]
for _ in range(3):
    e=w*x+b-y; rows.append((w,b,np.mean(e**2),2*np.mean(e*x),2*np.mean(e))); w-=0.005*rows[-1][3]; b-=0.005*rows[-1][4]
ok("step2 loss", round(rows[1][2],2), 4115.66, 1e-9); ok("step3 loss", round(rows[2][2],2), 647.26, 1e-9)
ok("after3 w", round(w,3), 23.279, 1e-9); ok("after3 b", round(b,3), 2.504, 1e-9); ok("after3 loss", round(float(np.mean((w*x+b-y)**2)),2), 316.36, 1e-9)
bw, bb = np.polyfit(x, y, 1); ok("LS w", round(bw,2), 28.51, 1e-9); ok("LS b", round(bb,2), -37.21, 1e-9)
ok("x mean", float(x.mean()), 7.75); ok("centered intercept", round(float(y.mean()),2), 183.75, 1e-9)
H = np.array([[2*np.mean(x*x), 2*np.mean(x)], [2*np.mean(x), 2]]); ok("stability limit", round(2/np.linalg.eigvalsh(H).max(), 5), 0.01447, 1e-9)
# 35.7-35.9
ok("C(30,6)", comb(30,6), 593775); ok("binomial", round(comb(30,6)*.2**6*.8**24, 3), 0.179, 1e-9)
lam = 173/52; ok("rate", round(lam,2), 3.33, 1e-9); ok("P0", round(exp(-lam),4), 0.0359, 1e-9); ok("weeks 0", round(52*exp(-lam),1), 1.9, 1e-9)
ok("weeks 8+", round(52*(1-sum(exp(-lam)*lam**k/factorial(k) for k in range(8))),1), 1.1, 1e-9)
ok("likelihood .1/.2", round((.2**6*.8**24)/(.1**6*.9**24),1), 3.8, 1e-9); ok("likelihood .2/.3", round((.2**6*.8**24)/(.3**6*.7**24),1), 2.2, 1e-9)
ok("0.9^24", round(.9**24,6), 0.079766, 1e-9); ok("0.8^24", round(.8**24,7), 0.0047224, 1e-9); ok("0.7^24", round(.7**24,8), 0.00019158, 1e-9)
ok("loglik", round(6*log(.2)+24*log(.8),4), -15.0121, 1e-9)
H2 = lambda p: -(p*log2(p)+(1-p)*log2(1-p))
ok("entropy .2", round(H2(.2),3), 0.722, 1e-9); ok("entropy web", round(H2(1/14),3), 0.371, 1e-9); ok("entropy other", round(H2(5/16),3), 0.896, 1e-9)
web = l[l.source=="Website"]; ok("web leads/wins", (len(web), int(web.won.sum())), (14,1))
wavg = 14/30*H2(1/14)+16/30*H2(5/16); ok("weighted", round(wavg,3), 0.651, 1e-9); ok("gain", round(H2(.2)-wavg,3), 0.071, 1e-9)
costs = [-log(.9), -log(.7), -log(.8), -log(.9), -log(.2)]; ok("log loss 5", round(sum(costs)/5,3), 0.480, 1e-9)
ok("rounded cost sum", round(sum(round(v,3) for v in costs),3), 2.399, 1e-9); ok("cost 0.01", round(-log(.01),1), 4.6, 1e-9)
ok("accuracy all-no", round(24/30,2), 0.8, 1e-9)
# 35.10
P = np.array([[16,50],[16,33],[10,41],[7,17],[4,5]], float); Z = P-P.mean(0); S = Z.T@Z/4
ok("var orders", float(S[0,0]), 28.8, 1e-9); ok("var rev", float(S[1,1]), 330.2, 1e-9); ok("cov", float(S[0,1]), 82.35, 1e-9)
lam1 = (S[0,0]+S[1,1])/2+math.sqrt(((S[0,0]-S[1,1])/2)**2+S[0,1]**2); ok("lambda1", round(lam1,2), 351.23, 1e-9)
ok("share", round(lam1/359,3), 0.978, 1e-9); ok("ratio v/u", round((lam1-28.8)/82.35,3), 3.915, 1e-9)
v = np.array([1,(lam1-28.8)/82.35]); v/=np.linalg.norm(v); ok("dir", list(v.round(3)), [0.247,0.969])
ok("Sharma score", round(float(Z[0]@v),2), 21.49, 1e-9); ok("Blue Bay score", round(float(Z[4]@v),2), -25.08, 1e-9)
# Answers
g, t = np.array([.386,.614]), np.array([.096,.904]); ok("ex1 cos", round(float(g@t/np.linalg.norm(g)/np.linalg.norm(t)),3), 0.898, 1e-9)
ok("ex3 loss", float(np.mean((25*x-y)**2)), 292.5, 1e-9); ok("ex3 deriv", float(2*np.mean((25*x-y)*x)), 97.5, 1e-9)
ok("ex4 H(.9)", round(H2(.9),3), 0.469, 1e-9); ok("ex7 at least one", round(1-exp(-3.33),3), 0.964, 1e-9); ok("ex7 month", round(exp(-1.5),3), 0.223, 1e-9)
ok("ex8 ratio", round(exp(0.9078),1), 2.5, 1e-9); ok("ex9 B cost", round(-log(.05),2), 3.0, 1e-9)
# Added in the Part 4 build (review fixes 35.3-35.31)
ok("Sharma avg order", round(502775/16), 31423); ok("model avg order", round(4335471/173), 25061)
ok("valley 10", round(float(np.mean((10*x-y)**2)),2), 14186.25, 1e-9); ok("valley 30", round(float(np.mean((30*x-y)**2)),2), 2486.25, 1e-9)
ok("valley 24.29", round(float(np.mean((24.29*x-y)**2)),2), 257.68, 1e-9)
ok("square slope", round((3.001**2-9)/0.001,3), 6.001, 1e-9); ok("14 nudge", round(14.001**2-14**2,6), 0.028001, 1e-9)
xb, yb = x.mean(), y.mean(); sxy = float(((x-xb)*(y-yb)).sum()); sxx = float(((x-xb)**2).sum())
ok("Sxy", sxy, 933.75, 1e-9); ok("Sxx", sxx, 32.75, 1e-9); ok("slope 22.10", round(sxy/sxx,4), 28.5115, 1e-9); ok("intercept 22.10", round(yb-sxy/sxx*xb,2), -37.21, 1e-9)
cx = np.array([1,2,3.]); cy = np.array([2,4,6.]); e = -cy
ok("checkpoint B loss", round(float(np.mean(e**2)),2), 18.67, 1e-9); ok("checkpoint B slope w", round(float(2*np.mean(e*cx)),2), -18.67, 1e-9)
ok("checkpoint B new w", round(float(-0.05*2*np.mean(e*cx)),3), 0.933, 1e-9); ok("checkpoint B new b", round(float(-0.05*2*np.mean(e)),3), 0.4, 1e-9)
ok("3 leads 1 won", round(3*.2*.8*.8,3), 0.384, 1e-9); ok("WLL", round(.2*.8*.8,3), 0.128, 1e-9)
ok("P5 of 30", round(comb(30,5)*.2**5*.8**25,3), 0.172, 1e-9); ok("P7 of 30", round(comb(30,7)*.2**7*.8**23,3), 0.154, 1e-9)
ok("rate 3.327", round(lam,3), 3.327, 1e-9); ok("e^-3.33", round(exp(-3.33),4), 0.0358, 1e-9)
ok("P1", round(lam*exp(-lam),3), 0.119, 1e-9); ok("weeks 1", round(52*lam*exp(-lam),1), 6.2, 1e-9)
ok("P2", round(lam**2/2*exp(-lam),3), 0.199, 1e-9); ok("weeks 2", round(52*lam**2/2*exp(-lam),1), 10.3, 1e-9)
ok("ln 0.2", round(log(.2),4), -1.6094, 1e-9); ok("ln 0.8", round(log(.8),4), -0.2231, 1e-9); ok("ln 0.16", round(log(.16),4), -1.8326, 1e-9)
ok("ln 2", round(log(2),4), 0.6931, 1e-9); ok("surprise win", round(-log2(.2),2), 2.32, 1e-9); ok("surprise loss", round(-log2(.8),2), 0.32, 1e-9)
ok("three-lead .5", .5**3, 0.125); ok("ex7 at least one (3.327)", round(1-exp(-lam),3), 0.964, 1e-9)
ok("checkpoint C entropy", round(H2(.25),3), 0.811, 1e-9); ok("checkpoint C log loss", round((-log(.5)*2-log(.75)*2)/4,3), 0.490, 1e-9)
angles = {0:28.8, 30:175.47, 60:326.17, 75.7:351.23, 90:330.2, 120:183.53}
for deg, want in angles.items():
    u = np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))]); ok(f"variance at {deg}", round(float(np.var(Z@u, ddof=1)),2), want, 1e-9)
ok("cov @ [1,0]", list((S@np.array([1.,0.])).round(2)), [28.8, 82.35])
Fs = c[["orders","revenue","avg_order_value","avg_discount_pct","storage_share","kitchen_share","industrial_share"]].to_numpy(float)
Fs = (Fs-Fs.mean(0))/Fs.std(0); ok("std cov diagonal", round(float(np.cov(Fs, rowvar=False)[0,0]),3), 1.045, 1e-9)
# Story (In the real world): Riverstone's full CRM, 2025 leads created by 2 October 2025 (Chapter 36's 90-day rule)
import subprocess
CRM = D.parent / "crm" / "leads.csv"
if not CRM.exists():
    subprocess.run(["python3", str(D.parent / "generate_riverstone_crm.py")], check=True)
cl = pd.read_csv(CRM, parse_dates=["created_at"]); cl["k"] = cl["email"].str.lower().str.strip()
cl = cl.sort_values("created_at"); gap = cl.groupby("k")["created_at"].diff(); cl = cl[~(gap.notna() & (gap <= pd.Timedelta(days=2)))]
ok("2025 enquiries per month", round((cl.created_at.dt.year == 2025).sum()/12), 394)
m = cl[(cl.created_at.dt.year == 2025) & (cl.created_at <= pd.Timestamp("2025-12-31 23:59") - pd.Timedelta(days=90))]
wins = int((m.status == "Won").sum()); r = wins/len(m)
ok("2025 matured leads", len(m), 3410); ok("2025 wins", wins, 250); ok("2025 win rate", round(r,3), 0.073, 1e-9)
ok("always-no accuracy", round(1-r,3), 0.927, 1e-9); ok("always-no right", len(m)-wins, 3160)
ok("base-rate log loss", round(-(r*log(r)+(1-r)*log(1-r)),2), 0.26, 1e-9)
per_week = (cl.created_at.dt.year == 2025).sum()/52
ok("3-week pilot leads", round(3*per_week, -1), 270.0, 0.02); ok("3-week pilot wins", round(3*per_week*r), 20); ok("3-month pilot wins", round(3*394*r), 87)
print("FAILED:" if fails else "All checks passed.", fails)
raise SystemExit(1 if fails else 0)
