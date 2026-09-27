# Generates the SVG figures for Chapter 47. Run: python3 make_figs47.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_wap():
    o=[]; y=70
    o.append(header_card(30,y,280,150,ACC,"1 · Write"))
    o.append(wrap(44,y+62,["Build the day's numbers into","audit.daily_flash_new","","Nobody reads this table."],12.5,INK,20))
    o.append(arrow(314,y+75,354,y+75,c=INK,sw=2.2))
    o.append(header_card(358,y,300,150,ORANGE,"2 · Audit"))
    o.append(wrap(372,y+62,["one row per day","revenue not negative","matches the ERP (orders and","revenue recomputed from source)"],12.5,INK,20))
    o.append(arrow(662,y+45,706,y-5,c=GREEN,sw=2.2)); o.append(text(640,y-28,"tests pass",12,GREEN,"bold"))
    o.append(arrow(662,y+110,706,y+165,c=RED,sw=2.2)); o.append(text(636,y+206,"a test fails",12,RED,"bold"))
    o.append(header_card(710,y-70,300,120,GREEN,"3 · Publish"))
    o.append(wrap(724,y-14,["One transaction swaps the day into","mart.daily_flash, which dashboards","and analysts read."],12,INK,19))
    o.append(rect(710,y+130,300,120,fill="#fbeaea",stroke=RED,sw=1.6,rx=8))
    o.append(text(726,y+158,"Publish blocked",14,RED,"bold",family=HEAD))
    o.append(wrap(726,y+182,["mart.daily_flash keeps its last","good data; an incident alert goes","to the owner."],12,INK,19))
    o.append(rect(30,y+230,640,60,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,y+256,"Readers of the published table only ever see data that passed its tests.",13,INK,"bold"))
    o.append(text(46,y+276,"In Chapter 46 the same failure left a wrong row where anyone could query it.",12,MUTED))
    return svg(1040,y+320,"".join(o))

def fig_incident():
    o=[]
    steps=[("1 · Detect",ACC,["Failed test, freshness","alert, or a person saying","the number looks wrong"]),
           ("2 · Classify",ACC,["S1 wrong data reached","people or systems","S2 output late, nothing sent","S3 minor or warning-level"]),
           ("3 · Contain",ORANGE,["Stop publishing and syncs","Tell the people who use it,","before they find out"]),
           ("4 · Fix and verify",GREEN,["Repair the cause, re-run","the affected days, run the","same tests, publish"]),
           ("5 · Review",PURPLE,["Blameless write-up:","timeline, cause, impact,","and the checks added","to catch it sooner"])]
    W=186; G=16; y=40
    for i,(t,c,lines) in enumerate(steps):
        x=30+i*(W+G)
        o.append(header_card(x,y,W,170,c,t,tsize=13))
        o.append(wrap(x+12,y+62,lines,11.5,INK,19))
        if i<4: o.append(arrow(x+W+2,y+90,x+W+G-2,y+90,c=INK,sw=2))
    o.append(rect(30,y+192,5*W+4*G,58,fill="#fff4e8",stroke=ORANGE,rx=7))
    o.append(text(46,y+216,"People forgive late data far more than wrong data they already acted on.",13,INK,"bold"))
    o.append(text(46,y+238,"So communication happens at step 3, not after step 4.",12,MUTED))
    return svg(1040,y+276,"".join(o))

def fig_observability():
    o=[]
    qs=[("Did it run?",ACC,["Run success or failure","Duration vs usual","Runs that never started"],"Chapter 46: the orchestrator"),
        ("Is it fresh?",GREEN,["Age of the newest row","Limits from the promise","to users, not from habit"],"raw.dispatch: 102.5 h old, limit 48 h"),
        ("Does it look normal?",PURPLE,["Rows loaded vs history","Key totals vs a median","Zero rows on a working day"],"2025 median day: Rs 27,442.50")]
    W=310; G=26; y=40
    for i,(t,c,lines,foot) in enumerate(qs):
        x=30+i*(W+G)
        o.append(header_card(x,y,W,190,c,t))
        o.append(wrap(x+14,y+64,lines,12.5,INK,21))
        o.append(path(f"M{x+14},{y+140} H{x+W-14}",stroke=RULE,sw=1))
        o.append(wrap(x+14,y+164,[foot],12,c,18,"bold"))
    o.append(rect(30,y+212,3*W+2*G,74,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,y+238,"Tests ask whether the data is right. Observability asks whether the platform is behaving normally.",13,INK,"bold"))
    o.append(text(46,y+262,"Stale data is the most common incident and the least noticed: nothing fails, the numbers simply stop changing.",12,MUTED))
    return svg(1040,y+312,"".join(o))

def fig_lineage():
    o=[]
    def box(x,y,w,h,t,s,c,fill="#fff"):
        return (rect(x,y,w,h,fill=fill,stroke=c,sw=1.6,rx=7)+rect(x,y,6,h,fill=c,rx=3)
                +text(x+16,y+26,t,13,INK,"bold")+text(x+16,y+46,s,11.5,MUTED))
    o.append(text(30,34,"A broken source, and everything it touches",15,INK,"bold",family=HEAD))
    o.append(box(30,60,240,64,"raw_order_items","BROKEN: loaded 0 rows",RED,"#fbeaea"))
    o.append(box(30,150,240,64,"raw_orders","healthy",ACC))
    o.append(box(30,240,240,64,"raw_dispatch","contract breach",ORANGE,"#fff4e8"))
    o.append(box(30,330,240,64,"raw_crm_leads","healthy",ACC))
    o.append(box(400,60,240,64,"daily_flash","affected",RED,"#fbeaea"))
    o.append(box(400,240,240,64,"dispatch_report","affected",ORANGE,"#fff4e8"))
    o.append(box(400,330,240,64,"weekly_pipeline_report","healthy",ACC))
    o.append(box(760,60,250,64,"deliver_flash","blocked: not sent",RED,"#fbeaea"))
    o.append(arrow(274,92,396,92,c=RED,sw=2)); o.append(arrow(274,170,396,100,c=MUTED,sw=1.6))
    o.append(arrow(274,270,396,270,c=ORANGE,sw=2)); o.append(arrow(274,182,396,262,c=MUTED,sw=1.6))
    o.append(arrow(274,358,396,358,c=MUTED,sw=1.6)); o.append(arrow(274,196,396,346,c=MUTED,sw=1.6))
    o.append(arrow(644,92,756,92,c=RED,sw=2))
    o.append(rect(700,180,310,150,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(716,206,"What lineage answers",13.5,INK,"bold",family=HEAD))
    o.append(wrap(716,232,["Impact: who must be told, and which","reports to hold.","Cause: for a wrong number, which","upstream tables could explain it.","Here: sales managers, not the whole","company; the warehouse team, not sales."],11.5,INK,19))
    return svg(1040,420,"".join(o))

if __name__=="__main__":
    for n,f in [("fig47-1-write-audit-publish.svg",fig_wap),("fig47-2-data-incident-flow.svg",fig_incident),
                ("fig47-3-three-questions-to-monitor.svg",fig_observability),("fig47-4-lineage-impact.svg",fig_lineage)]:
        open(n,"w").write(f())
    print("ok")
