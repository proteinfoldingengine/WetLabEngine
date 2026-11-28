"""Run with the pinned v16.53-four-child-boundary directory as the sole argument."""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import producer as p
import verifier as v

labels = {-1: {0}, 0: {0, 1}, 1: {1}}
def encode(state):
    return v.raw_roots(2, [labels[x] for x in state])

def cell_vertices(cell):
    return frozenset(product(*cell))

def boundary(corners):
    return {frozenset((a,b)) for a,b in combinations(corners,2)
            if sum(abs(x-y) for x,y in zip(a,b))==1}

def main():
    n=4
    roots = p.layout(p.Q)[0]
    states = set()
    relaxed = set()
    for state in product(labels, repeat=n):
        raw = encode(state)
        profile = v.profile_check(v.Q,2,raw)
        assert profile == [p.coordinate(raw,roots)]
        assert (profile==[2]) == (-1 in state and 1 in state)
        if profile==[2]: states.add(state)
        if abs(profile[0]-2)<=1: relaxed.add(state)
    assert len(relaxed)==81
    intervals=[(-1,), (0,), (1,), (-1,0), (0,1)]
    cells=defaultdict(set)
    for cell in product(intervals,repeat=n):
        corners=cell_vertices(cell)
        if corners<=states: cells[sum(len(x)-1 for x in cell)].add(corners)
    assert [len(cells[i]) for i in range(5)]==[50,96,48,0,0]
    incident=Counter()
    caps=[Counter(),Counter()]
    for square in cells[2]:
        edges=boundary(square)
        assert len(edges)==4
        incident.update(edges)
        sides={s[-1] for s in square}
        assert sides!={0}
        caps[int(min(sides)>=0)].update(edges)
        # Verify both exact two-move paths across both diagonals.
        for a,c in combinations(square,2):
            if frozenset((a,c)) in edges:continue
            for b in square-{a,c}:
                path=list(map(encode,(a,b,c)))
                assert v.path_check(v.Q,2,[2],path,path[0],path[-1])==0
    assert set(incident)==cells[1] and set(incident.values())=={2}
    valences=Counter()
    for state in states:
        link=defaultdict(set)
        edges={e for e in cells[1] if state in e}
        for face in cells[2]:
            if state in face:
                e,f=edges&boundary(face)
                link[e].add(f);link[f].add(e)
        assert set(link)==edges and all(len(n)==2 for n in link.values())
        todo=[next(iter(edges))]; seen=set()
        while todo:
            e=todo.pop()
            if e not in seen:
                seen.add(e);todo.extend(link[e]-seen)
        assert seen==edges
        valences[len(edges)]+=1
        assert (len(edges)==3)==(len(set(state))==2 and sorted(state.count(a) for a in (-1,1))==[1,3])
    assert valences=={3:8,4:42}
    print('valences',valences)
    equator={e for e in cells[1] if all(x[-1]==0 for x in e)}
    for cap in caps:
        assert sum(cap.values())==24*4
        assert {e for e,val in cap.items() if val==1}==equator
    assert len(equator)==12
    print('vertices, edges, faces; equator; cap faces',50,96,48,12,24)
    for k in (1,2,3):
        seen_counts=set()
        forced=Counter()
        for observed in combinations(range(n),k):
            groups=defaultdict(list)
            for s in states:groups[tuple(s[j] for j in observed)].append(s)
            seen_counts.add(len(groups))
            hidden=set(range(n))-set(observed)
            for seen,compatible in groups.items():
                missing=len({-1,1}-set(seen))
                for r in hidden:
                    all_single=all(s[r]!=0 for s in compatible)
                    assert all_single==(missing==len(hidden))
                    forced[all_single]+=1
        print('charts, distinct projected states per subset, forced singleton tests',k,seen_counts,forced)
    # Reproduce only the relevant campaign R-family normalizations.
    admissible_paths=0; visited_edges=set()
    for s in states:
        start=encode(s)
        path=p.normalize(start,p.Q,2,[2])
        assert v.path_check(v.Q,2,[2],path,start,v.model(v.Q,[2],2)[2])<=1
        proj=[tuple(next(x for x,S in labels.items() if S=={j for j,z in enumerate(raw) if z>>u&1}) for u in roots) for raw in path]
        if all(t in states for t in proj):admissible_paths+=1
        visited_edges.update(frozenset((a,b)) for a,b in zip(proj,proj[1:]) if a in states and b in states)
    print('campaign starts, fully exact paths, distinct exact edges used',len(states),admissible_paths,len(visited_edges))
if __name__=='__main__':main()
