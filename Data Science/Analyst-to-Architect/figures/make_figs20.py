# Figures for Chapter 20. Run from this folder:
#   python3 make_figs20.py            # the three diagrams (SVG)
#   python3 make_figs20.py --screens  # the two screenshots (PNG), rendered from real HTML with a browser
# The screenshots need the database: they run companion/ch20/daily_flash.py for 18 December 2025 first.
# Every canvas is 700 px wide and prints at 174 mm, so the smallest text (10.5 px) prints at 7.4 pt.
import math, os, pathlib, subprocess, sys
from make_figs import *

GREEN="#2f7d6d"; PURPLE="#7a4fa0"; GOLD="#b7791f"; RED="#b23b3b"; LIGHT="#dfe5ec"
HERE = pathlib.Path(__file__).resolve().parent
COMPANION = HERE.parent / "companion" / "ch20"

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def lines(x,y,rows,size,fill,step,weight="normal"):
    return "".join(text(x,y+i*step,r,size,fill,weight) for i,r in enumerate(rows))

# Figure 20.1: the ladder, as a staircase of bars with the notes inside each bar.
def ladder():
    rungs=[("1  Manual","Someone opens the files and does it","Every time, from scratch","0 hours saved",MUTED),
           ("2  Refreshable","Power Query, a model, or a saved query","One click, the same steps","Most of the errors gone",ACC),
           ("3  Scheduled","A script runs at a fixed time","Nobody has to remember","The report arrives",GREEN),
           ("4  Triggered","It runs when something happens","New file, form response, threshold","Minutes, not a day",PURPLE),
           ("5  Self-serve","People answer their own questions","A model or dashboard they trust","You stop being the bottleneck",GOLD)]
    o=[]; n=len(rungs)
    for i,(name,how,what,gain,c) in enumerate(rungs):
        y=10+(n-1-i)*74; w=420+i*65; x=10
        o.append(rect(x,y,w,64,fill="#fff",stroke=c,sw=1.6,rx=7)); o.append(rect(x,y,9,64,fill=c))
        o.append(text(x+22,y+22,name,13.5,c,"bold")); o.append(text(x+w-12,y+22,gain,11.5,INK,"bold",anchor="end"))
        o.append(text(x+22,y+40,how,11,INK)); o.append(text(x+22,y+56,what,11,MUTED))
    o.append(text(10,n*74+22,"Climbing costs effort and adds things that can break:",11.5,MUTED))
    o.append(text(10,n*74+40,"every rung above 2 needs logging, a failure alert, and an owner.",11.5,MUTED))
    return svg(700,n*74+50,"".join(o))

