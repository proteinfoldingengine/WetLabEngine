"""v15.52 Task 3 RED: explicit obstruction witness."""
from pathlib import Path
import unittest
import obstruction_contract as oc
import source_automorphisms as sa
import obstruction_witness as ow
class WitnessTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=oc.load_contract(root); cls.f=sa.frozen_fixture(cls.c)
  cls.a=sa.enumerate_automorphisms(cls.c,cls.f); cls.w=ow.find_witness(cls.c,cls.f,cls.a)
 def test_witness_found(self):
  self.assertEqual(self.w["status"],"WITNESS_FOUND")
 def test_quantum_outputs_inequivalent(self):
  self.assertNotEqual(self.w["Q1"]["typed_quantum_leg"],self.w["Q2"]["typed_quantum_leg"])
  self.assertFalse(ow.quantum_equivalent(self.c,self.w["Q1"],self.w["Q2"]))
 def test_all_E_observables_equal(self):
  self.assertEqual(self.w["Q1"]["E_observables"],self.w["Q2"]["E_observables"])
  self.assertEqual(set(self.w["E_observables_checked"]),{x["id"] for x in self.c["E"]["observables"]})
 def test_no_forbidden_fields_in_construction(self):
  self.assertTrue(set(self.c["forbidden_fields"]).isdisjoint(set(self.w["construction_inputs"])))
 def test_counterexample_observable_absent_in_frozen_algebra(self):
  self.assertIsNone(ow.find_separating_E_observable(self.c,self.w))
if __name__=="__main__": unittest.main()
