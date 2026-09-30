"""Prospective exact retained campaign; no historical result imports."""
from itertools import product, combinations
from collections import deque

def shape_code(p):
 def visit(v):return '('+''.join(sorted(visit(w) for w in range(1,len(p)) if p[w]==v))+')'
 return visit(0)

def shapes(bound):
 seen={}
 for n in range(1,bound+1):
  for tail in product(*(range(i) for i in range(1,n))):
   p=(-1,)+tail;seen.setdefault(shape_code(p),p)
 return sorted(seen.values(),key=lambda p:(len(p),p))

def states_for(p,k):
 n=len(p);full=(1<<n)-1
 views=[m for m in range(1,1<<n,2) if all(not(m>>v&1) or m>>p[v]&1 for v in range(1,n))]
 return sorted(x for x in product(views,repeat=k) if __import__('functools').reduce(int.__or__,x,0)==full)

def profile(p,s):
 out=[]
 for v in range(len(p)):
  children=sum(1<<w for w in range(1,len(p)) if p[w]==v)
  dp={0:0}
  for view in s:
   for covered,num in list(dp.items()):
    c=covered|(view&children);dp[c]=min(dp.get(c,len(s)+1),num+1)
  out.append(dp[children])
 return out

def graph_for(p,S):
 ids={s:i for i,s in enumerate(S)};A=[]
 for s in S:
  neighbors=[]
  for j in range(len(s)):
   for v in range(1,len(p)):
    t=list(s);t[j]^=1<<v
    if tuple(t) in ids:neighbors.append(ids[tuple(t)])
  A.append(sorted(neighbors))
 return A

def reach(A,allowed,a,b=None):
 if a not in allowed:return [],None
 seen={a};todo=deque([a]);prev={}
 while todo:
  x=todo.popleft()
  for y in A[x]:
   if y in allowed and y not in seen:seen.add(y);prev[y]=x;todo.append(y)
 path=None
 if b is not None and b in seen:
  path=[b]
  while path[-1]!=a:path.append(prev[path[-1]])
  path.reverse()
 return sorted(seen),path

def components(A,Q):
 groups=[]
 for q in sorted(set(map(tuple,Q))):
  todo={i for i,x in enumerate(Q) if tuple(x)==q};cs=[]
  while todo:
   c,_=reach(A,todo,min(todo));cs.append(c);todo-=set(c)
  groups.append({'q':list(q),'components':cs})
 return groups

def barriers(A,C,a,b):
 primary=[];paths=[]
 for i in range(3):
  for t in sorted({c[i] for c in C}):
   _,path=reach(A,{x for x,c in enumerate(C) if c[i]<=t},a,b)
   if path is not None:primary.append(t);paths.append(path);break
  else:raise ValueError('disconnected graph')
 allowed=set(range(len(A)));lex=[];lp=None
 for i in range(3):
  for t in sorted({C[x][i] for x in allowed}):
   trial={x for x in allowed if C[x][i]<=t};_,path=reach(A,trial,a,b)
   if path is not None:lex.append(t);allowed=trial;lp=path;break
  else:raise ValueError('no lex path')
 return primary,lex,paths,lp

def produce(bound=5):
 graphs=[]
 for p in shapes(bound):
  for k in range(1,4):
   S=states_for(p,k);A=graph_for(p,S);Q=[profile(p,s) for s in S];groups=components(A,Q);pairs=[]
   for group in groups:
    q=group['q'];cs=group['components']
    C=[]
    for qx in Q:
     d=[abs(x-y) for x,y in zip(qx,q)];C.append((sum(d),max(d,default=0),sum(x>0 for x in d)))
    for i,j in combinations(range(len(cs)),2):
     a,b=cs[i][0],cs[j][0];primary,lex,paths,lp=barriers(A,C,a,b)
     cuts=[reach(A,{x for x,c in enumerate(C) if c[t]<primary[t]},a)[0] for t in range(3)]
     pairs.append({'q':q,'components':[i,j],'representatives':[a,b],'primary':primary,'lex':lex,'paths':paths,'lex_path':lp,'lower_reachable':cuts,'endpoint_pairs':len(cs[i])*len(cs[j])})
   graphs.append({'parents':list(p),'views':k,'states':[list(s) for s in S],'q':Q,'edges':[[i,j] for i,row in enumerate(A) for j in row if i<j],'groups':groups,'pairs':pairs})
 pairs=[r for g in graphs for r in g['pairs']]
 nonunit=[{'parents':g['parents'],'views':g['views'],'pair':r} for g in graphs for r in g['pairs'] if r['primary']!=[1,1,1]]
 nonunit.sort(key=lambda w:(len(w['parents']),w['views'],w['parents'],w['pair']['q'],w['pair']['representatives']))
 return {'version':'16.37','bound':bound,'view_counts':[1,2,3],'graphs':graphs,'outcome':'NONUNIT_RETAINED_WITNESS' if nonunit else 'BOUNDED_UNIT_ONLY','nonunit':nonunit,'summary':{'graphs':len(graphs),'states':sum(len(g['states']) for g in graphs),'component_pairs':len(pairs),'endpoint_pairs':sum(r['endpoint_pairs'] for r in pairs),'nonunit_pairs':len(nonunit),'objective_distinctions':sum(r['primary']!=r['lex'] for r in pairs)},'universal_unit_law':'UNRESOLVED'}
