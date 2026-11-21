"""Replay two archived V1687.16 bracketings at their identical outer coordinate pair."""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp


HISTORICAL_PATH = Path("Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/H4_rock_test/v1687_16.py")
PIN = "090a03bf665b97d7784f688c8294a348ad20507f"
LEFT = "B3_(1((23)4))"
RIGHT = "B4_(1(2(34)))"
N = 12
I, J = 3, 2


def original_functions(path):
    raw = path.read_bytes()
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == PIN
    # The historical file writes to /home/claude at import. Load its original
    # functions and its static branch masks, without running unrelated audits.
    syntax = ast.parse(raw, filename=str(path))
    assert any(isinstance(node, ast.Assign) and ast.unparse(node) == "base = build_base()"
               for node in syntax.body)
    syntax.body = [node for node in syntax.body if isinstance(node, ast.FunctionDef)
                   or (isinstance(node, ast.Assign)
                   and any(isinstance(key, ast.Name) and key.id == "MASKS" for key in node.targets))]
    native = {"np": np, "sp": sp, "N": N}
    exec(compile(syntax, str(path), "exec"), native)
    return native


def apply_exact(x, y, gate):
    # Independent coordinate form, including the opposite directions of the rolls.
    return [x[i]+y[i]+gate*(x[(i-1)%N]*y[i]-x[i]*y[(i+1)%N]) for i in range(N)]


def contrast_matrix(q3, q4, gamma):
    delta = [a-b for a,b in zip(q3,q4)]
    return [[gamma*((delta[i] if j==(i-1)%N else 0)
                    -(delta[(i+1)%N] if j==i else 0)) for j in range(N)] for i in range(N)]


def response_records(native, branches, gates, left_gate, right_gate, nest_gate):
    x,b,c,d = branches
    gamma = gates["g1234r"]
    q3 = apply_exact(apply_exact(b,c,left_gate),d,nest_gate)
    q4 = apply_exact(b,apply_exact(c,d,right_gate),nest_gate)
    g = dict(gates, g23=left_gate, g34=right_gate, g234=nest_gate)
    arr = [np.array(v,dtype=object) for v in branches]
    def raw_brackets(a):
        out = native["bracket4_all"]([a,*arr[1:]],g)
        return out[LEFT],out[RIGHT]
    left, right = raw_brackets(arr[0])
    assert list(left)==apply_exact(x,q3,gamma) and list(right)==apply_exact(x,q4,gamma)
    matrix = contrast_matrix(q3,q4,gamma)
    for j in range(N):
        a = arr[0].copy()
        a[j] += 1
        p,m = raw_brackets(a)
        observed = (p-left)-(m-right)
        assert list(observed) == [row[j] for row in matrix]
        assert sum(observed)==0
    # A charge-neutral probe leaves total input fixed. The compensating site 10
    # lies outside rows 2 and 3's stencil. Use two finite signed magnitudes.
    slopes = [gamma*q3[I],gamma*q4[I]]
    diagonal = [1-gamma*q3[I],1-gamma*q4[I]]
    for h in (Fraction(1,2),Fraction(-3,4)):
        a = arr[0].copy()
        a[J] += h
        a[10] -= h
        p,m = raw_brackets(a)
        assert [(p[I]-left[I])/h,(m[I]-right[I])/h] == slopes
        assert [(p[J]-left[J])/h,(m[J]-right[J])/h] == diagonal
        assert (p[I]-left[I])-(m[I]-right[I]) == h*matrix[I][J]
    encode=lambda xs:[str(y) for y in xs]
    return {
        "q3":encode(q3),"q4":encode(q4),
        "slope_input2_output3":encode(slopes),"slope_input2_output2":encode(diagonal),
        "contrast_input2_output3":str(matrix[I][J]),"contrast_input2_output2":str(matrix[J][J]),
        "outer_outputs_3":encode([left[I],right[I]]),
        "outer_outputs_2":encode([left[J],right[J]]),
        "contrast_matrix_rows":[encode(row) for row in matrix],
        "rank":int(sp.Matrix(matrix).rank()),
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path)
    args=parser.parse_args()
    assert __debug__, "Requires unoptimized Python"
    default=Path(__file__).resolve().parents[5]/HISTORICAL_PATH
    native=original_functions(args.source or default)
    baseline=native["build_base"]()
    branches=[[int(t) for t in branch] for branch in baseline["branches"]]
    assert all(np.array_equal(branch,exact) for branch,exact in zip(baseline["branches"],branches))
    # Independently reconstruct gate_values() default seed 1 and check float images.
    gates={name:Fraction((idx+1)%11+2,(2*idx+1)%7+3) for idx,name in enumerate(baseline["gates"])}
    assert {name:float(value) for name,value in gates.items()} == baseline["gates"]
    assert [gates[k] for k in ("g23","g34","g234","g1234r")] == [Fraction(2,3),Fraction(8,7),1,3]
    record=response_records(native,branches,gates,gates["g23"],gates["g34"],gates["g234"])
    assert record["slope_input2_output3"]==["-63","-270"] and record["contrast_input2_output3"]=="207"
    assert record["slope_input2_output2"]==["64","271"] and record["contrast_input2_output2"]=="-207"
    assert record["rank"]==10
    # Use the original float inputs and its true default gate dictionary as well.
    origin=baseline["bracketings"]
    for sign in (1,-1):
        modified=[branch.copy() for branch in baseline["branches"]]
        modified[0][2]+=sign*0.5
        modified[0][10]-=sign*0.5
        new=native["bracket4_all"](modified,baseline["gates"])
        for i,key in enumerate((LEFT,RIGHT)):
            assert np.isclose((new[key][I]-origin[key][I])/(sign*0.5),
                              float(Fraction(record["slope_input2_output3"][i])),rtol=0,atol=1e-8)
    variants={}
    for gate in (Fraction(0),Fraction(1,2),Fraction(1),Fraction(-1)):
        row=response_records(native,branches,gates,gate,gate,gate)
        assert Fraction(row["contrast_input2_output3"])==207*gate**2
        assert row["rank"] == (0 if gate==0 else 8)
        variants[str(gate)]=row
    # Supplying the same effective right operand in both arms makes every entry zero.
    q3 = [Fraction(t) for t in record["q3"]]
    assert all(not value for row in contrast_matrix(q3,q3,gates["g1234r"]) for value in row)
    print(json.dumps({
        "source_blob":PIN,"historical_source_mode":"build_base() with seed=1",
        "archived_branch_comparisons":[LEFT,RIGHT],"port_indexing":"zero-based",
        "supplied_probe":"+h at 2, -h at 10; read 3 and 2",
        "archived":record,"matched_inner_gates":variants,"same_right_operand_control":"zero matrix",
        "column_sums":"zero for each impulse in every arm contrast",
        "physical_event_and_observable":"OPEN",
    },indent=2,sort_keys=True))


if __name__=="__main__":
    main()
