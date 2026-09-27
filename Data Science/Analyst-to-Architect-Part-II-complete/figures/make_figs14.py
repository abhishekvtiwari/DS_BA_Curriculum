# Generates the SVG figures for Chapter 14. Run: python3 make_figs14.py
# Numbers come from companion/ch14/answer_key.json and the queries verified in the chapter.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; SOFT="#e9eef4"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=11.3,mono=False):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+28} H{x} Z" fill="{c}"/>',
       text(x+12,y+19,title,12.3,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+12,y+48+i*19,l,size,INK,family=(MONO if mono else None)))
    return "".join(o)

def fig_workflow():
    o=[]
    st=[("1 Load as text","stg_orders_raw",["25,976 rows read","nothing rejected"],MUTED),
        ("2 Profile","count, pattern, range",["4 date formats","18 status spellings","6 price formats"],ACC),
        ("3 Fix","type, standardize, dedupe",["7 non-data rows out","137 duplicates out","17 values repaired"],PURPLE),
        ("4 Validate","rules that must be 0",["8 rules","20 lines quarantined"],ORANGE),
        ("5 Reconcile","against the source",["25,832 lines","25,812 identical","₹423,561,010.50"],GREEN),
        ("6 Document","cleaning log",["every rule, count,","and decision","dq_order_issues"],INK)]
    W=150; G=20
    for i,(t,sub,lines,c) in enumerate(st):
        x=30+i*(W+G)
        o.append(box(x,60,W,150,t,c,[sub,""]+lines,11))
        if i<5: o.append(arrow(x+W+2,135,x+W+G-2,135))
    o.append(text(30,36,"The cleaning workflow, with Riverstone's Q4 2025 order export",13.5,INK,"bold",family=HEAD))
    o.append(path("M960,215 C960,270 600,270 180,270 C140,270 110,250 105,215",stroke=MUTED,sw=1.4,dash="5 4"))
    o.append(f'<path d="M105,215 l-6,10 l12,0 z" fill="{MUTED}"/>')
    o.append(rect(330,256,420,26,fill="#fff",stroke=RULE,rx=13)); o.append(text(540,274,"A failed check sends you back to profiling, never to the report",11.5,MUTED,anchor="middle"))
    return svg(1060,300,"".join(o))

def fig_mapping():
    o=[]
    raw=[("Delivered",19835),("DELIVERED",697),("Dlvd",694),("Delivered␣",672),("delivered",653),
         ("Pending",1026),("Pending␣",57),("pending",52),("PENDING",39),
         ("Shipped",1004),("Shipped␣",51),("shipped",45),("SHIPPED",44),
         ("Cancelled",985),("Cxl",32),("CANCELLED",31),("Canceled",28),("cancelled",24)]
    groups={"Delivered":range(0,5),"Pending":range(5,9),"Shipped":range(9,13),"Cancelled":range(13,18)}
    col={"Delivered":GREEN,"Pending":ORANGE,"Shipped":ACC,"Cancelled":RED}
    o.append(text(30,30,"18 spellings in the export",13.5,INK,"bold",family=HEAD)); o.append(text(640,30,"4 values after the mapping table",13.5,INK,"bold",family=HEAD))
    o.append(text(330,30,"key = LOWER(TRIM(status))",12,MUTED,family=MONO))
    ys={}
    for g,rg in groups.items():
        for i in rg:
            y=50+i*21; name,n=raw[i]
            o.append(rect(30,y,230,18,fill="#fff",stroke=col[g],sw=1,rx=3))
            o.append(text(38,y+13,name,11,INK,family=MONO)); o.append(text(252,y+13,f"{n:,}",11,MUTED,anchor="end",family=MONO))
            ys.setdefault(g,[]).append(y+9)
    clean={"Delivered":22551,"Pending":1174,"Shipped":1144,"Cancelled":1100}
    for k,(g,rg) in enumerate(groups.items()):
        cy=sum(ys[g])/len(ys[g]); 
        for y in ys[g]: o.append(path(f"M262,{y} C400,{y} 500,{cy} 636,{cy}",stroke=col[g],sw=1.1))
        o.append(rect(640,cy-16,200,32,fill=col[g],rx=6)); o.append(text(652,cy+5,g,13,"#fff","bold"))
        o.append(text(830,cy+5,f"{clean[g]:,}",12,"#fff","bold",anchor="end",family=MONO))
    o.append(text(30,448,"Counts are raw data rows (duplicates still included). ␣ marks a trailing space. Unmapped values fail a validation rule instead of disappearing.",11.5,MUTED))
    return svg(880,465,"".join(o))

