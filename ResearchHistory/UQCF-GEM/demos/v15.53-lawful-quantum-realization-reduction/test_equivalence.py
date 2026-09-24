"""v15.53 Task 4 RED: structural equivalence, never label inequality."""
from copy import deepcopy
from itertools import permutations
import json
from pathlib import Path
import unittest

import realization_contract as rc
import realization_family as rf
import equivalence as eq

ROOT = Path(__file__).resolve().parents[4]

def relabel(r, op_p, basis_p):
    q = deepcopy(r)
    n = 4
    mul = [[0]*n for _ in range(n)]
    action = [[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            mul[op_p[a]][op_p[b]] = op_p[r["multiplication"][a][b]]
    for g in range(n):
        for x in range(n):
            action[op_p[g]][basis_p[x]] = basis_p[r["action"][g][x]]
    q["id"] = "RELABELLED"
    q["identity"] = op_p[r["identity"]]
    q["multiplication"] = mul
    q["action"] = action
    q["recovery_operations"] = sorted(op_p[g] for g in r["recovery_operations"])
    q["incidence"] = [[g,x,action[g][x]] for g in range(n) for x in range(n)]
    q["refinement"] = []
    for g in range(n):
        for h in range(n):
            for x in range(n):
                mid=action[h][x]; out=action[g][mid]
                q["refinement"].append([g,h,x,mid,out,mul[g][h]])
    return q

def brute_isomorphisms(c, left, right):
    found=[]
    for op_p in permutations(range(4)):
        for basis_p in permutations(range(4)):
            mapping=tuple(op_p)+tuple(basis_p)
            if eq.is_isomorphism(c,left,right,mapping):
                found.append(mapping)
    return tuple(found)

class EquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.c=rc.load_contract(ROOT)
        self.c4,self.v4=rf.enumerate_raw_realizations(self.c)
        self.c4r=relabel(self.c4,(1,2,3,0),(2,0,3,1))

    def test_self_equivalence(self):
        for r in (self.c4,self.v4):
            self.assertTrue(eq.are_equivalent(self.c,r,r))

    def test_c4_and_v4_are_structurally_inequivalent(self):
        self.assertFalse(eq.are_equivalent(self.c,self.c4,self.v4))
        self.assertNotEqual(eq.canonical_class_key(self.c,self.c4),eq.canonical_class_key(self.c,self.v4))

    def test_label_and_basis_relabeling_is_equivalent(self):
        self.assertEqual(rf.check_admissibility(self.c,self.c4r)["status"],"ADMISSIBLE")
        self.assertTrue(eq.are_equivalent(self.c,self.c4,self.c4r))
        self.assertEqual(eq.canonical_class_key(self.c,self.c4),eq.canonical_class_key(self.c,self.c4r))

    def test_symmetry_and_transitivity(self):
        c4r2=relabel(self.c4,(2,3,0,1),(1,3,0,2))
        self.assertTrue(eq.are_equivalent(self.c,self.c4r,self.c4))
        self.assertTrue(eq.are_equivalent(self.c,self.c4,c4r2))
        self.assertTrue(eq.are_equivalent(self.c,self.c4r,c4r2))

    def test_id_swap_does_not_change_class(self):
        q=deepcopy(self.c4); q["id"]="V4_REGULAR"
        self.assertEqual(eq.canonical_class_key(self.c,q),eq.canonical_class_key(self.c,self.c4))

    def test_operation_structure_change_changes_class_or_admissibility(self):
        q=deepcopy(self.c4); q["multiplication"][1][1]=1
        self.assertNotEqual(rf.check_admissibility(self.c,q)["status"],"ADMISSIBLE")

    def test_enumerator_matches_independent_bruteforce(self):
        self.assertEqual(eq.enumerate_isomorphisms(self.c,self.c4,self.c4r),brute_isomorphisms(self.c,self.c4,self.c4r))
        self.assertGreater(len(eq.enumerate_isomorphisms(self.c,self.c4,self.c4r)),0)

    def test_invented_nonpreserving_bijection_rejected(self):
        bad=tuple(range(4))+tuple((1,0,2,3))
        self.assertFalse(eq.is_isomorphism(self.c,self.c4,self.c4,bad))

    def test_json_roundtrip_preserves_class(self):
        for r in (self.c4,self.v4):
            q=json.loads(json.dumps(r))
            self.assertEqual(eq.canonical_class_key(self.c,r),eq.canonical_class_key(self.c,q))

    def test_family_partition_independent_of_enumeration_order(self):
        a={eq.canonical_class_key(self.c,r) for r in (self.c4,self.v4)}
        b={eq.canonical_class_key(self.c,r) for r in (self.v4,self.c4)}
        self.assertEqual(a,b)
        self.assertEqual(len(a),2)

if __name__=="__main__":
    unittest.main()
