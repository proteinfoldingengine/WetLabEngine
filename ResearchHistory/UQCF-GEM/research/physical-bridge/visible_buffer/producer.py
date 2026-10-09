"""Visible scripts and syntax-only BFS; tau is verification metadata, never a gate."""
import itertools,json,sys
from functools import lru_cache
SCOPE='2b7dc87aecd3b3b504e4c3be2270aa164bce13c6'
CLAIMS={'band':[3,4],'source_tau':4,'exact_tau_preserved':False,'guaranteed_progress':False,'observable_completion':True,'observer_origin':False,'runtime_guard_required':False,'universal_guard_derived':False,'all_issued_commands_safe':True,'new_labels':0,'all_tau3_sources_safe':False,'path_optimal':False,'mutable_phase_input':False}
COVERS=[(n,sum(1<<x for x in h)) for n in range(1,8) for h in itertools.combinations(range(7),n)]
@lru_cache(None)
def tau(s):
 if not s:return 0
 for n,h in COVERS:
  if all(v&h for v in s):return n
 raise ValueError('empty support')
def source(b,c,z):return tuple((1|(2 if b>>r&1 else 0)|(4 if c>>r&1 else 0) if r<3 else 2 if r==3 else 4 if r==4 else 24)|(64 if z>>r&1 else 0) for r in range(6))
def core(s):return tuple(v&31 for v in s)
@lru_cache(None)
def path(b,c):
 p=[r for r in range(3) if (b|c)>>r&1];r=[j for j in range(3) if j not in p]
 ops=[[5,0,1],[5,3,0]]+[[q,x,a] for q in p for x,a in ((3,1),(0,0))]+[[q,3,1] for q in r]+[[q,0,0] for q in r]
 s=list(source(b,c,0));ss=[s[:]]
 for q,x,a in ops:assert bool(s[q]&2**x)!=bool(a);s[q]^=2**x;ss.append(s[:])
 return {'id':[b,c],'covered':p,'deficit':r,'beta':max(1,len(r)),'commands':ops,'states':ss,'N':len(ops)}
def policy(o,b,c):
 p=path(b,c);ss=[tuple(v) for v in p['states']]
 if o in ss:
  n=ss.index(o);return [tuple(p['commands'][n])] if n<len(p['commands']) else []
 return []
def syntax_outcomes(s,cmd):
 q,x,a=cmd;out=[s]
 if bool(s[q]&2**x)!=bool(a):
  v=list(s);v[q]^=2**x;out.append(tuple(v))
 return out
def graph(b,c,z):
 start=source(b,c,z);floors=[v.bit_count() for v in start];p=path(b,c);seen={start};todo=[start];raw=[]
 for s in todo:
  for cmd in policy(core(s),b,c):
   for v in syntax_outcomes(s,cmd):
    raw.append((s,cmd,v))
    if v not in seen:seen.add(v);todo.append(v)
 states=sorted(seen);ids={s:j for j,s in enumerate(states)};cores=[tuple(v) for v in p['states']];nodes=[]
 for s in states:
  rank=cores.index(core(s));nodes.append({'state':list(s),'core':list(core(s)),'policy':[list(c) for c in policy(core(s),b,c)],'rank':rank,'tau':tau(s),'excess':sum(v.bit_count() for v in s)-sum(v.bit_count() for v in start),'target':rank==p['N']})
 edges=sorted([[ids[s],list(c),ids[v]] for s,c,v in raw])
 # This is a separate verification comparison, not the production transition rule.
 guarded=sorted([[ids[s],list(c),ids[v]] for s,c,v in raw if s==v or all(q.bit_count()>=f for q,f in zip(v,floors)) and 3<=tau(v)<=4])
 return {'id':[b,c,z],'floors':floors,'start':ids[start],'nodes':nodes,'edges':edges,'guarded_edges':guarded}
def fixtures():
 a=source(0,0,0);p=path(0,0);tri=(3,6,5,24);after=(3,6,5,25)
 return {'disjoint':{'states':[list(a),p['states'][1],p['states'][-1]],'taus':[tau(a),tau(tuple(p['states'][1])),tau(tuple(p['states'][-1]))]},'triangle':{'states':[list(tri),list(after)],'taus':[tau(tri),tau(after)],'floors':[2]*4,'command':[3,0,1]}}
def produce():
 out={'scope_commit':SCOPE,'claims':CLAIMS,'paths':[path(b,c) for b,c in itertools.product(range(8),range(8))],'sources':[],'graphs':[],'fixtures':fixtures()}
 for b,c,z in itertools.product(range(8),range(8),(0,24,32,63)):
  s=source(b,c,z);t=tau(s);rho=tau(tuple(v for v in s[:5] if not v&1));prepared=list(s);prepared[5]|=1;tp=tau(tuple(prepared));eligible=t==4
  out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'rho':rho,'prepared_tau':tp,'eligible':eligible})
  if eligible:out['graphs'].append(graph(b,c,z))
 return out
if __name__=='__main__':
 out=produce();open(sys.argv[1] if len(sys.argv)>1 else 'certificate.json','w').write(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sources':len(out['sources']),'eligible_sources':sum(s['eligible'] for s in out['sources']),'paths':len(out['paths']),'graphs':len(out['graphs']),'nodes':sum(len(g['nodes']) for g in out['graphs']),'syntax_edges':sum(len(g['edges']) for g in out['graphs']),'guarded_edges':sum(len(g['guarded_edges']) for g in out['graphs'])}))
