# Diagrams for Chapter 24. Run from this folder: python3 make_figs24.py
# Every canvas is 680 px wide and prints at 174 mm (493.2 pt), so 1 px prints at 0.725 pt:
# the smallest text here (10 px) prints at 7.3 pt.
# Figure 24.3's numbers come from companion/ch24/build_ch24_files.py (dec_dip), which computes
# them from the full Riverstone order data; nothing in it is typed by hand.
import math, pathlib, sys
from make_figs import *

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "companion" / "ch24"))

GREEN="#2f7d6d"; PURPLE="#7a4fa0"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"
W = 680
MINUS = "−"

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def lines(x,y,rows,size,fill,step,weight="normal",anchor="start"):
    return "".join(text(x,y+i*step,r,size,fill,weight,anchor) for i,r in enumerate(rows))


# Figure 24.1: power-interest grid. Each person sits in the quadrant section 24.3 and 24.9 give them.
def f1():
    o=[]
    gx,gy,gw,gh=46,8,620,330
    o.append(rect(gx,gy,gw,gh,fill="#fff",stroke=RULE,sw=1.4))
    o.append(path(f"M{gx+gw/2},{gy} V{gy+gh}",stroke=RULE,sw=1)); o.append(path(f"M{gx},{gy+gh/2} H{gx+gw}",stroke=RULE,sw=1))
    q=[("Keep satisfied","high power, low interest",gx+gw*0.25,gy+22),
       ("Manage closely","high power, high interest",gx+gw*0.75,gy+22),
       ("Monitor","low power, low interest",gx+gw*0.25,gy+gh-26),
       ("Keep informed","low power, high interest",gx+gw*0.75,gy+gh-26)]
    for t,sub,x,y in q:
        o.append(text(x,y,t,12,INK,"bold",anchor="middle")); o.append(text(x,y+15,sub,10.5,MUTED,anchor="middle"))
    # one axis title per axis, each clear of everything else
    cy=gy+gh/2
    o.append(f'<g transform="rotate(-90 20 {cy})">{text(20,cy+4,"POWER →",11.5,MUTED,"bold",anchor="middle")}</g>')
    o.append(text(gx+gw/2,gy+gh+20,"INTEREST →",11.5,MUTED,"bold",anchor="middle"))
    # (interest 0-1, power 0-1): upper half = high power, right half = high interest
    people=[("Vikram Singh","Sales Manager (asked)",0.60,0.73,ACC),
            ("Anita Rao","Sales Head (decides)",0.74,0.60,ACC),
            ("Board / owning family","",0.07,0.74,GOLD),
            ("Suresh Menon","Finance Manager",0.18,0.61,GOLD),
            ("Regional Sales Managers","",0.60,0.33,GREEN),
            ("Branch staff","",0.07,0.36,MUTED),
            ("IT / ERP team","",0.24,0.27,MUTED)]
    for name,role,ix,py,c in people:
        x=gx+gw*ix; y=gy+gh*(1-py)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c}"/>')
        o.append(text(x+9,y+4,name,11,INK,"bold"))
        if role: o.append(text(x+9,y+18,role,10.5,MUTED))
    o.append(text(10,gy+gh+44,"Manage closely: involve them in the question and show drafts.   Keep satisfied: brief them once, on their terms.",10.5,MUTED))
    o.append(text(10,gy+gh+60,"Keep informed: share the finding once it's solid; don't ask for their time.   Monitor: answer if asked.",10.5,MUTED))
    return svg(W,gy+gh+70,"".join(o))


