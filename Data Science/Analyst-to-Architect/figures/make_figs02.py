# Generates the SVG figures for Chapter 2. Run: python3 make_figs02.py
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.45), y2-L*math.sin(a-0.45)); p2=(x2-L*math.cos(a+0.45), y2-L*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 2.1: how big is big ----------
def fig_sizes():
    o=[]
    rows=[("1 byte","B","one English letter, digit, or space","'A' is stored as 01000001"),
          ("1 kilobyte","KB","1,000 bytes","a short plain-text email; the 4-order CSV in section 2.5 is 364 bytes"),
          ("1 megabyte","MB","1,000 KB","a phone photo is typically a few MB; 500,000 sales lines as CSV: 24 MB"),
          ("1 gigabyte","GB","1,000 MB","a feature-length film in HD is typically a few GB"),
          ("1 terabyte","TB","1,000 GB","a typical laptop or external hard drive"),
          ("1 petabyte","PB","1,000 TB","a large company's data warehouse, or a video platform's library")]
    cols=[ACC,"#1f6fa3",PURPLE,ORANGE,GREEN,"#5b6475"]
    x0=30; y=40; h=58
    for i,(name,ab,eq,ex) in enumerate(rows):
        w=110+i*34
        o.append(rect(x0,y,w,h-10,fill=cols[i],rx=6))
        o.append(text(x0+14,y+30,ab,20,"#fff","bold",family=HEAD))
        o.append(text(x0+w+18,y+20,f"{name}  =  {eq}",14,INK,"bold"))
        o.append(text(x0+w+18,y+40,ex,12.5,MUTED))
        y+=h
    o.append(text(x0,y+16,"Each step is 1,000 times the one before. (Some software counts in steps of 1,024; see section 2.2.)",12.5,MUTED,style="italic"))
    return svg(1000,y+34,"".join(o))

# ---------- Figure 2.2: row storage vs columnar storage ----------
def fig_row_vs_column():
    o=[]
    hdr=["date","customer","product","qty"]
    data=[["2025-08-30","2","105","77"],["2025-02-24","21","107","62"],["2025-11-03","7","101","15"],["2025-05-19","2","103","140"]]
    o.append(text(30,32,"CSV and Excel: stored row by row",15,ACC,"bold",family=HEAD))
    y=56
    for i,r in enumerate(data):
        x=30
        for j,v in enumerate(r):
            fill="#fdf3dc" if j==3 else "#eef4fa"
            o.append(rect(x,y,100 if j==0 else 70,28,fill=fill,stroke=RULE,sw=0.8))
            o.append(text(x+8,y+19,v,12,INK,family=MONO)); x+=(100 if j==0 else 70)
        o.append(text(x+10,y+19,f"row {i+1}",11.5,MUTED)); y+=34
    o.append(wrap(30,y+22,["To add up qty, the computer still reads every","value in every row, then throws most away."],12.3,MUTED,19))
    o.append(f'<line x1="470" y1="20" x2="470" y2="300" stroke="{RULE}" stroke-width="1.5"/>')
    X=500
    o.append(text(X,32,"Parquet: stored column by column",15,GREEN,"bold",family=HEAD))
    for j,hname in enumerate(hdr):
        yy=56+j*56
        o.append(text(X,yy+19,hname,12.5,INK,"bold",family=MONO))
        x=X+90
        for i,r in enumerate(data):
            fill="#e2f3ee" if j==3 else "#f6f9fc"
            o.append(rect(x,yy,86,28,fill=fill,stroke=RULE,sw=0.8)); o.append(text(x+8,yy+19,r[j],12,INK,family=MONO)); x+=86
    o.append(wrap(X,56+4*56+8,["To add up qty, it reads only the qty column.","Similar values sit together, so they compress well."],12.3,MUTED,19))
    return svg(960,330,"".join(o))

# ---------- Figure 2.3: an API request and response ----------
def fig_api():
    o=[]
    boxes=[(30,"Your program","a report script, an app,\nor a tool like Power BI",ACC),
           (390,"The API","checks the key,\nunderstands the request",PURPLE),
           (750,"Riverstone's database","holds the data;\nnever exposed directly",GREEN)]
    for x,t,sub,c in boxes:
        o.append(rect(x,90,220,110,fill="#fff",stroke=c,sw=1.8,rx=10))
        o.append(f'<path d="M{x},{98} a8,8 0 0 1 8,-8 H{x+212} a8,8 0 0 1 8,8 V{128} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,115,t,14.5,"#fff","bold",family=HEAD))
        for k,l in enumerate(sub.split("\n")): o.append(text(x+14,152+k*20,l,12.3,INK))
    # request
    o.append(arrow(255,118,385,118,ACC,2.2))
    o.append(text(262,70,"1  Request",13,ACC,"bold"))
    o.append(text(30,268,"What step 1 sends:",12.5,ACC,"bold"))
    o.append(rect(30,280,300,70,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(42,304,["GET /api/orders/5009","X-API-Key: demo-key-123"],12,INK,20,family=MONO))
    o.append(arrow(615,130,745,130,PURPLE,2.2)); o.append(text(622,82,"2  Query",13,PURPLE,"bold"))
    o.append(arrow(745,172,615,172,GREEN,2.2)); o.append(text(636,194,"3  Rows",13,GREEN,"bold"))
    o.append(arrow(385,176,255,176,PURPLE,2.2))
    o.append(text(270,214,"4  Response",13,PURPLE,"bold"))
    o.append(text(390,268,"What step 4 brings back:",12.5,PURPLE,"bold"))
    o.append(rect(390,280,420,100,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(402,304,["HTTP/1.0 200 OK","Content-Type: application/json","",'{ "order_id": 5009, "status": "Shipped", … }'],12,INK,20,family=MONO))
    o.append(text(30,40,"Like a restaurant: you (the program) never walk into the kitchen (the database). You give the waiter (the API) a clear order, and it brings back a dish.",12.5,MUTED,style="italic"))
    return svg(1010,400,"".join(o))

# ---------- Figure 2.4: the 3-2-1 backup rule ----------
def fig_321():
    o=[]
    items=[("3","copies of important data","the original, plus two backups",ACC),
           ("2","different types of storage","e.g. the laptop's drive and an external drive or a cloud service",PURPLE),
           ("1","copy kept somewhere else","off-site or in the cloud, safe from fire, theft, or ransomware at the office",GREEN)]
    for i,(n,t,d,c) in enumerate(items):
        x=30+i*325
        o.append(rect(x,30,305,200,fill="#fff",stroke=c,sw=1.8,rx=10))
        o.append(f'<circle cx="{x+50}" cy="85" r="34" fill="{c}"/>')
        o.append(text(x+50,98,n,34,"#fff","bold",anchor="middle",family=HEAD))
        o.append(text(x+22,150,t,14,INK,"bold"))
        words=d.split(" "); lines=[]; cur=""
        for w in words:
            if len(cur+" "+w)>38: lines.append(cur); cur=w
            else: cur=(cur+" "+w).strip()
        lines.append(cur)
        o.append(wrap(x+22,174,lines,12.3,MUTED,19))
    o.append(text(30,258,"A backup you have never restored is a hope, not a backup: test a restore regularly.",12.5,INK,"bold"))
    return svg(1010,276,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig2-1-how-big-is-big.svg",fig_sizes),("fig2-2-row-vs-column-storage.svg",fig_row_vs_column),("fig2-3-api-request-response.svg",fig_api),("fig2-4-three-two-one-backups.svg",fig_321)]:
        open(name,"w").write(fn())
    print("ok")
