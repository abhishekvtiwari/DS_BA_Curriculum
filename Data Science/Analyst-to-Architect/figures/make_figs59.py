# Generates the SVG figures for Chapter 59. Run: python3 make_figs59.py
# Both figures print at the full text width (493.2 pt), so on a 680 px canvas 1 px = 0.725 pt:
# the smallest text here, 10.5 px, prints at 7.6 pt (visual standard: 7 pt or more).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=680

def fig_frame():
    o=[text(20,26,"The six questions every project in this chapter answers",13,INK,"bold",family=HEAD)]
    steps=[("1","What decision changes?","If none, there is no project,\nhowever good the data",ACC),
           ("2","What data exists, and\nwhat must be created?","Usually the bigger half.\nUsually the labels",PURPLE),
           ("3","What is the simplest\nthing that could work?","The technical choice.\nThe smallest box here",GREEN),
           ("4","Where does the\noutput go?","Screen, queue, system of\nrecord, automated action",ORANGE),
           ("5","What does an error cost,\nand who finds it?","Sets the threshold, the review\ncapacity, whether to automate",RED),
           ("6","Who owns it in a year?","No answer: a demo\nwith a longer runway",INK)]
    cw, ch, gap = 206, 90, 11
    x, y = 20, 40
    for k,(number,question,detail,c) in enumerate(steps):
        inset = 8 if number == "3" else 0          # question 3 is drawn smaller, as the caption says
        bx, by, bw, bh = x+inset, y+inset/2, cw-2*inset, ch-inset
        o.append(rect(bx,by,bw,bh,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(rect(bx+10,by+10,22,22,fill=c,rx=11))
        o.append(text(bx+21,by+25.5,number,11.5,"#ffffff","bold",anchor="middle"))
        for i,line in enumerate(question.split("\n")):
            o.append(text(bx+38,by+25+i*15,line,11,c,"bold"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(bx+12,by+bh-26+i*13,line,10.5,MUTED))
        x += cw+gap
        if k == 2:
            x, y = 20, y+ch+10
    y += ch+10
    o.append(rect(20,y,640,44,fill="#f6f9fc",stroke=RULE,rx=8))
    o.append(text(340,y+18,"Question 3 is the one every case study is written about.",11.5,INK,"bold",anchor="middle"))
    o.append(text(340,y+35,"Questions 1, 2, 5 and 6 are where these nine projects were actually won or lost.",10.5,MUTED,anchor="middle"))
    return svg(W,y+52,"".join(o))

# One row per case, one column per pattern. A tick is drawn as a filled box with a white check mark,
# a blank as an empty box with a dash, so the grid reads without colour. The counts must match the text:
# 1. wrong problem 8 of 9 (not lead scoring) · 2. data work · 3. human attention (not pricing)
# 4. an organizational failure (not lead scoring, not pricing) · 5. the metric changed (6 of 9).
CASES=[("Case 1","Defect camera (Riverstone)"),("Case 2","Demand planning"),("Case 3","Lead scoring"),
       ("Case 4","Retail pricing"),("Case 5","Fraud detection"),("Case 6","Delivery routing"),
       ("Case 7","Support automation"),("Case 8","Predictive maintenance"),("Case 9","Order to cash (Riverstone)")]
PATTERNS=[(("1 The stated","problem was","wrong"),[1,1,0,1,1,1,1,1,1]),
          (("2 The data","work","dominated"),[0,1,1,1,1,1,0,1,1]),
          (("3 Human","attention","was the","constraint"),[1,1,1,0,1,1,1,1,1]),
          (("4 A failure","was organi-","zational"),[1,1,0,0,1,1,1,1,1]),
          (("5 The metric","had to","change"),[1,1,0,0,1,0,1,1,1])]

def fig_patterns():
    o=[text(20,26,"Five things went wrong in nine different projects",13,INK,"bold",family=HEAD)]
    x0, cell, rh = 240, 84, 25          # first pattern column, column width, row height
    for j,(lines,_) in enumerate(PATTERNS):
        cx = x0+j*cell+cell/2
        for i,line in enumerate(lines):
            o.append(text(cx,50+i*14,line,10.5,INK,"bold",anchor="middle"))
    y = 104
    for r,(num,name) in enumerate(CASES):
        if r%2==0: o.append(rect(20,y,640,rh,fill=ROWALT))
        o.append(text(28,y+17,num,11,INK,"bold"))
        o.append(text(80,y+17,name,11,INK))
        for j,(_,marks) in enumerate(PATTERNS):
            bx = x0+j*cell+cell/2-13
            if marks[r]:
                o.append(rect(bx,y+3,26,rh-6,fill=ACC,rx=4))
                o.append(path(f"M{bx+7},{y+12.5} l4.5,5 l8,-9",stroke="#ffffff",sw=2.2))
            else:
                o.append(rect(bx,y+3,26,rh-6,fill="#fff",stroke=RULE,rx=4))
                o.append(path(f"M{bx+9},{y+rh/2} h8",stroke=MUTED,sw=1.4))
        y += rh
    o.append(path(f"M20,{y+2} H660",stroke=RULE,sw=1))
    o.append(text(28,y+19,"Cases with the pattern",11,INK,"bold"))
    for j,(_,marks) in enumerate(PATTERNS):
        o.append(text(x0+j*cell+cell/2,y+19,f"{sum(marks)} of 9",11,INK,"bold",anchor="middle"))
    y += 34
    o.append(rect(20,y,640,50,fill="#e2f3ee",stroke=GREEN,rx=8))
    o.append(text(34,y+20,"None of these would have been prevented by a better algorithm.",11.5,INK,"bold"))
    o.append(text(34,y+38,"Most would have been caught in week two by sitting beside the person who had to use the thing.",10.5,INK))
    return svg(W,y+62,"".join(o))

if __name__=="__main__":
    open("fig59-1-project-frame.svg","w").write(fig_frame())
    open("fig59-2-patterns.svg","w").write(fig_patterns())
    print("ok59")
