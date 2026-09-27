# Generates the SVG figures for Chapter 40. Run from figures/ after checks/ch40_check.py has written ch40_results.json.
import json, pathlib
import numpy as np, pandas as pd
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch40_results.json").read_text())
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def poly(pts,c,sw=2,dash=None): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts if x==x and y==y),stroke=c,sw=sw,dash=dash)

def fig_decomp():
    o=[]; k=pd.Series(R["kitchen"]); k.index=pd.to_datetime(k.index); n=len(k); X0=90; W=760
    X=lambda i: X0+i/(n-1)*W
    panels=[("Kitchen units per month",k.to_numpy(),ACC),("Trend",np.array([R["trend"][d] if R["trend"][d] is not None else np.nan for d in R["kitchen"]]),GREEN),
            ("Seasonal factor",np.tile(np.array(R["seasonal"]),7)[:n],ORANGE),("Residual",np.array([R["resid"][d] if R["resid"][d] is not None else np.nan for d in R["kitchen"]]),PURPLE)]
    H=110; gap=40
    for p,(title,vals,c) in enumerate(panels):
        Y0=60+p*(H+gap)+H; lo,hi=np.nanmin(vals),np.nanmax(vals); pad=(hi-lo)*0.08 or 1
        Y=lambda v: Y0-(v-(lo-pad))/((hi+pad)-(lo-pad))*H
        o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE)); o.append(text(X0,Y0-H-8,title,12.5,INK,"bold",family=HEAD))
        for lab,v in [(f"{hi:,.0f}" if hi>10 else f"{hi:.2f}",hi),(f"{lo:,.0f}" if hi>10 else f"{lo:.2f}",lo)]: o.append(text(X0-8,Y(v)+4,lab,10.5,MUTED,anchor="end"))
        if title in ("Seasonal factor","Residual"): o.append(line(X0,Y(1),X0+W,Y(1),MUTED,1,"4 4"))
        o.append(poly([(X(i),Y(v)) for i,v in enumerate(vals)],c,1.8))
        if p==3:
            for yr in range(2019,2026):
                i=list(k.index).index(pd.Timestamp(f"{yr}-01-01")); o.append(text(X(i),Y0+18,str(yr),11,MUTED,anchor="middle"))
    return svg(900,60+4*(H+gap)+10,"".join(o))

def fig_acf():
    o=[]; band=R["band"]
    for p,(title,vals,c) in enumerate([("ACF",R["acf"],ACC),("PACF",R["pacf"],GREEN)]):
        X0=80+p*440; W=360; Y0=300; H=220; bw=10
        Y=lambda v: Y0-H/2-v/1.1*(H/2); X=lambda lag: X0+lag/25*W
        o.append(line(X0,Y(0),X0+W,Y(0),INK,1.2)); o.append(line(X0,Y(band),X0+W,Y(band),MUTED,1,"5 4")); o.append(line(X0,Y(-band),X0+W,Y(-band),MUTED,1,"5 4"))
        for v in [-1,-0.5,0.5,1]: o.append(text(X0-8,Y(v)+4,f"{v:.1f}",10.5,MUTED,anchor="end"))
        for lag in range(1,25):
            v=vals[lag]; o.append(rect(X(lag)-bw/2,min(Y(0),Y(v)),bw,abs(Y(v)-Y(0)),fill=RED if abs(v)>band else c))
            if lag in (1,6,12,18,24): o.append(text(X(lag),Y0+16,str(lag),11,MUTED,anchor="middle"))
        o.append(text(X0,Y0-H-14,f"{title} of the differenced log series",13,INK,"bold",family=HEAD))
        o.append(text(X0+W/2,Y0+38,"Lag (months)",12,INK,anchor="middle"))
        o.append(text(X0+W,Y(band)-6,f"±{band:.2f}",10.5,MUTED,anchor="end"))
    return svg(900,360,"".join(o))

