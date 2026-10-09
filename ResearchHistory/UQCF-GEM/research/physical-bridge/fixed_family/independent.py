"""Set supports, representative unions and truth-derived exhaustive fibers."""
import json,sys
from functools import lru_cache
@lru_cache(None)
def number(roots):
 covers={frozenset()}
 for r in roots:covers={h|{x} for h in covers for x in r}
 return min(map(len,covers))
def ht(roots):return number(tuple(tuple(sorted(r)) for r in roots))
@lru_cache(None)
def expected():
 states=[];fibers=[]
 for b in range(8):
  for c in range(8):
   co=[{0}|({1} if b&2**j else set())|({2} if c&2**j else set()) for j in range(3)]+[{1},{2},{3,4}];full=[];valid=[];values=[];tc=ht(co);assert tc in (3,4)
   for z in range(64):
    s=[r|({6} if z&2**j else set()) for j,r in enumerate(co)];t=ht(s);full.append(s);values.append(t);ok=t in (3,4)
    if ok:valid.append(z)
    states.append({'id':[b,c,z],'supports':[sum(2**x for x in r) for r in s],'tau':t,'protected':ok,'floors':list(map(len,co))})
   for f in range(1,64):
    selected=[j for j in range(6) if f&2**j];common=set.intersection(*(co[j] for j in selected));tb=ht([r for j,r in enumerate(co) if j not in selected]);yes=[];no=[]
    for z in valid:
     out=set.intersection(*(full[z][j] for j in selected))
     (no if out else yes).append(z)
    cat='mixed' if yes and no else 'forced_true' if yes else 'forced_false';assert valid and values[f]==min(tc,1+tb);assert (not no)==(tb<=1)
    if no:assert f in no and values[f]>=3
    fibers.append({'id':[b,c,f],'core_intersection':sorted(common),'complement_tau':tb,'category':cat,'preparation_possible':not no,'admissible_masks':valid[:],'yes_masks':yes,'no_masks':no,'witness':{'mask':f,'tau':values[f],'protected':values[f] in (3,4)}})
 return json.dumps({'scope_commit':'57d9cdd48eddf84c499a99ce8c62ec7cee2650ea','claims':{'fixed_family':True,'full_completion_fiber':True,'hidden_edits_covered':False,'retargeting_covered':False,'native_access_derived':False,'floors_above_core_covered':False,'requires_nonempty_hidden_palette':True,'nontrivial_universal_core_preparation':False},'states':states,'fibers':fibers},sort_keys=True,separators=(',',':'))
def verify(d):
 if json.dumps(d,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete fixed-family source/fiber/value/type mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete native completion-fiber and preparation classification')
