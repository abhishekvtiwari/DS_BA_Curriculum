# Generates the SVG figures for Chapter 3. Run: python3 make_figs03.py
from make_figs import *
from make_figs01 import wrap
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; TEAL="#1f6fa3"; GREY="#5b6475"

def head_box(x,y,w,h,title,color,lines,size=12):
    o=[rect(x+2,y+3,w,h,fill="#e9eef4",rx=8), rect(x,y,w,h,fill="#fff",stroke=color,sw=1.6,rx=8),
       f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+w-8} a8,8 0 0 1 8,8 V{y+34} H{x} Z" fill="{color}"/>',
       text(x+12,y+23,title,13.5,"#fff","bold",family=HEAD)]
    o.append(wrap(x+12,y+56,lines,size,INK,18))
    return "".join(o)

# ---------- Figure 3.1: departments and the data they create ----------
def fig_departments():
    o=[]
    deps=[("Sales",ACC,["enquiries (leads), quotes,","sales orders, customer visits"]),
          ("Marketing",PURPLE,["campaigns, website visits,","trade-fair contacts"]),
          ("Purchasing",ORANGE,["suppliers, purchase orders,","goods received"]),
          ("Production",GREEN,["production plans, machine","runs, output, scrap"]),
          ("Warehouse & dispatch",TEAL,["stock levels, picking lists,","delivery challans, deliveries"]),
          ("Finance",RED,["invoices, payments, expenses,","budgets, tax records"]),
          ("HR",GREY,["employees, attendance,","payroll, hiring"]),
          ("Customer support",ORANGE,["complaints, tickets, returns,","resolution times"])]
    W=232; H=92; G=16
    for i,(t,c,l) in enumerate(deps):
        r,cidx=divmod(i,4)
        x=30+cidx*(W+G); y=30+r*(H+84)
        o.append(head_box(x,y,W,H,t,c,l))
    cx=30+2*(W+G)-G/2; cy=30+H+42
    o.append(rect(cx-190,cy-24,380,48,fill=INK,rx=24))
    o.append(text(cx,cy+6,"Management uses all of it to decide",14,"#fff","bold",anchor="middle",family=HEAD))
    for cidx in range(4):
        x=30+cidx*(W+G)+W/2
        o.append(path(f"M{x},{30+H} V{cy-24}",stroke=RULE,sw=1.5,dash="4 3"))
        o.append(path(f"M{x},{30+H+84} V{cy+24}",stroke=RULE,sw=1.5,dash="4 3"))
    return svg(30*2+4*W+3*G, 30+2*H+84+30, "".join(o))

# ---------- Figure 3.2: one order from enquiry to cash ----------
STEPS=[("22 Oct 2025","Enquiry","Rakesh fills in the website form","CRM: new lead",ACC,False),
       ("4 Nov 2025","New customer","Credit check; 30-day terms","ERP: customer 1",ACC,False),
       ("22 Dec 2025","Quote","Neha sends prices by email","CRM: quote Q-2025-118",ACC,True),
       ("5 Jan 2026","Order","Rakesh emails; Neha re-types it","ERP: order 5001",PURPLE,True),
       ("5 Jan 2026","Stock check","Boxes and bottles made to stock at Taloja","ERP: stock reserved",GREEN,True),
       ("6 Jan 2026","Dispatch","Bhiwandi Main picks, packs, ships","ERP: delivery challan",TEAL,False),
       ("6 Jan 2026","Invoice","Raised when the order ships","ERP: invoice 9001",RED,False),
       ("8 Jan 2026","Delivery","Rakesh signs the proof of delivery","Status: Delivered",TEAL,True),
       ("2 Feb 2026","Payment","Bank transfer; finance matches it","ERP: payment 1",RED,True),
       ("3 Feb 2026","Report","January sales report","Report: Jan ₹104,210",GREY,True)]

