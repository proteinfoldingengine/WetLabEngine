"""One-time and per-edit restart controls on original v16.51 release/gain records."""
from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
import gzip
import hashlib
import json
import sys

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import producer
import verifier


def distance(s, t):
    return sum((x ^ y).bit_count() for x, y in zip(s, t))


def edit(s, t):
    assert distance(s, t) == 1
    j = next(i for i in range(len(s)) if s[i] != t[i])
    u = (s[j] ^ t[j]).bit_length() - 1
    return j, u, bool(t[j] & (1 << u))


def fresh(state, tree, q):
    old = state.copy()
    path = producer.normalize(state, tree, 2, q, trace=[])
    assert state == old and path[0] == state
    return path


def repeatedly_restart(state, tree, q):
    visits = {}
    while tuple(state) not in visits:
        visits[tuple(state)] = len(visits)
        path = fresh(state, tree, q)
        if len(path) == 1:
            return len(visits), ()
        state = path[1]
    onset = visits[tuple(state)]
    return onset, tuple(list(visits)[onset:])


def check_target_controls(mid, end, tree, q):
    nodes = producer.layout(tree)
    roots = nodes[0]
    for s in (mid, end):
        assert all(sum(bool(z & (1 << r)) for z in s) == 1 for r in roots)
    differing = [r for r in roots if any((x ^ y) & (1 << r) for x, y in zip(mid, end))]
    peaks = []
    for ordering in permutations(differing):
        s = mid.copy()
        path = [s.copy()]
        for root in ordering:
            old = next(j for j,z in enumerate(s) if z & (1 << root))
            sites = producer.vertices(nodes, root)
            for u in sites:
                s[1-old] |= 1 << u
                path.append(s.copy())
            for u in reversed(sites):
                s[old] &= ~(1 << u)
                path.append(s.copy())
        assert s == end and len(path)-1 == distance(mid,end)
        peaks.append(verifier.path_check(tree,2,q,path,mid,end)[0])
    return peaks


def main():
    doc = producer.produce()
    raw = (json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
    packet = gzip.compress(raw,compresslevel=9,mtime=0)
    packet = packet[:9] + bytes([3]) + packet[10:]
    assert hashlib.sha1(f'blob {len(packet)}\0'.encode()+packet).hexdigest()=='571d38f08006b7023a65ec64cac77fe23e0db52a'

    census = Counter()
    successors = defaultdict(set)
    unique = {}
    for case,row in enumerate(doc['cases']):
        spec = row['spec']
        q = spec['q']
        if row['failure'] or spec['k'] != 2 or q[0] != 2:
            continue
        census['qualified cases'] += 1
        tree = producer.TREES[spec['tree']]
        roots = producer.layout(tree)[0]
        path = row['path']
        for frame,state in enumerate(path):
            key = spec['tree'],tuple(q),tuple(state)
            successors[key].add(tuple(path[frame+1]) if frame+1<len(path) else ())
        for i,(pre,mid,gain) in enumerate(zip(path,path[1:],path[2:])):
            x,source,added = edit(pre,mid)
            y,peer,taken = edit(mid,gain)
            if added or not taken or x!=y or source==peer or not {source,peer}<=set(roots):
                continue
            if any(verifier.profile_check(tree,2,s)!=q for s in (pre,mid,gain)):
                continue
            early=pre.copy()
            early[y] |= 1 << peer
            if verifier.profile_check(tree,2,early)[0]!=1:
                continue
            census['matched occurrences'] += 1
            post = fresh(mid,tree,q)
            assert post == path[i+1:]
            assert fresh(pre,tree,q)[1] != mid
            target = verifier.model(tree,q,2)[2]
            assert verifier.path_check(tree,2,q,post,mid,target)==[0,0,0]
            assert len(post)-1 == distance(mid,target)
            assert distance(pre,target) == distance(mid,target)+1
            # Recover all legal exact first moves, allowing any non-root vertex.
            alternatives=[]
            for label in range(2):
                for site in range(1,len(producer.layout(tree))):
                    t = mid.copy()
                    t[label] ^= 1<<site
                    try:
                        if verifier.profile_check(tree,2,t)==q:
                            alternatives.append(t)
                    except verifier.InterfaceNotPreserved:
                        pass
            assert sorted(alternatives)==sorted([pre,gain])
            # Undoing the release first costs exactly two extra edits to target.
            detour = [mid,pre]+post
            assert verifier.path_check(tree,2,q,detour,mid,target)==[0,0,0]
            assert len(detour)-1==2+distance(mid,target)
            onset,cycle=repeatedly_restart(mid,tree,q)
            assert len(cycle)==2 and target not in [list(s) for s in cycle]
            unique[(spec['tree'],tuple(mid))]=(len(post)-1,onset,cycle,check_target_controls(mid,target,tree,q))
    print('census',dict(census),'different retained input keys',len(successors))
    print('archived successor multiplicities including stop',sorted(Counter(map(len,successors.values())).items()))
    for k,val in sorted(unique.items()):print(k,val)
    row=doc['cases'][13]
    path=row['path']
    assert path[0]==path[6]==[911,127] and path[1]==[907,127] and path[7]==[911,119]
    assert all(verifier.profile_check(producer.TREES['T'],2,s)==row['spec']['q'] for s in path)
    print('case 13 equal-input next commands (label,site,add)',edit(path[0],path[1]),edit(path[6],path[7]))


if __name__=='__main__':
    main()
