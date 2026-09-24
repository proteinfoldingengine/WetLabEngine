"""v15.50 Task 1 RED: target-blind common-ancestor contract."""
from pathlib import Path
import unittest
import common_contract as cc

class CommonContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(__file__).resolve().parents[4]; cls.c=cc.load_contract(cls.root)
 def test_sources_pinned(self):
  self.assertGreaterEqual(len(self.c["sources"]),4)
  self.assertTrue(all(len(v["git_blob_sha"])==40 for v in self.c["sources"].values()))
 def test_u_is_target_blind(self):
  u=self.c["U"]
  self.assertEqual(u["sort"],"ORDERED_RECOVERABILITY_INCIDENCE")
  self.assertFalse(any(k in u for k in ("quantum_labels","hilbert_dimension","node_site_dictionary","geometry")))
 def test_nontrivial_composition_refinement_disjoint(self):
  u=self.c["U"]
  self.assertTrue(u["composition"])
  self.assertNotEqual(u["refinement"]["left_path"],u["refinement"]["right_path"])
  self.assertTrue(u["disjoint_composition"])
 def test_targets_independently_typed(self):
  self.assertEqual(self.c["targets"]["retained"]["sort"],"RETAINED_RECOVERABILITY")
  self.assertEqual(self.c["targets"]["quantum"]["sort"],"QUANTUM_OPERATIONAL_RECOVERABILITY")
 def test_no_legs_supplied(self):
  self.assertIsNone(self.c["legs"]["F_R"]); self.assertIsNone(self.c["legs"]["F_Q"])
 def test_pair_object_forbidden(self):
  self.assertTrue(self.c["forbidden"]["pair_object"])
 def test_downstream_firewall(self):
  self.assertTrue(all(self.c["prohibited_inputs"].values()))
 def test_source_drift_fails_closed(self):
  with self.assertRaisesRegex(ValueError,"source_blob_mismatch"):
   cc.load_contract(self.root,overrides={"carrier_origin":b"drift"})
if __name__=="__main__": unittest.main()
