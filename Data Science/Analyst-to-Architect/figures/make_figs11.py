# Generates the SVG figures for Chapter 11. Run: python3 make_figs11.py
# Numbers come from checks/ch11_expected.py and checks/ch11_formula_tests.py.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; SOFT="#e9eef4"

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=11.5,mono=False):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+28} H{x} Z" fill="{c}"/>',
       text(x+12,y+19,title,12.5,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+12,y+48+i*20,l,size,INK,family=(MONO if mono else None)))
    return "".join(o)

# ---------- Figure 11.1: pivot table areas = GROUP BY ----------
def fig_pivot():
    o=[]
    areas=[("Filters","status ≠ Cancelled","WHERE status <> 'Cancelled'",ORANGE),
           ("Rows","segment","GROUP BY segment",ACC),
           ("Columns","quarter","… and quarter, spread across",PURPLE),
           ("Values","Sum of net_revenue","SUM(net_revenue)",GREEN)]
    o.append(text(30,28,"Field list areas",13.5,INK,"bold",family=HEAD)); o.append(text(250,28,"SQL it corresponds to (Chapter 12)",13.5,INK,"bold",family=HEAD))
    for i,(a,f,sql,c) in enumerate(areas):
        y=44+i*62
        o.append(rect(30,y,190,48,fill="#fff",stroke=c,sw=1.6,rx=6)); o.append(rect(30,y,190,18,fill=c,rx=6)); o.append(rect(30,y+10,190,8,fill=c))
        o.append(text(40,y+14,a,11.5,"#fff","bold")); o.append(text(40,y+38,f,12,INK,family=MONO))
        o.append(arrow(224,y+30,246,y+30)); o.append(text(252,y+34,sql,12,c,"bold",family=MONO))
    X=520; Y=58; hdr=["segment","Q1","Q2","Q3","Q4","Grand Total"]; wd=[104,76,76,80,80,96]
    rows=[["Hospitality","149,040","252,170","307,278","435,551","1,144,039"],["Retail","394,328","198,474","333,973","562,000","1,488,774"],
          ["Wholesale","190,944","275,925","479,039","756,751","1,702,659"],["Grand Total","734,312","726,568","1,120,289","1,754,302","4,335,471"]]
    o.append(text(X,Y-16,"Result: Sum of net_revenue (₹), 2025",13.5,INK,"bold",family=HEAD))
    o.append(rect(X,Y,sum(wd),24,fill=PURPLE,rx=4)); cx=X
    for h,w in zip(hdr,wd):
        o.append(text(cx+(8 if h=="segment" else w-8),Y+16,h,11,"#fff","bold",anchor=("start" if h=="segment" else "end"),family=MONO)); cx+=w
    for i,r in enumerate(rows):
        y=Y+24+i*26; last=i==3
        o.append(rect(X,y,sum(wd),26,fill=("#eef1f5" if last else "#fff"),stroke=RULE,sw=0.8)); cx=X
        for j,(v,w) in enumerate(zip(r,wd)):
            col = ACC if j==0 else (GREEN if (j==5 or last) else INK)
            o.append(text(cx+(8 if j==0 else w-8),y+17,v,11.3,col,"bold" if (last or j in (0,5)) else "normal",anchor=("start" if j==0 else "end"),family=MONO)); cx+=w
    o.append(text(X,Y+24+4*26+22,"Rows area → one row per segment. Columns area → one column per quarter.",11.5,MUTED))
    o.append(text(X,Y+24+4*26+40,"Values area → the aggregate in every cell. Filters → rows left out first.",11.5,MUTED))
    o.append(text(30,318,"The grand total reconciles to Chapter 10's tracker and Chapter 13's query: ₹4,335,471.",12.3,INK))
    return svg(1050,335,"".join(o))

