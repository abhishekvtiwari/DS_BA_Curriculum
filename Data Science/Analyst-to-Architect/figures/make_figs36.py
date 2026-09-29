# Generates the SVG figures for Chapter 36. Run from figures/: python3 make_figs36.py
# Numbers come from checks/ch36_check.py, which rebuilds the chapter's models from companion/crm/.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "checks"))
from make_figs import *
from ch36_check import results
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; GREY="#8a93a3"; PALE="#eef1f5"
R = results()
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)

# Every figure prints at 493.2 pt wide, so s px on a W px canvas prints at s*493.2/W pt.
# Canvases are 700 px wide and the smallest text is 10.5 px (7.4 pt).
def hatch(pid,c,bg="#fff"):
    return (f'<defs><pattern id="{pid}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="7" height="7" fill="{bg}"/><line x1="0" y1="0" x2="0" y2="7" stroke="{c}" stroke-width="2.6"/></pattern></defs>')

def fig_split():
    o=[]; X0=14; W=672; Y=46; H=46
    X=lambda m: X0+m/36*W       # m = months since Jan 2023
    end_test=33+2/31
    blocks=[(0,24,ACC,"Training","2023–2024",f"{R['n_train']:,} leads",f"win rate {R['r_train']:.2%}"),
            (24,30,GREEN,"Validation","Jan–Jun 2025",f"{R['n_valid']:,} leads",f"win rate {R['r_valid']:.2%}"),
            (30,end_test,ORANGE,"Test","Jul–2 Oct 2025",f"{R['n_test']:,} leads",f"win rate {R['r_test']:.2%}")]
    for a,b,c,t,sub,n,r in blocks:
        o.append(rect(X(a),Y,X(b)-X(a)-2,H,fill=c,rx=4))
        o.append(text((X(a)+X(b))/2,Y+28,t,13,"#fff","bold",anchor="middle",family=HEAD))
    xa=X(end_test)
    o.append(hatch("h36",GREY,PALE)); o.append(rect(xa,Y,X(36)-xa,H,fill="url(#h36)",rx=4))
    o.append(line(X0,Y+H+9,X(36),Y+H+9,INK,1.2))
    for m,lab in [(0,"Jan 2023"),(12,"Jan 2024"),(24,"Jan 2025"),(36,"31 Dec 2025 export")]:
        o.append(line(X(m),Y+H+5,X(m),Y+H+13,INK,1.2))
        o.append(text(X(m),Y+H+28,lab,11,INK,anchor="middle" if 0<m<36 else ("start" if m==0 else "end")))
    ly=Y+H+56
    items=[(c,t,sub,n,r) for _,_,c,t,sub,n,r in blocks]+[(None,"Excluded","3 Oct–31 Dec 2025","outcomes not","settled yet")]
    for i,(c,t,sub,n,r) in enumerate(items):
        x=X0+i*170
        o.append(rect(x,ly-11,13,13,fill=c if c else "url(#h36)",stroke=GREY if not c else "none",rx=2))
        o.append(text(x+19,ly,t,11.5,INK,"bold")); o.append(text(x+19,ly+16,sub,10.5,MUTED))
        o.append(text(x+19,ly+31,n,10.5,MUTED)); o.append(text(x+19,ly+46,r,10.5,MUTED))
    o.append(text(X0,24,"The model learns from the past and is judged on later leads",13,INK,"bold",family=HEAD))
    return svg(700,ly+56,"".join(o))

