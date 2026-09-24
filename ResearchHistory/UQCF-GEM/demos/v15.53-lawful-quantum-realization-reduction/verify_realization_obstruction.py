"""v15.53 Task 6: independent finite semantic verifier.

This module intentionally does not import realization_family, reduction,
equivalence, or witness_search.  It reconstructs the frozen family and
recomputes admissibility, retained reduction, structural equivalence, and
the obstruction search from the contract plus exact finite definitions.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from itertools import permutations
import json
from pathlib import Path

import realization_contract as rc

REALIZATION_SCHEMA = "uqcf-v1553-regular-permutation-unitary-v1"

def _c4_table():
    return [[(a+b) % 4 for b in range(4)] for a in range(4)]

def _v4_table():
    return [[a ^ b for b in range(4)] for a in range(4)]

def _candidate(name, multiplication):
    action = [[multiplication[g][x] for x in range(4)] for g in range(4)]
    incidence = [[g,x,action[g][x]] for g in range(4) for x in range(4)]
    refinement = []
    for g in range(4):
        for h in range(4):
            for x in range(4):
                mid=action[h][x]
                out=action[g][mid]
                refinement.append([g,h,x,mid,out,multiplication[g][h]])
    return {
        "schema": REALIZATION_SCHEMA,
        "id": name,
        "carrier_dim": 4,
        "operations": [0,1,2,3],
        "identity": 0,
        "multiplication": multiplication,
        "action": action,
        "recovery_operations": [0,1,2,3],
        "incidence": incidence,
        "refinement": refinement,
    }

def independent_frozen_family():
    return [
        _candidate("C4_REGULAR", _c4_table()),
        _candidate("V4_REGULAR", _v4_table()),
    ]

def _shape_table(table,n):
    return (
        isinstance(table,(list,tuple)) and len(table)==n
        and all(isinstance(row,(list,tuple)) and len(row)==n for row in table)
        and all(type(x) is int and 0 <= x < n for row in table for x in row)
    )

def independent_admissibility(contract, realization):
    if not isinstance(realization,dict):
        return {"status":"SCHEMA_INVALID"}
    if set(contract.get("forbidden_fields",())).intersection(realization):
        return {"status":"FORBIDDEN_FIELD"}
    required={
        "schema","id","carrier_dim","operations","identity","multiplication",
        "action","recovery_operations","incidence","refinement",
    }
    if set(realization)!=required or realization.get("schema")!=REALIZATION_SCHEMA:
        return {"status":"SCHEMA_INVALID"}
    if realization.get("carrier_dim")!=4 or realization.get("operations")!=[0,1,2,3]:
        return {"status":"CARRIER_OR_OPERATION_DOMAIN_INVALID"}
    ops=realization["operations"]; n=len(ops); mul=realization["multiplication"]
    if not _shape_table(mul,n):
        return {"status":"COMPOSITION_INVALID"}
    e=realization["identity"]
    if type(e) is not int or not 0 <= e < n:
        return {"status":"IDENTITY_INVALID"}
    if any(mul[e][g]!=g or mul[g][e]!=g for g in ops):
        return {"status":"IDENTITY_INVALID"}
    for a in ops:
        for b in ops:
            for c in ops:
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]:
                    return {"status":"ASSOCIATIVITY_INVALID"}
    action=realization["action"]
    if not _shape_table(action,n):
        return {"status":"ACTION_INVALID"}
    target=list(range(n))
    if list(action[e])!=target:
        return {"status":"ACTION_INVALID"}
    for g in ops:
        if sorted(action[g])!=target:
            return {"status":"ACTION_INVALID"}
    for g in ops:
        for h in ops:
            for x in range(n):
                if action[mul[g][h]][x] != action[g][action[h][x]]:
                    return {"status":"ACTION_INVALID"}
    recovery=realization["recovery_operations"]
    if (
        not isinstance(recovery,(list,tuple))
        or len(set(recovery))!=len(recovery)
        or any(type(g) is not int or g not in ops for g in recovery)
    ):
        return {"status":"RECOVERY_INVALID"}
    for g in recovery:
        if not any(mul[g][h]==e and mul[h][g]==e for h in ops):
            return {"status":"RECOVERY_INVALID"}
    expected_inc=[[g,x,action[g][x]] for g in ops for x in range(n)]
    if realization["incidence"]!=expected_inc:
        return {"status":"INCIDENCE_INVALID"}
    expected_ref=[]
    for g in ops:
        for h in ops:
            for x in range(n):
                mid=action[h][x]; out=action[g][mid]
                expected_ref.append([g,h,x,mid,out,mul[g][h]])
    if realization["refinement"]!=expected_ref:
        return {"status":"REFINEMENT_INVALID"}
    for src in range(n):
        for dst in range(n):
            if sum(action[g][src]==dst for g in ops)!=1:
                return {"status":"ACTION_NOT_REGULAR"}
    return {"status":"ADMISSIBLE"}

def _pairs(realization, operations):
    action=realization["action"]; n=realization["carrier_dim"]
    return sorted({(src,action[g][src]) for g in operations for src in range(n)})

def _orbits(realization):
    n=realization["carrier_dim"]; action=realization["action"]
    unseen=set(range(n)); result=[]
    while unseen:
        seed=min(unseen)
        orbit={action[g][seed] for g in realization["operations"]}
        result.append(sorted(orbit)); unseen-=orbit
    return result

def independent_reduce(contract, realization):
    status=independent_admissibility(contract,realization)["status"]
    if status!="ADMISSIBLE":
        raise ValueError("inadmissible_realization:"+status)
    n=realization["carrier_dim"]; e=realization["identity"]
    return {
        "object_count": n,
        "lineage_incidence": [list(x) for x in _pairs(realization,realization["operations"])],
        "dependency_incidence": [list(x) for x in _pairs(realization,[g for g in realization["operations"] if g!=e])],
        "recoverability_relation": [list(x) for x in _pairs(realization,realization["recovery_operations"])],
        "composition_table": [[src,mid,dst] for src in range(n) for mid in range(n) for dst in range(n)],
        "refinement_diagram": [[src,left,right,dst] for src in range(n) for left in range(n) for right in range(n) for dst in range(n)],
        "disjoint_partition": _orbits(realization),
    }

def independent_order_spectrum(contract, realization):
    """Return sorted element orders as an algebraic invariant, independent of isomorphism search."""
    status=independent_admissibility(contract,realization)["status"]
    if status!="ADMISSIBLE":
        raise ValueError("inadmissible_realization:"+status)
    ops=realization["operations"]; mul=realization["multiplication"]; e=realization["identity"]
    orders=[]
    for g in ops:
        value=e
        found=None
        for k in range(1,len(ops)+1):
            value=mul[value][g]
            if value==e:
                found=k
                break
        if found is None:
            raise ValueError("operation_without_finite_order")
        orders.append(found)
    return tuple(sorted(orders))

def _mapping_parts(mapping,n):
    if not isinstance(mapping,(tuple,list)) or len(mapping)!=2*n:
        return None
    op=tuple(mapping[:n]); basis=tuple(mapping[n:]); target=tuple(range(n))
    if tuple(sorted(op))!=target or tuple(sorted(basis))!=target:
        return None
    return op,basis

def independent_is_isomorphism(contract,left,right,mapping):
    if independent_admissibility(contract,left)["status"]!="ADMISSIBLE":
        return False
    if independent_admissibility(contract,right)["status"]!="ADMISSIBLE":
        return False
    n=left["carrier_dim"]
    if right["carrier_dim"]!=n:
        return False
    parts=_mapping_parts(mapping,n)
    if parts is None:
        return False
    op,basis=parts
    if op[left["identity"]]!=right["identity"]:
        return False
    if {op[g] for g in left["recovery_operations"]}!=set(right["recovery_operations"]):
        return False
    for a in range(n):
        for b in range(n):
            if op[left["multiplication"][a][b]]!=right["multiplication"][op[a]][op[b]]:
                return False
    for g in range(n):
        for x in range(n):
            if basis[left["action"][g][x]]!=right["action"][op[g]][basis[x]]:
                return False
    mapped_inc={(op[g],basis[x],basis[y]) for g,x,y in left["incidence"]}
    if mapped_inc!={tuple(row) for row in right["incidence"]}:
        return False
    mapped_ref={
        (op[g],op[h],basis[x],basis[mid],basis[out],op[prod])
        for g,h,x,mid,out,prod in left["refinement"]
    }
    return mapped_ref=={tuple(row) for row in right["refinement"]}

def independent_isomorphisms(contract,left,right):
    if independent_admissibility(contract,left)["status"]!="ADMISSIBLE":
        return ()
    if independent_admissibility(contract,right)["status"]!="ADMISSIBLE":
        return ()
    n=left["carrier_dim"]
    if right["carrier_dim"]!=n:
        return ()
    found=[]
    for op in permutations(range(n)):
        for basis in permutations(range(n)):
            mapping=tuple(op)+tuple(basis)
            if independent_is_isomorphism(contract,left,right,mapping):
                found.append(mapping)
    return tuple(found)

def verify_isomorphism_packet(contract,left,right,packet):
    actual=independent_isomorphisms(contract,left,right)
    if not isinstance(packet,(tuple,list)):
        return {"status":"INVALID_ISOMORPHISM_PACKET"}
    supplied=[]
    for mapping in packet:
        if not independent_is_isomorphism(contract,left,right,mapping):
            return {"status":"INVALID_ISOMORPHISM_PACKET"}
        supplied.append(tuple(mapping))
    if len(set(supplied))!=len(supplied):
        return {"status":"INVALID_ISOMORPHISM_PACKET"}
    if set(supplied)!=set(actual):
        return {"status":"INCOMPLETE_ISOMORPHISM_PACKET"}
    return {"status":"COMPLETE_ISOMORPHISM_PACKET","count":len(actual)}

def _relabel_key(r,op,basis):
    n=r["carrier_dim"]; inv_op=[0]*n; inv_basis=[0]*n
    for old,new in enumerate(op): inv_op[new]=old
    for old,new in enumerate(basis): inv_basis[new]=old
    return (
        n,
        op[r["identity"]],
        tuple(op[r["multiplication"][inv_op[a]][inv_op[b]]] for a in range(n) for b in range(n)),
        tuple(basis[r["action"][inv_op[g]][inv_basis[x]]] for g in range(n) for x in range(n)),
        tuple(sorted(op[g] for g in r["recovery_operations"])),
    )

def independent_class_key(contract,realization):
    status=independent_admissibility(contract,realization)["status"]
    if status!="ADMISSIBLE":
        raise ValueError("inadmissible_realization:"+status)
    n=realization["carrier_dim"]
    return min(
        _relabel_key(realization,op,basis)
        for op in permutations(range(n))
        for basis in permutations(range(n))
    )

def _canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"))

def _jsonable(value):
    if isinstance(value,tuple):
        return [_jsonable(x) for x in value]
    if isinstance(value,list):
        return [_jsonable(x) for x in value]
    if isinstance(value,dict):
        return {k:_jsonable(v) for k,v in value.items()}
    return value

def _structural(realization):
    q=deepcopy(realization); q.pop("id",None); return q

def _base_report():
    return {
        "schema":"uqcf-v1553-independent-verification-v1",
        "scope":"FROZEN_V15_53_FINITE_FAMILY_ONLY",
        "candidate_count":0,
        "admissible_count":0,
        "retained_fiber_count":0,
        "target_class_count":0,
        "primary_verdict":"VERIFICATION_FAILED",
        "witness":None,
        "reasons":[],
        "source_correspondence":"NOT_EVALUATED",
        "Pillar_3":"OPEN",
        "physical_gravity":False,
        "universal_quantum_origin_theorem":False,
        "physical_source_law":False,
        "interpretation":"Independent adjudication not completed.",
    }

def verify_realization_obstruction(contract,family=None):
    report=_base_report()
    family=independent_frozen_family() if family is None else deepcopy(family)
    if not isinstance(family,(list,tuple)) or not family:
        report["primary_verdict"]="FAMILY_INVALID"
        report["reasons"]=["EMPTY_OR_MALFORMED_FAMILY"]
        return report
    family=list(family)
    report["candidate_count"]=len(family)
    structures=[]
    for r in family:
        if not isinstance(r,dict):
            report["primary_verdict"]="FAMILY_INVALID"
            report["reasons"]=["MALFORMED_REALIZATION"]
            return report
        structures.append(_canon(_structural(r)))
    if len(set(structures))!=len(structures):
        report["primary_verdict"]="FAMILY_INVALID"
        report["reasons"]=["DUPLICATE_REALIZATION"]
        return report
    rows=[]
    invalid=[]
    for r in family:
        check=independent_admissibility(contract,r)
        if check["status"]!="ADMISSIBLE":
            invalid.append({"id":r.get("id"),"status":check["status"]})
            continue
        rows.append({
            "id":r.get("id"),
            "readout":independent_reduce(contract,r),
            "class_key":independent_class_key(contract,r),
        })
    report["admissible_count"]=len(rows)
    if invalid:
        report["primary_verdict"]="FAMILY_INVALID"
        report["reasons"]=["INADMISSIBLE_REALIZATION"]
        report["invalid_candidates"]=invalid
        report["interpretation"]="The independently checked frozen family contains an inadmissible realization."
        return report
    fibers={}
    for row in rows:
        fibers.setdefault(_canon(row["readout"]),[]).append(row)
    report["retained_fiber_count"]=len(fibers)
    report["target_class_count"]=len({_canon(_jsonable(row["class_key"])) for row in rows})
    witness=None
    for key in sorted(fibers):
        fiber=sorted(fibers[key],key=lambda r:(str(r["id"]),_canon(_jsonable(r["class_key"]))))
        for i,left in enumerate(fiber):
            for right in fiber[i+1:]:
                if left["class_key"]!=right["class_key"]:
                    left_model=next(r for r in family if r.get("id")==left["id"])
                    right_model=next(r for r in family if r.get("id")==right["id"])
                    witness={
                        "left_id":left["id"],
                        "right_id":right["id"],
                        "retained_readout":left["readout"],
                        "left_class_key":_jsonable(left["class_key"]),
                        "right_class_key":_jsonable(right["class_key"]),
                        "left_order_spectrum":list(independent_order_spectrum(contract,left_model)),
                        "right_order_spectrum":list(independent_order_spectrum(contract,right_model)),
                    }
                    break
            if witness is not None: break
        if witness is not None: break
    if witness is None:
        report["primary_verdict"]="NO_WITNESS_IN_FROZEN_FAMILY"
        report["interpretation"]="No obstruction witness occurs in the independently checked frozen v15.53 finite family."
    else:
        report["primary_verdict"]="CERTIFIED_FAMILY_OBSTRUCTION_WITNESS"
        report["witness"]=witness
        report["interpretation"]=(
            "Independent finite verification finds two admissible exact regular "
            "permutation-unitary realizations with identical registered retained "
            "readout and distinct registered structural equivalence classes. "
            "Certification is limited to the frozen v15.53 family."
        )
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[4]
    contract=rc.load_contract(root)
    report=verify_realization_obstruction(contract)
    raw=json.dumps(report,sort_keys=True,separators=(",",":"))+"\n"
    if args.output:
        args.output.write_text(raw,encoding="utf-8")
    else:
        print(raw,end="")

if __name__=="__main__":
    main()
