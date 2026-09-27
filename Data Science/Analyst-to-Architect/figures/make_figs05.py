# Generates the SVG figures for Chapter 5. Run: python3 make_figs05.py
# Numbers come from the mini database (riverstone), the same runs as checks/ch05_check.py.
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.4), y2-L*math.sin(a-0.4)); p2=(x2-L*math.cos(a+0.4), y2-L*math.sin(a+0.4))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def box(x,y,w,h,lines,fill="#fff",stroke=ACC,size=12.5,bold_first=False,lh=18,sw=1.5):
    o=[rect(x,y,w,h,fill=fill,stroke=stroke,sw=sw,rx=8)]
    ty=y+22
    for i,l in enumerate(lines):
        o.append(text(x+12,ty,l,size,INK,"bold" if (bold_first and i==0) else "normal")); ty+=lh
    return "".join(o)

# ---------- Figure 5.1: vague request to precise question ----------
def fig_precise():
    o=[]
    o.append(box(30,120,220,110,["The request","“Sales are down.","Find out why.”"],fill="#f3f5f8",stroke=GREY,size=14,bold_first=True,lh=24))
    checks=[("Metric and definition","billed revenue (invoices raised)"),("Period and comparison","March 2026 vs February 2026"),
            ("Scope","all customers; tax left out"),("Decision it serves","what sales does in the first week of April"),
            ("Deadline and precision","by Wednesday; to the nearest ₹1,000")]
    y=30
    for i,(t,d) in enumerate(checks):
        o.append(rect(320,y,330,54,fill="#fff",stroke=ACC,sw=1.4,rx=8))
        o.append(f'<circle cx="342" cy="{y+27}" r="12" fill="{ACC}"/>'); o.append(text(342,y+32,str(i+1),12.5,"#fff","bold",anchor="middle"))
        o.append(text(364,y+23,t,13,INK,"bold",family=HEAD)); o.append(text(364,y+42,d,12,MUTED))
        y+=62
    o.append(arrow(252,175,312,175,c=GREY))
    o.append(arrow(656,175,714,175,c=ACC))
    o.append(box(720,70,300,210,["The precise question","Why was billed revenue in","March 2026 (₹31,800) 80.3%","lower than in February","(₹161,700), and is it a fall","in demand or a matter of timing?"],fill="#eaf2f8",stroke=ACC,size=13.5,bold_first=True,lh=26,sw=2))
    return svg(1050,350,"".join(o))

# ---------- Figure 5.3: MECE, bad split vs good split ----------
def fig_mece():
    o=[]
    def panel(x0,title,col,groups,note_lines,ok):
        o.append(text(x0,30,title,15,INK,"bold",family=HEAD))
        o.append(rect(x0+150,48,190,40,fill=INK,rx=8)); o.append(text(x0+245,73,"Riverstone's 8 customers",12.5,"#fff","bold",anchor="middle"))
        gx=x0; W=150; G=15
        for i,(g,members) in enumerate(groups):
            x=gx+i*(W+G)
            o.append(path(f"M{x0+245},88 V110 H{x+W/2} V124",stroke=RULE,sw=1.5))
            h=40+len(members)*19
            o.append(rect(x,124,W,h,fill="#fff",stroke=col,sw=1.6,rx=8))
            o.append(text(x+10,146,g,12.5,INK,"bold"))
            for j,(m,flag) in enumerate(members):
                c = RED if flag else INK
                o.append(text(x+10,168+j*19,m,11.5,c,"bold" if flag else "normal"))
        ny=300
        for l in note_lines:
            o.append(text(x0,ny,l,12.5,RED if not ok else GREEN,"bold" if l==note_lines[0] else "normal")); ny+=20
    bad=[("Big (wholesale)",[("Coastal Foods",0),("Northgate",1)]),("In Mumbai",[("Sharma Hardware",0),("Metro Mart",1)]),("New in 2026",[("Green Leaf Hotels",0),("Metro Mart",1),("Sunrise Caterers",0),("Northgate",1),("Blue Bay Cafe",0)])]
    good=[("Retail",[("Sharma Hardware",0),("Patel Kitchenware",0),("Metro Mart",0)]),("Wholesale",[("Coastal Foods",0),("Northgate",0)]),("Hospitality",[("Green Leaf Hotels",0),("Sunrise Caterers",0),("Blue Bay Cafe",0)])]
    panel(30,"Not MECE",RED,bad,["Overlaps: Metro Mart and Northgate appear twice.","Gap: Patel Kitchenware is in no group.","Totals by group won't add up to the whole."],False)
    panel(555,"MECE",GREEN,good,["Every customer is in exactly one group.","Nothing is counted twice; nothing is left out.","Totals by group add up to the whole."],True)
    return svg(1070,370,"".join(o))

