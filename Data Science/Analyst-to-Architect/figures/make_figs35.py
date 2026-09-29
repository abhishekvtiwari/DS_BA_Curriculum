# Generates the SVG figures for Chapter 35. Run from figures/: python3 make_figs35.py
# Every number is recomputed from the companion CSV files (companion/ch35/), the same data as the chapter's code.
# Each figure prints at the full text width (493.2 pt). All canvases are 760 px wide, so a font of
# 11 px prints at 7.1 pt: no text in this file is smaller than 11 px (visual standard: >= 7 pt).
import math, pathlib
import numpy as np, pandas as pd
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"
DATA = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch35"
cust = pd.read_csv(DATA / "customers_2025.csv")
leads = pd.read_csv(DATA / "leads_2025.csv")
W = 760            # canvas width of every figure
FS = 11.5          # smallest font used (7.5 pt in print)

def arrow(x1,y1,x2,y2,c=MUTED,sw=2,head=10):
    a=math.atan2(y2-y1,x2-x1)
    p1=(x2-head*math.cos(a-0.4), y2-head*math.sin(a-0.4)); p2=(x2-head*math.cos(a+0.4), y2-head*math.sin(a+0.4))
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw)+f'<path d="M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def dot(x,y,r=5,c=ACC,stroke="#fff"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="{stroke}" stroke-width="1.5"/>'
def square(x,y,r=5,c=ACC): return f'<rect x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r}" height="{2*r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def triangle(x,y,r=6,c=ACC):
    return f'<path d="M{x:.1f},{y-r*1.15:.1f} L{x+r:.1f},{y+r*0.75:.1f} L{x-r:.1f},{y+r*0.75:.1f} Z" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def vtext(x,y,s,size=12,fill=INK,weight="normal"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="middle" transform="rotate(-90 {x} {y})">{s}</text>'

