"""Test order independence at a four-child junction of the pinned v16.53 program."""
from itertools import permutations, product
from multiprocessing import Pool
from collections import Counter
from random import Random
import json
import sys

import initiating_gain as prior

producer, verifier = prior.producer, prior.verifier
support = prior.raw_support
alphabet = tuple(range(6))
branches = ("P","R","C","D")
peers = ("A","B","C")
arities = {"outside":3,"gate":3,"anchor":3,"junction":4,
           **{b:3 for b in branches}, **{b+p:2 for b in branches for p in peers}}
identity = {name:tuple(range(n)) for name,n in arities.items()}


def prepare(bit, order, wide="A", key=(1,), seed="1", four=False):
    children = {"outside":("gate","key","end5"),"gate":("anchor","e","end4"),
                "anchor":("junction","zero","end3"),"junction":branches}
    holds = {"outside":set(range(6)),"gate":set(range(5)),"anchor":set(range(4)),
             "junction":{0,1,2},"key":set(key),"e":{1,2} if bit else {2},
             "zero":{0},"end3":{3},"end4":{4},"end5":{5}}
    for b,m in zip(branches,(1,2,0,0)):
        holds[b] = {0,m}
        children[b] = tuple(b+p for p in peers)
        def fork(prefix, address, selected):
            if len(address) == len(seed):
                holds[prefix] = {m if selected and address == seed else 0}
                return
            holds[prefix] = {0,m}
            digits = "0123" if four and len(address)+1 == len(seed) else "01"
            children[prefix] = tuple(prefix+digit for digit in digits)
            for digit in digits:
                fork(prefix+digit,address+digit,selected)
        for p in peers:
            fork(b+p,"",p==wide)
    sites = {}
    def build(name):
        sites[name] = len(sites)
        if name not in children:
            return ()
        return tuple(build(children[name][i]) for i in order[name])
    tree = build("outside")
    start = [sum(1<<v for name,v in sites.items() if j in holds[name]) for j in alphabet]
    profile = verifier.profile_check(tree,len(alphabet),start)
    return tree,sites,start,profile


def projection(state,region):
    return tuple(sum(1<<i for i,v in enumerate(region) if row>>v&1) for row in state)


