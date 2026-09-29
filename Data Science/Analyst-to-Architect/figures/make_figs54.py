# Generates the SVG figures for Chapter 54. Run: python3 make_figs54.py
# Every number shown was printed by the chapter's own code (companion/ch54, seed 54; section 54.5's
# sampling table, section 54.6's evaluation, section 54.7's pipeline counts).
# Canvas 720 px wide, printed at 493.2 pt: 10.5 px text prints at 7.2 pt, so no text is smaller than 10.5.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
W=720

def arrow(x1,y,x2,c=INK):
    return path(f"M{x1},{y} H{x2-2}",stroke=c,sw=2)+path(f"M{x2-8},{y-5} L{x2},{y} L{x2-8},{y+5}",stroke=c,sw=2)

def fig_next_token():
    o=[text(20,26,"One forward pass: a probability for every token",14,INK,"bold",family=HEAD),
       text(20,46,"“The crate was …”  (section 54.1; bars in order of probability)",11.5,MUTED)]
    rows=[("cracked",0.442,GREEN),("delivered",0.327,GREEN),("late",0.147,ACC),("empty",0.073,ACC),
          ("blue",0.011,ORANGE),("photosynthesis",0.000,RED)]
    y=64
    for token,p,c in rows:
        o.append(text(150,y+15,token,12,INK,"bold",anchor="end",family=MONO))
        o.append(rect(162,y,max(3,p*960),22,fill=c,stroke=c,rx=4))
        o.append(text(170+max(3,p*960),y+15,f"{p:.3f}",12,INK))
        y+=32
    o.append(text(20,y+14,"The model ranks tokens by how plausible they are, not by whether they are true.",11.5,MUTED))
    o.append(text(20,y+32,"When the plausible word and the true one differ, it confidently says the wrong one.",11.5,MUTED))
    return svg(W,y+44,"".join(o))

def fig_sampling():
    o=[text(20,26,"Temperature and top-p, measured over 10,000 draws",14,INK,"bold",family=HEAD)]
    tokens=["cracked","delivered","empty","late","blue","photo…"]
    rows=[("temperature 0 (greedy)",[1.000,0.000,0.000,0.000,0.000,0.000]),
          ("temperature 0.2",[0.816,0.181,0.000,0.003,0.000,0.000]),
          ("temperature 1.0",[0.442,0.330,0.075,0.143,0.009,0.000]),
          ("temperature 1.8",[0.349,0.297,0.126,0.178,0.044,0.005]),
          ("temperature 1.0 + top_p 0.9",[0.484,0.359,0.000,0.158,0.000,0.000])]
    x0=236; w=80
    for j,t in enumerate(tokens):
        o.append(text(x0+j*w+(w-6)/2,56,t,11,MUTED,"bold",anchor="middle"))
    y=66
    for label,values in rows:
        o.append(text(x0-10,y+20,label,11,INK,"bold",anchor="end"))
        for j,v in enumerate(values):
            shade=int(255-v*150)
            o.append(rect(x0+j*w,y,w-6,30,fill=f"rgb({shade},{min(255,shade+20)},{shade+8})",stroke=RULE,rx=4))
            o.append(text(x0+j*w+(w-6)/2,y+20,f"{v:.3f}",11.5,INK,"bold" if v>0.3 else "normal",anchor="middle",family=MONO))
        y+=36
    o.append(text(20,y+16,"Low temperature sharpens, high flattens. top_p 0.9 keeps the three tokens whose running",11.5,MUTED))
    o.append(text(20,y+34,"total first reaches 0.9, so empty, blue and photosynthesis can never be drawn.",11.5,MUTED))
    return svg(W,y+46,"".join(o))

