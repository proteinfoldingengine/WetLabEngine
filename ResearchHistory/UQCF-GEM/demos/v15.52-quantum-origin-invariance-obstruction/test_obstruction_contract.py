"""v15.52 Task 1 RED: obstruction theorem contract."""
from pathlib import Path
import unittest
import obstruction_contract as oc
class ContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(__file__).resolve().parents[4]; cls.c=oc.load_contract(cls.root)
 def test_sources_pinned(self):
  self.assertGreaterEqual(len(self.c["sources"]),3)
  self.assertTrue(all(len(v["git_blob_sha"])==40 for v in self.c["sources"].values()))
 def test_E_whitelist_explicit(self):
  self.assertEqual(set(self.c["E"]["allowed_fields"]),{"objects","lineage","dependency","recoverability","composition","refinement","disjoint_composition"})
 def test_observable_algebra_explicit(self):
  self.assertGreater(len(self.c["E"]["observables"]),0)
  self.assertTrue(all(x["source_definable"] for x in self.c["E"]["observables"]))
 def test_theorems_frozen(self):
  self.assertEqual(set(self.c["theorems"]),{"T1_INVARIANCE_OBSTRUCTION","T2_REPRESENTATION_ORIGIN_COROLLARY","T3_NECESSARY_NEW_DATUM"})
 def test_no_earned_quantum_collapse(self):
  self.assertEqual(self.c["quantum_equivalence"],"IDENTITY_ONLY")
 def test_forbidden_and_downstream_firewall(self):
  self.assertIn("target_dimension",self.c["forbidden_fields"])
  self.assertIn("matrix_algebra",self.c["forbidden_fields"])
  self.assertTrue(all(self.c["prohibited_inputs"].values()))
 def test_source_drift_fails_closed(self):
  with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
   oc.load_contract(self.root,overrides={"v1551_result":b"drift"})
if __name__=="__main__": unittest.main()
