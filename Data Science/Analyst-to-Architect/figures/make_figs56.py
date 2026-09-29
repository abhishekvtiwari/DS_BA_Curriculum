# Generates the SVG figures for Chapter 56. Run: python3 make_figs56.py
# Numbers come from the chapter's own measurements on companion/ch56 (seed 56; scikit-learn 1.9.1):
# PSI of image brightness against weeks 0-7, and weekly recall of defect-v1 at threshold 0.1 (section 56.8).
# Canvases are 720 px wide and print at 493.2 pt, so the smallest font here (10.5 px) prints at 7.2 pt.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=720

WEEKS=list(range(24))
PSI=[0.022,0.012,0.007,0.007,0.016,0.019,0.004,0.011,0.065,0.330,0.614,1.216,1.842,2.959,3.327,4.413,
     4.107,4.144,4.411,4.219,3.981,4.126,4.886,4.246]
RECALL=[0.97,0.92,0.97,0.98,1.00,0.95,0.95,1.00,0.94,0.97,0.98,0.96,1.00,0.93,0.98,0.98,
        0.80,0.81,0.86,0.79,0.86,0.86,0.90,0.87]


def fig_drift_vs_decay():
    o=[text(16,26,"Input drift is not model decay: six months on Riverstone's line",14,INK,"bold",family=HEAD)]
    x0,x1=62,700
    def px(w): return x0+w*(x1-x0)/23
    # top panel: PSI
    y0,y1=196,78
    def pyd(v): return y0-min(v,5)/5*(y0-y1)
    o.append(text(16,56,"PSI of image brightness (input drift)",12,ORANGE,"bold"))
    for v in (0,1,2,3,4,5):
        o.append(path(f"M{x0},{pyd(v)} H{x1}",stroke=RULE,sw=0.7,dash="3,4")); o.append(text(x0-8,pyd(v)+4,str(v),11,MUTED,anchor="end"))
    o.append(path(f"M{x0},{pyd(0.25)} H{x1}",stroke=RED,sw=1.3,dash="6,4"))
    o.append(text(x1,pyd(0.25)+15,"0.25 = “investigate”",11,RED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(w):.1f},{pyd(v):.1f}" for w,v in zip(WEEKS,PSI)),stroke=ORANGE,sw=2.4))
    # bottom panel: recall, axis from 0.7
    y2a,y2b=392,262
    def pyr(v): return y2a-(v-0.7)/0.3*(y2a-y2b)
    o.append(text(16,244,"recall: share of real defects caught (model decay)",12,PURPLE,"bold"))
    for v in (0.7,0.8,0.9,1.0):
        o.append(path(f"M{x0},{pyr(v):.1f} H{x1}",stroke=RULE,sw=0.7,dash="3,4")); o.append(text(x0-8,pyr(v)+4,f"{v:.1f}",11,MUTED,anchor="end"))
    o.append(path("M"+" L".join(f"{px(w):.1f},{pyr(v):.1f}" for w,v in zip(WEEKS,RECALL)),stroke=PURPLE,sw=2.4))
    for w,v in zip(WEEKS,RECALL):
        o.append(f'<circle cx="{px(w):.1f}" cy="{pyr(v):.1f}" r="2.6" fill="{PURPLE}"/>')
    # the two events, labelled in words (not by colour alone)
    for w,label,c in ((8,"week 8: new lamps (late April)",ACC),(16,"week 16: new mould (late June)",RED)):
        o.append(path(f"M{px(w):.1f},{y1-12} V{y2a}",stroke=c,sw=1.5,dash="5,4"))
        o.append(text(px(w)+6,y1-2,label,11,c,"bold"))
    for w in range(0,24,4):
        o.append(text(px(w),y2a+18,f"week {w}",11,MUTED,anchor="middle"))
    o.append(text(px(23),y2a+18,"23",11,MUTED,anchor="middle"))
    o.append(rect(16,y2a+32,688,62,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(28,y2a+52,"Weeks 8-15: PSI reaches 4.4, seventeen times “investigate”; recall 96.5%, as before (96.8%).",11.5,INK))
    o.append(text(28,y2a+72,"Weeks 16-23: PSI is flat and recall falls to 84.4% (18 of 69 flash parts caught).",11.5,INK,"bold"))
    o.append(text(28,y2a+88,"The alarm that cried wolf in late April stayed silent in late June.",10.5,MUTED))
    return svg(W,y2a+104,"".join(o))


def fig_layers():
    o=[text(16,26,"Three layers of monitoring, and what each one can see",14,INK,"bold",family=HEAD)]
    def row(y,h,name,question,signal,delay,action,c):
        o.append(rect(16,y,688,h,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(text(30,y+22,name,12.5,c,"bold",family=MONO))
        o.append(text(30,y+40,question,11,MUTED))
        o.append(text(250,y+22,signal,11.5,INK))
        o.append(text(250,y+40,f"delay: {delay}",11,MUTED))
        o.append(text(692,y+22,action,11.5,INK,"bold",anchor="end"))
    row(44,52,"1 service","is it up and fast?","uptime, error rate, p95 latency, memory","seconds","page a human",ACC)
    row(104,52,"2 input","does the data look like training?","feature distributions, PSI, KS, missing rates","minutes","daily digest",ORANGE)
    # layer 3: one layer, two streams
    y=164
    o.append(rect(16,y,688,150,fill="#fbf8fd",stroke=PURPLE,sw=1.6,rx=7))
    o.append(text(30,y+22,"3 output and outcome",12.5,PURPLE,"bold",family=MONO))
    o.append(text(250,y+22,"is it still right? one layer, two streams:",11.5,MUTED))
    o.append(rect(30,y+34,660,50,fill="#fff",stroke=PURPLE,sw=1.1,rx=6))
    o.append(text(42,y+54,"fast proxy (output)",11.5,PURPLE,"bold"))
    o.append(text(236,y+54,"share of parts predicted defective, per shift",11.5,INK))
    o.append(text(236,y+72,"delay: hours · needs no labels · measures change, not correctness",11,MUTED))
    o.append(text(678,y+54,"daily digest",11.5,INK,"bold",anchor="end"))
    o.append(rect(30,y+92,660,50,fill="#fff",stroke=GREEN,sw=1.1,rx=6))
    o.append(text(42,y+112,"slow truth (outcome)",11.5,GREEN,"bold"))
    o.append(text(236,y+112,"recall from a 2% audit of parts the model passed",11.5,INK))
    o.append(text(236,y+130,"delay: days to weeks · the only stream that counts misses",11,MUTED))
    o.append(text(678,y+112,"weekly review",11.5,INK,"bold",anchor="end"))
    y=334
    o.append(text(16,y,"The flash defect was invisible to the service and input layers, hidden in the fast proxy (misses",11.5,MUTED))
    o.append(text(16,y+18,"and extra false alarms cancelled out), and plain only in the audited outcome. Ground truth is late:",11.5,MUTED))
    o.append(text(16,y+36,"plan for it rather than hoping.",11.5,INK,"bold"))
    return svg(W,y+50,"".join(o))


def fig_lifecycle():
    o=[text(16,26,"The five things that must be versioned, and where they travel",14,INK,"bold",family=HEAD)]
    items=[("data","6,000 images,","hash 64712189",ACC),("features","conv108-v1:","108 features",ACC),
           ("code","train.py at","a Git commit",PURPLE),("artifact","defect_v1.joblib","95 kB",GREEN),
           ("config","threshold 0.1,","in metadata",ORANGE)]
    bw,gap,x=122,19,16
    for i,(title,l1,l2,c) in enumerate(items):
        o.append(rect(x,46,bw,78,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(text(x+bw/2,68,title,12.5,c,"bold",anchor="middle"))
        o.append(text(x+bw/2,90,l1,10.5,INK,anchor="middle",family=MONO))
        o.append(text(x+bw/2,107,l2,10.5,INK,anchor="middle",family=MONO))
        if i<4:
            ax=x+bw
            o.append(path(f"M{ax+2},85 H{ax+gap-3}",stroke=INK,sw=1.6)); o.append(path(f"M{ax+gap-8},80 L{ax+gap-2},85 L{ax+gap-8},90",stroke=INK,sw=1.6))
        x+=bw+gap
    o.append(rect(16,140,688,62,fill="#e2f3ee",stroke=GREEN,sw=1.4,rx=7))
    o.append(text(360,161,"one artifact carries the model AND its metadata, so a rollback restores",11.5,INK,anchor="middle"))
    o.append(text(360,177,"both the weights and the decision boundary",11.5,INK,anchor="middle"))
    o.append(text(360,194,"rollback = swap the file (or move the registry alias), restart, and time it",11,GREEN,"bold",anchor="middle"))
    o.append(text(16,226,"If any one of the five is missing, you cannot reproduce the model, compare it with its successor,",11.5,MUTED))
    o.append(text(16,244,"or explain a decision six months later.",11.5,MUTED))
    return svg(W,258,"".join(o))


if __name__=="__main__":
    for name,fn in [("fig56-1-drift-vs-decay.svg",fig_drift_vs_decay),("fig56-2-monitoring-layers.svg",fig_layers),
                    ("fig56-3-versioning.svg",fig_lifecycle)]:
        open(name,"w").write(fn())
    print("ok56")
