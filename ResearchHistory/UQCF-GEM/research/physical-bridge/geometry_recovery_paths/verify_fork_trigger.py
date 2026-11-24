"""Reconstruct each graph from the two endpoint shuffles and rooted subtree grades."""
from collections import Counter, defaultdict
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
import lzma
from math import comb
from pathlib import Path
import sys

from verify_fixed_pair import compare, encoded, members, need, restriction
from verify_receiver_turn import trees


def weave(left, right):
    for positions in combinations(range(len(left)+len(right)),len(left)):
        where = set(positions)
        a, b = iter(left), iter(right)
        yield [next(a) if i in where else next(b) for i in range(len(left)+len(right))]


def lineage(p, tip):
    path = [tip]
    while path[-1]:
        path.append(p[path[-1]])
    return path


def materialize(p, g, tips, s, a, extra=0):
    p, g = tuple(p), tuple(g)
    n = len(p)
    r = 1-s
    b, = set(tips)-{a}
    route_a, route_b = lineage(p,a), lineage(p,b)
    c = next(v for v in route_a if v in route_b)
    left, right = route_a[:route_a.index(c)], route_b[:route_b.index(c)]
    stem = route_a[route_a.index(c):-1]
    m, k = len(left), len(left)+len(right)-1
    active_n = n-extra-1 if extra else n
    full_active = (1<<active_n)-1
    prior = [full_active, full_active]
    if extra:
        relay = ((1<<n)-1) ^ full_active | 1
        prior += [relay, relay ^ (1<<(n-1))]
    after = prior.copy()
    after[s] ^= 1 << a
    spectator = [3*n+j for j in reversed(range(active_n,n-1))] if extra else []
    children = [sum(1<<w for w in range(1,n) if p[w]==v) for v in range(n)]

    @lru_cache(None)
    def profile(family):
        tau = []
        for kids in children:
            if not kids:
                tau.append(0)
                continue
            best = len(family)+1
            for subset in range(1,1<<len(family)):
                if subset.bit_count()>=best:
                    continue
                seen = 0
                for i in members(subset,len(family)):
                    seen |= family[i]
                if seen & kids == kids:
                    best = subset.bit_count()
            tau.append(best)
        return tuple(tau),max(1,max(tau))

    def key(state):
        return "/".join(map(str,state))

    def grade(view):
        return [list(t) for t in zip(members(view,n), restriction(p,view,g))]

    def meta(x, y, par):
        f, h = profile(tuple(x))
        ff, hh = profile(tuple(y))
        return [f[par], ff[par], h, hh, hh-h, ff[par]>f[par]]

    def snapshot(st):
        number = key(st)
        if number not in states:
            f, h = profile(tuple(st))
            states[number] = dict(receiver=grade(st[r]), tau=f[c], h=h, edges={})
        return number

    start = key(after)
    states, ends, details = {}, {}, {}
    for split in (False,True):
        owner = r if split else s
        sided = [s*n+v for v in left[1:]]
        opposite = [owner*n+v for v in right]
        suffix = [] if split else [s*n+v for v in stem]
        words = sorted(z for w in weave(sided,opposite) for z in weave(w+suffix,spectator))
        final = None
        for word in words:
            st = after.copy()
            for command in word:
                i, v = divmod(command,n)
                previous = snapshot(st)
                nxt = st.copy()
                nxt[i] ^= 1 << v
                need(bool(st[i] & (1<<v)) and not (st[i] & children[v]) and any(
                    j!=i and chart & (1<<v) for j,chart in enumerate(st)), "impossible reconstructed atom")
                following = snapshot(nxt)
                states[previous]["edges"][str(command)] = [following,p[v],meta(st,nxt,p[v])]
                st = nxt
            if final is None:
                final = snapshot(st)
            need(key(st)==final,"endpoint")
        factor = min(words, key=lambda word: [(cmd//n,-(cmd%n)) for cmd in word])
        ends[final] = dict(words=words, factor=factor, uniform_enabled="1/2")
        baseline = dict(grade(after[r]))[c]
        scalar = baseline + (sum(g[v] for v in right) if split else 0)
        need(dict(states[final]["receiver"])[c]==scalar,"terminal read")
        length = k + (0 if split else len(stem))
        interleavings = comb(length+extra,extra)
        num = comb(k,m-1)*interleavings
        need(num==len(words),"symbolic schedule multiplicity")
        fires_by_r = comb(k-1,m-1)*interleavings if split else 0
        details["write" if split else "unchanged"] = dict(count=num, edits=length+extra, scalar=scalar,
                early=num-fires_by_r if split else 0, local_triggers=num if split else 0,
                global_rises=num if split and not extra else 0, receiver_fired=fires_by_r, uniform_enabled="1/2")
    record = dict(parents=list(p), grades=list(g), source=s, cut=a, fork=c,
                  before=key(prior), after=start, prior_receiver=grade(prior[r]), source_fields=meta(prior,after,p[a]),
                  states=states, endpoints=ends)
    return record,details


def expected_data():
    universe, examples = {},{}
    totals = Counter()
    for p in trees():
        tips = [v for v in range(1,len(p)) if v not in p[1:]]
        if len(tips)!=2:
            continue
        g = [3 if v==0 else 4 if v not in tips else 2 for v in range(len(p))]
        for s in (0,1):
            decisions=[]
            for a in tips:
                row, counts = materialize(p,g,tips,s,a)
                universe["bare:"+"/".join(map(str,p))+f":{s}:{a}"] = row
                decisions.append(counts["write"])
                totals.update(source_arms=1,indexed_states=len(row["states"]),
                              legal_edges=sum(len(x["edges"]) for x in row["states"].values()),
                              complete_histories=sum(x["count"] for x in counts.values()),
                              with_fork_trigger=counts["write"]["count"], reading_before_trigger=counts["write"]["early"])
            distinct = decisions[0]["scalar"] != decisions[1]["scalar"]
            totals["distinct_mass_pairs" if distinct else "equal_mass_pairs"] += 1
            totals["distinct_mass_writes" if distinct else "equal_mass_writes"] += sum(x["count"] for x in decisions)
    for name,t in (("named",0),("one",1),("two",2),("balanced",0)):
        p = [-1,0,1,1,3,2,4]
        g = [5,3,4,1,4,2,2]
        if name=="balanced":
            g[0],g[2] = 4,5
        if t:
            g[0] -= t+1
            for i in range(t+1):
                p.append(0 if i==0 else len(p)-1)
                g.append(1)
        for a in (5,6):
            key=f"{name}:{a}"
            universe[key],examples[key] = materialize(p,g,(5,6),1,a,t)
    return universe,dict(totals),examples


def spectator_projection(universe):
    for a in (5,6):
        base = universe[f"named:{a}"]
        for group,t in (("one",1),("two",2)):
            row = universe[f"{group}:{a}"]
            need(base["prior_receiver"]==row["prior_receiver"], "changed active receiver preparation")
            for i in (0,1):
                masks=list(map(int,row["before"].split("/")))
                simple=list(map(int,base["before"].split("/")))
                need(restriction(tuple(row["parents"]),
                                 masks[i],tuple(row["grades"]))==restriction(tuple(base["parents"]),simple[i],tuple(base["grades"])),
                     "changed active source or receiver P1 prior")
            projected={}
            n=len(row["parents"])
            for end, result in row["endpoints"].items():
                active_end="/".join(end.split("/")[:2])
                projected[active_end]=Counter(tuple(7*(cmd//n)+cmd%n for cmd in w if cmd//n<2) for w in result["words"])
            for end,old in base["endpoints"].items():
                need(projected[end]=={tuple(w):comb(len(w)+t,t) for w in old["words"]},"unrelated command changed active history")
            for key, state in row["states"].items():
                old=base["states"]["/".join(key.split("/")[:2])]
                need(old["receiver"]==state["receiver"] and old["tau"]==state["tau"] and state["h"]==2,
                     "active projection or global masking")


def run(directory):
    data = lzma.decompress((directory/"fork_trigger_universe.json.xz").read_bytes())
    actual=json.loads(data)
    ref, counts, examples=expected_data()
    compare(ref, actual)
    need(encoded(actual)==data, "noncanonical universe")
    spectator_projection(ref)
    cert=dict(historical_sha="e61d5b0e827f7b412824ad46021e2ad6cc6f7875",
              historical_blobs=dict(overlap="b18f52109ccff9c7dc77542d3b8f3e5d5989102a",cut="c10ac57f988a439144e21898bd2b33ece0838a9b",
                                    gate="91cd1e507e955683e744fbdbb0745cac19d66cb3",poset="36c894db328c0865007df3ca273ddb059475fe4a"),
              raw_sha256=sha256(data).hexdigest(),bare=counts,examples=examples)
    compare(cert,json.loads((directory/"fork_trigger_certificate.json").read_bytes()))
    need([examples[f"named:{a}"]["write"]["scalar"] for a in (5,6)]==[10,9] and
         [examples[f"balanced:{a}"]["write"]["scalar"] for a in (5,6)]==[10,10], "mass matching control")
    arm=ref["named:5"]
    output=next(x for x in arm["endpoints"].values() if len(x["factor"])==4)
    edge=next(e for s in arm["states"].values() for e in s["edges"].values() if e[-1][-1])
    altered=[
        (arm["states"], lambda z:z.pop(arm["after"])),
        (output["words"], lambda z:z.append(z[0])),
        (output["words"], lambda z:z[0].__setitem__(0,987)),
        (edge, lambda z:z[2].__setitem__(5,False)),
        (edge, lambda z:z.__setitem__(1,9)),
        (arm["prior_receiver"], lambda z:z[1].__setitem__(1,0)),
        (examples["one:5"], lambda z:z["unchanged"].update(count=20)),
        (examples["one:6"], lambda z:z["write"].update(global_rises=z["write"]["count"])),
        (examples["two:5"], lambda z:z["write"].update(uniform_enabled="5/12")),
        (cert, lambda z:z.update(historical_sha="unbound")),
        (cert, lambda z:z["bare"].update(complete_histories=0)),
    ]
    for obj, mutate in altered:
        bad=deepcopy(obj)
        mutate(bad)
        try:
            compare(obj,bad)
        except ValueError:
            continue
        raise AssertionError("corrupt evidence accepted")
    print(json.dumps(dict(status="PASS",rejecting_controls=len(altered),**counts),sort_keys=True))


if __name__=="__main__":
    run(Path(sys.argv[1]))