# ---------- Figure 35.1: product-mix vectors and angles ----------
def fig_vectors():
    o=[]; X0=64; Y0=300; S=260
    def P(u,v): return X0+u*S, Y0-v*S
    for t in [0,0.25,0.5,0.75,1.0]:
        o.append(line(X0,Y0-t*S,X0+S,Y0-t*S,"#eef1f5")); o.append(line(X0+t*S,Y0,X0+t*S,Y0-S,"#eef1f5"))
        o.append(text(X0-8,Y0-t*S+4,f"{t:.2f}",FS,MUTED,anchor="end")); o.append(text(X0+t*S,Y0+18,f"{t:.2f}",FS,MUTED,anchor="middle"))
    o.append(line(X0,Y0,X0+S+8,Y0,INK,1.3)); o.append(line(X0,Y0,X0,Y0-S-8,INK,1.3))
    o.append(text(X0+S/2,Y0+38,"Storage share",12.5,INK,"bold",anchor="middle"))
    o.append(vtext(X0-44,Y0-S/2,"Kitchen share",12.5,INK,"bold"))
    pick=[("Sharma Hardware",ACC),("Green Leaf Hotels",PURPLE),("Tasty Tiffins",ORANGE)]
    vecs={}
    for name,c in pick:
        r=cust[cust.customer_name==name].iloc[0]; u,v=r.storage_share,r.kitchen_share; vecs[name]=(u,v)
        x,y=P(u,v); o.append(arrow(X0,Y0,x,y,c,3,12)); o.append(dot(x,y,4,c))
        if name=="Sharma Hardware":
            o.append(text(x-6,y-24,name,12,c,"bold")); o.append(text(x-6,y-10,f"[{u:.3f}, {v:.3f}]",FS,c))
        else:
            o.append(text(x+10,y-6,name,12,c,"bold")); o.append(text(x+10,y+9,f"[{u:.3f}, {v:.3f}]",FS,c))
    def ang(n): return math.degrees(math.atan2(vecs[n][1],vecs[n][0]))
    a1,a2=ang("Sharma Hardware"),ang("Green Leaf Hotels"); R=92
    p=lambda a:(X0+R*math.cos(math.radians(a)), Y0-R*math.sin(math.radians(a)))
    (sx,sy),(ex,ey)=p(a1),p(a2)
    o.append(f'<path d="M{sx:.1f},{sy:.1f} A{R},{R} 0 0 0 {ex:.1f},{ey:.1f}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    mx,my=p((a1+a2)/2); o.append(text(mx+6,my+4,f"{a2-a1:.0f}°",12.5,GREEN,"bold"))
    bx=420
    o.append(text(bx,40,"Reading the picture",14,INK,"bold",family=HEAD))
    cos2=lambda a,b:(vecs[a][0]*vecs[b][0]+vecs[a][1]*vecs[b][1])/(math.hypot(*vecs[a])*math.hypot(*vecs[b]))
    rows=[("Each arrow is one customer's mix.",INK),
          ("Its direction says what they buy;",INK),("its length doesn't matter for similarity.",INK),("",INK),
          (f"Angle Sharma to Green Leaf: {a2-a1:.0f}°",GREEN),
          (f"cosine in these 2 dimensions = {cos2('Sharma Hardware','Green Leaf Hotels'):.3f}",GREEN),("",INK),
          (f"Angle Sharma to Tasty Tiffins: {ang('Tasty Tiffins')-a1:.0f}°",ORANGE),
          (f"cosine in these 2 dimensions = {cos2('Sharma Hardware','Tasty Tiffins'):.3f}",ORANGE),("",INK),
          ("Smaller angle, higher cosine, more alike.",INK)]
    for i,(l,c) in enumerate(rows): o.append(text(bx,68+i*20,l,12,c,"bold" if c!=INK else "normal"))
    o.append(text(bx,300,"Industrial and Furniture shares are zero for",FS,MUTED,style="italic"))
    o.append(text(bx,316,"these three, apart from Sharma's 3.4% Furniture.",FS,MUTED,style="italic"))
    return svg(W,340,"".join(o))

# ---------- shared data for sections 35.4-35.6 ----------
x=np.array([4,7,8,12.]); y=np.array([66,174,198,297.])
def loss(w): return np.mean((w*x-y)**2)
def run(lr,steps):
    w=b=0.0; ws=[]; ls=[]
    for _ in range(steps):
        e=w*x+b-y; ws.append((w,b)); ls.append(np.mean(e**2)); w-=lr*2*np.mean(e*x); b-=lr*2*np.mean(e)
    ws.append((w,b)); ls.append(np.mean((w*x+b-y)**2)); return ws,ls

# ---------- Figure 35.2: the loss valley (one weight, no intercept) ----------
def fig_valley():
    o=[]; X0=90; Y0=250; PW=620; PH=210
    X=lambda w: X0+(w-10)/25*PW; Y=lambda v: Y0-v/15000*PH
    for v in range(0,15001,5000):
        o.append(line(X0,Y(v),X0+PW,Y(v),"#eef1f5")); o.append(text(X0-8,Y(v)+4,f"{v:,}",FS,MUTED,anchor="end"))
    for w in range(10,36,5): o.append(text(X(w),Y0+18,str(w),FS,MUTED,anchor="middle"))
    o.append(line(X0,Y0,X0+PW,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-PH,INK,1.2))
    o.append(text(X0+PW/2,Y0+38,"w (₹ thousand of revenue per order)",12,INK,anchor="middle"))
    o.append(vtext(X0-58,Y0-PH/2,"Loss (mean squared error)",12))
    ws=np.linspace(10,35,201)
    o.append(path("M"+" L".join(f"{X(w):.1f},{Y(loss(w)):.1f}" for w in ws),stroke=ACC,sw=3))
    best=(x*y).sum()/(x*x).sum()
    o.append(line(X(18.5),Y(9000)+4,X(20),Y(loss(20))-7,ORANGE,1.2)); o.append(dot(X(20),Y(loss(20)),6,ORANGE))
    o.append(text(X(18.5),Y(9000),f"you are here: w = 20, loss {loss(20):,.2f}",12,ORANGE,"bold",anchor="middle"))
    o.append(line(X(best),Y(5200)+4,X(best),Y(loss(best))-7,GREEN,1.2)); o.append(dot(X(best),Y(loss(best)),6,GREEN))
    o.append(text(X(best)+30,Y(5200),f"bottom: w = {best:.2f}, loss {loss(best):,.2f}",12,GREEN,"bold",anchor="middle"))
    o.append(text(X0+PW,30,"Downhill from w = 20 means increasing w",FS,MUTED,style="italic",anchor="end"))
    return svg(W,300,"".join(o))

# ---------- Figure 35.3: three hand steps ----------
def fig_steps():
    o=[]; ws,ls=run(0.005,3); bw,bb=np.polyfit(x,y,1)
    X0=62; Y0=280; PW=300; PH=230
    X=lambda v: X0+(v-2)/12*PW; Y=lambda v: Y0-v/330*PH
    o.append(text(X0-40,24,"Fitted line after each step",13.5,INK,"bold",family=HEAD))
    for v in range(0,331,100):
        o.append(line(X0,Y(v),X0+PW,Y(v),"#eef1f5")); o.append(text(X0-8,Y(v)+4,f"{v}",FS,MUTED,anchor="end"))
    for v in range(2,15,2): o.append(text(X(v),Y0+18,str(v),FS,MUTED,anchor="middle"))
    o.append(text(X0+PW/2,Y0+38,"Orders in 2025",12,INK,anchor="middle"))
    o.append(vtext(X0-44,Y0-PH/2,"Revenue, ₹ thousand",12))
    o.append(line(X0,Y0,X0+PW,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-PH,INK,1.2))
    cols=["#9bb7cc","#5e8fb3",ACC]; dashes=["2 4","6 4",None]
    for i,(w,b) in enumerate(ws[1:]):
        o.append(line(X(2),Y(w*2+b),X(14),Y(w*14+b),cols[i],2.4,dashes[i])); o.append(text(X(14)+6,Y(w*14+b)+4,f"step {i+1}",FS,cols[i] if i else "#5e8fb3","bold"))
    xe=(330-bb)/bw; o.append(line(X(2),Y(bw*2+bb),X(xe),Y(330),GREEN,2.6,"9 4"))
    o.append(text(X(xe)-14,Y(330)+4,"least squares",FS,GREEN,"bold",anchor="end"))
    for xi,yi in zip(x,y): o.append(dot(X(xi),Y(yi),6,ORANGE))
    bx=478; base=280; bwid=52; gap=18; Hh=220
    o.append(text(bx-10,24,"Loss before each step",13.5,INK,"bold",family=HEAD))
    labels=["step 1","step 2","step 3","after 3"]
    for i,(l,lab) in enumerate(zip(ls,labels)):
        h=max(2,l/41000*Hh); xx=bx+i*(bwid+gap)
        o.append(rect(xx,base-h,bwid,h,fill=ACC if i<3 else GREEN,rx=3))
        o.append(text(xx+bwid/2,base-h-7,f"{l:,.0f}",12,INK,"bold",anchor="middle"))
        o.append(text(xx+bwid/2,base+18,lab,FS,MUTED,anchor="middle"))
    o.append(line(bx-8,base,bx+4*(bwid+gap)-gap+8,base,RULE,1.2))
    return svg(W,330,"".join(o))

# ---------- Figure 35.4: learning rates ----------
def fig_lr():
    o=[]; X0=90; Y0=270; PW=420; PH=240; steps=30
    lo,hi=1,7
    X=lambda i: X0+i/(steps-1)*PW; Y=lambda v: Y0-(math.log10(v)-lo)/(hi-lo)*PH
    for k in range(lo,hi+1):
        o.append(line(X0,Y(10**k),X0+PW,Y(10**k),"#eef1f5")); o.append(text(X0-8,Y(10**k)+4,f"{10**k:,}",FS,MUTED,anchor="end"))
    for i in [0,4,9,14,19,24,29]: o.append(text(X(i),Y0+18,str(i+1),FS,MUTED,anchor="middle"))
    o.append(text(X0+PW/2,Y0+38,"Step",12,INK,anchor="middle"))
    o.append(vtext(X0-74,Y0-PH/2,"Loss (log scale)",12))
    o.append(line(X0,Y0,X0+PW,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-PH,INK,1.2))
    for lr,c,lab,dash in [(0.0005,PURPLE,"0.0005: too small","7 4"),(0.005,GREEN,"0.005: about right",None),(0.015,RED,"0.015: too large","2 3")]:
        _,ls=run(lr,steps-1)
        o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(ls)),stroke=c,sw=2.6,dash=dash))
        o.append(text(X(steps-1)+10,Y(ls[-1])+4,f"{lab} ({ls[-1]:,.0f})",12,c,"bold"))
    return svg(W,310,"".join(o))

