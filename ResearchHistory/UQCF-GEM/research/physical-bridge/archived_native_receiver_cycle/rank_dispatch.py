"""Check rank-dependent destination changes in the v16.53 R campaign."""
from collections import Counter
import gzip
from hashlib import sha1
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def edit(a, b):
    (label, changed), = [(j,u^v) for j,(u,v) in enumerate(zip(a,b)) if u!=v]
    assert changed.bit_count()==1
    return (changed.bit_length()-1,label,b[label]>a[label])


def main(demos):
    demo = demos/"v16.53-four-child-boundary"
    sys.path.insert(0,str(demo))
    import producer as p
    import verifier as v
    atom = load("atomic53control", demos/"v16.26-consistency-increment-law/engine.py")
    av = load("atomic53verify", demos/"v16.26-consistency-increment-law/verify.py")
    doc = p.produce()
    raw = gzip.compress((json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n").encode(),mtime=0)
    git = sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    assert git == "9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e"
    archive = doc["records"]
    panel = {tuple(r["start"]):(i,r) for i,r in enumerate(archive) if r["identity"][:2]==["R",3]}
    assert len(panel)==2401
    counts = Counter()
    for initial,(idx,r) in panel.items():
        assert r["q"] == v.profile_check(p.Q,3,r["start"])
        v.path_check(p.Q,3,r["q"],r["path"],r["start"],v.model(p.Q,r["q"],3)[2])
        for t,(a,b) in enumerate(zip(r["path"],r["path"][1:]),1):
            if panel[tuple(a)][1]["q"]==[2] and panel[tuple(b)][1]["q"]==[3]:
                assert t==len(r["path"])-1
                counts["terminal_rises_in_stock_paths"]+=1
        if r["q"]!=[2]:
            continue
        choices=[]
        for label,mask in enumerate(initial):
            for site in range(1,5):
                if not mask & (1 << site):
                    continue
                post=list(initial)
                post[label]^=1 << site
                item=panel.get(tuple(post))
                if item is None or item[1]["q"]!=[3]:
                    continue
                views=[[u for u in range(5) if z & (1 << u)] for z in initial]
                receipt=atom.atomic([-1,0,0,0,0],views,label,site)
                assert av.verify_atomic(receipt)==(1,True)
                assert [sum(1 << u for u in col) for col in receipt["after"]]==post
                before=edit(*r["path"][:2])
                after=edit(*item[1]["path"][:2])
                assert before[2] and after[2] and before[0]!=after[0]
                choices.append((site,after[0]))
                counts["triggering_cuts"]+=1
                counts["both_first_destinations_remote"]+=site not in (before[0],after[0])
        if choices:
            counts["source_states"]+=1
            counts["single_trigger_states"]+=len(choices)==1
        for (s,r1),(t,r2) in combinations(choices,2):
            counts["same_prior_pairs"]+=1
            counts["same_prior_changed_destination"]+=r1!=r2
            counts["same_prior_both_remote_and_changed"]+=r1!=r2 and not {r1,r2}&{s,t}

    def permuted_first(raw,names,order):
        start=[1+sum(1 << i for i,u in enumerate(names,1) if z & (1 << u)) for z in raw]
        q=[p.coordinate(start,[1,2,3,4])]
        trace=[]
        path=p.normalize(start,p.Q,3,q,list(order),trace)
        v.path_check(p.Q,3,q,path,start,p.canonical(p.Q,3,q,list(order)))
        kind="four_root_expand_contract" if q[0]==2 else "four_root_cover"
        assert sum(row["kind"]==kind for row in trace)==1
        site,label,add=edit(*path[:2])
        return names[site-1],label,add

    def permutations_panel(first,second,source_sites):
        result=Counter()
        for names in permutations(range(1,5)):
            for order in permutations(range(3)):
                a,b=(permuted_first(archive[i]["start"],names,order) for i in (first,second))
                result["runs_paired"]+=1
                result["different_destination"]+=a[0]!=b[0]
                result["both_remote_and_different"]+=a[0]!=b[0] and not {a[0],b[0]}&source_sites
        return result

    # The same first three frames as the preceding two-label layer repair.
    layer_prefix=[[27,31],[31,31],[31,29]]
    sys.path.insert(0,str(demos/"v16.54-parent-support-connectivity"))
    from mechanisms import produce as generate_layer
    from universe import case as layer_case
    peak=archive[274]["identity"][2:]
    generated=generate_layer(layer_case("M1","layers",2,[1]*4,1,peak,{"peak":2}))
    layer_path=[p.encode_roots(2,rows) for rows in generated["path"]]
    assert layer_path[::-1]==layer_prefix==archive[328]["path"][:3]
    assert archive[274]["path"][:3]==[[27,29],[27,31],[31,31]]
    return dict(certificate_git_blob=git,counts=counts,
                rank_switch_control=permutations_panel(643,642,{4}),
                same_rank_two_sources=permutations_panel(830,1172,{1,4}),
                records={i:archive[i] for i in (274,328,642,643,830,1172,1173)})


if __name__=="__main__":
    print(json.dumps(main(Path(sys.argv[1]).resolve()),indent=2,sort_keys=True))
