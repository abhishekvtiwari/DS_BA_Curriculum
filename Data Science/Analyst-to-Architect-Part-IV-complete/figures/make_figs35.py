# Generates the SVG figures for Chapter 35. Run from figures/: python3 make_figs35.py
# Every number is recomputed from the companion CSV files (companion/ch35/), the same data as the chapter's code.
import math, pathlib
import numpy as np, pandas as pd
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"
DATA = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch35"
cust = pd.read_csv(DATA / "customers_2025.csv")
leads = pd.read_csv(DATA / "leads_2025.csv")

def arrow(x1,y1,x2,y2,c=MUTED,sw=2,head=10):
    a=math.atan2(y2-y1,x2-x1)
    p1=(x2-head*math.cos(a-0.4), y2-head*math.sin(a-0.4)); p2=(x2-head*math.cos(a+0.4), y2-head*math.sin(a+0.4))
    return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw)+f'<path d="M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def dot(x,y,r=5,c=ACC,stroke="#fff"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="{stroke}" stroke-width="1.5"/>'
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)

# ---------- Figure 35.1: product-mix vectors and angles ----------
def fig_vectors():
    o=[]; X0=110; Y0=440; S=380
    def P(u,v): return X0+u*S, Y0-v*S
    for t in [0,0.25,0.5,0.75,1.0]:
        o.append(line(X0,Y0-t*S,X0+S,Y0-t*S,"#eef1f5")); o.append(line(X0+t*S,Y0,X0+t*S,Y0-S,"#eef1f5"))
        o.append(text(X0-10,Y0-t*S+4,f"{t:.2f}",11.5,MUTED,anchor="end")); o.append(text(X0+t*S,Y0+20,f"{t:.2f}",11.5,MUTED,anchor="middle"))
    o.append(line(X0,Y0,X0+S+10,Y0,INK,1.3)); o.append(line(X0,Y0,X0,Y0-S-10,INK,1.3))
    o.append(text(X0+S/2,Y0+44,"Storage share",13,INK,"bold",anchor="middle"))
    o.append(f'<text x="{X0-58}" y="{Y0-S/2}" font-size="13" fill="{INK}" font-weight="bold" text-anchor="middle" transform="rotate(-90 {X0-58} {Y0-S/2})">Kitchen share</text>')
    pick=[("Sharma Hardware",ACC),("Green Leaf Hotels",PURPLE),("Tasty Tiffins",ORANGE)]
    vecs={}
    for name,c in pick:
        r=cust[cust.customer_name==name].iloc[0]; u,v=r.storage_share,r.kitchen_share; vecs[name]=(u,v)
        x,y=P(u,v); o.append(arrow(X0,Y0,x,y,c,3,13)); o.append(dot(x,y,4,c))
        if name=="Sharma Hardware": o.append(text(x-40,y+30,f"{name} [{u:.3f}, {v:.3f}]",12.5,c,"bold"))
        else: o.append(text(x+10,y-8,f"{name} [{u:.3f}, {v:.3f}]",12.5,c,"bold"))
    def ang(n): return math.degrees(math.atan2(vecs[n][1],vecs[n][0]))
    # angle arc between Sharma and Green Leaf
    a1,a2=ang("Sharma Hardware"),ang("Green Leaf Hotels"); R=120
    p=lambda a:(X0+R*math.cos(math.radians(a)), Y0-R*math.sin(math.radians(a)))
    (sx,sy),(ex,ey)=p(a1),p(a2)
    o.append(f'<path d="M{sx:.1f},{sy:.1f} A{R},{R} 0 0 0 {ex:.1f},{ey:.1f}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    mx,my=p((a1+a2)/2); o.append(text(mx+8,my+2,f"{a2-a1:.0f}°",13,GREEN,"bold"))
    # right panel: explanation
    bx=640
    o.append(text(bx,90,"Reading the picture",15,INK,"bold",family=HEAD))
    cos2=lambda a,b:(vecs[a][0]*vecs[b][0]+vecs[a][1]*vecs[b][1])/(math.hypot(*vecs[a])*math.hypot(*vecs[b]))
    lines=[("Each arrow is one customer's mix.",INK),
           ("Its direction says what they buy;",INK),("its length doesn't matter for similarity.",INK),("",INK),
           (f"Angle Sharma → Green Leaf: {a2-a1:.0f}°",GREEN),
           (f"cosine in these 2 dimensions = {cos2('Sharma Hardware','Green Leaf Hotels'):.3f}",GREEN),("",INK),
           (f"Angle Sharma → Tasty Tiffins: {ang('Tasty Tiffins')-a1:.0f}°",ORANGE),
           (f"cosine in these 2 dimensions = {cos2('Sharma Hardware','Tasty Tiffins'):.3f}",ORANGE),("",INK),
           ("Smaller angle, higher cosine, more alike.",INK)]
    for i,(l,c) in enumerate(lines): o.append(text(bx,124+i*24,l,13,c,"bold" if c!=INK else "normal"))
    o.append(text(bx,420,"Industrial and Furniture shares are zero for these",11.5,MUTED,style="italic"))
    o.append(text(bx,438,"three customers, apart from Sharma's 3.4% Furniture.",11.5,MUTED,style="italic"))
    return svg(1000,500,"".join(o))

# ---------- shared gradient descent run ----------
x=np.array([4,7,8,12.]); y=np.array([66,174,198,297.])
def run(lr,steps):
    w=b=0.0; ws=[]; ls=[]
    for _ in range(steps):
        e=w*x+b-y; ws.append((w,b)); ls.append(np.mean(e**2)); w-=lr*2*np.mean(e*x); b-=lr*2*np.mean(e)
    ws.append((w,b)); ls.append(np.mean((w*x+b-y)**2)); return ws,ls

# ---------- Figure 35.2: three hand steps ----------
def fig_steps():
    o=[]; ws,ls=run(0.005,3); bw,bb=np.polyfit(x,y,1)
    X0=80; Y0=400; W=400; H=330
    X=lambda v: X0+(v-2)/12*W; Y=lambda v: Y0-v/330*H
    o.append(text(X0,40,"Fitted line after each step",14.5,INK,"bold",family=HEAD))
    for v in range(0,331,50):
        o.append(line(X0,Y(v),X0+W,Y(v),"#eef1f5")); o.append(text(X0-8,Y(v)+4,f"{v}",11.5,MUTED,anchor="end"))
    for v in range(2,15,2): o.append(text(X(v),Y0+20,str(v),11.5,MUTED,anchor="middle"))
    o.append(text(X0+W/2,Y0+44,"Orders in 2025",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-50}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-50} {Y0-H/2})">Revenue, ₹ thousand</text>')
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    cols=["#9bb7cc","#5e8fb3",ACC]
    for i,(w,b) in enumerate(ws[1:]):
        o.append(line(X(2),Y(w*2+b),X(14),Y(w*14+b),cols[i],2.2)); o.append(text(X(14)+6,Y(w*14+b)+4,f"after step {i+1}",11.5,cols[i],"bold"))
    xe=(330-bb)/bw; o.append(line(X(2),Y(bw*2+bb),X(xe),Y(330),GREEN,2.4,"7 5")); o.append(text(X(10.2),Y(330)+12,"least-squares line",11.5,GREEN,"bold",anchor="end"))
    for xi,yi in zip(x,y): o.append(dot(X(xi),Y(yi),6,ORANGE))
    # right: loss bars
    bx=610; base=400; bwid=70; gap=30; Hh=320
    o.append(text(bx,40,"Loss before each step",14.5,INK,"bold",family=HEAD))
    labels=["step 1","step 2","step 3","after 3"]
    for i,(l,lab) in enumerate(zip(ls,labels)):
        h=max(2,l/41000*Hh); xx=bx+i*(bwid+gap)
        o.append(rect(xx,base-h,bwid,h,fill=ACC if i<3 else GREEN,rx=3))
        o.append(text(xx+bwid/2,base-h-8,f"{l:,.0f}",13,INK,"bold",anchor="middle"))
        o.append(text(xx+bwid/2,base+20,lab,12,MUTED,anchor="middle"))
    o.append(line(bx-10,base,bx+4*(bwid+gap)-gap+10,base,RULE,1.2))
    return svg(1040,460,"".join(o))