def run(bit, order, palette, wide="A", key=(1,), seed="1", capture=False, four=False):
    tree,sites,start,q = prepare(bit,order,wide,key,seed,four)
    nodes,targets,widths = producer.data(tree,q)
    junction = sites["junction"]
    region = producer.vertices(nodes,junction)
    names = {v:name for name,v in sites.items()}
    observed = []
    lifts = []
    fork_visits = {}
    def watch(frame,event,result):
        if event == "call" and frame.f_code is producer.lift_root_path.__code__:
            args = frame.f_locals
            if any(args["tree"]):
                lifts.append(tuple(tuple(tuple(sorted(row)) for row in step) for step in args["root_path"]))
        if event != "return" or frame.f_code is not producer.normalize.__code__:
            return
        args = frame.f_locals
        if len(args["t"]) != 4:
            return
        root = 0
        labels = list(range(args["k"]))
        begin = 0
        caller = frame.f_back
        while caller is not None and "vs" in caller.f_locals and "labels" in caller.f_locals:
            parent = caller.f_locals
            root = parent["vs"][root]
            labels = [parent["labels"][j] for j in labels]
            begin += len(parent["path"])-1
            while caller is not None and caller.f_code is not producer.normalize.__code__:
                caller = caller.f_back
            if caller is not None:
                caller = caller.f_back
        if root == junction:
            observed.append((begin,labels,result))
        elif four:
            fork_visits.setdefault(root,[]).append((begin,labels,result))
    orig = sys.getprofile()
    sys.setprofile(watch)
    try:
        path = producer.normalize(start,tree,len(alphabet),q,palette)
    finally:
        sys.setprofile(orig)
    canonical = verifier.model(tree,q,len(alphabet))[2]
    endpoint = [canonical[palette.index(j)] for j in alphabet]
    verifier.path_check(tree,len(alphabet),q,path,start,endpoint)
    (begin,labels,local), = observed
    root_plan, = lifts
    for offset,local_step in enumerate(local):
        projected = projection(path[begin+offset],region)
        assert [projected[j] for j in labels] == local_step
    first_key = next(j for j in palette if j in key)
    chosen = first_key if bit else 2
    other = 3-chosen
    assert labels == [0,chosen,other]
    roots = nodes[junction]
    assert targets[junction] == 1
    assert sorted(widths[v] for v in roots) == [1,1,2,2]
    assert all(widths[sites[b+wide]]==2 for b in ("P","R"))
    full = {0,1,2}
    # Read the all-full parent junction directly off the returned whole path.
    peak = next(i for i in range(begin,begin+len(local))
                if all(support(path[i],v)==full for v in roots))
    active = "P" if other==1 else "R"
    owner = active+wide
    at = path[peak]
    descendants = [v for v in producer.vertices(nodes,sites[active])[1:] if other in support(at,v)]
    tip, = [v for v in descendants if not nodes[v]]
    chain = [sites[owner+seed[:i]] for i in range(len(seed))]
    assert descendants == chain+[tip]
    assert tip in nodes[chain[-1]]
    assert support(at,tip) == {other}
    edits = prior.edits(path)
    stop = next(i+1 for i in range(peak,len(edits)) if edits[i] == (other,sites[active],False))
    # Stop at the end of the four-child root lift, before recursion resumes.
    planned_final = [{labels[j] for j in row} for row in root_plan[-1]]
    assert planned_final == [set(labels[:widths[v]]) for v in roots]
    finish = next(i for i in range(stop,begin+len(local))
                  if all(support(path[i],v)==row for v,row in zip(roots,planned_final)))
    inner = set(region)-{junction,*roots}
    moves = [e for e in edits[peak:finish] if e[1] in inner]
    assert moves == [(chosen,v,True) for v in descendants]+[(other,v,False) for v in reversed(descendants)]
    first_write = next(i for i in range(peak,stop) if edits[i][1] in inner)
    assert all(support(at,v)==support(path[first_write],v) for v in inner)
    assert support(path[first_write],sites[active]) == full
    assert support(path[stop],sites[owner]) == {0,chosen}
    assert all(support(path[finish],sites[b+wide])=={0,chosen} for b in ("P","R"))
    result = dict(sites=sites,start=start,profile=q,endpoint=endpoint,priority=labels,
                peak=peak,first=first_write+1,withdrawal=stop,lift_end=finish,
                local_end=begin+len(local)-1,active=active,receiver=owner,tip=names[tip],
                moves=[(j,names[v],add) for j,v,add in moves],before=list(projection(at,region)),
                proper_before=projection(path[first_write],sorted(inner)),peak_state=at,
                after=list(projection(path[finish],region)),raw=path[first_write:stop+1],
                junction_region=region,root_plan=root_plan)
    if four:
        base = chain[-1]
        tips = nodes[base]
        initial_call,second = fork_visits[base]
        again,physical,returned = second
        assert initial_call[0] < peak < finish <= again
        assert physical == [0,chosen]
        vs = [base]+tips
        entries = [projection(st,vs) for st in path[again:again+len(returned)]]
        assert [list(row[j] for j in physical) for row in entries] == returned
        assert all(projection(st,vs)==entries[0] for st in path[stop:again+1])
        lacking = [v for v in tips if chosen not in support(path[again],v)]
        gains = [v for j,v,add in edits[again:again+len(returned)-1] if j==chosen and add]
        assert set(gains) == set(lacking) == set(tips)-{tip} and len(gains)==3
        assert len(returned)==9 and returned[0]==returned[-1]
        assert all(chosen not in support(st,v) for st in path[:first_write+1] for v in vs)
        local_tree = ((),(),(),())
        local_start = returned[0]
        local_q = verifier.profile_check(local_tree,2,local_start)
        fresh = producer.normalize(local_start,local_tree,2,local_q)
        assert fresh == returned
        verifier.path_check(local_tree,2,local_q,fresh,local_start,
                            verifier.model(local_tree,local_q,2)[2])
        previous = projection(at,vs)
        # Freshly applying the same rule to the actual pre-delivery holdings
        # reproduces the local masks, with the old physical label in role 1.
        assert [previous[0],previous[other]] == local_start and previous[chosen]==0
        passive = ("R" if active=="P" else "P")+wide+seed[:-1]
        _,passive_second = fork_visits[sites[passive]]
        assert passive_second[1] == physical and passive_second[2] == returned
        result["second"] = dict(begin=again,physical=physical,pre_physical=[0,other],root=names[base],
                                tips=[names[v] for v in tips],gains=[names[v] for v in gains],
                                path=returned,profile=local_q)
    if capture:
        result["tree"] = tree
        result["order"] = order
        result["palette"] = palette
        result["local_end_state"] = path[begin+len(local)-1]
    return result


