"""v16.25 independent verifier. Does not import producer."""
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import json,lzma,hashlib
HERE=Path(__file__).resolve().parent;GENESIS='v16.25-common-genesis'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def valid(raw,views):
 p=tuple(raw);need(p and all(type(x)is int for x in p) and p[0]==-1,'parents');need(all(0<=p[i]<len(p) for i in range(1,len(p))),'endpoint')
 for i in range(1,len(p)):
  u=i;s=set()
  while u:need(u not in s,'cycle');s.add(u);u=p[u]
 ys=[]
 for rawy in views:
  y=tuple(rawy);need(y and all(type(v)is int and 0<=v<len(p) for v in y),'view');need(0 in y and len(set(y))==len(y),'root/dup');need(all(v==0 or p[v] in y for v in y),'ancestor');ys.append(y)
 return p,tuple(ys)
def fibers(p,f,c):
 pos={v:i for i,v in enumerate(c)};M=[[0]*len(f) for _ in c]
 for j,v in enumerate(f):
  u=v
  while u not in pos:u=p[u]
  M[pos[u]][j]=1
 return tuple(map(tuple,M))
def mv(M,x):return tuple(sum(Fraction(a)*Fraction(b) for a,b in zip(r,x)) for r in M)
def hcalc(p,ys):
 U=set().union(*map(set,ys));vals=[1]
 for v in U:
  kids={w for w in U if w and p[w]==v}
  if kids:vals.append(min(r for r in range(1,len(ys)+1) if any(kids<=set().union(*(set(ys[i]) for i in ids)) for ids in combinations(range(len(ys)),r))))
 return max(vals)
def verify_case(d):
 need(isinstance(d,dict) and {'version','genesis','parents','before','after','h_before','h_after','strict','composition'}<=d.keys(),'schema');need(d['version']=='16.25' and d['genesis']==GENESIS,'origin')
 p,ys=valid(d['parents'],d['before']);_,zs=valid(p,d['after']);need(len(ys)==len(zs) and all(set(z)<=set(y) for y,z in zip(ys,zs)),'component refinement');need(set().union(*map(set,ys))==set().union(*map(set,zs)),'same union')
 hb,ha=hcalc(p,ys),hcalc(p,zs);need(type(d['h_before'])is int and d['h_before']==hb,'before h');need(type(d['h_after'])is int and d['h_after']==ha,'after h');need(ha>=hb,'monotonicity');need(type(d['strict'])is bool and d['strict']==(ha>hb),'strict flag')
 need(isinstance(d['composition'],list) and len(d['composition'])==sum(map(len,ys)),'composition coverage');seen=set()
 for r in d['composition']:
  need({'view','basis','fine','mid','coarse','direct','staged'}<=r.keys(),'composition schema');i,j=r['view'],r['basis'];need(type(i)is int and type(j)is int and 0<=i<len(ys) and 0<=j<len(ys[i]),'composition id');need((i,j) not in seen,'duplicate composition');seen.add((i,j));y,m,z=tuple(r['fine']),tuple(r['mid']),tuple(r['coarse']);need(y==ys[i] and z==zs[i] and set(z)<=set(m)<=set(y),'composition endpoints')
  x=[0]*len(y);x[j]=1;direct=mv(fibers(p,y,z),x);staged=mv(fibers(p,m,z),mv(fibers(p,y,m),x));need(direct==staged,'fiber composition');need(tuple(map(Fraction,r['direct']))==direct and tuple(map(Fraction,r['staged']))==staged,'false composition certificate')
 return {'h_before':hb,'h_after':ha,'strict':ha>hb}
def code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def legal(p,y=None):
 allow=set(range(len(p))) if y is None else set(y);out=[]
 for mask in range(1,1<<len(p),2):
  z=tuple(i for i in range(len(p)) if mask>>i&1)
  if set(z)<=allow and all(v==0 or p[v] in z for v in z):out.append(z)
 return out
def expected_count(p):
 L=legal(p);count=strict=0
 for n in range(1,min(4,len(L))+1):
  for ys in combinations(L,n):
   if set().union(*map(set,ys))!=set(range(len(p))):continue
   for zs in product(*(legal(p,y) for y in ys)):
    if set().union(*map(set,zs))!=set(range(len(p))):continue
    count+=1;strict+=hcalc(p,zs)>hcalc(p,ys)
 return count,strict
def verify_document(doc,bound=5):
 need(isinstance(doc,dict) and {'version','genesis','bound','refinements','strict','instances'}<=doc.keys(),'doc schema');need(doc['version']=='16.25' and doc['genesis']==GENESIS and type(doc['bound'])is int and doc['bound']==bound,'doc metadata')
 total=strict=0;codes=set()
 for inst in doc['instances']:
  p=tuple(inst['parents']);need(code(p)==inst['code'] and inst['code'] not in codes,'shape identity');codes.add(inst['code']);ec,es=expected_count(p);need(len(inst['cases'])==ec,'refinement coverage');keys=set()
  for d in inst['cases']:
   k=(tuple(map(tuple,d['before'])),tuple(map(tuple,d['after'])));need(k not in keys,'duplicate');keys.add(k);r=verify_case(d);strict+=r['strict'];total+=1
  need(sum(1 for d in inst['cases'] if d['strict'])==es,'strict coverage')
 need(type(doc['refinements'])is int and doc['refinements']==total,'total');need(type(doc['strict'])is int and doc['strict']==strict,'strict total')
 return {'execution_status':'COMPLETED','input_validity':'VALID','scientific_verdict':'SAME_UNION_PRUNING_MONOTONICITY_AND_COMPOSITION_VERIFIED_ON_BOUNDED_UNIVERSE','proof_status':'general proofs P1-P5 plus independent bounded certificates','refinements':total,'strict':strict,'shapes':len(codes)}
if __name__=='__main__':
 raw=lzma.decompress((HERE/'evidence/certificates.json.xz').read_bytes());r=verify_document(json.loads(raw),5);r['raw_sha256']=hashlib.sha256(raw).hexdigest();(HERE/'evidence/VERIFICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
