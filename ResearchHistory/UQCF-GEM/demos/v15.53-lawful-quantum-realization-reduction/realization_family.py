"""v15.53 Task 2: exact finite lawful realization family.

The family contains the two group structures of order four, represented by
their exact regular permutation actions.  A permutation action is an exact
unitary representation on the four-dimensional basis; no floating point
data or retained-source selector is used.
"""
from copy import deepcopy

SCHEMA = "uqcf-v1553-regular-permutation-unitary-v1"

def _c4_table():
    return [[(a+b) % 4 for b in range(4)] for a in range(4)]

def _v4_table():
    return [[a ^ b for b in range(4)] for a in range(4)]

def _candidate(name, multiplication):
    action = [[multiplication[g][x] for x in range(4)] for g in range(4)]
    incidence = [[g, x, action[g][x]] for g in range(4) for x in range(4)]
    refinement = []
    for g in range(4):
        for h in range(4):
            for x in range(4):
                mid = action[h][x]
                out = action[g][mid]
                refinement.append([g, h, x, mid, out, multiplication[g][h]])
    return {
        "schema": SCHEMA,
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

def enumerate_raw_realizations(contract):
    """Return the frozen raw family in deterministic order."""
    if contract.get("schema") != "uqcf-v1553-realization-contract-v1":
        raise ValueError("contract_schema")
    return (
        _candidate("C4_REGULAR", _c4_table()),
        _candidate("V4_REGULAR", _v4_table()),
    )

def _shape_table(table, n):
    return (
        isinstance(table, (list, tuple))
        and len(table) == n
        and all(isinstance(row, (list, tuple)) and len(row) == n for row in table)
        and all(type(x) is int and 0 <= x < n for row in table for x in row)
    )

def check_admissibility(contract, realization):
    """Exhaustively validate one finite realization; never trust status labels."""
    if not isinstance(realization, dict):
        return {"status":"SCHEMA_INVALID"}
    forbidden = set(contract.get("forbidden_fields", ()))
    if forbidden.intersection(realization):
        return {"status":"FORBIDDEN_FIELD"}

    required = {
        "schema","id","carrier_dim","operations","identity","multiplication",
        "action","recovery_operations","incidence","refinement",
    }
    if set(realization) != required or realization.get("schema") != SCHEMA:
        return {"status":"SCHEMA_INVALID"}
    if realization.get("carrier_dim") != 4:
        return {"status":"CARRIER_INVALID"}
    operations = realization.get("operations")
    if operations != [0,1,2,3]:
        return {"status":"OPERATION_DOMAIN_INVALID"}
    n = len(operations)
    mul = realization.get("multiplication")
    if not _shape_table(mul, n):
        return {"status":"COMPOSITION_INVALID"}
    e = realization.get("identity")
    if type(e) is not int or not 0 <= e < n:
        return {"status":"IDENTITY_INVALID"}
    if any(mul[e][g] != g or mul[g][e] != g for g in operations):
        return {"status":"IDENTITY_INVALID"}
    for a in operations:
        for b in operations:
            for c in operations:
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]:
                    return {"status":"ASSOCIATIVITY_INVALID"}

    action = realization.get("action")
    if not _shape_table(action, n):
        return {"status":"ACTION_INVALID"}
    identity_perm = list(range(n))
    if list(action[e]) != identity_perm:
        return {"status":"ACTION_INVALID"}
    for g in operations:
        if sorted(action[g]) != identity_perm:
            return {"status":"ACTION_INVALID"}
    for g in operations:
        for h in operations:
            gh = mul[g][h]
            for x in range(n):
                if action[gh][x] != action[g][action[h][x]]:
                    return {"status":"ACTION_INVALID"}

    recovery = realization.get("recovery_operations")
    if (
        not isinstance(recovery, (list, tuple))
        or len(set(recovery)) != len(recovery)
        or any(type(g) is not int or g not in operations for g in recovery)
    ):
        return {"status":"RECOVERY_INVALID"}
    # In this family every declared recovery operation must have a two-sided inverse.
    for g in recovery:
        if not any(mul[g][h] == e and mul[h][g] == e for h in operations):
            return {"status":"RECOVERY_INVALID"}

    expected_incidence = [[g, x, action[g][x]] for g in operations for x in range(n)]
    if realization.get("incidence") != expected_incidence:
        return {"status":"INCIDENCE_INVALID"}

    expected_refinement = []
    for g in operations:
        for h in operations:
            for x in range(n):
                mid = action[h][x]
                out = action[g][mid]
                expected_refinement.append([g,h,x,mid,out,mul[g][h]])
    if realization.get("refinement") != expected_refinement:
        return {"status":"REFINEMENT_INVALID"}

    # Regularity: each ordered pair of basis states has exactly one operation.
    for src in range(n):
        for dst in range(n):
            if sum(action[g][src] == dst for g in operations) != 1:
                return {"status":"ACTION_NOT_REGULAR"}

    return {
        "status":"ADMISSIBLE",
        "carrier_dim":n,
        "operation_count":n,
        "regular_action":True,
        "exact_permutation_unitary":True,
    }
