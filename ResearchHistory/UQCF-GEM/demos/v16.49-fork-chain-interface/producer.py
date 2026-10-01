"""Binary interface around two independently normalized internal chains."""
from itertools import product
import graph_producer as graph
import chain_normalize as chain
DOMAIN=(2,3)
LEFT=RIGHT=(2,2)
def full_profile(left,right,t):return [t[0]]+list(t[1:1+len(left)])+[0]*(sum(left)+1-len(left))+list(t[1+len(left):])+[0]*(sum(right)+1-len(right))
def pattern(left,right,k,q):
 off=2+sum(left);a=chain.need(left,q[1:]);b=chain.need(right,q[off:]);pa=list(range(a));pb=list(range(b)) if q[0]==1 else list(range(a,a+b));out=[1]*k
 for d,P,offset in ((left,pa,1),(right,pb,off)):
  view=chain.pattern(d,len(P),q[offset:])
  for j,z in zip(P,view):out[j]|=z<<offset
 return out
def transport(state,left,right,k,rolesA,rolesB):
 current=list(state);path=[current[:]];split=len(rolesA);roles=list(rolesA)+list(rolesB);off=2+sum(left)
 regions=(list(range(1,off)),list(range(off,off+sum(right)+1)))
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(current[:])
 def replace(i,y):
  x=roles[i];vertices=regions[0 if i<split else 1]
  if any(current[y]>>v&1 for v in vertices):raise ValueError('replacement destination present in child')
  used=[v for v in vertices if current[x]>>v&1]
  for v in used:change(y,v,True)
  for v in reversed(used):change(x,v,False)
  roles[i]=y
 def cross(i,j):
  x,y=roles[i],roles[j];replace(i,y);replace(j,x)
 def swap(i,j):
  if (i<split)!=(j<split):cross(i,j)
  else:
   pivot=split if i<split else 0;cross(i,pivot);cross(j,pivot);cross(i,pivot)
 for i in range(len(roles)):
  if roles[i]==i:continue
  if i in roles:swap(i,roles.index(i))
  else:replace(i,i)
 return path
def normalize(state,left,right,k,q):
 current=list(state);path=[current[:]];off=2+sum(left);pieces=((left,1),(right,off));palettes=[]
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(current[:])
 if q[0]==1:
  for _,offset in pieces:
   for j in range(k):
    if not current[j]>>offset&1:change(j,offset,True)
 for d,offset in pieces:
  P=[j for j in range(k) if current[j]>>offset&1];mask=(1<<(sum(d)+1))-1;view=[(current[j]>>offset)&mask for j in P]
  for nxt in chain.normalize(view,d,len(P),q[offset:])[1:]:
   for j,z in zip(P,nxt):current[j]=(current[j]&~(mask<<offset))|(z<<offset)
   path.append(current[:])
  width=chain.need(d,q[offset:]);palettes.append(P[:width])
  for j in P[width:]:change(j,offset,False)
 if q[0]==2:path.extend(transport(current,left,right,k,*palettes)[1:])
 return path
def corpus_specs():
 rows=[]
 for t in product((1,2),repeat=5):
  a=chain.need(LEFT,t[1:3]);b=chain.need(RIGHT,t[3:]);m=max(a,b) if t[0]==1 else a+b
  for k in (m,m+1):
   for p in ('identity','reversal','cyclic'):rows.append({'target':list(t),'k':k,'permutation':p})
 return rows
def produce(domain=DOMAIN,specs=None):
 entries=[];code='('+chain.tree(LEFT)+chain.tree(RIGHT)+')'
 for k in domain:
  g=graph.build(code,k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   for comp in rec['zero_components']:
    i=comp[0];q=rec['q']
    try:path=[index.get(tuple(z),-1) for z in normalize(g['states'][i],LEFT,RIGHT,k,q)]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'k':k,'graph':g,'normalizations':paths})
 corpus=[]
 for spec in (corpus_specs() if specs is None else specs):
  k=spec['k'];p=spec['permutation'];q=full_profile(LEFT,RIGHT,spec['target']);base=pattern(LEFT,RIGHT,k,q);start=[0]*k
  for j in range(k):start[j if p=='identity' else k-1-j if p=='reversal' else (j+1)%k]=base[j]
  a=chain.need(LEFT,q[1:]);b=chain.need(RIGHT,q[6:]);m=max(a,b) if q[0]==1 else a+b
  try:path=normalize(start,LEFT,RIGHT,k,q)
  except Exception:path=None
  corpus.append({'spec':spec,'palette_requirement':m,'start':start,'path':path})
 return {'schema':1,'domain':list(domain),'entries':entries,'corpus':corpus}
