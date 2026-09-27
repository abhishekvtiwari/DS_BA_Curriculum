# Diagrams for Chapter 17 (Python from Zero). Run: python3 make_figs17.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def card(x,y,w,h,title,c,lines,size=10.8):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=8),rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+26} H{x} Z" fill="{c}"/>',
       text(x+11,y+18,title,11.8,"#fff","bold",family=HEAD)]
    for i,l in enumerate(lines): o.append(text(x+11,y+46+i*17,l,size,INK))
    return "".join(o)

def f1():
    o=[text(30,32,"Three ways to run Python, and what each is for",14.5,INK,"bold",family=HEAD)]
    o.append(card(30,60,270,190,"The REPL",ACC,["Type python, get >>>","Each line runs as you press Enter","Prints the value of an expression","Nothing is saved","", "Use for: trying one thing,","checking what a function does"]))
    o.append(card(330,60,270,190,"A notebook (Jupyter)",GREEN,["Cells of code, output underneath","Notes and charts in between","State lives between cells","Cells can run out of order","","Use for: exploring data,","showing your working"]))
    o.append(card(630,60,270,190,"A script (.py)",PURPLE,["Runs top to bottom, every time","Only print() shows anything","Takes arguments, returns an exit code","Can be scheduled and versioned","","Use for: anything repeated,","shared, or run at 6 a.m."]))
    o.append(arrow(600,280,330,280,MUTED)); o.append(text(360,272,"when it works, move it into a script (section 17.14)",11.5,MUTED))
    return svg(930,300,"".join(o))

def f2():
    o=[text(30,32,"How to read a traceback",14.5,INK,"bold",family=HEAD)]
    o.append(rect(30,56,700,150,fill="#fff",stroke=RULE,rx=8))
    lines=["Traceback (most recent call last):",
           "  File \"summarize.py\", line 41, in <module>",
           "    raise SystemExit(main(folder))",
           "  File \"summarize.py\", line 28, in main",
           "    s = summarize(path)",
           "  File \"summarize.py\", line 19, in summarize",
           "    values.append(float(row[\"net_revenue\"]))",
           "ValueError: could not convert string to float: ''"]
    for i,l in enumerate(lines):
        c = RED if i==len(lines)-1 else INK
        o.append(text(46,80+i*17,l,10.6,c,"bold" if i==len(lines)-1 else None,family=MONO))
    o.append(arrow(760,196,742,196,RED)); o.append(text(768,192,"1. Read this first: what went wrong",11.6,RED,"bold"))
    o.append(arrow(760,175,742,175,ACC)); o.append(text(768,171,"2. Then this: the line that failed",11.6,ACC,"bold"))
    o.append(arrow(760,158,742,158,ACC)); o.append(text(768,154,"3. Your file and line number",11.6,ACC,"bold"))
    o.append(arrow(760,90,742,90,MUTED)); o.append(text(768,86,"4. The chain that led there (top = oldest)",11.6,MUTED))
    o.append(rect(30,222,1170,52,fill="#fff",stroke=GREEN,sw=1.5,rx=8)); o.append(rect(30,222,8,52,fill=GREEN))
    o.append(text(52,244,"What it tells you here:",12.2,INK,"bold"))
    o.append(text(52,264,"a blank net_revenue in the CSV reached float(). Fix by converting defensively and counting what failed (section 17.12).",11.4,MUTED))
    return svg(1210,290,"".join(o))

def f3():
    o=[text(30,32,"Which collection should I use?",14.5,INK,"bold",family=HEAD)]
    rows=[("list","Ordered, changeable","order lines in a file; the months of the year","values[0] · append() · sorted()",ACC),
          ("tuple","Fixed, unchangeable","(city, region); what a function returns","city, region = pair",GOLD),
          ("dict","Lookup: key → value","city → region; product → price; counts","d[k] · d.get(k, default) · d.items()",GREEN),
          ("set","Unique, fast membership","distinct cities; codes in A but not B","a & b · a | b · a - b",PURPLE),
          ("DataFrame","Rows and columns (Chapter 18)","a whole CSV, a query result","df.groupby() · df.merge()",MUTED)]
    for i,(name,what,egs,ops,c) in enumerate(rows):
        y=64+i*62
        o.append(rect(30,y,1080,50,fill="#fff",stroke=RULE,rx=6)); o.append(rect(30,y,8,50,fill=c))
        o.append(text(54,y+31,name,13,c,"bold",family=MONO))
        o.append(text(170,y+22,what,11.6,INK,"bold")); o.append(text(170,y+40,egs,11.2,MUTED))
        o.append(text(640,y+31,ops,11.2,INK,family=MONO))
    return svg(1130,64+5*62+16,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig17-1-three-ways-to-run.svg",f1),("fig17-2-traceback.svg",f2),("fig17-3-collections.svg",f3)]:
        open(n,"w").write(f())
    print("ok")
