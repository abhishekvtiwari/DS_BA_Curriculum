# Generates the SVG figures for Chapter 45. Run: python3 make_figs45.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Figures print at the full text width (493.2 pt), so a font of s px on a W px canvas prints at
# s * 493.2 / W pt. Canvases here are 720-760 px wide and the smallest text is 11 px (>= 7.1 pt).
# The load-strategies comparison (old Figure 45.3) is now a normal table in the chapter text.
import os
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_sources():
    o=[]
    src=[("Databases","ERP orders, customers","Hard: don't say what changed"),
         ("Files","Dispatch sheet, bank statements","Hard: late, repeated, malformed"),
         ("APIs","CRM leads","Hard: pages, limits, expiring tokens"),
         ("Events","Enquiries, sensor readings","Hard: late, out of order, twice"),
         ("SaaS tools","Email marketing, support desk","Hard: schemas and limits change")]
    y=10
    for name,ex,hard in src:
        o.append(rect(10,y,290,64,fill="#fff",stroke=RULE,sw=1.3,rx=7))
        o.append(text(22,y+20,name,13,INK,"bold",family=HEAD))
        o.append(text(22,y+38,ex,11.5,MUTED))
        o.append(text(22,y+55,hard,11.5,RED,"bold"))
        o.append(arrow(302,y+32,334,180,c=MUTED,sw=1.4))
        y+=72
    o.append(header_card(338,92,190,172,GREEN,"Ingestion",tsize=14))
    o.append(wrap(350,150,["Full, incremental,","hash or CDC loads","","Declared types","Retries, pagination"],11.5,INK,18))
    o.append(rect(338,278,190,58,fill="#fff4d6",stroke="#e2c46b",rx=7))
    o.append(wrap(350,302,["Load log and","reconciliation checks"],11.5,INK,18,"bold"))
    o.append(arrow(532,180,552,180,c=INK,sw=2.2))
    o.append(text(556,70,"WAREHOUSE",11,MUTED,"bold"))
    layers=[("Raw",["As it arrived, plus","file and load date"],ACC),
            ("Staging",["Typed, cleaned,","rejects listed"],ACC),
            ("Modeled",["Business-ready","tables (Ch 32)"],PURPLE)]
    yy=80
    for n,d,c in layers:
        o.append(rect(556,yy,194,70,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(556,yy,8,70,fill=c,rx=3))
        o.append(text(574,yy+22,n,13,c,"bold",family=HEAD))
        o.append(wrap(574,yy+41,d,11.5,INK,17)); yy+=78
    return svg(760,372,"".join(o))

def fig_watermark():
    o=[]; X=20; W=680
    o.append('<defs><pattern id="hatch45" width="10" height="10" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="10" height="10" fill="#fbeaea"/>'
             '<line x1="0" y1="0" x2="0" y2="10" stroke="#e6b8b8" stroke-width="3"/></pattern></defs>')
    o.append(text(X,24,"1 JANUARY: warehouse loaded up to order 10175",12.5,INK,"bold"))
    o.append(text(X,46,"2 JANUARY: what happens in the ERP, and what an ID-watermark load reads",12.5,INK,"bold"))
    top=62; wy=top+130; bot=wy+140
    o.append(rect(X,top,W,wy-top,fill="#eaf5f1"))
    o.append(rect(X,wy,W,bot-wy,fill="url(#hatch45)"))
    o.append(path(f"M{X},{wy} H{X+W}",stroke=INK,sw=2.5,dash="8 5"))
    o.append(rect(X+W-236,wy-11,228,22,fill="#fff",stroke=INK,sw=1,rx=4))
    o.append(text(X+W-122,wy+5,"watermark: order_id 10175",12,INK,"bold",anchor="middle"))
    o.append(text(X+12,top+22,"✓ READ by the load (order_id > 10175)",12,GREEN,"bold"))
    o.append(rect(X+8,wy+12,356,22,fill="#fff",rx=4))
    o.append(text(X+14,wy+28,"✗ NOT READ (order_id ≤ 10175): MISSED",12,RED,"bold"))
    for i,(t,s) in enumerate([("10176 inserted","✓ new order, loaded"),("10177 inserted","✓ new order, loaded")]):
        x=X+60+i*300; o.append(rect(x,top+42,260,66,fill="#fff",stroke=GREEN,sw=1.8,rx=7))
        o.append(text(x+14,top+68,t,13,INK,"bold")); o.append(text(x+14,top+92,s,11.5,GREEN,"bold"))
    for i,(t,s) in enumerate([("10174 updated","✗ Pending → Cancelled: missed"),("10175 updated","✗ Shipped → Delivered: missed")]):
        x=X+60+i*300; o.append(rect(x,wy+50,260,66,fill="#fff",stroke=RED,sw=1.8,rx=7,extra='stroke-dasharray="6 3"'))
        o.append(text(x+14,wy+76,t,13,INK,"bold")); o.append(text(x+14,wy+100,s,11.5,RED,"bold"))
    return svg(720,bot+10,"".join(o))

def fig_files():
    o=[]
    steps=[("1 Receive",ACC,["Check name and date","Hash; skip repeats","Log it after loading"]),
           ("2 Read",ACC,["Declare encoding,","delimiter, header, types","Awkward fields as text"]),
           ("3 Land raw",GREEN,["Exactly what arrived","+ file name","+ load date"]),
           ("4 Type in staging",GREEN,["Explicit date formats","Remove separators","TRY_CAST; list failures"]),
           ("5 Reconcile",PURPLE,["Records = rows loaded","Rejects listed","Totals vs sender"]),
           ("6 Alert or proceed",ORANGE,["Tell a person about","rejects before reports","and emails run"])]
    W=212; G=30; H=118; X0=12; ys=[10,172]
    for i,(t,c,lines) in enumerate(steps):
        r,k=divmod(i,3); x=X0+k*(W+G); y=ys[r]
        o.append(header_card(x,y,W,H,c,t,tsize=13))
        o.append(wrap(x+12,y+56,lines,11.5,INK,18))
        if k<2: o.append(arrow(x+W+4,y+H/2,x+W+G-4,y+H/2,c=INK,sw=2))
    # from step 3 (end of the first row) back to step 4 (start of the second row)
    x3=X0+2*(W+G)+W/2; x4=X0+W/2; yb=ys[0]+H+6; ym=ys[1]-22
    o.append(path(f"M{x3},{yb} V{ym} H{x4}",stroke=INK,sw=2))
    o.append(arrow(x4,ym,x4,ys[1]-4,c=INK,sw=2))
    return svg(720,ys[1]+H+14,"".join(o))

if __name__=="__main__":
    for n,f in [("fig45-1-sources-to-warehouse.svg",fig_sources),("fig45-2-watermark-misses-updates.svg",fig_watermark),
                ("fig45-3-reliable-file-loading.svg",fig_files)]:
        open(n,"w").write(f())
    for old in ("fig45-3-load-strategies-compared.svg","fig45-4-reliable-file-loading.svg"):
        if os.path.exists(old): os.remove(old)
    print("ok")
