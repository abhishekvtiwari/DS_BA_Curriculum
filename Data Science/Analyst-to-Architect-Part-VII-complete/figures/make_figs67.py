# Diagrams for Chapter 67. Run: python3 make_figs67.py
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

def f1():  # technical excellence -> leverage
    o=[text(30,30,"The shift every architect eventually makes",14.5,INK,"bold",family=HEAD)]
    o.append(box(50,70,380,190,"Individual contribution",MUTED,
               ["Impact = what you personally","build, this week","","Scales with your own hours","","The skill: write the best","query, the cleanest pipeline"],10.4))
    o.append(box(570,70,380,190,"Leverage",ACC,
               ["Impact = the decisions you make","and the people you enable","","Scales with judgment and trust","","The skill: make the right call,","and get others to build it well"],10.4))
    o.append(arrow(432,165,568,165,GOLD,2.2))
    o.append(text(450,150,"the shift",11,GOLD,"bold"))
    o.append(text(30,300,"Neither replaces the other — an architect who can't write the query anymore has lost the credibility that judgment rests on.",11.3,MUTED))
    o.append(text(30,318,"The shift is where your TIME goes, not whether the underlying skill still matters.",11.3,MUTED))
    return svg(1000,338,"".join(o))

def f2():  # first 90 days
    o=[text(30,30,"A first-90-days plan for a new architect",14.5,INK,"bold",family=HEAD)]
    phases=[("Weeks 1-4","Listen",ACC,["Read every design doc,","ADR, and postmortem that","already exists","","Ask \"what keeps you up","at night?\" of every team lead","","Build nothing yet"]),
           ("Weeks 5-8","Diagnose",GREEN,["Draw the real C4 diagram","(Ch 60) — not the one in","the wiki","","Run a failure analysis","(Ch 61) on the riskiest","system","","Score maturity honestly","(Ch 66)"]),
           ("Weeks 9-12","Earn credibility",GOLD,["Ship one small, visible,","real fix — not a redesign","","Close one long-open risk","(the way Ch 64 closed","Ch 60's access-control gap)","","Write it up; let the work","speak first"])]
    for i,(wk,name,c,lines) in enumerate(phases):
        x=30+i*320
        o.append(box(x,64,290,230,f"{wk}: {name}",c,lines,9.8))
        if i<2: o.append(arrow(x+292,179,x+318,179))
    o.append(text(30,320,"Notice what's missing from the first 90 days: a grand redesign. Chapter 60's own story already taught this lesson —",11.3,MUTED))
    o.append(text(30,338,"the instinct to rebuild everything after finally seeing it clearly is almost always premature, especially in week six.",11.3,MUTED))
    return svg(970,358,"".join(o))

def f3():  # the arc of the book
    o=[text(30,30,"The arc of this book, in one line",14.5,INK,"bold",family=HEAD)]
    milestones=[("Part I","Ch 1","One query\nagainst one table",MUTED),
               ("Part II","Ch 20","One automation\nsomeone relies on",ACC),
               ("Part V-VI","Ch 46-58","A pipeline and a model\nin production",GREEN),
               ("Part VII","Ch 60-61","A whole platform,\ndesigned and stress-tested",GOLD),
               ("Part VII","Ch 63-66","Governed, secured,\ncosted, and led",PURPLE),
               ("Now","Ch 67","Someone else's turn\nto learn from you",RED)]
    x0=60; gap=155
    o.append(path(f"M{x0},200 H{x0+5*gap}",stroke=LIGHT,sw=2))
    for i,(part,ch,label,c) in enumerate(milestones):
        x=x0+i*gap
        o.append(f'<circle cx="{x}" cy="200" r="9" fill="{c}"/>')
        o.append(text(x,178,part,9.6,MUTED,"bold",anchor="middle"))
        o.append(text(x,192,ch,9.2,c,"bold",anchor="middle"))
        for j,l in enumerate(label.split("\n")):
            o.append(text(x,224+j*14,l,9.6,INK,anchor="middle"))
    o.append(text(30,280,"Every layer was necessary. None of it, on its own, was sufficient. This last chapter is the one that makes the rest of it matter.",11.5,MUTED,"italic"))
    return svg(1020,300,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig67-1-leverage-shift.svg",f1),("fig67-2-first-90-days.svg",f2),
                ("fig67-3-book-arc.svg",f3)]:
        open(n,"w").write(f())
    print("ok")
