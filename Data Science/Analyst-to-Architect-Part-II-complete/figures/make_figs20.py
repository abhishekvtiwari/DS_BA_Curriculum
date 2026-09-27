# Diagrams for Chapter 20. Run: python3 make_figs20.py
# (fig20-3 is a real screenshot of the email produced by companion/ch20/daily_flash.py.)
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def ladder():
    rungs=[("1  Manual","Someone opens the files and does it","Every time, from scratch","0 hours saved",MUTED),
           ("2  Refreshable","Power Query / a model / a saved query","One click, same steps","Most of the error gone",ACC),
           ("3  Scheduled","A script runs at a fixed time","Nobody has to remember","The report arrives",GREEN),
           ("4  Triggered","It runs when something happens","New file, form response, threshold","Minutes, not a day",PURPLE),
           ("5  Self-serve","People answer their own questions","A model or dashboard they trust","You stop being the bottleneck",GOLD)]
    o=[text(30,34,"The analyst's automation ladder",15,INK,"bold",family=HEAD),
       text(30,56,"Each rung removes a different kind of work. Most reports should stop at 3; the ones people ask about hourly belong at 5.",11.6,MUTED)]
    for i,(name,how,what,gain,c) in enumerate(rungs):
        y=80+i*70; w=280+i*120
        o.append(rect(30,y,w,54,fill="#fff",stroke=c,sw=1.6,rx=7)); o.append(rect(30,y,9,54,fill=c))
        o.append(text(52,y+22,name,13.5,c,"bold")); o.append(text(52,y+41,how,11.4,INK))
        o.append(text(w+48,y+22,what,11.6,INK)); o.append(text(w+48,y+41,gain,11.4,MUTED))
    o.append(text(30,442,"Climbing costs effort and adds things that can break: every rung above 2 needs logging, failure alerts, and an owner.",11.6,MUTED))
    return svg(1120,460,"".join(o))

def flow():
    o=[text(30,34,"Mapping a report's flow, and finding the manual steps",15,INK,"bold",family=HEAD)]
    steps=[("ERP export","daily, 02:00","automatic",GREEN),("Analyst opens 4 files","08:30","MANUAL 25 min",RED),
           ("Clean and combine","in a workbook","MANUAL 30 min",RED),("Pivot + chart","in the same workbook","MANUAL 20 min",RED),
           ("Write commentary","3 sentences","judgment: keep",GOLD),("Email to 14 managers","by 10:00","MANUAL 5 min",RED)]
    for i,(name,when,kind,c) in enumerate(steps):
        x=30+i*180
        o.append(rect(x,80,160,96,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(text(x+12,104,name,11.8,INK,"bold")); o.append(text(x+12,124,when,11,MUTED))
        o.append(rect(x+12,136,136,26,fill=c,rx=4)); o.append(text(x+80,154,kind,11,"#fff","bold",anchor="middle"))
        if i<5: o.append(arrow(x+162,128,x+178,128))
    o.append(rect(30,200,1050,86,fill="#fff",stroke=ACC,sw=1.5,rx=8)); o.append(rect(30,200,9,86,fill=ACC))
    o.append(text(52,226,"What the map tells you",13,INK,"bold"))
    o.append(text(52,248,"80 minutes a day are mechanical; 3 sentences are judgment. Automate the 80, keep the 3, and put them in the email as a comment box.",11.6,INK))
    o.append(text(52,270,"Time the steps for one week before deciding: people are wrong about which step is the slow one.",11.6,MUTED))
    return svg(1110,300,"".join(o))

def trust():
    o=[text(30,34,"What makes an automation trustworthy",15,INK,"bold",family=HEAD)]
    items=[("It says what it did","A log line per run: rows, totals, time taken","logging, run history",ACC),
           ("It checks before it sends","Row counts, date range, totals vs last period","fail = no email",GREEN),
           ("It tells you when it breaks","A failure alert to a person, not a mailbox nobody reads","alert on exception",RED),
           ("It handles 'nothing today'","Says \"no sales recorded\" instead of an empty table","explicit empty case",GOLD),
           ("It can be run twice","Same input, same output, no duplicate emails","idempotent",PURPLE),
           ("Someone else can run it","Documented inputs, credentials in the environment, an owner","handover note",MUTED)]
    for i,(title,detail,tag,c) in enumerate(items):
        x=30+(i%2)*540; y=76+(i//2)*98
        o.append(rect(x,y,510,80,fill="#fff",stroke=RULE,rx=7)); o.append(rect(x,y,8,80,fill=c))
        o.append(text(x+22,y+26,title,13,INK,"bold")); o.append(text(x+22,y+48,detail,11.5,MUTED))
        o.append(rect(x+22,y+58,len(tag)*7+18,18,fill=c,rx=9)); o.append(text(x+31,y+71,tag,10.5,"#fff","bold"))
    o.append(text(30,384,"A report people trust is one they can check: the numbers, the time it ran, and what it excluded.",11.8,MUTED))
    return svg(1090,400,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig20-1-automation-ladder.svg",ladder),("fig20-2-report-flow.svg",flow),("fig20-4-trustworthy.svg",trust)]:
        open(n,"w").write(f())
    print("ok")
