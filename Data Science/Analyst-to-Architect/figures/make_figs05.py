# Generates the SVG figures for Chapter 5. Run: python3 make_figs05.py
# Numbers come from the mini database (riverstone), the same runs as checks/ch05_check.py.
# Redrawn 28 Sep 2026 (visual findings V5.1-V5.4): every canvas is 720 px wide, so a font of s px
# prints at s x 493.2 / 720 = 0.685 s pt; the smallest text here is 12 px (8.2 pt). Rupee amounts of
# a lakh or more use Indian grouping (option pick 67.9).
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"
W_CANVAS = 720

def lakh(n) -> str:
    """Indian digit grouping for rupee amounts: 4335471 -> '43,35,471'."""
    n = str(n).replace(',', ''); i, _, d = n.partition('.')
    if len(i) <= 3: out = i
    else:
        head, tail = i[:-3], i[-3:]
        out = ','.join([head[max(0, k-2):k] for k in range(len(head), 0, -2)][::-1]) + ',' + tail
    return out + ('.' + d if d else '')

def rs(v): return "₹" + lakh(v)

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.4), y2-L*math.sin(a-0.4)); p2=(x2-L*math.cos(a+0.4), y2-L*math.sin(a+0.4))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def box(x,y,w,h,lines,fill="#fff",stroke=ACC,size=13,bold_first=False,lh=19,sw=1.5):
    o=[rect(x,y,w,h,fill=fill,stroke=stroke,sw=sw,rx=8)]
    ty=y+24
    for i,l in enumerate(lines):
        o.append(text(x+14,ty,l,size,INK,"bold" if (bold_first and i==0) else "normal")); ty+=lh
    return "".join(o)

# ---------- Figure 5.1: vague request to precise question ----------
def fig_precise():
    o=[]
    checks=[("Metric and definition","billed revenue (invoices raised)"),("Period and comparison","March 2026 vs February 2026"),
            ("Scope","all customers; tax left out"),("Decision it serves","what sales does in the first week of April"),
            ("Deadline and precision","by Wednesday; to the nearest ₹1,000")]
    CX=236; CW=468; y=16
    o.append(box(16,122,176,96,["The request","“Sales are down.","Find out why.”"],fill="#f3f5f8",stroke=GREY,size=14,bold_first=True,lh=24))
    o.append(arrow(196,170,CX-8,170,c=GREY))
    for i,(t,d) in enumerate(checks):
        o.append(rect(CX,y,CW,54,fill="#fff",stroke=ACC,sw=1.4,rx=8))
        o.append(f'<circle cx="{CX+22}" cy="{y+27}" r="13" fill="{ACC}"/>'); o.append(text(CX+22,y+32,str(i+1),13,"#fff","bold",anchor="middle"))
        o.append(text(CX+46,y+23,t,14,INK,"bold",family=HEAD)); o.append(text(CX+46,y+43,d,13,MUTED))
        y+=62
    o.append(arrow(CX+CW/2,y-4,CX+CW/2,y+22,c=ACC))
    qy=y+28
    o.append(box(16,qy,688,92,["The precise question",
                              "Why was billed revenue in March 2026 (₹31,800) 80.3% lower than in February",
                              "(" + rs(161700) + "), and is it a fall in demand or a matter of timing?"],
                 fill="#eaf2f8",stroke=ACC,size=14,bold_first=True,lh=24,sw=2))
    return svg(W_CANVAS,qy+92+16,"".join(o))