# ---------- Figure 35.5: likelihood ----------
def fig_like():
    o=[]; X0=90; Y0=270; PW=600; PH=220
    ps=np.linspace(0.001,0.6,400); L=ps**6*(1-ps)**24; Lmax=L.max()
    X=lambda p: X0+p/0.6*PW; Y=lambda v: Y0-v/(Lmax*1.15)*PH
    for t in np.arange(0,0.61,0.1):
        o.append(line(X(t),Y0,X(t),Y0-PH,"#eef1f5")); o.append(text(X(t),Y0+18,f"{t:.1f}",FS,MUTED,anchor="middle"))
    for v in [0,1,2,3]:
        o.append(line(X0,Y(v*1e-7),X0+PW,Y(v*1e-7),"#eef1f5")); o.append(text(X0-8,Y(v*1e-7)+4,str(v),FS,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+PW,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-PH,INK,1.2))
    o.append(text(X0+PW/2,Y0+38,"Win rate p",12,INK,anchor="middle"))
    o.append(vtext(X0-40,Y0-PH/2,"Likelihood, in 0.0000001s",12))
    o.append(path("M"+" L".join(f"{X(p):.1f},{Y(v):.1f}" for p,v in zip(ps,L)),stroke=ACC,sw=3))
    for p,c in [(0.1,MUTED),(0.2,GREEN),(0.3,MUTED)]:
        v=p**6*(1-p)**24; o.append(line(X(p),Y0,X(p),Y(v),c,1.2,"4 4")); o.append(dot(X(p),Y(v),6,c))
        lab=f"p = {p}: {v*1e7:.2f}"
        if p==0.2: o.append(text(X(p)+10,Y(v)-6,lab,12,c,"bold"))
        else: o.append(text(X(p)+10,Y(v)-8,lab,12,c,"bold"))
    o.append(text(X0+PW,32,"maximum likelihood estimate = 6 ÷ 30 = 0.2",12.5,GREEN,"bold",anchor="end"))
    return svg(W,310,"".join(o))

