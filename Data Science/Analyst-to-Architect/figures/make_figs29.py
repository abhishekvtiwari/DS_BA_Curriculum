# Generates the SVG figures for Chapter 29. Run: python3 make_figs29.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def box(x,y,w,h,title,sub=None,color=ACC,fill="#fff",mono=False):
    o=[rect(x,y,w,h,fill=fill,stroke=color,sw=1.6,rx=7),
       text(x+w/2,y+(20 if sub else h/2+5),title,12.5,INK,"bold",anchor="middle",family=(MONO if mono else None))]
    if sub: o.append(text(x+w/2,y+37,sub,11,MUTED,anchor="middle"))
    return "".join(o)

def fig_before_after():
    o=[text(30,32,"From one script to a package",14,INK,"bold",family=HEAD)]
    o.append(text(30,66,"Before: monthly_report.py (40 lines)",13,RED,"bold"))
    before=["connect with a password in the code","hard-coded month and file name","load every order line, filter in pandas",
            "calculate, print","bare except: target = 0","write Monthly_Report_Dec_FINAL.xlsx","print('done')"]
    for i,l in enumerate(before):
        o.append(rect(30,80+i*34,330,28,fill="#fbeaea" if i in (0,1,4,5) else "#f6f9fc",stroke=RULE,rx=4))
        o.append(text(44,99+i*34,l,12,INK))
    o.append(text(30,338,"Everything in one file, run top to bottom.",12,MUTED,style="italic"))
    o.append(path("M385,200 H445",stroke=INK,sw=2.5)); o.append(path("M436,193 L447,200 L436,207",stroke=INK,sw=2.5))
    X=470
    o.append(text(X,66,"After: riverstone-report/",13,GREEN,"bold",family=MONO))
    tree=[("pyproject.toml","dependencies, tools, entry point",0),("uv.lock","exact versions of 32 packages",0),
          ("src/riverstone_report/","",0),("config.py","settings from env vars, validated",1),("db.py","the only module with SQL",1),
          ("transform.py","pure calculations",1),("excel.py","formatted workbook",1),("crm_client.py","retries, pages, rate limits",1),
          ("cli.py","riverstone-report --month",1),("errors.py","ReportError and friends",1),("tests/","23 tests",0)]
    for i,(n,d,ind) in enumerate(tree):
        y=92+i*24
        o.append(text(X+ind*26,y,n,12,GREEN if n.endswith("/") else INK,"bold" if n.endswith("/") else "normal",family=MONO))
        if d: o.append(text(X+250,y,d,11.5,MUTED))
    o.append(text(X,372,"Each file has one job, so each can be read, tested, and changed alone.",12,MUTED,style="italic"))
    return svg(1040,390,"".join(o))

def fig_layers():
    o=[text(30,32,"Keep the calculations pure: input and output live at the edges",14,INK,"bold",family=HEAD)]
    o.append(box(410,56,220,48,"cli.py","reads arguments, sets up logging",color=INK))
    o.append(box(60,150,200,48,"config.py","environment → ReportConfig",color=PURPLE))
    o.append(box(300,150,200,48,"db.py","SQL → DataFrame",color=ORANGE))
    o.append(box(540,150,200,48,"transform.py","DataFrame → results",color=GREEN,fill="#e2f3ee"))
    o.append(box(780,150,200,48,"excel.py","results → .xlsx",color=ORANGE))
    for x in (160,400,640,880): o.append(path(f"M520,104 V124 H{x} V150",stroke=RULE,sw=1.6))
    o.append(box(300,250,200,44,"PostgreSQL","riverstone_2025",color=RULE,fill="#f6f9fc"))
    o.append(box(780,250,200,44,"reports/ folder","riverstone_monthly_2025-12.xlsx",color=RULE,fill="#f6f9fc"))
    o.append(path("M400,198 V250",stroke=ORANGE,sw=1.6,dash="5,4")); o.append(path("M880,198 V250",stroke=ORANGE,sw=1.6,dash="5,4"))
    o.append(rect(540,240,200,64,fill="#fff",stroke=GREEN,sw=1.2,rx=6))
    for i,l in enumerate(["No database, no files:","tested with a 5-row","DataFrame in milliseconds"]): o.append(text(640,260+i*16,l,11.5,GREEN,anchor="middle"))
    o.append(text(30,338,"Orange modules touch the outside world and get a few integration tests. The green core holds the business rules and gets many fast unit tests.",12,MUTED))
    return svg(1040,355,"".join(o))

