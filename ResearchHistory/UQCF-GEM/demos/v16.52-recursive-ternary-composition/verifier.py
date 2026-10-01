"""Independent support sets, exact corpus reconstruction and total excursion."""
from itertools import product,combinations
from functools import lru_cache
from coverage import verify_identities
L=();B=(L,L);T=(L,L,L);A=(T,L,L);SHAPES={'A':A,'F':(T,T,L),'G':(T,T,T),'H':(A,T,B),'J':((T,L),(L,T),T)}
class InterfaceNotPreserved(ValueError):pass
SCOPE='finite rooted ordered trees with internal arity two or three; higher arity unresolved'
def topology(tree):
 children={};parent={};internal=[]
 def walk(t):
  v=len(children);children[v]=[]
  if t:
   internal.append(v)
   for branch in t:
    c=walk(branch);children[v].append(c);parent[c]=v
  return v
 walk(tree);return children,parent,internal
def hitting(supports):
 labels=sorted(set.union(*supports))
 for n in range(1,len(supports)+1):
  for chosen in combinations(labels,n):
   if all(set(chosen)&s for s in supports):return n
 raise ValueError('empty child support')
@lru_cache(None)
def root_feasible(widths,r,k):
 if k<1:return False
 def counts(remaining,n):
  if n==0:yield ();return
  for i in range(remaining+1):
   for tail in counts(remaining-i,n-1):yield (i,)+tail
 d=len(widths);regions=2**d-1
 for ns in counts(k,regions):
  if any(sum(ns[j-1] for j in range(1,regions+1) if j>>i&1)<w for i,w in enumerate(widths)):continue
  supports=[{j for j in range(1,regions+1) if ns[j-1] and j>>i&1} for i in range(d)]
  if hitting(supports)==r:return True
 return False
