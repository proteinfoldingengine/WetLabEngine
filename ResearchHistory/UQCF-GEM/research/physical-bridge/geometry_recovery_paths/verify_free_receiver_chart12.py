"""Independent terminal witnesses and fine-tip subset sums on chart 12's original input."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import sys
from free_receiver_io import FIXTURE, module, read_xz, require, same, save


def direct_spectrum(optional, grades, minimum):
    counts=[1]
    for v in optional:
        mass=grades[v]
        length=len(counts)
        counts.extend([0]*mass)
        for i in reversed(range(length)):
            counts[i+mass]+=counts[i]
    return [[minimum+i,count] for i,count in enumerate(counts) if count]


def canonical(p,g,rows,tips,own):
    keep=[]
    final=[{0} for _ in rows]
    paths={}
    for v in range(len(p)):
        ancestors=[v]
        while ancestors[-1]:
            ancestors.append(p[ancestors[-1]])
        paths[v]=ancestors
    for leaf in tips:
        j=12 if leaf in own else next(i for i,view in enumerate(rows) if i!=12 and leaf in view)
        final[j].update(paths[leaf])
        keep.append(j)
    # Every intermediate prefix contains a fixed globally covering final family.
    require(set.union(*final)==set(range(len(p))) and all(y<=x for x,y in zip(rows,final)), "covering endpoint")
    require(all(sum(leaf in view for view in final)==1 for leaf in tips), "private terminal tips")
    digest=sha256()
    moves=0
    for j,(start,end) in enumerate(zip(rows,final)):
        pending=set(start-end)
        order=sorted(pending,key=lambda v:(-len(paths[v]),v))
        position={v:i for i,v in enumerate(order)}
        for v in order:
            require(v!=0 and all(position[w]<position[v] for w in pending if p[w]==v), "witness ancestor order")
            digest.update(f"{j},{v}\n".encode())
        moves+=len(pending)
    receiver=final[12]
    root=sum(g[v] for v in range(len(p)) if all(x not in receiver for x in paths[v] if x))
    return dict(owners=keep,receiver=sorted(receiver),root=root,moves=moves,
                receiver_moves=len(rows[12]-receiver),complete_word_sha256=digest.hexdigest())


def verify(root,doc):
    f=module(root,FIXTURE,"independent_fixture","3324c0b46e09120ae526338444a19070b692d049")
    features,expected_work=f.fixture()
    p,g,initial=map(tuple,zip(*features))
    tips=sorted(v for v in range(1,len(p)) if v not in p)
    require((doc["tree_vertices"],doc["global_tips"])==(len(p),len(tips)),"tree identity")
    cases={(r["mode"],r["cut"]):r for r in doc["cases"]}
    require(len(cases)==len(doc["cases"])==4,"case coverage")
    spectra=set()
    summary=[]
    for mode in ("original","balanced"):
        before=[{v for v,h in enumerate(initial) if j in h} for j in range(25)]
        if mode=="balanced":
            for j in set(range(25))-{0,8,12,13}:
                before[j].difference_update((46,718))
        subtot=list(g)
        for v in reversed(range(1,len(p))):
            subtot[p[v]]+=subtot[v]
        for i in range(25):
            for j in range(i):
                require(sum(subtot[v]**2 for v in (before[i]^before[j]))==expected_work[i][j],"geometry")
        roots_by_cut={}
        allowed_by_cut={}
        for cut in (662,718):
            rec=cases[mode,cut]
            rows=[set(view) for view in before]
            require(cut in rows[0] and cut in tips and any(cut in view for view in rows[1:]),"legal cut")
            rows[0].remove(cut)
            available=set(tips)&rows[12]
            outside=set.union(*(x for i,x in enumerate(rows) if i!=12))
            forced=available-outside
            may=sorted(available-forced)
            require(all(p[v]==0 for v in available) and rows[12]==available|{0},"root-leaf chart")
            floor=sum(g)-sum(g[v] for v in available)
            calc=direct_spectrum(may,g,floor)
            digest=sha256(repr(calc).encode()).hexdigest()
            same(doc["polynomials"][digest],calc,"every terminal numerical multiplicity")
            spectra.add(digest)
            expected=dict(mode=mode,cut=cut,available=sorted(available),forced=sorted(forced),
                          prior_root=floor,optional=len(may),polynomial=digest,
                          minimum=canonical(p,g,rows,tips,available),maximum=canonical(p,g,rows,tips,forced))
            def tau(views):
                immediate={i for i in range(1,len(p)) if p[i]==0}
                from itertools import combinations
                return next(n for n in range(1,26) if any(immediate<=set.union(*c) for c in combinations(views,n)))
            expected["event"]=dict(index=0,leaf=cut,pre=tau(before),post=tau(rows))
            same(rec,expected,"real fixture and full witnesses")
            roots_by_cut[cut]={x for x,count in calc}
            allowed_by_cut[cut]=(available,forced)
            summary.append(dict(mode=mode,cut=cut,prior=floor,optional=len(may),forced=sorted(forced),
                    minimum=calc[0][0],maximum=calc[-1][0],distinct=len(calc),max_multiplicity=calc[-1][1],
                    max_global_moves=rec["maximum"]["moves"],max_receiver_moves=rec["maximum"]["receiver_moves"]))
        A,F0=allowed_by_cut[662]
        B,F1=allowed_by_cut[718]
        require(A==B and F0<=F1,"nested terminal sets")
        extra=sorted(roots_by_cut[662]-roots_by_cut[718])
        require(extra==([] if mode=="original" else [max(roots_by_cut[662])]) and not roots_by_cut[718]-roots_by_cut[662],
                "exclusive scalar")
        for row in summary:
            if row["mode"]==mode:
                row["common_records_power_of_two"]=len(A-(F0|F1))
                row["exclusive_662_root_grades"]=extra
    require(set(doc["polynomials"])==spectra,"polynomial inventory")
    return summary


if __name__=="__main__":
    root,data=map(Path,sys.argv[1:])
    doc=read_xz(data/"free_receiver_chart12.json.xz")
    rows=verify(root,doc)
    save(data/"free_receiver_spectra.json",rows)
    print([(r["mode"],r["cut"],r["minimum"],r["maximum"],r["exclusive_662_root_grades"]) for r in rows])
