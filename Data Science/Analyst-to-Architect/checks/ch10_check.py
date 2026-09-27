"""Chapter 10 number checks. Computes every number quoted in the chapter with pandas, independently of
the spreadsheets. Run from the book root:  python3 checks/ch10_check.py"""
import pandas as pd, numpy as np, datetime as dt, calendar

csv = "companion/ch10/riverstone_sales_export_2025.csv"
raw = pd.read_csv(csv, dtype=str, keep_default_na=False)
df = raw.copy()
df["order_date"] = pd.to_datetime(df["order_date"], format="%d-%m-%Y")
for c in ["order_id", "product_id", "quantity"]:
    df[c] = df[c].astype(int)
df["unit_price"] = df["unit_price"].astype(float)
df["discount_pct"] = df["discount_pct"].astype(float)
df["net_revenue"] = df.quantity * df.unit_price * (1 - df.discount_pct / 100)
cust = pd.DataFrame([
    ("0001","Sharma Hardware","Retail"),("0002","Patel Kitchenware","Retail"),("0003","Green Leaf Hotels","Hospitality"),
    ("0004","Coastal Foods","Wholesale"),("0005","Metro Mart","Retail"),("0006","Sunrise Caterers","Hospitality"),
    ("0007","Northgate Distributors","Wholesale"),("0008","Blue Bay Cafe","Hospitality"),("0009","Lakeview Resorts","Hospitality"),
    ("0010","City Needs Store","Retail"),("0011","Harbour Traders","Wholesale"),("0012","Fresh Bowl Kitchens","Hospitality"),
    ("0013","Om Sai Provisions","Retail"),("0014","Deccan Packaging","Wholesale"),("0015","Spice Route Restaurants","Hospitality"),
    ("0016","Home Plus","Retail"),("0017","Royal Banquets","Hospitality"),("0018","Evergreen Mart","Retail"),
    ("0019","Western Logistics","Wholesale"),("0020","Tasty Tiffins","Hospitality"),("0021","Kitchen Kraft","Retail"),
    ("0022","Festive Gifts Co","Retail"),("0023","Sea Breeze Hotel","Hospitality"),("0024","Prime Wholesale","Wholesale")],
    columns=["customer_code","customer_name","segment"])
df = df.merge(cust, on="customer_code", how="left")
ok = df[df.status != "Cancelled"]
out = {}
def show(k, v): out[k] = v; print(f"{k}: {v}")

