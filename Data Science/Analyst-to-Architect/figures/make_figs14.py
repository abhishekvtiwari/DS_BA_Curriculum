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
    # 2 rows of 3, snake order (1-2-3, then 4-5-6 right to left), so text prints at >= 7 pt; the loop goes to box 2
    o=[]
    st=[("1 Load as text","stg_orders_raw",["25,976 rows read","nothing rejected"],MUTED),
        ("2 Profile","count, pattern, range",["4 date formats","18 status spellings","6 price formats"],ACC),
        ("3 Fix","type, standardize, dedupe",["7 non-data rows out","137 duplicates out","17 values repaired"],PURPLE),
        ("4 Validate","rules that must be 0",["8 rules","20 lines quarantined"],ORANGE),
        ("5 Reconcile","against the source",["25,832 lines","25,812 identical","₹42,35,61,010.50"],GREEN),
        ("6 Document","cleaning log",["every rule, count,","and decision","dq_order_issues"],INK)]
    W=200; G=40; H=140; X0=20; Y1=50; Y2=270
    xs=[X0, X0+W+G, X0+2*(W+G)]
    pos=[(xs[0],Y1),(xs[1],Y1),(xs[2],Y1),(xs[2],Y2),(xs[1],Y2),(xs[0],Y2)]
    for (t,sub,lines,c),(x,y) in zip(st,pos):
        o.append(box(x,y,W,H,t,c,[sub,""]+lines,11.2))
    o.append(arrow(xs[0]+W+3,Y1+70,xs[1]-3,Y1+70)); o.append(arrow(xs[1]+W+3,Y1+70,xs[2]-3,Y1+70))
    o.append(arrow(xs[2]+W/2,Y1+H+6,xs[2]+W/2,Y2-4))
    o.append(arrow(xs[2]-3,Y2+70,xs[1]+W+3,Y2+70)); o.append(arrow(xs[1]-3,Y2+70,xs[0]+W+3,Y2+70))
    # failed check: from Validate (4) and Reconcile (5) back up to Profile (2)
    o.append(path(f"M{xs[1]+W/2},{Y2-2} V{Y1+H+10}",stroke=RED,sw=1.6,dash="5 4"))
    o.append(f'<path d="M{xs[1]+W/2},{Y1+H+6} l-6,10 l12,0 z" fill="{RED}"/>')
    o.append(path(f"M{xs[2]+W*0.25},{Y2-2} V{Y2-30} H{xs[1]+W/2}",stroke=RED,sw=1.6,dash="5 4"))
    o.append(text(xs[1]+W/2-8,Y1+H+36,"a failed check goes back",11.2,RED,"bold",anchor="end"))
    o.append(text(xs[1]+W/2-8,Y1+H+52,"to 2 Profile, never to the report",11.2,RED,"bold",anchor="end"))
    o.append(text(X0,30,"The cleaning workflow, with Riverstone's Q4 2025 order export",13.5,INK,"bold",family=HEAD))
    return svg(700,Y2+H+14,"".join(o))

def fig_mapping():
    o=[]
    raw=[("Delivered",19835),("DELIVERED",697),("Dlvd",694),("Delivered␣",672),("delivered",653),
         ("Pending",1026),("Pending␣",57),("pending",52),("PENDING",39),
         ("Shipped",1004),("Shipped␣",51),("shipped",45),("SHIPPED",44),
         ("Cancelled",985),("Cxl",32),("CANCELLED",31),("Canceled",28),("cancelled",24)]
    groups={"Delivered":range(0,5),"Pending":range(5,9),"Shipped":range(9,13),"Cancelled":range(13,18)}
    col={"Delivered":GREEN,"Pending":ORANGE,"Shipped":ACC,"Cancelled":RED}
    o.append(text(30,30,"18 spellings in the export",13.5,INK,"bold",family=HEAD)); o.append(text(620,30,"4 values after mapping",13.5,INK,"bold",family=HEAD))
    o.append(text(300,56,"key = LOWER(TRIM(status))",12.6,MUTED,family=MONO))
    ys={}
    for g,rg in groups.items():
        for i in rg:
            y=70+i*23; name,n=raw[i]
            o.append(rect(30,y,240,20,fill="#fff",stroke=col[g],sw=1,rx=3))
            o.append(text(38,y+15,name,12.6,INK,family=MONO)); o.append(text(262,y+15,f"{n:,}",12.6,MUTED,anchor="end",family=MONO))
            ys.setdefault(g,[]).append(y+10)
    clean={"Delivered":22551,"Pending":1174,"Shipped":1144,"Cancelled":1100}
    for k,(g,rg) in enumerate(groups.items()):
        cy=sum(ys[g])/len(ys[g])
        for y in ys[g]: o.append(path(f"M272,{y} C400,{y} 500,{cy} 616,{cy}",stroke=col[g],sw=1.1))
        o.append(rect(620,cy-17,230,34,fill=col[g],rx=6)); o.append(text(632,cy+5,g,13.5,"#fff","bold"))
        o.append(text(840,cy+5,f"{clean[g]:,}",13,"#fff","bold",anchor="end",family=MONO))
    o.append(text(30,512,"Counts are raw data rows (duplicates still included). ␣ marks a trailing space.",12.6,MUTED))
    o.append(text(30,531,"Unmapped values fail a validation rule instead of disappearing.",12.6,MUTED))
    return svg(880,545,"".join(o))

