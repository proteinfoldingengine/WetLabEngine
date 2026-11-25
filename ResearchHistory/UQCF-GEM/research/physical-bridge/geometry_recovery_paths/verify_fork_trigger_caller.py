"""Reconstruct complete normalization paths by assigning whole root-child subtrees."""
from collections import Counter
from copy import deepcopy
import json
import lzma
from pathlib import Path
import sys

from verify_fixed_pair import compare, encoded, need, restriction
from verify_receiver_turn import trees


def build(p,g,s,a):
    n=len(p)
    full=(1<<n)-1
    r=1-s
    children=[v for v,parent in enumerate(p) if parent==0]
    groups={v:[] for v in children}
    for v in range(1,n):
        top=v
        while p[top]!=0:
            top=p[top]
        groups[top].append(v)
    deep = p[a]!=0
    owner = 0 if deep else r
    q=[int(v in p[1:]) for v in range(n)]
    variants={}
    for target in ([full,full],[full,1],[1,full]):
        st=[full,full]
        st[s] ^= 1<<a
        path=[st.copy()]
        def set_bit(i,v,on):
            if bool(st[i]>>v&1)!=on:
                st[i] ^= 1<<v
                path.append(st.copy())
        if deep:
            set_bit(s,a,True)
        for top in children:
            for v in reversed(groups[top]):
                set_bit(1-owner,v,False)
        boundary=len(path)-1
        need(st[owner]==full and st[1-owner]==1,"cleanup allocation")
        target_owner=0 if target[0]==full else 1
        if target_owner!=owner:
            for top in children:
                for v in groups[top]:
                    set_bit(target_owner,v,True)
                for v in reversed(groups[top]):
                    set_bit(owner,v,False)
        if target==[full,full]:
            for top in reversed(children):
                for v in groups[top]:
                    set_bit(1,v,True)
        need(st==target,"target reconstruction")
        receiver_grades=[list(restriction(tuple(p),x[r],tuple(g))) for x in path[:boundary+1]]
        variants["/".join(map(str,target))]=dict(states=path,prefix=int(deep),suffix=0,checkpoint=boundary,
                                                  receiver_grades=receiver_grades)
    return dict(parents=list(p),grades=list(g),source=s,tip=a,profile=q,variants=variants)


def reconstruct():
    cases={}
    pairs=Counter()
    for p in trees():
        leaves=[v for v in range(1,len(p)) if v not in p[1:]]
        if len(leaves)!=2:
            continue
        g=[3 if v==0 else 2 if v in leaves else 4 for v in range(len(p))]
        for s in (0,1):
            for v in leaves:
                label="bare:"+"/".join(map(str,p))+f":{s}:{v}"
                cases[label]=build(p,g,s,v)
            pairs["matched_pairs"]+=1
            pairs["different_receiver_roots"]+=s==0 and sum(p[v]==0 for v in leaves)==1
            pairs["deep_readded"]+=sum(p[v]!=0 for v in leaves)
            pairs["receiver_changes"]+=sum(p[v]!=0 and s==0 for v in leaves)
            pairs["arms"]+=2
            pairs["target_runs"]+=6
    examples={}
    for group,p,g,tips in (("four",(-1,0,0,1),(3,4,2,2),(2,3)),("six",(-1,0,0,2,1,3),(3,4,1,4,2,2),(4,5)),
                            ("seven",(-1,0,1,1,3,2,4),(5,3,4,1,4,2,2),(5,6))):
        for s in (0,1):
            for a in tips:
                name=f"{group}:{s}:{a}"
                cases[name]=build(p,g,s,a)
                outputs=cases[name]["variants"]
                common=next(iter(outputs.values()))
                at=common["checkpoint"]
                deep=p[a]!=0
                drops_r=deep and s==0
                # A shallow tip is already gone at the non-keeper S. A deep tip
                # is restored in the one-edit expansion before all nonroot sites are removed.
                expected_idx=len(p) if deep else len(p)-2
                need(at==expected_idx and all(x["states"][:at+1]==common["states"][:at+1] and
                    x["receiver_grades"]==common["receiver_grades"] for x in outputs.values()),"common early prefix")
                examples[name]=dict(root=sum(g) if drops_r else g[0],checkpoint=at,prefix=int(deep),
                                    receiver_edits=len(p)-1 if drops_r else 0)
    return dict(identities=cases,bare=dict(pairs),examples=examples,
                pins=dict(builder="284b8cc9305c14f3ff6f3693c67a2c61ea00e93e",pathcheck="d4acda0e79a35b6c42ef0984ad362ba5e3bfb684",
                          qcheck="c6cf3143423da17c09bbdbbc2eab4800c91acc24"))


def main(out):
    raw=lzma.decompress((out/"fork_trigger_caller.json.xz").read_bytes())
    expected=reconstruct()
    compare(expected,json.loads(raw))
    need(encoded(expected)==raw,"noncanonical caller bytes")
    sample=expected["identities"]["four:0:3"]["variants"]["15/15"]
    checks=[(sample,lambda x:x["states"].pop(1)),(sample,lambda x:x["states"].append(x["states"][-1])),
            (sample,lambda x:x.update(checkpoint=0)),(sample,lambda x:x["receiver_grades"][-1].__setitem__(0,3)),
            (expected["pins"],lambda x:x.update(builder="unbound"))]
    for obj,mutate in checks:
        bad=deepcopy(obj)
        mutate(bad)
        try:
            compare(obj,bad)
        except ValueError:
            continue
        raise AssertionError("bad historical caller evidence accepted")
    print(json.dumps(dict(status="PASS",rejecting_controls=len(checks),**expected["bare"]),sort_keys=True))


if __name__=="__main__":
    main(Path(sys.argv[1]))
