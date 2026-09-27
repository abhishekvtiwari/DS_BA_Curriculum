# Generates the SVG figures for Chapter 34. Run: python3 make_figs34.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def fig_anatomy():
    o=[text(30,32,"Anatomy of a command",14,INK,"bold",family=HEAD)]
    o.append(rect(30,60,980,70,fill="#f6f9fc",stroke=RULE,rx=6))
    parts=[(50,"meera@laptop:~/ch34/practice$",MUTED,"the prompt: user, machine, folder"),
           (300,"grep",GREEN,"the command"),(390,"-c",PURPLE,"options (flags)"),
           (450,'"Pune"',ORANGE,"argument: what to look for"),(590,"../sales_lines_2025.csv",ACC,"argument: where to look")]
    for x,t,c,_ in parts: o.append(text(x,103,t,13.5,c,"bold",family=MONO))
    notes=[(300,"the command: a small program"),(390,"options change how it works"),(450,"arguments say what to work on"),(590,"often a file or a folder")]
    y=160
    for i,(x,note) in enumerate(notes):
        o.append(path(f"M{x+10},130 V{y+i*26-10}",stroke=RULE,sw=1.2))
        o.append(text(x+18,y+i*26,note,12,MUTED))
    o.append(text(30,295,"Output goes to the screen, errors go to a separate channel, and the command ends with an exit code:",12,INK))
    o.append(rect(30,310,300,40,fill="#e2f3ee",stroke=GREEN,rx=5)); o.append(text(180,335,"standard output  →  42",12.5,INK,"bold",anchor="middle",family=MONO))
    o.append(rect(350,310,300,40,fill="#fbeaea",stroke=RED,rx=5)); o.append(text(500,335,"standard error  →  (nothing)",12.5,INK,"bold",anchor="middle",family=MONO))
    o.append(rect(670,310,340,40,fill="#f6f9fc",stroke=RULE,rx=5)); o.append(text(840,335,"exit code  →  $? is 0 (found something)",12.5,INK,"bold",anchor="middle",family=MONO))
    return svg(1040,370,"".join(o))

def fig_pipeline():
    o=[text(30,32,"One question, five small tools: order lines by city",14,INK,"bold",family=HEAD)]
    stages=[("cut -d, -f5","keep column 5\n(the city)","327 lines",ACC),
            ("tail -n +2","drop the\nheader row","326 lines",PURPLE),
            ("sort","put identical\ncities together","326 lines",GREEN),
            ("uniq -c","collapse and\ncount runs","23 lines",ORANGE),
            ("sort -nr","biggest\nfirst","23 lines",GREEN)]
    x=30
    for i,(cmd,what,rows,c) in enumerate(stages):
        o.append(rect(x,70,170,110,fill="#fff",stroke=c,sw=2,rx=8))
        o.append(text(x+85,97,cmd,12.5,INK,"bold",anchor="middle",family=MONO))
        for j,l in enumerate(what.split("\n")): o.append(text(x+85,122+j*17,l,11.5,MUTED,anchor="middle"))
        o.append(text(x+85,168,rows,11.5,c,"bold",anchor="middle"))
        if i<4:
            o.append(path(f"M{x+170},125 H{x+196}",stroke=INK,sw=2)); o.append(path(f"M{x+189},119 L{x+198},125 L{x+189},131",stroke=INK,sw=2))
        x+=196
    o.append(rect(30,205,480,105,fill="#f6f9fc",stroke=RULE,rx=6))
    for i,l in enumerate(["     74 Mumbai","     42 Pune","     34 Bengaluru","     28 Delhi","     21 Kochi"]):
        o.append(text(48,230+i*17,l,12,INK,family=MONO))
    o.append(text(540,232,"Each tool reads what the one before it wrote.",12,INK))
    o.append(text(540,254,"Nothing is saved in between, and nothing is",12,INK))
    o.append(text(540,276,"loaded into memory twice: the same command",12,INK))
    o.append(text(540,298,"works on a 2 GB file on a server with no Excel.",12,INK))
    o.append(text(30,335,"Forgetting sort before uniq -c is the classic bug: uniq only collapses lines that are already next to each other.",12,MUTED,style="italic"))
    return svg(1040,350,"".join(o))