# Figure 24.2: how the December analysis was built (bottom-up) vs how it is told (an upright pyramid).
def f2():
    o=[]
    o.append(text(10,18,"How the analysis was built",12,MUTED,"bold"))
    o.append(text(10,33,"(in the order it was done)",10.5,MUTED))
    steps=["1  Pulled Nov and Dec order data","2  Customers, orders per customer, AOV","3  Ran the chain-linked decomposition",
           "4  Checked the segment mix","5  Compared with the May \u2192 June dip","6  Concluded: seasonal, no action"]
    for i,s in enumerate(steps):
        y=44+i*34
        last=i==len(steps)-1
        o.append(rect(10,y,240,26,fill=SOFT if last else "#fff",stroke=ACC if last else RULE,sw=1.4 if last else 1,rx=4))
        o.append(text(20,y+17,s,10.5,INK,"bold" if last else "normal"))
        if not last: o.append(arrow(130,y+26,130,y+34,MUTED,1.2))
    o.append(text(130,44+6*34+10,"the answer arrives last",10.5,RED,"bold",anchor="middle"))
    o.append(arrow(258,150,286,150,ACC,2))
    # right: upright pyramid, answer at the apex; the text sits beside each tier, so nothing clips
    o.append(text(296,18,"How it's told to Vikram Singh",12,MUTED,"bold"))
    o.append(text(296,33,"(top-down: the answer first)",10.5,MUTED))
    px,top,base,th=384,46,104,62      # apex x, apex y, half-width of the base, tier height
    tiers=[("Answer",["December's fall is","seasonal. No action","needed."],ACC,"#fff"),
           ("Reasons",["AOV drove two-thirds of it;","the mix didn't shift; same","shape as May \u2192 June."],GREEN,"#fff"),
           ("Detail",["The decomposition, the","segment table, the appendix."],LIGHT,INK)]
    hw=lambda y: base*(y-top)/(3*th)
    for i,(lab,rows,c,fc) in enumerate(tiers):
        y0=top+i*th; y1=y0+th
        o.append(f'<polygon points="{px-hw(y0):.1f},{y0} {px+hw(y0):.1f},{y0} {px+hw(y1):.1f},{y1} {px-hw(y1):.1f},{y1}" fill="{c}" stroke="#fff" stroke-width="2"/>')
        o.append(text(px,y1-10,lab,10,fc,"bold",anchor="middle"))
        tx=px+base+14; ym=(y0+y1)/2
        o.append(path(f"M{px+hw(ym)+4:.1f},{ym:.1f} H{tx-4}",stroke=RULE,sw=1))
        o.append(lines(tx,ym-(len(rows)-1)*7.5+4,rows,10.5,INK,15,"bold" if i==0 else "normal"))
    o.append(text(296,top+3*th+22,"A reader who stops after the top tier still has the answer.",10.5,MUTED))
    return svg(W,top+3*th+32,"".join(o))


# Figure 24.3: one message per slide. The waterfall uses the computed December numbers.
def f3():
    from build_ch24_files import dec_dip, cr
    n=dec_dip(); b=n["bridge"]; nov=n["nov"]["revenue"]; dec=n["dec"]["revenue"]
    ss=lambda k,s: n[k]["segment_share"][s]
    o=[]
    sw_,sh=325,300
    # before
    o.append(rect(10,8,sw_,sh,fill="#fff",stroke=RED,sw=1.6,rx=6)); o.append(rect(10,8,sw_,24,fill=RED,rx=0))
    o.append(text(20,25,"BEFORE",11,"#fff","bold")); o.append(text(88,25,"Slide title: “December Sales Review”",10.5,"#fff"))
    rows=[f"• Nov revenue ₹{cr(nov)} cr, Dec ₹{cr(dec)} cr ({MINUS}{abs(n['pct']):.1f}%)",
          f"• Customer effect {MINUS}₹{cr(b['customer'])} cr",
          f"• Orders/customer effect {MINUS}₹{cr(b['frequency'])} cr",
          f"• AOV effect {MINUS}₹{cr(b['aov'])} cr",
          f"• Retail share {ss('nov','Retail'):.1f}% → {ss('dec','Retail'):.1f}%",
          f"• Wholesale share {ss('nov','Wholesale'):.1f}% → {ss('dec','Wholesale'):.1f}%",
          f"• Hospitality share {ss('nov','Hospitality'):.1f}% → {ss('dec','Hospitality'):.1f}%",
          f"• Compare with May → June ({MINUS}{abs(n['pct_may_jun']):.1f}%)",
          "• Same pattern both times","• Recommend: review Jan actuals"]
    o.append(lines(22,54,rows,10.5,INK,22))
    o.append(text(22,sh-2,"→ the reader has to find the point",10.5,RED,"bold"))
    # after
    x0=345
    o.append(rect(x0,8,sw_,sh,fill="#fff",stroke=GREEN,sw=1.6,rx=6)); o.append(rect(x0,8,sw_,24,fill=GREEN))
    o.append(text(x0+10,25,"AFTER",11,"#fff","bold")); o.append(text(x0+62,25,"Slide title states the finding",10.5,"#fff"))
    o.append(text(x0+12,52,"December's dip is seasonal, not a problem",11.5,INK,"bold"))
    o.append(text(x0+12,74,f"₹{cr(dec)} crore, {abs(n['pct']):.0f}% below November",13,INK,"bold"))
    o.append(text(x0+12,91,"Led by smaller orders; the segment mix didn't shift.",10.5,MUTED))
    # waterfall: November, three effects (floating), December; values above, labels below the axis
    base_y,top_y=250,112; k=(base_y-top_y)/nov
    bars=[("Nov",0,nov,ACC,f"{cr(nov)}"),
          ("customers",nov+b["customer"],nov,RED,f"{MINUS}{cr(b['customer'])}"),
          ("orders/cust",nov+b["customer"]+b["frequency"],nov+b["customer"],RED,f"{MINUS}{cr(b['frequency'])}"),
          ("AOV",dec,nov+b["customer"]+b["frequency"],RED,f"{MINUS}{cr(b['aov'])}"),
          ("Dec",0,dec,ACC,f"{cr(dec)}")]
    bw,gap=44,17; bx=x0+22
    for i,(lab,lo,hi,c,val) in enumerate(bars):
        x=bx+i*(bw+gap); y_hi=base_y-hi*k; y_lo=base_y-lo*k
        o.append(rect(x,y_hi,bw,y_lo-y_hi,fill=c))
        o.append(text(x+bw/2,y_hi-4,val,10.5,INK,"bold",anchor="middle"))
        o.append(text(x+bw/2,base_y+14,lab,10,MUTED,anchor="middle"))
        if 0<i<len(bars)-1:
            pass
    o.append(path(f"M{bx-6},{base_y} H{bx+5*(bw+gap)-gap+6}",stroke=MUTED,sw=1))
    o.append(text(x0+12,base_y+30,"₹ crore",10,MUTED))
    o.append(text(x0+12,sh-2,"→ No action; re-check after January.",10.5,GREEN,"bold"))
    return svg(W,sh+16,"".join(o))


