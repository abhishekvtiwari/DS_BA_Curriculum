# Generates the SVG figures for Chapter 28. Run: python3 make_figs28.py
# Numbers come from the chapter's runs (checks/ch28_perf_log.txt and the SQL outputs in the manuscript).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def box(x,y,w,h,title,sub=None,color=ACC,fill="#fff"):
    o=[rect(x,y,w,h,fill=fill,stroke=color,sw=1.6,rx=7), text(x+w/2,y+(20 if sub else h/2+5),title,12.5,INK,"bold",anchor="middle")]
    if sub: o.append(text(x+w/2,y+37,sub,11,MUTED,anchor="middle"))
    return "".join(o)

def fig_org():
    o=[text(30,32,"staff: each row points to its manager (manager_id)",14,INK,"bold",family=HEAD)]
    W,Hb=138,44
    lv={1:70,2:160,3:250,4:340,5:430}
    colors={1:INK,2:ACC,3:PURPLE,4:GREEN,5:ORANGE}
    pos={}
    nodes=[(100,"Arvind Kapoor","Managing Director",1,None),
           (110,"Anita Rao","Sales Head",2,100),(130,"Harpreet Sethi","Head of Production",2,100),(120,"Suresh Menon","Finance Manager",2,100),(150,"Mahesh Yadav","Warehouse & Dispatch",2,100),
           (111,"Vikram Singh","Sales Mgr, Key Accounts",3,110),(112,"Farah Khan","Sales Executive",3,110),(131,"Ramesh Patil","Plant Mgr, Taloja",3,130),(132,"Kiran Bhosale","Plant Mgr, Chakan",3,130),
           (114,"Neha Kulkarni","Sales Executive",4,111),(115,"Rahul Mehta","Sales Executive",4,111),(133,"Ajay Kumar","Shift Supervisor",4,131),(135,"Swati Joshi","Shift Supervisor",4,132),
           (136,"Gopal Sahu","Machine Operator",5,133),(137,"Sunita Pawar","Machine Operator",5,133),(138,"Farid Shaikh","Machine Operator",5,135)]
    xs={100:430, 110:150,130:560,120:870,150:1010-138, 111:70,112:230,131:470,132:650, 114:20,115:170,133:430,135:650, 136:350,137:500,138:680}
    xs[150]=870; xs[120]=720
    for sid,n,t,l,m in nodes: pos[sid]=(xs[sid],lv[l])
    for sid,n,t,l,m in nodes:
        if m:
            x1,y1=pos[m]; x2,y2=pos[sid]
            o.append(path(f"M{x1+W/2},{y1+Hb} V{(y1+Hb+y2)/2} H{x2+W/2} V{y2}",stroke=RULE,sw=1.6))
    for sid,n,t,l,m in nodes:
        x,y=pos[sid]; o.append(box(x,y,W,Hb,n,t,color=colors[l]))
    for l,y in lv.items(): o.append(text(1100,y+27,f"level {l}",11.5,colors[l],"bold",anchor="end"))
    o.append(text(30,510,"The anchor row is the person with no manager (level 1). Each pass of the recursive part adds the next level down,",12,MUTED))
    o.append(text(30,530,"and the query stops when a pass finds nobody new. The chart shows 16 of the 35 people (the regional sales team is left out); the query returns all of them.",12,MUTED))
    return svg(1110,545,"".join(o))

