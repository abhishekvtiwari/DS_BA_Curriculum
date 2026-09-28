# Generates the SVG figures for Chapter 6, Planning Your Learning. Run: python3 make_figs06.py
# Both figures print at the full text width (493.2 pt), so every font here is >= 7 pt in print:
# on a 720-740 px canvas the smallest size used (11.5 px) prints at about 7.7 pt.
# (The old Figure 6.2, a six-month plan, was replaced by the hours table in section 6.1 under D6.)
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GREY="#5b6475"


# ---------- Figure 6.1: a weekly rhythm (one bar per day, length = hours) ----------
def fig_week():
    days=[("Mon",1.0,"1 h","Read a new section",ACC),
          ("Tue",1.0,"1 h","Exercises from that section",GREEN),
          ("Wed",1.0,"1 h","Read the next section",ACC),
          ("Thu",1.0,"1 h","Exercises",GREEN),
          ("Fri",0.5,"30 min","Review: recap and key terms from memory",PURPLE),
          ("Sat",2.5,"2.5 h","Project or lab work",ORANGE),
          ("Sun",1.0,"1 h","Redo missed exercises; plan next week",PURPLE)]
    W=720; x0=24; BX=78; BMAX=240; DX=400; y0=62; RH=40
    o=[text(x0,32,"One week, about 8 hours",16,INK,"bold",family=HEAD)]
    o.append(text(BX,y0-8,"Hours",12,MUTED,"bold")); o.append(text(DX,y0-8,"What you do",12,MUTED,"bold"))
    for i,(d,h,lab,what,c) in enumerate(days):
        y=y0+i*RH
        if i%2==0: o.append(rect(x0-8,y,W-2*x0+16,RH,fill="#f6f9fc"))
        o.append(text(x0,y+26,d,14,INK,"bold",family=HEAD))
        bw=h/2.5*BMAX
        o.append(rect(BX,y+8,bw,24,fill=c,rx=4,extra='fill-opacity="0.22"'))
        o.append(rect(BX,y+8,5,24,fill=c))
        o.append(text(BX+bw+10,y+26,lab,13.5,c,"bold"))
        o.append(text(DX,y+26,what,13,INK))
    yb=y0+7*RH
    o.append(path(f"M{x0},{yb+8} H{W-x0}",stroke=RULE,sw=1.2))
    o.append(text(x0,yb+34,"Total: 1 + 1 + 1 + 1 + 0.5 + 2.5 + 1 = 8 hours",13.5,INK,"bold"))
    return svg(W,yb+50,"".join(o))


# ---------- Figure 6.2: the tool timeline (the chapter that first needs each tool) ----------
def fig_tools():
    tools=[("Chapter 10","Spreadsheets",["Excel or","Google Sheets"],["Windows, Mac,","browser"],ACC),
           ("Chapter 12","Databases",["PostgreSQL and","DBeaver (MySQL","optional)"],["Windows, Mac,","Linux"],GREEN),
           ("Chapter 16","Dashboards",["Power BI","Desktop"],["Windows only"],ORANGE),
           ("Chapter 17","Programming",["Python,","VS Code,","Jupyter"],["Windows, Mac,","Linux"],PURPLE),
           ("Chapter 26","Versions",["Git"],["Windows, Mac,","Linux"],GREY)]
    W=740; x0=22; CW=128; G=(W-2*x0-5*CW)/4; ly=78; cy=104; CH=196
    o=[text(x0,32,"The core toolkit, and the chapter that first needs each tool",16,INK,"bold",family=HEAD)]
    # the line of chapters, read left to right
    o.append(path(f"M{x0},{ly} H{W-x0-10}",stroke=RULE,sw=2.5))
    o.append(f'<path d="M{W-x0},{ly} l-12,-6 v12 Z" fill="{RULE}"/>')
    for i,(ch,group,names,os_,c) in enumerate(tools):
        x=x0+i*(CW+G); cx=x+CW/2
        o.append(text(cx,ly-14,ch,13.5,INK,"bold",anchor="middle"))
        o.append(f'<circle cx="{cx}" cy="{ly}" r="7" fill="#fff" stroke="{c}" stroke-width="3"/>')
        o.append(path(f"M{cx},{ly+7} V{cy}",stroke=c,sw=1.6))
        o.append(rect(x+2,cy+3,CW,CH,fill="#e9eef4",rx=9))
        o.append(rect(x,cy,CW,CH,fill="#fff",stroke=c,sw=1.8,rx=9))
        o.append(f'<path d="M{x},{cy+9} a9,9 0 0 1 9,-9 H{x+CW-9} a9,9 0 0 1 9,9 V{cy+34} H{x} Z" fill="{c}"/>')
        o.append(text(x+10,cy+23,group,13,"#fff","bold",family=HEAD))
        for k,ln in enumerate(names):
            o.append(text(x+10,cy+56+k*18,ln,12.5,INK,"bold"))
        o.append(text(x+10,cy+134,"Runs on:",11.5,MUTED))
        for k,ln in enumerate(os_):
            o.append(text(x+10,cy+152+k*17,ln,12,INK))
    fy=cy+CH+22
    o.append(rect(x0,fy,W-2*x0,50,fill="#f3f5f8",rx=8))
    o.append(text(x0+14,fy+21,"Each tool is installed at the start of the chapter that first uses it. Later parts add their",12.5,INK))
    o.append(text(x0+14,fy+39,"own tools when you reach them: dbt, cloud accounts, containers, and machine-learning libraries.",12.5,INK))
    return svg(W,fy+64,"".join(o))


if __name__=="__main__":
    for name,fn in [("fig6-1-weekly-rhythm.svg",fig_week),("fig6-2-tool-timeline.svg",fig_tools)]:
        open(name,"w").write(fn())
    print("ok")
