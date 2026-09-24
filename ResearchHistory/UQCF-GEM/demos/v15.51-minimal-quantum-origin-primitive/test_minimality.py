"""v15.51 Task 4 RED: minimality and independent verification."""
from pathlib import Path
import copy, unittest
import primitive_contract as pc
import primitive_realizations as pr
import quantum_origin as qo
import minimality as mn
import verify_quantum_origin as vq
class MinimalityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=pc.load_contract(root)
  cls.rs={p:pr.enumerate_realizations(cls.c,p) for p in cls.c["packages"]}
  cls.os={p:qo.derive_outputs(cls.c,p,cls.rs[p]) for p in cls.c["packages"]}
 def test_no_minimal_successful_package(self):
  r=mn.minimal_packages(self.c,self.os)
  self.assertEqual(r["minimal_successful_packages"],[])
  self.assertEqual(set(r["insufficient_packages"]),set(self.c["packages"]))
 def test_independent_verifier_confirms_insufficiency(self):
  m=mn.minimal_packages(self.c,self.os); r=vq.verify(self.c,self.rs,self.os,m)
  self.assertEqual(r["status"],"VERIFIED_TESTED_PRIMITIVES_INSUFFICIENT")
  self.assertEqual(r["successful_packages"],[])
 def test_hidden_matrix_rejected(self):
  rs=copy.deepcopy(self.rs); rs["P1"]=list(rs["P1"]); rs["P1"][0]=dict(rs["P1"][0]); rs["P1"][0]["matrix_algebra"]="M2"
  with self.assertRaisesRegex(ValueError,"forbidden_quantum_primitive"): vq.verify(self.c,rs,self.os,mn.minimal_packages(self.c,self.os))
 def test_classical_relabel_rejected(self):
  rs=copy.deepcopy(self.rs); rs["P0"]=list(rs["P0"]); rs["P0"][0]=dict(rs["P0"][0]); rs["P0"][0]["theory_class"]="QUANTUM"
  with self.assertRaisesRegex(ValueError,"realization_ledger"): vq.verify(self.c,rs,self.os,mn.minimal_packages(self.c,self.os))
if __name__=="__main__": unittest.main()
