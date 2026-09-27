# Generates the SVG figures for Chapter 30. Run: python3 make_figs30.py
# Numbers come from the chapter's runs on companion/ch30 (seed 30).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_ci():
    o=[text(30,32,"The same lift, four sample sizes: what a confidence interval buys",14,INK,"bold",family=HEAD)]
    rows=[("2,500 per group","+0.55 pp","-0.56","+1.66",-0.56,1.66,RED,"could be a loss"),
          ("10,000 per group","+0.55 pp","-0.00","+1.10",-0.00,1.10,ORANGE,"still touches zero"),
          ("25,000 per group","+0.55 pp","+0.20","+0.90",0.20,0.90,GREEN,"the test as run"),
          ("100,000 per group","+0.55 pp","+0.37","+0.73",0.37,0.73,GREEN,"precise, and expensive")]
    x0,x1=300,900; lo,hi=-1.0,2.0
    def px(v): return x0+(v-lo)/(hi-lo)*(x1-x0)
    o.append(path(f"M{px(0)},70 V300",stroke=MUTED,sw=1.5,dash="4,4"))
    o.append(text(px(0),64,"no difference",11.5,MUTED,anchor="middle"))
    y=95
    for label,est,l,h,lov,hiv,c,note in rows:
        o.append(text(40,y+5,label,12,INK))
        o.append(path(f"M{px(lov)},{y} H{px(hiv)}",stroke=c,sw=3))
        for v in (lov,hiv): o.append(path(f"M{px(v)},{y-7} V{y+7}",stroke=c,sw=3))
        o.append(rect(px(0.55)-4,y-4,8,8,fill=c,stroke=c,rx=4))
        o.append(text(px(hiv)+14,y+5,f"{l} to {h} pp — {note}",11.5,c))
        y+=55
    for v in (-1,0,1,2):
        o.append(path(f"M{px(v)},300 V306",stroke=MUTED,sw=1.2)); o.append(text(px(v),322,f"{v:+.0f} pp",11,MUTED,anchor="middle"))
    o.append(text(30,355,"Every row measured the same +0.55 percentage points. Only the sample size changed, and with it what you are entitled to say.",12,MUTED))
    return svg(1130,375,"".join(o))

def fig_power():
    o=[text(30,32,"Power: the chance of catching an effect that is really there",14,INK,"bold",family=HEAD)]
    # power curve for two proportions, baseline 3.9%, effect 0.5pp, alpha .05 (computed with statsmodels)
    pts=[(1000,0.087),(2500,0.144),(5000,0.241),(10000,0.426),(15000,0.584),(20000,0.708),(25000,0.801),
         (30000,0.867),(40000,0.944),(50000,0.978),(60000,0.991)]
    x0,y0,x1,y1=90,300,900,70
    def px(n): return x0+(n/60000)*(x1-x0)
    def py(p): return y0-(p)*(y0-y1)
    o.append(path(f"M{x0},{y0} H{x1}",stroke=MUTED,sw=1.4)); o.append(path(f"M{x0},{y0} V{y1-10}",stroke=MUTED,sw=1.4))
    for p in (0,0.2,0.4,0.6,0.8,1.0):
        o.append(path(f"M{x0-5},{py(p)} H{x1}",stroke=RULE,sw=0.8,dash="3,4")); o.append(text(x0-12,py(p)+4,f"{p:.0%}",11,MUTED,anchor="end"))
    for n in (0,10000,20000,30000,40000,50000,60000):
        o.append(text(px(n),y0+20,f"{n//1000}k",11,MUTED,anchor="middle"))
    d="M"+" L".join(f"{px(n)},{py(p)}" for n,p in pts)
    o.append(path(d,stroke=ACC,sw=2.5))
    o.append(path(f"M{x0},{py(0.8)} H{px(25000)}",stroke=GREEN,sw=1.6,dash="5,4"))
    o.append(path(f"M{px(25000)},{y0} V{py(0.8)}",stroke=GREEN,sw=1.6,dash="5,4"))
    o.append(rect(px(25000)-5,py(0.801)-5,10,10,fill=GREEN,stroke=GREEN,rx=5))
    o.append(text(px(27000),py(0.63),"25,000 per group: 80% power",12,GREEN,"bold"))
    o.append(text(px(8000),py(0.14),"at 5,000 per group the test",12,RED))
    o.append(text(px(8000),py(0.08),"misses this effect 3 times in 4",12,RED))
    o.append(text(495,y0+42,"visitors per group",12,INK,anchor="middle"))
    o.append(text(30,372,"Detecting +0.5 percentage points on a 3.9% baseline, at the 5% level. Halving the effect you want to catch costs four times the data.",12,MUTED))
    return svg(1040,392,"".join(o))