# ---------- Figure 5.2: hypothesis loop ----------
def fig_loop():
    import math
    o=[]; cx,cy,RX,RY=360,206,214,156
    steps=[("1 Question","precise, tied to a decision"),("2 Hypotheses","possible answers, written down"),("3 Data needed","what would prove each wrong"),
           ("4 Test","query, count, compare"),("5 Conclude","keep, reject, or refine"),("6 Act or ask","decide, or a sharper question")]
    cols=[ACC,PURPLE,ORANGE,GREEN,RED,GREY]
    BW,BH=212,58
    pts=[]
    for i in range(6):
        a=-math.pi/2+i*2*math.pi/6
        pts.append((cx+RX*math.cos(a), cy+RY*math.sin(a)))
    def clip(x1,y1,x2,y2,hw=BW/2+6,hh=BH/2+6):
        dx,dy=x2-x1,y2-y1
        t=min(hw/abs(dx) if dx else 1e9, hh/abs(dy) if dy else 1e9)
        return x1+dx*t, y1+dy*t
    for i in range(6):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%6]
        sx,sy=clip(x1,y1,x2,y2); ex,ey=clip(x2,y2,x1,y1)
        o.append(arrow(sx,sy,ex,ey,c=MUTED,sw=2))
    for i,((x,y),(t,d)) in enumerate(zip(pts,steps)):
        o.append(rect(x-BW/2,y-BH/2,BW,BH,fill="#fff",stroke=cols[i],sw=1.8,rx=10))
        o.append(text(x,y-5,t,14.5,cols[i],"bold",anchor="middle",family=HEAD)); o.append(text(x,y+16,d,12.5,MUTED,anchor="middle"))
    o.append(text(cx,cy-4,"Most loops end",14,INK,"bold",anchor="middle")); o.append(text(cx,cy+16,"with a better question",14,INK,"bold",anchor="middle"))
    notes=[("Write hypotheses before you look at the data,"," so the data can prove you wrong."),
           ("A rejected hypothesis is progress:"," it removes a branch of the issue tree."),
           ("Stop when the answer is good enough for the decision,"," not when it's perfect.")]
    ny=cy+RY+BH/2+34
    for a,b in notes:
        o.append(f'<text x="16" y="{ny}" font-size="13" fill="{INK}"><tspan font-weight="bold">{a}</tspan><tspan fill="{MUTED}">{b}</tspan></text>'); ny+=21
    return svg(W_CANVAS,ny,"".join(o))

# ---------- Figure 5.3: MECE, bad split vs good split (stacked) ----------
def fig_mece():
    o=[]
    def panel(y0,verdict,title,col,groups,notes,gap_name=None):
        # verdict in words and a symbol, so the meaning never depends on colour
        o.append(text(16,y0+20,verdict,16,col,"bold",family=HEAD))
        o.append(text(16+(118 if verdict.startswith("✗") else 84),y0+20,title,14,INK,"bold"))
        o.append(rect(255,y0+34,210,36,fill=INK,rx=8)); o.append(text(360,y0+57,"Riverstone's 8 customers",13,"#fff","bold",anchor="middle"))
        W=216; G=12; x0=16
        top=y0+96
        for i,(g,members) in enumerate(groups):
            x=x0+i*(W+G)
            o.append(path(f"M360,{y0+70} V{y0+84} H{x+W/2} V{top}",stroke=RULE,sw=1.5))
            h=36+len(members)*19
            o.append(rect(x,top,W,h,fill="#fff",stroke=col,sw=1.6,rx=8))
            o.append(text(x+12,top+22,g,13.5,INK,"bold"))
            for j,(m,flag) in enumerate(members):
                o.append(text(x+12,top+42+j*19,m+("  (twice)" if flag else ""),13,RED if flag else INK,"bold" if flag else "normal"))
        ny=top+36+max(len(m) for _,m in groups)*19+22
        if gap_name:
            o.append(rect(x0,ny-15,290,22,fill="#fff",stroke=RED,sw=1.4,rx=5,extra='stroke-dasharray="4 3"'))
            o.append(text(x0+10,ny+1,"In no group: "+gap_name,13,RED,"bold"))
            ny+=28
        for l in notes:
            o.append(text(16,ny,l,13,INK)); ny+=19
        return ny
    bad=[("Big (wholesale)",[("Coastal Foods",0),("Northgate",1)]),("In Mumbai",[("Sharma Hardware",0),("Metro Mart",1)]),("New in 2026",[("Green Leaf Hotels",0),("Metro Mart",1),("Sunrise Caterers",0),("Northgate",1),("Blue Bay Cafe",0)])]
    good=[("Retail",[("Sharma Hardware",0),("Patel Kitchenware",0),("Metro Mart",0)]),("Wholesale",[("Coastal Foods",0),("Northgate",0)]),("Hospitality",[("Green Leaf Hotels",0),("Sunrise Caterers",0),("Blue Bay Cafe",0)])]
    y=panel(10,"✗ Not MECE","split: big, in Mumbai, new in 2026",RED,bad,
            ["Overlaps: Metro Mart and Northgate appear twice. Gap: Patel Kitchenware is in no group.","Totals by group won't add up to the whole."],gap_name="Patel Kitchenware")
    o.append(path(f"M16,{y+4} H704",stroke=RULE,sw=1.2))
    y=panel(y+22,"✓ MECE","split: segment",GREEN,good,
            ["Every customer is in exactly one group: nothing is counted twice, nothing is left out.","Totals by group add up to the whole. Source: Mini database (Jan–Mar 2026)."])
    return svg(W_CANVAS,y+4,"".join(o))

