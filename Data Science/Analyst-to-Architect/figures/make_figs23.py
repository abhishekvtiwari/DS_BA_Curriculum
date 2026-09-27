# Diagrams for Chapter 23. Run: python3 make_figs23.py
from make_figs import *
import pathlib, pandas as pd
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def card(x,y,w,h,title,c,lines,size=10.8):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+26} H{x} Z" fill="{c}"/>',
       text(x+11,y+18,title,11.5,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+11,y+45+i*17,l,size,INK))
    return "".join(o)

def f1():  # operating / cash conversion cycle
    o=[text(30,32,"The operating cycle: how cash becomes stock becomes cash again",14.5,INK,"bold",family=HEAD)]
    stages=[("Cash","in the bank",ACC),("Buy stock","pay suppliers\n(DPO: 38 days)",GOLD),
            ("Hold inventory","in the warehouse\n(DIO: 55 days)",ORANGE),
            ("Sell to customer","invoice raised",GREEN),
            ("Collect payment","(DSO: 42 days)",PURPLE),("Cash","back in the bank",ACC)]
    W=150
    for i,(t,sub,c) in enumerate(stages):
        x=20+i*(W+14)
        o.append(card(x,60,W,90,t,c,sub.split("\n"),10.6))
        if i<len(stages)-1: o.append(arrow(x+W+2,105,x+W+12,105))
    o.append(rect(20,180,984,80,fill="#fff",stroke=RED,sw=1.6,rx=8)); o.append(rect(20,180,9,80,fill=RED))
    o.append(text(42,206,"Cash conversion cycle = DIO + DSO − DPO = 55 + 42 − 38 = 59 days",13,INK,"bold"))
    o.append(text(42,228,"Riverstone's cash is tied up in stock and unpaid invoices for 59 days before it becomes cash again — even though the",11.5,MUTED))
    o.append(text(42,246,"company is profitable. A profitable company can still run out of cash if this cycle is long and growing fast.",11.5,MUTED))
    return svg(1024,278,"".join(o))

def f2():  # P&L waterfall
    d = pd.read_csv(pathlib.Path(__file__).resolve().parent.parent/"companion/ch23/monthly_revenue_2025.csv")
    REVENUE=1146641651; COGS=831803000; GP=REVENUE-COGS
    sd=round(REVENUE*0.052); mk=round(REVENUE*0.018); ad=round(REVENUE*0.041); dep=round(REVENUE*0.014)
    ebit=GP-sd-mk-ad-dep; interest=round(REVENUE*0.009); pbt=ebit-interest; tax=round(pbt*0.25); pat=pbt-tax
    steps=[("Revenue",REVENUE,True),("COGS",-COGS,False),("Gross\nprofit",GP,True),
           ("Selling &\ndist.",-sd,False),("Marketing",-mk,False),("Admin",-ad,False),("Deprec.",-dep,False),
           ("EBIT",ebit,True),("Interest",-interest,False),("Tax",-tax,False),("Net\nprofit",pat,True)]
    fig_w=1080; fig_h=440
    o=[text(30,32,"Riverstone's FY2025 P&L, top to bottom (₹ crore)",14.5,INK,"bold",family=HEAD)]
    maxv=REVENUE; scale=250/maxv
    run=0; x=30
    W=88
    for i,(label,val,is_total) in enumerate(steps):
        if is_total:
            h=abs(val)*scale
            y=360-h
            o.append(rect(x,y,W,h,fill=ACC,rx=3))
            o.append(text(x+W/2,y-8,f"{val/1e7:,.1f}",10.5,INK,"bold",anchor="middle"))
            run=val
        else:
            h=abs(val)*scale
            top=360-(run*scale); newrun=run+val; newtop=360-(newrun*scale)
            y=min(top,newtop)
            o.append(rect(x,y,W,h,fill=RED if val<0 else GREEN,rx=3))
            o.append(text(x+W/2,y-8,f"{val/1e7:+,.1f}",10.2,RED if val<0 else GREEN,"bold",anchor="middle"))
            run=newrun
        for j,l in enumerate(label.split("\n")):
            o.append(text(x+W/2,388+j*14,l,10,MUTED,anchor="middle"))
        x+=W+10
    o.append(path(f"M30,360 H{x-10}",stroke=RULE,sw=1))
    o.append(text(30,430,"Gross margin 27.5% · EBIT margin 15.0% · net margin 10.5%. Cost of goods sold is real (the order data); everything else is modelled for this chapter.",11,MUTED))
    return svg(fig_w,fig_h,"".join(o))

