"""Literal incidence toggles and subset hitting sets."""
import itertools,json,sys
from functools import lru_cache
SCOPE='b0a03eeba5127458b2404edac062487f789f3db7'
COVERS=[(n,sum(1<<x for x in h)) for n in range(1,8) for h in itertools.combinations(range(7),n)]
@lru_cache(None)
def tau(s):
 for n,h in COVERS:
  if all(h&r for r in s):return n
 raise AssertionError('empty support')
def patterns(b,c):return [7,8|b,16|c]
def source(b,c,z,a=(0,1,2)):
 pp=patterns(b,c);s=[sum(1<<a[i] for i in range(3) if pp[i]>>r&1) for r in range(5)]+[sum(1<<x for x in range(5) if x not in a)]
 return [v|(64 if z>>r&1 else 0) for r,v in enumerate(s)]
@lru_cache(None)
def certificate(pp,i):
 candidates=[]
 for n in range(3):
  for j in itertools.combinations([x for x in range(3) if x!=i],n):
   u=0
   for x in j:u|=pp[x]
   if (31&~pp[i])&~u:continue
   deficit=pp[i]&~u;covered=pp[i]&u;candidates.append((max(1,deficit.bit_count()),n,j,covered,deficit))
 if not candidates:raise ValueError('no sufficient certificate')
 _,_,j,p,r=min(candidates);return list(j),[x for x in range(5) if p>>x&1],[x for x in range(5) if r>>x&1]
def exchange(s,pp,i,d,cur):
 j,p,r=certificate(tuple(pp),i);a=cur[i];e=next(x for x in range(5) if x!=d and s[5]>>x&1)
 ops=[(5,5,1),(5,d,0)]+[(v,x,add) for v in p for x,add in [(d,1),(a,0)]]+[(v,d,1) for v in r]+[(v,a,0) for v in r]+[(5,a,1),(5,5,0)]
 ss=[s[:]];s=s[:]
 for v,x,add in ops:
  assert bool(s[v]&(1<<x))!=bool(add);s[v]^=1<<x;ss.append(s[:])
 mm=[]
 for n in range(len(ss)):
  phi=list(range(7));phi[5]=e
  if n>=3:phi[d]=a
  if n>=len(ss)-2:phi[a]=d
  mm.append(phi)
 return ss,mm,j,p,r
def stats(ss):return {'minimum_sizes':[min(s[r].bit_count() for s in ss) for r in range(6)],'taus':[tau(tuple(s)) for s in ss],'peak':max(sum(x.bit_count() for x in s) for s in ss)-sum(x.bit_count() for x in ss[0])}
def produce():
 c={'scope_commit':SCOPE,'claims':{'band':[3,4],'exact_tau':False,'path_optimal':False,'observer_origin':False,'guaranteed_requests':False},'sources_a':[],'sources_b':[],'handoffs':[],'goals':[]}
 for b,v,z in itertools.product(range(8),range(8),range(64)):
  s=source(b,v,z);t=tau(tuple(s));ok=t in (3,4);c['sources_a'].append({'id':[b,v,z],'state':s,'tau':t,'protected':ok})
  if not ok:continue
  for i,d in itertools.product(range(3),(3,4)):
   ss,mm,j,p,r=exchange(s,patterns(b,v),i,d,(0,1,2));c['handoffs'].append({'id':[b,v,z,i,d],'states':ss,'maps':mm,'certificate':j,'covered':p,'deficit':r,**stats(ss)})
 roles=list(itertools.permutations(range(5),3))
 for (b,v),z,a in itertools.product([(0,0),(1,2),(7,0)],[0,24,63],[(0,1,2),(2,3,4)]):
  pp=patterns(b,v);s=source(b,v,z,a);t=tau(tuple(s));ok=t in (3,4);c['sources_b'].append({'id':[b,v,z,*a],'state':s,'tau':t,'protected':ok})
  if not ok:continue
  for goal in roles:
   cur=list(a);ss=[s];plan=[]
   for i in range(3):
    if cur[i]==goal[i]:continue
    if goal[i] in cur:
     k=cur.index(goal[i]);d=min(set(range(5))-set(cur));part,*_=exchange(ss[-1],pp,k,d,cur);ss.extend(part[1:]);plan.append([k,d]);cur[k]=d
    d=goal[i];part,*_=exchange(ss[-1],pp,i,d,cur);ss.extend(part[1:]);plan.append([i,d]);cur[i]=d
   c['goals'].append({'id':[b,v,z,*a,*goal],'exchanges':plan,'states':ss,**stats(ss)})
 c['fixtures']={}
 for name,z in [('moving',0),('rise',24)]:
  ss,*_=exchange(source(1,2,z),patterns(1,2),0,3,(0,1,2));c['fixtures'][name]={'states':ss,'persistent_cover_tau':tau(tuple(x for s in ss for x in s)),**stats(ss)}
 return c
if __name__=='__main__':
 c=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({k:len(c[k]) for k in ('sources_a','sources_b','handoffs','goals')}))
