# Generates the SVG figures for Chapter 45. Run: python3 make_figs45.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_sources():
    o=[]
    src=[("Databases","ERP orders, customers","Don't say what changed"),
         ("Files","Dispatch sheet, bank statements","Late, repeated, malformed"),
         ("APIs","CRM leads","Pages, limits, expiring tokens"),
         ("Events","Enquiries, sensor readings","Late, out of order, twice"),
         ("SaaS tools","Email marketing, support desk","Schemas and limits change")]
    y=24
    for name,ex,hard in src:
        o.append(rect(30,y,300,78,fill="#fff",stroke=RULE,sw=1.3,rx=7))
        o.append(text(46,y+24,name,14,INK,"bold",family=HEAD)); o.append(text(46,y+44,ex,12,MUTED))
        o.append(text(46,y+64,hard,12,RED,"bold"))
        o.append(arrow(334,y+39,414,242,c=MUTED,sw=1.6))
        y+=90
    o.append(header_card(420,150,220,190,GREEN,"Ingestion"))
    o.append(wrap(434,210,["Full, incremental,","hash or CDC loads","","Declared types","Retries, pagination"],12.5,INK,19))
    o.append(rect(420,356,220,74,fill="#fff4d6",stroke="#e2c46b",rx=7))
    o.append(wrap(434,382,["Load log and","reconciliation checks"],12.5,INK,19,"bold"))
    o.append(arrow(644,245,700,245,c=INK,sw=2.2))
    layers=[("Raw","As it arrived, plus file and load date",ACC),("Staging","Typed, cleaned, rejects listed",ACC),("Modeled","Business-ready tables (Ch 32)",PURPLE)]
    o.append(text(706,120,"WAREHOUSE",11,MUTED,"bold"))
    yy=132
    for n,d,c in layers:
        o.append(rect(706,yy,300,70,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(706,yy,8,70,fill=c,rx=3))
        o.append(text(726,yy+28,n,14,c,"bold",family=HEAD)); o.append(text(726,yy+50,d,12,INK)); yy+=82
    return svg(1040,480,"".join(o))

def fig_watermark():
    o=[]; X=60; W=900
    o.append(text(X,34,"1 JANUARY: warehouse loaded up to order 10175",13,INK,"bold"))
    o.append(text(X,58,"2 JANUARY: what happens in the ERP, and what an ID-watermark load reads",13,INK,"bold"))
    top=80; H=300; wy=top+170
    o.append(rect(X,top,W,wy-top,fill="#eaf5f1"))
    o.append(rect(X,wy,W,top+H-wy,fill="#fbeaea"))
    o.append(path(f"M{X},{wy} H{X+W}",stroke=INK,sw=2.5,dash="8 5"))
    o.append(text(X+W-8,wy-10,"watermark: order_id 10175",12.5,INK,"bold",anchor="end"))
    o.append(text(X+14,top+24,"READ by the load (order_id > 10175)",12,GREEN,"bold"))
    o.append(text(X+14,wy+24,"NOT READ (order_id ≤ 10175)",12,RED,"bold"))
    for i,(t,s) in enumerate([("10176 inserted","new order, loaded"),("10177 inserted","new order, loaded")]):
        x=X+120+i*300; o.append(rect(x,top+60,240,70,fill="#fff",stroke=GREEN,sw=1.6,rx=7))
        o.append(text(x+14,top+90,t,13.5,INK,"bold")); o.append(text(x+14,top+112,s,12,GREEN,"bold"))
    for i,(t,s) in enumerate([("10174 updated","Pending → Cancelled: missed"),("10175 updated","Shipped → Delivered: missed")]):
        x=X+120+i*300; o.append(rect(x,wy+40,240,70,fill="#fff",stroke=RED,sw=1.6,rx=7))
        o.append(text(x+14,wy+70,t,13.5,INK,"bold")); o.append(text(x+14,wy+92,s,12,RED,"bold"))
    o.append(text(X,top+H+30,"The load finished without errors. Only a reconciliation against the source showed the two stale orders.",12.5,MUTED))
    return svg(1030,top+H+50,"".join(o))

def fig_strategies():
    o=[]
    cols=["","Full load","Incremental (watermark)","Hash comparison","Change data capture"]
    rows=[("Reads","Whole table","Rows past last ID/time","All keys and hashes","The change log"),
          ("Inserts","Yes","Yes","Yes","Yes"),
          ("Updates","Yes","Only with reliable updated_at","Yes","Yes, in order"),
          ("Deletes","Yes","No","Yes","Yes"),
          ("Load on source","Heavy for big tables","Light","Medium to heavy","Very light"),
          ("Complexity","Simplest","Simple, can miss silently","Moderate","Settings, permissions, slots")]
    X=30; CW=[140,170,262,190,230]; top=30; RH=46
    x=X
    o.append(rect(X,top,sum(CW),42,fill=INK,rx=6))
    for c,w in zip(cols,CW):
        o.append(text(x+12,top+27,c,13,"#ffffff","bold")); x+=w
    good={"Yes","Yes, in order","Very light","Light","Simplest"}; bad={"No","Only with reliable updated_at","Heavy for big tables","Simple, can miss silently"}
    for i,r in enumerate(rows):
        y=top+42+i*RH; x=X
        o.append(rect(X,y,sum(CW),RH,fill=ROWALT if i%2==0 else "#fff"))
        for j,(v,w) in enumerate(zip(r,CW)):
            col=INK if j==0 else (GREEN if v in good else RED if v in bad else INK)
            o.append(text(x+12,y+29,v,12.5,col,"bold" if j==0 or v in good|bad else None)); x+=w
    yb=top+42+len(rows)*RH
    o.append(path(f"M{X},{yb} H{X+sum(CW)}",stroke=RULE,sw=1))
    return svg(1030,yb+20,"".join(o))

def fig_files():
    o=[]
    steps=[("1 Receive",ACC,["Check name and date","Hash; skip repeats","Record in load log"]),
           ("2 Read",ACC,["Declare encoding,","delimiter, header, types","Awkward fields as text"]),
           ("3 Land raw",GREEN,["Exactly what arrived","+ file name","+ load date"]),
           ("4 Type in staging",GREEN,["Explicit date formats","Remove separators","TRY_CAST; list failures"]),
           ("5 Reconcile",PURPLE,["Records = rows loaded","Rejects listed","Totals vs sender"]),
           ("6 Alert or proceed",ORANGE,["Tell a person about","rejects before reports","and emails run"])]
    W=146; G=20; y=40
    for i,(t,c,lines) in enumerate(steps):
        x=30+i*(W+G)
        o.append(header_card(x,y,W,150,c,t,tsize=12.5))
        o.append(wrap(x+10,y+62,lines,11.5,INK,19))
        if i<5: o.append(arrow(x+W+2,y+90,x+W+G-2,y+90,c=INK,sw=2))
    return svg(1030,y+176,"".join(o))

if __name__=="__main__":
    for n,f in [("fig45-1-sources-to-warehouse.svg",fig_sources),("fig45-2-watermark-misses-updates.svg",fig_watermark),
                ("fig45-3-load-strategies-compared.svg",fig_strategies),("fig45-4-reliable-file-loading.svg",fig_files)]:
        open(n,"w").write(f())
    print("ok")