# ---------- Figure 11.2: three ways to look up ----------
def fig_lookups():
    o=[]
    X=30; Y=70; hdr=["A customer_code","B customer_name","C city","D segment"]; wd=[150,210,120,120]
    data=[["0012","Fresh Bowl Kitchens","Bengaluru","Hospitality"],["0013","Om Sai Provisions","Nashik","Retail"],["0014","Deccan Packaging","Hyderabad","Wholesale"],["0015","Spice Route Restaurants","Kolkata","Hospitality"]]
    o.append(text(X,Y-30,"Customers sheet (rows 13–16 shown)",13.5,INK,"bold",family=HEAD)); o.append(text(X,Y-12,"Question: what is the city for customer code 0014?",11.5,MUTED,style="italic"))
    o.append(rect(X,Y,sum(wd),24,fill=ACC,rx=4)); cx=X
    for h,w in zip(hdr,wd): o.append(text(cx+8,Y+16,h,11,"#fff","bold",family=MONO)); cx+=w
    for i,r in enumerate(data):
        y=Y+24+i*26; hit=i==2
        o.append(rect(X,y,sum(wd),26,fill=("#fdf3dc" if hit else "#fff"),stroke=RULE,sw=0.8)); cx=X
        for j,(v,w) in enumerate(zip(r,wd)):
            o.append(text(cx+8,y+17,v,11.5,(ORANGE if hit and j in (0,2) else INK),"bold" if hit and j in (0,2) else "normal",family=MONO)); cx+=w
    # bracket annotations
    o.append(rect(X+2,Y+26,146,102,fill="none",stroke=GREEN,sw=2,rx=4)); o.append(rect(X+362,Y+26,116,102,fill="none",stroke=PURPLE,sw=2,rx=4))
    o.append(text(X+2,Y+150,"lookup column",11.5,GREEN,"bold")); o.append(text(X+362,Y+150,"return column",11.5,PURPLE,"bold"))
    fx=[("XLOOKUP",GREEN,'=XLOOKUP("0014", A2:A25, C2:C25)',"Point at the lookup column and the return column. Default: exact match."),
        ("INDEX / MATCH",ACC,'=INDEX(C2:C25, MATCH("0014", A2:A25, 0))',"MATCH finds the position (14); INDEX returns item 14. Works in every version."),
        ("VLOOKUP",RED,'=VLOOKUP("0014", A2:D25, 3, FALSE)',"Counts columns (3). Insert a column inside A:D and it silently returns the wrong one.")]
    for i,(t,c,f,note) in enumerate(fx):
        y=250+i*62
        o.append(rect(X,y,1000,50,fill="#fff",stroke=c,sw=1.4,rx=6)); o.append(rect(X,y,130,50,fill=c,rx=6)); o.append(rect(X+120,y,10,50,fill=c))
        o.append(text(X+12,y+30,t,12.5,"#fff","bold",family=HEAD)); o.append(text(X+146,y+22,f,12.3,INK,"bold",family=MONO))
        o.append(text(X+146,y+41,note,11.5,MUTED)); o.append(text(X+986,y+30,"→ Hyderabad",12.3,c,"bold",anchor="end"))
    return svg(1060,445,"".join(o))

