# Generates the SVG figures for Chapter 41. Run from figures/ after checks/ch41_check.py has written ch41_results.json.
import json, pathlib
import numpy as np
from make_figs import *
GREEN="#2f7d6d"; RED="#b23b3b"; ORANGE="#c0662b"; PURPLE="#7a4fa0"; PALE="#eef1f5"
R = json.loads((pathlib.Path(__file__).resolve().parent.parent / "checks" / "ch41_results.json").read_text())

def fig_topics():
    o=[]; topics=R["lda_topics"]; labels=R["topics_order"]
    X0=60; colw=170
    for i,words in enumerate(topics):
        x=X0+i*colw
        o.append(text(x,40,f"LDA topic {i}",13.5,ACC,"bold",family=HEAD))
        for j,w in enumerate(words): o.append(text(x,68+j*22,w,12.5,INK))
    cross=R["cross_lda"]; Y0=260
    o.append(text(X0,Y0-14,"Discovered LDA topic vs. real category (row share, %)",13,INK,"bold",family=HEAD))
    cw=90; rh=30
    for j in range(5): o.append(text(X0+120+j*cw+cw/2,Y0+14,f"topic {j}",11.5,MUTED,anchor="middle"))
    for i,lab in enumerate(labels):
        y=Y0+34+i*rh
        o.append(text(X0+110,y+18,lab,12,INK,anchor="end"))
        row=cross[str(i)] if str(i) in cross else cross.get(i,{})
        total=sum(float(cross[str(j)].get(lab,0) if str(j) in cross else cross[j].get(lab,0)) for j in range(5))
        for j in range(5):
            key=str(j) if str(j) in cross else j
            v=float(cross[key].get(lab,0)); share=v/total if total else 0
            x=X0+120+j*cw
            o.append(rect(x,y,cw-8,22,fill=ACC,rx=3,extra=f'opacity="{0.15+0.75*share:.2f}"'))
            if share>0.05: o.append(text(x+(cw-8)/2,y+16,f"{share:.0%}",11,INK,anchor="middle"))
    return svg(920,Y0+34+5*rh+20,"".join(o))

def fig_embed():
    o=[]; X0=460; Y0=460; W=380; H=380
    pts=np.array(R["coords"]); words=R["vocab_words"]
    lo,hi=pts.min(0)-1,pts.max(0)+1
    X=lambda v: X0+(v-lo[0])/(hi[0]-lo[0])*W; Y=lambda v: Y0-(v-lo[1])/(hi[1]-lo[1])*H
    o.append(rect(X0-14,Y0-H-14,W+28,H+28,fill="none",stroke=RULE))
    groups={"broken":GREEN,"crack":GREEN,"damaged":GREEN,"invoice":ORANGE,"gst":ORANGE,"refund":ORANGE,
            "delivery":ACC,"dispatch":ACC,"tracking":ACC}
    for w,(x,y) in zip(words,pts):
        c=groups.get(w,MUTED)
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" fill="{c}"/>')
        o.append(text(X(x)+9,Y(y)+4,w,12.5,INK,"bold" if w in groups else "normal"))
    o.append(text(X0-14,Y0-H-44,"Fifteen ticket words by their word2vec PCA position",13.5,INK,"bold",family=HEAD))
    return svg(900,500,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig41-1-topic-models.svg",fig_topics),("fig41-2-word-embeddings.svg",fig_embed)]:
        open(name,"w").write(fn())
    print("ok")
