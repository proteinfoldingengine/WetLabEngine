"""Replay minimum exact-work equality sets for the historical 25-chart fixture."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha1
from itertools import combinations
import json
import os
from pathlib import Path
import sys

ROOT = Path("ResearchHistory/UQCF-GEM")
FIXTURE = ROOT / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py"
WATCH = {6,7,8,9,11,13,16,17,18,19,21,23,24}
ADDITIONS = {"14": {12}, "15": {14,22}}

def read_pinned(path, digest):
    raw = path.read_bytes()
    assert sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == digest
    return json.loads(raw)

def matches(columns):
    negative = [v for v, c in columns.items() if sum(c) < 0]
    zero = [v for v, c in columns.items() if sum(c) == 0]
    groups = defaultdict(list)
    for v,c in columns.items():
        if sum(c) > 0:
            groups[c].append(v)
    keys = sorted(groups)
    k = min(sum(c)//abs(c[0]) for c in keys)
    assert k > 0
    out = []
    for size in range(1,len(negative)+len(zero)+1):
        for special in combinations(negative+zero,size):
            t = tuple(-sum(c) for c in zip(*(columns[v] for v in special)))
            for total in range(max(map(abs,t)), sum(t)//k + 1):
                if any((total-a)%2 for a in t):
                    continue
                demand = tuple((total-a)//2 for a in t)
                candidates = [c for c in keys if abs(c[0]) <= total and all(a or b>0 for a,b in zip(demand,c))]
                def traverse(start, ds, left, used):
                    if left == 0:
                        if not any(ds):
                            out.append((sorted(special), [sorted(groups[c]) for c in used]))
                        return
                    if any(d>left for d in ds):
                        return
                    for z in range(start,len(candidates)):
                        c = candidates[z]
                        w = abs(c[0])
                        if w>left or used.count(c)>=len(groups[c]):
                            continue
                        ns = tuple(a-(w if b<0 else 0) for a,b in zip(ds,c))
                        if min(ns)>=0:
                            traverse(z,ns,left-w,used+[c])
                traverse(0,demand,total,[])
    return negative, zero, out

def main():
    sources, preparation, earlier, output = map(Path,sys.argv[1:])
    prep = read_pinned(preparation,"34fa8c957dec8b7433543553abb4c1d57db36b4a")
    old = read_pinned(earlier,"24816b42f2c00c9790e2417c95ba0589074050b0")
    output = output.resolve()
    os.chdir(sources)
    raw = FIXTURE.read_bytes()
    assert sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()=="3324c0b46e09120ae526338444a19070b692d049"
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    m = f.modules()
    features, original = f.fixture()
    parents, grades, _ = map(tuple,zip(*features))
    s = list(grades)
    for v in range(len(s)-1,0,-1):
        s[parents[v]] += s[v]
    squares = [x*x for x in s]
    labels = f.LABELS
    def clone(rows): return [r.copy() for r in rows]
    def cut(rows,i,v):
        assert v in rows[i] and v and sum(v in r for r in rows)>1
        assert not any(parents[u]==v for u in rows[i])
        rows[i].remove(v)
    def admission(work):
        exact=tuple(tuple(map(Fraction,row)) for row in work)
        return dict(m["carriers"].build_carrier(m["projection"].Payload(f.SIDE,Fraction(1),labels,exact,f.edges(work)[1],())).receipt)
    def differences(work):
        return [[i,j,original[i][j],work[i][j]] for i,j in combinations(labels,2) if original[i][j]!=work[i][j]]
    common = list(map(set,f.initial_state(features)))
    for i,v in prep["preparation"]: cut(common,i,v)
    assert len(prep["preparation"])==134 and f.work_for(common,squares)==original
    evidence = {}
    for source,shared in ((718,719),(719,718)):
        rows = clone(common)
        for v in (source,1355): cut(rows,0,v)
        assert f.work_for(rows,squares)==original and source not in rows[0] and {718,719}<=rows[12]
        assert [i for i in labels if source in rows[i]]==[12]
        result = {"routes":{},"blind":{},"positive":{}}
        for route,addition in ADDITIONS.items():
            watch=WATCH|addition
            editors={}
            for i in labels:
                constrained=sorted(f.grid()[i]|{j for j in labels if f.opposite(i,j)}|(watch if i==0 else {0} if i in watch else set()))
                outside=set().union(*(r for j,r in enumerate(rows) if j!=i))
                fixed=set(rows[i])-outside
                for v in tuple(fixed):
                    while v:
                        v=parents[v]
                        fixed.add(v)
                eligible=rows[i]-fixed-{0}
                cols={v:tuple(squares[v]*(1 if v in rows[j] else -1) for j in constrained) for v in sorted(eligible)}
                negatives,zeros,solutions=matches(cols)
                assert bool(solutions)==(i==12)
                assert all(shared in special for special,_ in solutions) if i==12 else True
                if i==12:
                    assert any(special==[shared] and len(mates)==1 and {1301,1302}<=set(mates[0]) for special,mates in solutions)
                    if route=="14":
                        assert len(solutions)==1 and len(solutions[0][1][0])==60
                editors[i]={"coordinates":constrained,"eligible_count":len(eligible),"negative":negatives,"zero":zeros,"relaxed_solutions":solutions}
            result["routes"][route]=editors
        for mate in (1301,1302):
            post=clone(rows)
            for v in (shared,mate): cut(post,12,v)
            work=f.work_for(post,squares)
            assert work==original and {source}==({718,719}&post[12])
            result["positive"][mate]=admission(work)
        controls={r["mate"]:{r["j"]} for r in old["arms"][str(source)]["admission_only"] if r["carrier"]=="accepted"}
        assert set().union(*controls.values())==WATCH
        controls.update({1362:{12,14},1399:{12,22},1046:{12,14,22}})
        for mate,delta in sorted(controls.items()):
            post=clone(rows)
            for v in (shared,mate): cut(post,0,v)
            work=f.work_for(post,squares)
            changes=differences(work)
            assert {j for i,j,before,after in changes if i==0}==delta and len(changes)==len(delta)
            assert post[12]==rows[12]==common[12]
            result["blind"][mate]={"changes":changes,"gate":admission(work)}
        evidence[source]=result
    assert evidence[718]["blind"]==evidence[719]["blind"]
    output.write_text(json.dumps(evidence,sort_keys=True,indent=2)+"\n",encoding="utf-8")

    summary = {}
    for source,r in evidence.items():
        z = summary[source] = {}
        z["editor_relaxation"] = {mode:{i:[v["negative"],v["zero"],[(s,[len(g) for g in gs]) for s,gs in v["relaxed_solutions"]]] for i,v in rows.items() if v["negative"] or v["zero"] or v["relaxed_solutions"]} for mode,rows in r["routes"].items()}
        z["blind_changed_entry_sets"] = {mate:[y[1] for y in v["changes"]] for mate,v in r["blind"].items()}
        z["positive_control_mates_with_full_gate"] = [str(v) for v in sorted(r["positive"])]
    output.with_suffix(".summary.json").write_text(json.dumps(summary,sort_keys=True,separators=(",", ":"))+"\n",encoding="utf-8")
    print("Two arms, two minimal sets, 25 editors, original carrier controls passed.")

if __name__=="__main__":
    main()
