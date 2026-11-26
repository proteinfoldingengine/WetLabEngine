"""Independent coordinates, exact source rank, exhaustive trades and set-based local readout."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, islice, product
from pathlib import Path
import json
import numpy as np
from sympy import Matrix

SHAPE=((0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
       (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),
       (9,3),(9,8),(10,0),(10,1),(10,10))
def point(x,y):
    return x%11+11*(y%11)


def kernel_check(columns,source):
    # Dictionary in orientation/translation order. Each type has two addressed copies.
    relevant=[s for s in dict.fromkeys(columns) if source in s]
    assert len(relevant)==100 and all(columns.count(s)==2 for s in relevant)
    m=Matrix([[int(i in s) for s in relevant] for i in range(121)])
    vectors=m.nullspace()
    assert len(vectors)==8
    kernel=Matrix.hstack(*vectors)
    assert all(x.is_Integer for x in kernel)
    # Sympy uses distinct free-coordinate unit rows. Every admissible difference
    # has free entries in [-2,2] and is represented exactly once.
    free=[next(i for i in range(100) if list(kernel.row(i))==[int(j==k) for j in range(8)])
          for k in range(8)]
    assert len(set(free))==8 and not any(m*kernel)
    basis=np.array(kernel.tolist(),dtype=np.int32)
    histogram=Counter()
    ordered_minimum=[]
    parameters=product(range(-2,3), repeat=8)
    while part:=list(islice(parameters,2048)):
        offsets=np.asarray(part,dtype=np.int32)@basis.T
        legal=offsets[(abs(offsets)<=2).all(axis=1)]
        assert (legal.sum(axis=1)==0).all()
        degrees=np.maximum(legal,0).sum(axis=1)
        histogram.update(map(int,degrees))
        for offset in legal[degrees==4]:
            ordered_minimum.append([[i for i,x in enumerate(offset) for _ in range(max(0,int(sign*x)))]
                                    for sign in (1,-1)])
    # Separate direct low-degree check. A base-4 digit stores the number of selected
    # footprints at one chart. Up to three choices means there are no carries.
    encoded=[sum(4**i for i in s) for s in relevant]
    direct=[]
    for k in (1,2,3):
        sigs=set()
        for idx in combinations_with_replacement(range(100),k):
            if k==3 and idx[0]==idx[-1]:
                continue
            value=sum(encoded[i] for i in idx)
            assert value not in sigs
            sigs.add(value)
        direct.append(len(sigs))
    assert min(k for k in histogram if k)==4 and histogram[4]==8
    return dict(rational_rank=100-len(vectors),feasible_difference_vectors=sum(histogram.values()),
                directed_minimal_vectors=ordered_minimum, exhaustive_distinct_signatures_k1_k2_k3=direct)


def local_anchor(world,order,receiver):
    # Compute winners as sets, then carry out only the initial anchor transfers
    # until a genuine receiver gain. This does not use the path or writer code.
    rows=[{v for v,s in enumerate(world,1) if i in s} for i in order]
    seen=set()
    survivors=[]
    for row in rows:
        survivors.append(row-seen)
        seen |= row
    assert len(seen)==968
    pos=order.index(receiver)
    boundary=len(survivors[pos])
    assert min(map(len,survivors))>len(order)
    for anchor in range(1,len(order)+1):
        old=next(i for i,s in enumerate(survivors) if anchor in s)
        new=anchor-1
        if old==new:
            continue
        survivors[new].add(anchor)
        survivors[old].remove(anchor)
        if new==pos:
            count=len(survivors[pos])
            return boundary,dict(address=anchor,leaves=count,pin=1937-2*count,new_to_prior=anchor not in rows[pos])
    return boundary,None


def main():
    data=json.loads(Path(__file__).with_name("results.json").read_text())
    col=[]
    for swap,sx,sy,tx,ty in product((False,True),(-1,1),(-1,1),range(11),range(11)):
        col.append(frozenset(point(tx+sx*(y if swap else x),ty+sy*(x if swap else y)) for x,y in SHAPE))
    check=kernel_check(col,0)
    source_states=[]
    for releases in data['leaf_addresses']:
        st=col.copy()
        for a in releases:
            assert 0 in st[a-1]
            st[a-1]=st[a-1]-{0}
        source_states.append(st)
    # A pair measurement at (0,j) sees only the number of these four leaves at j.
    aa,bb=data['leaf_addresses']
    assert all(sum(j in col[a-1] for a in aa)==sum(j in col[b-1] for b in bb) for j in range(121))
    relevant=[s for s in dict.fromkeys(col) if 0 in s]
    actual=[[relevant.index(col[a-1]) for a in arm] for arm in (aa,bb)]
    assert actual in check['directed_minimal_vectors']
    reflection=col.copy()
    for j in range(363,484):
        reflection[j]=frozenset(point(-(i//11),-(i%11)) for i in col[j])
    for key,worlds in [('single_source_collision',source_states),('source_last_control',source_states),
                       ('reflected_preparation',[col,reflection])]:
        exp=data[key]
        for w,arm in zip(worlds,exp['arms']):
            count,gain=local_anchor(w,exp['order'],exp['receiver'])
            assert count==arm['after_contraction']
            if gain:
                assert gain=={k:arm['first_gain'][k] for k in gain}
            else:
                assert arm['first_gain'] is None
    # For any common leaf priority, if source is last the winners agree on all leaves.
    order=data['source_last_control']['order']
    assert order[-1]==0 and all(next(i for i in order if i in a)==next(i for i in order if i in b)
                                     for a,b in zip(*source_states))
    return check


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