def fig_kfold():
    o=[]; X0=78; W=470; Y0=40; h=26; g=8
    for r in range(5):
        y=Y0+r*(h+g); o.append(text(X0-10,y+17,f"Round {r+1}",11.5,INK,"bold",anchor="end"))
        for k in range(5):
            x=X0+k*(W/5); sc=(k==r)
            o.append(rect(x,y,W/5-4,h,fill=ORANGE if sc else ACC,rx=3))
            o.append(text(x+(W/5-4)/2,y+17,"SCORE" if sc else "train",11 if sc else 10.5,"#fff","bold" if sc else "normal",anchor="middle"))
        o.append(text(X0+W+10,y+17,f"→ AUC {r+1}",11.5,MUTED))
    o.append(text(X0,24,"Training rows, cut into 5 folds",12.5,INK,"bold",family=HEAD))
    o.append(text(X0,Y0+5*(h+g)+14,"Average of the 5 scores = the estimate; their spread = how much it wobbles.",11,INK))
    return svg(700,Y0+5*(h+g)+26,"".join(o))

def fig_leak():
    o=[]; X0=190; W=420; Y0=44; bh=30; g=12
    rows=[("Honest features",R["honest"][0],False),("+ first_response_hours",R["first_response_hours"][0],True),
          ("+ days_in_pipeline",R["days_in_pipeline"][0],True),("+ has_quote",R["has_quote"][0],True)]
    X=lambda v: X0+(v-0.5)/0.5*W
    n=len(rows); bottom=Y0+n*(bh+g)
    o.append(hatch("leak36",RED,"#f6dada"))
    for v in [0.5,0.6,0.7,0.8,0.9,1.0]:
        o.append(line(X(v),Y0-6,X(v),bottom,PALE)); o.append(text(X(v),bottom+15,f"{v:.1f}",10.5,MUTED,anchor="middle"))
    for i,(lab,v,leak) in enumerate(rows):
        y=Y0+i*(bh+g)
        o.append(rect(X0,y,X(v)-X0,bh,fill="url(#leak36)" if leak else ACC,stroke=RED if leak else "none",sw=1.2,rx=3))
        o.append(text(X0-10,y+20,lab,11.5,INK,"bold" if not leak else "normal",anchor="end"))
        o.append(text(X(v)+7,y+20,f"{v:.3f}",11.5,INK,"bold"))
        o.append(text(X(v)+48,y+20,"LEAK" if leak else "honest",10.5,RED if leak else ACC,"bold"))
    o.append(line(X(R["honest"][0]),Y0-6,X(R["honest"][0]),bottom,ACC,1.3,"5 4"))
    o.append(text(X0+W/2,bottom+32,"Validation AUC (Jan–Jun 2025); the axis starts at 0.5, a coin toss",11,INK,anchor="middle"))
    o.append(text(14,24,"Adding one leaky column to the honest model",12.5,INK,"bold",family=HEAD))
    return svg(700,bottom+44,"".join(o))

def fig_pipeline():
    o=[]
    def box(x,y,w,h,t,sub=None,c=ACC,tc="#fff",sub2=None):
        o.append(rect(x,y,w,h,fill=c,rx=5))
        ty=y+h/2+4 if not sub else (y+h/2-3 if not sub2 else y+h/2-9)
        o.append(text(x+w/2,ty,t,11.5,tc,"bold",anchor="middle"))
        if sub: o.append(text(x+w/2,ty+15,sub,10.5,tc,anchor="middle"))
        if sub2: o.append(text(x+w/2,ty+29,sub2,10.5,tc,anchor="middle"))
    def arrow(x1,y1,x2,y2):
        o.append(line(x1,y1,x2,y2,INK,1.4)); o.append(f'<path d="M{x2},{y2} l-7,-4 l0,8 Z" fill="{INK}"/>')
    cy=150
    box(6,cy-32,84,64,"Raw lead","columns",GREY,sub2="(13)")
    o.append(path("M112,30 h336 v240 h-336 Z",stroke=RULE,sw=1.4,dash="6 5"))
    o.append(text(280,50,"ColumnTransformer",12,INK,"bold",anchor="middle",family=HEAD))
    o.append(text(128,74,"5 categorical columns",10.5,MUTED)); o.append(text(128,184,"8 numeric columns",10.5,MUTED))
    box(128,80,146,58,"Fill blanks","with \"Missing\"",ACC); box(290,80,146,58,"One-hot encode","6 sources → 6 columns",ACC)
    box(128,190,146,66,"Fill blanks","median + missing",GREEN,sub2="indicator"); box(290,190,146,66,"Standard scale","mean and sd from",GREEN,sub2="training rows")
    o.append(line(90,cy,106,cy,INK,1.4)); o.append(line(106,109,106,223,INK,1.4))
    arrow(106,109,126,109); arrow(106,223,126,223); arrow(274,109,288,109); arrow(274,223,288,223)
    o.append(line(436,109,462,109,INK,1.4)); o.append(line(436,223,462,223,INK,1.4)); o.append(line(462,109,462,223,INK,1.4)); arrow(462,cy,476,cy)
    box(478,cy-32,96,64,"Feature","matrix",GREY,sub2="(45 columns)"); arrow(574,cy,590,cy)
    box(592,cy-32,102,64,"Logistic","regression",ORANGE)
    o.append(text(643,cy+50,"→ P(won)",11.5,INK,"bold",anchor="middle"))
    o.append(text(6,298,"fit(train rows) learns every step · predict_proba(new rows) applies them unchanged",11,INK))
    return svg(700,310,"".join(o))

