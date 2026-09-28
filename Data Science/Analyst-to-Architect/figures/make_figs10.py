# Generates the SVG figures for Chapter 10. Run: python3 make_figs10.py
# Numbers come from checks/ch10_check.py, checks/ch10_formula_tests.py and checks/ch10_formula_tests_v3.py.
# Every figure prints at the full text width (493.2 pt). Canvases are 680 px wide and the smallest
# font is 10 px, so all text prints at 10 x 493.2 / 680 = 7.25 pt or more (visual standard: >= 7 pt).
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; SOFT="#e9eef4"
W=680

def wrap(x,y,lines,size=11,fill=INK,lh=15,weight="normal",family=None):
    return "".join(text(x,y+i*lh,l,size,fill,weight,family=family) for i,l in enumerate(lines))

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.4):
    import math
    a=math.atan2(y2-y1,x2-x1); s=6
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

def header_bar(x,y,w,h,c,rx=7):
    return f'<path d="M{x},{y+rx} a{rx},{rx} 0 0 1 {rx},-{rx} H{x+w-rx} a{rx},{rx} 0 0 1 {rx},{rx} V{y+h} H{x} Z" fill="{c}"/>'

# ---------- Figure 10.1: anatomy of a spreadsheet window, Excel and Google Sheets ----------
def fig_anatomy():
    o=[]
    def window(x,y,title,bar_color,menu,commands,namebox):
        WW=326; H=236
        o.append(rect(x+2,y+3,WW,H,fill=SOFT,rx=7)); o.append(rect(x,y,WW,H,fill="#fff",stroke=RULE,sw=1.1,rx=7))
        o.append(header_bar(x,y,WW,24,bar_color)); o.append(text(x+10,y+17,title,11.5,"#fff","bold",family=HEAD))
        o.append(rect(x,y+24,WW,20,fill="#f3f5f8")); o.append(text(x+8,y+38,menu,10,INK))
        o.append(rect(x,y+44,WW,20,fill="#fafbfc",stroke=RULE,sw=0.6)); o.append(text(x+8,y+58,commands,10,MUTED))
        # name box + formula bar
        o.append(rect(x+6,y+70,40,19,fill="#fff",stroke=RULE)); o.append(text(x+12,y+84,namebox,10.5,INK,family=MONO))
        o.append(text(x+52,y+84,"fx",10.5,MUTED,"bold",style="italic"))
        o.append(rect(x+68,y+70,WW-74,19,fill="#fff",stroke=RULE)); o.append(text(x+74,y+84,"2025-01-05",10.5,INK,family=MONO))
        # grid: columns A to C only
        gx=x+6; gy=y+96; cw=[24,64,90,102]; rh=18
        cx=gx
        for c,wd in zip(["","A","B","C"],cw):
            o.append(rect(cx,gy,wd,rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(cx+wd/2,gy+13,c,10,MUTED,anchor="middle")); cx+=wd
        data=[["order_id","order_date","customer_code"],["10001","2025-01-02","0002"],["10002","2025-01-05","0003"],
              ["10003","2025-01-12","0005"],["10003","2025-01-12","0005"]]
        for i,r in enumerate(data):
            yy=gy+rh*(i+1); cx=gx
            o.append(rect(cx,yy,cw[0],rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(cx+12,yy+13,str(i+1),10,MUTED,anchor="middle")); cx+=cw[0]
            for j,v in enumerate(r):
                sel=(i==2 and j==1)
                o.append(rect(cx,yy,cw[j+1],rh,fill="#fff",stroke=(ACC if sel else RULE),sw=(1.8 if sel else 0.6)))
                right = i>0 and j in (0,1)
                o.append(text(cx+(cw[j+1]-5 if right else 5),yy+13,v,10,INK,"bold" if i==0 else "normal",anchor=("end" if right else "start"),family=MONO))
                cx+=cw[j+1]
        ty=y+H-26
        o.append(path(f"M{x},{ty} H{x+WW}",stroke=RULE,sw=0.8))
        tx=x+8
        for k,tname in enumerate(["Data","Customers","Products","+"]):
            wd=len(tname)*6.3+14
            o.append(rect(tx,ty+4,wd,18,fill=("#fff" if k==0 else "#eef1f5"),stroke=RULE,rx=3))
            o.append(text(tx+wd/2,ty+17,tname,10,INK if k==0 else MUTED,"bold" if k==0 else "normal",anchor="middle")); tx+=wd+5
    window(8,8,"Excel (Microsoft 365)","#1f6e43","File  Home  Insert  Formulas  Data  Review  View","Ribbon: buttons grouped by tab","B3")
    window(346,8,"Google Sheets","#1a73e8","File  Edit  View  Insert  Format  Data  Tools  Extensions","Toolbar; everything else in the menus","B3")
    labels=[(8,266,"Name box: the address of the selected cell (B3)"),(8,284,"Formula bar: what the cell really contains"),
            (346,266,"Grid: columns are letters, rows are numbers"),(346,284,"Sheet tabs: one workbook holds many sheets")]
    for x,y,s in labels: o.append(text(x,y,"• "+s,11,INK))
    return svg(W,294,"".join(o))

# ---------- Figure 10.2: what you see vs what the cell contains ----------
def fig_value_display():
    o=[]
    rows=[("A7","32,063","32062.5","Number","A format rounds the display; formulas use 32062.5",ORANGE),
          ("A5","2025-01-02","45659","Number (a date)","A date is a day count, shown as a date",GREEN),
          ("A8","0005","0005","Text","A code: as text it keeps its leading zeros",PURPLE),
          ("A4","2900","2900␣","Text","A trailing space: SUM skips it, LEN says 5",RED)]
    o.append(text(40,18,"You see",11.5,INK,"bold",family=HEAD)); o.append(text(170,18,"The cell contains",11.5,INK,"bold",family=HEAD))
    o.append(text(300,18,"Type",11.5,INK,"bold",family=HEAD)); o.append(text(400,18,"Why it matters",11.5,INK,"bold",family=HEAD))
    for i,(addr,see,real,typ,why,c) in enumerate(rows):
        y=28+i*44
        o.append(text(8,y+20,addr,10.5,MUTED,"bold",family=MONO))
        o.append(rect(40,y,106,30,fill="#fff",stroke=RULE,sw=1.1))
        right = typ.startswith("Number")
        o.append(text(140 if right else 46,y+20,see,12.5,INK,anchor=("end" if right else "start"),family=MONO))
        o.append(arrow(150,y+15,166,y+15))
        o.append(rect(170,y,118,30,fill="#f6f9fc",stroke=c,sw=1.4,rx=4)); o.append(text(178,y+20,real,12.5,c,"bold",family=MONO))
        o.append(text(300,y+20,typ,11,INK,"bold"))
        o.append(text(400,y+20,why,10.5,INK))
    o.append(text(8,214,"Check with the formula bar, =ISNUMBER(A2), =ISTEXT(A2), and =LEN(A2). Numbers align right; text aligns left.",10.5,MUTED))
    return svg(W,224,"".join(o))

# ---------- Figure 10.3: CSV import damage (three panels, stacked) ----------
def fig_csv_import():
    o=[]
    panels=[("1. The CSV file (plain text)",MUTED,["order_date,customer_code","02-01-2025,0002","12-01-2025,0005","13-01-2025,0005"],
             ["Dates written day first","Codes padded to 4 digits"],None),
            ("2. Opened with month-first dates",RED,["order_date  customer_code","2025-02-01  2","2025-12-01  5","13-01-2025  5"],
             ["✗ 125 lines: wrong real dates","✓ 10 lines: right by luck (day = month)","✗ 195 lines: dates left as text","✗ 330 lines: codes lost their zeros"],
             ["wrong date","wrong date","text"]),
            ("3. Imported with column types set",GREEN,["order_date  customer_code","2025-01-02  0002","2025-01-12  0005","2025-01-13  0005"],
             ["✓ 330 lines: real, correct dates","✓ 330 lines: codes kept as text","✓ January revenue ₹2,02,640"],None)]
    PH=96; G=10; y=8
    for t,c,lines,notes,tags in panels:
        o.append(rect(8,y,W-16,PH,fill="#fff",stroke=c,sw=1.4,rx=7))
        o.append(header_bar(8,y,W-16,22,c)); o.append(text(18,y+16,t,11.5,"#fff","bold",family=HEAD))
        for k,l in enumerate(lines):
            yy=y+40+k*15
            if tags and k>0:
                o.append(rect(16,yy-11,176,14,fill=("#f8e1e1" if tags[k-1]=="text" else "#fdf3dc"),rx=2))
                o.append(text(200,yy,"← "+tags[k-1],10,RED,"bold"))
            o.append(text(20,yy,l,10.5,INK,"bold" if k==0 else "normal",family=MONO))
        for k,n in enumerate(notes):
            o.append(text(330,y+40+k*15,n,11,INK if c==MUTED else c,"bold" if c!=MUTED else "normal"))
        y+=PH+G
    o.append(text(8,y+8,"Nothing warned about panel 2: January revenue fell from ₹2,02,640 to ₹91,649 without an error message.",10.5,INK))
    return svg(W,y+16,"".join(o))

# ---------- Figure 10.4: relative vs absolute references when copied down ----------
def fig_references():
    o=[]
    def panel(x,title,sub,c,formulas,results,verdict):
        o.append(text(x,16,title,12,c,"bold",family=HEAD)); o.append(text(x,32,sub,10.5,MUTED,style="italic"))
        wd=[30,200,94]; hdr=["row","formula in O (copied down)","result"]
        cx=x; o.append(rect(x,40,sum(wd),20,fill=c,rx=3))
        for h,w in zip(hdr,wd): o.append(text(cx+5,54,h,10,"#fff","bold",family=MONO)); cx+=w
        for i,(r,f,v) in enumerate(zip(["2","3","…","331"],formulas,results)):
            y=60+i*22; cx=x
            o.append(rect(x,y,sum(wd),22,fill="#fff",stroke=RULE,sw=0.7))
            o.append(text(cx+5,y+15,r,10.5,MUTED,family=MONO)); cx+=wd[0]
            o.append(text(cx+5,y+15,f,10.5,INK,family=MONO)); cx+=wd[1]
            o.append(text(cx+wd[2]-5,y+15,v,10.5,INK,"bold",anchor="end",family=MONO))
        y=60+4*22+8
        o.append(rect(x,y,sum(wd),38,fill=("#e2f3ee" if c==GREEN else "#f8e1e1"),rx=4))
        o.append(wrap(x+8,y+16,verdict,11,c,15,"bold"))
    panel(8,"✗ Relative: the range slides down","=J2/SUM(J2:J331), filled down",RED,
          ["=J2/SUM(J2:J331)","=J3/SUM(J3:J332)","…","=J331/SUM(J331:J660)"],["0.066%","0.476%","…","100.000%"],
          ["Shares add up to 656.8%:","every row divides by less"])
    panel(348,"✓ Absolute: $ locks the range","=J2/SUM($J$2:$J$331), filled down",GREEN,
          ["=J2/SUM($J$2:$J$331)","=J3/SUM($J$2:$J$331)","…","=J331/SUM($J$2:$J$331)"],["0.066%","0.475%","…","0.198%"],
          ["Shares add up to 100.0%:","every row divides by the same total"])
    return svg(W,206,"".join(o))

# ---------- Figure 10.5: the tracker's structure and result ----------
def fig_tracker():
    o=[]
    def box(x,y,w,t,sub,lines,c,mono=False):
        h=40+15*len(lines)+6
        o.append(rect(x,y,w,h,fill="#fff",stroke=c,sw=1.4,rx=6)); o.append(header_bar(x,y,w,20,c,6))
        o.append(text(x+8,y+15,t,11,"#fff","bold",family=HEAD)); o.append(text(x+8,y+34,sub,10,MUTED,style="italic"))
        o.append(wrap(x+8,y+50,lines,10,INK,15,family=MONO if mono else None))
        return h
    h1=box(8,8,176,"Export CSV","the ERP sales export, 2025",["330 order lines","imported with types set"],MUTED)
    h2=box(204,8,196,"Data sheet","+ 5 calculated columns",["J net_revenue","K month_start","L first_line_of_order","M customer_name","N segment"],ACC,True)
    h3=box(8,150,176,"Tracker sheet","one row per month",["SUMIFS by month","% of target, vs last month","formatting and a chart"],GREEN)
    h4=box(204,150,196,"Reps sheet","one row per rep and segment",["SUMIFS by rep and segment","drop-down selector"],PURPLE)
    o.append(arrow(184,40,202,40)); o.append(arrow(260,8+h2,120,148)); o.append(arrow(300,8+h2,300,148))
    # mini tracker table
    X=418; Y=22
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    rev=["2,02,640","2,53,664","2,78,008","2,10,282","3,29,359","1,86,928","2,32,692","3,29,282","5,58,315","6,81,071","6,33,408","4,39,824"]
    pct=[67.5,84.6,86.9,65.7,102.9,62.3,83.1,102.9,146.9,131.0,126.7,115.7]
    wd=[46,92,116]
    o.append(text(X,Y-8,"Tracker result, 2025 (₹)",11.5,INK,"bold",family=HEAD))
    o.append(rect(X,Y,sum(wd),18,fill=GREEN,rx=3)); cx=X
    for h,w in zip(["month","net_revenue","% of target"],wd): o.append(text(cx+5,Y+13,h,10,"#fff","bold",family=MONO)); cx+=w
    for i in range(12):
        y=Y+18+i*17
        f="#fff"; tc=INK; mark="  "
        if pct[i]>=100: f="#e2f3ee"; tc=GREEN; mark=" ✓"
        elif pct[i]<80: f="#f8e1e1"; tc=RED; mark=" ✗"
        o.append(rect(X,y,sum(wd),17,fill="#fff",stroke=RULE,sw=0.6)); o.append(rect(X+wd[0]+wd[1],y,wd[2],17,fill=f,stroke=RULE,sw=0.6))
        o.append(text(X+5,y+12.5,months[i],10,INK,family=MONO)); o.append(text(X+wd[0]+wd[1]-5,y+12.5,rev[i],10,INK,anchor="end",family=MONO))
        o.append(text(X+sum(wd)-8,y+12.5,f"{pct[i]:.1f}%{mark}",10,tc,"bold",anchor="end",family=MONO))
    y=Y+18+12*17
    o.append(rect(X,y,sum(wd),19,fill="#eef1f5",stroke=RULE,sw=0.8))
    o.append(text(X+5,y+13.5,"Total",10,INK,"bold",family=MONO)); o.append(text(X+wd[0]+wd[1]-5,y+13.5,"43,35,471",10,INK,"bold",anchor="end",family=MONO))
    o.append(text(X+sum(wd)-8,y+13.5,"102.3%  ",10,INK,"bold",anchor="end",family=MONO))
    o.append(text(8,288,"✓ green: on or above target.  ✗ red: below 80% of target.  No mark: 80–99%.",10.5,MUTED))
    o.append(text(8,304,"The check cell compares the tracker total with the Data sheet total: difference 0.",10.5,MUTED))
    return svg(W,312,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig10-1-spreadsheet-anatomy.svg",fig_anatomy),("fig10-2-value-vs-display.svg",fig_value_display),
                    ("fig10-4-relative-vs-absolute.svg",fig_references),("fig10-3-csv-import-damage.svg",fig_csv_import),
                    ("fig10-5-monthly-tracker.svg",fig_tracker)]:
        open(name,"w").write(fn())
    print("ok")
