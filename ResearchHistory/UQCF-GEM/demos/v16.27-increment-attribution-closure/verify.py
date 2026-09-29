from itertools import combinations
import importlib.util,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parent/'engine.py';s=importlib.util.spec_from_file_location('prod',P);prod=importlib.util.module_from_spec(s);s.loader.exec_module(prod)
# verifier recomputes h/atomic independently enough for witness and re-enumerates endpoint path signatures
def need(x,m):
 if not x:raise ValueError(m)
def h(p,ys):
 U=set().union(*map(set,ys));vals=[1]
 for v in U:
  K={w for w in U if w and p[w]==v}
  if K:vals.append(min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r))))
 return max(vals)
def verify_path(p,before,after,path):
 cur=tuple(before);seen={};total=0
 for d in path:
  need(tuple(map(tuple,d['before']))==cur,'chain');i,leaf=d['index'],d['leaf'];need(leaf in cur[i] and leaf not in after[i],'event');need(not any(p[w]==leaf and w in cur[i] for w in cur[i]),'nonleaf');nxt=list(cur);nxt[i]=tuple(v for v in cur[i] if v!=leaf);nxt=tuple(nxt);need(set().union(*map(set,nxt))==set().union(*map(set,cur)),'union');delta=h(p,nxt)-h(p,cur);need(delta in (0,1) and d['delta_h']==delta,'delta');seen[(i,leaf)]=delta;total+=delta;cur=nxt
 need(cur==tuple(after),'endpoint');need(total==h(p,after)-h(p,before),'total');return seen
def verify_witness(d):
 need(d.get('version')=='16.27','version');p=tuple(d['parents']);before=tuple(map(tuple,d['before']));after=tuple(map(tuple,d['after']));A=verify_path(p,before,after,d['path_a']);B=verify_path(p,before,after,d['path_b']);chg=sorted(k for k in A if A[k]!=B[k]);need(chg and [list(x) for x in chg]==d['changed_events'],'changed');return True
def verify_document(doc,bound=4):
 need(doc['version']=='16.27' and doc['bound']==bound,'doc');fresh=prod.produce(bound);need(all(doc[k]==fresh[k] for k in ('endpoints','multi_path','path_dependent','paths','digest')),'enumeration');need(doc['first_witness'] is not None,'witness');verify_witness(doc['first_witness']);return {k:doc[k] for k in ('endpoints','multi_path','path_dependent','paths','digest')}