def fig_dupes():
    o=[]
    o.append(text(30,30,"Building a match key for customer names",13.5,INK,"bold",family=HEAD))
    steps=[("As entered","BHARAT  Stores Agra Pvt Ltd"),("LOWER","bharat  stores agra pvt ltd"),("collapse spaces, TRIM","bharat stores agra pvt ltd"),("remove legal suffix","bharat stores agra")]
    for i,(t,v) in enumerate(steps):
        x=30+i*250
        o.append(rect(x,50,228,64,fill="#fff",stroke=ACC if i<3 else GREEN,sw=1.5,rx=6))
        o.append(text(x+10,70,t,11.5,MUTED,"bold")); o.append(text(x+10,98,v,11.5,INK,family=MONO))
        if i<3: o.append(arrow(x+230,82,x+248,82))
    rows=[("match on name key only","48 groups, 96 records","every planted duplicate found; 0 false matches",GREEN),
          ("match on name key + city","46 groups, 92 records","misses 2 pairs where one record has no city",ORANGE),
          ("match on exact name","9 groups","misses every case, space, and suffix variant",RED)]
    for i,(a,b,c,col) in enumerate(rows):
        y=150+i*46
        o.append(rect(30,y,960,36,fill="#fff",stroke=col,sw=1.4,rx=6)); o.append(rect(30,y,8,36,fill=col))
        o.append(text(50,y+23,a,12.3,INK,"bold")); o.append(text(330,y+23,b,12.3,col,"bold",family=MONO)); o.append(text(560,y+23,c,12,INK))
    o.append(text(30,305,"Riverstone's CRM export: 5,027 records, 48 planted duplicates. A key finds candidates; a person confirms them before any merge.",11.8,MUTED))
    return svg(1010,320,"".join(o))

def fig_missing():
    o=[]
    o.append(text(30,30,"What to do with a missing or wrong value",13.5,INK,"bold",family=HEAD))
    q=[("Is it really missing?","'', NULL, 'N/A', '-', 'unknown', 'NULL' all mean the same thing",ACC),
       ("Can another column supply it reliably?","product from a unique list price; date from the entry timestamp",PURPLE),
       ("Is it needed for the number you report?","quantity is needed for revenue; sales rep is not",ORANGE)]
    for i,(t,sub,c) in enumerate(q):
        y=56+i*96
        o.append(rect(30,y,420,62,fill="#fff",stroke=c,sw=1.6,rx=8)); o.append(text(46,y+26,t,13,INK,"bold")); o.append(text(46,y+47,sub,11.3,MUTED))
    outs=[("Standardize to NULL","100 cities, 150 emails",ACC),("Repair, and log it","8 products, 9 dates",PURPLE),("Quarantine, and report the gap","14 quantities (+6 impossible)",ORANGE),("Keep NULL and label it","3.1% of lines have no sales rep",GREEN)]
    ys=[87,183,279,340]
    for i,((t,sub,c),y) in enumerate(zip(outs,ys)):
        o.append(rect(560,y-24,400,50,fill=c,rx=8)); o.append(text(576,y-2,t,13,"#fff","bold")); o.append(text(576,y+17,sub,11.5,"#fff"))
    o.append(arrow(452,87,556,87,ACC)); o.append(text(470,80,"yes",11,ACC,"bold"))
    o.append(arrow(240,120,240,150)); o.append(text(250,140,"then",11,MUTED))
    o.append(arrow(452,183,556,183,PURPLE)); o.append(text(470,176,"yes",11,PURPLE,"bold"))
    o.append(arrow(240,216,240,246)); o.append(text(250,236,"no",11,MUTED))
    o.append(arrow(452,279,556,279,ORANGE)); o.append(text(470,272,"yes",11,ORANGE,"bold"))
    o.append(path("M240,310 V340 H556",stroke=GREEN,sw=1.6)); o.append(f'<path d="M556,340 l-8,-5 l0,10 z" fill="{GREEN}"/>'); o.append(text(250,334,"no",11,GREEN,"bold"))
    o.append(text(30,390,"Never fill an identifier, a price, or a quantity with 0 or an average: the report would look complete and be wrong.",11.8,RED))
    return svg(990,405,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig14-1-cleaning-workflow.svg",fig_workflow),("fig14-4-status-mapping.svg",fig_mapping),("fig14-3-duplicate-match-keys.svg",fig_dupes),("fig14-2-missing-values-decisions.svg",fig_missing)]:
        open(n,"w").write(f())
    print("ok")
