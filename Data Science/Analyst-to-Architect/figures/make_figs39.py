# Generates the SVG figures for Chapter 39. Run from figures/ after checks/ch39_check.py has written ch39_results.json.
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas prints at s x 493.2 / W pt;
# every text here is at least 7 pt. Series are told apart by marker shape and direct labels, not colour alone.
import json, pathlib
from make_figs import *
ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"; WRONG="#b0572a"; WRONGBG="#f6e3d8"; RIGHTBG="#dcebf5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch39_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def poly(pts,c,sw=2.6,dash=None): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=sw,dash=dash)
def marker(x,y,c,shape,r=5.5):
    if shape=="o": return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
    if shape=="s": return f'<rect x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r}" height="{2*r}" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
    return f'<path d="M{x:.1f},{y-r*1.2:.1f} L{x+r*1.1:.1f},{y+r*0.8:.1f} L{x-r*1.1:.1f},{y+r*0.8:.1f} Z" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
def halo(x,y,s,size,fill,weight="normal",anchor="start"):
    """Text with a white outline, so it stays readable where it crosses a gridline."""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="#fff" stroke="#fff" stroke-width="4" stroke-linejoin="round" '
            f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>') + text(x,y,s,size,fill,weight,anchor=anchor)
def ylabel(x,y,s,size): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{INK}" text-anchor="middle" transform="rotate(-90 {x} {y})">{s}</text>'
def axes(o,X0,Y0,W,H,xl,yl,xt,yt,fs=14,fmt="{:.1f}",xmax=1,ymax=1):
    for v in xt: o.append(line(X0+v/xmax*W,Y0,X0+v/xmax*W,Y0-H,PALE)); o.append(text(X0+v/xmax*W,Y0+22,fmt.format(v),fs,MUTED,anchor="middle"))
    for v in yt: o.append(line(X0,Y0-v/ymax*H,X0+W,Y0-v/ymax*H,PALE)); o.append(text(X0-10,Y0-v/ymax*H+5,fmt.format(v),fs,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(text(X0+W/2,Y0+48,xl,fs+1,INK,anchor="middle")); o.append(ylabel(X0-52,Y0-H/2,yl,fs+1))

def fig_confusion():                       # 760 px wide: 1 px = 0.649 pt, so 11 px = 7.1 pt
    o=[]; X0=236; Y0=62; cw=160; ch=104
    cells=[("True positives","100",True),("False positives","386",False),("False negatives","46",False),("True negatives","1,693",True)]
    for i,(lab,v,right) in enumerate(cells):
        x=X0+(i%2)*cw; y=Y0+(i//2)*ch; c=ACC if right else WRONG
        o.append(rect(x,y,cw-8,ch-8,fill=RIGHTBG if right else WRONGBG,stroke=c,sw=2,rx=6,extra='' if right else 'stroke-dasharray="7 4"'))
        o.append(text(x+(cw-8)/2,y+42,v,26,c,"bold",anchor="middle",family=HEAD)); o.append(text(x+(cw-8)/2,y+66,lab,13,INK,anchor="middle"))
        o.append(text(x+(cw-8)/2,y+85,"correct" if right else "wrong",12,MUTED,anchor="middle",style="italic"))
    o.append(text(X0+cw/2-4,Y0-14,"Actually won",14,INK,"bold",anchor="middle")); o.append(text(X0+cw+cw/2-4,Y0-14,"Actually lost",14,INK,"bold",anchor="middle"))
    o.append(text(X0-14,Y0+ch/2-4,"Predicted won",14,INK,"bold",anchor="end")); o.append(text(X0-14,Y0+ch/2+16,"(score ≥ 0.1)",13,MUTED,anchor="end"))
    o.append(text(X0-14,Y0+ch+ch/2+4,"Predicted lost",14,INK,"bold",anchor="end"))
    o.append(text(X0+2*cw+6,Y0+ch/2-8,"precision =",13.5,INK)); o.append(text(X0+2*cw+6,Y0+ch/2+12,"100 ÷ (100 + 386)",13.5,INK))
    o.append(text(X0+2*cw+6,Y0+ch/2+34,"= 0.206",14,ACC,"bold"))
    o.append(text(X0+cw/2-4,Y0+2*ch+18,"recall = 100 ÷ (100 + 46) = 0.685",13.5,INK,anchor="middle"))
    o.append(text(X0+cw+cw/2+60,Y0+2*ch+44,"specificity = 1,693 ÷ 2,079 = 0.814",13.5,INK,anchor="middle"))
    return svg(760,330,"".join(o))

def fig_roc_pr():                          # 900 px wide: 1 px = 0.548 pt, so 13 px = 7.1 pt
    o=[]; W=320; H=280; Y0=330
    X0=82; axes(o,X0,Y0,W,H,"False positive rate","Recall (true positive rate)",[0,.5,1],[0,.5,1])
    o.append(line(X0,Y0,X0+W,Y0-H,MUTED,1.2,"6 5"))
    o.append(poly([(X0+a*W,Y0-b*H) for a,b in zip(R["fpr"],R["tpr"])],ACC))
    o.append(halo(X0+W*0.56,Y0-H*0.40,"chance",13,MUTED))
    o.append(halo(X0+W-8,Y0-22,"ROC-AUC 0.823",15,ACC,"bold",anchor="end"))
    X0=548; axes(o,X0,Y0,W,H,"Recall","Precision",[0,.5,1],[0,.5,1])
    o.append(line(X0,Y0-0.066*H,X0+W,Y0-0.066*H,MUTED,1.2,"6 5"))
    o.append(poly([(X0+a*W,Y0-b*H) for a,b in zip(R["rec"],R["prec"])],ORANGE,2))
    o.append(halo(X0+10,Y0-0.066*H-9,"base rate 0.066",13,MUTED))
    o.append(halo(X0+W-8,Y0-H+22,"PR-AUC 0.302",15,ORANGE,"bold",anchor="end"))
    return svg(900,390,"".join(o))

def fig_calib():                           # 900 px wide: 13 px = 7.1 pt
    o=[]; series=[("logistic regression",ACC,"o"),("Naive Bayes",ORANGE,"s"),("gradient boosting",PURPLE,"^")]
    # left: the whole range
    X0=78; Y0=350; W=300; H=300
    axes(o,X0,Y0,W,H,"Mean predicted probability","Actual win rate",[0,.5,1],[0,.5,1])
    o.append(line(X0,Y0,X0+W,Y0-H,MUTED,1.2,"6 5")); o.append(halo(X0+W*0.50,Y0-H*0.62,"perfect calibration",13,MUTED,anchor="end"))
    for name,c,m in series:
        mp,fp=R["calib"][name][1],R["calib"][name][0]
        pts=[(X0+a*W,Y0-b*H) for a,b in zip(mp,fp)]; o.append(poly(pts,c,2))
        for x,y in pts: o.append(marker(x,y,c,m,4.5))
    nb=R["calib"]["Naive Bayes"]; o.append(halo(X0+nb[1][-1]*W-6,Y0-nb[0][-1]*H-14,"Naive Bayes",14,ORANGE,"bold",anchor="end"))
    o.append(rect(X0,Y0-0.3*H,0.3*W,0.3*H,stroke=INK,sw=1,extra='stroke-dasharray="3 3"'))
    o.append(text(X0+0.3*W+6,Y0-0.3*H+14,"enlarged →",13,MUTED))
    # right: zoom on 0-0.3
    X0=560; W=300; Z=0.3
    axes(o,X0,Y0,W,H,"Mean predicted probability (0 to 0.3)","Actual win rate (0 to 0.3)",[0,.1,.2,.3],[0,.1,.2,.3],xmax=Z,ymax=Z)
    o.append(line(X0,Y0,X0+W,Y0-H,MUTED,1.2,"6 5"))
    for name,c,m in series:
        mp,fp=R["calib"][name][1],R["calib"][name][0]
        pts=[(X0+a/Z*W,Y0-b/Z*H) for a,b in zip(mp,fp) if a<=Z and b<=Z]; o.append(poly(pts,c,2))
        for x,y in pts: o.append(marker(x,y,c,m,5))
    # legend: marker + name (shape carries the meaning, colour repeats it)
    for i,(name,c,m) in enumerate(series):
        yy=Y0-H+18+i*24; o.append(marker(X0+18,yy-5,c,m,5.5)); o.append(text(X0+32,yy,name,14,INK))
    return svg(900,420,"".join(o))

def fig_profit():                          # 900 px wide: 13 px = 7.1 pt
    o=[]; X0=112; Y0=340; W=700; H=270; g=R["grid"]; pr=R["profits"]; mx=max(pr)
    X=lambda t: X0+t/0.5*W; Y=lambda v: Y0-v/2.6e6*H
    for t in [0,.1,.2,.3,.4,.5]: o.append(line(X(t),Y0,X(t),Y0-H,PALE)); o.append(text(X(t),Y0+22,f"{t:.1f}",14,MUTED,anchor="middle"))
    for v in [0,5e5,10e5,15e5,20e5,25e5]: o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+5,f"₹{v/1e5:.0f} lakh",14,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(poly([(X(t),Y(v)) for t,v in zip(g,pr)],ACC))
    best=g[pr.index(mx)]; o.append(line(X(best),Y0,X(best),Y(mx),ACC,1.5,"5 4")); o.append(marker(X(best),Y(mx),ACC,"o",6))
    o.append(halo(X(best)+12,Y(mx)-10,f"best: threshold {best:.3f}, ₹{mx/1e5:.1f} lakh",14,ACC,"bold"))
    o.append(line(X(0.0496),Y0,X(0.0496),Y(2.35e6),ORANGE,1.5,"3 4")); o.append(halo(X(0.0496)-8,Y(0.6e6),"break-even 0.0496",14,ORANGE,"bold",anchor="end"))
    o.append(text(X0+W/2,Y0+48,"Threshold (work leads scoring at or above it)",15,INK,anchor="middle"))
    o.append(ylabel(X0-88,Y0-H/2,"Expected profit, 2,225 validation leads",15))
    return svg(900,400,"".join(o))

def fig_pd():                              # 880 px wide: 1 px = 0.560 pt, so 13 px = 7.3 pt
    o=[]; X0=100; Y0=340; W=680; H=270; xs=R["pd_x"]; ys=R["pd_y"]
    X=lambda d: X0+d/max(xs)*W; Y=lambda v: Y0-v/0.5*H
    for d in [0,60,120,180,240]:
        if d<=max(xs): o.append(line(X(d),Y0,X(d),Y0-H,PALE)); o.append(text(X(d),Y0+22,str(d),14,MUTED,anchor="middle"))
    for v in [0,.1,.2,.3,.4,.5]: o.append(line(X0,Y(v),X0+W,Y(v),PALE)); o.append(text(X0-10,Y(v)+5,f"{v:.0%}",14,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(poly([(X(a),Y(b)) for a,b in zip(xs,ys)],ACC))
    for d,lab,anc,dx in [(90,"planted step at 90 days","start",6),(180,"planted step at 180 days","end",-6)]:
        o.append(line(X(d),Y0,X(d),Y0-H,ORANGE,1.2,"4 4")); o.append(halo(X(d)+dx,Y0-H+16,lab,14,ORANGE,"bold",anchor=anc))
    o.append(text(X0+W/2,Y0+48,"Days since last order (all other features as observed)",15,INK,anchor="middle"))
    o.append(ylabel(X0-58,Y0-H/2,"Average predicted churn probability",15))
    return svg(880,400,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig39-1-confusion-matrix.svg",fig_confusion),("fig39-2-roc-pr.svg",fig_roc_pr),("fig39-3-calibration.svg",fig_calib),
                    ("fig39-4-profit-curve.svg",fig_profit),("fig39-5-partial-dependence.svg",fig_pd)]:
        open(name,"w").write(fn())
    print("ok")
