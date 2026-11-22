"""Exact grade transport on the archived v16.45 fork replay."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
from zipfile import ZipFile

U = Path("ResearchHistory/UQCF-GEM")
FCV = U / "foundational-closure-verification"
BASE = U / "research/physical-bridge/forced_parent_deletion"
ARCHIVE = BASE / "fork_profile_write_evidence/fork-profile-write-replay.zip"
KEYS = ((), (0,), (0,0), (0,1), (1,), (1,0), (1,1))
PREP = (31,15,113)
MEET = (31,17,113)


def check_pin(path, sha):
    data = path.read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == sha


def run(out):
    check_pin(ARCHIVE, "cd0687a1cb657a07e6adc04aa818f315cfe9105a")
    check_pin(FCV / "lineage.py", "e95e3e978779164dd91f09b80e3389247e6320c2")
    sys.path.insert(0, str(FCV.resolve()))
    from lineage import Carrier, Pruning
    with ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        raw_paths = z.read("fork_certificate.json")
        packet = json.loads(raw_paths)

    def carrier(m):
        return Carrier("fork-grade", tuple(k for v,k in enumerate(KEYS) if m & (1 << v)))

    def push(x, old, new):
        p = Pruning(carrier(old), carrier(new))
        raw = p.aggregate(tuple(x[KEYS.index(k)] for k in p.fine.keys))
        small = dict(zip(p.coarse.keys,raw,strict=True))
        return tuple(small.get(k,0) for k in KEYS)

    def conflicts(s, family):
        return [(i,j) for i in range(3) for j in range(i+1,3)
                if push(family[i],s[i],s[i]&s[j]) != push(family[j],s[j],s[i]&s[j])]

    def glue_add(x,old,new,other,y):
        # O2 on new = old union (other intersection new).
        overlap = other & new
        previous = overlap & old
        peer = push(y,other,overlap)
        agreed = push(x,old,previous)
        assert push(peer,overlap,previous) == agreed
        return tuple(a+b-c for a,b,c in zip(x,peer,agreed,strict=True))

    def replay(g, name, rule):
        paths = [PREP,*map(tuple,packet["cases"][name]["masks"])]
        grades = [push(g,127,m) for m in PREP]
        traces = []
        for index,(old,new) in enumerate(zip(paths, paths[1:])):
            i, = (i for i in range(3) if old[i]!=new[i])
            bit = old[i]^new[i]
            assert bit.bit_count()==1
            x = grades[i]
            if old[i]&bit:
                grades[i]=push(x,old[i],new[i])
            elif rule=="glue":
                candidates=[glue_add(x,old[i],new[i],old[j],grades[j])
                            for j in range(3) if j!=i and old[j]&bit]
                assert candidates and all(z==candidates[0] for z in candidates)
                grades[i]=candidates[0]
            # In the zero-inclusion control the padded vector already has a zero at the new site.
            assert sum(x)==sum(grades[i])
            bad=conflicts(new,grades)
            if rule=="glue":
                assert not bad and grades==[push(g,127,m) for m in new]
            traces.append({"i":index,"state":new,"grades":grades.copy(),"disagreements":bad})
        return traces

    def delta(v):
        return tuple(int(j==v) for j in range(7))
    probes=[delta(j) for j in range(7)]
    balanced=tuple(a-b for a,b in zip(delta(2),delta(3),strict=True))
    covector=[]
    diagnostics={}
    for j,g in enumerate(probes+[balanced]):
        results={}
        for name in ("junction","left_leaf"):
            for rule in ("glue","zero"):
                rows=replay(g,name,rule)
                common,=(r for r in rows if r["state"]==MEET)
                remaining=rows[common["i"]+1:]
                fifth=next(r for r in remaining if r["state"][1]!=17)
                results[name,rule]=(common,fifth,rows[-1])
                if g==balanced:
                    bad=[r["i"] for r in rows if r["disagreements"]]
                    assert bad == ([3,4,5] if (name,rule)==("left_leaf","zero") else [])
                    assert all(r["disagreements"]==[(0,1)] for r in rows if r["disagreements"])
                    diagnostics[name+"_"+rule]={"incompatible_steps":bad,"common_grades":common["grades"],
                        "states_with_disagreement":[r["state"] for r in rows if r["disagreements"]]}
        assert results["junction","glue"][0]["grades"]==results["left_leaf","glue"][0]["grades"]
        for t in (1,2):
            junction=results["junction","glue"][t]
            leaf=results["left_leaf","glue"][t]
            diff=leaf["grades"][1][0]-junction["grades"][1][0]
            assert diff==sum(g[4:])
            assert push(junction["grades"][1],junction["state"][1],1)==leaf["grades"][1]
        if j<7:
            covector.append(int(diff))
        else:
            assert results["junction","zero"][0]["grades"][0][2]==1
            assert results["left_leaf","zero"][0]["grades"][0][2]==0
            assert results["junction","zero"][0]["grades"][1:]==results["left_leaf","zero"][0]["grades"][1:]

    assert covector==[0,0,0,0,1,1,1]
    # Two nonnegative inputs separate in the junction arm and coalesce on A in the left-leaf arm.
    for name in ("junction","left_leaf"):
        histories=[replay(delta(v),name,"zero") for v in (2,3)]
        source_views=[next(r["grades"][0] for r in rows if r["state"]==MEET) for rows in histories]
        assert (source_views[0]==source_views[1])==(name=="left_leaf")
    out.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(diagnostics,sort_keys=True,indent=2,default=int)+"\n").encode()
    (out/"grade_certificate.json").write_bytes(raw)
    (out/"fork_paths.json").write_bytes(raw_paths)
    return {"basis_replays":7,"balanced_probe":"delta_2 - delta_3","initial_masks":PREP,"common_masks":MEET,
            "receiver_root_difference_leaf_minus_junction":covector,
            "left_leaf_zero_inclusion_conflicts":[3,4,5],"conflicting_indices":["A","B"],
            "first_conflict_masks":[23,15,115],"all_meeting_families_compatible_for_balanced_probe":True,
            "certificate_sha256":hashlib.sha256(raw).hexdigest()}


if __name__=="__main__":
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
