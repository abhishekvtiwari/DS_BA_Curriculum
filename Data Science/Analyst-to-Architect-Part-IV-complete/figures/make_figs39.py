# Generates the SVG figures for Chapter 39. Run from figures/ after checks/ch39_check.py has written ch39_results.json.
import json, pathlib
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch39_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def poly(pts,c,sw=2.6,dash=None): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=sw,dash=dash)
def dot(x,y,c,r=5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def axes(o,X0,Y0,W,H,xl,yl,xt,yt):
    for v in xt: o.append(line(X0+v*W,Y0,X0+v*W,Y0-H,PALE)); o.append(text(X0+v*W,Y0+20,f"{v:.1f}",11.5,MUTED,anchor="middle"))
    for v in yt: o.append(line(X0,Y0-v*H,X0+W,Y0-v*H,PALE)); o.append(text(X0-10,Y0-v*H+4,f"{v:.1f}",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(text(X0+W/2,Y0+44,xl,12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-48}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-48} {Y0-H/2})">{yl}</text>')

def fig_confusion():
    o=[]; X0=250; Y0=90; cw=170; ch=110
    cells=[("True positives",100,GREEN),("False positives",386,ORANGE),("False negatives",46,RED),("True negatives","1,693",ACC)]
    for i,(lab,v,c) in enumerate(cells):
        x=X0+(i%2)*cw; y=Y0+(i//2)*ch
        o.append(rect(x,y,cw-8,ch-8,fill=c,rx=6)); o.append(text(x+(cw-8)/2,y+42,str(v),26,"#fff","bold",anchor="middle",family=HEAD)); o.append(text(x+(cw-8)/2,y+70,lab,12,"#fff",anchor="middle"))
    o.append(text(X0+cw/2-4,Y0-14,"Actually won",13,INK,"bold",anchor="middle")); o.append(text(X0+cw+cw/2-4,Y0-14,"Actually lost",13,INK,"bold",anchor="middle"))
    o.append(text(X0-14,Y0+ch/2,"Predicted won",13,INK,"bold",anchor="end")); o.append(text(X0-14,Y0+ch/2-16,"(score ≥ 0.1)",11,MUTED,anchor="end"))
    o.append(text(X0-14,Y0+ch+ch/2,"Predicted lost",13,INK,"bold",anchor="end"))
    o.append(text(X0+2*cw+10,Y0+ch/2-8,"precision = 100 ÷ (100 + 386)",12.5,INK)); o.append(text(X0+2*cw+10,Y0+ch/2+12,"= 0.206",13,GREEN,"bold"))
    o.append(text(X0+cw/2-4,Y0+2*ch+16,"recall = 100 ÷ (100 + 46) = 0.685",12.5,INK,anchor="middle"))
    o.append(text(X0+cw+cw/2-4,Y0+2*ch+40,"specificity = 1,693 ÷ 2,079 = 0.814",12.5,INK,anchor="middle"))
    return svg(860,360,"".join(o))

def fig_roc_pr():
    o=[]; W=340; H=300; Y0=360
    X0=80; axes(o,X0,Y0,W,H,"False positive rate","Recall (true positive rate)",[0,.5,1],[0,.5,1])
    o.append(poly([(X0+a*W,Y0-b*H) for a,b in zip(R["fpr"],R["tpr"])],ACC)); o.append(line(X0,Y0,X0+W,Y0-H,MUTED,1.2,"6 5"))
    o.append(text(X0+W-10,Y0-H+20,"ROC-AUC 0.823",13,ACC,"bold",anchor="end")); o.append(text(X0+W*0.62,Y0-H*0.52,"chance",11.5,MUTED))
    X0=540; axes(o,X0,Y0,W,H,"Recall","Precision",[0,.5,1],[0,.5,1])
    o.append(poly([(X0+a*W,Y0-b*H) for a,b in zip(R["rec"],R["prec"])],ORANGE,2))
    o.append(line(X0,Y0-0.066*H,X0+W,Y0-0.066*H,MUTED,1.2,"6 5")); o.append(text(X0+W-6,Y0-0.066*H-8,"base rate 0.066",11.5,MUTED,anchor="end"))
    o.append(text(X0+W-10,Y0-H+20,"PR-AUC 0.302",13,ORANGE,"bold",anchor="end"))
    return svg(960,420,"".join(o))

def fig_calib():
    o=[]; X0=100; Y0=380; W=560; H=300
    axes(o,X0,Y0,W,H,"Mean predicted probability (deciles)","Actual win rate",[0,.2,.4,.6,.8,1],[0,.2,.4,.6,.8,1])
    o.append(line(X0,Y0,X0+W,Y0-H,MUTED,1.2,"6 5")); o.append(text(X0+W*0.8,Y0-H*0.75,"perfect calibration",11.5,MUTED))
    for (name,(fpos,mpred)),c in zip(R["calib"].items(),[ACC,RED,GREEN]):
        pts=[(X0+a*W,Y0-b*H) for a,b in zip(mpred,fpos)]; o.append(poly(pts,c,2.2))
        for x,y in pts: o.append(dot(x,y,c,4))
    for i,(name,c) in enumerate(zip(R["calib"],[ACC,RED,GREEN])):
        o.append(rect(X0+W+30,Y0-H+20+i*26,14,14,fill=c,rx=2)); o.append(text(X0+W+52,Y0-H+32+i*26,name,12.5,INK))
    return svg(900,440,"".join(o))

def fig_profit():
    o=[]; X0=110; Y0=360; W=680; H=280; g=R["grid"]; pr=R["profits"]; mx=max(pr)
    X=lambda t: X0+t/0.5*W; Y=lambda v: Y0-v/2.6e6*H
    for t in [0,.1,.2,.3,.4,.5]: o.append(line(X(t),Y0,X(t),Y0-H,PALE)); o.append(text(X(t),Y0+20,f"{t:.1f}",11.5,MUTED,anchor="middle"))
    for v in [0,0.5e6,1e6,1.5e6,2e6,2.5e6]: o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"₹{v/1e6:.1f}M",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(poly([(X(t),Y(v)) for t,v in zip(g,pr)],ACC))
    best=g[pr.index(mx)]; o.append(line(X(best),Y0,X(best),Y(mx),GREEN,1.5,"5 4")); o.append(dot(X(best),Y(mx),GREEN,6))
    o.append(text(X(best)+10,Y(mx)-12,f"best: threshold {best:.3f}, ₹{mx/1e6:.2f}M",12.5,GREEN,"bold"))
    o.append(line(X(0.0496),Y0,X(0.0496),Y(2.35e6),ORANGE,1.5,"3 4")); o.append(text(X(0.0496)+6,Y(1.3e6),"break-even 0.05",11.5,ORANGE,"bold"))
    o.append(text(X0+W/2,Y0+44,"Threshold (work leads scoring at or above it)",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-70}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-70} {Y0-H/2})">Expected profit, 2,225 validation leads</text>')
    return svg(900,420,"".join(o))

def fig_pd():
    o=[]; X0=100; Y0=360; W=660; H=280; xs=R["pd_x"]; ys=R["pd_y"]
    X=lambda d: X0+d/max(xs)*W; Y=lambda v: Y0-v/0.5*H
    for d in [0,60,120,180,240,300,360]:
        if d<=max(xs): o.append(line(X(d),Y0,X(d),Y0-H,PALE)); o.append(text(X(d),Y0+20,str(d),11.5,MUTED,anchor="middle"))
    for v in [0,.1,.2,.3,.4,.5]: o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+4,f"{v:.0%}",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(poly([(X(a),Y(b)) for a,b in zip(xs,ys)],GREEN))
    for d,lab in [(90,"planted step at 90 days"),(180,"planted step at 180 days")]:
        o.append(line(X(d),Y0,X(d),Y0-H,ORANGE,1.2,"4 4")); o.append(text(X(d)+6,Y0-H+14,lab,11.5,ORANGE,"bold"))
    o.append(text(X0+W/2,Y0+44,"Days since last order (all other features as observed)",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-55}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-55} {Y0-H/2})">Average predicted churn probability</text>')
    return svg(880,420,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig39-1-confusion-matrix.svg",fig_confusion),("fig39-2-roc-pr.svg",fig_roc_pr),("fig39-3-calibration.svg",fig_calib),
                    ("fig39-4-profit-curve.svg",fig_profit),("fig39-5-partial-dependence.svg",fig_pd)]:
        open(name,"w").write(fn())
    print("ok")
