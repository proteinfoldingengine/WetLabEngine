#!/usr/bin/env python3
"""Bounded source interpretation check; no native correspondence is asserted."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
SOURCE = ROOT / "ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py"
SOURCE_BLOB = "8871e50f19322adbb62f34ea3837ba8e6cb16c8b"
FREEZE = "e8660972544938a08f701834cb0a2c4fddd1a7c6"
N, P, U = 4, 1, 2

def zero():
    return [[F(0) for _ in range(N)] for _ in range(N)]

def unit(i, j):
    a = zero()
    a[i][j] = F(1)
    return a

def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(N)] for i in range(N)]

def scale(c, a):
    return [[c * v for v in row] for row in a]

def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(N)), F(0))
             for j in range(N)] for i in range(N)]

def adj(a):
    return [list(row) for row in zip(*a)]

def tr(a):
    return sum((a[i][i] for i in range(N)), F(0))

def diag(vals):
    a = zero()
    for i, v in enumerate(vals):
        a[i][i] = F(v)
    return a

I = diag([1]*N)
Q = diag([1,1,0,1])
PU, PP = unit(U,U), unit(P,P)
K = unit(P,U)

def channel(a):
    return add(mul(mul(Q,a),Q), mul(mul(K,a),adj(K)))

def dual(f):
    return add(mul(mul(Q,f),Q),mul(mul(adj(K),f),K))

def expected_on_unit(i,j):
    # Independent coordinate-level P1 benchmark, not the Kraus implementation.
    if i == U or j == U:
        return unit(P,P) if i == j else zero()
    return unit(i,j)

def as_numpy(a):
    return np.array([[float(v) for v in row] for row in a],dtype=complex)

def run():
    data = SOURCE.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert blob == SOURCE_BLOB
    spec = importlib.util.spec_from_file_location("original_v1511_record_retention",SOURCE)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    errors = []
    def close(a,b):
        err = float(np.max(np.abs(np.asarray(a)-as_numpy(b))))
        errors.append(err)
        assert err < 1e-14, err

    units = [unit(i,j) for i in range(N) for j in range(N)]
    dual_checks = 0
    for i in range(N):
        for j in range(N):
            e = unit(i,j)
            assert channel(e) == expected_on_unit(i,j)
            # Reconstruct dual from all trace pairings and the coordinate rule.
            fdual = zero()
            for a in range(N):
                for b in range(N):
                    fdual[a][b] = tr(mul(e,expected_on_unit(b,a)))
            assert dual(e) == fdual
            assert fdual[P][P] == fdual[U][U]
            for x in units:
                assert tr(mul(e,channel(x))) == tr(mul(dual(e),x))
                dual_checks += 1

    assert channel(PP) == channel(PU) == PP
    assert dual(PP) == add(PP,PU)  # Positive complete-fiber control.
    assert dual(PU) == zero()     # Reject reuse of the original outcome effect.
    assert dual(Q) == I          # Q on output now always reads 1.
    assert PU[P][P] != PU[U][U] and Q[P][P] != Q[U][U]
    qn, pun, ppn = map(as_numpy,(Q,PU,PP))
    close(original.pinch(pun,[qn,pun]),PU)
    assert not original.refines(ppn,pun)
    assert not original.refines(pun,ppn)
    assert original.refines(ppn,qn)

    rows = []
    all_selected_u = []
    for nums, expected_q, expected_cp in [
        ([1,1,2,1],F(3,5),F(3,5)),
        ([1,1,1,2],F(4,5),F(2,5))
    ]:
        rho = diag([F(v,5) for v in nums])
        r = rho[U][U]
        q = 1-r
        assert q == expected_q
        sq = scale(1/q,mul(mul(Q,rho),Q))
        su = scale(1/r,mul(mul(PU,rho),PU))
        outu = mul(mul(K,su),adj(K))
        assert outu == PP
        assert channel(rho)[P][P] == expected_cp
        assert add(scale(q,sq),scale(r,outu)) == channel(rho)
        close(original.select_record(as_numpy(rho),[qn,pun],0),sq)
        old_u = original.select_record(as_numpy(rho),[qn,pun],1)
        close(old_u,su)
        close(as_numpy(K)@old_u@as_numpy(adj(K)),outu)
        all_selected_u.append(outu)
        rows.append({
            "q_weight":str(q),"u_weight":str(r),
            "nonselective_parent":str(channel(rho)[P][P]),
            "Q_conditioned_parent":str(sq[P][P]),
            "u_conditioned_parent":str(outu[P][P]),
        })
    assert all_selected_u[0] == all_selected_u[1]
    diffs = {key:str(F(rows[0][key])-F(rows[1][key]))
             for key in ("nonselective_parent","Q_conditioned_parent","u_conditioned_parent")}
    assert diffs == {"nonselective_parent":"1/5","Q_conditioned_parent":"1/12","u_conditioned_parent":"0"}
    assert SOURCE.read_bytes() == data
    return {
        "status":"PASS",
        "scope":"AUTHOR_CHECKED_APPLICATION_OF_EXISTING_FIBER_CRITERION",
        "native_event_binding":"NOT_DERIVED",
        "owner_access":"NOT_DERIVED",
        "independent_review":"NOT_REQUESTED_FOR_THIS_FOLLOWUP",
        "prior_review_does_not_cover_this_followup":True,
        "freeze_commit":FREEZE,
        "source_git_blob":blob,
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy_version":np.__version__,
        "matrix_units_checked":len(units),
        "exact_trace_pairings":dual_checks,
        "canonical_preparations":rows,
        "parent_contrasts":diffs,
        "old_pinch_preserves_u_effect":True,
        "C_dual_u_effect":"zero",
        "C_dual_Q_effect":"identity",
        "C_dual_parent_effect":"pi_p+pi_u",
        "pure_p_u_source_output_collision":True,
        "no_source_output_effect_recovers_original_binary_record":True,
        "u_to_p_is_original_projector_refinement":False,
        "Q_and_u_branch_outputs_both_supported_in_Q":True,
        "rejecting_controls":{
            "retain_original_u_effect":True,
            "identify_reset_as_projector_refinement":True,
            "claim_u_conditioned_canonical_separation":True
        },
        "original_source_numeric_comparisons":len(errors),
        "original_source_max_abs_error":max(errors),
        "original_source_bytes_unchanged":True,
        "scientific_breakthrough":False,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args()
    result = run()
    target = BASE/"record_retention_verification.json"
    if args.check:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
