# Diagram figure for Chapter 15 (chart chooser). Run: python3 make_figs15_diagrams.py
# Drawn on a 720 px canvas so that the smallest text (10.5 px) prints at 10.5 x 493.2 / 720 = 7.2 pt (V15.4).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; SOFT="#e9eef4"
def chooser():
    rows=[("Compare categories",["Which is biggest? How do they rank?"],"Sorted bar chart",["dot plot · lollipop","table for exact values"],ACC),
          ("Show change over time",["Is it rising? When did it change?"],"Line chart",["column chart for few periods","slope chart · sparkline"],GREEN),
          ("Show a distribution",["What's typical? How spread out?","Any outliers?"],"Histogram · box plot",["strip or dot plot","density curve"],PURPLE),
          ("Show a relationship",["Do two measures move together?"],"Scatter plot",["bubble chart","heatmap of binned values"],ORANGE),
          ("Show parts of a whole",["What share does each part take?"],"Stacked or 100% bar",["pie (2–3 parts) · treemap","waterfall for changes"],GOLD),
          ("Show where",["Does location matter?"],"Map (filled or dots)",["sorted bar of regions","tile grid"],INK)]
    W=720; o=[text(16,26,"Start from the question, then choose the chart",14,INK,"bold",family=HEAD),
       text(16,54,"The question",11,MUTED,"bold"),text(292,54,"First choice",11,MUTED,"bold"),text(466,54,"Also consider",11,MUTED,"bold")]
    RH=58
    for i,(q,sub,first,alt,c) in enumerate(rows):
        y=64+i*RH
        o.append(rect(16,y,W-32,RH-8,fill="#fff",stroke=RULE,rx=6)); o.append(rect(16,y,7,RH-8,fill=c,rx=2))
        o.append(text(32,y+18,q,12.5,INK,"bold"))
        for k,sline in enumerate(sub): o.append(text(32,y+32+k*12,sline,10.5,MUTED))
        o.append(rect(288,y+10,164,30,fill=c,rx=15)); o.append(text(370,y+29.5,first,11,"#fff","bold",anchor="middle"))
        for k,aline in enumerate(alt): o.append(text(466,y+21+k*14,aline,10.5,INK))
    yb=64+len(rows)*RH+14
    o.append(text(16,yb,"Three more questions: who reads it, explore or explain, and what should they do next?",11,MUTED,style="italic"))
    return svg(W,yb+12,"".join(o))
open("fig15-2-chart-chooser.svg","w").write(chooser()); print("ok")
