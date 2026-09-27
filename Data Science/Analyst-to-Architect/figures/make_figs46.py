# Generates the SVG figures for Chapter 46. Run: python3 make_figs46.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def node(x,y,w,h,title,sub,c,fill="#fff"):
    return (rect(x+3,y+4,w,h,fill="#e9eef4",rx=8)+rect(x,y,w,h,fill=fill,stroke=c,sw=1.6,rx=8)
            +rect(x,y,7,h,fill=c,rx=3)+text(x+18,y+26,title,13.5,INK,"bold")+text(x+18,y+46,sub,11.5,MUTED))

def fig_graph():
    o=[]
    o.append(rect(30,20,980,40,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(46,46,"Schedule: 30 6 * * *  ·  Asia/Kolkata  ·  one daily partition per run (e.g. 2026-01-05)",13,INK,"bold"))
    ys=[90,170,250,330]; names=[("raw_orders","hash + upsert from ERP"),("raw_order_items","hash + upsert from ERP"),("raw_dispatch","file, column check"),("raw_crm_leads","API, retry policy")]
    for (n,s),y in zip(names,ys):
        o.append(node(40,y,230,60,n,s,ACC))
    o.append(node(390,130,230,60,"daily_flash","partition overwrite",GREEN))
    o.append(arrow(274,120,386,152,c=INK,sw=2)); o.append(arrow(274,200,386,168,c=INK,sw=2))
    o.append(rect(390,220,230,70,fill="#fff4d6",stroke="#e2c46b",sw=1.4,rx=8))
    o.append(text(406,246,"check: flash_matches_erp",13,INK,"bold")); o.append(text(406,268,"blocking: failure stops delivery",11.5,RED,"bold"))
    o.append(path("M505,190 V218",stroke="#c9a53f",sw=2,dash="4 3"))
    o.append(node(740,130,230,60,"deliver_flash","outbox + delivery log",PURPLE))
    o.append(arrow(624,160,736,160,c=INK,sw=2))
    o.append(rect(740,230,230,120,fill="#fbfcfe",stroke=RULE,rx=8))
    o.append(wrap(754,254,["raw_dispatch and raw_crm_leads","have no arrow into the Flash:","their failures don't stop","the sales numbers."],12,MUTED,21))
    return svg(1040,420,"".join(o))

def fig_failure():
    o=[]
    def lane(x,title,c,steps,end,endc):
        out=[text(x,40,title,15,c,"bold",family=HEAD)]
        y=60
        for t,k in steps:
            col={"ok":INK,"bad":RED,"undo":ORANGE}[k]
            out.append(rect(x,y,440,40,fill="#fff",stroke=col if k!="ok" else RULE,sw=1.3,rx=6))
            out.append(text(x+14,y+26,t,12.5,col,"bold" if k!="ok" else None)); y+=50
        out.append(rect(x,y+6,440,54,fill=endc,rx=7))
        out.append(wrap(x+14,y+28,end,13,"#ffffff",20,"bold"))
        return "".join(out)
    o.append(lane(40,"Naive step: append",RED,[("Run 1: INSERT the day's row","ok"),("Worker lost before success is reported","bad"),("Orchestrator retries","ok"),("Run 2: INSERT the day's row again","bad"),("Run 2 succeeds","ok")],
                  ["2 rows for 2 January","SUM(revenue) = Rs 77,420 (true: 38,710)"],RED))
    o.append(lane(550,"Safe step: overwrite in a transaction",GREEN,[("Run 1: BEGIN; DELETE day; INSERT day","ok"),("Worker lost before COMMIT","bad"),("ROLLBACK: table unchanged","undo"),("Run 2: BEGIN; DELETE; INSERT; COMMIT","ok"),("Run 2 succeeds","ok")],
                  ["1 row for 2 January","SUM(revenue) = Rs 38,710"],GREEN))
    return svg(1040,390,"".join(o))

def fig_partitions():
    o=[]; X=60; W=170; G=16; y=110
    days=["1 Jan","2 Jan","3 Jan","4 Jan","5 Jan"]; vals=["0 orders","2 · Rs 38,710","0 orders","0 orders","1 · Rs 18,750"]
    o.append(path(f"M{X},{y-30} V{y-44} H{X+5*W+4*G} V{y-30}",stroke=ACC,sw=2))
    o.append(text(X+(5*W+4*G)/2,y-54,"Backfill: rebuild ingestion, Flash and check for every day, WITHOUT deliver_flash",13,ACC,"bold",anchor="middle"))
    for i,(d,v) in enumerate(zip(days,vals)):
        x=X+i*(W+G)
        o.append(rect(x,y,W,74,fill="#fbfcfe",stroke=ACC,sw=1.5,rx=7))
        o.append(text(x+14,y+28,d+" 2026",13.5,INK,"bold")); o.append(text(x+14,y+52,v,12,MUTED))
        if i in (1,4):
            ex=x+W/2-40; ey=y+100
            o.append(rect(ex,ey,80,50,fill="#fff",stroke=PURPLE,sw=1.6,rx=4))
            o.append(path(f"M{ex},{ey} L{ex+40},{ey+26} L{ex+80},{ey}",stroke=PURPLE,sw=1.6))
            o.append(text(x+W/2,ey+70,"sent by daily run",11.5,PURPLE,"bold",anchor="middle"))
    x=X+1*(W+G); cy=y+210
    o.append(arrow(x+W/2,cy+60,x+W/2,cy+8,c=ORANGE,sw=2))
    o.append(rect(x-40,cy+64,320,64,fill="#fff4e8",stroke=ORANGE,sw=1.5,rx=7))
    o.append(wrap(x-26,cy+88,["6 Jan: order 10177 corrected (6 → 7 crates).","Re-run 2 Jan only: Rs 40,110;","sends flash_2026-01-02_correction_1"],11.5,INK,17))
    o.append(rect(560,cy+64,420,64,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(wrap(574,cy+88,["Outbox after the backfill: still only the two","reports the daily runs sent. History is rebuilt, not re-sent."],12,INK,19))
    return svg(1040,cy+150,"".join(o))

def fig_gate():
    o=[]; y=90
    o.append(node(30,y,170,60,"Ingest","4 raw assets",ACC)); o.append(arrow(204,y+30,236,y+30,c=INK,sw=2))
    o.append(node(240,y,190,60,"Build Flash","partition overwrite",GREEN)); o.append(arrow(434,y+30,466,y+30,c=INK,sw=2))
    o.append(rect(470,y-10,220,80,fill="#fff4d6",stroke="#e2c46b",sw=1.6,rx=8))
    o.append(text(486,y+18,"check: flash_matches_erp",13,INK,"bold")); o.append(wrap(486,y+40,["same query on ERP and","warehouse; one row per day"],11.5,MUTED,17))
    o.append(arrow(694,y+10,760,y-30,c=GREEN,sw=2.2)); o.append(text(690,y-20,"passed",12,GREEN,"bold",anchor="end"))
    o.append(node(764,y-66,240,60,"deliver_flash","outbox + delivery log",PURPLE))
    o.append(arrow(694,y+50,760,y+100,c=RED,sw=2.2)); o.append(text(700,y+96,"failed",12,RED,"bold",anchor="end"))
    o.append(rect(764,y+76,240,48,fill=RED,rx=8)); o.append(text(884,y+106,"Delivery blocked",14,"#ffffff","bold",anchor="middle"))
    o.append(rect(560,y+150,444,124,fill="#fbfcfe",stroke=RED,sw=1.4,rx=8))
    o.append(text(576,y+176,"Alert to the pipeline owner",13.5,RED,"bold"))
    o.append(wrap(576,y+200,["What: Flash for 2026-01-05 NOT sent","Why: ERP orders=1, Rs 18,750 | warehouse orders=0, Rs 0","Next: compare raw.order_items with ERP, fix, re-run the day","Runbook: docs/runbooks/daily_flash.md"],11.5,INK,19))
    o.append(rect(30,y+150,500,124,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(wrap(46,y+178,["On 5 January the order-line load loaded nothing and","raised no error. The Flash built a row of 0 orders.","Only the check, comparing with the ERP, caught it:","checks catch the failures that don't crash."],12.5,INK,21))
    return svg(1040,y+300,"".join(o))

if __name__=="__main__":
    for n,f in [("fig46-1-riverstone-pipeline-graph.svg",fig_graph),("fig46-2-failure-test-naive-vs-safe.svg",fig_failure),
                ("fig46-3-partitions-backfill-corrections.svg",fig_partitions),("fig46-4-checks-gate-delivery.svg",fig_gate)]:
        open(n,"w").write(f())
    print("ok")
