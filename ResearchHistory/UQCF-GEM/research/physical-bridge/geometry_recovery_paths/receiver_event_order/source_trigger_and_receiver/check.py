"""Replay the historical source, the continuing four-child writer and its live nested read."""
import argparse
from collections import Counter, defaultdict
from functools import cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
from types import SimpleNamespace

from live import apply_atom, local, sites, sweep


def file_module(name, path):
    spec = spec_from_file_location(name,path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def modules(checkout):
    demos = checkout / "ResearchHistory/UQCF-GEM/demos"
    sys.path.insert(0,str(demos/"v16.53-four-child-boundary"))
    import producer, verifier, cover
    return SimpleNamespace(p=producer,v=verifier,cover=cover,
        atom=file_module("atom",demos/"v16.26-consistency-increment-law/engine.py"),
        av=file_module("atom_verify",demos/"v16.26-consistency-increment-law/verify.py"),
        p1=file_module("p1",demos/"v16.23-overlap-descent/engine.py"),
        v27=file_module("attribution",demos/"v16.27-increment-attribution-closure/engine.py"))


def stars(k):
    for roots in product(range(1,1<<k),repeat=4):
        yield tuple(1+sum(1<<i for i,r in enumerate(roots,1) if r&(1<<j)) for j in range(k))


@cache
def height(state):
    for n in range(1,len(state)+1):
        for group in combinations(state,n):
            union = 0
            for mask in group:
                union |= mask
            if union==31:
                return n
    raise ValueError("uncovered tip")


def move(before,after):
    (j,d), = [(i,a^b) for i,(a,b) in enumerate(zip(before,after)) if a!=b]
    assert d.bit_count()==1
    return j, d.bit_length()-1, before[j]>after[j]


def probe(lib, operation, *args):
    logs=[]
    def watch(frame,event,value):
        if event!="call":
            return
        if frame.f_code is lib.p.clear_role.__code__:
            v=frame.f_locals
            logs.append(["clear",v["child"],v["x"],v["y"]])
        if frame.f_code.co_name=="transfer" and frame.f_code.co_filename==lib.cover.__file__:
            parent,current=frame.f_back.f_locals,frame.f_locals
            if parent["x"]!=current["x"]:
                logs.append(["spare",parent["x"],current["x"],parent["j"],current["j"]])
    previous=sys.getprofile()
    sys.setprofile(watch)
    try:
        result=operation(*args)
    finally:
        sys.setprofile(previous)
    return result,logs


def permutation_orbit(key):
    state,source,tip=key
    orbit=set()
    for order in permutations((1,2,3,4)):
        for palette in permutations(range(3)):
            rep=tuple(1+sum(1<<order[t-1] for t in range(1,5) if state[j]&(1<<t)) for j in palette)
            orbit.add((rep,palette.index(source),order[tip-1]))
    return orbit


def flat(lib, campaign):
    p,v=lib.p,lib.v
    parents=(-1,0,0,0,0)
    pool={}
    for start in stars(3):
        if height(start)!=2:
            continue
        for tip in range(1,5):
            owners=[j for j,m in enumerate(start) if m & (1<<tip)]
            if len(owners)!=2:
                continue
            for j in owners:
                e=list(start);e[j]^=1<<tip
                if height(tuple(e))!=3:
                    continue
                rival,=set(owners)-{j}
                c,=set(range(3))-set(owners)
                key=(start,j,tip)
                pool[start,j,tip]=(key,c,True)
                pool[start,rival,tip]=(key,c,False)
    assert len(pool)==1440
    source_keys={key for key,_,high in pool.values() if high}
    rows=[r for r in campaign if r["identity"][:2]==["R",3]]
    assert {tuple(r["start"]) for r in rows}==set(stars(3))
    counts=Counter(); hits=[]; active=set()
    for row in rows:
        start=tuple(row["start"]);path=list(map(tuple,row["path"]));q,=row["q"]
        counts[q]+=1
        for i,(before,after) in enumerate(zip(path,path[1:])):
            j,tip,cut=move(before,after)
            if not cut or (before,j,tip) not in pool:
                continue
            key,c,high=pool[before,j,tip]
            observed,cert=apply_atom(lib,parents,before,j,tip)
            assert tuple(observed)==after and cert==[1,True,2,3] and high and q==3
            assert i+1==len(path)-1
            prefix=local(path[:i+1],c)
            marker=next(k for k,(a,b) in enumerate(zip(prefix,prefix[1:]),1) if (a>>1).bit_count()==3)
            assert (prefix[marker]>>1).bit_count()==2
            assert c!=j and local(path[i+1:],c)==(before[c],)
            # A new original call on exactly the final state yields a nontrivial closed excursion.
            renewed=p.normalize(list(after),p.Q,3,[q])
            v.path_check(p.Q,3,[q],renewed,list(after),list(after))
            seq=local(renewed,c)
            assert [(m>>1).bit_count() for m in seq[:3]]==[2,3,2]
            active.add(key);hits.append([start,i,before,after,c,marker])
    assert len(active)==1 and len(hits)==counts[3]
    orbit=permutation_orbit(next(iter(active)))
    assert orbit<=source_keys
    return {"three_chart_entries":len(rows),"entries_by_cover":dict(sorted(counts.items())),
            "source_pairs":len(source_keys),"original_internal_raising_steps":len(hits),
            "distinct_default_events":len(active),"distinct_events_under_all_priorities":len(orbit),
            "original_internal_competing_steps":0,"original_post_source_bystander_writes":0}, hits


def other_inputs(lib, campaign):
    p,v=lib.p,lib.v
    four={};four_records=[];pairs=0;op_counts=Counter()
    for z in stars(4):
        if height(z)!=3:
            continue
        route,log=probe(lib,p.normalize,list(z),p.Q,4,[3])
        _,_,end=v.model(p.Q,[3],4)
        v.path_check(p.Q,4,[3],route,list(z),end)
        assert not log
        current=tuple(local(route,i) for i in range(4))
        for j,seq in enumerate(current):
            key=(j,z[j])
            assert four.setdefault(key,seq)==seq
        four_records.append([z,current])
    for z,current in four_records:
        for j,m in enumerate(z):
            for t in range(1,5):
                if m&(1<<t) and any(n!=j and y&(1<<t) for n,y in enumerate(z)):
                    e=list(z);e[j]^=1<<t
                    if height(tuple(e))==3:
                        pairs+=3
    @cache
    def nested_run(name,q,z):
        tree=p.TREES[name]
        path,log=probe(lib,p.normalize,list(z),tree,len(z),list(q))
        _,_,end=v.model(tree,list(q),len(z))
        v.path_check(tree,len(z),list(q),path,list(z),end)
        return tuple(local(path,j) for j in range(len(z))),log
    nested=[]; comparisons=0
    for row in campaign:
        tag=row["identity"][0]
        if tag=="R" and row["identity"][1]==3 and row["q"]==[3]:
            path,log=probe(lib,p.normalize,row["start"],p.Q,3,[3])
            assert path==row["path"] and log==[]
        if tag!="N":
            continue
        _,name,q,k,perm,mode=row["identity"];q=tuple(q);z=tuple(row["start"])
        tree=p.TREES[name];base,log=nested_run(name,q,z);nested.append([row["identity"],log])
        assert base==tuple(local(row["path"],j) for j in range(k))
        for item in log:op_counts[item[0]]+=1
        nodes=p.layout(tree);parents=[-1]+[next(j for j,L in enumerate(nodes) if n in L) for n in range(1,len(nodes))]
        for site in range(1,len(nodes)):
            results=[]
            for j,m in enumerate(z):
                if not m>>site&1 or any(m>>vtx&1 for vtx in nodes[site]):
                    continue
                if not any(n!=j and y>>site&1 for n,y in enumerate(z)):
                    continue
                e,_=apply_atom(lib,parents,z,j,site)
                if tuple(v.profile_check(tree,k,e))==q:
                    outcomes,_=nested_run(name,q,tuple(e))
                    results.append((j,outcomes))
            for (j,a),(l,b) in combinations(results,2):
                for c in set(range(k))-{j,l}:
                    assert a[c]==b[c]
                    comparisons+=1
    test,spare=probe(lib,p.mechanism_record,"spare_current_bin")
    assert test==v.mechanism("spare_current_bin") and len(spare)==1 and spare[0][0]=="spare"
    return {"four_chart_stars_screened":15**4,"four_chart_target_three":len(four_records),
            "fixed_target_remote_withdrawal_observers":pairs,"four_chart_single_trace_classes":len(four),
            "nested_originals":len(nested),"nested_calls_with_clearance":sum(bool(x[1]) for x in nested),
            "nested_events":dict(op_counts),"nested_equal_target_rival_comparisons":comparisons,
            "diagnostic_spare":spare}, {"four_chart_trace_table":[[j,m,v] for (j,m),v in sorted(four.items())],
            "four_chart_inputs":[z for z,_ in four_records],"nested_originals":nested}


def receipt_consumers(lib):
    parents=(-1,0,0,0,0)
    start=[[0,1,2],[0,3,4],[0,4]]; after=[[0,1,2],[0,3],[0,4]]
    data=lib.atom.factor(parents,start,after)
    assert lib.av.verify_factor(data) is True
    paths=lib.v27.paths(parents,tuple(map(tuple,start)),tuple(map(tuple,after)))
    assert len(paths)==1
    certificate,=paths[0]
    projected=lib.v27.event_map(paths[0])
    assert projected=={(1,4):1}
    wrong=dict(certificate,trigger=False)
    try:
        lib.av.verify_atomic(wrong)
    except ValueError as error:
        assert str(error)=="false certificate"
    else:
        raise AssertionError("Accepted forged trigger")
    # The later path enumerator propagates after; its attribution projection reads delta_h.
    assert lib.v27.event_map([wrong])==projected
    return {"source_fields":[certificate["trigger"],certificate["delta_h"]],
            "v27_attribution":[[j,t,val] for (j,t),val in projected.items()],"false_trigger_rejected":True}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_checkout",type=Path)
    parser.add_argument("--raw",type=Path)
    opts=parser.parse_args()
    lib=modules(opts.historical_checkout.resolve());campaign=lib.p.produce()
    cert=lib.v.verify(campaign)
    a,ar=flat(lib,campaign["records"])
    b,br=other_inputs(lib,campaign["records"])
    c,cr=sweep(lib)
    raw=(json.dumps({"internal":ar,"others":br,"live":cr},sort_keys=True,separators=(",",":"))+"\n").encode()
    if opts.raw:opts.raw.write_bytes(raw)
    print(json.dumps({"original_campaign":[cert["status"],cert["records"],cert["moves"]],"flat":a,"controls":b,
          "live":c,"receipt_consumers":receipt_consumers(lib),"raw_sha256":sha256(raw).hexdigest()},sort_keys=True,indent=2))
