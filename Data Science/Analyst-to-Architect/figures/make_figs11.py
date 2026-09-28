# Generates the SVG figures for Chapter 11. Run from figures/:  python3 make_figs11.py
# Numbers come from checks/ch11_expected.py, checks/ch11_formula_tests.py and checks/ch11_challenge_sim.py.
# Redrawn for print (Part 2 build, 28 Sep 2026): every canvas is 720 px wide and prints at 493.2 pt,
# so the smallest text, 10.5 px, prints at 7.2 pt. Rupee amounts use Indian lakh grouping.
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
import os, math, datetime as dt
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; SOFT="#e9eef4"
CW=720          # canvas width
S=10.5          # smallest text size (7.2 pt in print)


def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'


def box(x,y,w,h,title,c,lines=(),size=S,mono=False,lh=16):
    o=[rect(x+2,y+3,w,h,fill=SOFT,rx=6),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.4,rx=6),
       f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 H{x+w-6} a6,6 0 0 1 6,6 V{y+22} H{x} Z" fill="{c}"/>',
       text(x+9,y+16,title,11.5,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+9,y+40+i*lh,l,size,INK,family=(MONO if mono else None)))
    return "".join(o)


def table(o,X,Y,hdr,rows,wd,c,rh=20,num_from=1,bold_last=False,size=S,hsize=S):
    o.append(rect(X,Y,sum(wd),rh,fill=c,rx=3)); cx=X
    for j,(h,w) in enumerate(zip(hdr,wd)):
        right=j>=num_from
        o.append(text(cx+(w-6 if right else 6),Y+rh-6,h,hsize,"#fff","bold",anchor=("end" if right else "start"))); cx+=w
    for i,r in enumerate(rows):
        y=Y+rh+i*rh; last=bold_last and i==len(rows)-1
        o.append(rect(X,y,sum(wd),rh,fill=("#eef1f5" if last else "#fff"),stroke=RULE,sw=0.7)); cx=X
        for j,(v,w) in enumerate(zip(r,wd)):
            right=j>=num_from
            o.append(text(cx+(w-6 if right else 6),y+rh-6,v,size,INK,"bold" if last else "normal",anchor=("end" if right else "start"),family=MONO)); cx+=w
    return Y+rh*(len(rows)+1)


# ---------- Figure 11.1: SUMIFS anatomy ----------
def fig_sumifs():
    o=[]
    o.append(text(16,20,"One pair of arguments per condition; all must hold (AND). Result: 14,88,773.75",12,INK,"bold",family=HEAD))
    parts=[("=SUMIFS(",INK,None),("Sales!J2:J331",GREEN,"sum range (first)"),(",",INK,None),
           ("Sales!N2:N331",ACC,"criteria range 1"),(",",INK,None),('"Retail"',ACC,"criterion 1"),(",",INK,None),
           ("Sales!H2:H331",PURPLE,"criteria range 2"),(",",INK,None),('"<>Cancelled"',PURPLE,"criterion 2"),(")",INK,None)]
    x=16; y=58; cw=7.25; k=0
    for t,c,lab in parts:
        w=len(t)*cw
        if lab: o.append(rect(x-2,y-15,w+4,21,fill="#f6f9fc",stroke=c,sw=1.3,rx=3))
        o.append(text(x,y,t,12,c,"bold",family=MONO))
        if lab:
            dy=22 if k%2==0 else 40; k+=1
            o.append(path(f"M{x+w/2},{y+7} L{x+w/2},{y+dy}",stroke=c,sw=1.1)); o.append(text(x+w/2,y+dy+12,lab,S,c,"bold",anchor="middle"))
        x+=w+(3 if t=="," else 0)
    rows=[('"Retail"',"equals (not case-sensitive)","118 lines"),('"<>Cancelled"',"not equal","326 lines"),
          ('">=50000"',"compare a number (no commas)","3 lines"),('">="&G1',"operator in quotes, cell outside","depends on G1"),
          ('">="&DATE(2025,7,1)',"dates: build them with DATE","Q3 ₹11,20,289 (with <= 30 Sep)"),
          ('"*Box*"',"wildcards: * any text, ? one character","169 lines"),('""  /  "<>"',"blank / not blank","19 / 311 rep cells")]
    X=16; Y=130; wd=[172,272,244]
    o.append(rect(X,Y,sum(wd),22,fill=ACC,rx=3))
    for j,(h,w) in enumerate(zip(["criterion","meaning","Riverstone result"],wd)): o.append(text(X+sum(wd[:j])+7,Y+15,h,S,"#fff","bold"))
    for i,(a,b,c) in enumerate(rows):
        yy=Y+22+i*21
        o.append(rect(X,yy,sum(wd),21,fill="#fff",stroke=RULE,sw=0.7))
        o.append(text(X+7,yy+15,a,S,INK,"bold",family=MONO)); o.append(text(X+wd[0]+7,yy+15,b,S,INK)); o.append(text(X+wd[0]+wd[1]+7,yy+15,c,S,GREEN,"bold"))
    return svg(CW,Y+22+len(rows)*21+10,"".join(o))


