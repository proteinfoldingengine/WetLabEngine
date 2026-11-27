from itertools import permutations
from copy import deepcopy
from hashlib import sha1
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(".").resolve()))
from mechanisms import produce
from verifier import verify_record
blobs={'mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f','model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8','verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43'}
for f,s in blobs.items():
 b=Path(f).read_bytes()
 assert s==sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
rows=[[j for j in range(12) if m>>j&1] for m in [3414,681,681,682,356,3536,651,555]]
p={'kind':'clone_sequence','k':12,'q':2,'a':[2,2,3,1,1,1,3,1]}
def run(rows,ops):
 c={'identity':['M4',p,rows,{'operations':[list(o) for o in ops]}]}
 r=produce(c)
 if r['status']!='PASS' or set(r['tau'])!={2}:return None
 assert not verify_record(c,r)
 return r
after=[run(rows,[(1,i)])['path'][-1] for i in (5,7)]
usage=[]
for frame in (rows,*after):
 saw={}
 for pair in permutations(range(12),2):
  r=run(frame,[pair])
  if r is None:continue
  assert r['facts']['preliminary_path']==r['path']
  info=r['facts']['clones'][0]
  widths=[len(q) for q in info['demands']]
  floors=[p['a'][i] for i in info['slots']]
  saw[pair]=([i for i,(a,b) in enumerate(zip(frame,r['path'][-1])) if a!=b],
     all(a<b for a,b in zip(widths,widths[1:])) and all(a<b for a,b in zip(floors,floors[1:])))
 usage.append(saw)
assert [len(u) for u in usage]==[72,69,69]
assert [sorted(set(usage[0])-set(x)) for x in usage[1:]]==[[(4,2),(10,2),(11,2)],[(2,4),(2,10),(2,11)]]
assert all(set(x)<=set(usage[0]) for x in usage[1:])
only=[{p for p,(rw,strict) in u.items() if strict and rw in ([1],[2])} for u in usage]
assert only[1]&only[2]=={(0,1)}
print(json.dumps({'before_and_after_counts':[len(u) for u in usage],
 'removed':[sorted(set(usage[0])-set(x)) for x in usage[1:]],
 'strict_lone_peer_operations':[sorted(x) for x in only]},indent=2))
