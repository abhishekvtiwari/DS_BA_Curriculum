# Generates the SVG figures for Chapter 28. Run: python3 make_figs28.py
# Numbers come from the chapter's runs (companion/ch28/ch28_perf_log.txt and the SQL outputs in the manuscript).
# Every figure prints at the full text width (493.2 pt), so each canvas is 700 px wide and the smallest
# font is 10.5 px, which prints at 10.5 x 493.2 / 700 = 7.4 pt. width() measures text with the real
# DejaVu fonts, and check() stops the script if any label would overflow its box.
from make_figs import *
from PIL import ImageFont
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=700
_FONTS={}
def width(s,size,bold=False,mono=False):
    key=(bold,mono)
    if key not in _FONTS:
        f="/usr/share/fonts/truetype/dejavu/DejaVuSans"+("Mono" if mono else "")+("-Bold" if bold else "")+".ttf"
        _FONTS[key]=f
    return ImageFont.truetype(_FONTS[key],100).getlength(s)*size/100
def check(s,size,room,bold=False,mono=False):
    w=width(s,size,bold,mono)
    if w>room: raise SystemExit(f"text too wide ({w:.0f} > {room:.0f} px): {s!r}")

def box(x,y,w,h,lines,color=ACC,fill="#fff",sizes=(11,10.5)):
    """A box with up to three centred lines: the first bold."""
    o=[rect(x,y,w,h,fill=fill,stroke=color,sw=1.4,rx=6)]
    n=len(lines); lh=13.5; top=y+h/2-(n-1)*lh/2+4
    for i,l in enumerate(lines):
        sz=sizes[0] if i==0 else sizes[1]
        check(l,sz,w-8,bold=(i==0))
        o.append(text(x+w/2,top+i*lh,l,sz,INK if i==0 else MUTED,"bold" if i==0 else "normal",anchor="middle"))
    return "".join(o)

def fig_org():
    o=[text(20,24,"staff: each row points to its manager (manager_id)",13,INK,"bold",family=HEAD)]
    bw,bh=112,40
    cols=[92,210,328,446,564]
    lv={1:44,2:104,3:164,4:224,5:284}
    colors={1:INK,2:ACC,3:PURPLE,4:GREEN,5:ORANGE}
    labels={1:"anchor",2:"pass 1",3:"pass 2",4:"pass 3",5:"pass 4"}
    nodes=[(100,"Arvind Kapoor","Managing Director",1,None,2),
           (110,"Anita Rao","Sales Head",2,100,0),(130,"Harpreet Sethi","Head of Production",2,100,2),
           (120,"Suresh Menon","Finance Manager",2,100,3),(150,"Mahesh Yadav","Warehouse Mgr",2,100,4),
           (111,"Vikram Singh","Sales Manager",3,110,0),(112,"Farah Khan","Sales Executive",3,110,1),
           (131,"Ramesh Patil","Plant Mgr, Taloja",3,130,2),(132,"Kiran Bhosale","Plant Mgr, Chakan",3,130,3),
           (114,"Neha Kulkarni","Sales Executive",4,111,0),(115,"Rahul Mehta","Sales Executive",4,111,1),
           (133,"Ajay Kumar","Shift Supervisor",4,131,2),(135,"Swati Joshi","Shift Supervisor",4,132,3),
           (136,"Gopal Sahu","Machine Operator",5,133,1),(137,"Sunita Pawar","Machine Operator",5,133,2),
           (138,"Farid Shaikh","Machine Operator",5,135,3)]
    pos={sid:(cols[c],lv[l]) for sid,n,t,l,m,c in nodes}
    for sid,n,t,l,m,c in nodes:
        if m:
            x1,y1=pos[m]; x2,y2=pos[sid]
            o.append(path(f"M{x1+bw/2},{y1+bh} V{(y1+bh+y2)/2} H{x2+bw/2} V{y2}",stroke=RULE,sw=1.4))
    for sid,n,t,l,m,c in nodes:
        x,y=pos[sid]; o.append(box(x,y,bw,bh,[n,t],color=colors[l]))
    for l,y in lv.items():
        o.append(text(12,y+17,f"level {l}",11,colors[l],"bold"))
        o.append(text(12,y+31,labels[l],10.5,MUTED))
    o.append(text(20,346,"Pass 5 reads the three operators, finds nobody who reports to them, and the query stops.",10.5,MUTED))
    return svg(W,358,"".join(o))

