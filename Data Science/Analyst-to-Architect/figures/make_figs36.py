# Generates the SVG figures for Chapter 36. Run from figures/: python3 make_figs36.py
# Numbers come from checks/ch36_check.py, which rebuilds the chapter's models from companion/crm/.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "checks"))
from make_figs import *
from ch36_check import results
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; GREY="#8a93a3"; PALE="#eef1f5"
R = results()
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)

def fig_split():
    o=[]; X0=60; W=900; Y=110; H=60
    X=lambda m: X0+m/36*W       # m = months since Jan 2023
    end_test=33+2/31
    blocks=[(0,24,ACC,"Training","2023–2024",f"{R['n_train']:,} leads · win rate {R['r_train']:.2%}"),
            (24,30,GREEN,"Validation","Jan–Jun 2025",f"{R['n_valid']:,} leads · win rate {R['r_valid']:.2%}"),
            (30,end_test,ORANGE,"Test","Jul–2 Oct 2025",f"{R['n_test']:,} leads · win rate {R['r_test']:.2%}")]
    for a,b,c,t,sub,n in blocks:
        o.append(rect(X(a),Y,X(b)-X(a)-3,H,fill=c,rx=4))
        o.append(text((X(a)+X(b))/2,Y+37,t,14 if t!="Test" else 13,"#fff","bold",anchor="middle",family=HEAD))
    xa=X(end_test)
    o.append(f'<defs><pattern id="h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="{PALE}"/><line x1="0" y1="0" x2="0" y2="8" stroke="{GREY}" stroke-width="2"/></pattern></defs>')
    o.append(rect(xa,Y,X(36)-xa,H,fill="url(#h)",rx=4))
    for m,lab in [(0,"Jan 2023"),(12,"Jan 2024"),(24,"Jan 2025"),(36,"31 Dec 2025 export")]:
        o.append(line(X(m),Y+H+10,X(m),Y+H+20,INK,1.2)); o.append(text(X(m),Y+H+38,lab,12,INK,anchor="middle" if 0<m<36 else ("start" if m==0 else "end")))
    o.append(line(X0,Y+H+15,X(36),Y+H+15,INK,1.2))
    ly=Y+H+80
    items=[(c,t,sub,n) for _,_,c,t,sub,n in blocks]+[(GREY,"Excluded","3 Oct–31 Dec 2025","outcomes not settled (last 90 days)")]
    for i,(c,t,sub,n) in enumerate(items):
        x=X0+i*232
        o.append(rect(x,ly,14,14,fill=c,rx=2)); o.append(text(x+22,ly+12,f"{t}: {sub}",13,INK,"bold"))
        o.append(text(x+22,ly+32,n,12,MUTED))
    o.append(text(X0,60,"The model learns from the past and is judged on later leads",15,INK,"bold",family=HEAD))
    return svg(1020,300,"".join(o))

def fig_kfold():
    o=[]; X0=170; W=620; Y0=70; h=34; g=14
    for r in range(5):
        y=Y0+r*(h+g); o.append(text(X0-16,y+22,f"Round {r+1}",13,INK,"bold",anchor="end"))
        for k in range(5):
            x=X0+k*(W/5); c=ORANGE if k==r else ACC
            o.append(rect(x,y,W/5-6,h,fill=c,rx=3)); o.append(text(x+(W/5-6)/2,y+22,"score" if k==r else "train",12,"#fff","bold",anchor="middle"))
        o.append(text(X0+W+18,y+22,f"→ AUC {r+1}",13,MUTED))
    o.append(text(X0,40,"Training rows, cut into 5 folds",14,INK,"bold",family=HEAD))
    o.append(text(X0,Y0+5*(h+g)+20,"Average of the 5 scores = estimate; their spread = how much it wobbles.",13,INK))
    return svg(1000,340,"".join(o))

def fig_leak():
    o=[]; X0=260; W=560; Y0=70; bh=46; g=22
    rows=[("Honest features",R["honest"][0],ACC),("+ first_response_hours",R["first_response_hours"][0],RED),
          ("+ days_in_pipeline",R["days_in_pipeline"][0],RED),("+ has_quote",R["has_quote"][0],RED)]
    X=lambda v: X0+(v-0.5)/0.5*W
    for v in [0.5,0.6,0.7,0.8,0.9,1.0]:
        o.append(line(X(v),Y0-10,X(v),Y0+4*(bh+g),PALE)); o.append(text(X(v),Y0+4*(bh+g)+18,f"{v:.1f}",11.5,MUTED,anchor="middle"))
    for i,(lab,v,c) in enumerate(rows):
        y=Y0+i*(bh+g); o.append(rect(X0,y,X(v)-X0,bh,fill=c,rx=3))
        o.append(text(X0-14,y+29,lab,13.5,INK,"bold" if i==0 else "normal",anchor="end")); o.append(text(X(v)+10,y+29,f"{v:.3f}",14,INK,"bold"))
    o.append(line(X(R["honest"][0]),Y0-10,X(R["honest"][0]),Y0+4*(bh+g),ACC,1.5,"5 4"))
    o.append(text(X0+W/2,Y0+4*(bh+g)+44,"Validation AUC (Jan–Jun 2025); axis starts at 0.5, a coin toss",12.5,INK,anchor="middle"))
    o.append(text(X0-240,40,"Adding one leaky column to the honest model",14.5,INK,"bold",family=HEAD))
    return svg(1000,420,"".join(o))

