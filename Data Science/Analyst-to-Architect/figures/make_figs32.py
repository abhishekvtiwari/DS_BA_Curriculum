# Generates the SVG figures for Chapter 32. Run: python3 make_figs32.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def node(x,y,w,h,title,sub,color,fill="#fff"):
    o=[rect(x,y,w,h,fill=fill,stroke=color,sw=1.6,rx=7),
       text(x+w/2,y+(20 if sub else h/2+5),title,12,INK,"bold",anchor="middle",family=MONO)]
    if sub: o.append(text(x+w/2,y+36,sub,10.5,MUTED,anchor="middle"))
    return "".join(o)

def fig_dag():
    o=[text(30,32,"The graph dbt builds from your ref() and source() calls",14,INK,"bold",family=HEAD)]
    o.append(text(60,62,"ERP tables (sources)",12,MUTED,"bold")); o.append(text(330,62,"staging (views)",12,MUTED,"bold"))
    o.append(text(600,62,"marts (tables)",12,MUTED,"bold")); o.append(text(880,62,"used by",12,MUTED,"bold"))
    srcs=["orders","order_items","customers","products","employees"]
    for i,s in enumerate(srcs): o.append(node(40,80+i*52,200,40,s,None,RULE,"#f6f9fc"))
    stg=[("stg_orders",0),("stg_order_items",1),("stg_customers",2),("stg_products",3)]
    for name,i in stg: o.append(node(300,80+i*52,220,40,name,None,ACC))
    marts=[("dim_date",0),("dim_customer",1),("dim_product",2),("dim_sales_rep",3),("fct_sales_line",4),("fct_daily_sales",5)]
    for name,i in marts:
        col = PK if name.startswith("fct") else GREEN
        o.append(node(580,80+i*52,220,40,name,None,col,"#fdf3dc" if name.startswith("fct") else "#e2f3ee"))
    o.append(node(860,80+4*52,150,40,"Power BI",None,PURPLE))
    def link(x1,y1,x2,y2,c=RULE):
        o.append(path(f"M{x1},{y1} C{(x1+x2)/2},{y1} {(x1+x2)/2},{y2} {x2},{y2}",stroke=c,sw=1.3))
    for si,ti in [(0,0),(1,1),(2,2),(3,3)]:
        link(240,100+si*52,300,100+ti*52)
    link(240,100+4*52,580,100+3*52)      # employees -> dim_sales_rep
    link(520,100+3*52,580,100+2*52)      # stg_products -> dim_product
    link(520,100+1*52,580,100+4*52,PK)   # stg_order_items -> fct_sales_line
    link(520,100+0*52,580,100+4*52,PK)   # stg_orders -> fct
    link(520,100+1*52,580,100+5*52,PK); link(520,100+0*52,580,100+5*52,PK)
    for i in (0,1,2,3): link(800,100+i*52,580,100+4*52,GREEN)
    link(800,100+4*52,860,100+4*52,PURPLE)
    o.append(text(40,420,"Nobody wrote this order down. dbt reads the ref() and source() calls in the SQL and builds the graph, then runs it in dependency order,",12,MUTED))
    o.append(text(40,440,"four models at a time. The same graph becomes the lineage diagram in the documentation site.",12,MUTED))
    return svg(1040,460,"".join(o))

def fig_materializations():
    o=[text(30,32,"Four materializations, and what each one costs",14,INK,"bold",family=HEAD)]
    rows=[("view","CREATE VIEW: nothing is stored","build: free","query: the full query, every time","staging models",ACC),
          ("table","CREATE TABLE AS: rebuilt each run","build: full rebuild","query: fast","marts",GREEN),
          ("incremental","new rows only after the first build","build: 0.90 s vs 13.91 s here","query: fast","large fact tables",PK),
          ("ephemeral","pasted into the models that ref it","build: nothing exists","query: recomputed each time","small intermediate steps",PURPLE)]
    y=70
    for name,what,build,query,use,c in rows:
        o.append(rect(30,y,980,58,fill="#fff",stroke=c,sw=1.8,rx=7))
        o.append(text(52,y+24,name,13,c,"bold",family=MONO)); o.append(text(52,y+44,what,11.5,MUTED))
        o.append(text(330,y+24,build,12,INK)); o.append(text(330,y+44,query,12,INK))
        o.append(text(700,y+34,use,12,INK))
        y+=68
    o.append(text(30,y+18,"Set the default per folder in dbt_project.yml; override it in a model with {{ config(materialized='...') }}.",12,MUTED))
    return svg(1040,y+38,"".join(o))

def fig_build():
    o=[text(30,32,"Why dbt build, and not dbt run followed by dbt test",14,INK,"bold",family=HEAD)]
    o.append(text(60,66,"dbt run, then dbt test",13,RED,"bold"))
    steps=[("stg_order_items","built",GREEN),("fct_sales_line","built (with bad data)",GREEN),
           ("dashboards","refreshed from it",GREEN),("tests","fail, an hour later",RED)]
    y=90
    for name,what,c in steps:
        o.append(rect(50,y,420,44,fill="#fff",stroke=c,sw=1.6,rx=6))
        o.append(text(70,y+27,name,12,INK,"bold",family=MONO)); o.append(text(250,y+27,what,12,MUTED))
        if name!="tests": o.append(path(f"M260,{y+44} V{y+56}",stroke=RULE,sw=1.4))
        y+=56
    o.append(text(60,y+10,"Bad numbers reached people before anyone knew.",12,RED))
    o.append(text(570,66,"dbt build",13,GREEN,"bold"))
    steps=[("stg_order_items","built, then tested: pass",GREEN),("test on the grain","FAIL: duplicate order_item_id",RED),
           ("fct_sales_line","SKIPPED",MUTED),("dashboards","still showing yesterday's build",ACC)]
    y=90
    for name,what,c in steps:
        o.append(rect(560,y,420,44,fill="#fff",stroke=c,sw=1.6,rx=6))
        o.append(text(580,y+27,name,12,INK,"bold",family=MONO)); o.append(text(760,y+27,what,12,MUTED))
        if name!="dashboards": o.append(path(f"M770,{y+44} V{y+56}",stroke=RULE,sw=1.4))
        y+=56
    o.append(text(570,y+10,"The failure stopped the branch. Nothing wrong shipped.",12,GREEN))
    o.append(text(30,y+40,"dbt build runs each model and its tests together, in dependency order, and skips everything downstream of a failure. The run exits non-zero,",12,MUTED))
    o.append(text(30,y+60,"so the scheduler raises an alarm (Chapter 29's exit codes).",12,MUTED))
    return svg(1040,y+80,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig32-1-project-layers.svg",fig_dag),("fig32-2-materializations.svg",fig_materializations),
                    ("fig32-3-build-stops-the-branch.svg",fig_build)]:
        open(name,"w").write(fn())
    print("ok32")
