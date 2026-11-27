from hashlib import sha1, sha256
from itertools import combinations, groupby
from collections import deque
from pathlib import Path
import json,sys
base=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
sources={'mechanisms.py':'ab3541cba29d5e1ebd4fe6c56128daf020c1a81f',
         'model.py':'a4a6407990c36084ab3b6e8e7da9022a4f9d63a8',
         'verifier.py':'e19999dfd46cd134d8191a59da7b8bf2cdb74b43'}
for name,h in sources.items():
    b=(base/name).read_bytes()
    assert sha1(f'blob {len(b)}'.encode()+b'\0'+b).hexdigest()==h
sys.path.insert(0,str(base))
from mechanisms import produce,degree_two
from verifier import verify_record

def hit(rows):
    return next(k for k in (1,2,3)
        if any(all(set(xs)&set(row) for row in rows) for xs in combinations(range(4),k)))

def enumerate_peer_completions(start,end):
    def pack(rows):return tuple(frozenset(row) for row in rows)
    start,end=pack(start),pack(end)
    q=deque([start]);dist={start:0};paths={start:1}
    while q:
        state=q.popleft()
        for i in (0,1):
            for lab in range(4):
                n=state[:i]+(state[i]^{lab},)+state[i+1:]
                if not n[i] or hit(n)!=2:continue
                v=dist[state]+1
                if n not in dist:
                    dist[n]=v;paths[n]=paths[state];q.append(n)
                elif dist[n]==v:
                    paths[n]+=paths[state]
    return dist[end],paths[end]

hashes=['c650cf16f88fe11169717ae520c09c2e45e56ac50aef0cbc54f87e1098aa9b87',
        'd7dd9422cd7c30d4cc288cfe6388a6d57ffbe0e8b17b2edc3a8a0747b4cb010b']
out=[]
P=[(0,1,0),(1,0,1)]
for i,h in enumerate(hashes):
    b=(packet/f'buffer-rows-{i}.json').read_bytes()
    assert sha256(b).hexdigest()==h
    rec=json.loads(b);case={'identity':rec['identity']};reads=[]
    def trace(frame,event,arg):
        if frame.f_code is not degree_two.__code__:return None
        if event=='line' and frame.f_lineno==50:
            loc=frame.f_locals;s=loc['route'].last
            reads.append({'rows':[sorted(r) for r in s],
                'pending':list(loc['pending']),'picked':loc['free']})
        return trace
    sys.settrace(trace)
    try:actual=produce(case)
    finally:sys.settrace(None)
    assert actual==rec and not verify_record(case,rec)
    p=rec['path']
    assert p[:2]==[[[0],[1],[0,1,2]],[[0],[1],[0,1,2,3]]]
    assert p[2]==([[0],[1],[0,1,3]] if i==0 else [[0],[1],[0,2,3]])
    assert reads[0]['pending']==P+([(2,3,2)] if i==0 else [(1,3,2)])
    assert reads[1]=={'rows':p[2],'pending':P,'picked':None if i==0 else P[0]}
    assert all(hit(s)==2 for s in p)
    local=[list(s) for s,g in groupby(f[0] for f in p)]
    sizes=[len(s) for s in local]
    assert sizes==([1,2,1,2,1] if i==0 else [1,2,1])
    assert p[0][0]==[0] and p[-1][0]==[1]
    bound,num=enumerate_peer_completions(p[2],p[-1])
    assert bound==(6 if i==0 else 4)
    if i==0:
        # Peer swap together with old-label rename preserves both endpoints and can move the buffer write to the other peer.
        mirrored=[[sorted(1-x if x<2 else x for x in row)
                   for row in (frame[1],frame[0],frame[2])] for frame in p[2:]]
        assert mirrored[0]==p[2] and mirrored[-1]==p[-1] and all(hit(s)==2 for s in mirrored)
        assert [len(s) for s,g in groupby(f[0] for f in mirrored)]==[1,2,1]
    out.append(dict(guard_reads=reads,local=local,size_word=sizes,path=p,
                    frozen_source_minimum=bound,exact_shortest_paths=num))
print(json.dumps(out,sort_keys=True,separators=(',',':')))
