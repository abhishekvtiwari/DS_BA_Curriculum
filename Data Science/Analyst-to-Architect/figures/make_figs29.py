# Generates the SVG figures for Chapter 29. Run: python3 make_figs29.py
# Canvases are 800 px wide and print at the full text width (493.2 pt), so 12 px text prints at 7.4 pt:
# every label here is 12 px or larger (visual standard: 7 pt minimum).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREENBG="#e2f3ee"; REDBG="#fbeaea"; GREY="#f6f9fc"
W = 800

def box(x,y,w,h,title,sub=None,color=ACC,fill="#fff",mono=True):
    o=[rect(x,y,w,h,fill=fill,stroke=color,sw=1.6,rx=7),
       text(x+w/2,y+(21 if sub else h/2+5),title,14,INK,"bold",anchor="middle",family=(MONO if mono else None))]
    if sub: o.append(text(x+w/2,y+40,sub,12,MUTED,anchor="middle"))
    return "".join(o)

def fig_before_after():
    o=[text(20,30,"From one script to a package",16,INK,"bold",family=HEAD)]
    o.append(text(20,62,"Before: monthly_report.py (40 lines)",13,RED,"bold"))
    before=["connect with a password in the code","hard-coded month and file name","load every order line, filter in pandas",
            "calculate, print","bare except: target = 0","write Monthly_Report_Dec_FINAL.xlsx","print('done')"]
    problems=(0,1,4,5)
    for i,l in enumerate(before):
        y=76+i*34
        bad=i in problems
        o.append(rect(20,y,300,28,fill=REDBG if bad else GREY,stroke=RED if bad else RULE,sw=1.2 if bad else 1,rx=4))
        if bad: o.append(text(32,y+19,"✗",13,RED,"bold"))
        o.append(text(50,y+19,l,12,INK))
    o.append(rect(20,322,14,14,fill=REDBG,stroke=RED,sw=1.2,rx=2)); o.append(text(27,334,"✗",12,RED,"bold",anchor="middle"))
    o.append(text(42,333,"a problem this chapter fixes",12,MUTED))
    o.append(text(20,358,"Everything in one file, run top to bottom.",12,MUTED,style="italic"))
    o.append(path("M330,196 H352",stroke=INK,sw=2.5)); o.append(path("M344,189 L354,196 L344,203",stroke=INK,sw=2.5))
    X=368
    o.append(text(X,62,"After: riverstone-report/",13,GREEN,"bold",family=MONO))
    tree=[("pyproject.toml","what it needs; tools; the command",0),("uv.lock","exact versions of all 58 packages",0),
          ("src/riverstone_report/","",0),("config.py","settings, checked",1),("db.py","the only module with SQL",1),
          ("transform.py","pure calculations",1),("excel.py","the formatted workbook",1),("crm_client.py","retries, pages, rate limits",1),
          ("cli.py","riverstone-report --month",1),("errors.py","ReportError and its kinds",1),("tests/","23 tests",0)]
    for i,(n,d,ind) in enumerate(tree):
        y=88+i*25
        folder=n.endswith("/")
        o.append(text(X+ind*20,y,n,12.5,GREEN if folder else INK,"bold" if folder else "normal",family=MONO))
        if d: o.append(text(X+186,y,d,12,MUTED))
    o.append(text(X,358,"Each file has one job, so each can be read, tested,",12,MUTED,style="italic"))
    o.append(text(X,376,"and changed alone.",12,MUTED,style="italic"))
    return svg(W,392,"".join(o))

def fig_layers():
    o=[text(20,30,"Keep the calculations pure: input and output at the edges",16,INK,"bold",family=HEAD)]
    o.append(box(290,50,220,52,"cli.py","arguments, logging, exit code",color=INK))
    xs=[16,212,408,604]; bw=180
    mods=[("config.py","env vars → ReportConfig",ORANGE,"#fff","EDGE"),("db.py","SQL → DataFrame",ORANGE,"#fff","EDGE"),
          ("transform.py","DataFrame → results",GREEN,GREENBG,"CORE"),("excel.py","results → .xlsx",ORANGE,"#fff","EDGE")]
    for x,(n,sub,c,f,tag) in zip(xs,mods):
        o.append(text(x+bw/2,146,tag,12,c,"bold",anchor="middle"))
        o.append(box(x,154,bw,52,n,sub,color=c,fill=f))
        o.append(path(f"M400,102 V124 H{x+bw/2} V134",stroke=RULE,sw=1.6))
    o.append(box(xs[1],262,bw,48,"PostgreSQL","riverstone_2025",color=RULE,fill=GREY,mono=False))
    o.append(box(xs[3],262,bw,48,"reports/","monthly .xlsx files",color=RULE,fill=GREY))
    o.append(box(xs[0],262,bw,48,"environment","RIVERSTONE_… variables",color=RULE,fill=GREY,mono=False))
    for x in (xs[0],xs[1],xs[3]): o.append(path(f"M{x+bw/2},206 V262",stroke=ORANGE,sw=1.6,dash="5,4"))
    o.append(rect(xs[2],250,bw,68,fill="#fff",stroke=GREEN,sw=1.2,rx=6))
    for i,l in enumerate(["No database, no files:","tested with a 5-row","DataFrame in milliseconds"]):
        o.append(text(xs[2]+bw/2,270+i*18,l,12,GREEN,anchor="middle"))
    o.append(text(20,348,"EDGE modules (orange) touch the outside world and get a few integration tests.",12.5,MUTED))
    o.append(text(20,368,"The CORE (green) holds the business rules and gets many fast unit tests.",12.5,MUTED))
    return svg(W,384,"".join(o))

