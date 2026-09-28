# Generates the SVG figures for Chapter 8. Run: python3 make_figs08.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

ROLES=["Data analyst","Business analyst","BI developer","Analytics engineer","Data scientist",
       "ML engineer","Data engineer","AI engineer","Automation / integration","Data architect"]
# 2 = core, 1 = useful, 0 = not needed to get in. Same matrix as section 8.3 and checks/ch08_check.py
SKILLS=[("Business and domain sense",      [2,2,1,1,2,1,1,1,2,2]),
        ("Communication and storytelling", [2,2,1,1,2,1,1,1,1,2]),
        ("Spreadsheets (Excel, Sheets)",   [2,2,1,0,1,0,0,0,2,1]),
        ("SQL",                            [2,1,2,2,2,1,2,1,1,2]),
        ("BI and dashboards",              [2,1,2,1,1,0,0,0,1,1]),
        ("Statistics",                     [1,0,0,0,2,1,0,1,0,0]),
        ("Python",                         [1,0,0,1,2,2,2,2,2,1]),
        ("Spreadsheet and report automation",[1,1,1,0,0,0,0,0,2,0]),
        ("Requirements and process mapping",[1,2,1,1,0,0,0,1,2,2]),
        ("Data modeling (incl. dbt)",      [0,0,2,2,0,0,2,0,0,2]),
        ("Machine learning",               [0,0,0,0,2,2,0,1,0,1]),
        ("Pipelines and orchestration",    [0,0,0,1,0,2,2,1,1,2]),
        ("Cloud and infrastructure",       [0,0,0,1,1,2,2,2,1,2]),
        ("APIs and integration",           [0,0,0,0,0,1,2,2,2,2]),
        ("LLMs and AI applications",       [0,0,0,0,1,1,0,2,1,1]),
        ("Git and version control",        [0,0,1,2,1,2,2,2,1,1]),
        ("System design and governance",   [0,0,0,1,0,1,1,1,1,2])]

CW_=720   # canvas width: prints at 493.2 pt, so 10.5 px = 7.2 pt

def door(x,y,label,c,size=11.5):
    w=max(100,len(label)*size*0.6+32)
    return (rect(x,y,w,28,fill="#fff",stroke=c,sw=1.4,rx=4)+rect(x+6,y+5,9,18,fill=c,rx=1.5)
            +f'<circle cx="{x+13}" cy="{y+14}" r="1.5" fill="#fff"/>'+text(x+22,y+19,label,size,INK)), w

# ---------- Figure 8.1: the career tree as tiers and doors ----------
def fig_tiers():
    o=[]
    tiers=[(6,"Architecture & leadership","Part 7",ORANGE,["Data architect"]),
           (5,"Production ML & AI","Part 6",PURPLE,["ML engineer","AI engineer"]),
           ("3|4",None,None,None,None),
           (2,"Advanced analytics & analytics engineering","Part 3",ACC,["Analytics engineer","BI developer","Senior analyst","RPA developer"]),
           (1,"The analyst core","Part 2",ACC,["Data analyst","Business analyst","BI analyst","Automation analyst"]),
           (0,"Foundations","Parts 0–1",MUTED,["Reporting / MIS assistant"])]
    X=16; W=688; y=16; H=88
    def band(xx,w,num,name,part,c,roles):
        b=[rect(xx,y,w,H,fill="#fbfcfe",stroke=c,sw=1.6,rx=8), rect(xx,y,8,H,fill=c,rx=3),
           text(xx+20,y+20,f"TIER {num} · {part.upper()}",11,c,"bold"),
           text(xx+20,y+40,name,13.5,INK,"bold",family=HEAD)]
        dx=xx+20
        for r in roles:
            d,wd=door(dx,y+50,r,c); b.append(d); dx+=wd+8
        return "".join(b)
    for t in tiers:
        if t[0]=="3|4":
            half=(W-20)/2
            o.append(band(X,half,3,"Data science & ML","Part 4",PURPLE,["Data scientist"]))
            o.append(band(X+half+20,half,4,"Engineering & integration","Part 5",GREEN,["Data engineer","Integration engineer"]))
            o.append(rect(X+half-18,y+H/2-12,56,24,fill="#fff4d6",stroke="#e2c46b",rx=12))
            o.append(text(X+half+10,y+H/2+4,"peers",11.5,INK,"bold",anchor="middle"))
        else:
            num,name,part,c,roles=t
            o.append(band(X,W,num,name,part,c,roles))
        y+=H+10
    o.append(text(X,y+10,"Read from the bottom up. Each role sits at the first tier that makes you a credible",12,MUTED))
    o.append(text(X,y+28,"applicant; you keep every skill below it.",12,MUTED))
    return svg(CW_,y+40,"".join(o))

