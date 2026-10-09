"""Closed-form set states/edges and root-representative hitting unions; no producer import."""
import json,sys
from functools import lru_cache
def bits(roots):return tuple(sum(2**x for x in r) for r in roots)
@lru_cache(None)
def number(s):
 roots=[{x for x in range(7) if v&2**x} for v in s];assert all(roots);families={frozenset()}
 for r in roots:families={f|{x} for f in families for x in r}
 return min(map(len,families))
def initial(b,c,z):
 v=[{0}|({1} if b&2**j else set())|({2} if c&2**j else set()) for j in range(3)]+[{1},{2},{3,4}]
 for j in range(6):
  if z&2**j:v[j].add(6)
 return v
def graph(b,c,z,slack):
 src=initial(b,c,z);p=[j for j in range(3) if 1 in src[j] or 2 in src[j]];r=[j for j in range(3) if j not in p];floors=list(map(len,src));floors[5]-=slack
 states={};changes=[];policies={}
 def add(v,rank,policy,target=False):
  s=bits(v);o=bits([q&set(range(5)) for q in v]);entry={'state':list(s),'core':list(o),'policy':policy,'rank':rank,'tau':number(s),'excess':sum(map(len,v))-sum(map(len,src)),'target':target}
  assert all(len(v[j])>=floors[j] for j in range(6));assert number(bits(src))<=entry['tau']<=4
  assert entry['excess']<=max(1,len(r))
  if o in policies:assert policies[o]==policy
  policies[o]=policy
  if s in states:assert states[s]==entry
  states[s]=entry;return s
 source_states=[]
 for marked in (False,True):
  v=[q.copy() for q in src]
  if marked:v[5].add(5)
  source_states.append(add(v,int(marked),[[5,3,0],[5,5,1]]))
 changes.append((source_states[0],[5,5,1],source_states[1]))
 target_roots=[(q-{0})|{3} if j<3 else (q-{3})|{0} if j==5 else q.copy() for j,q in enumerate(src)]
 target_clean=add(target_roots,10,[[5,5,0]],True);target_roots[5].add(5);target_dirty=add(target_roots,9,[[5,5,0]])
 changes.append((target_dirty,[5,5,0],target_clean))
 for marked in (False,True):
  if not marked and not slack:continue
  previous=None
  for t in range(7):
   v=[q.copy() for q in src];v[5].remove(3)
   if marked:v[5].add(5)
   for k,j in enumerate(p):
    if t>=2*k+1:v[j].add(3)
    if t>=2*k+2:v[j].remove(0)
   for k,j in enumerate(r):
    if t>=2*len(p)+k+1:v[j].add(3)
    if t>=2*len(p)+len(r)+k+1:v[j].remove(0)
   if t<2*len(p):cmd=[p[t//2],3 if t%2==0 else 0,1 if t%2==0 else 0]
   elif t<2*len(p)+len(r):cmd=[r[t-2*len(p)],3,1]
   elif t<6:cmd=[r[t-2*len(p)-len(r)],0,0]
   else:cmd=[5,0,1]
   current=add(v,2+t,[cmd])
   if previous is None:changes.append((source_states[int(marked)],[5,3,0],current))
   else:changes.append((previous,states[previous]['policy'][0],current))
   previous=current
  changes.append((previous,[5,0,1],target_dirty if marked else target_clean))
 ordered=sorted(states);ids={s:j for j,s in enumerate(ordered)}
 edges=[(s,cmd,s) for s in ordered for cmd in states[s]['policy']]+changes
 for s,cmd,v in changes:
  assert cmd in states[s]['policy'];assert states[v]['rank']>states[s]['rank']
  q,x,a=cmd;ss=[set(j for j in range(7) if s[i]&2**j) for i in range(6)]
  assert (x in ss[q])!=bool(a)
  if a:ss[q].add(x)
  else:ss[q].remove(x)
  assert bits(ss)==v
 assert {s for s in states if not any(e[0]==s for e in changes)}=={target_clean}
 assert states[target_dirty]['core']==states[target_clean]['core']
 assert states[target_dirty]['policy']==states[target_clean]['policy']
 # Reject a false progress interpretation: every state/request has its NOOP edge.
 assert all((s,cmd,s) in edges for s in states for cmd in states[s]['policy'])
 return {'id':[b,c,z,slack],'floors':floors,'start':ids[source_states[0]],'nodes':[states[s] for s in ordered],'edges':sorted([[ids[s],cmd,ids[v]] for s,cmd,v in edges])}
@lru_cache(None)
def expected():
 out={'scope_commit':'bc0bc6d34a4de9d8b65fcf2abcce54800c3e24ce','claims':{'band':[3,4],'marker_observed':False,'observer_origin':False,'guaranteed_progress':False,'observable_completion':False,'all_issued_commands_safe':False,'arbitrary_macro_composition':False,'mutable_phase_input':False},'sources':[],'graphs':[]}
 for b in range(8):
  for c in range(8):
   for z in (0,24,32,63):
    s=bits(initial(b,c,z));t=number(s);ok=t in (3,4);out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'protected':ok})
    if ok:
     for slack in (0,1):out['graphs'].append(graph(b,c,z,slack))
 return json.dumps(out,sort_keys=True,separators=(',',':'))
def verify(out):
 if json.dumps(out,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete canonical graph identity/type/value mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete guarded graph reconstruction')
