# Generates the SVG figures for Chapter 37. Run from figures/ after checks/ch37_check.py has written ch37_results.json.
import json, math, pathlib
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch37_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def dot(x,y,c,r=5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def poly(pts,c,sw=2.6,dash=None): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=sw,dash=dash)

def fig_lasso():
    o=[]; X0=100; Y0=380; W=680; H=300; data=R["lasso"]
    lo,hi=math.log10(0.001),math.log10(0.2)
    X=lambda a: X0+(math.log10(a)-lo)/(hi-lo)*W
    Yk=lambda k: Y0-k/20*H; Yr=lambda r: Y0-(r-0.90)/0.07*H
    for a in [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2]:
        o.append(line(X(a),Y0,X(a),Y0-H,PALE)); o.append(text(X(a),Y0+20,f"{a:g}",11.5,MUTED,anchor="middle"))
    for k in [0,5,10,15,20]: o.append(text(X0-10,Yk(k)+4,str(k),11.5,ACC,anchor="end"))
    for r in [0.90,0.92,0.94,0.96]: o.append(text(X0+W+10,Yr(r)+4,f"{r:.2f}",11.5,GREEN))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2))
    o.append(poly([(X(a),Yk(k)) for a,k,_ in data],ACC)); o.append(poly([(X(a),Yr(r)) for a,_,r in data],GREEN))
    for a,k,r in data: o.append(dot(X(a),Yk(k),ACC)); o.append(dot(X(a),Yr(r),GREEN))
    o.append(text(X0+W/2,Y0+44,"Lasso alpha (log scale)",12.5,INK,anchor="middle"))
    o.append(text(X0-10,Y0-H-18,"Features kept",13,ACC,"bold",anchor="start")); o.append(text(X0+W,Y0-H-18,"Test R²",13,GREEN,"bold",anchor="end"))
    return svg(900,440,"".join(o))

def fig_depth():
    o=[]; X0=100; Y0=380; W=680; H=300; data=R["depth"]
    xs=list(range(len(data)))
    X=lambda i: X0+i/(len(data)-1)*W; Y=lambda v: Y0-(v-0.5)/0.5*H
    for v in [0.5,0.6,0.7,0.8,0.9,1.0]:
        o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.1f}",11.5,MUTED,anchor="end"))
    for i,(d,_,_) in enumerate(data): o.append(text(X(i),Y0+20,"none" if d==30 else str(d),11.5,MUTED,anchor="middle"))
    o.append(poly([(X(i),Y(t)) for i,(_,t,_) in enumerate(data)],ORANGE)); o.append(poly([(X(i),Y(v)) for i,(_,_,v) in enumerate(data)],ACC))
    for i,(_,t,v) in enumerate(data): o.append(dot(X(i),Y(t),ORANGE)); o.append(dot(X(i),Y(v),ACC))
    best=max(range(len(data)),key=lambda i:data[i][2])
    o.append(text(X(best),Y(data[best][2])+26,f"best validation {data[best][2]:.3f}",12.5,ACC,"bold",anchor="middle"))
    o.append(text(X(len(data)-1)-8,Y(data[-1][1])+22,"training",13,ORANGE,"bold",anchor="end"))
    o.append(text(X(len(data)-1)-8,Y(data[-1][2])-12,"validation",13,ACC,"bold",anchor="end"))
    o.append(text(X0+W/2,Y0+44,"Maximum tree depth",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-55}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-55} {Y0-H/2})">AUC</text>')
    return svg(900,440,"".join(o))

def fig_curves():
    o=[]; H=260; W=380; Y0=360
    for p,(key,title) in enumerate([("logistic","Logistic regression"),("boosting","Gradient boosting (tuned)")]):
        X0=90+p*470; n,tr,cv=R["curves"][key]
        X=lambda v: X0+(v-0)/3300*W; Y=lambda v: Y0-(v-0.7)/0.3*H
        for v in [0.7,0.8,0.9,1.0]:
            o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.1f}",11.5,MUTED,anchor="end"))
        for v in [500,1500,2500]: o.append(text(X(v),Y0+20,f"{v:,}",11.5,MUTED,anchor="middle"))
        o.append(poly([(X(a),Y(b)) for a,b in zip(n,tr)],ORANGE)); o.append(poly([(X(a),Y(b)) for a,b in zip(n,cv)],ACC))
        for a,b,c in zip(n,tr,cv): o.append(dot(X(a),Y(b),ORANGE)); o.append(dot(X(a),Y(c),ACC))
        o.append(text(X0,Y0-H-20,title,14.5,INK,"bold",family=HEAD))
        o.append(text(X(n[-1]),Y(tr[-1])-12,f"train {tr[-1]:.3f}",12,ORANGE,"bold",anchor="end"))
        o.append(text(X(n[-1]),Y(cv[-1])+22,f"CV {cv[-1]:.3f}",12,ACC,"bold",anchor="end"))
        o.append(text(X0+W/2,Y0+44,"Training rows",12.5,INK,anchor="middle"))
    return svg(960,420,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig37-1-lasso-path.svg",fig_lasso),("fig37-2-tree-depth.svg",fig_depth),("fig37-3-learning-curves.svg",fig_curves)]:
        open(name,"w").write(fn())
    print("ok")
