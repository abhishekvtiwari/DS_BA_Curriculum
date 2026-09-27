# Diagrams for Chapter 24. Run: python3 make_figs24.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def f1():  # power-interest stakeholder grid
    o=[text(30,30,"Stakeholder mapping: power vs. interest",14.5,INK,"bold",family=HEAD)]
    gx,gy,gw,gh=140,60,760,420
    o.append(rect(gx,gy,gw,gh,fill="#fff",stroke=RULE,sw=1.4))
    o.append(path(f"M{gx+gw/2},{gy} V{gy+gh}",stroke=RULE,sw=1)); o.append(path(f"M{gx},{gy+gh/2} H{gx+gw}",stroke=RULE,sw=1))
    labels=[("Keep satisfied","(high power, low interest)",gx+gw*0.25,gy+18,MUTED),
            ("Manage closely","(high power, high interest)",gx+gw*0.75,gy+18,INK),
            ("Monitor","(low power, low interest)",gx+gw*0.25,gy+gh-8,MUTED),
            ("Keep informed","(low power, high interest)",gx+gw*0.75,gy+gh-8,MUTED)]
    for t,sub,x,y,c in labels:
        o.append(text(x,y,t,11.5,c,"bold",anchor="middle")); o.append(text(x,y+15,sub,9.5,MUTED,anchor="middle"))
    o.append(text(gx-14,gy+gh/2,"POWER",11,MUTED,"bold",anchor="middle")); o.append(f'<g transform="rotate(-90 {gx-14} {gy+gh/2})">{text(gx-14,gy+gh/2,"POWER",11,MUTED,"bold",anchor="middle")}</g>')
    o.append(text(gx+gw/2,gy+gh+22,"INTEREST →",11,MUTED,"bold",anchor="middle"))
    people=[("Anita Rao\n(Sales Head)",0.82,0.90,ACC),("Vikram Singh\n(Sales Mgr)",0.68,0.80,ACC),
            ("Finance Controller",0.75,0.35,GOLD),("Regional Sales Managers",0.55,0.85,GREEN),
            ("Branch staff",0.30,0.55,MUTED),("IT / ERP team",0.60,0.20,PURPLE),
            ("Board / owning family",0.90,0.15,RED)]
    for name,ix,py,c in people:
        x=gx+gw*ix; y=gy+gh*(1-py)
        o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>')
        for i,l in enumerate(name.split("\n")):
            o.append(text(x+9,y-4+i*12,l,9.8,INK,"bold" if i==0 else None))
    o.append(text(30,504,"Manage closely = involve in requirements and review drafts. Keep informed = share findings, don't ask for time. Keep satisfied = brief them once, on their terms.",11,MUTED))
    return svg(940,522,"".join(o))

def f2():  # pyramid principle: bottom-up thinking vs top-down telling
    o=[text(30,30,"The pyramid principle: how you think is not how you tell it",14.5,INK,"bold",family=HEAD)]
    o.append(text(30,58,"How the analysis was built (bottom-up)",12.5,MUTED,"bold"))
    steps=["Pulled Nov & Dec order data","Computed customers, orders/cust, AOV","Ran the chain-linked decomposition","Checked segment mix for a confound","Compared with the May–June pattern","Concluded: seasonal, no action needed"]
    for i,s in enumerate(steps):
        y=80+i*30
        o.append(rect(30,y,300,24,fill="#fff",stroke=RULE,rx=4)); o.append(text(42,y+16,s,10.3,INK))
        if i<len(steps)-1: o.append(arrow(180,y+24,180,y+30-4,MUTED,1.2))
    o.append(arrow(345,190,395,190,ACC,2))
    o.append(text(430,58,"How it's told to Anita Rao (top-down)",12.5,MUTED,"bold"))
    tiers=[("December's fall is seasonal — no action needed",120,ACC),
           ("Because: AOV drove 66% of it, mix didn't shift, same pattern as June",170,GREEN),
           ("Detail: the decomposition, the segment table, the appendix",220,LIGHT)]
    cx=680
    for i,(t,y,c) in enumerate(tiers):
        w=280-i*70
        o.append(f'<polygon points="{cx-w/2},{y+40} {cx+w/2},{y+40} {cx+w/2-25},{y} {cx-w/2+25},{y}" fill="{c}" stroke="{ACC}" stroke-width="1"/>')
        fontc = "#fff" if c in (ACC,GREEN) else INK
        o.append(text(cx,y+24,t,9.8 if i==2 else 10.6,fontc,"bold" if i==0 else None,anchor="middle"))
    o.append(text(430,290,"Say the answer first. The reasoning and the detail support it —",11,MUTED))
    o.append(text(430,306,"they don't have to be discovered in the order you found them.",11,MUTED))
    return svg(940,330,"".join(o))