def orders(seed,four=False):
    sizes = dict(arities)
    for b,p in product(branches,peers):
        for length in range(1,len(seed)):
            for addr in product("01",repeat=length):
                sizes[b+p+"".join(addr)] = 2
    if four:
        for b,p in product(branches,peers):
            for addr in product("01",repeat=len(seed)-1):
                sizes[b+p+"".join(addr)] = 4
    return sizes


def pair(order,palette,wide="A",key=(1,),seed="1",capture=False,four=False):
    a,b = [run(bit,order,palette,wide,key,seed,capture,four) for bit in (False,True)]
    for field in ("sites","profile","endpoint","before","proper_before"):
        assert a[field] == b[field],field
    e = a["sites"]["e"]
    assert [l^r for l,r in zip(a["start"],b["start"])] == [0,1<<e,0,0,0,0]
    assert not a["start"][1]>>e&1
    if b["priority"] == [0,1,2]:
        assert [a["receiver"],b["receiver"]] == ["P"+wide,"R"+wide]
        assert a["after"] != b["after"]
    else:
        assert a["receiver"] == b["receiver"] == "P"+wide
        assert a["moves"] == b["moves"] and a["after"] == b["after"]
    return (a,b)


def basic_case(args):
    index,row_order,palette = args
    rng = Random(53041+index)
    order = {name:tuple(rng.sample(range(n),n)) for name,n in arities.items()}
    order["junction"] = row_order
    wide = peers[index%3]
    a,b = pair(order,palette,wide)
    return a["tip"][-1],b["tip"][-1]


def deep_cases():
    rng = Random(53317)
    results = []
    for depth in range(1,5):
        for digits in product("01",repeat=depth):
            seed = "".join(digits)
            if depth==4 and seed not in ("0000","0101","1010","1111"):
                continue
            sizes = orders(seed)
            chosen = rng.choice(peers)
            order = {name:tuple(rng.sample(range(n),n)) for name,n in sizes.items()}
            palette = tuple(rng.sample(alphabet,len(alphabet)))
            a,b = pair(order,palette,chosen,seed=seed)
            assert len(a["moves"]) == len(b["moves"]) == 2*(depth+1)
            # Flip only the final binary traversal in both candidate branches.
            alternate = dict(order)
            for branch in ("P","R"):
                leaf_parent = branch+chosen+seed[:-1]
                alternate[leaf_parent] = order[leaf_parent][::-1]
            c,d = pair(alternate,palette,chosen,seed=seed)
            for orig,swapped in ((a,c),(b,d)):
                assert orig["receiver"] == swapped["receiver"]
                assert orig["tip"][:-1] == swapped["tip"][:-1]
                assert orig["tip"][-1] != swapped["tip"][-1]
            results.append((depth,len(a["sites"]),len(a["moves"])))
    return Counter(results)


def four_case(case):
    rng = Random(53074+case[0])
    order = {name:tuple(rng.sample(range(n),n)) for name,n in orders("1",True).items()}
    slot_order,tip_order = case[1]
    order.update(junction=slot_order, PA=tip_order, RA=tip_order[::-1])
    a,b = pair(order,tuple(rng.sample(alphabet,6)),four=True)
    return len(a["second"]["gains"]),len(b["second"]["gains"])


