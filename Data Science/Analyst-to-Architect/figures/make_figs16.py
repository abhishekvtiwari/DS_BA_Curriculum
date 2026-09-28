# Diagrams for Chapter 16 (Power BI). Run: python3 make_figs16.py
# Every figure prints at the full text width (493.2 pt), so a font of s px on a canvas W px wide prints at
# s * 493.2 / W pt. Canvases are 620 px wide and the smallest font is 9.2 px, which prints at 7.3 pt.
# The numbers drawn come from riverstone_full (see checks/ch16_check.py).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; GREY="#8a94a6"
W=620; S=9.2; B=9.8   # canvas width; smallest and body font sizes (px)

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.4,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=6
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def card(x,y,w,h,title,c,lines=(),size=B,mono=False,step=13.5):
    o=[rect(x+2,y+3,w,h,fill=SOFT,rx=6),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.4,rx=6),
       f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 H{x+w-6} a6,6 0 0 1 6,6 V{y+21} H{x} Z" fill="{c}"/>',
       text(x+8,y+15,title,10.2,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines):   # leading spaces become an indent (SVG collapses spaces)
        ind=(len(l)-len(l.lstrip()))*size*0.6
        o.append(text(x+8+ind,y+36+i*step,l.lstrip(),size,INK,family=MONO if mono else None))
    return "".join(o)

def f1():  # the pieces of Power BI
    o=[text(10,20,"The pieces of Power BI, and where each one runs",12,INK,"bold",family=HEAD)]
    o.append(card(10,34,170,104,"Power BI Desktop",ACC,["Windows, free","Power Query: get, clean","Model and relationships","DAX measures, pages","Saved as one .pbix file"]))
    o.append(card(225,34,170,104,"Power BI Service",GREEN,["In the browser","Workspaces hold content","Semantic model: data + DAX","Refresh, apps, sharing","Row-level security"]))
    o.append(card(440,34,170,104,"Readers",PURPLE,["Browser or mobile app","An app or a shared link","A licence to view","Export to Excel or PDF","Email subscriptions"]))
    o.append(arrow(182,84,221,84)); o.append(text(201,78,"publish",S,MUTED,anchor="middle"))
    o.append(arrow(397,84,436,84)); o.append(text(416,78,"share",S,MUTED,anchor="middle"))
    o.append(card(10,190,170,64,"Your data sources",GOLD,["riverstone_full database","CSV, Excel, SharePoint"]))
    o.append(card(225,190,170,64,"On-premises gateway",ORANGE,["For data inside the network","Runs on a server there"]))
    o.append(arrow(95,188,95,142)); o.append(text(101,168,"import",S,MUTED))
    o.append(arrow(310,188,310,142,ORANGE)); o.append(text(316,168,"scheduled refresh",S,MUTED))
    o.append(arrow(223,222,184,222,ORANGE)); o.append(text(203,215,"reads",S,MUTED,anchor="middle"))
    return svg(W,266,"".join(o))

def f2():  # star schema
    o=[text(10,20,"Riverstone's star schema in Power BI",12,INK,"bold",family=HEAD)]
    o.append(card(222,36,176,128,"FACT  Sales",ACC,["order_id, customer_id","product_id, sales_rep_id","order_date, status","quantity","net_revenue, product_cost","200,381 order lines"]))
    o.append(card(10,106,170,78,"DIM  Date",GOLD,["Date (key) · 1,096 rows","Year, Quarter, Month,","Financial Year · marked"]))
    o.append(card(440,36,170,78,"DIM  Customer",GREEN,["customer_id (key)","Customer, City, Segment,","Region · 5,027 rows"]))
    o.append(card(440,132,170,64,"DIM  Product",GREEN,["product_id (key)","Product, unit_cost · 8 rows"]))
    o.append(card(440,214,170,64,"DIM  Employee",GREEN,["employee_id (key)","Employee · 16 rows"]))
    o.append(card(222,214,176,64,"FACT  Targets",PURPLE,["target_month, target_revenue","36 rows, one per month"]))
    for (x1,y1,x2,y2,lx,ly) in [(182,130,219,112,184,112),(182,160,219,236,186,212),(438,75,401,90,404,72),(438,152,401,152,406,146),(438,236,401,160,400,244)]:
        o.append(arrow(x1,y1,x2,y2,MUTED,1.3)); o.append(text(lx,ly,"1 → ∗",S,MUTED))
    return svg(W,290,"".join(o))

