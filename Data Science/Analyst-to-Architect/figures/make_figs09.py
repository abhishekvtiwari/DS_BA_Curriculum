# Generates the SVG figures for Chapter 9. Run: python3 make_figs09.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas
# prints at s * 493.2 / W pt. Canvases here are 720-780 px and the smallest font is 11 px (>= 7 pt).
import math
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

# Farah's 12-week SQL practice log (fictional). Same data as section 9.7 and checks/ch09_check.py
WEEKS=list(range(1,13))
MINUTES=[180,200,210,220,240,260,270,240,240,250,240,250]
CHECK=[3,4,5,6,6,6,6,6,7,8,8,9]   # weekly check: 10 new problems of the same level, solved unaided
PLATEAU=(5,8)                      # weeks 5-8: the score stays at week 4's 6

# ---------- local helpers (kept here so other chapters' scripts can change theirs freely) ----------
def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.45), y2-L*math.sin(a-0.45)); p2=(x2-L*math.cos(a+0.45), y2-L*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def header_card(x,y,w,h,c,title,tsize=15):
    return "".join([rect(x+3,y+4,w,h,fill="#e9eef4",rx=8), rect(x,y,w,h,fill="#fff",stroke=c,sw=1.6,rx=8),
        f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+34} H{x} Z" fill="{c}"/>',
        text(x+12,y+23,title,tsize,"#fff","bold",family=HEAD)])

def lines_at(x,y,lines,size,fill,lh,**kw):
    return "".join(text(x,y+i*lh,l,size,fill,**kw) for i,l in enumerate(lines))

def wrapwords(s,n):
    out=[]; cur=""
    for w in s.split():
        if len((cur+" "+w).strip())>n: out.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
    out.append(cur); return out

# ---------- Figure 9.1: the three ingredients ----------
def fig_ingredients():
    o=[]
    items=[("Study",ACC,["Concepts, examples","and exercises"],"produces knowledge",["“I understand how","a join works.”"]),
           ("Projects",GREEN,["Real questions on","real, messy data"],"produces skill",["“I can answer this","question with a join.”"]),
           ("Feedback and time",PURPLE,["Reviews, mentors,","real users, many","repetitions"],"produces judgment",["“I know which join, and","when it will mislead.”"])]
    W=220; G=30; x0=20; y=20; h=206
    for i,(t,c,body,prod,quote) in enumerate(items):
        x=x0+i*(W+G)
        o.append(header_card(x,y,W,h,c,t))
        o.append(lines_at(x+14,y+58,body,12.5,INK,18))
        o.append(text(x+14,y+130,prod.upper(),11.5,c,"bold"))
        o.append(path(f"M{x+14},{y+141} H{x+W-14}",stroke=RULE,sw=1))
        o.append(lines_at(x+14,y+164,quote,12,MUTED,17,style="italic"))
        if i<2: o.append(arrow(x+W+3,y+100,x+W+G-3,y+100,c=INK,sw=2.2))
    # loop back from feedback to study
    c1=x0+W/2; c3=x0+2*(W+G)+W/2
    o.append(path(f"M{c3},{y+h+4} V{y+h+34} H{c1} V{y+h+14}",stroke=MUTED,sw=2,dash="6 4"))
    o.append(f'<path d="M{c1-6},{y+h+15} L{c1},{y+h+5} L{c1+6},{y+h+15} Z" fill="{MUTED}"/>')
    o.append(text(380,y+h+58,"Feedback shows what to study next. The loop repeats at every tier, for years.",12.5,MUTED,anchor="middle"))
    return svg(760,y+h+72,"".join(o))

# ---------- Figure 9.2: naive practice vs deliberate practice ----------
def fig_practice():
    o=[]
    rows=[("Goal",["“Do some SQL tonight”"],["“Build a monthly total of your spending log","and check it against the sum of every row”"]),
          ("Difficulty",["What already feels comfortable"],["Slightly beyond what you can do unaided"]),
          ("Attention",["Half-watching a video,","phone nearby"],["Full focus for a short, fixed block"]),
          ("Feedback",["None, or “it ran, so it’s right”"],["Compare with a known answer; find why it differs"]),
          ("Repetition",["Move on after one success"],["Redo it tomorrow without looking; vary it"]),
          ("Record",["Nothing written down"],["A log: what was hard, what to try next"])]
    x0=20; c1=108; c2=270; c3=382; top=16; RH=54; TW=c1+c2+c3
    o.append(rect(x0,top,TW,38,fill=INK,rx=6))
    o.append(text(x0+c1+14,top+25,"Naive practice",14,"#ffffff","bold",family=HEAD))
    o.append(text(x0+c1+c2+14,top+25,"Deliberate practice",14,"#ffffff","bold",family=HEAD))
    for i,(k,a,b) in enumerate(rows):
        y=top+38+i*RH
        o.append(rect(x0,y,TW,RH,fill=ROWALT if i%2==0 else "#fff"))
        o.append(text(x0+12,y+32,k,12.5,INK,"bold"))
        for (cx,col,ls) in ((x0+c1,RED,a),(x0+c1+c2,GREEN,b)):
            o.append(rect(cx+8,y+10,5,RH-20,fill=col,rx=2))
            y0=y+32 if len(ls)==1 else y+24
            o.append(lines_at(cx+22,y0,ls,12,INK,17))
    yb=top+38+len(rows)*RH
    o.append(path(f"M{x0},{yb} H{x0+TW}",stroke=RULE,sw=1))
    o.append(lines_at(x0,yb+24,["Same hours, different results: deliberate practice spends them where you’re weakest,",
                                "and checks every attempt."],12,MUTED,17))
    return svg(800,yb+50,"".join(o))

