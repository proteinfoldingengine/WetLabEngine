"""Trace a source-derived routing choice to an actual remote child and a retained bit."""
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
DEMOS = HERE.parents[2] / "demos"
OLD = "v16.48-recursive-chain-repair/"
ATOM = "v16.26-consistency-increment-law/"
X = tuple(range(9))
DEGREES = (2, 2, 2, 2)
P = (-1, 0, 1, 2, 3, 3, 2, 1, 0)
PREP = [257, 63, 455]
B = 1
Z = 7
ARCHIVE = OLD + "evidence/science/scientific/CERTIFICATE.json.gz"
PINS = {
    OLD+"producer.py": "7c4f65714d6b9ccda7f4bb0fc378b0daef957fff",
    OLD+"graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    OLD+"star_normalize.py": "d58cc9d1168d219b2869affd2d4ede889ebe579b",
    ARCHIVE: "ff8244239fb5ce092b07cbe775382593018b256d",
    ATOM+"engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    ATOM+"verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "v16.22-response-selection-closure/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
}

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, DEMOS / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def view(mask):
    return tuple(v for v in X if mask & 1 << v)

def exact(values):
    ints = tuple(map(int, values))
    assert all(x == i for x, i in zip(values, ints))
    return ints

def trace_normalize(machine, state, q):
    calls = []
    def watch(frame, event, returned):
        if event != "return" or frame.f_code is not machine.normalize.__code__:
            return
        parent = frame.f_back
        if parent.f_code.co_name != "inner":
            return
        outer = parent.f_back
        if outer.f_code is machine.normalize.__code__ and tuple(outer.f_locals["d"]) == DEGREES:
            values = frame.f_locals
            calls.append({"parent_labels": list(parent.f_locals["P"]), "raw_state": list(values["state"]),
                          "q": list(values["q"]), "returned_local_path": returned})
    old = sys.getprofile()
    try:
        sys.setprofile(watch)
        path = machine.normalize(state, DEGREES, 3, q)
    finally:
        sys.setprofile(old)
    call, = calls
    return path, call

def check_fields(green, overlap, states):
    full_green = green.candidate(P)
    assert full_green * green.root_laplacian(P) == sp.eye(8)
    def local_field(Y, grade):
        parents = tuple(-1 if v == 0 else Y.index(P[v]) for v in Y)
        marginal = overlap.push(P, X, Y, grade)
        rhs = sp.Matrix(len(Y)-1, 1, list(marginal[1:]))
        return (0,) + exact(green.candidate(parents) * rhs)
    for site in X[1:]:
        grade = tuple(int(v == site) - int(v == 0) for v in X)
        ambient = local_field(X, grade)
        assert ambient[Z] - ambient[P[Z]] == int(site == Z)
        for state in states:
            ys = list(map(view, state))
            current, field = ys[0], local_field(ys[0], grade)
            for other in ys[1:]:
                other_field = local_field(other, grade)
                field = overlap.glue_response(P, current, other, field, other_field)
                current = tuple(sorted(set(current) | set(other)))
            assert current == X and field == ambient
    high_before, high_after = [257,63,199], [257,191,199]
    V = view(high_before[2])
    assert high_before[2] == high_after[2] and Z in V
    def represent(Y, grade):
        local = dict(zip(Y, overlap.push(P, X, Y, grade)))
        return tuple(local.get(v, 0) for v in X)
    functional = []
    for site in X:
        grade = tuple(int(v == site) for v in X)
        old, new = view(high_before[B]), view(high_after[B])
        old_joint, new_joint = (tuple(sorted(set(Y) & set(V))) for Y in (old, new))
        diff = tuple(a-b for a,b in zip(represent(new, grade),represent(old, grade)))
        redundant = tuple(a-b for a,b in zip(represent(new_joint, grade),represent(old_joint, grade)))
        expected = tuple(grade[Z] * (int(v == Z) - int(v == P[Z])) for v in X)
        assert diff == redundant == expected
        response = local_field(V, tuple(map(int, diff)))
        functional.append(int(response[V.index(Z)] - response[V.index(P[Z])]))
    assert functional == [int(v == Z) for v in X]
    losses = []
    for actor in (0, 2):
        Y = view(PREP[actor])
        coarse = tuple(v for v in Y if v != 8)
        g = (1,) * len(X)
        fine_rep, reduced_rep = represent(Y,g), represent(coarse,g)
        loss = exact([a-b for a,b in zip(fine_rep,reduced_rep)])
        assert loss == (-1,0,0,0,0,0,0,0,1)
        field = local_field(X, loss)
        assert field[8] - field[0] == 1 and field[Z]-field[P[Z]] == 0
        losses.append({"lost_source": loss, "field": field})
    return {"edge": [P[Z],Z], "basis_drives": 8, "distinct_states": len(states),
            "whole_field_equalities": 8*len(states), "nonzero_common_field_residuals": 0,
            "unit_local_drive_drop": 1, "source_atom_loss_and_field_A_C": losses,
            "first_high_B_edit_port_functional":functional, "overlap_residual":0}

