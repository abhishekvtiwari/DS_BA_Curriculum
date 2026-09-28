# Generates the SVG figures for Chapter 2. Run: python3 make_figs02.py
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas
# prints at s * 493.2 / W pt. Canvases here are 660-720 px wide and the smallest font is 11 px,
# which prints at 7.5 pt or more (the book's minimum is 7 pt).
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"
DARKGREY="#414a5a"   # darker than MUTED, for secondary text that must still read in print

def arrow(x1,y1,x2,y2,c=MUTED,sw=2):
    import math
    a=math.atan2(y2-y1,x2-x1); L=9
    p1=(x2-L*math.cos(a-0.45), y2-L*math.sin(a-0.45)); p2=(x2-L*math.cos(a+0.45), y2-L*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 2.1: how big is big ----------
def fig_sizes():
    o=[]
    W=720
    rows=[("1 byte","B","one English letter, digit, or space","'A' is stored as 01000001"),
          ("1 kilobyte","KB","1,000 bytes","a short plain-text email; the 4-order CSV in section 2.5 is 364 bytes"),
          ("1 megabyte","MB","1,000 KB","a phone photo is typically a few MB"),
          ("1 gigabyte","GB","1,000 MB","a feature-length film in HD is typically a few GB"),
          ("1 terabyte","TB","1,000 GB","a typical laptop or external hard drive"),
          ("1 petabyte","PB","1,000 TB","a large company's data warehouse, or a video platform's library")]
    cols=[ACC,"#1f6fa3",PURPLE,ORANGE,GREEN,"#5b6475"]
    x0=20; y=20; h=58; tx=x0+200
    for i,(name,ab,eq,ex) in enumerate(rows):
        w=64+i*26            # the bar grows with each step; the label inside names the unit
        o.append(rect(x0,y,w,h-12,fill=cols[i],rx=6))
        o.append(text(x0+12,y+30,ab,18,"#fff","bold",family=HEAD))
        o.append(text(tx,y+18,f"{name}  =  {eq}",14,INK,"bold"))
        o.append(text(tx,y+38,ex,12,DARKGREY))
        y+=h
    o.append(wrap(x0,y+14,["Each step is 1,000 times the one before.","(Some software counts in steps of 1,024; see the Watch out box below.)"],12,DARKGREY,18))
    return svg(W,y+44,"".join(o))

# ---------- Figure 2.2: row storage vs columnar storage ----------
def fig_row_vs_column():
    o=[]
    W=660
    hdr=["date","customer","product","qty"]
    data=[["2025-08-30","2","105","77"],["2025-02-24","21","107","62"],["2025-11-03","7","101","15"],["2025-05-19","2","103","140"]]
    # top: row by row
    o.append(text(20,30,"CSV and Excel: stored row by row",15,ACC,"bold",family=HEAD))
    widths=[96,78,72,56]; y=46
    x=20
    for j,hn in enumerate(hdr):
        o.append(text(x+8,y+14,hn,11.5,MUTED,"bold",family=MONO)); x+=widths[j]
    y+=22
    for i,r in enumerate(data):
        x=20
        for j,v in enumerate(r):
            q=(j==3)
            o.append(rect(x,y,widths[j],26,fill="#fdf3dc" if q else "#eef4fa",stroke=RULE,sw=0.8))
            o.append(text(x+8,y+18,v,12,INK,"bold" if q else "normal",family=MONO)); x+=widths[j]
        o.append(text(x+10,y+18,f"row {i+1}",11.5,MUTED)); y+=30
    o.append(wrap(410,86,["To add up qty, the computer","still reads every value in every","row, then throws most away."],12,INK,19))
    ymid=y+12
    o.append(f'<line x1="20" y1="{ymid}" x2="{W-20}" y2="{ymid}" stroke="{RULE}" stroke-width="1.5"/>')
    # bottom: column by column
    Y=ymid+36
    o.append(text(20,Y,"Parquet: stored column by column",15,GREEN,"bold",family=HEAD))
    for j,hname in enumerate(hdr):
        yy=Y+16+j*36; q=(j==3)
        o.append(text(20,yy+18,hname,12.5,INK,"bold",family=MONO))
        x=110
        for i,r in enumerate(data):
            o.append(rect(x,yy,92,26,fill="#e2f3ee" if q else "#f6f9fc",stroke=RULE,sw=0.8))
            o.append(text(x+8,yy+18,r[j],12,INK,"bold" if q else "normal",family=MONO)); x+=92
    o.append(wrap(494,Y+36,["To add up qty, it reads","only the qty column.","Similar values sit","together, so they","compress well."],12,INK,19))
    return svg(W,Y+16+4*36+14,"".join(o))

# ---------- Figure 2.3: an API request and response ----------
def fig_api():
    o=[]
    W=720
    o.append(wrap(20,26,["Like a restaurant: you (the program) never walk into the kitchen (the database).","You give the waiter (the API) a clear order, and it brings back a dish."],12.5,INK,19,family=None))
    bw=186; gap=(W-40-3*bw)/2; top=96; bh=106
    boxes=[("Your program",["a report script, an app,","or a tool like Power BI"],ACC),
           ("The API",["checks the key,","understands the request"],PURPLE),
           ("The database",["holds Riverstone's orders;","never opened to outsiders"],GREEN)]
    xs=[20+i*(bw+gap) for i in range(3)]
    for x,(t,sub,c) in zip(xs,boxes):
        o.append(rect(x,top,bw,bh,fill="#fff",stroke=c,sw=1.8,rx=10))
        o.append(f'<path d="M{x},{top+8} a8,8 0 0 1 8,-8 H{x+bw-8} a8,8 0 0 1 8,8 V{top+36} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,top+24,t,14,"#fff","bold",family=HEAD))
        for k,l in enumerate(sub): o.append(text(x+14,top+62+k*20,l,12,INK))
    g1=xs[0]+bw; g2=xs[1]+bw
    # 1 request (program -> API), 4 response (API -> program)
    o.append(arrow(g1+4,top+30,xs[1]-4,top+30,ACC,2.2))
    o.append(arrow(xs[1]-4,top+80,g1+4,top+80,PURPLE,2.2))
    # 2 query (API -> database), 3 rows (database -> API)
    o.append(arrow(g2+4,top+30,xs[2]-4,top+30,PURPLE,2.2))
    o.append(arrow(xs[2]-4,top+80,g2+4,top+80,GREEN,2.2))
    o.append(text((g1+xs[1])/2,top-10,"1  Request →",13,ACC,"bold",anchor="middle"))
    o.append(text((g2+xs[2])/2,top-10,"2  Query →",13,PURPLE,"bold",anchor="middle"))
    o.append(text((g2+xs[2])/2,top+bh+20,"← 3  Rows",13,GREEN,"bold",anchor="middle"))
    o.append(text((g1+xs[1])/2,top+bh+20,"← 4  Response",13,PURPLE,"bold",anchor="middle"))
    # the two messages
    y2=top+bh+54
    o.append(text(20,y2,"What step 1 sends:",12.5,ACC,"bold"))
    o.append(rect(20,y2+12,290,66,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(32,y2+38,["GET /api/orders/5009","X-API-Key: demo-key-123"],12,INK,20,family=MONO))
    o.append(text(330,y2,"What step 4 brings back:",12.5,PURPLE,"bold"))
    o.append(rect(330,y2+12,W-20-330,100,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(wrap(342,y2+38,["HTTP/1.0 200 OK","Content-Type: application/json","",'{ "order_id": 5009, "status": "Shipped", … }'],12,INK,20,family=MONO))
    return svg(W,y2+128,"".join(o))

# ---------- Figure 2.4: the 3-2-1 backup rule ----------
def fig_321():
    o=[]
    W=680
    items=[("3","copies of important data","the original, plus two backups",ACC),
           ("2","different types of storage","for example the laptop's drive and an external drive or a cloud service",PURPLE),
           ("1","copy kept somewhere else","off-site or in the cloud, safe from fire, theft, or ransomware at the office",GREEN)]
    y=20; rh=78
    for n,t,d,c in items:
        o.append(rect(20,y,W-40,rh-10,fill="#fff",stroke=c,sw=1.8,rx=10))
        o.append(f'<circle cx="{20+40}" cy="{y+(rh-10)/2}" r="25" fill="{c}"/>')
        o.append(text(60,y+(rh-10)/2+10,n,28,"#fff","bold",anchor="middle",family=HEAD))
        o.append(text(104,y+28,t,14,INK,"bold"))
        o.append(text(104,y+50,d,12,DARKGREY))
        y+=rh
    o.append(wrap(20,y+14,["A backup you have never restored is a hope, not a backup:","test a restore regularly."],12.5,INK,19,weight="bold"))
    return svg(W,y+46,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig2-1-how-big-is-big.svg",fig_sizes),("fig2-2-row-vs-column-storage.svg",fig_row_vs_column),("fig2-3-api-request-response.svg",fig_api),("fig2-4-three-two-one-backups.svg",fig_321)]:
        open(name,"w").write(fn())
    print("ok")
