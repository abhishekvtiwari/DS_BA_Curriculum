# Generates the SVG figures for Chapter 1. Run: python3 make_figs01.py
# Every figure prints at the full text width (493.2 pt), so a font of s px on a W px canvas
# prints at s * 493.2 / W pt. All canvases here are 720 px wide and the smallest font is 11 px,
# which prints at 7.5 pt (the book's minimum is 7 pt).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def wrap(x,y,lines,size=12.5,fill=INK,lh=19,weight="normal",family=None):
    def lead(l):
        n=len(l)-len(l.lstrip(' ')); return ' '*n+l.lstrip(' ')
    return "".join(text(x,y+i*lh,lead(l),size,fill,weight,family=family) for i,l in enumerate(lines))

def head_bar(x,y,w,c,r=8,h=54):
    return f'<path d="M{x},{y+r} a{r},{r} 0 0 1 {r},-{r} H{x+w-r} a{r},{r} 0 0 1 {r},{r} V{y+h} H{x} Z" fill="{c}"/>'

# ---------- Figure 1.1: data -> information -> knowledge -> insight ----------
def fig_dikw():
    o=[]
    # listed top (highest step) to bottom (first step); the step number is printed, so colour is not needed to read it
    steps=[("INSIGHT","A conclusion someone can act on",GREEN,"So what should we do?",
            ["March is not a collapse. Ship the pending order and","call the big wholesale buyers this week."],None),
           ("KNOWLEDGE","An understanding of why",ORANGE,"Why did it happen?",
            ["A few big wholesale orders drive revenue. March had","none, and a ₹26,220 order is still Pending."],None),
           ("INFORMATION","Facts organized for a question",PURPLE,"What happened?",
            ["Delivered and shipped orders by month:","Jan ₹1,04,210 · Feb ₹1,61,700 · Mar ₹31,800"],None),
           ("DATA","Raw recorded facts",ACC,"What was recorded?",
            ["12 order rows, for example:","5009 · 2026-02-25 · Shipped","5012 · 2026-03-15 · Pending"],MONO)]
    W=720; LW=214; RH=92; GAP=18; step_in=18; top=20
    n=len(steps)
    for i,(t,sub,c,q,body,fam) in enumerate(steps):
        level=n-1-i                      # 3 for INSIGHT ... 0 for DATA
        x=20+level*step_in; y=top+i*(RH+GAP)
        o.append(rect(x+3,y+4,LW,RH,fill="#e9eef4",rx=8))
        o.append(rect(x,y,LW,RH,fill=c,rx=8))
        o.append(text(x+14,y+28,f"{level+1}  {t}",15,"#fff","bold",family=HEAD))
        o.append(text(x+14,y+52,sub,11.5,"#fff"))
        bx=x+LW+10; bw=W-20-bx
        o.append(rect(bx,y,bw,RH,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(text(bx+14,y+24,q,12.5,c,"bold",style="italic"))
        if fam==MONO:
            o.append(text(bx+14,y+46,body[0],12,INK))
            o.append(wrap(bx+14,y+64,body[1:],12,INK,18,family=MONO))
        else:
            o.append(wrap(bx+14,y+48,body,12,INK,19))
        if i<n-1:   # arrow from the step below up to this one
            ax=x+LW/2-step_in/2; y1=y+RH+GAP-2; y2=y+RH+4
            o.append(path(f"M{ax},{y1} V{y2+6}",stroke=MUTED,sw=2))
            o.append(f'<path d="M{ax-5},{y2+7} L{ax},{y2} L{ax+5},{y2+7} Z" fill="{MUTED}"/>')
    yb=top+n*(RH+GAP)-GAP
    o.append(path(f"M20,{yb+18} H{W-20}",stroke=RULE,sw=1.5))
    o.append(text(20,yb+40,"Each step up needs more context and more thinking, and is worth more to the business.",12,MUTED))
    return svg(W,yb+56,"".join(o))

# ---------- Figure 1.2: a receipt becomes a table ----------
def fig_receipt():
    o=[]
    W=700
    rx,ry,rw=20,20,300
    lines=[("Toor dal 1 kg","1 × 165","165"),("Basmati rice 5 kg","1 × 540","540"),("Milk 500 ml","4 × 28","112"),("Bath soap","3 × 45","135"),("Tea 250 g","1 × 140","140")]
    h=330
    o.append(rect(rx+3,ry+4,rw,h,fill="#e9eef4",rx=4))
    o.append(rect(rx,ry,rw,h,fill="#fffdf6",stroke="#d9cfb4",sw=1.2,rx=4))
    o.append(text(rx+rw/2,ry+28,"SAI KRUPA GENERAL STORE",13.5,INK,"bold",anchor="middle",family=MONO))
    o.append(text(rx+rw/2,ry+47,"Kothrud, Pune",11.5,MUTED,anchor="middle",family=MONO))
    o.append(text(rx+14,ry+74,"Bill No: 4417",11.5,INK,family=MONO))
    o.append(text(rx+rw-14,ry+74,"14-09-2026 18:42",11.5,INK,anchor="end",family=MONO))
    o.append(path(f"M{rx+14},{ry+86} H{rx+rw-14}",stroke="#b9ad8c",sw=1,dash="4 3"))
    yy=ry+108
    for n,qp,a in lines:
        o.append(rect(rx+8,yy-16,rw-16,23,fill="#fdf3dc",rx=3))
        o.append(text(rx+14,yy,n,11.5,INK,family=MONO)); o.append(text(rx+206,yy,qp,11.5,MUTED,anchor="end",family=MONO)); o.append(text(rx+rw-14,yy,a,11.5,INK,anchor="end",family=MONO))
        yy+=28
    o.append(path(f"M{rx+14},{yy-10} H{rx+rw-14}",stroke="#b9ad8c",sw=1,dash="4 3"))
    o.append(text(rx+14,yy+14,"TOTAL",12.5,INK,"bold",family=MONO)); o.append(text(rx+rw-14,yy+14,"₹1,092",12.5,INK,"bold",anchor="end",family=MONO))
    o.append(text(rx+14,yy+40,"Paid by: UPI",11.5,INK,family=MONO))
    o.append(text(rx+rw/2,yy+66,"Thank you! Visit again",11.5,MUTED,anchor="middle",family=MONO))
    # what changed, to the right of the receipt
    nx=rx+rw+30; nw=W-20-nx
    o.append(text(nx,ry+28,"What happens to the receipt",13.5,INK,"bold",family=HEAD))
    o.append(rect(nx,ry+44,nw,176,fill="#f6f9fc",stroke=RULE,rx=6))
    notes=["• Each item line on the receipt (shaded)","  becomes one row: a record.",
           "• Each kind of detail becomes one","  column: a field.",
           "• The bill number, date and payment","  method repeat on every row.",
           "• The total ₹1,092 is not a row: it can be","  calculated from the amount column."]
    o.append(wrap(nx+14,ry+70,notes,12,INK,20))
    # arrow down to the table
    ax=W/2; o.append(path(f"M{ax},{ry+h+14} V{ry+h+44}",stroke=MUTED,sw=2))
    o.append(f'<path d="M{ax-6},{ry+h+42} L{ax},{ry+h+52} L{ax+6},{ry+h+42} Z" fill="{MUTED}"/>')
    # table
    X=20; Y=ry+h+98
    headers=["bill_no","bill_date","item","qty","unit_price","amount","paid_by"]
    widths=[76,106,166,50,100,80,82]
    rows=[["4417","2026-09-14",n,q.split(" × ")[0],q.split(" × ")[1],a,"UPI"] for n,q,a in lines]
    t,cy,ybot=grid(X,Y,"The same bill as a table: one row per item",headers,rows,widths,rowfill=["#fdf3dc"]*5,subtitle="bill_no, bill_date and paid_by repeat on every row"); o.append(t)
    return svg(W,ybot+20,"".join(o))

# ---------- Figure 1.4: one order in three shapes ----------
def fig_three_forms():
    o=[]
    W=720
    def panel(x,y,w,h,t,sub,c):
        return (rect(x,y,w,h,fill="#fff",stroke=RULE,sw=1.2,rx=8)+head_bar(x,y,w,c)+
                text(x+14,y+24,t,15,"#fff","bold",family=HEAD)+text(x+14,y+44,sub,11.5,"#fff"))
    # structured, full width on top
    y0=20; h0=210
    o.append(panel(20,y0,W-40,h0,"1  Structured","Rows and columns with a fixed layout",ACC))
    t,_,yb=grid(36,y0+100,"order_items (order 5001)",["product_id","qty","price","disc_%"],[["101","20","450","0"],["103","50","120","5"]],[88,54,70,70]); o.append(t)
    t,_,_=grid(372,y0+100,"orders",["order_id","customer_id","order_date"],[["5001","1","2026-01-05"]],[84,104,110]); o.append(t)
    o.append(text(36,yb+26,"Easy to count, sum, sort and join. Spreadsheets and databases work this way.",12,MUTED))
    # semi-structured and unstructured, side by side below
    y1=y0+h0+16; h1=356; pw=(W-40-16)/2
    x1=20; x2=20+pw+16
    o.append(panel(x1,y1,pw,h1,"2  Semi-structured","Labels travel with the values",PURPLE))
    js=['{','  "order_id": 5001,','  "customer": "Sharma Hardware",','  "order_date": "2026-01-05",','  "items": [','    {"product_id": 101, "qty": 20,','     "price": 450, "disc_pct": 0},','    {"product_id": 103, "qty": 50,','     "price": 120, "disc_pct": 5}','  ]','}']
    o.append(rect(x1+10,y1+66,pw-20,226,fill="#f6f9fc",rx=5))
    o.append(wrap(x1+18,y1+88,js,11,INK,19.5,family=MONO))
    o.append(wrap(x1+14,y1+314,["JSON from a website or app. Each value","has a label; the layout can vary."],12,MUTED,18))
    o.append(panel(x2,y1,pw,h1,"3  Unstructured","Meaning is in the words, not a layout",ORANGE))
    o.append(rect(x2+10,y1+66,pw-20,226,fill="#fffdf6",stroke="#e5dcc3",rx=5))
    em=["From: Rakesh (Sharma Hardware)","To: Neha Kulkarni","Subject: Order","","Hi Neha,","Please send 20 of the 10L storage","boxes and 50 water bottles, at the","rates you quoted. 5% off the","bottles as discussed?","","Thanks, Rakesh"]
    o.append(wrap(x2+18,y1+88,em,12,INK,19.5))
    o.append(wrap(x2+14,y1+314,["An email. A person (or an AI tool) must","read it to pull out the facts."],12,MUTED,18))
    return svg(W,y1+h1+20,"".join(o))

# ---------- Figure 1.3: levels of measurement ----------
def fig_levels():
    o=[]
    W=720
    lv=[("Nominal","Names or labels, no order","segment, city, payment method","Allows: count · most common value (mode)",ACC),
        ("Ordinal","Order matters, gaps are unknown","T-shirt size, rating 1–5, High/Medium/Low","Adds: rank · median · \"higher than\"",PURPLE),
        ("Interval","Equal gaps, but no true zero","temperature in °C, calendar dates","Adds: differences · mean",ORANGE),
        ("Ratio","Equal gaps and a true zero","revenue, quantity, weight, age","Adds: \"twice as much\" · % change",GREEN)]
    x0=20; y0=20; rowh=96; LW=150
    for i,(n,d,ex,ops,c) in enumerate(lv):
        y=y0+i*rowh
        o.append(rect(x0,y,LW,rowh-12,fill=c,rx=7))
        o.append(text(x0+14,y+34,n,17,"#fff","bold",family=HEAD)); o.append(text(x0+14,y+58,f"Level {i+1}",12,"#fff"))
        bx=x0+LW+10; bw=W-20-bx
        o.append(rect(bx,y,bw,rowh-12,fill="#fff",stroke=RULE,sw=1.2,rx=7))
        o.append(text(bx+14,y+24,d,13.5,INK,"bold"))
        o.append(text(bx+14,y+45,"e.g. "+ex,12,MUTED,style="italic"))
        o.append(rect(bx+10,y+54,bw-20,22,fill="#f6f9fc",rx=5))
        o.append(text(bx+18,y+70,ops,12,c,"bold"))
    yb=y0+4*rowh
    o.append(text(x0,yb+10,"Each level keeps every calculation of the level before it and adds one more.",12.5,MUTED))
    return svg(W,yb+28,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig1-1-data-to-insight.svg",fig_dikw),("fig1-2-receipt-to-table.svg",fig_receipt),("fig1-3-levels-of-measurement.svg",fig_levels),("fig1-4-three-shapes-of-data.svg",fig_three_forms)]:
        open(name,"w").write(fn())
    print("ok")
