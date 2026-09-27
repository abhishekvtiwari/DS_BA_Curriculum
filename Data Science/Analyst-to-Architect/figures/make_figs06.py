# Generates the SVG figures for Chapter 6. Run: python3 make_figs06.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"; TEAL="#1f6fa3"

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.4), y2-L*math.sin(a-0.4)); p2=(x2-L*math.cos(a+0.4), y2-L*math.sin(a+0.4))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 6.1: the toolkit along the analyst path ----------
def fig_toolkit():
    o=[]
    tools=[("Spreadsheets","Excel or|Google Sheets","Ch 10–11, 19",ACC,"Windows, Mac, browser"),
           ("Databases","PostgreSQL, MySQL,|DBeaver","Ch 12–13, 14, 28",GREEN,"Windows, Mac, Linux"),
           ("Business intelligence","Power BI|Desktop","Ch 16",ORANGE,"Windows only"),
           ("Python","Python, VS Code,|Jupyter","Ch 17–18, 20–22, Part IV",PURPLE,"Windows, Mac, Linux"),
           ("Version control","Git","Ch 26 onward",GREY,"Windows, Mac, Linux")]
    W=182; G=22; x0=30; y=70
    o.append(text(x0,34,"The core toolkit, in the order the book first uses it",15,INK,"bold",family=HEAD))
    for i,(t,sub,ch,c,os_) in enumerate(tools):
        x=x0+i*(W+G)
        o.append(rect(x+2,y+3,W,180,fill="#e9eef4",rx=10)); o.append(rect(x,y,W,180,fill="#fff",stroke=c,sw=1.8,rx=10))
        o.append(f'<path d="M{x},{y+10} a10,10 0 0 1 10,-10 H{x+W-10} a10,10 0 0 1 10,10 V{y+40} H{x} Z" fill="{c}"/>')
        o.append(text(x+12,y+26,t,13.5,"#fff","bold",family=HEAD))
        [o.append(text(x+12,y+62+k*16,ln,12,INK,"bold")) for k,ln in enumerate(sub.split("|"))]
        o.append(text(x+12,y+104,"First used:",11.5,MUTED)); o.append(text(x+12,y+121,ch,12.5,INK))
        o.append(text(x+12,y+150,"Runs on:",11.5,MUTED)); o.append(text(x+12,y+167,os_,12,INK))
        if i<4: o.append(arrow(x+W+3,y+85,x+W+G-3,y+85,c=RULE))
    o.append(rect(x0,275,5*W+4*G,44,fill="#f3f5f8",rx=8))
    o.append(text(x0+14,302,"Later parts install their own tools when you reach them: dbt, the command line, cloud accounts, containers, and ML libraries.",12.5,INK))
    return svg(2*x0+5*W+4*G,340,"".join(o))

# ---------- Figure 6.2: a sample 6-month analyst plan ----------
def fig_plan():
    o=[]
    months=[("Month 1","Weeks 1–4","Part 0 and Part I: Chapters 1–9","foundations, the map, how learning works",GREY),
            ("Month 2","Weeks 5–8","Chapters 10–11: spreadsheets","Excel and Google Sheets, pivot tables, Power Query",ACC),
            ("Month 3","Weeks 9–12","Chapters 12–13: SQL","queries on the Riverstone database, in PostgreSQL and MySQL",GREEN),
            ("Month 4","Weeks 13–17","Chapters 14–16: cleaning, charts, Power BI","a first dashboard",ORANGE),
            ("Month 5","Weeks 18–22","Chapters 17–18 and 21–22: Python, statistics","pandas, descriptive statistics, not fooling yourself",PURPLE),
            ("Month 6","Weeks 23–26","Chapters 19–20 and 23–27: automation, business, portfolio","capstone project; start interview practice (Chapters 68–71)",RED)]
    x0=30; y0=60; H=58; G=12
    o.append(text(x0,34,"A sample six-month plan at about 8 hours a week",15,INK,"bold",family=HEAD))
    for i,(m,w,what,detail,c) in enumerate(months):
        y=y0+i*(H+G)
        o.append(rect(x0,y,120,H,fill=c,rx=8)); o.append(text(x0+60,y+25,m,14,"#fff","bold",anchor="middle",family=HEAD)); o.append(text(x0+60,y+44,w,11.5,"#fff",anchor="middle"))
        o.append(rect(x0+130,y,760,H,fill="#fff",stroke=c,sw=1.5,rx=8))
        o.append(text(x0+146,y+25,what,13.5,INK,"bold")); o.append(text(x0+146,y+45,detail,12,MUTED))
    y=y0+6*(H+G)
    o.append(text(x0,y+10,"Every week: one review session, the chapter exercises, and a little SQL or Python practice on something you've already learned.",12.5,INK,style="italic"))
    return svg(950,y+30,"".join(o))

# ---------- Figure 6.3: a weekly rhythm ----------
def fig_week():
    o=[]
    days=[("Mon","1 h","Read a new section; type out the examples",ACC),("Tue","1 h","Exercises from that section",GREEN),
          ("Wed","1 h","Read the next section",ACC),("Thu","1 h","Exercises",GREEN),
          ("Fri","30 min","Review: recap and key terms from memory",PURPLE),("Sat","2.5 h","Project or lab work",ORANGE),
          ("Sun","1 h","Redo missed exercises; plan next week",PURPLE)]
    x0=30; W=128; G=10; y=60
    o.append(text(x0,34,"One week, about 8 hours",15,INK,"bold",family=HEAD))
    maxh=2.5
    for i,(d,h,what,c) in enumerate(days):
        x=x0+i*(W+G)
        hrs={"1 h":1,"30 min":0.5,"2.5 h":2.5}[h]
        bh=40+hrs/maxh*130
        o.append(rect(x,y+170-bh+30,W,bh,fill=c,rx=8,extra='fill-opacity="0.15"')); o.append(rect(x,y+170-bh+30,W,6,fill=c,rx=3))
        o.append(text(x+W/2,y+18,d,14,INK,"bold",anchor="middle",family=HEAD))
        o.append(text(x+W/2,y+170-bh+56,h,15,c,"bold",anchor="middle"))
        words=what.split(); lines=[]; cur=""
        for wd in words:
            if len(cur+" "+wd)>17: lines.append(cur); cur=wd
            else: cur=(cur+" "+wd).strip()
        lines.append(cur)
        for j,l in enumerate(lines): o.append(text(x+W/2,y+230+j*17,l,12,INK,anchor="middle"))
    return svg(2*x0+7*W+6*G,y+300,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig6-1-toolkit-at-a-glance.svg",fig_toolkit),("fig6-2-six-month-plan.svg",fig_plan),("fig6-3-weekly-rhythm.svg",fig_week)]:
        open(name,"w").write(fn())
    print("ok")
