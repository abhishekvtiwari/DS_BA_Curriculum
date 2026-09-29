# Generates the SVG figures for Chapter 55. Run: python3 make_figs55.py
# Every number shown was printed by the chapter's own code on companion/ch55: the retrieval table
# (section 55.5), the refusal sweep (section 55.6), and the end-to-end ladder (section 55.9).
# Canvas 720 px wide, printed at 493.2 pt: 10.5 px text prints at 7.2 pt, so no text is smaller than 10.5.
# Meaning never rests on colour alone: every bar carries its number, and the chosen or best row is also
# marked in words.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; BLUE="#0f5c8c"
W=720

def arrow_down(x,y1,y2,c=INK,dash=None):
    return path(f"M{x},{y1} V{y2-2}",stroke=c,sw=2,dash=dash)+path(f"M{x-5},{y2-9} L{x},{y2} L{x+5},{y2-9}",stroke=c,sw=2)

def arrow_right(x1,y,x2,c=INK):
    return path(f"M{x1},{y} H{x2-2}",stroke=c,sw=2)+path(f"M{x2-8},{y-5} L{x2},{y} L{x2-8},{y+5}",stroke=c,sw=2)

def fig_pipeline():
    o=[text(18,26,"The assistant, end to end: retrieve, ground, cite, or refuse",14,INK,"bold",family=HEAD)]
    boxes=[("question","from a customer","",INK),
           ("retrieve","BM25 + vectors","top 3 chunks",ACC),
           ("confident?","BM25 ≥ 8 and","cosine ≥ 0.60",ORANGE),
           ("ground","answer ONLY from","numbered sources",PURPLE),
           ("cited answer","chunk ids stored","for tracing",GREEN)]
    bw,gap,x0,y0,bh=124,16,18,48,74
    centres=[]
    for k,(title,d1,d2,c) in enumerate(boxes):
        x=x0+k*(bw+gap); centres.append(x+bw/2)
        o.append(rect(x,y0,bw,bh,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+bw/2,y0+24,title,12,c,"bold",anchor="middle"))
        o.append(text(x+bw/2,y0+44,d1,10.5,INK,anchor="middle"))
        if d2: o.append(text(x+bw/2,y0+60,d2,10.5,INK,anchor="middle"))
        if k<4: o.append(arrow_right(x+bw,y0+bh/2,x+bw+gap))
    # tools path: from the question, for questions no document can answer
    y2=164
    o.append(arrow_down(centres[0],y0+bh,y2,GREEN))
    o.append(text(centres[0]+8,y0+bh+24,"a live lookup",10.5,GREEN,"bold"))
    o.append(rect(x0,y2,300,54,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=7))
    o.append(text(x0+150,y2+22,"tools, when documents can't answer",11.5,GREEN,"bold",anchor="middle"))
    o.append(text(x0+150,y2+41,"order status, price quote: read-only",10.5,INK,anchor="middle"))
    # refusal path: from the confidence check
    o.append(arrow_down(centres[2],y0+bh,y2,RED,dash="5,4"))
    o.append(text(centres[2]+8,y0+bh+24,"no",10.5,RED,"bold"))
    o.append(rect(340,y2,362,54,fill="#fbeaea",stroke=RED,sw=1.6,rx=7))
    o.append(text(521,y2+22,"refuse, and hand to the support desk",11.5,RED,"bold",anchor="middle"))
    o.append(text(521,y2+41,"7 of 10 unanswerable questions caught",10.5,INK,anchor="middle"))
    o.append(text(x0,y2+80,"Nothing retrieved is trusted: sources are numbered data, and every answer stores the chunk ids",10.5,INK))
    o.append(text(x0,y2+97,"it used. Superseded documents are filtered out at index time (section 55.10).",10.5,INK))
    return svg(W,y2+110,"".join(o))

RETRIEVAL=[("fixed 400",[("bm25",0.78,0.868),("vector",0.80,0.861),("hybrid",0.85,0.918)]),
           ("sentences",[("bm25",0.91,0.949),("vector",0.87,0.932),("hybrid",0.87,0.936)]),
           ("sections",[("bm25",0.89,0.938),("vector",0.85,0.912),("hybrid",0.85,0.909)]),
           ("sent+title",[("bm25",0.95,0.965),("vector",0.89,0.938),("hybrid",0.91,0.952)])]

def fig_retrieval():
    o=[text(18,26,"recall@1 for four chunking strategies and three searches",14,INK,"bold",family=HEAD),
       text(18,45,"55 answerable questions; bar length is recall@1 on a 0 to 1 scale",10.5,MUTED)]
    x0=190; scale=380
    best=max(r1 for _,rows in RETRIEVAL for _,r1,_ in rows)
    y=60
    for chunking,rows in RETRIEVAL:
        o.append(text(18,y+15,chunking,11.5,INK,"bold"))
        for method,r1,mrr in rows:
            is_best = r1==best
            c = GREEN if is_best else ACC
            o.append(text(x0-10,y+15,method,10.5,MUTED,anchor="end",family=MONO))
            o.append(rect(x0,y+2,scale*r1,18,fill=c,stroke=c,rx=3))
            label=f"{r1:.2f}   MRR {mrr:.3f}" + ("   highest" if is_best else "")
            o.append(text(x0+scale*r1+8,y+15,label,10.5,INK,"bold" if is_best else "normal"))
            y+=22
        y+=8
    for v in (0,0.5,1.0):
        o.append(path(f"M{x0+scale*v},{y-4} V{y+2}",stroke=MUTED,sw=1))
        o.append(text(x0+scale*v,y+16,f"{v:g}",10.5,MUTED,anchor="middle"))
    o.append(text(18,y+40,"With BM25, sentence chunks beat fixed ones by 13 points, and a title on every chunk adds 4 more.",10.5,INK))
    o.append(text(18,y+57,"The vector rows use this chapter's stand-in (TF-IDF plus SVD); a neural embedder would likely lift them.",10.5,INK))
    return svg(W,y+70,"".join(o))

