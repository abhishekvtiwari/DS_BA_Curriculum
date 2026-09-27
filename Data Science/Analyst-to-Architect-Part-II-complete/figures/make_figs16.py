# Diagrams for Chapter 16 (Power BI). Run: python3 make_figs16.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def card(x,y,w,h,title,c,lines=(),size=11.2,fill="#fff"):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8),rect(x,y,w,h,fill=fill,stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+26} H{x} Z" fill="{c}"/>',
       text(x+11,y+18,title,11.8,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+11,y+45+i*17,l,size,INK))
    return "".join(o)

def f1():  # the pieces of Power BI
    o=[text(30,32,"The pieces of Power BI, and where each one runs",14.5,INK,"bold",family=HEAD)]
    o.append(card(30,60,250,150,"Power BI Desktop (Windows, free)",ACC,["Connect and transform (Power Query)","Model tables and relationships","Write DAX measures","Design report pages","Saves one .pbix file"],10.8))
    o.append(card(330,60,250,150,"Power BI Service (browser)",GREEN,["Workspace holds the content","Semantic model (the data + DAX)","Reports and dashboards","Scheduled refresh, apps, sharing","Row-level security applied"],10.8))
    o.append(card(630,60,230,150,"Readers",PURPLE,["Browser or mobile app","An app or a shared link","Licence needed to view","Export to Excel or PDF","Subscriptions by email"],10.8))
    o.append(arrow(284,120,326,120)); o.append(text(288,112,"publish",10.5,MUTED))
    o.append(arrow(584,120,626,120)); o.append(text(590,112,"share",10.5,MUTED))
    o.append(card(30,250,250,120,"Your data sources",GOLD,["riverstone_full (PostgreSQL/MySQL)","CSV, Excel, SharePoint","Cloud services (APIs)"],10.8))
    o.append(card(330,250,250,120,"On-premises data gateway",ORANGE,["Only for data inside the network","Installed on a server that","can reach the database"],10.8))
    o.append(arrow(155,246,155,214)); o.append(text(160,232,"import or query",10.5,MUTED))
    o.append(arrow(330,310,286,310,ORANGE)); o.append(arrow(455,246,455,214,ORANGE)); o.append(text(462,232,"scheduled refresh",10.5,MUTED))
    o.append(text(30,395,"Desktop builds it; the Service runs it on a schedule and shares it. Nothing you build is visible to anyone until you publish.",11.5,MUTED))
    return svg(890,412,"".join(o))

def f2():  # star schema
    o=[text(30,32,"Riverstone's star schema in Power BI",14.5,INK,"bold",family=HEAD)]
    fact=["order_item_id","order_id  →  (degenerate)","customer_id","product_id","sales_rep_id","order_date","quantity, unit_price,","discount_pct","209,006 rows"]
    o.append(card(340,150,250,200,"FACT  Sales",ACC,fact,10.6))
    o.append(card(40,60,230,120,"DIM  Date",GOLD,["date (key)  ·  1,096 rows","year, quarter, month no.,","month name, is_weekend","Marked as date table"],10.4))
    o.append(card(660,60,230,120,"DIM  Customer",GREEN,["customer_id (key)","customer_name, city, region,","segment, signup_date","5,027 rows"],10.4))
    o.append(card(40,330,230,110,"DIM  Product",GREEN,["product_id (key)","product_name, category,","unit_price, unit_cost  ·  8 rows"],10.4))
    o.append(card(660,330,230,110,"DIM  Employee",GREEN,["employee_id (key)","employee_name, job_title,","manager  ·  16 rows"],10.4))
    o.append(card(340,430,250,90,"FACT  Targets",PURPLE,["target_month (→ Date)","target_revenue  ·  36 rows"],10.4))
    for (x1,y1,x2,y2) in [(272,140,338,205),(658,140,592,205),(272,360,338,300),(658,360,592,300),(465,428,465,352)]:
        o.append(arrow(x1,y1,x2,y2,MUTED,1.5))
    o.append(text(285,150,"1 → ∗",10.5,MUTED)); o.append(text(610,150,"1 → ∗",10.5,MUTED))
    o.append(text(285,352,"1 → ∗",10.5,MUTED)); o.append(text(610,352,"1 → ∗",10.5,MUTED)); o.append(text(478,400,"1 → ∗",10.5,MUTED))
    o.append(text(30,548,"One row per order line in the fact table; one row per thing in each dimension. Filters flow from the dimensions down into the facts,",11.5,MUTED))
    o.append(text(30,566,"which is why every table joins to Date rather than to each other. Both fact tables use the Date dimension, at different grains.",11.5,MUTED))
    return svg(920,584,"".join(o))

