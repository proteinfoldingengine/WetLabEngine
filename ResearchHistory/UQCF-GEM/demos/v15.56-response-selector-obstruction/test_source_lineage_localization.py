"""v15.56 Task 18 RED: audit source-event -> retained-lineage localization."""
import unittest
import source_lineage_localization as sl
class LocalizationTests(unittest.TestCase):
 def test_historical_evidence(self):
  r=sl.audit(); self.assertGreater(len(r["evidence_paths"]),0)
 def test_separate_localization_from_amplitude(self):
  r=sl.audit(); self.assertIn(r["localization_verdict"],(
   "SOURCE_LINEAGE_IDENTITY_EARNED","SOURCE_ORIGIN_ONLY_NOT_FULL_LINEAGE_KEY",
   "NO_SOURCE_LINEAGE_ATTACHMENT"))
  self.assertFalse(r["amplitude_rule_earned"])
 def test_required_key(self):
  self.assertEqual(sl.audit()["target_identity_key"],["genesis_id","child_branch_address"])
 def test_no_geometry(self):
  self.assertEqual(sl.audit()["geometry_used"],[])
if __name__=="__main__": unittest.main()