def isolated_orders(examples):
    fork = ((),(),(),())
    count = 0
    for example in examples:
        source = example["second"]["path"][0]
        for perm in permutations(range(1,5)):
            for ranks in ((0,1),(1,0)):
                start = list(projection(source,(0,)+perm))
                target = verifier.profile_check(fork,2,start)
                path = producer.normalize(start,fork,2,target,ranks)
                canonical = verifier.model(fork,target,2)[2]
                verifier.path_check(fork,2,target,path,start,[canonical[ranks.index(j)] for j in (0,1)])
                peak = next(i for i,s in enumerate(path) if s == [31,31])
                missing = {i for i in range(1,5) if not start[1]>>i&1}
                gains = [v for j,v,add in prior.edits(path[:peak+1]) if j==1 and add]
                assert set(gains)==missing and len(gains)==3
                count += 1
    return count


def compact_rule():
    for palette in permutations(alphabet):
        for held in ((2,), (1,2)):
            # Independent reduction at each unique overlapping pair. All other
            # pairs at that junction have empty intersection by construction.
            ordered = list(palette)
            for n,signal in ((5,(1,)),(4,held),(3,(0,))):
                inside = [j for j in ordered if j<n]
                pivot = next(j for j in inside if j in signal)
                ordered = [pivot]+[j for j in inside if j!=pivot]
            assert ordered == ([0,2,1] if len(held)==1 else [0,1,2])
    for perm in permutations((0,1,2,3)):
        widths = [(2,2,1,1)[i] for i in perm]
        for palette in ([0,1,2],[0,2,1]):
            assert producer.palettes(palette,widths,1) == [palette[:w] for w in widths]


def main():
    compact_rule()
    example = pair(identity,alphabet,capture=True)
    order4 = {name:tuple(range(n)) for name,n in orders("1",True).items()}
    four_example = pair(order4,alphabet,capture=True,four=True)
    if "--example" in sys.argv:
        print(json.dumps(dict(binary=example,four=four_example),sort_keys=True,separators=(",",":")))
        return
    for a in example:
        print("Example",a["priority"],a["receiver"],a["moves"],"all-full state",a["peak"],
              "source withdrawal",a["withdrawal"])
    # All junction traversals crossed with all relative orders of the three
    # active labels. The three exterior labels are interleaved reproducibly.
    cases = []
    rng = Random(5344)
    for row_order,active in product(permutations(range(4)),permutations(range(3))):
        rest = rng.sample([3,4,5],3)
        occupied = set(rng.sample(range(6),3))
        ix,iy = iter(active),iter(rest)
        palette = tuple(next(ix) if i in occupied else next(iy) for i in range(6))
        cases.append((len(cases),row_order,palette))
    with Pool(4) as pool:
        tips = Counter(pool.imap(basic_case,cases,chunksize=2))
    print("All 24 junction orders x 6 active label orders:",len(cases),"pairs")
    print("Terminal tip digits, no fixed named tip:",sorted(tips.items()))
    # Reorder the three upper forks independently, including the one that reads
    # the two labels at the evidence leaf. All local scan orders are covered.
    parent_count = 0
    for top,mid,low in product(permutations(range(3)),repeat=3):
        pair({**identity,"outside":top,"gate":mid,"anchor":low},alphabet)
        parent_count += 1
    print("Three independent upper fork orders:",parent_count,"pairs")
    print("Recursive receiver test: (depth, whole-tree sites, proper edits) and seed count",sorted(deep_cases().items()))
    cases = enumerate(product(permutations(range(4)),repeat=2))
    with Pool(4) as pool:
        follow = Counter(pool.imap(four_case,cases,chunksize=3))
    assert follow == {(3,3):576}
    print("Four-tip receivers, 24 junction x 24 receiving-fork orders, subsequent marker gains",sorted(follow.items()))
    print("Isolated frozen receiver: 24 leaf orders x 2 label orders x 2 arms:",isolated_orders(four_example))
    print("Compact priority: 720 external label orders in each arm, 24 junction traversals for each derived priority")
    # With a singleton 2 as key the extra incidence is silent. A tied upper
    # key restores the genuine dependence on the externally supplied order.
    for key in ((2,),(1,2)):
        counts = Counter()
        for order in permutations(range(3)):
            a,b = pair(identity,tuple(order)+(3,4,5),key=key)
            counts[a["receiver"],b["receiver"]] += 1
        print("Key",key,"receiver pairs",sorted(counts.items()))


if __name__ == "__main__":
    main()
