"""Exact one-leaf inference, source-order ambiguity and a held-exterior control."""
from collections import deque
from itertools import groupby
from pathlib import Path
import gzip
import hashlib
import json
import sys

sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import producer as p
import verifier as v

def mask(state, site):
    return sum((1<<j) for j,bits in enumerate(state) if bits & (1<<site))

def exact_graph(tree, target, start):
    n=len(p.layout(tree))
    todo=deque([start]); dist={start:0}; graph={}
    while todo:
        state=todo.popleft()
        edges=[]
        for j in range(2):
            for u in range(1,n):
                t=list(state)
                t[j]^=1<<u
                try:
                    profile=v.profile_check(tree,2,t)
                except v.InterfaceNotPreserved:
                    continue
                if profile!=target: continue
                t=tuple(t);edges.append(t)
                if t not in dist:
                    dist[t]=dist[state]+1;todo.append(t)
        graph[state]=edges
    return graph,dist

def partition(graph, states):
    pending=set(states); groups=[]
    while pending:
        seed=pending.pop(); stack=[seed]; group={seed}
        while stack:
            for t in graph[stack.pop()]:
                if t in pending:
                    pending.remove(t); stack.append(t); group.add(t)
        groups.append(group)
    return groups

def local_word(path,u):
    return tuple(x for x,_ in groupby(mask(s,u) for s in path))

def test_case(doc,case):
    row=doc['cases'][case]
    spec=row['spec'];tree=p.TREES[spec['tree']];q=spec['q']
    nodes=p.layout(tree); left,middle,right=nodes[0]
    regions=[p.vertices(nodes,r) for r in nodes[0]]
    start=tuple(row['start'])
    assert all(mask(start,i)==j for region,j in zip(regions,(2,1,2)) for i in region)
    graph,dist=exact_graph(tree,q,start)
    exterior=regions[0]+regions[2]
    parents={w:i for i,cs in enumerate(nodes) for w in cs}
    perm=[0]+regions[2]+regions[1]+regions[0]
    def remap(s,mapping):
        return [sum(((z>>u)&1)<<j for j,u in enumerate(mapping)) for z in s]
    alt=p.normalize(remap(start,perm),tree[::-1],2,q)
    alt=[remap(s,[perm.index(i) for i in range(len(perm))]) for s in alt]
    actual=row['path']
    for path in (actual,alt):
        assert v.path_check(tree,2,q,path,list(start),actual[-1])==[0,0,0]
    print('case',case,'reachable states and undirected edges',len(graph),sum(map(len,graph.values()))//2)
    for leaf in regions[1]:
        if nodes[leaf]:continue
        chain=[leaf]
        while chain[-1]!=middle:chain.append(parents[chain[-1]])
        with_b={s for s in graph if mask(s,leaf)&2}
        with_both={s for s in with_b if mask(s,leaf)==3}
        def ext(s):
            return tuple(mask(s,i) for i in exterior)
        for s in with_b:
            # The existing B-indexed row itself identifies exactly the all-A exterior branches.
            absent_b = {r for r in (left,right) if not s[1] & (1<<r)}
            assert absent_b == {reg[0] for reg in (regions[0],regions[2])
                                if all(mask(s,i)==1 for i in reg)}
            assert absent_b
            assert all(mask(s,i)==1 for i in regions[0]) or all(mask(s,i)==1 for i in regions[2])
        dual=partition(graph,with_both)
        assert len(dual)==2
        for group in dual:
            assert len({ext(s) for s in group})==1
            assert {tuple(mask(s,r) for r in (left,right)) for s in group} in ({(1,2)},{(2,1)})
        for s in with_both:
            for t in graph[s]:
                assert ext(t)==ext(s)
        # B as a singleton still certifies an all-A exterior subtree, but its identity can switch.
        with_b_only={s for s in with_b if mask(s,leaf)==2}
        singleton_groups=partition(graph,with_b_only)
        assert any({(1,2),(2,1)} <= {tuple(mask(s,r) for r in (left,right)) for s in g}
                   for g in singleton_groups)
        assert local_word(actual,leaf)==local_word(alt,leaf)==(1,3,2)
        original=next(i for i,s in enumerate(actual) if mask(s,leaf)==3)
        alternative=next(i for i,s in enumerate(alt) if mask(s,leaf)==3)
        assert (mask(actual[original],left),mask(alt[alternative],right))==(1,1)
        for path,k,side in ((actual,original,left),(alt,alternative,right)):
            # The branch address was already present in the B-indexed row before the leaf gained B.
            for index in (k-1,k):
                assert [r for r in (left,right) if not path[index][1] & (1<<r)] == [side]
            assert path[k-1][0]==path[k][0]
            assert path[k-1][1]^(1<<leaf)==path[k][1]
        lengths=tuple(2*len(reg)+len(chain) for reg in (regions[0],regions[2]))
        dmins=tuple(min(dist[s] for s in with_both if mask(s,r)==1) for r in (left,right))
        assert lengths==dmins
        # Return to the same global prior in both controls, with no clock in the local readout.
        prefix=actual[:original+1]
        closed_exact=prefix+prefix[-2::-1]
        relaxed=[list(start)]
        for u in reversed(chain):
            s=relaxed[-1].copy();s[1]|=1<<u;relaxed.append(s)
        closed_relaxed=relaxed+relaxed[-2::-1]
        assert all(ext(s)==ext(start) for s in closed_relaxed)
        assert local_word(closed_exact,leaf)==local_word(closed_relaxed,leaf)==(1,3,1)
        assert v.path_check(tree,2,q,closed_exact,list(start),list(start))==[0,0,0]
        assert v.path_check(tree,2,q,closed_relaxed,list(start),list(start))==[1,1,1]
        print('leaf',leaf,'B-present',len(with_b),'dual components',sorted(map(len,dual)),
              'min edits (left/right converted)',lengths,'original/reordered first dual frames',original,alternative)

def main():
    doc=p.produce()
    raw=(json.dumps(doc,sort_keys=True,separators=(',',':'))+'\n').encode()
    packet=gzip.compress(raw,compresslevel=9,mtime=0)
    packet=packet[:9]+bytes([3])+packet[10:]
    assert hashlib.sha1(f'blob {len(packet)}\0'.encode()+packet).hexdigest()=='571d38f08006b7023a65ec64cac77fe23e0db52a'
    for case in (14,302):test_case(doc,case)

if __name__=='__main__':main()
