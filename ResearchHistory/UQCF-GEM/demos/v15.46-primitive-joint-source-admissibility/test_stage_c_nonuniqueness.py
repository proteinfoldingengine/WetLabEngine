"""Stage C3 RED: exact inequivalent-representation witness."""
import unittest
from pathlib import Path
import stage_c_contract as sc
import stage_c_nonuniqueness as sn

class StageCNonuniquenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.contract=sc.load_contract(root)
        cls.w=sn.find_witness(cls.contract)
    def test_witness_uses_same_frozen_constraints(self):
        self.assertEqual(self.w["left"]["constraints"],self.w["right"]["constraints"])
        self.assertEqual(self.w["left"]["constraints"],self.contract["constraints"])
    def test_two_distinct_node_site_expansions(self):
        self.assertNotEqual(self.w["left"]["node_site_bijection"],self.w["right"]["node_site_bijection"])
        self.assertEqual(len(self.w["left"]["node_site_bijection"]),5)
        self.assertEqual(len(self.w["right"]["node_site_bijection"]),5)
    def test_reduct_is_identical(self):
        self.assertEqual(self.w["left"]["frozen_reduct"],self.w["right"]["frozen_reduct"])
    def test_not_related_by_earned_gauge(self):
        self.assertEqual(self.contract["earned_gauge"]["node_site"],"NONE_CERTIFIED")
        self.assertFalse(self.w["gauge_test"]["related_by_earned_gauge"])
    def test_no_candidate_specific_selector(self):
        self.assertEqual(self.w["left"]["added_selector"],None)
        self.assertEqual(self.w["right"]["added_selector"],None)
    def test_status(self):
        self.assertEqual(self.w["status"],"INEQUIVALENT_REPRESENTATIONS_FOUND")
if __name__=="__main__": unittest.main()
