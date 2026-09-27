# Diagrams for Chapter 60. Run: python3 make_figs60.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.6,shape="rect"):
    o=[]
    if shape=="person":
        o.append(f'<circle cx="{x+w/2}" cy="{y+18}" r="14" fill="{c}"/>')
        o.append(rect(x+w/2-22,y+34,44,h-34,fill=c,rx=8))
    else:
        o.append(rect(x+3,y+4,w,h,fill=SOFT,rx=8)); o.append(rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+26} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+18 if shape!="person" else y+66,title,10.8,"#fff" if shape!="person" else INK,"bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+44+i*15 if shape!="person" else y+82+i*13,l,size-1.2,INK if shape!="person" else MUTED,anchor="middle"))
    return "".join(o)

def f1():  # the four C4 zoom levels
    o=[text(30,30,"The C4 model: the same system, four levels of zoom",14.5,INK,"bold",family=HEAD)]
    levels=[("Level 1: Context","The system as one box,\namong the people and other\nsystems around it",ACC),
            ("Level 2: Container","The system opened up:\nits major deployable pieces\n(app, database, pipeline)",GREEN),
            ("Level 3: Component","One container opened up:\nthe modules inside it and\nhow they call each other",GOLD),
            ("Level 4: Code","One component's actual\nclasses or functions —\nrarely drawn by hand",PURPLE)]
    for i,(t,sub,c) in enumerate(levels):
        x=30+i*235
        o.append(box(x,60,210,150,t,c,sub.split("\n"),10.6))
        if i<3: o.append(arrow(x+212,135,x+228,135))
    o.append(text(30,240,"Zoom in one level at a time. A context diagram with component-level detail crammed in helps nobody; a component",11.3,MUTED))
    o.append(text(30,258,"diagram of the whole company is unreadable. Pick the zoom level the conversation needs, and stop there.",11.3,MUTED))
    return svg(970,278,"".join(o))

def f2():  # C4 context diagram for the Riverstone platform
    o=[text(30,32,"Context diagram: the Riverstone Analytics & AI Platform, level 1",14.5,INK,"bold",family=HEAD)]
    o.append(box(430,220,260,120,"Riverstone Analytics\n& AI Platform",ACC,["Turns orders, sensors and","documents into reports,","alerts and automated actions"],10.6))
    people=[("Branch\nmanager",70,70,"person"),("Sales & ops\nstaff",70,380,"person"),("Customer",1000,70,"person"),("Data &\nanalytics team",1000,380,"person")]
    for name,x,y,shp in people: o.append(box(x-55,y,110,100,name,MUTED,[],10.2,shape=shp))
    systems=[("ERP\n(order records)",560,70,GOLD,170),("CRM (Zoho)",560,400,GOLD,170),
             ("Plant sensors\n(Taloja)",190,240,GOLD,150),("Email\n(orders, support)",930,240,GOLD,170)]
    for name,x,y,c,w in systems: o.append(box(x-w/2,y,w,70,name,c,[],9.8))
    o.append(arrow(120,120,420,225,MUTED)); o.append(text(150,180,"reads dashboards",9.6,MUTED))
    o.append(arrow(120,400,420,300,MUTED)); o.append(text(150,340,"reorder flags,\nintake results",9.4,MUTED))
    o.append(arrow(945,120,700,235,MUTED)); o.append(text(790,175,"answers, drafts",9.6,MUTED))
    o.append(arrow(700,300,945,395,MUTED,dash="4 3")); o.append(text(770,370,"views daily flash",9.6,MUTED))
    o.append(arrow(265,270,428,270,GOLD)); o.append(text(280,262,"sensor readings",9.4,GOLD))
    o.append(path("M560,105 L560,138",stroke=GOLD,sw=1.6)); o.append(arrow(560,108,560,140,GOLD))
    o.append(text(566,125,"orders",9.4,GOLD))
    o.append(path("M560,340 L560,398",stroke=GOLD,sw=1.6)); o.append(arrow(560,396,560,398,GOLD))
    o.append(text(566,375,"leads, segments",9.4,GOLD))
    o.append(arrow(845,270,692,270,GOLD)); o.append(text(700,262,"emails",9.4,GOLD))
    o.append(text(30,530,"One box in the middle; every arrow crosses its boundary. At this zoom level, nobody asks which orchestrator runs inside — that's level 2.",11.3,MUTED))
    return svg(1090,552,"".join(o))

