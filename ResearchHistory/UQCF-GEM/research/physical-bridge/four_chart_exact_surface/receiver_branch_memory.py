"""Check a receiver-owned state and its later use by the pinned v16.53 normalizer."""
from collections import Counter
from multiprocessing import Pool
from itertools import permutations, groupby
import json
from random import Random
import sys

import initiating_gain as prior

producer, verifier = prior.producer, prior.verifier
alphabet, peers = prior.alphabet, prior.peers
support = prior.raw_support
fork = ((), (), ())
receiver_tree = (fork, fork, fork)


def fixture(marker, wide, grand, order, filled):
    old_tree, old_sites, old, _ = prior.prepare((marker,), wide, order, filled)
    old_nodes = producer.layout(old_tree)
    names = {site: name for name,site in old_sites.items()}
    sites, holdings = {}, []

    def build(name, held, children):
        sites[name] = len(holdings)
        holdings.append(held)
        return tuple(make(child) for child in children)

    def make(name):
        if len(name) in (2, 3) and name[0] in peers:
            peer, branch = name[0], int(name[1])
            if peer != wide:
                held = {2}
            elif branch == grand:
                held = {0,1,2} if len(name) == 2 else {int(name[2])}
            else:
                narrow = [i for i in range(3) if i != grand]
                held = {narrow.index(branch)}
            children = [name + str(i) for i in order[name]] if len(name) == 2 else []
            return build(name, held, children)
        site = old_sites[name]
        return build(name, support(old,site), [names[v] for v in old_nodes[site]])

    tree = make("outer")
    raw = [sum(1 << i for i,h in enumerate(holdings) if j in h) for j in alphabet]
    return tree, sites, raw, verifier.profile_check(tree,len(alphabet),raw)


def project(raw, sites, labels):
    return [sum(1 << i for i,v in enumerate(sites) if raw[j] >> v & 1) for j in labels]


def run(marker, wide, grand, order, palette, filled):
    tree, sites, raw, q = fixture(marker, wide, grand, order, filled)
    nodes, targets, widths = producer.data(tree,q)
    w, source = sites[wide], sites["source"]
    children = nodes[w]
    region = producer.vertices(nodes,w)
    assert [p for p in peers if widths[sites[p]] == 3] == [wide]
    assert targets[w] == 2 and sorted(widths[c] for c in children) == [1,1,3]
    assert widths[sites[wide+str(grand)]] == 3
    visits = []
    def observe(frame, event, result):
        if event != "return" or frame.f_code is not producer.normalize.__code__:
            return
        args = frame.f_locals
        if args["t"] != receiver_tree or args["q"][0] != 2:
            return
        # Pull the returned path's first index and label coordinates through the
        # four-child call and all ancestral recursive embeddings into the full path.
        f = frame.f_back
        labels = list(range(args["k"]))
        start = 0
        while f is not None and "vs" in f.f_locals and "labels" in f.f_locals:
            parent = f.f_locals
            labels = [parent["labels"][j] for j in labels]
            start += len(parent["path"])-1
            while f is not None and f.f_code is not producer.normalize.__code__:
                f = f.f_back
            if f is not None:
                f = f.f_back
        visits.append((start,labels,result,args["q"]))
    original = sys.getprofile()
    sys.setprofile(observe)
    try:
        path = producer.normalize(raw,tree,7,q,palette)
    finally:
        sys.setprofile(original)
    canonical = verifier.model(tree,q,7)[2]
    end = [canonical[palette.index(j)] for j in alphabet]
    verifier.path_check(tree,7,q,path,raw,end)
    assert len(visits) == 2
    for begin,labels,local_path,_ in visits:
        assert [project(s,region,labels) for s in path[begin:begin+len(local_path)]] == local_path
    begin,labels,local,local_q = visits[1]
    assert labels == [3,2,marker]
    # The observation uses only changes at the receiver root and marker labels.
    word = [tuple(sorted(support(s,w))) for s in path]
    cut = next(i for i,row in enumerate(word) if 3 in row and len(row) == 3)
    assert [r for r,_ in groupby(word[:cut+1])] == [(0,1,2),(0,1,2,3),tuple(sorted((2,3,marker)))]
    at_cut = [sorted(support(path[cut],c)) for c in children]
    assert cut <= begin
    assert all([sorted(support(state,c)) for c in children] == at_cut for state in path[cut:begin+1])
    moves = prior.edits(path)
    gain = (3,source,True)
    assert (gain in moves[:cut]) == (not filled)
    delivery = None
    if not filled:
        gained = moves.index(gain) + 1
        branch = sites[wide+str(grand)]
        tip_names = [wide+str(grand)+str(i) for i in range(3)]
        branch_sites = [branch]+[sites[name] for name in tip_names]
        removed = 1-marker
        leaf, = [v for v in branch_sites[1:] if removed in support(path[gained],v)]
        active = [w,branch,leaf]
        release = moves.index((removed,source,False),gained)
        within = [(j,v,up) for j,v,up in moves[gained:release] if v in region]
        assert within == [(3,v,True) for v in active]+[(removed,v,False) for v in reversed(active)]
        prior_to = project(path[gained],branch_sites,alphabet)
        after = project(path[cut],branch_sites,alphabet)
        named_narrow = [c for c in children if c != branch]
        assert all(support(path[gained-1],c) == support(path[cut],c) for c in named_narrow)
        delivery = dict(branch_sites=branch_sites, tip_names=tip_names, physical_before=prior_to,
                        physical_after=after, raw_window=path[gained-1:release+2])
        assert moves.index(gain) < moves.index((3,w,True)) < cut
        assert all(not(s[3] >> sites[p] & 1) for s in path[:cut+1] for p in peers if p != wide)
    assert sum(3 in row for row in at_cut) == (2 if filled else 1)
    assert (len(local) == 1) == filled
    return dict(tree=tree,sites=sites,start=raw,profile=q,end=end,word=[r for r,_ in groupby(word)],
                cut=cut,children=at_cut,visit=begin,labels=labels,local=local,local_q=local_q,
                source_gain=None if filled else moves.index(gain)+1,path_length=len(moves),delivery=delivery,
                trace=[path[cut],path[begin],path[begin+len(local)-1]])


