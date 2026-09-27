# Generates the SVG figures for Chapter 4. Run: python3 make_figs04.py
# Numbers come from the one-year database (riverstone_2025), the same runs as checks/ch04_check.py.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; GREY="#5b6475"

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.4), y2-L*math.sin(a-0.4)); p2=(x2-L*math.cos(a+0.4), y2-L*math.sin(a+0.4))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 4.1: percent changes don't cancel ----------
def fig_asym():
    o=[]; base=370; scale=1.5  # px per rupee
    def panel(x0,title,steps,col):
        o.append(text(x0,30,title,14.5,INK,"bold",family=HEAD))
        bw=90; gap=70
        for i,(label,v,note) in enumerate(steps):
            x=x0+i*(bw+gap); h=v*scale
            fill = GREY if i==0 else col
            o.append(rect(x,base-h,bw,h,fill=fill,rx=4))
            o.append(text(x+bw/2,base-h-10,f"₹{v:g}",15,INK,"bold",anchor="middle"))
            o.append(text(x+bw/2,base+22,label,12.5,MUTED,anchor="middle"))
            if i>0:
                o.append(arrow(x-gap+8,base-steps[i-1][1]*scale-30,x-8,base-h-30,c=col))
                o.append(text(x-gap/2,base-max(steps[i-1][1],v)*scale-48,note,13,col,"bold",anchor="middle"))
        o.append(path(f"M{x0-10},{base} H{x0+3*bw+2*gap+10}",stroke=RULE,sw=1.2))
    panel(40,"Up 50%, then down 50%",[("start",100,""),("after +50%",150,"+50% of 100"),("after −50%",75,"−50% of 150")],ACC)
    panel(560,"Down 20%, then up 20%",[("start",100,""),("after −20%",80,"−20% of 100"),("after +20%",96,"+20% of 80")],ORANGE)
    o.append(text(40,420,"Each percentage is taken of a different starting number, so equal-looking rises and falls don't cancel out.",13,MUTED,style="italic"))
    return svg(1040,440,"".join(o))

# ---------- Figure 4.2: bumpy real growth vs two smooth paths ----------
REV=[202640,253664,278008,210282,329359,186928,232692,329282,558315,681071,633408,439824]
MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def fig_growth():
    o=[]; X0=100; Y0=380; W=820; Hh=320; vmax=800000
    def X(i): return X0+i*W/11
    def Y(v): return Y0-v/vmax*Hh
    for v in range(0,800001,200000):
        o.append(path(f"M{X0},{Y(v)} H{X0+W}",stroke="#eef1f5",sw=1))
        o.append(text(X0-12,Y(v)+4,f"₹{v:,}",11.5,MUTED,anchor="end"))
    for i,m in enumerate(MONTHS): o.append(text(X(i),Y0+22,m,12,MUTED,anchor="middle"))
    avg=[REV[0]*1.1307**i for i in range(12)]
    cmp_=[REV[0]*(REV[11]/REV[0])**(i/11) for i in range(12)]
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(avg)),stroke=RED,sw=2.2,dash="6 4"))
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(cmp_)),stroke=GREEN,sw=2.4,dash="3 3"))
    o.append(path("M"+" L".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(REV)),stroke=ACC,sw=3))
    for i,v in enumerate(REV): o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{ACC}"/>')
    o.append(text(X(11)+8,Y(avg[11])+4,"₹782,621",12.5,RED,"bold"))
    o.append(text(X(11)+8,Y(REV[11])+4,"₹439,824",12.5,INK,"bold"))
    o.append(text(X(0)-4,Y(REV[0])+22,"₹202,640",12,INK,"bold",anchor="start"))
    ly=40
    for col,dash,lab in [(ACC,None,"Actual monthly revenue, 2025"),(GREEN,"3 3","Steady 7.3% a month: the compound rate (ends exactly at December)"),(RED,"6 4","13.1% a month: the simple average of the monthly % changes (overshoots)")]:
        o.append(path(f"M{X0},{ly} h34",stroke=col,sw=3,dash=dash)); o.append(text(X0+44,ly+4,lab,13,INK)); ly+=22
    return svg(1040,Y0+40,"".join(o))

