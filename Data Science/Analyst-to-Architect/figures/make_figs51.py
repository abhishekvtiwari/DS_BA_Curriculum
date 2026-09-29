# Generates the SVG figures for Chapter 51. Run: python3 make_figs51.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_loop():
    # 760 px canvas at 174 mm: every text is >= 12 px, so it prints at >= 7.8 pt
    o=[]
    stages=[("Source systems",MUTED,["ERP, CRM,","marketing tools"]),
            ("Ingestion",ACC,["Chapter 45"]),
            ("Warehouse",ACC,["raw, staging, mart","(Chapters 46-49)"]),
            ("Data products",GREEN,["reports, emails,","dashboards"])]
    W=164; G=24; X0=20; y=128
    for i,(t,c,lines) in enumerate(stages):
        x=X0+i*(W+G)
        o.append(header_card(x,y,W,104,c,t,tsize=14))
        o.append(wrap(x+12,y+60,lines,13,INK,19))
        if i<3: o.append(arrow(x+W+2,y+52,x+W+G-2,y+52,c=INK,sw=2.2))
    stopx=X0+3*(W+G)+W/2
    srcx=X0+W/2
    top_y=y-78
    # the return arrow: up from data products, left along the top, down into source systems
    o.append(path(f"M{stopx},{y-6} V{top_y} H{srcx} V{y-6}",stroke=PURPLE,sw=2.6))
    o.append(f'<path d="M{srcx-7},{y-18} L{srcx},{y-6} L{srcx+7},{y-18} Z" fill="{PURPLE}"/>')
    o.append(text((stopx+srcx)/2,top_y-10,"THIS CHAPTER: back into the systems people work in",13.5,PURPLE,"bold",anchor="middle"))
    # the label sits left of the purple line, so the line never crosses it
    o.append(text(stopx-12,y-30,"Most companies stop here",13,MUTED,"bold",anchor="end",style="italic"))
    o.append(rect(X0,y+132,4*W+3*G,58,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(X0+14,y+156,"A dashboard is pulled: someone has to open it and notice something.",13,INK,"bold"))
    o.append(text(X0+14,y+177,"A synced field is pushed: it already sits where the decision gets made.",13,MUTED))
    return svg(760,y+202,"".join(o))

def fig_patterns():
    # 800 px canvas at 174 mm: every text is >= 12 px, so it prints at >= 7.4 pt
    o=[]
    def node(cx,cy,r=12,c=ACC):
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{c}"/>'
    import math
    def ring(cx,cy,rad,n):
        return [(cx+rad*math.cos(2*math.pi*i/n-math.pi/2), cy+rad*math.sin(2*math.pi*i/n-math.pi/2)) for i in range(n)]
    panels=[("Point-to-point",RED,["up to n(n\u22121)/2 links:","5 systems \u2192 10"]),
            ("Hub-and-spoke",ACC,["n links:","5 systems \u2192 5"]),
            ("Message queue",GREEN,["senders and receivers","don't know each other"]),
            ("iPaaS",PURPLE,["a hosted hub: connectors,","monitoring, retries"])]
    PW=200; y0=30; cy=128; R=62
    for i,(title,c,note) in enumerate(panels):
        cx=PW/2+i*PW
        o.append(text(cx,y0,title,14,c,"bold",family=HEAD,anchor="middle"))
        pts=ring(cx,cy,R,5)
        if i==0:
            for a in range(5):
                for b in range(a+1,5):
                    o.append(path(f"M{pts[a][0]:.1f},{pts[a][1]:.1f} L{pts[b][0]:.1f},{pts[b][1]:.1f}",stroke=RULE,sw=1.3))
            for p_ in pts: o.append(node(*p_,c=c))
        elif i==1:
            for p_ in pts: o.append(path(f"M{cx},{cy} L{p_[0]:.1f},{p_[1]:.1f}",stroke=c,sw=1.6))
            o.append(node(cx,cy,17,c))
            o.append(text(cx,cy+4.5,"hub",12,"#fff","bold",anchor="middle"))
            for p_ in pts: o.append(node(*p_,c=MUTED))
        elif i==2:
            for p_ in pts: o.append(path(f"M{cx},{cy} L{p_[0]:.1f},{p_[1]:.1f}",stroke=MUTED,sw=1.4,dash="4 3"))
            o.append(rect(cx-34,cy-14,68,28,fill=c,rx=6))
            o.append(text(cx,cy+4.5,"queue",12.5,"#fff","bold",anchor="middle"))
            for p_ in pts: o.append(node(*p_,c=MUTED))
        else:
            for p_ in pts: o.append(path(f"M{cx},{cy} L{p_[0]:.1f},{p_[1]:.1f}",stroke=c,sw=1.6))
            o.append(rect(cx-44,cy-20,88,40,fill=c,rx=8))
            o.append(text(cx,cy-3,"integration",12,"#fff","bold",anchor="middle"))
            o.append(text(cx,cy+13,"platform",12,"#fff","bold",anchor="middle"))
            for p_ in pts: o.append(node(*p_,c=MUTED))
        for k,line in enumerate(note):
            o.append(text(cx,cy+R+34+k*17,line,12.5,MUTED if i else INK,anchor="middle",style="italic"))
    return svg(800,cy+R+64,"".join(o))

if __name__=="__main__":
    for n,f in [("fig51-1-the-full-loop.svg",fig_loop),("fig51-2-integration-patterns.svg",fig_patterns)]:
        open(n,"w").write(f())
    print("ok")
