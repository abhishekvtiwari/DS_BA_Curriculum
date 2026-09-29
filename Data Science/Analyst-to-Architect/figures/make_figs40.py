# Generates the SVG figures for Chapter 40. Run from figures/ after checks/ch40_check.py has written ch40_results.json.
# Every figure prints at the full text width (493.2 pt); on a 900 px canvas, 13.5 px prints at 7.4 pt, the smallest size used.
import json, pathlib
import numpy as np, pandas as pd
from make_figs import *
GREEN="#2f7d6d"; DKGREEN="#1f5e50"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"; GREY="#9aa3b2"; LIGHTBLUE="#7fa8c9"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch40_results.json").read_text())
TICK=13.5; LABEL=14; TITLE=15
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def poly(pts,c,sw=2,dash=None):
    """A polyline that breaks at missing values (NaN), instead of joining across them."""
    out=[]; seg=[]
    for x,y in pts:
        if x==x and y==y: seg.append((x,y))
        elif seg: out.append(seg); seg=[]
    if seg: out.append(seg)
    return "".join(path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in s),stroke=c,sw=sw,dash=dash) for s in out if len(s)>1)

def fig_decomp():
    o=[]; k=pd.Series(R["kitchen"]); k.index=pd.to_datetime(k.index); n=len(k); X0=110; W=760
    X=lambda i: X0+i/(n-1)*W
    trend=np.array([R["trend"][d] if R["trend"][d] is not None else np.nan for d in R["kitchen"]])
    resid=np.array([R["resid"][d] if R["resid"][d] is not None else np.nan for d in R["kitchen"]])
    panels=[("Kitchen units per month",k.to_numpy(),ACC,(20000,130000),[40000,80000,120000],lambda v:f"{v/1000:.0f}k"),
            ("Trend",trend,GREEN,(45000,95000),[50000,70000,90000],lambda v:f"{v/1000:.0f}k"),
            ("Seasonal factor (1.0 = an average month)",np.tile(np.array(R["seasonal"]),7)[:n],ORANGE,(0.75,1.5),[0.8,1.0,1.2,1.4],lambda v:f"{v:.1f}"),
            ("Residual (1.0 = as predicted)",resid,PURPLE,(0.55,1.35),[0.75,1.0,1.25],lambda v:f"{v:.2f}")]
    H=100; gap=44; top=34
    for p,(title,vals,c,(lo,hi),ticks,fmt) in enumerate(panels):
        Y0=top+p*(H+gap)+H
        Y=lambda v: Y0-(v-lo)/(hi-lo)*H
        o.append(text(X0,Y0-H-9,title,TITLE,INK,"bold",family=HEAD))
        for v in ticks:
            o.append(line(X0,Y(v),X0+W,Y(v),PALE,1)); o.append(text(X0-10,Y(v)+5,fmt(v),TICK,MUTED,anchor="end"))
        if p>=2: o.append(line(X0,Y(1),X0+W,Y(1),MUTED,1,"4 4"))
        o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE))
        o.append(poly([(X(i),Y(v)) for i,v in enumerate(vals)],c,2))
        if p==3:
            low=int(np.nanargmin(resid)); o.append(text(X(low)+10,Y(resid[low])+6,"May 2020: 37% below",TICK,PURPLE,"bold"))
            for yr in range(2019,2026):
                i=list(k.index).index(pd.Timestamp(f"{yr}-01-01")); o.append(line(X(i),Y0,X(i),Y0+6,INK,1)); o.append(text(X(i),Y0+24,str(yr),TICK,MUTED,anchor="middle"))
    return svg(900,top+4*(H+gap)-gap+36,"".join(o))

def fig_acf():
    o=[]; band=R["band"]
    for p,(title,vals) in enumerate([("ACF",R["acf"]),("PACF",R["pacf"])]):
        X0=78+p*440; W=360; Y0=290; H=220; bw=10
        Y=lambda v: Y0-H/2-v/0.7*(H/2); X=lambda lag: X0+lag/25*W
        o.append(line(X0,Y(0),X0+W,Y(0),INK,1.2)); o.append(line(X0,Y(band),X0+W,Y(band),MUTED,1.2,"5 4")); o.append(line(X0,Y(-band),X0+W,Y(-band),MUTED,1.2,"5 4"))
        for v in [-0.6,-0.3,0.3,0.6]: o.append(text(X0-8,Y(v)+5,f"{v:+.1f}",TICK,MUTED,anchor="end"))
        for lag in range(1,25):
            v=vals[lag]; out=abs(v)>band
            o.append(rect(X(lag)-bw/2,min(Y(0),Y(v)),bw,abs(Y(v)-Y(0)),fill=ACC if out else GREY))
            if out: o.append(text(X(lag),Y(v)-7 if v>0 else Y(v)+19,str(lag),TICK,ACC,"bold",anchor="middle"))
        for lag in (1,6,12,18,24): o.append(text(X(lag),Y0+22,str(lag),TICK,MUTED,anchor="middle"))
        o.append(text(X0,Y0-H-14,f"{title} of the differenced log series",TITLE,INK,"bold",family=HEAD))
        o.append(text(X0+W/2,Y0+44,"Lag (months)",LABEL,INK,anchor="middle"))
        o.append(text(X0+W,Y(-band)+19,f"band ±{band:.2f}",TICK,MUTED,anchor="end"))
    o.append(rect(78,366,14,14,fill=ACC)); o.append(text(100,378,"outside the band, labelled with its lag",LABEL,INK))
    o.append(rect(420,366,14,14,fill=GREY)); o.append(text(442,378,"inside the band",LABEL,INK))
    return svg(900,392,"".join(o))

