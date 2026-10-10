"""Independent set-support checker. Never imports producer or its helpers."""
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def hit(roots):
 if not roots:return 0
 if any(not a for a in roots):return 99
 first=min(roots,key=len)
 return 1+min(hit(tuple(a for a in roots if x not in a)) for x in first)
def supports(state):return tuple(frozenset(i for i in range(a.bit_length()) if a&(2**i)) for a in state)
def raw(roots):return tuple(sum(2**x for x in a) for a in roots)
@functools.lru_cache(None)
def original(q):return tuple([frozenset([0,i+1]) for i in range(q)]+[frozenset(range(1,q+1)),frozenset([q+1])])
@functools.lru_cache(None)
def footprints(roots,q):return [frozenset(i for i,a in enumerate(roots) if x in a) for x in range(q+2)]
def gate(roots,q,h):return all(a<=frozenset(range(q+2)) for a in roots) and all(len(a)>=f for a,f in zip(roots,[2]*q+[h,1])) and hit(roots)<=4 and all(any(a<=b for b in footprints(original(q),q)) for a in footprints(roots,q))
def hidden_tau(roots,m):return min(hit(roots),1+hit(tuple(a for i,a in enumerate(roots) if not m&(2**i))))
@functools.lru_cache(None)
def vectors(q,h):
 out=[]
 for size in range(q+3):
  for labels in itertools.combinations_with_replacement(range(q+2),size):
   v=tuple(labels.count(x) for x in range(q+2))
   roots=tuple(frozenset(i for i,x in enumerate(labels) if j in footprints(original(q),q)[x]) for j in range(q+2))
   if all(len(a)>=f for a,f in zip(roots,[2]*q+[h,1])):
    assert hit(roots)==3;out.append(v)
 return sorted(out)
@functools.lru_cache(None)
def layers(q,h):
 source=original(q);seen={source};out=[[source]]
 for depth in range(4):
  frontier=set()
  for rootsets in out[-1]:
   for position in range(q+2):
    for label in range(q+2):
     changed=list(rootsets);changed[position]=changed[position]^frozenset([label]);changed=tuple(changed)
     if changed not in seen and gate(changed,q,h):frontier.add(changed)
  out.append(sorted(frontier,key=raw));seen.update(frontier)
 return [[list(raw(a)) for a in L] for L in out]
def toggles(q,p,J):
 out=[[q,p+1]]
 for r in J:out.extend([[r,p+1],[r,r+1],[q,r+1]])
 return out
def path(start,operations):
 cur=supports(start);out=[cur]
 for root,label in operations:
  nxt=list(cur);nxt[root]=nxt[root]^frozenset([label]);cur=tuple(nxt);out.append(cur)
 return out
