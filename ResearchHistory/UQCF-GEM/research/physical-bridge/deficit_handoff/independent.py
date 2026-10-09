"""Set phases, representative unions, independently enumerated certificates."""
import json,sys
from functools import lru_cache
@lru_cache(None)
def number(s):
 roots=[{x for x in range(7) if v&(1<<x)} for v in s];assert all(roots);f={frozenset()}
 for r in roots:f={h|{x} for h in f for x in r}
 return min(map(len,f))
def pats(b,c):return [{0,1,2},{3}|{i for i in range(3) if b&(1<<i)},{4}|{i for i in range(3) if c&(1<<i)}]
def initial(b,c,z,a):
 pp=pats(b,c);roots=[{a[i] for i in range(3) if r in pp[i]} for r in range(5)]+[set(range(5))-set(a)]
 for r in range(6):
  if z&(1<<r):roots[r].add(6)
 return roots
def bits(r):return [sum(1<<x for x in v) for v in r]
def choose(pp,i):
 candidates=[]
 for mask in range(8):
  js=[j for j in range(3) if mask&(1<<j)]
  if i in js or len(js)>2:continue
  u=set().union(*(pp[j] for j in js)) if js else set()
  if not (set(range(5))-pp[i])<=u:continue
  p=sorted(pp[i]&u);r=sorted(pp[i]-u);candidates.append(((max(1,len(r)),len(js),tuple(js)),js,p,r))
 if not candidates:raise ValueError('certificate unavailable')
 _,j,p,r=sorted(candidates)[0];return j,p,r
def stats(ss):return {'minimum_sizes':[min(s[r].bit_count() for s in ss) for r in range(6)],'taus':[number(tuple(s)) for s in ss],'peak':max(sum(x.bit_count() for x in s) for s in ss)-sum(x.bit_count() for x in ss[0])}
def phases(roots,pp,i,d,cur):
 js,p,r=choose(pp,i);a=cur[i];e=next(iter((roots[5]&set(range(5)))-{d}));m=len(pp[i]);out=[];maps=[]
 for n in range(2*m+5):
  v=[x.copy() for x in roots];v[5]=(roots[5]-{d})|({d} if n<2 else set())|({5} if 1<=n<2*m+4 else set())|({a} if n>=2*m+3 else set())
  for j,x in enumerate(p):
   if n>=3+2*j:v[x].add(d)
   if n>=4+2*j:v[x].remove(a)
  for j,x in enumerate(r):
   if n>=3+2*len(p)+j:v[x].add(d)
   if n>=3+2*len(p)+len(r)+j:v[x].remove(a)
  phi=[e if x==5 else a if x==d and n>=3 else d if x==a and n>=2*m+3 else x for x in range(7)]
  assert all({phi[x] for x in v[j]}<=roots[j] for j in range(6))
  cover={cur[j] for j in js}|{e}
  if r:cover.add(a if n<=2+2*len(p)+len(r) else d)
  assert len(cover)<=4 and all(cover&x for x in v)
  assert all(len(v[j])>=len(roots[j]) for j in range(6))
  s=bits(v);t=number(tuple(s));assert number(tuple(bits(roots)))<=t<=4 and t>=3;out.append(s);maps.append(phi)
 assert stats(out)['peak']==max(1,len(r))
 return out,maps,js,p,r,v
@lru_cache(None)
def expected():
 c={'scope_commit':'b0a03eeba5127458b2404edac062487f789f3db7','claims':{'band':[3,4],'exact_tau':False,'path_optimal':False,'observer_origin':False,'guaranteed_requests':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for b in range(8):
  for v in range(8):
   for z in range(64):
    roots=initial(b,v,z,(0,1,2));s=bits(roots);t=number(tuple(s));ok=3<=t<=4;c['sources_a'].append({'id':[b,v,z],'state':s,'tau':t,'protected':ok})
    if ok:
     for i in range(3):
      for d in (3,4):
       ss,mm,j,p,r,_=phases(roots,pats(b,v),i,d,(0,1,2));c['handoffs'].append({'id':[b,v,z,i,d],'states':ss,'maps':mm,'certificate':j,'covered':p,'deficit':r,**stats(ss)})
 roles=[(a,b,c) for a in range(5) for b in range(5) for c in range(5) if len({a,b,c})==3]
 for b,v in [(0,0),(1,2),(7,0)]:
  for z in (0,24,63):
   for a in [(0,1,2),(2,3,4)]:
    roots=initial(b,v,z,a);s=bits(roots);t=number(tuple(s));ok=3<=t<=4;c['sources_b'].append({'id':[b,v,z,*a],'state':s,'tau':t,'protected':ok})
    if not ok:continue
    pp=pats(b,v);beta=max(max(1,len(choose(pp,i)[2])) for i in range(3))
    for goal in roles:
     r=[x.copy() for x in roots];cur=list(a);ss=[s];plan=[]
     for i in range(3):
      if cur[i]==goal[i]:continue
      if goal[i] not in r[5]:
       j=cur.index(goal[i]);assert j>i;d=sorted(r[5]&set(range(5)))[0];part,*_,r=phases(r,pp,j,d,cur);ss.extend(part[1:]);plan.append([j,d]);cur[j]=d
      part,*_,r=phases(r,pp,i,goal[i],cur);ss.extend(part[1:]);plan.append([i,goal[i]]);cur[i]=goal[i]
      assert cur[:i+1]==list(goal[:i+1])
     assert r==initial(b,v,z,goal) and len(plan)<=6 and len(ss)-1<=6*(2*max(map(len,pp))+4)
     meta=stats(ss);assert meta['peak']<=beta;c['goals'].append({'id':[b,v,z,*a,*goal],'exchanges':plan,'states':ss,**meta})
 c['fixtures']={}
 for name,z in [('moving',0),('rise',24)]:
  ss,*_=phases(initial(1,2,z,(0,1,2)),pats(1,2),0,3,(0,1,2));c['fixtures'][name]={'states':ss,'persistent_cover_tau':number(tuple(x for s in ss for x in s)),**stats(ss)}
 assert c['fixtures']['moving']['persistent_cover_tau']==5 and c['fixtures']['moving']['peak']==1
 assert c['fixtures']['rise']['taus'][0]==3 and c['fixtures']['rise']['taus'][4]==4
 return json.dumps(c,sort_keys=True,separators=(',',':'))
def verify(c):
 if json.dumps(c,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete identity/type/value certificate mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete reconstruction')
