# Generates the SVG figures for Chapter 33. Run: python3 make_figs33.py
# The growth curve uses the measured naive-matching times from checks/ch33_timings_log.txt.
from make_figs import *
import math
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_growth():
    o=[text(30,32,"How the work grows: the same five shapes, drawn to scale",14,INK,"bold",family=HEAD)]
    x0,x1,y0,y1=90,700,330,70
    def px(n): return x0+(n/100)*(x1-x0)
    def py(v): return y0-min(v,100)/100*(y0-y1)
    o.append(path(f"M{x0},{y0} H{x1}",stroke=MUTED,sw=1.4)); o.append(path(f"M{x0},{y0} V{y1-10}",stroke=MUTED,sw=1.4))
    o.append(text(395,y0+40,"input size n",12,INK,anchor="middle")); o.append(text(40,y1+130,"work",12,INK,anchor="middle"))
    curves=[("O(1) constant",lambda n: 2,GREEN),("O(log n) logarithmic",lambda n: 8*math.log2(n+1),ACC),
            ("O(n) linear",lambda n: n,PURPLE),("O(n log n)",lambda n: n*math.log2(n+1)/6.6,ORANGE),
            ("O(n²) quadratic",lambda n: n*n/100,RED)]
    label_at={"O(1) constant":(72,-10),"O(log n) logarithmic":(20,-12),"O(n) linear":(62,14),
              "O(n log n)":(56,24),"O(n²) quadratic":(82,16)}
    for label,fn,c in curves:
        pts=[(px(n),py(fn(n))) for n in range(1,101) if fn(n)<=105]
        o.append(path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=c,sw=2.4))
        n,dy=label_at[label]
        o.append(text(px(n),py(fn(n))+dy,label,11.5,c,"bold"))
    o.append(rect(760,70,250,270,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(776,96,"Measured: naive matching",12.5,INK,"bold"))
    for i,l in enumerate(["  250 invoices:  0.96 s","  500 invoices:  1.84 s"," 1000 invoices:  3.73 s"," 2000 invoices:  7.51 s","","20,000 (predicted): ~75 s","","With a dictionary index:","  build  0.045 s","  match  0.009 s"]):
        col = GREEN if "dictionary" in l or "0.0" in l else INK
        o.append(text(776,120+i*21,l,11.5,col,family=(MONO if ":" in l else None)))
    o.append(text(30,y0+70,"Doubling the input doubles a linear algorithm's work and quadruples a quadratic one. The curves are drawn; the numbers on the right were measured.",12,MUTED))
    return svg(1040,y0+90,"".join(o))

def fig_hash():
    o=[text(30,32,"Why a dictionary lookup does not get slower as it grows",14,INK,"bold",family=HEAD)]
    keys=[("(100001, 101)","3"),("(100002, 104)","6"),("(100003, 108)","3")]
    y=80
    for k,b in keys:
        o.append(rect(40,y,200,40,fill="#fff",stroke=ACC,sw=1.6,rx=6)); o.append(text(140,y+25,k,12,INK,"bold",anchor="middle",family=MONO))
        o.append(path(f"M240,{y+20} H300",stroke=MUTED,sw=1.5)); o.append(path(f"M292,{y+14} L302,{y+20} L292,{y+26}",stroke=MUTED,sw=1.5))
        o.append(rect(305,y,180,40,fill="#f6f9fc",stroke=RULE,rx=6)); o.append(text(395,y+25,"hash() % 8",12,MUTED,anchor="middle",family=MONO))
        o.append(path(f"M485,{y+20} H545",stroke=MUTED,sw=1.5)); o.append(path(f"M537,{y+14} L547,{y+20} L537,{y+26}",stroke=MUTED,sw=1.5))
        o.append(text(565,y+25,f"bucket {b}",12,PURPLE,"bold"))
        y+=60
    for i in range(8):
        yy=70+i*30
        fill = "#e2f3ee" if i in (3,6) else "#fff"
        o.append(rect(700,yy,180,26,fill=fill,stroke=RULE,rx=4))
        o.append(text(712,yy+18,f"bucket {i}",11.5,MUTED,family=MONO))
        if i==3: o.append(text(790,yy+18,"2 entries (a collision)",11,GREEN)); 
        if i==6: o.append(text(790,yy+18,"1 entry",11,GREEN))
    o.append(text(30,y+20,"To find a key, Python hashes it, takes the remainder, and looks in one bucket: the same two steps whether the dictionary holds ten keys or ten million.",12,MUTED))
    o.append(text(30,y+42,"Collisions (two keys in one bucket) are normal and cheap. Keys must be immutable, because a key that changed would hash to a different bucket.",12,MUTED))
    return svg(1040,y+62,"".join(o))

def fig_traversal():
    o=[text(30,32,"Same tree, two walks: depth-first uses a stack, breadth-first a queue",14,INK,"bold",family=HEAD)]
    nodes={"Arvind Kapoor":(430,70),"Anita Rao":(230,150),"Harpreet Sethi":(640,150),
           "Vikram Singh":(120,230),"Farah Khan":(330,230),"Ramesh Patil":(640,230),
           "Neha Kulkarni":(40,310),"Rahul Mehta":(210,310),"Ajay Kumar":(640,310)}
    edges=[("Arvind Kapoor","Anita Rao"),("Arvind Kapoor","Harpreet Sethi"),("Anita Rao","Vikram Singh"),
           ("Anita Rao","Farah Khan"),("Harpreet Sethi","Ramesh Patil"),("Vikram Singh","Neha Kulkarni"),
           ("Vikram Singh","Rahul Mehta"),("Ramesh Patil","Ajay Kumar")]
    for a,b in edges:
        x1,y1=nodes[a]; x2,y2=nodes[b]
        o.append(path(f"M{x1+70},{y1+34} C{x1+70},{y1+60} {x2+70},{y2-26} {x2+70},{y2}",stroke=RULE,sw=1.5))
    dfs=["Arvind Kapoor","Anita Rao","Vikram Singh","Neha Kulkarni","Rahul Mehta","Farah Khan","Harpreet Sethi","Ramesh Patil","Ajay Kumar"]
    bfs=["Arvind Kapoor","Anita Rao","Harpreet Sethi","Vikram Singh","Farah Khan","Ramesh Patil","Neha Kulkarni","Rahul Mehta","Ajay Kumar"]
    for name,(x,y) in nodes.items():
        o.append(rect(x,y,140,34,fill="#fff",stroke=ACC,sw=1.6,rx=6))
        o.append(text(x+70,y+22,name,11.5,INK,"bold",anchor="middle"))
        o.append(rect(x-2,y-10,20,18,fill=PURPLE,rx=4)); o.append(text(x+8,y+4,str(dfs.index(name)+1),10.5,"#fff","bold",anchor="middle"))
        o.append(rect(x+122,y-10,20,18,fill=GREEN,rx=4)); o.append(text(x+132,y+4,str(bfs.index(name)+1),10.5,"#fff","bold",anchor="middle"))
    o.append(rect(40,370,470,66,fill="#efe7f6",stroke=PURPLE,rx=7))
    o.append(text(58,392,"depth-first (purple): down one branch, then back up",12,PURPLE,"bold"))
    o.append(text(58,414," ".join(str(i+1) for i in range(9))+"   \u2190 the order the org chart prints in",11.5,INK,family=MONO))
    o.append(rect(540,370,470,66,fill="#e2f3ee",stroke=GREEN,rx=7))
    o.append(text(558,392,"breadth-first (green): level by level",12,GREEN,"bold"))
    o.append(text(558,414,"answers \u201cwho is two levels below the MD?\u201d and shortest paths",11.5,INK))
    return svg(1040,455,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig33-1-growth-curves.svg",fig_growth),("fig33-2-hash-table.svg",fig_hash),
                    ("fig33-3-traversals.svg",fig_traversal)]:
        open(name,"w").write(fn())
    print("ok33")