def frozen_orders(arms):
    # Permute all three top-level child blocks after capturing the receiver.
    # The 13 physical sites retain their identities and holdings.
    q = arms[0]["local_q"]
    nodes, _, widths = producer.data(receiver_tree,q)
    children = nodes[0]
    narrow = {c for c in children if widths[c] == 1}
    results = []
    for arm in arms:
        raw = arm["local"][0]
        # Local labels in the second visit are physically (3,2,marker).
        owners = {c for c in narrow if raw[2] >> c & 1}
        assert len(owners) == int(arm["source_gain"] is not None)
        for order in permutations(children):
            sites = [0]+[v for c in order for v in producer.vertices(nodes,c)]
            start = project(raw,sites,range(3))
            profile = verifier.profile_check(receiver_tree,3,start)
            path = producer.normalize(start,receiver_tree,3,profile)
            end = verifier.model(receiver_tree,profile,3)[2]
            verifier.path_check(receiver_tree,3,profile,path,start,end)
            changes = [(j,sites[v],add) for j,v,add in prior.edits(path) if sites[v] in narrow]
            withdraw = [v for j,v,add in changes if j == 2 and not add]
            assert sorted(withdraw) == sorted(owners)
            assert not any(j == 2 and add for j,v,add in changes)
            results.append((len(path)-1,withdraw))
    return results


def matched(inputs, save=False):
    marker, wide, grand, order, palette = inputs
    arms = [run(marker,wide,grand,order,palette,filled) for filled in (False,True)]
    a,b = arms
    assert a["sites"] == b["sites"] and a["tree"] == b["tree"]
    source = a["sites"]["source"]
    assert [x^y for x,y in zip(a["start"],b["start"])] == [0,0,0,1<<source,0,0,0]
    for key in ("profile","end","word","local_q","labels"):
        assert a[key] == b[key]
    assert a["local"][-1] == b["local"][-1]
    q = a["local_q"]
    nodes,_,widths = producer.data(receiver_tree,q)
    g, = [c for c in nodes[0] if widths[c] == 3]
    narrow = [c for c in nodes[0] if c != g]
    mask = sum(1<<v for v in producer.vertices(nodes,g))
    endpoints = verifier.model(receiver_tree,q,3)[2]
    matrix = {}
    for i,wide_arm in enumerate(arms):
        for j,narrow_arm in enumerate(arms):
            raw = [(l & mask) | (r & ~mask)
                   for l,r in zip(wide_arm["local"][0],narrow_arm["local"][0])]
            assert verifier.profile_check(receiver_tree,3,raw) == q
            path = producer.normalize(raw,receiver_tree,3,q)
            verifier.path_check(receiver_tree,3,q,path,raw,endpoints)
            if i == j:
                assert path == arms[i]["local"]
            changes = prior.edits(path)
            within = [v for label,v,add in changes if mask>>v & 1]
            narrow_moves = [v for label,v,add in changes if not(mask>>v & 1)]
            gains = [v for label,v,add in changes if label == 0 and add and v in narrow]
            assert gains == ([narrow[0]] if j == 0 else [])
            drops = [v for label,v,add in changes if label == 2 and not add and v in narrow]
            assert drops == ([narrow[1]] if j == 0 else [])
            assert bool(within) == (i == 0) and bool(narrow_moves) == (j == 0)
            matrix[str(i)+str(j)] = [len(within),len(narrow_moves),len(gains)]
    reorder = frozen_orders(arms)
    if save:
        return {"marker":marker,"wide":wide,"grand":grand,"order":order,"palette":palette,
                "arms":arms,"hybrids":matrix,"reordered":reorder}
    info = (a["sites"]["evidence"], [arm["start"] for arm in arms], a["profile"],a["end"])
    return (len(a["local"])-1,len(b["local"])-1),tuple(tuple(v) for v in matrix.values()),info


