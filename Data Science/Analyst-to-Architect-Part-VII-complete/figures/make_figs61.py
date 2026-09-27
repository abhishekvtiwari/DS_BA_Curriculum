# Diagrams for Chapter 61. Run: python3 make_figs61.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.6):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8)]
    o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+26} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+18,title,10.8,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+44+i*15,l,size-1.2,INK,anchor="middle"))
    return "".join(o)

def f1():  # CAP theorem, pick 2 of 3, with a partition forcing the real choice
    o=[text(30,32,"CAP: when the network partitions, pick one",14.5,INK,"bold",family=HEAD)]
    cx,cy,R=280,240,140
    import math
    pts=[]
    for i,ang in enumerate([-90,30,150]):
        a=math.radians(ang); pts.append((cx+R*math.cos(a), cy+R*math.sin(a)))
    labels=[("Consistency","every reader sees\nthe latest write",ACC),("Availability","the system keeps\nresponding",GREEN),("Partition\ntolerance","the network can\ndrop messages",GOLD)]
    o.append(f'<polygon points="{pts[0][0]},{pts[0][1]} {pts[1][0]},{pts[1][1]} {pts[2][0]},{pts[2][1]}" fill="#f3f6fa" stroke="{RULE}" stroke-width="1.4"/>')
    for (px,py),(name,sub,c) in zip(pts,labels):
        lx = px + (60 if px>cx else (-60 if px<cx else 0))
        ly = py + (-30 if py<cy else 40)
        o.append(f'<circle cx="{px}" cy="{py}" r="8" fill="{c}"/>')
        o.append(text(lx,ly,name,11.5,c,"bold",anchor="middle"))
        for i,l in enumerate(sub.split("\n")): o.append(text(lx,ly+16+i*13,l,9.6,MUTED,anchor="middle"))
    o.append(text(cx,cy+4,"P is not\noptional\nat scale",10.5,INK,"bold",anchor="middle"))
    # right: the real Riverstone choice
    o.append(box(560,90,420,140,"Order writes (PO-intake -> ERP)",ACC,
                 ["Choose Consistency: if the ERP link is unreachable,","refuse the write and queue it, rather than risk","two different totals existing anywhere (Ch 51)."],10.4))
    o.append(box(560,260,420,140,"Dashboard reads (warehouse -> BI)",GREEN,
                 ["Choose Availability: if the warehouse is a few","minutes stale, show yesterday's number with a","timestamp rather than show nothing at all."],10.4))
    o.append(text(30,440,"CAP is not a menu you pick from once. Different parts of the same platform make different, deliberate choices.",11.3,MUTED))
    return svg(1010,460,"".join(o))

def f2():  # consistency spectrum with real Riverstone systems placed on it
    o=[text(30,32,"The consistency spectrum, with real Riverstone systems on it",14.5,INK,"bold",family=HEAD)]
    o.append(path("M60,140 H960",stroke=RULE,sw=2))
    o.append(text(60,120,"STRONG",11.5,ACC,"bold"))
    o.append(text(60,180,"every reader sees",9.8,MUTED)); o.append(text(60,194,"the latest write, always",9.8,MUTED))
    o.append(text(910,120,"EVENTUAL",11.5,GOLD,"bold",anchor="end")); o.append(text(910,182,"readers may see stale data;",9.8,MUTED,anchor="end"))
    o.append(text(910,196,"it converges given time",9.8,MUTED,anchor="end"))
    items=[("Postgres, single\ntransaction",70,ACC),("Delta Lake reads\n(snapshot isolation)",270,BLUE2),
           ("Warehouse vs\nERP (Ch 45 sync lag)",470,GREEN),("CRM reverse-ETL\nsync (Ch 51)",670,GOLD),
           ("Support assistant's\ndocument index",880,RED)]
    for name,x,c in items:
        o.append(f'<circle cx="{x}" cy="140" r="7" fill="{c}"/>')
        o.append(path(f"M{x},140 V190",stroke=c,sw=1.2,dash="3 2"))
        for i,l in enumerate(name.split("\n")): o.append(text(x,220+i*15,l,10,INK,anchor="middle",weight="bold" if i==0 else None))
    o.append(text(30,290,"Nothing here is a defect. Strong consistency costs latency and availability; eventual consistency is a deliberate trade",11.3,MUTED))
    o.append(text(30,308,"for scale and resilience. The judgment is choosing which one each system genuinely needs — not defaulting to either.",11.3,MUTED))
    return svg(990,330,"".join(o))

