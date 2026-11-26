"""Test endogenous junction pruning and a live parent-admission gate."""
import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from historical import History, last_root_move, local, move, positions
from intervention import continuing, controls


def counts(c):
    return [list(k) + [n] for k, n in sorted(c.items())]


def put(state, chart, *sites):
    for site in sites:
        state[chart] |= 1 << site


def child_tail(lib, tree, site, state):
    """Use the original child call in ordered physical labels, extracting only this subtree."""
    p = lib.p
    nodes = p.layout(tree)
    verts = p.vertices(nodes, site)
    labels = [j for j, m in enumerate(state) if m & (1 << site)]
    raw = [sum(1 << a for a, v in enumerate(verts) if state[j] & (1 << v)) for j in labels]
    region = sum(1 << v for v in verts)
    path = p.normalize(raw, p.B, len(labels), [2])
    out = [state]
    for row in path[1:]:
        nxt = list(state)
        for j, m in zip(labels, row):
            nxt[j] = (state[j] & ~region) | sum(1 << v for a, v in enumerate(verts) if m & (1 << a))
        out.append(tuple(nxt))
    return tuple(out)


def originals(lib, campaign):
    offsets=[]; totals=Counter()
    for case in campaign:
        if case["identity"][0]!="N":
            continue
        _, name, q, k, perm, mode = case["identity"]
        tr = lib.p.TREES[name]; nodes=lib.p.layout(tr)
        path = tuple(map(tuple,case["path"]))
        assert path==lib.normalize(tr,tuple(q),tuple(case["start"]))
        if len(nodes[0])!=4 or q[0]>=4:
            offsets.append([case["identity"],[]]); continue
        i=last_root_move(nodes,path); details=[]
        if i is not None:
            donor,site,sgn=move(path[i-1],path[i])
            if sgn<0 and nodes[site]:
                assert lib.verify_cut(tr,path[i-1],donor,site)[0]==path[i]
                base,rec=continuing(lib,tr,tuple(q),path[0],site,None)
                assert base==path and len(rec["calls"])==8
                _,sham=continuing(lib,tr,tuple(q),path[0],site,())
                bystanders=[c for c in range(k) if c!=donor and len(local(path[i:],c))>1]
                totals[bool(bystanders),sham["outcome"]]+=1
                details=[i,donor,site,bystanders,sham["outcome"]]
        offsets.append([case["identity"],details])
    return {"original_N":len(offsets),"original_N_final_junction_by_later_bystander_and_veto":counts(totals)},offsets


def earlier_fixture(lib):
    p=lib.p;tr=(p.B,p.B,p.L,p.L);start=(159,369,287);site=4
    path,record=continuing(lib,tr,(2,1,1),start,site,None)
    assert path==lib.normalize(tr,(2,1,1),start)
    reads=[(members,r) for n,members,r in record["calls"] if n==site]
    assert len(reads)==2 and reads[0][0]==[0,1,2] and len(reads[1][0])==1
    single,=reads[1][0];assert reads[1][1]==[7]
    return {"reads":reads,"singleton":single}


def single_binary(lib):
    p=lib.p; tally=Counter(); classes=Counter();raw=[]
    for k in (3,4):
        for order in range(4):
            tr=tuple(p.B if i==order else p.L for i in range(4))
            nodes=p.layout(tr); site=nodes[0][order]; left,right=nodes[site]
            others=[x for x in nodes[0] if x!=site]
            unique=set()
            for a,b in permutations(range(k),2):
                for mask in range(1,1<<k):
                    if not (mask>>a&1 and mask>>b&1):
                        continue
                    for labels in product(range(k),repeat=3):
                        z=[1]*k
                        for j in range(k):
                            if mask>>j&1:put(z,j,site)
                        put(z,a,left);put(z,b,right)
                        for j,t in zip(labels,others):put(z,j,t)
                        z=tuple(z);assert z not in unique;unique.add(z)
                        q=lib.profile(tr,z)
                        path=lib.normalize(tr,q,z)
                        i=last_root_move(nodes,path)
                        if i is None:continue
                        donor,t,sgn=move(path[i-1],path[i])
                        if q[0]>=4 or t!=site or sgn!=-1:continue
                        before,after=path[i-1:i+1]
                        assert lib.verify_cut(tr,before,donor,t)[0]==after
                        assert lib.profile(tr,before)==q
                        yes=child_tail(lib,tr,t,after)
                        alt=child_tail(lib,tr,t,before)
                        assert yes==path[i:]
                        veto, report = continuing(lib,tr,q,z,t,())
                        assert report["outcome"]=="returned" and report["source"]==[before,after,donor]
                        assert veto[:i]==path[:i] and veto[i:]==alt
                        for j in range(k):
                            if j!=donor:
                                y,n=local(yes,j),local(alt,j)
                                assert y==n
                                tally[k,"equal moving bystander" if len(y)>1 else "equal resting bystander"]+=1
                        tally[k,"final junction release"]+=1
                        classes[k,order,before,donor]+=1
                        raw.append([k,order,z,i,before,donor])
            tally[k,"inputs"]+=len(unique)
    return {"one_binary_counts":counts(tally),"direct_comparison_contexts":len(classes)},raw


def classified_record(lib, tr, state, chart):
    """Read two addressed subtrees from this chart's mask alone, ignoring chart identity."""
    nodes=lib.p.layout(tr);w,s=nodes[0][-2:];m=state[chart]
    ternary, = [i for i,t in enumerate(nodes[w],1) if m & (1<<t)]
    binary=tuple(i for i,t in enumerate(nodes[s],1) if m & (1<<t))
    return ternary,binary


