# Generates the SVG figures for Chapter 50. Run: python3 make_figs50.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_log():
    o=[]
    o.append(text(30,32,"Producers",13.5,INK,"bold",family=HEAD))
    for i,(m,p) in enumerate([("M-03", 0),("M-07", 1),("M-12", 0),("M-21", 1)]):
        y=52+i*38
        o.append(rect(30,y,120,30,fill="#fff",stroke=RULE,sw=1.2,rx=5))
        o.append(text(42,y+20,f"{m} reading",11.5,INK))
        o.append(arrow(152,y+15,232,120+p*150,c=MUTED,sw=1.4))
    o.append(text(240,32,"Topic: sensor-readings (key = machine_id)",13.5,INK,"bold",family=HEAD))
    for p in range(2):
        ytop=100+p*150
        o.append(text(240,ytop-8,f"partition {p}",12,ACC,"bold"))
        for k in range(8):
            x=240+k*62
            fill="#e6edf4" if k<6 else "#f6f9fc"
            o.append(rect(x,ytop,58,44,fill=fill,stroke=RULE,sw=1,rx=4))
            o.append(text(x+8,ytop+18,f"off {k}",10.5,MUTED))
            o.append(text(x+8,ytop+36,["M-03","M-12","M-03","M-07","M-21","M-07","",""][k] if p else ["M-12","M-03","M-12","M-03","M-12","M-03","",""][k],11,INK,"bold"))
        o.append(text(240+8*62+6,ytop+26,"new events",11,MUTED,style="italic"))
    o.append(path("M240,296 H736",stroke=RULE,sw=1))
    o.append(text(240,330,"Order is guaranteed inside a partition:",12.5,GREEN,"bold"))
    o.append(text(240,352,"M-07 always lands in the same one.",12.5,GREEN,"bold"))
    o.append(text(240,374,"Across partitions there is no order at all: that is the price of parallelism.",12,MUTED))
    gx=760
    o.append(text(gx,32,"Consumer groups",13.5,INK,"bold",family=HEAD))
    for i,(name,c,lag,note) in enumerate([("scrap-monitor",GREEN,0,"committed offset 6: up to date"),("alerting",ORANGE,3,"committed offset 3: lag 3")]):
        y=100+i*150
        o.append(rect(gx,y,250,80,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(gx,y,6,80,fill=c,rx=3))
        o.append(text(gx+18,y+26,name,13,c,"bold"))
        o.append(wrap(gx+18,y+48,[note,"reads at its own speed"],11.5,INK,18))
    return svg(1040,400,"".join(o))

def fig_watermark():
    o=[]; X=70; W=880; y=70
    o.append(text(30,34,"Event time, five-minute windows, and a watermark ten minutes behind",14.5,INK,"bold",family=HEAD))
    for i in range(4):
        x=X+i*(W/4)
        o.append(rect(x,y,W/4-4,54,fill="#f2f4f7",stroke=RULE,sw=1,rx=5))
        o.append(text(x+12,y+22,f"{i*5:02d}:00 window" if False else f"00:{i*5:02d} - 00:{i*5+5:02d}",12.5,INK,"bold"))
        o.append(text(x+12,y+42,["450 on time + 6 late = 456","450","450","filling"][i],11.5,MUTED))
    marks=[("batch 1: newest event 00:09:50","watermark 23:59:50 (previous day)","nothing is final yet, so append mode emits nothing",ACC,y+110),
           ("batch 2: newest event 00:19:50","watermark 00:09:50","windows 00:00-00:05 and 00:05-00:10 close; the six events from 00:02 arrived first, so they count",GREEN,y+186),
           ("batch 3: newest event 00:29:50","watermark 00:19:50","more events from 00:02 arrive: now behind the watermark, so they are dropped and 456 stays 456",RED,y+262)]
    for title,wm,note,c,yy in marks:
        o.append(rect(30,yy,980,62,fill="#fbfcfe",stroke=c,sw=1.4,rx=7)); o.append(rect(30,yy,6,62,fill=c,rx=3))
        o.append(text(48,yy+24,title,12.5,c,"bold"))
        o.append(text(300,yy+24,wm,12.5,INK,"bold"))
        o.append(text(48,yy+46,note,11.5,MUTED))
    o.append(text(30,y+352,"The watermark is a promise about how long you wait. Everything later than it is dropped, silently, by design.",12.5,INK,"bold"))
    return svg(1040,y+372,"".join(o))

if __name__=="__main__":
    for n,f in [("fig50-1-log-partitions-offsets.svg",fig_log),("fig50-2-event-time-watermark.svg",fig_watermark)]:
        open(n,"w").write(f())
    print("ok")