def fig_base():
    # Bars start at 0 (V36.19), so bar length is honest; validation solid, test hatched (not colour alone).
    o=[]; X0=150; W=470; Y0=44; bh=15; gap=26
    X=lambda v: X0+v*W
    groups=[("Base rate",0.5,0.5),("Rule: 3 sources",R["rule_valid"],R["rule_test"]),("Logistic regression",R["honest"][0],R["test"][0])]
    o.append(hatch("test36",ORANGE,"#fbe6d8"))
    bottom=Y0+len(groups)*(2*bh+gap)-gap+6
    for v in [0,0.2,0.4,0.6,0.8,1.0]:
        o.append(line(X(v),Y0-6,X(v),bottom,PALE)); o.append(text(X(v),bottom+15,f"{v:.1f}",10.5,MUTED,anchor="middle"))
    for i,(lab,vv,vt) in enumerate(groups):
        y=Y0+i*(2*bh+gap)
        o.append(text(X0-10,y+bh+4,lab,11.5,INK,anchor="end"))
        o.append(rect(X0,y,X(vv)-X0,bh,fill=GREEN,rx=2)); o.append(text(X(vv)+6,y+11.5,f"{vv:.3f}",10.5,INK))
        o.append(rect(X0,y+bh+2,X(vt)-X0,bh,fill="url(#test36)",stroke=ORANGE,sw=1,rx=2)); o.append(text(X(vt)+6,y+bh+13.5,f"{vt:.3f}",10.5,INK))
    o.append(line(X(0.5),Y0-6,X(0.5),bottom,GREY,1.2,"4 3")); o.append(text(X(0.5)+4,Y0-10,"coin toss",10.5,MUTED))
    o.append(text(X0+W/2,bottom+32,"AUC (0.5 = a coin toss, 1.0 = perfect ranking)",11,INK,anchor="middle"))
    ly=bottom+54
    o.append(rect(X0,ly-10,14,12,fill=GREEN,rx=2)); o.append(text(X0+20,ly,"Validation (Jan–Jun 2025)",11,INK))
    o.append(rect(X0+200,ly-10,14,12,fill="url(#test36)",stroke=ORANGE,sw=1,rx=2)); o.append(text(X0+220,ly,"Test, scored once (Jul–2 Oct 2025)",11,INK))
    o.append(text(14,24,"Baselines against the model",12.5,INK,"bold",family=HEAD))
    return svg(700,ly+12,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig36-1-time-split.svg",fig_split),("fig36-2-kfold.svg",fig_kfold),("fig36-3-leakage.svg",fig_leak),
                    ("fig36-4-pipeline.svg",fig_pipeline),("fig36-5-baselines.svg",fig_base)]:
        open(name,"w").write(fn())
    print("ok")
