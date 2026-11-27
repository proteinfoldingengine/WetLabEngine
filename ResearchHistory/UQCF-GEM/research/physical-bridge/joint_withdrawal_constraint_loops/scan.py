"""Measure incompatible pairs with successful historical calls and an actual rejecting third call."""
import hashlib
import importlib.util
import itertools
import json
import sys
from functools import cache
from pathlib import Path


def pinned(path, expected):
    raw = path.read_bytes()
    assert hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest() == expected
    return raw


def mask(row):
    return sum(1 << x for x in row)


def run(root):
    base = root / "v16.26-consistency-increment-law"
    pinned(base / "engine.py", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    spec=importlib.util.spec_from_file_location("old",base/"engine.py")
    native=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    doc=json.loads(pinned(base/"evidence/PRODUCTION.json","25e15faf44bb59c77cdd48abf7c8473395c1ae04"))
    official={r["code"]:r for r in doc["instances"]}

    @cache
    def move(p,s,i,x):
        try:
            return tuple(map(tuple,native.atomic(p,s,i,x)["after"]))
        except ValueError:
            return None

    @cache
    def graph(p,s,a):
        edges = set()
        for i,j in itertools.combinations((k for k in range(len(s)) if k != a),2):
            for x in (set(s[i]) & set(s[j])) - {0}:
                u,v=move(p,s,i,x),move(p,s,j,x)
                if u is not None and v is not None and move(p,u,j,x) is None:
                    assert move(p,v,i,x) is None
                    edges.add((i,j))
        return tuple(sorted(edges))

    @cache
    def projected_words(p,s,actors):
        out = {tuple(() for _ in actors)}
        for k,i in enumerate(actors):
            for x in s[i]:
                t=move(p,s,i,x)
                if t is not None:
                    for word in projected_words(p,t,actors):
                        out.add(word[:k]+((x,)+word[k],)+word[k+1:])
        return frozenset(out)

    def named():
        p=(-1,0,0,0,0)
        s=((0,1,2),(0,1,3,4),(0,1,2,3),(0,2,4))  # A,B,C,D
        arms=[s,move(p,s,0,1),move(p,s,0,2)]
        assert all(arms)
        chart_words=[]
        rows=[]
        for state in arms:
            individual={i:projected_words(p,state,(i,)) for i in range(1,4)}
            chart_words.append(individual)
            tests=[]
            observed=[]
            for i,j in itertools.combinations(range(1,4),2):
                paired=projected_words(p,state,(i,j))
                product={(a[0],b[0]) for a,b in itertools.product(individual[i],individual[j])}
                assert paired <= product
                if paired != product:
                    observed.append((i,j))
                tests.append([i,j,len(product),len(paired)])
            assert tuple(observed) == graph(p,state,0)
            rows.append(dict(edges=observed,word_pair_counts=tests))
        assert chart_words[0] == chart_words[1] == chart_words[2]
        assert [len(r["edges"]) for r in rows] == [2,2,3]
        # Check the entire intrinsic graph under every chart and unconstrained tip renaming.
        relabels=0
        for pi in itertools.permutations(range(4)):
            for perm in itertools.permutations(range(1,5)):
                site=(0,)+perm
                for stage,state in enumerate(arms):
                    remapped=tuple(tuple(sorted(site[x] for x in state[idx])) for idx in pi)
                    edges=tuple(sorted(tuple(sorted((pi.index(i),pi.index(j)))) for i,j in rows[stage]["edges"]))
                    assert graph(p,remapped,pi.index(0)) == edges
                relabels+=1
        overlap_edges = [(i,j) for i,j in itertools.combinations(range(1,4),2)
                         if (set(s[i]) & set(s[j])) - {0}]
        assert len(overlap_edges)==3 and all(t[1:] == s[1:] for t in arms)
        return dict(states=arms,stages=rows,individual_language_sizes=[len(v) for v in chart_words[0].values()],
                    common_naive_overlap=overlap_edges,relabelings=relabels)

    example=named()
    matched=[]
    hits=[]
    example_seen=False
    total=0
    for sc,p in native.shapes(5):
        digest=hashlib.sha256()
        for s in native.covers(p):
            for a,row in enumerate(s):
                choices=[]
                for x in row:
                    try:
                        e=native.atomic(p,s,a,x)
                    except ValueError:
                        continue
                    total+=1
                    f=tuple(e[k] for k in ("tau_before","tau_after","h_before","h_after","trigger"))
                    digest.update((repr((s,a,x)+f)+"\n").encode())
                    hs={j for j,r in enumerate(s) if x in r}
                    if x not in p[1:] and len(hs)==3:
                        choices.append((x, hs-{a}, f, tuple(map(tuple,e["after"]))))
                for (x,h,f,u),(y,j,g,v) in itertools.combinations(choices,2):
                    if h==j or f!=g:
                        continue
                    old,l,r=graph(p,s,a),graph(p,u,a),graph(p,v,a)
                    key=[p,tuple(map(mask,s)),a,x,y,old,l,r]
                    matched.append(key)
                    if len(old)<3 and ((len(l)==3) != (len(r)==3)):
                        hits.append(key)
                        if (p==(-1,0,0,0,0) and tuple(map(mask,s))==(7,15,21,27)
                                and (a,x,y)==(0,1,2)):
                            example_seen=True
        assert digest.hexdigest()==official[sc]["digest"]
        graph.cache_clear()
        move.cache_clear()
    assert total==doc["atomic"] and example_seen
    def sha(rows):
        return hashlib.sha256((json.dumps(sorted(rows),separators=(",",":"))+"\n").encode()).hexdigest()
    return dict(events=total,matched=len(matched),triangle_pairs=len(hits),matched_sha256=sha(matched),
                triangle_sha256=sha(hits),example=example,triangle_pairs_complete=sorted(hits))


if __name__=="__main__":
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
