"""Enumerate endpoints by products of rooted subviews, without calling the historical atom."""
from collections import Counter
from functools import cache
from hashlib import sha1, sha256
from itertools import combinations, product
import json
import lzma
from math import factorial
from pathlib import Path
import sys


def mask_union(rows):
    u=0
    for r in rows:
        u |= r
    return u


@cache
def subviews(p, row):
    return tuple(v for v in range(1,row+1,2) if v & row == v
                 and all(not v & (1<<x) or v & (1<<p[x]) for x in range(1,len(p))))


@cache
def endpoints(p,s):
    u=mask_union(s)
    return tuple(t for t in product(*(subviews(p,v) for v in s)) if mask_union(t)==u)


def outgoing(p,s):
    for i,v in enumerate(s):
        for t in subviews(p,v):
            dropped=v^t
            if dropped and dropped.bit_count()==1:
                z=s[:i]+(t,)+s[i+1:]
                if mask_union(z)==mask_union(s):
                    yield i,dropped.bit_length()-1,z


def subsets(members):
    for n in range(len(members)+1):
        yield from combinations(members,n)


@cache
def projected(p,s,g):
    return frozenset(tuple(e[i] for i in g) for e in endpoints(p,s))


def small_domain():
    counts=Counter()
    digest=sha256()
    for n in range(1,5):
        reps={}
        for parents in product(*(range(j) for j in range(1,n))):
            p=(-1,)+parents
            def form(i):
                return tuple(sorted(form(j) for j in range(1,n) if p[j]==i))
            reps.setdefault(form(0),p)
        for p in reps.values():
            full=(1<<len(p))-1
            views=subviews(p,full)
            states=set()
            for k in range(1,min(len(views),4)+1):
                for rows in combinations(views,k):
                    if mask_union(rows)==full:
                        states.update(endpoints(p,rows))
            counts["states"]+=len(states)
            for s in sorted(states):
                edits=sorted(outgoing(p,s))
                for (a,x,sx),(b,y,sy) in combinations(edits,2):
                    if a!=b:
                        continue
                    counts["source_pairs"]+=1
                    for g in subsets(tuple(i for i in range(len(s)) if i!=a)):
                        counts["groups"]+=1
                        for true,alt,z in [(sx,sy,y),(sy,sx,x)]:
                            hm={i for i,v in enumerate(s) if i!=a and v & (1<<z)}
                            po=projected(p,true,g)
                            other=projected(p,alt,g)
                            exclusive=po-other
                            expected=frozenset(t for t in po if hm.issubset(g) and not mask_union(t)&(1<<z))
                            assert exclusive == expected
                            covered_leaf=not any(i and p[i]==z and mask_union(s)&(1<<i) for i in range(len(p)))
                            assert bool(exclusive)==(covered_leaf and hm.issubset(g))
                            if exclusive:
                                min_edits=min(sum(s[i].bit_count()-r.bit_count() for i,r in zip(g,t)) for t in exclusive)
                                assert min_edits==len(hm)
                            digest.update(repr((p,s,a,x,y,z,g,sorted(exclusive))).encode()+b"\n")
                            counts["projected_snapshots"]+=len(po)
            projected.cache_clear()
            endpoints.cache_clear()
    return dict(**counts,digest=digest.hexdigest())


def verify_cases(path, prior):
    raw=lzma.decompress(path.read_bytes())
    evidence=json.loads(raw)
    # Pin the already independently regenerated 24-case identity list.
    cases=prior.read_bytes()
    assert sha1(f"blob {len(cases)}\0".encode()+cases).hexdigest()=="9c80bb24a39c21bb96a2404724df5f1a59a8af46"
    expected=json.loads(cases)["triangle_pairs_complete"]
    def check_names(submitted):
        return [(r["p"],r["start"],r["source"],*r["cuts"]) for r in submitted]==[tuple(row[:5]) for row in expected]
    assert check_names(evidence)
    assert not check_names(evidence[:-1]) and not check_names(evidence+[evidence[-1]])
    assert not check_names(evidence[:1]+evidence[:1]+evidence[2:])
    totals=Counter()
    for r in evidence:
        p,s=tuple(r["p"]),tuple(r["start"])
        a=r["source"]
        remote=tuple(i for i in range(len(s)) if i!=a)
        x,y=r["cuts"]
        starts=[s[:a]+(s[a]^(1<<v),)+s[a+1:] for v in [x,y]]
        ends=[set(endpoints(p,t)) for t in starts]
        assert r["common"]==len(ends[0]&ends[1])
        both_terminal=[]
        for k,g in enumerate(r["graphs"]):
            canonical=sorted(ends[k])
            index={t:i for i,t in enumerate(canonical)}
            assert list(map(tuple,g["states"]))==canonical
            generated=[sorted((i,v,index[u]) for i,v,u in outgoing(p,t)) for t in canonical]
            assert [[tuple(e) for e in neighbors] for neighbors in g["moves"]]==generated
            arm=r["arms"][k]
            other=ends[1-k]
            alt_cut=r["cuts"][1-k]
            terminal=set(t for t,m in zip(canonical,generated) if not m)
            both_terminal.append(terminal)
            def exclusive(t):
                return not any(t[i] & 1<<alt_cut for i in remote)
            final=Counter("written" if exclusive(t) else "erased" for t in terminal)
            assert dict(final)==arm["terminal_states"]
            # In a star every assignment of last owners admits every permutation
            # of the specified, independent deletions to that fixed final state.
            word_counts=Counter()
            for t in terminal:
                steps=sum(a.bit_count()-b.bit_count() for a,b in zip(starts[k],t))
                word_counts["written" if exclusive(t) else "erased"]+=factorial(steps)
            assert dict(word_counts)==arm["maximal_paths"]
            st=Counter("erased" if t in other else "written" if exclusive(t) else "undecided" for t in canonical)
            assert st==arm["counts"]
            tip_counts=lambda t:tuple(sorted(t[i].bit_count()-1 for i in remote))
            anonymous={tip_counts(t) for t in canonical}-{tip_counts(t) for t in other}
            assert sorted(anonymous)==list(map(tuple,arm["anonymous_exclusive"]))
            assert sorted(t for t in canonical if tip_counts(t) in anonymous)==list(map(tuple,arm["anonymous_witnesses"]))
            for gg in arm["group_records"]:
                who=tuple(gg["charts"])
                true=projected(p,starts[k],who)
                unique=true-projected(p,starts[1-k],who)
                assert (len(true),len(unique))==(gg["snapshots"],gg["exclusive"])
                n=min((sum(s[i].bit_count()-row.bit_count() for i,row in zip(who,u)) for u in unique), default=None)
                assert gg["minimum_writes"]==n
            totals["arm_states"]+=len(canonical)
            totals["arm_edges"]+=sum(map(len,generated))
            totals["maximal_words"]+=sum(word_counts.values())
        assert r["common_terminal"]==len(set.intersection(*both_terminal))
    return dict(cases=len(expected),**totals,record_sha256=sha256(raw).hexdigest())


if __name__=="__main__":
    print(json.dumps(dict(case_verification=verify_cases(Path(sys.argv[1]),Path(sys.argv[2])/"native.json"),
                          general_check=small_domain()),sort_keys=True,indent=2))