# ---------- Figure 11.2: three ways to look up ----------
def fig_lookups():
    o=[]
    X=16; Y=46; hdr=["A code","B customer_name","C city","D segment"]; wd=[90,196,110,110]
    data=[["0012","Fresh Bowl Kitchens","Bengaluru","Hospitality"],["0013","Om Sai Provisions","Nashik","Retail"],
          ["0014","Deccan Packaging","Hyderabad","Wholesale"],["0015","Spice Route Restaurants","Kolkata","Hospitality"]]
    o.append(text(X,18,"Customers sheet (rows 13–16 shown)",12,INK,"bold",family=HEAD))
    o.append(text(X,35,"Question: what is the city for customer code 0014?",S,MUTED,style="italic"))
    o.append(rect(X,Y,sum(wd),20,fill=ACC,rx=3)); cx=X
    for h,w in zip(hdr,wd): o.append(text(cx+6,Y+14,h,S,"#fff","bold",family=MONO)); cx+=w
    for i,r in enumerate(data):
        y=Y+20+i*20; hit=i==2
        o.append(rect(X,y,sum(wd),20,fill=("#fdf3dc" if hit else "#fff"),stroke=RULE,sw=0.7)); cx=X
        for j,(v,w) in enumerate(zip(r,wd)):
            o.append(text(cx+6,y+14,v,S,(ORANGE if hit and j in (0,2) else INK),"bold" if hit and j in (0,2) else "normal",family=MONO)); cx+=w
    o.append(rect(X+2,Y+21,86,78,fill="none",stroke=GREEN,sw=1.8,rx=3)); o.append(rect(X+288,Y+21,106,78,fill="none",stroke=PURPLE,sw=1.8,rx=3))
    o.append(text(X+2,Y+114,"lookup column (A)",S,GREEN,"bold")); o.append(text(X+288,Y+114,"return column (C)",S,PURPLE,"bold"))
    o.append(text(X+530,Y+40,"Row 15 of the sheet",S,MUTED)); o.append(text(X+530,Y+56,"is the 14th code",S,MUTED)); o.append(text(X+530,Y+72,"in A2:A25.",S,MUTED))
    fx=[("XLOOKUP",GREEN,'=XLOOKUP("0014", A2:A25, C2:C25)',"Point at the lookup column and the return column. Exact match by default."),
        ("INDEX / MATCH",ACC,'=INDEX(C2:C25, MATCH("0014", A2:A25, 0))',"MATCH finds the position (14); INDEX returns item 14. Every version."),
        ("VLOOKUP",RED,'=VLOOKUP("0014", A2:D25, 3, FALSE)',"Counts columns (3). Insert a column inside A:D and it returns the wrong one.")]
    for i,(t,c,f,note) in enumerate(fx):
        y=Y+128+i*50
        o.append(rect(X,y,688,42,fill="#fff",stroke=c,sw=1.3,rx=5)); o.append(rect(X,y,104,42,fill=c,rx=5)); o.append(rect(X+96,y,8,42,fill=c))
        o.append(text(X+8,y+26,t,11.5,"#fff","bold",family=HEAD)); o.append(text(X+114,y+17,f,11,INK,"bold",family=MONO))
        o.append(text(X+114,y+34,note,S,MUTED)); o.append(text(X+680,y+17,"→ Hyderabad",11,c,"bold",anchor="end"))
    return svg(CW,Y+128+3*50+4,"".join(o))


