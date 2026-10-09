"""Bit-toggle production with exact subset transversals."""
import itertools,json,sys
from functools import lru_cache
SCOPE='2a20eebec47bb916abf419a9880d4b3f8e3c9c9b'
COVERS=[(n,sum(1<<x for x in h)) for n in range(1,6) for h in itertools.combinations(range(10),n)]
@lru_cache(None)
def tau(s):
 for n,h in COVERS:
  if all(h&r for r in s):return n
 raise AssertionError('no five-cover')
def source(p,q,z,a=(0,1)):
 s=[(1<<(4+r))|((1<<a[0]) if p>>r&1 else 0)|((1<<a[1]) if q>>r&1 else 0) for r in range(4)]
 s.append(sum(1<<x for x in range(4) if x not in a))
 return [b|(512 if z>>r&1 else 0) for r,b in enumerate(s)]
def exchange(s,p,q,i,d,a):
 roots=[r for r in range(4) if (p,q)[i]>>r&1];e=next(x for x in range(4) if x!=d and s[4]>>x&1)
 ops=[(4,8,1),(4,d,0)]+[(r,d,1) for r in roots]+[(r,a,0) for r in roots]+[(4,a,1),(4,8,0)]
 states=[s[:]];s=s[:]
 for r,x,add in ops:
  assert bool(s[r]&(1<<x))!=bool(add);s[r]^=1<<x;states.append(s[:])
 maps=[]
 for n in range(len(states)):
  m=list(range(10));m[8]=e
  if n>=3:m[d]=a
  if n>=3+2*len(roots):m[a]=d
  maps.append(m)
 return states,maps
def metadata(ss):return {'minimum_sizes':[min(s[r].bit_count() for s in ss) for r in range(5)],'taus':[tau(tuple(s)) for s in ss],'peak':max(sum(x.bit_count() for x in s) for s in ss)-sum(x.bit_count() for x in ss[0])}
def produce():
 c={'scope_commit':SCOPE,'claims':{'edit_bound_factor':2,'bound_formula':'2*k*(2*M+4)','observer_origin':False,'guaranteed_requests':False,'optimal':False,'one_excess_incidence':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for p,q,z in itertools.product(range(1,16),range(1,16),range(32)):
  s=source(p,q,z);t=tau(tuple(s));ok=t in (3,4);c['sources_a'].append({'id':[p,q,z],'state':s,'tau':t,'protected':ok})
  if not ok:continue
  for i,d in itertools.product(range(2),(2,3)):
   ss,mm=exchange(s,p,q,i,d,i);c['handoffs'].append({'id':[p,q,z,i,d],'states':ss,'maps':mm,**metadata(ss)})
 roles=list(itertools.permutations(range(4),2))
 for (p,q),z,a in itertools.product([(3,6),(3,12),(15,5)],[0,17,31],roles):
  s=source(p,q,z,a);t=tau(tuple(s));ok=t in (3,4);c['sources_b'].append({'id':[p,q,z,*a],'state':s,'tau':t,'protected':ok})
  if not ok:continue
  for goal in roles:
   cur=list(a);ss=[s];plan=[]
   for i in range(2):
    if cur[i]==goal[i]:continue
    if goal[i] in cur:
     j=cur.index(goal[i]);d=min(set(range(4))-set(cur));part,_=exchange(ss[-1],p,q,j,d,cur[j]);ss+=part[1:];plan.append([j,d]);cur[j]=d
    d=goal[i];part,_=exchange(ss[-1],p,q,i,d,cur[i]);ss+=part[1:];plan.append([i,d]);cur[i]=d
   c['goals'].append({'id':[p,q,z,*a,*goal],'exchanges':plan,'states':ss,**metadata(ss)})
 s=source(3,4,0);old=[s[:]];v=s[:]
 for r,x in [(4,8),(4,2),(0,2),(0,0),(1,2),(1,0),(4,0),(4,8)]:v[r]^=1<<x;old.append(v[:])
 ss,_=exchange(s,3,4,0,2,0)
 c['fixture']={'source_tau':tau(tuple(s)),'alternating_states':old,'alternating_taus':[tau(tuple(v)) for v in old],'batched_states':ss,'persistent_cover_tau':tau(tuple(r for v in ss for r in v))}
 return c
if __name__=='__main__':
 c=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({k:len(c[k]) for k in ('sources_a','sources_b','handoffs','goals')}))