def f3():  # filter context
    o=[text(10,20,"Where a measure's filters come from",12,INK,"bold",family=HEAD)]
    o.append(rect(10,34,196,132,fill="#fff",stroke=RULE,rx=6))
    o.append(text(20,52,"A cell in a visual",10.5,INK,"bold"))
    for i,t in enumerate(["Rows: Segment = Wholesale","Columns: Year = 2025","Slicer: Region = West"]):
        o.append(rect(20,62+i*28,176,21,fill=SOFT,stroke=ACC,sw=1,rx=4)); o.append(text(28,76.5+i*28,t,B,INK))
    o.append(text(20,156,"Together: the filter context",B,MUTED,style="italic"))
    o.append(arrow(208,100,244,100)); o.append(text(226,93,"applied to",S,MUTED,anchor="middle"))
    o.append(card(248,52,196,96,"The measure",GREEN,["Net Revenue =","  SUM ( Sales[net_revenue] )","","Evaluated once per cell"],size=S,step=13))
    o.append(arrow(446,100,480,100))
    o.append(rect(484,66,126,68,fill=GREEN,rx=6)); o.append(text(547,96,"₹10.5 crore",13,"#fff","bold",anchor="middle"))
    o.append(text(547,116,"one number",B,"#fff",anchor="middle"))
    o.append(rect(10,182,600,112,fill="#fff",stroke=PURPLE,sw=1.4,rx=6)); o.append(rect(10,182,6,112,fill=PURPLE))
    o.append(text(26,202,"CALCULATE changes the filter context before the measure runs",10.5,INK,"bold"))
    o.append(text(26,222,"CALCULATE ( [Net Revenue], Customer[Segment] = \"Retail\" )",S,INK,family=MONO))
    o.append(text(26,238,"replaces the Segment filter · REMOVEFILTERS clears it · KEEPFILTERS adds to it instead",B,MUTED))
    o.append(text(26,262,"CALCULATE ( [Net Revenue], DATESYTD ( 'Date'[Date] ) )",S,INK,family=MONO))
    o.append(text(26,278,"replaces the date filter with \"the year so far\"",B,MUTED))
    return svg(W,306,"".join(o))

REV25=[8.52,7.86,10.10,9.52,8.72,5.20,4.00,7.18,11.17,18.06,15.60,8.73]   # ₹ crore, 2025 by month
TGT25=[7.74,7.00,10.81,9.69,8.59,5.04,3.65,7.61,11.83,19.62,15.90,9.24]

def f4():  # report page wireframe
    o=[text(10,20,"The monthly pack as one report page",12,INK,"bold",family=HEAD)]
    o.append(rect(10,30,600,352,fill="#fff",stroke=RULE,rx=6))
    o.append(rect(10,30,600,34,fill=INK,rx=6)); o.append(rect(10,56,600,8,fill=INK))
    o.append(text(22,52,"Riverstone sales — 2025",12,"#fff","bold",family=HEAD))
    o.append(text(598,51,"Slicers: Year · Region · Segment",S,"#cbd5e1",anchor="end"))
    kpis=[("Net revenue","₹114.7 cr","+27.0% vs 2024",GREEN),("% of target","98.3%","gap −₹2.0 cr",ORANGE),("Gross margin","27.5%","+2.8 pts vs 2024",GREEN),("Orders","46,356","AOV ₹24,736",ACC)]
    for i,(t,v,s,c) in enumerate(kpis):
        x=22+i*146
        o.append(rect(x,74,136,58,fill=SOFT,stroke=c,sw=1.2,rx=5))
        o.append(text(x+8,88,t,S,MUTED)); o.append(text(x+8,108,v,13,INK,"bold",family=HEAD)); o.append(text(x+8,124,s,S,INK))
    # line chart: revenue (solid) and target (dashed), ₹ crore by month
    o.append(rect(22,142,344,138,fill="#fff",stroke=RULE,rx=5)); o.append(text(30,158,"Revenue and target by month, ₹ crore",B,INK,"bold"))
    x0,y0,dx,k=46,262,24,3.8
    o.append(path(f"M{x0},{y0} H{x0+11*dx+6}",stroke=RULE,sw=1))
    for v in (5,10,15,20):
        o.append(text(x0-6,y0-v*k+3,str(v),S,MUTED,anchor="end"))
    rev=" ".join(f"{'M' if i==0 else 'L'}{x0+i*dx},{y0-v*k:.1f}" for i,v in enumerate(REV25))
    tgt=" ".join(f"{'M' if i==0 else 'L'}{x0+i*dx},{y0-v*k:.1f}" for i,v in enumerate(TGT25))
    o.append(path(tgt,stroke=MUTED,sw=1.2,dash="4 3")); o.append(path(rev,stroke=ACC,sw=2))
    for i,m in enumerate("JFMAMJJASOND"):
        o.append(text(x0+i*dx,y0+12,m,S,MUTED,anchor="middle"))
    o.append(path("M300,190 H318",stroke=ACC,sw=2)); o.append(text(322,193,"revenue",S,INK))
    o.append(path("M300,206 H318",stroke=MUTED,sw=1.2,dash="4 3")); o.append(text(322,209,"target",S,INK))
    # region bars: labels in their own column, bars sized to fit the panel
    o.append(rect(376,142,222,138,fill="#fff",stroke=RULE,rx=5)); o.append(text(384,158,"Revenue by region, ₹ crore",B,INK,"bold"))
    for i,(n,v) in enumerate([("West",38.4),("South",31.9),("North",27.9),("East",14.2),("City missing",2.3)]):
        y=170+i*21
        o.append(text(452,y+11,n,S,INK,anchor="end"))
        w=v*2.9
        o.append(rect(458,y+1,w,13,fill=ACC if n!="City missing" else GREY,rx=2)); o.append(text(462+w,y+11,f"{v}",S,MUTED))
    # products and drill-through panels
    o.append(rect(22,290,344,82,fill="#fff",stroke=RULE,rx=5)); o.append(text(30,306,"Top products, share of revenue",B,INK,"bold"))
    for i,(n,v) in enumerate([("Storage Box 25L",20.2),("Food Container Set",18.7),("Storage Box 10L",17.1)]):
        y=314+i*18
        o.append(text(128,y+11,n,S,INK,anchor="end")); o.append(rect(134,y+1,v*9,12,fill=GOLD,rx=2)); o.append(text(138+v*9,y+11,f"{v}%",S,MUTED))
    o.append(rect(376,290,222,82,fill="#fff",stroke=RULE,rx=5)); o.append(text(384,306,"Behind the page",B,INK,"bold"))
    for i,t in enumerate(["Drill-through: customer detail","Tooltip page on hover","Bookmarks: revenue ⇄ margin"]):
        o.append(text(384,324+i*16,"• "+t,S,MUTED))
    return svg(W,392,"".join(o))

