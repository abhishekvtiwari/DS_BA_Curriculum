# Diagrams for Chapter 63. Run: python3 make_figs63.py
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

def f1():  # reference architecture: sources -> ingestion -> warehouse -> semantic -> delivery -> monitoring
    o=[text(30,30,"A reference architecture for automation, one layer at a time",14.5,INK,"bold",family=HEAD)]
    layers=[("SOURCES","ERP, CRM, sensors,\nemail, spreadsheets",MUTED),
           ("INGESTION","Dagster (Ch 46)\nscheduled + event-driven",ACC),
           ("WAREHOUSE","Postgres + Delta\n(Ch 45, 49)",BLUE2),
           ("SEMANTIC LAYER","One definition per\nmetric (Ch 23)",GREEN),
           ("DELIVERY &\nACTIVATION","Flash, BI, CRM sync,\nPO-intake (Ch 16,20,51,58)",GOLD),
           ("MONITORING","Run logs, alerting,\nfailure paging (Ch 20)",RED)]
    W=155
    for i,(name,sub,c) in enumerate(layers):
        x=30+i*(W+12)
        o.append(box(x,64,W,150,name,c,sub.split("\n"),9.6))
        if i<5: o.append(arrow(x+W+2,139,x+W+10,139))
    o.append(rect(30,245,1000,60,fill="#fff",stroke=RULE,rx=6))
    o.append(text(46,268,"Every automation in this book is a specialization of this one shape.",11.2,INK,"bold"))
    o.append(text(46,288,"A single macro (Ch 19) compresses all six layers into one spreadsheet; a full pipeline (Ch 46) spans all six explicitly.",10.8,MUTED))
    return svg(1060,325,"".join(o))

def f2():  # value vs effort prioritization, real Riverstone automations plotted
    o=[text(30,30,"Prioritizing automation: value, effort, and risk, plotted for real",14.5,INK,"bold",family=HEAD)]
    gx,gy,gw,gh=90,60,760,300
    o.append(rect(gx,gy,gw,gh,fill="#fff",stroke=RULE,sw=1.4))
    for i in range(1,4): o.append(path(f"M{gx+gw*i/4},{gy} V{gy+gh}",stroke=LIGHT,sw=1))
    for i in range(1,4): o.append(path(f"M{gx},{gy+gh*i/4} H{gx+gw}",stroke=LIGHT,sw=1))
    o.append(text(gx+gw/2,gy+gh+52,"EFFORT TO BUILD \u2192",11.5,MUTED,"bold",anchor="middle"))
    o.append(f'<g transform="rotate(-90 {gx-40} {gy+gh/2})">{text(gx-40,gy+gh/2,"VALUE \u2192",11.5,MUTED,"bold",anchor="middle")}</g>')
    # points: (effort 0-1, value 0-1, radius=risk, label, color)
    pts=[("Daily Flash\n(325h/yr saved)",0.18,0.55,16,ACC),
        ("Branch macro\nconsolidation",0.15,0.30,10,GREEN),
        ("PO-intake,\nassisted mode",0.55,0.80,14,GOLD),
        ("PO-intake,\nstraight-through",0.50,0.15,26,RED),
        ("Dagster\ningestion pipeline",0.85,0.90,20,BLUE2),
        ("CRM reverse-ETL\nsync",0.45,0.45,12,PURPLE)]
    for name,ex,ey,r,c in pts:
        px,py = gx+gw*ex, gy+gh*(1-ey)
        o.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{c}" fill-opacity="0.85" stroke="#fff" stroke-width="1.5"/>')
        for i,l in enumerate(name.split("\n")):
            o.append(text(px,py+r+14+i*13,l,9.4,INK,"bold" if i==0 else None,anchor="middle"))
    o.append(text(gx+18,gy+18,"quick wins",10,MUTED,"italic"))
    o.append(text(gx+gw-90,gy+18,"big bets",10,MUTED,"italic"))
    o.append(text(gx+18,gy+gh-8,"question marks",10,MUTED,"italic"))
    o.append(text(30,430,"Bubble size is risk (bigger = riskier). Straight-through PO-intake looks cheap and valuable on effort and speed alone \u2014",11.2,MUTED))
    o.append(text(30,448,"only its risk bubble, drawn honestly, shows why assisted mode (smaller circle, still high value) was the actual choice.",11.2,MUTED))
    return svg(970,466,"".join(o))

