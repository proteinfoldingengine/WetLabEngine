"""Trace the actual C ownership read, grade relay to A, and its first free amplitude."""
import gzip
import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache

import sympy as sp

import check_fixed_donor as fixed
import check_routed_chain as chain
from check_source_handoff import edits

A, B, C, D = range(4)
SITE = 9
CASES = (178, 184, 190)


def read_and_replay(machine, star, row):
    """Observe existing returns without changing indexing, arguments or code."""
    events = []
    def profile(frame, event, result):
        if event != "return" or frame.f_globals is not star.__dict__:
            return
        fn = frame.f_code.co_name
        if fn not in ("support", "change"):
            return
        outer = frame.f_back
        while outer and outer.f_code is not star.normalize.__code__:
            outer = outer.f_back
        if not outer or outer.f_locals.get("state") != [1, 1, 5, 3]:
            return
        completed = len(outer.f_locals["path"]) - 1
        info = frame.f_locals
        if fn == "support" and info["v"] == 1:
            events.append([completed,"read",result.copy(),frame.f_back.f_code.co_name,frame.f_back.f_lineno])
        if fn == "change":
            events.append([completed,"edit",info["j"],info["v"],info["add"]])
    spec = row["spec"]
    prior = sys.getprofile()
    try:
        sys.setprofile(profile)
        replay = machine.normalize(row["start"],spec["degrees"],spec["k"],spec["q"])
    finally:
        sys.setprofile(prior)
    assert replay == row["path"]
    gate = [event for event in events if 8 <= event[0] <= 10]
    assert gate[1:] == [[8,"read",[C],"recolor",23], [9,"edit",A,1,True],
                        [10,"edit",C,1,False], [10,"read",[A],"<listcomp>",21]] or (
        gate[1:] == [[8,"read",[C],"recolor",23], [9,"edit",A,1,True],
                     [10,"edit",C,1,False], [10,"read",[A],"colors",21]])
    assert gate[0] == [8,"edit",A,2,False]
    # Python 3.12 inlines list comprehensions; preserve stable scientific output.
    return {"support_return_at_state8":[C],"caller":"recolor:23",
            "subsequent_global_edits":["+A9","-C9"],"support_return_at_state10":[A]}


@lru_cache(None)
def push_rows(parents, mask):
    rows = {v: [0]*len(parents) for v in range(len(parents)) if mask >> v & 1}
    for v in range(len(parents)):
        w = v
        while w not in rows:
            w = parents[w]
        rows[w][v] = 1
    return rows


def arbitrary_histories(parents, path):
    # A distinct ambient vector at every state parametrizes compatible chart
    # marginals by O2; W1 equates only the projections for unchanged charts.
    n = len(parents)
    width = n * len(path)
    constraints = []
    def functional(t, row):
        return [0]*(t*n) + list(row) + [0]*(width-(t+1)*n)
    def chart(t, j, v):
        return sp.Matrix(functional(t,push_rows(parents,path[t][j])[v]))
    for t,(old,new) in enumerate(zip(path,path[1:])):
        for m,other in zip(old,new):
            if m != other:
                continue
            for row in push_rows(parents,m).values():
                constraints.append([x-y for x,y in zip(functional(t,row),functional(t+1,row))])
    matrix = sp.Matrix(constraints)
    kernel = matrix.nullspace()
    def original(v):
        return sp.Matrix(functional(0,[int(z==v) for z in range(n)]))
    source = original(SITE)
    plus = original(0) + original(10) + source
    forms = [(f"C9_state{t}",chart(t,C,SITE)-source) for t in range(5,10)]
    forms.extend([(f"A9_state{t}",chart(t,A,SITE)-source) for t in (9,10)])
    forms.extend([("Croot_before_gain",chart(4,C,0)-plus),
                  ("Croot_after_gain",chart(5,C,0)-plus+source),
                  ("Croot_after_release",chart(10,C,0)-plus)])
    for name, f in forms:
        assert all(f.dot(k)==0 for k in kernel),name
    assert any((chart(11,A,SITE)-source).dot(k)!=0 for k in kernel)
    return {"protected": [name for name,_ in forms], "rows":matrix.rows,
            "rank":width-len(kernel),"ambient_unknowns":width,"A9_free_at_state":11}


def counterhistory(native, parents, path):
    n = len(parents)
    sites = tuple(range(n))
    base = (2,) * n
    shifted = tuple(Fraction(2)+Fraction((v==SITE)-(v==0),2) for v in sites)
    views = [tuple(tuple(v for v in sites if m >> v & 1) for m in state) for state in path]
    # The two histories share exactly the same full initial source. Only the second
    # changes ambient representative, at the edit of the sole holder of site 9.
    evidence = []
    for switches in (False, True):
        previous = None
        values = []
        for t,family in enumerate(views):
            g = shifted if switches and t>=11 else base
            grades = tuple(native.push(parents,sites,view,g) for view in family)
            assert native.glue_many(parents,family,grades)==g
            if previous is not None:
                assert all(grades[j]==previous[j] for j in range(4) if family[j]==views[t-1][j])
            if t in (9,10,11):
                values.append(str(grades[A][family[A].index(SITE)]))
            previous = grades
        evidence.append(values)
    assert evidence == [["2","2","2"],["2","2","5/2"]]
    return evidence


def main():
    if not __debug__:
        raise ValueError("Checks require Python assertions")
    fixed.pins()
    raw = (chain.DEMOS/chain.ARCHIVE).read_bytes()
    assert fixed.blob(raw)==chain.PINS[chain.ARCHIVE]
    sys.path.insert(0,str(chain.DEMOS/chain.OLD))
    import producer
    import star_normalize
    native = chain.module("v16.23-overlap-descent/engine.py","relay_exact_p1")
    corpus = json.loads(gzip.decompress(raw))["corpus"]
    results = []
    for case in CASES:
        row = corpus[case]
        path = row["path"]
        p = tuple(producer.graph.parents(producer.tree(row["spec"]["degrees"])))
        tape = list(edits(path))
        assert tape[2:11]==[(B,9,True),(D,9,False),(C,9,True),(B,9,False),
                            (B,10,True),(A,10,False),(A,9,True),(C,9,False),(A,1,True)]
        results.append({"case":case,"ownership_read":read_and_replay(producer,star_normalize,row),
                        "exact_w1_w2":arbitrary_histories(p,path[:12]),
                        "same_initial_source_A9_at_states_9_10_11":counterhistory(native,p,path)})
    print(json.dumps({"archive":chain.PINS[chain.ARCHIVE],"cases":results},sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
