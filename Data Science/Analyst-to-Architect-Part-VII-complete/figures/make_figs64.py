# Diagrams for Chapter 64. Run: python3 make_figs64.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; GOLD="#b7791f"; RED="#b23b3b"; SOFT="#eef2f7"; LIGHT="#dfe5ec"; BLUE2="#2f6690"
def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6,dash=None):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw,dash=dash)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'
def box(x,y,w,h,title,c,lines=(),size=10.2):
    o=[rect(x+3,y+4,w,h,fill=SOFT,rx=7), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=7)]
    o.append(f'<path d="M{x},{y+8} a7,7 0 0 1 7,-7 H{x+w-7} a7,7 0 0 1 7,7 V{y+24} H{x} Z" fill="{c}"/>')
    o.append(text(x+w/2,y+16.5,title,10,"#fff","bold",anchor="middle",family=HEAD))
    for i,l in enumerate(lines): o.append(text(x+w/2,y+40+i*14,l,size-1.2,INK,anchor="middle"))
    return "".join(o)

def f1():  # RBAC access model closing Ch60's open risk
    o=[text(30,30,"Closing Chapter 60's open risk: an access-control model, by role",14.5,INK,"bold",family=HEAD)]
    roles=["Branch\nstaff","Regional\nmanager","Analytics\nteam","Data platform\nteam","External\nauditor"]
    resources=["Own branch\norders","All-branch\nrevenue","Customer\nPII","Model\ntraining data","Credential\nvault"]
    x0,y0,cw,rh=230,70,150,42
    for i,r in enumerate(resources): o.append(text(x0+i*cw+cw/2,y0-14,r,9.6,MUTED,"bold",anchor="middle"))
    for j,role in enumerate(roles):
        o.append(text(190,y0+j*rh+rh/2+14,role,9.8,INK,"bold",anchor="end"))
    # access grid: 1=own only,2=read,3=full,0=none
    grid=[[3,0,0,0,0],[3,2,0,0,0],[2,2,2,2,0],[2,2,2,3,2],[1,1,1,0,0]]
    labels={0:("none",MUTED),1:("audit\nonly",GOLD),2:("read",ACC),3:("full",GREEN)}
    for j,row in enumerate(grid):
        for i,val in enumerate(row):
            cx,cy=x0+i*cw+cw/2,y0+j*rh+rh/2
            lab,c=labels[val]
            o.append(rect(x0+i*cw+4,y0+j*rh+4,cw-8,rh-8,fill="#fff",stroke=c,sw=1.4,rx=5))
            o.append(text(cx,cy+4,lab,9,c,"bold",anchor="middle"))
    o.append(text(30,y0+5*rh+40,"Least privilege in one table: branch staff see only their own orders; only the platform team and an audited process reach the credential vault.",11.2,MUTED))
    o.append(text(30,y0+5*rh+58,"Customer PII is read-only even for regional managers — a specific, checkable answer to \"who can see what,\" not a policy document nobody consults.",11.2,MUTED))
    return svg(1010,y0+5*rh+80,"".join(o))

def f2():  # privacy by design pillars
    o=[text(30,30,"Privacy by design: four habits, built in from the start",14.5,INK,"bold",family=HEAD)]
    items=[("Data\nminimization","Collect only what the\nfeature actually needs",ACC,"Lead scoring uses order\nhistory, not browsing data"),
          ("Purpose\nlimitation","Data collected for one\nreason isn't reused for\nanother without new consent",GREEN,"Support tickets aren't fed\ninto marketing scoring"),
          ("Sensible\nretention","Keep data only as long\nas it's actually needed",GOLD,"Raw PO emails purged 90\ndays after order confirmed"),
          ("Anonymization /\npseudonymization","Strip or mask identity\nwhen the analysis doesn't\nneed it",PURPLE,"Ch 56 drift monitoring\nuses hashed customer IDs")]
    for i,(name,desc,c,ex) in enumerate(items):
        x=30+i*245
        o.append(box(x,60,225,140,name,c,desc.split("\n"),9.8))
        o.append(rect(x,206,225,50,fill="#f3f6fa",rx=6))
        for j,l in enumerate(ex.split("\n")): o.append(text(x+112,224+j*15,l,9.2,MUTED,anchor="middle"))
    o.append(text(30,285,"Each of these costs a little convenience today and removes a whole category of future incident, audit finding, or regulatory exposure.",11.3,MUTED))
    return svg(1010,304,"".join(o))

def f3():  # model governance / audit trail loop
    o=[text(30,30,"Model governance: a loop, not a one-time approval",14.5,INK,"bold",family=HEAD)]
    stages=[("Version &\nregister",ACC,"every model gets an ID,\na training-data snapshot"),
           ("Approve\nfor production",GOLD,"a person signs off,\nseparate from the builder"),
           ("Monitor in\nproduction",GREEN,"drift, fairness, and\nperformance, on a schedule"),
           ("Audit\ntrail",PURPLE,"every prediction traceable\nto a model version"),
           ("Retrain or\nretire",RED,"a decision, not\nneglect (Ch 63)")]
    cx,cy,R=505,220,150
    import math
    for i,(name,c,sub) in enumerate(stages):
        ang=math.radians(-90+i*72)
        x,y=cx+R*math.cos(ang),cy+R*math.sin(ang)
        o.append(box(x-90,y-45,180,90,name,c,sub.split(", "),9.4))
    for i in range(5):
        a1=math.radians(-90+i*72+18); a2=math.radians(-90+(i+1)*72-18)
        x1,y1=cx+(R-10)*math.cos(a1),cy+(R-10)*math.sin(a1)
        x2,y2=cx+(R-10)*math.cos(a2),cy+(R-10)*math.sin(a2)
        o.append(arrow(x1,y1,x2,y2,MUTED,1.4))
    o.append(text(cx,cy,"Chapter 56's\nMLOps loop,\ngoverned",10.5,INK,"bold",anchor="middle"))
    o.append(text(30,430,"Every stage produces a record. \"Which model made this decision, and who approved it\" should always have a one-query answer.",11.3,MUTED))
    return svg(1010,450,"".join(o))

if __name__ == "__main__":
    for n,f in [("fig64-1-access-model.svg",f1),("fig64-2-privacy-by-design.svg",f2),
                ("fig64-4-model-governance.svg",f3)]:
        open(n,"w").write(f())
    print("ok")