# ---------- Figure 35.6: small PCA ----------
def fig_pca_small():
    o=[]; pts=np.array([[16,50],[16,33],[10,41],[7,17],[4,5]],float); nm=["Sharma","Metro","Harbour","Patel","Blue Bay"]
    m=pts.mean(0); Z=pts-m; C=Z.T@Z/4; vals,vecs=np.linalg.eigh(C); vals=vals[::-1]; vecs=vecs[:,::-1]
    v1=vecs[:,0]*np.sign(vecs[1,0]); v2=np.array([v1[1],-v1[0]])
    X0=70; Y0=300; S=5.0     # 1 revenue unit = 5 px; orders drawn 3x wider
    X=lambda a: X0+a*S*3.0; Y=lambda b: Y0-b*S
    for t in range(0,21,4): o.append(line(X(t),Y0,X(t),Y(56),"#eef1f5")); o.append(text(X(t),Y0+18,str(t),FS,MUTED,anchor="middle"))
    for t in range(0,56,10): o.append(line(X0,Y(t),X(20),Y(t),"#eef1f5")); o.append(text(X0-8,Y(t)+4,str(t),FS,MUTED,anchor="end"))
    o.append(line(X0,Y0,X(20),Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y(56),INK,1.2))
    o.append(text((X0+X(20))/2,Y0+38,"Orders",12,INK,anchor="middle"))
    o.append(vtext(X0-40,Y(28),"Revenue, ₹ ten-thousands",12))
    k=26; o.append(arrow(X(m[0]-v1[0]*k),Y(m[1]-v1[1]*k),X(m[0]+v1[0]*k),Y(m[1]+v1[1]*k),GREEN,3,13))
    k2=math.sqrt(vals[1]/vals[0])*k*1.3
    o.append(arrow(X(m[0]),Y(m[1]),X(m[0]+v2[0]*k2),Y(m[1]+v2[1]*k2),ORANGE,3,11))
    off={"Sharma":(-10,-2,"end"),"Metro":(10,4,"start"),"Harbour":(-10,4,"end"),"Patel":(10,10,"start"),"Blue Bay":(10,6,"start")}
    for (a,b),n in zip(pts,nm):
        dx,dy,anc=off[n]; o.append(dot(X(a),Y(b),6,ACC)); o.append(text(X(a)+dx,Y(b)+dy,n,12,INK,anchor=anc))
    o.append(dot(X(m[0]),Y(m[1]),5,INK)); o.append(text(X(m[0])-12,Y(m[1])-8,"average (10.6, 29.2)",FS,MUTED,anchor="end"))
    tip=(X(m[0]+v1[0]*k),Y(m[1]+v1[1]*k)); o.append(text(tip[0]+8,tip[1]+14,"PC1",12.5,GREEN,"bold"))
    o.append(text(X(m[0]+v2[0]*k2)+8,Y(m[1]+v2[1]*k2)+4,"PC2",12.5,ORANGE,"bold"))
    bx=430; o.append(text(bx,50,"Principal components",14,INK,"bold",family=HEAD))
    rows=[(f"PC1 direction [{v1[0]:.3f}, {v1[1]:.3f}]",GREEN),(f"variance {vals[0]:.2f} = {vals[0]/vals.sum():.1%} of total",GREEN),("",INK),
          (f"PC2 direction [{v2[0]:.3f}, {v2[1]:.3f}]".replace("-","−"),ORANGE),(f"variance {vals[1]:.2f} = {vals[1]/vals.sum():.1%} of total",ORANGE),("",INK),
          ("The two components are at right angles.",INK),("Orders are drawn 3 times wider than",MUTED),("revenue so the points are easier to see,",MUTED),("which makes the right angle look slanted.",MUTED)]
    for i,(l,c) in enumerate(rows): o.append(text(bx,80+i*20,l,12,c,"bold" if c in (GREEN,ORANGE) else "normal"))
    return svg(W,340,"".join(o))