def f3():  # one message per slide: before/after
    o=[text(30,30,"One message per slide",14.5,INK,"bold",family=HEAD)]
    o.append(rect(30,58,430,300,fill="#fff",stroke=RED,sw=1.6,rx=6)); o.append(rect(30,58,430,26,fill=RED))
    o.append(text(44,76,"Before: \"December Sales Review\"",11.5,"#fff","bold"))
    rows=["• Nov revenue ₹15.60 cr, Dec ₹8.73 cr (-44.1%)","• Customer effect -₹1.26 cr","• Orders/customer effect -₹1.06 cr",
          "• AOV effect -₹4.55 cr","• Retail share 50.5% → 52.0%","• Wholesale share 22.0% → 21.1%","• Hospitality share 27.5% → 26.8%",
          "• Compare with May→June (-40.4%)","• Same pattern both times","• Recommend: review Jan actuals"]
    for i,r in enumerate(rows): o.append(text(46,102+i*24,r,10,MUTED))
    o.append(text(46,102+10*24+6,"→ reader has to find the point",10.5,RED,"bold"))
    o.append(rect(480,58,430,300,fill="#fff",stroke=GREEN,sw=1.6,rx=6)); o.append(rect(480,58,430,26,fill=GREEN))
    o.append(text(494,76,"After: \"December's dip is seasonal, not a problem\"",10.8,"#fff","bold"))
    o.append(text(494,110,"December revenue: ₹8.73 cr",13.5,INK,"bold"))
    o.append(text(494,132,"44% below November — but AOV-led,",11.5,MUTED))
    o.append(text(494,150,"mix-stable, and matches June's pattern.",11.5,MUTED))
    o.append(rect(494,175,390,120,fill=SOFT,rx=6))
    o.append(text(510,196,"Nov ₹15.6cr → Dec ₹8.73cr",10.5,INK))
    for i,(lab,v) in enumerate([("customers","-1.26"),("freq.","-1.06"),("AOV","-4.55")]):
        x=520+i*120
        o.append(rect(x,215,90,60*(float(v.strip('-'))/4.55),fill=RED))
        o.append(text(x+45,280,lab,9.5,MUTED,anchor="middle")); o.append(text(x+45,210,v,9.5,RED,"bold",anchor="middle"))
    o.append(text(494,320,"→ recommendation: no action; re-check after January",10.8,GREEN,"bold"))
    return svg(940,378,"".join(o))

def f4():  # handling pushback decision flow
    o=[text(30,30,"\"Can you just change the number?\" — a decision flow",14.5,INK,"bold",family=HEAD)]
    o.append(rect(30,60,260,70,fill="#fff",stroke=RULE,rx=6)); o.append(text(48,85,"A stakeholder asks you to",11.5,INK,"bold")); o.append(text(48,105,"change a method, filter, or number",11.5,INK,"bold"))
    o.append(arrow(160,130,160,158,MUTED))
    o.append(rect(60,160,200,60,fill="#fff",stroke=GOLD,sw=1.6,rx=6)); o.append(text(75,185,"Ask: what's the reason",10.6,INK)); o.append(text(75,203,"for the change?",10.6,INK))
    o.append(arrow(60,190,10,190,MUTED)); o.append(text(-40,186,"",1,INK))
    branches=[("A genuine error you missed\n(wrong filter, wrong period)",GREEN,"Fix it, thank them,\nre-check nearby numbers too",340),
              ("A reasonable alternative\ndefinition, argued on merits",ACC,"Show both versions,\nlet them choose, document it",440),
              ("\"It doesn't look good\" —\nno methodological reason",RED,"Hold the number; offer\nto explain it, in writing",540)]
    for label,c,resp,y in branches:
        o.append(path(f"M160,220 C160,{y-30} 260,{y} 300,{y}",stroke=c,sw=1.6))
        o.append(rect(300,y-24,270,52,fill="#fff",stroke=c,sw=1.4,rx=6))
        for i,l in enumerate(label.split("\n")): o.append(text(312,y-6+i*15,l,10,INK))
        o.append(arrow(570,y,610,y,c))
        o.append(rect(615,y-24,300,52,fill=c,rx=6))
        for i,l in enumerate(resp.split("\n")): o.append(text(628,y-6+i*15,l,10.2,"#fff","bold" if i==0 else None))
    o.append(text(30,570,"The test is always the same: would you be comfortable explaining this change, and the reason for it, to the person who first asked for the number?",11.3,MUTED))
    return svg(940,588,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig24-1-stakeholder-grid.svg",f1),("fig24-2-pyramid-principle.svg",f2),
                ("fig24-3-one-message-per-slide.svg",f3),("fig24-4-handling-pushback.svg",f4)]:
        open(n,"w").write(f())
    print("ok")
