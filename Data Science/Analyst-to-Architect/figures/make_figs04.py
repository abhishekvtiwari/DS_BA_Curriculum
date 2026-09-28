# Generates the SVG figures for Chapter 4. Run: python3 make_figs04.py
# Numbers come from the one-year database (riverstone_2025), the same runs as checks/ch04_check.py.
# Redrawn 28 Sep 2026 (visual findings V4.1-V4.4): every canvas is 720 px wide, so a font of s px
# prints at s x 493.2 / 720 = 0.685 s pt; the smallest text here is 12 px (8.2 pt). Rupee amounts of
# a lakh or more use Indian grouping (option pick 67.9).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"
W_CANVAS = 720

def lakh(n) -> str:
    """Indian digit grouping for rupee amounts: 4335471 -> '43,35,471'."""
    n = str(n).replace(',', ''); i, _, d = n.partition('.')
    if len(i) <= 3: out = i
    else:
        head, tail = i[:-3], i[-3:]
        out = ','.join([head[max(0, k-2):k] for k in range(len(head), 0, -2)][::-1]) + ',' + tail
    return out + ('.' + d if d else '')

def rs(v): return "₹" + lakh(v)

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.4), y2-L*math.sin(a-0.4)); p2=(x2-L*math.cos(a+0.4), y2-L*math.sin(a+0.4))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 4.1: percent changes don't cancel ----------
def fig_asym():
    o=[]; base=320; scale=1.5  # px per rupee
    def panel(x0,title,steps,col):
        o.append(text(x0,28,title,15,INK,"bold",family=HEAD))
        bw=66; gap=38
        for i,(label,v,note) in enumerate(steps):
            x=x0+i*(bw+gap); h=v*scale
            fill = GREY if i==0 else col
            o.append(rect(x,base-h,bw,h,fill=fill,rx=4))
            o.append(text(x+bw/2,base-h-9,f"₹{v:g}",15,INK,"bold",anchor="middle"))
            o.append(text(x+bw/2,base+20,label,12.5,MUTED,anchor="middle"))
            if i>0:
                o.append(arrow(x-gap+4,base-steps[i-1][1]*scale-26,x-4,base-h-26,c=col))
                o.append(text(x-gap/2,base-max(steps[i-1][1],v)*scale-44,note,13,col,"bold",anchor="middle"))
        o.append(path(f"M{x0-8},{base} H{x0+3*bw+2*gap+8}",stroke=RULE,sw=1.2))
    panel(24,"Up 50%, then down 50%",[("start",100,""),("after +50%",150,"+50% of 100"),("after −50%",75,"−50% of 150")],ACC)
    panel(386,"Down 20%, then up 20%",[("start",100,""),("after −20%",80,"−20% of 100"),("after +20%",96,"+20% of 80")],ORANGE)
    o.append(text(24,368,"Each percentage is taken of a different starting number,",13,MUTED,style="italic"))
    o.append(text(24,387,"so equal-looking rises and falls don't cancel out.",13,MUTED,style="italic"))
    return svg(W_CANVAS,402,"".join(o))

# ---------- Figure 4.2: bumpy real growth vs two smooth paths ----------
REV=[202640,253664,278008,210282,329359,186928,232692,329282,558315,681071,633408,439824]
MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def fig_growth():
    o=[]; X0=84; Y0=400; W=470; Hh=300; vmax=800000
    def X(i): return X0+i*W/11
    def Y(v): return Y0-v/vmax*Hh
    for v in range(0,800001,200000):
        o.append(path(f"M{X0},{Y(v)} H{X0+W}",stroke="#eef1f5",sw=1))
        o.append(text(X0-10,Y(v)+4,rs(v),12,MUTED,anchor="end"))
    for i,m in enumerate(MONTHS): o.append(text(X(i),Y0+20,m,12,MUTED,anchor="middle"))
    avg=[REV[0]*1.1307**i for i in range(12)]
    cmp_=[REV[0]*(REV[11]/REV[0])**(i/11) for i in range(12)]
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(avg)),stroke=RED,sw=2.4,dash="8 5"))
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(cmp_)),stroke=GREEN,sw=2.6,dash="2 3"))
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(REV)),stroke=ACC,sw=3))
    for i,v in enumerate(REV): o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{ACC}"/>')
    # direct labels at the right-hand end of each path (no colour words needed)
    xe=X(11)+10
    o.append(text(xe,Y(avg[11])+0,"13.1% average path",12.5,RED,"bold"))
    o.append(text(xe,Y(avg[11])+17,"ends at "+rs(782621),12.5,RED))
    o.append(text(xe,Y(REV[11])-8,"Actual December,",12.5,INK,"bold"))
    o.append(text(xe,Y(REV[11])+9,"where the 7.3%",12.5,GREEN,"bold"))
    o.append(text(xe,Y(REV[11])+26,"compound path ends:",12.5,GREEN,"bold"))
    o.append(text(xe,Y(REV[11])+43,rs(439824),12.5,INK,"bold"))
    o.append(text(X(0)+2,Y(REV[0])+22,rs(202640),12.5,INK,"bold",anchor="start"))
    o.append(text(X(9),Y(REV[9])-12,"actual revenue",12.5,ACC,"bold",anchor="middle"))
    ly=24
    for col,dash,lab in [(ACC,None,"Actual monthly revenue, 2025 (solid line, dots)"),
                         (GREEN,"2 3","Steady 7.3% a month, the compound rate (short dashes): ends exactly at December"),
                         (RED,"8 5","13.1% a month, the average of the monthly % changes (long dashes): overshoots")]:
        o.append(path(f"M20,{ly-4} h34",stroke=col,sw=3,dash=dash)); o.append(text(62,ly,lab,12.5,INK)); ly+=21
    o.append(text(20,Y0+44,"Source: One-year database (2025).",12,MUTED,style="italic"))
    return svg(W_CANVAS,Y0+56,"".join(o))

