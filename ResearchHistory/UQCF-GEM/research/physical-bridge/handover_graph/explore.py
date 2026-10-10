# Explicit exploratory lexicographic witness search, not an exhaustive scientific verdict.
import producer as p,itertools,json,collections,pathlib
stats={'multisets_examined':0,'protected_sources':0,'floor_cases':0,'no_anchored_cases':0,'static_vacancy_cases':0}
found=None
for v in itertools.combinations_with_replacement(range(1,32),5):
 stats['multisets_examined']+=1
 s=p.roots(v,5)
 if p.tau(s) not in (3,4):continue
 stats['protected_sources']+=1;M=p.maxima(s,5)
 choices=[[K for K in M if J&~K==0] for J in v]
 for mode in (0,1):
  stats['floor_cases']+=1;f=tuple(max(1,a.bit_count()-mode) for a in s)
  anchored=False
  for r in range(5):
   for a in itertools.product(*[([0] if x==r else choices[x]) for x in range(5)]):
    if p.gate(a,f,5):anchored=True;break
   if anchored:break
  if anchored:continue
  stats['no_anchored_cases']+=1
  if not any(p.gate(a+(0,),f,5) for a in itertools.combinations_with_replacement(M,4)):continue
  stats['static_vacancy_cases']+=1
  V,E,C=p.graph(M,f,5);start=p.expand(v,M);component=next(c for c in C if start in c)
  candidates=[a for a in component if 0 in a]
  if not candidates:continue
  target=min(candidates);adj={a:[] for a in V}
  for a,b in E:adj[a].append(b);adj[b].append(a)
  prev={start:None};todo=[start]
  for a in todo:
   if a==target:break
   for b in adj[a]:
    if b not in prev:prev[b]=a;todo.append(b)
  path=[];a=target
  while a is not None:path.append(a);a=prev[a]
  path.reverse();ops=[]
  for x,(J,K) in enumerate(zip(v,start)):
   ops.extend([i,x] for i in range(5) if K>>i&1 and not J>>i&1)
  for a,b in zip(path,path[1:]):ops+=p.lift(a,b)
  states=p.path_states(v,ops);assert states[-1]==target and all(p.gate(a,f,5) for a in states)
  found={'source':list(s),'footprints':list(v),'floors':list(f),'mode':mode,'maxima':list(M),'graph_path':[list(a) for a in path],'toggles':ops,'target':list(p.roots(target,5)),'visited_vertices':len(prev)};break
 if found:break
 if stats['multisets_examined']%10000==0:print(json.dumps(stats),flush=True)
r={'status':'FOUND' if found else 'COMPLETE_FIVE_BY_FIVE_NO_WITNESS','stats':stats,'witness':found,'limit':324632};pathlib.Path('handover_graph/exploratory.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
