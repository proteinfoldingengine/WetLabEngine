"""v15.56 Task 3 RED: classify the missing bridge-map type."""
import unittest
import bridge_type as bt

class BridgeTypeTests(unittest.TestCase):
 def test_domains_explicit(self):
  r=bt.classify_bridge_type()
  self.assertEqual(r["source_space"],"V1555_RESPONSE_Q4")
  self.assertEqual(r["target_space"],"V1545_RETAINED_SCALAR_FIELD")
 def test_no_map_invented(self):
  r=bt.classify_bridge_type(); self.assertIsNone(r["bridge_map"])
 def test_required_properties(self):
  r=bt.classify_bridge_type()
  self.assertEqual(set(r["required_properties"]),{
   "COVARIANCE","PROVENANCE_PRESERVATION","REDUCTION_CONSISTENCY",
   "COMPOSITION_COMPATIBILITY","NEUTRALITY"})
 def test_obstruction_named(self):
  r=bt.classify_bridge_type()
  self.assertEqual(r["primary_verdict"],"MISSING_CANONICAL_BRIDGE_MAP")
 def test_no_downstream_fit(self):
  self.assertEqual(bt.classify_bridge_type()["forbidden_inputs_used"],[])
if __name__=="__main__": unittest.main()