def fig_permissions():
    o=[text(30,32,"Reading ls -l",14,INK,"bold",family=HEAD)]
    o.append(rect(30,58,980,44,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(50,86,"-rw-r--r--  1  meera  meera  901  Jan  5  2026  customers.csv",14,INK,"bold",family=MONO))
    cols=[(38,"type","- file, d folder, l link"),(58,"user","owner: read + write"),(83,"group","read only"),(108,"others","read only"),
          (228,"links",""),(262,"owner",""),(330,"group",""),(398,"size","bytes"),(438,"changed",""),(556,"name","")]
    for i,(x,lab,note) in enumerate(cols[:4]):
        o.append(path(f"M{x+12},102 V{125+i*22}",stroke=colorfor(i),sw=1.4))
        o.append(text(x+20,129+i*22,f"{lab}: {note}" if note else lab,12,colorfor(i),"bold"))
    o.append(text(560,132,"Each set of three is read (r), write (w), execute (x).",12,INK))
    o.append(text(560,154,"On a folder, x means \"can go into it\".",12,INK))
    rows=[("644","rw- r-- r--","owner writes, everyone reads","data files, documents",ACC),
          ("755","rwx r-x r-x","owner writes, everyone reads and runs","scripts, folders",GREEN),
          ("600","rw- --- ---","owner only","SSH keys, .env files with passwords",ORANGE),
          ("700","rwx --- ---","owner only, and can enter","~/.ssh",PURPLE)]
    y=240
    for num,bits,who,use,c in rows:
        o.append(rect(30,y,980,42,fill="#fff",stroke=c,sw=1.5,rx=6))
        o.append(text(60,y+27,num,14,c,"bold",family=MONO)); o.append(text(130,y+27,bits,13,INK,family=MONO))
        o.append(text(290,y+27,who,12,INK)); o.append(text(620,y+27,use,12,MUTED))
        y+=52
    o.append(text(30,y+18,"chmod +x script.sh adds the execute bit; chmod 600 key removes everyone else's access.",12,MUTED))
    return svg(1040,y+35,"".join(o))

def colorfor(i):
    return [INK,"#2f7d6d","#7a4fa0","#c0662b"][i]

def fig_request():
    o=[text(30,32,"What happens when curl asks for a file",14,INK,"bold",family=HEAD)]
    o.append(rect(30,62,980,40,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(50,88,"curl --silent http://127.0.0.1:8034/exports/orders_2025-12-16.csv",13,INK,"bold",family=MONO))
    parts=[(120,"http","the protocol: HTTP, or https for encrypted",ACC),(190,"127.0.0.1","which machine (localhost = this one)",GREEN),
           (290,"8034","which program on it: the port",PURPLE),(350,"/exports/orders_…","what to ask for: the path",ORANGE)]
    y=128
    for i,(x,lab,note,c) in enumerate(parts):
        o.append(text(50,y+i*24,f"{lab}", 12.5,c,"bold",family=MONO)); o.append(text(200,y+i*24,note,12,INK))
    steps=[("1. Name → address","A name like api.example.com is looked up in DNS. 127.0.0.1 is already an address, so there is nothing to look up.",ACC),
           ("2. Connect to the port","The machine's program listening on 8034 accepts the connection. ss -ltn shows who is listening.",GREEN),
           ("3. Send the request","GET /exports/orders_2025-12-16.csv, plus headers such as an API key.",PURPLE),
           ("4. Read the answer","A status code (200 found, 404 missing, 429 slow down, 503 try later), headers, then the body.",ORANGE)]
    y=240
    for t,d,c in steps:
        o.append(rect(30,y,980,52,fill="#fff",stroke=c,sw=1.6,rx=7))
        o.append(text(50,y+22,t,12.5,c,"bold")); o.append(text(50,y+41,d,12,INK))
        y+=62
    return svg(1040,y+15,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig34-1-anatomy-of-a-command.svg",fig_anatomy),("fig34-2-pipeline-stages.svg",fig_pipeline),
                    ("fig34-3-permissions.svg",fig_permissions),("fig34-4-http-request.svg",fig_request)]:
        open(name,"w").write(fn())
    print("ok34")