# ---------- Figure 4.3: order values, mean vs median ----------
def fig_hist():
    bins=[34,45,36,28,14,9,4,1,1,0,1]
    o=[]; X0=90; Y0=330; bw=72; Hh=240; vmax=50
    def X(v): return X0+v/10000*bw
    for v in range(0,51,10):
        y=Y0-v/vmax*Hh
        o.append(path(f"M{X0},{y} H{X0+11*bw}",stroke="#eef1f5",sw=1))
        o.append(text(X0-10,y+4,str(v),11.5,MUTED,anchor="end"))
    for i,c in enumerate(bins):
        h=c/vmax*Hh
        if c: o.append(rect(X0+i*bw+3,Y0-h,bw-6,h,fill="#9cc3dd",rx=2))
    for k in range(0,12):
        o.append(text(X0+k*bw,Y0+20,f"{k*10}k",11.5,MUTED,anchor="middle"))
    o.append(path(f"M{X0},{Y0} H{X0+11*bw}",stroke=MUTED,sw=1.2))
    med=21375; mean=25061
    o.append(path(f"M{X(med):.1f},{Y0} V70",stroke=GREEN,sw=2.5))
    o.append(path(f"M{X(mean):.1f},{Y0} V70",stroke=RED,sw=2.5,dash="6 4"))
    for i,c in enumerate(bins):
        if c:
            h=c/vmax*Hh; cx=X0+i*bw+bw/2
            o.append(rect(cx-11,Y0-h-19,22,16,fill="#fff",rx=3)); o.append(text(cx,Y0-h-6,str(c),11.5,INK,anchor="middle"))
    o.append(text(X(med)-8,64,"median ₹21,375",13,GREEN,"bold",anchor="end"))
    o.append(text(X(mean)+8,64,"mean ₹25,061",13,RED,"bold"))
    o.append(text(X0+11*bw,120,"a few large orders",12.5,MUTED,anchor="end",style="italic"))
    o.append(text(X0+11*bw,138,"pull the mean to the right",12.5,MUTED,anchor="end",style="italic"))
    o.append(text(X0,24,"173 orders in 2025, grouped by value (number of orders in each ₹10,000 band)",14,INK,"bold",family=HEAD))
    o.append(text(X0+5.5*bw,Y0+44,"order value (₹)",12.5,MUTED,anchor="middle"))
    return svg(X0+11*bw+40,Y0+60,"".join(o))

# ---------- Figure 4.4: the same margins, two axes ----------
GM=[29.2,26.0,26.2,31.1,24.4,25.1,27.3,25.5,25.2,27.9,24.0,26.5]
def fig_axes():
    o=[]
    def panel(x0,title,lo,hi,step,col):
        W=400; Hh=240; Y0=320; bw=W/12
        def Y(v): return Y0-(v-lo)/(hi-lo)*Hh
        o.append(text(x0,34,title,14,INK,"bold",family=HEAD))
        v=lo
        while v<=hi+1e-9:
            o.append(path(f"M{x0},{Y(v)} H{x0+W}",stroke="#eef1f5",sw=1)); o.append(text(x0-8,Y(v)+4,f"{v:g}%",11,MUTED,anchor="end")); v+=step
        for i,g in enumerate(GM):
            h=Y0-Y(g); c = RED if i==10 else col
            o.append(rect(x0+i*bw+3,Y(g),bw-6,h,fill=c,rx=2))
            o.append(text(x0+i*bw+bw/2,Y0+18,MONTHS[i][0],11,MUTED,anchor="middle"))
        o.append(path(f"M{x0},{Y0} H{x0+W}",stroke=MUTED,sw=1.2))
    panel(70,"Axis starts at 23%: November looks like a collapse",23,32,1,"#9cc3dd")
    panel(590,"Axis starts at 0%: a dip of 3.9 points",0,35,5,"#9cc3dd")
    o.append(text(70,370,"Riverstone's monthly gross margin in 2025. Both charts show exactly the same twelve numbers; November is in red.",13,MUTED,style="italic"))
    return svg(1040,390,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig4-1-percent-changes-dont-cancel.svg",fig_asym),("fig4-2-average-growth-vs-compound.svg",fig_growth),
                    ("fig4-3-order-values-mean-vs-median.svg",fig_hist),("fig4-4-same-numbers-two-axes.svg",fig_axes)]:
        open(name,"w").write(fn())
    print("ok")
