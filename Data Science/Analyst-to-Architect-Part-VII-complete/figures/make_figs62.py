# Diagrams for Chapter 62. Run: python3 make_figs62.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.4):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=7), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=7)]
    o.append(f'<path d="M{x},{y+8} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+16.5,title,10.2,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+40+i*14,l,size-1.2,INK,anchor="middle"))
    return "".join(o)

def f1():  # Lambda vs Kappa vs what Riverstone actually does, same scenario
    o=[text(30,30,"One scenario, three ways: sensor readings to a line alert and a warehouse",14.5,INK,"bold",family=HEAD)]
    # Lambda
    o.append(text(40,66,"LAMBDA",12.5,ACC,"bold"))
    o.append(box(30,78,220,50,"Sensors",MUTED,[]))
    o.append(box(30,150,220,55,"Batch layer\n(nightly Dagster run)",ACC,["writes to warehouse"],9.6))
    o.append(box(30,225,220,55,"Speed layer\n(separate stream job)",GOLD,["writes to a fast store"],9.6))
    o.append(box(30,300,220,50,"Merge view\n(reconciles both)",GREEN,[]))
    o.append(arrow(140,128,140,148)); o.append(arrow(140,128,80,148)); o.append(path("M80,148 L80,130",stroke=ACC,sw=0)); 
    o.append(arrow(140,205,140,223)); o.append(arrow(140,280,140,298))
    o.append(text(30,368,"Two code paths for the",10,MUTED)); o.append(text(30,382,"same logic — accurate,",10,MUTED)); o.append(text(30,396,"but doubles the work.",10,MUTED))
    # Kappa
    o.append(text(300,66,"KAPPA",12.5,GREEN,"bold"))
    o.append(box(290,78,220,50,"Sensors",MUTED,[]))
    o.append(box(290,150,220,55,"One stream\n(everything is a stream)",GREEN,["replay to reprocess history"],9.6))
    o.append(box(290,225,220,55,"Stream consumer:\nline alert",GOLD,[],9.6))
    o.append(box(290,300,220,50,"Stream consumer:\nwarehouse table",ACC,[],9.6))
    o.append(arrow(400,128,400,148))
    o.append(arrow(400,205,340,223)); o.append(arrow(400,205,460,223))
    o.append(path("M340,246 L340,298",stroke=GOLD,sw=0))
    o.append(arrow(340,246,340,298,GOLD)); o.append(arrow(460,246,460,298,ACC))
    o.append(text(290,368,"One path, simpler —",10,MUTED)); o.append(text(290,382,"needs real streaming",10,MUTED)); o.append(text(290,396,"infrastructure to run.",10,MUTED))
    # What Riverstone does
    o.append(text(560,66,"WHAT RIVERSTONE ACTUALLY DOES",12.5,PURPLE,"bold"))
    o.append(box(550,78,220,50,"Sensors",MUTED,[]))
    o.append(box(550,150,220,55,"Edge inference\n(FastAPI, per image)",PURPLE,["line alert, <50ms"],9.6))
    o.append(box(550,225,220,55,"Async log\n(same event, logged)",GOLD,[],9.6))
    o.append(box(550,300,220,50,"Batch ingestion\n(Dagster, scheduled)",ACC,[]))
    o.append(arrow(660,128,660,148))
    o.append(arrow(660,205,660,223))
    o.append(arrow(660,280,660,298))
    o.append(text(550,368,"Neither textbook pattern:",10,MUTED)); o.append(text(550,382,"real-time where speed",10,MUTED)); o.append(text(550,396,"matters, batch elsewhere.",10,MUTED))
    return svg(810,414,"".join(o))

def f2():  # medallion layers mapped to Riverstone naming
    o=[text(30,30,"Medallion: bronze, silver, gold — a name for what Riverstone already does",14.5,INK,"bold",family=HEAD)]
    layers=[("BRONZE","Raw","Exactly as the source sent it, kept for replay and audit",ORANGE,"Ch 45's `raw` schema"),
           ("SILVER","Staging","Cleaned, typed, deduplicated, conformed to one shape",MUTED,"Ch 45's `staging` schema, Ch 47's tests"),
           ("GOLD","Modelled / Marts","Business-ready: the semantic layer's tables",GOLD,"Ch 23's semantic layer, dbt-style models")]
    for i,(tier,name,desc,c,note) in enumerate(layers):
        x=30+i*330
        o.append(rect(x,60,300,140,fill="#fff",stroke=c,sw=1.8,rx=8)); o.append(rect(x,60,300,34,fill=c))
        o.append(text(x+150,83,f"{tier} — {name}",12,"#fff","bold",anchor="middle"))
        import textwrap
        for j,l in enumerate(textwrap.wrap(desc,width=38)): o.append(text(x+16,116+j*16,l,10.4,INK))
        o.append(rect(x+14,168,272,24,fill=SOFT,rx=4)); o.append(text(x+150,184,note,9.6,MUTED,anchor="middle"))
        if i<2: o.append(arrow(x+302,130,x+328,130))
    o.append(text(30,235,"Medallion isn't a new thing to build — it's a name for the raw -> staging -> modelled layering this book has used since Chapter 45,",11.3,MUTED))
    o.append(text(30,253,"now recognized as an industry-standard convention rather than one team's private habit.",11.3,MUTED))
    return svg(970,272,"".join(o))

def f3():  # centralized vs data mesh vs data fabric
    o=[text(30,30,"Organizational patterns: who owns the data",14.5,INK,"bold",family=HEAD)]
    o.append(box(30,60,290,230,"Centralized",ACC,
                 ["One team owns all data:","ingestion, models, quality,","delivery — for everyone.","","Simple to govern.","Bottlenecks as the","company grows past","what one team can serve."],10.2))
    o.append(box(345,60,290,230,"Data mesh",GREEN,
                 ["Each domain team owns","its own data as a product,","on a shared self-serve","platform, under federated","governance.","","Scales organizationally.","Needs real platform and","cultural maturity to work."],10.2))
    o.append(box(660,60,290,230,"Data fabric",PURPLE,
                 ["An intelligent metadata","layer unifies distributed","data without necessarily","moving or re-owning it.","","Technology-led rather","than organization-led;","often paired with either","of the other two."],10.2))
    o.append(text(30,318,"Riverstone today: firmly centralized — a four-person data platform team (Chapter 60) serves the whole company. That's not a", 11.3,MUTED))
    o.append(text(30,336,"failure; it's the right fit for this size. Section 62.5 checks, honestly, whether that should change yet.",11.3,MUTED))
    return svg(970,356,"".join(o))

def f4():  # data mesh maturity scorecard for Riverstone
    o=[text(30,30,"Is Riverstone ready for a data mesh? A maturity check, scored honestly",14.5,INK,"bold",family=HEAD)]
    rows=[("Multiple domain teams that could each own data",1,5,"One data team; sales/ops/plant don't yet have their own builders"),
          ("A self-serve platform domains could use independently",2,5,"Dagster + warehouse exist, but no domain has used them without the platform team"),
          ("Federated governance (agreed standards, locally applied)",2,5,"Data contracts (Ch 47) exist for one pipeline, not yet a company standard"),
          ("A data-product mindset (data as something with an owner and a SLA)",3,5,"Chapter 60's containers each have an owner and NFRs — a real start"),
          ("Organizational appetite for the cultural change mesh requires",1,5,"Not raised; no domain team has asked to own its own data yet")]
    y=70
    for label,score,maxs,note in rows:
        o.append(text(30,y+14,label,10.6,INK,"bold"))
        bw=400; fw=bw*score/maxs
        o.append(rect(620,y,bw,16,fill=LIGHT,rx=8)); o.append(rect(620,y,fw,16,fill=GOLD if score<=2 else (ACC if score==3 else GREEN),rx=8))
        o.append(text(620+bw+10,y+13,f"{score}/{maxs}",10.5,INK,"bold"))
        import textwrap
        for j,l in enumerate(textwrap.wrap(note,width=95)): o.append(text(30,y+30+j*14,l,9.6,MUTED))
        y+=30+14*max(1,len(textwrap.wrap(note,width=95)))+14
    o.append(rect(30,y,990-60,50,fill="#fff",stroke=RED,sw=1.6,rx=6)); o.append(rect(30,y,7,50,fill=RED))
    o.append(text(50,y+22,"Verdict: not ready, and that's fine. A data mesh imposed here would add organizational",11,INK,"bold"))
    o.append(text(50,y+40,"complexity to solve a bottleneck that doesn't exist yet. Revisit when a second domain team asks to own its own data.",10.6,MUTED))
    return svg(990,y+70,"".join(o))


def f5():  # data contracts + semantic layer as decentralization glue
    o=[text(30,30,"Without a contract, decentralization is just chaos with more owners",14.5,INK,"bold",family=HEAD)]
    o.append(text(60,64,"NO CONTRACT",12,RED,"bold"))
    o.append(box(30,76,280,150,"Sales domain",RED,["publishes \"active_customer\"","as: ordered in last 30 days"],9.8))
    o.append(box(330,76,280,150,"Finance domain",RED,["publishes \"active_customer\"","as: has a non-zero balance"],9.8))
    o.append(box(30,240,580,60,"Two \"single sources of truth\" that disagree — and nobody outside either team knows it",RED,[],10.2))
    o.append(text(680,64,"WITH A CONTRACT",12,GREEN,"bold"))
    o.append(box(660,76,280,80,"Sales domain",GREEN,["publishes to the agreed","\"active_customer\" contract"],9.8))
    o.append(box(660,166,280,80,"Finance domain",GREEN,["reads the same contract,","doesn't redefine it"],9.8))
    o.append(box(660,256,280,60,"One shared definition\n(Ch 23's semantic layer)",ACC,[],9.8))
    o.append(arrow(800,156,800,164,GREEN)); o.append(arrow(800,246,800,254,ACC))
    o.append(text(30,330,"A data contract (Ch 47) states the shape and meaning of a dataset in writing, and a semantic layer (Ch 23) is where the",11.3,MUTED))
    o.append(text(30,348,"agreed, shared definitions actually live. Decentralized ownership without both isn't a mesh \u2014 it's just several teams guessing.",11.3,MUTED))
    return svg(970,368,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig62-1-lambda-kappa-riverstone.svg",f1),("fig62-2-medallion.svg",f2),
                ("fig62-3-org-patterns.svg",f3),("fig62-4-mesh-maturity.svg",f4),
                ("fig62-5-contracts-glue.svg",f5)]:
        open(n,"w").write(f())
    print("ok")
