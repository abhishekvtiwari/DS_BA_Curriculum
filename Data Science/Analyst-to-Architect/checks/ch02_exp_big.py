import pandas as pd, numpy as np, os, time, gzip, shutil, json
rng=np.random.default_rng(20260916)
n=500_000
prods=np.array([101,102,103,104,105,106,107,108]); price=dict(zip(prods,[450,780,120,650,1450,1200,520,690]))
df=pd.DataFrame({
 'line_id':np.arange(1,n+1),
 'order_date':pd.to_datetime('2025-01-01')+pd.to_timedelta(rng.integers(0,365,n),unit='D'),
 'customer_id':rng.integers(1,25,n),
 'product_id':rng.choice(prods,n),
 'quantity':rng.integers(1,200,n),
 'discount_pct':rng.choice([0,0,0,5,5,10,12],n).astype(float),
 'status':rng.choice(['Delivered']*8+['Shipped','Cancelled'],n),
})
df['unit_price']=df['product_id'].map(price).astype(float)
os.makedirs('big',exist_ok=True)
t=time.time(); df.to_csv('big/sales_lines.csv',index=False); print('csv write',round(time.time()-t,1))
with open('big/sales_lines.csv','rb') as f, gzip.open('big/sales_lines.csv.gz','wb') as g: shutil.copyfileobj(f,g)
t=time.time(); df.to_json('big/sales_lines.json',orient='records',date_format='iso'); print('json write',round(time.time()-t,1))
t=time.time(); df.to_parquet('big/sales_lines.parquet',index=False); print('parquet write',round(time.time()-t,1))
t=time.time(); df.to_excel('big/sales_lines.xlsx',index=False,engine='openpyxl'); print('xlsx write',round(time.time()-t,1))
for f in sorted(os.listdir('big')): print(f, os.path.getsize('big/'+f), round(os.path.getsize('big/'+f)/1e6,1),'MB')
for label,fn in [('csv all', lambda: pd.read_csv('big/sales_lines.csv')), ('csv one col', lambda: pd.read_csv('big/sales_lines.csv',usecols=['quantity'])),
                 ('parquet all', lambda: pd.read_parquet('big/sales_lines.parquet')), ('parquet one col', lambda: pd.read_parquet('big/sales_lines.parquet',columns=['quantity']))]:
    ts=[]
    for _ in range(3):
        t=time.time(); fn(); ts.append(time.time()-t)
    print(label, round(min(ts),3))
print('total qty', df.quantity.sum())