def fig_peeking():
    o=[text(30,32,"Peeking: what daily checks do to a test where nothing is different",14,INK,"bold",family=HEAD)]
    o.append(rect(40,70,460,150,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(60,100,"One planned look at the end",13,GREEN,"bold"))
    for i in range(20):
        c = RED if i < 1 else "#d8e3ea"
        o.append(rect(60+ (i%10)*42, 120+(i//10)*40, 34, 30, fill=c, stroke=RULE, rx=4))
    o.append(text(60,212,"1 in 20 tests calls a false winner: 5%",12,INK))
    o.append(rect(540,70,460,150,fill="#fbeaea",stroke=RED,sw=1.5,rx=8))
    o.append(text(560,100,"Looking every day for two weeks",13,RED,"bold"))
    for i in range(20):
        c = RED if i < 5 else "#d8e3ea"
        o.append(rect(560+(i%10)*42, 120+(i//10)*40, 34, 30, fill=c, stroke=RULE, rx=4))
    o.append(text(560,212,"5 in 20 call a false winner: 25.5%",12,INK))
    o.append(text(30,255,"Measured by simulation in section 30.10: 200 tests of two identical groups, 14 daily looks each, stopping at the first p < 0.05.",12,MUTED))
    o.append(text(30,277,"The p-value is only trustworthy for the look you promised in advance.",12,INK,"bold"))
    return svg(1040,300,"".join(o))

def fig_design():
    o=[text(30,32,"An experiment, in the order the decisions are made",14,INK,"bold",family=HEAD)]
    steps=[("Before","Question and change","the shorter enquiry form",ACC),
           ("Before","Primary metric + guardrails","enquiry rate per visitor; pages, value, orders",ACC),
           ("Before","MDE and sample size","0.5 pp → 25,000 per group",PURPLE),
           ("Before","Duration and stopping rule","two whole weeks, no interim decisions",PURPLE),
           ("During","Randomize and watch guardrails","50/50 by visitor",GREEN),
           ("After","Sample-ratio check","chi-square on group sizes — failed here",ORANGE),
           ("After","Primary metric with CI","+0.55 pp (0.19 to 0.91), p = 0.0026",GREEN),
           ("After","Effect size and decision","+14% relative; ship, fix the Safari tag",GREEN)]
    y=66
    for when,title,detail,c in steps:
        o.append(rect(30,y,120,40,fill="#f6f9fc",stroke=RULE,rx=6)); o.append(text(90,y+25,when,12,MUTED,"bold",anchor="middle"))
        o.append(rect(160,y,850,40,fill="#fff",stroke=c,sw=1.6,rx=6))
        o.append(text(180,y+25,title,12.5,c,"bold")); o.append(text(520,y+25,detail,12,INK))
        y+=48
    o.append(text(30,y+18,"Everything above the line is written down before a single visitor is randomized. That is what makes the numbers below it mean anything.",12,MUTED))
    return svg(1040,y+35,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig30-1-confidence-intervals.svg",fig_ci),("fig30-2-power-curve.svg",fig_power),
                    ("fig30-3-peeking.svg",fig_peeking),("fig30-4-experiment-order.svg",fig_design)]:
        open(name,"w").write(fn())
    print("ok30")
