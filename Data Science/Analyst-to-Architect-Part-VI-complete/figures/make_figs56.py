# Generates the SVG figures for Chapter 56. Run: python3 make_figs56.py
# Numbers come from the chapter's own measurements on companion/ch56 (seed 56).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

WEEKS=list(range(24))
PSI=[0.022,0.012,0.007,0.007,0.016,0.019,0.004,0.011,0.065,0.330,0.614,1.216,1.842,2.959,3.327,4.413,
     4.107,4.144,4.411,4.219,3.981,4.126,4.886,4.246]
RECALL=[1.00,0.95,0.97,1.00,1.00,0.98,0.95,1.00,0.94,0.97,0.98,0.96,0.97,0.98,0.98,0.98,
        0.80,0.82,0.88,0.79,0.81,0.86,0.87,0.87]

def fig_drift_vs_decay():
    o=[text(30,32,"Input drift is not model decay: six months on Riverstone's line",14,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=90,960,210,70
    def px(w): return x0+w*(x1-x0)/23
    def pyd(v): return y0-min(v,5)/5*(y0-y1)
    o.append(text(30,60,"PSI on image brightness",12,ORANGE,"bold"))
    for v in (0,1,2,3,4,5):
        o.append(path(f"M{x0},{pyd(v)} H{x1}",stroke=RULE,sw=0.7,dash="3,4")); o.append(text(x0-10,pyd(v)+4,str(v),11,MUTED,anchor="end"))
    o.append(path(f"M{x0},{pyd(0.25)} H{x1}",stroke=RED,sw=1.4,dash="6,4"))
    o.append(text(x1-4,pyd(0.25)-6,"0.25 = \u201cinvestigate\u201d",11,RED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(w)},{pyd(v)}" for w,v in zip(WEEKS,PSI)),stroke=ORANGE,sw=2.6))
    y2a,y2b=400,250
    def pyr(v): return y2a-(v-0.75)/0.3*(y2a-y2b)
    o.append(text(30,238,"recall (share of defects caught)",12,PURPLE,"bold"))
    for v in (0.8,0.9,1.0):
        o.append(path(f"M{x0},{pyr(v)} H{x1}",stroke=RULE,sw=0.7,dash="3,4")); o.append(text(x0-10,pyr(v)+4,f"{v:.1f}",11,MUTED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(w)},{pyr(v)}" for w,v in zip(WEEKS,RECALL)),stroke=PURPLE,sw=2.6))
    for w,label,c in ((8,"week 8: new lamps",ACC),(16,"week 16: new mould",RED)):
        o.append(path(f"M{px(w)},{y1-6} V{y2a}",stroke=c,sw=1.6,dash="5,4"))
        o.append(text(px(w)+8,y1+6,label,11.5,c,"bold"))
    for w in range(0,24,4):
        o.append(text(px(w),y2a+20,f"wk {w}",11,MUTED,anchor="middle"))
    o.append(rect(30,y2a+38,980,64,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(48,y2a+60,"Weeks 8-15: PSI reaches 4.4, seventeen times the \u201cinvestigate\u201d threshold, and recall never drops below 0.94.",12,INK))
    o.append(text(48,y2a+82,"Weeks 16-23: PSI is flat and recall falls fifteen points. The alarm that cried wolf in May stayed silent in July.",12,INK,"bold"))
    return svg(1040,y2a+120,"".join(o))

def fig_layers():
    o=[text(30,32,"Three layers of monitoring, and what each one can see",14,INK,"bold",family=HEAD)]
    rows=[("service","is it up and fast?","uptime, error rate, p95 latency, memory","seconds","page a human",ACC),
          ("input","does the data look like training?","feature distributions, PSI, KS, missing rates","minutes","daily digest",ORANGE),
          ("output","what is it saying?","predicted-defective rate per shift vs the QC tally","hours","daily digest",PURPLE),
          ("outcome","is it still right?","recall from a 2% audit of parts the model passed","days to weeks","weekly review",GREEN)]
    y=72
    for name,question,signal,delay,action,c in rows:
        o.append(rect(30,y,980,66,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(52,y+28,name,13,c,"bold",family=MONO)); o.append(text(52,y+50,question,11.5,MUTED))
        o.append(text(300,y+28,signal,12,INK)); o.append(text(300,y+50,f"delay: {delay}",11.5,MUTED))
        o.append(text(990,y+28,action,12,INK,"bold",anchor="end"))
        y+=78
    o.append(text(30,y+18,"The flash defect was invisible to the first three layers and obvious to the fourth, which is the slowest and the only one",12,MUTED))
    o.append(text(30,y+38,"that measures whether the model is still right. Ground truth is late; plan for it rather than hoping.",12,INK))
    return svg(1040,y+60,"".join(o))

def fig_lifecycle():
    o=[text(30,32,"The five things that must be versioned, and where they travel",14,INK,"bold",family=HEAD)]
    items=[(40,"data","6,000 images\nhash 1e86c528",ACC),(230,"features","108 convolution\nfeatures, in Git",ACC),
           (420,"code","train.py at a\ncommit hash",PURPLE),(610,"artifact","defect_v1.joblib\n96 kB",GREEN),
           (800,"config","threshold 0.1,\nin the metadata",ORANGE)]
    for x,title,detail,c in items:
        o.append(rect(x,70,170,84,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+85,96,title,12.5,c,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+85,118+i*16,line,11,MUTED,anchor="middle",family=MONO))
        if x<800:
            o.append(path(f"M{x+170},112 H{x+226}",stroke=INK,sw=1.8)); o.append(path(f"M{x+218},106 L{x+228},112 L{x+218},118",stroke=INK,sw=1.8))
    o.append(rect(40,180,930,52,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=8))
    o.append(text(505,202,"one artifact carries the model AND its metadata, so a rollback restores both the weights and the decision boundary",12,INK,anchor="middle"))
    o.append(text(505,222,"rollback = swap the file, restart, four minutes \u2014 timed on a quiet afternoon, written in the runbook",12,GREEN,"bold",anchor="middle"))
    o.append(text(30,262,"If any one of the five is missing, you cannot reproduce the model, compare it with its successor, or explain a decision six months later.",12,MUTED))
    return svg(1040,286,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig56-1-drift-vs-decay.svg",fig_drift_vs_decay),("fig56-2-monitoring-layers.svg",fig_layers),
                    ("fig56-3-versioning.svg",fig_lifecycle)]:
        open(name,"w").write(fn())
    print("ok56")
