"""Independent Prüfer/recursive-view/subfamily/scalar-Dijkstra verification."""
from itertools import product, permutations, combinations
from collections import deque
from heapq import heappush,heappop

def need(x,msg):
 if not x:raise ValueError(msg)

def shapes(bound):
 representatives={}
 for n in range(1,bound+1):
  sequences=[()] if n<=2 else product(range(n),repeat=n-2)
  for seq in sequences:
   deg=[1]*n
   for x in seq:deg[x]+=1
   edges=[]
   for x in seq:
    leaf=next(i for i in range(n) if deg[i]==1);edges.append((leaf,x));deg[leaf]-=1;deg[x]-=1
   left=[i for i in range(n) if deg[i]==1]
   if len(left)==2:edges.append(tuple(left))
   adj=[[] for _ in range(n)]
   for a,b in edges:adj[a].append(b);adj[b].append(a)
   for root in range(n):
    parent={root:None};todo=[root]
    for x in todo:
     for y in adj[x]:
      if y not in parent:parent[y]=x;todo.append(y)
    def code(x):return '('+''.join(sorted(code(y) for y in adj[x] if parent.get(y)==x))+')'
    key=code(root)
    for tail in permutations([x for x in range(n) if x!=root]):
     order=(root,)+tail;ids={x:i for i,x in enumerate(order)}
     if all(parent[x] is None or ids[parent[x]]<ids[x] for x in order):
      p=tuple(-1 if parent[x] is None else ids[parent[x]] for x in order)
      if key not in representatives or p<representatives[key]:representatives[key]=p
 return sorted(representatives.values(),key=lambda p:(len(p),p))

def raw_graph(p,k):
 children=[[w for w in range(1,len(p)) if p[w]==v] for v in range(len(p))]
 def views(v):
  options=[(frozenset(),)+tuple(views(w)) for w in children[v]]
  return [frozenset({v}).union(*parts) for parts in product(*options)]
 full=frozenset(range(len(p)))
 sets=[x for x in product(views(0),repeat=k) if frozenset().union(*x)==full]
 sets.sort(key=lambda s:tuple(sum(1<<v for v in x) for x in s))
 S=[[sum(1<<v for v in x) for x in s] for s in sets]
 Q=[]
 for s in sets:
  row=[]
  for ch in children:
   if not ch:row.append(0);continue
   row.append(next(r for r in range(1,k+1) if any(set(ch)<=frozenset().union(*z) for z in combinations(s,r))))
  Q.append(row)
 A=[[] for _ in S];E=[]
 for i in range(len(S)):
  for j in range(i+1,len(S)):
   if sum((a^b).bit_count() for a,b in zip(S[i],S[j]))==1:A[i].append(j);A[j].append(i);E.append([i,j])
 return S,Q,A,E

def component_groups(A,Q):
 groups=[]
 for q in sorted(set(tuple(x) for x in Q)):
  unseen={i for i,x in enumerate(Q) if tuple(x)==q};parts=[]
  while unseen:
   start=min(unseen);unseen.remove(start);part=[start]
   for x in part:
    for y in A[x]:
     if y in unseen:unseen.remove(y);part.append(y)
   parts.append(sorted(part))
  groups.append({'q':list(q),'components':parts})
 return groups

def visit(A,allowed,a):
 if a not in allowed:return []
 seen={a};todo=[a]
 for x in todo:
  for y in A[x]:
   if y in allowed and y not in seen:seen.add(y);todo.append(y)
 return sorted(seen)

def scalar(A,c,a):
 dist={a:c[a]};heap=[(c[a],a)]
 while heap:
  z,x=heappop(heap)
  if dist[x]!=z:continue
  for y in A[x]:
   value=max(z,c[y])
   if value<dist.get(y,float('inf')):dist[y]=value;heappush(heap,(value,y))
 return dist

def path_check(path,A,C,a,b,expected,objective):
 need(isinstance(path,list) and path and path[0]==a and path[-1]==b,'path endpoints')
 need(all(type(x) is int and 0<=x<len(A) for x in path),'path state')
 need(all(y in A[x] for x,y in zip(path,path[1:])),'illegal path')
 z=[max(C[x][j] for x in path) for j in range(3)]
 need(z==expected if objective is None else z[objective]==expected,'path cost')

def pair_key(r):return (tuple(r['q']),tuple(r['components']))

