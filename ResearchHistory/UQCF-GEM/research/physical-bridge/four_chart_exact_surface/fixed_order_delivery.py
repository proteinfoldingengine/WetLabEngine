"""Replay fixed-order delivery with the historical v16.53 producer and verifier."""
import json
import sys
from itertools import combinations, permutations, groupby, product
from collections import Counter
from multiprocessing import Pool
from random import Random

import initiating_gain as prior

producer, verifier = prior.producer, prior.verifier
support = prior.raw_support
labels = tuple(range(5))
peers = ("A","B","C")
junction_children = ("J","S","K","L")


def peer_name(branch, peer):
    return peer if branch == "S" else branch+peer


arities = {"outer":3, "Q":4, **{v:3 for v in junction_children},
           **{peer_name(v,p):3 for v in junction_children for p in peers}}
identity = {name:tuple(range(n)) for name,n in arities.items()}


def prepare(evidence, wide, order, condition="evidence"):
    # Construction uses fixed physical labels. Palette and traversal are independent inputs.
    holdings = {"outer":set(labels),"Q":set(range(4)),"e":set(evidence or ()),"d":{4}}
    children = {"outer":("Q","e","d"),"Q":junction_children}
    for name, missing in zip(junction_children,(0,3,1,2)):
        holdings[name] = set(range(4))-{missing}
        branch_peers = tuple(peer_name(name,p) for p in peers)
        children[name] = branch_peers
        original = sorted(holdings[name])
        for p,peer in zip(peers,branch_peers):
            holdings[peer] = set(original)
            tips = tuple(peer+str(i) for i in range(3))
            children[peer] = tips
            for i,tip in enumerate(tips):
                holdings[tip] = {original[i if p == wide else 0]}
    if condition in ("reduce","alt"):
        holdings[peer_name("L",wide)+"2"].add(1 if condition == "reduce" else 0)
    elif condition == "neutral":
        other = next(p for p in peers if p != wide)
        holdings[peer_name("L",other)+"2"].add(1)
    else:
        assert condition in ("evidence","base")
    sites = {}
    def build(name):
        sites[name] = len(sites)
        if name not in children:
            return ()
        return tuple(build(children[name][i]) for i in order[name])
    tree = build("outer" if condition == "evidence" else "Q")
    k = len(holdings["outer" if condition == "evidence" else "Q"])
    start = [sum(1<<v for name,v in sites.items() if j in holdings[name]) for j in range(k)]
    return tree, sites, start, verifier.profile_check(tree,k,start)


def project(state,sites):
    return tuple(sum(1<<i for i,v in enumerate(sites) if row>>v & 1) for row in state)


