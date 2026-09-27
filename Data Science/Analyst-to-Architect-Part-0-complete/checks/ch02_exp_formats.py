import pandas as pd, json, os
df = pd.DataFrame({
 'order_id':[5006,5007,5008,5009],
 'customer_name':['Metro Mart','Coastal Foods','Sunrise Caterers','Northgate Distributors'],
 'order_date':pd.to_datetime(['2026-02-06','2026-02-11','2026-02-19','2026-02-25']).date,
 'status':['Delivered','Delivered','Delivered','Shipped'],
 'sales_rep':['Rahul Mehta','Rahul Mehta',None,'Farah Khan'],
 'net_revenue':[14640.00,32625.00,23325.00,76560.00],
 'delivery_note':[None,'Call before delivery',None,'Gate 2, Okhla Phase II'],
})
os.makedirs('orders_extract', exist_ok=True)
df.to_csv('orders_extract/orders_feb_2026.csv', index=False, float_format='%.2f')
df.to_excel('orders_extract/orders_feb_2026.xlsx', index=False)
recs=[{k:(None if (isinstance(v,float) and pd.isna(v)) else (str(v) if k=='order_date' else v)) for k,v in r.items()} for r in df.to_dict('records')]
recs=[{k:(None if v is None or (not isinstance(v,(int,float,str)) ) else v) for k,v in r.items()} for r in recs]
open('orders_extract/orders_feb_2026.json','w').write(json.dumps(recs, indent=2, ensure_ascii=False)+'\n')
# XML hand-built for readability
from xml.sax.saxutils import escape
x=['<?xml version="1.0" encoding="UTF-8"?>','<orders>']
for r in recs:
    x.append(f'  <order id="{r["order_id"]}">')
    for k in ['customer_name','order_date','status','sales_rep','net_revenue','delivery_note']:
        v=r[k]
        if v is None: x.append(f'    <{k}/>')
        else:
            if k=='net_revenue': v=f'{v:.2f}'
            x.append(f'    <{k}>{escape(str(v))}</{k}>')
    x.append('  </order>')
x.append('</orders>')
open('orders_extract/orders_feb_2026.xml','w').write('\n'.join(x)+'\n')
df2=df.copy(); df2['order_date']=pd.to_datetime(df2['order_date'])
df2.to_parquet('orders_extract/orders_feb_2026.parquet', index=False)
for f in sorted(os.listdir('orders_extract')): print(f, os.path.getsize('orders_extract/'+f))
