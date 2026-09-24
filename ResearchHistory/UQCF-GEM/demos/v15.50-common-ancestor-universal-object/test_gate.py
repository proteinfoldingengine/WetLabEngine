"""v15.50 Task 5 RED: final mechanical adjudication."""
from pathlib import Path
import copy, unittest
import common_contract as cc
import common_candidates as ca
import common_factorizations as cf
import verify_common_ancestor as vc
import gate as g

class GateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=cc.load_contract(root); cls.u=ca.enumerate_candidates(cls.c)[0]
  cls.fr=cf.derive_retained_leg(cls.c,cls.u); cls.fq=cf.derive_quantum_legs(cls.c,cls.u); cls.v=vc.verify(cls.c,cls.u,cls.fr,cls.fq)
 def test_verified_insufficiency_adjudicates(self):
  r=g.adjudicate(self.c,self.v)
  self.assertEqual(r["verdict"],"COMMON_ANCESTOR_INSUFFICIENT")
  self.assertTrue(r["U_well_typed"]); self.assertFalse(r["quantum_leg_derived"])
 def test_unknown_verdict_rejected(self):
  r=g.adjudicate(self.c,self.v); r["verdict"]="MAYBE"
  with self.assertRaisesRegex(ValueError,"verdict"): g.verify_result(r)
 def test_physical_claim_rejected(self):
  r=g.adjudicate(self.c,self.v); r["physical_gravity"]=True
  with self.assertRaisesRegex(ValueError,"claim_boundary"): g.verify_result(r)
 def test_invalid_verification_rejected(self):
  v=copy.deepcopy(self.v); v["status"]="BROKEN"
  with self.assertRaisesRegex(ValueError,"verification_status"): g.adjudicate(self.c,v)
if __name__=="__main__": unittest.main()