def fig_prompts():
    o=[text(20,26,"Three prompts, 60 emails, one number each",14,INK,"bold",family=HEAD),
       text(20,46,"Measured on the chapter's stand-in model: the method is real, the numbers illustrate it.",11.5,MUTED)]
    rows=[("naive",13,161,3,RED),("with instructions",35,215,0,ORANGE),("plus one example",47,227,0,GREEN)]
    y=66; x0=150; bw=400
    for label,exact,fields,bad,c in rows:
        o.append(text(x0-10,y+19,label,12,INK,"bold",anchor="end"))
        o.append(rect(x0,y,bw,28,fill=ROWALT,stroke=RULE,rx=4))
        o.append(rect(x0,y,bw*exact/60,28,fill=c,stroke=c,rx=4))
        o.append(text(x0+bw*exact/60+8,y+19,f"{exact} of 60",12,INK,"bold"))
        o.append(text(x0+bw+10,y+12,f"fields {fields}/240",11,MUTED))
        o.append(text(x0+bw+10,y+26,f"{bad} unparseable",11,MUTED))
        y+=40
    o.append(text(x0,y+4,"bar = emails fully correct (all four fields right)",11,MUTED))
    o.append(text(20,y+30,"Same stand-in, same emails, same marking: only the wording of the prompt changed.",11.5,MUTED))
    return svg(W,y+42,"".join(o))

def fig_pipeline():
    o=[text(20,26,"The pipeline: the model proposes, the rules dispose",14,INK,"bold",family=HEAD)]
    steps=[(20,"email arrives","20–40 a day,\nfive shapes",MUTED),
           (150,"prompt","instructions,\nthen the email",ACC),
           (280,"parse","JSON object,\nor None",PURPLE),
           (410,"validate","codes, dates,\nquantities",GREEN)]
    for x,title,detail,c in steps:
        o.append(rect(x,50,112,70,fill="#fff",stroke=c,sw=1.8,rx=7))
        o.append(text(x+56,72,title,12,c if c!=MUTED else INK,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+56,92+i*15,line,11,MUTED,anchor="middle"))
    for x,_,_,_ in steps[:-1]:
        o.append(arrow(x+113,85,x+149))
    o.append(arrow(522,85,558,GREEN))
    o.append(rect(558,50,142,70,fill=FKBG,stroke=GREEN,sw=1.8,rx=7))
    o.append(text(629,72,"load to ERP",12,GREEN,"bold",anchor="middle"))
    o.append(text(629,92,"59 of 60 loaded",11,INK,anchor="middle"))
    o.append(text(629,107,"47 right, 12 wrong",11,RED,"bold",anchor="middle"))
    o.append(path("M466,120 V160 H206 V128",stroke=ORANGE,sw=2,dash="5,4")); o.append(path("M200,134 L206,124 L212,134",stroke=ORANGE,sw=2))
    o.append(rect(286,146,280,30,fill=PKBG,stroke=ORANGE,sw=1.4,rx=6))
    o.append(text(426,166,"retry once, quoting the exact problems",11,ORANGE,"bold",anchor="middle"))
    o.append(path("M466,176 V200",stroke=RED,sw=2)); o.append(path("M460,194 L466,202 L472,194",stroke=RED,sw=2))
    o.append(rect(330,202,272,40,fill="#fbeaea",stroke=RED,sw=1.4,rx=6))
    o.append(text(466,219,"still failing: a person, with the reason",11.5,RED,"bold",anchor="middle"))
    o.append(text(466,235,"1 of 60 here (“no items”)",11,INK,anchor="middle"))
    o.append(text(20,268,"Validation catches malformed answers; only a check against the truth finds the 12 that",11.5,MUTED))
    o.append(text(20,286,"are well-formed, plausible and wrong. Sample loaded orders by hand every week.",11.5,MUTED))
    return svg(W,298,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig54-1-next-token.svg",fig_next_token),("fig54-2-sampling.svg",fig_sampling),
                    ("fig54-3-prompt-results.svg",fig_prompts),("fig54-4-pipeline.svg",fig_pipeline)]:
        open(name,"w").write(fn())
    print("ok54")
