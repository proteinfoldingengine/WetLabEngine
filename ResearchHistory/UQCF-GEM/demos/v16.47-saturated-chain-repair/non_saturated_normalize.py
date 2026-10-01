"""Complete nested-chain graphs; outer scaffold and reviewed nested repair."""
from itertools import combinations
import graph_producer as graph
from star_normalize import normalize as star
from nested_normalize import normalize as nested
DOMAIN=tuple((2,2,2,k) for k in (2,3,4))+tuple((a,b,c,k) for a,b,c in ((2,2,3),(2,3,2),(3,2,2)) for k in (2,3))
def tree(a,b,c):return '((('+'()'*c+')'+'()'*(b-1)+')'+'()'*(a-1)+')'
def normalize(state,a,b,c,k,q):
 r,s,t=q[:3]
 if r>=a:raise ValueError('saturated outer root outside normalization scope')
 current=list(state);path=[list(current)];side=list(range(b+c+2,a+b+c+1));labels=list(range(k))
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(list(current))
 h=next(z for z in range(1,k+1) if any(all(any(current[j]>>v&1 for j in H) for v in side) for H in combinations(labels,z)))
 view=[1|sum(1<<(i+1) for i,v in enumerate(side) if current[j]>>v&1) for j in labels]
 for nxt in star(view,len(side),k,h)[1:]:
  for j,mask in enumerate(nxt):
   for i,v in enumerate(side):
    if mask>>(i+1)&1:current[j]|=1<<v
    else:current[j]&=~(1<<v)
  path.append(list(current))
 for j in labels:
  if not current[j]>>1&1:change(j,1,True)
 if h==r-1:
  change(r-1,side[r-1],True);change(0,side[r-1],False)
 # U's subtree occupies consecutive global vertices1..b+c+1.
 width=b+c+1;mask=(1<<width)-1;view=[(z>>1)&mask for z in current]
 for nxt in nested(view,b,c,k,s,t)[1:]:
  current=[(old&~(mask<<1))|(new<<1) for old,new in zip(current,nxt)];path.append(list(current))
 return path
def produce(domain=DOMAIN):
 entries=[]
 for a,b,c,k in domain:
  g=graph.build(tree(a,b,c),k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   if rec['q'][0]>=a:continue
   for component in rec['zero_components']:
    i=component[0];q=rec['q']
    try:path=[index.get(tuple(t),-1) for t in normalize(g['states'][i],a,b,c,k,q)]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'a':a,'b':b,'c':c,'k':k,'graph':g,'normalizations':paths})
 return {'schema':1,'domain':[list(x) for x in domain],'entries':entries}
