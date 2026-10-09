"""Closed set slices and exact syntax-only graphs, representative hitting unions."""
import json,sys
from functools import lru_cache
def bits(v):return tuple(sum(2**x for x in q) for q in v)
@lru_cache(None)
def number(s):
 if not s:return 0
 roots=[{x for x in range(7) if v&2**x} for v in s];assert all(roots);f={frozenset()}
 for r in roots:f={h|{x} for h in f for x in r}
 return min(map(len,f))
def initial(b,c,z):
 roots=[{0}|({1} if b&2**j else set())|({2} if c&2**j else set()) for j in range(3)]+[{1},{2},{3,4}]
 for j in range(6):
  if z&2**j:roots[j].add(6)
 return roots
@lru_cache(None)
def path(b,c):
 src=initial(b,c,0);p=[j for j in range(3) if src[j]&{1,2}];r=[j for j in range(3) if j not in p];ss=[];commands=[]
 for n in range(9):
  v=[q.copy() for q in src]
  if n>=1:v[5].add(0)
  if n>=2:v[5].remove(3)
  for k,j in enumerate(p):
   if n>=3+2*k:v[j].add(3)
   if n>=4+2*k:v[j].remove(0)
  for k,j in enumerate(r):
   if n>=3+2*len(p)+k:v[j].add(3)
   if n>=3+2*len(p)+len(r)+k:v[j].remove(0)
  ss.append(list(bits(v)))
  if n==0:cmd=[5,0,1]
  elif n==1:cmd=[5,3,0]
  elif n<2+2*len(p):t=n-2;cmd=[p[t//2],3 if t%2==0 else 0,1 if t%2==0 else 0]
  elif n<2+2*len(p)+len(r):cmd=[r[n-2-2*len(p)],3,1]
  elif n<8:cmd=[r[n-2-2*len(p)-len(r)],0,0]
  else:continue
  commands.append(cmd)
 assert len({tuple(v) for v in ss})==9
 for n,cmd in enumerate(commands):
  q,x,a=cmd;v=ss[n][:];assert bool(v[q]&2**x)!=bool(a);v[q]^=2**x;assert v==ss[n+1]
 return {'id':[b,c],'covered':p,'deficit':r,'beta':max(1,len(r)),'commands':commands,'states':ss,'N':8}
def graph(b,c,z):
 src=initial(b,c,z);floors=list(map(len,src));p=path(b,c);states={}
 for n,core in enumerate(p['states']):
  v=[{x for x in range(5) if q&2**x} for q in core]
  for j in range(6):
   if z&2**j:v[j].add(6)
  s=bits(v);t=number(s);assert all(len(v[j])>=floors[j] for j in range(6));assert 3<=t<=4
  if n in (0,8):assert t==4
  if n==1:assert t==3
  excess=sum(map(len,v))-sum(map(len,src));assert excess<=p['beta'] and all(5 not in q for q in v)
  states[s]={'state':list(s),'core':core,'policy':[p['commands'][n]] if n<8 else [],'rank':n,'tau':t,'excess':excess,'target':n==8}
 ordered=sorted(states);ids={s:j for j,s in enumerate(ordered)};byrank={v['rank']:s for s,v in states.items()};edges=[]
 for n in range(8):
  s=byrank[n];v=byrank[n+1];cmd=p['commands'][n];q,x,a=cmd;assert cmd in states[s]['policy'] and bool(s[q]&2**x)!=bool(a);t=list(s);t[q]^=2**x;assert tuple(t)==v
  edges.extend([[ids[s],cmd,ids[s]],[ids[s],cmd,ids[v]]])
 assert not states[byrank[8]]['policy'] and states[byrank[8]]['target']
 # All successors passed worst-floor and exact-band checks, so guard adds no restriction.
 assert max(n['excess'] for n in states.values())==p['beta']
 return {'id':[b,c,z],'floors':floors,'start':ids[byrank[0]],'nodes':[states[s] for s in ordered],'edges':sorted(edges),'guarded_edges':sorted(edges)}
def fixtures():
 p=path(0,0);a=bits(initial(0,0,0));tri=bits([{0,1},{1,2},{0,2},{3,4}]);after=bits([{0,1},{1,2},{0,2},{0,3,4}]);assert number(tri)==3 and number(after)==2
 return {'disjoint':{'states':[list(a),p['states'][1],p['states'][-1]],'taus':[number(a),number(tuple(p['states'][1])),number(tuple(p['states'][-1]))]},'triangle':{'states':[list(tri),list(after)],'taus':[number(tri),number(after)],'floors':[2]*4,'command':[3,0,1]}}
@lru_cache(None)
def expected():
 out={'scope_commit':'2b7dc87aecd3b3b504e4c3be2270aa164bce13c6','claims':{'band':[3,4],'source_tau':4,'exact_tau_preserved':False,'guaranteed_progress':False,'observable_completion':True,'observer_origin':False,'runtime_guard_required':False,'universal_guard_derived':False,'all_issued_commands_safe':True,'new_labels':0,'all_tau3_sources_safe':False,'path_optimal':False,'mutable_phase_input':False},'paths':[path(b,c) for b in range(8) for c in range(8)],'sources':[],'graphs':[],'fixtures':fixtures()}
 for b in range(8):
  for c in range(8):
   for z in (0,24,32,63):
    src=initial(b,c,z);s=bits(src);t=number(s);rho=number(bits([q for q in src[:5] if 0 not in q]));prepared=[q.copy() for q in src];prepared[5].add(0);tp=number(bits(prepared));assert tp==min(t,1+rho);eligible=t==4
    if eligible:assert rho==2 and tp==3
    out['sources'].append({'id':[b,c,z],'state':list(s),'tau':t,'rho':rho,'prepared_tau':tp,'eligible':eligible})
    if eligible:out['graphs'].append(graph(b,c,z))
 return json.dumps(out,sort_keys=True,separators=(',',':'))
def verify(out):
 if json.dumps(out,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete visible-buffer identity/type/value mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent full syntax-only/guarded equivalence and exact stopping reconstruction')
