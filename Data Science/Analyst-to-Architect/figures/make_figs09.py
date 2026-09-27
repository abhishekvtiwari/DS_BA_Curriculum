# Generates the SVG figures for Chapter 9. Run: python3 make_figs09.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

# Farah's 12-week SQL practice log (fictional). Same data as section 9.7 and checks/ch09_check.py
WEEKS=list(range(1,13))
MINUTES=[180,200,210,220,240,260,270,240,240,250,240,250]
CHECK=[3,4,5,6,6,6,6,6,7,8,8,9]   # weekly check: 10 new problems of the same level, solved unaided

# ---------- Figure 9.1: the three ingredients ----------
def fig_ingredients():
    o=[]
    items=[("Study",ACC,["Concepts, examples,","and exercises"],"produces knowledge","\"I understand how a join works.\""),
           ("Projects",GREEN,["Real questions on","real, messy data"],"produces skill","\"I can answer this question with a join.\""),
           ("Feedback and time",PURPLE,["Reviews, mentors, real","users, many repetitions"],"produces judgment","\"I know which join, and when it will mislead.\"")]
    W=300; G=40; y=40; h=210
    for i,(t,c,body,prod,quote) in enumerate(items):
        x=30+i*(W+G)
        o.append(header_card(x,y,W,h,c,t))
        o.append(wrap(x+14,y+62,body,13,INK,20))
        o.append(text(x+14,y+122,prod.upper(),11,c,"bold"))
        o.append(path(f"M{x+14},{y+134} H{x+W-14}",stroke=RULE,sw=1))
        o.append(text(x+14,y+160,quote,12,MUTED,style="italic"))
        if i<2: o.append(arrow(x+W+4,y+105,x+W+G-4,y+105,c=INK,sw=2.2))
    # loop back
    o.append(path(f"M{30+2*(W+G)+W/2},{y+h+4} V{y+h+40} H{30+W/2} V{y+h+12}",stroke=MUTED,sw=2,dash="6 4"))
    o.append(f'<path d="M{30+W/2-6},{y+h+14} L{30+W/2},{y+h+4} L{30+W/2+6},{y+h+14} Z" fill="{MUTED}"/>')
    o.append(text(515,y+h+62,"Feedback shows what to study next. The loop repeats at every tier, for years.",12.5,MUTED,anchor="middle"))
    return svg(1030,y+h+84,"".join(o))

# ---------- Figure 9.2: naive practice vs deliberate practice ----------
def fig_practice():
    o=[]
    rows=[("Goal","\"Do some SQL tonight\"","\"Write a LEFT JOIN that keeps never-ordered customers\""),
          ("Difficulty","What already feels comfortable","Slightly beyond what you can do unaided"),
          ("Attention","Half-watching a video, phone nearby","Full focus for a short, fixed block"),
          ("Feedback","None, or \"it ran, so it's right\"","Compare with a known answer; find why it differs"),
          ("Repetition","Move on after one success","Redo it tomorrow without looking; vary it"),
          ("Record","Nothing written down","A log: what was hard, what to try next")]
    x0=30; c1=150; c2=380; c3=440; top=30; RH=50
    o.append(rect(x0,top,c1+c2+c3,40,fill=INK,rx=6))
    o.append(text(x0+14,top+26,"",13,"#fff","bold"))
    o.append(text(x0+c1+14,top+26,"Naive practice",14,"#ffffff","bold",family=HEAD))
    o.append(text(x0+c1+c2+14,top+26,"Deliberate practice",14,"#ffffff","bold",family=HEAD))
    for i,(k,a,b) in enumerate(rows):
        y=top+40+i*RH
        o.append(rect(x0,y,c1+c2+c3,RH,fill=ROWALT if i%2==0 else "#fff"))
        o.append(text(x0+14,y+30,k,13,INK,"bold"))
        o.append(rect(x0+c1+8,y+10,6,RH-20,fill=RED,rx=2)); o.append(text(x0+c1+24,y+30,a,12.5,INK))
        o.append(rect(x0+c1+c2+8,y+10,6,RH-20,fill=GREEN,rx=2)); o.append(text(x0+c1+c2+24,y+30,b,12.5,INK))
    yb=top+40+len(rows)*RH
    o.append(path(f"M{x0},{yb} H{x0+c1+c2+c3}",stroke=RULE,sw=1))
    o.append(text(x0,yb+26,"Same hours, different results: deliberate practice spends them where you're weakest, and checks every attempt.",12.5,MUTED))
    return svg(1030,yb+44,"".join(o))

