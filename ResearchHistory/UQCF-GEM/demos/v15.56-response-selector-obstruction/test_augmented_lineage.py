"""v15.56 Task 11 RED: augmented lineage schema sufficiency + minimality."""
import unittest
import augmented_lineage as al
class AugmentedTests(unittest.TestCase):
 def test_augmented_fields(self):
  r=al.classify_augmented()
  self.assertEqual(r["fields"],["genesis_id","parent_address","child_branch_address","repair_index","recoverability_depth"])
 def test_sufficient(self):
  self.assertTrue(al.classify_augmented()["unique_correspondence"])
 def test_child_address_necessary(self):
  r=al.classify_augmented(); self.assertFalse(r["ablation"]["child_branch_address"]["unique"])
 def test_minimality_is_reported_not_assumed(self):
  r=al.classify_augmented(); self.assertIn(r["primary_verdict"],(
   "AUGMENTED_SCHEMA_MINIMAL","AUGMENTED_SCHEMA_SUFFICIENT_NOT_MINIMAL"))
 def test_no_geometry(self):
  self.assertEqual(al.classify_augmented()["geometry_fields"],[])
if __name__=="__main__": unittest.main()
