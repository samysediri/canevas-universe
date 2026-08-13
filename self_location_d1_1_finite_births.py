"""SELF-LOCATION D1.1 — source-corrected finite human birth-distribution test.

D1 failed before producing a result because the OWID series ended in 2023.
D1.1 is a technical source correction. This revision only fixes UNData transport:
DownloadHandler returns a ZIP archive containing a CSV. No scientific threshold,
tail scenario, observed rank, or verdict rule is changed.
"""
from __future__ import annotations
import io, math, urllib.request, zipfile
import pandas as pd

BIRTH_YEAR=1992
PRB_EVER_1950=107_901_175_171
PRB_EVER_2022=117_020_448_575
OWID="https://ourworldindata.org/grapher/annual-number-of-births-by-world-region.csv?v=1&csvType=full&useColumnShortNames=true"
UNDATA_CBR="https://data.un.org/Handlers/DownloadHandler.ashx?DataFilter=variableID:53;crID:900&DataMartId=PopDiv&Format=csv"
UNDATA_POP="https://data.un.org/Handlers/DownloadHandler.ashx?DataFilter=variableID:12;crID:900&DataMartId=PopDiv&Format=csv"
TAILS=[('EXTINCTION_2100','zero',None),('EXP_DECAY_5PCT','exp',.05),('EXP_DECAY_2PCT','exp',.02),('EXP_DECAY_1PCT','exp',.01),('EXP_DECAY_0P5PCT','exp',.005),('EXP_DECAY_0P25PCT','exp',.0025),('PLATEAU_1000Y','plateau',1000),('PLATEAU_10000Y','plateau',10000),('INDEFINITE_PLATEAU','infinite',None)]

def _decode_csv_bytes(raw):
 if raw.startswith((b'\xff\xfe',b'\xfe\xff')) or raw[:100].count(b'\x00')>10:
  return raw.decode('utf-16')
 try:return raw.decode('utf-8-sig')
 except UnicodeDecodeError:return raw.decode('latin-1')

