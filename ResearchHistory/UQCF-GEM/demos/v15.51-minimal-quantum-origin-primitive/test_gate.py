"""v15.51 Task 5 RED: final mechanical adjudication."""
from pathlib import Path
import copy, unittest
import primitive_contract as pc
import primitive_realizations as pr
import quantum_origin as qo
import minimality as mn
import verify_quantum_origin as vq
import gate as g
class GateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=pc.load_contract(root)
  cls.rs={p:pr.enumerate_realizations(cls.c,p) for p in cls.c["packages"]}
  cls.os={p:qo.derive_outputs(cls.c,p,cls.rs[p]) for p in cls.c["packages"]}
  cls.m=mn.minimal_packages(cls.c,cls.os); cls.v=vq.verify(cls.c,cls.rs,cls.os,cls.m)
 def test_insufficiency_adjudicates(self):
  r=g.adjudicate(self.c,self.v)
  self.assertEqual(r["verdict"],"TESTED_PRIMITIVES_INSUFFICIENT")
  self.assertEqual(r["successful_packages"],[])
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
