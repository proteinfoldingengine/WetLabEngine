"""Closed role-prefix sets, last-exit erasure and full outcome reconstruction."""
import json,sys
from functools import lru_cache
def bits(roots):return tuple(sum(2**x for x in r) for r in roots)
@lru_cache(None)
def number(s):
 roots=[{x for x in range(7) if v&2**x} for v in s];assert all(roots);families={frozenset()}
 for r in roots:families={f|{x} for f in families for x in r}
 return min(map(len,families))
def pats(b,c):return [{0,1,2},{3}|{j for j in range(3) if b&2**j},{4}|{j for j in range(3) if c&2**j}]
def initial(b,c,z):
 pp=pats(b,c);v=[{j for j in range(3) if r in pp[j]} for r in range(5)]+[{3,4}]
 for j in range(6):
  if z&2**j:v[j].add(6)
 return v
@lru_cache(None)
def path(b,c):
 pp=pats(b,c);assignment=[0,1,2];incoming=3;raw=[];cmds=[];covered=[];deficit=[]
 for j in range(3):
  u=set().union(*(pp[k] for k in range(3) if k!=j));p=sorted(pp[j]&u);r=sorted(pp[j]-u);covered.append(p);deficit.append(r);m=len(pp[j])
  start=[{assignment[k] for k in range(3) if q in pp[k]} for q in range(5)]+[{4}]
  for t in range(2*m+1):
   v=[q.copy() for q in start]
   for k,q in enumerate(p):
    if t>=2*k+1:v[q].add(incoming)
    if t>=2*k+2:v[q].remove(assignment[j])
   for k,q in enumerate(r):
    if t>=2*len(p)+k+1:v[q].add(incoming)
    if t>=2*len(p)+len(r)+k+1:v[q].remove(assignment[j])
   if j==0 or t>0:raw.append(list(bits(v)))
   if t<2*len(p):cmds.append([p[t//2],incoming if t%2==0 else assignment[j],1 if t%2==0 else 0])
   elif t<2*len(p)+len(r):cmds.append([r[t-2*len(p)],incoming,1])
   elif t<2*m:cmds.append([r[t-2*len(p)-len(r)],assignment[j],0])
  old=assignment[j];assignment[j]=incoming;incoming=old
 # Last-exit construction is independent of the producer's chronological stack.
 simple=[];edge_indices=[];i=0
 while True:
  simple.append(raw[i]);last=max(j for j,v in enumerate(raw) if v==raw[i])
  if last==len(raw)-1:break
  edge_indices.append(last);i=last+1
 assert len({tuple(v) for v in simple})==len(simple)
 for n,i in enumerate(edge_indices):
  assert raw[i]==simple[n] and raw[i+1]==simple[n+1]
  q,x,a=cmds[i];v=simple[n][:];assert bool(v[q]&2**x)!=bool(a);v[q]^=2**x;assert v==simple[n+1]
 goal=[{assignment[j] for j in range(3) if r in pp[j]} for r in range(5)]+[{4}]
 assert tuple(simple[-1])==bits(goal)
 return {'id':[b,c],'covered':covered,'deficit':deficit,'beta':max(1,*(len(r) for r in deficit)),'raw':raw,'commands':cmds,'simple':simple,'edge_indices':edge_indices,'N':len(cmds)}
def graph(b,c,z,slack):
 src=initial(b,c,z);floors=list(map(len,src));floors[5]-=slack;p=path(b,c);L=len(p['simple'])-1;states={};changes=[];policies={}
 def lift(core,marked):
  v=[{x for x in range(5) if q&2**x} for q in core]
  for j in range(6):
   if z&2**j:v[j].add(6)
  if marked:v[5].add(5)
  return v
 def add(v,rank,policy,target=False):
  s=bits(v);o=bits([q&set(range(5)) for q in v]);entry={'state':list(s),'core':list(o),'policy':policy,'rank':rank,'tau':number(s),'excess':sum(map(len,v))-sum(map(len,src)),'target':target}
  assert all(len(v[j])>=floors[j] for j in range(6));assert number(bits(src))<=entry['tau']<=4 and entry['excess']<=p['beta']
  if o in policies:assert policies[o]==policy
  policies[o]=policy
  if s in states:assert states[s]==entry
  states[s]=entry;return s
 source_states=[]
 for marked in (False,True):source_states.append(add(lift(list(bits(initial(b,c,0))),marked),int(marked),[[5,3,0],[5,5,1]]))
 changes.append((source_states[0],[5,5,1],source_states[1]))
 goal=p['simple'][-1][:];goal[5]|=4
 clean=add(lift(goal,False),L+4,[[5,5,0]],True);dirty=add(lift(goal,True),L+3,[[5,5,0]]);changes.append((dirty,[5,5,0],clean))
 for marked in (False,True):
  if not marked and not slack:continue
  prev=None
  for t,v in enumerate(p['simple']):
   cmd=p['commands'][p['edge_indices'][t]] if t<L else [5,2,1];s=add(lift(v,marked),2+t,[cmd])
   changes.append((source_states[int(marked)],[5,3,0],s) if prev is None else (prev,states[prev]['policy'][0],s));prev=s
  changes.append((prev,[5,2,1],dirty if marked else clean))
 raw_taus=[]
 for v in p['raw']:
  roots=lift(v,not bool(slack));assert all(len(roots[j])>=floors[j] for j in range(6));t=number(bits(roots));assert 3<=number(bits(src))<=t<=4;assert sum(map(len,roots))-sum(map(len,src))<=p['beta'];raw_taus.append(t)
 ordered=sorted(states);ids={s:j for j,s in enumerate(ordered)};edges=[(s,cmd,s) for s in ordered for cmd in states[s]['policy']]+changes
 for s,cmd,v in changes:
  assert cmd in states[s]['policy'] and states[v]['rank']>states[s]['rank'];q,x,a=cmd;ss=list(s);assert bool(ss[q]&2**x)!=bool(a);ss[q]^=2**x;assert tuple(ss)==v
 assert {s for s in states if not any(e[0]==s for e in changes)}=={clean}
 assert states[dirty]['core']==states[clean]['core'] and states[dirty]['policy']==states[clean]['policy']
 return {'id':[b,c,z,slack],'floors':floors,'start':ids[source_states[0]],'nodes':[states[s] for s in ordered],'edges':sorted([[ids[s],cmd,ids[v]] for s,cmd,v in edges]),'raw_taus':raw_taus}
def fixtures():
 p=path(0,0);x=p['raw'][6][:];x[5]|=32;y=x[:];y[5]|=1
 q=path(4,3);v=[s[:] for s in q['raw'][5:8]]
 for s in v:s[5]|=32
 assert x==([*y[:5],y[5]^1]) and v[0]==v[-1];assert q['commands'][5:7]==[[2,0,0],[2,0,1]]
 assert len(q['simple'])<len(q['raw'])
 return {'parking':{'states':[x,y,x],'commands':[[5,0,1],[5,0,0]],'taus':[number(tuple(s)) for s in (x,y,x)]},'shared':{'id':[4,3,0],'states':v,'commands':q['commands'][5:7],'taus':[number(tuple(s)) for s in v]}}
@lru_cache(None)
def expected():
 out={'scope_commit':'b9eb2d1d2d87b8692e3b90d32524a95d3e389bf7','claims':{'band':[3,4],'marker_observed':False,'observer_origin':False,'guaranteed_progress':False,'observable_completion':False,'all_issued_commands_safe':False,'arbitrary_macro_composition':False,'mutable_phase_input':False,'raw_core_simple':False,'path_optimal':False},'paths':[path(b,c) for b in range(8) for c in range(8)],'sources':[],'graphs':[],'fixtures':fixtures()}
 for b in range(8):
  for c in range(8):
   for z in (0,24,32,63):
    s=bits(initial(b,c,z));t=number(s);ok=t in (3,4);out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'protected':ok})
    if ok:
     for slack in (0,1):out['graphs'].append(graph(b,c,z,slack))
 return json.dumps(out,sort_keys=True,separators=(',',':'))
def verify(out):
 if json.dumps(out,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete cyclic path/graph identity/type/value mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete pipeline and guarded graph reconstruction')