def fig_refusal():
    o=[text(18,26,"Refusal is a business trade, not a setting",14,INK,"bold",family=HEAD)]
    rows=[("BM25 < 6, cosine < 0.50",3,3),("BM25 < 8, cosine < 0.60",5,7),
          ("BM25 < 9, cosine < 0.60",15,7),("BM25 < 10, cosine < 0.60",17,8)]
    ax, aw, amax = 196, 210, 20       # left panel: answerable questions wrongly refused, count 0-20
    bx, bw, bmax = 470, 150, 10       # right panel: unanswerable questions correctly refused, count 0-10
    o.append(text(ax,50,"answerable, wrongly refused",11.5,ORANGE,"bold"))
    o.append(text(ax,66,"(of 55; fewer is better)",10.5,MUTED))
    o.append(text(bx,50,"unanswerable, correctly refused",11.5,BLUE,"bold"))
    o.append(text(bx,66,"(of 10; more is better)",10.5,MUTED))
    y=78
    for label,wrong,right in rows:
        chosen = label.startswith("BM25 < 8")
        if chosen: o.append(rect(10,y-3,700,28,fill="#f6f9fc",stroke=RULE,rx=4))
        o.append(text(ax-10,y+15,label,10.5,INK,"bold" if chosen else "normal",anchor="end",family=MONO))
        o.append(rect(ax,y+2,aw*wrong/amax,18,fill=ORANGE,stroke=ORANGE,rx=3))
        o.append(text(ax+aw*wrong/amax+6,y+15,f"{wrong}",10.5,INK,"bold"))
        o.append(rect(bx,y+2,bw*right/bmax,18,fill=BLUE,stroke=BLUE,rx=3))
        o.append(text(bx+bw*right/bmax+6,y+15,f"{right}",10.5,INK,"bold"))
        if chosen: o.append(text(704,y+15,"chosen",10.5,INK,"bold",anchor="end"))
        y+=32
    for v in (0,10,20):
        o.append(path(f"M{ax+aw*v/amax},{y-4} V{y+2}",stroke=MUTED,sw=1))
        o.append(text(ax+aw*v/amax,y+16,str(v),10.5,MUTED,anchor="middle"))
    for v in (0,5,10):
        o.append(path(f"M{bx+bw*v/bmax},{y-4} V{y+2}",stroke=MUTED,sw=1))
        o.append(text(bx+bw*v/bmax,y+16,str(v),10.5,MUTED,anchor="middle"))
    o.append(text(18,y+40,"Catching more of the questions the corpus cannot answer always means refusing more of the ones",10.5,INK))
    o.append(text(18,y+57,"it can. Riverstone starts with the middle rule; section 55.6 prices each rule in rupees.",10.5,INK))
    return svg(W,y+70,"".join(o))

def fig_evaluation():
    o=[text(18,26,"Four numbers, each stricter than the last",14,INK,"bold",family=HEAD),
       text(18,45,"55 answerable questions; bar length out of 55",10.5,MUTED)]
    steps=[("answered, not refused",50,"50 of 55",GREEN),
           ("cited the right document",38,"38 of the 50 answered",ACC),
           ("answer contained the fact",12,"12 of the 38 cited correctly",ORANGE)]
    x0=200; scale=300
    y=58
    for label,value,note,c in steps:
        o.append(text(x0-10,y+17,label,11,INK,"bold",anchor="end"))
        o.append(rect(x0,y,scale,26,fill="#f6f9fc",stroke=RULE,rx=4))
        o.append(rect(x0,y,scale*value/55,26,fill=c,stroke=c,rx=4))
        o.append(text(x0+scale+10,y+17,note,10.5,INK))
        y+=36
    y+=6
    o.append(path(f"M18,{y} H702",stroke=RULE,sw=1))
    o.append(text(18,y+20,"10 unanswerable questions; bar length out of 10 (a different scale)",10.5,MUTED))
    y+=32
    o.append(text(x0-10,y+17,"correctly refused",11,INK,"bold",anchor="end"))
    o.append(rect(x0,y,scale,26,fill="#f6f9fc",stroke=RULE,rx=4))
    o.append(rect(x0,y,scale*7/10,26,fill=PURPLE,stroke=PURPLE,rx=4))
    o.append(text(x0+scale+10,y+17,"7 of 10",10.5,INK))
    y+=36
    o.append(text(18,y+20,"The gaps between the rungs say which component to work on next: the stand-in generator loses",10.5,INK))
    o.append(text(18,y+37,"most between the right document and the right fact, which is where a real model helps most.",10.5,INK))
    return svg(W,y+50,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig55-1-assistant-pipeline.svg",fig_pipeline),("fig55-2-retrieval-table.svg",fig_retrieval),
                    ("fig55-3-refusal-tradeoff.svg",fig_refusal),("fig55-4-evaluation-ladder.svg",fig_evaluation)]:
        open(name,"w").write(fn())
    print("ok55")