def fig_backtest():
    o=[]; X0=120; W=740; Y0=60; rh=44; n=84; X=lambda m: X0+m/n*W
    for f in range(5):
        cut=n-12*(5-f); y=Y0+f*rh
        o.append(rect(X(0),y,X(cut)-X(0),30,fill=ACC,rx=3)); o.append(rect(X(cut),y,X(cut+12)-X(cut),30,fill=ORANGE,rx=3))
        o.append(text(X0-10,y+20,f"Fold {f+1}",12.5,INK,"bold",anchor="end")); o.append(text(X(cut+12)+8,y+20,f"forecast {2021+f}",11.5,MUTED))
    for yr in range(2019,2027): o.append(line(X((yr-2019)*12),Y0+5*rh,X((yr-2019)*12),Y0+5*rh+6,INK,1)); o.append(text(X((yr-2019)*12),Y0+5*rh+22,str(yr),11,MUTED,anchor="middle"))
    o.append(line(X(0),Y0+5*rh,X(n),Y0+5*rh,INK,1.2))
    o.append(rect(X0,Y0+5*rh+40,14,14,fill=ACC,rx=2)); o.append(text(X0+22,Y0+5*rh+52,"training history",12,INK))
    o.append(rect(X0+180,Y0+5*rh+40,14,14,fill=ORANGE,rx=2)); o.append(text(X0+202,Y0+5*rh+52,"12-month forecast window, scored by WAPE",12,INK))
    return svg(960,Y0+5*rh+80,"".join(o))

def fig_sensor():
    o=[]; t=pd.Series(R["temp"]); t.index=pd.to_datetime(t.index); b=pd.Series(R["baseline"]); b.index=pd.to_datetime(b.index)
    pr=pd.Series(R["pressure"]); pr.index=pd.to_datetime(pr.index); n=len(t); X0=80; W=780
    X=lambda i: X0+i/(n-1)*W
    # temperature panel
    Y0=230; H=170; lo,hi=208,228; Y=lambda v: Y0-(v-lo)/(hi-lo)*H
    o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE)); o.append(text(X0,Y0-H-8,"Temperature (°C) with 24-hour median baseline",12.5,INK,"bold",family=HEAD))
    bv=b.to_numpy(); band_top=[(X(i),Y(v+6)) for i,v in enumerate(bv) if v==v]; band_bot=[(X(i),Y(v-6)) for i,v in enumerate(bv) if v==v]
    if band_top: o.append(f'<path d="M'+" L".join(f"{x:.1f},{y:.1f}" for x,y in band_top)+" L"+" L".join(f"{x:.1f},{y:.1f}" for x,y in band_bot[::-1])+f' Z" fill="{GREEN}" opacity="0.12"/>')
    o.append(poly([(X(i),Y(v)) for i,v in enumerate(t.to_numpy())],ACC,1)); o.append(poly([(X(i),Y(v)) for i,v in enumerate(bv)],GREEN,1.6))
    for v in [210,215,220,225]: o.append(text(X0-8,Y(v)+4,str(v),10.5,MUTED,anchor="end"))
    hot=int(np.argmax(t.to_numpy())); o.append(text(X(hot)-10,Y(226)-4,"heater fault, Wed night",11.5,RED,"bold",anchor="end"))
    # pressure panel
    Y0=470; H=170; lo,hi=95,155; Y=lambda v: Y0-(v-lo)/(hi-lo)*H
    o.append(rect(X0,Y0-H,W,H,fill="none",stroke=RULE)); o.append(text(X0,Y0-H-8,"Pressure (bar); stoppage minutes drawn as a gap",12.5,INK,"bold",family=HEAD))
    pv=pr.to_numpy().copy(); pv[np.array(R["status"])=="stopped"]=np.nan
    o.append(poly([(X(i),Y(min(v,155))) for i,v in enumerate(pv)],ORANGE,1))
    for v in [100,120,140]: o.append(text(X0-8,Y(v)+4,str(v),10.5,MUTED,anchor="end"))
    sp=int(np.nanargmax(pv)); o.append(text(X(sp)+8,Y(150),"pressure spikes, Tue noon",11.5,RED,"bold"))
    for d in range(7): i=d*1440; o.append(text(X(i)+2,Y0+18,["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][d],11,MUTED))
    return svg(900,500,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig40-1-decomposition.svg",fig_decomp),("fig40-2-acf-pacf.svg",fig_acf),("fig40-3-backtest.svg",fig_backtest),("fig40-4-sensor-anomalies.svg",fig_sensor)]:
        open(name,"w").write(fn())
    print("ok")