def fig_bom():
    o=[text(20,24,"Bill of materials: quantities multiply as you go down",13,INK,"bold",family=HEAD)]
    rows={0:40,1:104,2:176,3:258}
    for d,y in rows.items():
        if d: o.append(text(8,y+26,f"depth {d}",10.5,MUTED,"bold"))
    o.append(box(290,rows[0],150,40,["Garden Chair (106)","product, 1 unit"],color=INK))
    l1=[(90,"Seat shell","assembly, × 1",ACC),(230,"Steel frame","assembly, × 1",ACC),(370,"Product label","material, × 1",GREEN),(510,"Shipping carton","material, × 1",GREEN)]
    for x,n,q,c in l1:
        o.append(path(f"M365,{rows[0]+40} V{rows[1]-10} H{x+60} V{rows[1]}",stroke=RULE,sw=1.4)); o.append(box(x,rows[1],120,44,[n,q],color=c))
    l2=[(80,"PP granules","× 2.2 kg","material",GREEN,150),(198,"Masterbatch","× 0.08 kg","material",GREEN,150),
        (316,"Leg assembly","× 2","assembly",ACC,290),(434,"Steel tube","× 1.0 kg","material",GREEN,290),(552,"Fastener pack","× 1","material",GREEN,290)]
    for x,n,q,k,c,px in l2:
        o.append(path(f"M{px},{rows[1]+44} V{rows[2]-10} H{x+55} V{rows[2]}",stroke=RULE,sw=1.4)); o.append(box(x,rows[2],110,56,[n,q,k],color=c))
    l3=[(300,"Steel tube","1.2 kg × 2 = 2.4 kg"),(450,"Fastener pack","1 × 2 = 2")]
    for x,n,q in l3:
        o.append(path(f"M371,{rows[2]+56} V{rows[3]-10} H{x+65} V{rows[3]}",stroke=RULE,sw=1.4)); o.append(box(x,rows[3],130,44,[n,q],color=ORANGE,fill="#fbeee4"))
    o.append(text(20,332,"Depth-3 boxes (shaded) are found on the second pass of the recursive part: each child's quantity is",10.5,MUTED))
    o.append(text(20,348,"multiplied by its parent's running quantity. Steel tube appears twice: 1.0 kg + 2.4 kg = 3.4 kg per chair.",10.5,MUTED))
    py=364
    o.append(rect(20,py,W-40,84,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(32,py+20,"Material cost of one chair",10.5,INK,"bold"))
    left=["PP granules 2.2 kg × ₹110 = ₹242.00","Masterbatch 0.08 kg × ₹260 = ₹20.80","Steel tube 3.4 kg × ₹95 = ₹323.00"]
    right=["Fasteners 3 × ₹14 = ₹42.00","Label ₹2 + carton ₹18 = ₹20.00","Total ₹647.80"]
    for i,l in enumerate(left): check(l,10.5,300); o.append(text(32,py+40+i*16,l,10.5,INK))
    for i,l in enumerate(right): check(l,10.5,300,bold=(i==2)); o.append(text(360,py+40+i*16,l,10.5,INK,"bold" if i==2 else "normal"))
    return svg(W,py+96,"".join(o))

def fig_scan_index():
    o=[text(20,24,"Finding customer 2718's 40 orders among 714,285",13,INK,"bold",family=HEAD)]
    o.append(text(20,52,"Sequential scan: read every row",12,RED,"bold"))
    for r in range(9):
        for c in range(13):
            hit=(r,c) in [(2,4),(6,9)]
            o.append(rect(20+c*21,64+r*17,17,12,fill=("#f3c9c9" if hit else "#eef1f5"),stroke=(RED if hit else RULE),sw=(1.2 if hit else 0.6)))
    o.append(path("M20,226 H290",stroke=RED,sw=2.2)); o.append(path("M283,221 L292,226 L283,231",stroke=RED,sw=2.2))
    o.append(text(20,250,"714,285 rows checked, 714,245 thrown away",10.5,INK))
    o.append(text(20,272,"median 38.77 ms",13,RED,"bold"))
    X=340
    o.append(text(X,52,"B-tree index: follow the sorted keys",12,GREEN,"bold"))
    o.append(box(X+110,62,130,30,["root: 1 … 5000"],color=GREEN))
    for i,lab in enumerate(["1 … 1700","1701 … 3400","3401 … 5000"]):
        x=X+5+i*115; o.append(path(f"M{X+175},92 V102 H{x+50} V112",stroke=RULE,sw=1.3))
        o.append(box(x,112,100,28,[lab],color=(GREEN if i==1 else RULE)))
    o.append(text(X+10,180,"…",12,MUTED,"bold",anchor="middle")); o.append(text(X+340,180,"…",12,MUTED,"bold",anchor="middle"))
    for i,lab in enumerate(["2701 … 2717","2718 … 2735","2736 … 2752"]):
        x=X+25+i*102; o.append(path(f"M{X+170},140 V150 H{x+45} V160",stroke=RULE,sw=1.3))
        o.append(box(x,160,90,28,[lab],color=(GREEN if i==1 else RULE),sizes=(10.5,10.5)))
    o.append(text(X,256,"(leaf pages under 1701 … 3400; one branch shown)",10.5,MUTED))
    o.append(path(f"M{X+172},188 V210",stroke=GREEN,sw=1.8))
    o.append(box(X+57,212,230,28,["40 row pointers → 40 rows"],color=GREEN))
    o.append(text(X,272,"a few index pages, then 40 table pages",10.5,INK))
    o.append(text(X,294,"median 0.18 ms",13,GREEN,"bold"))
    o.append(text(20,322,"PostgreSQL 16 on the author's test machine, riverstone_perf. Your times will differ; the ratio (about 200 to 1) is what matters.",10.5,MUTED,style="italic"))
    return svg(W,334,"".join(o))

def fig_plan():
    o=[text(20,24,"Reading EXPLAIN ANALYZE from the inside out",13,INK,"bold",family=HEAD)]
    o.append(text(20,42,"customer 2718's revenue, before order_items.order_id had an index (loops=1 and the Hash's memory line trimmed)",10.5,MUTED))
    lines=[("Aggregate (actual time=285.475..285.485 rows=1)",0,INK,"5"),
           ("->  Hash Join (actual time=5.181..285.266 rows=108)",1,INK,"4"),
           ("Hash Cond: (oi.order_id = o.order_id)",3,MUTED,""),
           ("->  Seq Scan on order_items oi (actual time=0.027..142.289 rows=1926847)",2,RED,"3"),
           ("->  Hash (actual time=0.151..0.158 rows=40)",2,INK,"2"),
           ("->  Bitmap Heap Scan on orders o (actual time=0.025..0.143 rows=40)",3,GREEN,""),
           ("->  Bitmap Index Scan on idx_orders_customer_id (actual time=0.014..0.015 rows=40)",4,GREEN,"1"),
           ("Execution Time: 285.549 ms",0,INK,"")]
    y=70
    for s_,ind,c,n in lines:
        if n:
            o.append(rect(24,y-13,18,18,fill=ORANGE,rx=9)); o.append(text(33,y,n,10.5,"#fff","bold",anchor="middle"))
        x=50+ind*14; check(s_,10.5,W-10-x,mono=True,bold=c in (RED,GREEN))
        o.append(text(x,y,s_,10.5,c,"bold" if c in (RED,GREEN) else "normal",family=MONO)); y+=22
    o.append(rect(16,52,W-26,y-64,fill="none",stroke=RULE,rx=6))
    notes=["1  Start at the most indented step: the index finds customer 2718's 40 orders in 0.015 ms.",
           "2  The table rows are fetched, and their 40 order ids go into a small in-memory hash table.",
           "3  The expensive step: all 1,926,847 order lines are read, taking 142 ms of the total.",
           "4  The Hash Join checks each line against the hash table and keeps 108: another 143 ms.",
           "5  The top node is the final result. Its last time, 285 ms, is the whole query."]
    for i,l in enumerate(notes):
        check(l,10.5,W-30); o.append(text(20,y+14+i*19,l,10.5,INK))
    o.append(text(20,y+14+5*19+4,"Times are milliseconds, shown as first row..last row. This is one run; the median of seven was 262.47 ms.",10.5,MUTED,style="italic"))
    return svg(W,y+14+5*19+16,"".join(o))

def fig_normal():
    o=[text(20,24,"Normalization, one rule at a time (the same six orders)",13,INK,"bold",family=HEAD)]
    cols=[("0NF: order_sheet","6 rows",["products packed in","one cell:","'101 Storage Box","10L x45 @430; …'"],RED),
          ("1NF","10 rows",["one value per cell,","one row per order line,","key (order_id,","product_id)"],ORANGE),
          ("2NF: split by key","6 + 4 + 10 rows",["orders (order_id)","products (product_id)","order_lines","(need both)"],PURPLE),
          ("3NF: customers","4 customers",["city depends on the","customer, not the order:","move it to its own","table"],GREEN)]
    bw,gap,x=154,20,15
    for i,(t,n,d,c) in enumerate(cols):
        o.append(rect(x,40,bw,150,fill="#fff",stroke=c,sw=1.8,rx=7))
        check(t,11.5,bw-16,bold=True); o.append(text(x+8,62,t,11.5,c,"bold")); o.append(text(x+8,80,n,10.5,MUTED,"bold"))
        for j,l in enumerate(d):
            mono=(i==0 and j>1); check(l,10.5,bw-14,mono=mono)
            o.append(text(x+8,106+j*18,l,10.5,INK,family=(MONO if mono else None)))
        if i<3:
            ax=x+bw+3; o.append(path(f"M{ax},115 H{ax+gap-6}",stroke=INK,sw=1.8)); o.append(path(f"M{ax+gap-11},110 L{ax+gap-5},115 L{ax+gap-11},120",stroke=INK,sw=1.8))
        x+=bw+gap
    for i,l in enumerate(["0NF → 1NF: you can filter and add up.   1NF → 2NF: a product's name is stored once.",
                          "2NF → 3NF: a customer's city is stored once, so it can't disagree with itself.",
                          "At every step the net revenue still totals ₹1,29,040."]):
        check(l,10.5,W-30); o.append(text(20,214+i*18,l,10.5,INK))
    return svg(W,262,"".join(o))

def fig_star():
    o=[text(20,24,"Riverstone's 2025 sales as a star schema (schema dw)",13,INK,"bold",family=HEAD)]
    fx,fy,fw,fh=110,120,220,146
    dims=[(10,44,"dim_date","365 days"),(270,44,"dim_customer","27 customer versions"),
          (10,290,"dim_product","8 products"),(270,290,"dim_sales_rep","6 reps, incl. unknown")]
    dw,dh=160,44
    # spokes first, from each dimension's inner corner to the fact box, with a visible gap
    for x,y,n,s in dims:
        sx=x+dw/2; sy=y+dh if y<fy else y
        ex=fx+(40 if x<fx else fw-40); ey=fy if y<fy else fy+fh
        o.append(path(f"M{sx},{sy} L{ex},{ey}",stroke=GREEN,sw=2))
    o.append(rect(fx,fy,fw,fh,fill="#fdf3dc",stroke=PK,sw=1.8,rx=7))
    o.append(text(fx+fw/2,fy+20,"fact_sales_line",12,INK,"bold",anchor="middle"))
    o.append(text(fx+fw/2,fy+36,"one non-cancelled order line",10.5,MUTED,anchor="middle",style="italic"))
    for i,l in enumerate(["date_key","customer_key","product_key","sales_rep_key","quantity, net_revenue,","product_cost"]):
        check(l,10.5,fw-16,mono=(i<4)); o.append(text(fx+10,fy+56+i*14,l,10.5,INK,family=(MONO if i<4 else None)))
    for x,y,n,s in dims:
        o.append(box(x,y,dw,dh,[n,s],color=GREEN,fill="#e2f3ee"))
    X=452
    o.append(text(X,56,"dim_customer: Metro Mart",12,INK,"bold"))
    o.append(box(X,68,116,40,["key 6: Thane","is_current = f"],color=PURPLE,fill="#efe7f6"))
    o.append(box(X+120,68,116,40,["key 7: Mumbai","is_current = t"],color=GREEN,fill="#e2f3ee"))
    o.append(path(f"M{X},122 H{X+236}",stroke=MUTED,sw=1.4))
    for x in (X,X+118,X+236): o.append(path(f"M{x},116 V128",stroke=MUTED,sw=1.4))
    o.append(text(X,144,"2024-12-22",10.5,MUTED)); o.append(text(X+118,160,"2025-07-01",10.5,MUTED,anchor="middle")); o.append(text(X+236,144,"9999-12-31",10.5,MUTED,anchor="end"))
    for i,l in enumerate(["A March 2025 order joins to key 6","(Thane): the city at the time of","the order.","","Reconciles: ₹43,35,471 in 326 fact","lines, exactly the sales_lines view. ✓"]):
        check(l,10.5,W-X-8); o.append(text(X,190+i*17,l,10.5,INK))
    return svg(W,346,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig28-1-org-chart-levels.svg",fig_org),("fig28-2-bill-of-materials.svg",fig_bom),
                    ("fig28-3-scan-vs-index.svg",fig_scan_index),("fig28-4-reading-a-plan.svg",fig_plan),
                    ("fig28-5-normalization-steps.svg",fig_normal),("fig28-6-star-schema-scd2.svg",fig_star)]:
        open(name,"w").write(fn())
    print("ok28")