# ---------- Figure 8.2: skills matrix heatmap ----------
ABBR=["DA","BA","BI","AE","DS","MLE","DE","AIE","AUT","ARC"]
def fig_matrix():
    # core: dark cell with a white filled dot; useful: mid-blue cell with a hollow dot; not needed: blank with a dash.
    # The symbols match the table in section 8.3, so the figure reads in greyscale too.
    o=[]; x0=16; L=212; CW=48; RH=24; top=40
    for j,a in enumerate(ABBR):
        o.append(text(x0+L+j*CW+CW/2,top-12,a,11.5,INK,"bold",anchor="middle"))
    for i,(s,vals) in enumerate(SKILLS):
        yy=top+i*RH
        if i%2==0: o.append(rect(x0,yy,L+10*CW,RH,fill=ROWALT))
        o.append(text(x0+6,yy+16.5,s,11.5,INK))
        for j,v in enumerate(vals):
            cx=x0+L+j*CW; mx=cx+CW/2
            if v==2:
                o.append(rect(cx+5,yy+3,CW-10,RH-6,fill=ACC,rx=4))
                o.append(f'<circle cx="{mx}" cy="{yy+RH/2}" r="4.5" fill="#fff"/>')
            elif v==1:
                o.append(rect(cx+5,yy+3,CW-10,RH-6,fill="#9dbfdc",rx=4))
                o.append(f'<circle cx="{mx}" cy="{yy+RH/2}" r="4" fill="none" stroke="{INK}" stroke-width="1.5"/>')
            else:
                o.append(path(f"M{mx-4},{yy+RH/2} H{mx+4}",stroke=MUTED,sw=1.4))
    yb=top+len(SKILLS)*RH
    o.append(path(f"M{x0},{yb} H{x0+L+10*CW}",stroke=RULE,sw=1))
    ly=yb+28
    def sw(x,kind):
        if kind==2: return rect(x,ly-14,30,18,fill=ACC,rx=4)+f'<circle cx="{x+15}" cy="{ly-5}" r="4.5" fill="#fff"/>'
        if kind==1: return rect(x,ly-14,30,18,fill="#9dbfdc",rx=4)+f'<circle cx="{x+15}" cy="{ly-5}" r="4" fill="none" stroke="{INK}" stroke-width="1.5"/>'
        return rect(x,ly-14,30,18,fill="#fff",stroke=RULE,rx=4)+path(f"M{x+11},{ly-5} H{x+19}",stroke=MUTED,sw=1.4)
    o.append(sw(x0,2)); o.append(text(x0+38,ly,"core: needed to be hired",11.5,INK))
    o.append(sw(x0+215,1)); o.append(text(x0+253,ly,"useful: helps, often a plus",11.5,INK))
    o.append(sw(x0+438,0)); o.append(text(x0+476,ly,"not needed to get in",11.5,INK))
    k1="DA data analyst · BA business analyst · BI BI developer · AE analytics engineer · DS data scientist"
    k2="MLE ML engineer · DE data engineer · AIE AI engineer · AUT automation / integration · ARC data architect"
    o.append(text(x0,ly+26,k1,10.5,MUTED)); o.append(text(x0,ly+42,k2,10.5,MUTED))
    return svg(CW_,ly+54,"".join(o))