# ---------- Figure 9.3: anatomy of a portfolio piece ----------
def fig_portfolio():
    o=[]
    px,py,pw=16,16,450; P=70
    secs=[("The question","Which regular customers have stopped ordering, and what should sales do?"),
          ("The data","Riverstone one-year database, 2025: orders, customers (fictional)"),
          ("The approach","Each customer's usual gap between orders vs days since last order"),
          ("The result","Two regular customers silent for over five months; table and chart"),
          ("The check","Hand-checked one customer; totals reconciled to annual revenue"),
          ("The decision","Call both this week; send the list to reps every Monday"),
          ("What I'd do next","Automate the Monday email; add payment delays as a signal")]
    ph=64+len(secs)*P
    o.append(rect(px+3,py+4,pw,ph,fill="#e9eef4",rx=8))
    o.append(rect(px,py,pw,ph,fill="#fff",stroke=RULE,sw=1.4,rx=8))
    o.append(text(px+18,py+34,"At-risk customers: a one-page write-up",15,ACC,"bold",family=HEAD))
    cols=[ACC,ACC,ACC,GREEN,GREEN,ORANGE,PURPLE]
    y=py+56; ys=[]
    for (h,b),c in zip(secs,cols):
        o.append(rect(px+18,y,5,52,fill=c,rx=2))
        o.append(text(px+34,y+15,h,13,INK,"bold"))
        o.append(lines_at(px+34,y+33,wrapwords(b,52),12,MUTED,16))
        ys.append(y+26); y+=P
    notes=[(0,ACC,"Start with the business question",["Not with the tool you used."]),
           (3,GREEN,"Show the result a manager reads",["One table or chart, clearly labeled."]),
           (4,GREEN,"Show that you checked it",["This is what separates you","from copy-paste."]),
           (5,ORANGE,"End in a decision",["Every technique ends in","something someone can do."]),
           (6,PURPLE,"Say what you’d improve",["It shows judgment, and invites","the interview question."])]
    nx=490; nw=276; nh=62
    for idx,c,t,s in notes:
        ny=ys[idx]-nh/2
        o.append(rect(nx,ny,nw,nh,fill="#fbfcfe",stroke=c,sw=1.3,rx=6))
        o.append(text(nx+12,ny+20,t,12.5,c,"bold"))
        o.append(lines_at(nx+12,ny+38,s,11.5,INK,15))
        o.append(path(f"M{px+pw+4},{ys[idx]} H{nx-4}",stroke=c,sw=1.4,dash="4 3"))
    return svg(780,py+ph+20,"".join(o))

# ---------- Figure 9.4: Farah's practice log ----------
def fig_log():
    o=[]; X=62; Y=54; W=600; H=250
    bw=W/12; maxm=350
    # axis titles, horizontal, at the top
    o.append(text(X-50,Y-30,"Bars: practice minutes per week",12,MUTED,"bold"))
    o.append(text(X+W+46,Y-30,"Line: weekly check score (out of 10)",12,ACC,"bold",anchor="end"))
    o.append(text(X-50,Y-12,"minutes",11,MUTED))
    o.append(text(X+W+46,Y-12,"score",11,ACC,anchor="end"))
    # plateau shading: weeks 5-8
    a,b=PLATEAU
    o.append(rect(X+(a-1)*bw,Y,(b-a+1)*bw,H,fill="#fff4d6"))
    o.append(text(X+(a-1+(b-a+1)/2)*bw,Y+17,f"Plateau, weeks {a}–{b}:",12,ORANGE,"bold",anchor="middle"))
    o.append(text(X+(a-1+(b-a+1)/2)*bw,Y+33,"score stuck at 6",12,ORANGE,"bold",anchor="middle"))
    # gridlines and ticks
    for m in range(0,301,100):
        yy=Y+H-m/maxm*H
        o.append(path(f"M{X},{yy} H{X+W}",stroke=RULE,sw=1)); o.append(text(X-8,yy+4,str(m),11,MUTED,anchor="end"))
    for s in range(0,11,2):
        yy=Y+H-s/10*H; o.append(text(X+W+8,yy+4,str(s),11,ACC,anchor="start"))
    pts=[]
    for i,(w,m,s) in enumerate(zip(WEEKS,MINUTES,CHECK)):
        bx=X+i*bw; bh=m/maxm*H
        o.append(rect(bx+bw*0.2,Y+H-bh,bw*0.6,bh,fill="#cfd8e3",rx=2))
        o.append(text(bx+bw/2,Y+H+18,f"W{w}",11.5,INK,anchor="middle"))
        pts.append((bx+bw/2,Y+H-s/10*H))
    o.append(path("M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts),stroke=ACC,sw=3))
    for (x,y),s in zip(pts,CHECK):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff" stroke="{ACC}" stroke-width="2.5"/>')
        o.append(text(x,y-11,str(s),11.5,ACC,"bold",anchor="middle"))
    ax=X+7.5*bw
    o.append(path(f"M{ax},{Y+H+26} V{Y+H+38}",stroke=GREEN,sw=2))
    o.append(text(ax,Y+H+54,"From week 8: harder problems on her own questions, reviewed weekly",12,GREEN,"bold",anchor="middle"))
    return svg(720,Y+H+68,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig9-1-three-ingredients.svg",fig_ingredients),("fig9-2-naive-vs-deliberate-practice.svg",fig_practice),
                    ("fig9-3-anatomy-of-a-portfolio-piece.svg",fig_portfolio),("fig9-4-practice-log-plateau.svg",fig_log)]:
        open(name,"w",encoding="utf-8").write(fn())
    print("ok")
