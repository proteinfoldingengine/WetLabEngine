import hashlib
from itertools import groupby
import json
from pathlib import Path
import sys
def sha(b):return hashlib.sha256(b).hexdigest()
here=Path(__file__).resolve().parent
demo=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(demo))
from mechanisms import produce
from verifier import verify_record
def record(path,sha256):
    data=path.read_bytes()
    assert sha(data.rstrip(b'\n')+b'\n')==sha256
    return json.loads(data)
a=record(here.parent/'buffer-rows-0.json','c650cf16f88fe11169717ae520c09c2e45e56ac50aef0cbc54f87e1098aa9b87')
f=record(here/'root-residue-fresh-original.json','15dc722c8666598a00ed051e3165bdca85d6ffaf28ee36ad28d97db6cbc32693')
m=record(here/'root-residue-mirror-original.json','f1b5ebc5f66debcd9693b0694f7fc6fe48fcc381ebc84600eb7e6a4a852681ac')
for r in (a,f,m):
    case={'identity':r['identity']}
    assert produce(case)==r
    assert not verify_record(case,r)
def word(x):return [n for n,_ in groupby(len(row[0]) for row in x['path'])]
def swap(rows):return [sorted(5-i if i in (2,3) else i for i in r) for r in rows]
assert a['identity'][1]==f['identity'][1]==m['identity'][1]
assert a['identity'][3]==f['identity'][3]
assert f['path']==a['path'][2:]
assert all(2 not in row for row in f['path'][0])
assert len(f['events'])==1 and f['events'][0]==dict(a['events'][1],start=0,end=6)
assert all(rows[2]==f['path'][0][2] for rows in f['path'])
assert m['identity'][2]==swap(a['identity'][2])
assert m['identity'][3]['target']==swap(a['identity'][3]['target'])
assert m['path'][:3]==list(map(swap,a['path'][:3]))
assert [(r['events'][0]['source'],r['events'][0]['target']) for r in (a,m)]==[(2,3),(3,2)]
assert [r['events'][1]['buffer'] for r in (a,m)]==[2,2]
assert all(2 in row[2] for row in m['path'][2:]) and all(3 not in r for r in m['path'][2])
assert all(word(r)==[1,2,1,2,1] for r in (a,m,f))
print(json.dumps(dict(fresh_exact_suffix=True,original=1914516,mirror=1914567,fresh=1914568,size_word=word(f)),sort_keys=True))