def run(evidence,wide,order,palette=labels,condition="evidence"):
    tree, sites, start, q = prepare(evidence,wide,order,condition)
    k = len(start)
    # Observe original recursive calls without injecting any edit. Map every
    # captured result back onto the complete path to check its coordinates.
    local_calls = []
    def observe(frame,event,result):
        if event != "return" or frame.f_code is not producer.normalize.__code__:
            return
        args = frame.f_locals
        if args["t"] != ((),(),()) or args["q"] != [3]:
            return
        local_sites = list(range(4))
        local_labels = list(range(args["k"]))
        begin = 0
        caller = frame.f_back
        while caller is not None and "vs" in caller.f_locals and "labels" in caller.f_locals:
            parent = caller.f_locals
            local_sites = [parent["vs"][i] for i in local_sites]
            local_labels = [parent["labels"][j] for j in local_labels]
            begin += len(parent["path"])-1
            while caller is not None and caller.f_code is not producer.normalize.__code__:
                caller = caller.f_back
            if caller is not None:
                caller = caller.f_back
        if local_sites[0] == sites[wide]:
            local_calls.append((local_sites,local_labels,begin,result))

    old = sys.getprofile()
    sys.setprofile(observe)
    try:
        # The primary matched experiment uses the historical default order.
        path = producer.normalize(start,tree,k,q,None if tuple(palette) == tuple(range(k)) else palette)
    finally:
        sys.setprofile(old)
    canonical = verifier.model(tree,q,k)[2]
    endpoint = [canonical[palette.index(j)] for j in range(k)]
    verifier.path_check(tree,k,q,path,start,endpoint)
    nodes, targets, widths = producer.data(tree,q)
    s,w = sites["S"],sites[wide]
    reduced = condition in ("reduce","alt")
    if condition != "evidence":
        held = sorted(support(path[-1],w))
        raw = project(path[-1],[w]+nodes[w])
        local_start = [raw[j] for j in held]
        fork = ((),(),())
        local_profile = verifier.profile_check(fork,len(held),local_start)
        replay = producer.normalize(local_start,fork,len(held),local_profile)
        verifier.path_check(fork,len(held),local_profile,replay,local_start,
                            verifier.model(fork,local_profile,len(held))[2])
        assert replay == [local_start]
    q_widths = [widths[c] for c in nodes[sites["Q"]]]
    assert targets[sites["Q"]] == 2
    assert sorted(q_widths) == ([2,3,3,3] if reduced else [3,3,3,3])
    assert [name for name in peers if widths[sites[name]] == 3] == [wide]
    edits = prior.edits(path)
    priority = list(palette)
    if condition == "evidence":
        anchor = next(j for j in palette if j in evidence)
        priority = [anchor]+[j for j in palette if j < 4 and j != anchor]
    assert len(local_calls) == 2
    for vs,ls,begin,returned in local_calls:
        projection = [project(st,vs) for st in path[begin:begin+len(returned)]]
        assert [list(row[j] for j in ls) for row in projection] == returned
    vs,ls,begin,returned = local_calls[-1]
    visits = dict(priority=ls,begin=begin,edits=len(returned)-1,local_path=returned)
    # Audit all four children. A label missing before expansion is the unique
    # spare if the subsequent withdrawal is active in the proper descendants.
    event_map = {}
    target_rows = producer.palettes(priority,q_widths,2)
    for pos,root in enumerate(nodes[sites["Q"]]):
        missing, = set(range(4))-support(start,root)
        if reduced and root == sites["L"]:
            # This branch has two canonical withdrawals. The permutation result
            # applies only to the four equal-width runs.
            continue
        withdrawn, = set(range(4))-set(target_rows[pos])
        if not reduced:
            assert withdrawn == priority[3-pos]
        arrival = edits.index((missing,root,True))
        leave = next(i for i in range(arrival+1,len(edits)) if edits[i][1:] == (root,False))
        assert edits[leave][0] == withdrawn
        descendants = producer.vertices(nodes,root)[1:]
        occupied = [v for v in descendants if withdrawn in support(path[arrival+1],v)]
        actual = [e for e in edits[arrival+1:leave] if e[1] in descendants]
        assert actual == ([(missing,v,True) for v in occupied]+
                          [(withdrawn,v,False) for v in reversed(occupied)])
        assert bool(occupied) == (missing != withdrawn)
        event_map[missing] = dict(removed=withdrawn,sites=occupied,root=root,
                                  at_gain=project(path[arrival+1],[root]+descendants))
    if not reduced:
        assert {e["removed"] for e in event_map.values()} == set(event_map)
    gain = edits.index((3,s,True))
    release = next(i for i,e in enumerate(edits) if i>gain and e[1:] == (s,False))
    gone = edits[release][0]
    region = producer.vertices(nodes,s)
    tip_sites = [sites[wide+str(i)] for i in range(3)]
    after_gain = path[gain+1]
    used = [v for v in region[1:] if gone in support(after_gain,v)]
    moves = [(j,v,add) for j,v,add in edits[gain+1:release] if v in region]
    expected = [(3,v,True) for v in used]+[(gone,v,False) for v in reversed(used)]
    assert moves == expected
    tips = [v for v in tip_sites if v in used]
    named = {v:name for name,v in sites.items()}
    prior_state = project(after_gain,region)
    first = next(i for i in range(gain+1,release+1) if edits[i][1] in region)
    assert project(path[first],region) == prior_state
    return dict(tree=tree, sites=sites, source_end=project(endpoint,region),
                receiver_end=project(endpoint,[w]+tip_sites), q_widths=q_widths,
                target_rows=target_rows, start=start, q=q, endpoint=endpoint, gain=gain+1,
                release=release+1, gone=gone, visit=visits, event_map=event_map,
                priority=priority, used=[named[v] for v in used],
                leaves=[named[v] for v in tips],moves=[(j,named[v],add) for j,v,add in moves],
                prior=prior_state,source_region=[named[v] for v in region],
                source_prefix=[list(row) for row,_ in groupby(project(st,region) for st in path[:first+1])],
                resulting=project(path[release+1],region),raw=path[first:release+2],
                gain_window=[path[gain],after_gain],frames=len(path),local_targets=targets[sites["Q"]],
                receiver_sites=[w]+tip_sites, receiver_cut=project(path[release+1],[w]+tip_sites))


