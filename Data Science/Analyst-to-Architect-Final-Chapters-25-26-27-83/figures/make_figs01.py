# Generates the SVG figures for Chapter 1. Run: python3 make_figs01.py
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"

def wrap(x,y,lines,size=12.5,fill=INK,lh=19,weight="normal",family=None):
    def lead(l):
        n=len(l)-len(l.lstrip(' ')); return '\u00a0'*n+l.lstrip(' ')
    return "".join(text(x,y+i*lh,lead(l),size,fill,weight,family=family) for i,l in enumerate(lines))

# ---------- Figure 1.1: data -> information -> knowledge -> insight ----------
def fig_dikw():
    o=[]
    steps=[("DATA","Raw recorded facts",ACC,
            ["12 order rows, e.g.","5009 · 2026-02-25 · Shipped","5012 · 2026-03-15 · Pending"],"What was recorded?"),
           ("INFORMATION","Facts organized for a question",PURPLE,
            ["Revenue by month:","Jan ₹104,210","Feb ₹161,700","Mar ₹31,800"],"What happened?"),
           ("KNOWLEDGE","Understanding why",ORANGE,
            ["A few big wholesale orders","drive revenue. March had none,","and a ₹26,220 order is","still Pending."],"Why did it happen?"),
           ("INSIGHT","A conclusion someone can act on",GREEN,
            ["March is not a collapse.","Ship the pending order and","follow up with the big","wholesale buyers this week."],"So what do we do?")]
    W=232; G=18; base=440
    for i,(t,sub,c,body,q) in enumerate(steps):
        x=30+i*(W+G); top=250-i*62
        h=base-top
        o.append(rect(x+3,top+4,W,h,fill="#e9eef4",rx=8))
        o.append(rect(x,top,W,h,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x},{top+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{top+54} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,top+24,t,15,"#fff","bold",family=HEAD))
        o.append(text(x+14,top+44,sub,11.5,"#ffffff"))
        o.append(text(x+14,top+80,q,12.5,c,"bold",style="italic"))
        o.append(wrap(x+14,top+106,body,12.3,INK,19,family=MONO if i==0 else None))
        if i<3:
            ax=x+W+2; ay=top+30
            o.append(path(f"M{ax},{ay} H{ax+G-4}",stroke=MUTED,sw=2))
            o.append(f'<path d="M{ax+G-4},{ay-5} L{ax+G+2},{ay} L{ax+G-4},{ay+5} Z" fill="{MUTED}"/>')
    o.append(path(f"M30,{base+22} H{30+4*W+3*G}",stroke=RULE,sw=1.5))
    o.append(text(30,base+44,"Each step up needs more context and more thinking, and is worth more to the business.",12.5,MUTED))
    return svg(1030,500,"".join(o))

# ---------- Figure 1.2: a receipt becomes a table ----------
def fig_receipt():
    o=[]
    rx,ry,rw=30,30,300
    lines=[("Toor dal 1 kg","1 × 165","165"),("Basmati rice 5 kg","1 × 540","540"),("Milk 500 ml","4 × 28","112"),("Bath soap","3 × 45","135"),("Tea 250 g","1 × 140","140")]
    h=372
    o.append(rect(rx+3,ry+4,rw,h,fill="#e9eef4",rx=4))
    o.append(rect(rx,ry,rw,h,fill="#fffdf6",stroke="#d9cfb4",sw=1.2,rx=4))
    o.append(text(rx+rw/2,ry+30,"SAI KRUPA GENERAL STORE",13.5,INK,"bold",anchor="middle",family=MONO))
    o.append(text(rx+rw/2,ry+50,"Kothrud, Pune",11.5,MUTED,anchor="middle",family=MONO))
    o.append(text(rx+16,ry+80,"Bill No: 4417",11.5,INK,family=MONO))
    o.append(text(rx+rw-16,ry+80,"14-09-2026 18:42",11.5,INK,anchor="end",family=MONO))
    o.append(path(f"M{rx+14},{ry+94} H{rx+rw-14}",stroke="#b9ad8c",sw=1,dash="4 3"))
    yy=ry+118; ys=[]
    for n,qp,a in lines:
        o.append(rect(rx+8,yy-16,rw-16,24,fill="#fdf3dc",rx=3))
        o.append(text(rx+16,yy,n,11.5,INK,family=MONO)); o.append(text(rx+196,yy,qp,11.5,MUTED,anchor="end",family=MONO)); o.append(text(rx+rw-16,yy,a,11.5,INK,anchor="end",family=MONO))
        ys.append(yy-4); yy+=30
    o.append(path(f"M{rx+14},{yy-10} H{rx+rw-14}",stroke="#b9ad8c",sw=1,dash="4 3"))
    o.append(text(rx+16,yy+14,"TOTAL",12.5,INK,"bold",family=MONO)); o.append(text(rx+rw-16,yy+14,"₹1,092",12.5,INK,"bold",anchor="end",family=MONO))
    o.append(text(rx+16,yy+40,"Paid by: UPI",11.5,INK,family=MONO))
    o.append(text(rx+rw/2,yy+70,"Thank you! Visit again",11,MUTED,anchor="middle",family=MONO))
    # table
    X=420; Y=96
    headers=["bill_no","bill_date","item","qty","unit_price","amount","paid_by"]
    widths=[70,100,150,44,90,70,74]
    rows=[["4417","2026-09-14",n,q.split(" × ")[0],q.split(" × ")[1],a,"UPI"] for n,q,a in lines]
    t,cy,ybot=grid(X,Y,"The same bill as a table: one row per item",headers,rows,widths,subtitle="bill_no, bill_date, and paid_by repeat on every row"); o.append(t)
    for a,b in zip(ys,cy):
        o.append(path(f"M{rx+rw+2},{a} C{rx+rw+45},{a} {X-45},{b} {X-2},{b}",stroke="#c9a227",sw=1.4))
    o.append(rect(X,ybot+26,sum(widths),108,fill="#f6f9fc",stroke=RULE,rx=6))
    notes=["• Each line on the receipt became one row (a record).","• Each kind of detail became one column (a field).","• The total ₹1,092 is not a row: it can be calculated","  from the amount column whenever someone needs it."]
    o.append(wrap(X+14,ybot+50,notes,12.3,INK,23))
    return svg(1040,430,"".join(o))

