"""Independent support sets, exact corpus reconstruction and total excursion."""
from itertools import product,combinations
from functools import lru_cache
from coverage import verify_identities
L=();C=(L,L);D=(C,L);F=(C,C);SHAPES={'T':(C,C,C),'U':(C,D,F)}
SCOPE='one ternary root over finite full binary child trees; repeated ternary composition unresolved'
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
def root_feasible(a,b,c,r,k):
 if k<1:return False
 def counts(remaining,n):
  if n==0:yield ();return
  for i in range(remaining+1):
   for tail in counts(remaining-i,n-1):yield (i,)+tail
 for ns in counts(k,7):
  if any(sum(ns[j-1] for j in range(1,8) if j>>i&1)<w for i,w in enumerate((a,b,c))):continue
  supports=[{j for j in range(1,8) if ns[j-1] and j>>i&1} for i in range(3)]
  if hitting(supports)==r:return True
 return False
def model(tree,target,k,permutation='identity',mode='compact'):
 ch,parents,internal=topology(tree)
 if len(ch[0])!=3 or any(len(ch[v]) not in (0,2) for v in ch if v):raise ValueError('scope')
 if len(target)!=len(internal) or any(type(x)!=int or x not in ((1,2,3) if i==0 else (1,2)) for i,x in enumerate(target)):raise ValueError('target')
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
 supports={0:set(range(k))};offset=0
 for c in ch[0]:
  if Q[0]==1:assigned=list(range(w[c]))
  elif Q[0]==3:assigned=list(range(offset,offset+w[c]))
  else:assigned=sorted({j%M for j in range(offset,offset+w[c])})
  offset+=w[c]
  def binary_fill(v,palette):
   supports[v]=set(palette)
   if ch[v]:
    left,right=ch[v];binary_fill(left,palette[:w[left]])
    shift=0 if Q[v]==1 else w[left];binary_fill(right,palette[shift:shift+w[right]])
  binary_fill(c,assigned)
 def raw(s):return [sum(1<<v for v,S in s.items() if j in S) for j in range(k)]
 endpoint=raw(supports)
 if permutation not in ('identity','reversal','cyclic') or mode not in ('compact','interface_and_binary_inflated'):raise ValueError('case mode')
 def perm(j):return j if permutation=='identity' else k-1-j if permutation=='reversal' else (j+1)%k
 start={v:{perm(j) for j in S} for v,S in supports.items()}
 if mode=='interface_and_binary_inflated':
  for c in ch[0]:
   for j in range(k):
    if j in start[c]:continue
    start[c].add(j)
    if hitting([start[x] for x in ch[0]])!=Q[0]:start[c].remove(j)
  for v in internal[1:]:
   if Q[v]==1:
    for c in ch[v]:start[c]=set(start[v])
 return M,raw(start),endpoint
@lru_cache(None)
def cached_topology(tree):return topology(tree)
def profile_check(tree,k,raw):
 ch,parents,internal=cached_topology(tree);n=len(ch)
 if not isinstance(raw,list) or len(raw)!=k or any(type(z)!=int or z<0 or z>=1<<n for z in raw):raise ValueError('state representation')
 supports=[{j for j,z in enumerate(raw) if z>>v&1} for v in range(n)]
 if supports[0]!=set(range(k)):raise ValueError('root changed')
 if any(not S for S in supports) or any(not supports[v]<=supports[p] for v,p in parents.items()):raise ValueError('state admission')
 return [hitting([supports[c] for c in ch[v]]) for v in internal]
def path_check(tree,k,target,path,start,end):
 if not isinstance(path,list) or not path or path[0]!=start:raise ValueError('path start')
 peaks=[0,0,0]
 for i,raw in enumerate(path):
  profile=profile_check(tree,k,raw)
  if len(profile)!=len(target):raise ValueError('target length')
  defects=[abs(a-b) for a,b in zip(profile,target)]
  costs=[sum(defects),max(defects,default=0),sum(bool(z) for z in defects)]
  if costs[0]>1:raise ValueError('total excursion exceeds one')
  peaks=[max(a,b) for a,b in zip(peaks,costs)]
  if i and sum((a^b).bit_count() for a,b in zip(raw,path[i-1]))!=1:raise ValueError('nonprimitive move')
 if profile_check(tree,k,path[0])!=target or path[-1]!=end or profile_check(tree,k,path[-1])!=target:raise ValueError('exact canonical endpoint')
 return peaks
def expected_specs():
 rows=[]
 for name,n in (('T',3),('U',6)):
  for inner in product((1,2),repeat=n):
   for r in (1,2,3):
    q=[r,*inner];M=model(SHAPES[name],q,16)[0]
    for k in (M,M+1):
     for perm in ('identity','reversal','cyclic'):
      for mode in ('compact','interface_and_binary_inflated'):rows.append({'tree':name,'q':q,'k':k,'permutation':perm,'mode':mode})
 return rows
def verify(doc):
 if set(doc)!={'schema','scope','cases'} or doc['schema']!=1 or doc['scope']!=SCOPE:raise ValueError('schema/scope')
 rows=doc['cases']
 if not isinstance(rows,list) or any(not isinstance(row,dict) for row in rows):raise ValueError('record list')
 verify_identities([row.get('spec') for row in rows],expected_specs());results=[];width_checks={}
 for index,row in enumerate(rows):
  if set(row)!={'spec','width','start','path','failure'}:raise ValueError('record keys')
  if row['failure'] is not None:raise ValueError('recorded construction failure: '+str(index))
  s=row['spec'];tree=SHAPES[s['tree']];q=s['q'];k=s['k'];M,start,end=model(tree,q,k,s['permutation'],s['mode'])
  if type(row['width'])!=int or row['width']!=M or row['start']!=start:raise ValueError('width/start')
  # Derive child widths from canonical endpoint cardinalities, independently of producer.
  ch,parents,internal=topology(tree);sizes=tuple(sum(bool(z>>c&1) for z in end) for c in ch[0]);key=(*sizes,q[0])
  if key not in width_checks:
   if not root_feasible(*sizes,q[0],M) or root_feasible(*sizes,q[0],M-1):raise ValueError('minimum palette refuted')
   width_checks[key]=M
  peaks=path_check(tree,k,q,row['path'],start,end)
  results.append({'case':index,'steps':len(row['path'])-1,'peaks':peaks})
 return {'status':'VERIFIED','outcome':'TERNARY_Q2_INTERFACE_VALIDATED','cases':len(rows),'root_two_cases':sum(row['spec']['q'][0]==2 for row in rows),'total_moves':sum(r['steps'] for r in results),'cases_with_unit_excursion':sum(r['peaks'][0]==1 for r in results),'construction_failures':[],'scope':SCOPE,'nonunit_witness':'NOT_CLAIMED','width_checks':[{'widths':list(key[:3]),'root_target':key[3],'minimum_palette':M} for key,M in sorted(width_checks.items())],'results':results}
