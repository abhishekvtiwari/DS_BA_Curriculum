# Generates the SVG figures for Chapter 33. Run: python3 make_figs33.py
# Every canvas is 700 px wide and prints at 174 mm (493.2 pt), so 10 px of text prints at 7.05 pt;
# the smallest text here is 10.5 px (7.4 pt).
# Figure 33.1's side panel reads the measured times from checks/ch33_timings_log.txt.
# Figure 33.2's bucket numbers are the real hash() % 8 values printed in section 33.3.
import math, pathlib, re
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=700
LOG=(pathlib.Path(__file__).resolve().parents[1]/"checks"/"ch33_timings_log.txt").read_text(encoding="utf-8")

def measured(pattern):
    return re.search(pattern, LOG).group(1)

def fig_growth():
    o=[text(20,26,"How the work grows: five shapes on one scale",13,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=72,462,300,70                  # plot box: n from 0 to 100, work from 0 to 120
    YMAX=120
    def px(n): return x0+n/100*(x1-x0)
    def py(v): return y0-v/YMAX*(y0-y1)
    # axes, ticks and grid
    o.append(path(f"M{x0},{y0} H{x1}",stroke=MUTED,sw=1.2)); o.append(path(f"M{x0},{y0} V{y1}",stroke=MUTED,sw=1.2))
    for n in (0,25,50,75,100):
        o.append(path(f"M{px(n):.1f},{y0} v5",stroke=MUTED,sw=1)); o.append(text(px(n),y0+18,str(n),10.5,MUTED,anchor="middle"))
    for v in (0,40,80,120):
        o.append(path(f"M{x0},{py(v):.1f} h-5",stroke=MUTED,sw=1)); o.append(text(x0-8,py(v)+4,str(v),10.5,MUTED,anchor="end"))
        if v: o.append(path(f"M{x0},{py(v):.1f} H{x1}",stroke="#e6ebf1",sw=1))
    o.append(text((x0+x1)/2,y0+36,"input size n",11,INK,anchor="middle"))
    o.append(f'<text x="22" y="{(y0+y1)/2:.0f}" font-size="11" fill="{INK}" text-anchor="middle" transform="rotate(-90 22 {(y0+y1)/2:.0f})">work (steps)</text>')
    curves=[("O(1)",lambda n: 3,GREEN),("O(log n)",lambda n: 2*math.log2(n) if n>=1 else 0,ACC),
            ("O(n)",lambda n: n,PURPLE),("O(n log n)",lambda n: n*math.log2(n) if n>=1 else 0,ORANGE),
            ("O(n²)",lambda n: n*n,RED)]
    for label,fn,c in curves:
        pts=[]; n=0.0
        while n<=100:
            v=fn(n)
            if v>YMAX:                      # leave through the top edge of the chart
                lo,hi=n-0.25,n
                for _ in range(30):
                    mid=(lo+hi)/2
                    lo,hi=(mid,hi) if fn(mid)<=YMAX else (lo,mid)
                pts.append((px(lo),py(YMAX))); break
            pts.append((px(n),py(v))); n+=0.25
        dash = {"O(1)":None,"O(log n)":"6 3","O(n)":None,"O(n log n)":"2 3","O(n²)":None}[label]
        o.append(path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=2.4,dash=dash))
        ex,ey=pts[-1]
        if ey<=py(YMAX)+0.5:                # left through the top: label above the exit point
            if label=="O(n²)":
                o.append(text(ex-2,y1-8,"O(n²) quadratic",11,c,"bold",anchor="end"))
            else:
                o.append(text(ex+2,y1-8,"O(n log n)",11,c,"bold"))
        else:                                # reached n = 100: label at the line end
            words={"O(1)":"O(1) constant","O(log n)":"O(log n)","O(n)":"O(n) linear"}[label]
            dy={"O(1)":2,"O(log n)":-3,"O(n)":4}[label]
            o.append(text(x1+6,ey+dy,words,11,c,"bold"))
    # measured panel
    px0=556
    o.append(rect(px0,60,136,250,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(px0+8,80,"Measured:",11,INK,"bold")); o.append(text(px0+8,95,"naive matching",11,INK,"bold"))
    rows=[(n,measured(rf"{n:>5} invoices x 176,110 order lines:\s+([\d.]+) s")) for n in (250,500,1000,2000)]
    y=115
    for n,t in rows:
        o.append(text(px0+8,y,f"{n:>5,} inv.",10.5,INK,family=MONO)); o.append(text(px0+128,y,f"{t} s",10.5,INK,anchor="end",family=MONO)); y+=17
    pred=measured(r"predicted for 20,000 invoices: (\d+) s")
    o.append(text(px0+8,y+4,"20,000 inv.",10.5,INK,family=MONO)); o.append(text(px0+128,y+4,f"~{pred} s",10.5,INK,anchor="end",family=MONO))
    o.append(text(px0+8,y+18,"(predicted)",10.5,MUTED))
    y+=48
    o.append(text(px0+8,y,"With a",11,GREEN,"bold")); o.append(text(px0+8,y+15,"dictionary index:",11,GREEN,"bold"))
    o.append(text(px0+8,y+34,"build",10.5,GREEN,family=MONO)); o.append(text(px0+128,y+34,measured(r"build the index over 176,110 lines: ([\d.]+) s")+" s",10.5,GREEN,anchor="end",family=MONO))
    o.append(text(px0+8,y+51,"match",10.5,GREEN,family=MONO)); o.append(text(px0+128,y+51,measured(r"look up all 20,000 invoices:\s+([\d.]+) s")+" s",10.5,GREEN,anchor="end",family=MONO))
    o.append(text(20,y0+62,"Doubling n doubles the work of a linear algorithm and quadruples a quadratic one. The curves are drawn",10.5,MUTED))
    o.append(text(20,y0+78,"to one scale (O(1) as 3 steps, O(log n) as 2 × log₂ n); the times on the right were measured.",10.5,MUTED))
    return svg(W,y0+90,"".join(o))

def fig_hash():
    o=[text(20,26,"Why a dictionary lookup does not get slower as it grows",13,INK,"bold",family=HEAD)]
    keys=[("(100001, 101)",7),("(100002, 104)",6),("(100003, 108)",0),("(100004, 105)",7)]
    # the real values, recomputed here so the figure can't drift from the code
    for k,b in keys:
        t=tuple(int(x) for x in k.strip("()").split(", "))
        assert hash(t)%8==b, (k,hash(t)%8)
    y=52
    for k,b in keys:
        o.append(rect(20,y,122,30,fill="#fff",stroke=ACC,sw=1.4,rx=5)); o.append(text(81,y+20,k,11,INK,"bold",anchor="middle",family=MONO))
        o.append(path(f"M142,{y+15} H160",stroke=MUTED,sw=1.4)); o.append(path(f"M154,{y+10} L161,{y+15} L154,{y+20}",stroke=MUTED,sw=1.4))
        o.append(rect(163,y,92,30,fill="#f6f9fc",stroke=RULE,rx=5)); o.append(text(209,y+20,"hash() % 8",11,MUTED,anchor="middle",family=MONO))
        o.append(path(f"M255,{y+15} H273",stroke=MUTED,sw=1.4)); o.append(path(f"M267,{y+10} L274,{y+15} L267,{y+20}",stroke=MUTED,sw=1.4))
        o.append(text(280,y+20,f"bucket {b}",11,PURPLE,"bold"))
        y+=46
    entries={7:"(100001, 101)  (100004, 105)",6:"(100002, 104)",0:"(100003, 108)"}
    by=44
    o.append(text(380,by,"8 buckets",11,INK,"bold"))
    for i in range(8):
        yy=by+8+i*26
        fill = "#e2f3ee" if i in entries else "#fff"
        o.append(rect(380,yy,310,23,fill=fill,stroke=RULE,rx=3))
        o.append(text(388,yy+16,f"bucket {i}",10.5,MUTED,family=MONO))
        if i in entries: o.append(text(460,yy+16,entries[i],10.5,INK,"bold",family=MONO))
        else: o.append(text(460,yy+16,"empty",10.5,MUTED))
    o.append(text(380,by+8+8*26+17,"Bucket 7 holds two keys: a collision, and normal.",10.5,GREEN,"bold"))
    ny=by+8+8*26+46
    o.append(text(20,ny,"To find a key: hash it, take the remainder, look in one bucket. The same steps whether the dictionary",10.5,MUTED))
    o.append(text(20,ny+16,"holds ten keys or ten million.",10.5,MUTED))
    return svg(W,ny+28,"".join(o))

def fig_traversal():
    o=[text(20,26,"One tree, two walks: depth-first uses a stack, breadth-first a queue",13,INK,"bold",family=HEAD)]
    BW,BH=116,28
    nodes={"Arvind Kapoor":(300,52),"Anita Rao":(150,112),"Harpreet Sethi":(470,112),
           "Vikram Singh":(72,172),"Farah Khan":(228,172),"Ramesh Patil":(470,172),
           "Neha Kulkarni":(8,232),"Rahul Mehta":(136,232),"Ajay Kumar":(470,232),"Gopal Sahu":(470,292)}
    edges=[("Arvind Kapoor","Anita Rao"),("Arvind Kapoor","Harpreet Sethi"),("Anita Rao","Vikram Singh"),
           ("Anita Rao","Farah Khan"),("Harpreet Sethi","Ramesh Patil"),("Vikram Singh","Neha Kulkarni"),
           ("Vikram Singh","Rahul Mehta"),("Ramesh Patil","Ajay Kumar"),("Ajay Kumar","Gopal Sahu")]
    for a,b in edges:
        x1,y1=nodes[a]; x2,y2=nodes[b]
        o.append(path(f"M{x1+BW/2},{y1+BH} C{x1+BW/2},{y1+BH+18} {x2+BW/2},{y2-18} {x2+BW/2},{y2}",stroke=RULE,sw=1.5))
    dfs=["Arvind Kapoor","Anita Rao","Vikram Singh","Neha Kulkarni","Rahul Mehta","Farah Khan","Harpreet Sethi","Ramesh Patil","Ajay Kumar","Gopal Sahu"]
    bfs=["Arvind Kapoor","Anita Rao","Harpreet Sethi","Vikram Singh","Farah Khan","Ramesh Patil","Neha Kulkarni","Rahul Mehta","Ajay Kumar","Gopal Sahu"]
    for name,(x,y) in nodes.items():
        o.append(rect(x,y,BW,BH,fill="#fff",stroke=ACC,sw=1.4,rx=5))
        o.append(text(x+BW/2,y+19,name,10.5,INK,"bold",anchor="middle"))
        o.append(rect(x-4,y-11,28,16,fill=PURPLE,rx=4)); o.append(text(x+10,y+1,f"D{dfs.index(name)+1}",10.5,"#fff","bold",anchor="middle"))
        o.append(rect(x+BW-24,y-11,28,16,fill=GREEN,rx=4)); o.append(text(x+BW-10,y+1,f"B{bfs.index(name)+1}",10.5,"#fff","bold",anchor="middle"))
    ky=346
    o.append(rect(8,ky,334,58,fill="#efe7f6",stroke=PURPLE,rx=6))
    o.append(text(18,ky+19,"D1 to D10: depth-first (a stack)",11,PURPLE,"bold"))
    o.append(text(18,ky+36,"down one branch, then back up: the order",10.5,INK))
    o.append(text(18,ky+51,"the indented org chart prints in",10.5,INK))
    o.append(rect(356,ky,334,58,fill="#e2f3ee",stroke=GREEN,rx=6))
    o.append(text(366,ky+19,"B1 to B10: breadth-first (a queue)",11,GREEN,"bold"))
    o.append(text(366,ky+36,"level by level: answers “who is two",10.5,INK))
    o.append(text(366,ky+51,"levels below the MD?” and shortest paths",10.5,INK))
    return svg(W,ky+70,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig33-1-growth-curves.svg",fig_growth),("fig33-2-hash-table.svg",fig_hash),
                    ("fig33-3-traversals.svg",fig_traversal)]:
        open(name,"w",encoding="utf-8").write(fn())
    print("ok33")
