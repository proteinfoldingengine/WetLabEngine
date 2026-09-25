"""v15.56 Task 21 RED: minimal source localization binding record."""
import unittest
import source_binding as sb
class BindingTests(unittest.TestCase):
 def test_fields(self):
  r=sb.classify(); self.assertEqual(r["candidate_fields"],[
   "genesis_id","provenance_root","source_event","full_lineage_address"])
 def test_binding_sufficiency(self):
  self.assertTrue(sb.classify()["sufficient_for_typed_localization"])
 def test_ablation_reported(self):
  self.assertEqual(set(sb.classify()["ablation"]),{
   "genesis_id","provenance_root","source_event","full_lineage_address"})
 def test_no_amplitude(self):
  self.assertFalse(sb.classify()["amplitude_earned"])
 def test_no_geometry(self):
  self.assertEqual(sb.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
