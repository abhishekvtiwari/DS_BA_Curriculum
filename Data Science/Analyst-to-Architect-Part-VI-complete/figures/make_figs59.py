# Generates the SVG figures for Chapter 59. Run: python3 make_figs59.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_frame():
    o=[text(30,32,"The six questions every project in this chapter answers",14,INK,"bold",family=HEAD)]
    steps=[("1","What decision changes?","If none, there is no project,\nhowever good the data",ACC),
           ("2","What data exists, and\nwhat must be created?","Usually the bigger half.\nUsually the labels",PURPLE),
           ("3","What is the simplest\nthing that could work?","The technical choice.\nThe smallest box here",GREEN),
           ("4","Where does the output go?","Screen, queue, system of record,\nautomated action",ORANGE),
           ("5","What does an error cost,\nand who finds it?","Sets the threshold, the review\ncapacity, and whether to automate",RED),
           ("6","Who owns it in a year?","No answer: a demo\nwith a longer runway",INK)]
    x,y=30,72
    for number,question,detail,c in steps:
        o.append(rect(x,y,300,120,fill="#fff",stroke=c,sw=1.8,rx=9))
        o.append(rect(x+16,y+14,26,26,fill=c,rx=13))
        o.append(text(x+29,y+32,number,13,"#ffffff","bold",anchor="middle"))
        for i,line in enumerate(question.split("\n")):
            o.append(text(x+56,y+32+i*17,line,12.5,c,"bold"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+22,y+76+i*17,line,11.5,MUTED))
        x += 330
        if x > 700:
            x, y = 30, y+140
    o.append(rect(30,y+8,980,54,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(520,y+30,"Question 3 is the one every case study is written about.",12.5,INK,"bold",anchor="middle"))
    o.append(text(520,y+50,"Questions 1, 2, 5 and 6 are where these nine projects were actually won or lost.",12,MUTED,anchor="middle"))
    return svg(1040,y+84,"".join(o))

def fig_patterns():
    o=[text(30,32,"Five things went wrong in nine different industries",14,INK,"bold",family=HEAD)]
    cases=["quality","demand","leads","pricing","fraud","routing","support","mainten.","order-cash"]
    patterns=[("the stated problem was the wrong one",[1,1,0,1,1,1,1,0,1]),
              ("data work dominated the schedule",[0,1,1,1,1,1,0,1,1]),
              ("the constraint was human attention",[1,1,1,0,1,1,1,1,1]),
              ("the failure was organizational",[1,1,1,1,1,1,1,1,1]),
              ("the metric had to change",[1,1,0,0,1,0,1,1,1])]
    x0=430; cell=64
    for j,case in enumerate(cases):
        o.append(text(x0+j*cell+cell/2,66,case,9.5,MUTED,anchor="middle"))
    y=80
    for label,marks in patterns:
        o.append(text(x0-16,y+24,label,12,INK,"bold",anchor="end"))
        for j,mark in enumerate(marks):
            c = ACC if mark else "#eef2f5"
            o.append(rect(x0+j*cell,y,cell-6,36,fill=c,stroke=RULE if not mark else c,rx=5))
            if mark:
                o.append(path(f"M{x0+j*cell+18},{y+19} l6,7 l13,-14",stroke="#ffffff",sw=2.4))
        y+=44
    o.append(rect(30,y+14,980,66,fill="#e2f3ee",stroke=GREEN,rx=8))
    o.append(text(48,y+38,"Not one of these five is a modeling error, and not one would have been prevented by a better algorithm.",12.5,INK,"bold"))
    o.append(text(48,y+60,"Most would have been caught in week two by sitting beside the person who had to use the thing.",12,INK))
    return svg(1040,y+102,"".join(o))

if __name__=="__main__":
    open("fig59-1-project-frame.svg","w").write(fig_frame())
    open("fig59-2-patterns.svg","w").write(fig_patterns())
    print("ok59")
