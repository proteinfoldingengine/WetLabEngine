"""Frozen overlapping-core family and explicit normalization/exchange paths."""
from pathlib import Path
import importlib.util
def load(name,file):
 s=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parent.parent/'v16.41-unit-barrier-dichotomy'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
base=load('v41_producer','producer.py')
DOMAIN=((0,3),(0,4),(0,5),(1,3),(1,4),(2,3))
def code(d,m):
 c='('+'()'*m+')'
 for _ in range(d):c='('+c+'()'+')'
 return c
def structure(p):
 children=[[w for w in range(1,len(p)) if p[w]==v] for v in range(len(p))]
 core=next(v for v,c in enumerate(children) if len(c)>=3)
 return core,children[core],[v for v,c in enumerate(children) if not c and p[v]!=core]
def normalization(p,x):
 state=list(x);path=[list(state)];core,leaves,sides=structure(p)
 a,b=[j for j,mask in enumerate(state) if mask>>core&1]
 A,B=1<<a,1<<b
 def support(v):return sum(1<<j for j,mask in enumerate(state) if mask>>v&1)
 def setleaf(v,target):
  for j in (a,b):
   if target>>j&1 and not state[j]>>v&1:state[j]|=1<<v;path.append(list(state))
  for j in (a,b):
   if not target>>j&1 and state[j]>>v&1:state[j]&=~(1<<v);path.append(list(state))
 if support(leaves[0])==B and sum(support(v)==B for v in leaves)==1:
  t=next(v for v in leaves[1:] if support(v)!=A or sum(support(w)==A for w in leaves if w!=v)>=1)
  setleaf(t,B)
 setleaf(leaves[0],A);setleaf(leaves[1],B)
 for v in leaves[2:]:setleaf(v,A|B)
 return path
def theorem_path(p,x,y):
 state=list(x);path=[list(state)];core,leaves,sides=structure(p)
 def label(v,s):return next(j for j,mask in enumerate(s) if mask>>v&1)
 def chain(v):
  out=[]
  while v>=0:out.append(v);v=p[v]
  return out
 for side in sides:
  a,b=label(side,state),label(side,y)
  if a==b:continue
  other=next((v for v in sides if state[b]>>v&1),core)
  ca,cb=chain(side),chain(other);lca=next(v for v in ca if v in cb)
  childa=ca[ca.index(lca)-1];childb=cb[cb.index(lca)-1]
  va=[v for v in range(len(p)) if state[a]>>v&1 and childa in chain(v)]
  vb=[v for v in range(len(p)) if state[b]>>v&1 and childb in chain(v)]
  for lab,vertices,add in [(a,vb,True),(b,va,True),(a,list(reversed(va)),False),(b,list(reversed(vb)),False)]:
   for v in vertices:
    if add:state[lab]|=1<<v
    else:state[lab]&=~(1<<v)
    path.append(list(state))
 left=normalization(p,state);right=normalization(p,y)
 if left[-1]!=right[-1]:raise ValueError('normal-form endpoint mismatch')
 return path+left[1:]+list(reversed(right))[1:]
def produce(domain=DOMAIN):
 entries=[]
 for d,m in domain:
  c=code(d,m);p=base.parents(c);q=[2 if v in p[1:] else 0 for v in range(len(p))]
  g=base.build(c,d+2,q);index={tuple(s):i for i,s in enumerate(g['states'])};rec=g['profiles'][0]
  def retained_path(fn,*args):
   try:return [index.get(tuple(s),-1) for s in fn(*args)]
   except Exception:return None
  norms=[]
  for i in sorted(v for comp in rec['zero_components'] for v in comp):
   norms.append({'state':i,'path':retained_path(normalization,p,g['states'][i])})
  constructions=[]
  for pair in rec['pairs']:
   x,y=pair['endpoints'];constructions.append({'components':pair['components'],'path':retained_path(theorem_path,p,g['states'][x],g['states'][y])})
  entries.append({'d':d,'m':m,'graph':g,'normalizations':norms,'constructions':constructions})
 return {'schema':1,'domain':[list(x) for x in domain],'entries':entries}