# Figure 24.4: "can you just change the number?" as a decision flow.
def f4():
    o=[]
    o.append(rect(10,8,250,48,fill="#fff",stroke=RULE,rx=6))
    o.append(text(22,28,"A stakeholder asks you to change",11,INK,"bold")); o.append(text(22,44,"a method, a filter, or a number",11,INK,"bold"))
    o.append(arrow(260,32,300,32,MUTED))
    o.append(rect(300,8,370,48,fill="#fff",stroke=GOLD,sw=1.6,rx=6))
    o.append(text(312,28,"You ask: “Help me understand why — is something",11,INK)); o.append(text(312,44,"wrong with the calculation, or should the comparison change?”",11,INK))
    o.append(text(10,82,"THE REASON TURNS OUT TO BE…",10.5,MUTED,"bold")); o.append(text(372,82,"SO YOU…",10.5,MUTED,"bold"))
    branches=[("1","A genuine error you missed","(wrong filter, wrong period)",GREEN,"Fix it and thank them;","re-check nearby numbers too"),
              ("2","A reasonable alternative definition,","argued on its merits",ACC,"Show both versions, let them","choose, document which and why"),
              ("3","“It doesn't look good”:","no methodological reason",RED,"Hold the number; offer to","explain the method in writing")]
    for i,(num,l1,l2,c,r1,r2) in enumerate(branches):
        y=94+i*62
        o.append(rect(10,y,340,50,fill="#fff",stroke=c,sw=1.6,rx=6)); o.append(rect(10,y,26,50,fill=c,rx=0))
        o.append(text(23,y+30,num,13,"#fff","bold",anchor="middle"))
        o.append(text(46,y+21,l1,11,INK)); o.append(text(46,y+37,l2,11,MUTED))
        o.append(arrow(350,y+25,372,y+25,c))
        o.append(rect(372,y,298,50,fill=c,rx=6))
        o.append(text(384,y+21,r1,11,"#fff","bold")); o.append(text(384,y+37,r2,11,"#fff"))
    y=94+3*62+10
    o.append(text(10,y,"The test is always the same: would you be comfortable explaining this change, and the reason for it,",10.5,MUTED))
    o.append(text(10,y+15,"to the person who first asked for the number?",10.5,MUTED))
    return svg(W,y+24,"".join(o))


if __name__ == "__main__":
    for n,f in [("fig24-1-stakeholder-grid.svg",f1),("fig24-2-pyramid-principle.svg",f2),
                ("fig24-3-one-message-per-slide.svg",f3),("fig24-4-handling-pushback.svg",f4)]:
        (HERE / n).write_text(f(), encoding="utf-8")
    print("ok")
