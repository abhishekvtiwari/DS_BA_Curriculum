# Generates the SVG figures for Chapter 57. Run: python3 make_figs57.py
# Every number was measured by the chapter's own code (companion/ch57).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_upgrade():
    o=[text(30,32,"The day the provider changed the model behind the same name",14,INK,"bold",family=HEAD)]
    rows=[("pinned model v1, our parser",47,0,GREEN,"the system as it ran on Friday"),
          ("new model v2, same parser",0,60,RED,"every reply unparseable: nothing loads"),
          ("new model v2, tolerant parser",47,0,GREEN,"strip comments, normalize the date: 20 minutes")]
    y=80
    for label,correct,bad,c,note in rows:
        o.append(text(290,y+22,label,12.5,INK,"bold",anchor="end"))
        o.append(rect(310,y,520,34,fill="#f6f9fc",stroke=RULE,rx=5))
        o.append(rect(310,y,520*correct/60,34,fill=c,stroke=c,rx=5))
        if bad:
            o.append(text(322,y+22,f"{bad} of 60 unparseable",12,RED,"bold"))
        else:
            o.append(text(322,y+22,f"{correct} of 60 correct",12,"#ffffff","bold"))
        o.append(text(848,y+22,note,11.5,MUTED))
        y+=58
    o.append(rect(310,y+8,520,54,fill="#fdf3dc",stroke=PK,rx=6))
    o.append(text(570,y+30,"The model was not worse.",12.5,INK,"bold",anchor="middle"))
    o.append(text(570,y+50,"A contract we assumed and never enforced had changed.",12,INK,anchor="middle"))
    o.append(text(30,y+92,"Nightly golden-set runs turn this into a Saturday-night build failure. Without them, it is a Monday morning with no orders in the ERP.",12,MUTED))
    return svg(1040,y+112,"".join(o))

def fig_drift():
    o=[text(30,32,"Monitoring a system with no accuracy: refusals as the early warning",14,INK,"bold",family=HEAD)]
    weeks=list(range(1,9)); refusal=[0.15,0.18,0.20,0.15,0.32,0.25,0.42,0.38]
    conf=[0.587,0.577,0.577,0.584,0.573,0.545,0.450,0.481]
    x0,x1,y0,y1=110,880,300,80
    def px(w): return x0+(w-1)*(x1-x0)/7
    def py(v): return y0-v/0.5*(y0-y1)
    for v in (0,0.1,0.2,0.3,0.4,0.5):
        o.append(path(f"M{x0},{py(v)} H{x1}",stroke=RULE,sw=0.7,dash="3,4")); o.append(text(x0-10,py(v)+4,f"{v:.0%}",11,MUTED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(w)},{py(v)}" for w,v in zip(weeks,refusal)),stroke=ORANGE,sw=2.6))
    for w,v in zip(weeks,refusal):
        o.append(rect(px(w)-4,py(v)-4,8,8,fill=ORANGE,stroke=ORANGE,rx=4))
    def pyc(v): return y0-(v-0.40)/0.25*(y0-y1)
    o.append(path("M"+" L".join(f"{px(w)},{pyc(v)}" for w,v in zip(weeks,conf)),stroke=PURPLE,sw=2.2,dash="6,4"))
    o.append(path(f"M{px(5)},{y1-10} V{y0}",stroke=RED,sw=1.6,dash="5,4"))
    o.append(text(px(5)+8,y1+4,"week 5: customers start asking about a new product line",11.5,RED,"bold"))
    o.append(text(x0,y1-14,"refusal rate (solid)",12,ORANGE,"bold"))
    o.append(text(x0+210,y1-14,"mean retrieval confidence (dashed)",12,PURPLE,"bold"))
    for w in weeks:
        o.append(text(px(w),y0+20,f"wk {w}",11,MUTED,anchor="middle"))
    o.append(rect(30,y0+40,980,58,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(48,y0+62,"Nothing changed: same prompt, same model, same code. Customers started asking about something nobody had written down.",12,INK))
    o.append(text(48,y0+84,"The fix is three documents, not a model change. The assistant's own honesty is the monitor.",12,GREEN,"bold"))
    return svg(1040,y0+116,"".join(o))

def fig_resilience():
    o=[text(30,32,"Cost and failure: the two things that decide whether a feature survives",14,INK,"bold",family=HEAD)]
    o.append(rect(30,70,480,210,fill="#fff",stroke=GREEN,sw=1.8,rx=8))
    o.append(text(50,98,"Caching, on a realistic day of 300 requests",12.5,GREEN,"bold"))
    bars=[("no cache","Rs 23.62",1.0,MUTED),("exact-match cache","Rs 4.52",4.52/23.62,GREEN)]
    y=120
    for label,value,share,c in bars:
        o.append(text(50,y+20,label,12,INK))
        o.append(rect(200,y,280,28,fill="#f6f9fc",stroke=RULE,rx=4))
        o.append(rect(200,y,280*share,28,fill=c,stroke=c,rx=4))
        o.append(text(210,y+19,value,12,"#ffffff" if share>0.3 else INK,"bold"))
        y+=46
    o.append(text(50,y+16,"81% hit rate, 81% of the cost gone,",12,INK,"bold"))
    o.append(text(50,y+36,"and not one prompt improved.",12,INK))
    o.append(rect(530,70,480,210,fill="#fff",stroke=ACC,sw=1.8,rx=8))
    o.append(text(550,98,"Fallback, with the provider failing 20% of calls",12.5,ACC,"bold"))
    routes=[("primary model",48,GREEN),("cheaper fallback",9,ACC),("failed: sent to a human",3,RED)]
    y=120
    for label,count,c in routes:
        o.append(text(550,y+20,label,12,INK))
        o.append(rect(790,y,200,28,fill="#f6f9fc",stroke=RULE,rx=4))
        o.append(rect(790,y,200*count/60,28,fill=c,stroke=c,rx=4))
        o.append(text(996,y+19,f"{count}",12,INK,"bold",anchor="end"))
        y+=46
    o.append(text(550,y+16,"95% of emails served through",12,INK,"bold"))
    o.append(text(550,y+36,"29 provider errors.",12,INK))
    o.append(text(30,312,"Neither of these is modelling work, and together they decide the bill and the uptime. Build them before tuning a prompt.",12,MUTED))
    return svg(1040,334,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig57-1-provider-upgrade.svg",fig_upgrade),("fig57-2-topic-drift.svg",fig_drift),
                    ("fig57-3-cost-and-failure.svg",fig_resilience)]:
        open(name,"w").write(fn())
    print("ok57")
