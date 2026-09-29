# Generates the SVG figures for Chapter 52. Run: python3 make_figs52.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
# Every figure is drawn on a 720 px canvas, so 11.5 px text prints at 7.9 pt (the book's minimum is 7 pt).
from make_figs import *
from make_figs07 import arrow
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
YOU_BG="#fff4e8"; PROV_BG="#eaf1f8"
W=720


def fig_responsibility():
    """Figure 52.1: the shared-responsibility line at three heights, for IaaS, PaaS and SaaS."""
    o=[]
    layers=["Your data, and who can access it","How you configure the service","Application code",
            "Operating system and runtime","Virtualization layer","Hardware and data centres"]
    # how many layers (from the top) the customer manages, per level
    cols=[("IaaS","e.g. a virtual server",4),("PaaS","e.g. managed PostgreSQL",3),("SaaS","e.g. a CRM, Gmail",2)]
    x0, lw, cw, top, rh = 20, 222, 150, 72, 40
    o.append(text(x0, 24, "Who secures what, at each service level", 15, INK, "bold", family=HEAD))
    o.append(text(x0, 46, "Each cell says who is responsible; the heavy line is where the split falls.", 12, MUTED))
    for j,(name,eg,n) in enumerate(cols):
        cx = x0+lw+10+j*(cw+8)
        o.append(text(cx+cw/2, top-4, name, 13.5, INK, "bold", anchor="middle"))
    for i,lay in enumerate(layers):
        y = top+8+i*rh
        o.append(text(x0, y+25, lay, 12, INK, "bold" if i<2 else "normal"))
        for j,(name,eg,n) in enumerate(cols):
            cx = x0+lw+10+j*(cw+8)
            yours = i < n
            label = "You: your settings" if (name=="SaaS" and i==1) else ("You" if yours else "Provider")
            o.append(rect(cx, y+3, cw, rh-6, fill=YOU_BG if yours else PROV_BG, stroke=ORANGE if yours else ACC, sw=1, rx=5))
            o.append(text(cx+cw/2, y+25, label, 12, ORANGE if yours else ACC, "bold" if yours else "normal", anchor="middle"))
    # the heavy line under the customer's last layer, per column
    for j,(name,eg,n) in enumerate(cols):
        cx = x0+lw+10+j*(cw+8)
        ly = top+8+n*rh
        o.append(path(f"M{cx-3},{ly} H{cx+cw+3}", stroke=INK, sw=3.2))
        o.append(text(cx+cw/2, top+8+6*rh+18, eg, 11.5, MUTED, anchor="middle", style="italic"))
    fy = top+8+6*rh+34
    o.append(rect(x0, fy, W-2*x0, 50, fill="#f6f9fc", stroke=RULE, rx=7))
    o.append(text(x0+14, fy+21, "The line moves with what you rent. What never moves:", 12.5, INK, "bold"))
    o.append(text(x0+14, fy+40, "your data, who can access it, and how you configure the service are always yours.", 12, INK))
    return svg(W, fy+62, "".join(o))