def f3():  # the reliability toolkit
    o=[text(30,30,"The reliability toolkit",14.5,INK,"bold",family=HEAD)]
    items=[("Sharding","Split data across machines\nby key, so no one machine\nholds it all",ACC,"Warehouse partitioned\nby reading_date (Ch 49)"),
           ("Replication","Keep copies for availability\nand durability, at a\nconsistency cost",GREEN,"Postgres read replicas\nfor BI queries"),
           ("Load balancing","Spread requests across\nmultiple instances of\nthe same service",GOLD,"The defect-model\nFastAPI service, scaled"),
           ("Caching","Serve from memory for\nspeed; the hard part is\nknowing when it's stale",PURPLE,"LLMOps prompt cache\n(Ch 57): 81% hit rate"),
           ("Message queues","Decouple producer from\nconsumer; absorb bursts\nwithout losing work",RED,"The mini-log pattern\n(Ch 50)")]
    for i,(name,desc,c,ex) in enumerate(items):
        x=30+i*192
        o.append(box(x,60,175,140,name,c,desc.split("\n"),10))
        o.append(rect(x,206,175,50,fill="#f3f6fa",rx=6))
        for j,l in enumerate(ex.split("\n")): o.append(text(x+87.5,224+j*15,l,9.4,MUTED,anchor="middle"))
    o.append(text(30,286,"None of these is exotic — Parts V and VI already use every one. This chapter names them as a reusable kit.",11.3,MUTED))
    return svg(990,304,"".join(o))

def f4():  # failure analysis of the platform: reusing ch60's containers, annotated
    o=[text(30,30,"Failure analysis: the Riverstone platform, container by container",14.5,INK,"bold",family=HEAD)]
    rows=[("Ingestion (Dagster)","Single scheduler instance","Pipelines pause; last-good data still readable","Retries + alerting; no auto-failover yet",GOLD),
          ("Warehouse (Postgres+Delta)","Single primary database","All reads/writes fail; total outage for the platform","None — this is platform's one true SPOF",RED),
          ("Semantic layer","None (stateless, recomputed)","Stale metrics until next run","Degrades gracefully: old numbers, clearly timestamped",GREEN),
          ("BI & Flash","Power BI service; SMTP","Dashboards unavailable; flash delayed, not lost","Retried on schedule; queued, not dropped",GREEN),
          ("Defect model service","Single FastAPI instance (today)","Line alerts stop; QC reverts to manual sampling","Documented fallback procedure exists",GOLD),
          ("Support assistant","Depends on document index","Assistant refuses instead of guessing (Ch 55)","By design: fails safe, not silently wrong",GREEN),
          ("PO-intake pipeline","CRM/ERP network link","New orders queue instead of writing blind","Chooses consistency; see this chapter's story",GREEN),
          ("Reverse-ETL sync","CRM API availability","CRM falls behind; reconciled once link returns","Eventual consistency, accepted on purpose",GREEN)]
    o.append(rect(30,55,940,26,fill=INK,rx=4))
    heads=["Container","Weakest link","What breaks","How it degrades"]
    xs=[40,300,490,720]
    for h,x in zip(heads,xs): o.append(text(x,73,h,10.5,"#fff","bold"))
    y=90
    for name,spof,breaks,degrade,c in rows:
        o.append(rect(30,y,940,34,fill="#fff" if (y//34)%2==0 else "#f7f9fb"))
        o.append(rect(30,y,5,34,fill=c))
        o.append(text(40,y+21,name,9.8,INK,"bold"))
        import textwrap
        o.append(text(300,y+21,spof,9.4,MUTED))
        o.append(text(490,y+21,breaks,9.2,MUTED))
        o.append(text(720,y+21,degrade,9.2,MUTED))
        y+=34
    o.append(text(30,y+26,"One true single point of failure: the warehouse. Everything else degrades; the warehouse going down is a full platform outage —",11.2,MUTED))
    o.append(text(30,y+44,"which is exactly the finding that earns it a redundancy investment other containers don't yet need.",11.2,MUTED))
    return svg(1000,y+62,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig61-1-cap-theorem.svg",f1),("fig61-2-consistency-spectrum.svg",f2),
                ("fig61-3-reliability-toolkit.svg",f3),("fig61-4-failure-analysis.svg",f4)]:
        open(n,"w").write(f())
    print("ok")
