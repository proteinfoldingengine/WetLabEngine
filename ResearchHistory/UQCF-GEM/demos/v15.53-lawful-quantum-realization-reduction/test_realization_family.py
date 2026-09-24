"""v15.53 Task 2 RED: exact realization family and admissibility."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import realization_contract as rc
import realization_family as rf

ROOT = Path(__file__).resolve().parents[4]

class RealizationFamilyTests(unittest.TestCase):
    def setUp(self):
        self.c = rc.load_contract(ROOT)
        self.family = rf.enumerate_raw_realizations(self.c)

    def test_family_is_exact_nonempty_and_deterministic(self):
        self.assertEqual(self.family, rf.enumerate_raw_realizations(self.c))
        self.assertEqual(tuple(r["id"] for r in self.family), ("C4_REGULAR","V4_REGULAR"))

    def test_no_duplicate_canonical_records(self):
        stripped = []
        for r in self.family:
            q = deepcopy(r); q.pop("id")
            stripped.append(json.dumps(q, sort_keys=True, separators=(",",":")))
        self.assertEqual(len(stripped), len(set(stripped)))

    def test_baselines_are_admissible(self):
        for r in self.family:
            self.assertEqual(rf.check_admissibility(self.c, r)["status"], "ADMISSIBLE")

    def test_id_is_metadata_only(self):
        r = deepcopy(self.family[0]); r["id"] = "renamed"
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "ADMISSIBLE")

    def test_changed_composition_entry_fails(self):
        r = deepcopy(self.family[0]); r["multiplication"][1][1] = 1
        self.assertNotEqual(rf.check_admissibility(self.c, r)["status"], "ADMISSIBLE")

    def test_broken_identity_fails(self):
        r = deepcopy(self.family[0]); r["identity"] = 1
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "IDENTITY_INVALID")

    def test_recovery_operation_outside_domain_fails(self):
        r = deepcopy(self.family[0]); r["recovery_operations"].append(9)
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "RECOVERY_INVALID")

    def test_malformed_typed_incidence_fails(self):
        r = deepcopy(self.family[0]); r["incidence"][0] = [0,0,3]
        self.assertEqual(rf.check_admissibility(self.c, r)["status"], "INCIDENCE_INVALID")

    def test_forbidden_target_or_selector_fields_fail(self):
        for key in ("target_class","E_observables","node_site_dictionary","post_result_gauge"):
            r = deepcopy(self.family[0]); r[key] = "smuggled"
            self.assertEqual(rf.check_admissibility(self.c, r)["status"], "FORBIDDEN_FIELD")

    def test_json_roundtrip_preserves_admissibility(self):
        for r in self.family:
            q = json.loads(json.dumps(r))
            self.assertEqual(rf.check_admissibility(self.c, q), rf.check_admissibility(self.c, r))

    def test_actions_are_regular_and_distinct_groups(self):
        c4,v4 = self.family
        self.assertNotEqual(c4["multiplication"], v4["multiplication"])
        for r in self.family:
            for src in range(4):
                for dst in range(4):
                    self.assertEqual(sum(r["action"][g][src] == dst for g in range(4)), 1)

if __name__ == "__main__":
    unittest.main()