def fig_vpc():
    """Figure 52.2: the VPC computed in section 52.1."""
    o=[]
    o.append(rect(16,16,W-32,300,fill="#fbfcfe",stroke=ACC,sw=1.8,rx=10))
    o.append(text(32,42,"VPC  10.0.0.0/16   (65,536 addresses)",14.5,ACC,"bold",family=HEAD))
    for az_name, subs, x0 in [("Availability zone A",("10.0.0.0/24","10.0.2.0/24"),32),
                              ("Availability zone B",("10.0.1.0/24","10.0.3.0/24"),368)]:
        o.append(rect(x0,58,320,244,fill="#fff",stroke=RULE,sw=1.3,rx=8))
        o.append(text(x0+14,82,az_name,13,INK,"bold"))
        o.append(rect(x0+12,94,296,84,fill="#eef2f9",stroke=MUTED,sw=1.2,rx=6))
        o.append(text(x0+24,116,"public subnet",12.5,MUTED,"bold"))
        o.append(text(x0+24,138,subs[0],12.5,INK,family=MONO))
        o.append(text(x0+24,160,"load balancer · 251 usable hosts",12,MUTED))
        o.append(arrow(x0+160,178,x0+160,196,c=MUTED,sw=1.6))
        o.append(rect(x0+12,198,296,92,fill="#eaf5f1",stroke=GREEN,sw=1.2,rx=6))
        o.append(text(x0+24,220,"private subnet",12.5,GREEN,"bold"))
        o.append(text(x0+24,242,subs[1],12.5,INK,family=MONO))
        o.append(text(x0+24,262,"pipeline container, database",12,INK))
        o.append(text(x0+24,280,"251 usable hosts",12,MUTED))
    o.append(rect(16,328,W-32,62,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(30,351,"Security groups: the public subnet accepts internet traffic on port 443 (HTTPS);",12.5,INK,"bold"))
    o.append(text(30,373,"the private subnet accepts traffic only from the public subnet's security group.",12,MUTED))
    return svg(W,404,"".join(o))


def fig_dockerfile_layers():
    """Figure 52.3: the Dockerfile's steps, numbered, in build order."""
    o=[]
    steps=[("FROM python:3.14-slim",ACC,"base image: small and official"),
           ("RUN useradd --create-home pipeline",ACC,"the user to run as, made once"),
           ("WORKDIR /app\nCOPY requirements.txt .\nRUN pip install ...",GREEN,"dependencies: rebuilt only when\nrequirements.txt changes"),
           ("COPY ingest.py riverstone_pipeline.py\n  run_flash.py ./",ORANGE,"application code:\nwhat usually changes"),
           ("RUN mkdir ... && chown ...",ORANGE,"folders the pipeline writes to"),
           ("ENV ...   USER pipeline",PURPLE,"settings; stop being root"),
           ("CMD [\"python\", \"run_flash.py\"]",MUTED,"what runs when a container starts")]
    y=16; lh=16
    for i,(instr,c,note) in enumerate(steps):
        il=instr.split("\n"); nl=note.split("\n")
        h=max(len(il),len(nl))*lh+18
        o.append(rect(16,y,W-32,h,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(rect(16,y,30,h,fill=c,rx=4))
        o.append(text(31,y+h/2+5,str(i+1),13,"#fff","bold",anchor="middle"))
        def block(lines, x, size, fill, family=None, style=""):
            y0 = y + h/2 - (len(lines)-1)*lh/2 + 4.5
            return "".join(text(x, y0+k*lh, l, size, fill, family=family, style=style) for k,l in enumerate(lines))
        o.append(block(il, 56, 11.5, INK, family=MONO))
        o.append(block(nl, 420, 12, MUTED, style="italic"))
        if i<len(steps)-1: o.append(arrow(360,y+h,360,y+h+10,c=MUTED,sw=1.5))
        y+=h+10
    o.append(rect(16,y+2,W-32,52,fill=YOU_BG,stroke=ORANGE,rx=7))
    o.append(text(30,y+23,"Steps 1–3 rarely change, so Docker reuses them from its cache.",12.5,INK,"bold"))
    o.append(text(30,y+43,"Editing ingest.py rebuilds from step 4 down: seconds, not minutes.",12,MUTED))
    return svg(W,y+66,"".join(o))


def fig_labels():
    """Figure 52.4: how a Deployment and a Service find their Pods, by label."""
    o=[]
    o.append(rect(16,20,210,96,fill="#fff",stroke=ACC,sw=1.6,rx=8))
    o.append(text(30,44,"Deployment flash-page",12.5,ACC,"bold"))
    o.append(text(30,66,"replicas: 2",12,INK,family=MONO))
    o.append(text(30,86,"selector:",12,INK,family=MONO))
    o.append(text(46,104,"app: flash-page",12,INK,family=MONO))
    o.append(rect(494,20,210,96,fill="#fff",stroke=PURPLE,sw=1.6,rx=8))
    o.append(text(508,44,"Service flash-page",12.5,PURPLE,"bold"))
    o.append(text(508,66,"port 80 → 8080",12,INK))
    o.append(text(508,86,"selector:",12,INK,family=MONO))
    o.append(text(524,104,"app: flash-page",12,INK,family=MONO))
    for k,x in enumerate([250,390]):
        o.append(rect(x,192,120,78,fill="#eaf5f1",stroke=GREEN,sw=1.4,rx=8))
        o.append(text(x+60,216,f"Pod {k+1}",12.5,GREEN,"bold",anchor="middle"))
        o.append(text(x+60,236,"label:",11.5,INK,anchor="middle",family=MONO))
        o.append(text(x+60,254,"app: flash-page",11.5,INK,anchor="middle",family=MONO))
    o.append(text(30,138,"keeps 2 Pods with this label",12,ACC,style="italic"))
    o.append(text(690,138,"sends traffic to Pods with this label",12,PURPLE,anchor="end",style="italic"))
    o.append(arrow(150,146,300,188,c=ACC,sw=1.6)); o.append(arrow(170,146,430,188,c=ACC,sw=1.6))
    o.append(arrow(580,146,330,188,c=PURPLE,sw=1.6)); o.append(arrow(600,146,460,188,c=PURPLE,sw=1.6))
    o.append(rect(16,288,W-32,50,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(30,309,"The three labels must match exactly. A typo in one leaves the Service",12.5,INK,"bold"))
    o.append(text(30,328,"with no Pods to send to, and Kubernetes reports no error.",12,MUTED))
    return svg(W,352,"".join(o))


if __name__=="__main__":
    for n,f in [("fig52-1-shared-responsibility.svg",fig_responsibility),
                ("fig52-2-vpc-subnets.svg",fig_vpc),
                ("fig52-3-dockerfile-layers.svg",fig_dockerfile_layers),
                ("fig52-4-labels.svg",fig_labels)]:
        open(n,"w").write(f())
    print("ok")
