# Generates the SVG figures for Chapter 50. Run: python3 make_figs50.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Canvases are 760 px wide, so they print at 493.2 / 760 = 0.649 pt per px: every font here is at least
# 11 px, which prints at 7.1 pt or more.
# Figure 50.1 matches the companion's mini_log.py: its hash puts M-04 and M-08 in partition 0 and
# M-07 and M-21 in partition 1 (section 50.2 prints "M-07 always goes to partition 1").
# Figure 50.2 matches the three runs of section 50.5 and the hand table before them.
from make_figs import *
from make_figs07 import arrow
GREEN="#2f7d6d"; ORANGE="#c0662b"; RED="#b23b3b"
W=760


def fig_log():
    o=[]
    o.append(text(16,24,"Producers",13,INK,"bold",family=HEAD))
    o.append(text(190,24,"Topic sensor-readings, key = machine id",13,INK,"bold",family=HEAD))
    SX, SW, GAP = 190, 54, 4                      # slot x, slot width, gap
    tops=[64,178]
    contents=[["M-04","M-08","M-04","M-08","M-04","M-08"],["M-07","M-21","M-07","M-21","M-07","M-21"]]
    prods=[("M-04",0,48),("M-08",0,90),("M-07",1,162),("M-21",1,204)]
    for m,p,y in prods:
        o.append(rect(16,y,118,30,fill="#fff",stroke=RULE,sw=1.2,rx=5))
        o.append(text(28,y+20,f"{m} readings",11.5,INK))
        o.append(arrow(136,y+15,SX-6,tops[p]+23,c=MUTED,sw=1.4))
    for p in range(2):
        ytop=tops[p]
        o.append(text(SX,ytop-8,f"partition {p}",12,ACC,"bold"))
        for k in range(7):
            x=SX+k*(SW+GAP)
            if k<6:
                o.append(rect(x,ytop,SW,46,fill="#e6edf4",stroke=RULE,sw=1,rx=4))
                o.append(text(x+7,ytop+18,f"off {k}",11,MUTED))
                o.append(text(x+7,ytop+37,contents[p][k],11.5,INK,"bold"))
            else:
                o.append(rect(x,ytop,SW,46,fill="#fff",stroke=RULE,sw=1,rx=4,extra='stroke-dasharray="4 3"'))
                o.append(text(x+7,ytop+18,"off 6",11,MUTED))
                o.append(text(x+7,ytop+37,"next",11,MUTED,style="italic"))
    # committed-offset markers: a committed offset is the NEXT position to read
    def marker(p,off,label,c,dy,left=False):
        x=SX+off*(SW+GAP)-GAP/2; y=tops[p]+46
        return (path(f"M{x},{y+2} V{y+dy}",stroke=c,sw=1.8)
                +f'<path d="M{x},{y+1} l-5,9 h10 Z" fill="{c}"/>'
                +text(x-6 if left else x+6,y+dy+2,label,11,c,"bold",anchor="end" if left else "start"))
    o.append(marker(0,6,"both groups: offset 6",GREEN,22,left=True))
    o.append(marker(1,3,"alerting: offset 3 (lag 3)",ORANGE,22))
    o.append(marker(1,6,"scrap-monitor: offset 6 (lag 0)",GREEN,40,left=True))
    # the group table on the right
    gx=610
    o.append(text(gx,24,"Consumer groups",13,INK,"bold",family=HEAD))
    for i,(name,c,lines) in enumerate([("scrap-monitor",GREEN,["offsets: 6 and 6","lag 0: up to date"]),
                                       ("alerting",ORANGE,["offsets: 6 and 3","lag 3: three events","behind in partition 1"])]):
        y=48+i*112
        h=78 if i==0 else 96
        o.append(rect(gx,y,142,h,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(gx,y,6,h,fill=c,rx=3))
        o.append(text(gx+16,y+24,name,12.5,c,"bold"))
        for j,l in enumerate(lines):
            o.append(text(gx+16,y+46+j*18,l,11,INK))
    o.append(path(f"M16,296 H{W-16}",stroke=RULE,sw=1))
    o.append(text(16,320,"Order is guaranteed inside a partition: every M-07 reading is in partition 1, in the order it was sent.",11.5,INK,"bold"))
    o.append(text(16,342,"Across partitions there is no order: that is the price of reading them in parallel.",11.5,MUTED))
    o.append(text(16,364,"A committed offset is the next position the group will read, so offset 3 means offsets 0, 1 and 2 are done.",11.5,MUTED))
    return svg(W,380,"".join(o))


def fig_watermark():
    o=[]
    o.append(text(16,24,"Event time, 5-minute windows, and a watermark 10 minutes behind the newest event",13,INK,"bold",family=HEAD))
    X0, PX = 70, 20.0                              # x of 00:00, pixels per minute
    xm=lambda minutes: X0+minutes*PX
    ay=176                                         # axis y
    # windows
    counts=["456 = 450 + 6","450","450","open","open","open"]
    for i in range(6):
        x=xm(i*5)
        o.append(rect(x+1,ay-50,5*PX-2,44,fill="#f2f4f7" if i<3 else "#fff",stroke=RULE,sw=1,rx=4))
        o.append(text(x+7,ay-32,f"00:{i*5:02d}–00:{i*5+5:02d}",11,INK,"bold"))
        o.append(text(x+7,ay-14,counts[i],11,MUTED if i>=3 else INK))
    o.append(text(16,46,"Boxes: Bhiwandi Main readings per window after all three runs. Dashed lines: the watermark after each run.",11,MUTED,style="italic"))
    # axis
    o.append(path(f"M{xm(-2)},{ay} H{xm(30)+8}",stroke=INK,sw=1.4))
    for m in range(0,31,5):
        o.append(path(f"M{xm(m)},{ay-4} V{ay+4}",stroke=INK,sw=1.2))
        o.append(text(xm(m),ay+18,f"00:{m:02d}",11,INK,anchor="middle"))
    o.append(text(xm(30)+12,ay+4,"event time",11,MUTED,style="italic"))
    # late readings at 00:02
    o.append(f'<circle cx="{xm(2)}" cy="{ay}" r="5" fill="{RED}"/>')
    o.append(path(f"M{xm(2)},{ay+6} V{ay+34}",stroke=RED,sw=1.2))
    o.append(text(xm(2)+6,ay+44,"late readings with event time 00:02: six from M-07 arrive in run 2, six from M-09 in run 3",11,RED,"bold"))
    # watermarks (after each run), labelled by text, not colour alone
    wms=[(-10/60,"after run 1: 23:59:50",ACC,80),(9+50/60,"after run 2: 00:09:50",GREEN,80),(19+50/60,"after run 3: 00:19:50",ORANGE,80)]
    for m,label,c,ly in wms:
        x=xm(m)
        o.append(path(f"M{x},{ly+4} V{ay+2}",stroke=c,sw=1.8,dash="5 3"))
        o.append(text(x+4,ly,label,11,c,"bold"))
    # three run cards
    cards=[("Run 1: events 00:00 to 00:09:50","watermark in force: none yet; after the run: 23:59:50",
            ["No window ends by 23:59:50, so append mode writes nothing."],ACC),
           ("Run 2: events 00:10 to 00:19:50, plus six M-07 readings from 00:02","watermark in force: 23:59:50; after the run: 00:09:50",
            ["00:02 is later than 23:59:50, so the six are kept: 450 + 6 = 456.",
             "00:00–00:05 ends before 00:09:50: written. 00:05–00:10 ends at 00:10:00: it waits."],GREEN),
           ("Run 3: events 00:20 to 00:29:50, plus six M-09 readings from 00:02","watermark in force: 00:09:50; after the run: 00:19:50",
            ["00:02 is earlier than 00:09:50, so the six are dropped, silently; 456 stays 456.",
             "00:05–00:10 and 00:10–00:15 now end before 00:19:50: both are written."],ORANGE)]
    y=240
    for title,wm,notes,c in cards:
        h=48+18*len(notes)
        o.append(rect(16,y,W-32,h,fill="#fbfcfe",stroke=c,sw=1.4,rx=7)); o.append(rect(16,y,6,h,fill=c,rx=3))
        o.append(text(32,y+22,title,12,c,"bold"))
        o.append(text(32,y+42,wm,11.5,INK,"bold"))
        for j,n in enumerate(notes):
            o.append(text(32,y+62+j*18,n,11.5,INK))
        y+=h+8
    o.append(text(16,y+16,"A window is final once the watermark passes its end; a reading older than the watermark in force is dropped.",11.5,INK,"bold"))
    return svg(W,y+28,"".join(o))


if __name__=="__main__":
    for n,f in [("fig50-1-log-partitions-offsets.svg",fig_log),("fig50-2-event-time-watermark.svg",fig_watermark)]:
        open(n,"w").write(f())
    print("ok")
