# Generates the SVG figures for Chapter 49. Run: python3 make_figs49.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Both figures use a 760 px canvas, so 11 px text prints at 11 x 493.2 / 760 = 7.1 pt (the minimum is 7 pt).
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=760
FIELDS=["machine_id","plant","line_type","reading_ts","temperature_c","pressure_bar","units_made","scrap_flag"]
SHORT=["id","plant","line","ts","temp","pres","units","scrap"]

def cross(x,y,c=RED):
    """A small cross in a circle: 'reads everything' (shape as well as colour)."""
    return (f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{c}" stroke-width="1.8"/>'
            + path(f"M{x-4},{y-4} L{x+4},{y+4} M{x+4},{y-4} L{x-4},{y+4}",stroke=c,sw=1.8))

def tick(x,y,c=GREEN):
    """A small tick in a circle: 'reads one stripe'."""
    return (f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{c}" stroke-width="1.8"/>'
            + path(f"M{x-4},{y} L{x-1},{y+3.5} L{x+4.5},{y-4}",stroke=c,sw=1.8))

def fig_row_vs_col():
    o=[]
    o.append(text(24,28,"Row oriented (CSV, an operational database)",15,INK,"bold",family=HEAD))
    y=44
    for r in range(4):
        x=24
        for f,s in zip(FIELDS,SHORT):
            hot=f=="temperature_c"; w=60
            o.append(rect(x,y,w,26,fill="#fbeaea" if hot else "#eef2f6",stroke=RED if hot else RULE,sw=1.2 if hot else 0.8,rx=3))
            o.append(text(x+w/2,y+17.5,s,12,INK if hot else MUTED,"bold" if hot else "normal",anchor="middle"))
            x+=w+3
        o.append(text(x+8,y+17.5,f"reading {r+1}",12,MUTED,style="italic"))
        y+=30
    o.append(text(24,y+10,"… 216,000 readings, each one's 8 fields stored side by side",12,MUTED,style="italic"))
    o.append(text(24,y+30,"Key: id = machine_id · ts = reading_ts · temp = temperature_c · pres = pressure_bar",11.5,MUTED))
    o.append(cross(33,y+56)); o.append(text(48,y+61,"Average temperature: reads every box, all 8 fields of every reading.",13,RED,"bold"))
    top=y+92
    o.append(text(24,top,"Columnar (Parquet, every analytics warehouse)",15,INK,"bold",family=HEAD))
    y2=top+16
    for f in FIELDS:
        hot=f=="temperature_c"
        o.append(rect(24,y2,190,24,fill="#fbeaea" if hot else "#f2f4f7",stroke=RED if hot else RULE,sw=1.4 if hot else 0.8,rx=4))
        o.append(text(36,y2+16.5,f,12.5,INK if hot else MUTED,"bold" if hot else "normal",family=MONO))
        o.append(text(224,y2+16.5,("the only stripe read" if hot else "216,000 values, stored together"),12,RED if hot else MUTED,"bold" if hot else "normal"))
        y2+=28
    bx=470; by=top+16
    o.append(rect(bx,by,266,150,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(bx+14,by+26,"The same 216,000 readings",14,INK,"bold",family=HEAD))
    for k,(name,size) in enumerate([("CSV","14.6 MB"),("SQLite table","16.3 MB"),("Parquet","1.3 MB")]):
        o.append(text(bx+14,by+54+k*23,name,13,INK)); o.append(text(bx+200,by+54+k*23,size,13,INK,anchor="end"))
    o.append(wrap(bx+14,by+122,["Values of one kind sit together, so","Parquet is about 11 times smaller."],12,GREEN,18,"bold"))
    o.append(tick(33,y2+18)); o.append(text(48,y2+23,"Average temperature: reads one stripe; the other seven are never touched.",13,GREEN,"bold"))
    return svg(W,y2+40,"".join(o))

def fig_log():
    o=[]
    o.append(text(24,28,"The folder: ordinary Parquet",15,INK,"bold",family=HEAD))
    o.append(text(300,28,"The log: what each version contains",15,INK,"bold",family=HEAD))
    vers=[("version 0",ACC,["metaData: 8 columns","add part-0000"],"first write: the whole day"),
          ("version 1",ORANGE,["remove part-0000","add part-0001"],"M-07 corrected, one atomic commit"),
          ("version 2",PURPLE,["remove part-0001","add part-0000"],"restore: back to version 0's file"),
          ("version 3",GREEN,["metaData: 9 columns","add part-0002"],"append with a new column, shift")]
    files={"part-0000":("1.25 MB","216,000 readings"),"part-0001":("1.25 MB","216,000, M-07 corrected"),
           "part-0002":("0.11 MB","8,640 readings of M-01")}
    fy={}
    vy=44; h=92
    for i,(name,c,lines,note) in enumerate(vers):
        o.append(rect(300,vy,436,h,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(300,vy,6,h,fill=c,rx=3))
        o.append(text(318,vy+22,name,13.5,c,"bold"))
        o.append(text(410,vy+22,f"_delta_log/…0{i}.json",12,MUTED,family=MONO))
        yy=vy+44
        for l in lines:
            o.append(text(318,yy,l,12.5,INK,family=MONO)); yy+=19
        o.append(text(318,yy+2,note,12,MUTED,style="italic"))
        added=lines[-1].split()[-1]
        if added not in fy:                     # draw each file once, level with the version that first adds it
            fy[added]=vy+h/2
            size,what=files[added]
            o.append(rect(24,vy+18,228,56,fill="#fff",stroke=RULE,sw=1.2,rx=6))
            o.append(text(38,vy+40,added+".parquet",12.5,INK,family=MONO))
            o.append(text(38,vy+60,f"{size} · {what}",11.5,MUTED))
        ty=fy[added]
        o.append(arrow(296,vy+h/2,256,ty if ty==vy+h/2 else ty+14,c=c,sw=1.5))
        vy+=h+12
    o.append(text(24,vy+4,"Each arrow points at the file a version adds. File names are shortened.",11.5,MUTED,style="italic"))
    o.append(rect(24,vy+16,712,62,fill="#fff4d6",stroke="#e2c46b",rx=7))
    o.append(wrap(38,vy+40,["Readers follow the log, not the folder, so a commit becomes visible all at once.",
                            "Time travel reads an older version's list. Vacuum deletes files no kept version needs."],12.5,INK,21,"bold"))
    return svg(W,vy+92,"".join(o))

if __name__=="__main__":
    for n,f in [("fig49-1-row-vs-columnar.svg",fig_row_vs_col),("fig49-2-transaction-log.svg",fig_log)]:
        open(n,"w").write(f())
    print("ok")