# ---------- Figure 35.3: learning rates ----------
def fig_lr():
    o=[]; X0=110; Y0=400; W=640; H=340; steps=30
    lo,hi=1,7   # log10 range 10..10^7
    X=lambda i: X0+i/(steps-1)*W; Y=lambda v: Y0-(math.log10(v)-lo)/(hi-lo)*H
    for k in range(lo,hi+1):
        o.append(line(X0,Y(10**k),X0+W,Y(10**k),"#eef1f5")); o.append(text(X0-10,Y(10**k)+4,f"{10**k:,}",11.5,MUTED,anchor="end"))
    for i in [0,4,9,14,19,24,29]: o.append(text(X(i),Y0+20,str(i+1),11.5,MUTED,anchor="middle"))
    o.append(text(X0+W/2,Y0+44,"Step",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-86}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-86} {Y0-H/2})">Loss (log scale)</text>')
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    for lr,c,lab in [(0.0005,PURPLE,"0.0005: too small"),(0.005,GREEN,"0.005: about right"),(0.015,RED,"0.015: too large")]:
        _,ls=run(lr,steps-1)
        o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(ls)),stroke=c,sw=2.6))
        o.append(text(X(steps-1)+10,Y(ls[-1])+4,f"{lab} ({ls[-1]:,.0f})",12.5,c,"bold"))
    return svg(1040,460,"".join(o))