# ---------- Figure 4.3: order values, mean vs median ----------
def fig_hist():
    bins=[34,45,36,28,14,9,4,1,1,0,1]
    o=[]; X0=64; Y0=330; bw=54; Hh=220; vmax=50
    def X(v): return X0+v/10000*bw
    for v in range(0,51,10):
        y=Y0-v/vmax*Hh
        o.append(path(f"M{X0},{y} H{X0+11*bw}",stroke="#eef1f5",sw=1))
        o.append(text(X0-10,y+4,str(v),12,MUTED,anchor="end"))
    for i,c in enumerate(bins):
        h=c/vmax*Hh
        if c: o.append(rect(X0+i*bw+3,Y0-h,bw-6,h,fill="#9cc3dd",rx=2))
    for k in range(0,12):
        o.append(text(X0+k*bw,Y0+20,str(k*10),12,MUTED,anchor="middle"))
    o.append(path(f"M{X0},{Y0} H{X0+11*bw}",stroke=MUTED,sw=1.2))
    med=21375; mean=25061
    o.append(path(f"M{X(med):.1f},{Y0} V78",stroke=GREEN,sw=2.5))
    o.append(path(f"M{X(mean):.1f},{Y0} V78",stroke=RED,sw=2.5,dash="6 4"))
    for i,c in enumerate(bins):
        if c:
            h=c/vmax*Hh; cx=X0+i*bw+bw/2
            o.append(rect(cx-13,Y0-h-20,26,17,fill="#fff",rx=3)); o.append(text(cx,Y0-h-7,str(c),12,INK,anchor="middle"))
    o.append(text(X(med)-8,72,"median ₹21,375",13,GREEN,"bold",anchor="end"))
    o.append(text(X(mean)+8,72,"mean ₹25,061",13,RED,"bold"))
    o.append(text(X0+11*bw,130,"a few large orders",13,MUTED,anchor="end",style="italic"))
    o.append(text(X0+11*bw,148,"pull the mean to the right",13,MUTED,anchor="end",style="italic"))
    o.append(text(16,24,"173 orders in 2025, grouped by value",15,INK,"bold",family=HEAD))
    o.append(text(16,44,"Height of each bar: number of orders in that ₹10,000 band",12.5,MUTED))
    o.append(text(X0+5.5*bw,Y0+42,"order value (₹ thousand)",12.5,MUTED,anchor="middle"))
    o.append(text(16,Y0+64,"Source: One-year database (2025).",12,MUTED,style="italic"))
    return svg(W_CANVAS,Y0+76,"".join(o))

# ---------- Figure 4.4: the same margins, two axes ----------
GM=[29.2,26.0,26.2,31.1,24.4,25.1,27.3,25.5,25.2,27.9,24.0,26.5]
def fig_axes():
    o=[]
    TOP=86; Hh=250; Y0=TOP+Hh; W=276
    def panel(x0,title1,title2,lo,hi,step):
        bw=W/12
        def Y(v): return Y0-(v-lo)/(hi-lo)*Hh
        o.append(text(x0-44,24,title1,14,INK,"bold",family=HEAD))
        o.append(text(x0-44,43,title2,14,INK,"bold",family=HEAD))
        v=lo
        while v<=hi+1e-9:
            o.append(path(f"M{x0},{Y(v)} H{x0+W}",stroke="#eef1f5",sw=1)); o.append(text(x0-8,Y(v)+4,f"{v:g}%",12,MUTED,anchor="end")); v+=step
        for i,g in enumerate(GM):
            h=Y0-Y(g); nov = i==10
            o.append(rect(x0+i*bw+2.5,Y(g),bw-5,h,fill=RED if nov else "#9cc3dd",rx=2))
            o.append(text(x0+i*bw+bw/2,Y0+18,MONTHS[i][0],12,INK if nov else MUTED,"bold" if nov else "normal",anchor="middle"))
        # November labelled in words and with a pointer, not by colour alone
        nx=x0+10*bw+bw/2
        o.append(path(f"M{nx},{TOP-6} V{Y(24.0)-4}",stroke=INK,sw=1.2,dash="2 2"))
        o.append(text(nx,TOP-12,"November 24.0%",12.5,INK,"bold",anchor="end"))
        o.append(path(f"M{x0},{Y0} H{x0+W}",stroke=MUTED,sw=1.2))
    panel(62,"Axis starts at 23%:","November looks like a collapse",23,32,1)
    panel(418,"Axis starts at 0%:","a dip of 3.9 points",0,35,5)
    o.append(text(18,Y0+48,"Riverstone's monthly gross margin in 2025. Both charts show exactly the same",13,MUTED,style="italic"))
    o.append(text(18,Y0+67,"twelve numbers. Source: One-year database (2025).",13,MUTED,style="italic"))
    return svg(W_CANVAS,Y0+80,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig4-1-percent-changes-dont-cancel.svg",fig_asym),("fig4-2-average-growth-vs-compound.svg",fig_growth),
                    ("fig4-3-order-values-mean-vs-median.svg",fig_hist),("fig4-4-same-numbers-two-axes.svg",fig_axes)]:
        open(name,"w").write(fn())
    print("ok")
