"""v15.51 Task 2 RED: abstract operational realizations."""
from pathlib import Path
import unittest
import primitive_contract as pc
import primitive_realizations as pr
class RealizationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=pc.load_contract(root)
 def test_every_package_has_deterministic_realizations(self):
  for p in self.c["packages"]:
   a=pr.enumerate_realizations(self.c,p); b=pr.enumerate_realizations(self.c,p)
   self.assertEqual(a,b); self.assertGreater(len(a),0)
 def test_all_realizations_obey_package(self):
  for p in self.c["packages"]:
   self.assertTrue(all(pr.check_realization(self.c,p,r)["status"]=="REALIZATION_VALID" for r in pr.enumerate_realizations(self.c,p)))
 def test_classical_controls_remain_visible(self):
  for p in ("P0","P1","P2","P3","P123","P4"):
   rs=pr.enumerate_realizations(self.c,p)
   self.assertTrue(any(r["theory_class"]=="CLASSICAL" for r in rs))
 def test_noncommutative_package_has_explicit_witness(self):
  rs=pr.enumerate_realizations(self.c,"P3")
  self.assertTrue(any(r.get("noncommutative_witness") for r in rs))
 def test_interference_package_has_explicit_witness(self):
  rs=pr.enumerate_realizations(self.c,"P1")
  self.assertTrue(any(r.get("interference_witness") for r in rs))
 def test_hilbert_smuggling_rejected(self):
  r=dict(pr.enumerate_realizations(self.c,"P1")[0]); r["hilbert_space"]="C2"
  self.assertEqual(pr.check_realization(self.c,"P1",r)["status"],"FORBIDDEN_QUANTUM_PRIMITIVE")
 def test_target_dimension_rejected(self):
  r=dict(pr.enumerate_realizations(self.c,"P2")[0]); r["target_dimension"]=32
  self.assertEqual(pr.check_realization(self.c,"P2",r)["status"],"FORBIDDEN_QUANTUM_PRIMITIVE")
if __name__=="__main__": unittest.main()