# ---------- Figure 11.3: pivot table areas ----------
def fig_pivot():
    o=[]
    o.append(text(16,18,"The four areas of the field list, and what each one does",12,INK,"bold",family=HEAD))
    areas=[("Filters","status ≠ Cancelled",["leaves rows out","before summarizing"],ORANGE),
           ("Rows","segment",["one row per","segment"],ACC),
           ("Columns","quarter",["one column per","quarter"],PURPLE),
           ("Values","Sum of net_revenue",["the number in","every cell"],GREEN)]
    W=164; G=10
    for i,(a,f,d,c) in enumerate(areas):
        x=16+i*(W+G); y=30
        o.append(box(x,y,W,86,a,c,[],S))
        o.append(text(x+9,y+40,f,S,c,"bold",family=MONO))
        for k,l in enumerate(d): o.append(text(x+9,y+58+k*15,l,S,INK))
    X=16; Y=150
    o.append(text(X,Y-10,"Result: Sum of net_revenue (₹), 2025, cancelled orders filtered out",12,INK,"bold",family=HEAD))
    hdr=["segment","Q1","Q2","Q3","Q4","Grand Total"]; wd=[118,104,104,110,110,142]
    rows=[["Hospitality","1,49,040","2,52,170","3,07,278","4,35,551","11,44,039"],["Retail","3,94,328","1,98,474","3,33,973","5,62,000","14,88,774"],
          ["Wholesale","1,90,944","2,75,925","4,79,039","7,56,751","17,02,659"],["Grand Total","7,34,312","7,26,568","11,20,289","17,54,302","43,35,471"]]
    end=table(o,X,Y,hdr,rows,wd,PURPLE,bold_last=True)
    o.append(text(X,end+17,"Values rounded to whole rupees. The grand total matches Chapter 10's tracker: ₹43,35,471.",S,MUTED))
    return svg(CW,end+26,"".join(o))