def fig_dupes():
    # steps in the same order as the SQL: remove suffix, collapse spaces, LOWER
    o=[]
    o.append(text(20,28,"Building a match key for customer names",13.5,INK,"bold",family=HEAD))
    steps=[("As entered","BHARAT\u00a0\u00a0Stores Agra Pvt Ltd"),("1 remove legal suffix","BHARAT\u00a0\u00a0Stores Agra"),
           ("2 collapse spaces (two spaces become one)","BHARAT Stores Agra"),("3 LOWER","bharat stores agra")]
    for i,(t,v) in enumerate(steps):
        x=20+(i%2)*350; y=44+(i//2)*72
        o.append(rect(x,y,310,58,fill="#fff",stroke=ACC if i<3 else GREEN,sw=1.5,rx=6))
        o.append(text(x+10,y+21,t,11.5,MUTED,"bold")); o.append(text(x+10,y+45,v,12,INK,family=MONO))
    o.append(arrow(332,73,368,73)); o.append(path("M525,104 V110 H175 V114",stroke=MUTED,sw=1.6)); o.append(f'<path d="M175,116 l-5,-8 l10,0 z" fill="{MUTED}"/>')
    o.append(arrow(332,145,368,145))
    rows=[("match on name key only","48 groups, 96 records","every planted duplicate found; 0 false matches",GREEN,"✓"),
          ("match on name key + city","46 groups, 92 records","misses 2 pairs where one record has no city",ORANGE,"!"),
          ("match on exact name","9 groups","misses every case, space, and suffix variant",RED,"✗")]
    for i,(a,b,c,col,mk) in enumerate(rows):
        y=200+i*56
        o.append(rect(20,y,660,48,fill="#fff",stroke=col,sw=1.4,rx=6)); o.append(rect(20,y,24,48,fill=col))
        o.append(text(32,y+30,mk,14,"#fff","bold",anchor="middle"))
        o.append(text(56,y+20,a,12,INK,"bold")); o.append(text(660,y+20,b,12,col,"bold",anchor="end",family=MONO)); o.append(text(56,y+40,c,11.5,INK))
    o.append(text(20,388,"Riverstone's CRM export: 5,027 records, 48 planted duplicate pairs.",11.5,MUTED))
    o.append(text(20,406,"A key finds candidates; a person confirms them before any merge.",11.5,MUTED))
    return svg(700,418,"".join(o))

def fig_missing():
    o=[]
    o.append(text(20,28,"What to do with a missing or wrong value",13.5,INK,"bold",family=HEAD))
    q=[("Is it really missing?",["'', NULL, 'N/A', '-', 'unknown', 'NULL'","all mean the same thing"],ACC),
       ("Can another column supply it reliably?",["product from a unique list price;","date from the entry timestamp"],PURPLE),
       ("Is it needed for the number you report?",["quantity is needed for revenue;","sales rep is not"],ORANGE)]
    for i,(t,subs,c) in enumerate(q):
        y=48+i*100
        o.append(rect(20,y,330,72,fill="#fff",stroke=c,sw=1.6,rx=8)); o.append(text(32,y+22,t,12,INK,"bold"))
        for j,sub in enumerate(subs): o.append(text(32,y+42+j*17,sub,11,MUTED))
    outs=[("1 Standardize to NULL","100 cities, 150 emails",ACC),("2 Repair, and log it","8 products, 9 dates",PURPLE),
          ("3 Quarantine, report the gap","14 quantities (+6 impossible)",ORANGE),("4 Keep NULL and label it","3.1% of lines have no rep",GREEN)]
    ys=[84,184,284,356]
    for (t,sub,c),y in zip(outs,ys):
        o.append(rect(440,y-26,245,52,fill=c,rx=8)); o.append(text(452,y-5,t,12,"#fff","bold")); o.append(text(452,y+15,sub,11,"#fff"))
    o.append(arrow(352,84,436,84,ACC)); o.append(text(362,77,"yes",11,ACC,"bold"))
    o.append(arrow(185,121,185,146)); o.append(text(195,138,"then",11,MUTED))
    o.append(arrow(352,184,436,184,PURPLE)); o.append(text(362,177,"yes",11,PURPLE,"bold"))
    o.append(arrow(185,221,185,246)); o.append(text(195,238,"no",11,MUTED))
    o.append(arrow(352,284,436,284,ORANGE)); o.append(text(362,277,"yes",11,ORANGE,"bold"))
    o.append(path("M185,321 V356 H432",stroke=GREEN,sw=1.6)); o.append(f'<path d="M436,356 l-8,-5 l0,10 z" fill="{GREEN}"/>'); o.append(text(195,348,"no",11,GREEN,"bold"))
    o.append(text(20,410,"Never fill an identifier, a price, or a quantity with 0 or an average:",11.5,RED,"bold"))
    o.append(text(20,428,"the report would look complete and be wrong.",11.5,RED,"bold"))
    return svg(700,440,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig14-1-cleaning-workflow.svg",fig_workflow),("fig14-4-status-mapping.svg",fig_mapping),("fig14-3-duplicate-match-keys.svg",fig_dupes),("fig14-2-missing-values-decisions.svg",fig_missing)]:
        open(n,"w").write(f())
    print("ok")