def fig_bom():
    o=[text(30,32,"Bill of materials: quantities multiply as you go down",14,INK,"bold",family=HEAD)]
    o.append(box(390,55,220,46,"Garden Chair (106)","1 unit",color=INK))
    lvl1=[(40,"Seat shell","× 1"),(290,"Steel frame","× 1"),(540,"Product label","× 1  (material)"),(790,"Shipping carton","× 1  (material)")]
    for x,n,q in lvl1:
        o.append(path(f"M500,101 V125 H{x+100} V145",stroke=RULE,sw=1.6)); o.append(box(x,145,200,46,n,q,color=ACC))
    o.append(path("M140,191 V215 H80 V235",stroke=RULE,sw=1.6)); o.append(path("M140,191 V215 H220 V235",stroke=RULE,sw=1.6))
    o.append(box(10,235,140,46,"PP granules","× 2.2 kg",color=GREEN)); o.append(box(158,235,124,46,"Masterbatch","× 0.08 kg",color=GREEN))
    for x in [370,500,640]: o.append(path(f"M390,191 V215 H{x} V235",stroke=RULE,sw=1.6))
    o.append(box(305,235,130,46,"Leg assembly","× 2",color=ACC)); o.append(box(440,235,120,46,"Steel tube","× 1.0 kg",color=GREEN)); o.append(box(570,235,140,46,"Fastener pack","× 1",color=GREEN))
    o.append(path("M370,281 V305 H320 V325",stroke=RULE,sw=1.6)); o.append(path("M370,281 V305 H450 V325",stroke=RULE,sw=1.6))
    o.append(box(250,325,140,46,"Steel tube","1.2 kg × 2 = 2.4 kg",color=ORANGE)); o.append(box(400,325,140,46,"Fastener pack","1 × 2 = 2",color=ORANGE))
    o.append(rect(730,225,290,160,fill="#f6f9fc",stroke=RULE,rx=6))
    for i,l in enumerate(["Material cost of one chair",
                          "PP 2.2 kg × ₹110 = ₹242.00",
                          "Masterbatch 0.08 kg × ₹260 = ₹20.80",
                          "Steel tube 3.4 kg × ₹95 = ₹323.00",
                          "Fasteners 3 × ₹14 = ₹42.00",
                          "Label ₹2 + carton ₹18 = ₹20.00","Total ₹647.80"]):
        o.append(text(745,248+i*21,l,11.5,INK,"bold" if i in (0,6) else "normal"))
    o.append(text(30,400,"Orange boxes are found on the third pass: the recursive CTE multiplies each child's quantity by its parent's running quantity.",12,MUTED))
    return svg(1040,415,"".join(o))

def fig_scan_index():
    o=[text(30,32,"Finding customer 2718's 40 orders among 714,285",14,INK,"bold",family=HEAD)]
    # left: seq scan
    o.append(text(30,66,"Sequential scan: read every row",13,RED,"bold"))
    for r in range(10):
        for c in range(16):
            hit = (r,c) in [(2,5),(7,11)]
            o.append(rect(30+c*24,80+r*20,20,15,fill=("#f3c9c9" if hit else "#eef1f5"),stroke=RULE,sw=0.6))
    o.append(path("M30,292 H410",stroke=RED,sw=2.5)); o.append(path("M402,286 L412,292 L402,298",stroke=RED,sw=2.5))
    o.append(text(30,318,"714,285 rows checked, 714,245 thrown away",12,INK))
    o.append(text(30,340,"median 30.11 ms",15,RED,"bold"))
    # right: btree
    X=520
    o.append(text(X,66,"B-tree index: follow the sorted keys",13,GREEN,"bold"))
    o.append(box(X+170,82,150,36,"root: 1 … 5000",color=GREEN))
    for i,(lab) in enumerate(["1 … 1700","1701 … 3400","3401 … 5000"]):
        x=X+20+i*165; o.append(path(f"M{X+245},118 V132 H{x+65} V145",stroke=RULE,sw=1.5))
        o.append(box(x,145,130,34,lab,color=(GREEN if i==1 else RULE)))
    for i,lab in enumerate(["2701 … 2717","2718 … 2735","2736 … 2752"]):
        x=X+120+i*125; o.append(path(f"M{X+250},179 V193 H{x+55} V205",stroke=RULE,sw=1.5))
        o.append(box(x,205,110,34,lab,color=(GREEN if i==1 else RULE)))
    o.append(path(f"M{X+300},239 V258",stroke=GREEN,sw=2)); o.append(box(X+180,258,240,34,"40 row pointers → 40 rows",color=GREEN))
    o.append(text(X,318,"a few index pages, then 40 table pages (Heap Blocks: 40)",12,INK))
    o.append(text(X,340,"median 0.08 ms",15,GREEN,"bold"))
    o.append(text(30,380,"PostgreSQL 16 on a 1-vCPU sandbox, riverstone_perf. Your times will differ; the ratio is what matters.",11.5,MUTED,style="italic"))
    return svg(1040,395,"".join(o))

