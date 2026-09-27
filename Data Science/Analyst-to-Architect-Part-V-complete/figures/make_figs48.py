# Generates the SVG figures for Chapter 48. Run: python3 make_figs48.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_shuffle():
    o=[]
    o.append(rect(380,20,290,60,fill=INK,rx=8))
    o.append(text(525,44,"Driver",15,"#fff","bold",anchor="middle",family=HEAD))
    o.append(text(525,66,"your code, the plan, the results you collect",11,"#c9d4e0",anchor="middle"))
    W=210; G=26; ytop=140
    for i in range(4):
        x=40+i*(W+G)
        o.append(rect(x,ytop,W,300,fill="#fbfcfe",stroke=RULE,sw=1.3,rx=8))
        o.append(text(x+14,ytop+24,f"Worker {i+1}",13,INK,"bold"))
        for k in range(2):
            o.append(rect(x+14,ytop+40+k*40,W-28,32,fill="#e6edf4",stroke=ACC,sw=1,rx=5))
            o.append(text(x+24,ytop+61+k*40,f"partition {i*2+k+1}",11.5,INK))
        o.append(path(f"M{x+14},{ytop+130} H{x+W-14}",stroke=RULE,sw=1,dash="4 3"))
        o.append(text(x+14,ytop+152,"filter, select,",11.5,GREEN))
        o.append(text(x+14,ytop+170,"partial totals",11.5,GREEN))
        o.append(rect(x+14,ytop+196,W-28,40,fill="#eaf5f1",stroke=GREEN,sw=1,rx=5))
        o.append(text(x+24,ytop+221,"no communication",11.5,GREEN,"bold"))
        o.append(rect(x+14,ytop+248,W-28,40,fill="#fbeaea",stroke=RED,sw=1,rx=5))
        o.append(text(x+24,ytop+273,"shuffle: rows move",11.5,RED,"bold"))
    for i in range(4):
        for j in range(4):
            if i!=j and (i+j)%2==0:
                o.append(path(f"M{40+i*(W+G)+W/2},{ytop+268} C{40+i*(W+G)+W/2},{ytop+320} {40+j*(W+G)+W/2},{ytop+320} {40+j*(W+G)+W/2},{ytop+268}",stroke=RED,sw=1.3))
    o.append(text(40,ytop+335,"NARROW: each worker uses only its own partitions. Cheap, fully parallel.",12.5,GREEN,"bold"))
    o.append(text(40,ytop+358,"WIDE: rows for the same key must meet, so they cross the network. This is the cost.",12.5,RED,"bold"))
    o.append(arrow(525,ytop-8,525,84,c=MUTED,sw=2))
    o.append(wrap(700,104,["collect() brings every row","back into the driver's memory"],12,ORANGE,18,"bold"))
    return svg(1040,ytop+390,"".join(o))

def fig_plan():
    o=[]
    left=["AdaptiveSparkPlan isFinalPlan=false","+- HashAggregate(keys=[machine_id], sum(units_made))",
          "   +- Exchange hashpartitioning(machine_id, 8)","      +- HashAggregate(partial_sum(units_made))",
          "         +- Project [machine_id, units_made]","            +- FileScan parquet [machine_id, units_made]"]
    right=["*(1) Project [machine_id, temperature_c]","+- *(1) Filter (plant = Bhiwandi Main)","   +- *(1) ColumnarToRow",
           "      +- FileScan parquet","             PartitionFilters: [reading_date = 2025-12-01]",
           "             PushedFilters: [EqualTo(plant, Bhiwandi Main)]","             ReadSchema: machine_id, plant, temperature_c"]
    def panel(x,title,c,lines,hl,note1,note2):
        out=[header_card(x,30,470,250,c,title)]
        y=92
        for i,l in enumerate(lines):
            if i in hl:
                out.append(rect(x+10,y-15,450,24,fill="#fff4d6",stroke="#e2c46b",rx=4))
            out.append(f'<text x="{x+18}" y="{y}" font-size="11.5" font-family="{MONO}" fill="{INK}" xml:space="preserve">{l.replace(" ", chr(160))}</text>')
            y+=25
        out.append(text(x+18,268,note1,12,c,"bold"))
        return "".join(out)
    o.append(panel(30,"Group by machine: one shuffle",RED,left,{2},"Exchange = the shuffle: rows for a machine move together",""))
    o.append(panel(540,"One day, two columns: no shuffle",GREEN,right,{4,5,6},"PartitionFilters and ReadSchema = work never done",""))
    o.append(rect(30,300,980,64,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,326,"Read a plan from the bottom up. Count the exchanges: each one writes data to disk, sends it, and reads it back.",12.5,INK,"bold"))
    o.append(text(46,348,"Then look at the scan: PartitionFilters skip whole folders, ReadSchema shows which columns are read at all.",12,MUTED))
    return svg(1040,384,"".join(o))

if __name__=="__main__":
    for n,f in [("fig48-1-driver-workers-shuffle.svg",fig_shuffle),("fig48-2-reading-the-plan.svg",fig_plan)]:
        open(n if n.startswith("fig") else n,"w").write(f())
    print("ok")
