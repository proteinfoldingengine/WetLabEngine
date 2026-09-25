"""v15.56 Task 10 RED: minimal lineage-history sufficiency theorem toy."""
import unittest
import lineage_schema as ls
class SchemaTests(unittest.TestCase):
 def test_fields_minimal(self):
  r=ls.classify_schema()
  self.assertEqual(r["fields"],["genesis_id","parent_address","repair_index","recoverability_depth"])
 def test_unique_addresses(self):
  self.assertTrue(ls.classify_schema()["address_uniqueness_required"])
 def test_sufficiency_question(self):
  self.assertIn(ls.classify_schema()["primary_verdict"],(
   "SCHEMA_SUFFICIENT_FOR_UNIQUE_CORRESPONDENCE",
   "SCHEMA_INSUFFICIENT_FOR_UNIQUE_CORRESPONDENCE"))
 def test_adversarial_controls(self):
  r=ls.classify_schema()
  self.assertEqual(set(r["controls"]),{
   "SIBLING_SWAP","DUPLICATE_DEPTH","REPAIR_REORDER","GENESIS_MISMATCH"})
 def test_no_geometry(self):
  self.assertEqual(ls.classify_schema()["geometry_fields"],[])
if __name__=="__main__": unittest.main()