def configurations():
    per = list(permutations(range(3)))
    rng = Random(165327)
    sizes = {**prior.arities,**{p+str(i):3 for p in peers for i in range(3)}}
    for wide in peers:
        for grand in range(3):
            for left in per:
                for right in per:
                    order = {k:tuple(rng.sample(range(n),n)) for k,n in sizes.items()}
                    order[wide] = left
                    order[wide+str(grand)] = right
                    palette = tuple(rng.sample(alphabet,len(alphabet)))
                    for marker in (0,1):
                        yield marker,wide,grand,order,palette


def same_branch_prior(identity):
    # Capture all six enumerations per marker and match on the *whole* named
    # four-site branch immediately after the source gain, before clearance.
    records = [{},{}]
    for marker in (0,1):
        for order in permutations(range(3)):
            arm = run(marker,"A",0,{**identity,"A0":order},alphabet,False)
            d = arm["delivery"]
            before = tuple(d["physical_before"])
            after = tuple(d["physical_after"])
            assert before not in records[marker]
            records[marker][before] = (order,after)
    assert set(records[0]) == set(records[1]) and len(records[0]) == 6
    out = []
    for before,(order0,after0) in sorted(records[0].items()):
        order1,after1 = records[1][before]
        assert order0 != order1 and after0 != after1
        assert all(before[j].bit_count() == 2 for j in (0,1,2)) and before[3] == 0
        for marker,after in enumerate((after0,after1)):
            expected = list(before)
            expected[3],expected[1-marker] = before[1-marker],0
            assert tuple(expected) == after
        out.append(dict(before=before,orders=[order0,order1],after=[after0,after1]))
    return out


def main():
    identity = {**prior.identity,**{p+str(i):tuple(range(3)) for p in peers for i in range(3)}}
    examples = [matched((marker,"A",0,identity,alphabet),save=True) for marker in (0,1)]
    named = same_branch_prior(identity)
    if "--example" in sys.argv[2:]:
        print(json.dumps({"examples":examples,"matched_branch_priors":named},sort_keys=True,separators=(",",":")))
        return
    print("Two source withdrawals on an identical four-site prior:",len(named),"matched priors from 12 additional whole paths")
    for example in examples:
        print("Default marker",example["marker"])
        for arm in example["arms"]:
            print("  source gain",arm["source_gain"],"receiver cut",arm["cut"],"children",arm["children"],
                  "next visit",arm["visit"],"local edits",len(arm["local"])-1)
        print("  post-capture order changes [edit count, narrow marker withdrawal sites]",example["reordered"])
        print("  mixed states [wide edits, narrow edits, narrow root gains of 3]",example["hybrids"])
    counts = Counter()
    mixed = Counter()
    settings = list(configurations())
    with Pool(4) as pool:
        previous = None
        for row,(moves,matrix,info) in enumerate(pool.imap(matched,settings,chunksize=4)):
            if row % 2:
                site,starts,profile,end = info
                assert site == previous[0] and profile == previous[2] and end == previous[3]
                for left,right in zip(starts,previous[1]):
                    assert [a^b for a,b in zip(left,right)] == [1<<site,1<<site,0,0,0,0,0]
            previous = info
            counts[moves] += 1
            mixed[matrix] += 1
    assert counts == {(24,0):648}
    assert mixed == {((8,16,1),(8,0,0),(0,16,1),(0,0,0)):648}
    print("Matched pairs",len(settings),"whole paths",2*len(settings),"local replay paths",4*len(settings))
    print("Source gain vs prefill, next native visit edit counts",sorted(counts.items()))
    print("Hybrid matrices",sorted(mixed.items()))
    print("Fixed physical snapshots, six new child orders per arm:",12*len(settings),
          "replays; named narrow marker withdrawal exactly matches its captured owner in every replay")


if __name__ == "__main__":
    main()