def f3():  # filter context
    o=[text(30,32,"Where a measure's filters come from",14.5,INK,"bold",family=HEAD)]
    o.append(rect(30,60,300,190,fill="#fff",stroke=RULE,rx=8))
    o.append(text(46,84,"A cell in a visual",12.5,INK,"bold"))
    rows=[("Rows: Segment = Wholesale",ACC),("Columns: Year = 2025",ACC),("Slicer: Region = West",ACC),("Page filter: Status ≠ Cancelled",ACC)]
    for i,(t,c) in enumerate(rows):
        o.append(rect(46,102+i*32,268,24,fill=SOFT,stroke=c,sw=1,rx=4)); o.append(text(56,118+i*32,t,10.8,INK))
    o.append(text(46,238,"Together: the filter context",11.5,MUTED,style="italic"))
    o.append(arrow(334,155,392,155)); o.append(text(336,146,"applied to",10.5,MUTED))
    o.append(card(400,80,320,150,"The measure",GREEN,["Net Revenue =","  SUMX(Sales,","    Sales[quantity] * Sales[unit_price]","    * (1 - Sales[discount_pct] / 100))","","Evaluated once per cell"],10.4))
    o.append(arrow(724,155,782,155)); o.append(rect(790,120,160,70,fill=GREEN,rx=8)); o.append(text(870,152,"₹8.5 crore",14,"#fff","bold",anchor="middle"))
    o.append(text(870,174,"one number",10.5,"#fff",anchor="middle"))
    o.append(rect(30,282,920,120,fill="#fff",stroke=PURPLE,sw=1.6,rx=8)); o.append(rect(30,282,8,120,fill=PURPLE))
    o.append(text(52,308,"CALCULATE changes the filter context before the measure runs",12.8,INK,"bold"))
    o.append(text(52,334,"CALCULATE([Net Revenue], Customer[segment] = \"Retail\")",11.2,INK,family=MONO))
    o.append(text(52,356,"replaces the Segment filter  ·  REMOVEFILTERS() clears it  ·  KEEPFILTERS() adds to it instead of replacing",11,MUTED))
    o.append(text(52,378,"CALCULATE([Net Revenue], DATESYTD(Date[date])) replaces the date filter with \"year so far\"",11,MUTED))
    return svg(980,420,"".join(o))

def f4():  # report page wireframe
    o=[text(30,30,"The monthly pack as one report page",14.5,INK,"bold",family=HEAD)]
    o.append(rect(30,50,900,470,fill="#fff",stroke=RULE,rx=8))
    o.append(rect(30,50,900,52,fill=INK,rx=8)); o.append(rect(30,90,900,12,fill=INK))
    o.append(text(48,82,"Riverstone sales — December 2025",15,"#fff","bold",family=HEAD))
    o.append(text(700,74,"Slicers:  Year  ·  Region  ·  Segment",11,"#cbd5e1"))
    kpis=[("Net revenue","₹114.7 cr","+27.0% vs LY",GREEN),("% of target","98.3%","−₹2.0 cr",ORANGE),("Gross margin","27.5%","+2.8 pts",GREEN),("Orders","46,356","AOV ₹24,736",ACC)]
    for i,(t,v,s,c) in enumerate(kpis):
        x=48+i*218
        o.append(rect(x,118,200,74,fill=SOFT,stroke=c,sw=1.4,rx=6))
        o.append(text(x+12,138,t,10.8,MUTED)); o.append(text(x+12,163,v,17,INK,"bold",family=HEAD)); o.append(text(x+12,182,s,10.5,c))
    o.append(rect(48,208,560,180,fill="#fff",stroke=RULE,rx=6)); o.append(text(60,230,"Revenue and target by month (line + dashed target)",11.5,INK,"bold"))
    o.append(path("M70,360 L110,350 L150,330 L190,336 L230,346 L270,370 L310,376 L350,352 L390,320 L430,270 L470,292 L510,344",stroke=ACC,sw=2.4))
    o.append(path("M70,352 L110,346 L150,322 L190,330 L230,342 L270,368 L310,368 L350,344 L390,312 L430,258 L470,286 L510,336",stroke=MUTED,sw=1.3,dash="5 4"))
    o.append(rect(624,208,290,180,fill="#fff",stroke=RULE,rx=6)); o.append(text(636,230,"Revenue by region (sorted bars)",11.5,INK,"bold"))
    for i,(n,w) in enumerate([("West",250),("South",208),("North",182),("East",93),("City missing",15)]):
        y=246+i*27; o.append(rect(636,y,w,17,fill=ACC if n!="City missing" else "#b8c0cc",rx=3)); o.append(text(636+w+6,y+13,n,10,MUTED))
    o.append(rect(48,404,560,100,fill="#fff",stroke=RULE,rx=6)); o.append(text(60,426,"Top products and segments (bar + matrix)",11.5,INK,"bold"))
    for i in range(4):
        o.append(rect(60,436+i*16,300-i*55,10,fill=GOLD,rx=2))
    o.append(rect(624,404,290,100,fill="#fff",stroke=RULE,rx=6)); o.append(text(636,426,"Customers needing attention",11.5,INK,"bold"))
    o.append(text(636,448,"drill-through → customer detail page",10.5,MUTED)); o.append(text(636,468,"tooltip page on hover",10.5,MUTED))
    o.append(text(636,488,"bookmarks: revenue ⇄ margin view",10.5,MUTED))
    o.append(text(30,540,"Four cards answer \"how are we doing?\" in one line; the visuals below answer \"why?\". Everything else lives on drill-through pages.",11.5,MUTED))
    return svg(960,558,"".join(o))

