"""Compare original v16.43 primitive traces to a separate exact cover calculation."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

demos = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(demos / "v16.43-star-fiber-classification"),
                str(demos / "v16.23-overlap-descent")]
from producer import normalize
from engine import push

K = 3
labels = range(K)
palettes = tuple(h for size in range(1,K+1) for h in combinations(labels,size))
def first_cover(columns):
    return next(h for h in palettes if all(any(s & (1<<a) for a in h) for s in columns))

def rows_of(columns):
    return tuple(1 + sum(1 << v for v,s in enumerate(columns,1) if s & (1 << a))
                 for a in labels)

def drop(columns, leaf, chart):
    changed = list(columns)
    changed[leaf] ^= 1 << chart
    assert changed[leaf] and columns[leaf] & (1<<chart)
    return tuple(changed)

@lru_cache(maxsize=24000)
def replay(columns):
    h = first_cover(columns)
    m = len(columns)
    source = rows_of(columns)
    trace = normalize(source, m, K, len(h))
    assert tuple(trace[0]) == source
    for step, nxt in zip(trace,trace[1:]):
        assert sum((x^y).bit_count() for x,y in zip(step,nxt)) == 1
        assert all(r & 1 for r in nxt) and nxt[0] | nxt[1] | nxt[2] == (1<<(m+1))-1
    single = next(i for i,s in enumerate(trace) if sum(r.bit_count()-1 for r in s)==m)
    predicted = tuple(1 << next(a for a in h if s & (1<<a)) for s in columns)
    assert tuple(trace[single]) == rows_of(predicted)
    assert single == sum(c.bit_count()-1 for c in columns)
    if m>len(h):
        canon = tuple(1 << (v if v < len(h) else 0) for v in range(m))
        assert tuple(trace[-1]) == rows_of(canon)
    return tuple(trace[single]),tuple(trace[-1]),single

def record(row,m):
    ambient=tuple(range(m+1))
    view=tuple(v for v in ambient if row & (1<<v))
    grades=push((-1,)+(0,)*m,ambient,view,(1,)+(2,)*m)
    return dict(leaves=list(view[1:]),pin=int(grades[0]))

def worked(columns, cases, b):
    out={}
    for key,(leaf,a) in cases.items():
        cut=drop(columns,leaf,a)
        snap,end,steps=replay(cut)
        out[key]=dict(cut=list(cut),h=first_cover(cut),before=record(rows_of(cut)[b],len(cut)),
                      contraction=record(snap[b],len(cut)),terminal=record(end[b],len(cut)),steps=steps)
    return out

def census():
    counts=Counter()
    for m in range(2,6):
        for cols in product(range(1,1<<K),repeat=m):
            counts["states"]+=1
            h=first_cover(cols)
            if len(h)<2 or m<=len(h):
                continue
            a,b=h[:2]
            initial,final,_=replay(cols)
            first=[i for i,s in enumerate(cols) if s&(1<<a) and s&(1<<b)]
            second=[i for i,s in enumerate(cols) if s&(1<<a) and not s&(1<<b)
                    and any(s & (1<<d) for d in h[2:])]
            def arm(i,actor):
                new=drop(cols,i,actor)
                assert first_cover(new)==h and rows_of(new)[b]==rows_of(cols)[b]
                snap,end,n=replay(new)
                assert end==final
                return snap[b],n
            for i in first:
                old,n=arm(i,a)
                assert old==initial[b] | (1<<(i+1)) and old!=initial[b]
                for c in labels:
                    if c not in (a,b) and cols[i] & (1<<c):
                        alt,nn=arm(i,c)
                        assert alt==initial[b] and n==nn
                        counts["same_leaf_other_actor"]+=1
                for j in second:
                    alt,nn=arm(j,a)
                    assert alt==initial[b] and n==nn
                    counts["fixed_actor_different_counts"]+=1
                for j in first:
                    if j>i and cols[i]==cols[j]:
                        alt,nn=arm(j,a)
                        assert alt==initial[b] | (1<<(j+1)) and n==nn
                        assert old!=alt and old.bit_count()==alt.bit_count()
                        counts["twins_same_work"]+=1
    return dict(counts)

fixed=(1,2,4,7,5)
twins=(1,2,4,7,7)
fixed_out=worked(fixed,{"drop_S_at_A":(3,0),"drop_T_at_A":(4,0),"drop_S_at_C":(3,2)},1)
twin_out=worked(twins,{"drop_S_at_A":(3,0),"drop_twin_at_A":(4,0)},1)
assert fixed_out["drop_S_at_A"]["contraction"]==dict(leaves=[2,4],pin=7)
assert fixed_out["drop_T_at_A"]["contraction"]==dict(leaves=[2],pin=9)
assert fixed_out["drop_S_at_C"]["contraction"]==dict(leaves=[2],pin=9)
assert twin_out["drop_twin_at_A"]["contraction"]==dict(leaves=[2,5],pin=7)
def work(rows):
    return [4*(u^v).bit_count() for u,v in combinations(rows,2)]
assert work(rows_of(tuple(twin_out["drop_S_at_A"]["cut"])))==work(rows_of(tuple(twin_out["drop_twin_at_A"]["cut"])))
# Reindexing the three charts reruns the historical order; map the ordered roles back.
ordered_roles=[]
for order in permutations(labels):
    cols=tuple(sum(1<<i for i,c in enumerate(order) if mask & (1<<c)) for mask in twins)
    h=first_cover(cols)
    a,b=h[:2]
    witness=worked(cols,{"cut":(3,a),"twin":(4,a)},b)
    assert witness["cut"]["contraction"]["leaves"]!=witness["twin"]["contraction"]["leaves"]
    ordered_roles.append([order[a],order[b]])
assert len(set(map(tuple,ordered_roles)))==6
# If withdrawing A's sole hit on a leaf, the old cover can disappear.
# A sharper negative: q=1 originally, but no one label hits both after the cut.
control=(1,3)
assert first_cover(control)==(0,) and first_cover(drop(control,1,0))==(0,1)
def local_cut(cols, leaf, marker, b=1):
    changed=drop(cols,leaf,0)
    h=first_cover(changed)
    path=normalize(rows_of(changed),len(cols),K,len(h))
    bit=1<<(marker+1)
    for i,(old,new) in enumerate(zip(path,path[1:]),1):
        if old[b] & bit and not new[b] & bit:
            return dict(record=record(new[b],len(cols)), step=i,
                        local_edits=sum(a[b]!=z[b] for a,z in zip(path[:i],path[1:i+1])))
    raise AssertionError("Marker retained")
local_fixed=(1,2,4,7,3,5)
local_twins=(1,2,7,3,7)
local_results={
    "fixed":[local_cut(local_fixed,i,4) for i in (3,5)],
    "twins":[local_cut(local_twins,i,3) for i in (2,4)],
    "swapped_twins":[local_cut(local_twins,i,3) for i in (4,2)],
    "adjacent_twins":[local_cut((1,2,7,7,3),i,4) for i in (2,3)],
}
for key in ("fixed","twins"):
    lo,hi=[z["record"] for z in local_results[key]]
    assert lo["pin"]+2==hi["pin"] and len(lo["leaves"])==len(hi["leaves"])+1
lo,hi=[z["record"] for z in local_results["adjacent_twins"]]
assert lo["pin"]==hi["pin"] and lo["leaves"]!=hi["leaves"]
# Bind semantic twin identities across the order permutation.
assert [z["record"]["pin"] for z in local_results["twins"]]==list(reversed([z["record"]["pin"] for z in local_results["swapped_twins"]]))
def promote_receiver(columns, cut_leaf):
    # Keep physical chart 0 as the source and physical chart 1 as the receiver.
    order=(1,0,2)
    cut=drop(columns,cut_leaf,0)
    ordered=tuple(sum(1<<i for i,c in enumerate(order) if s&(1<<c)) for s in cut)
    h=first_cover(ordered)
    assert {order[i] for i in h}==set(first_cover(cut))
    path=normalize(rows_of(ordered),len(columns),K,len(h))
    boundary=next(i for i,rows in enumerate(path) if sum(r.bit_count()-1 for r in rows)==len(columns))
    assert all(state[0]==rows_of(cut)[1] for state in path[:boundary+1])
    return dict(edits_at_receiver=0,contraction=record(path[boundary][0],len(columns)),steps=boundary)

priority={
    "fixed":[promote_receiver(local_fixed,i) for i in (3,5)],
    "twins":[promote_receiver(local_twins,i) for i in (2,4)],
}
assert all(arms[0]["contraction"]==arms[1]["contraction"] for arms in priority.values())
print(json.dumps(dict(priority=priority,local=local_results,census=census(),fixed=fixed_out,twins=twin_out,
                      chart_reindexing_roles=ordered_roles,control_covers=[first_cover(control),first_cover(drop(control,1,0))]),sort_keys=True))
