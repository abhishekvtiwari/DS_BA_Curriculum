# Generates the SVG figures for Chapter 51. Run: python3 make_figs51.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_loop():
    o=[]
    stages=[("Source systems",MUTED,["ERP, CRM,","marketing tools"]),
            ("Ingestion",ACC,["Ch 45"]),
            ("Warehouse",ACC,["raw, staging,","mart (Ch 46-49)"]),
            ("Data products",GREEN,["reports, emails,","dashboards"])]
    W=200; G=30; y=140
    for i,(t,c,lines) in enumerate(stages):
        x=30+i*(W+G)
        o.append(header_card(x,y,W,110,c,t,tsize=13.5))
        o.append(wrap(x+14,y+64,lines,12,INK,19))
        if i<3: o.append(arrow(x+W+2,y+55,x+W+G-2,y+55,c=INK,sw=2.2))
    stopx=30+3*(W+G)+W/2
    o.append(text(stopx,y-58,"Most companies stop here",12.5,MUTED,"bold",anchor="middle",style="italic"))
    # return arrow from data products back to source systems, labeled "this chapter", drawn ABOVE the row
    top_y = y-90
    o.append(path(f"M{stopx},{y-6} V{top_y} H{30+W/2} V{y-6}",stroke=PURPLE,sw=2.6))
    o.append(f'<path d="M{30+W/2-7},{y-18} L{30+W/2},{y-6} L{30+W/2+7},{y-18} Z" fill="{PURPLE}"/>')
    o.append(text((stopx+30+W/2)/2,top_y-10,"THIS CHAPTER: back into operational systems",13,PURPLE,"bold",anchor="middle"))
    o.append(rect(30,y+180,4*W+3*G,60,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,y+206,"A dashboard is pulled: someone has to open it and notice something.",12.5,INK,"bold"))
    o.append(text(46,y+226,"A synced field is pushed: it's already sitting where the decision gets made.",12,MUTED))
    return svg(1040,y+260,"".join(o))

def fig_patterns():
    o=[]
    def node(cx,cy,r=16,c=ACC):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
    import math
    def ring(cx,cy,rad,n):
        return [(cx+rad*math.cos(2*math.pi*i/n-math.pi/2), cy+rad*math.sin(2*math.pi*i/n-math.pi/2)) for i in range(n)]
    panels=[("Point-to-point",RED,"n^2 connections"),("Hub-and-spoke",ACC,"n connections"),
            ("Message queue",GREEN,"senders & receivers don't know each other"),("iPaaS",PURPLE,"connectors, monitoring, retries included")]
    W=250; y0=50
    for i,(title,c,note) in enumerate(panels):
        cx = 150+i*260; cy=170
        o.append(text(cx,y0,title,13.5,c,"bold",family=HEAD,anchor="middle"))
        pts = ring(cx,cy,80,5)
        if i==0:
            for a in range(5):
                for b in range(a+1,5):
                    o.append(path(f"M{pts[a][0]:.1f},{pts[a][1]:.1f} L{pts[b][0]:.1f},{pts[b][1]:.1f}",stroke=RULE,sw=1.3))
            for p in pts: o.append(node(*p,c=c))
        elif i==1:
            for p in pts:
                o.append(path(f"M{cx},{cy} L{p[0]:.1f},{p[1]:.1f}",stroke=c,sw=1.6))
            o.append(node(cx,cy,20,c))
            for p in pts: o.append(node(*p,r=13,c=MUTED))
        elif i==2:
            o.append(rect(cx-46,cy-16,92,32,fill=c,rx=6))
            o.append(text(cx,cy+5,"queue",11.5,"#fff","bold",anchor="middle"))
            for k,p in enumerate(pts):
                dashed = 'stroke-dasharray="4 3"'
                o.append(f'<path d="M{cx},{cy} L{p[0]:.1f},{p[1]:.1f}" stroke="{MUTED}" stroke-width="1.4" {dashed}/>')
                o.append(node(*p,r=13,c=MUTED))
        else:
            o.append(rect(cx-55,cy-22,110,44,fill=c,rx=8))
            o.append(text(cx,cy-2,"integration",11,"#fff","bold",anchor="middle"))
            o.append(text(cx,cy+14,"platform",11,"#fff","bold",anchor="middle"))
            for p in pts:
                o.append(path(f"M{cx},{cy} L{p[0]:.1f},{p[1]:.1f}",stroke=c,sw=1.6))
            for p in pts: o.append(node(*p,r=13,c=MUTED))
        o.append(text(cx,cy+110,note,11.5,MUTED,anchor="middle",style="italic"))
    return svg(1040,300,"".join(o))

if __name__=="__main__":
    for n,f in [("fig51-1-the-full-loop.svg",fig_loop),("fig51-2-integration-patterns.svg",fig_patterns)]:
        open(n,"w").write(f())
    print("ok")
