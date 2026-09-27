from make_figs import *

def fig_group_vs_window():
    o=[]
    rows=[["Metro Mart","5006","14640"],["Metro Mart","5012","26220"],["Sharma Hardware","5001","14700"],["Sharma Hardware","5005","14550"],["Sharma Hardware","5011","11700"]]
    t,_,_=grid(30,60,"order_totals (5 rows)",["customer","order_id","order_revenue"],rows,[150,80,120]); o.append(t)
    o.append(text(30,238,"Same input, two different questions:",12.5,MUTED,"bold"))
    # group by result
    X=440
    t,_,yy=grid(X,60,"GROUP BY customer",["customer","total"],[["Metro Mart","40860"],["Sharma Hardware","40950"]],[150,100],color="#7a4fa0",subtitle="2 rows: the orders are collapsed"); o.append(t)
    o.append(text(X,yy+22,"SUM(order_revenue) … GROUP BY customer",11.5,MUTED,family=MONO))
    # window result
    t,_,yy2=grid(X,210,"SUM(...) OVER (PARTITION BY customer)",["customer","order_id","order_revenue","customer_total"],[r+[("40860" if r[0]=="Metro Mart" else "40950")] for r in rows],[150,80,120,120],color="#2f7d6d",subtitle="5 rows: every order kept, total added alongside"); o.append(t)
    for i in range(5):
        pass
    o.append(rect(30,258,370,120,fill="#f6f9fc",stroke=RULE,rx=6))
    for i,l in enumerate(["GROUP BY answers: what is each customer's total?",
                          "A window answers: what is each order, and",
                          "how big is it compared with its customer's total?",
                          "Windows add information without losing rows."]):
        o.append(text(46,285+i*24,l,12.5,INK,"bold" if i==3 else "normal"))
    return svg(960,380,"".join(o))

def fig_anatomy():
    o=[]
    y=60
    parts=[("AVG(revenue)","#0f5c8c","1  What to calculate"),("OVER (","#5b6475",""),("PARTITION BY category","#7a4fa0","2  Restart for each group (optional)"),("ORDER BY month","#c0662b","3  The order of rows inside each group"),("ROWS BETWEEN 2 PRECEDING AND CURRENT ROW","#2f7d6d","4  Which rows count: the frame (optional)"),(")","#5b6475","")]
    x=30
    widths=[]
    for code,c,lab in parts:
        w=len(code)*8.0+16
        o.append(rect(x,y,w,38,fill="#fff",stroke=c,sw=2,rx=6)); o.append(text(x+w/2,y+24,code,13,c,"bold",anchor="middle",family=MONO))
        if lab:
            o.append(path(f"M{x+w/2},{y+38} V{y+62}",stroke=c,sw=1.5))
        widths.append((x,w,c,lab)); x+=w+8
    # labels staggered
    ly=[y+80,y+80,y+104,y+80,y+104,y]
    for (x0,w,c,lab),yy in zip(widths,[y+82,0,y+82,y+106,y+82,0]):
        if lab: o.append(text(x0+w/2,yy,lab,12,c,"bold",anchor="middle"))
    # frame illustration
    months=[("Jan","202,640"),("Feb","253,664"),("Mar","278,008"),("Apr","210,282"),("May","329,359"),("Jun","186,928")]
    o.append(text(30,210,"The frame slides down the rows. For April, the 3-month window is February, March and April:",13,INK,"bold"))
    bx=30; by=230
    for i,(mn,v) in enumerate(months):
        infr = i in (1,2,3); cur = i==3
        fill = "#e2f3ee" if infr else "#fff"
        o.append(rect(bx,by+i*30,300,28,fill=fill,stroke="#2f7d6d" if infr else RULE,sw=1.8 if infr else 0.8,rx=3))
        o.append(text(bx+14,by+i*30+19,mn+" 2025",12.5,INK,"bold" if cur else "normal",family=MONO)); o.append(text(bx+286,by+i*30+19,v,12.5,INK,"bold" if cur else "normal",anchor="end",family=MONO))
        if cur: o.append(text(bx+312,by+i*30+19,"◄ CURRENT ROW",12,"#2f7d6d","bold"))
        if i==1: o.append(text(bx+312,by+i*30+19,"◄ 2 PRECEDING",12,"#2f7d6d"))
    o.append(rect(480,262,470,92,fill="#f6f9fc",stroke=RULE,rx=6))
    o.append(text(496,290,"moving_avg_3m for April",13,INK,"bold"))
    o.append(text(496,314,"(253,664 + 278,008 + 210,282) ÷ 3 = 247,318",13,INK,family=MONO))
    o.append(text(496,338,"In May, the frame moves on: March, April, May.",12.5,MUTED))
    return svg(1050,420,"".join(o))