def f3():  # container diagram
    o=[text(30,30,"Container diagram: opening the platform box, level 2",14.5,INK,"bold",family=HEAD)]
    conts=[("Ingestion\n(Dagster)",40,70,"Pulls orders, sensors,\nCRM, dispatch files",ACC),
           ("Warehouse\n(Postgres + Delta)",230,70,"Raw, staging, modelled\ntables; sensor archive",BLUE2),
           ("Semantic layer\n(dbt-style models)",420,70,"One definition of\nrevenue, active customer",GREEN),
           ("BI & Flash\n(Power BI, email)",610,70,"Dashboards, the daily\nsales flash",GOLD),
           ("Defect model\nservice (FastAPI)",40,220,"Scores images from\nthe Taloja line",PURPLE),
           ("Support assistant\n(RAG)",230,220,"Answers from policy\nand spec documents",PURPLE),
           ("PO intake\npipeline",420,220,"Reads order emails,\nwrites to the ERP",PURPLE),
           ("Reverse-ETL\nsync",610,220,"Writes scores and\nflags back to the CRM",ACC)]
    for name,x,y,sub,c in conts:
        o.append(box(x,y,170,110,name,c,sub.split("\n"),10))
    o.append(arrow(125,180,125,218)); o.append(arrow(315,180,315,218))
    o.append(arrow(400,120,418,120)); o.append(arrow(590,120,608,120))
    o.append(arrow(505,180,505,218))
    o.append(rect(30,360,760,60,fill="#fff",stroke=RULE,rx=6))
    o.append(text(46,384,"Shared services (used by every container above): credential vault, run logs, alerting, monitoring",11.5,INK,"bold"))
    o.append(text(46,404,"— drawn once here, not repeated eight times on the diagram.",10.6,MUTED))
    o.append(text(30,445,"Each box is something you could deploy and scale on its own. This is the level where you decide what talks to what, and how.",11.3,MUTED))
    return svg(820,462,"".join(o))

def f4():  # ADR card example
    o=[text(30,30,"An architecture decision record, filled in",14.5,INK,"bold",family=HEAD)]
    ADR_H=520
    o.append(rect(30,58,900,ADR_H,fill="#fff",stroke=RULE,sw=1.4,rx=8))
    rows=[("ADR-014","Table format for the sensor archive",ACC),
          ("Status","Accepted, 18 Sep 2026",MUTED),
          ("Context","The Taloja sensor archive is 19.8M+ rows and growing daily. A six-week correction to machine M-07's readings failed mid-run under plain Parquet files, leaving the archive in a partly-corrected, unrecoverable state for two days.",INK),
          ("Decision","Store the sensor archive as a Delta Lake table (delta-rs), not plain Parquet files.",INK),
          ("Alternatives considered","(1) Plain Parquet with manual versioning by folder name — rejected: exactly what failed. (2) Apache Iceberg — comparable guarantees, rejected only because the team has no existing Java/Spark operational experience. (3) Keep it in Postgres — rejected: cost and query performance at this row count.",INK),
          ("Consequences","Atomic overwrites and time travel (Ch49); one more format for the team to operate; the `deltalake` Python package must be pinned and tested on version upgrades.",INK),
          ("Owner","Data platform team. Revisit if Iceberg adoption becomes a company standard.",MUTED)]
    y=80
    for label,val,c in rows:
        o.append(text(46,y,label,10.8,c,"bold"))
        # wrap val roughly
        import textwrap
        wrapped=textwrap.wrap(val,width=98)
        for i,ln in enumerate(wrapped):
            o.append(text(220,y+i*16,ln,10.4,INK))
        y+=max(22,len(wrapped)*16+8)
    return svg(960,y+20,"".join(o))

def f5():  # trade-off / NFR turning vague into numbers
    o=[text(30,30,"Turning a vague requirement into a number",14.5,INK,"bold",family=HEAD)]
    pairs=[("\"Make it fast\"","The daily flash email must be sent within 10 minutes of the 06:00 ERP load finishing, p95",ACC),
           ("\"Make it reliable\"","99.5% of scheduled pipeline runs succeed without manual intervention, measured monthly",GREEN),
           ("\"Make it secure\"","No analyst credential can read another branch's customer data; access reviewed quarterly",RED),
           ("\"Make it scale\"","The warehouse must handle 5x current order volume with no schema change",GOLD),
           ("\"Keep it cheap\"","Platform cost stays under ₹0.50 per 1,000 order lines processed, reviewed monthly",PURPLE)]
    for i,(vague,precise,c) in enumerate(pairs):
        y=64+i*72
        o.append(rect(30,y,260,56,fill="#fff",stroke=RULE,rx=6)); o.append(text(46,y+33,vague,12,MUTED,"italic"))
        o.append(arrow(295,y+28,335,y+28,c,1.8))
        o.append(rect(345,y,600,56,fill="#fff",stroke=c,sw=1.5,rx=6)); o.append(rect(345,y,7,56,fill=c))
        import textwrap
        wrapped=textwrap.wrap(precise,width=68)
        for j,ln in enumerate(wrapped): o.append(text(364,y+22+j*16,ln,10.6,INK))
    return svg(970,64+5*72+10,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig60-1-c4-levels.svg",f1),("fig60-2-context-diagram.svg",f2),
                ("fig60-3-container-diagram.svg",f3),("fig60-4-adr-example.svg",f4),
                ("fig60-5-nfr-precision.svg",f5)]:
        open(n,"w").write(f())
    print("ok")