def main():
    for path, expected in PINS.items():
        raw = (DEMOS/path).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest() == expected
    sys.path.insert(0, str(DEMOS/OLD))
    machine = module(OLD+"producer.py","chain_machine")
    atom = module(ATOM+"engine.py","chain_atom")
    verifier = module(ATOM+"verify.py","chain_atom_verify")
    green = module("v16.22-response-selection-closure/engine.py","chain_green")
    overlap = module("v16.23-overlap-descent/engine.py","chain_overlap")
    raw = (DEMOS/ARCHIVE).read_bytes()
    archive = json.loads(gzip.decompress(raw))
    fresh = machine.produce()
    assert json.loads(json.dumps(fresh)) == archive
    entry = archive["entries"][1]
    graph = entry["graph"]
    states = graph["states"]
    assert len(states) == 34321 and len(entry["normalizations"]) == 41
    assert graph["parents"] == list(P) and entry["degrees"] == list(DEGREES) and states[14730] == PREP
    root_rows = entry["normalizations"]
    def profile(i):
        return graph["attained_profiles"][graph["profile_ids"][i]]
    result = {}
    paths = {}
    for name, actor, row, i in (("delete_A",0,2,8),("delete_C",2,33,14725),("no_deletion",None,None,14730)):
        ys = list(map(view, PREP))
        if actor is not None:
            event = atom.atomic(P,ys,actor,8)
            verifier.verify_atomic(event)
            ys = event["after"]
        start = [sum(1<<v for v in y) for y in ys]
        assert start == states[i] and start[B] == PREP[B]
        assert [((m>>1)&127) for m in start] == [0,31,99]
        q = profile(i)
        assert [atom.tau_at(P,ys,v) for v in X] == q
        path, call = trace_normalize(machine, start, q)
        if row is None:
            assert not any(r["state"]==i for r in root_rows)
        else:
            original = root_rows[row]
            assert original["state"] == i and original["q"] == q
            assert path == [states[j] for j in original["path"]]
        assert call["q"] == [1,2,1]
        expected = [31,99] if actor == 2 else [1,31,99]
        assert call["raw_state"] == expected
        bits = [int(bool(s[B] & 1<<Z)) for s in path]
        assert bits == ([0]+[1]*(len(path)-1) if actor == 2 else [0]*len(path))
        if actor != 2:
            assert all(s[B]==63 for s in path)
        paths[name]=path
        result[name] = {"archive_normalization":row,"state_id":i,"start":start,"q":q,"whole_moves":len(path)-1,
                        "B_at_v7_including_start":bits,"end":path[-1],"fixed_child_v1":call}
    low, high = paths["delete_A"], paths["delete_C"]
    assert len(low)==len(high)==11 and low[1]==PREP and low[2]==high[0] and low[3]!=high[1]
    assert high[1]==[257,191,199] and low[-1]==[455,63,1] and high[-1]==[257,199,63]
    assert trace_normalize(machine, low[2], profile(14725))[0]==high
    assert paths["no_deletion"]==low[1:]
    distinct = sorted({tuple(s) for row in paths.values() for s in row})
    result={"archive_sha256":hashlib.sha256(raw).hexdigest(),"unchanged_default_producer_matches_full_archive":True,
            "complete_domain_entries":len(archive["entries"]),"directed_corpus_cases":len(archive["corpus"]),
            "graph_states":len(states),"archived_calls_in_selected_tree":len(root_rows),"arms":result,
            "coalesced_state_after_2_low_moves":low[2],"restart_with_recomputed_q_reproduces_high":True,
            "common_field":check_fields(green,overlap,distinct),"native_physical_activation_and_access":"OPEN"}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=="__main__":
    main()
