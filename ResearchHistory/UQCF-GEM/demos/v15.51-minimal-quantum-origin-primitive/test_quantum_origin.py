"""v15.51 Task 3 RED: quantum-origin output classification."""
from pathlib import Path
import unittest
import primitive_contract as pc
import primitive_realizations as pr
import quantum_origin as qo
class QuantumOriginTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=pc.load_contract(root)
 def test_all_packages_classified(self):
  for p in self.c["packages"]:
   r=qo.derive_outputs(self.c,p,pr.enumerate_realizations(self.c,p))
   self.assertIn(r["status"],("INSUFFICIENT","SUFFICIENT_NONUNIQUE","SUFFICIENT_UNIQUE"))
 def test_classical_alternative_blocks_unique_quantum_origin(self):
  for p in self.c["packages"]:
   r=qo.derive_outputs(self.c,p,pr.enumerate_realizations(self.c,p))
   if r["classical_realization_present"]:
    self.assertNotEqual(r["status"],"SUFFICIENT_UNIQUE")
 def test_weak_packages_do_not_derive_all_outputs(self):
  for p in ("P0","P1","P2","P3"):
   r=qo.derive_outputs(self.c,p,pr.enumerate_realizations(self.c,p))
   self.assertEqual(r["status"],"INSUFFICIENT")
   self.assertTrue(r["missing_outputs"])
 def test_strongest_package_still_not_unique(self):
  r=qo.derive_outputs(self.c,"P4",pr.enumerate_realizations(self.c,"P4"))
  self.assertNotEqual(r["status"],"SUFFICIENT_UNIQUE")
 def test_no_target_dimension_in_output(self):
  for p in self.c["packages"]:
   r=qo.derive_outputs(self.c,p,pr.enumerate_realizations(self.c,p))
   self.assertNotIn("target_dimension",r)
if __name__=="__main__": unittest.main()
