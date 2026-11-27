"""Exhaust the two-label states of the original v16.53 template C."""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import producer
import verifier

A, B, D = 1, 2, 3
tree = producer.TREES['C']
target = [2, 2]
def raw(rows):
    return [1 + sum(1 << i for i, mask in enumerate(rows, 1) if mask & bit)
            for bit in (A, B)]

def distances(start, allowed):
    paths = {start: (start,)}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for t in neighbors[s]:
            if t in allowed and t not in paths:
                paths[t] = paths[s] + (t,)
                queue.append(t)
    return paths

profiles = {}
for s in product((A, B, D), repeat=6):
    try: profiles[s] = tuple(verifier.profile_check(tree,2,raw(s)))
    except verifier.InterfaceNotPreserved: pass
neighbors = {}
for s in profiles:
    neighbors[s] = [t for i,mask in enumerate(s) for bit in (A, B)
                    if (t := s[:i] + (mask ^ bit,) + s[i+1:]) in profiles]
exact = {s for s,q in profiles.items() if q==(2,2)}
starts = [s for s in exact if D in s[3:]]
assert len(exact)==24 and len(starts)==12
assert all(s[0]==D and {s[1],s[2]}=={A,B} for s in exact)
assert all(len(set(neighbors[s]) & exact)==2 for s in exact)
assert len(distances(min(exact),exact))==12
counts = Counter()
for start in sorted(starts):
    helper = start.index(D,3)
    active = [i for i in range(3,6) if i!=helper]
    end = tuple((D^x) if i in active else x for i,x in enumerate(start))
    first = set(neighbors[start]) & exact
    assert {s[helper] for s in first}=={A,B}
    for s in first:
        assert s[:helper]+s[helper+1:]==start[:helper]+start[helper+1:]
        t, = (set(neighbors[s]) & exact)-{start}
        peer, = [i for i in active if start[i]==s[helper]]
        assert t==s[:peer]+(D,)+s[peer+1:]
    for name,condition,freeze in [
        ('exact',lambda q:q==(2,2),False),
        ('exact, helper held',lambda q:q==(2,2),True),
        ('outer exact, inner may deviate, helper held',lambda q:q[0]==2,True),
        ('inner exact, outer may deviate, helper held',lambda q:q[1]==2,True),
    ]:
        allowed={s for s,q in profiles.items() if condition(q) and (not freeze or s[helper]==D)}
        path=distances(start,allowed).get(end)
        cost=None if path is None else len(path)-1
        counts[name,cost]+=1
        if path:
            encoded=list(map(raw,path))
            assert verifier.path_check(tree,2,target,encoded,encoded[0],encoded[-1])==(0 if name=='exact' else 1)
print('exact vertices, components, candidate priors:',len(exact),2,len(starts))
print('swap distance per control:', sorted(counts.items()))
def decode(state):
    return tuple(sum(b for b,z in zip((A,B),state) if z & 1<<i) for i in range(1,7))
for perm in ('identity','reversal','cyclic'):
    for mode in ('compact','inflated'):
        s=producer.initial(tree,2,target,perm,mode)
        path=producer.normalize(s,tree,2,target)
        ps=[tuple(verifier.profile_check(tree,2,t)) for t in path]
        assert verifier.path_check(tree,2,target,path,s,verifier.model(tree,target,2)[2])==1
        print(perm,mode,'prior',decode(s),'first edit profile',ps[1],'profiles',sorted(set(ps)))