# ---------- Figure 11.4: spill ----------
def fig_spill():
    o=[]
    def grid(x,y,title,sub,c,cells,blocked=False):
        o.append(text(x,y-26,title,12,c,"bold",family=HEAD)); o.append(text(x,y-9,sub,S,MUTED,style="italic"))
        cw=[30,232]; rh=21
        o.append(rect(x,y,sum(cw),rh,fill="#eef1f5",stroke=RULE)); o.append(text(x+cw[0]+7,y+15,"F",S,MUTED))
        for i in range(8):
            yy=y+rh*(i+1)
            o.append(rect(x,yy,cw[0],rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(x+15,yy+15,str(i+1),S,MUTED,anchor="middle"))
            v,style=cells[i] if i<len(cells) else ("","")
            fill={"anchor":"#e2f3ee","spill":"#f2faf7","block":"#f8e1e1"}.get(style,"#fff")
            o.append(rect(x+cw[0],yy,cw[1],rh,fill=fill,stroke=RULE,sw=0.6))
            o.append(text(x+cw[0]+7,yy+15,v,S,(RED if style=="block" or v=="#SPILL!" else (MUTED if style=="spill" else INK)),"bold" if style in("anchor","block") else "normal",family=MONO))
        if not blocked:
            o.append(rect(x+cw[0]+1,y+rh*2+1,cw[1]-2,rh*6-2,fill="none",stroke=GREEN,sw=2,extra='stroke-dasharray="5 3"'))
            o.append(text(x+cw[0]+cw[1]-6,y+rh*8+16,"spill range (dashed)",S,GREEN,"bold",anchor="end"))
    names=["Blue Bay Cafe","City Needs Store","Coastal Foods","Deccan Packaging","Evergreen Mart"]
    grid(16,50,"The formula lives in one cell…","F2: =SORT(UNIQUE(Sales[customer_name]))",GREEN,
         [("customer (23 names)",""),("Blue Bay Cafe  ← formula","anchor")]+[(n,"spill") for n in names[1:]]+[("… 18 more rows","spill")])
    grid(310,50,"…and a blocked spill shows #SPILL!","Someone typed a note in F4",RED,
         [("customer (23 names)",""),("#SPILL!  ← formula","anchor"),("",""),("check later  ← blocks it","block")],blocked=True)
    return svg(600,50+21*9+26,"".join(o))


# ---------- Figure 11.5: Power Query pipeline ----------
def fig_pq():
    o=[]
    o.append(text(16,18,"Applied Steps, recorded once and replayed on every Refresh",12,INK,"bold",family=HEAD))
    steps=[("1 Source","Folder: 12 CSV files","12 files",MUTED),("2 Combine","Stack every file","330 rows",ACC),
           ("3 Types","Dates read as en-IN; codes kept as text","330 rows",ACC),("4 Filter","status ≠ Cancelled","326 rows",ORANGE),
           ("5 Add column","net_revenue","326 rows",PURPLE),("6 Load","Table on a sheet","₹43,35,471",GREEN)]
    W=206; G=30; H=92
    for i,(t,sub,cnt,c) in enumerate(steps):
        r,k=divmod(i,3); x=16+k*(W+G); y=32+r*(H+30)
        lines=[sub] if len(sub)<30 else [sub.split("; ")[0]+";",sub.split("; ")[1]]
        o.append(box(x,y,W,H,t,c,lines,S))
        o.append(rect(x+10,y+H-28,W-20,20,fill="#f6f9fc",stroke=RULE,rx=10)); o.append(text(x+W/2,y+H-14,cnt,11,c,"bold",anchor="middle"))
        if k<2: o.append(arrow(x+W+2,y+H/2,x+W+G-2,y+H/2))
    # row 1 end -> row 2 start
    o.append(path(f"M{16+2*(W+G)+W/2},{32+H+2} V{32+H+15} H{16+W/2} V{32+H+28}",stroke=MUTED,sw=1.6))
    o.append(f'<path d="M{16+W/2},{32+H+30} l-5,-8 l10,0 z" fill="{MUTED}"/>')
    y2=32+2*H+30
    o.append(path(f"M{16+2*(W+G)+W/2},{y2+2} V{y2+22} H{16+W/2+40} ",stroke=GREEN,sw=1.6,dash="6 4"))
    o.append(text(16+2*(W+G)+W/2-12,y2+18,"Next month: drop in a file → Data → Refresh All → all six steps run again",S,GREEN,"bold",anchor="end"))
    return svg(CW,y2+30,"".join(o))


# ---------- Figure 11.6: data model ----------
def fig_model():
    o=[]
    o.append(box(250,100,220,140,"Sales (fact) · 330 rows",ACC,["order_id","order_date → Calendar","customer_code → Customers","product_id → Products","quantity, unit_price,","discount_pct, status"],S,True))
    dims=[(16,16,"Customers · 24 rows",GREEN,["customer_code (key)","customer_name","city, segment"]),
          (16,210,"Products · 8 rows",PURPLE,["product_id (key)","product_name, category","unit_cost"]),
          (504,120,"Calendar · 365 rows",ORANGE,["Date (key)","Month, Quarter, Year","marked as date table"])]
    for x,y,t,c,l in dims: o.append(box(x,y,200,88,t,c,l,S,True))
    def rel(x1,y1,x2,y2,c):
        o.append(path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=2))
        o.append(text(x1+(5 if x2>x1 else -12),y1-5,"1",12,c,"bold")); o.append(text(x2+(-12 if x2>x1 else 5),y2-5,"*",13,c,"bold"))
    rel(216,70,250,140,GREEN); rel(216,250,250,215,PURPLE); rel(504,165,470,165,ORANGE)
    o.append(text(16,320,"1 = one row on this side (one customer) · * = many rows (many order lines)",S,MUTED))
    o.append(rect(16,332,688,62,fill="#fff4d6",stroke="#e2c46b",rx=5))
    o.append(text(26,351,'Valid Net Revenue := CALCULATE([Net Revenue], Sales[status] <> "Cancelled")',11,INK,"bold",family=MONO))
    o.append(text(26,368,"A measure is written once and recalculated for every pivot cell: by segment (via Customers),",S,INK))
    o.append(text(26,384,"by category (via Products), or year to date (via Calendar). Filters flow from the 1 side to the * side.",S,INK))
    return svg(CW,402,"".join(o))


