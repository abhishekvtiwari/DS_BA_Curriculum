# Diagram for Chapter 65 (Figure 65.3, tagging and showback). Run: python3 make_figs65.py
# The shares are computed from companion/ch65/monthly_cost_model.csv, the same groupby as section 65.4.
# Canvas 760 px prints at 493.2 pt, so 11 px text prints at 7.1 pt; nothing below is smaller than 11.5 px.
import pathlib
import pandas as pd
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; GOLD="#b7791f"; SOFT="#eef2f7"; GREY="#6b7280"
D = pathlib.Path(__file__).resolve().parent.parent / "companion" / "ch65"

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    return path(f"M{x1},{y1} L{x2-6},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{x2-8},{y2-4.5} L{x2-8},{y2+4.5} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines):
    o=[rect(x+3,y+3,w,h,fill=SOFT,rx=7), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=7)]
    o.append(f'<path d="M{x},{y+7} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+17,title,12.5,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+42+i*16,l,12,INK,anchor="middle"))
    return "".join(o)

def f1():
    costs = pd.read_csv(D / "monthly_cost_model.csv")
    total = costs.monthly_inr.sum()
    share = (costs.groupby("owner").monthly_inr.sum() / total * 100).round(1)
    o=[text(20,26,"Tagging and showback: one bill, split honestly by owner",15,INK,"bold",family=HEAD)]
    o.append(box(20,44,220,78,"1. Tag at creation",ACC,["owner, container, environment","(Chapter 63's ownership)"]))
    o.append(box(270,44,220,78,"2. One bill, grouped",GOLD,["one AWS invoice, split","by tag automatically"]))
    o.append(box(520,44,220,78,"3. Showback, per owner",GREEN,[f"₹{total:,.0f} a month,","shared out below"]))
    o.append(arrow(243,83,267,83)); o.append(arrow(493,83,517,83))
    rows=[("data platform","Data platform team","warehouse compute, storage, backups; orchestration",ACC),
          ("AI applications","AI applications","defect-model serving; PO-intake and RAG LLM calls",PURPLE),
          ("shared","Shared","data transfer out: dashboards, API replies, emails",GOLD),
          ("plant operations","Plant operations","sensor archive, hot and cold tiers",GREEN)]
    y=144
    for key,name,scope,c in rows:
        o.append(rect(20,y,720,36,fill="#fff",stroke=RULE,rx=6)); o.append(rect(20,y,6,36,fill=c))
        o.append(text(36,y+23,name,12.5,INK,"bold"))
        o.append(text(190,y+23,scope,12,MUTED))
        o.append(text(728,y+23,f"{share[key]:.1f}%",13,INK,"bold",anchor="end"))
        y+=42
    o.append(text(20,y+14,"Showback shows each owner its real cost without charging it; a genuinely shared cost stays \"shared\".",12,MUTED))
    return svg(760,y+26,"".join(o))

if __name__ == "__main__":
    open("fig65-3-tagging-showback.svg","w").write(f1())
    print("ok")
