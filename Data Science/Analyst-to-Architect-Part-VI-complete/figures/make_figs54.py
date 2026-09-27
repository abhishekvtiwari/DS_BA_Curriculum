# Generates the SVG figures for Chapter 54. Run: python3 make_figs54.py
# Every number shown was measured by the chapter's own code (companion/ch54, seed 54).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_next_token():
    o=[text(30,32,"What one forward pass produces: a probability for every token",14,INK,"bold",family=HEAD)]
    rows=[("cracked",0.442,GREEN),("delivered",0.327,GREEN),("late",0.147,ACC),("empty",0.073,ACC),
          ("blue",0.011,ORANGE),("photosynthesis",0.000,RED)]
    y=76
    for token,p,c in rows:
        o.append(text(180,y+16,token,12.5,INK,"bold",anchor="end",family=MONO))
        o.append(rect(200,y,max(3,p*620),24,fill=c,stroke=c,rx=4))
        o.append(text(210+max(3,p*620),y+17,f"{p:.3f}",12,INK))
        y+=38
    o.append(text(30,y+14,"\u201cThe crate was \u2026\u201d  The model ranks every token it knows. Sampling (section 54.5) decides which one is taken,",12,MUTED))
    o.append(text(30,y+34,"and the tail is never quite zero \u2014 which is the mechanical root of hallucination.",12,INK))
    return svg(1040,y+54,"".join(o))

def fig_prompts():
    o=[text(30,32,"Three prompts, 60 emails, one number: prompting is engineering",14,INK,"bold",family=HEAD)]
    rows=[("naive",12,156,4,RED),("with instructions",35,215,0,ORANGE),("plus one example",47,227,0,GREEN)]
    y=80
    for label,exact,fields,bad,c in rows:
        o.append(text(210,y+22,label,12.5,INK,"bold",anchor="end"))
        o.append(rect(230,y,600,34,fill="#f6f9fc",stroke=RULE,rx=5))
        o.append(rect(230,y,600*exact/60,34,fill=c,stroke=c,rx=5))
        o.append(text(240,y+22,f"{exact} of 60 emails fully correct",12,"#ffffff" if exact>20 else INK,"bold"))
        o.append(text(850,y+22,f"fields {fields}/240" + (f"  ·  {bad} unparseable" if bad else ""),12,MUTED))
        y+=56
    o.append(rect(230,y+10,600,60,fill="#fdf3dc",stroke=PK,rx=6))
    o.append(text(250,y+34,"Validation lets 59 of 60 through. Only 47 are actually right.",12.5,INK,"bold"))
    o.append(text(250,y+54,"The gap is a dozen well-formed, plausible, wrong orders.",12,INK))
    o.append(text(30,y+96,"Same model, same emails, same evaluation set. Only the wording changed \u2014 and the wording is code, so it belongs in Git.",12,MUTED))
    return svg(1040,y+116,"".join(o))

def fig_pipeline():
    o=[text(30,32,"The pipeline that ships: the model proposes, the rules dispose",14,INK,"bold",family=HEAD)]
    steps=[(30,"email arrives","60 a day, five shapes",RULE),
           (230,"prompt the model","instructions + example\ntemperature 0",ACC),
           (430,"parse","strip chat and fences\nJSON or nothing",PURPLE),
           (630,"validate","codes, dates, quantities\nbusiness rules",GREEN)]
    for x,title,detail,c in steps:
        o.append(rect(x,70,180,80,fill="#fff",stroke=c,sw=1.8,rx=8))
        o.append(text(x+90,96,title,12.5,c,"bold",anchor="middle"))
        for i,line in enumerate(detail.split("\n")):
            o.append(text(x+90,118+i*16,line,11,MUTED,anchor="middle"))
        if x<630:
            o.append(path(f"M{x+180},110 H{x+228}",stroke=INK,sw=2)); o.append(path(f"M{x+220},104 L{x+230},110 L{x+220},116",stroke=INK,sw=2))
    o.append(path("M810,110 H870",stroke=GREEN,sw=2)); o.append(path("M862,104 L872,110 L862,116",stroke=GREEN,sw=2))
    o.append(rect(870,70,150,80,fill="#e2f3ee",stroke=GREEN,sw=1.8,rx=8))
    o.append(text(945,104,"load to ERP",12.5,GREEN,"bold",anchor="middle")); o.append(text(945,126,"59 of 60",12,INK,anchor="middle"))
    o.append(path("M720,150 V200 H330 V174",stroke=ORANGE,sw=2,dash="5,4")); o.append(path("M324,182 L330,172 L336,182",stroke=ORANGE,sw=2))
    o.append(rect(560,200,320,44,fill="#fdf3dc",stroke=ORANGE,sw=1.6,rx=7))
    o.append(text(720,227,"retry once, quoting the exact problems",12,ORANGE,"bold",anchor="middle"))
    o.append(path("M720,244 V280",stroke=RED,sw=2)); o.append(path("M714,272 L720,282 L726,272",stroke=RED,sw=2))
    o.append(rect(560,282,320,50,fill="#fbeaea",stroke=RED,sw=1.6,rx=7))
    o.append(text(720,304,"still failing: a human, with the reason",12.5,RED,"bold",anchor="middle"))
    o.append(text(720,322,"the exception queue is the product, not the failure",11.5,INK,anchor="middle"))
    o.append(text(30,366,"Nothing the model returns is trusted. Every field is checked against real product codes, a plausible date window and sane quantities,",12,MUTED))
    o.append(text(30,386,"which is also what stops a prompt-injection line in a customer's email from changing an order.",12,INK))
    return svg(1040,406,"".join(o))

def fig_sampling():
    o=[text(30,32,"Temperature and top-p, measured over 10,000 draws",14,INK,"bold",family=HEAD)]
    tokens=["cracked","delivered","late","empty","blue","photosyn."]
    rows=[("temperature 0.2",[0.816,0.181,0.003,0.000,0.000,0.000]),
          ("temperature 1.0",[0.442,0.330,0.143,0.075,0.009,0.000]),
          ("temperature 1.8",[0.349,0.297,0.178,0.126,0.044,0.005]),
          ("t 1.0, top_p 0.9",[0.580,0.420,0.000,0.000,0.000,0.000])]
    x0=250; w=120
    for j,t in enumerate(tokens):
        o.append(text(x0+j*w+w/2,72,t,11.5,MUTED,"bold",anchor="middle"))
    y=86
    for label,values in rows:
        o.append(text(x0-16,y+24,label,12,INK,"bold",anchor="end",family=MONO))
        for j,v in enumerate(values):
            shade=int(255-v*150)
            o.append(rect(x0+j*w,y,w-6,38,fill=f"rgb({shade},{min(255,shade+20)},{shade+8})",stroke=RULE,rx=5))
            o.append(text(x0+j*w+(w-6)/2,y+24,f"{v:.3f}",12,INK,"bold" if v>0.3 else "normal",anchor="middle",family=MONO))
        y+=46
    o.append(text(30,y+22,"Temperature divides the scores before softmax: low sharpens, high flattens. top_p cuts the tail off entirely, so the two",12,MUTED))
    o.append(text(30,y+42,"rightmost tokens can never be drawn. For extraction use temperature 0; for drafting, 0.3\u20130.7.",12,INK))
    return svg(1040,y+62,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig54-1-next-token.svg",fig_next_token),("fig54-2-prompt-results.svg",fig_prompts),
                    ("fig54-3-pipeline.svg",fig_pipeline),("fig54-4-sampling.svg",fig_sampling)]:
        open(name,"w").write(fn())
    print("ok54")
