"""Traverse actual v16.26 withdrawals after each of the previously matched source choices."""
import hashlib
import importlib.util
import itertools
import json
import lzma
import sys
from collections import Counter
from functools import cache
from pathlib import Path

STAGE = "v16.26-consistency-increment-law"


def pin(path, expected):
    raw = path.read_bytes()
    actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if actual != expected:
        raise ValueError(f"Unexpected historical file: {path}")
    return raw


def module(path, expected):
    pin(path, expected)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def view(mask):
    return tuple(i for i in range(mask.bit_length()) if mask >> i & 1)


def bits(rows):
    return tuple(sum(1 << v for v in row) for row in rows)


def graph(start, moves):
    stack = [start]
    edges = {}
    while stack:
        s = stack.pop()
        if s in edges:
            continue
        edges[s] = moves(s)
        stack.extend(t for _, _, t in edges[s])
    return edges


def packed_graph(edges):
    states = sorted(edges)
    index = {s: k for k, s in enumerate(states)}
    return {"states": states, "moves": [[(i,v,index[t]) for i,v,t in edges[s]] for s in states]}


def project(s, group):
    return tuple(s[i] for i in group)


def raw_bytes(x):
    return (json.dumps(x, separators=(",",":"), sort_keys=True) + "\n").encode()


def run(demos, prior, out):
    native = module(demos / STAGE / "engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    checker = module(demos / STAGE / "verify.py", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    p1 = module(demos / "v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    cases = json.loads(pin(prior / "native.json", "9c80bb24a39c21bb96a2404724df5f1a59a8af46"))["triangle_pairs_complete"]

    @cache
    def push(p, mask):
        return tuple(map(int, p1.push(p, tuple(range(len(p))), view(mask), (1,) * len(p))))

    @cache
    def move(p, s, i, x):
        try:
            e = native.atomic(p, tuple(map(view,s)), i, x)
        except ValueError:
            return None
        checker.verify_atomic(e)
        return bits(e["after"])

    @cache
    def legal(p, s):
        result = []
        for i, row in enumerate(s):
            for v in view(row):
                t = move(p,s,i,v)
                if t is not None:
                    result.append((i,v,t))
        return tuple(result)

    records = []
    signature_counts = Counter()
    named = None
    for p,s,a,x,y,before,left,right in cases:
        p,s = tuple(p),tuple(s)
        remote = tuple(i for i in range(len(s)) if i != a)
        holders = {v: {i for i in remote if s[i] >> v & 1} for v in (x,y)}
        groups = [g for n in range(len(remote)+1) for g in itertools.combinations(remote,n)]
        graphs = [graph(move(p,s,a,v),lambda state: legal(p,state)) for v in (x,y)]
        shape = lambda state: tuple(sorted(state[i].bit_count()-1 for i in remote))
        projected = [{g:{project(t,g) for t in gr} for g in groups} for gr in graphs]
        shapes = [{shape(t) for t in gr} for gr in graphs]
        terminals = [{t for t,edges in gr.items() if not edges} for gr in graphs]
        arms = []
        for k,(cut,uncut) in enumerate(((x,y),(y,x))):
            gr = graphs[k]
            other = graphs[1-k]
            start = move(p,s,a,cut)
            full = projected[1-k][remote]
            uniq = lambda t: project(t,remote) not in full
            group_records = []
            for g in groups:
                old_proj = projected[k][g]
                exclusive = old_proj - projected[1-k][g]
                expected = {row for row in old_proj if holders[uncut].issubset(g)
                            and all(not mask & (1<<uncut) for mask in row)}
                assert exclusive == expected
                edits = [sum(s[i].bit_count()-m.bit_count() for i,m in zip(g,row)) for row in exclusive]
                group_records.append(dict(charts=g, snapshots=len(old_proj), exclusive=len(exclusive),
                                          minimum_writes=min(edits, default=None)))
            status = {}
            for t in gr:
                if uniq(t):
                    status[t] = "written"
                elif not t[a] & (1<<uncut):
                    status[t] = "erased"
                else:
                    status[t] = "undecided"
                assert (t in other) == (not t[a] & (1<<uncut))
                for i in remote:
                    assert push(p,t[i]) == (len(p)+1-t[i].bit_count(),)+(1,)*(t[i].bit_count()-1)
            for t,edges in gr.items():
                for _,_,u in edges:
                    assert status[t] == "undecided" or status[t] == status[u]
            by_end = Counter()
            # Follow every full word. Distinct orderings that reach the same holdings remain distinct.
            def walk(t):
                if not gr[t]:
                    assert status[t] in ("written", "erased")
                    by_end[status[t]] += 1
                for _,_,u in gr[t]:
                    walk(u)
            walk(start)
            exclusive_shapes=shapes[k]-shapes[1-k]
            terminal_shapes={shape(t) for t in terminals[k]}
            common_terminal_shapes={shape(t) for t in terminals[1-k]}
            assert all(status[t]=="written" for t in gr if shape(t) in exclusive_shapes)
            # Leaving the source unmarked counts its root among the four; this is a different measurement.
            global_shapes=lambda states:{tuple(sorted(m.bit_count()-1 for m in t)) for t in states}
            signature_counts[len(left if k==0 else right),tuple(sorted(exclusive_shapes))]+=1
            arms.append(dict(arm="triangle" if len(left if k==0 else right)==3 else "path",cut=cut,
                             counts=dict(Counter(status.values())),maximal_paths=dict(by_end),
                             terminal_states=dict(Counter(status[t] for t in terminals[k])),
                             group_records=group_records,anonymous_exclusive=sorted(exclusive_shapes),
                             terminal_only_exclusive=sorted(terminal_shapes-common_terminal_shapes),
                             whole_atlas_anonymous_exclusive=sorted(global_shapes(gr)-global_shapes(other)),
                             anonymous_witnesses=sorted(t for t in gr if shape(t) in exclusive_shapes),
                             all_states=len(gr),all_edges=sum(map(len,gr.values()))))
        common_states=set(graphs[0]) & set(graphs[1])
        common_terminals=terminals[0] & terminals[1]
        double_cut=move(p,move(p,s,a,x),a,y)
        assert double_cut==move(p,move(p,s,a,y),a,x)
        assert common_states==set(graph(double_cut,lambda t:legal(p,t)))
        rec=dict(p=p,start=s,source=a,cuts=[x,y],arms=arms,common=len(common_states),
                 common_terminal=len(common_terminals),graphs=[packed_graph(g) for g in graphs])
        records.append(rec)
        if s==(7,15,21,27) and (a,x,y)==(0,1,2):
            named={k:v for k,v in rec.items() if k!="graphs"}
    raw=raw_bytes(records)
    out.write_bytes(lzma.compress(raw))
    assert named is not None
    return dict(cases=len(records),record_bytes=len(raw),record_sha256=hashlib.sha256(raw).hexdigest(),
                signatures_by_topology=sorted([n,sig,f] for (n,sig),f in signature_counts.items()),named=named)


if __name__=="__main__":
    print(json.dumps(run(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])),sort_keys=True,indent=2))