def rich(lib):
    p=lib.p;tr=(p.L,p.L,p.T,p.B);nodes=p.layout(tr)
    x,y,w,site=nodes[0];left,right=nodes[site]
    tally=Counter();raw=[];controls_index={};starts=set()
    pattern=Counter(); record_sets=[set(),set()]; membership_choices=Counter()
    late_states=Counter()
    for pal in permutations(("A","B","C")):
        common=pal.index("A")
        for owners in permutations(range(3),2):
            extra,=set(range(3))-set(owners)
            for bonus in (False,True):
                for ternary in permutations(range(3)):
                    start=[1]*3;put(start,common,x,y)
                    for j,t in zip(ternary,nodes[w]):put(start,j,w,t)
                    for j,t in zip(owners,nodes[site]):put(start,j,site,t)
                    if bonus:put(start,extra,site)
                    start=tuple(start);starts.add(start);q=lib.profile(tr,start)
                    path=lib.normalize(tr,q,start);i=last_root_move(nodes,path)
                    donor,observed,sign=move(path[i-1],path[i]);assert (observed,sign)==(site,-1)
                    before,after=path[i-1:i+1]
                    assert [(j,t) for j,t,d in lib.moves(tr,before) if d<0]==[(donor,site)]
                    exact,certificate=lib.verify_cut(tr,before,donor,site);assert exact==after
                    changers=[r for r in range(3) if r!=donor and len(local(path[i:],r))>1]
                    tally[q[0],len(changers)]+=1
                    detail=[pal,owners,bonus,ternary,start,q,i,before,after,donor,changers]
                    if q[0]==2:
                        assert donor==0 and certificate==(1,2,0,True)
                        assert q==(2,3,2) and not bonus and common not in owners
                        # A legal non-idle edit at the same profile can leave the subtree untouched.
                        for r in (1,2):
                            new = lib.moves(tr,after)[r,x,1]
                            assert lib.profile(tr,new)==q
                            assert all((m & (1<<left | 1<<right)) == (n & (1<<left | 1<<right))
                                       for m,n in zip(new,after))
                        assert (len(changers)==2)==(common==2)
                        assert all(local(path[i:],j)[-1] & (1<<site) for j in (1,2))
                        for c in (1,2):
                            key=start,c
                            if key not in controls_index:
                                controls_index[key]=controls(lib,tr,q,start,site,path,i,donor,c)
                            checked=controls_index[key]
                            assert checked["base_calls"][-1][1]==[1,2]
                            assert path[i:] == child_tail(lib,tr,site,path[i])
                            assert not [action for action in lib.moves(tr,path[-1]) if action[2] < 0]
                            expected=classified_record(lib,tr,path[-1],c)
                            record_sets[0].add(expected)
                            clean=[b for b in checked["bypasses"] if b["clean_prior"]]
                            assert len(clean)==2
                            for b in clean:
                                assert b["second_input"][1]==[0,1,2]
                                alternate=classified_record(lib,tr,b["after_read"][-1],c)
                                assert alternate!=expected
                                assert b["after_read"] == child_tail(lib,tr,site,b["state_before_read"])
                                last=b["after_read"][-1]
                                cuts={a:z for a,z in lib.moves(tr,last).items() if a[2] < 0}
                                assert set(cuts)=={(2,site,-1)}
                                cap,=cuts.values()
                                assert not [a for a in lib.moves(tr,cap) if a[2]<0]
                                assert classified_record(lib,tr,cap,c)==alternate
                                late_states[1,2]+=1
                                record_sets[1].add(alternate)
                                pattern[len(changers),len(checked["live_receiver"])>1,
                                        len(b["receiver"])>1]+=1
                        membership_choices[pal.index("A"),donor==pal.index("A"),len(changers)]+=1
                    raw.append(detail)
    assert set(record_sets[0])=={(2,(1,)),(3,(2,))}
    assert set(record_sets[1])=={(2,(2,)),(3,())}
    assert not record_sets[0].intersection(record_sets[1])
    example=(409,681,79); ex=next(row for row in raw if row[4]==example and row[5][0]==2)
    examplepath=lib.normalize(tr,ex[5],example);i=ex[6]
    evidence=[{"entry":z,"chart":c,**vv} for (z,c),vv in sorted(controls_index.items())]
    summary={"presentations":len(raw),"distinct_indexed_inputs":len(starts),"by_cover_and_writing_bystanders":counts(tally),
             "cover_two_by_original_double_holder_rank":counts(membership_choices),
             "clean_comparisons_by_natural_writes_and_receiver_activity":counts(pattern),
             "local_record_sets":[sorted(s) for s in record_sets],
             "clean_comparisons_by_ordinary_closure_size":counts(late_states),
             "example":{"start":example,"index":i,"before":examplepath[i-1],"after":examplepath[i],
                        "suffix":examplepath[i:],"acquirer_P1":[lib.grades(tr,m) for m in local(examplepath[i:],2)]}}
    return summary,{"presentations":raw,"controls":evidence}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("historical_checkout",type=Path)
    parser.add_argument("--raw",type=Path);args=parser.parse_args()
    lib=History(args.historical_checkout.resolve())
    campaign=lib.p.produce(); checked=lib.v.verify(campaign)
    ns,nr=originals(lib,campaign["records"]);bs,br=single_binary(lib);ps,pr=rich(lib)
    raw=(json.dumps({"released":nr,"one_binary":br,"extension":pr},sort_keys=True,separators=(",",":"))+"\n").encode()
    if args.raw:args.raw.write_bytes(raw)
    print(json.dumps({"historical_campaign":[checked["status"],checked["records"],checked["moves"]],
                      "prior_fixture":earlier_fixture(lib),"released":ns,"one_binary":bs,"two_subtrees":ps,
                      "raw_sha256":sha256(raw).hexdigest()},sort_keys=True,indent=2))
