"""Separate 11x11 verification from row bits and explicit small-family enumeration."""
from collections import Counter
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import json

here = Path(__file__).resolve().parent
reported = json.loads((here/'results.json').read_text())
V = tuple(product(range(11), repeat=2))
origin = (0,0)

def displacement(x,y):
    jumps = [min((i-j)%11, (j-i)%11) for i,j in zip(x,y)]
    return tuple(sorted(jumps))

shape = {v for v in V if displacement(v,origin) in {(0,0),(0,1),(1,1),(0,2)}
         or (displacement(v,origin) in {(2,3),(3,4)} and displacement(v,(3,3)) not in {(0,0),(0,1)})}
assert len(shape) == 25
def plus(x,y):
    return tuple((i+j)%11 for i,j in zip(x,y))
T = {t:frozenset(plus(s,t) for s in shape) for t in V}

# Directly count per-address differences from only the 121 variable columns.
# The other 847 are the same in every state, so these pair checks extend to all 968.
pairs = tuple(combinations(V,2))
def distances(rows):
    return tuple(len(rows[a]^rows[b]) for a,b in pairs)
def transpose(col):
    return {v:{label for label,group in col.items() if v in group} for v in V}
base = distances(transpose(T))
grid = {}
for u,v in V:
    grid[plus((u,u),(v,-v))] = (u,v)
results = []
for row in reported['squares']:
    r = row['side']
    out = set(q for q in V if max(grid[q]) >= r)
    groups = {}
    for t,support in T.items():
        groups.setdefault(frozenset(support & out), []).append(t)
    blocks = [sorted(g) for g in groups.values()]
    mult = Counter(map(len,blocks))
    assert {str(n):k for n,k in mult.items()} == row['named_class_sizes']
    ways = prod(comb(n,n//2)**k for n,k in mult.items())
    assert ways == row['profiles']
    if r != 9:
        continue
    choices = [list(combinations(block,len(block)//2)) for block in blocks]
    baseline_out = None
    profiles = set()
    for selections in product(*choices):
        cols = {}
        picked = set()
        for block, negative in zip(blocks,selections):
            k = len(negative)
            picked.update(negative)
            for label, src in zip(block, list(negative) + sorted(set(block)-set(negative))):
                cols[label] = set(V)-T[src] if label in block[:k] else T[src]
        rows = transpose(cols)
        assert distances(rows) == base
        memberships = tuple(frozenset(rows[q]) for q in sorted(out))
        populations = tuple(len(cols[t]) for t in V)
        if baseline_out is None:
            baseline_out = memberships, populations
        assert (memberships, populations) == baseline_out
        d = tuple(len(rows[q]) for q in V)
        assert all(count == 25+len(picked)-2*sum(q in T[t] for t in picked)
                   for q,count in zip(V,d))
        profiles.add(d)
    assert len(profiles) == ways == 16
    results.append(dict(side=r, explicitly_enumerated=len(profiles), exterior_charts=len(out)))
# Verify the convolution inverse independently by elimination over F11.
matrix = [[int(q in T[t]) for t in V] for q in V]
for j in range(len(V)):
    pivot = next(i for i in range(j,len(V)) if matrix[i][j] % 11)
    matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
    row = matrix[j]
    inv = pow(row[j], -1, 11)
    for i in range(j+1,len(V)):
        scale = matrix[i][j]*inv % 11
        if scale:
            matrix[i] = [(x-scale*y)%11 for x,y in zip(matrix[i],row)]
print(json.dumps(dict(exact_rank_mod_11=len(V), small_family=results),sort_keys=True))