def admissible_tables(widths):
    # Independent finite enumeration in the physical default label order.
    palette = tuple(range(4))
    admitted = []
    for rows in product(*(combinations(palette,width) for width in widths)):
        if set.intersection(*(set(row) for row in rows)):
            continue
        if any(all(set(pair).intersection(row) for row in rows)
               for pair in combinations(palette,2)):
            admitted.append(rows)
    best = min(admitted,key=lambda rows:tuple(j not in row for row in rows for j in palette))
    return len(admitted),[list(row) for row in best],sorted({row[2] for row in admitted})


def common_prior(left,right):
    for key in ("tree","sites","source_region","prior","source_prefix"):
        assert left[key] == right[key],key
    assert left["resulting"] != right["resulting"]
    assert left["receiver_cut"] != right["receiver_cut"]
    assert left["leaves"] != right["leaves"]


def structural(inputs,examples=False):
    wide,order = inputs
    arms = {condition:run((),wide,order,tuple(range(4)),condition)
            for condition in ("base","reduce","alt","neutral")}
    a,b = arms["base"],arms["reduce"]
    common_prior(a,b)
    tip = a["sites"][peer_name("L",wide)+"2"]
    assert [u^v for u,v in zip(a["start"],b["start"])] == [0,1<<tip,0,0]
    assert not a["start"][1] >> tip & 1 and b["start"][1] >> tip & 1
    internal = [v for v,cs in enumerate(producer.layout(a["tree"])) if cs]
    diffs = [(internal[i],x,y) for i,(x,y) in enumerate(zip(a["q"],b["q"])) if x!=y]
    assert diffs == [(a["sites"][peer_name("L",wide)],3,2)]
    assert a["priority"] == b["priority"] == [0,1,2,3]
    assert [a["gone"],b["gone"]] == [1,2]
    assert [a["visit"]["edits"],b["visit"]["edits"]] == [4,0]
    for arm in (a,b):
        assert arm["used"] == [wide,arm["leaves"][0]]
        gone = arm["gone"]
        assert arm["receiver_end"][gone] == 0 and arm["receiver_end"][3] & 1
        for j in {0,1,2,3}-{gone}:
            assert arm["receiver_end"][j] & 1
    for original,control in [(a,arms["neutral"]),(b,arms["alt"])]:
        for key in ("q","q_widths","priority","source_prefix","resulting","visit","endpoint"):
            # Whole-tree offsets may change even when the local call is identical.
            if key == "visit":
                assert original[key]["local_path"] == control[key]["local_path"]
                assert original[key]["priority"] == control[key]["priority"]
            else:
                assert original[key] == control[key],key
    return arms if examples else (a["leaves"][0],b["leaves"][0])


