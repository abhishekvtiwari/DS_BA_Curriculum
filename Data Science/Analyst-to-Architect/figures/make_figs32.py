# Generates the SVG figures for Chapter 32. Run: python3 make_figs32.py
# Every figure prints at the full text width (493.2 pt), so on an 800 px canvas 12 px text prints at 7.4 pt.
import math
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; RED="#b23b3b"; SNAP="#6b4c9a"

def arrowhead(x2,y2,a,c=MUTED,s=7):
    p1=(x2-s*math.cos(a-0.42),y2-s*math.sin(a-0.42)); p2=(x2-s*math.cos(a+0.42),y2-s*math.sin(a+0.42))
    return f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def edge(x1,y1,x2,y2,c=MUTED):
    """A left-to-right dependency: straight when level, an S-curve inside the gutter otherwise, with an arrowhead."""
    if y1==y2:
        return path(f"M{x1},{y1} H{x2}",stroke=c,sw=1.3)+arrowhead(x2,y2,0,c)
    mx=(x1+x2)/2
    return path(f"M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}",stroke=c,sw=1.3)+arrowhead(x2,y2,0,c)

def node(x,y,w,h,label,color,fill="#fff",dash=None,family=MONO,size=12):
    extra=f'stroke-dasharray="{dash}"' if dash else ""
    return rect(x,y,w,h,fill=fill,stroke=color,sw=1.5,rx=6,extra=extra)+text(x+w/2,y+h/2+4.5,label,size,INK,"bold",anchor="middle",family=family)

def fig_dag():
    W=800
    C1,C2,C3,C4,C5=(12,122),(170,150),(356,134),(526,134),(706,84)   # (x, width) of each column
    yc=lambda r: 90+44*r; H=28
    o=[text(12,24,"The graph dbt builds from the ref(), source() and snapshot calls",14,INK,"bold",family=HEAD)]
    for (x,w),lab in [(C1,"sources"),(C2,"staging + snapshot"),(C3,"marts (tables): dimensions and facts"),(C5,"used by")]:
        o.append(text(x,52,lab,12,MUTED,"bold"))
    def box(col,r,label,color,fill="#fff",dash=None,family=MONO):
        x,w=col; o.append(node(x,yc(r)-H/2,w,H,label,color,fill,dash,family))
    for r,s in [(1,"erp.orders"),(2,"erp.order_items"),(3,"erp.products"),(4,"erp.employees"),(6,"crm.customers")]:
        box(C1,r,s,RULE,"#f6f9fc")
    for r,s in [(1,"stg_orders"),(2,"stg_order_items"),(3,"stg_products")]:
        box(C2,r,s,ACC)
    box(C2,6,"customers_snapshot",SNAP,"#f3eef9",dash="5 3")
    for r,s in [(0,"fct_daily_sales")]:
        box(C3,r,s,PK,"#fdf3dc")
    for r,s in [(3,"dim_product"),(4,"dim_sales_rep"),(6,"dim_customer"),(7,"dim_date")]:
        box(C3,r,s,GREEN,"#e2f3ee")
    # the fact table is drawn tall so that every input arrives level, without crossing another box
    x,w=C4; top=yc(1)-H/2; bot=yc(6)+H/2
    o.append(rect(x,top,w,bot-top,fill="#fdf3dc",stroke=PK,sw=1.5,rx=6))
    o.append(text(x+w/2,(top+bot)/2+4.5,"fct_sales_line",12,INK,"bold",anchor="middle",family=MONO))
    xb,wb=C5; yb=yc(3.5)
    o.append(node(xb,yb-H/2,wb,H,"Power BI",PURPLE,family=SANS))
    R=lambda col: col[0]+col[1]; L=lambda col: col[0]
    # sources -> staging, snapshot, and the one dimension read straight from a source
    o.append(edge(R(C1),yc(1),L(C2),yc(1)))
    o.append(edge(R(C1),yc(2),L(C2),yc(2)))
    o.append(edge(R(C1),yc(3),L(C2),yc(3)))
    o.append(edge(R(C1),yc(3)-6,L(C2),yc(2)+7))              # products -> stg_order_items (unit_cost)
    o.append(edge(R(C1),yc(4),L(C3),yc(4)))                  # employees -> dim_sales_rep
    o.append(edge(R(C1),yc(6),L(C2),yc(6)))                  # crm.customers -> snapshot
    # staging -> marts
    o.append(edge(R(C2),yc(3),L(C3),yc(3)))                  # stg_products -> dim_product
    o.append(edge(R(C2),yc(6),L(C3),yc(6)))                  # snapshot -> dim_customer
    o.append(edge(R(C2),yc(1)-6,L(C3),yc(0)-5))              # stg_orders -> fct_daily_sales
    o.append(edge(R(C2),yc(2)-6,L(C3),yc(0)+6))              # stg_order_items -> fct_daily_sales
    o.append(edge(R(C2),yc(1),L(C4),yc(1)))                  # stg_orders -> fct_sales_line
    o.append(edge(R(C2),yc(2),L(C4),yc(2)))                  # stg_order_items -> fct_sales_line
    for r in (3,4,6):
        o.append(edge(R(C3),yc(r),L(C4),yc(r)))              # dimensions -> fct_sales_line
    o.append(edge(R(C4),yb,L(C5),yb,PURPLE))
    o.append(text(L(C4),yc(7)+4.5,"← no inputs: built from generate_series",12,MUTED))
    y=yc(7)+44
    o.append(text(12,y,"Each arrow points from a model to the model that uses it. Nobody wrote this order down: dbt reads the calls",12,MUTED))
    o.append(text(12,y+18,"in the SQL, builds the graph, and runs it in dependency order, four models at a time (threads: 4).",12,MUTED))
    return svg(W,y+30,"".join(o))

