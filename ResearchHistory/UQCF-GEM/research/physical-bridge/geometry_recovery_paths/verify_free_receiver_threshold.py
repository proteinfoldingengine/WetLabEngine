"""Check the increment capacities and the two last-step outcomes directly from fine-tip support."""
from collections import defaultdict
from pathlib import Path
import sys
from free_receiver_io import FIXTURE,module,read_xz,require,same,save


def reconstruct(features):
    grades=[entry[1] for entry in features]
    B={i for i,(_,_,h) in enumerate(features) if 12 in h and i}
    root=sum(grades)-sum(grades[v] for v in B)
    local_ones={v for v in B if grades[v]==1}
    require(all(features[v][0]==0 for v in B) and not any(p in B for p,g,h in features),"chart geometry")
    expected=[]
    for mode in ("original","balanced"):
        for cut in (662,718):
            allowed=defaultdict(list)
            for v in sorted(B):
                h=set(features[v][2])
                if mode=="balanced" and v in (46,718): h&={0,8,12,13}
                if v==cut: h.discard(0)
                if h-{12}: allowed[grades[v]].append(v)
            prefix=[v for v in allowed[1] if v!=718]
            left=sorted(set(allowed[1])-set(prefix))
            middle=root+len(prefix)
            def read(v):
                return dict(status="success",root=middle+grades[v],nonroot_units=len(local_ones)-len(prefix)-(grades[v]==1),
                            receiver_count=len(B)-len(prefix)-1)
            alternative=min(v for g,vs in allowed.items() if g>1 for v in vs)
            expected.append(dict(mode=mode,cut=cut,quota=[[g,len(vs)] for g,vs in sorted(allowed.items())],
                prior_units=len(local_ones),prefix=prefix,root_after_prefix=middle,remaining_units=left,
                unit=read(718) if left else dict(status="same union"),nonunit_vertex=alternative,nonunit=read(alternative)))
    return expected


def verify(records,expected):
    same(records,expected,"every addressed common-prefix and decisive numerical field")
    old,control,first,second=records
    require(old["quota"]==control["quota"],"baseline grade-word controls")
    cap1,cap2=map(dict,(first["quota"],second["quota"]))
    require(set(cap1)==set(cap2) and {g:cap1[g]-cap2[g] for g in cap1 if cap1[g]!=cap2[g]}=={1:1},"one-unit change")
    require(first["prefix"]==second["prefix"] and len(first["prefix"])==cap2[1],"same maximal common unit word")
    require(first["unit"]["status"]=="success" and second["unit"]=={"status":"same union"} and
            first["nonunit"]==second["nonunit"] and first["unit"]["nonroot_units"]==1,
            "positive word and matched nonunit control")


if __name__=="__main__":
    root,data=map(Path,sys.argv[1:])
    f=module(root,FIXTURE,"threshold_verifier_fixture","3324c0b46e09120ae526338444a19070b692d049")
    expected=reconstruct(f.fixture()[0])
    records=read_xz(data/"free_receiver_threshold.json.xz")
    verify(records,expected)
    a,b=records[2:]
    changes=[("prefix",a["prefix"][:-1]),("quota",b["quota"]),("unit",b["unit"]),
             ("nonunit",{"status":"same union"}),("remaining_units",[])]
    for k,value in changes:
        try: verify([*records[:2],{**a,k:value},b],expected)
        except ValueError: continue
        raise ValueError("accepted wrong "+k)
    result=dict(shortest_increment_word=dict(a["quota"])[1],common_unit_prefix=len(a["prefix"]),
                first_positive_root=a["unit"]["root"],root_after_common_prefix=a["root_after_prefix"],
                initial_unit_atoms=a["prior_units"],remaining_unit_atoms=a["unit"]["nonroot_units"],
                next_nonunit=a["nonunit"]["root"],rejecting_controls=len(changes))
    save(data/"free_receiver_lengths.json",result)
    print(result)
