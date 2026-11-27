"""Original M4 automatic clip: exact position of the extra receiver edits."""
from hashlib import sha1
from pathlib import Path
from copy import deepcopy
from itertools import groupby
import json,sys
sys.path.insert(0,str(Path(".").resolve()))
from mechanisms import produce
from verifier import verify_record,covering_number
from model import cover,state
blobs={'mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f','model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8','verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43'}
for n,digest in blobs.items():
    b=Path(n).read_bytes()
    assert sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==digest
p={'kind':'clone_sequence','k':6,'a':[1,2,1,1,1,1],'q':2}
base=[[0,2],[0,2],[1,3],[1,4,5],[2,3],[2,4]]
other=deepcopy(base);other[1].append(4)
docs=[]
for rows,command in ((base,[0,1]),(other,[0,1]),(base,[0,3])):
    c={'identity':['M4',p,rows,{'operations':[command]}]}
    r=produce(c);assert r['status']=='PASS' and not verify_record(c,r)
    raw=r['facts']['preliminary_path'];out=r['path']
    assert all(covering_number(x)==2 for x in out)
    def word(i,path):return [x for x,_ in groupby(row[i] for row in path)]
    def events(path):
        ds=[]
        for a,b in zip(path,path[1:]):
            changes=[(i,x,x in b[i]) for i in range(len(a)) for x in set(a[i])^set(b[i])]
            assert len(changes)==1
            ds.extend(changes)
        return ds
    assert all(word(i,raw)==[base[i]] and out[-1][i]==base[i] for i in (2,3))
    ds=events(out);raw_cover=[covering_number(x) for x in raw]
    docs.append({'command':command,'raw_cover':raw_cover,'raw_covers':[cover(state(x)) for x in raw],
        'layers':r['facts']['layers'],'output_events':ds,'raw_events':events(raw),
        'result_writes':{i:word(i,out) for i in (0,1,2,3)},'source_cut_index':ds.index((0,2,False))})
assert docs[0]['raw_cover']==[2,2,3,2,2,2]
assert docs[0]['raw_covers'][2]==(0,1,2)
assert docs[0]['output_events'][:4]==[(0,3,True),(2,0,True),(3,0,True),(0,2,False)]
assert docs[0]['result_writes'][2]==[[1,3],[0,1,3],[1,3]]
assert docs[0]['result_writes'][3]==[[1,4,5],[0,1,4,5],[1,4,5]]
assert all(d['layers']==[] and d['result_writes'][2]==[[1,3]] and d['result_writes'][3]==[[1,4,5]] for d in docs[1:])
assert docs[0]['raw_events'][:2]==docs[1]['raw_events'][:2]
print(json.dumps(docs,indent=2))
