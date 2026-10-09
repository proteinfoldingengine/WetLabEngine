"""Global count transfer, literal supports and dictionary record fibers."""
import itertools,json,sys
from functools import lru_cache
QUERIES=[list(h) for k in (1,2) for h in itertools.combinations(range(7),k)]
MASKS=[sum(1<<x for x in h) for h in QUERIES]
CLAIMS={'sufficient_global_order':2,'global_order1_sufficient':False,'native_access_derived':False,'minimal_bits':False,'initial_band_supplied':True,'complete_palette_supplied':True}
@lru_cache(None)
def tau(s):
 for k in range(1,8):
  for h in itertools.combinations(range(7),k):
   mask=sum(1<<x for x in h)
   if all(v&mask for v in s):return k
 raise ValueError('empty root')
def source(b,c,z):return tuple((1|(2 if b>>r&1 else 0)|(4 if c>>r&1 else 0) if r<3 else 2 if r==3 else 4 if r==4 else 24)|(64 if z>>r&1 else 0) for r in range(6))
def decode(m):
 table={tuple(q):v for q,v in zip(QUERIES,m)}
 return [table[tuple(sorted({0,x}))]-table[(x,)]+table[tuple(sorted({4,x}))] for x in range(7)]
def fibers(rows,order):
 groups={}
 for s in rows:
  if s['protected']:
   key=tuple(s['id'][:2]+s['moments'][:7 if order==1 else 28]);groups.setdefault(key,[]).append(s)
 return [{'record':list(k),'members':[s['id'] for s in v],'mixed':len({s['admitted'] for s in v})>1} for k,v in sorted(groups.items())]
def produce():
 rows=[]
 for b,c,z in itertools.product(range(8),range(8),range(64)):
  s=source(b,c,z);m=[sum(not(v&h) for v in s) for h in MASKS];d=decode(m);outside=[sum(not(s[r]&2**x) for r in (3,4)) for x in range(7)];t=tau(s);protected=3<=t<=4
  rows.append({'id':[b,c,z],'state':list(s),'tau':t,'protected':protected,'admitted':protected and all(d),'moments':m,'outside_misses':outside,'decoded':d})
 return {'scope_commit':'5023e725651ce62bf3dc7a7e99ecc1dd5cd74ab6','claims':CLAIMS,'floors':[1,1,1,1,1,2],'queries':QUERIES,'sources':rows,'fibers1':fibers(rows,1),'fibers2':fibers(rows,2),'witness':[[0,0,3],[0,0,24]]}
if __name__=='__main__':
 out=produce();open(sys.argv[1],'w').write(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sources':len(out['sources']),'protected':sum(s['protected'] for s in out['sources']),'admitted':sum(s['admitted'] for s in out['sources']),'fibers1':len(out['fibers1']),'mixed1':sum(f['mixed'] for f in out['fibers1']),'fibers2':len(out['fibers2']),'mixed2':sum(f['mixed'] for f in out['fibers2'])}))