def fig_backtest():
    o=[]; X0=120; W=720; Y0=24; rh=42; n=84; X=lambda m: X0+m/n*W; F=14
    for f in range(5):
        cut=n-12*(5-f); y=Y0+f*rh
        o.append(rect(X(0),y,X(cut)-X(0),28,fill=ACC,rx=3)); o.append(rect(X(cut),y,X(cut+12)-X(cut),28,fill=ORANGE,rx=3))
        o.append(text(X0-12,y+19,f"Fold {f+1}",F,INK,"bold",anchor="end")); o.append(text(X(cut+12)+8,y+19,f"forecast {2021+f}",F,MUTED))
        o.append(text(X(0)+8,y+19,f"{cut} months",F,"#ffffff","bold"))
    base=Y0+5*rh
    for yr in range(2019,2027): o.append(line(X((yr-2019)*12),base,X((yr-2019)*12),base+6,INK,1)); o.append(text(X((yr-2019)*12),base+24,str(yr),F,MUTED,anchor="middle"))
    o.append(line(X(0),base,X(n),base,INK,1.2))
    o.append(rect(X0,base+40,15,15,fill=ACC,rx=2)); o.append(text(X0+23,base+53,"training history",F,INK))
    o.append(rect(X0+190,base+40,15,15,fill=ORANGE,rx=2)); o.append(text(X0+213,base+53,"12-month forecast window, scored by WAPE",F,INK))
    return svg(960,base+70,"".join(o))

def fig_sensor():
    o=[]; t=pd.Series(R["temp"]); t.index=pd.to_datetime(t.index); b=pd.Series(R["baseline"]); b.index=pd.to_datetime(b.index)
    pr=pd.Series(R["pressure"]); pr.index=pd.to_datetime(pr.index); st=np.array(R["status"]); n=len(t); X0=70; W=800
    X=lambda i: X0+i/(n-1)*W
    stopped=np.where(st=="stopped")[0]; s0,s1=int(stopped.min()),int(stopped.max())
    # temperature panel
    Y0=205; H=170; lo,hi=206,228; clamp=lambda v: min(max(v,lo),hi); Y=lambda v: Y0-(clamp(v)-lo)/(hi-lo)*H
    o.append(text(X0,Y0-H-10,"Temperature (°C) against a 24-hour median baseline, ±6 °C band",TITLE,INK,"bold",family=HEAD))
    bv=b.to_numpy(); idx=[i for i,v in enumerate(bv) if v==v]
    top=" L".join(f"{X(i):.1f},{Y(bv[i]+6):.1f}" for i in idx); bot=" L".join(f"{X(i):.1f},{Y(bv[i]-6):.1f}" for i in idx[::-1])
    o.append(f'<path d="M{top} L{bot} Z" fill="{GREEN}" opacity="0.13"/>')
    o.append(poly([(X(i),Y(v)) for i,v in enumerate(t.to_numpy())],LIGHTBLUE,1)); o.append(poly([(X(i),Y(v)) for i,v in enumerate(bv)],DKGREEN,2.4))
    o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE))
    for v in [210,215,220,225]: o.append(text(X0-8,Y(v)+5,str(v),TICK,MUTED,anchor="end"))
    hot=int(np.argmax(t.to_numpy())); o.append(text(X(hot)-12,Y(225)+4,"heater fault, Wed night",LABEL,RED,"bold",anchor="end"))
    o.append(line(X0+W-250,Y0-H+18,X0+W-226,Y0-H+18,DKGREEN,2.4)); o.append(text(X0+W-218,Y0-H+23,"baseline (median)",TICK,INK))
    # pressure panel
    Y0=450; H=170; lo,hi=95,158; Y=lambda v: Y0-(clamp2(v)-lo)/(hi-lo)*H; clamp2=lambda v: min(max(v,lo),hi)
    o.append(text(X0,Y0-H-10,"Pressure (bar); the stoppage is shaded",TITLE,INK,"bold",family=HEAD))
    o.append(rect(X(s0),Y0-H,max(X(s1)-X(s0),5),H,fill=PALE,stroke=MUTED,sw=0.8))
    o.append(text(X(s1)+8,Y0-14,"stoppage, Wed 22:02–22:33",LABEL,MUTED,"bold"))
    pv=pr.to_numpy().copy(); pv[st=="stopped"]=np.nan
    o.append(poly([(X(i),Y(v)) for i,v in enumerate(pv)],ORANGE,1))
    o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE))
    for v in [100,120,140]: o.append(text(X0-8,Y(v)+5,str(v),TICK,MUTED,anchor="end"))
    sp=int(np.nanargmax(pv)); o.append(f'<circle cx="{X(sp):.1f}" cy="{Y(pv[sp]):.1f}" r="7" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append(text(X(sp)+12,Y(pv[sp])+5,"3 pressure spikes, Tue 12:00–12:02",LABEL,RED,"bold"))
    for d in range(7): i=d*1440; o.append(line(X(i),Y0,X(i),Y0+6,INK,1)); o.append(text(X(i)+4,Y0+24,["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][d],TICK,MUTED))
    return svg(900,482,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig40-1-decomposition.svg",fig_decomp),("fig40-2-acf-pacf.svg",fig_acf),("fig40-3-backtest.svg",fig_backtest),("fig40-4-sensor-anomalies.svg",fig_sensor)]:
        open(name,"w").write(fn())
    print("ok")
