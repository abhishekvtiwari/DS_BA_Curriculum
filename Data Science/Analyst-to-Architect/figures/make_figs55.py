# Generates the SVG figures for Chapter 55. Run: python3 make_figs55.py
# Every number comes from the chapter's own measurements on companion/ch55 (seed 55).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_pipeline():
    o=[text(30,32,"The assistant, end to end: retrieve, ground, cite, or refuse",14,INK,"bold",family=HEAD)]
    boxes=[(30,"question","from a customer",RULE),
           (210,"retrieve","BM25 + vectors\ntop 3 chunks",ACC),
           (400,"confident?","BM25 >= 8 and\ncosine >= 0.60",ORANGE),
           (590,"ground","answer ONLY from\nthe numbered sources",PURPLE),
           (780,"answer + citation","with the chunk id\nstored for tracing",GREEN)]
    for x,title,detail,c in boxes:
        o.append(rect(x,70,170,78,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+85,96,title,12.5,c,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+85,118+i*16,line,11,MUTED,anchor="middle"))
        if x<780:
            o.append(path(f"M{x+170},109 H{x+208}",stroke=INK,sw=2)); o.append(path(f"M{x+200},103 L{x+210},109 L{x+200},115",stroke=INK,sw=2))
    o.append(path("M485,148 V200",stroke=RED,sw=2,dash="5,4")); o.append(path("M479,192 L485,202 L491,192",stroke=RED,sw=2))
    o.append(rect(330,202,320,50,fill="#fbeaea",stroke=RED,sw=1.6,rx=7))
    o.append(text(490,224,"no: refuse and hand to the support desk",12,RED,"bold",anchor="middle"))
    o.append(text(490,242,"7 of 10 unanswerable questions caught",11.5,INK,anchor="middle"))
    o.append(rect(700,202,320,50,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=7))
    o.append(text(860,224,"tools, when documents cannot answer",12,GREEN,"bold",anchor="middle"))
    o.append(text(860,242,"order status, price quote: read-only",11.5,INK,anchor="middle"))
    o.append(text(30,292,"Nothing retrieved is trusted: sources are numbered data, superseded documents are filtered at index time, and every answer",12,MUTED))
    o.append(text(30,312,"stores the chunk ids it used, so a wrong answer is traced to its document in a minute.",12,INK))
    return svg(1040,334,"".join(o))

def fig_retrieval():
    o=[text(30,32,"Chunking matters more than the search algorithm",14,INK,"bold",family=HEAD)]
    rows=[("fixed 400","bm25",0.78,0.868),("fixed 400","vector",0.80,0.861),("fixed 400","hybrid",0.85,0.918),
          ("sentences","bm25",0.91,0.949),("sentences","vector",0.87,0.932),("sentences","hybrid",0.87,0.936),
          ("sections","bm25",0.76,0.830),("sections","vector",0.85,0.912),("sections","hybrid",0.80,0.861)]
    y=78
    best=max(r[2] for r in rows)
    for chunking,method,r1,mrr in rows:
        c = GREEN if r1==best else (ACC if r1>=0.85 else MUTED)
        o.append(text(150,y+17,chunking,12,INK,"bold",anchor="end"))
        o.append(text(230,y+17,method,12,MUTED,anchor="end",family=MONO))
        o.append(rect(250,y,620*r1,26,fill=c,stroke=c,rx=4))
        o.append(text(260+620*r1,y+17,f"recall@1 {r1:.2f}   MRR {mrr:.3f}",11.5,INK))
        y+=32
    o.append(text(30,y+22,"55 questions whose correct source document was recorded in advance. Sentence chunks with plain keyword search win on this",12,MUTED))
    o.append(text(30,y+42,"corpus of short policies and product codes; hybrid search rescues the worst chunking. \u201cJust use embeddings\u201d is not what the numbers say.",12,INK))
    return svg(1040,y+64,"".join(o))

def fig_refusal():
    o=[text(30,32,"Refusal is a business trade, not a setting",14,INK,"bold",family=HEAD)]
    rows=[("BM25 < 6 or cosine < 0.50",3,3),("BM25 < 8 or cosine < 0.60",5,7),
          ("BM25 < 9 or cosine < 0.60",15,7),("BM25 < 10 or cosine < 0.60",17,8)]
    o.append(text(300,66,"answerable questions wrongly refused",12,RED,"bold",anchor="middle"))
    o.append(text(760,66,"unanswerable questions correctly refused",12,GREEN,"bold",anchor="middle"))
    y=86
    for label,wrong,right in rows:
        chosen = label.startswith("BM25 < 8")
        o.append(text(150,y+18,label,12,INK,"bold" if chosen else "normal",anchor="end",family=MONO))
        o.append(rect(170,y,260*wrong/55*3,26,fill=RED,stroke=RED,rx=4))
        o.append(text(180+260*wrong/55*3,y+18,f"{wrong} of 55",11.5,INK))
        o.append(rect(620,y,260*right/10,26,fill=GREEN,stroke=GREEN,rx=4))
        o.append(text(630+260*right/10,y+18,f"{right} of 10",11.5,INK))
        if chosen:
            o.append(text(1000,y+18,"chosen",12,ACC,"bold",anchor="end"))
        y+=40
    o.append(text(30,y+22,"Catching more of the questions the corpus cannot answer always means refusing more of the ones it can. Riverstone takes the",12,MUTED))
    o.append(text(30,y+42,"middle rule, because a wrong answer reaches a customer and a handover costs two minutes of someone's time.",12,INK))
    return svg(1040,y+64,"".join(o))

def fig_evaluation():
    o=[text(30,32,"Four numbers, each stricter than the last",14,INK,"bold",family=HEAD)]
    steps=[("answered rather than refused",50,55,GREEN,"the refusal threshold is not over-cautious"),
           ("cited the right document",38,55,ACC,"retrieval ranked the right document first"),
           ("answer contained the fact",18,55,ORANGE,"where a real model would change the result most"),
           ("correctly refused (unanswerable)",7,10,PURPLE,"the remaining three are guardrail work")]
    y=76
    for label,value,total,c,note in steps:
        o.append(text(280,y+20,label,12.5,INK,"bold",anchor="end"))
        o.append(rect(300,y,520,30,fill="#f6f9fc",stroke=RULE,rx=5))
        o.append(rect(300,y,520*value/total,30,fill=c,stroke=c,rx=5))
        o.append(text(312,y+20,f"{value} of {total}","12","#ffffff" if value/total>0.3 else INK,"bold")) if False else o.append(text(312,y+20,f"{value} of {total}",12,"#ffffff" if value/total>0.3 else INK,"bold"))
        o.append(text(840,y+20,note,11.5,MUTED))
        y+=46
    o.append(text(30,y+20,"Measured on the same 65 questions used for retrieval, so a change anywhere in the pipeline shows up in the ladder.",12,MUTED))
    o.append(text(30,y+40,"The gaps between the rungs say which component to work on next, which is the whole reason to measure four things instead of one.",12,INK))
    return svg(1040,y+62,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig55-1-assistant-pipeline.svg",fig_pipeline),("fig55-2-retrieval-table.svg",fig_retrieval),
                    ("fig55-3-refusal-tradeoff.svg",fig_refusal),("fig55-4-evaluation-ladder.svg",fig_evaluation)]:
        open(name,"w").write(fn())
    print("ok55")
