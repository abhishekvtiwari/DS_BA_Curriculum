# Automated pre-scan per PDF: fonts, pages, blank-ish pages, text outside margins, mid-token wraps, cover labels
import subprocess,sys,re,json,os
from xml.etree import ElementTree as ET
pdf=sys.argv[1]; out=sys.argv[2]
r={}
r['fonts']=subprocess.run(['pdffonts',pdf],capture_output=True,text=True).stdout
info=subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout
r['pages']=int(re.search(r'Pages:\s+(\d+)',info).group(1))
r['pagesize']=re.search(r'Page size:\s+(.*)',info).group(1)
r['images']=subprocess.run(['pdfimages','-list',pdf],capture_output=True,text=True).stdout.count('\n')-2
x=subprocess.run(['pdftotext','-bbox-layout',pdf,'-'],capture_output=True,text=True).stdout
x=re.sub(r'<!DOCTYPE[^>]*>','',x); x=x.replace('xmlns="http://www.w3.org/1999/xhtml"','')
root=ET.fromstring(x)
pages=[];outside=[];sparse=[]
for i,p in enumerate(root.iter('page'),1):
    W=float(p.get('width'));H=float(p.get('height'))
    ws=list(p.iter('word'))
    area=0; ymax=0
    for w in ws:
        x0,y0,x1,y1=[float(w.get(k)) for k in ('xMin','yMin','xMax','yMax')]
        area+=(x1-x0)*(y1-y0)
        if y0<H-60 and y0>50: ymax=max(ymax,y1)
        if x1>W-18 or x0<18: outside.append((i,w.text,round(x0),round(x1)))
    lastfrac=round(ymax/H,2)
    if i not in (1,) and i!=r['pages'] and lastfrac<0.6: sparse.append((i,lastfrac))
r['text_near_edge']=outside[:60]
r['sparse_pages(text ends above 60% of page)']=sparse
t=subprocess.run(['pdftotext','-layout',pdf,'-'],capture_output=True,text=True).stdout
r['draft_labels']=sorted(set(re.findall(r'(?i)(draft[^\n]{0,60}|v\d[^\n]{0,20}20\d\d|for review[^\n]{0,30}|coordinator[^\n]{0,60}|to be confirmed[^\n]{0,40})',t)))[:20]
r['tofu']=len(re.findall('[�□]',t))
pg=t.split('\f'); hy=[]
for n,s in enumerate(pg,1):
    for m in re.finditer(r'(\S*[A-Za-z_]-)\n\s*([a-z_]\S*)',s):
        hy.append((n,m.group(1)+'|'+m.group(2)))
r['line_end_hyphen_breaks']=hy[:80]
json.dump(r,open(out,'w'),indent=1)