def fig_ranks():
    o=[]
    rows=[["Water Bottle 1L","230","1","1","1"],["Industrial Crate","125","2","2","2"],["Food Container Set","85","3","3","3"],["Storage Box 10L","85","4","3","3"],["Storage Box 25L","60","5","5","4"],["Garden Chair","0","6","6","5"]]
    fills=[None,None,"#fff4d6","#fff4d6",None,None]
    t,cy,yy=grid(30,50,"Units sold, ranked three ways",["product_name","units","ROW_NUMBER","RANK","DENSE_RANK"],rows,[180,70,120,80,120],rowfill=fills); o.append(t)
    notes=[("ROW_NUMBER","Always 1, 2, 3, 4… Ties get different numbers,","so add a tie-breaker to ORDER BY (here: product name)."),
           ("RANK","Ties share a number, then it skips: 3, 3, 5.","Like a race: two joint third places, then fifth."),
           ("DENSE_RANK","Ties share a number, no gaps: 3, 3, 4.","Use it for 'the top 3 distinct sales levels'.")]
    for i,(h_,a,b) in enumerate(notes):
        y=70+i*72
        o.append(rect(640,y-18,380,62,fill="#f6f9fc",stroke=RULE,rx=6))
        o.append(text(654,y,h_,13,ACC,"bold",family=MONO)); o.append(text(654,y+19,a,12,INK)); o.append(text(654,y+36,b,12,MUTED))
    return svg(1050,280,"".join(o))

def fig_islands():
    o=[]
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    active={0:"24300",2:"24301",3:"24301",4:"24301",5:"24301",7:"24302",10:"24304"}
    colors={"24300":"#7a4fa0","24301":"#2f7d6d","24302":"#c0662b","24304":"#0f5c8c"}
    o.append(text(30,32,"Patel Kitchenware's order months in 2025",14,INK,"bold",family=HEAD))
    for i,m in enumerate(months):
        x=30+i*82
        if i in active:
            c=colors[active[i]]
            o.append(rect(x,50,74,40,fill=c,rx=5,extra='fill-opacity="0.18"')); o.append(rect(x,50,74,40,stroke=c,sw=2,rx=5))
            o.append(text(x+37,76,m,13,c,"bold",anchor="middle"))
        else:
            o.append(rect(x,50,74,40,fill="#fff",stroke=RULE,rx=5,extra='stroke-dasharray="4 3"')); o.append(text(x+37,76,m,13,"#9aa3b2",anchor="middle"))
    o.append(text(30,122,"The trick: month_number − row_number stays the same while months are consecutive.",13,INK,"bold"))
    rows=[["Jan","24301","1","24300"],["Mar","24303","2","24301"],["Apr","24304","3","24301"],["May","24305","4","24301"],["Jun","24306","5","24301"],["Aug","24308","6","24302"],["Nov","24311","7","24304"]]
    fills=["#efe7f6","#e2f3ee","#e2f3ee","#e2f3ee","#e2f3ee","#f8e8dc","#e3eef7"]
    t,_,_=grid(30,150,"",["month","month_number","row_number","island_id"],rows,[80,130,120,110],rowfill=fills); o.append(t)
    o.append(rect(520,160,500,140,fill="#f6f9fc",stroke=RULE,rx=6))
    for i,l in enumerate(["Each consecutive run shares one island_id.",
                          "Group by island_id to get each streak:",
                          "   Mar–Jun  →  4 months in a row (the longest)",
                          "   Jan, Aug, Nov  →  1 month each",
                          "Real uses: attendance streaks, machine uptime runs."]):
        o.append(text(536,188+i*24,l,12.5,INK if i!=2 else "#2f7d6d","bold" if i==2 else "normal"))
    return svg(1050,340,"".join(o))

if __name__=="__main__":
    for name,fn in [("fig13-1-group-by-vs-window.svg",fig_group_vs_window),("fig13-2-window-anatomy-and-frame.svg",fig_anatomy),("fig13-3-row-number-rank-dense-rank.svg",fig_ranks),("fig13-4-gaps-and-islands.svg",fig_islands)]:
        open(name,"w").write(fn())
    print("ok13")