def fig_pipeline():
    o=[]
    def box(x,y,w,h,t,sub=None,c=ACC,tc="#fff"):
        o.append(rect(x,y,w,h,fill=c,rx=6)); o.append(text(x+w/2,y+(h/2+5 if not sub else h/2-4),t,13.5,tc,"bold",anchor="middle"))
        if sub: o.append(text(x+w/2,y+h/2+15,sub,11.5,tc,anchor="middle"))
    def arrow(x1,y1,x2,y2):
        o.append(line(x1,y1,x2,y2,INK,1.6)); o.append(f'<path d="M{x2},{y2} l-9,-5 l0,10 Z" fill="{INK}"/>' if y1==y2 else "")
    box(20,170,150,70,"Raw lead columns","13 columns",GREY)
    o.append(rect(210,40,440,330,fill="none",rx=10)); o.append(path("M210,40 h440 v330 h-440 Z",stroke=RULE,sw=1.5,dash="6 5"))
    o.append(text(430,64,"ColumnTransformer",14,INK,"bold",anchor="middle",family=HEAD))
    box(240,95,180,64,"Fill blanks","\"Missing\"",ACC); box(450,95,180,64,"One-hot encode","6 sources → 6 columns",ACC)
    o.append(text(230,88,"5 categorical columns",12,MUTED))
    box(240,255,180,64,"Fill blanks","median + missing indicator",GREEN); box(450,255,180,64,"Standard scale","learned from training rows",GREEN)
    o.append(text(230,248,"8 numeric columns",12,MUTED))
    arrow(170,205,208,205); o.append(line(208,205,208,127,INK,1.6)); o.append(line(208,205,208,287,INK,1.6))
    arrow(208,127,238,127); arrow(208,287,238,287); arrow(420,127,448,127); arrow(420,287,448,287)
    o.append(line(630,127,672,127,INK,1.6)); o.append(line(630,287,672,287,INK,1.6)); o.append(line(672,127,672,287,INK,1.6)); arrow(672,205,700,205)
    box(700,170,130,70,"Feature matrix","45 columns",GREY); arrow(830,205,858,205)
    box(858,160,130,90,"Logistic","regression",ORANGE)
    o.append(text(923,280,"→ win probability",12.5,INK,"bold",anchor="middle"))
    o.append(text(20,400,"fit(train) learns every step from training rows · predict_proba(new rows) applies them unchanged",12.5,INK))
    return svg(1010,420,"".join(o))

def fig_base():
    o=[]; X0=120; Y0=360; H=280; gw=220; bw=70
    Y=lambda v: Y0-(v-0.4)/0.5*H
    for v in [0.4,0.5,0.6,0.7,0.8,0.9]:
        o.append(line(X0-10,Y(v),X0+3*gw,Y(v),PALE)); o.append(text(X0-16,Y(v)+4,f"{v:.1f}",11.5,MUTED,anchor="end"))
    groups=[("Base rate",0.5,0.5),("Rule: 3 sources",R["rule_valid"],R["rule_test"]),("Logistic regression",R["honest"][0],R["test"][0])]
    for i,(lab,vv,vt) in enumerate(groups):
        x=X0+i*gw+30
        for j,(v,c,t) in enumerate([(vv,GREEN,"valid"),(vt,ORANGE,"test")]):
            xx=x+j*(bw+8); o.append(rect(xx,Y(v),bw,Y0-Y(v),fill=c,rx=3)); o.append(text(xx+bw/2,Y(v)-8,f"{v:.3f}",13,INK,"bold",anchor="middle"))
        o.append(text(x+bw+4,Y0+24,lab,13,INK,anchor="middle"))
    o.append(line(X0-10,Y0,X0+3*gw,Y0,INK,1.2))
    o.append(f'<text x="{X0-60}" y="{Y(0.65)}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-60} {Y(0.65)})">AUC (axis starts at 0.4)</text>')
    for j,(c,t) in enumerate([(GREEN,"Validation (Jan–Jun 2025)"),(ORANGE,"Test, scored once (Jul–2 Oct 2025)")]):
        o.append(rect(X0+3*gw+20,90+j*30,16,16,fill=c,rx=2)); o.append(text(X0+3*gw+44,103+j*30,t,13,INK))
    return svg(1080,400,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig36-1-time-split.svg",fig_split),("fig36-2-kfold.svg",fig_kfold),("fig36-3-leakage.svg",fig_leak),
                    ("fig36-4-pipeline.svg",fig_pipeline),("fig36-5-baselines.svg",fig_base)]:
        open(name,"w").write(fn())
    print("ok")