# ---------- Figure 11.7: the stockroom model ----------
def fig_stockroom():
    o=[]
    o.append(text(16,18,"The Riverstone Stockroom: one row per day, 1 Jan to 31 Dec 2025 (Storage Box 10L)",12,INK,"bold",family=HEAD))
    cols=[("Log sheet","330 text codes",["02.01.2025|SO…","→ date, product,","qty, status"],MUTED),
          ("demand","SUMIFS by date",["units of product","101 on lines not","cancelled"],ACC),
          ("po_placed","every Monday",["1 if yesterday's","closing ≤ reorder","point (ROP)"],ORANGE),
          ("receipts","L days later",["Q units arrive at","the start of day","d + L"],PURPLE),
          ("closing","running balance",["yesterday's","closing + receipts","− demand"],GREEN)]
    W=130; G=9.5
    for i,(t,sub,lines,c) in enumerate(cols):
        x=16+i*(W+G); y=30
        o.append(box(x,y,W,100,t,c,[sub]+lines,S,lh=15))
        if i<4: o.append(arrow(x+W+1,y+50,x+W+G-1,y+50))
    xa=16+2*(W+G)+W/2; xb=16+4*(W+G)+W/2
    o.append(path(f"M{xb},134 C{xb},166 {xa},166 {xa},134",stroke=ORANGE,sw=1.6,dash="6 4")); o.append(f'<path d="M{xa},134 l-5,9 l10,0 z" fill="{ORANGE}"/>')
    o.append(text((xa+xb)/2,178,"closing feeds next Monday's decision",S,ORANGE,"bold",anchor="middle"))
    X=16; Y=196
    hdr=["date","wkday","demand","receipts","po","closing"]; wd=[82,50,58,64,32,60]
    o.append(rect(X,Y,sum(wd),20,fill=GREEN,rx=3)); cx=X
    for h,w in zip(hdr,wd): o.append(text(cx+5,Y+14,h,S,"#fff","bold",family=MONO)); cx+=w
    sample=[("2025-02-09","7","0","0","0","95"),("2025-02-10","1","0","0","1","95"),("2025-02-16","7","25","0","0","70"),("2025-02-17","1","30","250","1","290")]
    for i,r in enumerate(sample):
        yy=Y+20+i*20; cx=X
        o.append(rect(X,yy,sum(wd),20,fill=("#fdf3dc" if r[4]=="1" else "#fff"),stroke=RULE,sw=0.7))
        for v,w in zip(r,wd): o.append(text(cx+5,yy+14,v,S,INK,"bold" if r[4]=="1" else "normal",family=MONO)); cx+=w
    o.append(text(X,Y+20+4*20+15,"Shaded rows: a PO is placed (po = 1).",S,MUTED))
    notes=["ROP 100, Q 250, lead time 7 days:",
           "• 8 purchase orders",
           "• lowest closing −45, on 3 Oct",
           "• 7 days below zero; year-end closing 215",
           "• total cost ₹1,18,210",
           "  (holding + shortage + orders)",
           "17 Feb: 250 units arrive, yet another order",
           "is placed, because the rule reads Sunday's",
           "stock, not stock already on order."]
    for i,l in enumerate(notes): o.append(text(390,Y+12+i*16,l,S,GREEN if i==0 else INK,"bold" if i==0 else "normal"))
    return svg(CW,max(Y+20+4*20+24,Y+12+len(notes)*16),"".join(o))