def fig_plan():
    o=[text(30,32,"Reading EXPLAIN ANALYZE: from the inside out (customer 2718's revenue, no index on order_items.order_id)",14,INK,"bold",family=HEAD)]
    lines=[("Aggregate (actual time=225.300..225.326 rows=1)",0,INK,"4"),
           ("->  Hash Join (actual time=4.120..225.209 rows=108)",1,INK,""),
           ("Hash Cond: (oi.order_id = o.order_id)",2,MUTED,""),
           ("->  Seq Scan on order_items oi (actual time=0.013..116.108 rows=1926847)",2,RED,"3"),
           ("->  Hash (actual time=0.060..0.084 rows=40)",2,INK,"2"),
           ("->  Bitmap Heap Scan on orders o (actual time=0.018..0.051 rows=40)",3,GREEN,""),
           ("->  Bitmap Index Scan on idx_orders_customer_id (rows=40)",4,GREEN,"1"),
           ("Execution Time: 225.368 ms",0,INK,"")]
    y=74
    for s_,ind,c,n in lines:
        if n:
            o.append(rect(34,y-15,20,20,fill=ORANGE,rx=10)); o.append(text(44,y,n,11.5,"#fff","bold",anchor="middle"))
        o.append(text(66+ind*30,y,s_,12,c,"bold" if c in (RED,GREEN) else "normal",family=MONO)); y+=28
    o.append(rect(26,52,988,y-66,fill="none",stroke=RULE,rx=6))
    notes=["1  Read the most indented step first: the index finds customer 2718's 40 orders in a fraction of a millisecond.",
           "2  Their 40 order ids go into a small in-memory hash table.",
           "3  The expensive step: every one of 1,926,847 order lines is read and checked against that hash table.",
           "4  The top node is the final result. Its second time (225 ms) is the whole query; the Seq Scan's 116 ms is about half of it."]
    for i,l in enumerate(notes): o.append(text(30,y+20+i*22,l,12,INK))
    o.append(text(30,y+20+4*22+6,"Actual times are in milliseconds, shown as first row..last row. The other 109 ms is the Hash Join checking each of those lines.",11.5,MUTED,style="italic"))
    return svg(1040,y+20+4*22+20,"".join(o))

def fig_normal():
    o=[text(30,32,"Normalization, one rule at a time (the same six orders)",14,INK,"bold",family=HEAD)]
    cols=[("0NF: order_sheet","6 rows","products packed in one cell:\n'101 Storage Box 10L x45\n @430; 102 Storage …'",RED),
          ("1NF: order_lines_1nf","10 rows","one value per cell,\none row per order line,\nkey (order_id, product_id)",ORANGE),
          ("2NF: split by key","6 + 4 + 10 rows","orders (depend on order_id)\nproducts (depend on product_id)\norder_lines (need both)",PURPLE),
          ("3NF: customers","4 customers","city depends on customer,\nnot on the order: move it\nto its own table",GREEN)]
    x=30
    for i,(t,n,d,c) in enumerate(cols):
        o.append(rect(x,60,225,160,fill="#fff",stroke=c,sw=2,rx=8))
        o.append(text(x+14,88,t,13,c,"bold")); o.append(text(x+14,110,n,12,MUTED,"bold"))
        for j,l in enumerate(d.split("\n")): o.append(text(x+14,140+j*22,l,11.5,INK,family=(MONO if i==0 and j>0 else None)))
        if i<3: o.append(path(f"M{x+228},155 H{x+252}",stroke=INK,sw=2)); o.append(path(f"M{x+245},149 L{x+253},155 L{x+245},161",stroke=INK,sw=2))
        x+=257
    o.append(text(30,252,"Problems removed:  0NF → 1NF you can filter and sum.  1NF → 2NF a product's name is stored once.",12,INK))
    o.append(text(30,274,"2NF → 3NF a customer's city is stored once, so it can't disagree with itself.  Every step: the net revenue still totals ₹129,040.",12,INK))
    return svg(1070,290,"".join(o))

