"""Saturated nested-chain repair with exact inner palette transport."""
import graph_producer as graph
from nested_normalize import normalize as nested
from non_saturated_normalize import normalize as non_saturated
DOMAIN=((2,2,2,2),(2,2,2,3),(2,2,2,4),(2,2,3,2),(2,2,3,3),(2,3,2,2),(2,3,2,3),(3,2,2,2),(3,2,2,3))
def tree(a,b,c):return '((('+'()'*c+')'+'()'*(b-1)+')'+'()'*(a-1)+')'
def transport(state,a,b,c,k,outer,inner):
 current=list(state);path=[list(current)];l=a-1;roles=list(outer)+list(inner)
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(list(current))
 def replace_inner(x,y):
  vertices=[v for v in range(1,b+c+2) if current[x]>>v&1]
  for v in vertices:change(y,v,True)
  for v in reversed(vertices):change(x,v,False)
 def replace(i,y):
  x=roles[i]
  if i<l:change(y,b+c+2+i,True);change(x,b+c+2+i,False)
  else:replace_inner(x,y)
  roles[i]=y
 def cross(i,o):
  x,y=roles[i],roles[o];replace_inner(x,y);v=b+c+2+o
  change(x,v,True);change(y,v,False);roles[i],roles[o]=y,x
 def swap(i,j):
  if i<l and j<l:
   x,y=roles[i],roles[j];u,v=b+c+2+i,b+c+2+j
   change(y,u,True);change(x,v,True);change(x,u,False);change(y,v,False);roles[i],roles[j]=y,x
  elif i>=l and j>=l:cross(i,0);cross(j,0);cross(i,0)
  else:cross(i,j) if i>=l else cross(j,i)
 for i in range(len(roles)):
  if roles[i]==i:continue
  if i in roles:swap(i,roles.index(i))
  else:replace(i,i)
 return path
def normalize(state,a,b,c,k,q):
 r,s,t=q[:3]
 if r<a:return non_saturated(state,a,b,c,k,q)
 current=list(state);path=[list(current)];S=[j for j in range(k) if current[j]>>1&1];width=b+c+1;mask=(1<<width)-1
 if len(S)>1:
  view=[(current[j]>>1)&mask for j in S]
  for nxt in nested(view,b,c,len(S),s,t)[1:]:
   for j,z in zip(S,nxt):current[j]=(current[j]&~(mask<<1))|(z<<1)
   path.append(list(current))
 d=max(s,t) if s<b else b-1+t
 for j in S[d:]:current[j]&=~2;path.append(list(current))
 outer=[]
 for v in range(b+c+2,a+b+c+1):
  palette=[j for j in range(k) if current[j]>>v&1];outer.append(palette[0])
  for j in palette[1:]:current[j]&=~(1<<v);path.append(list(current))
 path.extend(transport(current,a,b,c,k,outer,S[:d])[1:])
 return path
def produce(domain=DOMAIN):
 entries=[]
 for a,b,c,k in domain:
  g=graph.build(tree(a,b,c),k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   for component in rec['zero_components']:
    i=component[0];q=rec['q']
    try:path=[index.get(tuple(t),-1) for t in normalize(g['states'][i],a,b,c,k,q)]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'a':a,'b':b,'c':c,'k':k,'graph':g,'normalizations':paths})
 return {'schema':1,'domain':[list(x) for x in domain],'entries':entries}
