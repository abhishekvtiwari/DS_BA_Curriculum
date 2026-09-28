# Generates the SVG figures for Chapter 7. Run: python3 make_figs07.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Canvas 720 px wide: a figure prints at 493.2 pt, so the smallest font here (10.5 px) prints at 7.2 pt.
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; TEAL="#1f6f86"
CW_=720

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.45), y2-L*math.sin(a-0.45)); p2=(x2-L*math.cos(a+0.45), y2-L*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def header_card(x,y,w,h,c,title,sub=None,tsize=15):
    o=[rect(x+3,y+4,w,h,fill="#e9eef4",rx=8), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+34} H{x} Z" fill="{c}"/>',
       text(x+12,y+23,title,tsize,"#fff","bold",family=HEAD)]
    if sub: o.append(text(x+12,y+54,sub,12,c,"bold",style="italic"))
    return "".join(o)

def wrapc(s,n,sep=" "):
    """Split s into lines of at most n characters, breaking at sep."""
    parts=s.split(sep); lines=[]; cur=""
    for p_ in parts:
        cand=(cur+sep+p_) if cur else p_
        if len(cand)>n and cur: lines.append(cur+("" if sep==" " else " "+sep.strip())); cur=p_
        else: cur=cand
    lines.append(cur); return lines

# ---------- Figure 7.1: four questions, tracks, and roles (2 x 2 panels) ----------
def fig_questions():
    o=[]
    cols=[("Question 1",ACC,["What happened?"],"Analytics & BI",
           ["Data analyst","Business analyst","BI developer"],"Parts 2–3"),
          ("Question 2",PURPLE,["What will happen,","and why?"],"Data science, ML & AI",
           ["Data scientist","ML engineer","AI engineer"],"Parts 4 and 6"),
          ("Question 3",GREEN,["How does data move,","and get put to work?"],"Engineering & integration",
           ["Data engineer","Analytics engineer","Automation analyst,","  RPA developer,","  integration engineer"],"Parts 2, 3 and 5"),
          ("Question 4",ORANGE,["How should the whole","system be designed?"],"Architecture",
           ["Data architect"],"Part 7")]
    W=336; G=16; h=300; x0=16; y0=16
    for i,(qn,c,q,track,roles,part) in enumerate(cols):
        x=x0+(i%2)*(W+G); top=y0+(i//2)*(h+G)
        o.append(rect(x+3,top+4,W,h,fill="#e9eef4",rx=8)); o.append(rect(x,top,W,h,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x},{top+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{top+80} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,top+22,qn.upper(),11,"#ffffff","bold"))
        o.append(wrap(x+14,top+46,q,15,"#ffffff",22,"bold",family=HEAD))
        o.append(text(x+14,top+104,"TRACK",11,MUTED,"bold"))
        o.append(text(x+14,top+124,track,14,c,"bold"))
        o.append(path(f"M{x+14},{top+138} H{x+W-14}",stroke=RULE,sw=1))
        o.append(text(x+14,top+158,"ROLES",11,MUTED,"bold"))
        yy=top+180
        for r in roles:
            if not r.startswith("  "): o.append(f'<circle cx="{x+19}" cy="{yy-4}" r="3.5" fill="{c}"/>')
            o.append(text(x+30,yy,r.strip(),13,INK)); yy+=21
        o.append(text(x+14,top+h-14,"Taught in "+part,12,MUTED,style="italic"))
    y2=y0+2*(h+G)+6
    o.append(rect(x0,y2,2*W+G,76,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(x0+14,y2+22,"Underneath all four: governance and data quality",12.5,INK))
    o.append(text(x0+14,y2+41,"(data stewards, data quality and governance analysts).",12.5,INK))
    o.append(text(x0+14,y2+62,"Shared by every role: SQL, business context, and some automation of repeated work.",12,INK,"bold"))
    return svg(CW_,y2+92,"".join(o))

# ---------- Figure 7.2: the field grows like a tree ----------
def fig_tree():
    o=[]; BH=84
    def box(cx,y,w,h,c,title,lines):
        x=cx-w/2
        return header_card(x,y,w,h,c,title,tsize=13)+wrap(x+12,y+54,lines,12,INK,18)
    R=[20,132,244,356,468,580]   # row tops, top of the tree first
    top=box(360,R[0],340,BH,ORANGE,"Architecture & leadership · Part 7",["Designs the whole system; has walked","part of every branch below"])
    ai=box(360,R[1],340,BH,PURPLE,"Production ML & AI · Part 6",["Models, AI applications, and automations","running inside the business"])
    ds=box(190,R[2],300,BH,PURPLE,"Data science & ML · Part 4",["Prediction, experiments, models"])
    de=box(530,R[2],300,BH,GREEN,"Engineering & integration · Part 5",["Pipelines, platforms, pushing data","into other systems"])
    br=box(360,R[3],400,BH,ACC,"Advanced analytics & analytics engineering",["Part 3 · the branch point: statistics,","tested models of data, software habits"])
    tr=box(360,R[4],300,BH,ACC,"The analyst core · Part 2",["Spreadsheets, SQL, BI, Python,","automation, statistics, business sense"])
    gr=box(360,R[5],420,68,MUTED,"Foundations · Parts 0 and 1",["What data is, how a business runs on it"])
    con=[path(f"M360,{R[5]} V{R[4]+BH}",stroke=RULE,sw=10),
         path(f"M360,{R[4]} V{R[3]+BH}",stroke=RULE,sw=10),
         path(f"M300,{R[3]} C300,{R[3]-24} 190,{R[2]+BH+24} 190,{R[2]+BH}",stroke=RULE,sw=8),
         path(f"M420,{R[3]} C420,{R[3]-24} 530,{R[2]+BH+24} 530,{R[2]+BH}",stroke=RULE,sw=8),
         path(f"M190,{R[2]} C190,{R[2]-22} 310,{R[1]+BH+22} 310,{R[1]+BH}",stroke=RULE,sw=6),
         path(f"M530,{R[2]} C530,{R[2]-22} 410,{R[1]+BH+22} 410,{R[1]+BH}",stroke=RULE,sw=6),
         path(f"M360,{R[1]} V{R[0]+BH}",stroke=RULE,sw=6)]
    o.extend(con); o.extend([top,ai,ds,de,br,tr,gr])
    # side notes beside the analyst core
    o.append(rect(16,R[4]-6,184,96,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(26,R[4]+14,["Most people enter here.","Every branch above","keeps using these skills:","SQL never leaves you."],11.5,INK,20))
    o.append(rect(520,R[4]-6,184,96,fill="#fff4d6",stroke="#e2c46b",rx=6))
    o.append(wrap(530,R[4]+14,["Part 8, the interview","playbook, has question","banks for every level","of the tree."],11.5,INK,20))
    return svg(CW_,R[5]+68+16,"".join(o))

# ---------- Figure 7.3: from source to action (stages top to bottom) ----------
def fig_source_to_action():
    o=[]
    stages=[("Sources",MUTED,"Orders (ERP) · Leads (CRM) · Payments · Support tickets"),
            ("Move and check",GREEN,"Scheduled loads · Quality checks · Warehouse"),
            ("Shape and predict",PURPLE,"Shared definitions · Risk score · Forecasts"),
            ("Deliver and act",ACC,"Dashboard · Report in the email body · Task written into the CRM · Alert when a rule trips")]
    who=["Business systems record it","Data engineer · integration engineer","Analytics engineer · data scientist · ML engineer","Analyst · BI developer · integration engineer · AI engineer"]
    manual=["Export by hand","Copy-paste into one file","Formulas re-typed each week","Emailed attachment, re-keyed into the CRM"]
    X=[16,286,500]; WD=[256,200,204]; top=40; RH=104; G=20
    o.append(text(X[0],26,"AUTOMATED FLOW",11,MUTED,"bold"))
    o.append(text(X[1],26,"WHO AUTOMATES IT",11,MUTED,"bold"))
    o.append(text(X[2],26,"THE SAME STEP BY HAND",11,RED,"bold"))
    for i,(name,c,items) in enumerate(stages):
        y=top+i*(RH+G)
        o.append(header_card(X[0],y,WD[0],RH,c,name,tsize=13.5))
        o.append(wrap(X[0]+12,y+54,wrapc(items,37," · "),11.5,INK,18))
        o.append(rect(X[1],y,WD[1],RH,fill="#f6f9fc",stroke=RULE,rx=6))
        o.append(wrap(X[1]+12,y+26,wrapc(who[i],24," · "),12,INK,19,"bold"))
        o.append(rect(X[2],y,WD[2],RH,fill="#fbeaea",stroke="#e3b7b7",rx=6))
        o.append(text(X[2]+12,y+24,"By hand:",11,RED,"bold"))
        o.append(wrap(X[2]+12,y+44,wrapc(manual[i],26),12,INK,18))
        if i<3: o.append(arrow(X[0]+WD[0]/2,y+RH+2,X[0]+WD[0]/2,y+RH+G-2,c=INK,sw=2.2))
    return svg(CW_,top+4*RH+3*G+16,"".join(o))

# ---------- Figure 7.4: three ways to organize a data team (one row each) ----------
def fig_teams():
    o=[]
    depts=["Sales","Finance","Operations","Marketing"]
    panels=[("Centralized",ACC,["One data team serves every","department from the middle."],
             "+ one version of the numbers","– can feel far from the business","Often the first setup"),
            ("Embedded",PURPLE,["Analysts sit inside departments","and report to their heads."],
             "+ deep business context, fast","– definitions drift apart","Common where departments differ a lot"),
            ("Hub-and-spoke",GREEN,["A central hub owns the platform","and definitions; spokes sit in teams."],
             "+ context and consistency","– needs clear ownership rules","Common as companies grow")]
    PH=176; G=14; x0=16; W=688
    for i,(name,c,desc,plus,minus,note) in enumerate(panels):
        y=16+i*(PH+G)
        o.append(rect(x0,y,W,PH,fill="#fbfcfe",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x0},{y+8} a8,8 0 0 1 8,-8 H{x0+W-8} a8,8 0 0 1 8,8 V{y+30} H{x0} Z" fill="{c}"/>')
        o.append(text(x0+14,y+21,name,14,"#fff","bold",family=HEAD))
        # diagram: hub above, four departments below
        dx0=x0+14; DW=96; DG=10; dy=y+112; hx=dx0+(4*DW+3*DG)/2
        hw,hh,hy=170,40,y+44
        for k in range(4):
            ex=dx0+k*(DW+DG)+DW/2
            if i==0: o.append(arrow(hx+(k-1.5)*30,hy+hh,ex,dy-2,c=c,sw=1.6))
            if i==2: o.append(path(f"M{hx+(k-1.5)*30},{hy+hh} L{ex},{dy}",stroke=c,sw=1.6,dash="5 4"))
        if i==1:
            o.append(rect(hx-hw/2,hy,hw,hh,fill="#fff",stroke=RULE,sw=1,rx=6,extra='stroke-dasharray="5 4"'))
            o.append(text(hx,hy+17,"no central team",12,MUTED,anchor="middle",style="italic"))
            o.append(text(hx,hy+33,"(or a very small one)",11,MUTED,anchor="middle",style="italic"))
        else:
            o.append(rect(hx-hw/2,hy,hw,hh,fill=c,rx=6))
            o.append(text(hx,hy+18,"Data team" if i==0 else "Hub",13,"#fff","bold",anchor="middle"))
            o.append(text(hx,hy+33,"all analysts here" if i==0 else "platform · standards",11,"#ffffff",anchor="middle"))
        for k,d in enumerate(depts):
            xx=dx0+k*(DW+DG)
            o.append(rect(xx,dy,DW,52,fill="#fff",stroke=RULE,sw=1.2,rx=6))
            o.append(text(xx+10,dy+20,d,12,INK,"bold"))
            if i>0:
                o.append(f'<circle cx="{xx+17}" cy="{dy+37}" r="6" fill="{c}"/>')
                o.append(text(xx+28,dy+41,"analyst",11,MUTED))
        # text column
        tx=x0+452
        o.append(wrap(tx,y+54,desc,12,INK,18))
        o.append(text(tx,y+104,plus,12.5,GREEN,"bold"))
        o.append(text(tx,y+128,minus,12.5,RED,"bold"))
        o.append(wrap(tx,y+150,wrapc(note,26),11.5,MUTED,15))
    return svg(CW_,16+3*PH+2*G+16,"".join(o))

# ---------- Figure 7.5: one request, every role (five phases, top to bottom) ----------
def fig_one_request():
    o=[]
    phases=[("Clarify and answer",ACC,[("Business analyst","makes the request a clear question"),
                                        ("Data analyst","finds the five quiet customers")]),
            ("Share and standardize",ACC,[("BI developer","at-risk page on the sales dashboard"),
                                           ("Analytics engineer","one tested definition of \"active\"")]),
            ("Supply trusted data",GREEN,[("Data engineer","fresh, checked data from payments, support and the CRM by 6 a.m.")]),
            ("Predict",PURPLE,[("Data scientist","predicts who will go quiet next"),
                               ("ML engineer","scores every customer each night")]),
            ("Act",TEAL,[("Integration engineer","tasks in the CRM, Monday email"),
                         ("AI engineer","call brief drafted; rep approves")])]
    x0=16; W=688
    o.append(rect(x0,14,W,58,fill="#fff4e8",stroke=ORANGE,sw=1.6,rx=8))
    o.append(text(x0+14,34,"Data architect, across every phase",13.5,ORANGE,"bold",family=HEAD))
    o.append(text(x0+14,56,"Designs how the pieces fit: where the score lives, who owns each definition, who may see what.",11.5,INK))
    LW=164; CWd=252; G=10; RH=50; RG=10; ytop=86
    for i,(ph,c,cards) in enumerate(phases):
        y=ytop+i*(RH+RG)
        o.append(f'<circle cx="{x0+14}" cy="{y+18}" r="12" fill="{c}"/>'); o.append(text(x0+14,y+22.5,str(i+1),12,"#fff","bold",anchor="middle"))
        o.append(wrap(x0+34,y+23,wrapc(ph,13),13,c,17,"bold",family=HEAD))
        if i<4: o.append(arrow(x0+14,y+32,x0+14,y+RH+RG+4,c=MUTED,sw=1.8))
        x=x0+LW+G
        for role,did in cards:
            w=CWd if len(cards)==2 else 2*CWd+G
            o.append(rect(x+3,y+3,w,RH,fill="#e9eef4",rx=7)); o.append(rect(x,y,w,RH,fill="#fff",stroke=c,sw=1.4,rx=7))
            o.append(text(x+12,y+20,role,13,INK,"bold"))
            o.append(text(x+12,y+39,did,11.5,MUTED))
            x+=w+G
    yb=ytop+5*(RH+RG)+4
    o.append(rect(x0,yb,W,52,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(x0+14,yb+20,"Start: \"Some customers seem to have stopped ordering. Which ones, and what should we do?\"",11.5,INK))
    o.append(text(x0+14,yb+40,"End: every Monday, each sales rep knows which customers to call, and why.",11.5,INK,"bold"))
    return svg(CW_,yb+62,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig7-1-four-questions-and-roles.svg",fig_questions),("fig7-2-the-field-as-a-tree.svg",fig_tree),
                    ("fig7-3-source-to-action.svg",fig_source_to_action),
                    ("fig7-4-three-team-structures.svg",fig_teams),("fig7-5-one-request-every-role.svg",fig_one_request)]:
        open(name,"w").write(fn())
    print("ok")