def image(roots,pi):return tuple(frozenset(pi[x] for x in a) for a in roots)
def verify(D,n=7):
 hidden=set();slices=0
 def check(q,h,states,exact=True):
  nonlocal slices
  for a in states:
   assert gate(a,q,h) and (hit(a)==3 if exact else 3<=hit(a)<=4),'unsafe state'
   hidden.add((q,a));slices+=1
 sourceids=[(q,h) for q in range(2,n+1) for h in range(1,q+1)]
 assert [(a['q'],a['h']) for a in D['sources']]==sourceids,'source identities'
 for a in D['sources']:
  q,h=a['q'],a['h'];s=original(q);assert a['source']==list(raw(s)) and a['floors']==[2]*q+[h,1]
  assert a['footprints']==[sum(2**i for i in f) for f in footprints(s,q)]
  assert a['protected_masks']==[m for m in range(2**(q+2)) if hidden_tau(s,m)==3]
  assert a['anchored_failures']==list(range(q+2))
  for r in range(q+2):assert not gate(tuple(a-frozenset([r]) for a in s),q,h)
  if h==q:
   for i in range(q+2):
    for x in range(q+2):assert not gate(path(raw(s),[[i,x]])[-1],q,h)
 assert [(a['q'],a['h']) for a in D['capacity']]==sourceids,'capacity identities'
 for a in D['capacity']:
  q,h=a['q'],a['h'];V=vectors(q,h);assert a['vectors']==[list(v) for v in V],'complete multiplicity vectors'
  m=min(map(sum,V));assert a['minimum']==m==min(q+2,h+3);assert a['witness']==list(min(v for v in V if sum(v)==m))
 primaryids=[(q,h,p,r) for q,h in sourceids for p in range(q) for r in range(q) if p!=r]
 assert [(a['q'],a['h'],a['p'],a['r']) for a in D['primary']]==primaryids,'primary identities'
 for a in D['primary']:
  q,h,p,r=(a[k] for k in ['q','h','p','r']);ops=toggles(q,p,[r]);assert a['ops']==ops,'route operations';S=path(raw(original(q)),ops);assert a['states']==[list(raw(s)) for s in S]
  assert a['positive']==(h<=q-2)
  if h<=q-2:check(q,h,S);assert not footprints(S[-1],q)[r+1]
  elif h==q-1:check(q,h,S[:-1]);assert not gate(S[-1],q,h)
  else:assert not gate(S[1],q,h)
 batchids=[(q,h,p,list(J)) for q,h in sourceids if h<=q-2 for p in range(q) for m in range(1,q-h) for J in itertools.combinations([r for r in range(q) if r!=p],m)]
 assert [(a['q'],a['h'],a['p'],a['J']) for a in D['batch']]==batchids,'batch identities'
 for a in D['batch']:
  q,h,p,J=(a[k] for k in ['q','h','p','J']);assert a['ops']==toggles(q,p,J);S=path(raw(original(q)),a['ops']);assert a['states']==[list(raw(s)) for s in S];check(q,h,S)
  survivor=next(x+1 for x in range(q) if x!=p and x not in J);assert all(all(root&{0,survivor,q+1} for root in s) for s in S)
  assert all(not footprints(S[-1],q)[r+1] for r in J);assert len(a['ops'])==1+3*len(J)
  if len(J)==q-h-1:assert len(set().union(*S[-1]))==h+3
 bfsids=[(q,h) for q,h in [(3,1),(4,1),(4,2)] if q<=n];assert [(a['q'],a['h']) for a in D['bfs']]==bfsids,'BFS identities'
 for a in D['bfs']:
  q,h=a['q'],a['h'];L=layers(q,h);assert a['layers']==L,'complete BFS layers';assert a['first_vacancy']==4
  for depth,layer in enumerate(L):
   S=[supports(s) for s in layer];check(q,h,S,exact=False)
   assert any(len(set().union(*s))<q+2 for s in S)==(depth==4)
 assert [a['pi'] for a in D['permutations']]==list(map(list,itertools.permutations(range(5)))),'permutation identities'
 for a in D['permutations']:
  S=path(raw(original(3)),a['ops']);assert a['states']==[list(raw(s)) for s in S];check(3,1,S);assert S[-1]==image(original(3),a['pi'])
  assert a['ops'][:4]==toggles(3,0,[1]) and a['ops'][-4:]==[[i,a['pi'][x]] for i,x in toggles(3,0,[1])[::-1]]
 pairs=[([1,2,3,4,0],[4,0,1,2,3]),([2,0,1,4,3],[1,0,3,2,4]),([4,3,2,1,0],[1,2,3,4,0])]
 assert [(a['pi'],a['sigma']) for a in D['renewal']]==pairs,'renewal identities'
 for a in D['renewal']:
  S=path(raw(original(3)),a['ops']);assert a['states']==[list(raw(s)) for s in S];check(3,1,S);assert S[-1]==image(image(original(3),a['pi']),a['sigma'])
  b=a['boundary'];L=toggles(3,0,[1]);PL=[[i,a['pi'][x]] for i,x in L];assert S[b]==image(original(3),a['pi']),'renewal intermediate restoration';assert a['ops'][:4]==L and a['ops'][b-4:b]==PL[::-1] and a['ops'][b:b+4]==PL and a['ops'][-4:]==[[i,a['sigma'][x]] for i,x in PL[::-1]],'renewal release/restoration'
 checks=0
 for q,s in hidden:
  for mask in range(2**(q+2)):
   if hidden_tau(original(q),mask)==3:assert 3<=hidden_tau(s,mask)<=4;checks+=1
 assert D['control']=={'mask':20,'source_tau':hidden_tau(original(3),20),'candidate_tau':hidden_tau(supports((3,7,9,14,16)),20)}
 counts={k:len(D[k]) for k in ['sources','primary','capacity','batch','bfs','permutations','renewal']};counts.update(positive=sum(a['positive'] for a in D['primary']),route_and_bfs_slices=slices,unique_hidden_states=len(hidden),hidden_checks=checks,capacity_vectors=sum(len(a['vectors']) for a in D['capacity']),bfs_layer_sizes=[[len(L) for L in a['layers']] for a in D['bfs']]);assert D['counts']==counts,'counts';return counts
if __name__=='__main__':
 counts=verify(json.loads(pathlib.Path(sys.argv[1]).read_text()));result={'status':'ACCEPTED','complete_identity_comparison':True,'counts':counts};pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
