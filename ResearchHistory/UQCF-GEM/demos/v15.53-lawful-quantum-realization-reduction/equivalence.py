"""v15.53 Task 4: exact structural isomorphism and canonical classes."""
from itertools import permutations
import realization_family as rf

def _valid(r, contract):
    return rf.check_admissibility(contract, r).get("status") == "ADMISSIBLE"

def _split_mapping(mapping, n):
    if not isinstance(mapping, (tuple, list)) or len(mapping) != 2*n:
        return None
    op = tuple(mapping[:n]); basis = tuple(mapping[n:])
    target = tuple(range(n))
    if tuple(sorted(op)) != target or tuple(sorted(basis)) != target:
        return None
    return op, basis

def is_isomorphism(contract, left, right, mapping):
    if not _valid(left, contract) or not _valid(right, contract):
        return False
    n = left["carrier_dim"]
    if right["carrier_dim"] != n:
        return False
    parts = _split_mapping(mapping, n)
    if parts is None:
        return False
    op, basis = parts
    if op[left["identity"]] != right["identity"]:
        return False
    if {op[g] for g in left["recovery_operations"]} != set(right["recovery_operations"]):
        return False
    for a in range(n):
        for b in range(n):
            if op[left["multiplication"][a][b]] != right["multiplication"][op[a]][op[b]]:
                return False
    for g in range(n):
        for x in range(n):
            if basis[left["action"][g][x]] != right["action"][op[g]][basis[x]]:
                return False
    mapped_incidence = {
        (op[g], basis[x], basis[y]) for g,x,y in left["incidence"]
    }
    if mapped_incidence != {tuple(row) for row in right["incidence"]}:
        return False
    mapped_refinement = {
        (op[g],op[h],basis[x],basis[mid],basis[out],op[prod])
        for g,h,x,mid,out,prod in left["refinement"]
    }
    if mapped_refinement != {tuple(row) for row in right["refinement"]}:
        return False
    return True

def enumerate_isomorphisms(contract, left, right):
    if not _valid(left, contract) or not _valid(right, contract):
        return ()
    if left["carrier_dim"] != right["carrier_dim"]:
        return ()
    n = left["carrier_dim"]
    found = []
    for op in permutations(range(n)):
        for basis in permutations(range(n)):
            mapping = tuple(op) + tuple(basis)
            if is_isomorphism(contract, left, right, mapping):
                found.append(mapping)
    return tuple(found)

def are_equivalent(contract, left, right):
    return bool(enumerate_isomorphisms(contract, left, right))

def _relabel_key(r, op, basis):
    n = r["carrier_dim"]
    inv_op = [0]*n
    inv_basis = [0]*n
    for old,new in enumerate(op): inv_op[new]=old
    for old,new in enumerate(basis): inv_basis[new]=old
    identity = op[r["identity"]]
    mul = tuple(
        op[r["multiplication"][inv_op[a]][inv_op[b]]]
        for a in range(n) for b in range(n)
    )
    action = tuple(
        basis[r["action"][inv_op[g]][inv_basis[x]]]
        for g in range(n) for x in range(n)
    )
    recovery = tuple(sorted(op[g] for g in r["recovery_operations"]))
    return (n, identity, mul, action, recovery)

def canonical_class_key(contract, realization):
    """Canonical exact class key under all permitted finite relabelings."""
    if not _valid(realization, contract):
        raise ValueError("inadmissible_realization")
    n = realization["carrier_dim"]
    # Incidence/refinement are deterministic consequences checked by
    # admissibility, so this nonredundant key is exact for the frozen family.
    return min(
        _relabel_key(realization, op, basis)
        for op in permutations(range(n))
        for basis in permutations(range(n))
    )
