"""v15.50 Task 3 RED: independent retained/quantum legs."""
from pathlib import Path
import unittest
import common_contract as cc
import common_candidates as ca
import common_factorizations as cf

class CommonFactorizationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  root=Path(__file__).resolve().parents[4]; cls.c=cc.load_contract(root); cls.u=ca.enumerate_candidates(cls.c)[0]
 def test_retained_leg_is_derivable(self):
  r=cf.derive_retained_leg(self.c,self.u)
  self.assertEqual(r["status"],"RETAINED_LEG_DERIVED")
  self.assertFalse(r["uses_quantum_target"])
 def test_quantum_leg_requires_extra_information(self):
  q=cf.derive_quantum_legs(self.c,self.u)
  self.assertEqual(q["status"],"QUANTUM_LEG_UNDERDETERMINED")
  self.assertEqual(q["lawful_legs"],[])
  self.assertIn("quantum_subsystem_structure",q["missing_information"])
 def test_no_lookup_repair(self):
  q=cf.derive_quantum_legs(self.c,self.u)
  self.assertFalse(q["lookup_table_used"])
 def test_classification_is_insufficient(self):
  fr=cf.derive_retained_leg(self.c,self.u); fq=cf.derive_quantum_legs(self.c,self.u)
  r=cf.classify_factorizations(self.c,self.u,fr,fq)
  self.assertEqual(r["status"],"COMMON_ANCESTOR_INSUFFICIENT_EVIDENCE")
  self.assertEqual(r["reason"],"U_DOES_NOT_ORIGINATE_QUANTUM_LEG")
if __name__=="__main__": unittest.main()
