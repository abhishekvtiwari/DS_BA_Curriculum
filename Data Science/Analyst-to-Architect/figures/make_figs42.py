# Generates the SVG figures for Chapter 42. Run from figures/ after checks/ch42_check.py has written ch42_results.json.
import json, pathlib
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch42_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)

def fig_compare():
    o=[]; X0=140; Y0=380; W=680; H=280
    S = R["summary"]
    methods = [("Popularity", S["popularity"], MUTED), ("Item-based CF", S["item_cf"], ACC),
               ("SVD (4 factors)", S["svd"][0][1:], GREEN), ("SVD (12 factors)", S["svd"][2][1:], RED),
               ("ALS (8 factors)", S["als"][0][1:], PURPLE), ("ALS (16 factors)", S["als"][1][1:], RED),
               ("Content-based", S["content"], ORANGE), ("Hybrid", S["hybrid"], "#8a6d3b")]
    Y=lambda v: Y0-(v-0)/0.8*H
    for v in [0,0.2,0.4,0.6,0.8]:
        o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.0%}",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2))
    bw=W/len(methods)
    for i,(name,(p,n),c) in enumerate(methods):
        x=X0+i*bw+bw*0.2
        o.append(rect(x,Y(p),bw*0.6,Y0-Y(p),fill=c,rx=3))
        o.append(text(x+bw*0.3,Y(p)-8,f"{p:.1%}",11.5,INK,"bold",anchor="middle"))
        o.append(text(x+bw*0.3,Y0+18,name,10.5,INK,anchor="middle"))
        o.append(text(x+bw*0.3,Y0+32,f"NDCG {n:.2f}",10,MUTED,anchor="middle"))
    o.append(text(X0,40,"Precision@5, leave-one-out evaluation",15,INK,"bold",family=HEAD))
    return svg(1000,460,"".join(o))

def fig_segment():
    o=[]; segs = R["segment_top"]; names = R["names"]
    X0=80; Y0=60; rowh=100
    for i,(seg,items) in enumerate(segs.items()):
        y = Y0 + i*rowh
        o.append(text(X0,y,seg,14,INK,"bold",family=HEAD))
        for j,(pid,share) in enumerate(items.items()):
            bx = X0+140+j*260
            w = share*220
            o.append(rect(bx,y-16,w,22,fill=[ACC,GREEN,ORANGE][i],rx=3))
            o.append(text(bx+4,y+38,f"{names[pid]}",12,INK))
            o.append(text(bx+w+8,y-1,f"{share:.0%}",12,INK,"bold"))
    return svg(1000,Y0+3*rowh,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig42-1-method-comparison.svg",fig_compare),("fig42-2-segment-preferences.svg",fig_segment)]:
        open(name,"w").write(fn())
    print("ok")
