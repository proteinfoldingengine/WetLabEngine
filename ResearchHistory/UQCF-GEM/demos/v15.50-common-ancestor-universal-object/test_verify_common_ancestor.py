"""v15.50 Task 4 RED: independent common-ancestor verifier."""
from pathlib import Path
import copy, unittest
import common_contract as cc
import common_candidates as ca
import common_factorizations as cf
import verify_common_ancestor as vc

class VerifyCommonAncestorTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.root=root; cls.c=cc.load_contract(root)
  cls.u=ca.enumerate_candidates(cls.c)[0]; cls.fr=cf.derive_retained_leg(cls.c,cls.u); cls.fq=cf.derive_quantum_legs(cls.c,cls.u)
 def test_insufficiency_verifies(self):
  r=vc.verify(self.c,self.u,self.fr,self.fq)
  self.assertEqual(r["status"],"VERIFIED_COMMON_ANCESTOR_INSUFFICIENT")
  self.assertTrue(r["U_target_blind"]); self.assertTrue(r["retained_leg_lawful"]); self.assertFalse(r["quantum_leg_derivable"])
 def test_hidden_target_label_rejected(self):
  u=copy.deepcopy(self.u); u["quantum_labels"]=["q0"]
  with self.assertRaisesRegex(ValueError,"target_contamination"): vc.verify(self.c,u,self.fr,self.fq)
 def test_lookup_quantum_leg_rejected(self):
  fq=copy.deepcopy(self.fq); fq["lookup_table_used"]=True
  with self.assertRaisesRegex(ValueError,"lookup_quantum_leg"): vc.verify(self.c,self.u,self.fr,fq)
 def test_fake_quantum_leg_rejected(self):
  fq=copy.deepcopy(self.fq); fq["lawful_legs"]=[{"map":[0,1,2,3]}]
  with self.assertRaisesRegex(ValueError,"unearned_quantum_leg"): vc.verify(self.c,self.u,self.fr,fq)
 def test_broken_retained_leg_rejected(self):
  fr=copy.deepcopy(self.fr); fr["preserves_composition"]=False
  with self.assertRaisesRegex(ValueError,"retained_leg"): vc.verify(self.c,self.u,fr,self.fq)
if __name__=="__main__": unittest.main()
