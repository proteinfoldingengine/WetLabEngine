"""Independent threshold audit of the supplied 18 inherited endpoint records.
No producer/verifier imports. Coverage identities are inherited from PR81;
this script does not independently enumerate the canonical endpoint universe.
"""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def state_space(parents, k):
    n = len(parents)
    views = []
    for mask in range(1 << n):
        nodes = frozenset(i for i in range(n) if mask & (1 << i))
        if 0 in nodes and all(v == 0 or parents[v] in nodes for v in nodes):
            views.append(nodes)
    return {tuple(x) for x in product(views, repeat=k)
            if frozenset().union(*x) == frozenset(range(n))}

def neighbors(states, n):
    out = {}
    for state in states:
        adjacent = []
        for i, view in enumerate(state):
            for v in range(1,n):
                other = list(state)
                other[i] = view ^ {v}
                other = tuple(other)
                if other in states:
                    adjacent.append(other)
        out[state] = adjacent
    return out

def profile(parents, state):
    values = []
    for v in range(len(parents)):
        children = frozenset(w for w in range(1,len(parents)) if parents[w] == v)
        if not children:
            values.append(0)
            continue
        for size in range(1,len(state)+1):
            if any(children <= frozenset().union(*family)
                   for family in combinations(state,size)):
                values.append(size)
                break
    return tuple(values)

def reachable(graph, allowed, start, end):
    if start not in allowed or end not in allowed:
        return False
    todo, seen = deque([start]), {start}
    while todo:
        x = todo.popleft()
        if x == end:
            return True
        for y in graph[x]:
            if y in allowed and y not in seen:
                seen.add(y)
                todo.append(y)
    return False

def minima(graph, costs, start, end, lexicographic):
    restrictions = set(graph)
    answer = []
    for i in range(3):
        base = restrictions if lexicographic else set(graph)
        for t in sorted({costs[x][i] for x in base}):
            allowed = {x for x in base if costs[x][i] <= t}
            if reachable(graph,allowed,start,end):
                answer.append(t)
                if lexicographic:
                    restrictions = allowed
                break
        else:
            raise ValueError("disconnected full cover graph")
    return tuple(answer)

def audit():
    records = json.loads((HERE.parent / "v16.36-barrier-law-closure" / "PRODUCTION.json").read_text())["pairs"]
    if len(records) != 18:
        raise ValueError("expected the frozen supplied 18-record corpus")
    cache, results = {}, []
    for index,r in enumerate(records):
        p,k = tuple(r["parents"]),r["view_count"]
        if (p,k) not in cache:
            states = state_space(p,k)
            graph = neighbors(states,len(p))
            qs = {x:profile(p,x) for x in states}
            cache[p,k] = graph,qs
        graph,qs = cache[p,k]
        a,b = tuple(map(frozenset,r["a"])),tuple(map(frozenset,r["b"]))
        q0 = tuple(r["q"])
        if a not in graph or b not in graph or qs[a] != q0 or qs[b] != q0:
            raise ValueError("invalid supplied endpoint/profile")
        costs = {}
        for x,qx in qs.items():
            d = [abs(u-v) for u,v in zip(qx,q0)]
            costs[x] = (sum(d),max(d,default=0),sum(v != 0 for v in d))
        independent = minima(graph,costs,a,b,False)
        lex = minima(graph,costs,a,b,True)
        supplied = (r["B1"],r["Binf"],r["Bs"])
        results.append({"record":index,"parents":p,"views":k,
                        "states":len(graph),"supplied":supplied,
                        "independent":independent,"lexicographic":lex})
    return {"scope":"SUPPLIED_18_RECORD_NUMERICAL_AUDIT_NOT_UNIVERSE_ENUMERATION",
            "records":len(results),
            "independent_disagreements":sum(x["independent"] != x["supplied"] for x in results),
            "lexicographic_disagreements":sum(x["lexicographic"] != x["supplied"] for x in results),
            "objective_distinctions":sum(x["independent"] != x["lexicographic"] for x in results),
            "results":results}

if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, sort_keys=True))
