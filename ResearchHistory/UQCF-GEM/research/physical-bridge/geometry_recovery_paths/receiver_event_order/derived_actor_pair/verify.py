"""Independent reconstruction from the pinned table's equations and two leaf columns."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json,sys

I=range(25);A=0;B=12;MU=1984
def move(i,a,b):
    return ((i%5+a)%5)+5*((i//5+b)%5)
N={i:{move(i,*o) for o in ((1,0),(-1,0),(0,1),(0,-1))} for i in I}
def opposite(i,j):return j in {move(i,*o) for o in ((2,0),(-2,0),(0,2),(0,-2))}
L=N[A];H=N[B]
def direct(i,j):
    if i==j:return 0
    if {i,j}=={A,B}:return MU+14
    for x,y in ((i,j),(j,i)):
        if x in (A,B):
            bias=0 if y in L|H else 20 if opposite(A,y) or opposite(B,y) else 8
            return MU+bias+(4 if (x==A)==(y in H) else 0)
    if j in N[i]:return MU
    if not opposite(i,j):return MU+8
    center,=N[i]&N[j]
    cr=N[center]-{i,j}
    m=cr&{A,B}
    return MU+20 if not m else direct(*sorted(cr))
w0=[[direct(i,j) for j in I] for i in I]
def norms(i,j):return (set(w0[i][x]-MU for x in N[j]),set(w0[j][x]-MU for x in N[i]))
far=[(i,j) for i,j in combinations(I,2) if i not in N[j] and not N[i]&N[j]]
const=[[i,j,next(iter(u)),next(iter(v))] for i,j in far for u,v in [norms(i,j)] if len(u)==len(v)==1]
assert len(far)==150 and Counter(tuple(r[-2:]) for r in const)=={(4,4):1,(8,8):27}
assert [c[:2] for c in const if c[-2:]==[4,4]]==[[A,B]]
firsts={A:[(A,1,-1),(A,2,1)],B:[(B,1,1),(B,2,-1)]}
S={1:set(I)-{B}-H,2:{B}|H}
def enc(w):return sha256(json.dumps(w,separators=(',',':')).encode()).hexdigest()
def matrix(s):
    return [[w0[i][j]+4*sum(int((i in z)!=(j in z))-int((i in S[a])!=(j in S[a]))
                           for a,z in s.items()) for j in I] for i in I]
def transition(s,e):
    i,a,v=e; out={k:set(z) for k,z in s.items()}
    assert (i in out[a])==(v<0)
    out[a]^={i}; assert all(out.values())
    return out
def audit(result):
    assert result['initial']==w0 and result['mu']==MU
    assert result['far']==len(far) and result['constant_pair_defects']==const
    traces={(tuple(a),tuple(b)):d for a,b,d in result['traces']}
    assert len(traces)==8
    assert {tuple(x) for x in result['null']}=={e for z in firsts.values() for e in z}
    seen=set()
    for first,rows in result['outcomes']:
        i,a,v=first; j=(B if i==A else A); first=tuple(first)
        assert first in firsts[i] and {tuple(r[0]) for r in rows}==set(firsts[j])
        shared=transition(S,first); mid=matrix(shared)
        for step,pre,middle,after,field in rows:
            step=tuple(step); seen.add((first,step))
            last=transition(shared,step); end=matrix(last)
            expected=[enc(k) for k in (w0,mid,end)]
            assert traces[first,step]==expected
            other=lambda r:(r[0],3-r[1],-r[2])
            assert traces[other(first),other(step)]==expected
            root=241 if j==A else 242
            assert pre==middle==[str(root),'2' if j in S[a] else 'absent']
            assert after==[str(root-2*step[-1]),'2' if j in last[a] else 'absent']
            assert field=='0'
    assert seen==set(traces)
    assert result['directions_match_full_work']==['same_sign','transfer']
    assert result['type_matrix_diffs']==[[A,B,1998,1990]]
raw=Path(sys.argv[1]).read_bytes()
value=json.loads(raw);audit(value)
for field,bad in [('constant_pair_defects',const[:1]),('traces',value['traces'][:-1]),('type_matrix_diffs',[])]:
    try:audit(dict(value,**{field:bad}))
    except AssertionError:pass
    else:raise AssertionError('falsified evidence admitted')
print(json.dumps({'raw_sha256':sha256(raw).hexdigest(),'actor_candidates':[[0,12]],'ordered_histories':8,'exact_trace_alias_pairs':4,'rejecting_controls':3},sort_keys=True))