def read_csv_url(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 raw=urllib.request.urlopen(req,timeout=60).read()
 # UNData DownloadHandler serves a ZIP archive even when Format=csv.
 if raw.startswith(b'PK'):
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   names=[n for n in z.namelist() if not n.endswith('/')]
   if not names: raise RuntimeError('UNData ZIP archive contained no file')
   raw=z.read(names[0])
 text=_decode_csv_bytes(raw)
 return pd.read_csv(io.StringIO(text))

def historical():
 df=read_csv_url(OWID); lower={str(c).lower():c for c in df.columns}; ent=lower.get('entity'); yr=lower.get('year'); code=lower.get('code')
 if ent:
  w=df[df[ent].astype(str).str.lower().eq('world')].copy()
  if not w.empty:df=w
 meta={x for x in (ent,yr,code) if x}; nums=[]
 for c in df.columns:
  if c in meta:continue
  s=pd.to_numeric(df[c],errors='coerce')
  if s.notna().sum()>50:nums.append((c,s))
 chosen=next(((c,s) for c,s in nums if 'birth' in str(c).lower()),nums[0]); c,s=chosen
 out=pd.DataFrame({'Year':pd.to_numeric(df[yr],errors='coerce'),'births':s}).dropna();out.Year=out.Year.astype(int);out=out.groupby('Year',as_index=False).births.sum()
 return out,c

def undata_series(url,value_name):
 df=read_csv_url(url); cols={str(c).strip().lower():c for c in df.columns}
 y=next((c for k,c in cols.items() if 'year' in k),None); v=next((c for k,c in cols.items() if k=='value' or k.startswith('value')),None); variant=next((c for k,c in cols.items() if 'variant' in k),None); area=next((c for k,c in cols.items() if 'country or area' in k),None)
 if y is None or v is None: raise RuntimeError(f'UNData schema unexpected: {list(df.columns)}')
 if area is not None:
  w=df[df[area].astype(str).str.strip().str.lower().eq('world')]
  if not w.empty:df=w
 if variant is not None:
  m=df[df[variant].astype(str).str.strip().str.lower().eq('medium')]
  if not m.empty:df=m
 out=pd.DataFrame({'Year':pd.to_numeric(df[y],errors='coerce'),value_name:pd.to_numeric(df[v],errors='coerce')}).dropna();out.Year=out.Year.astype(int);return out.groupby('Year',as_index=False)[value_name].mean()

def projection():
 cbr=undata_series(UNDATA_CBR,'cbr');pop=undata_series(UNDATA_POP,'pop_thousands');p=cbr.merge(pop,on='Year');p=p[(p.Year>=2024)&(p.Year<=2100)].copy();p['births']=p.pop_thousands*p.cbr
 if 2100 not in set(p.Year) or 2024 not in set(p.Year):raise RuntimeError(f'UN WPP projection incomplete: {p.Year.min()}..{p.Year.max()}')
 return p[['Year','births']]

def exp_tail(b,r):a=1-r;return b*a/(1-a)
def cross_tail(rem,b,k,p):
 if rem<=0:return 2100
 if k=='zero':return None
 if k=='plateau':n=math.ceil(rem/b);return 2100+n if n<=int(p) else None
 if k=='exp':
  a=1-float(p);tot=exp_tail(b,float(p))
  if rem>tot:return None
  rhs=1-rem*(1-a)/(b*a)
  return None if rhs<=0 else 2100+max(1,math.ceil(math.log(rhs)/math.log(a)))
 return None

def main():
 h,col=historical();p=projection();d=pd.concat([h[h.Year<=2023],p],ignore_index=True).sort_values('Year')
 for need in (1950,1992,2022,2024,2100):
  if need not in set(d.Year):raise RuntimeError(f'Required year {need} missing')
 before=d[(d.Year>=1950)&(d.Year<1992)].births.sum();b92=float(d.loc[d.Year==1992,'births'].iloc[0]);r=PRB_EVER_1950+before+.5*b92
 cum2100=r+.5*b92+d[(d.Year>1992)&(d.Year<=2100)].births.sum();b2100=float(d.loc[d.Year==2100,'births'].iloc[0])
 print('='*82);print('SELF-LOCATION D1.1 — FINITE HUMAN BIRTH DISTRIBUTION');print('='*82);print('D1 status = TECHNICAL_FAILURE_NO_RESULT');print(f'historical births = OWID/UN column {col} through 2023');print('projection births = UN WPP 2024 medium, reconstructed from official population x crude birth rate, 2024-2100');print(f'approx mid-1992 cumulative rank r = {r:,.0f}');print(f'2100 annual births = {b2100:,.0f}');print(f'cumulative births through 2100 = {cum2100:,.0f}');print('\nSCENARIOS')
 finite=[]
 for name,k,param in TAILS:
  if k=='infinite':print(f'{name:22s} N_total=INFINITE q=0 in limit');continue
  tail=0 if k=='zero' else exp_tail(b2100,float(param)) if k=='exp' else b2100*int(param);nt=cum2100+tail;q=r/nt;target=2*r
  if target<=cum2100:
   cur=r+.5*b92;cross=None
   for y in range(1993,2101):
    cur+=float(d.loc[d.Year==y,'births'].iloc[0])
    if cur>=target:cross=y;break
  else:cross=cross_tail(target-cum2100,b2100,k,param)
  c25=.25<=q<=.75;c10=.10<=q<=.90;finite.append((name,q,c25,c10,nt,cross));print(f'{name:22s} N_total={nt/1e9:10.3f}B q={q:.4f} |q-.5|={abs(q-.5):.4f} central25={c25} central10={c10} 2r_cross={cross}')
 n=len(finite);c25=sum(x[2] for x in finite);c10=sum(x[3] for x in finite);verdict='ROBUST_INTERIOR' if all(x[3] for x in finite) and c25/n>=.75 else 'SENSITIVE_TO_TAIL' if any(x[2] for x in finite) and any(not x[3] for x in finite) else 'GENERALLY_NONCENTRAL' if c25/n<.25 else 'INTERMEDIATE'
 print('\nPREDECLARED ROBUSTNESS SUMMARY');print(f'finite scenarios = {n}');print(f'in [0.25,0.75] = {c25}/{n} ({c25/n:.3f})');print(f'in [0.10,0.90] = {c10}/{n} ({c10/n:.3f})');print('PREDECLARED D1.1 VERDICT =',verdict);ref=min(x[4] for x in finite);print('\nTOY SELF-LOCATION WEIGHTING (DIAGNOSTIC ONLY)')
 for name,q,_,_,nt,_ in finite:print(f'{name:22s} SSA relative likelihood vs shortest-N = {ref/nt:.6g} simple SIA+SSA = 1.0')
 print('\nINTERPRETATION LOCK:');print('- D1 produced no scientific result; D1.1 only corrects failed data transport/source access.');print('- Population peak is not the median of cumulative births.');print('- Post-2100 tails remain sensitivity models, not forecasts.');print('- Exact 2r crossing is diagnostic only and cannot select a tail.');print('- Finite future is assumed by finite scenarios, not established by data.');print('- SSA/SIA differ; no observer measure is derived.');print('- Prehistoric cumulative births remain highly uncertain.');print('- No printed year predicts extinction or the end of the world.');print('\nFINISHED SELF-LOCATION D1.1')
if __name__=='__main__':main()
