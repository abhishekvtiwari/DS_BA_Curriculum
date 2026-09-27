# Diagram for Chapter 65. Run: python3 make_figs65.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.2):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=7), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=7)]
    o.append(f'<path d="M{x},{y+8} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+16.5,title,10,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+40+i*14,l,size-1.2,INK,anchor="middle"))
    return "".join(o)

def f1():  # tagging and showback flow
    o=[text(30,30,"Tagging and showback: one bill, split honestly by owner",14.5,INK,"bold",family=HEAD)]
    o.append(box(30,64,220,90,"Every resource\ntagged at creation",ACC,["owner, container, environment","(Ch 63's ownership model)"],9.8))
    o.append(box(300,64,220,90,"Monthly bill,\ntagged & grouped",GOLD,["one AWS invoice,","split by tag automatically"],9.8))
    o.append(box(570,64,220,90,"Showback report,\nper team",GREEN,["\"your containers cost","Rs X this month\""],9.8))
    o.append(arrow(255,109,296,109)); o.append(arrow(525,109,566,109))
    rows=[("Data platform team","Warehouse, orchestration",f"~66%",ACC),
         ("AI applications team","Defect model, RAG, PO-intake LLM calls",f"~11%",PURPLE),
         ("Shared / platform overhead","Backups, transfer, monitoring",f"~23%",GOLD)]
    y=195
    for name,scope,share,c in rows:
        o.append(rect(30,y,760,44,fill="#fff",stroke=RULE,rx=6)); o.append(rect(30,y,6,44,fill=c))
        o.append(text(48,y+27,name,10.6,INK,"bold"))
        o.append(text(300,y+27,scope,10,MUTED))
        o.append(text(730,y+27,share,11,c,"bold",anchor="end"))
        y+=52
    o.append(text(30,y+18,"Showback shows a team its real cost without automatically charging it back — the first step, before any budget or chargeback policy exists.",11.2,MUTED))
    return svg(820,y+40,"".join(o))

if __name__ == "__main__":
    open("fig65-3-tagging-showback.svg","w").write(f1())
    print("ok")
