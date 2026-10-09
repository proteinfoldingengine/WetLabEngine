"""Literal hidden completions and the analytic fixed-family classification."""
import itertools,json,sys
from functools import lru_cache
CLAIMS={'fixed_family':True,'full_completion_fiber':True,'hidden_edits_covered':False,'retargeting_covered':False,'native_access_derived':False,'floors_above_core_covered':False,'requires_nonempty_hidden_palette':True,'nontrivial_universal_core_preparation':False}
@lru_cache(None)
def tau(s):
 if not s:return 0
 for n in range(1,8):
  for h in itertools.combinations(range(7),n):
   v=sum(2**x for x in h)
   if all(r&v for r in s):return n
 raise ValueError('empty root')
def core(b,c):return tuple(1|(2 if b>>j&1 else 0)|(4 if c>>j&1 else 0) for j in range(3))+(2,4,24)
def state(c,z):return tuple(v|(64 if z>>j&1 else 0) for j,v in enumerate(c))
def intersection(s):
 out=127
 for r in s:out&=r
 return out
def produce():
 states=[];fibers=[]
 for b,c in itertools.product(range(8),range(8)):
  co=core(b,c);ss=[state(co,z) for z in range(64)];ts=[tau(s) for s in ss];valid=[z for z,t in enumerate(ts) if 3<=t<=4]
  for z,s in enumerate(ss):states.append({'id':[b,c,z],'supports':list(s),'tau':ts[z],'protected':z in valid,'floors':[v.bit_count() for v in co]})
  for f in range(1,64):
   inds=[j for j in range(6) if f>>j&1];ci=intersection(tuple(co[j] for j in inds));tb=tau(tuple(co[j] for j in range(6) if j not in inds));yes=[z for z in valid if intersection(tuple(ss[z][j] for j in inds))==0];no=[z for z in valid if z not in yes]
   category='forced_false' if ci else 'forced_true' if tb<=1 else 'mixed'
   fibers.append({'id':[b,c,f],'core_intersection':[x for x in range(7) if ci>>x&1],'complement_tau':tb,'category':category,'preparation_possible':tb<=1,'admissible_masks':valid,'yes_masks':yes,'no_masks':no,'witness':{'mask':f,'tau':ts[f],'protected':f in valid}})
 return {'scope_commit':'57d9cdd48eddf84c499a99ce8c62ec7cee2650ea','claims':CLAIMS,'states':states,'fibers':fibers}
if __name__=='__main__':
 d=produce();open(sys.argv[1],'w').write(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'states':len(d['states']),'protected_states':sum(s['protected'] for s in d['states']),'fibers':len(d['fibers']),'categories':{k:sum(f['category']==k for f in d['fibers']) for k in ['forced_true','forced_false','mixed']},'protected_fiber_memberships':sum(len(f['admissible_masks']) for f in d['fibers']),'preparable':sum(f['preparation_possible'] for f in d['fibers'])}))
