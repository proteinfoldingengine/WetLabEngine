"""v15.53 Task 3 RED: target-blind retained reduction."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import realization_contract as rc
import realization_family as rf
import reduction as red

ROOT = Path(__file__).resolve().parents[4]

class ReductionTests(unittest.TestCase):
    def setUp(self):
        self.c = rc.load_contract(ROOT)
        self.family = rf.enumerate_raw_realizations(self.c)

    def test_output_domain_is_exactly_frozen_seven(self):
        for r in self.family:
            out = red.reduce_to_retained(self.c, r)
            self.assertEqual(tuple(out), tuple(self.c["retained_observables"]))
            self.assertTrue(red.validate_retained(self.c, out))

    def test_c4_and_v4_reduce_to_same_retained_pair_groupoid(self):
        left = red.reduce_to_retained(self.c, self.family[0])
        right = red.reduce_to_retained(self.c, self.family[1])
        self.assertEqual(left, right)
        self.assertEqual(left["object_count"], 4)
        self.assertEqual(len(left["recoverability_relation"]), 16)
        self.assertEqual(len(left["composition_table"]), 64)

    def test_reduction_is_deterministic_and_id_blind(self):
        r = deepcopy(self.family[0])
        a = red.reduce_to_retained(self.c, r)
        self.assertEqual(a, red.reduce_to_retained(self.c, r))
        r["id"] = "anything"
        self.assertEqual(a, red.reduce_to_retained(self.c, r))

    def test_target_metadata_is_rejected_not_consumed(self):
        r = deepcopy(self.family[0]); r["target_class"] = "smuggled"
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "FORBIDDEN_FIELD")
        with self.assertRaises(ValueError):
            red.reduce_to_retained(self.c, r)

    def test_recovery_subset_changes_recomputed_recoverability(self):
        r = deepcopy(self.family[0])
        r["recovery_operations"] = [0]
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "ADMISSIBLE")
        out = red.reduce_to_retained(self.c, r)
        self.assertEqual(out["recoverability_relation"], [[i,i] for i in range(4)])

    def test_copied_external_readout_is_never_trusted(self):
        r = deepcopy(self.family[0]); r["E_observables"] = {"object_count":999}
        with self.assertRaises(ValueError):
            red.reduce_to_retained(self.c, r)

    def test_json_roundtrip_preserves_reduction(self):
        for r in self.family:
            q = json.loads(json.dumps(r))
            self.assertEqual(red.reduce_to_retained(self.c, q), red.reduce_to_retained(self.c, r))

    def test_internal_basis_relabeling_does_not_create_selector_effect(self):
        r = deepcopy(self.family[0])
        p = [1,0,3,2]
        inv = [0]*4
        for i,j in enumerate(p): inv[j] = i
        old = r["action"]
        r["action"] = [[p[old[g][inv[x]]] for x in range(4)] for g in range(4)]
        r["incidence"] = [[g,x,r["action"][g][x]] for g in range(4) for x in range(4)]
        r["refinement"] = []
        for g in range(4):
            for h in range(4):
                for x in range(4):
                    mid=r["action"][h][x]; out=r["action"][g][mid]
                    r["refinement"].append([g,h,x,mid,out,r["multiplication"][g][h]])
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "ADMISSIBLE")
        self.assertEqual(red.reduce_to_retained(self.c, r), red.reduce_to_retained(self.c, self.family[0]))

if __name__ == "__main__":
    unittest.main()
