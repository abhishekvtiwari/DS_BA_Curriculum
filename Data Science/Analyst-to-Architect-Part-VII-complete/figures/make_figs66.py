# Diagrams for Chapter 66. Run: python3 make_figs66.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.2):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=7), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=7)]
    o.append(f'<path d="M{x},{y+8} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+16.5,title,10,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+40+i*14,l,size-1.2,INK,anchor="middle"))
    return "".join(o)

def f1():  # 5-stage maturity model with Riverstone plotted across 5 dimensions
    o=[text(30,30,"A data maturity model, five stages, scored honestly across five dimensions",14.5,INK,"bold",family=HEAD)]
    stages=["1 Ad hoc","2 Reactive","3 Proactive","4 Managed","5 Optimized"]
    x0,y0,cw=280,66,138
    for i,s in enumerate(stages):
        o.append(text(x0+i*cw+cw/2,y0-12,s,9.8,MUTED,"bold",anchor="middle"))
        o.append(path(f"M{x0+i*cw},{y0} V{y0+280}",stroke=LIGHT,sw=1))
    o.append(path(f"M{x0+5*cw},{y0} V{y0+280}",stroke=LIGHT,sw=1))
    dims=[("Data quality\n& reliability","Ch 14, 47",3.6,ACC),
         ("Architecture\n& platform","Ch 60-62",3.2,BLUE2),
         ("Governance\n& security","Ch 63-64",3.4,GREEN),
         ("Cost\ndiscipline","Ch 65",2.6,GOLD),
         ("Data-driven\nculture","Ch 19, 24",2.2,PURPLE)]
    rh=52
    for j,(name,ref,score,c) in enumerate(dims):
        y=y0+j*rh+14
        o.append(text(30,y+8,name.split(chr(10))[0],10.4,INK,"bold"))
        o.append(text(30,y+22,name.split(chr(10))[1]+" ("+ref+")",9,MUTED))
        cx=x0+(score-1)*cw
        o.append(f'<circle cx="{cx}" cy="{y+4}" r="7" fill="{c}"/>')
        o.append(text(cx,y-10,f"{score:.1f}",9.6,c,"bold",anchor="middle"))
    o.append(text(30,y0+300,"Riverstone sits mostly in stage 3 (Proactive): real governance and cost discipline exist, but data-driven culture",11.2,MUTED))
    o.append(text(30,y0+318,"still lags — most decisions are still made by habit and hierarchy, not by routinely consulting the platform.",11.2,MUTED))
    return svg(1010,y0+340,"".join(o))

def f2():  # team structure evolution
    o=[text(30,30,"Team structure: from four people to a function, one hire at a time",14.5,INK,"bold",family=HEAD)]
    o.append(box(30,64,280,150,"2026: Chapter 60\nFour-person team",ACC,["Meera (lead) + 3","Centralized, serves","the whole company","","Every request queues","behind every other"],9.8))
    o.append(box(360,64,280,150,"Today: + 1 domain hire",GREEN,["Taloja plant's own","data analyst (Ch 62)","","First real domain","capacity outside the","central team"],9.8))
    o.append(box(690,64,280,150,"Proposed next hire",GOLD,["A data governance /","catalog owner (Ch 64)","","Not another generalist","— the specific gap","this chapter's audit found"],9.8))
    o.append(arrow(313,139,357,139)); o.append(arrow(643,139,687,139))
    o.append(text(30,244,"Each hire is justified by a specific, named gap this book already found — not headcount added because growth \"felt right.\"",11.3,MUTED))
    return svg(1000,264,"".join(o))

def f3():  # vendor selection: build vs buy scorecard
    o=[text(30,30,"Build vs. buy: a managed data catalog, scored honestly",14.5,INK,"bold",family=HEAD)]
    rows=[("Time to working solution","Buy: weeks","Build: months",GREEN),
         ("Fit to Riverstone's exact needs","Buy: good enough","Build: perfect, eventually",GOLD),
         ("Ongoing maintenance burden","Buy: vendor's problem","Build: the 4-person team's problem",RED),
         ("Cost at current scale","Buy: predictable subscription","Build: engineering time, unbounded",GOLD),
         ("Lock-in risk","Buy: real, but exit paths exist","Build: none, but nobody else knows it",GREEN)]
    y=64
    o.append(rect(30,y,940,26,fill=INK,rx=4))
    for h,x in zip(["Dimension","Buy","Build","Edge to"],[40,330,590,860]): o.append(text(x,y+18,h,10.2,"#fff","bold"))
    y+=34
    for dim,buy,build,c in rows:
        o.append(rect(30,y,940,38,fill="#fff" if (int(y)//38)%2==0 else "#f7f9fb"))
        o.append(rect(30,y,5,38,fill=c))
        o.append(text(40,y+24,dim,9.8,INK,"bold"))
        o.append(text(330,y+24,buy.split(": ")[1],9.4,MUTED))
        o.append(text(590,y+24,build.split(": ")[1],9.4,MUTED))
        o.append(text(900,y+24,"Buy" if c!=RED else "Buy",10,c,"bold",anchor="middle"))
        y+=38
    o.append(text(30,y+26,"At a 4-person team's scale, buy wins on every dimension that matters — build only wins if Riverstone's catalog needs",11.2,MUTED))
    o.append(text(30,y+44,"are genuinely unlike anyone else's, which a governance catalog's needs, honestly, are not.",11.2,MUTED))
    return svg(1000,y+64,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig66-1-maturity-model.svg",f1),("fig66-2-team-evolution.svg",f2),
                ("fig66-3-build-vs-buy.svg",f3)]:
        open(n,"w").write(f())
    print("ok")
