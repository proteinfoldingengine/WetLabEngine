"""Literal cyclic scripts, stack loop erasure, guarded BFS and subset hitting sets."""
import itertools,json,sys
from functools import lru_cache
SCOPE='b9eb2d1d2d87b8692e3b90d32524a95d3e389bf7'
CLAIMS={'band':[3,4],'marker_observed':False,'observer_origin':False,'guaranteed_progress':False,'observable_completion':False,'all_issued_commands_safe':False,'arbitrary_macro_composition':False,'mutable_phase_input':False,'raw_core_simple':False,'path_optimal':False}
COVERS=[(n,sum(1<<x for x in h)) for n in range(1,8) for h in itertools.combinations(range(7),n)]
@lru_cache(None)
def tau(s):
 for n,h in COVERS:
  if all(v&h for v in s):return n
 raise ValueError('empty support')
def source(b,c,z):return tuple((1|(2 if b>>r&1 else 0)|(4 if c>>r&1 else 0) if r<3 else 2 if r==3 else 4 if r==4 else 24)|(64 if z>>r&1 else 0) for r in range(6))
def core(s):return tuple(v&31 for v in s)
@lru_cache(None)
def path(b,c):
 pp=[7,8|b,16|c];cur=[0,1,2];incoming=3;s=list(source(b,c,0));s[5]^=8;raw=[s[:]];ops=[];covered=[];deficit=[]
 for j in range(3):
  u=0
  for k in range(3):
   if k!=j:u|=pp[k]
  p=[r for r in range(5) if pp[j]>>r&1 and u>>r&1];d=[r for r in range(5) if pp[j]>>r&1 and not u>>r&1];covered.append(p);deficit.append(d)
  seq=[(r,x,a) for r in p for x,a in ((incoming,1),(cur[j],0))]+[(r,incoming,1) for r in d]+[(r,cur[j],0) for r in d]
  for r,x,a in seq:
   assert bool(s[r]&(1<<x))!=bool(a);s[r]^=1<<x;raw.append(s[:]);ops.append([r,x,a])
  old=cur[j];cur[j]=incoming;incoming=old
 simple=[raw[0]];edges=[]
 for i,v in enumerate(raw[1:]):
  if v in simple:
   k=simple.index(v);simple=simple[:k+1];edges=edges[:k]
  else:simple.append(v);edges.append(i)
 return {'id':[b,c],'covered':covered,'deficit':deficit,'beta':max(1,*(len(d) for d in deficit)),'raw':raw,'commands':ops,'simple':simple,'edge_indices':edges,'N':len(ops)}
def policy(o,b,c):
 p=path(b,c);ss=[tuple(s) for s in p['simple']];target=list(ss[-1]);target[5]|=4
 if o==source(b,c,0):return [(5,3,0),(5,5,1)]
 if o==tuple(target):return [(5,5,0)]
 if o in ss:
  t=ss.index(o);return [tuple(p['commands'][p['edge_indices'][t]]) if t<len(ss)-1 else (5,2,1)]
 return []
def outcomes(s,cmd,floors):
 r,x,a=cmd;out=[s]
 if bool(s[r]&(1<<x))==bool(a):return out
 v=list(s);v[r]^=1<<x;v=tuple(v)
 if all(q.bit_count()>=f for q,f in zip(v,floors)) and 3<=tau(v)<=4:out.append(v)
 return out
def graph(b,c,z,slack):
 start=source(b,c,z);floors=[v.bit_count() for v in start];floors[5]-=slack;p=path(b,c)
 seen={start};todo=[start];raw=[]
 for s in todo:
  for cmd in policy(core(s),b,c):
   for v in outcomes(s,cmd,floors):
    raw.append((s,cmd,v))
    if v not in seen:seen.add(v);todo.append(v)
 states=sorted(seen);ids={s:i for i,s in enumerate(states)};ss=[tuple(v) for v in p['simple']];L=len(ss)-1;target=list(ss[-1]);target[5]|=4;nodes=[]
 for s in states:
  o=core(s);marked=bool(s[5]&32)
  rank=int(marked) if o==source(b,c,0) else L+3 if o==tuple(target) and marked else L+4 if o==tuple(target) else 2+ss.index(o)
  nodes.append({'state':list(s),'core':list(o),'policy':[list(c) for c in policy(o,b,c)],'rank':rank,'tau':tau(s),'excess':sum(v.bit_count() for v in s)-sum(v.bit_count() for v in start),'target':o==tuple(target) and not marked})
 lift=lambda v:tuple(q|(64 if z>>r&1 else 0)|(32 if r==5 and not slack else 0) for r,q in enumerate(v))
 return {'id':[b,c,z,slack],'floors':floors,'start':ids[start],'nodes':nodes,'edges':sorted([[ids[s],list(cmd),ids[v]] for s,cmd,v in raw]),'raw_taus':[tau(lift(v)) for v in p['raw']]}
def fixtures():
 p=path(0,0);x=p['raw'][6][:];x[5]|=32;y=x[:];y[5]|=1
 q=path(4,3);v=[s[:] for s in q['raw'][5:8]]
 for s in v:s[5]|=32
 return {'parking':{'states':[x,y,x],'commands':[[5,0,1],[5,0,0]],'taus':[tau(tuple(s)) for s in (x,y,x)]},'shared':{'id':[4,3,0],'states':v,'commands':q['commands'][5:7],'taus':[tau(tuple(s)) for s in v]}}
def produce():
 out={'scope_commit':SCOPE,'claims':CLAIMS,'paths':[path(b,c) for b,c in itertools.product(range(8),range(8))],'sources':[],'graphs':[],'fixtures':fixtures()}
 for b,c,z in itertools.product(range(8),range(8),(0,24,32,63)):
  s=source(b,c,z);t=tau(s);ok=3<=t<=4;out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'protected':ok})
  if ok:
   for slack in (0,1):out['graphs'].append(graph(b,c,z,slack))
 return out
if __name__=='__main__':
 out=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sources':len(out['sources']),'protected_sources':sum(s['protected'] for s in out['sources']),'paths':len(out['paths']),'paths_shortened':sum(len(p['edge_indices'])<p['N'] for p in out['paths']),'graphs':len(out['graphs']),'nodes':sum(len(g['nodes']) for g in out['graphs']),'edges':sum(len(g['edges']) for g in out['graphs'])}))
