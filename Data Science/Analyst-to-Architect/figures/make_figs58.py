# Generates the SVG figures for Chapter 58. Run: python3 make_figs58.py
# Every number was measured by the chapter's own pipeline (companion/ch58).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_pipeline():
    o=[text(30,32,"Riverstone's purchase-order intake, end to end",14,INK,"bold",family=HEAD)]
    boxes=[(30,"email","40 a day,\nfive shapes",RULE),(200,"extract","pinned model,\nprompt v3",ACC),
           (370,"parse","fences, comments,\nnormalized dates",ACC),(540,"validate","PO shape, real codes,\nplausible dates",PURPLE),
           (710,"decide","under the limit?",ORANGE),(880,"write","one transaction,\naudited",GREEN)]
    for x,title,detail,c in boxes:
        o.append(rect(x,70,150,78,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+75,96,title,12.5,c,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+75,118+i*15,line,10.5,MUTED,anchor="middle"))
        if x<880:
            o.append(path(f"M{x+150},109 H{x+196}",stroke=INK,sw=1.8)); o.append(path(f"M{x+188},103 L{x+198},109 L{x+188},115",stroke=INK,sw=1.8))
    o.append(rect(880,170,150,44,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=7))
    o.append(text(955,190,"loaded: 53",12,GREEN,"bold",anchor="middle")); o.append(text(955,207,"88% of emails",11,INK,anchor="middle"))
    o.append(path("M785,148 V196 H650 V196",stroke=ORANGE,sw=1.8,dash="5,4"))
    o.append(rect(420,174,220,44,fill="#fdf3dc",stroke=ORANGE,sw=1.6,rx=7))
    o.append(text(530,194,"awaiting approval: 6",12,ORANGE,"bold",anchor="middle")); o.append(text(530,211,"over Rs 100,000",11,INK,anchor="middle"))
    o.append(path("M615,148 V174",stroke=RED,sw=1.8,dash="5,4"))
    o.append(rect(170,174,220,44,fill="#fbeaea",stroke=RED,sw=1.6,rx=7))
    o.append(text(280,194,"held for review: 1",12,RED,"bold",anchor="middle")); o.append(text(280,211,"validation failed",11,INK,anchor="middle"))
    o.append(rect(30,240,1000,62,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(48,262,"The write is the part that is different: a UNIQUE key on the source email, one transaction for the header and its lines,",12,INK))
    o.append(text(48,284,"and an audit row naming the pipeline version. Replaying the whole morning wrote nothing twice.",12,GREEN,"bold"))
    return svg(1060,322,"".join(o))

def fig_two_rates():
    o=[text(30,32,"The same system, described two ways",14,INK,"bold",family=HEAD)]
    o.append(rect(40,70,470,190,fill="#e2f3ee",stroke=GREEN,sw=1.8,rx=8))
    o.append(text(275,100,"what the business case says",12.5,GREEN,"bold",anchor="middle"))
    o.append(text(275,148,"88%",34,GREEN,"bold",anchor="middle"))
    o.append(text(275,176,"straight-through rate",12.5,INK,anchor="middle"))
    o.append(text(275,204,"53 of 60 emails loaded",11.5,MUTED,anchor="middle"))
    o.append(text(275,224,"without anyone touching them",11.5,MUTED,anchor="middle"))
    o.append(rect(550,70,470,190,fill="#fbeaea",stroke=RED,sw=1.8,rx=8))
    o.append(text(785,100,"what the ground truth says",12.5,RED,"bold",anchor="middle"))
    o.append(text(785,148,"19%",34,RED,"bold",anchor="middle"))
    o.append(text(785,176,"silent error rate",12.5,INK,anchor="middle"))
    o.append(text(785,204,"10 of those 53 orders are wrong:",11.5,MUTED,anchor="middle"))
    o.append(text(785,224,"a quantity, a date, a missing line",11.5,MUTED,anchor="middle"))
    rows=[("manual (today)",120,600,0,0,600,MUTED),
          ("assisted: review each draft",40,198,0,0,198,GREEN),
          ("straight through",9,47,6.7,13333,13380,RED)]
    y=300
    o.append(text(30,y-14,"Cost per day at 40 emails, counting labour AND the cost of being wrong",12.5,INK,"bold"))
    o.append(text(300,y+14,"minutes",11.5,MUTED,anchor="end")); o.append(text(430,y+14,"labour Rs",11.5,MUTED,anchor="end"))
    o.append(text(570,y+14,"errors/day",11.5,MUTED,anchor="end")); o.append(text(720,y+14,"error cost Rs",11.5,MUTED,anchor="end"))
    o.append(text(860,y+14,"total Rs/day",11.5,MUTED,anchor="end"))
    y+=26
    for label,minutes,labour,errors,error_cost,total,c in rows:
        o.append(rect(30,y,1000,34,fill="#fff",stroke=c,sw=1.6,rx=6))
        o.append(text(48,y+22,label,12,c,"bold"))
        o.append(text(300,y+22,f"{minutes}",12,INK,anchor="end")); o.append(text(430,y+22,f"{labour}",12,INK,anchor="end"))
        o.append(text(570,y+22,f"{errors:.1f}",12,INK,anchor="end")); o.append(text(720,y+22,f"{error_cost:,}",12,INK,anchor="end"))
        o.append(text(860,y+22,f"{total:,}",12.5,c,"bold",anchor="end"))
        y+=42
    o.append(text(30,y+18,"Straight through saves the most labour and costs the most money. The recommendation this chapter's own numbers force is the",12,MUTED))
    o.append(text(30,y+38,"middle row: the model drafts every order, a person confirms it in 45 seconds, and nothing reaches the ERP unseen.",12,INK,"bold"))
    return svg(1060,y+60,"".join(o))

def fig_segments():
    o=[text(30,32,"Automate the segment you are excellent at, not everything you are mediocre at",14,INK,"bold",family=HEAD)]
    rows=[("bulleted",13,0),("forwarded",14,0),("terse",10,0),("table",7,4),("prose",3,8)]
    y=80
    for name,right,wrong in rows:
        total=right+wrong
        o.append(text(150,y+20,name,12.5,INK,"bold",anchor="end"))
        o.append(rect(170,y,600*total/14,32,fill=GREEN if not wrong else "#f6f9fc",stroke=GREEN if not wrong else RULE,rx=5))
        if wrong:
            o.append(rect(170+600*right/14,y,600*wrong/14,32,fill=RED,stroke=RED,rx=5))
            o.append(rect(170,y,600*right/14,32,fill=GREEN,stroke=GREEN,rx=5))
        o.append(text(790,y+21,f"{right} correct, {wrong} wrong",12,INK))
        o.append(text(1010,y+21,"automate" if not wrong else "review",12,GREEN if not wrong else RED,"bold",anchor="end"))
        y+=44
    o.append(rect(170,y+10,600,54,fill="#e2f3ee",stroke=GREEN,rx=7))
    o.append(text(470,y+32,"37 of 37 correct across three styles",12.5,GREEN,"bold",anchor="middle"))
    o.append(text(470,y+52,"62% of the volume, at 100% accuracy, automatic today",12,INK,anchor="middle"))
    o.append(text(30,y+96,"Nobody would have guessed this split: prose is hard, as expected, and tables are the second worst, because several items on one",12,MUTED))
    o.append(text(30,y+116,"row are exactly what the extraction misses. You find the segment by measuring it, not by looking at the emails.",12,INK))
    return svg(1060,y+138,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig58-1-intake-pipeline.svg",fig_pipeline),("fig58-2-two-rates.svg",fig_two_rates),
                    ("fig58-3-segments.svg",fig_segments)]:
        open(name,"w").write(fn())
    print("ok58")