def f3():  # KPI tree
    o=[text(30,30,"A KPI tree: revenue decomposed into things a team can act on",14.5,INK,"bold",family=HEAD)]
    o.append(card(400,58,220,64,"Net revenue","₹114.7 cr",[],12))
    o.append(card(120,160,180,90,"Active customers",ACC,["4,599 in 2025","new + retained − churned"],10.4))
    o.append(card(330,160,180,90,"Orders per customer",GREEN,["≈10.1 / year","frequency"],10.4))
    o.append(card(540,160,180,90,"Average order value",ORANGE,["₹24,736","price × basket size"],10.4))
    o.append(card(750,160,180,90,"Gross margin",PURPLE,["27.5%","price − cost of goods"],10.4))
    for x2 in (210,420,630,840): o.append(arrow(510,122,x2,158))
    o.append(card(60,286,190,86,"New customers",GOLD,["marketing spend","÷ CAC"],10.2))
    o.append(card(270,286,190,86,"Retention rate",GOLD,["93.3%","1 − churn"],10.2))
    for x2,px in [(155,210),(365,210)]: o.append(arrow(x2,250,x2,284))
    o.append(card(480,286,190,86,"Units per order",GOLD,["basket size"],10.2))
    o.append(card(690,286,190,86,"Price / discount",GOLD,["list price, rebate band"],10.2))
    for x2,px in [(575,420),(785,420)]: o.append(arrow(x2,250,x2,284))
    o.append(text(30,404,"Each box is owned by a team: marketing owns new customers, sales owns orders per customer and discount, ops owns cost and margin.",11.5,MUTED))
    return svg(1010,420,"".join(o))

def f4():  # root cause waterfall May->June
    steps=[("May 2025",87249568,True),("Fewer\ncustomers",-4899282,False),("Fewer orders\nper customer",-5070734,False),
           ("Lower average\norder value",-25307069,False),("June 2025",51972483,True)]
    fig_w=880; fig_h=380
    o=[text(30,32,"Diagnosing the May → June dip: a chain-linked bridge",14.5,INK,"bold",family=HEAD)]
    maxv=90000000; scale=260/maxv
    run=0; x=40; W=140
    for i,(label,val,is_total) in enumerate(steps):
        if is_total:
            h=val*scale; y=330-h
            o.append(rect(x,y,W,h,fill=ACC,rx=3))
            o.append(text(x+W/2,y-10,f"₹{val/1e7:.2f} cr",11,INK,"bold",anchor="middle"))
            run=val
        else:
            h=abs(val)*scale; top=330-(run*scale); newrun=run+val; newtop=330-(newrun*scale)
            y=min(top,newtop)
            o.append(rect(x,y,W,h,fill=RED,rx=3))
            o.append(text(x+W/2,y-10,f"−₹{abs(val)/1e7:.2f} cr",10.5,RED,"bold",anchor="middle"))
            run=newrun
        for j,l in enumerate(label.split("\n")):
            o.append(text(x+W/2,352+j*15,l,10.6,MUTED,anchor="middle"))
        x+=W+14
    o.append(text(30,-100+380,"",1,INK))
    return svg(fig_w,fig_h,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig23-1-operating-cycle.svg",f1),("fig23-2-pnl-waterfall.svg",f2),
                ("fig23-3-kpi-tree.svg",f3),("fig23-4-root-cause.svg",f4)]:
        open(n,"w").write(f())
    print("ok")