def _verify(d,bound=5):
 need(d.get('version')=='16.37' and d.get('bound')==bound and d.get('view_counts')==[1,2,3],'domain')
 expected={(p,k) for p in shapes(bound) for k in (1,2,3)}
 keys=[(tuple(g['parents']),g['views']) for g in d['graphs']]
 need(len(keys)==len(set(keys)) and set(keys)==expected,'canonical graph universe')
 ordered=sorted(d['graphs'],key=lambda g:(len(g['parents']),g['parents'],g['views']))
 nonunit=[];endpoint=0;pair_count=0;states_count=0;distinctions=0;small=[]
 for g in ordered:
  p=tuple(g['parents']);k=g['views'];S,Q,A,E=raw_graph(p,k);groups=component_groups(A,Q)
  need(g['states']==S and g['q']==Q and g['edges']==E and g['groups']==groups,'state/profile/edge/component reconstruction')
  expected_pairs={(tuple(z['q']),(i,j)) for z in groups for i,j in combinations(range(len(z['components'])),2)}
  actual=[pair_key(r) for r in g['pairs']]
  need(len(actual)==len(set(actual)) and set(actual)==expected_pairs,'canonical component-pair universe')
  lookup={pair_key(r):r for r in g['pairs']};states_count+=len(S)
  for group in groups:
   q=group['q'];cs=group['components'];C=[]
   for qx in Q:
    delta=[abs(x-y) for x,y in zip(qx,q)];C.append((sum(delta),max(delta,default=0),sum(x!=0 for x in delta)))
   for i,j in combinations(range(len(cs)),2):
    r=lookup[tuple(q),(i,j)];a,b=cs[i][0],cs[j][0]
    need(r['representatives']==[a,b],'representative identity')
    primary=[scalar(A,[x[t] for x in C],a)[b] for t in range(3)]
    # Independent lex oracle: enumerate cost-threshold boxes in lexicographic order.
    lex=None
    for lim in product(*(sorted({c[t] for c in C}) for t in range(3))):
     allowed={x for x,c in enumerate(C) if all(c[t]<=lim[t] for t in range(3))}
     if b in visit(A,allowed,a):lex=list(lim);break
    need(r['primary']==primary and r['lex']==lex,'objective values')
    need(len(r['paths'])==3 and len(r['lower_reachable'])==3,'witness counts')
    for t in range(3):
     path_check(r['paths'][t],A,C,a,b,primary[t],t)
     cut=visit(A,{x for x,c in enumerate(C) if c[t]<primary[t]},a)
     need(r['lower_reachable'][t]==cut and b not in cut,'lower threshold certificate')
    path_check(r['lex_path'],A,C,a,b,lex,None)
    count=len(cs[i])*len(cs[j]);need(r['endpoint_pairs']==count,'endpoint coverage')
    if len(p)<=4:
     for aa in cs[i]:
      for bb in cs[j]:
       ends=sorted([S[aa],S[bb]]);small.append([list(p),k,q,*ends])
    endpoint+=count;pair_count+=1;distinctions+=primary!=lex
    if primary!=[1,1,1]:nonunit.append({'parents':list(p),'views':k,'pair':r})
 nonunit.sort(key=lambda w:(len(w['parents']),w['views'],w['parents'],w['pair']['q'],w['pair']['representatives']))
 need(d['nonunit']==nonunit,'nonunit witness set')
 need(d['outcome']==('NONUNIT_RETAINED_WITNESS' if nonunit else 'BOUNDED_UNIT_ONLY'),'verdict')
 need(d['universal_unit_law']=='UNRESOLVED','universal claim')
 summary={'graphs':len(ordered),'states':states_count,'component_pairs':pair_count,'endpoint_pairs':endpoint,'nonunit_pairs':len(nonunit),'objective_distinctions':distinctions}
 need(d['summary']==summary,'summary')
 return {'status':'VERIFIED','summary':summary,'canonical_inherited_endpoint_pairs':sorted(small),'outcome':d['outcome']}


def verify(d,bound=5):
 def schema(x):
  if type(x) in (int,str):return
  if type(x) is list:
   for y in x:schema(y)
   return
  if type(x) is dict:
   if any(type(k) is not str for k in x):raise ValueError('nonstring key')
   for y in x.values():schema(y)
   return
  raise ValueError('certificate primitive type')
 schema(d)
 try:return _verify(d,bound)
 except (KeyError,TypeError,IndexError) as e:raise ValueError('malformed certificate') from e
