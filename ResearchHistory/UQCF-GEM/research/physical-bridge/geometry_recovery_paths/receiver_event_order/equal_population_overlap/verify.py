"""Independent set reconstruction, minor check, negative controls and triple census."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


def coord(i):
    return i%11, i//11


def address(x,y):
    return x%11 + 11*(y%11)


def points():
    # Original 25 positions read geometrically from the archived chart table.
    return [(0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),
            (2,8),(3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),
            (8,9),(9,0),(9,3),(9,8),(10,0),(10,1),(10,10)]


def minor_det_mod_101(rows):
    # Separate pure-Python calculation using exact integers, with pivot swaps.
    d = 1
    for j in range(len(rows)):
        k = next(k for k in range(j,len(rows)) if rows[k][j])
        if k != j:
            d = -d
            rows[k],rows[j] = rows[j],rows[k]
        top = rows[j]
        d = d * top[j] % 101
        inv = pow(top[j],-1,101)
        for lower in rows[j+1:]:
            if lower[j]:
                factor = lower[j]*inv % 101
                lower[j:] = [(a-factor*b)%101 for a,b in zip(lower[j:],top[j:])]
    return d


def main(directory):
    out = json.loads((directory/'results.json').read_text())
    cert = json.loads((directory/'rank_minor.json').read_text())
    sites = range(121)
    blocks = []
    for sx,sy in product((-1,1),repeat=2):
        blocks.append([frozenset(address(sx*x+tx,sy*y+ty) for x,y in points())
                       for tx,ty in product(range(11),repeat=2)])
    dictionary = sum(blocks,[])
    assert len(set(dictionary))==484
    pairs = list(combinations_with_replacement(sites,2))
    rr,cc = cert['row_indices'],cert['column_indices']
    assert len(set(rr))==len(set(cc))==len(rr)==len(cc)==482
    minor = [[int(i in dictionary[c] and j in dictionary[c]) for c in cc]
             for i,j in (pairs[k] for k in rr)]
    det = minor_det_mod_101(minor)
    assert det == cert['determinant_mod_101'] == out['determinant'] != 0
    rows = [[sum(1<<t for t,s in enumerate(block) if i in s) for i in sites] for block in blocks]
    def populations(indices):
        vals = []
        for row in rows:
            bits = (1<<121)-1
            for i in indices:
                bits &= row[i]
            vals.append(bits.bit_count())
        return vals
    for i,j in pairs:
        t,u,v,w = populations((i,j))
        assert (t,u)==(w,v)
    params = list(product(range(-2,3),repeat=2))
    line = set(out['line'])
    assert line=={address(i,-i) for i in range(11)}
    for side in range(12):
        if side==0:
            E = line
        elif side==11:
            E = set()
        else:
            E = set(sites)-{address(u+v,u-v) for u,v in product(range(side),repeat=2)}
        restricted = [Counter(s.intersection(E) for s in block) for block in blocks]
        def profile(a,b):
            hist = Counter()
            for count,block in zip((2+a,2+b,2-b,2-a),restricted):
                for mask,n in block.items():
                    hist[mask] += count*n
            return +hist
        base = profile(0,0)
        allowed = [list(p) for p in params if profile(*p)==base]
        expected = out['line_solutions'] if not side else (params if side==11 else out['square_exterior_solutions'][str(side)])
        assert allowed == list(map(list,expected))
    # An unmatched replacement changes pair data, a permutation of names does not change any triple.
    src,dst = blocks[3][0],blocks[0][0]
    damaged = sum(((i in src)^(j in src))!=((i in dst)^(j in dst)) for i,j in combinations(sites,2))
    assert damaged>0
    original = dictionary*2
    swapped = original.copy()
    swapped[0],swapped[1] = swapped[1],swapped[0]
    assert Counter(swapped)==Counter(original) and swapped!=original
    # In this second implementation use orbit co-holding counts directly.
    change, fixed, single_triple_max = Counter(),Counter(),0
    anchors = (0,41)
    probes = []
    for triple in combinations(sites,3):
        w,x,y,z = populations(triple)
        first,second = w-z,x-y
        change[first]+=1
        if len(line.intersection(triple))==2:
            fixed[first]+=1
        single_triple_max=max(single_triple_max,len({a*first+b*second for a,b in params}))
        if set(anchors)<=set(triple) and len(line.intersection(triple))==2:
            probes.append((triple,2*(w+x+y+z),first,second))
    assert sorted(change.items())==list(map(tuple,out['triple_deltas']))
    assert sorted(fixed.items())==list(map(tuple,out['two_line_triple_deltas']))
    witness = tuple(out['example']['charts'])
    pair_counts = [2*sum(populations(p)) for p in combinations(witness,2)]
    w,x,y,z = populations(witness)
    base = 2*(w+x+y+z)
    for state,intersection in zip(out['example']['p1'],[base,base+w-z]):
        union = 600-sum(pair_counts)+intersection
        assert (state['pair_intersections'],state['union_leaves'],state['root_grade']) == (pair_counts,union,1937-2*union)
    # Keep the original witness and select the least indexed third chart giving an independent equation.
    r = next(p for p in probes if p[0]==witness)
    s = next(p for p in probes if r[2]*p[3]!=r[3]*p[2])
    signatures = {(r[1]+a*r[2]+b*r[3],s[1]+a*s[2]+b*s[3]) for a,b in params}
    assert len(signatures)==25 and single_triple_max<25
    for a,b,first,second in out['joint_readout_signatures']:
        for probe,root in ((r,first),(s,second)):
            charts,offset,da,db = probe
            pair_sum = sum(2*sum(populations(p)) for p in combinations(charts,2))
            assert root==1937-2*(600-pair_sum+offset+a*da+b*db)
    return dict(modular_minor_determinant=det, unmatched_substitution_changes_pairs=damaged,
                triple_changes=sum(change.values())-change[0], two_fixed_triple_changes=sum(fixed.values())-fixed[0],
                max_distinct_readings_one_triple=single_triple_max,
                two_triples=[r,s], two_triple_signatures=len(signatures),
                control_leaf_rename_preserves_column_multiset=True)


if __name__=="__main__":
    print(json.dumps(main(Path(__file__).resolve().parent),sort_keys=True,indent=2))