def model(tree,target,k,permutation='identity',mode='compact'):
 ch,parents,internal=topology(tree)
 if any(len(cs) not in (0,2,3) for cs in ch.values()):raise ValueError('scope')
 if len(target)!=len(internal) or any(type(x)!=int or x not in range(1,len(ch[internal[i]])+1) for i,x in enumerate(target)):raise ValueError('target')
 Q=dict(zip(internal,target));w={}
 def size(v):
  if not ch[v]:w[v]=1
  else:
   sizes=[size(c) for c in ch[v]]
   if Q[v]==1:w[v]=max(sizes)
   elif Q[v]==len(sizes):w[v]=sum(sizes)
   else:w[v]=max(*sizes,(sum(sizes)+1)//2)
  return w[v]
 M=size(0)
 if type(k)!=int or k<M:raise ValueError('palette width')
 supports={}
 def fill(v,palette):
  supports[v]=set(palette);offset=0
  for c in ch[v]:
   if Q[v]==1:assigned=palette[:w[c]]
   elif Q[v]==len(ch[v]):assigned=palette[offset:offset+w[c]]
   else:
    chosen={palette[j%w[v]] for j in range(offset,offset+w[c])};assigned=[x for x in palette if x in chosen]
   offset+=w[c];fill(c,assigned)
 fill(0,list(range(k)))
 def raw(s):return [sum(1<<v for v,S in s.items() if j in S) for j in range(k)]
 endpoint=raw(supports)
 if permutation not in ('identity','reversal','cyclic') or mode not in ('compact','inflated'):raise ValueError('case mode')
 def perm(j):return j if permutation=='identity' else k-1-j if permutation=='reversal' else (j+1)%k
 start={v:{perm(j) for j in S} for v,S in supports.items()}
 if mode=='inflated':
  for v in range(1,len(ch)):
   for j in range(k):
    if j in start[v] or j not in start[parents[v]]:continue
    start[v].add(j)
    if any(hitting([start[c] for c in ch[u]])!=Q[u] for u in internal):start[v].remove(j)
 return M,raw(start),endpoint
@lru_cache(None)
def cached_topology(tree):return topology(tree)
def profile_check(tree,k,raw):
 ch,parents,internal=cached_topology(tree);n=len(ch)
 if not isinstance(raw,list) or len(raw)!=k or any(type(z)!=int or z<0 or z>=1<<n for z in raw):raise InterfaceNotPreserved('state representation')
 supports=[{j for j,z in enumerate(raw) if z>>v&1} for v in range(n)]
 if supports[0]!=set(range(k)):raise InterfaceNotPreserved('root changed')
 if any(not S for S in supports) or any(not supports[v]<=supports[p] for v,p in parents.items()):raise InterfaceNotPreserved('state admission')
 return [hitting([supports[c] for c in ch[v]]) for v in internal]
def path_check(tree,k,target,path,start,end):
 if not isinstance(path,list) or not path or path[0]!=start:raise InterfaceNotPreserved('path start')
 peaks=[0,0,0]
 for i,raw in enumerate(path):
  profile=profile_check(tree,k,raw)
  if len(profile)!=len(target):raise ValueError('target length')
  defects=[abs(a-b) for a,b in zip(profile,target)]
  costs=[sum(defects),max(defects,default=0),sum(bool(z) for z in defects)]
  if costs[0]>1:raise InterfaceNotPreserved('total excursion exceeds one')
  peaks=[max(a,b) for a,b in zip(peaks,costs)]
  if i and sum((a^b).bit_count() for a,b in zip(raw,path[i-1]))!=1:raise InterfaceNotPreserved('nonprimitive move')
 if profile_check(tree,k,path[0])!=target or path[-1]!=end or profile_check(tree,k,path[-1])!=target:raise InterfaceNotPreserved('exact canonical endpoint')
 return peaks
@lru_cache(None)
def expected_specs():
 rows=[]
 for name,tree in SHAPES.items():
  ch,parents,internal=topology(tree)
  for profile in product(*(range(1,len(ch[v])+1) for v in internal)):
   q=list(profile);M=model(tree,q,len(ch))[0]
   for k in (M,M+1):
    for perm in ('identity','reversal','cyclic'):
     for mode in ('compact','inflated'):rows.append({'tree':name,'q':q,'k':k,'permutation':perm,'mode':mode})
 return rows
def verify(doc):
 if set(doc)!={'schema','scope','kind','cases'} or doc['schema']!=1 or doc['scope']!=SCOPE or doc['kind'] not in ('campaign','canonical_coverage_control'):raise ValueError('schema/scope')
 rows=doc['cases']
 if not isinstance(rows,list) or any(not isinstance(row,dict) for row in rows):raise ValueError('record list')
 verify_identities([row.get('spec') for row in rows],expected_specs());results=[];width_checks={}
 for index,row in enumerate(rows):
  if set(row)!={'spec','width','start','path','failure'}:raise ValueError('record keys')
  if row['failure'] is not None:raise InterfaceNotPreserved('recorded construction failure: '+str(index))
  s=row['spec'];tree=SHAPES[s['tree']];q=s['q'];k=s['k'];M,start,end=model(tree,q,k,s['permutation'],s['mode'])
  if doc['kind']=='canonical_coverage_control':start=end
  if type(row['width'])!=int or row['width']!=M or row['start']!=start:raise ValueError('width/start')
  ch,parents,internal=topology(tree)
  for vertex in internal:
   # Local canonical support cardinalities, independently reconstructed at each vertex.
   sizes=tuple(sum(bool(z>>c&1) for z in end) for c in ch[vertex]);target=q[internal.index(vertex)]
   localM=max(sizes) if target==1 else sum(sizes) if target==len(sizes) else max(max(sizes),(sum(sizes)+1)//2)
   key=(sizes,target)
   if key not in width_checks:
    if not root_feasible(sizes,target,localM) or root_feasible(sizes,target,localM-1):raise InterfaceNotPreserved('minimum palette refuted')
    width_checks[key]=localM
  if doc['kind']=='canonical_coverage_control' and row['path']!=[end]:raise ValueError('control singleton path')
  peaks=path_check(tree,k,q,row['path'],start,end)
  results.append({'case':index,'steps':len(row['path'])-1,'peaks':peaks})
 return {'status':'VERIFIED','kind':doc['kind'],'outcome':'RECURSIVE_INTERFACE_VALIDATED' if doc['kind']=='campaign' else 'COVERAGE_CONTROL_VERIFIED','cases':len(rows),'root_two_cases':sum(row['spec']['q'][0]==2 for row in rows),'total_moves':sum(r['steps'] for r in results),'cases_with_unit_excursion':sum(r['peaks'][0]==1 for r in results),'construction_failures':[],'scope':SCOPE,'nonunit_witness':'NOT_CLAIMED','width_checks':[{'widths':list(key[0]),'root_target':key[1],'minimum_palette':M} for key,M in sorted(width_checks.items())],'results':results}
