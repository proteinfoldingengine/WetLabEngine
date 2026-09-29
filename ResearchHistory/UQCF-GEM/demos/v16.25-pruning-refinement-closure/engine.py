"""v16.25 producer: exact same-union componentwise pruning/refinement audit."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json,hashlib,lzma
HERE=Path(__file__).resolve().parent; GENESIS='v16.25-common-genesis'
def need(ok,msg):
 if not ok: raise ValueError(msg)
def parents(raw):
 need(isinstance(raw,(list,tuple)) and raw,'empty carrier');p=tuple(raw)
 need(all(type(x) is int for x in p) and p[0]==-1,'parent identifiers');need(all(0<=p[i]<len(p) for i in range(1,len(p))),'parent endpoint')
 for i in range(1,len(p)):
  seen=set();u=i
  while u: need(u not in seen,'cycle');seen.add(u);u=p[u]
 return p
def retained(p,raw):
 need(isinstance(raw,(list,tuple)) and raw,'empty view');y=tuple(raw);need(all(type(x) is int and 0<=x<len(p) for x in y),'view identity');need(0 in y and len(set(y))==len(y),'root/duplicate');need(all(v==0 or p[v] in y for v in y),'missing ancestor');return y
def exact(x):
 need(type(x) in (int,str) or isinstance(x,Fraction),'inexact scalar')
 try:return Fraction(x)
 except Exception as e:raise ValueError('invalid scalar') from e
def push_between(raw,fine,coarse,source):
 p=parents(raw);f=retained(p,fine);c=retained(p,coarse);need(set(c)<=set(f),'coarse not retained in fine');need(isinstance(source,(list,tuple)) and len(source)==len(f),'source dimension');out={v:Fraction(0) for v in c}
 for v,a in zip(f,map(exact,source)):
  u=v
  while u not in out:u=p[u]
  out[u]+=a
 return tuple(out[v] for v in c)
def push(raw,keep,source):
 p=parents(raw);return push_between(p,tuple(range(len(p))),keep,source)
def threshold(raw,views):
 p=parents(raw);ys=tuple(retained(p,y) for y in views);need(ys,'empty cover');U=set().union(*map(set,ys));vals=[1]
 for v in U:
  kids={w for w in U if w and p[w]==v}
  if kids: vals.append(min(r for r in range(1,len(ys)+1) if any(kids<=set().union(*(set(ys[i]) for i in ids)) for ids in combinations(range(len(ys)),r))))
 return max(vals)
def legal_subviews(p,y):
 allow=set(y);out=[]
 for mask in range(1,1<<len(p),2):
  z=tuple(i for i in range(len(p)) if mask>>i&1)
  if set(z)<=allow and all(v==0 or p[v] in z for v in z):out.append(z)
 return tuple(out)
def midpoint(p,y,z):
 removed=[v for v in y if v not in z]
 if not removed:return y
 leaves=[v for v in removed if not any(p[w]==v and w in removed for w in removed)];m=tuple(v for v in y if v!=max(leaves));return m if set(z)<=set(m) else y
def composition_records(p,ys,zs):
 rows=[]
 for i,(y,z) in enumerate(zip(ys,zs)):
  m=midpoint(p,y,z)
  for j in range(len(y)):
   x=[0]*len(y);x[j]=1;direct=push_between(p,y,z,x);staged=push_between(p,m,z,push_between(p,y,m,x))
   rows.append({'view':i,'basis':j,'fine':list(y),'mid':list(m),'coarse':list(z),'direct':[str(a) for a in direct],'staged':[str(a) for a in staged]})
 return rows
def certify_refinement(raw,before,after):
 p=parents(raw);ys=tuple(retained(p,y) for y in before);zs=tuple(retained(p,z) for z in after);need(len(ys)==len(zs) and ys,'indexed cover size');need(all(set(z)<=set(y) for y,z in zip(ys,zs)),'not componentwise retained subview');need(set().union(*map(set,ys))==set().union(*map(set,zs)),'same union required');hb,ha=threshold(p,ys),threshold(p,zs)
 return {'version':'16.25','genesis':GENESIS,'parents':list(p),'before':[list(y) for y in ys],'after':[list(z) for z in zs],'h_before':hb,'h_after':ha,'strict':ha>hb,'composition':composition_records(p,ys,zs)}
def shape_code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def shapes(bound):
 found={}
 for n in range(1,bound+1):
  for q in product(*(range(i) for i in range(1,n))):
   p=(-1,)+q;found.setdefault(shape_code(p),p)
 return [(c,found[c]) for c in sorted(found,key=lambda x:(len(x),x))]
def covers(p):
 L=legal_subviews(p,tuple(range(len(p))))
 for n in range(1,min(4,len(L))+1):
  for ys in combinations(L,n):
   if set().union(*map(set,ys))==set(range(len(p))):yield ys
def refinements(p,ys):
 for zs in product(*(legal_subviews(p,y) for y in ys)):
  if set().union(*map(set,zs))==set().union(*map(set,ys)):yield zs
def produce(bound=5):
 need(type(bound)is int and 1<=bound<=5,'bound');inst=[];total=strict=0
 for code,p in shapes(bound):
  count=inc=0;hist={};digest=hashlib.sha256()
  for ys in covers(p):
   hb=threshold(p,ys)
   for zs in refinements(p,ys):
    ha=threshold(p,zs);count+=1;inc+=ha>hb
    hist[f'{hb}->{ha}']=hist.get(f'{hb}->{ha}',0)+1
    digest.update((repr((ys,zs,hb,ha))+'\n').encode())
  total+=count;strict+=inc;inst.append({'code':code,'parents':list(p),'refinements':count,'strict':inc,'transitions':hist,'digest':digest.hexdigest()})
 return {'version':'16.25','genesis':GENESIS,'bound':bound,'refinements':total,'strict':strict,'instances':inst}
if __name__=='__main__':
 doc=produce(5);raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode();out=HERE/'evidence';out.mkdir(exist_ok=True);(out/'certificates.json.xz').write_bytes(lzma.compress(raw));rec={'execution_status':'COMPLETED','refinements':doc['refinements'],'strict':doc['strict'],'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest()};(out/'PRODUCTION.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
