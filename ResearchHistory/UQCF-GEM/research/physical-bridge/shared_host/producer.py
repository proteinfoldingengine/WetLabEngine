"""Incidence-toggle producer; exact subset hitting enumeration."""
import itertools,json,sys
from functools import lru_cache
SCOPE='0da4cab896c7f60d4aa244372e5bd104cddca097'
@lru_cache(None)
def tau(s):
 for n in range(1,10):
  for h in itertools.combinations(range(9),n):
   m=sum(1<<x for x in h)
   if all(m&r for r in s):return n
 raise AssertionError('empty root')
def source(u,v,a=(0,1)):
 h=[x for x in range(4) if x not in a]
 s=[(1<<a[0])|16,(1<<a[0])|32,(1<<a[1])|16,(1<<a[1])|32,48,sum(1<<x for x in h)]
 return [r|(128 if u>>i&1 else 0)|(256 if v>>i&1 else 0) for i,r in enumerate(s)]
def exchange(s,i,d):
 s=s[:];a=next(x for x in range(4) if s[2*i]>>x&1);e=next(x for x in range(4) if x!=d and s[5]>>x&1)
 states=[s[:]];maps=[]
 for r,x,add in [(5,6,1),(5,d,0),(2*i,d,1),(2*i,a,0),(2*i+1,d,1),(2*i+1,a,0),(5,a,1),(5,6,0)]:
  assert bool(s[r]&(1<<x)) != bool(add)
  s[r]^=1<<x;states.append(s[:])
 for n in range(9):
  m=list(range(9));m[6]=e
  if n>=3:m[d]=a
  if n>=7:m[a]=d
  maps.append(m)
 return states,maps
def minimum(states):return [min(s[r].bit_count() for s in states) for r in range(6)]
def produce():
 c={'scope_commit':SCOPE,'claims':{'edit_bound_factor':16,'observer_origin':False,'guaranteed_requests':False,'optimal':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for u,v in itertools.product(range(64),repeat=2):
  s=source(u,v);t=tau(tuple(s));c['sources_a'].append({'id':[u,v],'state':s,'tau':t,'protected':t==3})
  if t!=3:continue
  for i,d in itertools.product(range(2),(2,3)):
   ss,mm=exchange(s,i,d)
   c['handoffs'].append({'id':[u,v,i,d],'states':ss,'maps':mm,'minimum_sizes':minimum(ss),'taus':[tau(tuple(x)) for x in ss]})
 roles=list(itertools.permutations(range(4),2))
 for u in range(64):
  for a in roles:
   s=source(u,0,a);t=tau(tuple(s));c['sources_b'].append({'id':[u,*a],'state':s,'tau':t,'protected':t==3})
   if t!=3:continue
   for goal in roles:
    cur=list(a);states=[s];plan=[]
    for i in range(2):
     if cur[i]==goal[i]:continue
     if goal[i] in cur:
      j=cur.index(goal[i]);d=min(set(range(4))-set(cur));part,_=exchange(states[-1],j,d);states+=part[1:];plan.append([j,d]);cur[j]=d
     d=goal[i];part,_=exchange(states[-1],i,d);states+=part[1:];plan.append([i,d]);cur[i]=d
    c['goals'].append({'id':[u,*a,*goal],'exchanges':plan,'states':states,'minimum_sizes':minimum(states),'taus':[tau(tuple(x)) for x in states]})
 return c
if __name__=='__main__':
 c=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({k:len(c[k]) for k in ('sources_a','sources_b','handoffs','goals')}))