# ---------- Figure 9.4: Farah's practice log ----------
def fig_log():
    o=[]; X=90; Y=40; W=860; H=300
    bw=W/12
    maxm=300
    # plateau shading weeks 4-8
    o.append(rect(X+3*bw,Y,5*bw,H,fill="#fff4d6"))
    o.append(text(X+5.5*bw,Y+18,"plateau: score stuck at 6 for five weeks",12,ORANGE,"bold",anchor="middle"))
    # axes
    for m in range(0,301,100):
        yy=Y+H-m/maxm*H
        o.append(path(f"M{X},{yy} H{X+W}",stroke=RULE,sw=1)); o.append(text(X-10,yy+4,str(m),11,MUTED,anchor="end"))
    for s in range(0,11,2):
        yy=Y+H-s/10*H; o.append(text(X+W+10,yy+4,str(s),11,ACC,anchor="start"))
    o.append(f'<text transform="translate(34,{Y+H/2}) rotate(-90)" font-size="12" fill="{MUTED}" text-anchor="middle">Practice minutes per week (bars)</text>')
    o.append(f'<text transform="translate({X+W+46},{Y+H/2}) rotate(90)" font-size="12" fill="{ACC}" text-anchor="middle">Weekly check score out of 10 (line)</text>')
    pts=[]
    for i,(w,m,s) in enumerate(zip(WEEKS,MINUTES,CHECK)):
        bx=X+i*bw; bh=m/maxm*H
        o.append(rect(bx+bw*0.22,Y+H-bh,bw*0.56,bh,fill="#cfd8e3",rx=2))
        o.append(text(bx+bw/2,Y+H+20,f"W{w}",11.5,INK,anchor="middle"))
        pts.append((bx+bw/2,Y+H-s/10*H))
    o.append(path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=ACC,sw=3))
    for (x,y),s in zip(pts,CHECK):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff" stroke="{ACC}" stroke-width="2.5"/>')
        o.append(text(x,y-12,str(s),11.5,ACC,"bold",anchor="middle"))
    ax=X+7.5*bw
    o.append(path(f"M{ax},{Y+H+30} V{Y+H+44}",stroke=GREEN,sw=2))
    o.append(text(ax,Y+H+60,"from week 8: harder problems on her own questions, reviewed weekly",12,GREEN,"bold",anchor="middle"))
    return svg(1030,Y+H+76,"".join(o))

# ---------- Figure 9.3: anatomy of a portfolio piece ----------
def fig_portfolio():
    o=[]
    px,py,pw=30,24,520
    secs=[("The question","Which regular customers have stopped ordering, and what should sales do?"),
          ("The data","Riverstone one-year database, 2025: orders, customers (fictional)"),
          ("The approach","Each customer's usual gap between orders vs days since last order"),
          ("The result","Two regular customers silent for over five months; table and chart"),
          ("The check","Hand-checked one customer; totals reconciled to annual revenue"),
          ("The decision","Call both this week; send the list to reps every Monday"),
          ("What I'd do next","Automate the Monday email; add payment delays as a signal")]
    y=py+50
    o.append(rect(px+3,py+4,pw,len(secs)*62+62,fill="#e9eef4",rx=8))
    o.append(rect(px,py,pw,len(secs)*62+62,fill="#fff",stroke=RULE,sw=1.4,rx=8))
    o.append(text(px+18,py+32,"At-risk customers: a one-page write-up",15,ACC,"bold",family=HEAD))
    cols=[ACC,ACC,ACC,GREEN,GREEN,ORANGE,PURPLE]
    ys=[]
    for (h,b),c in zip(secs,cols):
        o.append(rect(px+18,y,5,44,fill=c,rx=2))
        o.append(text(px+34,y+16,h,13,INK,"bold"))
        words=b.split(); lines=[]; cur=""
        for w_ in words:
            if len((cur+" "+w_).strip())>62: lines.append(cur); cur=w_
            else: cur=(cur+" "+w_).strip()
        lines.append(cur)
        o.append(wrap(px+34,y+34,lines,12,MUTED,16))
        ys.append(y+22); y+=62
    notes=[(0,ACC,"Start with the business question","Not with the tool you used."),
           (3,GREEN,"Show the result a manager reads","One table or chart, clearly labeled."),
           (4,GREEN,"Show that you checked it","This is what separates you from copy-paste."),
           (5,ORANGE,"End in a decision","Every technique ends in something someone can do."),
           (6,PURPLE,"Say what you'd improve","It shows judgment, and invites the interview question.")]
    nx=610
    for idx,c,t,s in notes:
        ny=ys[idx]-24
        o.append(rect(nx,ny,400,50,fill="#fbfcfe",stroke=c,sw=1.3,rx=6))
        o.append(text(nx+14,ny+21,t,13,c,"bold")); o.append(text(nx+14,ny+40,s,12,INK))
        o.append(path(f"M{px+pw+4},{ys[idx]} H{nx-4}",stroke=c,sw=1.4,dash="4 3"))
    return svg(1040,py+len(secs)*62+86,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig9-1-three-ingredients.svg",fig_ingredients),("fig9-2-naive-vs-deliberate-practice.svg",fig_practice),
                    ("fig9-3-anatomy-of-a-portfolio-piece.svg",fig_portfolio),("fig9-4-practice-log-plateau.svg",fig_log)]:
        open(name,"w").write(fn())
    print("ok")