# ---------- Figure 5.4: issue tree for March revenue ----------
def fig_tree():
    o=[]
    STATUS={"yes":(GREEN,"supported by the data"),"part":(ORANGE,"partly explains"),"no":(GREY,"can't be answered with this data"),"call":(PURPLE,"hypothesis to test outside the data")}
    def node(x,y,w,h,lines,stroke=ACC,fill="#fff",status=None):
        o.append(rect(x,y,w,h,fill=fill,stroke=stroke,sw=1.6,rx=8))
        ty=y+20
        for i,l in enumerate(lines):
            o.append(text(x+10,ty,l,12.5 if i else 13,INK if i==0 else MUTED,"bold" if i==0 else "normal")); ty+=17
        if status:
            c=STATUS[status[0]][0]
            pw=len(status[1])*8+20
            o.append(rect(x+w-pw-8,y+h-26,pw,20,fill=c,rx=10)); o.append(text(x+w-8-pw/2,y+h-11.5,status[1],12,"#fff","bold",anchor="middle"))
    RX,RW=10,166; L1X,L1W=202,196; L2X,L2W=430,280
    # level 2 positions first, so parents can be centred on their children
    L2=[("Which customers stopped?","Coastal, Sunrise, Northgate:","ordered Feb, not Mar",("yes","FOUND")),
        ("Why didn't they reorder?","all three have overdue","balances ("+rs(82510)+")",("call","TEST: CALL")),
        ("Mix: wholesale orders?","67.5% of Feb billed;","none placed in March",("yes","FOUND")),
        ("Pending order 5012","₹26,220 booked, not billed;","with it, March = ₹58,020",("part","TIMING")),
        ("Seasonal March dip?","needs March last year:","not in this data",("no","UNKNOWN"))]
    H2=88; G2=8; y2=[10+i*(H2+G2) for i in range(5)]
    for (a,b,c,st),y in zip(L2,y2): node(L2X,y,L2W,H2,[a,b,c],status=st)
    H1=96
    L1=[("Fewer invoiced orders?","5 in Feb → 2 in Mar","−₹97,020 of the fall",("yes","MAIN CAUSE"),[0,1]),
        ("Smaller orders?","avg ₹32,340 → ₹15,900","−₹32,880 of the fall",("yes","CONTRIBUTES"),[2]),
        ("Timing or season?","March not closed; one","order still Pending",("part","PARTLY"),[3,4])]
    y1=[]
    for a,b,c,st,kids in L1:
        cy=(y2[kids[0]]+y2[kids[-1]]+H2)/2; y=cy-H1/2; y1.append(y)
        node(L1X,y,L1W,H1,[a,b,c],status=st)
        for k in kids:
            o.append(path(f"M{L1X+L1W},{cy} H{L1X+L1W+16} V{y2[k]+H2/2} H{L2X}",stroke=RULE,sw=1.6))
    ry=y1[1]; RH=H1
    node(RX,ry,RW,RH,["Why did March","billed revenue","fall 80.3%?",rs(161700)+" → ₹31,800"],stroke=INK,fill="#eef2f6")
    for y in y1:
        o.append(path(f"M{RX+RW},{ry+RH/2} H{RX+RW+16} V{y+H1/2} H{L1X}",stroke=RULE,sw=1.6))
    # legend: the pill words already say the status; the legend explains them
    ly=y2[-1]+H2+26
    for k,(lx,dy) in zip(["yes","part","call","no"],[(10,0),(280,0),(10,22),(280,22)]):
        c,lab=STATUS[k]
        o.append(rect(lx,ly+dy-12,14,14,fill=c,rx=3)); o.append(text(lx+20,ly+dy,lab,12.5,INK))
    o.append(text(710,ly,"Source: Mini database (Jan–Mar 2026).",12,MUTED,anchor="end",style="italic"))
    ly+=22
    return svg(W_CANVAS,ly+12,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig5-1-vague-to-precise-question.svg",fig_precise),("fig5-3-mece-bad-and-good-splits.svg",fig_mece),
                    ("fig5-4-issue-tree-march-revenue.svg",fig_tree),("fig5-2-hypothesis-loop.svg",fig_loop)]:
        open(name,"w").write(fn())
    print("ok")