# ---------- Figure 11.3: spill ----------
def fig_spill():
    o=[]
    def grid(x,y,title,sub,c,cells,blocked=False):
        o.append(text(x,y-30,title,13.5,c,"bold",family=HEAD)); o.append(text(x,y-12,sub,11.5,MUTED,style="italic"))
        cw=[34,196]; rh=24
        o.append(rect(x,y,sum(cw),rh,fill="#eef1f5",stroke=RULE)); o.append(text(x+cw[0]+8,y+16,"F",11,MUTED))
        for i in range(8):
            yy=y+rh*(i+1)
            o.append(rect(x,yy,cw[0],rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(x+17,yy+16,str(i+1),11,MUTED,anchor="middle"))
            v,style=cells[i] if i<len(cells) else ("","")
            fill="#fff"
            if style=="anchor": fill="#e2f3ee"
            if style=="spill": fill="#f2faf7"
            if style=="block": fill="#f8e1e1"
            o.append(rect(x+cw[0],yy,cw[1],rh,fill=fill,stroke=RULE,sw=0.6))
            o.append(text(x+cw[0]+8,yy+16,v,11.3,(RED if style=="block" or v=="#SPILL!" else (MUTED if style=="spill" else INK)),"bold" if style in("anchor","block") else "normal",family=MONO))
        if not blocked:
            o.append(rect(x+cw[0]+1,y+rh*2+1,cw[1]-2,rh*6-2,fill="none",stroke=GREEN,sw=2,extra='stroke-dasharray="5 3"'))
    names=["Blue Bay Cafe","City Needs Store","Coastal Foods","Deccan Packaging","Evergreen Mart"]
    grid(30,70,"The formula lives in one cell…","F2: =SORT(UNIQUE(Sales[customer_name]))",GREEN,
         [("customer (23 names)",""),("Blue Bay Cafe","anchor")]+[(n,"spill") for n in names[1:]]+[("… 18 more rows","spill")])
    grid(380,70,"…and a blocked spill shows #SPILL!","Someone typed a note in F4",RED,
         [("customer (23 names)",""),("#SPILL!","anchor"),("",""),("check later","block")],blocked=True)
    notes=["The dashed range is the spill range. Only F2",
           "holds a formula; the other cells show its",
           "results and can't be typed into.",
           "Refer to the whole result as F2# (Excel);",
           "it grows or shrinks with the data.",
           "Clear the blocking cell and it spills again.",
           "Google Sheets spills the same way; a blocked",
           "result shows #REF! (array not expanded)."]
    for i,l in enumerate(notes): o.append(text(660,86+i*22,l,12,INK))
    return svg(1060,300,"".join(o))

# ---------- Figure 11.4: Power Query pipeline ----------
def fig_pq():
    o=[]
    steps=[("Source","Folder: 12 CSV files","12 files",MUTED),("Combine","Stack every file","330 rows",ACC),
           ("Types","Dates read as en-IN;","330 rows",ACC),("Filter","status ≠ Cancelled","326 rows",ORANGE),
           ("Add column","net_revenue","326 rows",PURPLE),("Load","Table on a sheet","₹4,335,471",GREEN)]
    extra={2:"codes kept as text"}
    W=150; G=22
    for i,(t,sub,cnt,c) in enumerate(steps):
        x=30+i*(W+G); y=70
        lines=[sub]+([extra[i]] if i in extra else [])
        o.append(box(x,y,W,110,t,c,lines,11))
        o.append(rect(x+12,y+80,W-24,22,fill="#f6f9fc",stroke=RULE,rx=11)); o.append(text(x+W/2,y+95,cnt,11.5,c,"bold",anchor="middle"))
        if i<5: o.append(arrow(x+W+2,y+55,x+W+G-2,y+55))
    o.append(text(30,40,"Applied Steps in the Power Query Editor, recorded once and replayed on every Refresh",13.5,INK,"bold",family=HEAD))
    # refresh loop
    o.append(path("M950,190 C950,250 520,250 105,250 C70,250 70,215 105,190",stroke=GREEN,sw=1.8,dash="6 4"))
    o.append(f'<path d="M105,190 l-6,10 l12,0 z" fill="{GREEN}"/>')
    o.append(rect(330,236,400,28,fill="#e2f3ee",rx=14)); o.append(text(530,255,"Next month: drop in a file → Data → Refresh All",12,GREEN,"bold",anchor="middle"))
    o.append(text(30,300,"Nothing here edits the CSV files. Each step is a recorded instruction; delete or edit a step and everything after it recalculates.",12.2,MUTED))
    return svg(1070,318,"".join(o))

# ---------- Figure 11.5: data model ----------
def fig_model():
    o=[]
    o.append(box(390,110,260,190,"Sales (fact) · 330 rows",ACC,["order_id","order_date  → Calendar","customer_code → Customers","product_id → Products","quantity, unit_price,","discount_pct, status"],11.3,True))
    dims=[(40,40,"Customers · 24 rows",GREEN,["customer_code (key)","customer_name","city, segment"]),
          (40,240,"Products · 8 rows",PURPLE,["product_id (key)","product_name, category","unit_cost"]),
          (760,140,"Calendar · 365 rows",ORANGE,["Date (key)","Month, Quarter, Year","marked as date table"])]
    for x,y,t,c,l in dims: o.append(box(x,y,240,120,t,c,l,11.3,True))
    def rel(x1,y1,x2,y2,c):
        o.append(path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=2))
        o.append(text(x1+(6 if x2>x1 else -14),y1-6,"1",12,c,"bold")); o.append(text(x2+(-14 if x2>x1 else 6),y2-6,"*",14,c,"bold"))
    rel(280,100,390,160,GREEN); rel(280,300,390,250,PURPLE); rel(760,200,650,200,ORANGE)
    o.append(rect(40,390,850,74,fill="#fff4d6",stroke="#e2c46b",rx=6))
    o.append(text(56,414,"Valid Net Revenue := CALCULATE([Net Revenue], Sales[status] <> \"Cancelled\")",12.3,INK,"bold",family=MONO))
    o.append(text(56,436,"A measure is written once and recalculated for every pivot cell: by segment (via Customers),",12,INK))
    o.append(text(56,454,"by category (via Products), or year to date (via Calendar). Filters flow from the 1 side to the * side.",12,INK))
    return svg(1040,480,"".join(o))

