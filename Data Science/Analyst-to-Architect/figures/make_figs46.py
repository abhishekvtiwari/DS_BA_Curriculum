# Generates the SVG figures for Chapter 46. Run: python3 make_figs46.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Canvases are 760 px wide, so they print at 493.2 / 760 = 0.649 pt per px: every font here is at least
# 11 px, which prints at 7.1 pt or more.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=760

def node(x,y,w,h,title,sub,c,fill="#fff"):
    return (rect(x+3,y+4,w,h,fill="#e9eef4",rx=8)+rect(x,y,w,h,fill=fill,stroke=c,sw=1.6,rx=8)
            +rect(x,y,7,h,fill=c,rx=3)+text(x+16,y+24,title,13,INK,"bold")+text(x+16,y+43,sub,11.5,MUTED))

def envelope(x,y,w,h,c):
    return rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=4)+path(f"M{x},{y} L{x+w/2},{y+h*0.52} L{x+w},{y}",stroke=c,sw=1.6)

def fig_graph():
    o=[]
    o.append(rect(16,14,728,54,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(30,36,"Schedule: 30 6 * * *  ·  Asia/Kolkata",12.5,INK,"bold"))
    o.append(text(30,56,"Each run builds the last complete day: the 6:30 run on 6 Jan builds partition 2026-01-05",11.5,MUTED))
    ys=[92,166,240,314]
    names=[("raw_orders","whole table: hash + upsert"),("raw_order_items","whole table: hash + upsert"),
           ("raw_dispatch","one day's file, column check"),("raw_crm_leads","whole list: API, retry policy")]
    for (n,s),y in zip(names,ys):
        o.append(node(20,y,215,56,n,s,ACC))
    o.append(node(290,130,200,56,"daily_flash","per day: partition overwrite",GREEN))
    o.append(arrow(239,120,286,150,c=INK,sw=2)); o.append(arrow(239,194,286,166,c=INK,sw=2))
    o.append(rect(290,214,200,66,fill="#fff4d6",stroke="#e2c46b",sw=1.4,rx=8))
    o.append(text(304,238,"check: flash_matches_erp",12,INK,"bold"))
    o.append(text(304,260,"blocking: a failure",11.5,RED,"bold")); o.append(text(304,275,"stops delivery",11.5,RED,"bold"))
    o.append(path("M390,186 V212",stroke="#c9a53f",sw=2,dash="4 3"))
    o.append(node(545,130,195,56,"deliver_flash","per day: outbox + log",PURPLE))
    o.append(arrow(494,158,541,158,c=INK,sw=2))
    o.append(rect(290,304,450,66,fill="#fbfcfe",stroke=RULE,rx=8))
    o.append(wrap(304,328,["raw_dispatch and raw_crm_leads have no arrow into the Flash:",
                           "their failures don't stop the sales numbers."],12,MUTED,20))
    return svg(W,390,"".join(o))

def fig_failure():
    o=[]
    def lane(x,title,c,steps,end,mark):
        out=[text(x,34,title,14,c,"bold",family=HEAD)]
        y=50
        for t,k in steps:
            col={"ok":INK,"bad":RED,"undo":ORANGE}[k]
            out.append(rect(x,y,350,36,fill="#fff",stroke=col if k!="ok" else RULE,sw=1.3,rx=6))
            out.append(text(x+12,y+23,t,11.5,col,"bold" if k!="ok" else "normal")); y+=44
        out.append(rect(x,y+6,350,56,fill=c,rx=7))
        out.append(text(x+16,y+45,mark,26,"#ffffff","bold"))
        out.append(wrap(x+52,y+29,end,12.5,"#ffffff",20,"bold"))
        return "".join(out)
    o.append(lane(20,"Naive step: append",RED,
                  [("Run 1: INSERT the day's row","ok"),("Worker lost before success is reported","bad"),
                   ("Orchestrator retries","ok"),("Run 2: INSERT the day's row again","bad"),("Run 2 succeeds","ok")],
                  ["Wrong: 2 rows for 2 January","SUM(revenue) = ₹77,420 (true: ₹38,710)"],"✗"))
    o.append(lane(390,"Safe step: overwrite in a transaction",GREEN,
                  [("Run 1: BEGIN; DELETE the day's row","ok"),("Worker lost between DELETE and INSERT","bad"),
                   ("ROLLBACK: the old row is still there","undo"),("Run 2: BEGIN; DELETE; INSERT; COMMIT","ok"),
                   ("Run 2 succeeds","ok")],
                  ["Right: 1 row for 2 January","SUM(revenue) = ₹38,710"],"✓"))
    return svg(W,340,"".join(o))

def fig_partitions():
    o=[]; X=31; BW=130; G=12; y=86
    days=["1 Jan","2 Jan","3 Jan","4 Jan","5 Jan"]
    vals=[("0 orders","holiday"),("2 orders","₹38,710"),("0 orders","weekend"),("0 orders","weekend"),
          ("0 orders","ERP day not run yet")]
    span=5*BW+4*G
    o.append(path(f"M{X},{y-14} V{y-26} H{X+span} V{y-14}",stroke=ACC,sw=2))
    o.append(text(X+span/2,y-36,"Backfill: rebuild the Flash and its check for every day, without deliver_flash",
                  12.5,ACC,"bold",anchor="middle"))
    for i,(d,(v1,v2)) in enumerate(zip(days,vals)):
        x=X+i*(BW+G)
        o.append(rect(x,y,BW,78,fill="#fbfcfe",stroke=ACC,sw=1.5,rx=7))
        o.append(text(x+12,y+24,d+" 2026",13,INK,"bold"))
        o.append(text(x+12,y+46,v1,11.5,INK)); o.append(text(x+12,y+64,v2,11.5,MUTED))
    x2=X+BW+G                                  # the 2 January column
    ex,ey=x2+BW/2-36,y+100
    o.append(envelope(ex,ey,72,44,PURPLE))
    o.append(text(x2+BW/2,ey+62,"flash_2026-01-02",11.5,PURPLE,"bold",anchor="middle"))
    o.append(text(x2+BW/2,ey+78,"sent by its daily run",11.5,PURPLE,anchor="middle"))
    # the late correction: a panel whose arrow runs into the 2 January envelope
    px,py=X+2*(BW+G),y+96
    o.append(rect(px,py,span-2*(BW+G),96,fill="#fff4e8",stroke=ORANGE,sw=1.5,rx=7))
    o.append(arrow(px,py+22,ex+76,py+22,c=ORANGE,sw=2.2))
    o.append(wrap(px+14,py+24,["Late correction, 6 Jan: order 10177 was 7 crates, not 6.",
                               "Re-run 2 Jan only: the Flash becomes ₹40,110, and delivery",
                               "sends flash_2026-01-02_correction_1, labeled CORRECTION."],11.5,INK,19))
    ny=py+116
    o.append(rect(X,ny,span,50,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(wrap(X+14,ny+21,["Outbox after the backfill: still only the report the 2 January daily run sent.",
                              "History is rebuilt, not re-sent."],12,INK,19))
    return svg(W,ny+66,"".join(o))

def fig_gate():
    o=[]; y=96
    o.append(node(16,y,130,56,"Ingest","4 raw assets",ACC)); o.append(arrow(150,y+28,170,y+28,c=INK,sw=2))
    o.append(node(174,y,160,56,"Build Flash","per-day overwrite",GREEN)); o.append(arrow(338,y+28,358,y+28,c=INK,sw=2))
    o.append(rect(362,y-10,190,76,fill="#fff4d6",stroke="#e2c46b",sw=1.6,rx=8))
    o.append(text(376,y+14,"check: flash_matches_erp",12,INK,"bold"))
    o.append(wrap(376,y+34,["same query on ERP and","warehouse; one row a day"],11.5,MUTED,17))
    o.append(arrow(556,y+4,596,y-34,c=GREEN,sw=2.2)); o.append(text(566,y-30,"✓ passed",12,GREEN,"bold",anchor="end"))
    o.append(node(600,y-70,145,56,"deliver_flash","outbox + log",PURPLE))
    o.append(arrow(556,y+52,596,y+90,c=RED,sw=2.2)); o.append(text(566,y+96,"✗ failed",12,RED,"bold",anchor="end"))
    o.append(rect(600,y+72,145,44,fill=RED,rx=8)); o.append(text(672,y+99,"✗ Delivery blocked",12.5,"#ffffff","bold",anchor="middle"))
    o.append(rect(350,y+136,395,118,fill="#fbfcfe",stroke=RED,sw=1.4,rx=8))
    o.append(text(364,y+160,"Alert to the pipeline owner",13,RED,"bold"))
    o.append(wrap(364,y+182,["What: the Flash for 2026-01-05 was NOT sent",
                             "Why: ERP 1 order, ₹18,750 | warehouse 0, ₹0",
                             "Next: compare raw.order_items with the ERP, fix,","then re-run the day. Runbook: daily_flash.md"],11.5,INK,18))
    o.append(rect(16,y+136,318,118,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(wrap(30,y+160,["On 5 January the order-line load loaded","nothing and raised no error. The Flash",
                            "built a row of 0 orders. Only the check,","comparing with the ERP, caught it: checks",
                            "catch the failures that don't crash."],12,INK,19))
    return svg(W,y+270,"".join(o))

if __name__=="__main__":
    for n,f in [("fig46-1-riverstone-pipeline-graph.svg",fig_graph),("fig46-2-failure-test-naive-vs-safe.svg",fig_failure),
                ("fig46-3-partitions-backfill-corrections.svg",fig_partitions),("fig46-4-checks-gate-delivery.svg",fig_gate)]:
        open(n,"w").write(f())
    print("ok")
