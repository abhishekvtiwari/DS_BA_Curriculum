# Generates the SVG figures for Chapter 52. Run: python3 make_figs52.py
# Analyst to Architect. Riverstone Supplies is fictional; every name and number is invented.
from make_figs import *
from make_figs01 import wrap
from make_figs07 import arrow, header_card
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_responsibility():
    o=[]
    o.append(header_card(30,30,460,320,ACC,"Provider secures: THE CLOUD"))
    o.append(wrap(46,100,["Physical data centers and hardware","The virtualization layer","Managed services' own software","Network backbone between regions"],13,INK,26))
    o.append(rect(30,220,460,110,fill="#eaf5f1",stroke=GREEN,sw=1.4,rx=7))
    o.append(text(46,244,"You never touch this layer directly.",12.5,GREEN,"bold"))
    o.append(wrap(46,266,["A data center flooding, a hardware fault,","a hypervisor bug: the provider's problem."],12,INK,20))

    o.append(header_card(520,30,490,320,ORANGE,"You secure: WHAT'S IN THE CLOUD"))
    o.append(wrap(536,100,["Your data, and who can read or change it","IAM: identities, roles, permissions (52.1)","Network rules: VPCs, subnets, security groups","How you configure every service you use","Your application code and its containers","Secrets: tokens, passwords, keys (52.6)"],13,INK,26))
    o.append(rect(520,290,490,42,fill="#fff4e8",stroke=ORANGE,sw=1.4,rx=7))
    o.append(text(536,316,"A public bucket, an open port, a committed secret: always yours.",12,ORANGE,"bold"))

    o.append(rect(30,372,980,54,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,398,"The line never moves, whatever the provider or the service.",13.5,INK,"bold"))
    o.append(text(46,417,"\"The provider secures the cloud; you secure what's in it.\"",12.5,MUTED,style="italic"))
    return svg(1040,446,"".join(o))

def fig_vpc():
    o=[]
    o.append(rect(30,30,980,340,fill="#fbfcfe",stroke=ACC,sw=1.8,rx=10))
    o.append(text(50,58,"VPC  10.0.0.0/16   (65,536 addresses)",15,ACC,"bold",family=HEAD))
    azs=[("Availability zone A","A",70),("Availability zone B","B",545)]
    for az_name, zone_letter, x0 in azs:
        o.append(rect(x0,80,440,270,fill="#fff",stroke=RULE,sw=1.3,rx=8))
        o.append(text(x0+16,106,az_name,13.5,INK,"bold"))
        o.append(rect(x0+16,124,408,90,fill="#eef2f9",stroke=MUTED,sw=1.2,rx=6))
        o.append(text(x0+28,148,"public subnet",12.5,MUTED,"bold"))
        o.append(text(x0+28,168,"10.0.0.0/24" if zone_letter == "A" else "10.0.1.0/24",12.5,INK,family=MONO))
        o.append(text(x0+28,188,"load balancer  ·  251 usable hosts",11.5,MUTED))
        o.append(rect(x0+16,226,408,110,fill="#eaf5f1",stroke=GREEN,sw=1.2,rx=6))
        o.append(text(x0+28,250,"private subnet",12.5,GREEN,"bold"))
        o.append(text(x0+28,270,"10.0.2.0/24" if zone_letter == "A" else "10.0.3.0/24",12.5,INK,family=MONO))
        o.append(text(x0+28,290,"pipeline container",11.5,INK))
        o.append(text(x0+28,308,"database  ·  251 usable hosts",11.5,MUTED))
        o.append(path(f"M{x0+220},{214} V{226}",stroke=MUTED,sw=1.6))
    o.append(rect(30,384,980,54,fill="#f6f9fc",stroke=RULE,rx=7))
    o.append(text(46,410,"Security groups: the public subnet accepts internet traffic on 443; the private subnet",13,INK,"bold"))
    o.append(text(46,429,"accepts traffic only from the public subnet's security group, and nothing from the internet directly.",12,MUTED))
    return svg(1040,456,"".join(o))

def fig_dockerfile_layers():
    o=[]
    steps=[("FROM python:3.12-slim",ACC,"base image: small, official"),
           ("RUN apt-get install libpq-dev",ACC,"system packages, cache cleaned"),
           ("COPY requirements.txt .\nRUN pip install",GREEN,"dependencies: rebuilds only when this file changes"),
           ("COPY *.py .",ORANGE,"application code: this is what usually changes"),
           ("RUN useradd; USER pipeline",PURPLE,"drop root before anything runs"),
           ("CMD [\"dagster\", \"dev\", ...]",MUTED,"what runs when a container starts")]
    y=30
    for i,(instr,c,note) in enumerate(steps):
        o.append(rect(30,y,980,50,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(rect(30,y,8,50,fill=c,rx=3))
        lines = instr.split("\n")
        for j,l in enumerate(lines):
            o.append(f'<text x="52" y="{y+22+j*17}" font-size="12.5" font-family="{MONO}" fill="{INK}">{l}</text>')
        o.append(text(560,y+30,note,12,MUTED,style="italic"))
        if i<len(steps)-1: o.append(arrow(520,y+50,520,y+62,c=MUTED,sw=1.6))
        y+=62
    o.append(rect(30,y+6,980,52,fill="#fff4e8",stroke=ORANGE,rx=7))
    o.append(text(46,y+28,"Layers 1-3 rarely change and stay cached. Editing ingest.py only rebuilds from layer 4 down.",13,INK,"bold"))
    o.append(text(46,y+46,"That ordering, dependencies before code, is the single biggest speed-up available to a Dockerfile.",12,MUTED))
    return svg(1040,y+72,"".join(o))

if __name__=="__main__":
    for n,f in [("fig52-1-shared-responsibility.svg",fig_responsibility),
                ("fig52-2-vpc-subnets.svg",fig_vpc),
                ("fig52-3-dockerfile-layers.svg",fig_dockerfile_layers)]:
        open(n,"w").write(f())
    print("ok")
