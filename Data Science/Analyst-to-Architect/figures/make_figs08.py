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

def door(x,y,label,c):
    w=max(118,len(label)*7.3+34)
    return (rect(x,y,w,30,fill="#fff",stroke=c,sw=1.4,rx=4)+rect(x+6,y+6,10,18,fill=c,rx=1.5)
            +f'<circle cx="{x+14}" cy="{y+15}" r="1.6" fill="#fff"/>'+text(x+24,y+20,label,12,INK)), w

# ---------- Figure 8.1: the career tree as tiers and doors ----------
def fig_tiers():
    o=[]
    tiers=[(6,"Architecture & leadership","Part VII",ORANGE,["Data architect"]),
           (5,"Production ML & AI","Part VI",PURPLE,["ML engineer","AI engineer"]),
           ("3|4",None,None,None,None),
           (2,"Advanced analytics & analytics engineering","Part III",ACC,["Analytics engineer","BI developer","Senior analyst","RPA developer"]),
           (1,"The analyst core","Part II",ACC,["Data analyst","Business analyst","BI analyst","Automation analyst"]),
           (0,"Foundations","Parts 0–I",MUTED,["Reporting / MIS assistant"])]
    X=30; W=980; y=24; H=96
    for t in tiers:
        if t[0]=="3|4":
            half=(W-20)/2
            for k,(num,name,part,c,roles) in enumerate([(3,"Data science & ML","Part IV",PURPLE,["Data scientist"]),
                                                       (4,"Engineering & integration","Part V",GREEN,["Data engineer","Integration engineer"])]):
                xx=X+k*(half+20)
                o.append(rect(xx,y,half,H,fill="#fbfcfe",stroke=c,sw=1.6,rx=8))
                o.append(rect(xx,y,8,H,fill=c,rx=3))
                o.append(text(xx+22,y+26,f"TIER {num}",11,c,"bold"))
                o.append(text(xx+82,y+26,name,14.5,INK,"bold",family=HEAD))
                o.append(text(xx+half-14,y+26,part,11.5,MUTED,anchor="end",style="italic"))
                dx=xx+22
                for r in roles:
                    d,w=door(dx,y+46,r,c); o.append(d); dx+=w+10
            o.append(rect(X+half-18,y+H/2-13,56,26,fill="#fff4d6",stroke="#e2c46b",rx=13))
            o.append(text(X+half+10,y+H/2+5,"peers",11.5,INK,"bold",anchor="middle"))
        else:
            num,name,part,c,roles=t
            o.append(rect(X,y,W,H,fill="#fbfcfe",stroke=c,sw=1.6,rx=8))
            o.append(rect(X,y,8,H,fill=c,rx=3))
            o.append(text(X+22,y+26,f"TIER {num}",11,c,"bold"))
            o.append(text(X+82,y+26,name,14.5,INK,"bold",family=HEAD))
            o.append(text(X+W-14,y+26,part,11.5,MUTED,anchor="end",style="italic"))
            dx=X+22
            for r in roles:
                d,w=door(dx,y+46,r,c); o.append(d); dx+=w+10
        y+=H+14
    o.append(text(X,y+8,"Read from the bottom up. Each role sits at the first tier that makes you a credible applicant; you keep every skill below it.",12.5,MUTED))
    return svg(1040,y+26,"".join(o))

# ---------- Figure 8.2: skills matrix heatmap ----------
def fig_matrix():
    o=[]; L=240; CW=66; RH=27; top=150; x0=30
    for j,r in enumerate(ROLES):
        cx=x0+L+j*CW+CW/2
        o.append(f'<text transform="translate({cx+4},{top-10}) rotate(-45)" font-size="12" fill="{INK}" font-weight="bold">{r}</text>')
    for i,(s,vals) in enumerate(SKILLS):
        yy=top+i*RH
        if i%2==0: o.append(rect(x0,yy,L+10*CW,RH,fill=ROWALT))
        o.append(text(x0+8,yy+18,s,12.5,INK))
        for j,v in enumerate(vals):
            cx=x0+L+j*CW
            if v==2: o.append(rect(cx+6,yy+4,CW-12,RH-8,fill=ACC,rx=4))
            elif v==1: o.append(rect(cx+6,yy+4,CW-12,RH-8,fill="#cfe0ee",rx=4))
    yb=top+len(SKILLS)*RH
    o.append(path(f"M{x0},{yb} H{x0+L+10*CW}",stroke=RULE,sw=1))
    ly=yb+30
    o.append(rect(x0,ly-14,34,18,fill=ACC,rx=4)); o.append(text(x0+44,ly,"core: needed to be hired",12.5,INK))
    o.append(rect(x0+260,ly-14,34,18,fill="#cfe0ee",rx=4)); o.append(text(x0+304,ly,"useful: helps, often asked as a plus",12.5,INK))
    o.append(rect(x0+600,ly-14,34,18,fill="#fff",stroke=RULE,rx=4)); o.append(text(x0+644,ly,"not needed to get in",12.5,INK))
    return svg(1040,ly+22,"".join(o))

