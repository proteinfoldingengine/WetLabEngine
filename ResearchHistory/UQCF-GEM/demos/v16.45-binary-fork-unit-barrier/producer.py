"""Complete binary-fork graphs and sequential branch normalizations."""
import graph_producer as graph
from star_normalize import normalize as star
DOMAIN=tuple((b,c,k) for b,c in ((2,2),(2,3),(3,3)) for k in (2,3))
def tree(b,c):return '(('+'()'*c+')('+'()'*b+'))'
def normalize(state,b,c,k,q):
 current=list(state);path=[list(current)];r,s,t=q[0],q[1],q[c+2]
 palettes=[list(range(s)),list(range(t)) if r==1 else list(range(s,s+t))]
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(list(current))
 for w,leaves,h,D in ((1,list(range(2,c+2)),s,palettes[0]),(c+2,list(range(c+3,b+c+3)),t,palettes[1])):
  for j in range(k):
   if not current[j]>>w&1:change(j,w,True)
  order=D+[j for j in range(k) if j not in D]
  view=[1|sum(1<<(i+1) for i,v in enumerate(leaves) if current[j]>>v&1) for j in order]
  for nxt in star(view,len(leaves),k,h)[1:]:
   for j,mask in zip(order,nxt):
    for i,v in enumerate(leaves):
     if mask>>(i+1)&1:current[j]|=1<<v
     else:current[j]&=~(1<<v)
   path.append(list(current))
  for j in range(k):
   if j not in D:change(j,w,False)
 return path
def produce(domain=DOMAIN):
 entries=[]
 for b,c,k in domain:
  g=graph.build(tree(b,c),k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   for component in rec['zero_components']:
    i=component[0];q=rec['q']
    try:path=[index.get(tuple(t),-1) for t in normalize(g['states'][i],b,c,k,q)]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'b':b,'c':c,'k':k,'graph':g,'normalizations':paths})
 return {'schema':1,'domain':[list(x) for x in domain],'entries':entries}