# ---------- Figure 11.1: SUMIFS anatomy ----------
def fig_sumifs():
    o=[]
    parts=[("=SUMIFS(",INK,None),("Sales!J2:J331",GREEN,"sum range (always first)"),(", ",INK,None),
           ("Sales!N2:N331",ACC,"criteria range 1"),(", ",INK,None),('"Retail"',ACC,"criterion 1"),(", ",INK,None),
           ("Sales!H2:H331",PURPLE,"criteria range 2"),(", ",INK,None),('"<>Cancelled"',PURPLE,"criterion 2"),(")",INK,None)]
    x=30; y=70; cw=9.9; k=0
    for t,c,lab in parts:
        w=len(t)*cw
        if lab:
            o.append(rect(x-2,y-20,w+4,30,fill="#f6f9fc",stroke=c,sw=1.6,rx=4))
        o.append(text(x,y,t,14.5,c,"bold",family=MONO))
        if lab:
            dy=36 if k%2==0 else 58; k+=1
            o.append(path(f"M{x+w/2},{y+12} L{x+w/2},{y+dy}",stroke=c,sw=1.2)); o.append(text(x+w/2,y+dy+14,lab,11.3,c,"bold",anchor="middle"))
        x+=w
    o.append(text(30,24,"One pair of arguments per condition; all conditions must hold (AND). Result: 1,488,773.75",13,INK,"bold",family=HEAD))
    rows=[('"Retail"',"equals (not case-sensitive)","118 lines"),('"<>Cancelled"',"not equal","326 lines"),
          ('">=50000"',"compare a number (no commas)","3 lines"),('">="&G1',"operator in quotes, cell outside","depends on G1"),
          ('">="&DATE(2025,7,1)',"dates: build them with DATE","Q3 ₹1,120,289 (with <= 30 Sep)"),
          ('"*Box*"',"wildcards: * any text, ? one character","169 lines"),('""  /  "<>"',"blank / not blank","19 / 311 rep cells")]
    X=30; Y=170; wd=[230,330,300]
    o.append(rect(X,Y,sum(wd),26,fill=ACC,rx=4))
    for j,(h,w) in enumerate(zip(["criterion","meaning","Riverstone result"],wd)): o.append(text(X+sum(wd[:j])+10,Y+18,h,11.5,"#fff","bold"))
    for i,(a,b,c) in enumerate(rows):
        yy=Y+26+i*28
        o.append(rect(X,yy,sum(wd),28,fill="#fff",stroke=RULE,sw=0.8))
        o.append(text(X+10,yy+19,a,12,INK,"bold",family=MONO)); o.append(text(X+wd[0]+10,yy+19,b,12,INK)); o.append(text(X+wd[0]+wd[1]+10,yy+19,c,12,GREEN,"bold"))
    return svg(1000,Y+26+len(rows)*28+20,"".join(o))

# ---------- Figure 11.7: the stockroom model ----------
def fig_stockroom():
    o=[]
    o.append(text(30,28,"The Riverstone Stockroom: one row per day, 1 Jan to 31 Dec 2025 (Storage Box 10L)",13.5,INK,"bold",family=HEAD))
    cols=[("Log sheet","330 text codes",["02.01.2025|SO10001|…","→ date, product, qty, status","(TEXTSPLIT or MID/FIND)"],MUTED),
          ("demand","SUMIFS by date",["units of product 101","on non-cancelled lines"],ACC),
          ("po_placed","every Monday",["1 if yesterday's closing","≤ reorder point (ROP)"],ORANGE),
          ("receipts","L days later",["Q units arrive at","start of day d + L"],PURPLE),
          ("closing","running balance",["yesterday's closing","+ receipts − demand"],GREEN)]
    W=176; G=16
    for i,(t,sub,lines,c) in enumerate(cols):
        x=30+i*(W+G); y=48
        o.append(box(x,y,W,124,t,c,[sub]+lines,11))
        if i<4: o.append(arrow(x+W+2,y+62,x+W+G-2,y+62))
    o.append(path("M890,176 C890,232 502,232 502,176",stroke=ORANGE,sw=1.8,dash="6 4")); o.append(f'<path d="M502,176 l-6,10 l12,0 z" fill="{ORANGE}"/>')
    o.append(text(696,246,"closing feeds next Monday's decision",11.5,ORANGE,"bold",anchor="middle"))
    X=30; Y=270
    hdr=["date","wkday","demand","receipts","po","closing"]; wd=[110,70,80,84,50,84]
    o.append(rect(X,Y,sum(wd),24,fill=GREEN,rx=4)); cx=X
    for h,w in zip(hdr,wd): o.append(text(cx+8,Y+16,h,11,"#fff","bold",family=MONO)); cx+=w
    sample=[("2025-02-09","7","0","0","0","95"),("2025-02-10","1","0","0","1","95"),("2025-02-16","7","25","0","0","70"),("2025-02-17","1","30","250","1","290")]
    for i,r in enumerate(sample):
        yy=Y+24+i*24; cx=X
        o.append(rect(X,yy,sum(wd),24,fill=("#fdf3dc" if r[4]=="1" else "#fff"),stroke=RULE,sw=0.7))
        for v,w in zip(r,wd): o.append(text(cx+8,yy+16,v,11,INK,family=MONO)); cx+=w
    notes=["ROP 100, Q 250, lead time 7 days:",
           "• 8 purchase orders; lowest closing −45 on 3 Oct",
           "• 7 days below zero; year-end closing 215",
           "• total cost ₹118,210 (holding + shortage + orders)",
           "17 Feb: 250 units arrive, yet another order is placed,",
           "because the rule reads Sunday's stock, not stock on order."]
    for i,l in enumerate(notes): o.append(text(560,Y+18+i*21,l,12,INK if i else GREEN,"bold" if i==0 else "normal"))
    return svg(1010,Y+24+4*24+30,"".join(o))