# ---------- Figure 1.3: one order in three shapes ----------
def fig_three_forms():
    o=[]
    cols=[("Structured","Rows and columns with a fixed layout",ACC),("Semi-structured","Labels travel with the values",PURPLE),("Unstructured","Meaning is in the words, not a layout",ORANGE)]
    W=318; G=20; top=30; h=360
    for i,(t,sub,c) in enumerate(cols):
        x=30+i*(W+G)
        o.append(rect(x,top,W,h,fill="#fff",stroke=RULE,sw=1.2,rx=8))
        o.append(f'<path d="M{x},{top+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{top+54} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,top+24,t,15,"#fff","bold",family=HEAD)); o.append(text(x+14,top+44,sub,11.5,"#fff"))
    # structured
    x=44
    t,_,yb=grid(x,top+100,"order_items (order 5001)",["product_id","qty","price","disc_%"],[["101","20","450","0"],["103","50","120","5"]],[84,54,70,70]); o.append(t)
    t,_,yb2=grid(x,yb+44,"orders",["order_id","customer_id","order_date"],[["5001","1","2026-01-05"]],[80,94,104]); o.append(t)
    o.append(wrap(x,yb2+30,["Easy to count, sum, sort,","and join. Spreadsheets and","databases work this way."],11.8,MUTED,18))
    # semi-structured JSON
    x=30+W+G+14
    js=['{','  "order_id": 5001,','  "customer": "Sharma Hardware",','  "order_date": "2026-01-05",','  "items": [','    {"product_id": 101, "qty": 20,','     "price": 450, "disc_pct": 0},','    {"product_id": 103, "qty": 50,','     "price": 120, "disc_pct": 5}','  ]','}']
    o.append(rect(x-4,top+74,W-20,222,fill="#f6f9fc",rx=5))
    o.append(wrap(x+4,top+96,js,11.3,INK,19.5,family=MONO))
    o.append(wrap(x,top+318,["JSON from a website or app. Each","value has a label; the layout can vary."],11.8,MUTED,18))
    # unstructured email
    x=30+2*(W+G)+14
    o.append(rect(x-4,top+74,W-20,222,fill="#fffdf6",stroke="#e5dcc3",rx=5))
    em=["From: Rakesh (Sharma Hardware)","To: Neha Kulkarni","Subject: Order","","Hi Neha,","Please send 20 of the 10L storage","boxes and 50 water bottles, at the","rates you quoted. 5% off the","bottles as discussed?","","Thanks, Rakesh"]
    o.append(wrap(x+4,top+96,em,11.5,INK,19.5))
    o.append(wrap(x,top+318,["An email. A person (or an AI tool)","must read it to pull out the facts."],11.8,MUTED,18))
    return svg(1034,410,"".join(o))

# ---------- Figure 1.4: levels of measurement ----------
def fig_levels():
    o=[]
    lv=[("Nominal","Names or labels, no order","segment, city, payment method","count · most common value (mode)",ACC),
        ("Ordinal","Order matters, gaps are unknown","T-shirt size, rating 1–5, High/Medium/Low","+ rank · median · \"higher than\"",PURPLE),
        ("Interval","Equal gaps, but no true zero","temperature in °C, calendar dates","+ differences · mean",ORANGE),
        ("Ratio","Equal gaps and a true zero","revenue, quantity, weight, age","+ \"twice as much\" · % change",GREEN)]
    x0=30; y0=40; stepw=180; rowh=78
    for i,(n,d,ex,ops,c) in enumerate(lv):
        y=y0+i*rowh
        w=420+i*stepw*0.0
        o.append(rect(x0,y,170,rowh-10,fill=c,rx=7))
        o.append(text(x0+14,y+30,n,17,"#fff","bold",family=HEAD)); o.append(text(x0+14,y+52,f"Level {i+1}",11.5,"#fff"))
        o.append(rect(x0+180,y,780,rowh-10,fill="#fff",stroke=RULE,sw=1.2,rx=7))
        o.append(text(x0+196,y+26,d,13.5,INK,"bold"))
        o.append(text(x0+196,y+50,"e.g. "+ex,12.3,MUTED,style="italic"))
        o.append(rect(x0+640,y+12,306,rowh-34,fill="#f6f9fc",rx=5))
        o.append(text(x0+652,y+40,ops,12.3,c,"bold"))
    o.append(text(x0,y0+4*rowh+14,"Each level allows everything above it, plus something new. Use only the maths your level allows.",12.5,MUTED))
    return svg(1000,y0+4*rowh+30,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig1-1-data-to-insight.svg",fig_dikw),("fig1-2-receipt-to-table.svg",fig_receipt),("fig1-3-levels-of-measurement.svg",fig_levels),("fig1-4-three-shapes-of-data.svg",fig_three_forms)]:
        open(name,"w").write(fn())
    print("ok")