# ---------- Figure 35.4: likelihood ----------
def fig_like():
    o=[]; X0=110; Y0=380; W=760; H=300
    ps=np.linspace(0.001,0.6,400); L=ps**6*(1-ps)**24; Lmax=L.max()
    X=lambda p: X0+p/0.6*W; Y=lambda v: Y0-v/(Lmax*1.1)*H
    for t in np.arange(0,0.61,0.1):
        o.append(line(X(t),Y0,X(t),Y0-H,"#eef1f5")); o.append(text(X(t),Y0+20,f"{t:.1f}",11.5,MUTED,anchor="middle"))
    for v in [0,1e-7,2e-7,3e-7]:
        o.append(line(X0,Y(v),X0+W,Y(v),"#eef1f5")); o.append(text(X0-10,Y(v)+4,f"{v*1e7:.0f} × 10⁻⁷" if v else "0",11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y0-H,INK,1.2))
    o.append(text(X0+W/2,Y0+44,"Win rate p",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-82}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-82} {Y0-H/2})">Likelihood p⁶(1 − p)²⁴</text>')
    o.append(path("M"+" L".join(f"{X(p):.1f},{Y(v):.1f}" for p,v in zip(ps,L)),stroke=ACC,sw=3))
    for p,c in [(0.1,MUTED),(0.2,GREEN),(0.3,MUTED)]:
        v=p**6*(1-p)**24; o.append(line(X(p),Y0,X(p),Y(v),c,1.2,"4 4")); o.append(dot(X(p),Y(v),6,c))
        e=math.floor(math.log10(v)); sup=str(-e).translate(str.maketrans("0123456789","⁰¹²³⁴⁵⁶⁷⁸⁹"))
        lab=f"p = {p}: {v/10**e:.2f} × 10⁻{sup}"
        if p==0.1: o.append(text(X(p)-12,Y(v)-10,lab,12.5,c,"bold",anchor="end"))
        elif p==0.2: o.append(text(X(p),Y(v)-14,lab,12.5,c,"bold",anchor="middle"))
        else: o.append(text(X(p)+12,Y(v)-14,lab,12.5,c,"bold"))
    o.append(text(X(0.2),Y0-H-6,"maximum likelihood estimate = 6 ÷ 30 = 0.2",13,GREEN,"bold",anchor="middle"))
    return svg(1000,440,"".join(o))

# ---------- Figure 35.5: small PCA ----------
def fig_pca_small():
    o=[]; pts=np.array([[16,50],[16,33],[10,41],[7,17],[4,5]],float); nm=["Sharma","Metro","Harbour","Patel","Blue Bay"]
    m=pts.mean(0); Z=pts-m; C=Z.T@Z/4; vals,vecs=np.linalg.eigh(C); vals=vals[::-1]; vecs=vecs[:,::-1]
    v1=vecs[:,0]*np.sign(vecs[1,0]); v2=vecs[:,1]*np.sign(vecs[0,1]*-1 if vecs[0,1]<0 else 1)
    X0=110; Y0=440; S=7.2   # same scale on both axes so right angles look right
    X=lambda a: X0+a*S*3.0; Y=lambda b: Y0-b*S
    for t in range(0,21,4): o.append(line(X(t),Y0,X(t),Y(58),"#eef1f5")); o.append(text(X(t),Y0+20,str(t),11.5,MUTED,anchor="middle"))
    for t in range(0,56,10): o.append(line(X0,Y(t),X(20),Y(t),"#eef1f5")); o.append(text(X0-10,Y(t)+4,str(t),11.5,MUTED,anchor="end"))
    o.append(line(X0,Y0,X(20),Y0,INK,1.2)); o.append(line(X0,Y0,X0,Y(58),INK,1.2))
    o.append(text((X0+X(20))/2,Y0+44,"Orders",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-50}" y="{Y(29)}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-50} {Y(29)})">Revenue, ₹ ten-thousands</text>')
    k=24; o.append(arrow(X(m[0]-v1[0]*k),Y(m[1]-v1[1]*k),X(m[0]+v1[0]*k),Y(m[1]+v1[1]*k),GREEN,3,14))
    k2=math.sqrt(vals[1]/vals[0])*k*1.3
    o.append(arrow(X(m[0]),Y(m[1]),X(m[0]+v2[0]*k2),Y(m[1]+v2[1]*k2),ORANGE,3,12))
    for (a,b),n in zip(pts,nm): o.append(dot(X(a),Y(b),6,ACC)); o.append(text(X(a)+10,Y(b)+4,n,12,INK))
    o.append(dot(X(m[0]),Y(m[1]),5,INK)); o.append(text(X(m[0])+12,Y(m[1])+18,"average (10.6, 29.2)",11.5,MUTED))
    o.append(text(X(m[0]+v1[0]*k)-14,Y(m[1]+v1[1]*k)+6,"PC1",13,GREEN,"bold",anchor="end")); o.append(text(X(m[0]+v2[0]*k2)-6,Y(m[1]+v2[1]*k2)-10,"PC2",13,ORANGE,"bold",anchor="end"))
    bx=660; o.append(text(bx,90,"Principal components",15,INK,"bold",family=HEAD))
    L=[(f"PC1 direction [{v1[0]:.3f}, {v1[1]:.3f}]",GREEN),(f"variance {vals[0]:.2f} = {vals[0]/vals.sum():.1%} of total",GREEN),("",INK),
       (f"PC2 direction [{v2[0]:.3f}, {v2[1]:.3f}]".replace("-","−"),ORANGE),(f"variance {vals[1]:.2f} = {vals[1]/vals.sum():.1%} of total",ORANGE),("",INK),
       ("The two components are at right angles.",INK),("Orders are drawn 3× wider than revenue so",MUTED),("the points are easier to see, which makes",MUTED),("the right angle look slanted.",MUTED)]
    for i,(l,c) in enumerate(L): o.append(text(bx,124+i*24,l,13,c,"bold" if c in (GREEN,ORANGE) else "normal"))
    return svg(1040,500,"".join(o))