def equal_profile(inputs,examples=False):
    wide,order = inputs
    a,b = [run((marker,),wide,order) for marker in (0,3)]
    common_prior(a,b)
    e = a["sites"]["e"]
    assert [u^v for u,v in zip(a["start"],b["start"])] == [1<<e,0,0,1<<e,0]
    assert a["q"] == b["q"] and a["endpoint"] == b["endpoint"]
    assert [a["priority"],b["priority"]] == [[0,1,2,3],[3,0,1,2]]
    assert [a["gone"],b["gone"]] == [2,1]
    assert [a["visit"]["edits"],b["visit"]["edits"]] == [0,4]
    return (a,b) if examples else (a["leaves"][0],b["leaves"][0])


def configurations(kind):
    rng = Random(531313)
    for wide in peers:
        for target in permutations(range(3)):
            for source_order in permutations(range(3)):
                for swapped in (False,True):
                    order = {name:tuple(rng.sample(range(n),n)) for name,n in arities.items()}
                    if kind == "structural":
                        order["Q"] = (2,0,1,3) if swapped else (0,2,1,3)
                    else:
                        order["Q"] = (2,1,0,3) if swapped else (0,1,2,3)
                    order["S"] = source_order
                    order[wide] = target
                    yield wide,order


def placement_census():
    rows = []
    for order in permutations(range(4)):
        fixed = {**identity,"Q":order}
        a,b = [run((),"A",fixed,tuple(range(4)),c) for c in ("base","reduce")]
        assert a["prior"] == b["prior"] and a["source_prefix"] == b["source_prefix"]
        branch_changes = []
        for missing,changed in b["event_map"].items():
            original = a["event_map"][missing]
            assert original["at_gain"] == changed["at_gain"]
            if original["removed"] != changed["removed"]:
                branch_changes.append((missing,bool(original["sites"]),bool(changed["sites"])))
        rows.append((order,a["gone"],b["gone"],a["used"],b["used"],branch_changes))
    return rows


def main():
    order = {**identity,"Q":(0,2,1,3)}
    samples = structural(("A",order),True)
    companion = equal_profile(("A",identity),True)
    tables = [admissible_tables(samples[key]["q_widths"]) for key in ("base","reduce")]
    for key,table,count in zip(("base","reduce"),tables,(24,108)):
        assert samples[key]["target_rows"] == table[1]
        assert table[0] == count and len(table[2]) == 4
    census = placement_census()
    active_pairs = sum(a!=b and bool(left) and bool(right) for _,a,b,left,right,_ in census)
    any_branch = sum(any(old and new for _,old,new in row[-1]) for row in census)
    assert (active_pairs,any_branch) == (2,13)
    if "--example" in sys.argv:
        print(json.dumps(dict(structural=samples,equal_profile=companion,admissible=tables,placements=census),
                         sort_keys=True,separators=(",",":")))
        return
    for key,row in samples.items():
        print(key,"widths",row["q_widths"],"remove",row["gone"],"write",row["leaves"],
              "later edits",row["visit"]["edits"],"receiver endpoint masks",row["receiver_end"])
    for key,row in zip(("evidence 0","evidence 3"),companion):
        print(key,"remove",row["gone"],"write",row["leaves"],"later edits",row["visit"]["edits"])
    print("Admissible target tables and positional minima",tables)
    print("All 24 junction orders, observed withdrawal pairs",
          sorted(Counter((a,b) for order,a,b,left,right,changes in census).items()))
    print("Two different leaf writes",active_pairs)
    print("All 72 non-perturbed branches, counts for changed withdrawals by active clearance in both arms",
          sorted(Counter((old,new) for row in census for _,old,new in row[-1]).items()))
    print("Junction orders with at least one other branch actively writing two different roles",
          any_branch)
    for kind,fn in (("structural",structural),("equal profile",equal_profile)):
        with Pool(4) as pool:
            pairs = Counter(pool.imap(fn,configurations(kind),chunksize=3))
        assert sum(pairs.values()) == 216
        assert len(pairs) == 18 and set(pairs.values()) == {12}
        print(kind,"216 matched pairs;",4*216 if kind=="structural" else 2*216,
              "verified whole paths including controls; 18 ordered recipient-leaf pairs each realized 12 times")


if __name__ == "__main__":
    main()