# Figure 20.2: the flow, in two rows of three steps.
def flow():
    steps=[("ERP export","daily, 02:00","automatic",GREEN),("Analyst opens 4 files","08:30","MANUAL 25 min",RED),
           ("Clean and combine","in a workbook","MANUAL 30 min",RED),("Pivot + chart","in the same workbook","MANUAL 20 min",RED),
           ("Write commentary","3 sentences","judgment: keep",GOLD),("Email 14 managers","by 10:00","MANUAL 5 min",RED)]
    o=[]; bw,bh,gap=200,92,45
    pos=[(10+(i%3)*(bw+gap), 10+(i//3)*(bh+40)) for i in range(6)]
    for i,((name,when,kind,c),(x,y)) in enumerate(zip(steps,pos)):
        o.append(rect(x,y,bw,bh,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(text(x+12,y+24,f"{i+1}  {name}",12.5,INK,"bold")); o.append(text(x+12,y+44,when,11,MUTED))
        o.append(rect(x+12,y+56,bw-24,24,fill=c,rx=4)); o.append(text(x+bw/2,y+72.5,kind,11,"#fff","bold",anchor="middle"))
        if i%3<2: o.append(arrow(x+bw+3,y+bh/2,x+bw+gap-3,y+bh/2))
    x3,y3=pos[2]; x4,y4=pos[3]
    o.append(path(f"M{x3+bw/2},{y3+bh+2} V{y3+bh+20} H{x4+bw/2} V{y4-9}",stroke=MUTED,sw=1.6))
    o.append(arrow(x4+bw/2,y4-10,x4+bw/2,y4-2))
    by=10+2*(bh+40)-8
    o.append(rect(10,by,680,84,fill="#fff",stroke=ACC,sw=1.5,rx=8)); o.append(rect(10,by,9,84,fill=ACC))
    o.append(text(32,by+24,"What the map tells you",12.5,INK,"bold"))
    o.append(text(32,by+45,"80 minutes a day are mechanical; 3 sentences are judgment. Automate the 80,",11.5,INK))
    o.append(text(32,by+64,"keep the 3. Time the steps for a week first: people misjudge which step is slow.",11.5,INK))
    return svg(700,by+94,"".join(o))

# Figure 20.5: six properties, in a 2 x 3 grid.
def trust():
    items=[("It says what it did",["A log line per run: rows, totals,","and the time it took"],"logging, run history",ACC),
           ("It checks before it sends",["Row counts, date range, and","today against the recent median"],"fail = no email",GREEN),
           ("It tells you when it breaks",["A failure alert to a person,","not a mailbox nobody reads"],"alert on failure",RED),
           ("It handles 'nothing today'",["Says \"no sales recorded\"","instead of an empty table"],"explicit empty case",GOLD),
           ("It can be run twice",["Same input, same output,","and no duplicate emails"],"idempotent",PURPLE),
           ("Someone else can run it",["Documented inputs, credentials","in the environment, an owner"],"handover note",MUTED)]
    o=[]; cw,ch=335,100
    for i,(title,detail,tag,c) in enumerate(items):
        x=10+(i%2)*(cw+10); y=10+(i//2)*(ch+10)
        o.append(rect(x,y,cw,ch,fill="#fff",stroke=RULE,rx=7)); o.append(rect(x,y,8,ch,fill=c))
        o.append(text(x+22,y+24,title,12.5,INK,"bold")); o.append(lines(x+22,y+44,detail,11,MUTED,16))
        o.append(rect(x+22,y+70,len(tag)*6.4+20,20,fill=c,rx=10)); o.append(text(x+32,y+84,tag,10.5,"#fff","bold"))
    fy=10+3*(ch+10)+12
    o.append(text(10,fy,"A report people trust is one they can check: the numbers, when it ran, and what it excluded.",11.5,MUTED))
    return svg(700,fy+10,"".join(o))

# ---------------------------------------------------------------- screenshots (PNG)

TILE_HTML = """<table role="presentation" cellpadding="0" cellspacing="0" style="background:#f3f6fa;border:1px solid #dfe5ec;border-radius:6px">
  <tr><td style="padding:10px 12px">
    <div style="font:12px Arial,sans-serif;color:#5b6475">Net revenue</div>
    <div style="font:bold 20px Arial,sans-serif;color:#1d2330;padding-top:2px">₹2,511,819</div>
    <div style="font:12px Arial,sans-serif;color:#2f7d6d;padding-top:2px">+2.3% vs last year</div>
  </td></tr>
</table>"""

def shoot(html, out, width, scale=3):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": width, "height": 200}, device_scale_factor=scale)
        p.set_content(html); p.wait_for_timeout(300)
        p.locator("#shot").screenshot(path=str(out)); b.close()

def screens():
    # Figure 20.4: the tile as plain HTML (left) and the row built by tile() in Python (right), as a browser draws them.
    sys.path.insert(0, str(COMPANION)); import daily_flash as f
    row = ("<table role='presentation'><tr>" + f.tile("Net revenue", "₹2,511,819", "+2.3% vs last year", f.GOOD)
           + f.tile("Orders", "118", "116 customers") + "</tr></table>")
    label = "font:11px Arial,sans-serif;color:#5b6475;padding-bottom:6px"
    page = (f"<body style='margin:0;background:#fff'><div id='shot' style='width:668px;padding:14px 16px;display:flex;gap:40px;"
            f"border:1px solid #c9d3df'><div><div style='{label}'>The plain HTML, as written by hand</div>{TILE_HTML}</div>"
            f"<div><div style='{label}'>row: two tiles built by tile()</div>{row}</div></div></body>")
    shoot(page, HERE / "fig20-4-kpi-tile.png", 700)
    # Figure 20.3: the Flash as a recipient sees it, framed as an email window with its real subject line.
    env = dict(os.environ)
    run = subprocess.run([sys.executable, "daily_flash.py", "2025-12-18"], cwd=COMPANION, env=env,
                         capture_output=True, text=True, check=True)
    subject = run.stdout.strip().splitlines()[-1]
    body = (COMPANION / "out" / "daily_flash_2025-12-18.html").read_text(encoding="utf-8")
    inner = body.split("<body", 1)[1].split(">", 1)[1].rsplit("</body>", 1)[0]
    chrome = ("font:12px Arial,sans-serif;color:#1d2330;background:#eef2f7;border-bottom:1px solid #c9d3df;"
              "padding:8px 16px")
    page = (f"<body style='margin:0;background:#fff'><div id='shot' style='width:672px;margin:0 0 18px 0;"
            f"border:1px solid #9aa7b8;border-radius:6px;overflow:hidden'>"
            f"<div style='{chrome}'><b>Subject:</b> {subject}</div>"
            f"<div style='padding:16px'>{inner}</div></div></body>")
    shoot(page, HERE / "fig20-3-daily-flash-email.png", 700, scale=3.2)

if __name__ == "__main__":
    os.chdir(HERE)
    for n,fn in [("fig20-1-automation-ladder.svg",ladder),("fig20-2-report-flow.svg",flow),("fig20-5-trustworthy.svg",trust)]:
        open(n,"w").write(fn())
    if "--screens" in sys.argv:
        screens()
    print("ok")