# ---------- Figure 11.8: closing stock under two policies ----------
def stock_series():
    """Same simulation as checks/ch11_challenge_sim.py, run on the companion workbook."""
    import pandas as pd
    here=os.path.dirname(os.path.abspath(__file__))
    S_=pd.read_excel(os.path.join(here,"..","companion","ch11","ch11_practice.xlsx"),sheet_name="Sales")
    days=pd.date_range("2025-01-01","2025-12-31",freq="D")
    dem=S_[(S_.product_id==101)&(S_.status!="Cancelled")].groupby("order_date").quantity.sum()
    demand=[int(dem.get(d,0)) for d in days]
    def sim(rop,q,lead):
        rec=[0]*(len(days)+60); closing=[]; pos=0; st=300
        for i,d in enumerate(days):
            if d.weekday()==0 and i>0 and closing[i-1]<=rop: rec[i+lead]+=q; pos+=1
            st=st+rec[i]-demand[i]; closing.append(st)
        return closing,pos
    return sim(100,250,7), sim(50,150,7)


def fig_stock():
    (a,pa),(b,pb)=stock_series()
    assert (pa,pb)==(8,13) and sum(1 for v in a if v<0)==7 and sum(1 for v in b if v<0)==21
    o=[]; X0=52; Y0=34; W=652; H=220
    lo,hi=-100,600
    def px(i): return X0+i*W/364
    def py(v): return Y0+H-(v-lo)*H/(hi-lo)
    o.append(f'<rect x="{X0}" y="{py(0):.1f}" width="{W}" height="{py(lo)-py(0):.1f}" fill="#f8e1e1" opacity="0.6"/>')
    for v in range(-100,601,100):
        o.append(path(f"M{X0},{py(v):.1f} H{X0+W}",stroke=(INK if v==0 else RULE),sw=(1.2 if v==0 else 0.6)))
        o.append(text(X0-6,py(v)+4,f"{v:,}".replace("-","−"),S,MUTED,anchor="end",family=MONO))
    for m,lab in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]):
        i=(dt.date(2025,m+1,1)-dt.date(2025,1,1)).days
        o.append(text(px(i)+27,Y0+H+15,lab,S,MUTED,anchor="middle"))
    for d,c,dash,w in [(a,ACC,None,1.6),(b,ORANGE,"5 3",1.6)]:
        pts=" ".join(f"{px(i):.1f},{py(v):.1f}" for i,v in enumerate(d))
        da=f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{w}"{da}/>')
    o.append(text(X0+6,py(-65),"backorders (negative stock)",S,RED))
    o.append(text(16,18,"Storage Box 10L closing stock in 2025 (units), lead time 7 days, Monday review",12,INK,"bold",family=HEAD))
    ly=Y0+H+34
    o.append(path(f"M{X0},{ly-4} H{X0+30}",stroke=ACC,sw=2.2)); o.append(text(X0+38,ly,"solid: ROP 100, Q 250 · 8 POs, 7 negative days, total cost ₹1,18,210",S,INK))
    o.append(path(f"M{X0},{ly+14} H{X0+30}",stroke=ORANGE,sw=2.2,dash="5 3")); o.append(text(X0+38,ly+18,"dashed: ROP 50, Q 150 · 13 POs, 21 negative days, ₹84,840 (the cheapest)",S,INK))
    return svg(CW,ly+28,"".join(o))


if __name__ == "__main__":
    for name,fn in [("fig11-1-sumifs-anatomy.svg",fig_sumifs),("fig11-2-three-lookups.svg",fig_lookups),
                    ("fig11-3-pivot-areas-group-by.svg",fig_pivot),("fig11-4-dynamic-array-spill.svg",fig_spill),
                    ("fig11-5-power-query-steps.svg",fig_pq),("fig11-6-data-model-star.svg",fig_model),
                    ("fig11-7-stockroom-model.svg",fig_stockroom),("fig11-8-stockroom-policies.svg",fig_stock)]:
        open(name,"w").write(fn())
    print("ok")