# ---------- Figure 8.3: decoding a job description ----------
def fig_jd():
    o=[]
    jx,jy,jw=16,16,404
    lines=[("h","Data Analyst"),("h","(Sales Analytics and Automation)"),
           ("m","Riverstone Supplies · head office, hybrid"),
           ("m","1–3 years (freshers with strong projects considered)"),("s",""),
           ("b","What you'll do"),
           ("t","• Run a weekly at-risk customer list for sales reps"),
           ("t","• Build and maintain the sales dashboard (Power BI)"),
           ("t","• Agree definitions ('active customer') with finance"),
           ("t","• Automate reports, incl. the Daily Sales Flash"),("s",""),
           ("b","Must have"),
           ("t","• SQL: joins, aggregation; window functions a plus"),
           ("t","• Excel or Google Sheets: lookups, pivot tables"),
           ("t","• A BI tool, Power BI preferred"),
           ("t","• Automated a recurring report, with any tool"),
           ("t","• Clear written English"),("s",""),
           ("b","Nice to have"),
           ("t","• Python (pandas) · VBA or Apps Script"),
           ("t","• Forecasting or customer analytics"),
           ("t","• Experience with a CRM or ERP")]
    marks={0:1,3:2,6:3,8:4,11:5,15:6,18:7}
    NH=58; NG=8; notes_h=7*NH+6*NG
    steps={"h":20,"m":17,"b":19,"t":18,"s":7}
    natural=30+sum(steps[k] for k,_ in lines)
    f=(notes_h-30)/(natural-30)          # spread the posting's lines to the height of the notes column
    yy=jy+30; ys={}; body=[]
    for i,(k,t) in enumerate(lines):
        if k=="h": body.append(text(jx+40,yy,t,13.5,ACC,"bold",family=HEAD))
        elif k=="m": body.append(text(jx+40,yy,t,11,MUTED))
        elif k=="b": body.append(text(jx+40,yy,t,12,INK,"bold"))
        elif k=="t": body.append(text(jx+40,yy,t,11,INK))
        if i in marks: ys[marks[i]]=yy
        yy+=steps[k]*f
    h=notes_h
    o.append(rect(jx+3,jy+4,jw,h,fill="#e9eef4",rx=8)); o.append(rect(jx,jy,jw,h,fill="#fff",stroke=RULE,sw=1.4,rx=8))
    o.extend(body)
    notes={1:(ACC,"Title = track + tier",["Analytics & BI, tier 1, with the","automation thread."]),
           2:(GREEN,"A door for freshers",["\"Strong projects\" means a portfolio","can replace experience."]),
           3:(ACC,"Duties are outputs",["At-risk list: Ch 13 · dashboard: Ch 16","· automation: Ch 20."]),
           4:(PURPLE,"Hidden skill",["Agreeing definitions is stakeholder","work: Ch 23–24."]),
           5:(GREEN,"Must-haves = the keys",["These decide the shortlist. Score","yourself on each."]),
           6:(GREEN,"\"With any tool\"",["They care about the result, not a","brand of software."]),
           7:(ORANGE,"Nice-to-haves are not rules",["Apply if you meet the must-haves;","these are tie-breakers."])}
    nx=432; nw=272; ny=jy
    for n in sorted(notes):
        c,title,sub=notes[n]
        y0=ys[n]
        o.append(f'<circle cx="{jx+20}" cy="{y0-4}" r="10" fill="{c}"/>'); o.append(text(jx+20,y0+0.5,str(n),11.5,"#fff","bold",anchor="middle"))
        o.append(rect(nx,ny,nw,NH,fill="#fbfcfe",stroke=c,sw=1.3,rx=6))
        o.append(f'<circle cx="{nx+18}" cy="{ny+18}" r="10" fill="{c}"/>'); o.append(text(nx+18,ny+22.5,str(n),11.5,"#fff","bold",anchor="middle"))
        o.append(text(nx+36,ny+22,title,12,c,"bold"))
        o.append(wrap(nx+36,ny+39,sub,11,INK,14))
        ny+=NH+NG
    return svg(CW_,jy+h+16,"".join(o))

# ---------- Figure 8.4: three entry routes ----------
def fig_routes():
    o=[]
    routes=[("Fresher",ACC,["Degree, course, or","self-study"],["Projects and a","portfolio"],["Internship or","entry analyst role"],
             "Advantage: time to build skills from zero","Obstacle: no work evidence yet"),
            ("Career switcher",PURPLE,["Experience in another","field (finance, sales, ops)"],["Tier 1 keys plus projects","on your own domain"],["Domain analyst role","(e.g. finance analyst)"],
             "Advantage: business context employers value","Obstacle: less time; starting over feels risky"),
            ("Internal move",GREEN,["A job inside a company","(sales, support, ops)"],["Automate your own work;","volunteer analysis"],["Internal opening or","role reshaped around you"],
             "Advantage: people already trust you","Obstacle: being seen as 'only' your old job")]
    y=12; BW=200; G=32; X=16; W=688; LH=110
    for name,c,a,b,d,adv,obs in routes:
        o.append(rect(X,y,W,LH,fill="#fbfcfe",stroke=c,sw=1.5,rx=8))
        o.append(text(X+14,y+24,name,14,c,"bold",family=HEAD))
        xs=[X+14,X+14+BW+G,X+14+2*(BW+G)]
        for k,(xx,lines) in enumerate(zip(xs,[a,b,d])):
            o.append(rect(xx,y+34,BW,46,fill="#fff",stroke=RULE,sw=1.2,rx=6))
            o.append(wrap(xx+10,y+52,lines,11.5,INK,16))
            if k<2: o.append(arrow(xx+BW+3,y+57,xx+BW+G-4,y+57,c=c,sw=2))
        o.append(text(X+14,y+99,"+ "+adv,11.5,GREEN,"bold")); o.append(text(X+344,y+99,"– "+obs,11.5,RED,"bold"))
        y+=LH+8
    return svg(CW_,y+4,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig8-1-career-tree-tiers.svg",fig_tiers),("fig8-2-skills-matrix.svg",fig_matrix),
                    ("fig8-3-decoding-a-job-description.svg",fig_jd),("fig8-4-three-entry-routes.svg",fig_routes)]:
        open(name,"w").write(fn())
    print("ok")
