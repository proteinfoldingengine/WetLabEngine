"""v15.47 Task 4 RED: independent verifier of candidates/classes."""
from pathlib import Path
import copy, unittest
import functor_contract as fc
import functor_candidates as cand
import functor_classes as cls_module
import verify_functoriality as vf

class VerifyFunctorialityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[4]
        cls.c=fc.load_contract(root); cls.cs=cand.enumerate_candidates(cls.c)
        cls.ledger=cls_module.surviving_classes(cls.c,cls.cs)

    def test_valid_ledgers_verify(self):
        r=vf.verify(self.c,self.cs,self.ledger)
        self.assertEqual(r["status"],"VERIFIED_120_SURVIVORS_120_CLASSES")
        self.assertEqual(r["survivor_count"],120)
        self.assertEqual(r["equivalence_class_count"],120)

    def test_omitted_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError,"candidate_family"):
            vf.verify(self.c,self.cs[:-1],self.ledger)

    def test_duplicated_class_member_rejected(self):
        l=copy.deepcopy(self.ledger); l["classes"][-1]=l["classes"][0]
        with self.assertRaisesRegex(ValueError,"class_partition"):
            vf.verify(self.c,self.cs,l)

    def test_invented_equivalence_rejected(self):
        l=copy.deepcopy(self.ledger); l["target_equivalence"]="ALL_SITE_PERMUTATIONS"
        with self.assertRaisesRegex(ValueError,"target_equivalence"):
            vf.verify(self.c,self.cs,l)

    def test_broken_composition_rejected(self):
        cs=copy.deepcopy(list(self.cs)); cs[0]["morphism_images"]["ba"]="BROKEN"
        with self.assertRaisesRegex(ValueError,"functor_law"):
            vf.verify(self.c,cs,self.ledger)

    def test_broken_refinement_rejected(self):
        cs=copy.deepcopy(list(self.cs)); cs[0]["morphism_images"]["q"]="BROKEN"
        with self.assertRaisesRegex(ValueError,"functor_law"):
            vf.verify(self.c,cs,self.ledger)

    def test_dimension_change_rejected(self):
        cs=copy.deepcopy(list(self.cs)); cs[0]["carrier_dimension"]=125
        with self.assertRaisesRegex(ValueError,"dimension"):
            vf.verify(self.c,cs,self.ledger)

    def test_downstream_selector_rejected(self):
        c=copy.deepcopy(self.c); c["prohibited_inputs"]["curvature"]=False
        with self.assertRaisesRegex(ValueError,"downstream_firewall"):
            vf.verify(c,self.cs,self.ledger)

if __name__=="__main__": unittest.main()
