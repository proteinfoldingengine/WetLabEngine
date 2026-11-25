"""Exercise the unmodified v16.39 state-dependent prefix and three common target choices."""
from collections import Counter, defaultdict
from hashlib import sha1
import importlib.util
import json
import lzma
from pathlib import Path
import sys

from check_fixed_pair import bitmask, integer_tuple, modules, require, wire

PINS = {
    "builder": ("v16.39-theorem-validation/construct.py","284b8cc9305c14f3ff6f3693c67a2c61ea00e93e"),
    "pathcheck": ("v16.39-theorem-validation/check.py","d4acda0e79a35b6c42ef0984ad362ba5e3bfb684"),
    "qcheck": ("v16.33-consistency-quotient-kernel/verifier.py","c6cf3143423da17c09bbdbbc2eab4800c91acc24"),
}


def load_history(root):
    ops=modules(root)
    for name,(leaf,blob) in PINS.items():
        file=root/"ResearchHistory/UQCF-GEM/demos"/leaf
        data=file.read_bytes()
        require(sha1(f"blob {len(data)}\0".encode()+data).hexdigest()==blob,leaf)
        spec=importlib.util.spec_from_file_location("fork_caller_"+name,file)
        ops[name]=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ops[name])
    return ops


def decode(masks,size):
    return tuple(tuple(v for v in range(size) if m & (1<<v)) for m in masks)


def arm(ops,p,g,source,tip):
    n=len(p)
    full=(1<<n)-1
    receiver=1-source
    nodes=tuple(range(n))
    initial=ops["cut"].atomic(p,(nodes,nodes),source,tip)
    ops["gate"].verify_atomic(initial)
    start=list(map(bitmask,initial["after"]))
    children=[v for v in range(1,n) if p[v]==0]
    q=list(ops["qcheck"].qq(p,initial["after"]))
    variants={}
    for target in ([full,full],[full,1],[1,full]):
        result=ops["builder"].build(p,2,q,start,target)
        ops["pathcheck"].path_states(p,2,q,start,target,result)
        states=result["states"]
        at=next(i for i,x in enumerate(states) if all(sum(bool(y & (1<<v)) for y in x)==1 for v in children))
        grades=[list(g)]
        for i,(old,new) in enumerate(zip(states,states[1:]),1):
            j,= [j for j in (0,1) if old[j]!=new[j]]
            diff=old[j]^new[j]
            require(diff.bit_count()==1,"nonprimitive")
            v=diff.bit_length()-1
            fine,coarse=(old,new) if old[j]&diff else (new,old)
            ev=ops["cut"].atomic(p,decode(fine,n),j,v)
            ops["gate"].verify_atomic(ev)
            require(list(map(bitmask,ev["after"]))==coarse,"native move differs")
            if i<=at:
                a,b=decode(old,n)[receiver],decode(new,n)[receiver]
                require(set(b)<=set(a),"receiver expansion prior to read")
                grades.append(list(integer_tuple(ops["overlap"].push(p,a,b,tuple(grades[-1])))))
        variants["/".join(map(str,target))]=dict(states=states, prefix=result["zero_prefix"], suffix=result["zero_suffix"],
                checkpoint=at, receiver_grades=grades)
    choices=list(variants.values())
    prefix=choices[0]["states"][:choices[0]["checkpoint"]+1]
    require(all(x["states"][:x["checkpoint"]+1]==prefix for x in choices),"target-dependent early path")
    return dict(parents=list(p), grades=list(g), source=source, tip=tip, profile=q, variants=variants)


def main(root,out):
    ops=load_history(root)
    bare=json.loads(lzma.decompress((out/"fork_trigger_universe.json.xz").read_bytes()))
    result={}
    for key,row in bare.items():
        if key.startswith("bare:"):
            result[key]=arm(ops,tuple(row["parents"]),tuple(row["grades"]),row["source"],row["cut"])
    examples=(("four",(-1,0,0,1),(3,4,2,2),(2,3)),
              ("six",(-1,0,0,2,1,3),(3,4,1,4,2,2),(4,5)),
              ("seven",(-1,0,1,1,3,2,4),(5,3,4,1,4,2,2),(5,6)))
    for group,p,g,tips in examples:
        for source in (0,1):
            for tip in tips:
                result[f"{group}:{source}:{tip}"]=arm(ops,p,g,source,tip)
    pairs=defaultdict(list)
    counts=Counter()
    named={}
    for key,row in result.items():
        record=next(iter(row["variants"].values()))
        idx=record["checkpoint"]
        observation=dict(root=record["receiver_grades"][-1][0], checkpoint=idx, prefix=record["prefix"],
                         receiver_edits=sum(a[1-row["source"]]!=b[1-row["source"]]
                         for a,b in zip(record["states"][:idx],record["states"][1:idx+1])))
        if key.startswith("bare:"):
            counts["arms"]+=1
            counts["target_runs"]+=len(row["variants"])
            counts["deep_readded"]+=observation["prefix"]==1
            counts["receiver_changes"]+=observation["receiver_edits"]>0
            pairs[key.rsplit(":",1)[0]].append(observation["root"])
        else:
            named[key]=observation
    counts["matched_pairs"]=len(pairs)
    counts["different_receiver_roots"]=sum(a!=b for a,b in pairs.values())
    obj=dict(identities=result,bare=dict(counts),examples=named,pins={k:v for k,(_,v) in PINS.items()})
    (out/"fork_trigger_caller.json.xz").write_bytes(lzma.compress(wire(obj),preset=6))
    print(json.dumps(dict(counts),sort_keys=True))


if __name__=="__main__":
    main(Path(sys.argv[1]),Path(sys.argv[2]))
