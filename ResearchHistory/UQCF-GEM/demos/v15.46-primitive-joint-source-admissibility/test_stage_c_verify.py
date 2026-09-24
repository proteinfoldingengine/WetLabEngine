"""Stage C4 RED: independent verifier for the C3 witness."""
import copy, unittest
from pathlib import Path
import stage_c_contract as sc
import stage_c_nonuniqueness as sn
import stage_c_verify as sv

class StageCVerifyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=sc.load_contract(root); cls.w=sn.find_witness(cls.c)
    def test_valid_witness_verifies(self):
        r=sv.verify_witness(self.c,self.w)
        self.assertEqual(r["status"],"VERIFIED_INEQUIVALENT_REPRESENTATIONS")
        self.assertTrue(r["same_frozen_constraints"])
        self.assertFalse(r["related_by_earned_gauge"])
    def test_omitted_constraint_rejected(self):
        w=copy.deepcopy(self.w); w["right"]["constraints"]=w["right"]["constraints"][:-1]
        with self.assertRaisesRegex(ValueError,"constraint_mismatch"): sv.verify_witness(self.c,w)
    def test_invented_cross_domain_relation_rejected(self):
        w=copy.deepcopy(self.w); w["right"]["frozen_reduct"]["cross_domain_relations"]=["invented"]
        with self.assertRaisesRegex(ValueError,"reduct_mismatch"): sv.verify_witness(self.c,w)
    def test_newly_declared_gauge_rejected(self):
        w=copy.deepcopy(self.w); w["gauge_test"]["earned_node_site_gauge"]="S5"
        with self.assertRaisesRegex(ValueError,"gauge_mismatch"): sv.verify_witness(self.c,w)
    def test_identical_realizations_rejected(self):
        w=copy.deepcopy(self.w); w["right"]["node_site_bijection"]=w["left"]["node_site_bijection"]
        with self.assertRaisesRegex(ValueError,"not_distinct"): sv.verify_witness(self.c,w)
    def test_changed_dimension_type_rejected(self):
        w=copy.deepcopy(self.w); w["right"]["frozen_reduct"]["quantum_carrier_origin"]="DIMENSION_125"
        with self.assertRaisesRegex(ValueError,"reduct_mismatch"): sv.verify_witness(self.c,w)
if __name__=="__main__": unittest.main()
