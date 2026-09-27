# Generates the SVG figures for Chapter 7. Run: python3 make_figs07.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

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

# ---------- Figure 7.1: four questions, tracks, and roles ----------
def fig_questions():
    o=[]
    cols=[("Question 1",ACC,["What happened?"],"Analytics & BI",
           ["Data analyst","Business analyst","BI developer"],"Parts II–III"),
          ("Question 2",PURPLE,["What will happen,","and why?"],"Data science, ML & AI",
           ["Data scientist","ML engineer","AI engineer"],"Parts IV and VI"),
          ("Question 3",GREEN,["How does data move,","and get put to work?"],"Engineering & integration",
           ["Data engineer","Analytics engineer","Automation analyst,","  RPA developer,","  integration engineer"],"Parts II, III and V"),
          ("Question 4",ORANGE,["How should the whole","system be designed?"],"Architecture",
           ["Data architect"],"Part VII")]
    W=236; G=14; top=30; h=330
    for i,(qn,c,q,track,roles,part) in enumerate(cols):
        x=30+i*(W+G)
        o.append(rect(x+3,top+4,W,h,fill="#e9eef4",rx=8)); o.append(rect(x,top,W,h,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x},{top+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{top+80} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,top+22,qn.upper(),11,"#ffffff","bold"))
        o.append(wrap(x+14,top+46,q,15,"#ffffff",22,"bold",family=HEAD))
        o.append(text(x+14,top+108,"TRACK",10.5,MUTED,"bold"))
        o.append(text(x+14,top+128,track,13.5,c,"bold"))
        o.append(path(f"M{x+14},{top+142} H{x+W-14}",stroke=RULE,sw=1))
        o.append(text(x+14,top+164,"ROLES",10.5,MUTED,"bold"))
        yy=top+186
        for r in roles:
            if not r.startswith("  "): o.append(f'<circle cx="{x+19}" cy="{yy-4}" r="3.5" fill="{c}"/>')
            o.append(text(x+30,yy,r.strip(),13,INK)); yy+=22
        o.append(text(x+14,top+h-16,"Taught in "+part,11.5,MUTED,style="italic"))
    y2=top+h+22
    o.append(rect(30,y2,4*W+3*G,48,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(46,y2+20,"Underneath all four: governance and data quality (data stewards, data quality and governance analysts).",12.5,INK))
    o.append(text(46,y2+38,"Shared by every role: SQL, business context, and some automation of repeated work.",12.5,INK,"bold"))
    return svg(1030,y2+66,"".join(o))

# ---------- Figure 7.2: the field grows like a tree ----------
def fig_tree():
    o=[]
    def box(cx,y,w,h,c,title,lines):
        x=cx-w/2
        return header_card(x,y,w,h,c,title,tsize=13.5)+wrap(x+12,y+56,lines,12,INK,18)
    # geometry (y grows downward; the tree grows upward)
    top=box(515,24,330,96,ORANGE,"Architecture & leadership · Part VII",["Designs the whole system; has walked","part of every branch below"])
    ai=box(515,150,330,96,PURPLE,"Production ML & AI · Part VI",["Models, AI applications, and automations","running inside the business"])
    ds=box(275,290,300,96,PURPLE,"Data science & ML · Part IV",["Prediction, experiments, models"])
    de=box(755,290,300,96,GREEN,"Engineering & integration · Part V",["Pipelines, platforms, pushing data","into other systems"])
    br=box(515,430,360,96,ACC,"Advanced analytics & analytics engineering",["Part III · the branch point: statistics,","tested models of data, software habits"])
    tr=box(515,570,360,96,ACC,"The analyst core · Part II",["Spreadsheets, SQL, BI, Python, automation,","statistics, business sense"])
    gr=box(515,710,420,78,MUTED,"Foundations · Parts 0 and I",["What data is, how a business runs on it"])
    # connectors (drawn first so boxes sit on top)
    con=[]
    con.append(path("M515,710 V666",stroke=RULE,sw=10))
    con.append(path("M515,570 V526",stroke=RULE,sw=10))
    con.append(path("M455,430 C455,400 275,420 275,386",stroke=RULE,sw=8))
    con.append(path("M575,430 C575,400 755,420 755,386",stroke=RULE,sw=8))
    con.append(path("M275,290 C275,262 455,276 455,246",stroke=RULE,sw=6))
    con.append(path("M755,290 C755,262 575,276 575,246",stroke=RULE,sw=6))
    con.append(path("M515,150 V120",stroke=RULE,sw=6))
    o.extend(con); o.extend([top,ai,ds,de,br,tr,gr])
    # side notes
    o.append(rect(30,560,200,112,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(44,584,["Most people enter here.","Every branch above keeps","using these skills:","SQL never leaves you."],12,INK,20))
    o.append(rect(800,560,210,112,fill="#fff4d6",stroke="#e2c46b",rx=6))
    o.append(wrap(814,584,["Part VIII, the interview","playbook, has question","banks for every level","of the tree."],12,INK,20))
    return svg(1040,810,"".join(o))

# ---------- Figure 7.4: three ways to organize a data team ----------
def fig_teams():
    o=[]
    depts=["Sales","Finance","Operations","Marketing"]
    PW=320; G=20; top=20
    panels=[("Centralized",ACC,["One data team serves every","department from the middle."],
             "+ one version of the numbers","– can feel far from the business","Often the first setup"),
            ("Embedded",PURPLE,["Analysts sit inside departments","and report to their heads."],
             "+ deep business context, fast","– definitions drift apart","Common where departments differ a lot"),
            ("Hub-and-spoke",GREEN,["A central hub owns the platform","and definitions; spokes sit in teams."],
             "+ context and consistency","– needs clear ownership rules","Common as companies grow")]
    for i,(name,c,desc,plus,minus,note) in enumerate(panels):
        px=30+i*(PW+G)
        o.append(rect(px,top,PW,470,fill="#fbfcfe",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{px},{top+8} a8,8 0 0 1 8,-8 H{px+PW-8} a8,8 0 0 1 8,8 V{top+36} H{px} Z" fill="{c}"/>')
        o.append(text(px+14,top+25,name,15,"#fff","bold",family=HEAD))
        o.append(wrap(px+14,top+60,desc,12,INK,18))
        coords=[(px+14,top+100),(px+166,top+100),(px+14,top+280),(px+166,top+280)]
        hx,hy,hw,hh=px+PW/2-80,top+192,160,56; hcx,hcy=px+PW/2,hy+hh/2
        # connectors first
        for k,(dx,dy) in enumerate(coords):
            ex=dx+70; ey=dy+62 if k<2 else dy
            sy=hy if k<2 else hy+hh
            if i==0: o.append(arrow(hcx+(-30 if k%2==0 else 30),sy,ex,ey+(2 if k<2 else -2),c=c,sw=1.6))
            if i==2: o.append(path(f"M{hcx+(-30 if k%2==0 else 30)},{sy} L{ex},{ey}",stroke=c,sw=1.6,dash="5 4"))
        if i==1:
            o.append(rect(hx,hy,hw,hh,fill="#fff",stroke=RULE,sw=1,rx=6,extra='stroke-dasharray="5 4"'))
            o.append(text(hcx,hy+24,"no central team",12,MUTED,anchor="middle",style="italic"))
            o.append(text(hcx,hy+42,"(or a very small one)",11,MUTED,anchor="middle",style="italic"))
        else:
            o.append(rect(hx,hy,hw,hh,fill=c,rx=6))
            o.append(text(hcx,hy+25,"Data team" if i==0 else "Hub",13.5,"#fff","bold",anchor="middle"))
            o.append(text(hcx,hy+44,"all analysts here" if i==0 else "platform · standards",11,"#eef3f8",anchor="middle"))
        for (dx,dy),d in zip(coords,depts):
            o.append(rect(dx,dy,140,62,fill="#fff",stroke=RULE,sw=1.2,rx=6))
            o.append(text(dx+12,dy+24,d,13,INK,"bold"))
            if i>0:
                o.append(f'<circle cx="{dx+22}" cy="{dy+44}" r="7" fill="{c}"/>')
                o.append(text(dx+36,dy+48,"analyst",11.5,MUTED))
        o.append(path(f"M{px+14},{top+372} H{px+PW-14}",stroke=RULE,sw=1))
        o.append(text(px+14,top+400,plus,12.5,GREEN,"bold"))
        o.append(text(px+14,top+426,minus,12.5,RED,"bold"))
        o.append(text(px+14,top+452,note,11.5,MUTED,style="italic"))
    return svg(1040,510,"".join(o))

# ---------- Figure 7.5: one request, every role ----------
def fig_one_request():
    o=[]
    phases=[("1 · Clarify and answer",ACC,[("Business analyst","turns the request into a clear question"),
                                          ("Data analyst","finds the five quiet customers")]),
            ("2 · Share and standardize",ACC,[("BI developer","at-risk page on the sales dashboard"),
                                             ("Analytics engineer","one tested definition of \"active\"")]),
            ("3 · Predict",PURPLE,[("Data scientist","predicts who will go quiet next"),
                                  ("ML engineer","scores every customer each night")]),
            ("4 · Run and act",GREEN,[("Data engineer","fresh, checked data by 6 a.m."),
                                     ("Integration engineer","tasks in the CRM, Monday email"),
                                     ("AI engineer","call brief drafted; rep approves")])]
    CW=226; G=28; x0=30; ytop=120
    o.append(rect(x0,24,4*CW+3*G,62,fill="#fff4e8",stroke=ORANGE,sw=1.6,rx=8))
    o.append(text(x0+16,50,"Data architect",14,ORANGE,"bold",family=HEAD))
    o.append(text(x0+16,72,"Designs how the pieces fit: where the score lives, who owns each definition, who may see what, what it costs.",12,INK))
    for i,(ph,c,cards) in enumerate(phases):
        x=x0+i*(CW+G)
        o.append(text(x,ytop,ph,13.5,c,"bold",family=HEAD))
        yy=ytop+14
        for role,did in cards:
            o.append(rect(x+3,yy+3,CW,74,fill="#e9eef4",rx=7)); o.append(rect(x,yy,CW,74,fill="#fff",stroke=c,sw=1.4,rx=7))
            o.append(text(x+12,yy+26,role,13.5,INK,"bold"))
            words=did.split(); lines=[]; cur=""
            for w_ in words:
                if len((cur+" "+w_).strip())>30: lines.append(cur); cur=w_
                else: cur=(cur+" "+w_).strip()
            lines.append(cur)
            o.append(wrap(x+12,yy+47,lines,12,MUTED,17))
            yy+=88
        if i<3: o.append(arrow(x+CW+2,ytop+50,x+CW+G-2,ytop+50,c=MUTED,sw=2))
    yb=ytop+14+3*88+12
    o.append(rect(x0,yb,4*CW+3*G,50,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(x0+16,yb+21,"Start: Anita asks, \"Some customers seem to have stopped ordering. Which ones, and what should we do?\"",12.5,INK))
    o.append(text(x0+16,yb+40,"End: every Monday, each sales rep knows which customers to call, and why.",12.5,INK,"bold"))
    return svg(1030,yb+68,"".join(o))

# ---------- Figure 7.3: from source to action ----------
def fig_source_to_action():
    o=[]
    stages=[("Sources",MUTED,["Orders (ERP)","Leads (CRM)","Payments","Support tickets"]),
            ("Move and check",GREEN,["Scheduled loads","Quality checks","Warehouse"]),
            ("Shape and predict",PURPLE,["Shared definitions","Risk score","Forecasts"]),
            ("Deliver and act",ACC,["Dashboard","Report in the email body","Task written into the CRM","Alert when a rule trips"])]
    who=["Business systems record it","Data engineer · integration engineer","Analytics engineer · data scientist · ML engineer","Analyst · BI developer · integration engineer · AI engineer"]
    manual=["Export by hand","Copy-paste into one file","Formulas re-typed each week","Emailed attachment; re-keyed into the CRM"]
    W=226; G=28; top=64; h=160
    o.append(text(30,36,"AUTOMATED FLOW",11,MUTED,"bold"))
    for i,(name,c,items) in enumerate(stages):
        x=30+i*(W+G)
        o.append(header_card(x,top,W,h,c,name))
        yy=top+62
        for it in items:
            o.append(f'<circle cx="{x+18}" cy="{yy-4}" r="3.5" fill="{c}"/>'); o.append(text(x+30,yy,it,12.5,INK)); yy+=26
        if i<3: o.append(arrow(x+W+3,top+75,x+W+G-3,top+75,c=INK,sw=2.2))
    # who automates each stage
    yw=top+h+26
    o.append(text(30,yw,"WHO AUTOMATES THIS STAGE",11,MUTED,"bold"))
    for i,wtext in enumerate(who):
        x=30+i*(W+G)
        parts=wtext.split(" · "); lines=[]; cur=""
        for p_ in parts:
            cand=(cur+" · "+p_) if cur else p_
            if len(cand)>30: lines.append(cur); cur=p_
            else: cur=cand
        lines.append(cur)
        o.append(rect(x,yw+10,W,74,fill="#f6f9fc",stroke=RULE,rx=6))
        o.append(wrap(x+12,yw+32,lines,12,INK,18,"bold"))
    ym=yw+112
    o.append(text(30,ym,"THE SAME FLOW DONE BY HAND",11,RED,"bold"))
    for i,m in enumerate(manual):
        x=30+i*(W+G)
        words=m.split(); lines=[]; cur=""
        for w_ in words:
            if len((cur+" "+w_).strip())>28: lines.append(cur); cur=w_
            else: cur=(cur+" "+w_).strip()
        lines.append(cur)
        o.append(rect(x,ym+10,W,58,fill="#fbeaea",stroke="#e3b7b7",rx=6))
        o.append(wrap(x+12,ym+32,lines,12,INK,18))
    return svg(1030,ym+86,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig7-1-four-questions-and-roles.svg",fig_questions),("fig7-2-the-field-as-a-tree.svg",fig_tree),
                    ("fig7-3-source-to-action.svg",fig_source_to_action),
                    ("fig7-4-three-team-structures.svg",fig_teams),("fig7-5-one-request-every-role.svg",fig_one_request)]:
        open(name,"w").write(fn())
    print("ok")