def f5():  # publish, refresh, secure
    o=[text(30,32,"From a .pbix file to a report the branches trust",14.5,INK,"bold",family=HEAD)]
    steps=[("1  Build",ACC,["Desktop: Power Query,","model, DAX, pages","Test with the roles you","defined (View as)"]),
           ("2  Publish",GREEN,["Publish to a workspace","Semantic model + report","land in the Service"]),
           ("3  Refresh",ORANGE,["Set credentials","Schedule (8/day Pro,","48/day PPU)","Gateway for on-prem data"]),
           ("4  Secure",PURPLE,["Roles: East sees East","Members mapped to roles","Test as a real user"]),
           ("5  Deliver",GOLD,["Publish an app","Or share the report","Subscriptions, alerts","Usage metrics"])]
    for i,(t,c,lines) in enumerate(steps):
        x=30+i*182
        o.append(card(x,66,166,150,t,c,lines,10.2))
        if i<4: o.append(arrow(x+168,140,x+178,140))
    o.append(rect(30,240,910,96,fill="#fff",stroke=RULE,rx=8))
    o.append(text(46,266,"What breaks most often",12.5,INK,"bold"))
    items=[("Refresh fails: credentials or gateway",RED),("Numbers differ: filters, not DAX",ORANGE),("Viewers can't open it: licence",PURPLE),("Slow report: too many visuals",ACC)]
    for i,(t,c) in enumerate(items):
        x=46+i*228; o.append(rect(x,282,8,36,fill=c)); o.append(text(x+16,298,t.split(':')[0]+":",11,INK,"bold")); o.append(text(x+16,314,t.split(': ')[1],10.6,MUTED))
    return svg(970,352,"".join(o))

def f6():  # RLS
    o=[text(30,32,"Row-level security: one report, four views",14.5,INK,"bold",family=HEAD)]
    o.append(card(30,66,260,140,"Role \"Region manager\"",PURPLE,["Table: Customer","DAX rule:","[region] = LOOKUPVALUE(","  UserRegion[region],","  UserRegion[email],","  USERPRINCIPALNAME())"],10.2))
    o.append(card(330,66,250,140,"UserRegion (a small table)",ACC,["arjun@…  →  South","pooja@…  →  West and East","sandeep@…  →  North","anita@…  →  (no role: sees all)"],10.2))
    o.append(arrow(294,136,326,136))
    o.append(text(30,236,"What each person sees when they open the same report (2025 net revenue):",12,INK,"bold"))
    rows=[("Anita Rao (no role)","₹114.7 cr","all 4,599 customers",GREEN),("Pooja Desai (West + East)","₹52.6 cr","West ₹38.4 cr + East ₹14.2 cr",ACC),
          ("Arjun Nair (South)","₹31.9 cr","1,289 customers",ACC),("Sandeep Gill (North)","₹27.9 cr","1,127 customers",ACC)]
    for i,(who,v,d,c) in enumerate(rows):
        y=256+i*38
        o.append(rect(30,y,900,30,fill="#fff",stroke=RULE,rx=5)); o.append(rect(30,y,7,30,fill=c))
        o.append(text(50,y+20,who,11.5,INK,"bold")); o.append(text(320,y+20,v,11.5,c,"bold",family=MONO)); o.append(text(460,y+20,d,11,MUTED))
    o.append(text(30,432,"₹2.3 crore of 2025 revenue belongs to customers with no city, so it has no region: it appears only in the unfiltered view.",11.3,MUTED))
    o.append(text(30,450,"Rules filter the dimension; the filter flows to the facts. Security lives in the semantic model, not in the report pages.",11.3,MUTED))
    return svg(960,468,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig16-1-power-bi-pieces.svg",f1),("fig16-2-star-schema.svg",f2),("fig16-3-filter-context.svg",f3),
                ("fig16-4-report-page.svg",f4),("fig16-5-publish-refresh.svg",f5),("fig16-6-row-level-security.svg",f6)]:
        open(n,"w").write(f())
    print("ok")
