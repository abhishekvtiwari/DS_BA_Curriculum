# Generates the SVG figures for Chapter 43. Run from figures/ after checks/ch43_check.py has written ch43_results.json.
import json, pathlib
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch43_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def dot(x,y,c,r=5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def poly(pts,c,sw=2.6): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=sw)

def fig_xor():
    o=[]; X0=100; Y0=340; W=280; H=280
    pts=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
    X=lambda a: X0+a*W; Y=lambda b: Y0-b*H
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    for v in [0,1]: o.append(text(X(v),Y0+22,str(v),12.5,MUTED,anchor="middle")); o.append(text(X0-14,Y(v)+4,str(v),12.5,MUTED,anchor="end"))
    for a,b,lab in pts:
        c = ORANGE if lab else ACC
        o.append(dot(X(a),Y(b),c,10)); o.append(text(X(a)+16,Y(b)+5,str(lab),13,c,"bold"))
    o.append(text(X0+W/2,40,"XOR: no single straight line separates them",14.5,INK,"bold",family=HEAD))
    o.append(text(X0+W/2,Y0+50,"Input 1",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-46}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-46} {Y0-H/2})">Input 2</text>')
    # try a few lines to show none separate cleanly
    for m,cc in [(0.5,PALE)]:
        pass
    o.append(line(X0-10,Y(0.5),X0+W+10,Y(0.5),RED,1.4,"5 4"))
    o.append(line(X0+W*0.5,Y0+15,X0+W*0.5,Y0-H-15,RED,1.4,"5 4"))
    o.append(text(X0+W+30,Y(0.5),"cuts orange from orange",11,RED))
    return svg(680,400,"".join(o))

def fig_transfer():
    o=[]; X0=110; Y0=340; W=680; H=280
    data = R["transfer_scratch"]
    ns = sorted(int(k) for k in data)
    X=lambda n: X0+(n-1)/29*W; Y=lambda v: Y0-(v-0.5)/0.5*H
    for v in [0.5,0.6,0.7,0.8,0.9,1.0]:
        o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.0%}",11.5,MUTED,anchor="end"))
    for n in ns: o.append(text(X(n),Y0+20,str(n),11.5,MUTED,anchor="middle"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2))
    transfer_pts=[(X(n),Y(data[str(n)][0])) for n in ns]; scratch_pts=[(X(n),Y(data[str(n)][1])) for n in ns]
    o.append(poly(transfer_pts,ACC)); o.append(poly(scratch_pts,ORANGE))
    for x,y in transfer_pts: o.append(dot(x,y,ACC,5))
    for x,y in scratch_pts: o.append(dot(x,y,ORANGE,5))
    o.append(text(X(ns[-1])+10,Y(data[str(ns[-1])][0]),"transfer (frozen features)",12.5,ACC,"bold"))
    o.append(text(X(ns[-1])+10,Y(data[str(ns[-1])][1])+18,"from scratch",12.5,ORANGE,"bold"))
    o.append(text(X0,40,"Transfer learning vs. training from scratch, by training-set size",14.5,INK,"bold",family=HEAD))
    o.append(text(X0+W/2,Y0+44,"Examples per class in the new task",12.5,INK,anchor="middle"))
    return svg(1000,420,"".join(o))

def fig_tabular():
    o=[]; X0=140; Y0=320; W=560; H=230
    tc = R["tabular_comparison"]
    methods = [("Logistic\nregression", tc["logistic"], ACC), ("Small neural\nnetwork", tc["network"], GREEN), ("Gradient\nboosting", tc["boosting"], ORANGE)]
    Y=lambda v: Y0-(v-0.5)/0.35*H
    for v in [0.5,0.6,0.7,0.8]:
        o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.2f}",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2))
    bw=W/3
    for i,(name,val,c) in enumerate(methods):
        x=X0+i*bw+bw*0.25
        o.append(rect(x,Y(val),bw*0.5,Y0-Y(val),fill=c,rx=3))
        o.append(text(x+bw*0.25,Y(val)-10,f"{val:.3f}",13,INK,"bold",anchor="middle"))
        for j,line_txt in enumerate(name.split("\n")):
            o.append(text(x+bw*0.25,Y0+24+j*16,line_txt,12,INK,anchor="middle"))
    o.append(text(X0,40,"Validation AUC on Riverstone churn (Chapter 37 data)",14.5,INK,"bold",family=HEAD))
    return svg(840,400,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig43-1-xor.svg",fig_xor),("fig43-2-transfer-learning.svg",fig_transfer),("fig43-3-tabular-comparison.svg",fig_tabular)]:
        open(name,"w").write(fn())
    print("ok")
