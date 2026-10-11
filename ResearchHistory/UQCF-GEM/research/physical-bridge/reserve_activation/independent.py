"""Independent assignment/set reconstruction. Does not import producer."""
if not __debug__:raise RuntimeError('independent checker requires assertions enabled')
import functools,gzip,hashlib,itertools,json,pathlib,sys

def abstract_sources(fixture=False):
 cases=[(1,0,0),(2,1,3),(3,2,45),(2,2,15)] if fixture else ((p,q,m) for p in (1,2,3,4) for q in (0,1,2,3) for m in range(2**(p*q)))
 for p,q,m in cases:yield {'p':p,'q':q,'m':m}

def native_sources(fixture=False):
 carrier=[[i,j] for i,j in itertools.product(range(4),range(4,7))]
 if fixture:
  definitions=[('chain',[[0,4],[1,4],[1,5],[2,5],[2,6],[3,6]],1),('full',carrier,2),('empty',[],1),('cherry',[[0,4],[1,4]],1)]
  for name,edges,mult in definitions:
   s={'H':carrier,'G':edges,'a':[mult for _ in range(7)],'I':list(range(4)),'C':[4,5,6],'name':name}
   if name=='cherry':s['forced']=[['T',0,4],['V',1,-1]]
   yield s
  carrier2=[[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[5,6]]
  yield {'H':carrier2,'G':carrier2,'a':[2]*7,'I':[2,3,4,5],'C':[0,1,6],'name':'k2'}
 else:
  for number in range(2**12):
   edges=[edge for k,edge in enumerate(carrier) if (number//(2**k))%2]
   for mult in [1,2]:yield {'H':carrier,'G':edges,'a':[mult]*7,'I':[0,1,2,3],'C':[4,5,6]}

def abstract_record(s):
 p,q,number=s['p'],s['q'],s['m'];neighbors=[{w for w in range(q) if (number//(2**(i*q+w)))%2} for i in range(p)]
 # Enumerate all assignments, rather than accepting producer's traversal universe.
 universe=[]
 for st in itertools.product(range(-2,q),repeat=p):
  assigned=[v for v in st if v>=0]
  if st.count(-2)<=1 and len(assigned)==len(set(assigned)):universe.append(st)
 universe=set(universe);adj={};all_candidates={}
 for st in sorted(universe):
  if -2 in st:continue
  R={v for v in st if v>=0};actions=[];nexts=[]
  for i in range(p):
   if st[i]!=-1:continue
   missing=neighbors[i]-R
   options=[('V',-1,not missing)]+[('T',w,missing=={w}) for w in range(q) if w not in R]
   for kind,w,valid in options:
    actions.append((kind,i,w,valid))
    if valid:
     target=tuple((-2 if kind=='V' else w) if k==i else st[k] for k in range(p));assert target in universe;nexts.append((kind,i,w,target))
  adj[st]=nexts;all_candidates[st]=actions
 origin=(-1,)*p;reachable={origin}
 while True:
  expanded=reachable|{target for st in reachable for _,_,_,target in adj.get(st,[])}
  if expanded==reachable:break
  reachable=expanded
 states=sorted(reachable);idx={st:k for k,st in enumerate(states)}
 candidates=sorted([[idx[st],kind,i,w,ok] for st in states for kind,i,w,ok in all_candidates.get(st,[])])
 edges=sorted([[idx[st],kind,i,w,idx[target]] for st in states for kind,i,w,target in adj.get(st,[])])
 terminals=[idx[st] for st in states if -2 in st]
 R=set()
 while True:
  additions={w for ns in neighbors for w in ns if ns-{w}<=R}
  if additions<=R:break
  R|=additions
 Z=[i for i,ns in enumerate(neighbors) if ns<=R];surplus=len(Z)-len(R);assert bool(terminals)==(surplus>0)
 for st in states:
  if -2 in st:continue
  if not any(kind=='T' for kind,_,_,_ in adj[st]):assert {v for v in st if v>=0}==R
 current=origin;canonical=[]
 while -2 not in current:
  available=adj.get(current,[]);release=[x for x in available if x[0]=='V'];transfer=[x for x in available if x[0]=='T']
  if not release and not transfer:break
  kind,i,w,current=min(release or transfer,key=lambda x:(x[1],x[2]));canonical.append([kind,i,w])
 return {'kind':'abstract','source':s,'states':[list(x) for x in states],'source_index':idx[origin],'candidates':candidates,'edges':edges,'terminals':terminals,'closure':sorted(R),'Z':Z,'surplus':surplus,'canonical':canonical}

@functools.lru_cache(None)
def cover_number(footprints,roots):
 f=[set(x) for x in sorted(set(footprints)) if x];target=set(roots)
 for k in range(1,len(f)+1):
  if any(set().union(*items)==target for items in itertools.combinations(f,k)):return k
 return len(f)+1

def mask(s):return sum(2**i for i in s)
@functools.lru_cache(None)
def masks_and_exposed(stars,root_count):
 roots=set(range(root_count));original=[set(x) for x in stars];result=[]
 for number in range(2**root_count):
  hidden={k for k in roots if number//2**k%2};exposed=roots-hidden
  if exposed and not any(exposed<=x for x in original):result.append((number,tuple(sorted(exposed))))
 return tuple(result)
@functools.lru_cache(None)
def hidden_valid(stars,root_count,footprint):
 f=set(footprint)
 return all(not set(exposed)<=f for _,exposed in masks_and_exposed(stars,root_count))

def native_record(s):
 edges=[tuple(x) for x in s['H']];saturated=set(map(tuple,s['G']));multiplicities=s['a'];donor_types=s['I'];cover=s['C'];vertices=list(range(len(multiplicities)));roots=set(range(len(edges)))
 assert edges==sorted(set(edges)) and all(u in vertices and v in vertices and u<v for u,v in edges)
 assert saturated<=set(edges) and len(saturated)==len(s['G']);assert all(type(a)==int and a>0 for a in multiplicities)
 stars=[{k for k,e in enumerate(edges) if v in e} for v in vertices];star_key=tuple(tuple(sorted(f)) for f in stars)
 assert all(stars) and cover_number(star_key,tuple(sorted(roots))) in [3,4]
 assert donor_types and len(set(donor_types))==len(donor_types) and set(donor_types)<=set(vertices)
 assert len(set(cover))==len(cover)<=4 and set(cover)<=set(vertices) and all(set(e)&set(cover) for e in edges)
 assert all(multiplicities[i]>1 for i in set(donor_types)&set(cover)) and all(len(set(e)&set(donor_types))<2 for e in saturated)
 first=[];original=[]
 for v,a in enumerate(multiplicities):first.append(len(original));original.extend([set(stars[v]) for _ in range(a)])
 anchors=[first[v] for v in cover];donor_labels={i:first[i]+(1 if i in cover else 0) for i in donor_types}
 neighbor={i:set().union(*(set(e)-{i} for e in saturated if i in e)) for i in donor_types}
 assigned={};steps=[]
 if 'forced' in s:steps=[list(x) for x in s['forced']]
 else:
  while True:
   unused=sorted(set(donor_types)-assigned.keys());R=set(assigned.values());free=[i for i in unused if neighbor[i]<=R]
   if free:steps.append(['V',free[0],-1]);break
   pair=next(((i,w) for i in unused for w in sorted(neighbor[i]-R) if neighbor[i]<=R|{w}),None)
   if pair is None:break
   i,w=pair;steps.append(['T',i,w]);assigned[i]=w
 footprints=[set(f) for f in original];states=[[mask(f) for f in footprints]];operations=[];boundaries=[];used=set();R=set();released=False;cost=0
 for kind,i,w in steps:
  assert i in donor_types and i not in used and not released;label=donor_labels[i]
  if kind=='T':
   assert w not in R and neighbor[i]-R=={w};pivot=edges.index(tuple(sorted([i,w])));target={pivot};cost+=len(stars[i])+len(stars[w])-2
  else:assert kind=='V' and neighbor[i]<=R;target=set();cost+=len(stars[i])
  for root in sorted(footprints[label]-target):
   footprints[label].remove(root);operations.append([label,root,0]);states.append([mask(f) for f in footprints])
  if kind=='T':
   for root in sorted(stars[w]-footprints[label]):
    footprints[label].add(root);operations.append([label,root,1]);states.append([mask(f) for f in footprints])
   R.add(w)
  else:released=True
  used.add(i);boundaries.append([len(operations),sorted(used),sorted(R)])
 floors=[multiplicities[u]+multiplicities[v] if (u,v) in saturated else 1 for u,v in edges]
 evaluations=[];distinct=sorted(set(tuple(row) for row in states))
 for row in distinct:
  fs=[{k for k in roots if value//2**k%2} for value in row];counts=[sum(k in f for f in fs) for k in sorted(roots)];t=cover_number(tuple(tuple(sorted(f)) for f in fs),tuple(sorted(roots)))
  assert all(actual>=required for actual,required in zip(counts,floors));assert 3<=t<=4
  assert all(any(f<=star for star in stars) for f in fs) and all(fs[label]==original[label] for label in anchors)
  assert all(hidden_valid(star_key,len(edges),tuple(sorted(f))) for f in set(map(frozenset,fs)))
  evaluations.append([list(row),counts,t])
 assert len(operations)==cost;assert all(0 not in row for row in states[:-1]);assert (0 in states[-1])==released
 reverse_operations=[[label,root,1-value] for label,root,value in operations[::-1]];reverse_states=[[mask(f) for f in footprints]]
 for label,root,value in reverse_operations:
  assert (root in footprints[label])!=bool(value)
  if value:footprints[label].add(root)
  else:footprints[label].remove(root)
  reverse_states.append([mask(f) for f in footprints])
 assert footprints==original and reverse_states==states[::-1]
 protected=[number for number,_ in masks_and_exposed(star_key,len(edges))]
 activated=set()
 while True:
  add={w for ns in neighbor.values() for w in ns if ns-{w}<=activated}
  if add<=activated:break
  activated|=add
 compensated=[i for i in donor_types if neighbor[i]<=activated];assert released==(len(compensated)>len(activated))
 return {'kind':'native','source':s,'closure':sorted(activated),'Z':compensated,'floors':floors,'anchors':anchors,'donors':[[i,donor_labels[i]] for i in donor_types],'macros':steps,'boundaries':boundaries,'ops':operations,'states':states,'evaluations':evaluations,'reverse_ops':reverse_operations,'reverse_states':reverse_states,'released':released,'protected_masks':protected,'distinct_states':len(distinct),'slice_occurrences':len(states),'hidden_checks':len(distinct)*len(protected),'cost':cost}

def verify(data,fixture=False,identity_path=None):
 assert data['schema']=='reserve-activation-v1' and data['fixture']==fixture
 handle=None
 if identity_path is None:iterator=iter(data['records'])
 else:
  try:handle=gzip.open(identity_path,'rt');iterator=iter(handle)
  except OSError as e:raise AssertionError('Missing canonical stream') from e
 counts=dict(abstract_sources=0,abstract_states=0,abstract_candidates=0,abstract_edges=0,abstract_terminals=0,native_sources=0,native_positive=0,native_macros=0,native_edits=0,slice_occurrences=0,distinct_states=0,hidden_checks=0);digests=[]
 try:
  for declarations,reconstruct in [(abstract_sources,abstract_record),(native_sources,native_record)]:
   for source in declarations(fixture):
    expected=reconstruct(source)
    try:actual=next(iterator)
    except StopIteration as e:raise AssertionError('Truncated canonical stream') from e
    if isinstance(actual,str):actual=json.loads(actual)
    assert actual==expected,'Complete canonical record mismatch'
    digests.append(hashlib.sha256((json.dumps(expected,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest())
    if expected['kind']=='abstract':
     counts['abstract_sources']+=1
     for suffix in ['states','candidates','edges','terminals']:counts['abstract_'+suffix]+=len(expected[suffix])
    else:
     counts['native_sources']+=1;counts['native_positive']+=int(expected['released']);counts['native_macros']+=len(expected['macros']);counts['native_edits']+=len(expected['ops'])
     for key in ['slice_occurrences','distinct_states','hidden_checks']:counts[key]+=expected[key]
  marker=object();assert next(iterator,marker) is marker,'Extra canonical record'
 except (OSError,EOFError,json.JSONDecodeError) as e:raise AssertionError('Corrupt canonical stream') from e
 finally:
  if handle:handle.close()
 assert counts==data['counts'] and digests==data['record_sha256']
 if identity_path is not None and 'identity_archive_sha256' in data:assert hashlib.sha256(pathlib.Path(identity_path).read_bytes()).hexdigest()==data['identity_archive_sha256']
 return True
if __name__=='__main__':
 p=pathlib.Path(sys.argv[1]);d=json.loads(p.read_text());verify(d,identity_path=str(p)+'.identities.jsonl.gz');result={'accepted':True,'counts':d['counts'],'certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'canonical_sha256':d['identity_archive_sha256']};pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
