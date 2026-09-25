"""v15.56 Task 4 RED: exact bridge-space classification contract."""
import unittest
import bridge_space as bs

class BridgeSpaceTests(unittest.TestCase):
 def test_exact_field(self):
  r=bs.classify_bridge_space(); self.assertEqual(r["scalar_field"],"Q")
 def test_source_dimension(self):
  r=bs.classify_bridge_space(); self.assertEqual(r["source_dimension"],4)
 def test_target_not_collapsed_to_single_scalar(self):
  r=bs.classify_bridge_space(); self.assertGreater(r["target_dimension"],1)
 def test_constraints_named(self):
  r=bs.classify_bridge_space()
  self.assertEqual(set(r["constraints_encoded"]),{
   "COVARIANCE","PROVENANCE_PRESERVATION","REDUCTION_CONSISTENCY",
   "COMPOSITION_COMPATIBILITY","NEUTRALITY"})
 def test_reports_dimension(self):
  r=bs.classify_bridge_space(); self.assertIsInstance(r["bridge_space_dimension"],int)
 def test_no_downstream_selection(self):
  self.assertEqual(bs.classify_bridge_space()["forbidden_inputs_used"],[])
if __name__=="__main__": unittest.main()