def f5():  # publish, refresh, secure
    o=[text(10,20,"From a .pbix file to a report the branches trust",12,INK,"bold",family=HEAD)]
    steps=[("1  Build",ACC,["In Desktop:","Power Query,","model, DAX,","pages; test","with View as"]),
           ("2  Publish",GREEN,["To a shared","workspace;","model and","report land in","the Service"]),
           ("3  Refresh",ORANGE,["Credentials,","a schedule","(8 a day Pro,","48 PPU); a","gateway if needed"]),
           ("4  Secure",PURPLE,["Roles in the","model; map","people to","roles; Test","as role"]),
           ("5  Deliver",GOLD,["Publish an","app, or share","the report;","subscriptions,","usage metrics"])]
    for i,(t,c,lines) in enumerate(steps):
        x=10+i*122
        o.append(card(x,34,110,106,t,c,lines,size=S,step=13))
        if i<4: o.append(arrow(x+111,87,x+120,87))
    o.append(rect(10,156,600,86,fill="#fff",stroke=RULE,rx=6))
    o.append(text(22,174,"What breaks most often",10.5,INK,"bold"))
    items=[("Refresh fails:","credentials or the gateway",RED),("Numbers differ:","filters, not DAX",ORANGE),
           ("Viewers can't open it:","a licence is missing",PURPLE),("The report is slow:","too many visuals",ACC)]
    for i,(a,b,c) in enumerate(items):
        x=22+(i%2)*296; y=184+(i//2)*28
        o.append(rect(x,y,5,24,fill=c)); o.append(text(x+12,y+10,a,B,INK,"bold")); o.append(text(x+12,y+22,b,S,MUTED))
    return svg(W,252,"".join(o))

def f6():  # RLS
    o=[text(10,20,"Row-level security: one report, four views",12,INK,"bold",family=HEAD)]
    o.append(card(10,34,262,126,"Role \"Region manager\" on Customer",PURPLE,
                  ["Customer[Region]","  IN CALCULATETABLE (","    VALUES ( UserRegion[region] ),","    UserRegion[email]","      = USERPRINCIPALNAME () )"],size=S,mono=True,step=14))
    o.append(text(18,154,"Leaders: role \"All regions\", rule TRUE ()",S,PURPLE,"bold"))
    o.append(card(316,34,294,126,"UserRegion (a small hidden table)",ACC,
                  ["pooja.desai@…    →  West","pooja.desai@…    →  East","arjun.nair@…     →  South","sandeep.gill@…   →  North","Anita Rao: the All regions role"],size=S,step=15))
    o.append(arrow(314,97,276,97)); o.append(text(295,90,"reads",S,MUTED,anchor="middle"))
    o.append(text(10,184,"What each person sees in the same report (2025 net revenue):",10.5,INK,"bold"))
    rows=[("Anita Rao (All regions)","₹114.7 cr","all 4,599 customers"),("Pooja Desai (West + East)","₹52.6 cr","West ₹38.4 cr + East ₹14.2 cr"),
          ("Arjun Nair (South)","₹31.9 cr","1,289 customers"),("Sandeep Gill (North)","₹27.9 cr","1,127 customers")]
    for i,(who,v,d) in enumerate(rows):
        y=194+i*28
        o.append(rect(10,y,600,23,fill="#fff",stroke=RULE,rx=4)); o.append(rect(10,y,5,23,fill=GREEN if i==0 else ACC))
        o.append(text(24,y+15.5,who,B,INK,"bold")); o.append(text(236,y+15.5,v,B,INK,"bold",family=MONO)); o.append(text(330,y+15.5,d,B,MUTED))
    o.append(text(10,322,"₹2.3 crore from customers with no city has no region: only the All regions role sees it.",B,MUTED))
    return svg(W,334,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig16-1-power-bi-pieces.svg",f1),("fig16-2-star-schema.svg",f2),("fig16-3-filter-context.svg",f3),
                ("fig16-4-report-page.svg",f4),("fig16-5-publish-refresh.svg",f5),("fig16-6-row-level-security.svg",f6)]:
        open(n,"w").write(f())
    print("ok")
