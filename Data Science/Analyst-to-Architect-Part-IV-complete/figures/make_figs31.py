# Generates the SVG figures for Chapter 31. Run: python3 make_figs31.py
# Data comes from companion/ch31/causal_data (seed 31); the series below were read from those files.
from make_figs import *
import csv, math, pathlib
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
DATA = pathlib.Path(__file__).resolve().parents[1] / "companion" / "ch31" / "causal_data"

def panel_series():
    rows = list(csv.DictReader(open(DATA / "region_month.csv")))
    months = sorted({r["month"] for r in rows})
    north = [math.log(int(r["orders"])) for m in months for r in rows if r["month"] == m and r["region"] == "North"]
    others = [sum(math.log(int(r["orders"])) for r in rows if r["month"] == m and r["region"] != "North") / 3
              for m in months]
    return months, north, others

def fig_parallel():
    months, north, others = panel_series()
    o=[text(30,32,"North against the other regions: parallel, then a step",14,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=80,980,320,70
    lo,hi=7.2,8.1
    def px(i): return x0+i*(x1-x0)/(len(months)-1)
    def py(v): return y0-(v-lo)/(hi-lo)*(y0-y1)
    for v in (7.2,7.4,7.6,7.8,8.0):
        o.append(path(f"M{x0},{py(v)} H{x1}",stroke=RULE,sw=0.8,dash="3,4")); o.append(text(x0-10,py(v)+4,f"{v:.1f}",11,MUTED,anchor="end"))
    change=months.index("2025-10-01")
    o.append(path(f"M{px(change)},{y1-10} V{y0}",stroke=RED,sw=1.8,dash="6,4"))
    o.append(text(px(change)+8,y1-14,"prices rise 6% in North",12,RED,"bold"))
    o.append(path("M"+" L".join(f"{px(i)},{py(v)}" for i,v in enumerate(others)),stroke=ACC,sw=2.4))
    o.append(path("M"+" L".join(f"{px(i)},{py(v)}" for i,v in enumerate(north)),stroke=PURPLE,sw=2.4))
    o.append(text(px(2),py(others[2])-14,"other regions (average)",12,ACC,"bold"))
    o.append(text(px(2),py(north[2])+20,"North",12,PURPLE,"bold"))
    for i,m in enumerate(months):
        if m.endswith("-01-01") or m.endswith("-07-01"):
            o.append(text(px(i),y0+20,m[:7],11,MUTED,anchor="middle"))
    o.append(text(30,y0+50,"Log of monthly orders. Before October 2025 the gap between the lines wanders without direction; after it, North sits about 7% lower and stays there.",12,MUTED))
    o.append(text(30,y0+70,"Difference-in-differences is the change in that gap: -7.0% (95% CI -10.1% to -3.9%). The true effect built into the data is -8%.",12,INK))
    return svg(1040,y0+90,"".join(o))

def fig_balance():
    o=[text(30,32,"Matching is only worth something if it balanced the groups",14,INK,"bold",family=HEAD)]
    rows=[("prior revenue (log)",0.635,0.002),("growth in 2024",0.082,-0.098),("years as customer",0.239,0.106),("propensity score",0.683,0.033)]
    x0,x1=340,940; lo,hi=-0.2,0.8
    def px(v): return x0+(v-lo)/(hi-lo)*(x1-x0)
    o.append(path(f"M{px(0)},70 V265",stroke=MUTED,sw=1.4))
    o.append(rect(px(-0.1),70,px(0.1)-px(-0.1),195,fill="#e2f3ee",stroke="none"))
    o.append(text(px(0),62,"0",11,MUTED,anchor="middle")); o.append(text(px(0.1)+6,62,"the 0.1 rule of thumb",11,GREEN))
    y=100
    for label,before,after in rows:
        o.append(text(40,y+5,label,12,INK))
        o.append(path(f"M{px(before)},{y} L{px(after)},{y}",stroke=RULE,sw=1.4,dash="4,3"))
        o.append(rect(px(before)-5,y-5,10,10,fill=RED,stroke=RED,rx=5))
        o.append(rect(px(after)-5,y-5,10,10,fill=GREEN,stroke=GREEN,rx=5))
        y+=45
    o.append(rect(60,285,14,14,fill=RED,stroke=RED,rx=7)); o.append(text(84,297,"before matching",12,INK))
    o.append(rect(260,285,14,14,fill=GREEN,stroke=GREEN,rx=7)); o.append(text(284,297,"after matching",12,INK))
    o.append(text(30,330,"Standardized mean difference: the gap between the groups in units of standard deviation. Prior revenue starts at 0.63 and ends at 0.00.",12,MUTED))
    return svg(1040,350,"".join(o))

def fig_rd():
    rows=list(csv.DictReader(open(DATA / "delivery_threshold.csv")))
    bins={}
    for r in rows:
        c=(float(r["order_value"])-25000)/1000
        if abs(c)<=5:
            b=math.floor(c*2)/2
            bins.setdefault(b,[]).append(int(r["repeat_within_90_days"]))
    pts=sorted((b, sum(v)/len(v)) for b,v in bins.items())
    o=[text(30,32,"Free delivery at ₹25,000: the estimate is the size of the step",14,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=90,960,300,70
    lo,hi=0.2,0.55
    def px(c): return x0+(c+5)/10*(x1-x0)
    def py(p): return y0-(p-lo)/(hi-lo)*(y0-y1)
    for p in (0.2,0.3,0.4,0.5):
        o.append(path(f"M{x0},{py(p)} H{x1}",stroke=RULE,sw=0.8,dash="3,4")); o.append(text(x0-10,py(p)+4,f"{p:.0%}",11,MUTED,anchor="end"))
    o.append(path(f"M{px(0)},{y1-10} V{y0}",stroke=RED,sw=1.8,dash="6,4"))
    o.append(text(px(0)+8,y1-14,"₹25,000: free delivery starts",12,RED,"bold"))
    for c,p in pts:
        col = PURPLE if c<0 else GREEN
        o.append(rect(px(c+0.25)-3,py(p)-3,6,6,fill=col,stroke=col,rx=3))
    o.append(path(f"M{px(-5)},{py(0.288)} L{px(-0.02)},{py(0.327)}",stroke=PURPLE,sw=2.4))
    o.append(path(f"M{px(0.02)},{py(0.40)} L{px(5)},{py(0.44)}",stroke=GREEN,sw=2.4))
    o.append(path(f"M{px(0)},{py(0.327)} V{py(0.40)}",stroke=ORANGE,sw=3))
    o.append(text(px(0.35),py(0.365),"+7.3 points",12,ORANGE,"bold"))
    for c in (-5,-2.5,0,2.5,5):
        o.append(text(px(c),y0+20,f"₹{25000+c*1000:,.0f}",11,MUTED,anchor="middle"))
    o.append(text(30,y0+48,"Each dot is the reorder rate for orders in a ₹500 band. The slope either side is the ordinary relationship between order size and reordering;",12,MUTED))
    o.append(text(30,y0+68,"only the jump at the line is caused by the rule. True effect built into the data: +6.0 points.",12,INK))
    return svg(1040,y0+88,"".join(o))

def fig_synth():
    months, north, others = panel_series()
    rows = list(csv.DictReader(open(DATA / "region_month.csv")))
    series = {r: [math.log(int(x["orders"])) for m in months for x in rows if x["month"] == m and x["region"] == r]
              for r in ("West", "South", "East")}
    w = {"West": 0.187, "South": 0.303, "East": 0.509}
    synth = [sum(w[r] * series[r][i] for r in w) for i in range(len(months))]
    o=[text(30,32,"Synthetic North: a blend of the other regions, built only from the months before the change",14,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=80,980,300,70
    lo,hi=7.35,7.85
    def px(i): return x0+i*(x1-x0)/(len(months)-1)
    def py(v): return y0-(v-lo)/(hi-lo)*(y0-y1)
    for v in (7.4,7.5,7.6,7.7,7.8):
        o.append(path(f"M{x0},{py(v)} H{x1}",stroke=RULE,sw=0.8,dash="3,4")); o.append(text(x0-10,py(v)+4,f"{v:.1f}",11,MUTED,anchor="end"))
    change=months.index("2025-10-01")
    o.append(rect(px(change),y1-10,x1-px(change),y0-y1+10,fill="#fdf3dc",stroke="none"))
    o.append(path(f"M{px(change)},{y1-10} V{y0}",stroke=RED,sw=1.8,dash="6,4"))
    o.append(text(px(change)+10,y1-14,"price rise",12,RED,"bold"))
    o.append(path("M"+" L".join(f"{px(i)},{py(v)}" for i,v in enumerate(synth)),stroke=ACC,sw=2.4,dash="6,4"))
    o.append(path("M"+" L".join(f"{px(i)},{py(v)}" for i,v in enumerate(north)),stroke=PURPLE,sw=2.4))
    o.append(text(px(1),py(north[1])+24,"North (real)",12,PURPLE,"bold"))
    o.append(text(x0+130,y1+6,"synthetic North = 0.19 West + 0.30 South + 0.51 East",12,ACC,"bold"))
    for i,m in enumerate(months):
        if m.endswith("-01-01") or m.endswith("-07-01"):
            o.append(text(px(i),y0+20,m[:7],11,MUTED,anchor="middle"))
    o.append(text(30,y0+48,"The weights were chosen to track North for the fifteen months before October 2025 (root mean squared error 0.043 in log orders).",12,MUTED))
    o.append(text(30,y0+68,"Everything in the shaded area is the estimate: an average gap of -6.6%, against a true effect of -8%.",12,INK))
    return svg(1040,y0+88,"".join(o))

def fig_choose():
    o=[text(30,32,"Which method, and what it costs you",14,INK,"bold",family=HEAD)]
    rows=[("Can you randomize?","Run the experiment (Chapter 30)","strongest evidence",GREEN),
          ("Is there a threshold rule?","Regression discontinuity","strong, but only near the cut-off",GREEN),
          ("Do you have before-and-after for both groups?","Difference-in-differences","needs parallel trends",ACC),
          ("Many untreated units, one treated?","Synthetic control","judge it by the pre-change fit",ACC),
          ("Only cross-sectional data, good covariates?","Matching / propensity scores","assumes nothing unmeasured",ORANGE),
          ("Something that shifts treatment but not the outcome?","Instrumental variables","exclusion is untestable",ORANGE),
          ("None of the above?","Describe, don't claim cause","say so plainly",RED)]
    y=70
    for question,method,caveat,c in rows:
        o.append(rect(30,y,420,44,fill="#f6f9fc",stroke=RULE,rx=6)); o.append(text(46,y+27,question,12,INK))
        o.append(path(f"M455,{y+22} H485",stroke=MUTED,sw=1.6)); o.append(path(f"M477,{y+16} L487,{y+22} L477,{y+28}",stroke=MUTED,sw=1.6))
        o.append(rect(495,y,515,44,fill="#fff",stroke=c,sw=1.8,rx=6))
        o.append(text(512,y+20,method,12.5,c,"bold")); o.append(text(512,y+37,caveat,11.5,MUTED))
        y+=52
    o.append(text(30,y+18,"Work down the list: the first row you can answer yes to is usually the strongest evidence available to you.",12,MUTED))
    return svg(1040,y+38,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig31-1-parallel-trends.svg",fig_parallel),("fig31-2-matching-balance.svg",fig_balance),
                    ("fig31-3-discontinuity.svg",fig_rd),("fig31-4-synthetic-control.svg",fig_synth),
                    ("fig31-5-which-method.svg",fig_choose)]:
        open(name,"w").write(fn())
    print("ok31")
