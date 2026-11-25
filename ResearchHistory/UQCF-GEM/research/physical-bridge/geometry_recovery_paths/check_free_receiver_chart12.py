"""Compute the exact terminal root-grade distribution from the frozen 25-chart input."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import sys
from free_receiver_io import ATOM, FIXTURE, P1, module, require, write_xz

R = 12


def root_blocks(p):
    out = {}
    for v in range(1,len(p)):
        w=v
        while p[w] != 0:
            w=p[w]
        out[v]=w
    return out


def polynomial(factors, grade):
    values = {grade:1}
    for mass,stay,drop in factors:
        new = defaultdict(int)
        for x,count in values.items():
            if stay:
                new[x] += count * stay
            if drop:
                new[x+mass] += count * drop
        values = new
    return [[x,values[x]] for x in sorted(values)]


def endpoint(p,g,holders,tips,chosen,push):
    owners = [R if v in chosen else min(holders[v]-{R}) for v in tips]
    views = [{0} for _ in range(25)]
    for v,i in zip(tips,owners):
        while v != -1:
            views[i].add(v)
            v=p[v]
    depth=[0]*len(p)
    for i in range(1,len(p)):
        depth[i]=depth[p[i]]+1
    # Construct a complete deletion history. The final owner of each fine tip is never touched.
    count=[len(x) for x in holders]
    child_counts=[Counter(p[v] for v in range(1,len(p)) if i in holders[v]) for i in range(25)]
    digest=sha256()
    moves=receiver_moves=0
    for j,view in enumerate(views):
        surplus = [v for v,h in enumerate(holders) if j in h and v not in view]
        for v in sorted(surplus,key=lambda v:(-depth[v],v)):
            require(v and child_counts[j][v]==0 and count[v]>=2, "witness deletion")
            child_counts[j][p[v]]-=1
            count[v]-=1
            digest.update(f"{j},{v}\n".encode())
            moves+=1
            receiver_moves+=j==R
    for j,view in enumerate(views):
        require(all(v==0 or child_counts[j][v] or count[v]==1 for v in view), "nonterminal witness")
    nodes=sorted(views[R])
    root=int(push(tuple(p),tuple(range(len(p))),tuple(nodes),tuple(g))[0])
    return dict(owners=owners,receiver=nodes,root=root,moves=moves,receiver_moves=receiver_moves,
                complete_word_sha256=digest.hexdigest())


def produce(root,out):
    fixture=module(root,FIXTURE,"chart_fixture","3324c0b46e09120ae526338444a19070b692d049")
    atom=module(root,ATOM,"chart_atom","c10ac57f988a439144e21898bd2b33ece0838a9b").atomic
    push=module(root,P1,"chart_p1","b18f52109ccff9c7dc77542d3b8f3e5d5989102a").push
    features,target=fixture.fixture()
    p,g,h0=zip(*features)
    tips=sorted(set(range(1,len(p)))-set(p))
    blocks=root_blocks(p)
    per_root=defaultdict(list)
    for v in tips:
        per_root[blocks[v]].append(v)
    subtree=list(g)
    for v in reversed(range(1,len(p))):
        subtree[p[v]]+=subtree[v]
    squares=[x*x for x in subtree]
    results=[]
    polys={}
    for mode in ("original","balanced"):
        h=[set(s) for s in h0]
        if mode=="balanced":
            for j in sorted(h[718]-{0,R}):
                for v in (718,46):
                    require(j in h[v] and len(h[v])>=2 and v in tips, "illegal preparation")
                    h[v].remove(j)
        before=tuple(tuple(v for v,s in enumerate(h) if j in s) for j in range(25))
        work=fixture.work_for(before,squares)
        require(work==target and len(list(combinations(range(25),2)))==300,"matched prior geometry")
        for cut in (662,718):
            event=atom(p,before,0,cut)
            after=tuple(map(tuple,event["after"]))
            require(after[R]==before[R] and len(before[0])-len(after[0])==1 and cut not in after[0], "source event")
            post=[set(s) for s in h]
            post[cut].remove(0)
            available={v for v in tips if R in post[v]}
            forced={v for v in available if post[v]=={R}}
            factors=[]
            for w,desc in sorted(per_root.items()):
                may=len(set(desc)&(available-forced))
                drop=int(not (set(desc)&forced))
                factors.append((subtree[w],2**may-drop,drop))
            pol=polynomial(factors,g[0])
            key=sha256(repr(pol).encode()).hexdigest()
            polys[key]=pol
            low=endpoint(p,g,post,tips,available,push)
            high=endpoint(p,g,post,tips,forced,push)
            require(low["root"]==pol[0][0] and high["root"]==pol[-1][0],"projected extrema")
            require(sum(n for x,n in pol)==2**(len(available)-len(forced)),"terminal mass")
            results.append(dict(mode=mode,cut=cut,prior_root=int(push(p,tuple(range(len(p))),before[R],g)[0]),
                available=sorted(available),forced=sorted(forced),polynomial=key,minimum=low,maximum=high,
                optional=len(available)-len(forced),event=dict(index=event["index"],leaf=event["leaf"],
                pre=event["tau_before"],post=event["tau_after"])))
    output=dict(cases=results,polynomials=polys,tree_vertices=len(p),global_tips=len(tips))
    write_xz(out/"free_receiver_chart12.json.xz",output)
    for row in results:
        print(row["mode"],row["cut"],"optional",row["optional"],"forced",row["forced"],"root",
              row["minimum"]["root"],row["maximum"]["root"],"distinct",len(polys[row["polynomial"]]))


if __name__=="__main__":
    produce(Path(sys.argv[1]),Path(sys.argv[2]))
