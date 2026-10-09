"""Set construction, representative unions, containment moments, complete fibers."""
import json,sys
from functools import lru_cache
@lru_cache(None)
def number(roots):
 covers={frozenset()}
 for r in roots:covers={s|{x} for s in covers for x in r}
 return min(map(len,covers))
@lru_cache(None)
def expected():
 queries=[[x] for x in range(7)]+[[x,y] for x in range(7) for y in range(x+1,7)];rows=[]
 for b in range(8):
  for c in range(8):
   for z in range(64):
    roots=[{0}|({1} if b&2**j else set())|({2} if c&2**j else set()) for j in range(3)]+[{1},{2},{3,4}]
    for j in range(6):
     if z&2**j:roots[j].add(6)
    contain=[sum(x in r for r in roots) for x in range(7)];moments=[6-n for n in contain]
    for x,y in queries[7:]:moments.append(6-contain[x]-contain[y]+sum(x in r and y in r for r in roots))
    f=[r for r in roots if 0 not in r and 4 not in r];assert len(f)==2
    direct=[sum(x not in r for r in f) for x in range(7)];common=set.intersection(*f);t=number(tuple(tuple(sorted(r)) for r in roots));protected=t in (3,4)
    rows.append({'id':[b,c,z],'state':[sum(2**x for x in r) for r in roots],'tau':t,'protected':protected,'admitted':protected and not common,'moments':moments,'outside_misses':direct,'decoded':direct})
 def partition(width):
  byrecord=sorted((tuple(s['id'][:2]+s['moments'][:width]),tuple(s['id']),s['admitted']) for s in rows if s['protected']);out=[];last=None;flags=set()
  for rec,ident,adm in byrecord:
   if rec!=last:
    out.append({'record':list(rec),'members':[],'mixed':False});last=rec;flags=set()
   out[-1]['members'].append(list(ident));flags.add(adm);out[-1]['mixed']=len(flags)>1
  return out
 out={'scope_commit':'5023e725651ce62bf3dc7a7e99ecc1dd5cd74ab6','claims':{'sufficient_global_order':2,'global_order1_sufficient':False,'native_access_derived':False,'minimal_bits':False,'initial_band_supplied':True,'complete_palette_supplied':True},'floors':[1,1,1,1,1,2],'queries':queries,'sources':rows,'fibers1':partition(7),'fibers2':partition(28),'witness':[[0,0,3],[0,0,24]]}
 assert any(f['mixed'] for f in out['fibers1']) and not any(f['mixed'] for f in out['fibers2'])
 return json.dumps(out,sort_keys=True,separators=(',',':'))
def verify(out):
 if json.dumps(out,sort_keys=True,separators=(',',':'))!=expected():raise ValueError('complete source/record/fiber identity mismatch')
 return True
if __name__=='__main__':verify(json.load(open(sys.argv[1])));print('PASS independent complete global record transfer and fiber reconstruction')