def fig_star():
    o=[text(30,32,"Riverstone's 2025 sales as a star schema (schema dw)",14,INK,"bold",family=HEAD)]
    cx,cy=420,200
    o.append(rect(cx-140,cy-80,280,170,fill="#fdf3dc",stroke=PK,sw=2,rx=8))
    o.append(text(cx,cy-55,"fact_sales_line",14,INK,"bold",anchor="middle"))
    o.append(text(cx,cy-35,"grain: one non-cancelled order line",11,MUTED,anchor="middle",style="italic"))
    for i,l in enumerate(["date_key → dim_date","customer_key → dim_customer","product_key → dim_product","sales_rep_key → dim_sales_rep","quantity · net_revenue · product_cost"]):
        o.append(text(cx-128,cy-10+i*20,l,11.5,INK,family=MONO))
    dims=[(60,70,"dim_date","365 rows: day, month, quarter"),(560,70,"dim_customer","27 rows (24 customers, SCD2)"),(60,300,"dim_product","8 rows: name, category"),(560,300,"dim_sales_rep","6 rows incl. 'No rep recorded'")]
    for x,y,n,s in dims:
        o.append(rect(x,y,220,56,fill="#e2f3ee",stroke=GREEN,sw=1.6,rx=7)); o.append(text(x+110,y+23,n,13,INK,"bold",anchor="middle")); o.append(text(x+110,y+42,s,11,MUTED,anchor="middle"))
    o.append(path(f"M280,98 L280,140",stroke=GREEN,sw=1.6)); o.append(path("M560,98 L560,140",stroke=GREEN,sw=1.6))
    o.append(path("M280,300 L280,290",stroke=GREEN,sw=1.6)); o.append(path("M560,300 L560,290",stroke=GREEN,sw=1.6))
    # SCD2 timeline
    X=830; o.append(text(X,70,"dim_customer: Metro Mart",13,INK,"bold"))
    o.append(rect(X,90,130,40,fill="#efe7f6",stroke=PURPLE,rx=5)); o.append(text(X+65,107,"key 6: Thane",11.5,INK,"bold",anchor="middle")); o.append(text(X+65,123,"is_current = f",10.5,MUTED,anchor="middle"))
    o.append(rect(X+136,90,130,40,fill="#e2f3ee",stroke=GREEN,rx=5)); o.append(text(X+201,107,"key 7: Mumbai",11.5,INK,"bold",anchor="middle")); o.append(text(X+201,123,"is_current = t",10.5,MUTED,anchor="middle"))
    o.append(path(f"M{X},145 H{X+266}",stroke=MUTED,sw=1.5))
    for x in (X,X+133,X+266): o.append(path(f"M{x},139 V151",stroke=MUTED,sw=1.5))
    o.append(text(X,168,"from 2024-12-22",10.5,MUTED)); o.append(text(X+133,186,"2025-07-01",10.5,MUTED,anchor="middle")); o.append(text(X+266,168,"to 9999-12-31",10.5,MUTED,anchor="end"))
    for i,l in enumerate(["A March 2025 order joins to key 6","(Thane): the city at the time","of the order.","","Reconciles: ₹4,335,471 in 326 fact","lines, exactly the sales_lines","view. ✓"]):
        o.append(text(X,220+i*20,l,11.5,INK))
    return svg(1110,380,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig28-1-org-chart-levels.svg",fig_org),("fig28-2-bill-of-materials.svg",fig_bom),
                    ("fig28-3-scan-vs-index.svg",fig_scan_index),("fig28-4-reading-a-plan.svg",fig_plan),
                    ("fig28-5-normalization-steps.svg",fig_normal),("fig28-6-star-schema-scd2.svg",fig_star)]:
        open(name,"w").write(fn())
    print("ok28")
