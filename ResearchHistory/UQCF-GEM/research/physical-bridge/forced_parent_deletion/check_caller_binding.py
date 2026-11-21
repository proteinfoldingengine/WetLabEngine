"""Trace the archived caller and exhaust its matched seed domain."""
import ast
from fractions import Fraction
import itertools
import json
from pathlib import Path
import sys

import numpy as np
import check_bracket_ports as archive


def run():
    root = Path(__file__).resolve().parents[5]
    path = root / archive.HISTORICAL_PATH
    native = archive.original_functions(path)
    default = native["build_base"]()
    assert default["branches"][0][0] == -9
    keys = tuple(default["gates"])
    index = keys.index("g1234r")
    assert index == 17
    assert [pair for pair in itertools.product(range(2,13),range(3,10))
            if Fraction(*pair)==3] == [(9,3),(12,4)]

    # Every integer seed is equivalent to one representative here.
    period = 29 * 11 * 7
    matching = [s for s in range(period)
                if np.array_equal(native["values_for_mask"](native["MASKS"]["J1"],"j1",s),
                                  default["branches"][0])
                and native["gate_values"](s)["g1234r"]==3]
    exact_residues = [s for s in range(period)
                      if s % 29 == 1 and (s%11,(s+34)%7) in ((1,0),(4,1))]
    # First-coordinate negative grade excludes the fallback for a raw zero.
    # 5(seed+3)+14 == 5 (mod 29), leaving seed == 1 (mod 29).
    assert matching == exact_residues and len(matching)==2

    results = []
    for s in matching:
        state = native["build_base"](s)
        assert all(np.array_equal(a,b) for a,b in zip(state["branches"],default["branches"]))
        j1,j2,j3,j4 = [np.array([int(t) for t in xs],dtype=object) for xs in state["branches"]]
        gates = {k:Fraction((i+s)%11+2,(2*i+s)%7+3) for i,k in enumerate(keys)}
        assert {k:float(v) for k,v in gates.items()} == state["gates"]
        R = native["recombine"]
        q3 = R(R(j2,j3,gates["g23"]),j4,gates["g234"])
        q4 = R(j2,R(j3,j4,gates["g34"]),gates["g234"])
        probe = j1.copy()
        for symbol,q in (("B3",q3),("B4",q4)):
            observed = []
            for index in (2,1):
                probe[:] = j1
                probe[index] += 1
                probe[10] -= 1
                delta = R(probe,q,Fraction(3)) - R(j1,q,Fraction(3))
                assert delta[index+1] == 3*q[index+1]
                observed.append(str(delta[index+1]))
            results.append({"seed":s,"grouping":symbol,"input_2_to_3_and_1_to_2_slopes":observed,
                            "operand":list(map(str,q)),
                            "inner_gates":[str(gates[k]) for k in ("g23","g34","g234")]})

    # Check the independent mask rejection on every B4 two-prune scalar hit.
    assessed = json.loads((Path(__file__).parent/"evidence/two_prunes/result.json").read_text())
    witnesses = []
    for hit in assessed["B4"]["scalar_hits"]:
        copied = np.array(default["branches"][1:],copy=True)
        for k,u,p in hit["edits"]:
            copied[k,p] += copied[k,u]
            copied[k,u] = 0
        masks = [native["MASKS"][k] for k in ("J2","J3","J4")]
        mismatch = [(k+2,i) for k,mask in enumerate(masks) for i,m in enumerate(mask)
                    if bool(copied[k,i]) != bool(m)]
        assert mismatch
        witnesses.append({"edits":hit["edits"],"different_support_slots":mismatch})

    # Observe calls from the actual original audit. It consumes all stored bracket results,
    # including B3 and B4, after build_base supplies them.
    syntax = ast.parse(path.read_bytes())
    assignments = {ast.unparse(n) for n in syntax.body if isinstance(n,ast.Assign)}
    assert "base = build_base()" in assignments
    assert "algebra_audit = algebra_generator_audit(P, base)" in assignments
    native["EPS"] = 1e-8
    projection,_,_ = native["H4_residual_projection"](default)
    assert all(np.allclose(projection @ j,j,rtol=0,atol=1e-9) for j in default["branches"])
    audit_function = native["algebra_generator_audit"]
    code = native["recombine"].__code__
    seen = set()
    def trace(frame,event,arg):
        if event == "call" and frame.f_code is code and frame.f_back.f_code is audit_function.__code__:
            for operand in ("x","y"):
                field = frame.f_locals[operand]
                for key in (archive.LEFT,archive.RIGHT):
                    if field is default["bracketings"][key]:
                        seen.add(key)
    before = sys.getprofile()
    try:
        sys.setprofile(trace)
        later = audit_function(projection,default)
    finally:
        sys.setprofile(before)
    assert seen == {archive.LEFT,archive.RIGHT}
    print(json.dumps({"source_blob":archive.PIN,"seed_period":period,"matched_seeds":matching,
                      "responses":results,"b4_support_rejections":witnesses,
                      "original_later_audit":{"directly_read_bracket_outputs":sorted(seen),
                                             "pair_count":later["generated_pair_tests"]}},
                     indent=2,sort_keys=True))


if __name__=="__main__":
    run()
