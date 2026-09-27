# Generates the SVG figures for Chapter 38. Run from figures/ after checks/ch38_check.py has written ch38_results.json.
import json, pathlib
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch38_results.json").read_text())
CLUSTER_COLORS = [ACC, ORANGE, GREEN, PURPLE]
NAMES = {0: "Growing regulars", 1: "Key accounts", 2: "Occasional buyers", 3: "Drifting away"}
def line(x1,y1,x2,y2,c=RULE,sw=1,dash=None): return path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}",stroke=c,sw=sw,dash=dash)
def dot(x,y,c,r=3.4,stroke="none"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" opacity="0.75"/>'
def poly(pts,c,sw=2.6): return path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=sw)

def fig_choose_k():
    o=[]; X0=110; Y0=360; W=680; H=280; data=R["k"]
    X=lambda k: X0+(k-2)/6*W
    Yi=lambda v: Y0-(v-13000)/13500*H; Ys=lambda v: Y0-(v-0.15)/0.16*H
    for k,_,_ in data: o.append(line(X(k),Y0,X(k),Y0-H,PALE)); o.append(text(X(k),Y0+20,str(k),12,MUTED,anchor="middle"))
    for v in [15000,20000,25000]: o.append(text(X0-10,Yi(v)+4,f"{v//1000}k",11.5,ACC,anchor="end"))
    for v in [0.15,0.20,0.25,0.30]: o.append(text(X0+W+10,Ys(v)+4,f"{v:.2f}",11.5,GREEN))
    o.append(line(X0,Y0,X0+W,Y0,INK,1.2))
    o.append(poly([(X(k),Yi(i)) for k,i,_ in data],ACC)); o.append(poly([(X(k),Ys(s)) for k,_,s in data],GREEN))
    for k,i,s in data: o.append(dot(X(k),Yi(i),ACC,5)); o.append(dot(X(k),Ys(s),GREEN,5))
    o.append(text(X(2)+8,Ys(data[0][2])-14,f"silhouette peaks at k = 2 ({data[0][2]:.3f})",12.5,GREEN,"bold"))
    o.append(text(X(4),Yi(data[2][1])+26,"k = 4 chosen: stable and usable",12.5,ACC,"bold",anchor="middle"))
    o.append(text(X0-10,Y0-H-16,"Inertia",13,ACC,"bold")); o.append(text(X0+W,Y0-H-16,"Silhouette",13,GREEN,"bold",anchor="end"))
    o.append(text(X0+W/2,Y0+44,"Number of clusters (k)",12.5,INK,anchor="middle"))
    return svg(900,420,"".join(o))

def fig_profiles():
    o=[]; X0=250; Y0=90; rowh=96; W=520
    prof=R["profile"]
    maxes={"revenue":max(p["revenue"] for p in prof.values()), "orders":max(p["orders"] for p in prof.values()),
           "recency":max(p["recency"] for p in prof.values()), "churn":max(p["churn"] for p in prof.values())}
    cols=[("revenue","Median revenue","₹{:,.0f}"),("orders","Orders","{:.0f}"),("recency","Days since order","{:.0f}"),("churn","Churn rate","{:.1%}")]
    cw=W/4
    for j,(_,label,_) in enumerate(cols): o.append(text(X0+j*cw+cw/2-10,Y0-16,label,12,MUTED,anchor="middle"))
    for i,(cid,p) in enumerate(sorted(prof.items(), key=lambda kv: -kv[1]["revenue"])):
        y=Y0+i*rowh; c=CLUSTER_COLORS[int(cid)]
        o.append(text(X0-20,y+22,NAMES[int(cid)],14,INK,"bold",anchor="end",family=HEAD))
        o.append(text(X0-20,y+42,f"{p['size']:,} accounts · {p['revenue_share']:.1%} of revenue",12,MUTED,anchor="end"))
        for j,(key,_,fmt) in enumerate(cols):
            w=max(3,p[key]/maxes[key]*(cw-40))
            o.append(rect(X0+j*cw,y+8,w,20,fill=c,rx=3))
            o.append(text(X0+j*cw,y+46,fmt.format(p[key]),12,INK))
    o.append(text(X0-20,Y0-16,"Cluster",12,MUTED,anchor="end"))
    return svg(820,90+4*rowh+30,"".join(o))

def fig_maps():
    o=[]; W=270; H=250
    for panel,(key,title) in enumerate([("pca","PCA (54.1% of variance)"),("tsne","t-SNE"),("umap","UMAP")]):
        pts=np.array(R["coords"][key]); labs=R["coords"]["labels"]; X0=70+panel*300; Y0=330
        lo,hi=pts.min(axis=0),pts.max(axis=0)
        X=lambda v: X0+(v-lo[0])/(hi[0]-lo[0])*W; Y=lambda v: Y0-(v-lo[1])/(hi[1]-lo[1])*H
        o.append(rect(X0-12,Y0-H-14,W+24,H+28,fill="none",stroke=RULE))
        for (a,b),l in zip(pts,labs): o.append(dot(X(a),Y(b),CLUSTER_COLORS[l],2.6))
        o.append(text(X0-12,Y0-H-24,title,13.5,INK,"bold",family=HEAD))
    for i,(cid,name) in enumerate(sorted(NAMES.items())):
        o.append(dot(90+i*230,385,CLUSTER_COLORS[cid],5)); o.append(text(100+i*230,389,name,12,INK))
    return svg(1000,410,"".join(o))

def fig_dendro():
    import io, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    Z=np.array(R["linkage"])
    fig,ax=plt.subplots(figsize=(9,3.6))
    dendrogram(Z,ax=ax,color_threshold=Z[-3,2],no_labels=True,above_threshold_color="#8a93a3")
    ax.axhline(Z[-3,2],color="#c0662b",linestyle="--",linewidth=1.5)
    ax.text(0.99,Z[-3,2],"  cut here for 4 clusters",color="#c0662b",fontsize=9,va="bottom",ha="right",transform=ax.get_yaxis_transform())
    ax.set_ylabel("Distance at which groups merged"); ax.set_xlabel("800 sampled accounts")
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    buf=io.StringIO(); fig.tight_layout(); fig.savefig(buf,format="svg"); plt.close(fig)
    return buf.getvalue()[buf.getvalue().index("<svg"):]

if __name__=="__main__":
    for name,fn in [("fig38-1-choosing-k.svg",fig_choose_k),("fig38-2-cluster-profiles.svg",fig_profiles),
                    ("fig38-4-pca-tsne-umap.svg",fig_maps),("fig38-3-dendrogram.svg",fig_dendro)]:
        open(name,"w").write(fn())
    print("ok")