def f3():  # shared services
    o=[text(30,30,"Shared services: build once, every automation uses them",14.5,INK,"bold",family=HEAD)]
    o.append(box(370,150,260,110,"Every automation\nin the platform",INK,[],11)) 
    items=[("Notification\nservice",90,60,ACC,"one place to send\nemail, Slack, SMS"),
           ("Credential\nvault",90,260,GREEN,"no password in\nany script (Ch 20)"),
           ("Run logs","740",60,GOLD,"every run, every\noutcome, centrally"),
           ("Alerting","740",260,RED,"pages a person on\nfailure (Ch 20)")]
    for i,(name,x,y,c,sub) in enumerate([("Notification\nservice",90,60,ACC,"one place to send\nemail, Slack, SMS"),
           ("Credential\nvault",90,260,GREEN,"no password in\nany script (Ch 20)"),
           ("Run logs",740,60,GOLD,"every run, every\noutcome, centrally"),
           ("Alerting",740,260,RED,"pages a person on\nfailure (Ch 20)")]):
        o.append(box(x,y,200,110,name,c,sub.split("\n"),10))
    o.append(arrow(290,115,430,175,ACC)); o.append(arrow(290,290,430,235,GREEN))
    o.append(arrow(738,115,632,175,GOLD)); o.append(arrow(738,290,632,235,RED))
    o.append(text(30,400,"Without these built once and shared, every one of Riverstone's 40+ automations reinvents its own logging, its own alerting,",11.2,MUTED))
    o.append(text(30,418,"and — worst of all — its own place to hide a password. Chapter 20's daily flash already assumes all four exist.",11.2,MUTED))
    return svg(1000,440,"".join(o))

def f4():  # shadow IT audit findings
    o=[text(30,30,"The first automation audit: what an inventory actually finds",14.5,INK,"bold",family=HEAD)]
    rows=[("Documented, owned, monitored","6","Ch 20 Flash, Ch 46 pipeline, Ch 51 sync, Ch 55 assistant, Ch 56/57 model services, Ch 58 PO-intake",GREEN),
         ("Working, but no owner on record","11","Branch-level macros, personal Apps Script projects, one Power Automate flow nobody remembers building",GOLD),
         ("Duplicated logic, disagreeing outputs","4","Two branches independently built near-identical consolidation macros with different bugs",ORANGE),
         ("Business-critical, single point of failure","1","MASTER_FINAL_v7_USE_THIS.xlsm (Ch 19) \u2014 still running, still unowned until the Ch 19 rewrite",RED),
         ("Actively broken, nobody had noticed","2","A stale Apps Script trigger silently stopped firing 5 months earlier",RED)]
    y=64
    o.append(rect(30,y,940,26,fill=INK,rx=4))
    for h,x in zip(["Category","Count","Examples"],[40,320,400]): o.append(text(x,y+18,h,10.5,"#fff","bold"))
    y+=34
    for cat,count,ex,c in rows:
        h=34
        o.append(rect(30,y,940,h,fill="#fff" if (int(y)//34)%2==0 else "#f7f9fb"))
        o.append(rect(30,y,5,h,fill=c))
        o.append(text(40,y+22,cat,9.8,INK,"bold"))
        o.append(text(320,y+22,count,10.5,c,"bold"))
        import textwrap
        o.append(text(400,y+22,ex[:95]+("..." if len(ex)>95 else ""),9.2,MUTED))
        y+=h
    o.append(text(30,y+28,"24 automations found, once someone actually looked. Only 6 had ever been through anything like this chapter's governance model.",11.2,MUTED))
    return svg(1000,y+48,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig63-1-reference-architecture.svg",f1),("fig63-2-prioritization.svg",f2),
                ("fig63-3-shared-services.svg",f3),("fig63-4-audit-findings.svg",f4)]:
        open(n,"w").write(f())
    print("ok")
