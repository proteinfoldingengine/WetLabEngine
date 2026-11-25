"""Compare every nonsource command menu with the measured work-row changes."""
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import sys

from check_receiver_command import FIXTURE, PINS, hash_blob


def identify(scores, labels, editor, leaf, squared):
    if set(scores) != set(labels) - {editor} or set(scores.values()) - {-squared,squared}:
        raise ValueError("incomplete or malformed work-row change")
    positive = sorted(j for j, value in scores.items() if value > 0)
    if not positive:
        raise ValueError("union would be lost")
    return positive, [(positive[0],leaf)] if len(positive) == 1 else []


def run(sources, primary):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f

    m = f.modules()
    features, _ = f.fixture()
    parents, grades, _ = map(tuple,zip(*features))
    totals = list(grades)
    for v in range(len(parents)-1,0,-1):
        totals[parents[v]] += totals[v]
    a, labels = f.A, f.LABELS
    p,q,r = (primary[key] for key in ("p","q","r"))
    outsiders = primary["other_holders"]
    initial = f.initial_state(features)
    weights = {}
    for v in range(1,len(parents)):
        squared = totals[v] ** 2
        weights[squared] = weights.get(squared,0) | (1 << v)

    def work_row(rows):
        masks = [sum(1 << v for v in row if v) for row in rows]
        return {j:sum(w * ((masks[a] ^ masks[j]) & mask).bit_count() for w,mask in weights.items())
                for j in labels if j != a}

    def menus(rows):
        supports = Counter(v for row in rows for v in row)
        answer = {}
        for i,row in enumerate(rows):
            if i != a:
                nonleaves = {parents[v] for v in row}
                answer[i] = {v for v in row if v != 0 and v not in nonleaves and supports[v] > 1}
        return answer

    comparisons = {}
    for name, cols in (("original",()),("isolated",(q,)),("balanced",(q,r))):
        rows = tuple(tuple(v for v in row if i not in outsiders or v not in cols)
                     for i,row in enumerate(initial))
        w_before, menu_before = work_row(rows), menus(rows)
        results = {}
        for leaf in (p,q,f.T):
            assert leaf not in parents and totals[leaf] > 0
            event = m["atom"].atomic(parents, rows, a, leaf)
            m["verify"].verify_atomic(event)
            after = tuple(map(tuple,event["after"]))
            w_after, menu_after = work_row(after), menus(after)
            diffs = {j:w_after[j]-old for j,old in w_before.items()}
            positives, expected = identify(diffs,labels,a,leaf,totals[leaf]**2)
            holders = [j for j in labels if j != a and leaf in after[j]]
            lost = sorted((j,v) for j,menu in menu_before.items() for v in menu-menu_after[j])
            assert all(menu_after[j] <= menu for j,menu in menu_before.items())
            assert holders == positives and lost == expected
            assert len(positives) + sum(d < 0 for d in diffs.values()) == 24
            assert w_after[f.B] == primary["arms"][name]["source_arms"][str(leaf)]["work_AB"]
            for owner, site in expected:
                before_probe = m["atom"].atomic(parents,rows,owner,site)
                m["verify"].verify_atomic(before_probe)
                try:
                    m["atom"].atomic(parents,after,owner,site)
                except ValueError as exc:
                    assert str(exc) == "same union"
                else:
                    raise AssertionError("Predicted command veto passed the native atom")
            missing = {j:d for j,d in diffs.items() if j != 1}
            try:
                identify(missing,labels,a,leaf,totals[leaf]**2)
            except ValueError as exc:
                assert "incomplete" in str(exc)
            else:
                raise AssertionError("Missing row entry admitted")
            reversed_signs = {j:-v for j,v in diffs.items()}
            assert identify(reversed_signs,labels,a,leaf,totals[leaf]**2)[0] != holders
            assert sorted([*lost,(1,leaf)]) != expected
            results[str(leaf)] = {"positive_labels":positives, "negative_labels":sorted(set(diffs)-set(positives)),
                                  "magnitude":totals[leaf]**2, "lost_commands":lost}
        comparisons[name] = results
    return {"schema":"work-row-coverage/1","comparisons":comparisons,"nonsource_menus_compared":9*24,
            "controls":["missing_row_entry","reversed_signs","spurious_lost_command"]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    sources, primary, output = (Path(p).resolve() for p in sys.argv[1:])
    resource.setrlimit(resource.RLIMIT_AS,(1_500_000_000,1_500_000_000))
    report=run(sources,json.loads(primary.read_bytes()))
    raw=(json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({"sha256":sha256(raw).hexdigest(),"bytes":len(raw),
                      "nonsource_menus_compared":report["nonsource_menus_compared"]}))