def fig_order_to_cash(mark_manual=False):
    o=[]
    W=178; H=150; G=20; x0=30; y0=40
    for i,(d,t,who,rec,c,manual) in enumerate(STEPS):
        r,cidx=divmod(i,5)
        x=x0+cidx*(W+G); y=y0+r*(H+60)
        stroke = RED if (mark_manual and manual) else c
        o.append(rect(x+2,y+3,W,H,fill="#e9eef4",rx=8))
        o.append(rect(x,y,W,H,fill="#fdecec" if (mark_manual and manual) else "#fff",stroke=stroke,sw=2 if (mark_manual and manual) else 1.5,rx=8))
        o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y+30} H{x} Z" fill="{c}"/>')
        o.append(text(x+10,y+20,f"{i+1}  {t}",13,"#fff","bold",family=HEAD))
        o.append(text(x+10,y+50,d,11.5,MUTED,"bold"))
        words=who.split(); lines=[]; cur=""
        for w in words:
            if len(cur+" "+w)>24: lines.append(cur); cur=w
            else: cur=(cur+" "+w).strip()
        lines.append(cur)
        o.append(wrap(x+10,y+72,lines,11.5,INK,17))
        o.append(rect(x+8,y+H-38,W-16,28,fill="#f6f9fc",rx=4))
        o.append(text(x+14,y+H-19,rec,10.5,INK,family=MONO))
        if mark_manual and manual:
            o.append(f'<circle cx="{x+W-14}" cy="{y+45}" r="10" fill="{RED}"/>')
            o.append(text(x+W-14,y+49.5,"!",13,"#fff","bold",anchor="middle"))
        if cidx<4:
            o.append(path(f"M{x+W+2},{y+H/2} H{x+W+G-4}",stroke=MUTED,sw=2))
            o.append(f'<path d="M{x+W+G-4},{y+H/2-5} L{x+W+G+1},{y+H/2} L{x+W+G-4},{y+H/2+5} Z" fill="{MUTED}"/>')
    # wrap arrow from step 5 to 6
    xr=x0+4*(W+G)+W/2; xl=x0+W/2; ym=y0+H+30
    o.append(path(f"M{xr},{y0+H+2} V{ym} H{xl} V{y0+H+60-4}",stroke=MUTED,sw=2))
    o.append(f'<path d="M{xl-5},{y0+H+60-6} L{xl},{y0+H+60+1} L{xl+5},{y0+H+60-6} Z" fill="{MUTED}"/>')
    ybot=y0+2*H+60
    if mark_manual:
        o.append(f'<circle cx="{x0+10}" cy="{ybot+30}" r="10" fill="{RED}"/>'); o.append(text(x0+10,ybot+34.5,"!",13,"#fff","bold",anchor="middle"))
        o.append(text(x0+28,ybot+35,"A person copies, re-types, or checks data by hand at this step",12.5,INK,"bold"))
    else:
        o.append(text(x0,ybot+35,"Ten steps and more than three months from a website enquiry to one line in a monthly report.",12.5,MUTED,style="italic"))
    return svg(x0*2+5*W+4*G, ybot+52, "".join(o))

# ---------- Figure 3.4: bookings, billings, collections ----------
def fig_bbc():
    o=[]
    months=["January","February","March"]
    data={"Booked (orders placed)":[116210,161700,58020],"Billed (invoiced)":[104210,161700,31800],"Collected (cash in)":[0,64700,132550]}
    cols=[ACC,PURPLE,GREEN]
    X0=90; Y0=330; Hmax=260; vmax=180000; gw=250; bw=58
    for v in range(0,180001,40000):
        y=Y0-v/vmax*Hmax
        o.append(path(f"M{X0-6},{y} H{X0+3*gw}",stroke="#eef1f5",sw=1))
        o.append(text(X0-12,y+4,f"₹{v:,}",11,MUTED,anchor="end"))
    for i,m in enumerate(months):
        gx=X0+i*gw+26
        for j,(k,vals) in enumerate(data.items()):
            v=vals[i]; h=v/vmax*Hmax; x=gx+j*(bw+8)
            o.append(rect(x,Y0-h,bw,h,fill=cols[j],rx=3))
            o.append(text(x+bw/2,Y0-h-7,f"₹{v:,}",10.5,INK,"bold",anchor="middle"))
        o.append(text(gx+(3*bw+16)/2,Y0+22,m+" 2026",12.5,INK,"bold",anchor="middle"))
    o.append(path(f"M{X0-6},{Y0} H{X0+3*gw}",stroke=MUTED,sw=1.2))
    lx=X0
    for j,k in enumerate(data):
        o.append(rect(lx,Y0+44,14,14,fill=cols[j],rx=2)); o.append(text(lx+20,Y0+56,k,12.5,INK)); lx+=240
    o.append(text(X0,24,"Riverstone, first quarter of 2026: three different numbers for \"sales\"",14,INK,"bold",family=HEAD))
    return svg(X0+3*gw+30, Y0+76, "".join(o))

if __name__ == "__main__":
    for name,fn in [("fig3-1-departments-and-their-data.svg",fig_departments),
                    ("fig3-2-one-order-enquiry-to-cash.svg",lambda: fig_order_to_cash(False)),
                    ("fig3-4-where-manual-work-hides.svg",lambda: fig_order_to_cash(True)),
                    ("fig3-3-booked-billed-collected.svg",fig_bbc)]:
        open(name,"w").write(fn())
    print("ok")
