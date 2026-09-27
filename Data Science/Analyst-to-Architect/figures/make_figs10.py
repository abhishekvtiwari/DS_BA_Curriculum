# Generates the SVG figures for Chapter 10. Run: python3 make_figs10.py
# Numbers come from checks/ch10_check.py and checks/ch10_formula_tests.py.
from make_figs import *
GREEN="#2f7d6d"; PURPLE="#7a4fa0"; ORANGE="#c0662b"; RED="#b23b3b"; SOFT="#e9eef4"

def wrap(x,y,lines,size=12.5,fill=INK,lh=19,weight="normal",family=None):
    return "".join(text(x,y+i*lh,l,size,fill,weight,family=family) for i,l in enumerate(lines))

def arrow(x1,y1,x2,y2,c=MUTED,sw=1.6):
    import math
    a=math.atan2(y2-y1,x2-x1); s=7
    p1=(x2-s*math.cos(a-0.45),y2-s*math.sin(a-0.45)); p2=(x2-s*math.cos(a+0.45),y2-s*math.sin(a+0.45))
    return path(f"M{x1},{y1} L{x2},{y2}",stroke=c,sw=sw)+f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}"/>'

# ---------- Figure 10.1: anatomy of a spreadsheet window, Excel and Google Sheets ----------
def fig_anatomy():
    o=[]
    def window(x,y,title,bar_color,menu,commands,sheet_tabs,namebox):
        W=470; H=330
        o.append(rect(x+3,y+4,W,H,fill=SOFT,rx=8)); o.append(rect(x,y,W,H,fill="#fff",stroke=RULE,sw=1.2,rx=8))
        o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y+30} H{x} Z" fill="{bar_color}"/>')
        o.append(text(x+14,y+20,title,12.5,"#fff","bold",family=HEAD))
        o.append(rect(x,y+30,W,26,fill="#f3f5f8")); o.append(text(x+12,y+48,menu,11.5,INK))
        o.append(rect(x,y+56,W,30,fill="#fafbfc",stroke=RULE,sw=0.6)); o.append(text(x+12,y+76,commands,11,MUTED))
        # name box + formula bar
        o.append(rect(x+8,y+92,70,22,fill="#fff",stroke=RULE)); o.append(text(x+14,y+107,namebox,11.5,INK,family=MONO))
        o.append(text(x+86,y+107,"fx",11.5,MUTED,"bold",style="italic"))
        o.append(rect(x+106,y+92,W-114,22,fill="#fff",stroke=RULE)); o.append(text(x+112,y+107,"2025-01-05",11.5,INK,family=MONO))
        # grid
        gx=x+8; gy=y+122; cw=[30,72,90,112,82,68]; rh=22
        cols=["","A","B","C","D","E"]
        cx=gx
        for c,wd in zip(cols,cw):
            o.append(rect(cx,gy,wd,rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(cx+wd/2,gy+15,c,11,MUTED,anchor="middle")); cx+=wd
        data=[["order_id","order_date","customer_code","product_id","quantity"],["10001","2025-01-02","0002","108","10"],
              ["10002","2025-01-05","0003","107","55"],["10003","2025-01-12","0005","101","25"],["10003","2025-01-12","0005","102","45"],["10004","2025-01-13","0005","101","15"]]
        for i,r in enumerate(data):
            yy=gy+rh*(i+1); cx=gx
            o.append(rect(cx,yy,cw[0],rh,fill="#eef1f5",stroke=RULE,sw=0.6)); o.append(text(cx+15,yy+15,str(i+1),11,MUTED,anchor="middle")); cx+=cw[0]
            for j,v in enumerate(r):
                sel=(i==2 and j==1)
                o.append(rect(cx,yy,cw[j+1],rh,fill="#fff",stroke=(ACC if sel else RULE),sw=(2 if sel else 0.6)))
                right = i>0 and j in (0,1,3,4)
                o.append(text(cx+(cw[j+1]-6 if right else 6),yy+15,v,11,INK,"bold" if i==0 else "normal",anchor=("end" if right else "start"),family=MONO))
                cx+=cw[j+1]
        ty=y+H-30
        o.append(path(f"M{x},{ty} H{x+W}",stroke=RULE,sw=0.8))
        tx=x+10
        for k,tname in enumerate(sheet_tabs):
            wd=len(tname)*7.2+18
            o.append(rect(tx,ty+4,wd,20,fill=("#fff" if k==0 else "#eef1f5"),stroke=RULE,rx=3))
            o.append(text(tx+wd/2,ty+18,tname,11,INK if k==0 else MUTED,"bold" if k==0 else "normal",anchor="middle")); tx+=wd+6
        return W
    window(30,40,"Excel (Microsoft 365)","#1f6e43","File  Home  Insert  Formulas  Data  Review  View","Ribbon: buttons grouped by tab (Home → Number, Styles …)",["Data","Customers","Products","+"],"B3")
    window(540,40,"Google Sheets","#1a73e8","File  Edit  View  Insert  Format  Data  Tools  Extensions","Toolbar: undo, format, borders; everything else in the menus",["Data","Customers","Products","+"],"B3")
    labels=[(30,405,"Name box: the address of the selected cell (B3)"),(30,425,"Formula bar: what the cell really contains"),
            (540,405,"Grid: columns are letters, rows are numbers"),(540,425,"Sheet tabs: one workbook (file) holds many sheets")]
    for x,y,s in labels: o.append(text(x,y,"• "+s,12.3,INK))
    o.append(text(30,24,"The same workbook open in both apps: the grid, name box, formula bar, and sheet tabs work the same way",12.5,MUTED,style="italic"))
    return svg(1040,440,"".join(o))

# ---------- Figure 10.2: what you see vs what the cell contains ----------
def fig_value_display():
    o=[]
    rows=[("32,063","32062.5","Number","A display format rounds what you see; formulas use 32062.5",ORANGE),
          ("2025-01-02","45659","Number (a date)","Dates are day counts; the format makes 45659 look like a date",GREEN),
          ("0005","0005","Text","A code, not a quantity: text keeps its leading zeros",PURPLE),
          ("2900","2900␣","Text","A trailing space makes it text: SUM ignores it, LEN says 5",RED)]
    o.append(text(30,32,"You see",13.5,INK,"bold",family=HEAD)); o.append(text(230,32,"The cell really contains",13.5,INK,"bold",family=HEAD))
    o.append(text(470,32,"Type",13.5,INK,"bold",family=HEAD)); o.append(text(640,32,"Why it matters",13.5,INK,"bold",family=HEAD))
    for i,(see,real,typ,why,c) in enumerate(rows):
        y=52+i*70
        o.append(rect(30,y,150,40,fill="#fff",stroke=RULE,sw=1.2))
        right = typ.startswith("Number")
        o.append(text(170 if right else 40,y+26,see,15,INK,anchor=("end" if right else "start"),family=MONO))
        o.append(arrow(188,y+20,222,y+20))
        o.append(rect(230,y,210,40,fill="#f6f9fc",stroke=c,sw=1.5,rx=4)); o.append(text(242,y+26,real,15,c,"bold",family=MONO))
        o.append(rect(470,y+8,140,24,fill="#fff",stroke=c,rx=12)); o.append(text(540,y+24,typ,11.5,c,"bold",anchor="middle"))
        o.append(text(640,y+25,why,12.3,INK))
    o.append(text(30,340,"Check with the formula bar, =ISNUMBER(A1), =ISTEXT(A1), and =LEN(A1). Numbers align right by default; text aligns left.",12.5,MUTED))
    return svg(1060,360,"".join(o))

# ---------- Figure 10.4: relative vs absolute references when copied down ----------
def fig_references():
    o=[]
    def panel(x,title,sub,c,formulas,results,verdict):
        o.append(text(x,34,title,14,c,"bold",family=HEAD)); o.append(text(x,54,sub,11.5,MUTED,style="italic"))
        hdr=["row","formula in O (copied down)","result"]; wd=[44,300,110]
        cx=x; o.append(rect(x,68,sum(wd),24,fill=c,rx=4))
        for h,w in zip(hdr,wd): o.append(text(cx+8,85,h,11,"#fff","bold",family=MONO)); cx+=w
        for i,(r,f,v) in enumerate(zip(["2","3","…","331"],formulas,results)):
            y=92+i*28; cx=x
            o.append(rect(x,y,sum(wd),28,fill="#fff",stroke=RULE,sw=0.8))
            o.append(text(cx+8,y+18,r,11.5,MUTED,family=MONO)); cx+=wd[0]
            o.append(text(cx+8,y+18,f,11.3,INK,family=MONO)); cx+=wd[1]
            o.append(text(cx+wd[2]-8,y+18,v,11.5,INK,"bold",anchor="end",family=MONO))
        o.append(rect(x,92+4*28+10,sum(wd),30,fill=("#e2f3ee" if c==GREEN else "#f8e1e1"),rx=5))
        o.append(text(x+10,92+4*28+30,verdict,12.3,c,"bold"))
    panel(30,"Relative: the range slides down","=J2/SUM(J2:J331) filled from O2 to O331",RED,
          ["=J2/SUM(J2:J331)","=J3/SUM(J3:J332)","…","=J331/SUM(J331:J660)"],["0.066%","0.476%","…","100.000%"],
          "Shares add up to 656.8%: every row divides by less")
    panel(540,"Absolute: $ locks the range","=J2/SUM($J$2:$J$331) filled from O2 to O331",GREEN,
          ["=J2/SUM($J$2:$J$331)","=J3/SUM($J$2:$J$331)","…","=J331/SUM($J$2:$J$331)"],["0.066%","0.475%","…","0.198%"],
          "Shares add up to 100.0%: every row divides by the same total")
    o.append(text(30,290,"Press F4 (Windows) or Cmd+T (Mac Excel) while the cursor is in a reference to cycle J2 → $J$2 → J$2 → $J2. Google Sheets uses F4 too.",12.3,MUTED))
    return svg(1040,305,"".join(o))

# ---------- Figure 10.3: CSV import damage ----------
def fig_csv_import():
    o=[]
    cols=[("The CSV file (plain text)",MUTED,["order_date,customer_code","02-01-2025,0002","12-01-2025,0005","13-01-2025,0005"],
           ["Dates written day first","Codes padded to 4 digits"]),
          ("Opened with month-first dates",RED,["order_date   customer_code","2025-02-01   2","2025-12-01   5","13-01-2025   5"],
           ["125 lines: wrong real dates","10 lines: right by luck (day = month)","195 lines: dates left as text","330 lines: codes lost their zeros"]),
          ("Imported with column types set",GREEN,["order_date   customer_code","2025-01-02   0002","2025-01-12   0005","2025-01-13   0005"],
           ["330 lines: real, correct dates","330 lines: codes kept as text","January revenue ₹202,640 ✓"])]
    W=318; G=22
    for i,(t,c,lines,notes) in enumerate(cols):
        x=30+i*(W+G); y=40
        o.append(rect(x+3,y+4,W,300,fill=SOFT,rx=8)); o.append(rect(x,y,W,300,fill="#fff",stroke=c,sw=1.6,rx=8))
        o.append(f'<path d="M{x},{y+8} a8,8 0 0 1 8,-8 H{x+W-8} a8,8 0 0 1 8,8 V{y+36} H{x} Z" fill="{c}"/>')
        o.append(text(x+14,y+24,t,13.5,"#fff","bold",family=HEAD))
        for k,l in enumerate(lines):
            yy=y+68+k*28
            if k>0: o.append(rect(x+10,yy-18,W-20,24,fill=("#fdf3dc" if (i==1 and k<3) else ("#f8e1e1" if i==1 else "#f6f9fc")),rx=3))
            o.append(text(x+16,yy,l,12,INK,"bold" if k==0 else "normal",family=MONO))
        for k,n in enumerate(notes):
            o.append(text(x+16,y+200+k*24,"• "+n,12.3,c if i else INK))
        if i<2: o.append(arrow(x+W+2,y+150,x+W+G-2,y+150))
    o.append(text(30,24,"The same export, three ways (330 order lines). Counts are measured on Riverstone's 2025 export.",12.5,MUTED,style="italic"))
    o.append(text(30,370,"Month-first reading turns 2 January into 1 February, and January revenue drops from ₹202,640 to ₹91,649 without any error message.",12.3,INK))
    return svg(1040,385,"".join(o))

# ---------- Figure 10.5: the tracker's structure ----------
def fig_tracker():
    o=[]
    boxes=[(30,"Export CSV","the ERP sales export, 2025",["330 order lines","imported with types set"],MUTED),
           (250,"Data sheet","+ 5 calculated columns",["J net_revenue","K month_start","L first_line_of_order","M customer_name (XLOOKUP)","N segment (XLOOKUP)"],ACC),
           (470,"Tracker sheet","one row per month",["SUMIFS by month","% of target, vs previous month","conditional formatting, chart"],GREEN),
           (470,"Reps sheet","one row per rep and segment",["SUMIFS by rep and segment","drop-down selector"],PURPLE)]
    ys=[60,60,40,210]
    for (x,t,sub,lines,c),y in zip(boxes,ys):
        h=36+22*len(lines)+26
        o.append(rect(x,y,200,h,fill="#fff",stroke=c,sw=1.6,rx=8)); o.append(rect(x,y,200,30,fill=c,rx=8)); o.append(rect(x,y+18,200,12,fill=c))
        o.append(text(x+12,y+20,t,13,"#fff","bold",family=HEAD)); o.append(text(x+12,y+48,sub,11,MUTED,style="italic"))
        o.append(wrap(x+12,y+72,lines,11.3,INK,22,family=MONO if c==ACC else None))
    o.append(arrow(232,110,248,110)); o.append(arrow(452,110,468,90)); o.append(arrow(452,150,468,250))
    # mini tracker table
    X=700; Y=58
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    rev=[202640,253664,278008,210282,329359,186928,232692,329282,558315,681071,633408,439824]
    pct=[67.5,84.6,86.9,65.7,102.9,62.3,83.1,102.9,146.9,131.0,126.7,115.7]
    hdr=["month","net_revenue","% target"]; wd=[64,112,86]
    o.append(text(X,Y-12,"Tracker result (2025)",13.5,INK,"bold",family=HEAD))
    o.append(rect(X,Y,sum(wd),22,fill=GREEN,rx=4)); cx=X
    for h,w in zip(hdr,wd): o.append(text(cx+8,Y+15,h,11,"#fff","bold",family=MONO)); cx+=w
    for i in range(12):
        y=Y+22+i*21
        f="#fff"; tc=INK
        if pct[i]>=100: f="#e2f3ee"; tc=GREEN
        elif pct[i]<80: f="#f8e1e1"; tc=RED
        o.append(rect(X,y,sum(wd),21,fill="#fff",stroke=RULE,sw=0.6)); o.append(rect(X+wd[0]+wd[1],y,wd[2],21,fill=f,stroke=RULE,sw=0.6))
        o.append(text(X+8,y+15,months[i],11,INK,family=MONO)); o.append(text(X+wd[0]+wd[1]-8,y+15,f"{rev[i]:,}",11,INK,anchor="end",family=MONO))
        o.append(text(X+sum(wd)-8,y+15,f"{pct[i]:.1f}%",11,tc,"bold",anchor="end",family=MONO))
    y=Y+22+12*21
    o.append(rect(X,y,sum(wd),23,fill="#eef1f5",stroke=RULE,sw=0.8))
    o.append(text(X+8,y+16,"Total",11,INK,"bold",family=MONO)); o.append(text(X+wd[0]+wd[1]-8,y+16,"4,335,471",11,INK,"bold",anchor="end",family=MONO)); o.append(text(X+sum(wd)-8,y+16,"102.3%",11,INK,"bold",anchor="end",family=MONO))
    o.append(text(30,385,"Green: on target. Red: below 80% of target. The check cell compares the tracker total with the Data sheet total (difference 0).",12.3,MUTED))
    return svg(1000,400,"".join(o))

if __name__ == "__main__":
    for name,fn in [("fig10-1-spreadsheet-anatomy.svg",fig_anatomy),("fig10-2-value-vs-display.svg",fig_value_display),
                    ("fig10-4-relative-vs-absolute.svg",fig_references),("fig10-3-csv-import-damage.svg",fig_csv_import),
                    ("fig10-5-monthly-tracker.svg",fig_tracker)]:
        open(name,"w").write(fn())
    print("ok")