# ---------- Figure 11.6: the Stockroom case, closing stock under two policies ----------
def fig_stock():
    import json
    d=json.load(open("/tmp/stock.json")) if __import__("os").path.exists("/tmp/stock.json") else None
    o=[]; X0=70; Y0=40; W=900; H=260
    lo,hi=-100,600
    def px(i): return X0+i*W/364
    def py(v): return Y0+H-(v-lo)*H/(hi-lo)
    for v in range(-100,601,100):
        o.append(path(f"M{X0},{py(v):.1f} H{X0+W}",stroke=(INK if v==0 else RULE),sw=(1.2 if v==0 else 0.6)))
        o.append(text(X0-8,py(v)+4,f"{v:,}",10.5,MUTED,anchor="end",family=MONO))
    for m,lab in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]):
        import datetime as dt
        i=(dt.date(2025,m+1,1)-dt.date(2025,1,1)).days
        o.append(text(px(i)+30,Y0+H+18,lab,10.5,MUTED))
    o.append(f'<rect x="{X0}" y="{py(0):.1f}" width="{W}" height="{py(lo)-py(0):.1f}" fill="#f8e1e1" opacity="0.6"/>')
    for key,c,lab in [("a",ACC,"ROP 100, Q 250: 8 POs, 7 negative days, cost ₹118,210"),("b",ORANGE,"ROP 50, Q 150: 13 POs, 21 negative days, cost ₹84,840 (cheapest)")]:
        pts=" ".join(f"{px(i):.1f},{py(v):.1f}" for i,v in enumerate(d[key]))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="1.6"/>')
    o.append(path(f"M{X0},{py(100):.1f} H{X0+W}",stroke=ACC,sw=1,dash="4 3")); o.append(text(X0+W-4,py(100)-5,"ROP 100",10.5,ACC,anchor="end"))
    o.append(text(X0+6,py(-60),"backorders (negative stock)",11,RED))
    o.append(rect(X0,Y0+H+34,14,4,fill=ACC)); o.append(text(X0+20,Y0+H+40,"ROP 100, Q 250: 8 POs, 7 negative days, total cost ₹118,210",11.5,INK))
    o.append(rect(X0+480,Y0+H+34,14,4,fill=ORANGE)); o.append(text(X0+500,Y0+H+40,"ROP 50, Q 150: 13 POs, 21 negative days, ₹84,840 (cheapest)",11.5,INK))
    o.append(text(X0,24,"Storage Box 10L closing stock in 2025 (units), lead time 7 days, weekly Monday review",13.5,INK,"bold",family=HEAD))
    return svg(1000,360,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig11-1-sumifs-anatomy.svg",fig_sumifs),("fig11-7-stockroom-model.svg",fig_stockroom),("fig11-3-pivot-areas-group-by.svg",fig_pivot),("fig11-2-three-lookups.svg",fig_lookups),
                    ("fig11-4-dynamic-array-spill.svg",fig_spill),("fig11-5-power-query-steps.svg",fig_pq),
                    ("fig11-6-data-model-star.svg",fig_model),("fig11-8-stockroom-policies.svg",fig_stock)]:
        open(name,"w").write(fn())
    print("ok")
