"""Stage C1 RED: primitive contract must be pinned and exclude downstream selectors."""
from pathlib import Path
import unittest
import stage_c_contract as sc

class StageCContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(cls.root)

    def test_contract_has_no_cross_domain_relation(self):
        self.assertEqual(self.c["cross_domain_relations"],[])
        self.assertEqual(self.c["earned_gauge"]["node_site"],"NONE_CERTIFIED")

    def test_v1509_boundary_is_pinned(self):
        self.assertEqual(self.c["sources"]["carrier_origin"]["git_blob_sha"],
                         "ec73ef9240dcef062c95a82c511a874d0d2923ef")

    def test_downstream_geometry_and_assumed_source_excluded(self):
        self.assertFalse(self.c["admissible_inputs"]["v15_39_incidence_source"])
        self.assertFalse(self.c["admissible_inputs"]["v15_43_to_v15_45_geometry"])

    def test_required_representation_fields_are_unearned(self):
        self.assertEqual(self.c["quantum_sort"]["carrier_origin"],"NOT_DERIVED")
        self.assertEqual(self.c["quantum_sort"]["factorization_selector"],"NONE_CERTIFIED")
        self.assertEqual(self.c["quantum_sort"]["joint_state_selector"],"NONE_CERTIFIED")

    def test_source_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
            sc.load_contract(self.root,overrides={"carrier_origin":b"drift"})

if __name__=="__main__": unittest.main()
