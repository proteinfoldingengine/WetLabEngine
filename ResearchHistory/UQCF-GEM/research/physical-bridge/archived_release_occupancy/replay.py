from hashlib import sha1, sha256
from itertools import combinations, groupby
from pathlib import Path
import json, sys

directory=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
hashes={
    'mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f',
    'model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8',
    'verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43'
}
for name,expected in hashes.items():
    b=(directory/name).read_bytes()
    assert sha1(f'blob {len(b)}'.encode()+b'\0'+b).hexdigest()==expected
sys.path.insert(0,str(directory))
from mechanisms import produce, degree_two
from verifier import verify_record

def hit(s):
    labels=set().union(*map(set,s))
    return next(k for k in range(1,len(labels)+1)
                if any(all(set(x)&set(r) for r in s) for x in combinations(labels,k)))

def gain(s,i,x):
    return [sorted(set(r)|({x} if j==i else set())) for j,r in enumerate(s)]

def pick(s,pending):
    return sorted(e for e in pending if sum(e[1] in r for r in s)<2)

P=[(0,1,0),(1,0,1)]
input_hashes=['fbc68485582106d77d16ba486cec953ca0775c19b775e1900b8866fc1890330f',
              '9bd064d7279a4a4278c05bd7f5f963f28fbeb7b45d2789344cc092d0d3288dc6']
paths=[]
for i,h in enumerate(input_hashes):
    b=(packet/f'rows-{i}.json').read_bytes()
    assert sha256(b).hexdigest()==h
    rec=json.loads(b); c={'identity':rec['identity']}; reads=[]
    def trace(frame,event,arg):
        if frame.f_code is not degree_two.__code__:
            return None
        if event=='line' and frame.f_lineno==50:
            loc=frame.f_locals
            reads.append({'rows':[sorted(r) for r in loc['route'].last],
                          'pending':list(loc['pending']),'picked':loc['free']})
        return trace
    sys.settrace(trace)
    try:
        actual=produce(c)
    finally:
        sys.settrace(None)
    assert actual==rec and not verify_record(c,rec)
    path=rec['path']
    assert path[:2]==[[[0],[1],[0,1]],[[0],[1],[0,1,2]]]
    assert [hit(s) for s in path]==[2]*7
    assert [hit(gain(path[1],j,x)) for _,x,j in P]==[1,1]
    assert [hit(gain(path[2],j,x)) for _,x,j in P]==([2,1] if i==0 else [1,2])
    assert reads[0]['pending']==P+([(1,2,2)] if i==0 else [(0,2,2)])
    assert len(reads)==3 and reads[1]=={'rows':path[2],'pending':P,'picked':P[i]}
    assert pick(path[1],P)==[] and pick(path[2],P)==[P[i]]
    assert path[3]==gain(path[2],P[i][2],P[i][1])
    assert path[2][:2]==path[0][:2] and path[3][0]==([0,1] if i==0 else [0])
    # Not all exact legal gains are on the scheduler's pending list.
    assert hit(gain(path[2],2,1-i))==2 # undo is allowed in the top-level q=2 constraint
    paths.append(dict(index=i,guard_reads=reads,path=path))
assert [[list(k) for k,g in groupby(s[0] for s in d['path'])] for d in paths]==[[[0],[0,1],[1]]]*2
assert [[list(k) for k,g in groupby(s[1] for s in d['path'])] for d in paths]==[[[1],[0,1],[0]]]*2
print(json.dumps(paths,sort_keys=True,separators=(',',':')))
