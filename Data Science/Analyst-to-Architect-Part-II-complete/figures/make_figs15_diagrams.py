# Diagram figure for Chapter 15 (chart chooser). Run: python3 make_figs15_diagrams.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; SOFT="#e9eef4"
def chooser():
    rows=[("Compare categories","Which is biggest? How do they rank?","Sorted bar chart","dot plot · lollipop · table for exact values",ACC),
          ("Show change over time","Is it rising? When did it change?","Line chart","column chart for few periods · slope chart · sparkline",GREEN),
          ("Show a distribution","What's typical? How spread out? Outliers?","Histogram · box plot","strip or dot plot · density curve",PURPLE),
          ("Show a relationship","Do two measures move together?","Scatter plot","bubble chart · heatmap of binned values",ORANGE),
          ("Show parts of a whole","What share does each part take?","Stacked or 100% bar","pie (2–3 parts) · treemap · waterfall for changes",GOLD),
          ("Show where","Does location matter?","Map (filled or dots)","sorted bar of regions · tile grid",INK)]
    o=[text(30,32,"Start from the question, then choose the chart",15,INK,"bold",family=HEAD),
       text(30,70,"The question",12,MUTED,"bold"),text(390,70,"First choice",12,MUTED,"bold"),text(640,70,"Also consider",12,MUTED,"bold")]
    for i,(q,sub,first,alt,c) in enumerate(rows):
        y=84+i*62
        o.append(rect(30,y,980,52,fill="#fff",stroke=RULE,rx=7)); o.append(rect(30,y,8,52,fill=c,rx=2))
        o.append(text(52,y+22,q,13.5,INK,"bold")); o.append(text(52,y+41,sub,11.5,MUTED))
        o.append(rect(386,y+11,236,30,fill=c,rx=15)); o.append(text(504,y+31,first,12.5,"#fff","bold",anchor="middle"))
        o.append(text(640,y+31,alt,12,INK))
    o.append(text(30,470,"Two more questions decide the details: who is reading it, and what should they do next?",12,MUTED,style="italic"))
    return svg(1040,490,"".join(o))
open("fig15-2-chart-chooser.svg","w").write(chooser()); print("ok")
