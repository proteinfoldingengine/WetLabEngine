"""v15.56 Task 12 RED: identity-key induced correspondence typing."""
import unittest
import identity_correspondence as ic
class IdentityCorrespondenceTests(unittest.TestCase):
 def test_key(self):
  self.assertEqual(ic.classify()["identity_key"],["genesis_id","child_branch_address"])
 def test_partial_not_total(self):
  r=ic.classify(); self.assertEqual(r["correspondence_kind"],"PARTIAL_BIJECTION_ON_SHARED_KEYS")
 def test_no_forced_match(self):
  self.assertTrue(ic.classify()["unmatched_descendants_preserved"])
 def test_induced_scalar_map_requires_field_attachment(self):
  r=ic.classify(); self.assertFalse(r["scalar_map_earned"])
  self.assertIn("SCALAR_VALUE_TO_LINEAGE_KEY_ATTACHMENT",r["missing_for_scalar_map"])
 def test_no_geometry(self):
  self.assertEqual(ic.classify()["geometry_used"],[])
if __name__=="__main__": unittest.main()
