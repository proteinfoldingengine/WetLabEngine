"""Complete two-branch graphs and sequential local-star repair candidates."""
from itertools import combinations
import graph_producer as graph
from star_normalize import normalize as star
DOMAIN=tuple((a,b,k) for a in (2,3) for b in (2,3) for k in (2,3,4))
def tree(a,b):return '('+'('+'()'*b+')'+'()'*(a-1)+')'
def normalize(state,a,b,k,r,s):
 current=list(state);path=[list(current)];side=list(range(b+2,a+b+1));inner=list(range(2,b+2));labels=list(range(k))
 def support(v):return [j for j in labels if current[j]>>v&1]
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(list(current))
 def local(leaves,palette,q):
  if len(palette)==1:return
  view=[1|sum(1<<(i+1) for i,v in enumerate(leaves) if current[j]>>v&1) for j in palette]
  for nxt in star(view,len(leaves),len(palette),q)[1:]:
   for j,mask in zip(palette,nxt):
    for i,v in enumerate(leaves):
     if mask>>(i+1)&1:current[j]|=1<<v
     else:current[j]&=~(1<<v)
   path.append(list(current))
 t=next(z for z in range(1,k+1) if any(all(any(current[j]>>v&1 for j in H) for v in side) for H in combinations(labels,z)))
 local(side,labels,t)
 desired=list(range(s)) if r<=a-1 else list(range(a-1,a-1+s))
 for j in labels:
  if j not in support(1):change(j,1,True)
 if k>s:
  local(inner,desired+[j for j in labels if j not in desired],s)
  for j in labels:
   if j not in desired:change(j,1,False)
 if r<=a-1 and t==r-1:
  change(r-1,side[r-1],True);change(0,side[r-1],False)
 local(inner,desired,s)
 return path
def produce(domain=DOMAIN):
 entries=[]
 for a,b,k in domain:
  g=graph.build(tree(a,b),k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   q=rec['q']
   for component in rec['zero_components']:
    i=component[0]
    try:path=[index.get(tuple(t),-1) for t in normalize(g['states'][i],a,b,k,q[0],q[1])]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'a':a,'b':b,'k':k,'graph':g,'normalizations':paths})
 return {'schema':1,'domain':[list(x) for x in domain],'entries':entries}
