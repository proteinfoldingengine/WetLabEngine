"""v16.29 producer: actual four-state profiles, subset-union DP, no research imports."""
from collections import Counter
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import hashlib,json,lzma
HERE=Path(__file__).resolve().parent
ORIGIN='v16.29-common-genesis'
PARENT_SHA='daedbb1ac332aa8c8058700b9f3a6b0eaa2a9d0a3341918b42a6b0495ba94df4'
PARENT=HERE.parent/'v16.28-diamond-attribution-closure/evidence/FULL_CERTIFICATES.json.xz'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def validate(raw,views):
 need(isinstance(raw,(list,tuple)) and raw,'empty tree');p=tuple(raw)
 need(all(type(x)is int for x in p) and p[0]==-1,'root/parent type')
 need(all(0<=x<len(p) for x in p[1:]),'parent outside tree')
 for node in range(1,len(p)):
  seen=set()
  while node:
   need(node not in seen,'cycle');seen.add(node);node=p[node]
 need(isinstance(views,(list,tuple)) and views,'empty family');ys=[]
 for rawy in views:
  need(isinstance(rawy,(list,tuple)) and rawy,'empty view');y=tuple(rawy)
  need(all(type(x)is int and 0<=x<len(p) for x in y),'view identity')
  need(len(set(y))==len(y) and 0 in y,'duplicate identity/missing root')
  need(all(x==0 or p[x] in y for x in y),'missing ancestor');ys.append(y)
 return p,tuple(ys)

def cut(p,ys,event):
 need(isinstance(event,(list,tuple)) and len(event)==2 and all(type(x)is int for x in event),'event type')
 i,c=event;need(0<=i<len(ys) and 0<c<len(p) and c in ys[i],'event endpoint')
 need(not any(w and p[w]==c for w in ys[i]),'not current leaf')
 out=list(ys);out[i]=tuple(x for x in ys[i] if x!=c);out=tuple(out)
 need(set().union(*map(set,out))==set().union(*map(set,ys)),'changed union')
 return out

@lru_cache(None)
def profile(p,ys):
 U=set().union(*map(set,ys));out=[]
 for v in range(len(p)):
  K=sum(1<<w for w in U if w and p[w]==v)
  if not K:out.append(0);continue
  best={0:0}
  for y in ys:
   mask=sum(1<<w for w in y)&K
   nxt=dict(best)
   for covered,n in best.items():nxt[covered|mask]=min(nxt.get(covered|mask,len(ys)+1),n+1)
   best=nxt
  need(K in best,'uncovered child');out.append(best[K])
 return tuple(out)

def certify(raw,before,events):
 p,ys=validate(raw,before)
 need(isinstance(events,(list,tuple)) and len(events)==2,'two events required')
 a,b=events;need(a!=b,'duplicate event')
 ye=cut(p,ys,a);yf=cut(p,ys,b);yef=cut(p,ye,b);need(yef==cut(p,yf,a),'noncommuting actual states')
 states=(ys,ye,yf,yef);profiles=[profile(p,s) for s in states];hs=[max((1,)+t) for t in profiles]
 local=[profiles[3][v]-profiles[1][v]-profiles[2][v]+profiles[0][v] for v in range(len(p))]
 glob=hs[3]-hs[1]-hs[2]+hs[0];parents=[p[a[1]],p[b[1]]]
 B=max([1]+[profiles[0][v] for v in range(len(p)) if v not in parents])
 if parents[0]!=parents[1]:prediction=-(hs[1]-hs[0])*(hs[2]-hs[0])
 else:
  x,y,z,w=[t[parents[0]] for t in profiles]
  prediction=w-y-z+x if B<=x else int(w==x+2) if B==x+1 else 0
 mechanism=('LOCAL_TRANSMITTED' if any(local) else 'MAX_ONLY') if glob else ('LOCAL_MASKED' if any(local) else 'ZERO')
 return {'version':'16.29','genesis':ORIGIN,'parents':list(p),'before':[list(y) for y in ys],
         'events':[list(a),list(b)],'states':[[list(y) for y in s] for s in states],
         'profiles':[list(t) for t in profiles],'heights':hs,'parent_pair':parents,
         'local_mixed':local,'global_mixed':glob,'background':B,'prediction':prediction,'mechanism':mechanism}

def code(p):
 def rec(v):return '('+''.join(sorted(rec(w) for w in range(1,len(p)) if p[w]==v))+')'
 return rec(0)

def shapes(bound):
 found={}
 for n in range(1,bound+1):
  for q in product(*(range(i) for i in range(1,n))):
   p=(-1,)+q;found.setdefault(code(p),p)
 return [(k,found[k]) for k in sorted(found,key=lambda k:(len(k),k))]

