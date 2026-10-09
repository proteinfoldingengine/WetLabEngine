"""Independent set-based closed-phase reconstruction and representative-union covers."""
import itertools,json,sys
from functools import lru_cache
@lru_cache(None)
def cover_number(s):
 roots=[{x for x in range(9) if r&(1<<x)} for r in s]
 # A retained host core label with B,C is always an explicit three-cover.
 assert any(all({4,5,e}&r for r in roots) for e in range(4))
 frontier={frozenset()}
 for root in roots:
  frontier={h|{x} for h in frontier for x in root if len(h|{x})<=2}
 return min(map(len,frontier)) if frontier else 3
def initial(u,v,a):
 roots=[{a[0],4},{a[0],5},{a[1],4},{a[1],5},{4,5},set(range(4))-set(a)]
 for i,r in enumerate(roots):
  if u&(1<<i):r.add(7)
  if v&(1<<i):r.add(8)
 return roots
def bits(roots):return [sum(1<<x for x in r) for r in roots]
def low(states):return [min(x[r].bit_count() for x in states) for r in range(6)]
def phases(roots,i,d):
 a=next(iter(roots[2*i]&set(range(4))));e=next(iter((roots[5]&set(range(4)))-{d}));out=[];maps=[];src=bits(roots)
 for n in range(9):
  r=[x.copy() for x in roots]
  r[5]=(roots[5]-{d})|({d} if n<2 else set())|({6} if 1<=n<8 else set())|({a} if n>=7 else set())
  r[2*i]=(roots[2*i]-{a})|({a} if n<4 else set())|({d} if n>=3 else set())
  r[2*i+1]=(roots[2*i+1]-{a})|({a} if n<6 else set())|({d} if n>=5 else set())
  m=[(e if x==6 else a if x==d and n>=3 else d if x==a and n>=7 else x) for x in range(9)]
  assert all({m[x] for x in r[j]}<=roots[j] for j in range(6))
  b=bits(r);assert all(b[j].bit_count()>=src[j].bit_count() for j in range(6));assert cover_number(tuple(b))==3
  out.append(b);maps.append(m)
 return out,maps,r
@lru_cache(None)
def expected():
 c={'scope_commit':'0da4cab896c7f60d4aa244372e5bd104cddca097','claims':{'edit_bound_factor':16,'observer_origin':False,'guaranteed_requests':False,'optimal':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for u in range(64):
  for v in range(64):
   r=initial(u,v,(0,1));s=bits(r);t=cover_number(tuple(s));c['sources_a'].append({'id':[u,v],'state':s,'tau':t,'protected':t==3})
   if t==3:
    for i in (0,1):
     for d in (2,3):
      ss,mm,_=phases(r,i,d);c['handoffs'].append({'id':[u,v,i,d],'states':ss,'maps':mm,'minimum_sizes':low(ss),'taus':[cover_number(tuple(x)) for x in ss]})
 assignments=[(a,b) for a in range(4) for b in range(4) if a!=b]
 for u in range(64):
  for a in assignments:
   roots=initial(u,0,a);s=bits(roots);t=cover_number(tuple(s));c['sources_b'].append({'id':[u,*a],'state':s,'tau':t,'protected':t==3})
   if t!=3:continue
   for goal in assignments:
    r=[x.copy() for x in roots];states=[s];plan=[]
    for i in (0,1):
     target=goal[i]
     if target in r[2*i]:continue
     if target not in r[5]:
      j=next(j for j in (0,1) if target in r[2*j]);assert j>i
      spare=sorted(r[5]&set(range(4)))[0];ss,_,r=phases(r,j,spare);plan.append([j,spare]);states.extend(ss[1:])
     ss,_,r=phases(r,i,target);plan.append([i,target]);states.extend(ss[1:])
     assert all(goal[j] in r[2*j] and goal[j] in r[2*j+1] for j in range(i+1))
    assert len(plan)<=4 and r==initial(u,0,goal)
    c['goals'].append({'id':[u,*a,*goal],'exchanges':plan,'states':states,'minimum_sizes':low(states),'taus':[cover_number(tuple(x)) for x in states]})
 return json.dumps(c,sort_keys=True,separators=(',',':'))
def verify(c):
 if json.dumps(c,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('certificate differs in identity, type, value, multiplicity, or scope')
 return True
if __name__=='__main__':
 verify(json.load(open(sys.argv[1])));print('PASS independent complete reconstruction')
