# Generates the SVG figures for Chapter 48. Run: python3 make_figs48.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

# Figures print at the full text width, 174 mm = 493.2 pt. On a 760 px canvas a font of s px prints at
# s x 493.2 / 760 pt, so every text here is at least 11 px (7.1 pt).
W_CANVAS=760

def fig_shuffle():
    o=[]
    o.append(rect(250,14,260,56,fill=INK,rx=8))
    o.append(text(380,38,"Driver",16,"#fff","bold",anchor="middle",family=HEAD))
    o.append(text(380,58,"your code, the plan, small results",12,"#c9d4e0",anchor="middle"))
    o.append(arrow(380,114,380,74,c=ORANGE,sw=2))
    o.append(wrap(392,90,["collect() brings every row back","into the driver's memory"],12,ORANGE,16,"bold"))
    W=168; G=14; x0=20; ytop=122
    xs=[x0+i*(W+G) for i in range(4)]
    for i,x in enumerate(xs):
        o.append(rect(x,ytop,W,232,fill="#fbfcfe",stroke=RULE,sw=1.3,rx=8))
        o.append(text(x+12,ytop+22,f"Worker {i+1}",13,INK,"bold"))
        for k in range(2):
            o.append(rect(x+10,ytop+32+k*34,W-20,28,fill="#e6edf4",stroke=ACC,sw=1,rx=5))
            o.append(text(x+20,ytop+51+k*34,f"partition {i*2+k+1}",12,INK))
        # narrow stage: solid border
        o.append(rect(x+10,ytop+104,W-20,62,fill="#eaf5f1",stroke=GREEN,sw=1.6,rx=5))
        o.append(text(x+20,ytop+123,"NARROW",12,GREEN,"bold"))
        o.append(text(x+20,ytop+141,"filter, select,",12,INK))
        o.append(text(x+20,ytop+158,"partial totals",12,INK))
        # wide stage: dashed border
        o.append(rect(x+10,ytop+176,W-20,48,fill="#fbeaea",stroke=RED,sw=1.6,rx=5,extra='stroke-dasharray="6 4"'))
        o.append(text(x+20,ytop+195,"WIDE",12,RED,"bold"))
        o.append(text(x+20,ytop+213,"shuffle: rows move",12,INK))
    # shuffle arrows run below the workers, from one worker's bottom edge to another's
    yb=ytop+232
    cx=[x+W/2 for x in xs]
    arcs=[(cx[i]+40,cx[i+1]-40,20) for i in range(3)] + [(cx[i+1]-10,cx[i]+10,38) for i in range(3)]
    for x1,x2,depth in arcs:
        o.append(path(f"M{x1},{yb} C{x1},{yb+depth} {x2},{yb+depth} {x2},{yb+10}",stroke=RED,sw=1.4))
        o.append(arrow(x2,yb+10,x2,yb+1,c=RED,sw=1.4))
    y=yb+64
    o.append(text(20,y,"NARROW (solid boxes): each worker uses only its own partitions. Cheap, fully parallel.",12.5,INK,"bold"))
    o.append(text(20,y+21,"WIDE (dashed boxes, arrows underneath): rows for the same key must meet, so they cross",12.5,INK,"bold"))
    o.append(text(20,y+40,"between workers, through shuffle files and, on a cluster, the network. This is the cost.",12.5,INK,"bold"))
    return svg(W_CANVAS,y+54,"".join(o))

GROUP_PLAN=["AdaptiveSparkPlan isFinalPlan=false",
    "+- HashAggregate(keys=[machine_id], functions=[sum(units_made)])",
    "   +- Exchange hashpartitioning(machine_id, 8), ENSURE_REQUIREMENTS",
    "      +- HashAggregate(keys=[machine_id], functions=[partial_sum(units_made)])",
    "         +- Project [machine_id, units_made]",
    "            +- FileScan parquet [machine_id,units_made,reading_date] Batched: true",
    "        PartitionFilters: []",
    "        PushedFilters: []",
    "        ReadSchema: struct<machine_id:string,units_made:int>"]
PRUNE_PLAN=["*(1) Project [machine_id, temperature_c]",
    "+- *(1) Filter (isnotnull(plant) AND (plant = Bhiwandi Main))",
    "   +- *(1) ColumnarToRow",
    "      +- FileScan parquet [machine_id,plant,temperature_c,reading_date] Batched: true",
    "        PartitionFilters: [isnotnull(reading_date), (reading_date = 2025-12-01)]",
    "        PushedFilters: [IsNotNull(plant), EqualTo(plant,Bhiwandi Main)]",
    "        ReadSchema: struct<machine_id:string,plant:string,temperature_c:double>"]

def plan_panel(y,title,c,lines,notes):
    """A plan printed in full; notes = {line index: margin label}; noted lines are highlighted."""
    h=34+len(lines)*19+16
    out=[header_card(12,y,736,h,c,title,tsize=14)]
    yy=y+56
    for i,l in enumerate(lines):
        if i in notes:
            out.append(rect(18,yy-14,724,19,fill="#fff4d6",stroke="#e2c46b",rx=3))
            out.append(text(738,yy,"\u2190 "+notes[i],11.5,c,"bold",anchor="end"))
        out.append(f'<text x="24" y="{yy}" font-size="11" font-family="{MONO}" fill="{INK}" xml:space="preserve">{esc(l).replace(" ", chr(160))}</text>')
        yy+=19
    return "".join(out), y+h

def fig_plan():
    o=[]
    a,y=plan_panel(10,"Group by machine: one Exchange, one shuffle",RED,GROUP_PLAN,{2:"the shuffle"})
    o.append(a)
    b,y=plan_panel(y+16,"One day at one plant: no Exchange, and pruning",GREEN,PRUNE_PLAN,
                   {4:"1 folder of 92",6:"3 columns read"})
    o.append(b)
    o.append(text(12,y+26,"Read a plan from the bottom up. Count the Exchange lines: each one is a shuffle, the cost.",12.5,INK,"bold"))
    o.append(text(12,y+46,"Then check the scan: PartitionFilters skips whole folders; ReadSchema lists the only columns read.",12.5,INK))
    return svg(W_CANVAS,y+58,"".join(o))

if __name__=="__main__":
    for n,f in [("fig48-1-driver-workers-shuffle.svg",fig_shuffle),("fig48-2-reading-the-plan.svg",fig_plan)]:
        open(n if n.startswith("fig") else n,"w").write(f())
    print("ok")
