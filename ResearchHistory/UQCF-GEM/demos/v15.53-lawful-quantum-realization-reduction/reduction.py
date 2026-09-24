"""v15.53 Task 3: target-blind reduction to retained pair-groupoid readouts."""
import realization_family as rf

def _pairs_from_ops(realization, operations):
    action = realization["action"]
    return sorted({(src, action[g][src]) for g in operations for src in range(realization["carrier_dim"])})

def _orbits(realization):
    n = realization["carrier_dim"]
    action = realization["action"]
    unseen = set(range(n))
    parts = []
    while unseen:
        seed = min(unseen)
        orbit = {action[g][seed] for g in realization["operations"]}
        parts.append(sorted(orbit))
        unseen -= orbit
    return parts

def validate_retained(contract, readout):
    keys = tuple(contract["retained_observables"])
    if not isinstance(readout, dict) or tuple(readout) != keys:
        return False
    n = readout["object_count"]
    if type(n) is not int or n < 0:
        return False
    pair_fields = ("lineage_incidence","dependency_incidence","recoverability_relation")
    for key in pair_fields:
        rows = readout[key]
        if not isinstance(rows, list):
            return False
        if any(not isinstance(row, list) or len(row) != 2 or any(type(i) is not int or not 0 <= i < n for i in row) for row in rows):
            return False
    if any(not isinstance(row, list) or len(row) != 3 or any(type(i) is not int or not 0 <= i < n for i in row) for row in readout["composition_table"]):
        return False
    if any(not isinstance(row, list) or len(row) != 4 or any(type(i) is not int or not 0 <= i < n for i in row) for row in readout["refinement_diagram"]):
        return False
    flat = [i for block in readout["disjoint_partition"] for i in block]
    if sorted(flat) != list(range(n)) or len(flat) != len(set(flat)):
        return False
    return True

def reduce_to_retained(contract, realization):
    """Forget operation labels while retaining exact action reachability structure."""
    check = rf.check_admissibility(contract, realization)
    if check.get("status") != "ADMISSIBLE":
        raise ValueError("inadmissible_realization:" + str(check.get("status")))
    n = realization["carrier_dim"]
    identity = realization["identity"]
    all_pairs = _pairs_from_ops(realization, realization["operations"])
    dependency_pairs = _pairs_from_ops(
        realization, [g for g in realization["operations"] if g != identity]
    )
    recoverable = _pairs_from_ops(realization, realization["recovery_operations"])

    # A free transitive action reduces to the pair groupoid: one retained arrow
    # for each ordered pair; retained composition depends only on endpoints.
    composition = [[src, mid, dst] for src in range(n) for mid in range(n) for dst in range(n)]
    # Every two length-2 paths with the same endpoints refine the same unique arrow.
    refinement = [[src, left, right, dst]
                  for src in range(n) for left in range(n)
                  for right in range(n) for dst in range(n)]

    out = {
        "object_count": n,
        "lineage_incidence": [list(x) for x in all_pairs],
        "dependency_incidence": [list(x) for x in dependency_pairs],
        "recoverability_relation": [list(x) for x in recoverable],
        "composition_table": composition,
        "refinement_diagram": refinement,
        "disjoint_partition": _orbits(realization),
    }
    if not validate_retained(contract, out):
        raise ValueError("retained_schema_invalid")
    return out