def legal(p):
 out=[]
 for mask in range(1,1<<len(p),2):
  y=tuple(v for v in range(len(p)) if mask>>v&1)
  if all(v==0 or p[v] in y for v in y):out.append(y)
 return out

def inputs(p):
 L=legal(p);U=set(range(len(p)))
 for k in range(1,min(4,len(L))+1):
  for ys in combinations(L,k):
   if set().union(*map(set,ys))!=U:continue
   events=[(i,v) for i,y in enumerate(ys) for v in y if v and not any(w and p[w]==v for w in y)]
   for ev in combinations(events,2):
    removed=set(ev)
    zs=[tuple(v for v in y if (i,v) not in removed) for i,y in enumerate(ys)]
    if set().union(*map(set,zs))==U:yield ys,ev

def transported(p,ys,events):
 pi=[0]+list(range(len(p)-1,0,-1));q=[-1]*len(p)
 for v in range(1,len(p)):q[pi[v]]=pi[p[v]]
 a=[[pi[v] for v in reversed(y)] for y in reversed(ys)]
 e=[[len(ys)-1-i,pi[v]] for i,v in events]
 return q,a,e

def parent_groups():
 raw=lzma.decompress(PARENT.read_bytes());need(hashlib.sha256(raw).hexdigest()==PARENT_SHA,'parent archive identity')
 doc=json.loads(raw);out=[]
 for group in doc['instances']:
  rows=[]
  for ci,old in enumerate(group['cases']):
   E=old['events'];statevals=dict(old['states'])
   for di,(s,e,f,expected) in enumerate(old['diamonds']):
    removed={tuple(E[j]) for j in range(len(E)) if s>>j&1}
    current=[[v for v in y if (i,v) not in removed] for i,y in enumerate(old['before'])]
    c=certify(old['parents'],current,[E[e],E[f]])
    need(c['heights']==[statevals[s],statevals[s|(1<<e)],statevals[s|(1<<f)],statevals[s|(1<<e)|(1<<f)]],'parent scalar states')
    need(c['global_mixed']==expected,'parent diamond')
    rows.append({'id':[ci,di],'certificate':c})
  out.append({'code':group['code'],'variant':group['variant'],'parents':group['parents'],'records':rows})
 return out

def examples():
 specs={
  'max_negative':((-1,0,0,1,1),[(0,1,2),(0,1,3,4),(0,2),(0,1,4)],[(0,2),(1,4)]),
  'max_positive':((-1,0,0,1,1,1),[(0,1,3,4,5),(0,1,3),(0,1,4),(0,2)],[(0,3),(0,4)]),
  'masked':((-1,0,0,1,1),[(0,1,3,4),(0,1,3),(0,1,4),(0,2)],[(0,3),(0,4)]),
  'transmitted_negative':((-1,0,0),[(0,1),(0,2),(0,1,2)],[(2,1),(2,2)]),
  'transmitted_positive':((-1,0,0),[(0,1,2)]*2,[(0,1),(1,2)]),
  'zero':((-1,0),[(0,1)]*3,[(0,1),(1,1)])}
 return {name:certify(*spec) for name,spec in specs.items()}

def produce(bound=5,include_parent=True):
 need(type(bound)is int and 1<=bound<=5 and type(include_parent)is bool,'declared bounds')
 groups=[]
 for sc,p in shapes(bound):
  specs=list(inputs(p));original=[certify(p,y,e) for y,e in specs]
  groups.append({'code':sc,'variant':'original','parents':list(p),'cases':original})
  q,_,_=transported(p,[(0,)],[])
  groups.append({'code':sc,'variant':'relabeled','parents':q,'cases':[certify(*transported(p,y,e)) for y,e in specs]})
 return {'version':'16.29','genesis':ORIGIN,'tree_bound':bound,'view_bound':4,'include_parent':include_parent,
         'parent_raw_sha256':PARENT_SHA if include_parent else None,'parent':parent_groups() if include_parent else [],
         'extension':groups,'examples':examples()}

if __name__=='__main__':
 d=produce();e=HERE/'evidence';e.mkdir(exist_ok=True)
 raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();(e/'FULL_CERTIFICATES.json.xz').write_bytes(lzma.compress(raw))
 (e/'EXAMPLES.json').write_text(json.dumps(d['examples'],indent=2,sort_keys=True)+'\n')
 r={'execution_status':'COMPLETED','raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'scope':'producer only; independent verification required'}
 (e/'PRODUCTION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