# ---------- Figure 35.7: PCA of all customers ----------
def fig_pca_all():
    feats=["orders","revenue","avg_order_value","avg_discount_pct","storage_share","kitchen_share","industrial_share"]
    F=cust[feats].to_numpy(float); Fs=(F-F.mean(0))/F.std(0)
    vals,vecs=np.linalg.eigh(np.cov(Fs,rowvar=False)); idx=np.argsort(vals)[::-1]; vals=vals[idx]; vecs=vecs[:,idx]
    sg=np.sign(vecs[feats.index("industrial_share"),:]); sg[1]=np.sign(vecs[feats.index("storage_share"),1]); vecs=vecs*sg
    sc=Fs@vecs; share=vals/vals.sum()
    o=[]; X0=112; Y0=330; PW=480; PH=300
    X=lambda a: X0+(a+3)/7.5*PW; Y=lambda b: Y0-(b+3)/6.5*PH
    for t in range(-3,5): o.append(line(X(t),Y0,X(t),Y0-PH,"#eef1f5")); o.append(text(X(t),Y0+18,str(t),FS,MUTED,anchor="middle"))
    for t in range(-3,4): o.append(line(X0,Y(t),X0+PW,Y(t),"#eef1f5")); o.append(text(X0-8,Y(t)+4,str(t),FS,MUTED,anchor="end"))
    o.append(line(X(0),Y0,X(0),Y0-PH,RULE,1.2)); o.append(line(X0,Y(0),X0+PW,Y(0),RULE,1.2))
    o.append(text(X0+PW/2,Y0+38,f"PC1 ({share[0]:.1%}): kitchenware buyers (left) to wholesale crate buyers (right)",12,INK,anchor="middle"))
    o.append(vtext(X0-76,Y0-PH/2,f"PC2 ({share[1]:.1%})",12,INK,"bold"))
    o.append(vtext(X0-60,Y0-PH/2,"down: many orders · up: few, storage-only orders",FS,INK))
    shape={"Wholesale":(triangle,ORANGE),"Retail":(dot,ACC),"Hospitality":(square,PURPLE)}
    label={"Prime Wholesale":(10,4),"City Needs Store":(10,4),"Harbour Traders":(0,-12),"Green Leaf Hotels":(10,4),"Sharma Hardware":(10,4),"Tasty Tiffins":(-6,22),"Western Logistics":(10,-8),"Royal Banquets":(10,4)}
    for (a,b),n,s in zip(sc[:,:2],cust.customer_name,cust.segment):
        fn,c=shape[s]; o.append(fn(X(a),Y(b),6,c))
        if n in label:
            dx,dy=label[n]; o.append(text(X(a)+dx,Y(b)+dy,n,FS,INK,anchor="end" if dx<-6 else ("middle" if dx==0 else "start")))
    lx=630; o.append(text(lx-6,50,"Segment",12.5,INK,"bold"))
    for i,(s,(fn,c)) in enumerate(shape.items()):
        o.append(fn(lx+6,72+i*24,6,c)); o.append(text(lx+20,76+i*24,s,12,INK))
    return svg(W,380,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig35-1-vectors-angle.svg",fig_vectors),("fig35-1b-loss-valley.svg",fig_valley),("fig35-2-gradient-steps.svg",fig_steps),
                    ("fig35-3-learning-rates.svg",fig_lr),("fig35-4-likelihood.svg",fig_like),("fig35-5-pca-small.svg",fig_pca_small),
                    ("fig35-6-pca-customers.svg",fig_pca_all)]:
        open(name,"w").write(fn())
    print("ok")
