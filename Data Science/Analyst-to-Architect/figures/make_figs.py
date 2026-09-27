# Generates the SVG figures for Chapter 12. Run: python3 make_figs.py
from html import escape as esc
INK="#1d2330"; MUTED="#5b6475"; ACC="#0f5c8c"; RULE="#c9d3df"; BG="#ffffff"
PK="#b7791f"; PKBG="#fdf3dc"; FK="#2f7d6d"; FKBG="#e2f3ee"; ROWALT="#f6f9fc"
SANS="DejaVu Sans, Arial, sans-serif"; HEAD="Poppins, DejaVu Sans, sans-serif"; MONO="DejaVu Sans Mono, monospace"

def svg(w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{SANS}"><rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>'
def text(x,y,s,size=13,fill=INK,weight="normal",anchor="start",family=None,style=""):
    fam=f' font-family="{family}"' if family else ""
    st=f' font-style="{style}"' if style else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{fam}{st}>{esc(s)}</text>'
def rect(x,y,w,h,fill="none",stroke="none",sw=1,rx=0,extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def path(d,stroke=ACC,sw=2,dash=None):
    da=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{da}/>'
def badge(x,y,label):
    c,bg=(PK,PKBG) if label=="PK" else (FK,FKBG)
    return rect(x,y-12,29,18,fill=bg,stroke=c,sw=1,rx=3)+text(x+14.5,y+2,label,size=11,fill=c,weight="bold",anchor="middle")

H=40; R=29
class Table:
    def __init__(s,x,y,w,name,cols,note=None):
        s.x,s.y,s.w,s.name,s.cols,s.note=x,y,w,name,cols,note
    def ry(s,i): return s.y+H+i*R+R/2
    def bottom(s): return s.y+H+len(s.cols)*R+6
    def draw(s):
        o=[rect(s.x+2,s.y+3,s.w,s.bottom()-s.y,fill="#e9eef4",rx=7),
           rect(s.x,s.y,s.w,s.bottom()-s.y,fill="#fff",stroke=RULE,sw=1.2,rx=7),
           f'<path d="M{s.x},{s.y+7} a7,7 0 0 1 7,-7 H{s.x+s.w-7} a7,7 0 0 1 7,7 V{s.y+H} H{s.x} Z" fill="{ACC}"/>',
           text(s.x+14,s.y+26.5,s.name,size=17,fill="#fff",weight="bold",family=HEAD)]
        if s.note: o.append(text(s.x+s.w-12,s.y+23,s.note,size=10.5,fill="#d6e6f2",anchor="end"))
        for i,(c,t,k) in enumerate(s.cols):
            yy=s.y+H+i*R
            if i%2==1: o.append(rect(s.x+1,yy,s.w-2,R,fill=ROWALT))
            cy=yy+R/2+5
            if k: o.append(badge(s.x+10,cy-3.5,k))
            o.append(text(s.x+46,cy,c,size=15,fill=INK,weight="bold" if k=="PK" else "normal",family=MONO))
            o.append(text(s.x+s.w-12,cy,t,size=11.5,fill=MUTED,anchor="end"))
        return "".join(o)

def card(x1,y1,x2,y2,dx1,dy1,dx2,dy2):
    return text(x1+dx1,y1+dy1,"1",size=15,fill=ACC,weight="bold")+text(x2+dx2,y2+dy2,"N",size=15,fill=ACC,weight="bold")

# ---------- Figure 12.1: schema ----------
def fig_schema():
    W=270
    cu=Table(30,60,W,"customers",[("customer_id","INTEGER","PK"),("customer_name","VARCHAR",""),("city","VARCHAR",""),("segment","VARCHAR",""),("signup_date","DATE","")])
    pr=Table(30,480,W,"products",[("product_id","INTEGER","PK"),("product_name","VARCHAR",""),("category","VARCHAR",""),("unit_price","NUMERIC",""),("unit_cost","NUMERIC","")])
    od=Table(385,60,W,"orders",[("order_id","INTEGER","PK"),("customer_id","INTEGER","FK"),("order_date","DATE",""),("status","VARCHAR",""),("sales_rep_id","INTEGER","FK")])
    oi=Table(385,480,W,"order_items",[("order_item_id","INTEGER","PK"),("order_id","INTEGER","FK"),("product_id","INTEGER","FK"),("quantity","INTEGER",""),("unit_price","NUMERIC",""),("discount_pct","NUMERIC","")])
    inv=Table(740,60,W,"invoices",[("invoice_id","INTEGER","PK"),("order_id","INTEGER","FK"),("invoice_date","DATE",""),("due_date","DATE",""),("amount","NUMERIC","")])
    pay=Table(740,318,W,"payments",[("payment_id","INTEGER","PK"),("invoice_id","INTEGER","FK"),("payment_date","DATE",""),("amount","NUMERIC",""),("method","VARCHAR","")])
    em=Table(740,578,W,"employees",[("employee_id","INTEGER","PK"),("employee_name","VARCHAR",""),("job_title","VARCHAR",""),("manager_id","INTEGER","FK")])
    o=[]
    # customers.customer_id -> orders.customer_id
    y0,y1=cu.ry(0),od.ry(1); o.append(path(f"M{cu.x+W},{y0} H342 V{y1} H{od.x}")); o.append(card(cu.x+W,y0,od.x,y1,6,-6,-16,-6))
    # products.product_id -> order_items.product_id
    y0,y1=pr.ry(0),oi.ry(2); o.append(path(f"M{pr.x+W},{y0} H342 V{y1} H{oi.x}")); o.append(card(pr.x+W,y0,oi.x,y1,6,-6,-16,-6))
    # orders.order_id -> order_items.order_id (left gutter inside column)
    xm=od.x+W-60; o.append(path(f"M{xm},{od.bottom()} V{oi.y}")); o.append(text(xm+8,od.bottom()+18,"1",13,ACC,"bold")); o.append(text(xm+8,oi.y-8,"N",13,ACC,"bold")); o.append(text(xm-8,(od.bottom()+oi.y)/2+4,"order_id",11,MUTED,anchor="end",style="italic"))
    # orders.order_id -> invoices.order_id
    y0,y1=od.ry(0),inv.ry(1); o.append(path(f"M{od.x+W},{y0} H690 V{y1} H{inv.x}")); o.append(card(od.x+W,y0,inv.x,y1,6,-6,-16,-6))
    # invoices.invoice_id -> payments.invoice_id (right side)
    y0,y1=inv.ry(0),pay.ry(1); o.append(path(f"M{inv.x+W},{y0} H1032 V{y1} H{inv.x+W}")); o.append(text(inv.x+W+8,y0-6,"1",13,ACC,"bold")); o.append(text(inv.x+W+8,y1-6,"N",13,ACC,"bold"))
    # employees.employee_id -> orders.sales_rep_id
    y0,y1=em.ry(0),od.ry(4); o.append(path(f"M{em.x},{y0} H712 V{y1} H{od.x+W}")); o.append(text(em.x-16,y0-6,"1",13,ACC,"bold")); o.append(text(od.x+W+6,y1-6,"N",13,ACC,"bold"))
    # employees.manager_id -> employees.employee_id (self)
    y0,y1=em.ry(0),em.ry(3); o.append(path(f"M{em.x+W},{y1} H1032 V{y0} H{em.x+W}",dash="5 4")); o.append(text(em.x+W+8,y0-6,"1",13,ACC,"bold")); o.append(text(em.x+W+8,y1-6,"N",13,ACC,"bold"))
    for t in (cu,pr,od,oi,inv,pay,em): o.append(t.draw())
    # relationship captions
    o.append(text(342-4, 52, "", 10))
    # legend
    ly=800
    o.append(rect(30,ly-20,980,34,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(badge(44,ly+2,"PK")); o.append(text(80,ly+2,"primary key: identifies each row",13,INK))
    o.append(badge(330,ly+2,"FK")); o.append(text(366,ly+2,"foreign key: points to a row in another table",13,INK))
    o.append(path(f"M680,{ly-3} H730")); o.append(text(668,ly+2,"1",13,ACC,"bold")); o.append(text(736,ly+2,"N",13,ACC,"bold"))
    o.append(text(756,ly+2,"one row links to many rows",13,INK))
    o.append(path(f"M{em.x+W+2},{0}",sw=0))
    return svg(1050,825,"".join(x for x in o if x))

# ---------- Figure 12.2: one order, many tables ----------
def mini(x,y,name,headers,rows,widths,color,hl=None):
    hl=hl or []
    w=sum(widths); o=[rect(x,y,w,26,fill=color,rx=5), text(x+10,y+18,name,12.5,"#fff","bold",family=HEAD)]
    yy=y+26
    o.append(rect(x,yy,w,22,fill="#eef2f6"))
    cx=x
    for h_,wd in zip(headers,widths):
        o.append(text(cx+7,yy+15,h_,11,MUTED,"bold",family=MONO)); cx+=wd
    yy+=22
    for r in rows:
        o.append(rect(x,yy,w,24,fill="#fff",stroke=RULE,sw=0.8))
        cx=x
        for v,wd in zip(r,widths):
            o.append(text(cx+7,yy+16.5,v,12.5,INK,family=MONO)); cx+=wd
        yy+=24
    o.append(rect(x,y,w,yy-y,stroke=color,sw=1.5,rx=5))
    return "".join(o), yy

def fig_one_order():
    o=[]
    C_ORD="#0f5c8c"; C_CUS="#2f7d6d"; C_EMP="#7a4fa0"; C_ITM="#c0662b"; C_PRD="#5b6475"
    # order slip
    sx,sy,sw,sh=20,30,390,470
    o.append(rect(sx+3,sy+4,sw,sh,fill="#e9eef4",rx=10)); o.append(rect(sx,sy,sw,sh,fill="#fffdf7",stroke="#d8cfb8",sw=1.2,rx=10))
    o.append(text(sx+20,sy+34,"RIVERSTONE SUPPLIES",15,INK,"bold",family=HEAD)); o.append(text(sx+20,sy+54,"Order slip, as a person sees it",11.5,MUTED,style="italic"))
    def band(y,h,c): return rect(sx+10,y,sw-20,h,fill=c,rx=5,extra='fill-opacity="0.10"')+rect(sx+10,y,4,h,fill=c)
    o.append(band(sy+70,52,C_ORD)); o.append(text(sx+24,sy+91,"Order no. 5001",13,INK,"bold")); o.append(text(sx+24,sy+111,"Date 05 Jan 2026 · Status Delivered",12,INK))
    o.append(band(sy+132,52,C_CUS)); o.append(text(sx+24,sy+153,"Customer: Sharma Hardware",13,INK,"bold")); o.append(text(sx+24,sy+173,"Mumbai · Retail",12,INK))
    o.append(band(sy+194,32,C_EMP)); o.append(text(sx+24,sy+215,"Sales rep: Neha Kulkarni",12.5,INK))
    o.append(band(sy+236,150,C_ITM))
    o.append(text(sx+24,sy+258,"Product",11,MUTED,"bold")); o.append(text(sx+196,sy+258,"Qty",11,MUTED,"bold",anchor="middle")); o.append(text(sx+226,sy+258,"Price",11,MUTED,"bold")); o.append(text(sx+280,sy+258,"Disc",11,MUTED,"bold")); o.append(text(sx+368,sy+258,"Net ₹",11,MUTED,"bold",anchor="end"))
    for i,(p,q,pr,d,n) in enumerate([("Storage Box 10L","20","450","0%","9,000"),("Water Bottle 1L","50","120","5%","5,700")]):
        yy=sy+290+i*34
        o.append(text(sx+24,yy,p,12.5,INK)); o.append(text(sx+196,yy,q,12.5,INK,anchor="middle")); o.append(text(sx+226,yy,pr,12.5,INK)); o.append(text(sx+284,yy,d,12.5,INK)); o.append(text(sx+368,yy,n,12.5,INK,anchor="end"))
    o.append(f'<line x1="{sx+24}" y1="{sy+360}" x2="{sx+368}" y2="{sy+360}" stroke="{RULE}"/>')
    o.append(text(sx+24,sy+378,"Total",13,INK,"bold")); o.append(text(sx+368,sy+378,"₹14,700",13,INK,"bold",anchor="end"))
    o.append(rect(sx+10,sy+400,sw-20,56,fill="#fff4d6",stroke="#e2c46b",rx=6))
    o.append(text(sx+22,sy+423,"The line values and the total are not stored.",11.5,INK,"bold")); o.append(text(sx+22,sy+442,"SQL calculates them: quantity × price × (1 − discount).",11.5,INK))
    # right side tables
    X=520
    t,_=mini(X,20,"orders",["order_id","customer_id","order_date","status","sales_rep_id"],[["5001","1","2026-01-05","Delivered","3"]],[80,100,100,90,110],C_ORD); o.append(t)
    t,_=mini(X,112,"customers",["customer_id","customer_name","city","segment"],[["1","Sharma Hardware","Mumbai","Retail"]],[100,150,80,80],C_CUS); o.append(t)
    t,_=mini(X,204,"employees",["employee_id","employee_name","job_title"],[["3","Neha Kulkarni","Sales Executive"]],[100,130,140],C_EMP); o.append(t)
    t,_=mini(X,296,"order_items",["order_id","product_id","quantity","unit_price","discount_pct"],[["5001","101","20","450.00","0.00"],["5001","103","50","120.00","5.00"]],[80,90,80,90,110],C_ITM); o.append(t)
    t,_=mini(X,412,"products",["product_id","product_name","category"],[["101","Storage Box 10L","Storage"],["103","Water Bottle 1L","Kitchen"]],[90,160,100],C_PRD); o.append(t)
    # connectors
    def conn(y1,y2,c): return path(f"M{sx+sw},{y1} C{sx+sw+55},{y1} {X-55},{y2} {X},{y2}",stroke=c,sw=2)
    o.append(conn(sy+96,59,C_ORD)); o.append(conn(sy+158,151,C_CUS)); o.append(conn(sy+210,243,C_EMP)); o.append(conn(sy+300,346,C_ITM)); o.append(conn(sy+320,452,C_PRD))
    o.append(text(X,535,"Keys tie the pieces together:",12,INK,"bold"))
    o.append(text(X,555,"orders.customer_id = 1 finds the customer; sales_rep_id = 3 finds the rep;",11.5,MUTED))
    o.append(text(X,573,"order_items.order_id = 5001 finds the lines; product_id finds each product.",11.5,MUTED))
    return svg(1050,590,"".join(o))

# ---------- Figure 12.3: join matching ----------
def grid(x,y,title,headers,rows,widths,color=ACC,nullcols=None,rowfill=None,subtitle=None):
    if subtitle:
        o=[text(x,y-26,title,13.5,INK,"bold",family=HEAD), text(x,y-9,subtitle,11,MUTED,style="italic")]
    else:
        o=[text(x,y-8,title,13.5,INK,"bold",family=HEAD)]
    w=sum(widths); o.append(rect(x,y,w,24,fill=color,rx=4)); cx=x
    for h_,wd in zip(headers,widths): o.append(text(cx+8,y+16.5,h_,11,"#fff","bold",family=MONO)); cx+=wd
    yy=y+24; centers=[]
    for i,r in enumerate(rows):
        f=(rowfill[i] if rowfill and rowfill[i] else "#fff")
        o.append(rect(x,yy,w,24,fill=f,stroke=RULE,sw=0.8)); cx=x
        for j,(v,wd) in enumerate(zip(r,widths)):
            if v=="NULL": o.append(text(cx+8,yy+16.5,"NULL",11.5,"#b23b3b","bold",family=MONO,style="italic"))
            else: o.append(text(cx+8,yy+16.5,v,11.5,INK,family=MONO))
            cx+=wd
        centers.append(yy+12); yy+=24
    return "".join(o), centers, yy

def fig_joins():
    o=[]
    t,cy,_=grid(30,50,"customers",["customer_id","customer_name"],[["1","Sharma Hardware"],["2","Patel Kitchenware"],["8","Blue Bay Cafe"]],[100,160]); o.append(t)
    t,oy,_=grid(360,50,"orders",["order_id","customer_id"],[["5001","1"],["5005","1"],["5011","1"],["5003","2"]],[90,100]); o.append(t)
    for a,b in [(0,0),(0,1),(0,2),(1,3)]:
        o.append(path(f"M290,{cy[a]} C325,{cy[a]} 325,{oy[b]} 360,{oy[b]}",stroke="#2f7d6d",sw=2))
    o.append(text(30,196,"Blue Bay Cafe (customer 8) has no matching order.",12,"#b23b3b","bold"))
    o.append(text(30,216,"Lines show rows whose customer_id values are equal.",12,MUTED))
    # results
    t,_,_=grid(600,68,"INNER JOIN result",["customer_name","order_id"],[["Sharma Hardware","5001"],["Sharma Hardware","5005"],["Sharma Hardware","5011"],["Patel Kitchenware","5003"]],[180,100],subtitle="4 rows: matches only"); o.append(t)
    t,_,_=grid(600,256,"LEFT JOIN result",["customer_name","order_id"],[["Sharma Hardware","5001"],["Sharma Hardware","5005"],["Sharma Hardware","5011"],["Patel Kitchenware","5003"],["Blue Bay Cafe","NULL"]],[180,100],rowfill=[None,None,None,None,"#fdecec"],subtitle="5 rows: every customer kept"); o.append(t)
    o.append(rect(30,262,520,118,fill="#f6f9fc",stroke=RULE,rx=6))
    for i,s_ in enumerate(["INNER JOIN keeps a row only when both sides match.",
                           "LEFT JOIN keeps every row from the left table (customers);",
                           "where there is no match, the right side is filled with NULL.",
                           "Sharma Hardware appears three times: one output row per match."]):
        o.append(text(46,290+i*24,s_,12.5,INK,"bold" if i==3 else "normal"))
    return svg(900,420,"".join(o))

# ---------- Figure 12.4: fan-out ----------
def fig_fanout():
    o=[]
    o.append(text(30,32,"What goes wrong: join first, then add up",15,"#b23b3b","bold",family=HEAD))
    t,_,_=grid(30,70,"invoices",["invoice_id","amount"],[["9002","73260.00"]],[90,100]); o.append(t)
    t,_,_=grid(250,70,"payments",["invoice_id","amount"],[["9002","40000.00"],["9002","33260.00"]],[90,100]); o.append(t)
    t,_,yy=grid(30,190,"after the JOIN (2 rows)",["invoice_id","invoice_amt","paid"],[["9002","73260.00","40000.00"],["9002","73260.00","33260.00"]],[90,110,100],rowfill=["#fdecec","#fdecec"]); o.append(t)
    o.append(text(30,yy+30,"SUM(invoice_amt) = 146,520  ✗  counted twice",13,"#b23b3b","bold"))
    o.append(text(30,yy+52,"SUM(paid) = 73,260   ✓  payments are the finest grain, so none repeat",12,MUTED))
    o.append(f'<line x1="470" y1="20" x2="470" y2="330" stroke="{RULE}" stroke-width="1.5"/>')
    X=495
    o.append(text(X,32,"The fix: add up payments first, then join",15,"#2f7d6d","bold",family=HEAD))
    t,_,_=grid(X,70,"payments summed per invoice",["invoice_id","paid"],[["9002","73260.00"]],[90,100],color="#2f7d6d"); o.append(t)
    t,_,yy=grid(X,190,"after the JOIN (1 row)",["invoice_id","invoice_amt","paid"],[["9002","73260.00","73260.00"]],[90,110,100],color="#2f7d6d",rowfill=["#e2f3ee"]); o.append(t)
    o.append(text(X,yy+30,"One row per invoice: totals are correct  ✓",13,"#2f7d6d","bold"))
    o.append(text(X,yy+52,"Rule: bring every table to the same grain before joining.",12,MUTED))
    return svg(900,340,"".join(o))

# ---------- Figure 12.5: execution order ----------
def fig_order():
    o=[]
    written=["SELECT","FROM","JOIN","WHERE","GROUP BY","HAVING","ORDER BY","LIMIT"]
    run=[("FROM / JOIN","gather and combine tables"),("WHERE","drop rows"),("GROUP BY","make groups"),("HAVING","drop groups"),("SELECT","compute columns and aliases"),("DISTINCT","remove duplicate rows"),("ORDER BY","sort (aliases exist now)"),("LIMIT","keep first n")]
    o.append(text(30,34,"You write it in this order",14,MUTED,"bold",family=HEAD))
    x=30; wd=112; gap=14
    for w_ in written:
        o.append(rect(x,48,wd,32,fill="#eef2f6",stroke=RULE,rx=16)); o.append(text(x+wd/2,69,w_,12,INK,"bold",anchor="middle",family=MONO)); x+=wd+gap
    o.append(text(30,122,"The database runs it in this order",14,ACC,"bold",family=HEAD))
    x=30
    for i,(k,d) in enumerate(run):
        o.append(rect(x,146,wd,82,fill="#fff",stroke=ACC,sw=1.5,rx=8))
        o.append(f'<circle cx="{x+wd/2}" cy="146" r="12" fill="{ACC}"/>'); o.append(text(x+wd/2,150.5,str(i+1),12,"#fff","bold",anchor="middle"))
        o.append(text(x+wd/2,178,k,11.5,INK,"bold",anchor="middle",family=MONO))
        words=d.split(" "); lines=[]; cur=""
        for wd_ in words:
            if len((cur+" "+wd_).strip())>16: lines.append(cur); cur=wd_
            else: cur=(cur+" "+wd_).strip()
        lines.append(cur)
        for j,l in enumerate(lines): o.append(text(x+wd/2,198+j*15,l,10.5,MUTED,anchor="middle"))
        if i<7: o.append(path(f"M{x+wd+1},187 H{x+wd+gap-6}",sw=2)); o.append(f'<path d="M{x+wd+gap-6},182 l6,5 l-6,5 z" fill="{ACC}"/>')
        x+=wd+gap
    o.append(rect(30,250,994,54,fill="#fff4d6",stroke="#e2c46b",rx=6))
    o.append(text(46,272,"This is why WHERE can't use COUNT(*) or a SELECT alias (step 2 runs before steps 3 and 5),",12.5,INK))
    o.append(text(46,292,"and why ORDER BY can use an alias (step 7 runs after step 5).",12.5,INK))
    return svg(1050,320,"".join(o))

if __name__ == "__main__":
  for name,fn in [("fig12-1-riverstone-schema.svg",fig_schema),("fig12-2-one-order-many-tables.svg",fig_one_order),("fig12-3-inner-vs-left-join.svg",fig_joins),("fig12-4-fan-out.svg",fig_fanout),("fig12-5-execution-order.svg",fig_order)]:
      open(name,"w").write(fn())
  print("ok")
