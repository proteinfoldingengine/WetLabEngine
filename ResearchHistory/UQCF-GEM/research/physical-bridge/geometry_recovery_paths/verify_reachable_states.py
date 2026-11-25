"""Check the generator sets and an actual error-free, persistent local record witness."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

from check_receiver_command import FIXTURE, PINS, hash_blob


def encoded(values):
    return sha256(json.dumps(sorted(values),separators=(",",":")).encode()).hexdigest()


def run(sources, primary):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f

    m = f.modules()
    features, _ = f.fixture()
    parents, grades, supports = map(tuple,zip(*features))
    a,b,p,q,r = (primary[k] for k in ("A","B","p","q","r"))
    all_rows = f.initial_state(features)
    assert all(parents[v] == 0 for v in all_rows[b] if v)
    other = primary["unrelated_receiver_unit"]

    def drop(rows,i,v):
        event = m["atom"].atomic(parents,rows,i,v)
        m["verify"].verify_atomic(event)
        return tuple(map(tuple,event["after"]))

    reports = {}
    for name in ("original","balanced"):
        current = [set(h) for h in supports]
        if name == "balanced":
            for i in primary["other_holders"]:
                current[q].remove(i)
                current[r].remove(i)
        rows = tuple(tuple(v for v,h in enumerate(current) if i in h) for i in f.LABELS)
        families, traces, data = {}, {}, {}
        for x in (p,q):
            after = drop(rows,a,x)
            outside = set().union(*(y for i,y in enumerate(after) if i!=b))
            local = set(after[b])
            removable = (local & outside) - {0}
            fixed = local - removable
            # Independent per-leaf owner construction from the source-event support.
            alternate = {v for v,h in enumerate(current) if v and b in h
                         and (h - {b} - ({a} if v == x else set()))}
            assert alternate == removable and rows[b] == after[b]
            assert len(removable) == primary["arms"][name]["source_arms"][str(x)]["B_menu_size"]
            families[x] = removable
            data[str(x)] = {"free":len(removable),"fixed":sorted(fixed),
                            "free_ids_sha256":encoded(removable)}
            # The same successful unrelated receiver action leaves q present in both arms.
            neutral = drop(after,b,other)
            assert q in neutral[b]
            traces[x] = neutral[b]
            if q in removable:
                witness = drop(after,b,q)
                assert q not in witness[b] and set(witness[b]) == local-{q}
                # Show an actual later successful local edit; the general persistence proof is monotonicity.
                later = drop(witness,b,other)
                assert q not in later[b] and set(later[b]) == local-{q,other}
                data[str(x)].update(witness="success",local_after_q=encoded(witness[b]),
                                     local_after_q_then_other=encoded(later[b]))
            else:
                try:
                    m["atom"].atomic(parents,after,b,q)
                except ValueError as exc:
                    assert str(exc) == "same union"
                else:
                    raise AssertionError("Forbidden receiver command succeeded")
                data[str(x)]["witness"] = "no returned state"
        assert traces[p] == traces[q]
        extras = sorted(families[p]-families[q])
        assert not families[q]-families[p] and extras == ([q] if name=="balanced" else [])
        reports[name] = {"view_12_size":len(rows[b]),"free_only_after_p":extras,
                         "arms":data,"common_actual_row_after_unrelated":encoded(traces[p])}
    return {"schema":"reachable-B-sets/1","source_p":p,"source_q":q,
            "receiver":b,"unrelated_command":other,"preparations":reports,
            "balanced_free_exponents":[1305,1304],"counts_are":"distinct existential memberships",
            "uncertain_if_q_present":True,"only_p_if_q_absent_in_balanced_case":True}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    sources, core, output = (Path(p).resolve() for p in sys.argv[1:])
    result=run(sources,json.loads(core.read_bytes()))
    raw=(json.dumps(result,sort_keys=True,indent=2)+"\n").encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({"sha256":sha256(raw).hexdigest(),"bytes":len(raw),"free_exponents":result["balanced_free_exponents"]}))