# ---------- Figure 8.3: decoding a job description ----------
def fig_jd():
    o=[]
    jx,jy,jw=30,24,540
    lines=[("h","Data Analyst (Sales Analytics and Automation)"),
           ("m","Riverstone Supplies · head office, hybrid · 1–3 years"),
           ("m","(freshers with strong projects considered)"),("s",""),
           ("b","What you'll do"),
           ("t","• Run a weekly at-risk customer list for sales reps"),
           ("t","• Build and maintain the sales dashboard (Power BI)"),
           ("t","• Agree definitions like 'active customer' with finance"),
           ("t","• Automate recurring reports, incl. the Daily Sales Flash"),("s",""),
           ("b","Must have"),
           ("t","• SQL: joins, aggregation; window functions a plus"),
           ("t","• Excel or Google Sheets: lookups, pivot tables"),
           ("t","• A BI tool, Power BI preferred"),
           ("t","• Automated a recurring report, with any tool"),
           ("t","• Clear written English"),("s",""),
           ("b","Nice to have"),
           ("t","• Python (pandas) · VBA or Apps Script"),
           ("t","• Forecasting or customer analytics · CRM experience")]
    marks={0:1,2:2,5:3,7:4,10:5,14:6,17:7}
    yy=jy+36; ys={}
    body=[]
    for i,(k,t) in enumerate(lines):
        if k=="h": body.append(text(jx+46,yy,t,15.5,ACC,"bold",family=HEAD)); yy+=24
        elif k=="m": body.append(text(jx+46,yy,t,12,MUTED)); yy+=19
        elif k=="b": body.append(text(jx+46,yy,t,13,INK,"bold")); yy+=21
        elif k=="t": body.append(text(jx+46,yy,t,12.3,INK)); yy+=20
        else: yy+=8
        if i in marks: ys[marks[i]]=yy-(24 if k=="h" else 20 if k in "tb" else 19)
    h=yy-jy+6
    o.append(rect(jx+3,jy+4,jw,h,fill="#e9eef4",rx=8)); o.append(rect(jx,jy,jw,h,fill="#fff",stroke=RULE,sw=1.4,rx=8))
    o.extend(body)
    notes={1:(ACC,"Title = track + tier","Analytics & BI, tier 1, with the automation thread."),
           2:(GREEN,"A door for freshers","\"Strong projects\" means a portfolio can replace experience."),
           3:(ACC,"Duties are outputs","At-risk list: Ch 13 · dashboard: Ch 16 · automation: Ch 20."),
           4:(PURPLE,"Hidden skill","Agreeing definitions is stakeholder work: Ch 23–24."),
           5:(GREEN,"Must-haves = the keys","These decide the shortlist. Score yourself on each."),
           6:(GREEN,"\"With any tool\"","They care about the result, not a brand of software."),
           7:(ORANGE,"Nice-to-haves are not rules","Apply if you meet the must-haves; these are tie-breakers.")}
    nx=600; ny=jy+10
    for n in sorted(notes):
        c,title,sub=notes[n]
        y0=ys[n]
        o.append(f'<circle cx="{jx+24}" cy="{y0-4}" r="11" fill="{c}"/>'); o.append(text(jx+24,y0+0.5,str(n),12,"#fff","bold",anchor="middle"))
        o.append(rect(nx,ny,410,56,fill="#fbfcfe",stroke=c,sw=1.3,rx=6))
        o.append(f'<circle cx="{nx+20}" cy="{ny+20}" r="11" fill="{c}"/>'); o.append(text(nx+20,ny+24.5,str(n),12,"#fff","bold",anchor="middle"))
        o.append(text(nx+40,ny+24,title,13,c,"bold")); o.append(text(nx+40,ny+44,sub,11.5,INK))
        ny+=64
    return svg(1040,max(jy+h,ny)+20,"".join(o))

# ---------- Figure 8.4: three entry routes ----------
def fig_routes():
    o=[]
    routes=[("Fresher",ACC,["Degree, course, or","self-study"],["Projects and a","portfolio"],["Internship or","entry analyst role"],
             "Advantage: time to build skills from zero","Obstacle: no work evidence yet"),
            ("Career switcher",PURPLE,["Experience in another","field (finance, sales, ops)"],["Tier 1 keys plus projects","on your own domain"],["Domain analyst role","(e.g. finance analyst)"],
             "Advantage: business context employers value","Obstacle: less time; starting over feels risky"),
            ("Internal move",GREEN,["A job inside a company","(sales, support, ops)"],["Automate your own work;","volunteer analysis"],["Internal opening or","role reshaped around you"],
             "Advantage: people already trust you","Obstacle: being seen as 'only' your old job")]
    y=24; BW=250; G=46
    for name,c,a,b,d,adv,obs in routes:
        o.append(rect(30,y,980,132,fill="#fbfcfe",stroke=c,sw=1.5,rx=8))
        o.append(text(48,y+30,name,15,c,"bold",family=HEAD))
        xs=[48,48+BW+G,48+2*(BW+G)]
        for k,(xx,lines) in enumerate(zip(xs,[a,b,d])):
            o.append(rect(xx,y+44,BW,52,fill="#fff",stroke=RULE,sw=1.2,rx=6))
            o.append(wrap(xx+12,y+65,lines,12.3,INK,18))
            if k<2: o.append(arrow(xx+BW+4,y+70,xx+BW+G-6,y+70,c=c,sw=2))
        o.append(text(48,y+118,adv,12,GREEN,"bold")); o.append(text(530,y+118,obs,12,RED,"bold"))
        y+=148
    o.append(text(30,y+6,"All three routes end at the same tier 1 door. What differs is the evidence you bring to it.",12.5,MUTED))
    return svg(1040,y+24,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig8-1-career-tree-tiers.svg",fig_tiers),("fig8-2-skills-matrix.svg",fig_matrix),
                    ("fig8-3-decoding-a-job-description.svg",fig_jd),("fig8-4-three-entry-routes.svg",fig_routes)]:
        open(name,"w").write(fn())
    print("ok")
