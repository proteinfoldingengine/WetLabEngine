"""Independent closed-phase set reconstruction; exact representative unions."""
import json,sys
from functools import lru_cache
@lru_cache(None)
def number(s):
 roots=[{x for x in range(10) if r&(1<<x)} for r in s]
 assert all(roots)
 # Ordinary states have five roots. The multi-slice fixture has this explicit five-cover.
 assert len(roots)==5 or all({4,5,1,7,3}&r for r in roots)
 f={frozenset()}
 for r in roots:f={h|{x} for h in f for x in r if len(h|{x})<=4}
 return min(map(len,f)) if f else 5

def initial(p,q,z,a):
 roots=[{4+r}|({a[0]} if p&(1<<r) else set())|({a[1]} if q&(1<<r) else set()) for r in range(4)]+[set(range(4))-set(a)]
 for r in range(5):
  if z&(1<<r):roots[r].add(9)
 return roots

def bits(r):return [sum(1<<x for x in v) for v in r]
def stats(ss):return {'minimum_sizes':[min(s[r].bit_count() for s in ss) for r in range(5)],'taus':[number(tuple(s)) for s in ss],'peak':max(sum(x.bit_count() for x in s) for s in ss)-sum(x.bit_count() for x in ss[0])}
def phases(roots,pat,a,d):
 active=[r for r in range(4) if pat&(1<<r)];m=len(active);e=next(iter((roots[4]&set(range(4)))-{d}));states=[];maps=[]
 for n in range(2*m+5):
  r=[v.copy() for v in roots]
  r[4]=(roots[4]-{d})|({d} if n<2 else set())|({8} if 1<=n<2*m+4 else set())|({a} if n>=2*m+3 else set())
  for j,index in enumerate(active):
   if n>=3+j:r[index].add(d)
   if n>=3+m+j:r[index].remove(a)
  phi=[e if x==8 else a if x==d and n>=3 else d if x==a and n>=2*m+3 else x for x in range(10)]
  assert all({phi[x] for x in r[j]}<=roots[j] for j in range(5))
  assert all(len(r[j])>=len(roots[j]) for j in range(5))
  b=bits(r);assert number(tuple(b))==number(tuple(bits(roots)));states.append(b);maps.append(phi)
 assert stats(states)['peak']==m and len(states)==2*m+5
 return states,maps,r
@lru_cache(None)
def expected():
 c={'scope_commit':'2a20eebec47bb916abf419a9880d4b3f8e3c9c9b','claims':{'edit_bound_factor':2,'bound_formula':'2*k*(2*M+4)','observer_origin':False,'guaranteed_requests':False,'optimal':False,'one_excess_incidence':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for p in range(1,16):
  for q in range(1,16):
   for z in range(32):
    r=initial(p,q,z,(0,1));s=bits(r);t=number(tuple(s));ok=3<=t<=4;c['sources_a'].append({'id':[p,q,z],'state':s,'tau':t,'protected':ok})
    if ok:
     for i in (0,1):
      for d in (2,3):
       ss,mm,_=phases(r,(p,q)[i],i,d);c['handoffs'].append({'id':[p,q,z,i,d],'states':ss,'maps':mm,**stats(ss)})
 roles=[(a,b) for a in range(4) for b in range(4) if a!=b]
 for p,q in [(3,6),(3,12),(15,5)]:
  for z in [0,17,31]:
   for a in roles:
    r0=initial(p,q,z,a);s=bits(r0);t=number(tuple(s));ok=3<=t<=4;c['sources_b'].append({'id':[p,q,z,*a],'state':s,'tau':t,'protected':ok})
    if not ok:continue
    for goal in roles:
     r=[v.copy() for v in r0];cur=list(a);ss=[s];plan=[]
     for i in (0,1):
      if cur[i]==goal[i]:continue
      if goal[i] not in r[4]:
       j=cur.index(goal[i]);assert j>i;spare=sorted(r[4]&set(range(4)))[0];part,_,r=phases(r,(p,q)[j],cur[j],spare);ss.extend(part[1:]);plan.append([j,spare]);cur[j]=spare
      part,_,r=phases(r,(p,q)[i],cur[i],goal[i]);ss.extend(part[1:]);plan.append([i,goal[i]]);cur[i]=goal[i]
      assert cur[:i+1]==list(goal[:i+1])
     assert r==initial(p,q,z,goal) and len(plan)<=4
     assert len(ss)-1<=4*(2*max(p.bit_count(),q.bit_count())+4)
     c['goals'].append({'id':[p,q,z,*a,*goal],'exchanges':plan,'states':ss,**stats(ss)})
 r=initial(3,4,0,(0,1));s=bits(r);old=[]
 # Independent nine closed phases for the adverse alternating schedule.
 for n in range(9):
  v=[x.copy() for x in r]
  v[4]=(r[4]-{2})|({2} if n<2 else set())|({8} if 1<=n<8 else set())|({0} if n>=7 else set())
  v[0]=(r[0]-{0})|({0} if n<4 else set())|({2} if n>=3 else set())
  v[1]=(r[1]-{0})|({0} if n<6 else set())|({2} if n>=5 else set());old.append(bits(v))
 ss,_,_=phases(r,3,0,2)
 c['fixture']={'source_tau':number(tuple(s)),'alternating_states':old,'alternating_taus':[number(tuple(v)) for v in old],'batched_states':ss,'persistent_cover_tau':number(tuple(x for v in ss for x in v))}
 assert c['fixture']['source_tau']==4 and c['fixture']['alternating_taus'][4]==5 and c['fixture']['persistent_cover_tau']==5
 return json.dumps(c,sort_keys=True,separators=(',',':'))
def verify(c):
 if json.dumps(c,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete certificate identity/type/value mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete reconstruction')