def fig_retries():
    o=[text(20,30,"Fetching 43 leads from the mock CRM API: two failures, no lost data",16,INK,"bold",family=HEAD)]
    steps=[("page 1","200","10 leads",GREEN),("page 2","503","wait 0.637 s (backoff + jitter)",RED),("page 2","200","10 leads",GREEN),
           ("page 3","429","wait 1.000 s (Retry-After: 1)",ORANGE),("page 3","200","10 leads",GREEN),("page 4","200","10 leads",GREEN),
           ("page 5","200","3 leads, next_page: null",GREEN)]
    y=52
    for pg,st,note,c in steps:
        o.append(rect(20,y,74,28,fill=GREY,stroke=RULE,rx=4)); o.append(text(57,y+19,pg,12.5,INK,"bold",anchor="middle",family=MONO))
        o.append(path(f"M94,{y+14} H160",stroke=MUTED,sw=1.5)); o.append(path(f"M152,{y+8} L162,{y+14} L152,{y+20}",stroke=MUTED,sw=1.5))
        o.append(rect(165,y,56,28,fill="#fff",stroke=c,sw=2,rx=4)); o.append(text(193,y+19,st,13,c,"bold",anchor="middle",family=MONO))
        o.append(text(232,y+19,note,12,INK))
        y+=38
    X=478; PW=306
    o.append(rect(X,52,PW,280,fill=GREY,stroke=RULE,rx=6))
    o.append(text(X+14,76,"The client's rules",13,INK,"bold"))
    rules=[["Retry 429, 500, 502, 503, 504,","connection errors, timeouts"],["Don't retry 400, 401, 403, 404:","retrying can't fix them"],
           ["Wait 0.5 s × 2^(attempt − 1),","plus jitter up to half of that"],["429 with Retry-After:","wait exactly that long"],
           ["Give up after 4 attempts:","raise CrmApiError"],["Always set a timeout: (3.05, 10) s"]]
    yy=102
    for item in rules:
        o.append(text(X+14,yy,"•",12,INK,"bold"))
        for j,l in enumerate(item):
            o.append(text(X+28,yy+j*16,l,12,INK,"bold" if j==0 else "normal"))
        yy+=16*len(item)+10
    o.append(text(20,356,"A real run against the local mock server; the waits are the chapter's output.",12,MUTED,style="italic"))
    return svg(W,370,"".join(o))

def fig_tests():
    o=[text(20,30,"What each kind of test is for",16,INK,"bold",family=HEAD)]
    rows=[("Unit tests","transform.py, config.py, and crm_client.py with a fake session","14 tests","milliseconds; no database or network",GREEN,590),
          ("Parametrized tests","parse_month (good and bad input), top_customers","3 tests → 8 cases","one test function, many inputs",PURPLE,440),
          ("Integration test","December 2025 against riverstone_2025","1 test","needs the database; skipped without it",ORANGE,290)]
    y=52
    for name,what,count,note,c,w in rows:
        o.append(rect(20,y,w,72,fill="#fff",stroke=c,sw=2,rx=8))
        o.append(text(34,y+24,name,13.5,c,"bold")); o.append(text(34,y+44,what,12,INK)); o.append(text(34,y+62,note,12,MUTED,style="italic"))
        o.append(text(w+36,y+42,count,13,INK,"bold"))
        y+=88
    o.append(text(20,y+14,"The integration test reconciles to a number the book already trusts:",12.5,MUTED))
    o.append(text(20,y+33,"December 2025 net revenue ₹4,39,823.50, 115.7% of target.",12.5,MUTED))
    return svg(W,y+48,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig29-1-script-to-package.svg",fig_before_after),("fig29-2-pure-core-layers.svg",fig_layers),
                    ("fig29-3-tests-by-kind.svg",fig_tests),("fig29-4-retries-and-pages.svg",fig_retries)]:
        open(name,"w").write(fn())
    print("ok29")