# ---------- Figure 35.6: PCA of all customers ----------
def fig_pca_all():
    feats=["orders","revenue","avg_order_value","avg_discount_pct","storage_share","kitchen_share","industrial_share"]
    F=cust[feats].to_numpy(float); Fs=(F-F.mean(0))/F.std(0)
    vals,vecs=np.linalg.eigh(np.cov(Fs,rowvar=False)); idx=np.argsort(vals)[::-1]; vals=vals[idx]; vecs=vecs[:,idx]
    sg=np.sign(vecs[feats.index("industrial_share"),:]); sg[1]=np.sign(vecs[feats.index("storage_share"),1]); vecs=vecs*sg
    sc=Fs@vecs; share=vals/vals.sum()
    o=[]; X0=140; Y0=460; W=680; H=400
    X=lambda a: X0+(a+3)/7.5*W; Y=lambda b: Y0-(b+3)/6.5*H
    for t in range(-3,5): o.append(line(X(t),Y0,X(t),Y0-H,"#eef1f5")); o.append(text(X(t),Y0+20,str(t),11.5,MUTED,anchor="middle"))
    for t in range(-3,4): o.append(line(X0,Y(t),X0+W,Y(t),"#eef1f5")); o.append(text(X0-10,Y(t)+4,str(t),11.5,MUTED,anchor="end"))
    o.append(line(X(0),Y0,X(0),Y0-H,RULE,1.2)); o.append(line(X0,Y(0),X0+W,Y(0),RULE,1.2))
    o.append(text(X0+W/2,Y0+44,f"PC1 ({share[0]:.1%}): kitchenware buyers ← → wholesale crate buyers",12.5,INK,anchor="middle"))
    o.append(f'<text x="{X0-48}" y="{Y0-H/2}" font-size="12.5" fill="{INK}" text-anchor="middle" transform="rotate(-90 {X0-48} {Y0-H/2})">PC2 ({share[1]:.1%}): many orders ← → few storage-only orders</text>')
    colors={"Wholesale":ORANGE,"Retail":ACC,"Hospitality":PURPLE}
    label={"Prime Wholesale":(10,4),"City Needs Store":(10,4),"Harbour Traders":(0,-14),"Green Leaf Hotels":(10,4),"Sharma Hardware":(10,4),"Tasty Tiffins":(8,20),"Western Logistics":(10,-8),"Royal Banquets":(10,4)}
    for (a,b),n,s in zip(sc[:,:2],cust.customer_name,cust.segment):
        o.append(dot(X(a),Y(b),7,colors[s]))
        if n in label:
            dx,dy=label[n]; o.append(text(X(a)+dx,Y(b)+dy,n,11.5,INK,anchor="end" if dx<0 else ("middle" if dx==0 else "start")))
    lx=860
    for i,(s,c) in enumerate(colors.items()):
        o.append(dot(lx,110+i*28,7,c)); o.append(text(lx+16,115+i*28,s,13,INK))
    return svg(1040,520,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig35-1-vectors-angle.svg",fig_vectors),("fig35-2-gradient-steps.svg",fig_steps),("fig35-3-learning-rates.svg",fig_lr),
                    ("fig35-4-likelihood.svg",fig_like),("fig35-5-pca-small.svg",fig_pca_small),("fig35-6-pca-customers.svg",fig_pca_all)]:
        open(name,"w").write(fn())
    print("ok")
