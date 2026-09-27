# Generates the SVG figures for Chapter 49. Run: python3 make_figs49.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
FIELDS=["machine_id","plant","line_type","reading_ts","temperature_c","pressure_bar","units_made","scrap_flag"]

def fig_row_vs_col():
    o=[]
    o.append(text(30,34,"Row oriented (CSV, operational database)",14.5,INK,"bold",family=HEAD))
    y=56
    for r in range(4):
        x=30
        for f in FIELDS:
            w=54 if f!="temperature_c" else 62
            fill="#fbeaea" if f=="temperature_c" else "#eef2f6"
            o.append(rect(x,y,w,30,fill=fill,stroke=RULE,sw=0.8,rx=3))
            o.append(text(x+5,y+20,f[:6],9.5,INK if f=="temperature_c" else MUTED))
            x+=w+2
        o.append(text(x+10,y+20,f"reading {r+1}",11,MUTED,style="italic"))
        y+=34
    o.append(text(30,y+22,"A query for average temperature must read every box: all 8 fields of all 216,000 rows.",12.5,RED,"bold"))
    top=y+50
    o.append(text(30,top+22,"Columnar (Parquet, every analytics warehouse)",14.5,INK,"bold",family=HEAD))
    y2=top+44
    for i,f in enumerate(FIELDS):
        hot = f=="temperature_c"
        o.append(rect(30,y2,300,26,fill="#fbeaea" if hot else "#f2f4f7",stroke=RED if hot else RULE,sw=1.2 if hot else 0.8,rx=4))
        o.append(text(42,y2+18,f,11.5,INK if hot else MUTED,"bold" if hot else None))
        o.append(text(340,y2+18,"216,000 values of the same kind, stored together",11.5,MUTED if not hot else RED))
        y2+=30
    o.append(rect(700,top+44,310,150,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(716,top+70,"Same 216,000 readings",13.5,INK,"bold",family=HEAD))
    o.append(wrap(716,top+96,["CSV            14.6 MB","SQLite table   16.3 MB","Parquet         1.3 MB"],12.5,INK,22,family=MONO))
    o.append(text(716,top+178,"11x smaller, and one column to read",11.5,GREEN,"bold"))
    o.append(text(30,y2+24,"The same query reads one stripe. The other seven are never touched.",12.5,GREEN,"bold"))
    return svg(1040,y2+50,"".join(o))

def fig_log():
    o=[]
    o.append(text(30,34,"The folder: ordinary Parquet files",14,INK,"bold",family=HEAD))
    files=[("part-0000.parquet","1.25 MB"),("part-0001.parquet","0.42 MB"),("part-0002.parquet","1.25 MB"),("part-0003.parquet","0.31 MB")]
    y=56
    for n,s in files:
        o.append(rect(30,y,260,42,fill="#fff",stroke=RULE,sw=1.2,rx=6))
        o.append(f'<text x="44" y="{y+26}" font-size="11.5" font-family="{MONO}" fill="{INK}">{n}</text>')
        o.append(text(240,y+26,s,11,MUTED)); y+=52
    o.append(text(30,y+14,"No file is special. Nothing here says",12,MUTED))
    o.append(text(30,y+32,"which files make up the table today.",12,MUTED))
    o.append(text(370,34,"The log: which files each version contains",14,INK,"bold",family=HEAD))
    vers=[("version 0",ACC,["metaData: 8 columns","add part-0000","add part-0001"],"first write"),
          ("version 1",ORANGE,["remove part-0001","add part-0002"],"M-07 corrected, one atomic commit"),
          ("version 2",GREEN,["add part-0003"],"an append")]
    vy=56
    for name,c,lines,note in vers:
        h=32+len(lines)*20+34
        o.append(rect(370,vy,420,h,fill="#fbfcfe",stroke=c,sw=1.5,rx=7)); o.append(rect(370,vy,6,h,fill=c,rx=3))
        o.append(text(388,vy+24,name,13,c,"bold"))
        yy=vy+44
        for l in lines:
            o.append(f'<text x="388" y="{yy}" font-size="11.5" font-family="{MONO}" fill="{INK}">{l}</text>'); yy+=20
        o.append(text(388,yy+12,note,11.5,MUTED,style="italic"))
        o.append(arrow(366,vy+h/2,296,vy+h/2,c=c,sw=1.4))
        vy+=h+16
    o.append(rect(820,56,190,150,fill="#fff4d6",stroke="#e2c46b",rx=7))
    o.append(wrap(834,82,["Readers follow the log,","not the folder.","","A commit becomes","visible all at once:","that is atomicity."],12,INK,20))
    o.append(rect(30,vy+4,980,52,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,vy+34,"Time travel is reading an older version's file list. Vacuum deletes files no kept version needs.",12.5,INK,"bold"))
    return svg(1040,vy+72,"".join(o))

if __name__=="__main__":
    for n,f in [("fig49-1-row-vs-columnar.svg",fig_row_vs_col),("fig49-2-transaction-log.svg",fig_log)]:
        open(n,"w").write(f())
    print("ok")