# ---------- Figure 5.4: issue tree for March revenue ----------
def fig_tree():
    o=[]
    def node(x,y,w,h,lines,stroke=ACC,fill="#fff",status=None):
        o.append(rect(x,y,w,h,fill=fill,stroke=stroke,sw=1.6,rx=8))
        ty=y+20
        for i,l in enumerate(lines):
            o.append(text(x+10,ty,l,12 if i else 12.5,INK if i==0 else MUTED,"bold" if i==0 else "normal")); ty+=17
        if status:
            c={"yes":GREEN,"part":ORANGE,"no":GREY,"call":PURPLE}[status[0]]
            o.append(rect(x+w-104,y+h-24,96,18,fill=c,rx=9)); o.append(text(x+w-56,y+h-11,status[1],10.5,"#fff","bold",anchor="middle"))
    node(20,190,210,92,["Why did March billed","revenue fall 80.3%?","₹161,700 → ₹31,800"],stroke=INK,fill="#eef2f6")
    # level 1
    L1=[(300,40,"Fewer invoiced orders?","5 in Feb → 2 in Mar","−₹97,020 of the fall",("yes","MAIN CAUSE")),
        (300,190,"Smaller orders?","avg ₹32,340 → ₹15,900","−₹32,880 of the fall",("yes","CONTRIBUTES")),
        (300,340,"Timing or season?","March not closed; one","order still Pending",("part","PARTLY"))]
    for x,y,a,b,c,st in L1:
        node(x,y,250,92,[a,b,c],status=st)
        o.append(path(f"M230,236 H265 V{y+46} H300",stroke=RULE,sw=1.6))
    # level 2
    L2=[(620,10,"Which customers stopped?","Coastal, Sunrise, Northgate:","ordered Feb, not Mar",("yes","FOUND")),
        (620,110,"Why didn't they reorder?","all three have overdue","balances (₹82,510)",("call","TEST: CALL")),
        (620,210,"Mix: wholesale orders?","67.5% of Feb billed;","none placed in March",("yes","FOUND")),
        (620,310,"Pending order 5012","₹26,220 booked, not billed;","with it, March = ₹58,020",("part","TIMING")),
        (620,410,"Seasonal March dip?","needs March last year:","not in this data",("no","UNKNOWN"))]
    links=[(0,0),(0,1),(1,2),(2,3),(2,4)]
    for i,(x,y,a,b,c,st) in enumerate(L2):
        node(x,y,270,80,[a,b,c],status=st)
    for p,cidx in links:
        py=L1[p][1]+46; cy=L2[cidx][1]+40
        o.append(path(f"M550,{py} H585 V{cy} H620",stroke=RULE,sw=1.6))
    # legend
    ly=510
    for c,lab in [(GREEN,"supported by the data"),(ORANGE,"partly explains"),(PURPLE,"hypothesis to test outside the data"),(GREY,"can't be answered with this data")]:
        o.append(rect(20,ly-11,14,14,fill=c,rx=3)); o.append(text(40,ly,lab,12,INK)); ly+=20
    return svg(910,590,"".join(o))

# ---------- Figure 5.2: hypothesis loop ----------
def fig_loop():
    import math
    o=[]; cx,cy,RX,RY=320,250,235,185
    steps=[("1 Question","precise, tied to a decision"),("2 Hypotheses","possible answers, written down"),("3 Data needed","what would prove each wrong"),
           ("4 Test","query, count, compare"),("5 Conclude","keep, reject, or refine"),("6 Act or ask","decide, or a sharper question")]
    cols=[ACC,PURPLE,ORANGE,GREEN,RED,GREY]
    pts=[]
    for i in range(6):
        a=-math.pi/2+i*2*math.pi/6
        pts.append((cx+RX*math.cos(a), cy+RY*math.sin(a)))
    def clip(x1,y1,x2,y2,hw=114,hh=36):
        dx,dy=x2-x1,y2-y1
        t=min(hw/abs(dx) if dx else 1e9, hh/abs(dy) if dy else 1e9)
        return x1+dx*t, y1+dy*t
    for i in range(6):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%6]
        sx,sy=clip(x1,y1,x2,y2); ex,ey=clip(x2,y2,x1,y1)
        o.append(arrow(sx,sy,ex,ey,c=MUTED,sw=2))
    for i,((x,y),(t,d)) in enumerate(zip(pts,steps)):
        o.append(rect(x-108,y-30,216,60,fill="#fff",stroke=cols[i],sw=1.8,rx=10))
        o.append(text(x,y-6,t,13.5,cols[i],"bold",anchor="middle",family=HEAD)); o.append(text(x,y+14,d,11.5,MUTED,anchor="middle"))
    o.append(text(cx,cy-4,"Most loops end",13,INK,"bold",anchor="middle")); o.append(text(cx,cy+15,"with a better question",13,INK,"bold",anchor="middle"))
    notes=["Write hypotheses before you look at the data,","so the data can prove you wrong.","","A rejected hypothesis is progress:","it removes a branch of the issue tree.","","Stop when the answer is good enough","for the decision, not when it's perfect."]
    ny=150
    for l in notes:
        o.append(text(690,ny,l,13.5,INK if l and not l.startswith(("so","it","for")) else MUTED)); ny+=24
    return svg(1060,500,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig5-1-vague-to-precise-question.svg",fig_precise),("fig5-3-mece-bad-and-good-splits.svg",fig_mece),
                    ("fig5-4-issue-tree-march-revenue.svg",fig_tree),("fig5-2-hypothesis-loop.svg",fig_loop)]:
        open(name,"w").write(fn())
    print("ok")
