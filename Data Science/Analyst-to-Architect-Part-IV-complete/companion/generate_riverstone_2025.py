"""Generates riverstone_2025_setup.sql: one year (2025) of fictional Riverstone Supplies data
for Chapter 13. Deterministic: the same seed always produces the same data."""
import random, datetime as dt
random.seed(20251)
D = dt.date

customers = [
 # id, name, city, segment, signup, profile, rep, churn_month
 (1,"Sharma Hardware","Mumbai","Retail",D(2024,11,4),"steady",3,None),
 (2,"Patel Kitchenware","Ahmedabad","Retail",D(2024,12,15),"occasional",3,None),
 (3,"Green Leaf Hotels","Pune","Hospitality",D(2024,9,8),"steady",5,None),
 (4,"Coastal Foods","Chennai","Wholesale",D(2024,10,20),"big",4,None),
 (5,"Metro Mart","Mumbai","Retail",D(2024,12,22),"steady",4,None),
 (6,"Sunrise Caterers","Nagpur","Hospitality",D(2025,2,3),"churn",None,6),
 (7,"Northgate Distributors","Delhi","Wholesale",D(2025,2,17),"big",5,None),
 (8,"Blue Bay Cafe","Pune","Hospitality",D(2025,3,1),"occasional",3,None),
 (9,"Lakeview Resorts","Udaipur","Hospitality",D(2024,8,12),"seasonal",5,None),
 (10,"City Needs Store","Jaipur","Retail",D(2024,12,5),"churn",4,4),
 (11,"Harbour Traders","Kochi","Wholesale",D(2025,4,9),"steady",4,None),
 (12,"Fresh Bowl Kitchens","Bengaluru","Hospitality",D(2025,2,20),"steady",3,None),
 (13,"Om Sai Provisions","Nashik","Retail",D(2025,3,14),"churn",3,8),
 (14,"Deccan Packaging","Hyderabad","Wholesale",D(2025,5,6),"big",5,None),
 (15,"Spice Route Restaurants","Kolkata","Hospitality",D(2025,6,2),"steady",5,None),
 (16,"Home Plus","Surat","Retail",D(2025,6,18),"occasional",4,None),
 (17,"Royal Banquets","Lucknow","Hospitality",D(2025,7,7),"seasonal",3,None),
 (18,"Evergreen Mart","Indore","Retail",D(2025,7,21),"steady",4,None),
 (19,"Western Logistics","Mumbai","Wholesale",D(2025,8,11),"big",5,None),
 (20,"Tasty Tiffins","Pune","Hospitality",D(2025,8,25),"churn",3,10),
 (21,"Kitchen Kraft","Bengaluru","Retail",D(2025,9,3),"steady",4,None),
 (22,"Festive Gifts Co","Delhi","Retail",D(2025,9,15),"seasonal",None,None),
 (23,"Sea Breeze Hotel","Goa","Hospitality",D(2025,10,6),"steady",5,None),
 (24,"Prime Wholesale","Ahmedabad","Wholesale",D(2025,11,10),"big",4,None),
]
products = [
 (101,"Storage Box 10L","Storage",430,300),(102,"Storage Box 25L","Storage",750,540),(103,"Water Bottle 1L","Kitchen",115,70),
 (104,"Food Container Set","Kitchen",620,430),(105,"Industrial Crate","Industrial",1400,1100),(106,"Garden Chair","Furniture",1150,850),
 (107,"Lunch Box Set","Kitchen",380,240),(108,"Stackable Bin","Storage",290,190),
]
price = {p[0]:p[3] for p in products}
employees = [(1,"Anita Rao","Sales Head",None),(2,"Vikram Singh","Sales Manager",1),(3,"Neha Kulkarni","Sales Executive",2),(4,"Rahul Mehta","Sales Executive",2),(5,"Farah Khan","Sales Executive",1)]
season = {1:1.0,2:0.95,3:1.05,4:1.0,5:0.95,6:0.72,7:0.62,8:0.88,9:1.1,10:1.55,11:1.4,12:0.95}
base = {"steady":0.92,"occasional":0.45,"big":0.95,"churn":0.92,"seasonal":0.35}
def month_start(d): return D(d.year,d.month,1)
orders=[]; items=[]; oid=6000; iid=1
for (cid,name,city,seg,signup,prof,rep,churn) in customers:
    for m in range(1,13):
        if D(2025,m,1) < month_start(signup) and not (signup.year==2024): continue
        if signup.year==2025 and m < signup.month: continue
        if churn and m > churn: continue
        p = base[prof]*min(1.0, 0.55+0.45*season[m])
        if prof=="seasonal": p = 0.15 if m<9 else min(0.95, 0.35*season[m]*2.2)
        n = 0
        if random.random() < min(p,0.97): n = 1
        if prof in ("big","steady") and random.random() < 0.25*season[m]: n += 1
        for _ in range(n):
            day = random.randint(1,28)
            if signup.year==2025 and m==signup.month: day=max(day,signup.day)
            od = D(2025,m,day)
            status = "Delivered"
            if random.random() < 0.04: status="Cancelled"
            if od >= D(2025,12,20): status = random.choice(["Shipped","Pending"])
            r = rep
            if r and random.random()<0.03: r=None
            oid+=1; orders.append((oid,cid,od,status,r))
            if seg=="Wholesale": pool=[105,105,102,108,101]; qty=(10,45); disc=[5,8,10,12]
            elif seg=="Hospitality": pool=[103,104,107,101,108]; qty=(10,60); disc=[0,0,5]
            else:
                pool=[101,103,104,107,108,102]; qty=(10,50); disc=[0,0,0,5]
                if m in (3,4,5): pool += [106,106]
            if prof=="seasonal" and m in (10,11): pool += [107,104]
            chosen = random.sample(sorted(set(pool)), k=min(len(set(pool)), random.choice([1,1,2,2,3])))
            for pid in chosen:
                q = max(5, int(random.randint(*qty)*season[m])//5*5)
                items.append((iid,oid,pid,q,price[pid],random.choice(disc))); iid+=1
# sort orders by date and renumber for realism
orders.sort(key=lambda o:(o[2],o[1]))
remap={}; new_orders=[]
for i,o in enumerate(orders, start=1):
    remap[o[0]]=10000+i; new_orders.append((10000+i,)+o[1:])
items=[(it[0],remap[it[1]])+it[2:] for it in items]
items.sort(key=lambda it:(it[1],it[2]))
items=[(i+1,)+it[1:] for i,it in enumerate(items)]
targets=[(D(2025,m,1), t) for m,t in zip(range(1,13),[300000,300000,320000,320000,320000,300000,280000,320000,380000,520000,500000,380000])]
# leads with duplicates and stage history
sources=["Website","Trade fair","Referral","IndiaMART listing","Cold call"]
companies=["Anand Stores","Bright Kitchens","Cafe Mocha Lane","Delta Hospitality","Elite Mart","Fortune Foods","Garnet Hotels","Hilltop Resorts","Indigo Caterers","Jasmine Retail",
 "Kaveri Distributors","Lotus Banquets","Mango Tree Cafe","Nova Supermart","Orchid Hotels","Pearl Packaging","Quick Bite Foods","Ruby Traders","Saffron Kitchens","Tulip Mart",
 "Urban Pantry","Vista Resorts","Willow Cafe","Xpress Wholesale","Yellow Chilli Diner","Zenith Supplies","Aroma Bakers","Bharat Provisions","Crown Hotels","Daily Fresh Mart"]
leads=[]; hist=[]; lid=0
for i,c in enumerate(companies):
    created = dt.datetime(2025, random.randint(1,11), random.randint(1,28), random.randint(9,18), random.choice([5,20,35,50]))
    email = c.lower().replace(" ","").replace("'","")+"@example.com"
    src=random.choice(sources); owner=random.choice([3,4,5])
    if i % 4 == 1: src = "Website"   # web-form enquiries are the ones that get submitted twice
    lid+=1; leads.append((lid,created,c,email,src,owner))
    stages=["New"]
    r=random.random()
    if r<0.75: stages.append("Contacted")
    if r<0.45: stages.append("Quoted")
    if r<0.22: stages.append("Won")
    elif r<0.45 and random.random()<0.5: stages.append("Lost")
    t=created
    for st in stages:
        hist.append((lid,st,t)); t=t+dt.timedelta(days=random.randint(2,15), hours=random.randint(0,6))
    if i % 4 == 1:  # duplicate form submissions of the same enquiry
        for k in range(random.choice([1,1,2])):
            lid+=1; dup_t = created + dt.timedelta(minutes=random.choice([2,7,45,180]))
            leads.append((lid,dup_t,c if k==0 else c.upper(),email,src,owner)); hist.append((lid,"New",dup_t))
def q(v):
    if v is None: return "NULL"
    if isinstance(v,(int,float)): return str(v)
    if isinstance(v,dt.datetime): return f"'{v:%Y-%m-%d %H:%M:%S}'"
    if isinstance(v,dt.date): return f"'{v:%Y-%m-%d}'"
    return "'"+str(v).replace("'","''")+"'"
def ins(table, rows):
    return f"INSERT INTO {table} VALUES\n" + ",\n".join(" ("+", ".join(q(x) for x in r)+")" for r in rows) + ";\n\n"
sql = """-- Riverstone Supplies (fictional) — one year of data (2025) for Chapter 13.
-- Generated by generate_riverstone_2025.py (seed 2025). Every name and number is invented.
DROP TABLE IF EXISTS lead_stage_history, leads, sales_targets, order_items, orders, products, customers, employees;

CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, customer_name VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30) NOT NULL, signup_date DATE NOT NULL);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL, unit_price NUMERIC(10,2) NOT NULL, unit_cost NUMERIC(10,2) NOT NULL);
CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, employee_name VARCHAR(100) NOT NULL, job_title VARCHAR(50) NOT NULL, manager_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id), order_date DATE NOT NULL, status VARCHAR(20) NOT NULL, sales_rep_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL, unit_price NUMERIC(10,2) NOT NULL, discount_pct NUMERIC(5,2) NOT NULL DEFAULT 0);
CREATE TABLE sales_targets (target_month DATE PRIMARY KEY, target_revenue NUMERIC(12,2) NOT NULL);
CREATE TABLE leads (lead_id INTEGER PRIMARY KEY, created_at TIMESTAMP NOT NULL, company_name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, source VARCHAR(30) NOT NULL, owner_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE lead_stage_history (lead_id INTEGER NOT NULL REFERENCES leads(lead_id), stage VARCHAR(20) NOT NULL, entered_at TIMESTAMP NOT NULL, PRIMARY KEY (lead_id, stage));

"""
sql += ins("customers",[c[:5] for c in customers]) + ins("products",products) + ins("employees",employees)
sql += ins("orders",new_orders) + ins("order_items",items) + ins("sales_targets",targets) + ins("leads",leads) + ins("lead_stage_history",hist)
open("riverstone_2025_setup.sql","w").write(sql)
print(len(new_orders),"orders",len(items),"items",len(leads),"leads",len(hist),"history")