show("lines", len(df)); show("orders", df.order_id.nunique())
show("status lines", df.status.value_counts().to_dict())
show("status orders", df.drop_duplicates("order_id").status.value_counts().to_dict())
show("cancelled orders", sorted(df[df.status=="Cancelled"].order_id.unique().tolist()))
show("cancelled net revenue", round(df[df.status=="Cancelled"].net_revenue.sum(), 2))
show("SUM all lines incl cancelled", round(df.net_revenue.sum(), 2))
show("SUM non-cancelled", round(ok.net_revenue.sum(), 2))
show("non-cancelled orders", ok.order_id.nunique())
show("row2", df.iloc[0][["order_id","order_date","customer_code","product_id","quantity","unit_price","discount_pct","status","sales_rep","net_revenue"]].tolist())
show("row5 (10003 line 2)", df.iloc[3][["order_id","product_id","quantity","unit_price","discount_pct","net_revenue"]].tolist())
show("lines with a discount", int((df.discount_pct > 0).sum()))
show("COUNTIFS Delivered & discount>0", int(((df.status=="Delivered") & (df.discount_pct>0)).sum()))
show("average net revenue per non-cancelled line", round(ok.net_revenue.mean(), 2))
show("median line", round(ok.net_revenue.median(), 2))
show("min line", ok.net_revenue.min()); show("max line", ok.net_revenue.max())
mx = ok.loc[ok.net_revenue.idxmax()]
show("max line detail", [int(mx.order_id), str(mx.order_date.date()), mx.customer_name, int(mx.product_id), int(mx.quantity), mx.unit_price, mx.discount_pct])
show("lines >= 50,000 (non-cancelled)", int((ok.net_revenue >= 50000).sum()))
show("lines >= 50,000 (all)", int((df.net_revenue >= 50000).sum()))
show("segment revenue", ok.groupby("segment").net_revenue.sum().round(2).to_dict())
show("segment orders", ok.groupby("segment").order_id.nunique().to_dict())
show("rep revenue", ok.groupby(ok.sales_rep.replace("", "(no rep)")).net_revenue.sum().round(2).to_dict())
show("rep orders", ok.groupby(ok.sales_rep.replace("", "(no rep)")).order_id.nunique().to_dict())
show("lines without rep", int((df.sales_rep=="").sum()))
tg = [300000,300000,320000,320000,320000,300000,280000,320000,380000,520000,500000,380000]
m = ok.groupby(ok.order_date.dt.month).agg(rev=("net_revenue","sum"), orders=("order_id","nunique"))
m["target"] = tg; m["pct"] = (m.rev/m.target*100).round(1); m["mom"] = (m.rev.pct_change()*100).round(1)
print(m)
show("annual target", sum(tg)); show("pct of annual target", round(ok.net_revenue.sum()/sum(tg)*100, 1))
show("months on target", m.index[m.rev >= m.target].tolist())
show("months below 80%", m.index[m.pct < 80].tolist())
show("Q4 revenue", round(m.loc[10:12].rev.sum(),2)); show("Q4 share %", round(m.loc[10:12].rev.sum()/ok.net_revenue.sum()*100,1))
# lookup example
show("0005 lookup", cust.set_index("customer_code").loc["0005","customer_name"])
# CSV damage when dates are read month-first
d = raw.order_date
day = d.str[:2].astype(int); mon = d.str[3:5].astype(int)
show("dates day<=12 (silently wrong unless day==month)", int((day<=12).sum()))
show("dates day==month (accidentally right)", int((day==mon).sum()))
show("dates day>12 (left as text)", int((day>12).sum()))
# what a month-first reading does to January revenue
wrong = df.copy()
wrong["bad_date"] = [dt.date(2025, dd, mm) if dd <= 12 else None for dd, mm in zip(day, mon)]
jan_bad = wrong[(wrong.status!="Cancelled") & wrong.bad_date.map(lambda x: x is not None and x.month==1)].net_revenue.sum()
show("January revenue after month-first damage", round(jan_bad, 2))
show("January revenue correct", round(m.loc[1].rev, 2))
# dates and serials
show("serial of 2025-01-02 (1900 system)", (dt.date(2025,1,2) - dt.date(1899,12,30)).days)
show("EOMONTH(2025-01-12,0)", "2025-01-31")
show("NETWORKDAYS 2025-12-01..2025-12-31", int(np.busday_count("2025-12-01", "2026-01-01")))
show("order 10001 weekday", dt.date(2025,1,2).strftime("%A"))
# first-line-of-order flag reconciles
show("sum of first-line flags (non-cancelled)", int((~ok.duplicated("order_id")).sum()))
# share of total for row 2
show("row2 share of total %", round(2900/ok.net_revenue.sum()*100, 3))
# text functions
show('LEN("2900 ")', len("2900 ")); show('TEXT(5,"0000")', f"{5:04d}")
# largest customer
show("top customers", ok.groupby("customer_name").net_revenue.sum().sort_values(ascending=False).head(3).round(2).to_dict())
show("November wholesale lines", int(((ok.order_date.dt.month==11) & (ok.segment=="Wholesale")).sum()))
show("November wholesale revenue", round(ok[(ok.order_date.dt.month==11) & (ok.segment=="Wholesale")].net_revenue.sum(),2))
show("Farah Khan lines", int((df.sales_rep=="Farah Khan").sum()))
show("Garden chair lines", int((df.product_id==106).sum()), )
show("max quantity", int(df.quantity.max())); show("min quantity", int(df.quantity.min()))
show("distinct discount values", sorted(df.discount_pct.unique().tolist()))
# relative-reference trap: share of export total copied down without $
j = df.net_revenue.tolist(); tail = [sum(j[i:]) for i in range(len(j))]
show("sum of shares, correct %", round(sum(x/sum(j) for x in j)*100, 1))
show("sum of shares, relative copy %", round(sum(a/b for a, b in zip(j, tail))*100, 1))
show("row3 share correct/wrong %", (round(j[1]/sum(j)*100, 3), round(j[1]/tail[1]*100, 3)))
h1 = m.loc[1:6]; h2 = m.loc[7:12]
show("H1 revenue, target, pct", (round(h1.rev.sum(),2), int(h1.target.sum()), round(h1.rev.sum()/h1.target.sum()*100,1)))
show("H2 revenue, target, pct", (round(h2.rev.sum(),2), int(h2.target.sum()), round(h2.rev.sum()/h2.target.sum()*100,1)))
show("months on target May-Dec", int((m.loc[5:12].rev >= m.loc[5:12].target).sum()))
top = df.sort_values("net_revenue", ascending=False).head(3)
show("top 3 lines", top[["order_id","customer_name","product_id","quantity","discount_pct","net_revenue","sales_rep"]].values.tolist())
show("cancelled lines", int((df.status=="Cancelled").sum()))
show("non-cancelled lines", int((df.status!="Cancelled").sum()))
wrong_ok = wrong[(wrong.status!="Cancelled") & wrong.bad_date.notna()]
show("damaged tracker: annual total of lines with (wrong) real dates", round(wrong_ok.net_revenue.sum(), 2))
show("damaged tracker: lines counted", len(wrong_ok))
show("damaged: December revenue", round(wrong_ok[wrong_ok.bad_date.map(lambda x: x.month==12)].net_revenue.sum(), 2))
show("correct December", round(m.loc[12].rev, 2))
jan_damaged_lines = raw[raw.order_date.str[:2] == "01"]
show("lines landing in damaged January", (len(jan_damaged_lines), sorted(set(jan_damaged_lines.order_date))))
show("no-rep non-cancelled lines", int(((df.sales_rep=="") & (df.status!="Cancelled")).sum()))
show("first-line flag total, all lines", df.order_id.nunique())
show("damaged total as % of real", round(1739092.25/4335471*100, 1))