def fig_materializations():
    W=800
    o=[text(12,24,"Four materializations, and what each one costs",14,INK,"bold",family=HEAD)]
    o.append(text(24,52,"materialization",12,MUTED,"bold")); o.append(text(160,52,"what dbt creates, and what it suits",12,MUTED,"bold"))
    o.append(text(488,52,"cost to build, and to query",12,MUTED,"bold"))
    rows=[("view","creates: a view; nothing is stored","suits: staging models","build: almost free","query: the full query, every time",ACC),
          ("table","creates: a table, rebuilt each run","suits: marts","build: a full rebuild","query: fast",GREEN),
          ("incremental","creates: a table; later runs add new rows","suits: large fact tables","build: new rows only (0.55 s, not 2.19 s)","query: fast",PK),
          ("ephemeral","creates: nothing; its SQL is pasted in","suits: small intermediate steps","build: nothing stored","query: runs inside each model that uses it",PURPLE)]
    y=64
    for name,what,use,build,query,c in rows:
        o.append(rect(12,y,776,56,fill="#fff",stroke=c,sw=1.8,rx=7))
        o.append(rect(12,y,8,56,fill=c,rx=3))
        o.append(text(30,y+33,name,13,INK,"bold",family=MONO))
        o.append(text(160,y+23,what,12,INK)); o.append(text(160,y+43,use,12,INK))
        o.append(text(488,y+23,build,12,INK)); o.append(text(488,y+43,query,12,INK))
        y+=66
    o.append(text(12,y+16,"Set the default per folder in dbt_project.yml; override it in one model with {{ config(materialized='...') }}.",12,MUTED))
    return svg(W,y+30,"".join(o))

def fig_build():
    W=800
    o=[text(12,24,"Why dbt build, and not dbt run followed by dbt test",14,INK,"bold",family=HEAD)]
    def column(x,heading,mark,hc,steps,outcome):
        o.append(text(x,56,f"{mark}  {heading}",13,hc,"bold"))
        y=72
        for i,(name,what,c,sw) in enumerate(steps):
            o.append(rect(x,y,370,40,fill="#fff",stroke=c,sw=sw,rx=6))
            o.append(text(x+12,y+25,name,12,INK,"bold",family=MONO)); o.append(text(x+150,y+25,what,12,INK))
            if i<len(steps)-1:
                o.append(path(f"M{x+185},{y+40} V{y+50}",stroke=MUTED,sw=1.4)+arrowhead(x+185,y+52,math.pi/2))
            y+=52
        o.append(text(x,y+12,outcome,12,hc))
        return y
    column(12,"dbt run, then dbt test","✗",RED,
           [("stg_order_items","built",MUTED,1.4),("fct_sales_line","built, with bad data",RED,2.2),
            ("dashboards","refreshed from it",RED,2.2),("tests","FAIL, an hour later",RED,2.2)],
           "✗ Bad numbers reached people before anyone knew.")
    y=column(418,"dbt build","✓",GREEN,
           [("stg_order_items","built",MUTED,1.4),("its grain test","FAIL: duplicate order_item_id",RED,2.2),
            ("fct_sales_line","SKIPPED",MUTED,1.4),("dashboards","still show yesterday's build",GREEN,2.2)],
           "✓ The failure stopped the branch: nothing wrong shipped.")
    o.append(text(12,y+44,"dbt build runs each model and then its tests, in dependency order, and skips everything downstream of a failure.",12,MUTED))
    o.append(text(12,y+62,"The run ends with a non-zero exit code, so the scheduler raises an alarm (Chapter 29's exit codes).",12,MUTED))
    return svg(W,y+74,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig32-1-project-layers.svg",fig_dag),("fig32-2-materializations.svg",fig_materializations),
                    ("fig32-3-build-stops-the-branch.svg",fig_build)]:
        open(name,"w").write(fn())
    print("ok32")