def fig_retries():
    o=[text(30,32,"Fetching 43 leads from the mock CRM API: two failures, no lost data",14,INK,"bold",family=HEAD)]
    steps=[("page 1","200","10 leads",GREEN,None),("page 2","503","wait 0.637 s (backoff + jitter)",RED,None),("page 2","200","10 leads",GREEN,None),
           ("page 3","429","wait 1.000 s (Retry-After: 1)",ORANGE,None),("page 3","200","10 leads",GREEN,None),("page 4","200","10 leads",GREEN,None),("page 5","200","3 leads, next_page: null",GREEN,None)]
    y=62
    for i,(pg,st,note,c,_) in enumerate(steps):
        o.append(rect(40,y,90,30,fill="#f6f9fc",stroke=RULE,rx=4)); o.append(text(85,y+20,pg,12,INK,"bold",anchor="middle",family=MONO))
        o.append(path(f"M130,{y+15} H250",stroke=MUTED,sw=1.5)); o.append(path(f"M242,{y+9} L252,{y+15} L242,{y+21}",stroke=MUTED,sw=1.5))
        o.append(rect(255,y,70,30,fill="#fff",stroke=c,sw=2,rx=4)); o.append(text(290,y+20,st,12.5,c,"bold",anchor="middle",family=MONO))
        o.append(text(340,y+20,note,12,INK))
        y+=40
    X=640
    o.append(rect(X,62,370,270,fill="#f6f9fc",stroke=RULE,rx=6))
    rules=["Retry: 429, 500, 502, 503, 504,","  connection errors, timeouts","Don't retry: 400, 401, 403, 404","  (retrying can't fix them)",
           "Wait: 0.5 s × 2^(attempt−1),","  plus random jitter up to half","429 with Retry-After: wait that long","Give up after 4 attempts: raise CrmApiError","Always set a timeout: (3.05, 10) s"]
    for i,l in enumerate(rules): o.append(text(X+16,90+i*27,l,12,INK,"bold" if not l.startswith("  ") else "normal"))
    o.append(text(30,355,"Real run on the local mock server; the wait times are from the chapter's output.",11.5,MUTED,style="italic"))
    return svg(1040,370,"".join(o))

def fig_tests():
    o=[text(30,32,"What each kind of test is for",14,INK,"bold",family=HEAD)]
    rows=[("Unit tests","transform.py, config.py, and crm_client.py with a fake session","14 tests","milliseconds; no database or network",GREEN,760),
          ("Parametrized tests","parse_month (good and bad input), top_customers","3 tests → 8 cases","one test function, many inputs",PURPLE,560),
          ("Integration test","December 2025 against riverstone_2025","1 test","needs the database; skipped without it",ORANGE,360)]
    y=70
    for name,what,count,note,c,w in rows:
        o.append(rect(30,y,w,70,fill="#fff",stroke=c,sw=2,rx=8))
        o.append(text(46,y+26,name,13,c,"bold")); o.append(text(46,y+48,what,12,INK)); o.append(text(46,y+64,note,11,MUTED,style="italic"))
        o.append(text(w+50,y+40,count,12.5,INK,"bold"))
        y+=90
    o.append(text(30,y+10,"The integration test reconciles to a number the book already trusts: December 2025 net revenue ₹439,823.50, 115.7% of target.",12,MUTED))
    return svg(1040,y+30,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig29-1-script-to-package.svg",fig_before_after),("fig29-2-pure-core-layers.svg",fig_layers),
                    ("fig29-3-tests-by-kind.svg",fig_tests),("fig29-4-retries-and-pages.svg",fig_retries)]:
        open(name,"w").write(fn())
    print("ok29")
