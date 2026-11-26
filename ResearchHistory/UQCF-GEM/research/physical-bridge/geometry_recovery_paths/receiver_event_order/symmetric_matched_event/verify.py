"""Independent finite geometry/role checker, with explicit witness and no producer import."""
import json
from itertools import combinations
from pathlib import Path

L=11
V=tuple((x,y) for x in range(L) for y in range(L))
A=(0,0); B=(3,3); C=(8,3)
S={(0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
   (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),(9,3),
   (9,8),(10,0),(10,1),(10,10)}
tar={(0,1):0,(0,2):12,(2,3):4,(3,4):4,(1,3):16,(3,5):16}
def typ(p,q):
    jumps=[(x-y)%L for x,y in zip(p,q)]
    a,b=(min(i,L-i) for i in jumps)
    return min(a,b),max(a,b)
def prior(p,q): return tar.get(typ(p,q),8)
def chosen(p):
    return frozenset(q for q in V if prior(p,q)==0)
expected_S = {r for r in V if typ(A,r) in {(0,0),(0,1),(0,2),(1,1)}
              or (prior(A,r)==4 and prior(B,r)!=0 and r!=B)}
assert S==expected_S and len(S)==25
S1=frozenset(S); S2=frozenset((-x%L,y) for x,y in S)
images=[]
core=set(S)
for _ in range(4):
    for f in (1,-1):
        for c,d in V:
            images.append(frozenset(((f*x+c)%L,(y+d)%L) for x,y in core))
    core={(-y%L,x) for x,y in core}
assert (len(images),len(set(images)))==(968,484)
def symmetric_difference(x,p,q): return int((p in x)!=(q in x))
def part_delta(old,new,p,q):
    return 4*(symmetric_difference(new,p,q)-symmetric_difference(old,p,q))
def report(first, expected_recipient):
    pruned=first-{A}
    def first_work(p,q): return prior(p,q)+part_delta(first,pruned,p,q)
    near=lambda p,weighted : frozenset(q for q in V if p!=q and weighted(p,q)==0)
    assert len(pruned)==24 and expected_recipient not in pruned
    assert len(near(A,first_work))==4 and any(len(near(p,first_work))!=4 for p in V)
    # All nonadjacent actor repairs must swap neighborhoods, by the separate degree/opposite proof.
    receivers=[p for p in V if chosen(p)==near(A,first_work)]
    assert receivers==[expected_recipient]
    assert all(first_work(expected_recipient,k)==4 for k in chosen(A))
    receiver=receivers[0]
    swap=lambda p : receiver if p==A else A if p==receiver else p
    expected={p:frozenset(swap(q) for q in chosen(swap(p))) for p in V}
    now=list(images)
    now.remove(first)
    now.append(pruned)
    degree=[]
    for leaf in set(now):
        altered=leaf^{receiver}
        def after(p,q): return first_work(p,q)+part_delta(leaf,altered,p,q)
        if near(receiver,after)!=expected[receiver] or min(after(receiver,p) for p in V if p!=receiver)!=0:
            continue
        assert all(near(p,after)==expected[p] for p in V)
        failures=[]
        for center, my_neighbors in expected.items():
            six={pair:after(*pair) for pair in combinations(sorted(my_neighbors),2)}
            high=max(six.values())
            largest={p for p,v in six.items() if v==high}
            target={p for p in six if typ(*(swap(k) for k in p))==(0,2)}
            if largest!=target:
                failures.append((center,high,largest))
        if failures:
            assert ((1,0),20,{((2,0),receiver)}) in failures
        degree.append((leaf==pruned,receiver not in leaf,len(failures)))
    assert len(degree)==4 and all(item[1] for item in degree)
    assert [same for same,gain,bad in degree if bad==0]==[True]
    def gain_only(p,q): return prior(p,q)+part_delta(first,first|{receiver},p,q)
    assert any(len(near(p,gain_only))!=4 for p in V)
    return {"label":receiver[0]+L*receiver[1],"row_candidates":len(degree),
            "opposite_rejections":sum(bad!=0 for _,_,bad in degree),"sole_same_leaf_gain":True,
            "fixed_B_pin_offset":-2 if receiver==B else 0}
res=[report(S1,B),report(S2,C)]
if len(__import__('sys').argv)>1:
    receipt=json.loads(Path(__import__('sys').argv[1]).read_text())
    for item, received in zip(res,receipt["same_prior_two_events"],strict=True):
        assert (item["label"],item["opposite_rejections"],item["fixed_B_pin_offset"]) == (
            received["actor"],received["rejected_after_degree"]["opposites_ambiguous"],received["B_Pin_change"])
print(json.dumps({"same_state_two_events":res, "controls":"source only; gain alone; three wrong leaf gains per arm", "status":"pass"},sort_keys=True))
