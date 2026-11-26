"""Exact dictionary census and numerical P1 union on a prepared finite atlas."""
from collections import Counter, defaultdict
from hashlib import sha1
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path
import runpy
import sys

import numpy as np


def pinned(path, expected):
    raw = Path(path).read_bytes()
    assert sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == expected
    return runpy.run_path(str(path))


def determinant_witness(incidence, pairs):
    # An independent nonzero minor gives a lower bound on the rational rank.
    import random
    pool = random.Random(2611).sample(range(len(pairs)), 960)
    matrix = np.array([incidence[i] * incidence[j] for i, j in (pairs[k] for k in pool)],
                      dtype=np.int32)
    rows, cols = [], []
    for c in range(matrix.shape[1]):
        step = len(cols)
        available = np.flatnonzero(matrix[step:, c])
        if not len(available):
            continue
        p = step + int(available[0])
        matrix[[step,p]] = matrix[[p,step]]
        pool[step], pool[p] = pool[p], pool[step]
        pivot = int(matrix[step,c])
        multipliers = matrix[step+1:,c] * pow(pivot,-1,101) % 101
        matrix[step+1:,c:] = (matrix[step+1:,c:] - multipliers[:,None]*matrix[step,c:]) % 101
        rows.append(pool[step])
        cols.append(c)
    # Rows recorded in pivot order have no later interchanges in this minor.
    det = 1
    for i,c in enumerate(cols):
        det = (det * int(matrix[i,c])) % 101
    return dict(row_indices=rows, column_indices=cols, determinant_mod_101=det)


def point(x,y):
    return x % 11 + 11*(y % 11)


def mask(inds):
    return sum(1 << i for i in inds)


def members(bits,n):
    return [i for i in range(n) if bits >> i & 1]


def main(orbit_path, engine_path, cert_path):
    hist = pinned(orbit_path, "45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b")
    engine = pinned(engine_path, "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    orbit, charts, rows = hist["orbit"], hist["charts"], hist["rows"]
    groups = [orbit[k:k+121] for k in range(0,484,121)]
    cols = sum(groups,[])
    assert len(set(cols)) == 484 and Counter(orbit) == Counter({v:2 for v in cols})
    assert all(v.bit_count() == 25 for v in cols)
    inc = np.array([[(s >> i) & 1 for s in cols] for i in charts],dtype=np.int32)
    pairs = list(combinations_with_replacement(charts,2))
    certificate = determinant_witness(inc,pairs)
    assert len(certificate["column_indices"]) == 482 and certificate["determinant_mod_101"]
    for g,h in [(0,3),(1,2)]:
        d = inc[:,g*121:(g+1)*121]
        e = inc[:,h*121:(h+1)*121]
        assert np.array_equal(d@d.T,e@e.T)
    cert_path.write_text(json.dumps(certificate,separators=(",",":"))+"\n")
    def allowed(exterior):
        restrictions = [Counter(v & exterior for v in group) for group in groups]
        keys = set().union(*restrictions)
        return [[a,b] for a,b in product(range(-2,3),repeat=2)
                if all(a*(restrictions[0][k]-restrictions[3][k])
                       + b*(restrictions[1][k]-restrictions[2][k]) == 0 for k in keys)]
    square_counts = {}
    full = (1<<121)-1
    for side in range(1,11):
        square = mask(point(u+v,u-v) for u in range(side) for v in range(side))
        square_counts[side] = allowed(full ^ square)
    refl = [point(-(i//11),-(i%11)) for i in charts]
    line = [i for i in charts if refl[i]==i]
    moved = orbit.copy()
    for k in range(363,484):
        moved[k] = mask(refl[i] for i in members(orbit[k],121))
    new = [mask(j for j,v in enumerate(moved) if v >> i & 1) for i in charts]
    assert all((a^b).bit_count()*4 == hist["work"][i][j]
               for i,a in enumerate(new) for j,b in enumerate(new))
    assert all(r.bit_count()==200 for r in rows+new)
    assert [i for i in charts if rows[i]==new[i]] == line
    assert Counter(Counter(moved).values()) == {1:121,2:242,3:121}
    deltas, fixed_two = Counter(), Counter()
    best = None
    for triple in combinations(charts,3):
        i,j,k = triple
        n = (rows[i]&rows[j]&rows[k]).bit_count()
        m = (new[i]&new[j]&new[k]).bit_count()
        deltas[m-n] += 1
        if sum(v in line for v in triple)==2:
            fixed_two[m-n] += 1
            if m!=n and (best is None or abs(m-n)>abs(best[2]-best[1])):
                best = (triple,n,m)
    assert best is not None
    triple, n, m = best
    parents = (-1,)+(0,)*968
    fine = tuple(range(969))
    grades = (1,)+(2,)*968
    def p1_read(read_rows, triple, orders):
        views = [(0,)+tuple(k+1 for k in members(read_rows[i],968)) for i in triple]
        vals = [engine["push"](parents,fine,V,grades) for V in views]
        union = tuple(sorted(set().union(*views)))
        direct = engine["push"](parents,fine,union,grades)
        for order in orders:
            answer = engine["glue_many"](parents,[views[h] for h in order],[vals[h] for h in order],True)
            assert answer == direct
        for V,val in zip(views,vals):
            assert engine["push"](parents,union,V,direct) == val
        return dict(union_leaves=len(union)-1, root_grade=int(direct[0]),
                    pair_intersections=[(read_rows[i]&read_rows[j]).bit_count() for i,j in combinations(triple,2)])
    # A follow-up readout, chosen after the initial census, on all 25 states.
    # Match supports to leaf addresses inside each restriction class.
    fixed = mask(line)
    slots = defaultdict(list)
    for idx,support in enumerate(orbit):
        slots[support & fixed].append(idx)
    signatures = []
    for a,b in product(range(-2,3),repeat=2):
        offered = defaultdict(list)
        for group,weight in zip(groups,(2+a,2+b,2-b,2-a)):
            for support in group:
                offered[support & fixed].extend([support]*weight)
        assigned = [None]*968
        for key,indices in slots.items():
            assert len(offered[key])==len(indices)
            for idx,support in zip(indices,offered[key]):
                assigned[idx]=support
        state = [mask(j for j,s in enumerate(assigned) if s >> i & 1) for i in charts]
        assert all(state[i]==rows[i] for i in line)
        assert all((state[i]^state[j]).bit_count()*4==hist["work"][i][j] for i,j in pairs)
        roots = [p1_read(state,t,[(0,1,2)])["root_grade"] for t in [(0,5,41),(0,1,41)]]
        signatures.append([a,b,*roots])
    assert len({(v,w) for a,b,v,w in signatures})==25
    return dict(rank=len(certificate["column_indices"]),determinant=certificate["determinant_mod_101"],
                dictionary_solutions=len(allowed(0)), square_exterior_solutions=square_counts,
                line=line,line_solutions=allowed(mask(line)),same_pairs=7260,changed_rows=121-len(line),
                baseline_multiplicities=sorted(Counter(Counter(orbit).values()).items()),
                alternative_multiplicities=sorted(Counter(Counter(moved).values()).items()),
                triple_deltas=sorted(deltas.items()), two_line_triple_deltas=sorted(fixed_two.items()),
                joint_readout_signatures=signatures,
                example=dict(charts=triple, triple_intersections=[n,m],p1=[p1_read(state,triple,permutations(range(3))) for state in (rows,new)]))


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1],sys.argv[2],Path(sys.argv[3])),sort_keys=True,indent=2))
