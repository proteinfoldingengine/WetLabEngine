"""Guarded bit toggles, subset transversals and exhaustive reachable-state BFS."""
import itertools,json,sys
from functools import lru_cache
SCOPE='bc0bc6d34a4de9d8b65fcf2abcce54800c3e24ce'
COVERS=[(n,sum(1<<x for x in h)) for n in range(1,8) for h in itertools.combinations(range(7),n)]
CLAIMS={'band':[3,4],'marker_observed':False,'observer_origin':False,'guaranteed_progress':False,'observable_completion':False,'all_issued_commands_safe':False,'arbitrary_macro_composition':False,'mutable_phase_input':False}
@lru_cache(None)
def tau(s):
 for n,h in COVERS:
  if all(v&h for v in s):return n
 raise ValueError('empty support')
def source(b,c,z):return tuple((1|(2 if b>>r&1 else 0)|(4 if c>>r&1 else 0) if r<3 else 2 if r==3 else 4 if r==4 else 24)|(64 if z>>r&1 else 0) for r in range(6))
def core(s):return tuple(v&31 for v in s)
@lru_cache(None)
def templates(b,c):
 p=[r for r in range(3) if (b|c)>>r&1];d=[r for r in range(3) if r not in p]
 ops=[(r,x,a) for r in p for x,a in ((3,1),(0,0))]+[(r,3,1) for r in d]+[(r,0,0) for r in d]
 s=list(source(b,c,0));initial=tuple(s);s[5]^=8;prefix=[tuple(s)]
 for r,x,a in ops:s[r]^=1<<x;prefix.append(tuple(s))
 s[5]|=1
 return initial,prefix,tuple(s),ops
def policy(observation,b,c):
 initial,prefix,target,ops=templates(b,c)
 if observation==initial:return [(5,3,0),(5,5,1)]
 if observation==target:return [(5,5,0)]
 if observation in prefix:
  t=prefix.index(observation);return [ops[t] if t<len(ops) else (5,0,1)]
 return []
def outcomes(s,cmd,floors):
 r,x,a=cmd;out=[s]
 if bool(s[r]&(1<<x))==bool(a):return out
 v=list(s);v[r]^=1<<x;v=tuple(v)
 if all(q.bit_count()>=f for q,f in zip(v,floors)) and 3<=tau(v)<=4:out.append(v)
 return out
def graph(b,c,z,slack):
 start=source(b,c,z);floors=[v.bit_count() for v in start];floors[5]-=slack
 seen={start};todo=[start];raw=[]
 for s in todo:
  for cmd in policy(core(s),b,c):
   for v in outcomes(s,cmd,floors):
    raw.append((s,cmd,v))
    if v not in seen:seen.add(v);todo.append(v)
 states=sorted(seen);ids={s:i for i,s in enumerate(states)};initial,prefix,target,_=templates(b,c);nodes=[]
 for s in states:
  o=core(s);marked=bool(s[5]&32)
  rank=int(marked) if o==initial else 9 if o==target and marked else 10 if o==target else 2+prefix.index(o)
  nodes.append({'state':list(s),'core':list(o),'policy':[list(c) for c in policy(o,b,c)],'rank':rank,'tau':tau(s),'excess':sum(v.bit_count() for v in s)-sum(v.bit_count() for v in start),'target':o==target and not marked})
 edges=sorted([[ids[s],list(cmd),ids[v]] for s,cmd,v in raw])
 return {'id':[b,c,z,slack],'floors':floors,'start':ids[start],'nodes':nodes,'edges':edges}
def produce():
 out={'scope_commit':SCOPE,'claims':CLAIMS,'sources':[],'graphs':[]}
 for b,c,z in itertools.product(range(8),range(8),(0,24,32,63)):
  s=source(b,c,z);t=tau(s);ok=3<=t<=4;out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'protected':ok})
  if ok:
   for slack in (0,1):out['graphs'].append(graph(b,c,z,slack))
 return out
if __name__=='__main__':
 out=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sources':len(out['sources']),'protected_sources':sum(s['protected'] for s in out['sources']),'graphs':len(out['graphs']),'nodes':sum(len(g['nodes']) for g in out['graphs']),'edges':sum(len(g['edges']) for g in out['graphs'])}))
